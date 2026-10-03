#!/usr/bin/env python3
"""Paired attribute audit in CompilerGym's actual LLVM 10 execution path.

Unlike baseline_audit.py this uses canonical environment inputs, the service's
own -Oz implementation, and service actions (not opt CLI pass sequences).
Run in the cgym container; see results/baseline_audit/llvm10_canonical/README.md.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

import compiler_gym
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
LLVM = Path.home() / ".local/share/compiler_gym/llvm-v0/bin"
SCHEMA = 1


def command(args, **kwargs):
    p = subprocess.run([str(x) for x in args], capture_output=True, text=True,
                       timeout=120, **kwargs)
    if p.returncode:
        raise RuntimeError(f"{args[0]} failed ({p.returncode}): {p.stderr[-1500:]}")
    return p.stdout


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


def function_args_end(line):
    """Find end of the argument list in an llvm-dis definition header."""
    match = re.search(r'@(?:"(?:[^"\\]|\\.)*"|[^\s(]+)\(', line)
    if not match:
        raise ValueError(f"Unsupported definition header: {line[:150]}")
    depth, quoted, escaped = 1, False, False
    for pos in range(match.end(), len(line)):
        ch = line[pos]
        if escaped:
            escaped = False
        elif quoted and ch == "\\":
            escaped = True
        elif ch == '"':
            quoted = not quoted
        elif not quoted:
            depth += (ch == "(") - (ch == ")")
            if depth == 0:
                return pos + 1
    raise ValueError("Unclosed function arguments")


def add_attributes(src, dst):
    # Add inline function attributes. Do not modify shared groups: those can
    # also be used by declarations/call sites. Group-less definitions work too.
    lines = command([LLVM / "llvm-dis", src, "-o", "-"]).splitlines()
    n = 0
    for i, line in enumerate(lines):
        if line.startswith("define "):
            at = function_args_end(line)
            # LLVM's grammar places these markers before function attributes.
            prefix = re.match(r"(?:\s+(?:local_unnamed_addr|unnamed_addr))?(?:\s+addrspace\(\d+\))?", line[at:])
            at += prefix.end()
            lines[i] = line[:at] + " minsize optsize" + line[at:]
            n += 1
    command([LLVM / "llvm-as", "-o", dst], input="\n".join(lines) + "\n")
    command([LLVM / "opt", "-verify", dst, "-disable-output"])
    out = command([LLVM / "llvm-dis", dst, "-o", "-"])
    groups = dict(re.findall(r"^attributes #(\d+) = \{(.*)\}$", out, re.M))
    verified = 0
    for line in out.splitlines():
        if line.startswith("define "):
            suffix = line[function_args_end(line):]
            attrs = suffix + " " + " ".join(groups[g] for g in re.findall(r"#(\d+)", suffix))
            if not all(re.search(rf"\b{x}\b", attrs) for x in ("minsize", "optsize")):
                raise AssertionError(f"Unannotated definition: {line}")
            verified += 1
    assert verified == n, (verified, n)
    return {"definitions": n, "verified_size_definitions": verified}


def ic(path):
    return int(command(["ic", path]).strip())


def ir_digest(path):
    # Bitcode serialization can differ after llvm-as/service reserialization.
    # Compare the complete disassembled IR, except its path-derived comment.
    ll = command([LLVM / "llvm-dis", path, "-o", "-"])
    ll = re.sub(r"^; ModuleID = .*\n", "", ll, count=1)
    return hashlib.sha256(ll.encode()).hexdigest()


def measure(path, wd, expected_ic=None):
    count = ic(path)
    if expected_ic is not None and count != expected_ic:
        raise AssertionError(f"Export IC {count} != environment IC {expected_ic}")
    obj = Path(wd) / "measurement.o"
    command([LLVM / "llc", "-filetype=obj", path, "-o", obj])
    berk = int(command([LLVM / "llvm-size", obj]).splitlines()[1].split()[0])
    code = 0
    sections = {}
    for line in command([LLVM / "llvm-size", "-A", obj]).splitlines():
        p = line.split()
        if len(p) >= 2 and (p[0] in (".text", "__text") or p[0].startswith(".text.")):
            sections[p[0]] = int(p[1])
            code += int(p[1])
    if not sections:
        raise AssertionError("No recognized code section; refusing silent zero")
    return {"ic": count, "text": berk, "text_sec": code,
            "bitcode_sha256": digest(path), "object_sha256": digest(obj)}


def export_measure(env, path, wd):
    env.write_bitcode(str(path))
    return measure(path, wd, int(env.observation["IrInstructionCount"]))


def select(entries):
    valid = [(i, e) for i, e in enumerate(entries) if e.get("ok")]
    if not valid:
        return None
    result = {"n_ok": len(valid), "n_fail": len(entries) - len(valid)}
    for metric in ("ic", "text", "text_sec"):
        i, e = min(valid, key=lambda pair: (pair[1][metric], pair[0]))
        result[f"by_{metric}"] = {"index": i, **e}
    return result


def one(task):
    source, cfg = task
    uri = source["uri"]
    rec = {"uri": uri, "suite": uri.split("/")[2],
           "paper_reference": source, "fingerprint": cfg["fingerprint"]}
    start = time.monotonic()
    seed = int.from_bytes(hashlib.sha256(f'{cfg["seed"]}:{uri}'.encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    random = rng.choice(cfg["action_ids"], size=(cfg["k"], cfg["steps"])).tolist()
    rec["random_actions"] = random
    try:
        with tempfile.TemporaryDirectory(prefix="cgym-canonical-") as temp, compiler_gym.make("llvm-v0") as env:
            wd = Path(temp)
            for action, name in cfg["pass_names"].items():
                assert env.action_space.flags[int(action)] == name, (action, name)
            env.reset(benchmark=uri)
            original = {"o0": int(env.observation["IrInstructionCount"]),
                        "oz": int(env.observation["IrInstructionCountOz"])}
            rec["original_environment"] = original
            for key in ("o0", "oz"):
                if key in source:
                    assert original[key] == source[key], (uri, key, original[key], source[key])
            plain = wd / "plain-export.bc"
            env.write_bitcode(str(plain))
            assert ic(plain) == original["o0"]
            attr = wd / "attr-export.bc"
            rec["attribute_info"] = add_attributes(plain, attr)
            for variant, initial in (("plain", plain), ("attr", attr)):
                # Content-specific URI prevents CompilerGym's URI cache from
                # returning an earlier module after a file has been overwritten.
                src = wd / f"input-{digest(initial)}.bc"
                initial.rename(src)
                variant_uri = src.as_uri()
                env.reset(benchmark=variant_uri)
                d = rec[variant] = {"input_sha256": digest(src)}
                loaded = wd / f"{variant}-loaded.bc"
                env.write_bitcode(str(loaded))
                d["loaded_sha256"] = digest(loaded)
                d["ir_sha256"] = ir_digest(src)
                assert ir_digest(loaded) == d["ir_sha256"], "Input IR changed on file URI load"
                d["o0_ic"] = int(env.observation["IrInstructionCount"])
                assert d["o0_ic"] == original["o0"], "Attributes changed input IC"
                oz_ic = int(env.observation["IrInstructionCountOz"])
                if variant == "plain":
                    assert oz_ic == original["oz"]
                env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                d["oz"] = export_measure(env, wd / f"{variant}-oz.bc", wd)
                assert d["oz"]["ic"] == oz_ic, "Applied service -Oz differs from observation"
                # opt CLI is diagnostic only; never the main reference.
                cli = wd / f"{variant}-cli-oz.bc"
                command([LLVM / "opt", "-Oz", src, "-o", cli])
                d["cli_oz_diagnostic"] = measure(cli, wd)
                for method, sequences in (("portfolio", cfg["portfolio"]), ("random", random)):
                    entries = d[method] = []
                    for i, sequence in enumerate(sequences):
                        try:
                            env.reset(benchmark=variant_uri)
                            _, _, done, info = env.multistep(sequence, timeout=120)
                            if done:
                                raise RuntimeError(f"Environment ended early: {info}")
                            entries.append({"ok": True, **export_measure(env, wd / "candidate.bc", wd)})
                        except Exception as e:
                            entries.append({"ok": False, "error": repr(e)[:1500]})
                    d[method + "_best"] = select(entries)
                    if variant == "plain" and method == "portfolio" and "portfolio_ics" in source:
                        observed = [e.get("ic") for e in entries]
                        assert observed == source["portfolio_ics"], ("Portfolio reproduction", observed, source["portfolio_ics"])
    except Exception as e:
        rec["failed"] = repr(e)[:1500]
    rec["seconds"] = round(time.monotonic() - start, 3)
    return rec


def summary(records, k):
    # Strict common set: every intended candidate in both conditions succeeds.
    # A failure cannot improve best-of-K by changing the attempted budget.
    common = [r for r in records if "failed" not in r and all(
        len(r.get(v, {}).get(m, [])) == k and all(e.get("ok") for e in r[v][m])
        for v in ("plain", "attr") for m in ("portfolio", "random"))]
    out = {"attempted": len(records), "complete_paired": len(common),
           "excluded": [{"uri": r["uri"], "error": r.get("failed", "candidate failure")}
                        for r in records if r not in common],
           "candidate_failures": sum(not e.get("ok") for r in records
                                     for v in ("plain", "attr") for m in ("portfolio", "random")
                                     for e in r.get(v, {}).get(m, []))}
    for v in ("plain", "attr"):
        out[v] = {}
        for method in ("portfolio", "random"):
            out[v][method] = {}
            for metric in ("ic", "text", "text_sec"):
                base = [r[v]["oz"][metric] for r in common]
                candidate = [r[v][method + "_best"]["by_ic"][metric] for r in common]
                b, c = sum(base), sum(candidate)
                out[v][method][metric] = {"baseline_sum": b, "candidate_sum": c,
                    "gain_pct": 100 * (1 - c / b) if b else None,
                    "wins": sum(x < y for x, y in zip(candidate, base)),
                    "ties": sum(x == y for x, y in zip(candidate, base)),
                    "losses": sum(x > y for x, y in zip(candidate, base))}
    return out


def self_test():
    fixture = '''target triple = "x86_64-unknown-linux-gnu"
declare void @callee() #0
define void @grouped() #0 {
  call void @callee() #0
  ret void
}
define void @ungrouped(void ()* %f) local_unnamed_addr {
  call void %f()
  ret void
}
attributes #0 = { nounwind }
'''
    with tempfile.TemporaryDirectory() as temp:
        wd = Path(temp)
        src, dst = wd / "source.bc", wd / "attr.bc"
        command([LLVM / "llvm-as", "-o", src], input=fixture)
        assert add_attributes(src, dst)["verified_size_definitions"] == 2
        assert ic(src) == ic(dst)
        ll = command([LLVM / "llvm-dis", dst, "-o", "-"])
        assert "attributes #0 = { nounwind }" in ll
        assert "declare void @callee() #0" in ll
        assert "call void @callee() #0" in ll
        # Directly test the same cache-safe loading used by the campaign.
        with compiler_gym.make("llvm-v0") as env:
            seen = []
            for uri in ("benchmark://npb-v0/116", "benchmark://npb-v0/117"):
                env.reset(benchmark=uri)
                count = int(env.observation["IrInstructionCount"])
                env.write_bitcode(str(src))
                unique = wd / f"input-{digest(src)}.bc"
                unique.write_bytes(src.read_bytes())
                env.reset(benchmark=unique.as_uri())
                assert int(env.observation["IrInstructionCount"]) == count
                seen.append(count)
            assert seen == [5075, 2166], seen
            # Batched actions must match the original step-by-step semantics.
            actions = json.loads((ROOT / "results/portfolio_selection.json").read_text())["portfolio"][0]["actions"]
            env.reset(benchmark="benchmark://npb-v0/116")
            env.multistep(actions)
            env.write_bitcode(str(src))
            env.reset(benchmark="benchmark://npb-v0/116")
            for action in actions:
                _, _, done, info = env.step(action)
                assert not done, info
            env.write_bitcode(str(dst))
            assert digest(src) == digest(dst), "multistep differs from step"
    print("PASS: attributes on grouped/ungrouped definitions; declaration/call-site preservation; input identity; multistep equivalence", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--suite", action="append", default=[])
    p.add_argument("--uri", action="append", default=[])
    p.add_argument("--out", type=Path, default=ROOT / "results/baseline_audit/llvm10_canonical")
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=45)
    p.add_argument("--max-ic", type=int, default=6000)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.suite and not args.uri:
        p.error("Supply --suite (original battery membership) or --uri")
    names = {x["action_id"]: x["name"] for x in yaml.safe_load((ROOT / "configs/passes.yaml").read_text())["passes"]}
    portfolio = [x["actions"] for x in json.loads((ROOT / "results/portfolio_selection.json").read_text())["portfolio"][:args.k]]
    assert len(portfolio) == args.k and all(a in names for seq in portfolio for a in seq)
    sources, excluded_cap = {}, []
    for suite in args.suite:
        files = sorted((ROOT / "results/battery" / suite).glob("*.json"))
        if not files:
            p.error(f"No original battery files for {suite}")
        for path in files:
            rec = json.loads(path.read_text())
            if "uri" in rec:
                if rec["o0"] > args.max_ic:
                    excluded_cap.append({"uri": rec["uri"], "o0": rec["o0"]})
                    continue
                sources[rec["uri"]] = {"uri": rec["uri"], "o0": rec["o0"], "oz": rec["oz"],
                                      "file": str(path.relative_to(ROOT)), "sha256": digest(path)}
                prior = ROOT / "results/portfolio_eval" / suite / "portfolio_seed0" / path.name
                if prior.exists():
                    sources[rec["uri"]]["portfolio_ics"] = json.loads(prior.read_text())["sample_ics"][:args.k]
                    sources[rec["uri"]]["portfolio_reference_sha256"] = digest(prior)
    for uri in args.uri:
        sources.setdefault(uri, {"uri": uri})
    cfg = {"schema": SCHEMA, "script_sha256": digest(__file__), "k": args.k,
           "seed": args.seed, "steps": args.steps, "portfolio": portfolio,
           "pass_names": names, "action_ids": sorted(names), "compiler_gym": compiler_gym.__version__,
           "llvm_version": command([LLVM / "opt", "--version"]).strip(),
           "ic_tool_sha256": digest(command(["which", "ic"]).strip()),
           "numpy_version": np.__version__, "selection": "minimum IC; first candidate breaks ties",
           "baseline": "service llvm.apply_baseline_optimizations=-Oz",
           "codegen": "bundled llc defaults, original per-module triple and datalayout",
           "sources": sources, "max_ic": args.max_ic, "excluded_above_cap": excluded_cap}
    cfg["fingerprint"] = hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()
    args.out.mkdir(parents=True, exist_ok=True)
    lock = (args.out / ".run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Another process is writing this output directory")
    manifest = args.out / "manifest.json"
    if manifest.exists():
        assert json.loads(manifest.read_text())["fingerprint"] == cfg["fingerprint"], "Different protocol or source files: choose a new output directory"
    atomic_json(manifest, cfg)
    records, pending = [], []
    for uri, source in sorted(sources.items()):
        key = hashlib.sha256(uri.encode()).hexdigest()
        path = args.out / "records" / f"{key}.json"
        if path.exists():
            rec = json.loads(path.read_text())
            assert rec["fingerprint"] == cfg["fingerprint"] and rec["uri"] == uri
            records.append(rec)
        else:
            pending.append((source, path))
    print(f"{len(sources)} modules; {len(records)} resumed; {len(pending)} pending", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(one, (source, cfg)): path for source, path in pending}
        for future in as_completed(futures):
            rec = future.result()
            atomic_json(futures[future], rec)
            records.append(rec)
            print(f'{len(records)}/{len(sources)} {rec["uri"]}: {rec.get("failed", "completed")} ({rec["seconds"]}s)', flush=True)
    records.sort(key=lambda r: r["uri"])
    suites = sorted({r["suite"] for r in records})
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "fingerprint": cfg["fingerprint"],
              "summary": summary(records, args.k),
              "suites": {s: summary([r for r in records if r["suite"] == s], args.k) for s in suites}}
    atomic_json(args.out / "summary.json", report)
    print(json.dumps(report, indent=2), flush=True)
    if report["summary"]["complete_paired"] != len(sources):
        raise SystemExit("Incomplete matrix: inspect recorded failures")


if __name__ == "__main__":
    main()

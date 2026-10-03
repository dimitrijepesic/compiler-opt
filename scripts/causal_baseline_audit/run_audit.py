#!/usr/bin/env python3
"""Causal baseline audit: unrolling vs size attributes in the CompilerGym 0.2.5 -Oz reference.

Reference cells only (no portfolio / GNN search). Per program and per input
variant (plain, attr) the script records:

  service_original   ORIGINAL service, llvm.apply_baseline_optimizations=-Oz
  service_marked     ORIGINAL service on the same input with
                     !llvm.loop {llvm.loop.unroll.disable} on every natural loop
                     (input-level intervention; the pipeline is untouched)
  replica_service / replica_service_marked
                     helper program replica_oz (same LLVM 10.0.0 release
                     libraries, service code copied verbatim); must reproduce
                     the two service cells IR-for-IR before anything else from
                     the replica is interpreted
  replica_disable_unroll   replica with PassManagerBuilder::DisableUnrollLoops
  replica_threshold0       replica with -unroll-threshold=0

plus a separate code generation control on fixed optimized IR. See
results/causal_baseline_audit/PROTOCOL.md. Run inside the `causal-audit`
container (image cgym-causal:0.2.5):

  python scripts/causal_baseline_audit/run_audit.py prepare
  python scripts/causal_baseline_audit/run_audit.py run --stage pilot --workers 2
  python scripts/causal_baseline_audit/run_audit.py gate
  python scripts/causal_baseline_audit/run_audit.py run --stage campaign --workers 4
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import compiler_gym  # noqa: E402
from baseline_audit_cgym_matrix import LLVM, add_attributes, atomic_json, command, digest, ic, measure  # noqa: E402

SCHEMA = 1
OUT = ROOT / "results/causal_baseline_audit"
CANON = ROOT / "results/baseline_audit/llvm10_canonical"
CANON_FINGERPRINT = "8db1604d49185a07ab80c58560d0608434f33c04a78e38931e5a924e6d52b539"
PILOT = ["benchmark://npb-v0/116", "benchmark://npb-v0/94", "benchmark://npb-v0/96", "benchmark://blas-v0/25"]
REPLICA = Path("/usr/local/bin/replica_oz")
SERVICE = Path(compiler_gym.__file__).parent / "envs/llvm/service/compiler_gym-llvm-service"
VARIANTS = ("plain", "attr")
SERVICE_CELLS = ("service_original", "service_marked")
REPLICA_CELLS = {"replica_service": ("input", "--mode=service"),
                 "replica_service_marked": ("marked", "--mode=service"),
                 "replica_disable_unroll": ("input", "--mode=disable-unroll"),
                 "replica_threshold0": ("input", "--mode=unroll-threshold-0")}
METRICS = ("ic", "text", "text_sec")
CONTROLS = ("plain_oz_late_attr", "plain_marked_oz_late_attr", "attr_oz_stripped")


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def key(uri):
    return sha(uri)


def dis(path):
    ll = command([LLVM / "llvm-dis", path, "-o", "-"])
    return re.sub(r"^; ModuleID = .*\n", "", ll, count=1)


def strip_loop_md(ll):
    """Remove !llvm.loop attachments. Every other metadata reference (the BLAS
    inputs carry TBAA) is replaced by a hash of the node's expanded content, so
    the result does not depend on how the nodes happen to be numbered."""
    lines = ll.splitlines()
    defs = dict(m.groups() for m in (re.match(r"^!(\d+) = (.*)$", l) for l in lines) if m)
    memo = {}

    def canon(n, stack):
        if n in memo:
            return memo[n]
        if n in stack:
            return "cycle"
        if n not in defs:
            return "undefined"
        cyclic = []

        def sub(m):
            r = canon(m.group(1), stack | {n})
            cyclic.append(r == "cycle")
            return "<" + r + ">"
        text = re.sub(r"!(\d+)\b", sub, defs[n])
        if not any(cyclic):
            memo[n] = text
        return text

    out = []
    for line in lines:
        if re.match(r"^!\d+ = ", line):
            continue
        line = re.sub(r", !llvm\.loop !\d+", "", line)
        out.append(re.sub(r"!(\d+)\b", lambda m: "!{" + sha(canon(m.group(1), frozenset()))[:16] + "}", line))
    # The blank separator line before the metadata section goes with it.
    return "\n".join(out).rstrip("\n") + "\n"


def normalize_size_attrs(ll):
    """Expand attribute group references and drop minsize/optsize, so that two
    modules compare equal iff they differ only in those two function attributes."""
    groups = {n: re.sub(r"\b(?:minsize|optsize)\b ?", "", body).strip()
              for n, body in re.findall(r"^attributes #(\d+) = \{(.*)\}$", ll, re.M)}
    out = []
    for line in ll.splitlines():
        # "; Function Attrs:" is a disassembler comment that repeats the group contents.
        if line.startswith("attributes #") or line.startswith("; Function Attrs:"):
            continue
        if line.startswith("define "):
            line = re.sub(r" (?:minsize|optsize)\b", "", line)

        def expand(m):
            g = groups.get(m.group(1))
            if g is None:
                return m.group(0)
            return (" {" + g + "}") if g else ""
        out.append(re.sub(r" #(\d+)\b", expand, line))
    return "\n".join(out).rstrip("\n") + "\n"


def remove_size_attributes(src, dst):
    """Inverse of add_attributes: drop minsize/optsize everywhere; verify none is left."""
    lines = command([LLVM / "llvm-dis", src, "-o", "-"]).splitlines()
    emptied = set()
    for i, line in enumerate(lines):
        if line.startswith("attributes #"):
            n, body = re.match(r"^attributes #(\d+) = \{(.*)\}$", line).groups()
            body = re.sub(r"\b(?:minsize|optsize)\b ?", "", body).strip()
            if body:
                lines[i] = f"attributes #{n} = {{ {body} }}"
            else:  # LLVM rejects empty attribute groups
                emptied.add(n)
                lines[i] = None
        elif line.startswith("define "):
            lines[i] = re.sub(r" (?:minsize|optsize)\b", "", line)
    kept = []
    for line in lines:
        if line is None:
            continue
        if emptied:
            line = re.sub(r" #(\d+)\b", lambda m: "" if m.group(1) in emptied else m.group(0), line)
        kept.append(line)
    command([LLVM / "llvm-as", "-o", dst], input="\n".join(kept) + "\n")
    command([LLVM / "opt", "-verify", dst, "-disable-output"])
    out = command([LLVM / "llvm-dis", dst, "-o", "-"])
    left = [l for l in out.splitlines()
            if (l.startswith("attributes #") or l.startswith("define ")) and re.search(r"\b(?:minsize|optsize)\b", l)]
    if left:
        raise AssertionError(f"size attributes left: {left[:3]}")
    return {"definitions": sum(l.startswith("define ") for l in out.splitlines())}


def count_size_definitions(ll):
    groups = dict(re.findall(r"^attributes #(\d+) = \{(.*)\}$", ll, re.M))
    total = both = 0
    for line in ll.splitlines():
        if line.startswith("define "):
            total += 1
            attrs = line + " " + " ".join(groups.get(g, "") for g in re.findall(r"#(\d+)", line))
            both += all(re.search(rf"\b{x}\b", attrs) for x in ("minsize", "optsize"))
    return {"definitions": total, "with_minsize_optsize": both}


def run_replica(src, dst, *flags):
    p = subprocess.run([str(REPLICA), *flags, str(src), str(dst)], capture_output=True, text=True, timeout=900)
    if p.returncode:
        raise RuntimeError(f"replica_oz failed ({p.returncode}): {p.stderr[-1500:]}")
    return int(p.stdout.strip()), p.stderr


def parse_remarks(stderr):
    by_name, by_function, by_message = {}, {}, {}
    for line in stderr.splitlines():
        if line.startswith("remark\t"):
            _, _, name, function, message = line.split("\t", 4)
            by_name[name] = by_name.get(name, 0) + 1
            by_function[function] = by_function.get(function, 0) + 1
            by_message[message] = by_message.get(message, 0) + 1
    return {"total": sum(by_name.values()), "by_name": by_name, "by_function": by_function, "by_message": by_message}


def full_measure(path, wd, keep_as=None):
    d = measure(path, wd)
    ll = dis(path)
    d["ir_sha256"] = sha(ll)
    d["ir_nometa_sha256"] = sha(strip_loop_md(ll))
    d["ir_nosize_sha256"] = sha(normalize_size_attrs(strip_loop_md(ll)))
    d["loop_attachments"] = len(re.findall(r", !llvm\.loop !\d+", ll))
    d["size_definitions"] = count_size_definitions(ll)
    if keep_as is not None:
        shutil.copyfile(Path(wd) / "measurement.o", keep_as.with_suffix(".o"))
        keep_as.with_suffix(".ll").write_text(ll)
    return d


def one(task):
    uri, ref, cfg, keep = task
    rec = {"schema": SCHEMA, "uri": uri, "suite": uri.split("/")[2], "stage": cfg["stage"],
           "fingerprint": cfg["fingerprint"], "reference": ref, "checks": {}, "soft": {}}
    chk, soft = rec["checks"], rec["soft"]
    start = time.monotonic()
    temp = None
    try:
        if keep:
            wd = Path(keep)
            if wd.exists():
                shutil.rmtree(wd)
            wd.mkdir(parents=True)
        else:
            temp = tempfile.TemporaryDirectory(prefix="causal-audit-")
            wd = Path(temp.name)
        with compiler_gym.make("llvm-v0") as env:
            env.reset(benchmark=uri)
            rec["environment"] = {"o0": int(env.observation["IrInstructionCount"]),
                                  "oz": int(env.observation["IrInstructionCountOz"])}
            chk["environment_matches_reference"] = (rec["environment"]["o0"] == ref["o0"]
                                                    and rec["environment"]["oz"] == ref["oz"])
            inputs = {"plain": wd / "plain.bc", "attr": wd / "attr.bc"}
            env.write_bitcode(str(inputs["plain"]))
            rec["attribute_info"] = add_attributes(inputs["plain"], inputs["attr"])
            rec["inputs"], rec["cells"] = {}, {}
            for v in VARIANTS:
                src = inputs[v]
                src_ll = dis(src)
                marked = wd / f"{v}-marked.bc"
                run_replica(src, marked, "--mark-unroll-disable", f"--stats={wd / (v + '-marked.stats.json')}")
                mstats = json.loads((wd / f"{v}-marked.stats.json").read_text())
                marked_ll = dis(marked)
                rec["inputs"][v] = {"sha256": digest(src), "ir_sha256": sha(src_ll), "ic": ic(src),
                                    "size_definitions": count_size_definitions(src_ll),
                                    "metadata_nodes": len(re.findall(r"^!\d+ = ", src_ll, re.M))}
                rec["inputs"][v + "_marked"] = {"sha256": digest(marked), "ir_sha256": sha(marked_ll), "ic": ic(marked),
                                                "marked_loops": mstats["marked_loops"],
                                                "preexisting_loop_ids": mstats["preexisting_loop_ids"],
                                                "loop_attachments": len(re.findall(r", !llvm\.loop !\d+", marked_ll))}
                chk[f"{v}_input_ir_matches_canonical"] = sha(src_ll) == ref[v]["ir_sha256"]
                soft[f"{v}_input_bitcode_matches_canonical"] = digest(src) == ref[v]["input_sha256"]
                chk[f"{v}_marking_changed_only_loop_metadata"] = strip_loop_md(marked_ll) == strip_loop_md(src_ll)
                chk[f"{v}_input_ic_is_o0"] = rec["inputs"][v]["ic"] == ref["o0"] == rec["inputs"][v + "_marked"]["ic"]
                if keep:
                    (wd / f"{v}.ll").write_text(src_ll)
                    (wd / f"{v}-marked.ll").write_text(marked_ll)

                for cell, inp in zip(SERVICE_CELLS, (src, marked)):
                    # Content-specific URI: CompilerGym caches benchmarks by URI.
                    unique = wd / f"input-{digest(inp)}.bc"
                    shutil.copyfile(inp, unique)
                    env.reset(benchmark=unique.as_uri())
                    loaded = wd / f"{v}-{cell}-loaded.bc"
                    env.write_bitcode(str(loaded))
                    chk[f"{v}/{cell}_load_ir_identical"] = sha(dis(loaded)) == sha(dis(inp))
                    o0_obs = int(env.observation["IrInstructionCount"])
                    oz_obs = int(env.observation["IrInstructionCountOz"])
                    env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                    out = wd / f"{v}-{cell}.bc"
                    env.write_bitcode(str(out))
                    d = rec["cells"][f"{v}/{cell}"] = {"executor": "original service", "input_sha256": digest(inp),
                                                       "observation_o0": o0_obs, "observation_oz": oz_obs,
                                                       **full_measure(out, wd, out if keep else None)}
                    chk[f"{v}/{cell}_export_ic_is_observation"] = d["ic"] == oz_obs and o0_obs == ref["o0"]
                    if not keep:
                        loaded.unlink()

                for cell, (which, mode) in REPLICA_CELLS.items():
                    inp = src if which == "input" else marked
                    out = wd / f"{v}-{cell}.bc"
                    stats = wd / f"{v}-{cell}.stats.json"
                    n, err = run_replica(inp, out, mode, "--remarks", f"--stats={stats}")
                    if keep:
                        (wd / f"{v}-{cell}.remarks.txt").write_text(err)
                    d = rec["cells"][f"{v}/{cell}"] = {"executor": "replica_oz " + mode, "input_sha256": digest(inp),
                                                       "unroll_remarks": parse_remarks(err),
                                                       **full_measure(out, wd, out if keep else None)}
                    assert d["ic"] == n, (d["ic"], n)
                    d["functions"] = {f["name"]: f["ic"] for f in json.loads(stats.read_text())["after"]["functions"]}

                c = rec["cells"]
                for metric in METRICS:
                    chk[f"{v}/service_original_{metric}_matches_canonical"] = \
                        c[f"{v}/service_original"][metric] == ref[v]["oz"][metric]
                for h in ("bitcode_sha256", "object_sha256"):
                    soft[f"{v}/service_original_{h}_matches_canonical"] = \
                        c[f"{v}/service_original"][h] == ref[v]["oz"][h]
                # Replica fidelity: complete disassembled IR, not only the IC.
                for svc, rep in (("service_original", "replica_service"), ("service_marked", "replica_service_marked")):
                    chk[f"{v}/{rep}_reproduces_service_ir"] = c[f"{v}/{rep}"]["ir_sha256"] == c[f"{v}/{svc}"]["ir_sha256"]
                    chk[f"{v}/{rep}_reproduces_service_metrics"] = all(
                        c[f"{v}/{rep}"][m] == c[f"{v}/{svc}"][m] for m in METRICS)
                    soft[f"{v}/{rep}_reproduces_service_bitcode"] = \
                        c[f"{v}/{rep}"]["bitcode_sha256"] == c[f"{v}/{svc}"]["bitcode_sha256"]
                    soft[f"{v}/{rep}_reproduces_service_object"] = \
                        c[f"{v}/{rep}"]["object_sha256"] == c[f"{v}/{svc}"]["object_sha256"]
                # Effectiveness of the interventions: no loop is unrolled at all.
                chk[f"{v}/marked_no_unroll_remarks"] = c[f"{v}/replica_service_marked"]["unroll_remarks"]["total"] == 0
                chk[f"{v}/disable_unroll_no_unroll_remarks"] = c[f"{v}/replica_disable_unroll"]["unroll_remarks"]["total"] == 0
                if v == "plain":  # -unroll-threshold=0 deliberately leaves optsize functions alone
                    chk["plain/threshold0_no_unroll_remarks"] = c["plain/replica_threshold0"]["unroll_remarks"]["total"] == 0
                # Agreement of the three interventions (recorded, not required).
                for other in ("replica_disable_unroll", "replica_threshold0"):
                    soft[f"{v}/{other}_ir_equals_marked_modulo_loop_metadata"] = \
                        c[f"{v}/{other}"]["ir_nometa_sha256"] == c[f"{v}/service_marked"]["ir_nometa_sha256"]
                    soft[f"{v}/{other}_metrics_equal_marked"] = all(
                        c[f"{v}/{other}"][m] == c[f"{v}/service_marked"][m] for m in METRICS)

            # Does disabling unrolling on the plain input give the attr result, up to the attributes?
            c = rec["cells"]
            soft["plain_marked_ir_equals_attr_original_modulo_size_attrs"] = \
                c["plain/service_marked"]["ir_nosize_sha256"] == c["attr/service_original"]["ir_nosize_sha256"]
            soft["plain_marked_ir_equals_attr_marked_modulo_size_attrs"] = \
                c["plain/service_marked"]["ir_nosize_sha256"] == c["attr/service_marked"]["ir_nosize_sha256"]
            soft["attr_marked_ir_equals_attr_original_modulo_loop_metadata"] = \
                c["attr/service_marked"]["ir_nometa_sha256"] == c["attr/service_original"]["ir_nometa_sha256"]

            # Code generation control: fixed optimized IR, attributes changed only before llc.
            rec["codegen_control"] = {}
            for name, base, fn in (("plain_oz_late_attr", "plain/service_original", add_attributes),
                                   ("plain_marked_oz_late_attr", "plain/service_marked", add_attributes),
                                   ("attr_oz_stripped", "attr/service_original", remove_size_attributes)):
                src = wd / (base.replace("/", "-") + ".bc")
                dst = wd / f"control-{name}.bc"
                info = fn(src, dst)
                d = rec["codegen_control"][name] = {"base_cell": base, "info": info,
                                                    **full_measure(dst, wd, dst if keep else None)}
                chk[f"control/{name}_ic_unchanged"] = d["ic"] == c[base]["ic"]
                chk[f"control/{name}_ir_identical_modulo_size_attrs"] = \
                    sha(normalize_size_attrs(dis(src))) == sha(normalize_size_attrs(dis(dst)))
                want = 0 if fn is remove_size_attributes else d["size_definitions"]["definitions"]
                chk[f"control/{name}_attribute_state"] = d["size_definitions"]["with_minsize_optsize"] == want
            chk["attr_original_all_definitions_sized"] = \
                c["attr/service_original"]["size_definitions"]["with_minsize_optsize"] == \
                c["attr/service_original"]["size_definitions"]["definitions"]
            chk["plain_original_no_definition_sized"] = c["plain/service_original"]["size_definitions"]["with_minsize_optsize"] == 0
        rec["complete"] = True
        bad = sorted(k for k, ok in chk.items() if not ok)
        if bad:
            rec["failed"] = "hard checks failed: " + ", ".join(bad)
    except Exception as e:  # keep the failure visible
        rec["failed"] = repr(e)[:2000]
    finally:
        if temp is not None:
            temp.cleanup()
    rec["seconds"] = round(time.monotonic() - start, 3)
    return rec


def expected_check_names():
    names = ["environment_matches_reference", "attr_original_all_definitions_sized", "plain_original_no_definition_sized",
             "plain/threshold0_no_unroll_remarks"]
    for v in VARIANTS:
        names += [f"{v}_input_ir_matches_canonical", f"{v}_marking_changed_only_loop_metadata", f"{v}_input_ic_is_o0",
                  f"{v}/marked_no_unroll_remarks", f"{v}/disable_unroll_no_unroll_remarks"]
        names += [f"{v}/{c}_load_ir_identical" for c in SERVICE_CELLS]
        names += [f"{v}/{c}_export_ic_is_observation" for c in SERVICE_CELLS]
        names += [f"{v}/service_original_{m}_matches_canonical" for m in METRICS]
        for rep in ("replica_service", "replica_service_marked"):
            names += [f"{v}/{rep}_reproduces_service_ir", f"{v}/{rep}_reproduces_service_metrics"]
    for name in CONTROLS:
        names += [f"control/{name}_ic_unchanged", f"control/{name}_ir_identical_modulo_size_attrs",
                  f"control/{name}_attribute_state"]
    return sorted(names)


def record_state(rec, fingerprint, uri):
    """'valid', 'failed' (explicit, kept visible) or 'invalid' (must be rerun)."""
    if not isinstance(rec, dict) or rec.get("fingerprint") != fingerprint or rec.get("uri") != uri \
            or rec.get("schema") != SCHEMA:
        return "invalid"
    if "failed" in rec:
        return "failed"
    if not rec.get("complete") or sorted(rec.get("checks", {})) != expected_check_names() \
            or not all(rec["checks"].values()):
        return "invalid"
    cells = rec.get("cells", {})
    wanted = [f"{v}/{c}" for v in VARIANTS for c in (*SERVICE_CELLS, *REPLICA_CELLS)]
    if sorted(cells) != sorted(wanted) or sorted(rec.get("codegen_control", {})) != sorted(CONTROLS):
        return "invalid"
    for d in (*cells.values(), *rec["codegen_control"].values()):
        if not all(isinstance(d.get(m), int) and d[m] > 0 for m in METRICS):
            return "invalid"
        if not all(isinstance(d.get(h), str) and len(d[h]) == 64 for h in ("bitcode_sha256", "object_sha256", "ir_sha256")):
            return "invalid"
    return "valid"


def prepare(args):
    manifest = json.loads((CANON / "manifest.json").read_text())
    assert manifest["fingerprint"] == CANON_FINGERPRINT, "canonical audit manifest changed"
    sources = manifest["sources"]
    npb = sorted((u for u in sources if u.startswith("benchmark://npb-v0/")), key=lambda u: int(u.rsplit("/", 1)[1]))
    assert len(npb) == 120, len(npb)
    missing = [u for u in PILOT if u not in sources]
    assert not missing, f"pilot programs outside the canonical cohort: {missing}"
    refs = {}
    for uri in sorted(set(npb) | set(PILOT)):
        path = CANON / "records" / f"{key(uri)}.json"
        r = json.loads(path.read_text())
        assert r["uri"] == uri and "failed" not in r and r["fingerprint"] == CANON_FINGERPRINT
        assert r["original_environment"] == {"o0": sources[uri]["o0"], "oz": sources[uri]["oz"]}
        refs[uri] = {"o0": sources[uri]["o0"], "oz": sources[uri]["oz"],
                     "canonical_record": str(path.relative_to(ROOT)), "canonical_record_sha256": digest(path)}
        for v in VARIANTS:
            refs[uri][v] = {"input_sha256": r[v]["input_sha256"], "ir_sha256": r[v]["ir_sha256"],
                            "oz": {k: r[v]["oz"][k] for k in (*METRICS, "bitcode_sha256", "object_sha256")}}
            assert r[v]["o0_ic"] == sources[uri]["o0"]
        assert refs[uri]["plain"]["oz"]["ic"] == sources[uri]["oz"]
    data = {"schema": SCHEMA, "canonical_manifest_sha256": digest(CANON / "manifest.json"),
            "canonical_fingerprint": CANON_FINGERPRINT, "pilot": PILOT, "campaign": npb, "references": refs}
    path = OUT / "inputs.json"
    if path.exists() and json.loads(path.read_text()) != data:
        raise SystemExit("inputs.json exists with different content; refusing to overwrite")
    atomic_json(path, data)
    print(f"inputs.json: {len(PILOT)} pilot, {len(npb)} campaign programs; sha256 {digest(path)}")


def configuration(stage):
    files = {"run_audit.py": Path(__file__), "helper baseline_audit_cgym_matrix.py": ROOT / "scripts/baseline_audit_cgym_matrix.py",
             "replica_oz.cpp": HERE / "replica_oz.cpp", "Dockerfile": HERE / "Dockerfile", "build_image.sh": HERE / "build_image.sh",
             "replica_oz": REPLICA, "ic": Path(command(["which", "ic"]).strip()), "service": SERVICE,
             "inputs.json": OUT / "inputs.json", "PROTOCOL.md": OUT / "PROTOCOL.md",
             "environment_host.json": OUT / "environment_host.json",
             "canonical manifest": CANON / "manifest.json"}
    for tool in ("opt", "llc", "llvm-size", "llvm-dis", "llvm-as", "clang"):
        files["llvm-v0/bin/" + tool] = (LLVM / tool).resolve()
    assert (HERE / "replica_oz.cpp").read_bytes() == Path("/opt/replica_oz.cpp").read_bytes(), \
        "replica_oz.cpp differs from the source the image was built from"
    cfg = {"schema": SCHEMA, "stage": stage, "sha256": {k: digest(p) for k, p in files.items()},
           "paths": {k: str(p) for k, p in files.items()},
           "compiler_gym": compiler_gym.__version__,
           "bundled_llvm": command([LLVM / "opt", "--version"]).strip(),
           "replica_llvm": command(["/opt/llvm10/bin/llvm-config", "--version"]).strip(),
           "python": sys.version.split()[0],
           "cells": {"service": list(SERVICE_CELLS), "replica": {k: list(v) for k, v in REPLICA_CELLS.items()}},
           "primary_no_unroll_cell": "service_marked",
           "commands": {"service_oz": 'env.reset(benchmark=file URI); env.send_param("llvm.apply_baseline_optimizations", "-Oz"); env.write_bitcode(out)',
                        "mark": "replica_oz --mark-unroll-disable in.bc marked.bc",
                        "replica": "replica_oz <mode> --remarks --stats=stats.json in.bc out.bc",
                        "object": "llc -filetype=obj in.bc -o measurement.o",
                        "berkeley_text": "llvm-size measurement.o (first column)",
                        "code_bytes": "llvm-size -A measurement.o, sum of .text, .text.* or __text",
                        "ic": "ic in.bc (scripts/baseline_audit/ic.cpp, Module::getInstructionCount)"}}
    cfg["fingerprint"] = sha(json.dumps(cfg, sort_keys=True))
    return cfg


def gate_status(cfg_pilot_fingerprint):
    inputs = json.loads((OUT / "inputs.json").read_text())
    states = {}
    for uri in inputs["pilot"]:
        path = OUT / "pilot/records" / f"{key(uri)}.json"
        states[uri] = record_state(json.loads(path.read_text()), cfg_pilot_fingerprint, uri) if path.exists() else "missing"
    return {"passed": all(s == "valid" for s in states.values()), "states": states,
            "pilot_fingerprint": cfg_pilot_fingerprint, "required_checks": expected_check_names()}


def gate(args):
    status = gate_status(configuration("pilot")["fingerprint"])
    status["timestamp"] = datetime.now(timezone.utc).isoformat()
    atomic_json(OUT / "pilot/GATE.json", status)
    print(json.dumps(status["states"], indent=1), "\nPILOT GATE:", "PASSED" if status["passed"] else "NOT PASSED")
    if not status["passed"]:
        raise SystemExit(1)


def run(args):
    inputs = json.loads((OUT / "inputs.json").read_text())
    cfg = configuration(args.stage)
    if args.stage == "campaign":
        # Recomputed from the pilot records and the current files, not read from GATE.json.
        status = gate_status(configuration("pilot")["fingerprint"])
        if not status["passed"]:
            raise SystemExit(f"pilot gate not passed under the current files: {status['states']}")
    out = OUT / args.stage
    (out / "records").mkdir(parents=True, exist_ok=True)
    lock = (out / ".run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("another process is writing this stage")
    manifest = out / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text())["fingerprint"] != cfg["fingerprint"]:
        raise SystemExit("protocol, scripts, tools or inputs changed since this stage started: "
                         "move the old stage directory aside instead of resuming it")
    atomic_json(manifest, cfg)
    uris = inputs[args.stage]
    done, pending = {}, []
    for uri in uris:
        path = out / "records" / f"{key(uri)}.json"
        state = "missing"
        if path.exists():
            try:
                rec = json.loads(path.read_text())
            except ValueError:
                rec = None
            state = record_state(rec, cfg["fingerprint"], uri)
            if state == "invalid" or (state == "failed" and args.retry_failed):
                aside = out / "records_superseded"
                aside.mkdir(exist_ok=True)
                path.replace(aside / f"{key(uri)}.{int(time.time())}.json")
                state = "missing"
        if state == "missing":
            keep = str(out / "artifacts" / uri.split("//")[1].replace("/", "_")) if args.stage == "pilot" else None
            pending.append((uri, inputs["references"][uri], cfg, keep))
        else:
            done[uri] = state
    print(f"{len(uris)} programs; {len(done)} resumed ({sum(s == 'failed' for s in done.values())} failed); "
          f"{len(pending)} pending", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(one, task): task[0] for task in pending}
        for n, future in enumerate(as_completed(futures), 1):
            rec = future.result()
            atomic_json(out / "records" / f"{key(rec['uri'])}.json", rec)
            print(f"{n}/{len(pending)} {rec['uri']}: {rec.get('failed', 'ok')} ({rec['seconds']}s)", flush=True)
    states = {}
    for uri in uris:
        states[uri] = record_state(json.loads((out / "records" / f"{key(uri)}.json").read_text()), cfg["fingerprint"], uri)
    counts = {s: sum(v == s for v in states.values()) for s in ("valid", "failed", "invalid")}
    atomic_json(out / "status.json", {"timestamp": datetime.now(timezone.utc).isoformat(),
                                      "fingerprint": cfg["fingerprint"], "counts": counts,
                                      "not_valid": {u: s for u, s in states.items() if s != "valid"}})
    print("finished", json.dumps(counts), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prepare")
    sub.add_parser("gate")
    r = sub.add_parser("run")
    r.add_argument("--stage", choices=("pilot", "campaign"), required=True)
    r.add_argument("--workers", type=int, default=2)
    r.add_argument("--retry-failed", action="store_true")
    args = p.parse_args()
    {"prepare": prepare, "gate": gate, "run": run}[args.cmd](args)


if __name__ == "__main__":
    main()

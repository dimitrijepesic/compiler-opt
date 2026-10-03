#!/usr/bin/env python3
"""
Selector audit: candidate generation (GNN vs random) x candidate selection
(IR instruction count vs code-section bytes) on the same eight candidates.

Question. Does the GNN produce better candidates than random search while
selection by IR instruction count (IC) fails to pass their advantage on to
code bytes?  Fixed scope: the `attr` condition (minsize/optsize on function
definitions, canonical CompilerGym LLVM 10 service module), all 347
programs of results/gnn_attribute_audit, no new training or sampling.

Inputs (frozen by --prepare into results/selector_audit/inputs.json):
  GNN    the stored action traces of the three from-scratch checkpoints
         (seeds 42, 123, 456); NPB exclusively from
         results/gnn_attribute_audit/npb_offset78/records_gnn_seed*/, the
         other five suites from results/gnn_attribute_audit/records_gnn_seed*/;
         every trace must have 45 successful, non-terminating steps.
  random replicate 42 = the stored candidates of
         results/gnn_attribute_audit/records_null (attr condition, metrics and
         hashes reused with provenance; replayed only in the pilot);
         replicates 43..46 = new draws with the same rule
         (seed = int.from_bytes(sha256(f"{rep}:{uri}").digest()[:8], "big"),
         numpy.random.default_rng, rng.choice(sorted 36 action ids, size=(8, 45))),
         replicate 42 must regenerate the stored actions exactly.

Per program (--run): reset the original URI, export the canonical module,
add the attributes with the canonical helper (scripts/baseline_audit_cgym_matrix.py,
unchanged), load it through a content-hashed file:// URI, check IR digest,
input hash, attribute counts, target triple/datalayout, O0 and the
IrInstructionCountOz observation against the stored records; apply the
service -Oz and check it against the stored baseline; replay every GNN trace
and every new random sequence from that input (reset, then the 45 actions
through the service), export the final module and measure it with the same
llc/llvm-size/ic tools as the audit (IC, code sections `text_sec`, Berkeley
`text`, bitcode and object SHA-256).  Replayed ICs must equal the stored
ICs; for the stored IC-winner the bytes and hashes are compared too.  Any
failure, done flag or mismatch is recorded, never skipped.  Timings of
replay, export/codegen and measurement are recorded separately.

Modes:
  --prepare               write inputs.json and manifest.json (run in the container)
  --run [--pilot] [...]   pilot (12 preselected programs, step-by-step replay,
                          multistep equivalence check, replicate-42 replay) or
                          the full campaign; atomic per-program records; resume
                          skips finished records with the same fingerprint and
                          refuses a directory written under another fingerprint
  --list-pending          show what --run would do without running anything
"""

import argparse
import fcntl
import glob
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
OUT_DEFAULT = ROOT / "results" / "selector_audit"
GNN_DIR = ROOT / "results" / "gnn_attribute_audit"
SUITES = ["npb-v0", "mibench-v1", "blas-v0", "chstone-v0", "csmith-v0", "poj104-v1"]
SEEDS = [42, 123, 456]
REPLICATES = [42, 43, 44, 45, 46]
K = 8
STEPS = 45
W = {}


# ------------------------------------------------------------------ helpers
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_text(s):
    return hashlib.sha256(s.encode()).hexdigest()


def uri_key(uri):
    return sha_text(uri)


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, indent=1) + "\n")
    tmp.replace(path)


def load_json(path):
    return json.loads(Path(path).read_text())


def pass_action_ids():
    ids = []
    for m in re.finditer(r"action_id: (\d+)\n  name: (\S+)", (ROOT / "configs" / "passes.yaml").read_text()):
        ids.append(int(m.group(1)))
    assert len(ids) == 36
    return sorted(ids)


def random_sequences(replicate, uri, action_ids):
    seed = int.from_bytes(hashlib.sha256(f"{replicate}:{uri}".encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    return seed, rng.choice(action_ids, size=(K, STEPS)).tolist()


def pilot_uris(programs):
    out = []
    for suite in sorted(set(p["suite"] for p in programs)):
        ps = [p for p in programs if p["suite"] == suite]
        out.append(min(ps, key=lambda p: (p["o0"], p["uri"]))["uri"])
        out.append(min(ps, key=lambda p: (-p["o0"], p["uri"]))["uri"])
    return sorted(set(out))


# ------------------------------------------------------------------ prepare
def prepare(out):
    programs = load_json(GNN_DIR / "programs.json")["programs"]
    action_ids = pass_action_ids()
    inputs, problems = [], []
    for p in programs:
        uri, suite = p["uri"], p["suite"]
        key = uri_key(uri)
        rec = {"uri": uri, "suite": suite, "o0": p["o0"], "oz": p["oz"], "gnn": {}, "random": {}}
        base = GNN_DIR / "npb_offset78" if suite == "npb-v0" else GNN_DIR
        ref = None
        for seed in SEEDS:
            f = base / f"records_gnn_seed{seed}" / f"{key}.json"
            g = load_json(f)
            a = g["attr"]
            assert "failed" not in g and g["uri"] == uri and len(a["samples"]) == K
            traces, ics = [], []
            for j, smp in enumerate(a["samples"]):
                acts = smp["actions"]
                if not smp.get("ok") or len(acts) != STEPS or any(s[1] != 1 or s[2] != 0 for s in acts):
                    problems.append({"uri": uri, "seed": seed, "sample": j, "problem": "failed/done/short trace"})
                traces.append([s[0] for s in acts])
                ics.append(int(smp["ic"]))
            rec["gnn"][str(seed)] = {"source": os.path.relpath(f, ROOT), "source_sha256": digest(f),
                                     "traces": traces, "stored_ics": ics,
                                     "stored_best_by_ic": a["best_by_ic"], "stored_argmax": a["argmax"],
                                     "input_sha256": a["input_sha256"], "ir_sha256": a["ir_sha256"],
                                     "o0_ic": a["o0_ic"], "oz_ic_observation": a["oz_ic_observation"],
                                     "attribute_info": g["attribute_info"]}
            ident = (a["input_sha256"], a["ir_sha256"], a["o0_ic"], a["oz_ic_observation"])
            if ref is None:
                ref = ident
            elif ident != ref:
                problems.append({"uri": uri, "seed": seed, "problem": "input identity differs between seeds"})
        f = GNN_DIR / "records_null" / f"{key}.json"
        n = load_json(f)
        a = n["attr"]
        assert "failed" not in n and n["uri"] == uri and len(a["random"]) == K and all(e["ok"] for e in a["random"])
        if (a["input_sha256"], a["ir_sha256"], a["o0_ic"], a["oz_ic_observation"]) != ref:
            problems.append({"uri": uri, "problem": "null input identity differs from GNN records"})
        seed42, gen42 = random_sequences(42, uri, action_ids)
        if gen42 != n["random_actions"]:
            problems.append({"uri": uri, "problem": "replicate 42 does not regenerate the stored random actions"})
        rec["random"]["42"] = {"source": os.path.relpath(f, ROOT), "source_sha256": digest(f), "seed_int": seed42,
                               "sequences": n["random_actions"], "stored_candidates": a["random"],
                               "stored_oz": a["oz"], "input_sha256": a["input_sha256"], "ir_sha256": a["ir_sha256"]}
        for rep in REPLICATES[1:]:
            s, seqs = random_sequences(rep, uri, action_ids)
            rec["random"][str(rep)] = {"source": "generated", "seed_int": s, "sequences": seqs}
        rec["stored_attr_oz"] = a["oz"]
        rec["attribute_info"] = load_json(base / f"records_gnn_seed{SEEDS[0]}" / f"{key}.json")["attribute_info"]
        inputs.append(rec)
    pilot = pilot_uris(programs)
    data = {"timestamp": datetime.now(timezone.utc).isoformat(), "n": len(inputs),
            "gnn_candidates": len(inputs) * len(SEEDS) * K,
            "random_candidates_reused": len(inputs) * K, "random_candidates_new": len(inputs) * (len(REPLICATES) - 1) * K,
            "action_ids": action_ids, "pilot_uris": pilot, "problems": problems, "programs": inputs}
    atomic_json(out / "inputs.json", data)
    manifest = build_manifest(out, data)
    atomic_json(out / "manifest.json", manifest)
    print(f"{len(inputs)} programs, {data['gnn_candidates']} GNN candidates, {data['random_candidates_new']} new random "
          f"candidates, {len(problems)} problems, pilot {len(pilot)} programs -> {out}/inputs.json, manifest fingerprint "
          f"{manifest['fingerprint'][:16]}")
    if problems:
        print("PROBLEMS:", json.dumps(problems[:10], indent=1))


def build_manifest(out, inputs_data):
    import compiler_gym
    import baseline_audit_cgym_matrix as audit
    import subprocess
    ic_tool = subprocess.run(["which", "ic"], capture_output=True, text=True).stdout.strip()
    m = {"schema": 1, "created": datetime.now(timezone.utc).isoformat(),
         "script_sha256": digest(__file__),
         "helper": "scripts/baseline_audit_cgym_matrix.py", "helper_sha256": digest(audit.__file__),
         "gnn_script_sha256": digest(ROOT / "scripts" / "evaluate_gnn_attribute_audit.py"),
         "passes_yaml_sha256": digest(ROOT / "configs" / "passes.yaml"),
         "inputs_sha256": sha_text(json.dumps(inputs_data["programs"], sort_keys=True)),
         "n_programs": inputs_data["n"], "pilot_uris": inputs_data["pilot_uris"],
         "compiler_gym": compiler_gym.__version__, "numpy": np.__version__,
         "llvm_version": audit.command([audit.LLVM / "opt", "--version"]).strip(),
         "ic_tool_sha256": digest(ic_tool) if ic_tool else None,
         "seeds_gnn": SEEDS, "replicates_random": REPLICATES, "k": K, "steps": STEPS,
         "random_rule": "seed=int.from_bytes(sha256(f'{rep}:{uri}').digest()[:8],'big'); numpy default_rng; rng.choice(sorted 36 action ids, size=(8,45))",
         "condition": "attr: minsize optsize on function definitions (canonical add_attributes)",
         "baseline": "service llvm.apply_baseline_optimizations=-Oz on the attributed module",
         "replay": "reset attributed file URI, then the stored/new action ids through the service; final module exported and measured",
         "measurement": "bundled llc -filetype=obj; llvm-size (Berkeley text) and llvm-size -A (.text*/__text sum = text_sec); ic tool for IC; sha256 of bitcode and object",
         "selectors": {"ic_first": "min IC, first candidate on ties (the paper's rule)",
                       "code_first": "min text_sec, first candidate on ties",
                       "ic_then_code": "min IC, ties by min text_sec, then first (diagnostic)",
                       "berkeley_first": "min Berkeley text, first on ties (diagnostic)",
                       "oz_fallback": "separate tables only: baseline is an extra candidate; guarantee holds only for the metric selected on"},
         "gnn_sources": "npb-v0: results/gnn_attribute_audit/npb_offset78/records_gnn_seed*; other suites: results/gnn_attribute_audit/records_gnn_seed*",
         "random_42_source": "results/gnn_attribute_audit/records_null (attr candidates reused; replayed only in the pilot)"}
    m["fingerprint"] = sha_text(json.dumps({k: v for k, v in m.items() if k != "created"}, sort_keys=True))
    return m


# ---------------------------------------------------------------- worker
def _close_worker():
    try:
        if W.get("env") is not None:
            W["env"].close()
    except Exception:
        pass


def init_worker(cfg):
    import atexit
    import compiler_gym
    import baseline_audit_cgym_matrix as audit
    W.update({"cfg": cfg, "audit": audit, "env": compiler_gym.make("llvm-v0")})
    atexit.register(_close_worker)


def header_lines(audit, bc):
    ll = audit.command([audit.LLVM / "llvm-dis", bc, "-o", "-"])
    return {"triple": next((l for l in ll.splitlines() if l.startswith("target triple")), None),
            "datalayout": next((l for l in ll.splitlines() if l.startswith("target datalayout")), None)}


def replay(env, audit, uri, actions, wd, mode):
    """Reset to the attributed input and apply the actions. Returns
    (measurement dict or None, steps applied, error, done_seen, timings)."""
    t0 = time.perf_counter()
    env.reset(benchmark=uri)
    done_seen = False
    err = None
    applied = 0
    if mode == "multistep":
        try:
            _, _, done, info = env.multistep(list(actions), timeout=120)
            applied = len(actions)
            if done:
                done_seen = True
                err = f"environment ended early: {info}"
        except Exception as e:
            err = repr(e)[:300]
    else:
        for a in actions:
            try:
                _, _, done, info = env.step(int(a))
                applied += 1
                if done:
                    done_seen = True
                    err = f"done at step {applied}: {info}"
                    break
            except Exception as e:
                err = f"step {applied + 1}: {repr(e)[:300]}"
                break
    t1 = time.perf_counter()
    if err:
        return None, applied, err, done_seen, {"replay_s": t1 - t0, "export_s": 0, "measure_s": 0}
    bc = wd / "candidate.bc"
    env.write_bitcode(str(bc))
    ic_env = int(env.observation["IrInstructionCount"])
    t2 = time.perf_counter()
    m = audit.measure(bc, wd)  # ic (tool), text, text_sec, bitcode_sha256, object_sha256
    t3 = time.perf_counter()
    m["ic_env"] = ic_env
    return m, applied, None, done_seen, {"replay_s": t1 - t0, "export_s": t2 - t1, "measure_s": t3 - t2}


def one(prog):
    cfg, audit, env = W["cfg"], W["audit"], W["env"]
    uri = prog["uri"]
    mode = cfg["replay_mode"]
    rec = {"uri": uri, "suite": prog["suite"], "fingerprint": cfg["fingerprint"], "replay_mode": mode,
           "pilot": cfg["pilot"], "timings": {"replay_s": 0.0, "export_s": 0.0, "measure_s": 0.0, "steps": 0,
                                              "sequences": 0, "candidates_measured": 0}}
    t_start = time.monotonic()
    tm = rec["timings"]

    def acc(t, steps):
        tm["replay_s"] += t["replay_s"]; tm["export_s"] += t["export_s"]; tm["measure_s"] += t["measure_s"]
        tm["steps"] += steps; tm["sequences"] += 1; tm["candidates_measured"] += 1

    try:
        with tempfile.TemporaryDirectory(prefix="selector-audit-") as temp:
            wd = Path(temp)
            t0 = time.perf_counter()
            # ---- input identity
            env.reset(benchmark=uri)
            o0 = int(env.observation["IrInstructionCount"]); oz = int(env.observation["IrInstructionCountOz"])
            plain = wd / "plain-export.bc"
            env.write_bitcode(str(plain))
            attr = wd / "attr-export.bc"
            info = audit.add_attributes(plain, attr)
            src = wd / f"input-attr-{digest(attr)}.bc"
            attr.rename(src)
            vuri = src.as_uri()
            env.reset(benchmark=vuri)
            loaded = wd / "attr-loaded.bc"
            env.write_bitcode(str(loaded))
            ir_sha = audit.ir_digest(src)
            g0 = prog["gnn"][str(SEEDS[0])]
            ident = {"o0_ic": o0, "oz_ic_observation_plain": oz, "input_sha256": digest(src), "ir_sha256": ir_sha,
                     "ir_sha256_after_load": audit.ir_digest(loaded), "attribute_info": info,
                     "attr_o0_ic": int(env.observation["IrInstructionCount"]),
                     "attr_oz_ic_observation": int(env.observation["IrInstructionCountOz"]),
                     "headers_plain": header_lines(audit, plain), "headers_attr": header_lines(audit, src)}
            ident["checks"] = {
                "o0_matches_battery": o0 == prog["o0"], "oz_matches_battery": oz == prog["oz"],
                "input_sha256_matches_stored": ident["input_sha256"] == g0["input_sha256"],
                "ir_sha256_matches_stored": ir_sha == g0["ir_sha256"],
                "ir_unchanged_on_load": ident["ir_sha256_after_load"] == ir_sha,
                "attribute_info_matches_stored": info == prog["attribute_info"],
                "all_definitions_annotated": info["definitions"] == info["verified_size_definitions"],
                "attr_o0_unchanged": ident["attr_o0_ic"] == o0,
                "attr_oz_observation_matches_stored": ident["attr_oz_ic_observation"] == g0["oz_ic_observation"],
                "triple_datalayout_preserved": ident["headers_plain"] == ident["headers_attr"] and ident["headers_attr"]["triple"] is not None}
            rec["input"] = ident
            # ---- baseline through the service
            env.reset(benchmark=vuri)
            env.send_param("llvm.apply_baseline_optimizations", "-Oz")
            bz = wd / "oz.bc"
            env.write_bitcode(str(bz))
            base = audit.measure(bz, wd)
            base["ic_env"] = int(env.observation["IrInstructionCount"])
            st = prog["stored_attr_oz"]
            base["checks"] = {"ic_matches_observation": base["ic"] == ident["attr_oz_ic_observation"] == base["ic_env"],
                              "ic_matches_stored": base["ic"] == st["ic"], "text_matches_stored": base["text"] == st["text"],
                              "text_sec_matches_stored": base["text_sec"] == st["text_sec"],
                              "bitcode_sha256_matches_stored": base["bitcode_sha256"] == st["bitcode_sha256"],
                              "object_sha256_matches_stored": base["object_sha256"] == st["object_sha256"]}
            rec["baseline"] = base
            tm["input_and_baseline_s"] = time.perf_counter() - t0
            # ---- GNN replay (all 8 traces of each seed)
            rec["gnn"] = {}
            for seed in SEEDS:
                g = prog["gnn"][str(seed)]
                cands = []
                for j, trace in enumerate(g["traces"]):
                    m, applied, err, done_seen, t = replay(env, audit, vuri, trace, wd, mode)
                    acc(t, applied)
                    c = {"index": j, "actions": trace, "steps_applied": applied, "done_seen": done_seen, "stored_ic": g["stored_ics"][j]}
                    if err:
                        c.update({"ok": False, "error": err})
                    else:
                        c.update({"ok": True, **m, "ic_matches_stored": m["ic"] == g["stored_ics"][j] == m["ic_env"]})
                    cands.append(c)
                bi = g["stored_best_by_ic"]
                w = cands[bi["index"]]
                winner = {"index": bi["index"], "stored": bi}
                if w.get("ok"):
                    winner.update({"replay": {k: w[k] for k in ("ic", "text", "text_sec", "bitcode_sha256", "object_sha256")},
                                   "ic_match": w["ic"] == bi["ic"], "text_match": w["text"] == bi["text"],
                                   "text_sec_match": w["text_sec"] == bi["text_sec"],
                                   "bitcode_sha256_match": w["bitcode_sha256"] == bi["bitcode_sha256"],
                                   "object_sha256_match": w["object_sha256"] == bi["object_sha256"]})
                rec["gnn"][str(seed)] = {"source": g["source"], "source_sha256": g["source_sha256"], "candidates": cands,
                                         "old_ic_winner": winner, "n_ok": sum(c.get("ok", False) for c in cands),
                                         "n_ic_match": sum(c.get("ic_matches_stored", False) for c in cands)}
            # ---- random: replicate 42 reused (replayed in the pilot), 43..46 replayed
            rec["random"] = {}
            for rep in REPLICATES:
                r = prog["random"][str(rep)]
                entry = {"seed_int": r["seed_int"], "source": r["source"], "sequences": r["sequences"]}
                if rep == 42:
                    entry["source_sha256"] = r["source_sha256"]
                    entry["candidates"] = [{"index": j, "actions": r["sequences"][j], "ok": True, "reused": True,
                                            **{k: e[k] for k in ("ic", "text", "text_sec", "bitcode_sha256", "object_sha256")}}
                                           for j, e in enumerate(r["stored_candidates"])]
                    if cfg["pilot"]:
                        rp = []
                        for j, seq in enumerate(r["sequences"]):
                            m, applied, err, done_seen, t = replay(env, audit, vuri, seq, wd, mode)
                            acc(t, applied)
                            e = r["stored_candidates"][j]
                            rp.append({"index": j, "ok": err is None, "error": err, "steps_applied": applied, "done_seen": done_seen,
                                       **({} if err else {**m, "matches_stored": {k: m[k] == e[k] for k in ("ic", "text", "text_sec", "bitcode_sha256", "object_sha256")}})})
                        entry["pilot_replay"] = rp
                else:
                    cands = []
                    for j, seq in enumerate(r["sequences"]):
                        m, applied, err, done_seen, t = replay(env, audit, vuri, seq, wd, mode)
                        acc(t, applied)
                        c = {"index": j, "actions": seq, "steps_applied": applied, "done_seen": done_seen}
                        c.update({"ok": False, "error": err} if err else {"ok": True, **m})
                        cands.append(c)
                    entry["candidates"] = cands
                entry["n_ok"] = sum(c.get("ok", False) for c in entry["candidates"])
                rec["random"][str(rep)] = entry
            # ---- pilot: multistep vs step equivalence on one GNN trace and one new random sequence
            if cfg["pilot"]:
                eq = {}
                for label, actions in (("gnn_seed42_sample0", prog["gnn"]["42"]["traces"][0]),
                                       ("random_43_seq0", prog["random"]["43"]["sequences"][0])):
                    a, *_ = replay(env, audit, vuri, actions, wd, "step")
                    b, *_ = replay(env, audit, vuri, actions, wd, "multistep")
                    eq[label] = {"step": a and {k: a[k] for k in ("ic", "text_sec", "bitcode_sha256", "object_sha256")},
                                 "multistep": b and {k: b[k] for k in ("ic", "text_sec", "bitcode_sha256", "object_sha256")},
                                 "equal": bool(a and b and a["bitcode_sha256"] == b["bitcode_sha256"] and a["object_sha256"] == b["object_sha256"])}
                rec["multistep_equivalence"] = eq
    except Exception as e:
        rec["failed"] = repr(e)[:1200]
        try:
            env.close()
        except Exception:
            pass
        import compiler_gym
        W["env"] = compiler_gym.make("llvm-v0")
    rec["seconds"] = round(time.monotonic() - t_start, 2)
    return rec


# ---------------------------------------------------------------- driver
def record_ok(rec):
    if "failed" in rec:
        return False
    if not all(rec["input"]["checks"].values()) or not all(rec["baseline"]["checks"].values()):
        return False
    return all(g["n_ok"] == K and g["n_ic_match"] == K for g in rec["gnn"].values()) and \
        all(r["n_ok"] == K for r in rec["random"].values())


def run(args):
    out = args.out
    manifest = load_json(out / "manifest.json")
    inputs = load_json(out / "inputs.json")
    if inputs["problems"]:
        raise SystemExit(f"inputs.json lists {len(inputs['problems'])} problems; fix them before running")
    if manifest["script_sha256"] != digest(__file__):
        raise SystemExit("the script changed since --prepare: rerun --prepare (new fingerprint) or restore the script")
    cfg = {"fingerprint": sha_text(manifest["fingerprint"] + f"|replay={args.replay}|pilot={int(args.pilot)}"),
           "manifest_fingerprint": manifest["fingerprint"], "replay_mode": args.replay, "pilot": args.pilot}
    programs = inputs["programs"]
    if args.pilot:
        keep = set(inputs["pilot_uris"])
        programs = [p for p in programs if p["uri"] in keep]
    if args.uri:
        programs = [p for p in programs if p["uri"] in set(args.uri)]
    sub = out / ("pilot" if args.pilot else "records")
    sub.mkdir(parents=True, exist_ok=True)
    run_manifest = sub / "run_manifest.json"
    if run_manifest.exists():
        old = load_json(run_manifest)
        if old["fingerprint"] != cfg["fingerprint"]:
            raise SystemExit(f"{sub} was written under fingerprint {old['fingerprint'][:16]}, current is "
                             f"{cfg['fingerprint'][:16]}: use a new output directory")
    done, pending = [], []
    for p in programs:
        path = sub / f"{uri_key(p['uri'])}.json"
        if path.exists():
            r = load_json(path)
            if r.get("fingerprint") == cfg["fingerprint"] and "failed" not in r:
                done.append(r)
                continue
        pending.append((p, path))
    print(f"[{'pilot' if args.pilot else 'campaign'} replay={args.replay}] {len(programs)} programs, {len(done)} done, "
          f"{len(pending)} pending, workers={args.workers}, fingerprint {cfg['fingerprint'][:16]}", flush=True)
    if args.list_pending:
        for p, path in pending:
            print("  pending:", p["uri"])
        return
    lock = (sub / ".run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another process is writing {sub}")
    cfg["command"] = " ".join(["python", os.path.relpath(__file__, ROOT)] + sys.argv[1:])
    cfg["started"] = datetime.now(timezone.utc).isoformat()
    cfg["workers"] = args.workers
    cfg["hardware"] = "amd64 Ubuntu 22.04 container under Rosetta 2 (Colima vz VM) on Apple M5 Pro; emulated, no timing claim"
    atomic_json(run_manifest, cfg)
    t0 = time.monotonic()
    n_fail = n_bad = 0
    with ProcessPoolExecutor(args.workers, initializer=init_worker, initargs=(cfg,)) as pool:
        futures = {pool.submit(one, p): path for p, path in pending}
        for k, fut in enumerate(as_completed(futures), 1):
            rec = fut.result()
            atomic_json(futures[fut], rec)
            ok = record_ok(rec)
            n_fail += "failed" in rec
            n_bad += (not ok) and ("failed" not in rec)
            if "failed" in rec:
                extra = ""
            else:
                gnn_s = "/".join("%d:%d" % (g["n_ok"], g["n_ic_match"]) for g in rec["gnn"].values())
                rnd_s = "/".join(str(r["n_ok"]) for r in rec["random"].values())
                base_s = "OK" if all(rec["baseline"]["checks"].values()) else "MISMATCH"
                in_s = "OK" if all(rec["input"]["checks"].values()) else "MISMATCH"
                extra = f" gnn ok:icmatch {gnn_s} rnd ok {rnd_s} base {base_s} input {in_s}"
            print(f"  {k}/{len(pending)} {rec['uri']}: {rec.get('failed', 'ok' if ok else 'CHECK')[:100]} ({rec['seconds']}s){extra}", flush=True)
    print(f"finished {len(pending)} in {(time.monotonic() - t0) / 60:.1f} min; failed {n_fail}, with mismatches {n_bad} -> {sub}", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    p.add_argument("--prepare", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--replay", choices=["step", "multistep"], default="step")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--uri", nargs="*", default=[])
    p.add_argument("--list-pending", action="store_true")
    args = p.parse_args()
    if args.prepare:
        args.out.mkdir(parents=True, exist_ok=True)
        prepare(args.out)
    elif args.run or args.list_pending:
        run(args)
    else:
        p.error("choose --prepare or --run")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GNN sampler and paired random null with and without size attributes, on the
347 programs of the original battery evaluation.

Question. The paper's best-of-8 GNN sampler beats a paired best-of-8 random
null on IR whose functions carry no `minsize`/`optsize` attributes (the IR
CompilerGym ships). Does the comparison, and the margin over the `-Oz`
reference, survive when both sides run on the same IR with the attributes a
size build would carry?

Protocol (see results/baseline_audit/llvm10_canonical/README.md for the
baseline conventions, which are reused through that audit's helper
functions without modification):

- Programs: the 347 programs on which all three GNN seeds were evaluated in
  results/battery_policy (NPB 120, MiBench 40, BLAS 50, CHStone 12, csmith
  28, POJ-104 97); `--prepare` writes the explicit list with the stored
  reference numbers to programs.json.
- Policies: the existing from-scratch checkpoints
  results/ppo_gnn/checkpoint_best_seed{42,123,456}.pt (hashes recorded), the
  36-pass action space, 45-step episodes, best-of-8. The original sampling
  regime of scripts/evaluate_policy_battery.py is reproduced: encoder and
  policy in train mode (dropout active) for sampled rollouts, eval mode for
  the argmax rollout, torch seed = seed*100000 + i*100 + j with i the
  program's index in the original run's enumeration (reconstructed from
  the stored samples, see eligible_index()) and j the sample index, a
  failed `step` skipped without advancing the state. The plain condition is
  therefore a re-run of the original evaluation and is checked against the
  stored per-program sample ICs.
- Inputs come from the CompilerGym service: the benchmark is reset, its
  canonical bitcode exported, O0/Oz checked against the stored battery
  values, attributes added to function definitions only (canonical helper),
  and both variants loaded back through content-specific file:// URIs with
  an IR-identity check. Graphs are parsed from the service's IR of the
  loaded module; the graph cache is a fresh temporary directory per worker.
- Random null: eight 45-action sequences per program, drawn as in the
  canonical audit (seed 42 and a SHA-256 per-URI seed), applied to both
  variants through service actions (`multistep`), every sequence recorded.
  These are fresh draws; the stored null's best-of-8 is kept for reference.
- Reference: the service's own `llvm.apply_baseline_optimizations=-Oz`,
  exported and required to match `IrInstructionCountOz`.
- Selection: minimum final IC (first on ties). Bytes (Berkeley text and
  code sections, bundled llc, module's own triple) for the reference and
  for the selected candidate of each method.
- Every failure is recorded; totals use the common set and the excluded
  programs are listed.

Modes:
  --prepare                 write programs.json (host or container)
  --null --workers N        reference + random null, both conditions
  --seed S --workers N      GNN sampler for one checkpoint, both conditions
  --summarize               summary.json and REPORT.md from the records
Resume: rerun the same command; finished records are skipped when the
protocol fingerprint matches.
"""

import argparse
import fcntl
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

OUT_DEFAULT = ROOT / "results" / "gnn_attribute_audit"
SUITES = ["blas-v0", "chstone-v0", "csmith-v0", "mibench-v1", "npb-v0", "poj104-v1"]
EXPECTED = {"npb-v0": 120, "mibench-v1": 40, "blas-v0": 50, "chstone-v0": 12, "csmith-v0": 28, "poj104-v1": 97}
SEEDS = [42, 123, 456]
K = 8
STEPS = 45
MAX_IC = 6000
NULL_SEED = 42
CKPT_DIR = ROOT / "results" / "ppo_gnn"
VARIANTS = ("plain", "attr")

W = {}  # per-worker state


# ----------------------------------------------------------------- helpers
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def uri_key(uri):
    return hashlib.sha256(uri.encode()).hexdigest()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, indent=1) + "\n")
    tmp.replace(path)


def load_json(path):
    return json.loads(Path(path).read_text())


def eligible_index():
    """Per program: its position within its suite's eligible list (the
    aggregate's benchmark order, programs with an Oz value and O0 IC <=
    6000), the six-suite global index, and the reconstructed index that
    the original evaluation actually used for the torch seed.

    scripts/evaluate_policy_battery.py enumerates the eligible programs of
    the suites passed to --suites in sorted order and keeps counting over
    programs whose record already exists. The stored sample ICs are
    reproduced exactly (pilot/index_test_output.txt,
    pilot/index_search_output.txt, pilot/index_test_npb_output.txt) by
    these per-suite offsets, which correspond to two invocations: blas,
    csmith, npb, poj104 together (csmith after 50 blas programs, npb after
    50 + 28 = 78, poj104 after 50 + 28 + 120 = 198); then all six suites
    (chstone after 50 blas, mibench after 50 + 12 + 28 = 90). blas is at
    offset 0 in both. The first full campaign (records_gnn_seed*/) used
    offset 0 for npb, which reproduced only the tiny NPB modules; the
    corrected offset 78 is used for the supplementary NPB rerun
    (npb_offset78/)."""
    offsets = {"blas-v0": 0, "chstone-v0": 50, "csmith-v0": 50, "mibench-v1": 90, "npb-v0": 78, "poj104-v1": 198}
    position, global_index, seed_index = {}, {}, {}
    g = 0
    for suite in sorted(SUITES):
        agg = load_json(ROOT / "results" / "battery" / suite / "_aggregate.json")
        pos = 0
        for r in agg["benchmarks"]:
            if "oz" in r and r.get("o0", 10 ** 9) <= MAX_IC:
                position[r["uri"]] = pos
                global_index[r["uri"]] = g
                seed_index[r["uri"]] = offsets[suite] + pos
                pos += 1
                g += 1
    return position, global_index, seed_index


def prepare(out):
    position, global_index, seed_index = eligible_index()
    programs = []
    for suite in SUITES:
        agg = {r["uri"]: r for r in load_json(ROOT / "results" / "battery" / suite / "_aggregate.json")["benchmarks"]
               if "oz" in r}
        recs = {}
        for seed in SEEDS:
            for f in sorted(glob.glob(str(ROOT / "results" / "battery_policy" / suite / f"ppo_gnn_seed{seed}" / "*.json"))):
                r = load_json(f)
                recs.setdefault(r["uri"], {})[seed] = (r, f)
        uris = sorted(u for u, s in recs.items() if len(s) == 3)
        assert len(uris) == EXPECTED[suite], (suite, len(uris))
        for u in uris:
            b = agg[u]
            stored = {}
            for seed in SEEDS:
                r, f = recs[u][seed]
                stored[str(seed)] = {"sample_ics": r["sample_ics"], "argmax_ic": r["argmax_ic"],
                                     "best_of_k_ic": r["best_of_k_ic"],
                                     "random_null_best_of_k": r["random_null_best_of_k"],
                                     "file": os.path.relpath(f, ROOT), "sha256": digest(f)}
            programs.append({"uri": u, "suite": suite, "o0": b["o0"], "oz": b["oz"],
                             "position_in_suite": position[u], "global_index": global_index[u],
                             "eligible_index": seed_index[u],
                             "stored_random_episode_ics_first8": b["random_reduced_episode_ics"][:K],
                             "stored": stored})
    data = {"timestamp": datetime.now(timezone.utc).isoformat(), "n": len(programs),
            "per_suite": {s: EXPECTED[s] for s in SUITES},
            "eligible_index_rule": "eligible_index = reconstructed torch-seed index of the original run "
                                   "(per-suite offsets blas 0, chstone 50, csmith 50, mibench 90, npb 0, poj104 198 "
                                   "+ position in the suite's eligible list); see eligible_index() docstring and pilot/",
            "programs": programs}
    atomic_json(out / "programs.json", data)
    print(f"{len(programs)} programs -> {out / 'programs.json'}")


def config(out, mode, seed):
    """Protocol fingerprint; identical fingerprint is required to resume."""
    import compiler_gym
    import baseline_audit_cgym_matrix as audit
    programs = load_json(out / "programs.json")
    cfg = {"schema": 1, "mode": mode, "seed": seed, "k": K, "steps": STEPS, "max_ic": MAX_IC,
           "null_seed": NULL_SEED,
           "script_sha256": digest(__file__),
           "canonical_helper": "scripts/baseline_audit_cgym_matrix.py",
           "canonical_helper_sha256": digest(audit.__file__),
           "programs_sha256": hashlib.sha256(json.dumps(programs["programs"], sort_keys=True).encode()).hexdigest(),
           "passes_yaml_sha256": digest(ROOT / "configs" / "passes.yaml"),
           "hyperparams_sha256": digest(ROOT / "configs" / "hyperparams.yaml"),
           "compiler_gym": compiler_gym.__version__,
           "llvm_version": audit.command([audit.LLVM / "opt", "--version"]).strip(),
           "ic_tool_sha256": digest(audit.command(["which", "ic"]).strip()),
           "numpy": np.__version__,
           "baseline": "service llvm.apply_baseline_optimizations=-Oz",
           "selection": "minimum final IC, first candidate on ties",
           "attribute_method": "canonical add_attributes: minsize optsize on function definitions only"}
    if mode == "gnn":
        import torch
        import torch_geometric
        ckpt = CKPT_DIR / f"checkpoint_best_seed{seed}.pt"
        cfg.update({"torch": torch.__version__, "torch_geometric": torch_geometric.__version__,
                    "checkpoint": os.path.relpath(ckpt, ROOT), "checkpoint_sha256": digest(ckpt),
                    "agent_source_sha256": digest(ROOT / "src" / "agents" / "ppo_gnn.py"),
                    "graph_parser_sha256": digest(ROOT / "src" / "features" / "programl.py"),
                    "torch_seed_rule": "seed*100000 + eligible_index*100 + sample_index",
                    "dropout": "train mode (encoder dropout and policy) during sampled rollouts, eval mode for argmax",
                    "torch_threads": torch.get_num_threads()})
    cfg["fingerprint"] = hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()
    return cfg, programs["programs"]


# ---------------------------------------------------------------- inputs
def make_inputs(env, prog, wd, audit):
    """Reset the original URI, export, check O0/Oz, build the attribute
    variant, load both through content-specific file URIs."""
    uri = prog["uri"]
    env.reset(benchmark=uri)
    o0 = int(env.observation["IrInstructionCount"])
    oz = int(env.observation["IrInstructionCountOz"])
    if (o0, oz) != (prog["o0"], prog["oz"]):
        raise AssertionError(f"O0/Oz mismatch vs stored battery: {(o0, oz)} vs {(prog['o0'], prog['oz'])}")
    plain = wd / "plain-export.bc"
    env.write_bitcode(str(plain))
    if audit.ic(plain) != o0:
        raise AssertionError("export IC != environment IC")
    attr = wd / "attr-export.bc"
    info = audit.add_attributes(plain, attr)
    inputs = {}
    for variant, path in (("plain", plain), ("attr", attr)):
        src = wd / f"input-{variant}-{digest(path)}.bc"
        path.rename(src)
        vuri = src.as_uri()
        env.reset(benchmark=vuri)
        loaded = wd / f"{variant}-loaded.bc"
        env.write_bitcode(str(loaded))
        ir_sha = audit.ir_digest(src)
        if audit.ir_digest(loaded) != ir_sha:
            raise AssertionError(f"{variant}: IR changed on file URI load")
        v_o0 = int(env.observation["IrInstructionCount"])
        if v_o0 != o0:
            raise AssertionError(f"{variant}: input IC changed ({v_o0} vs {o0})")
        v_oz = int(env.observation["IrInstructionCountOz"])
        if variant == "plain" and v_oz != oz:
            raise AssertionError("plain: Oz observation changed on reload")
        inputs[variant] = {"uri": vuri, "path": src, "input_sha256": digest(src), "ir_sha256": ir_sha,
                           "o0_ic": v_o0, "oz_ic_observation": v_oz}
    return {"o0": o0, "oz": oz, "attribute_info": info}, inputs


# ---------------------------------------------------------------- null mode
def _close_worker():
    # Close the CompilerGym service on worker exit; an orphaned service keeps
    # the inherited stdout pipe open and the driver's shell never sees EOF.
    for key in ("env", "agent"):
        obj = W.get(key)
        try:
            if obj is not None:
                obj.close()
        except Exception:
            pass


def init_null(cfg):
    import atexit
    import compiler_gym
    import baseline_audit_cgym_matrix as audit
    W.update({"cfg": cfg, "audit": audit, "env": compiler_gym.make("llvm-v0"),
              "names": {int(a): n for a, n in load_pass_names().items()}})
    atexit.register(_close_worker)


def load_pass_names():
    names = {}
    for m in re.finditer(r"action_id: (\d+)\n  name: (\S+)", (ROOT / "configs" / "passes.yaml").read_text()):
        names[str(int(m.group(1)))] = m.group(2)
    return names


def one_null(prog):
    cfg, audit, env = W["cfg"], W["audit"], W["env"]
    uri = prog["uri"]
    rec = {"uri": uri, "suite": prog["suite"], "mode": "null", "fingerprint": cfg["fingerprint"],
           "eligible_index": prog["eligible_index"],
           "stored_random_null_best_of_8": min(prog["stored_random_episode_ics_first8"])}
    t0 = time.monotonic()
    seed = int.from_bytes(hashlib.sha256(f"{NULL_SEED}:{uri}".encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    action_ids = sorted(W["names"])
    sequences = rng.choice(action_ids, size=(K, STEPS)).tolist()
    rec["random_actions"] = sequences
    try:
        with tempfile.TemporaryDirectory(prefix="gnn-audit-null-") as temp:
            wd = Path(temp)
            head, inputs = make_inputs(env, prog, wd, audit)
            rec.update(head)
            for variant in VARIANTS:
                inp = inputs[variant]
                d = rec[variant] = {k: v for k, v in inp.items() if k != "path"}
                env.reset(benchmark=inp["uri"])
                env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                d["oz"] = audit.export_measure(env, wd / f"{variant}-oz.bc", wd)
                if d["oz"]["ic"] != inp["oz_ic_observation"]:
                    raise AssertionError("service -Oz export differs from observation")
                entries = d["random"] = []
                for sequence in sequences:
                    try:
                        env.reset(benchmark=inp["uri"])
                        _, _, done, info = env.multistep(sequence, timeout=120)
                        if done:
                            raise RuntimeError(f"environment ended early: {info}")
                        entries.append({"ok": True, **audit.export_measure(env, wd / "candidate.bc", wd)})
                    except Exception as e:
                        entries.append({"ok": False, "error": repr(e)[:800]})
                d["random_best"] = audit.select(entries)
    except Exception as e:
        rec["failed"] = repr(e)[:1200]
        try:
            env.close()
        except Exception:
            pass
        import compiler_gym
        W["env"] = compiler_gym.make("llvm-v0")
    rec["seconds"] = round(time.monotonic() - t0, 2)
    return rec


# ----------------------------------------------------------------- gnn mode
def init_gnn(cfg):
    import torch
    import baseline_audit_cgym_matrix as audit
    cache = tempfile.mkdtemp(prefix="graphcache-")
    os.environ["COMPILER_OPT_CACHE_DIR"] = cache  # fresh cache per worker: no stale graphs
    os.chdir(ROOT)  # the agent reads configs/ by relative path
    from src.agents.ppo_gnn import PPOGNNAgent
    import atexit
    agent = PPOGNNAgent(seed=cfg["seed"])
    agent.load_checkpoint(str(ROOT / cfg["checkpoint"]))
    assert agent.num_actions == 36 and agent.max_episode_steps == STEPS
    W.update({"cfg": cfg, "audit": audit, "agent": agent, "torch": torch, "cache": cache})
    atexit.register(_close_worker)


def sample_rollout(agent, torch, uri, rng_seed, out_bc):
    """The original sampled rollout (scripts/evaluate_policy_battery.py,
    default dropout-active regime), plus a record of every action and a
    bitcode export of the final module."""
    torch.manual_seed(rng_seed)
    agent.gnn.train()
    agent.policy.train()
    modes = {"gnn_training": agent.gnn.training, "policy_training": agent.policy.training}
    agent.env.reset(benchmark=uri)
    state = agent._get_graph()
    steps = []
    for _ in range(agent.max_episode_steps):
        with torch.no_grad():
            logits = agent.policy(agent.gnn(state))
            action_idx = torch.distributions.Categorical(logits=logits).sample().item()
        action = agent.action_map[action_idx]
        try:
            _, _, done, _ = agent.env.step(action)
            steps.append([action, 1, int(bool(done))])
        except Exception:
            steps.append([action, 0, None])
            continue
        state = agent._get_graph()
    final = int(agent.env.observation["IrInstructionCount"])
    agent.env.write_bitcode(str(out_bc))
    return final, steps, modes


def one_gnn(prog):
    cfg, audit, agent, torch = W["cfg"], W["audit"], W["agent"], W["torch"]
    uri, i, seed = prog["uri"], prog["eligible_index"], cfg["seed"]
    rec = {"uri": uri, "suite": prog["suite"], "mode": "gnn", "seed": seed, "fingerprint": cfg["fingerprint"],
           "eligible_index": i, "stored": prog["stored"][str(seed)]}
    t0 = time.monotonic()
    try:
        with tempfile.TemporaryDirectory(prefix="gnn-audit-") as temp:
            wd = Path(temp)
            head, inputs = make_inputs(agent.env, prog, wd, audit)
            rec.update(head)
            for variant in VARIANTS:
                inp = inputs[variant]
                d = rec[variant] = {k: v for k, v in inp.items() if k != "path"}
                samples = d["samples"] = []
                for j in range(K):
                    rng_seed = seed * 100000 + i * 100 + j
                    bc = wd / f"{variant}-sample{j}.bc"
                    try:
                        ic, steps, modes = sample_rollout(agent, torch, inp["uri"], rng_seed, bc)
                        samples.append({"ok": True, "ic": ic, "torch_seed": rng_seed, "actions": steps,
                                        "failed_steps": sum(1 for s in steps if not s[1]),
                                        "done_flags": sum(1 for s in steps if s[2]), "modes": modes})
                    except Exception as e:
                        samples.append({"ok": False, "torch_seed": rng_seed, "error": repr(e)[:800]})
                        raise
                # argmax rollout exactly as the original (agent.evaluate), then export
                _, _, details = agent.evaluate([inp["uri"]], "ref")
                d["argmax_ic"] = int(details[0]["final_ic"])
                argmax_bc = wd / f"{variant}-argmax.bc"
                agent.env.write_bitcode(str(argmax_bc))
                d["argmax"] = audit.measure(argmax_bc, wd, d["argmax_ic"])
                ok = [(j, s) for j, s in enumerate(samples) if s.get("ok")]
                if ok:
                    j, s = min(ok, key=lambda p: (p[1]["ic"], p[0]))
                    d["best_by_ic"] = {"index": j, **audit.measure(wd / f"{variant}-sample{j}.bc", wd, s["ic"])}
                    d["n_ok"], d["n_fail"] = len(ok), K - len(ok)
                # reproduction of the stored evaluation (plain condition only)
                if variant == "plain":
                    st = prog["stored"][str(seed)]
                    got = [s.get("ic") for s in samples]
                    d["reproduction"] = {"stored_sample_ics": st["sample_ics"], "sample_ics_match": got == st["sample_ics"],
                                         "n_sample_matches": sum(a == b for a, b in zip(got, st["sample_ics"])),
                                         "stored_argmax_ic": st["argmax_ic"], "argmax_match": d["argmax_ic"] == st["argmax_ic"],
                                         "stored_best_of_k_ic": st["best_of_k_ic"],
                                         "best_of_k_match": (d.get("best_by_ic") or {}).get("ic") == st["best_of_k_ic"]}
    except Exception as e:
        rec["failed"] = repr(e)[:1200]
        agent._recycle_env()
    rec["seconds"] = round(time.monotonic() - t0, 2)
    return rec


# ------------------------------------------------------------------ driver
def run(args):
    mode = "null" if args.null else "gnn"
    out = args.out
    cfg, programs = config(out, mode, args.seed)
    if args.suites:
        programs = [p for p in programs if p["suite"] in args.suites]
    if args.pilot:
        by = {}
        for p in programs:
            by.setdefault(p["suite"], []).append(p)
        programs = [p for s in SUITES for p in by.get(s, [])[:args.pilot]]
    if args.uri:
        programs = [p for p in programs if p["uri"] in set(args.uri)]
    sub = out / ("records_null" if mode == "null" else f"records_gnn_seed{args.seed}")
    sub.mkdir(parents=True, exist_ok=True)
    lock = (sub / ".run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another process is writing {sub}")
    manifest = sub / "manifest.json"
    if manifest.exists() and load_json(manifest)["fingerprint"] != cfg["fingerprint"]:
        raise SystemExit("protocol fingerprint changed: use a new output directory or restore the protocol")
    cfg["command"] = " ".join(["python", os.path.relpath(__file__, ROOT)] + sys.argv[1:])
    cfg["resume"] = "rerun the same command; existing records with this fingerprint are skipped"
    atomic_json(manifest, cfg)
    done, pending = [], []
    for p in programs:
        path = sub / f"{uri_key(p['uri'])}.json"
        if path.exists():
            r = load_json(path)
            if r["fingerprint"] == cfg["fingerprint"] and "failed" not in r:
                done.append(r)
                continue
        pending.append((p, path))
    print(f"[{mode} seed={args.seed}] {len(programs)} programs, {len(done)} done, {len(pending)} pending, "
          f"workers={args.workers}", flush=True)
    init, work = (init_null, one_null) if mode == "null" else (init_gnn, one_gnn)
    t0 = time.monotonic()
    n_fail = 0
    with ProcessPoolExecutor(args.workers, initializer=init, initargs=(cfg,)) as pool:
        futures = {pool.submit(work, p): path for p, path in pending}
        for k, fut in enumerate(as_completed(futures), 1):
            rec = fut.result()
            atomic_json(futures[fut], rec)
            n_fail += "failed" in rec
            extra = ""
            if mode == "gnn" and "failed" not in rec:
                rp = rec["plain"].get("reproduction", {})
                extra = (f" repro samples {rp.get('n_sample_matches')}/{K} argmax {'Y' if rp.get('argmax_match') else 'N'}"
                         f" | bo8 plain {rec['plain']['best_by_ic']['ic']} attr {rec['attr']['best_by_ic']['ic']}"
                         f" | oz plain {rec['plain']['oz_ic_observation']} attr {rec['attr']['oz_ic_observation']}")
            elif "failed" not in rec:
                extra = (f" | oz plain {rec['plain']['oz']['ic']} attr {rec['attr']['oz']['ic']}"
                         f" | rnd8 plain {rec['plain']['random_best']['by_ic']['ic'] if rec['plain']['random_best'] else None}"
                         f" attr {rec['attr']['random_best']['by_ic']['ic'] if rec['attr']['random_best'] else None}")
            print(f"  {k}/{len(pending)} {rec['uri']}: {rec.get('failed', 'ok')[:120]} ({rec['seconds']}s){extra}",
                  flush=True)
    print(f"[{mode} seed={args.seed}] finished {len(pending)} in {(time.monotonic() - t0) / 60:.1f} min, "
          f"{n_fail} failed -> {sub}", flush=True)


# ----------------------------------------------------------------- summary
def summarize(out):
    programs = {p["uri"]: p for p in load_json(out / "programs.json")["programs"]}
    null = {}
    for f in glob.glob(str(out / "records_null" / "*.json")):
        if os.path.basename(f).startswith("manifest"):
            continue
        r = load_json(f)
        null[r["uri"]] = r
    gnn = {}
    for seed in SEEDS:
        for f in glob.glob(str(out / f"records_gnn_seed{seed}" / "*.json")):
            if os.path.basename(f).startswith("manifest"):
                continue
            r = load_json(f)
            gnn.setdefault(seed, {})[r["uri"]] = r

    def null_ok(r):
        return "failed" not in r and all(r[v]["random_best"] and r[v]["random_best"]["n_fail"] == 0 for v in VARIANTS)

    def gnn_ok(r):
        return "failed" not in r and all("best_by_ic" in r[v] and r[v]["n_fail"] == 0 for v in VARIANTS)

    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "programs": len(programs),
              "null_records": len(null), "null_ok": sum(null_ok(r) for r in null.values()),
              "null_failures": [{"uri": u, "error": r.get("failed", "candidate failure")} for u, r in null.items() if not null_ok(r)],
              "gnn": {}, "tables": {}, "baseline_change": {}, "reproduction": {}}
    metrics = ("ic", "text", "text_sec")
    for seed in SEEDS:
        recs = gnn.get(seed, {})
        ok = {u: r for u, r in recs.items() if gnn_ok(r)}
        common = sorted(u for u in ok if u in null and null_ok(null[u]))
        rep = [r["plain"]["reproduction"] for r in ok.values()]
        report["gnn"][str(seed)] = {
            "records": len(recs), "ok": len(ok), "common_with_null": len(common),
            "failures": [{"uri": u, "error": r.get("failed", "sample failure")} for u, r in recs.items() if not gnn_ok(r)],
            "missing": sorted(set(programs) - set(recs))}
        report["reproduction"][str(seed)] = {
            "programs_checked": len(rep),
            "all_8_samples_match": sum(x["sample_ics_match"] for x in rep),
            "sample_matches_total": sum(x["n_sample_matches"] for x in rep),
            "argmax_match": sum(x["argmax_match"] for x in rep),
            "best_of_8_match": sum(x["best_of_k_match"] for x in rep)}
        for suite in SUITES + ["ALL"]:
            us = [u for u in common if suite == "ALL" or programs[u]["suite"] == suite]
            if not us:
                continue
            row = {"n": len(us)}
            for v in VARIANTS:
                for m in metrics:
                    oz = sum(null[u][v]["oz"][m] for u in us)
                    g = sum(ok[u][v]["best_by_ic"][m] for u in us)
                    rn = sum(null[u][v]["random_best"]["by_ic"][m] for u in us)
                    am = sum(ok[u][v]["argmax"][m] for u in us)
                    w = sum(ok[u][v]["best_by_ic"][m] < null[u][v]["random_best"]["by_ic"][m] for u in us)
                    t = sum(ok[u][v]["best_by_ic"][m] == null[u][v]["random_best"]["by_ic"][m] for u in us)
                    row[f"{v}_{m}"] = {"oz": oz, "gnn_bo8": g, "random_bo8": rn, "argmax": am,
                                       "gnn_minus_random": g - rn,
                                       "gnn_minus_random_pct_of_oz": round(100 * (g - rn) / oz, 3) if oz else None,
                                       "gnn_gain_vs_oz_pct": round(100 * (oz - g) / oz, 3) if oz else None,
                                       "random_gain_vs_oz_pct": round(100 * (oz - rn) / oz, 3) if oz else None,
                                       "gnn_vs_random_wtl": f"{w}/{t}/{len(us) - w - t}"}
            if seed == SEEDS[0] or suite not in report["baseline_change"]:
                report["baseline_change"][suite] = {
                    "n": len(us),
                    **{m: {"oz_plain": sum(null[u]["plain"]["oz"][m] for u in us),
                           "oz_attr": sum(null[u]["attr"]["oz"][m] for u in us),
                           "change_pct": round(100 * (sum(null[u]["attr"]["oz"][m] for u in us) / max(sum(null[u]["plain"]["oz"][m] for u in us), 1) - 1), 3)}
                       for m in metrics}}
            report["tables"].setdefault(suite, {})[str(seed)] = row
    atomic_json(out / "summary.json", report)
    write_report(out, report)
    print(f"-> {out / 'summary.json'}, {out / 'REPORT.md'}")


def write_report(out, rep):
    L = ["# GNN sampler vs paired random null, with and without size attributes", "",
         f"Generated {rep['timestamp']}. Programs: {rep['programs']}. Null records ok: {rep['null_ok']}/{rep['null_records']}.", ""]
    for seed in SEEDS:
        g = rep["gnn"].get(str(seed), {})
        r = rep["reproduction"].get(str(seed), {})
        L.append(f"- seed {seed}: GNN records {g.get('records', 0)}, ok {g.get('ok', 0)}, common with null {g.get('common_with_null', 0)}, "
                 f"failures {len(g.get('failures', []))}, missing {len(g.get('missing', []))}; reproduction of the stored plain run: "
                 f"all 8 samples identical on {r.get('all_8_samples_match', 0)}/{r.get('programs_checked', 0)} programs, "
                 f"{r.get('sample_matches_total', 0)}/{K * max(r.get('programs_checked', 0), 1)} individual samples, "
                 f"argmax identical on {r.get('argmax_match', 0)}, best-of-8 identical on {r.get('best_of_8_match', 0)}")
    L += ["", "## Baseline change (service -Oz, attributes vs plain; n = common programs)", "",
          "| Suite | n | IC plain | IC attr | change | text plain | text attr | change | code plain | code attr | change |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for suite, b in rep["baseline_change"].items():
        L.append(f"| {suite} | {b['n']} | " + " | ".join(
            f"{b[m]['oz_plain']} | {b[m]['oz_attr']} | {b[m]['change_pct']:+.1f}%" for m in ("ic", "text", "text_sec")) + " |")
    for m, label in (("ic", "IC"), ("text", "Berkeley text"), ("text_sec", "code section")):
        L += ["", f"## GNN best-of-8 minus random best-of-8 ({label}; negative = GNN smaller). Gains are vs the same condition's -Oz.", "",
              "| Suite | seed | n | plain: GNN-rnd | % of Oz | W/T/L | GNN vs Oz | rnd vs Oz | attr: GNN-rnd | % of Oz | W/T/L | GNN vs Oz | rnd vs Oz |",
              "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|"]
        for suite, seeds in rep["tables"].items():
            for seed, row in seeds.items():
                p, a = row[f"plain_{m}"], row[f"attr_{m}"]
                L.append(f"| {suite} | {seed} | {row['n']} | {p['gnn_minus_random']:+d} | {p['gnn_minus_random_pct_of_oz']:+.2f}% | {p['gnn_vs_random_wtl']} | "
                         f"{p['gnn_gain_vs_oz_pct']:+.1f}% | {p['random_gain_vs_oz_pct']:+.1f}% | {a['gnn_minus_random']:+d} | {a['gnn_minus_random_pct_of_oz']:+.2f}% | "
                         f"{a['gnn_vs_random_wtl']} | {a['gnn_gain_vs_oz_pct']:+.1f}% | {a['random_gain_vs_oz_pct']:+.1f}% |")
    L += ["", "## Failures and exclusions", ""]
    L.append(f"- null: {len(rep['null_failures'])} " + ("; ".join(f"{x['uri']}: {x['error'][:80]}" for x in rep["null_failures"][:20]) if rep["null_failures"] else ""))
    for seed in SEEDS:
        g = rep["gnn"].get(str(seed), {})
        L.append(f"- gnn seed {seed}: {len(g.get('failures', []))} failed " +
                 ("; ".join(f"{x['uri']}: {x['error'][:80]}" for x in g.get("failures", [])[:20])) +
                 (f"; {len(g.get('missing', []))} not yet evaluated" if g.get("missing") else ""))
    L += ["", "The attribute condition adds `minsize optsize` to function definitions of the environment's module; "
          "it is not a source-level `clang -Oz` build (see results/baseline_audit/llvm10_source_check for that comparison)."]
    (out / "REPORT.md").write_text("\n".join(L) + "\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    p.add_argument("--prepare", action="store_true")
    p.add_argument("--null", action="store_true")
    p.add_argument("--seed", type=int, default=None, choices=SEEDS)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--pilot", type=int, default=0, help="first N programs of every suite")
    p.add_argument("--suites", nargs="*", default=[])
    p.add_argument("--uri", nargs="*", default=[])
    p.add_argument("--summarize", action="store_true")
    args = p.parse_args()
    if args.prepare:
        prepare(args.out)
    elif args.summarize:
        summarize(args.out)
    elif args.null or args.seed is not None:
        run(args)
    else:
        p.error("choose --prepare, --null, --seed S or --summarize")


if __name__ == "__main__":
    main()

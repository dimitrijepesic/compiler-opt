#!/usr/bin/env python3
"""Matched-budget byte-search pilot, contract paper/byte_optimizer_pilot_plan.md v2.

Question: at the same budget of 24 candidate attempts plus one -Oz reference,
do byte-guided local mutations find smaller code than fresh uniform random
sequences?  Nothing here assumes that they do.

Two arms per (program, random start 42/43/44), both from the same eight frozen
start sequences and the same attributed service -Oz reference:
  local    8 initial + 2 rounds x 8 mutations of the 4 smallest (code bytes)
  control  8 initial + 16 fresh uniform random sequences
The frozen audit helpers and records are only read.  All new data goes to
results/byte_local_search_v2/.

Modes (run inside the CompilerGym 0.2.5 container unless noted):
  --selftest            pure-Python tests of generation, fallback ties, budget
                        accounting, failure handling and resume (no container)
  --prepare             freeze manifest.json (refuses to overwrite)
  --run                 execute the pilot; atomic per-program records; resume
                        skips finished records of the same manifest and refuses
                        a directory written under another one
  --smoke URI --out DIR mechanics check on one NON-pilot program, outside the
                        results directory
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
OUT_DEFAULT = ROOT / "results" / "byte_local_search_v2"
SEL = ROOT / "results" / "selector_audit"
SOURCE_CHECK = ROOT / "results" / "size_portfolio_source_check" / "functional_checks.json"
REPORT_SCRIPT = ROOT / "scripts" / "report_byte_local_search_v2.py"

STARTS = [42, 43, 44]
STEPS, INIT, ROUNDS, PER_ROUND, BEAM, CONTROL_NEW, BUDGET = 45, 8, 2, 8, 4, 16, 24
METRICS = ("ic", "text", "text_sec")
HASHES = ("bitcode_sha256", "object_sha256")
# (slot, nominal parent rank in the beam, mutation kind); contract section "Frozen algorithm", step 3.
MUTATION_SLOTS = [(0, 0, "replace1"), (1, 1, "replace1"), (2, 2, "replace1"), (3, 3, "replace1"),
                  (4, 0, "swap"), (5, 1, "swap"), (6, 2, "replace2"), (7, 3, "replace1_swap")]

PROTOCOL = {
    "contract": "paper/byte_optimizer_pilot_plan.md (v2)",
    "starts": STARTS, "steps": STEPS, "initial": INIT, "rounds": ROUNDS, "mutations_per_round": PER_ROUND,
    "beam_width": BEAM, "control_fresh_sequences": CONTROL_NEW, "attempt_budget_per_arm": BUDGET,
    "reference_measurements_per_run": 1,
    "objective": "code-section bytes (text_sec) of the llc object; the search never reads Berkeley text",
    "mutation_slots": [{"slot": s, "parent_rank": p, "kind": k} for s, p, k in MUTATION_SLOTS],
    "rng_local": "numpy default_rng(int.from_bytes(sha256('byte-local-v2:{seed}:{uri}:{round}:{parent}:{mutation}')[:8],'big')); "
                 "round in {1,2}; parent = nominal beam rank of the slot; mutation = kind label",
    "rng_control": "numpy default_rng(int.from_bytes(sha256('byte-random-control-v2:{seed}:{uri}')[:8],'big')); "
                   "rng.choice(sorted 36 action ids, size=(16,45)); rows 0-7 are attempts 8-15, rows 8-15 attempts 16-23",
    "resolved_details": {
        "beam": "four smallest valid attempts so far by (text_sec, attempt index); attempt index is the global order 0-23 "
                "(initial 0-7 in frozen candidate order, round 1 = 8-15, round 2 = 16-23); older attempts win ties; "
                "no de-duplication by bytes, hashes or sequence",
        "short_beam": "with fewer than four valid attempts, slot parent rank p uses beam[p mod len(beam)]; with no valid "
                      "attempt the remaining mutation attempts are recorded as failed ('no valid parent'), not executed, and consume budget",
        "replace": "positions = rng.choice(45, size=n, replace=False); for each position in drawn order the new pass is "
                   "rng.choice(action ids different from the current pass at that position)",
        "swap": "i = rng.choice(indices with seq[i] != seq[i+1]); swap i and i+1; if no such index the sequence is "
                "unchanged, flagged ineffective, still executed and counted",
        "replace1_swap": "one replacement first, then the adjacent swap on the result, same generator",
        "execution": "every attempt is executed, including duplicates and ineffective mutations; nothing is cached within or "
                     "across arms, so each arm executes its own copy of the eight start sequences (24 executions per arm); "
                     "the -Oz reference is executed once per program and shared by its six runs (accounting: one per run)",
        "replay": "env.reset(attributed file URI) then env.multistep(actions, timeout=120), as in the frozen selector campaign",
        "failure": "an exception, a done flag, or a measurement error marks the attempt failed; it consumes budget, cannot "
                   "enter the beam and cannot be delivered; the environment is recreated after an exception; no retry",
        "fallback": "delivered = the -Oz object when its text_sec <= the best valid attempt's text_sec (ties go to -Oz)",
        "strict_secondary": "same attempts; a candidate is eligible only if text_sec <= -Oz text_sec and Berkeley text <= -Oz "
                            "Berkeley text; the search itself is unchanged",
        "start_verification": "each arm's replay of the eight start sequences must equal the frozen ic, text and text_sec; a "
                              "metric mismatch blocks that program (fail closed, no criteria evaluated); a hash-only difference "
                              "with equal metrics is recorded and reported, never waived silently",
        "input_baseline": "any input-identity or reference mismatch against the frozen selector audit blocks the program before any search",
        "curve": "best delivered bytes after the first 8, 16 and 24 attempts of each arm, always with the fallback",
        "functional_checks": "CHStone (existing fixed-vector self-tests) and, best effort, csmith (differential stdout/exit "
                             "code): link reference and delivered objects with 'clang -no-pie', run with a 30 s timeout; the "
                             "delivered program must exit 0 with the reference's stdout; other suites have no harness and are "
                             "reported as unchecked",
        "workers": "one worker, no concurrent campaign, so that the emulated timings are not contended",
    },
    "criteria": {
        "A_s": "per start s: 100 * sum_p(control24_bytes - local24_bytes) / sum_p(Oz_bytes) over the 12 programs (delivered bytes, with fallback)",
        "C1": "mean over the three starts of A_s >= 0.5",
        "C2": "A_s > 0 for at least two of the three starts",
        "C3": "mean over starts of A_s restricted to the 10 non-NPB programs > 0, and the per-suite mean over starts is > 0 in at least two of the five non-NPB suites",
        "C4": "no delivered object exceeds the -Oz text_sec (primary rule) and every available functional check passes; unchecked programs listed",
    },
    "timing_label": "amd64 container under Rosetta 2 on Apple silicon; describes this host only, not native optimization speed",
}


# ------------------------------------------------------------------ small helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_text(s: str) -> str:
    return sha_bytes(s.encode())


def digest(path) -> str:
    return sha_bytes(Path(path).read_bytes())


def uri_key(uri: str) -> str:
    return sha_text(uri)


def load_json(path):
    return json.loads(Path(path).read_text())


def atomic_json(path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, indent=1) + "\n")
    tmp.replace(path)


def fingerprint_of(manifest: dict) -> str:
    return sha_text(json.dumps({k: v for k, v in manifest.items() if k not in ("created", "fingerprint")}, sort_keys=True))


# ------------------------------------------------------------------ deterministic generation
def seed_from(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def frozen_start_sequences(replicate: int, uri: str, action_ids):
    """The frozen selector-audit rule; used only to confirm the recorded starts."""
    rng = np.random.default_rng(seed_from(f"{replicate}:{uri}"))
    return rng.choice(action_ids, size=(INIT, STEPS)).tolist()


def control_sequences(seed: int, uri: str, action_ids):
    rng = np.random.default_rng(seed_from(f"byte-random-control-v2:{seed}:{uri}"))
    return rng.choice(action_ids, size=(CONTROL_NEW, STEPS)).tolist()


def mutation_rng(seed: int, uri: str, rnd: int, parent_rank: int, kind: str):
    return np.random.default_rng(seed_from(f"byte-local-v2:{seed}:{uri}:{rnd}:{parent_rank}:{kind}"))


def mutate(parent, kind: str, rng, action_ids):
    seq = [int(a) for a in parent]
    detail = {"kind": kind, "replacements": [], "swap": None}

    def replace(n):
        for p in (int(x) for x in rng.choice(STEPS, size=n, replace=False)):
            others = [a for a in action_ids if a != seq[p]]
            new = int(rng.choice(others))
            detail["replacements"].append({"position": p, "old": seq[p], "new": new})
            seq[p] = new

    def swap():
        pairs = [i for i in range(STEPS - 1) if seq[i] != seq[i + 1]]
        if pairs:
            i = int(rng.choice(pairs))
            seq[i], seq[i + 1] = seq[i + 1], seq[i]
            detail["swap"] = {"position": i}

    if kind == "replace1":
        replace(1)
    elif kind == "replace2":
        replace(2)
    elif kind == "swap":
        swap()
    elif kind == "replace1_swap":
        replace(1)
        swap()
    else:
        raise ValueError(kind)
    detail["ineffective"] = seq == [int(a) for a in parent]
    return seq, detail


# ------------------------------------------------------------------ search logic (evaluator injected)
def beam_of(attempts):
    valid = [a for a in attempts if a["ok"]]
    return sorted(valid, key=lambda a: (a["text_sec"], a["attempt"]))[:BEAM]


def deliver(attempts, base, n, strict=False):
    pool = [a for a in attempts[:n] if a["ok"]]
    if strict:
        pool = [a for a in pool if a["text_sec"] <= base["text_sec"] and a["text"] <= base["text"]]
    best = min(pool, key=lambda a: (a["text_sec"], a["attempt"])) if pool else None
    if best is None or base["text_sec"] <= best["text_sec"]:
        return {"returned_reference": True, "attempt": None, "text_sec": base["text_sec"], "text": base["text"], "ic": base["ic"]}
    return {"returned_reference": False, "attempt": best["attempt"], "text_sec": best["text_sec"], "text": best["text"], "ic": best["ic"]}


def _attempt(index, origin, actions, result, **extra):
    a = {"attempt": index, "origin": origin, "actions": [int(x) for x in actions], **extra}
    a.update(result)
    a["ok"] = bool(result.get("ok"))
    return a


def run_local(evaluate, starts, seed, uri, action_ids):
    attempts, beams = [], []
    for j, seq in enumerate(starts):
        attempts.append(_attempt(len(attempts), "initial", seq, evaluate(seq, len(attempts)), start_index=j))
    for rnd in range(1, ROUNDS + 1):
        beam = beam_of(attempts)
        beams.append({"round": rnd, "parents": [{"rank": r, "attempt": b["attempt"], "text_sec": b["text_sec"]} for r, b in enumerate(beam)]})
        for slot, prank, kind in MUTATION_SLOTS:
            idx = len(attempts)
            if not beam:
                attempts.append(_attempt(idx, f"round{rnd}", [], {"ok": False, "error": "no valid parent", "executed": False},
                                         round=rnd, slot=slot, parent_rank=prank, kind=kind))
                continue
            parent = beam[prank % len(beam)]
            t0 = time.perf_counter()
            seq, detail = mutate(parent["actions"], kind, mutation_rng(seed, uri, rnd, prank, kind), action_ids)
            gen = time.perf_counter() - t0
            res = evaluate(seq, idx)
            attempts.append(_attempt(idx, f"round{rnd}", seq, res, round=rnd, slot=slot, parent_rank=prank, kind=kind,
                                     parent_attempt=parent["attempt"], mutation=detail, generation_s=gen))
    assert len(attempts) == BUDGET, len(attempts)
    return attempts, beams


def run_control(evaluate, starts, fresh):
    attempts = []
    for j, seq in enumerate(starts):
        attempts.append(_attempt(len(attempts), "initial", seq, evaluate(seq, len(attempts)), start_index=j))
    for j, seq in enumerate(fresh):
        attempts.append(_attempt(len(attempts), "fresh_random", seq, evaluate(seq, len(attempts)), fresh_index=j))
    assert len(attempts) == BUDGET, len(attempts)
    return attempts


def summarize_arm(attempts, base):
    out = {"executed": sum(1 for a in attempts if a.get("executed", True)), "attempt_count": len(attempts),
           "failed": sum(1 for a in attempts if not a["ok"]), "curve": {}, "curve_strict": {}}
    for n in (8, 16, 24):
        out["curve"][str(n)] = deliver(attempts, base, n)
        out["curve_strict"][str(n)] = deliver(attempts, base, n, strict=True)
    return out


def arm_record(attempts, base, frozen, wall_s, beams=None):
    """Everything stored for one arm of one run; the attempt list itself must survive."""
    rec = {"attempts": attempts, **({"beams": beams} if beams is not None else {}), "wall_s": wall_s,
           "start_verification": verify_starts(attempts, frozen)}
    summary = summarize_arm(attempts, base)
    assert not set(summary) & set(rec), set(summary) & set(rec)
    rec.update(summary)
    return rec


def verify_starts(attempts, frozen):
    """Compare an arm's replay of the eight start sequences with the frozen record."""
    rows, metric_ok, hash_ok = [], True, True
    for a, f in zip(attempts[:INIT], frozen):
        m = a["ok"] and all(a[k] == f[k] for k in METRICS)
        h = a["ok"] and all(a[k] == f[k] for k in HASHES)
        metric_ok &= bool(m)
        hash_ok &= bool(h)
        rows.append({"attempt": a["attempt"], "metrics_match": bool(m), "hashes_match": bool(h),
                     **({} if m and h else {"replayed": {k: a.get(k) for k in METRICS + HASHES}, "frozen": {k: f[k] for k in METRICS + HASHES}})})
    return {"metrics_match": metric_ok, "hashes_match": hash_ok, "rows": rows}


# ------------------------------------------------------------------ container side
class Cgym:
    def __init__(self):
        import compiler_gym
        import baseline_audit_cgym_matrix as audit
        self.cg, self.audit = compiler_gym, audit
        self.env = compiler_gym.make("llvm-v0")

    def renew(self):
        try:
            self.env.close()
        except Exception:
            pass
        self.env = self.cg.make("llvm-v0")

    def close(self):
        try:
            self.env.close()
        except Exception:
            pass

    def measure_timed(self, bc, obj):
        """Same quantities as audit.measure, timed by component and keeping the object."""
        a, t = self.audit, {}
        t0 = time.perf_counter()
        a.command([a.LLVM / "llc", "-filetype=obj", bc, "-o", obj])
        t["codegen_s"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        berk = int(a.command([a.LLVM / "llvm-size", obj]).splitlines()[1].split()[0])
        code, seen = 0, False
        for line in a.command([a.LLVM / "llvm-size", "-A", obj]).splitlines():
            p = line.split()
            if len(p) >= 2 and (p[0] in (".text", "__text") or p[0].startswith(".text.")):
                code += int(p[1])
                seen = True
        if not seen:
            raise AssertionError("no recognized code section")
        count = a.ic(bc)
        t["metric_s"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        hashes = {"bitcode_sha256": digest(bc), "object_sha256": digest(obj)}
        t["hash_s"] = time.perf_counter() - t0
        return {"ic": count, "text": berk, "text_sec": code, **hashes}, t

    def evaluator(self, vuri, wd, arm):
        d = Path(wd) / arm
        d.mkdir(parents=True, exist_ok=True)

        def evaluate(actions, index):
            timing = {"reset_s": 0.0, "optimize_s": 0.0, "export_s": 0.0, "codegen_s": 0.0, "metric_s": 0.0, "hash_s": 0.0}
            t_all = time.perf_counter()
            env_failed = True
            try:
                t0 = time.perf_counter()
                self.env.reset(benchmark=vuri)
                timing["reset_s"] = time.perf_counter() - t0
                t0 = time.perf_counter()
                _, _, done, info = self.env.multistep([int(x) for x in actions], timeout=120)
                timing["optimize_s"] = time.perf_counter() - t0
                if done:
                    raise RuntimeError(f"environment ended early: {info}")
                t0 = time.perf_counter()
                bc, obj = d / f"attempt_{index:02d}.bc", d / f"attempt_{index:02d}.o"
                self.env.write_bitcode(str(bc))
                ic_env = int(self.env.observation["IrInstructionCount"])
                timing["export_s"] = time.perf_counter() - t0
                env_failed = False
                m, t = self.measure_timed(bc, obj)
                timing.update(t)
                if m["ic"] != ic_env:
                    raise AssertionError(f"IC tool {m['ic']} != environment {ic_env}")
                res = {"ok": True, "executed": True, **m, "ic_env": ic_env}
            except Exception as e:
                res = {"ok": False, "executed": True, "error": repr(e)[:400]}
                if env_failed:
                    self.renew()
            timing["total_s"] = time.perf_counter() - t_all
            res["timing"] = timing
            return res
        return evaluate


def header_lines(audit, bc):
    ll = audit.command([audit.LLVM / "llvm-dis", bc, "-o", "-"])
    return {"triple": next((l for l in ll.splitlines() if l.startswith("target triple")), None),
            "datalayout": next((l for l in ll.splitlines() if l.startswith("target datalayout")), None)}


def run_executable(audit, obj, exe):
    try:
        audit.command([audit.LLVM / "clang", "-no-pie", obj, "-o", exe])
    except Exception as e:
        return {"linked": False, "error": repr(e)[:300]}
    try:
        r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=30)
        return {"linked": True, "exit_code": r.returncode, "stdout_sha256": sha_text(r.stdout), "stdout_len": len(r.stdout),
                "stdout": r.stdout if len(r.stdout) <= 2000 else None}
    except subprocess.TimeoutExpired:
        return {"linked": True, "timeout": True}
    except Exception as e:
        return {"linked": True, "error": repr(e)[:300]}


def functional_checks(cg, prog, base_obj, delivered, art):
    """delivered: {label: object path} for runs whose delivered object is a candidate."""
    suite = prog["suite"]
    if suite not in ("chstone-v0", "csmith-v0"):
        return {"status": "unchecked", "reason": "no functional harness for this suite"}
    if not delivered:
        return {"status": "not_needed", "reason": "every run delivered the reference object"}
    ref = run_executable(cg.audit, base_obj, art / "reference.elf")
    out = {"reference": ref, "delivered": {}}
    if not ref.get("linked") or ref.get("timeout") or ref.get("exit_code") != 0:
        out.update({"status": "unchecked", "reason": "reference object does not link, times out or exits non-zero"})
        return out
    if suite == "chstone-v0" and SOURCE_CHECK.exists():
        name = prog["uri"].split("/")[-1]
        old = next((p for p in load_json(SOURCE_CHECK)["programs"] if p["name"] == name), None)
        if old:
            out["reference_stdout_equals_source_build_stdout"] = sha_text(old["tests"]["real_clang_oz"]["stdout"]) == ref["stdout_sha256"]
    ok = True
    for label, obj in delivered.items():
        r = run_executable(cg.audit, obj, art / f"{label}.elf")
        r["passes"] = bool(r.get("linked") and not r.get("timeout") and r.get("exit_code") == 0
                           and r.get("stdout_sha256") == ref["stdout_sha256"])
        ok &= r["passes"]
        out["delivered"][label] = r
    out["status"] = "pass" if ok else "fail"
    return out


def execute_program(prog, manifest, out, cg=None):
    own = cg is None
    cg = cg or Cgym()
    audit, uri = cg.audit, prog["uri"]
    rec = {"uri": uri, "suite": prog["suite"], "fingerprint": manifest["fingerprint"], "complete": False, "blocked": False,
           "block_reasons": [], "timing_label": PROTOCOL["timing_label"]}
    t_start = time.monotonic()
    art = Path(out) / "artifacts" / uri_key(uri)
    try:
        with tempfile.TemporaryDirectory(prefix="byte-local-v2-") as temp:
            wd = Path(temp)
            env = cg.env
            t0 = time.perf_counter()
            env.reset(benchmark=uri)
            o0, oz = int(env.observation["IrInstructionCount"]), int(env.observation["IrInstructionCountOz"])
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
            ident = prog["identity"]
            ir_sha = audit.ir_digest(src)
            hp, ha = header_lines(audit, plain), header_lines(audit, src)
            checks = {
                "o0_matches_frozen": o0 == prog["o0"], "oz_matches_frozen": oz == prog["oz"],
                "input_sha256_matches_frozen": digest(src) == ident["input_sha256"],
                "ir_sha256_matches_frozen": ir_sha == ident["ir_sha256"],
                "ir_unchanged_on_load": audit.ir_digest(loaded) == ir_sha,
                "attribute_info_matches_frozen": info == ident["attribute_info"],
                "all_definitions_annotated": info["definitions"] == info["verified_size_definitions"],
                "attr_o0_unchanged": int(env.observation["IrInstructionCount"]) == o0,
                "attr_oz_observation_matches_frozen": int(env.observation["IrInstructionCountOz"]) == ident["oz_ic_observation"],
                "triple_datalayout_preserved": hp == ha and ha["triple"] is not None}
            rec["input"] = {"o0_ic": o0, "oz_ic_observation_plain": oz, "input_sha256": digest(src), "ir_sha256": ir_sha,
                            "attribute_info": info, "headers": ha, "checks": checks}
            # reference through the service
            env.reset(benchmark=vuri)
            t1 = time.perf_counter()
            env.send_param("llvm.apply_baseline_optimizations", "-Oz")
            t_opt = time.perf_counter() - t1
            art.mkdir(parents=True, exist_ok=True)
            bz, bo = art / "reference.bc", art / "reference.o"
            t1 = time.perf_counter()
            env.write_bitcode(str(bz))
            ic_env = int(env.observation["IrInstructionCount"])
            t_exp = time.perf_counter() - t1
            base, bt = cg.measure_timed(bz, bo)
            helper = audit.measure(bz, wd)
            st = prog["stored_attr_oz"]
            bchecks = {"ic_matches_observation": base["ic"] == ic_env == ident["oz_ic_observation"],
                       **{f"{k}_matches_frozen": base[k] == st[k] for k in METRICS + HASHES},
                       "timed_measure_equals_frozen_helper": base == helper}
            rec["reference"] = {**base, "ic_env": ic_env, "checks": bchecks,
                                "timing": {"optimize_s": t_opt, "export_s": t_exp, **bt}}
            rec["input_and_reference_s"] = time.perf_counter() - t0
            for name, c in (("input", checks), ("reference", bchecks)):
                rec["block_reasons"] += [f"{name}:{k}" for k, v in c.items() if not v]
            if rec["block_reasons"]:
                rec["blocked"] = True
            else:
                rec["runs"], delivered_objs = {}, {}
                for seed in manifest["protocol"]["starts"]:
                    s = prog["starts"][str(seed)]
                    t_g = time.perf_counter()
                    regenerated = control_sequences(seed, uri, manifest["action_ids"])
                    run = {"control_generation_s": time.perf_counter() - t_g}
                    if regenerated != prog["control_sequences"][str(seed)]:
                        rec["blocked"] = True
                        rec["block_reasons"].append(f"start {seed}: control sequences do not regenerate from the manifest rule")
                        rec["runs"][str(seed)] = run
                        continue
                    t_l = time.perf_counter()
                    la, beams = run_local(cg.evaluator(vuri, wd, f"s{seed}_local"), s["sequences"], seed, uri, manifest["action_ids"])
                    run["local"] = arm_record(la, base, s["frozen_candidates"], time.perf_counter() - t_l, beams)
                    t_c = time.perf_counter()
                    ca = run_control(cg.evaluator(vuri, wd, f"s{seed}_control"), s["sequences"], prog["control_sequences"][str(seed)])
                    run["control"] = arm_record(ca, base, s["frozen_candidates"], time.perf_counter() - t_c)
                    for arm in ("local", "control"):
                        if not run[arm]["start_verification"]["metrics_match"]:
                            rec["blocked"] = True
                            rec["block_reasons"].append(f"start {seed} {arm}: replayed start metrics differ from the frozen record")
                        for rule in ("curve", "curve_strict"):
                            dl = run[arm][rule]["24"]
                            if not dl["returned_reference"]:
                                label = f"s{seed}_{arm}_{'strict' if rule == 'curve_strict' else 'primary'}"
                                a = dl["attempt"]
                                for ext in ("bc", "o"):
                                    shutil.copyfile(wd / f"s{seed}_{arm}" / f"attempt_{a:02d}.{ext}", art / f"{label}.{ext}")
                                delivered_objs[label] = art / f"{label}.o"
                    rec["runs"][str(seed)] = run
                rec["functional"] = functional_checks(cg, prog, bo, delivered_objs, art)
            rec["complete"] = True
    except Exception as e:
        rec["failed"] = repr(e)[:1200]
        cg.renew()
    rec["seconds"] = round(time.monotonic() - t_start, 2)
    if own:
        cg.close()
    return rec


# ------------------------------------------------------------------ manifest
def build_manifest(image_id=None):
    import compiler_gym
    import baseline_audit_cgym_matrix as audit
    sel_inputs, sel_manifest = load_json(SEL / "inputs.json"), load_json(SEL / "manifest.json")
    action_ids = sel_inputs["action_ids"]
    assert len(action_ids) == 36 and action_ids == sorted(action_ids)
    ic_tool = subprocess.run(["which", "ic"], capture_output=True, text=True).stdout.strip()
    tools = {"compiler_gym": compiler_gym.__version__, "numpy": np.__version__,
             "llvm_version": audit.command([audit.LLVM / "opt", "--version"]).strip(),
             "ic_tool_sha256": digest(ic_tool) if ic_tool else None, "helper_sha256": digest(audit.__file__)}
    for k, v in tools.items():
        if sel_manifest[k] != v:
            raise SystemExit(f"tool mismatch against the frozen selector audit: {k}: {v!r} != {sel_manifest[k]!r}")
    programs = []
    for uri in sel_inputs["pilot_uris"]:
        p = next(x for x in sel_inputs["programs"] if x["uri"] == uri)
        key = uri_key(uri)
        campaign, pilot = load_json(SEL / "records" / f"{key}.json"), load_json(SEL / "pilot" / f"{key}.json")
        g0 = p["gnn"]["42"]
        entry = {"uri": uri, "suite": p["suite"], "o0": p["o0"], "oz": p["oz"], "stored_attr_oz": p["stored_attr_oz"],
                 "identity": {"input_sha256": g0["input_sha256"], "ir_sha256": g0["ir_sha256"],
                              "oz_ic_observation": g0["oz_ic_observation"], "attribute_info": p["attribute_info"]},
                 "frozen_sources": {"campaign_record_sha256": digest(SEL / "records" / f"{key}.json"),
                                    "pilot_record_sha256": digest(SEL / "pilot" / f"{key}.json")},
                 "starts": {}, "control_sequences": {}}
        assert campaign["baseline"]["text_sec"] == p["stored_attr_oz"]["text_sec"]
        for seed in STARTS:
            seqs = p["random"][str(seed)]["sequences"]
            if seqs != frozen_start_sequences(seed, uri, action_ids):
                raise SystemExit(f"{uri}: start {seed} does not regenerate from the frozen rule")
            frozen = [{k: c[k] for k in METRICS + HASHES} for c in campaign["random"][str(seed)]["candidates"]]
            pil = pilot["random"][str(seed)]
            pil_c = pil.get("pilot_replay") or pil["candidates"]
            for f, q in zip(frozen, pil_c):
                if any(f[k] != q[k] for k in METRICS):
                    raise SystemExit(f"{uri}: start {seed}: frozen campaign and pilot metrics disagree")
            assert [c["actions"] for c in campaign["random"][str(seed)]["candidates"]] == seqs
            entry["starts"][str(seed)] = {"sequences": seqs, "frozen_candidates": frozen,
                                          "frozen_hashes_equal_in_pilot_and_campaign": all(
                                              f[k] == q[k] for f, q in zip(frozen, pil_c) for k in HASHES)}
            entry["control_sequences"][str(seed)] = control_sequences(seed, uri, action_ids)
        programs.append(entry)
    m = {"schema": 1, "created": datetime.now(timezone.utc).isoformat(), "protocol": PROTOCOL,
         "pilot_uris": sel_inputs["pilot_uris"], "action_ids": action_ids, "programs": programs,
         "sources": {"script_sha256": digest(__file__), "report_script_sha256": digest(REPORT_SCRIPT),
                     "contract_sha256": digest(ROOT / "paper" / "byte_optimizer_pilot_plan.md"),
                     "selector_inputs_sha256": digest(SEL / "inputs.json"),
                     "selector_manifest_fingerprint": sel_manifest["fingerprint"],
                     "passes_yaml_sha256": digest(ROOT / "configs" / "passes.yaml")},
         "tools": {**tools, "python": platform.python_version(), "machine": platform.machine(),
                   "container_image_id": image_id}}
    m["fingerprint"] = fingerprint_of(m)
    return m


# ------------------------------------------------------------------ driver
def check_manifest(manifest, script=__file__, report=REPORT_SCRIPT):
    if manifest.get("fingerprint") != fingerprint_of(manifest):
        raise SystemExit("manifest.json does not match its own fingerprint: it was edited after --prepare")
    if manifest["sources"]["script_sha256"] != digest(script):
        raise SystemExit("the runner changed since --prepare: start a new output directory with a new manifest")
    if manifest["sources"]["report_script_sha256"] != digest(report):
        raise SystemExit("the report script changed since --prepare: start a new output directory with a new manifest")


def run_programs(out, manifest, execute, uris=None, log=print):
    """Resume-safe loop.  `execute(prog)` returns the record; tests inject a fake."""
    out = Path(out)
    rec_dir = out / "records"
    rec_dir.mkdir(parents=True, exist_ok=True)
    fp = manifest["fingerprint"]
    run_manifest = rec_dir / "run_manifest.json"
    if run_manifest.exists() and load_json(run_manifest)["fingerprint"] != fp:
        raise SystemExit(f"{rec_dir} was written under another manifest: use a new output directory")
    pending, done = [], 0
    for prog in manifest["programs"]:
        if uris and prog["uri"] not in uris:
            continue
        path = rec_dir / f"{uri_key(prog['uri'])}.json"
        if path.exists():
            old = load_json(path)
            if old.get("fingerprint") != fp:
                raise SystemExit(f"{path.name} belongs to another manifest: refusing to mix or overwrite")
            if old.get("complete") and "failed" not in old:
                done += 1
                continue
            # A crashed program is retried, but its failed record is kept, never overwritten.
            keep = rec_dir / "failed_attempts"
            keep.mkdir(exist_ok=True)
            path.replace(keep / f"{path.stem}.{len(list(keep.glob(path.stem + '.*.json')))}.json")
        pending.append((prog, path))
    log(f"{done} done, {len(pending)} pending, manifest {fp[:16]}")
    lock = (rec_dir / ".run.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another process is writing {rec_dir}")
    if not run_manifest.exists():
        atomic_json(run_manifest, {"fingerprint": fp, "started": datetime.now(timezone.utc).isoformat(),
                                   "command": " ".join(sys.argv), "workers": 1, "hardware": PROTOCOL["timing_label"]})
    for k, (prog, path) in enumerate(pending, 1):
        rec = execute(prog)
        atomic_json(path, rec)
        state = "FAILED " + rec["failed"][:80] if "failed" in rec else ("BLOCKED " + "; ".join(rec["block_reasons"])[:120] if rec.get("blocked") else "ok")
        log(f"  {k}/{len(pending)} {prog['uri']}: {state} ({rec.get('seconds')}s)")
    lock.close()
    return len(pending)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--smoke", metavar="URI")
    ap.add_argument("--image-id")
    ap.add_argument("--uri", nargs="*", default=[])
    args = ap.parse_args()
    if args.selftest:
        import test_byte_local_search_v2 as t
        raise SystemExit(t.main())
    if args.prepare:
        path = args.out / "manifest.json"
        if path.exists():
            raise SystemExit(f"{path} exists: the manifest is frozen; use a new output directory")
        m = build_manifest(args.image_id)
        atomic_json(path, m)
        print(f"manifest frozen: {len(m['programs'])} programs, fingerprint {m['fingerprint'][:16]} -> {path}")
    elif args.smoke:
        if args.out.resolve() == OUT_DEFAULT.resolve():
            raise SystemExit("--smoke needs an --out outside the results directory")
        sel_inputs = load_json(SEL / "inputs.json")
        if args.smoke in sel_inputs["pilot_uris"]:
            raise SystemExit("--smoke refuses pilot programs")
        base_m = build_manifest(args.image_id)
        p = next(x for x in sel_inputs["programs"] if x["uri"] == args.smoke)
        key = uri_key(p["uri"])
        campaign = load_json(SEL / "records" / f"{key}.json")
        prog = {"uri": p["uri"], "suite": p["suite"], "o0": p["o0"], "oz": p["oz"], "stored_attr_oz": p["stored_attr_oz"],
                "identity": {"input_sha256": p["gnn"]["42"]["input_sha256"], "ir_sha256": p["gnn"]["42"]["ir_sha256"],
                             "oz_ic_observation": p["gnn"]["42"]["oz_ic_observation"], "attribute_info": p["attribute_info"]},
                "starts": {str(s): {"sequences": p["random"][str(s)]["sequences"],
                                    "frozen_candidates": [{k: c[k] for k in METRICS + HASHES} for c in campaign["random"][str(s)]["candidates"]]}
                           for s in STARTS},
                "control_sequences": {str(s): control_sequences(s, p["uri"], base_m["action_ids"]) for s in STARTS}}
        m = {**base_m, "programs": [prog], "pilot_uris": [], "smoke": True}
        m["fingerprint"] = fingerprint_of(m)
        atomic_json(args.out / "manifest.json", m)
        rec = execute_program(prog, m, args.out)
        atomic_json(args.out / "records" / f"{key}.json", rec)
        print(json.dumps({k: rec.get(k) for k in ("uri", "complete", "blocked", "block_reasons", "failed", "seconds")}, indent=1))
    elif args.run:
        manifest = load_json(args.out / "manifest.json")
        check_manifest(manifest)
        cg = Cgym()
        try:
            run_programs(args.out, manifest, lambda prog: execute_program(prog, manifest, args.out, cg), set(args.uri) or None)
        finally:
            cg.close()
    else:
        ap.error("choose --selftest, --prepare, --run or --smoke")


if __name__ == "__main__":
    main()

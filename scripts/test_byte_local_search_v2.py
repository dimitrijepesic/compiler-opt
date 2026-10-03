#!/usr/bin/env python3
"""Tests for scripts/byte_local_search_v2.py.  Pure Python: no container, no compiler.

Each test names the failure it is meant to catch.  Run:
    python3 scripts/test_byte_local_search_v2.py      (or the runner's --selftest)
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import traceback
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import byte_local_search_v2 as B  # noqa: E402

IDS = [1, 2, 8, 10, 16, 21, 24, 25, 26, 29, 30, 31, 33, 38, 39, 41, 46, 52, 53, 55, 59, 66, 72, 83, 90, 91, 93, 96, 97,
       103, 104, 105, 109, 110, 111, 117]
URI = "benchmark://unit-test/1"


def seed_independent(text):
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big")


def starts(seed=7):
    return np.random.default_rng(seed).choice(IDS, size=(8, 45)).tolist()


def fake_evaluator(fail=lambda seq, idx: False, size=None):
    """Deterministic 'compiler': bytes depend only on the sequence."""
    calls = []
    size = size or (lambda seq: 1000 + sum((i + 1) * a for i, a in enumerate(seq)) % 400)

    def evaluate(seq, idx):
        calls.append(list(seq))
        if fail(seq, idx):
            return {"ok": False, "executed": True, "error": "injected"}
        b = size(seq)
        return {"ok": True, "executed": True, "ic": b // 4, "text": b + 100, "text_sec": b,
                "bitcode_sha256": "b", "object_sha256": "o"}
    return evaluate, calls


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ------------------------------------------------------------------ 1. deterministic generation
def test_rng_namespaces_match_the_contract():
    """Catches a typo or reordering in either RNG namespace string, or a changed draw order."""
    expect = np.random.default_rng(seed_independent(f"byte-random-control-v2:43:{URI}")).choice(IDS, size=(16, 45)).tolist()
    assert B.control_sequences(43, URI, IDS) == expect
    parent = starts()[0]
    rng = np.random.default_rng(seed_independent(f"byte-local-v2:44:{URI}:2:3:replace1"))
    p = int(rng.choice(45, size=1, replace=False)[0])
    new = int(rng.choice([a for a in IDS if a != parent[p]]))
    want = list(parent)
    want[p] = new
    got, detail = B.mutate(parent, "replace1", B.mutation_rng(44, URI, 2, 3, "replace1"), IDS)
    assert got == want and detail["replacements"] == [{"position": p, "old": parent[p], "new": new}]


def test_frozen_start_rule_regenerates_recorded_starts():
    """Catches RNG stream drift of this interpreter against the frozen campaign."""
    inp = json.loads((B.SEL / "inputs.json").read_text())
    assert inp["action_ids"] == IDS
    for uri in inp["pilot_uris"]:
        prog = next(x for x in inp["programs"] if x["uri"] == uri)
        for seed in B.STARTS:
            assert B.frozen_start_sequences(seed, uri, IDS) == prog["random"][str(seed)]["sequences"], (uri, seed)


def test_generation_is_repeatable_and_namespaced():
    """Catches hidden global RNG state and namespaces that collide."""
    parent = starts()[1]
    a = B.mutate(parent, "replace2", B.mutation_rng(42, URI, 1, 2, "replace2"), IDS)
    assert a == B.mutate(parent, "replace2", B.mutation_rng(42, URI, 1, 2, "replace2"), IDS)
    assert B.control_sequences(42, URI, IDS) == B.control_sequences(42, URI, IDS)
    variants = {json.dumps(B.mutate(parent, k, B.mutation_rng(s, u, r, p, k), IDS)[0])
                for s, u, r, p, k in [(42, URI, 1, 2, "replace2"), (43, URI, 1, 2, "replace2"), (42, URI + "x", 1, 2, "replace2"),
                                      (42, URI, 2, 2, "replace2"), (42, URI, 1, 3, "replace2")]}
    assert len(variants) == 5
    assert B.control_sequences(42, URI, IDS) != B.control_sequences(43, URI, IDS)


def test_mutation_invariants():
    """Catches replacements that keep the old pass, repeated positions, non-adjacent or equal-pair swaps."""
    rng0 = np.random.default_rng(11)
    for n in range(300):
        parent = rng0.choice(IDS, size=45).tolist()
        for kind in ("replace1", "replace2", "swap", "replace1_swap"):
            seq, d = B.mutate(parent, kind, np.random.default_rng(n), IDS)
            assert len(seq) == 45 and all(a in IDS for a in seq)
            diff = [i for i in range(45) if seq[i] != parent[i]]
            if kind == "replace1":
                assert len(diff) == 1 and len(d["replacements"]) == 1
            if kind == "replace2":
                assert len(diff) == 2 and len({r["position"] for r in d["replacements"]}) == 2
            if kind == "swap":
                assert Counter(seq) == Counter(parent) and len(diff) == 2 and diff[1] == diff[0] + 1
                assert parent[diff[0]] != parent[diff[1]]
            if kind == "replace1_swap":
                assert 1 <= len(diff) <= 3 and d["swap"] is not None
            for r in d["replacements"]:
                assert r["new"] != r["old"] and parent[r["position"]] == r["old"]
            assert d["ineffective"] == (seq == parent)


def test_swap_without_unequal_pair_is_ineffective_but_counted():
    """Catches a free retry or a crash when no unequal adjacent pair exists."""
    flat = [IDS[0]] * 45
    seq, d = B.mutate(flat, "swap", np.random.default_rng(1), IDS)
    assert seq == flat and d["ineffective"] and d["swap"] is None
    seq, d = B.mutate(flat, "replace1_swap", np.random.default_rng(1), IDS)
    assert d["swap"] is not None and seq != flat
    ev, calls = fake_evaluator()
    attempts, _ = B.run_local(ev, [flat] * 8, 42, URI, IDS)
    assert len(attempts) == 24 and len(calls) == 24
    assert any(a.get("mutation", {}).get("ineffective") for a in attempts)


# ------------------------------------------------------------------ 2. fallback and ties
def cand(i, code, text=None, ok=True):
    return {"attempt": i, "ok": ok, "text_sec": code, "text": text if text is not None else code + 100, "ic": 1}


def test_fallback_tie_goes_to_reference():
    """Catches '<' vs '<=' in the fallback, and failed candidates winning."""
    base = {"text_sec": 500, "text": 600, "ic": 9}
    assert B.deliver([cand(0, 500)], base, 24)["returned_reference"] is True
    d = B.deliver([cand(0, 499)], base, 24)
    assert d == {"returned_reference": False, "attempt": 0, "text_sec": 499, "text": 599, "ic": 1}
    assert B.deliver([cand(0, 1, ok=False)], base, 24)["returned_reference"] is True
    assert B.deliver([], base, 24)["text_sec"] == 500
    assert B.deliver([cand(0, 480), cand(1, 480)], base, 24)["attempt"] == 0      # older attempt wins a tie
    assert B.deliver([cand(i, 490 if i < 20 else 400) for i in range(24)], base, 16)["text_sec"] == 490   # budget prefix


def test_strict_rule_protects_both_metrics_without_changing_search():
    """Catches a strict rule that ignores Berkeley text, or that rejects an exact Berkeley tie."""
    base = {"text_sec": 500, "text": 600, "ic": 9}
    pool = [cand(0, 450, text=650), cand(1, 470, text=600), cand(2, 460, text=601)]
    assert B.deliver(pool, base, 24)["attempt"] == 0
    assert B.deliver(pool, base, 24, strict=True)["attempt"] == 1
    assert B.deliver([cand(0, 450, text=650)], base, 24, strict=True)["returned_reference"] is True


# ------------------------------------------------------------------ 3. budget accounting and beam
def test_budget_and_parent_assignment():
    """Catches wrong attempt counts, wrong parents, a beam that is not the 4 smallest, and wrong tie order."""
    ev, calls = fake_evaluator()
    st = starts()
    attempts, beams = B.run_local(ev, st, 42, URI, IDS)
    assert len(calls) == 24 and [a["attempt"] for a in attempts] == list(range(24))
    assert [a["origin"] for a in attempts] == ["initial"] * 8 + ["round1"] * 8 + ["round2"] * 8
    assert [a["actions"] for a in attempts[:8]] == st
    for rnd, lo in ((1, 8), (2, 16)):
        beam = sorted(attempts[:lo], key=lambda a: (a["text_sec"], a["attempt"]))[:4]
        assert [p["attempt"] for p in beams[rnd - 1]["parents"]] == [b["attempt"] for b in beam]
        for a, (slot, prank, kind) in zip(attempts[lo:lo + 8], B.MUTATION_SLOTS):
            assert (a["slot"], a["parent_rank"], a["kind"]) == (slot, prank, kind)
            assert a["parent_attempt"] == beam[prank]["attempt"]
            assert 1 <= hamming(a["actions"], beam[prank]["actions"]) <= 3        # derived from that parent, not another
    assert [k for _, _, k in B.MUTATION_SLOTS] == ["replace1"] * 4 + ["swap"] * 2 + ["replace2", "replace1_swap"]
    assert [p for _, p, _ in B.MUTATION_SLOTS] == [0, 1, 2, 3, 0, 1, 2, 3]
    ev2, calls2 = fake_evaluator()
    fresh = B.control_sequences(42, URI, IDS)
    ctrl = B.run_control(ev2, st, fresh)
    assert len(calls2) == 24 and [a["actions"] for a in ctrl] == st + fresh
    s = B.summarize_arm(ctrl, {"text_sec": 10 ** 6, "text": 10 ** 6, "ic": 1})
    assert s["attempt_count"] == 24 and s["executed"] == 24 and s["failed"] == 0
    best = [min(a["text_sec"] for a in ctrl[:n]) for n in (8, 16, 24)]
    assert [s["curve"][str(n)]["text_sec"] for n in (8, 16, 24)] == best and best[0] >= best[1] >= best[2]


def test_arm_record_keeps_the_attempt_list():
    """Catches the summary overwriting the per-attempt list (found by the smoke run: 'attempts' became the integer 24)."""
    ev, _ = fake_evaluator()
    st = starts()
    attempts, beams = B.run_local(ev, st, 42, URI, IDS)
    frozen = [{k: a[k] for k in B.METRICS + B.HASHES} for a in attempts[:8]]
    rec = B.arm_record(attempts, {"text_sec": 10 ** 6, "text": 10 ** 6, "ic": 1}, frozen, 1.5, beams)
    assert isinstance(rec["attempts"], list) and len(rec["attempts"]) == 24 and rec["attempts"][8]["kind"] == "replace1"
    assert rec["attempt_count"] == 24 and rec["beams"] == beams and rec["start_verification"]["metrics_match"]
    assert set(rec["curve"]) == {"8", "16", "24"} == set(rec["curve_strict"])
    json.dumps(rec)


def test_beam_tie_break_prefers_older_attempts():
    """Catches a beam that lets a merely-equal mutant displace its parent."""
    ev, _ = fake_evaluator(size=lambda seq: 777)
    attempts, beams = B.run_local(ev, starts(), 42, URI, IDS)
    assert [p["attempt"] for p in beams[0]["parents"]] == [0, 1, 2, 3]
    assert [p["attempt"] for p in beams[1]["parents"]] == [0, 1, 2, 3]


# ------------------------------------------------------------------ 4. failures
def test_failed_attempts_consume_budget_and_never_win():
    """Catches failed attempts entering the beam, being delivered, or being retried for free."""
    ev, calls = fake_evaluator(fail=lambda seq, idx: idx in (0, 3, 9, 17))
    attempts, beams = B.run_local(ev, starts(), 42, URI, IDS)
    assert len(calls) == 24 and [a["attempt"] for a in attempts if not a["ok"]] == [0, 3, 9, 17]
    for b in beams:
        assert not {p["attempt"] for p in b["parents"]} & {0, 3, 9, 17}
    s = B.summarize_arm(attempts, {"text_sec": 10 ** 6, "text": 10 ** 6, "ic": 1})
    assert s["failed"] == 4 and s["curve"]["24"]["attempt"] not in (0, 3, 9, 17)


def test_all_initial_failures_do_not_invent_candidates():
    """Catches a crash or silent budget shrink when nothing valid exists."""
    ev, calls = fake_evaluator(fail=lambda seq, idx: True)
    attempts, _ = B.run_local(ev, starts(), 42, URI, IDS)
    assert len(attempts) == 24 and len(calls) == 8
    assert all(not a["ok"] for a in attempts) and all(a["executed"] is False for a in attempts[8:])
    base = {"text_sec": 500, "text": 600, "ic": 9}
    s = B.summarize_arm(attempts, base)
    assert (s["attempt_count"], s["executed"], s["failed"]) == (24, 8, 24) and s["curve"]["24"]["returned_reference"]


def test_short_beam_reuses_parents_by_rank_modulo():
    """Catches an IndexError or a dropped slot when fewer than four attempts are valid."""
    ev, calls = fake_evaluator(fail=lambda seq, idx: idx not in (2, 5) and idx < 8)
    attempts, beams = B.run_local(ev, starts(), 42, URI, IDS)
    assert len(calls) == 24 and len(beams[0]["parents"]) == 2
    order = [p["attempt"] for p in beams[0]["parents"]]
    assert [a["parent_attempt"] for a in attempts[8:16]] == [order[p % 2] for _, p, _ in B.MUTATION_SLOTS]


def test_real_evaluator_failure_paths():
    """Catches an exception escaping the evaluator, and an environment that is not renewed after a service error."""
    class Env:
        def __init__(self, boom):
            self.boom, self.observation = boom, {"IrInstructionCount": 5}
        def reset(self, benchmark=None):
            pass
        def multistep(self, actions, timeout=None):
            if self.boom == "raise":
                raise RuntimeError("service died")
            return None, None, self.boom == "done", {"why": "x"}
        def write_bitcode(self, p):
            Path(p).write_bytes(b"bc")
    for boom, renewed in (("raise", 1), ("done", 1), ("measure", 0)):
        cg = B.Cgym.__new__(B.Cgym)
        cg.env, n = Env(boom), []
        cg.renew = lambda n=n: n.append(1)
        cg.measure_timed = lambda bc, obj: (_ for _ in ()).throw(RuntimeError("llc failed"))
        with tempfile.TemporaryDirectory() as t:
            res = cg.evaluator("file:///x", t, "arm")([1, 2, 3], 0)
        assert res["ok"] is False and res["executed"] is True and "error" in res and len(n) == renewed, (boom, res, n)
        assert set(res["timing"]) >= {"reset_s", "optimize_s", "export_s", "codegen_s", "metric_s", "hash_s", "total_s"}


def test_start_verification_distinguishes_metrics_from_hashes():
    """Catches a hash-only difference being reported as a metric mismatch, or the reverse being waived."""
    frozen = [{"ic": 1, "text": 2, "text_sec": 3, "bitcode_sha256": "a", "object_sha256": "b"}] * 8
    good = [dict(f, attempt=i, ok=True) for i, f in enumerate(frozen)]
    assert B.verify_starts(good, frozen) == {"metrics_match": True, "hashes_match": True,
                                             "rows": [{"attempt": i, "metrics_match": True, "hashes_match": True} for i in range(8)]}
    hash_only = [dict(g) for g in good]
    hash_only[4]["object_sha256"] = "z"
    v = B.verify_starts(hash_only, frozen)
    assert v["metrics_match"] and not v["hashes_match"] and v["rows"][4]["replayed"]["object_sha256"] == "z"
    bad = [dict(g) for g in good]
    bad[1]["text_sec"] = 4
    assert not B.verify_starts(bad, frozen)["metrics_match"]
    failed = [dict(g) for g in good]
    failed[0] = {"attempt": 0, "ok": False, "error": "x"}
    assert not B.verify_starts(failed, frozen)["metrics_match"]


# ------------------------------------------------------------------ 5. manifest-safe resume
def manifest(n=3, tweak=None):
    m = {"schema": 1, "created": "t", "protocol": {"starts": [42]}, "action_ids": list(IDS),
         "programs": [{"uri": f"benchmark://unit/{i}", "suite": "s"} for i in range(n)]}
    if tweak:
        tweak(m)
    m["fingerprint"] = B.fingerprint_of(m)
    return m


def executor(m, calls, fail_on=(), crash_on=()):
    def ex(prog):
        calls.append(prog["uri"])
        if prog["uri"] in crash_on:
            raise RuntimeError("killed")
        rec = {"uri": prog["uri"], "fingerprint": m["fingerprint"], "complete": True, "seconds": 0}
        if prog["uri"] in fail_on:
            rec.update({"complete": False, "failed": "boom"})
        return rec
    return ex


def test_resume_skips_completed_records_and_keeps_them_byte_identical():
    """Catches re-execution or rewriting of finished records."""
    m = manifest()
    with tempfile.TemporaryDirectory() as t:
        calls = []
        assert B.run_programs(t, m, executor(m, calls), log=lambda s: None) == 3 and len(calls) == 3
        before = {p.name: p.read_bytes() for p in (Path(t) / "records").glob("*.json")}
        calls.clear()
        assert B.run_programs(t, m, executor(m, calls), log=lambda s: None) == 0 and calls == []
        assert before == {p.name: p.read_bytes() for p in (Path(t) / "records").glob("*.json")}


def test_changed_manifest_is_rejected_and_nothing_is_touched():
    """Catches results of two protocols being mixed in one directory."""
    m = manifest()
    with tempfile.TemporaryDirectory() as t:
        B.run_programs(t, m, executor(m, []), log=lambda s: None)
        before = {p.name: p.read_bytes() for p in (Path(t) / "records").glob("*.json")}
        m2 = manifest(tweak=lambda x: x["action_ids"].__setitem__(0, 999))
        assert m2["fingerprint"] != m["fingerprint"]
        calls = []
        try:
            B.run_programs(t, m2, executor(m2, calls), log=lambda s: None)
            raise AssertionError("changed manifest accepted")
        except SystemExit:
            pass
        assert calls == [] and before == {p.name: p.read_bytes() for p in (Path(t) / "records").glob("*.json")}
        (Path(t) / "records" / "run_manifest.json").unlink()            # even without the run manifest, records are checked
        try:
            B.run_programs(t, m2, executor(m2, calls), log=lambda s: None)
            raise AssertionError("foreign records accepted")
        except SystemExit:
            pass
        assert calls == []


def test_edited_manifest_or_script_is_detected():
    """Catches an edited manifest with a stale fingerprint, and a runner or report edited after --prepare."""
    with tempfile.TemporaryDirectory() as t:
        script, report = Path(t) / "s.py", Path(t) / "r.py"
        script.write_text("a")
        report.write_text("b")
        m = manifest(tweak=lambda x: x.update({"sources": {"script_sha256": B.digest(script), "report_script_sha256": B.digest(report)}}))
        B.check_manifest(m, script, report)
        for change in (lambda: m["action_ids"].append(5), lambda: script.write_text("a2"), lambda: report.write_text("b2")):
            m_ok = json.loads(json.dumps(m))
            change()
            try:
                B.check_manifest(m, script, report)
                raise AssertionError("change not detected")
            except SystemExit:
                pass
            m.clear()
            m.update(m_ok)
            script.write_text("a")
            report.write_text("b")


def test_crash_leaves_completed_records_and_no_partial_file():
    """Catches partial JSON or lost records when the process dies mid-program."""
    m = manifest()
    with tempfile.TemporaryDirectory() as t:
        calls = []
        try:
            B.run_programs(t, m, executor(m, calls, crash_on={"benchmark://unit/1"}), log=lambda s: None)
            raise AssertionError("crash swallowed")
        except RuntimeError:
            pass
        rec = Path(t) / "records"
        files = sorted(p.name for p in rec.glob("*.json"))
        assert files == sorted([B.uri_key("benchmark://unit/0") + ".json", "run_manifest.json"]), files
        assert not list(rec.glob("*.tmp.*"))
        json.loads((rec / (B.uri_key("benchmark://unit/0") + ".json")).read_text())
        calls.clear()
        B.run_programs(t, m, executor(m, calls), log=lambda s: None)
        assert calls == ["benchmark://unit/1", "benchmark://unit/2"]


def test_failed_program_is_retried_and_its_failed_record_is_kept():
    """Catches a failure record being overwritten by the retry."""
    m = manifest()
    with tempfile.TemporaryDirectory() as t:
        B.run_programs(t, m, executor(m, [], fail_on={"benchmark://unit/2"}), log=lambda s: None)
        calls = []
        B.run_programs(t, m, executor(m, calls), log=lambda s: None)
        assert calls == ["benchmark://unit/2"]
        kept = list((Path(t) / "records" / "failed_attempts").glob("*.json"))
        assert len(kept) == 1 and json.loads(kept[0].read_text())["failed"] == "boom"
        assert "failed" not in json.loads((Path(t) / "records" / (B.uri_key("benchmark://unit/2") + ".json")).read_text())


def test_atomic_json_never_damages_an_existing_file():
    """Catches a write that truncates the target before the new content is complete."""
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "x.json"
        B.atomic_json(p, {"a": 1})
        try:
            B.atomic_json(p, {"a": object()})
            raise AssertionError("unserializable accepted")
        except TypeError:
            pass
        assert json.loads(p.read_text()) == {"a": 1} and not list(Path(t).glob("*.tmp.*"))


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}\n{traceback.format_exc()}")
    print(f"{len(tests) - failed}/{len(tests)} tests passed (numpy {np.__version__})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

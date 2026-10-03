#!/usr/bin/env python3
"""Independent check and stress test of the budgeted, baseline-safe selector.

Reads only frozen per-program records; runs no compiler. It does not import
scripts/analyze_budgeted_selector.py. Besides reproducing that script's cells
it answers the questions a referee would ask before the selector can carry a
paper:

1. How much of the saving is the -Oz fallback, how much the byte selection and
   how much the IC shortlist?
2. Does ranking by IC beat measuring k arbitrary candidates? (exact expectation
   over all k-subsets of the same pool, i.e. a plain best-of-k byte search)
3. What happens to Berkeley text when only code-section bytes are protected,
   and what does a fallback that protects both object metrics cost?
4. How are the savings distributed over programs and suites?
5. What did sequence application and object measurement cost in the frozen
   campaign (emulated amd64; ratios only)?

Outputs: results/budgeted_selector_review/{verification.json,REVIEW_TABLES.md}
"""
from __future__ import annotations

import glob
import hashlib
import itertools
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEL_RECORDS = ROOT / "results/selector_audit/records"
CANON_RECORDS = ROOT / "results/baseline_audit/llvm10_canonical/records"
AUDIT_SUMMARY = ROOT / "results/budgeted_selector_audit/summary.json"
SEL_SUMMARY = ROOT / "results/selector_audit/summary.json"
OUT = ROOT / "results/budgeted_selector_review"
KS = list(range(1, 9))
SUITES = ["npb-v0", "mibench-v1", "blas-v0", "chstone-v0", "csmith-v0", "poj104-v1"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dir_digest(paths) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(Path(p).name.encode())
        h.update(Path(p).read_bytes())
    return h.hexdigest()


# ---------------------------------------------------------------- loading
def load_selector():
    progs = []
    paths = sorted(glob.glob(str(SEL_RECORDS / "*.json")))
    for path in paths:
        d = json.loads(Path(path).read_text())
        if not ("uri" in d and "gnn" in d and "random" in d):
            continue
        pools = {}
        for seed, blk in d["gnn"].items():
            pools[f"gnn{seed}"] = blk["candidates"]
        for seed, blk in d["random"].items():
            pools[f"rnd{seed}"] = blk["candidates"]
        for name, cands in pools.items():
            assert len(cands) == 8 and all(c["ok"] for c in cands), (d["uri"], name)
            assert [c["index"] for c in cands] == list(range(8))
        progs.append({"uri": d["uri"], "suite": d["suite"], "base": d["baseline"], "pools": pools,
                      "timings": d.get("timings", {})})
    assert len(progs) == 347, len(progs)
    return progs, paths


def load_canonical():
    progs = []
    paths = sorted(glob.glob(str(CANON_RECORDS / "*.json")))
    for path in paths:
        d = json.loads(Path(path).read_text())
        a = d["attr"]
        pools = {}
        for name in ("portfolio", "random"):
            cands = [dict(c, index=i) for i, c in enumerate(a[name])]
            assert len(cands) == 8 and all(c["ok"] for c in cands), (d["uri"], name)
            pools[name] = cands
        progs.append({"uri": d["uri"], "suite": d["suite"], "base": a["oz"], "pools": pools})
    assert len(progs) == 210, len(progs)
    return progs, paths


# -------------------------------------------------------------- selectors
def shortlist(cands, k, prefilter):
    if prefilter == "ic":                       # the proposed rule
        return sorted(cands, key=lambda c: (c["ic"], c["index"]))[:k]
    if prefilter == "ic_distinct":              # same, never measuring one module twice
        seen, out = set(), []
        for c in sorted(cands, key=lambda c: (c["ic"], c["index"])):
            if c["bitcode_sha256"] in seen:
                continue
            seen.add(c["bitcode_sha256"])
            out.append(c)
            if len(out) == k:
                break
        return out
    if prefilter == "first":                    # first k by index, no ranking
        return cands[:k]
    raise ValueError(prefilter)


def pick(short, base, fallback):
    """Return (text_sec, text, returned_baseline) of the delivered object."""
    if fallback == "pareto":                    # never worse in either object metric
        short = [c for c in short if c["text_sec"] <= base["text_sec"] and c["text"] <= base["text"]]
    best = min(short, key=lambda c: (c["text_sec"], c["index"])) if short else None
    if fallback == "none":
        return best["text_sec"], best["text"], False
    if best is None or base["text_sec"] <= best["text_sec"]:
        return base["text_sec"], base["text"], True
    return best["text_sec"], best["text"], False


def evaluate(progs, pool, k, prefilter, fallback):
    ref_c = ref_t = sel_c = sel_t = 0
    returned = wins = losses_text = 0
    per_prog = []
    for p in progs:
        b = p["base"]
        c, t, ret = pick(shortlist(p["pools"][pool], k, prefilter), b, fallback)
        ref_c += b["text_sec"]; ref_t += b["text"]; sel_c += c; sel_t += t
        returned += ret
        wins += c < b["text_sec"]
        losses_text += t > b["text"]
        per_prog.append(100.0 * (b["text_sec"] - c) / b["text_sec"])
    improved = [x for x in per_prog if x > 0]
    return {
        "n": len(progs), "ref_code": ref_c, "sel_code": sel_c,
        "gain_code_pct": 100.0 * (ref_c - sel_c) / ref_c,
        "gain_berkeley_pct": 100.0 * (ref_t - sel_t) / ref_t,
        "baseline_returned": returned, "programs_improved": wins,
        "programs_code_regressed": sum(x < 0 for x in per_prog),
        "programs_berkeley_regressed": losses_text,
        "median_prog_gain_pct": statistics.median(per_prog),
        "median_gain_among_improved_pct": statistics.median(improved) if improved else 0.0,
    }


def expected_best_of_k(progs, pool, k, fallback=True):
    """Exact expectation of the delivered code bytes when k of the 8 candidates
    are chosen uniformly at random (= plain best-of-k byte search with fallback)."""
    ref = exp = 0.0
    for p in progs:
        b = p["base"]["text_sec"]
        vals = [c["text_sec"] for c in p["pools"][pool]]
        tot = cnt = 0
        for sub in itertools.combinations(vals, k):
            m = min(sub)
            tot += min(m, b) if fallback else m
            cnt += 1
        ref += b
        exp += tot / cnt
    return 100.0 * (ref - exp) / ref


def rng(vals):
    return [round(min(vals), 2), round(max(vals), 2)]


def main() -> None:
    sel, sel_paths = load_selector()
    can, can_paths = load_canonical()
    gnn = ["gnn42", "gnn123", "gnn456"]
    rnd = [f"rnd{s}" for s in range(42, 47)]
    cohorts = {
        "S347_all": sel,
        "S347_without_npb": [p for p in sel if p["suite"] != "npb-v0"],
        **{f"S347_{s}": [p for p in sel if p["suite"] == s] for s in SUITES},
    }
    can_cohorts = {
        "C210_all": can,
        "C210_without_npb": [p for p in can if p["suite"] != "npb-v0"],
        **{f"C210_{s}": [p for p in can if p["suite"] == s] for s in SUITES[:3]},
    }
    out = {"scope": "frozen records only; no compiler executions",
           "inputs": {"selector_records_digest": dir_digest(sel_paths),
                      "canonical_records_digest": dir_digest(can_paths),
                      "audit_summary_sha256": sha(AUDIT_SUMMARY)}}

    # 1. reproduce the cells of analyze_budgeted_selector.py ---------------
    audit = json.loads(AUDIT_SUMMARY.read_text())["results"]
    name_map = {f"random{s}": f"rnd{s}" for s in range(42, 47)} | {g: g for g in gnn}
    mismatches = 0
    for row in audit:
        coh = cohorts["S347_all" if row["subset"] == "all" else "S347_without_npb"]
        mine = evaluate(coh, name_map[row["generator"]], row["k"], "ic", "code" if row["fallback"] else "none")
        if (mine["sel_code"], mine["ref_code"], mine["baseline_returned"]) != (
                row["selected_text_sec_sum"], row["baseline_text_sec_sum"], row["baseline_returned"]):
            mismatches += 1
    out["audit_cells_checked"] = len(audit)
    out["audit_cells_mismatched"] = mismatches

    # 2. full curves --------------------------------------------------------
    curves = {}
    for cname, progs, pools in ([(c, p, gnn + rnd) for c, p in cohorts.items()] +
                                [(c, p, ["portfolio", "random"]) for c, p in can_cohorts.items()]):
        curves[cname] = {}
        for pool in pools:
            curves[cname][pool] = {}
            for fb in ("none", "code", "pareto"):
                curves[cname][pool][fb] = {str(k): evaluate(progs, pool, k, "ic", fb) for k in KS}
            curves[cname][pool]["ic_distinct_code"] = {str(k): evaluate(progs, pool, k, "ic_distinct", "code") for k in KS}
            curves[cname][pool]["plain_best_of_k_code"] = {str(k): expected_best_of_k(progs, pool, k) for k in KS}
            # Fixed prefix (first k by index): the natural shortlist of an ordered portfolio.
            curves[cname][pool]["prefix_code"] = {str(k): evaluate(progs, pool, k, "first", "code") for k in KS}
    out["curves"] = curves

    # 2b. what the IC shortlist is worth against a plain byte search, per pool
    worth = {}
    for cname in ("S347_all", "S347_without_npb"):
        worth[cname] = {}
        for pool in gnn + rnd:
            ic = [curves[cname][pool]["code"][str(k)]["gain_code_pct"] for k in KS]
            pl = [curves[cname][pool]["plain_best_of_k_code"][str(k)] for k in KS]
            worth[cname][pool] = {
                "advantage_points_at_equal_k": {str(k): ic[k - 1] - pl[k - 1] for k in KS},
                "plain_candidates_needed_to_match_shortlist": {
                    str(k): next(j for j in KS if pl[j - 1] >= ic[k - 1] - 1e-9) for k in KS},
            }
    out["ic_shortlist_worth"] = worth

    # 3. timing of the frozen campaign -------------------------------------
    t = json.loads(SEL_SUMMARY.read_text())["timing"]
    seq_ms = 1000.0 * t["replay_s"] / t["sequences"]
    meas_ms = 1000.0 * t["measure_s"] / t["candidates_measured"]
    out["timing"] = {
        "source": "results/selector_audit/summary.json timing (amd64 container under Rosetta; "
                  "measurement = llc + llvm-size + IC tool + hashing as subprocesses)",
        "ms_per_45_action_sequence": seq_ms, "ms_per_object_measurement": meas_ms,
        "ratio_measurement_to_sequence": meas_ms / seq_ms,
        "model_cost_ms": {f"shortlist_k{k}_of_8": 8 * seq_ms + (k + 1) * meas_ms for k in KS}
                         | {f"plain_best_of_{k}": k * seq_ms + (k + 1) * meas_ms for k in KS},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verification.json").write_text(json.dumps(out, indent=1) + "\n")

    # ------------------------------------------------------------ tables
    L = ["# Budgeted selector: independent tables", "",
         "Generated by `scripts/verify_budgeted_selector.py` from frozen records; no compiler run.",
         f"Cells of `results/budgeted_selector_audit/summary.json` checked: {len(audit)}, mismatched: {mismatches}.", ""]

    def g(c, pool, fb, k, key="gain_code_pct"):
        v = curves[c][pool][fb][str(k)]
        return v if isinstance(v, float) else v[key]

    def table(title, c, groups):
        L.extend([f"## {title}", "",
                  "| generator | rule | " + " | ".join(f"k={k}" for k in KS) + " |",
                  "|---|---|" + "---:|" * len(KS)])
        for label, pools in groups:
            for fb, rule in (("none", "IC top-k, bytes, no fallback"), ("code", "IC top-k, bytes, -Oz fallback"),
                             ("plain_best_of_k_code", "k arbitrary candidates, bytes, -Oz fallback (exact mean)"),
                             ("ic_distinct_code", "IC top-k distinct modules, bytes, -Oz fallback"),
                             ("pareto", "IC top-k, bytes, fallback protecting code and Berkeley text")):
                cells = []
                for k in KS:
                    lo, hi = rng([g(c, p, fb, k) for p in pools])
                    cells.append(f"{lo:.2f}" if lo == hi else f"{lo:.2f}-{hi:.2f}")
                L.append(f"| {label} | {rule} | " + " | ".join(cells) + " |")
        L.append("")

    table("347 programs, code-section saving (%) vs attributed service -Oz", "S347_all",
          [("GNN (3)", gnn), ("random (5)", rnd)])
    table("227 programs without NPB", "S347_without_npb", [("GNN (3)", gnn), ("random (5)", rnd)])
    table("210 programs (NPB, MiBench, BLAS)", "C210_all", [("portfolio", ["portfolio"]), ("random", ["random"])])
    table("90 programs (MiBench, BLAS)", "C210_without_npb", [("portfolio", ["portfolio"]), ("random", ["random"])])

    L.extend(["## What the IC shortlist is worth (IC shortlist minus k arbitrary candidates, both with fallback)", "",
              "| cohort | advantage k=1 | k=2 | k=4 | plain candidates needed to match shortlist of 1 |", "|---|---:|---:|---:|---:|"])
    for cname in ("S347_all", "S347_without_npb"):
        cells = []
        for k in (1, 2, 4):
            lo, hi = rng([worth[cname][p]["advantage_points_at_equal_k"][str(k)] for p in gnn + rnd])
            cells.append(f"{lo:.2f} to {hi:.2f}")
        js = [worth[cname][p]["plain_candidates_needed_to_match_shortlist"]["1"] for p in gnn + rnd]
        L.append(f"| {cname} | " + " | ".join(cells) + f" | {min(js)}-{max(js)} |")
    L.extend(["", "## Ordered portfolio: fixed prefix vs IC shortlist (210 cohort, both with fallback)", "",
              "| rule | " + " | ".join(f"k={k}" for k in KS) + " |", "|---|" + "---:|" * len(KS)])
    for rule, label in (("prefix_code", "first k sequences"), ("code", "IC shortlist of k")):
        L.append(f"| portfolio, {label} | " + " | ".join(f"{g('C210_all', 'portfolio', rule, k):.2f}" for k in KS) + " |")
    L.append("")

    L.extend(["## Berkeley text of the delivered object (%, positive = smaller), 347 programs", "",
              "| generator | fallback | k=2 | k=4 | k=8 | programs with larger Berkeley text at k=8 |", "|---|---|---:|---:|---:|---:|"])
    for label, pools in (("GNN (3)", gnn), ("random (5)", rnd)):
        for fb in ("code", "pareto"):
            cells = []
            for k in (2, 4, 8):
                lo, hi = rng([g("S347_all", p, fb, k, "gain_berkeley_pct") for p in pools])
                cells.append(f"{lo:.2f} to {hi:.2f}")
            lo, hi = rng([g("S347_all", p, fb, 8, "programs_berkeley_regressed") for p in pools])
            L.append(f"| {label} | {fb} | " + " | ".join(cells) + f" | {int(lo)}-{int(hi)} |")
    L.append("")

    L.extend(["## Per suite, IC top-k + bytes + code fallback (347 cohort)", "",
              "| suite | n | GNN k=2 | GNN k=8 | random k=2 | random k=8 |", "|---|---:|---:|---:|---:|---:|"])
    for s in SUITES:
        c = f"S347_{s}"
        row = [s, str(len(cohorts[c]))]
        for pools in (gnn, rnd):
            for k in (2, 8):
                lo, hi = rng([g(c, p, "code", k) for p in pools])
                row.append(f"{lo:.2f}-{hi:.2f}")
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    L.extend(["## Distribution over programs (347 cohort, code fallback)", "",
              "| generator | k | programs improved | -Oz returned | median gain, all programs | median gain, improved programs |",
              "|---|---:|---:|---:|---:|---:|"])
    for label, pools in (("GNN (3)", gnn), ("random (5)", rnd)):
        for k in (2, 4, 8):
            cols = []
            for key in ("programs_improved", "baseline_returned"):
                lo, hi = rng([g("S347_all", p, "code", k, key) for p in pools])
                cols.append(f"{int(lo)}-{int(hi)}")
            for key in ("median_prog_gain_pct", "median_gain_among_improved_pct"):
                lo, hi = rng([g("S347_all", p, "code", k, key) for p in pools])
                cols.append(f"{lo:.2f}-{hi:.2f}%")
            L.append(f"| {label} | {k} | " + " | ".join(cols) + " |")
    L.append("")

    tm = out["timing"]
    L.extend(["## Cost in the frozen campaign (emulated amd64; use ratios only)", "",
              f"- one 45-action sequence in the service: {tm['ms_per_45_action_sequence']:.1f} ms",
              f"- one object measurement (llc, llvm-size, IC tool, hashes; subprocesses): {tm['ms_per_object_measurement']:.0f} ms",
              f"- ratio: {tm['ratio_measurement_to_sequence']:.0f}x", "",
              "| rule | " + " | ".join(f"k={k}" for k in KS) + " |", "|---|" + "---:|" * len(KS),
              "| 8 sequences, measure top-k + -Oz (s) | " + " | ".join(f"{tm['model_cost_ms'][f'shortlist_k{k}_of_8']/1000:.2f}" for k in KS) + " |",
              "| k sequences, measure all + -Oz (s) | " + " | ".join(f"{tm['model_cost_ms'][f'plain_best_of_{k}']/1000:.2f}" for k in KS) + " |", ""])
    (OUT / "REVIEW_TABLES.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

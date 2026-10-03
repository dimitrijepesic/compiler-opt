#!/usr/bin/env python3
"""
Report for the selector audit (results/selector_audit): recomputes every
selection and every sum from the individual candidate records.

Generators: GNN seeds 42, 123, 456 (8 replayed traces each) and random
replicates 42..46 (8 sequences each; 42 reused from the null records).
Selectors (first candidate on ties):
  ic_first        minimum IC                          (the paper's rule)
  code_first      minimum code-section bytes (text_sec)
  ic_then_code    minimum IC, ties by text_sec         (diagnostic)
  berkeley_first  minimum Berkeley text                (diagnostic)
Oz fallback (baseline as an extra candidate) only in the separate table.

Per cohort (each suite, ALL, without NPB) and generator x selector:
sums of IC / text_sec / text, gain = 100 (Oz - X) / Oz, W/T/L vs Oz, the
median per-program relative saving, selection regret
code(IC winner) - min code(all 8); every GNN seed against every random
replicate as (GNN - random)/Oz with W/T/L, and mean/min/max over the
replicates (a range, not a confidence interval); suite contributions to the
pooled saving. Invariants checked on every program: code_first is never
worse than ic_first in text_sec; tie-breaks pick the first index; the old
ic_first selection reproduces results/gnn_attribute_audit/verification/
report_gnn_merged.json.

  python3 scripts/report_selector_audit.py                 # records/ -> summary.json, REPORT.md
  python3 scripts/report_selector_audit.py --records pilot # the pilot records
  python3 scripts/report_selector_audit.py --self-test     # selector and resume/failure tests
"""

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
OUT_DEFAULT = ROOT / "results" / "selector_audit"
MERGED = ROOT / "results" / "gnn_attribute_audit" / "verification" / "report_gnn_merged.json"
SUITES = ["npb-v0", "mibench-v1", "blas-v0", "chstone-v0", "csmith-v0", "poj104-v1"]
SEEDS = ["42", "123", "456"]
REPLICATES = ["42", "43", "44", "45", "46"]
K = 8
METRICS = ("ic", "text_sec", "text")
SELECTORS = ("ic_first", "code_first", "ic_then_code", "berkeley_first")
GENERATORS = [f"gnn{s}" for s in SEEDS] + [f"rnd{r}" for r in REPLICATES]


# ---------------------------------------------------------------- selection
def select(cands, selector):
    """Return (index, candidate). Explicit loop, strict '<' so the first
    candidate wins ties."""
    key = {"ic_first": lambda c: (c["ic"],), "code_first": lambda c: (c["text_sec"],),
           "ic_then_code": lambda c: (c["ic"], c["text_sec"]), "berkeley_first": lambda c: (c["text"],)}[selector]
    best_i, best_k = None, None
    for i, c in enumerate(cands):
        if not c.get("ok"):
            raise ValueError("selection over a candidate set with failures")
        k = key(c)
        if best_k is None or k < best_k:
            best_i, best_k = i, k
    return best_i, cands[best_i]


def select_with_fallback(cands, baseline, metric):
    """Oz fallback: the baseline is an extra candidate; it wins ties."""
    i, c = select(cands, {"ic": "ic_first", "text_sec": "code_first", "text": "berkeley_first"}[metric])
    if baseline[metric] <= c[metric]:
        return "oz", baseline
    return i, c


# ------------------------------------------------------------------ loading
def load_records(rec_dir):
    recs = []
    for f in sorted(glob.glob(str(rec_dir / "*.json"))):
        if os.path.basename(f).startswith("run_manifest"):
            continue
        recs.append(json.load(open(f)))
    return recs


def record_status(r):
    """(complete: bool, reasons: list)"""
    reasons = []
    if "failed" in r:
        return False, [f"failed: {r['failed'][:120]}"]
    reasons += [f"input:{k}" for k, v in r["input"]["checks"].items() if not v]
    reasons += [f"baseline:{k}" for k, v in r["baseline"]["checks"].items() if not v]
    for s, g in r["gnn"].items():
        if g["n_ok"] != K:
            reasons.append(f"gnn{s}: {g['n_ok']}/8 replayed")
        if g["n_ic_match"] != K:
            reasons.append(f"gnn{s}: {g['n_ic_match']}/8 IC matches")
        w = g["old_ic_winner"]
        if not all(w.get(k) for k in ("ic_match", "text_match", "text_sec_match", "bitcode_sha256_match", "object_sha256_match")):
            reasons.append(f"gnn{s}: old IC-winner bytes/hashes differ")
    for rep, e in r["random"].items():
        if e["n_ok"] != K:
            reasons.append(f"rnd{rep}: {e['n_ok']}/8")
    return not reasons, reasons


def candidates(r, gen):
    if gen.startswith("gnn"):
        return r["gnn"][gen[3:]]["candidates"]
    return r["random"][gen[3:]]["candidates"]


# ----------------------------------------------------------------- analysis
def cohort_table(rows, oz_of):
    """rows: list of records (complete). Returns per-generator, per-selector sums etc."""
    n = len(rows)
    oz = {m: sum(oz_of(r)[m] for r in rows) for m in METRICS}
    out = {"n": n, "oz": oz, "generators": {}, "pairs": {}, "pair_summary": {}}
    picks = {}  # (gen, selector) -> list of chosen candidate dicts aligned with rows
    for gen in GENERATORS:
        out["generators"][gen] = {}
        for sel in SELECTORS:
            chosen = [select(candidates(r, gen), sel)[1] for r in rows]
            picks[(gen, sel)] = chosen
            d = out["generators"][gen][sel] = {}
            for m in METRICS:
                vals = [c[m] for c in chosen]
                base = [oz_of(r)[m] for r in rows]
                s = sum(vals)
                d[m] = {"sum": s, "gain_pct": 100 * (oz[m] - s) / oz[m] if oz[m] else None,
                        "wtl_vs_oz": [sum(v < b for v, b in zip(vals, base)), sum(v == b for v, b in zip(vals, base)),
                                      sum(v > b for v, b in zip(vals, base))],
                        "median_program_gain_pct": median(100 * (b - v) / b for v, b in zip(vals, base) if b) if n else None}
        # selection regret in code bytes: code(IC winner) - min code(all 8)
        regret = [select(candidates(r, gen), "ic_first")[1]["text_sec"] - min(c["text_sec"] for c in candidates(r, gen)) for r in rows]
        assert all(x >= 0 for x in regret)
        out["generators"][gen]["regret_code_bytes"] = {"sum": sum(regret), "programs_with_regret": sum(x > 0 for x in regret),
                                                       "median_bytes": median(regret) if regret else None,
                                                       "pct_of_oz_code": 100 * sum(regret) / oz["text_sec"] if oz["text_sec"] else None}
    for s in SEEDS:
        out["pair_summary"][f"gnn{s}"] = {}
        for sel in SELECTORS:
            out["pair_summary"][f"gnn{s}"][sel] = {}
            for m in METRICS:
                pcts = []
                for rep in REPLICATES:
                    g = picks[(f"gnn{s}", sel)]; q = picks[(f"rnd{rep}", sel)]
                    diff = sum(c[m] for c in g) - sum(c[m] for c in q)
                    w = sum(a[m] < b[m] for a, b in zip(g, q)); t = sum(a[m] == b[m] for a, b in zip(g, q))
                    pct = 100 * diff / oz[m] if oz[m] else None
                    out["pairs"].setdefault(f"gnn{s}-rnd{rep}", {}).setdefault(sel, {})[m] = {
                        "gnn_minus_random": diff, "pct_of_oz": pct, "wtl_gnn_vs_random": [w, t, n - w - t]}
                    pcts.append(pct)
                out["pair_summary"][f"gnn{s}"][sel][m] = {"mean_pct": sum(pcts) / len(pcts), "min_pct": min(pcts), "max_pct": max(pcts),
                                                          "n_replicates": len(pcts)}
    # Oz fallback (separate): baseline as extra candidate, in each metric
    out["oz_fallback"] = {}
    for gen in GENERATORS:
        out["oz_fallback"][gen] = {}
        for m in METRICS:
            chosen = [select_with_fallback(candidates(r, gen), oz_of(r), m) for r in rows]
            s = sum(c[m] for _, c in chosen)
            out["oz_fallback"][gen][m] = {"sum": s, "gain_pct": 100 * (oz[m] - s) / oz[m] if oz[m] else None,
                                          "baseline_returned": sum(i == "oz" for i, _ in chosen),
                                          "note": "no-regression holds only in this metric"}
    return out


def analyze(recs):
    complete = []; excluded = []
    for r in recs:
        ok, reasons = record_status(r)
        (complete if ok else excluded).append((r, reasons))
    rows = [r for r, _ in complete]
    oz_of = lambda r: r["baseline"]
    cohorts = {}
    for suite in SUITES:
        sub = [r for r in rows if r["suite"] == suite]
        if sub:
            cohorts[suite] = cohort_table(sub, oz_of)
    cohorts["ALL"] = cohort_table(rows, oz_of)
    cohorts["without_npb"] = cohort_table([r for r in rows if r["suite"] != "npb-v0"], oz_of)
    # suite contribution to pooled code-byte saving, per generator and selector
    contrib = {}
    for gen in GENERATORS:
        contrib[gen] = {}
        for sel in ("ic_first", "code_first"):
            total = cohorts["ALL"]["oz"]["text_sec"] - cohorts["ALL"]["generators"][gen][sel]["text_sec"]["sum"]
            contrib[gen][sel] = {"total_saved_bytes": total}
            for suite in SUITES:
                if suite in cohorts:
                    saved = cohorts[suite]["oz"]["text_sec"] - cohorts[suite]["generators"][gen][sel]["text_sec"]["sum"]
                    contrib[gen][sel][suite] = {"saved_bytes": saved, "share_of_total_pct": 100 * saved / total if total else None}
    # invariants
    inv = {"code_first_never_worse_in_code": True, "ic_first_never_worse_in_ic": True, "tie_break_first_index": True,
           "ic_then_code_same_ic_as_ic_first": True, "checked_selections": 0}
    for r in rows:
        for gen in GENERATORS:
            cs = candidates(r, gen)
            i_ic, c_ic = select(cs, "ic_first"); i_code, c_code = select(cs, "code_first"); i_tc, c_tc = select(cs, "ic_then_code")
            inv["checked_selections"] += 3
            if c_code["text_sec"] > c_ic["text_sec"]:
                inv["code_first_never_worse_in_code"] = False
            if c_ic["ic"] > c_code["ic"]:
                inv["ic_first_never_worse_in_ic"] = False
            if c_tc["ic"] != c_ic["ic"] or c_tc["text_sec"] > c_ic["text_sec"]:
                inv["ic_then_code_same_ic_as_ic_first"] = False
            # tie-break: the chosen index is the first among all candidates attaining the minimum key
            if i_ic != min(j for j, c in enumerate(cs) if c["ic"] == c_ic["ic"]) or \
               i_code != min(j for j, c in enumerate(cs) if c["text_sec"] == c_code["text_sec"]):
                inv["tie_break_first_index"] = False
    # reproduction of the merged GNN tables (attr condition, ic and text_sec of the IC-selected candidate; random replicate 42)
    repro = {"available": MERGED.exists(), "rows_checked": 0, "rows_equal": 0, "mismatches": []}
    if MERGED.exists():
        merged = json.load(open(MERGED))["rows"]
        by = {(x["metric"], x["suite"], str(x["seed"]), x["cond"]): x for x in merged}
        for suite in SUITES + ["ALL"]:
            if suite not in cohorts or cohorts[suite]["n"] != (347 if suite == "ALL" else {"npb-v0": 120, "mibench-v1": 40, "blas-v0": 50, "chstone-v0": 12, "csmith-v0": 28, "poj104-v1": 97}[suite]):
                continue  # only complete cohorts are comparable with the merged tables
            for s in SEEDS:
                for m in ("ic", "text_sec", "text"):
                    x = by.get((m, suite, s, "attr"))
                    if not x:
                        continue
                    ours_g = cohorts[suite]["generators"][f"gnn{s}"]["ic_first"][m]["sum"]
                    ours_r = cohorts[suite]["generators"]["rnd42"]["ic_first"][m]["sum"]
                    ours_oz = cohorts[suite]["oz"][m]
                    repro["rows_checked"] += 1
                    if (ours_g, ours_r, ours_oz) == (x["gnn"], x["random"], x["oz"]):
                        repro["rows_equal"] += 1
                    else:
                        repro["mismatches"].append({"suite": suite, "seed": s, "metric": m, "ours": [ours_g, ours_r, ours_oz], "merged": [x["gnn"], x["random"], x["oz"]]})
    # timing
    tm = {"programs": len(rows), "replay_s": sum(r["timings"]["replay_s"] for r in rows), "export_s": sum(r["timings"]["export_s"] for r in rows),
          "measure_s": sum(r["timings"]["measure_s"] for r in rows), "steps": sum(r["timings"]["steps"] for r in rows),
          "sequences": sum(r["timings"]["sequences"] for r in rows), "candidates_measured": sum(r["timings"]["candidates_measured"] for r in rows),
          "input_and_baseline_s": sum(r["timings"].get("input_and_baseline_s", 0) for r in rows),
          "wall_seconds_sum": sum(r["seconds"] for r in rows)}
    tm["ms_per_step"] = 1000 * tm["replay_s"] / tm["steps"] if tm["steps"] else None
    tm["s_per_candidate_measurement"] = tm["measure_s"] / tm["candidates_measured"] if tm["candidates_measured"] else None
    attempts = {"records": len(recs), "complete": len(rows), "excluded": [{"uri": r["uri"], "reasons": rs} for r, rs in excluded],
                "gnn_candidates_attempted": sum(len(g["candidates"]) for r in recs if "failed" not in r for g in r["gnn"].values()),
                "gnn_candidates_ok": sum(g["n_ok"] for r in recs if "failed" not in r for g in r["gnn"].values()),
                "gnn_ic_matches": sum(g["n_ic_match"] for r in recs if "failed" not in r for g in r["gnn"].values()),
                "random_new_candidates_attempted": sum(len(e["candidates"]) for r in recs if "failed" not in r for rep, e in r["random"].items() if rep != "42"),
                "random_new_candidates_ok": sum(e["n_ok"] for r in recs if "failed" not in r for rep, e in r["random"].items() if rep != "42"),
                "random_42_reused": sum(len(r["random"]["42"]["candidates"]) for r in recs if "failed" not in r),
                "old_winner_full_match": sum(all(g["old_ic_winner"].get(k) for k in ("ic_match", "text_match", "text_sec_match", "bitcode_sha256_match", "object_sha256_match"))
                                             for r in recs if "failed" not in r for g in r["gnn"].values()),
                "old_winner_checked": sum(len(r["gnn"]) for r in recs if "failed" not in r)}
    return {"cohorts": cohorts, "suite_contribution": contrib, "invariants": inv, "merged_reproduction": repro, "timing": tm, "attempts": attempts}


# -------------------------------------------------------------------- report
def pct(x):
    return "n/a" if x is None else f"{x:+.2f}%"


def write_report(out, res, meta):
    C = res["cohorts"]; L = []
    L += ["# Selector audit: candidate generation vs selection metric", "",
          f"Generated {meta['timestamp']}. Records: {res['attempts']['records']}, complete common set: {res['attempts']['complete']}. "
          f"Excluded: {len(res['attempts']['excluded'])}. Manifest fingerprint {meta['manifest_fingerprint'][:16]}, run fingerprint {meta['run_fingerprint'][:16]}, replay mode {meta['replay_mode']}.", "",
          "Definitions: gain = 100 (Oz - X) / Oz with the attributed service -Oz of the same program; "
          "GNN - random as % of Oz; W/T/L per program; regret = code(IC winner) - min code(all 8). "
          "Selection: minimum, first candidate on ties. No Oz fallback except in the labelled table.", ""]
    a = res["attempts"]
    L += ["## Attempts and checks", "",
          f"- GNN candidates: {a['gnn_candidates_ok']}/{a['gnn_candidates_attempted']} replayed, {a['gnn_ic_matches']} with IC equal to the stored IC; "
          f"stored IC-winners with equal bytes and hashes: {a['old_winner_full_match']}/{a['old_winner_checked']}.",
          f"- Random: {a['random_42_reused']} reused candidates of replicate 42; {a['random_new_candidates_ok']}/{a['random_new_candidates_attempted']} new candidates of replicates 43-46 replayed.",
          f"- Excluded programs: " + ("none" if not a["excluded"] else "; ".join(f"{x['uri']} ({', '.join(x['reasons'])})" for x in a["excluded"])), ""]
    inv = res["invariants"]; rp = res["merged_reproduction"]
    L += ["## Invariants", "",
          f"- code_first never worse than ic_first in code bytes: {inv['code_first_never_worse_in_code']}; ic_first never worse in IC: {inv['ic_first_never_worse_in_ic']}; "
          f"ic_then_code keeps the IC minimum: {inv['ic_then_code_same_ic_as_ic_first']}; tie-breaks pick the first index: {inv['tie_break_first_index']} ({inv['checked_selections']} selections).",
          f"- Old ic_first selection reproduces report_gnn_merged.json (GNN, random-42 and Oz sums, attr): {rp['rows_equal']}/{rp['rows_checked']} rows" + (f"; mismatches: {rp['mismatches'][:5]}" if rp["mismatches"] else ""), ""]
    # 2x2 per cohort, code bytes and IC
    for m, label in (("text_sec", "code-section bytes"), ("ic", "IC"), ("text", "Berkeley text")):
        L += [f"## {label}: generator x selector, gain vs Oz (sum-based), W/T/L vs Oz, median per-program gain", "",
              "| cohort | n | generator | ic_first | W/T/L | median | code_first | W/T/L | median | ic_then_code | berkeley_first |", "|---|---:|---|---:|---|---:|---:|---|---:|---:|---:|"]
        for coh in SUITES + ["ALL", "without_npb"]:
            if coh not in C:
                continue
            for gen in GENERATORS:
                g = C[coh]["generators"][gen]
                L.append(f"| {coh} | {C[coh]['n']} | {gen} | {pct(g['ic_first'][m]['gain_pct'])} | {'/'.join(map(str, g['ic_first'][m]['wtl_vs_oz']))} | {pct(g['ic_first'][m]['median_program_gain_pct'])} | "
                         f"{pct(g['code_first'][m]['gain_pct'])} | {'/'.join(map(str, g['code_first'][m]['wtl_vs_oz']))} | {pct(g['code_first'][m]['median_program_gain_pct'])} | "
                         f"{pct(g['ic_then_code'][m]['gain_pct'])} | {pct(g['berkeley_first'][m]['gain_pct'])} |")
        L.append("")
    # absolute sums for ALL and per suite (code and IC)
    L += ["## Absolute sums (code bytes / IC / Berkeley) of the selected candidates", "",
          "| cohort | n | Oz code | Oz IC | Oz Berkeley | generator | ic_first code | ic_first IC | ic_first Berkeley | code_first code | code_first IC | code_first Berkeley |", "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|"]
    for coh in SUITES + ["ALL", "without_npb"]:
        if coh not in C:
            continue
        for gen in GENERATORS:
            g = C[coh]["generators"][gen]; oz = C[coh]["oz"]
            L.append(f"| {coh} | {C[coh]['n']} | {oz['text_sec']:,} | {oz['ic']:,} | {oz['text']:,} | {gen} | {g['ic_first']['text_sec']['sum']:,} | {g['ic_first']['ic']['sum']:,} | {g['ic_first']['text']['sum']:,} | "
                     f"{g['code_first']['text_sec']['sum']:,} | {g['code_first']['ic']['sum']:,} | {g['code_first']['text']['sum']:,} |")
    L.append("")
    # GNN vs random pairs
    for m, label in (("text_sec", "code-section bytes"), ("ic", "IC"), ("text", "Berkeley text")):
        L += [f"## {label}: GNN minus random as % of Oz (negative = GNN smaller), every seed against every replicate; W/T/L = programs where GNN < / = / > random", "",
              "| cohort | GNN seed | selector | rnd42 | rnd43 | rnd44 | rnd45 | rnd46 | mean | min | max |", "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for coh in SUITES + ["ALL", "without_npb"]:
            if coh not in C:
                continue
            for s in SEEDS:
                for sel in ("ic_first", "code_first"):
                    cells = []
                    for rep in REPLICATES:
                        p = C[coh]["pairs"][f"gnn{s}-rnd{rep}"][sel][m]
                        cells.append(f"{pct(p['pct_of_oz'])} ({'/'.join(map(str, p['wtl_gnn_vs_random']))})")
                    ps = C[coh]["pair_summary"][f"gnn{s}"][sel][m]
                    L.append(f"| {coh} | {s} | {sel} | " + " | ".join(cells) + f" | {pct(ps['mean_pct'])} | {pct(ps['min_pct'])} | {pct(ps['max_pct'])} |")
        L.append("")
    # regret
    L += ["## Selection regret in code bytes: code(IC winner) - min code(all 8)", "", "| cohort | generator | regret bytes | % of Oz code | programs with regret | median bytes |", "|---|---|---:|---:|---:|---:|"]
    for coh in SUITES + ["ALL", "without_npb"]:
        if coh not in C:
            continue
        for gen in GENERATORS:
            r = C[coh]["generators"][gen]["regret_code_bytes"]
            L.append(f"| {coh} | {gen} | {r['sum']:,} | {pct(r['pct_of_oz_code'])} | {r['programs_with_regret']}/{C[coh]['n']} | {r['median_bytes']} |")
    L.append("")
    # suite contribution
    L += ["## Suite contribution to the pooled code-byte saving (share of total saved bytes)", "", "| generator | selector | total saved | " + " | ".join(SUITES) + " |", "|---|---|---:|" + "---:|" * len(SUITES)]
    for gen in GENERATORS:
        for sel in ("ic_first", "code_first"):
            c = res["suite_contribution"][gen][sel]
            L.append(f"| {gen} | {sel} | {c['total_saved_bytes']:,} | " + " | ".join(f"{c[s]['saved_bytes']:,} ({c[s]['share_of_total_pct']:+.0f}%)" if s in c and c[s]['share_of_total_pct'] is not None else "n/a" for s in SUITES) + " |")
    L.append("")
    # Oz fallback
    L += ["## Separate table: Oz fallback (baseline as a ninth candidate; guarantee only in the selected metric)", "", "| cohort | generator | code: gain | baseline returned | IC: gain | baseline returned | Berkeley: gain | baseline returned |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for coh in ("ALL", "without_npb"):
        for gen in GENERATORS:
            f = C[coh]["oz_fallback"][gen]
            L.append(f"| {coh} | {gen} | {pct(f['text_sec']['gain_pct'])} | {f['text_sec']['baseline_returned']} | {pct(f['ic']['gain_pct'])} | {f['ic']['baseline_returned']} | {pct(f['text']['gain_pct'])} | {f['text']['baseline_returned']} |")
    L.append("")
    t = res["timing"]
    L += ["## Timing (emulated; not GNN inference time)", "",
          f"{meta['hardware']}; workers {meta['workers']}. Over {t['programs']} programs: replay of {t['sequences']} sequences / {t['steps']} service steps {t['replay_s']:.0f} s "
          f"({t['ms_per_step']:.2f} ms per step); export {t['export_s']:.0f} s; measurement of {t['candidates_measured']} candidates {t['measure_s']:.0f} s ({t['s_per_candidate_measurement']:.2f} s each); "
          f"input preparation and baseline {t['input_and_baseline_s']:.0f} s; summed per-program wall time {t['wall_seconds_sum'] / 60:.1f} min. "
          "Replaying stored GNN actions without the model is not GNN inference latency, and parallel campaign wall time is not a deployment cost.", ""]
    L += ["Structure caveats: modules of a suite are related, not independent applications; three checkpoints and five random replicates are not fifteen independent experiments; "
          "checkpoint inference was not repeated, so GNN sampling variance is not estimated; ranges over replicates are not confidence intervals. No p-values are reported."]
    (out / "REPORT.md").write_text("\n".join(L) + "\n")
    return L


# ---------------------------------------------------------------- self-test
def self_test():
    # selectors: ties, ordering, regret
    cs = [{"ok": True, "ic": 10, "text_sec": 100, "text": 150}, {"ok": True, "ic": 9, "text_sec": 120, "text": 140},
          {"ok": True, "ic": 9, "text_sec": 90, "text": 160}, {"ok": True, "ic": 12, "text_sec": 90, "text": 130}]
    assert select(cs, "ic_first")[0] == 1, "first minimum-IC candidate must win the tie"
    assert select(cs, "code_first")[0] == 2, "first minimum-code candidate must win the tie"
    assert select(cs, "ic_then_code")[0] == 2
    assert select(cs, "berkeley_first")[0] == 3
    base = {"ic": 9, "text_sec": 95, "text": 100}
    assert select_with_fallback(cs, base, "ic")[0] == "oz", "baseline wins IC ties"
    assert select_with_fallback(cs, base, "text_sec")[0] == 2
    assert select_with_fallback(cs, base, "text")[0] == "oz"
    try:
        select(cs + [{"ok": False}], "ic_first"); raise SystemExit("selection over failures must raise")
    except ValueError:
        pass
    # invariant on random synthetic sets
    import random
    rnd = random.Random(1)
    for _ in range(2000):
        cs = [{"ok": True, "ic": rnd.randint(1, 5), "text_sec": rnd.randint(1, 5), "text": rnd.randint(1, 5)} for _ in range(8)]
        a = select(cs, "ic_first")[1]; b = select(cs, "code_first")[1]
        assert b["text_sec"] <= a["text_sec"] and a["ic"] <= b["ic"]
    # failure / resume behaviour of the evaluation script (no container needed for --list-pending)
    ev = ROOT / "scripts" / "evaluate_selector_audit.py"
    src = OUT_DEFAULT
    assert (src / "manifest.json").exists() and (src / "inputs.json").exists(), "run --prepare first"
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        shutil.copy(src / "manifest.json", t / "manifest.json"); shutil.copy(src / "inputs.json", t / "inputs.json")
        (t / "records").mkdir()
        inputs = json.load(open(t / "inputs.json"))
        u0, u1 = inputs["programs"][0]["uri"], inputs["programs"][1]["uri"]
        def run_list(extra=()):
            return subprocess.run([sys.executable, str(ev), "--list-pending", "--replay", "multistep", "--out", str(t), "--uri", u0, u1, *extra],
                                  capture_output=True, text=True, cwd=str(ROOT))
        r = run_list(); assert r.returncode == 0 and "2 pending" in r.stdout, r.stdout + r.stderr
        fp = None
        for line in r.stdout.splitlines():
            if "fingerprint" in line:
                fp = line.split("fingerprint")[-1].strip()
        # a record with the right fingerprint is skipped, a failed one is re-queued
        manifest_fp = json.load(open(t / "manifest.json"))["fingerprint"]
        full_fp = hashlib.sha256((manifest_fp + "|replay=multistep|pilot=0").encode()).hexdigest()
        assert full_fp.startswith(fp), "fingerprint derivation changed"
        key0 = hashlib.sha256(u0.encode()).hexdigest(); key1 = hashlib.sha256(u1.encode()).hexdigest()
        json.dump({"uri": u0, "fingerprint": full_fp, "suite": "x"}, open(t / "records" / f"{key0}.json", "w"))
        json.dump({"uri": u1, "fingerprint": full_fp, "failed": "boom"}, open(t / "records" / f"{key1}.json", "w"))
        r = run_list(); assert "1 done, 1 pending" in r.stdout and u1 in r.stdout, r.stdout
        # a directory written under another fingerprint is refused
        json.dump({"fingerprint": "deadbeef"}, open(t / "records" / "run_manifest.json", "w"))
        r = run_list(); assert r.returncode != 0 and "another fingerprint" in (r.stdout + r.stderr) or "use a new output directory" in (r.stdout + r.stderr), r.stdout + r.stderr
        # a changed script is refused
        m = json.load(open(t / "manifest.json")); m["script_sha256"] = "0" * 64; json.dump(m, open(t / "manifest.json", "w"))
        (t / "records" / "run_manifest.json").unlink()
        r = run_list(); assert r.returncode != 0 and "script changed" in (r.stdout + r.stderr), r.stdout + r.stderr
    print("self-test passed: selector ties/ordering, fallback tie rule, failure exclusion, code_first/ic_first invariants on 2000 random sets, "
          "resume skips finished records, re-queues failed records, refuses foreign fingerprints and a changed script")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    p.add_argument("--records", default="records", help="records subdirectory (records or pilot)")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    rec_dir = args.out / args.records
    recs = load_records(rec_dir)
    manifest = json.load(open(args.out / "manifest.json"))
    run_manifest = json.load(open(rec_dir / "run_manifest.json"))
    bad_fp = [r["uri"] for r in recs if r.get("fingerprint") != run_manifest["fingerprint"]]
    if bad_fp:
        raise SystemExit(f"{len(bad_fp)} records carry another fingerprint: {bad_fp[:3]}")
    res = analyze(recs)
    meta = {"timestamp": datetime.now(timezone.utc).isoformat(), "records_dir": str(rec_dir.relative_to(ROOT)),
            "manifest_fingerprint": manifest["fingerprint"], "run_fingerprint": run_manifest["fingerprint"],
            "replay_mode": run_manifest["replay_mode"], "workers": run_manifest.get("workers"), "hardware": run_manifest.get("hardware"),
            "report_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "record_hashes_sha256": hashlib.sha256("".join(sorted(hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in glob.glob(str(rec_dir / "*.json")) if "run_manifest" not in f)).encode()).hexdigest()}
    summary = {"meta": meta, **res}
    suffix = "" if args.records == "records" else f"_{args.records}"
    json.dump(summary, open(args.out / f"summary{suffix}.json", "w"), indent=1)
    lines = write_report(args.out, summary, meta)
    if suffix:
        (args.out / f"REPORT{suffix}.md").write_text((args.out / "REPORT.md").read_text()); (args.out / "REPORT.md").unlink()
    print("\n".join(lines[:40]))
    print(f"... -> {args.out}/summary{suffix}.json, REPORT{suffix}.md")


if __name__ == "__main__":
    main()

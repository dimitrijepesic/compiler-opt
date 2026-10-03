#!/usr/bin/env python3
"""Retrospective analysis of a budgeted, baseline-safe selector.

The frozen selector campaign measured IC and object sizes for all eight
candidates.  This script does not run a compiler.  It asks what would happen
if IC were used as a cheap prefilter, only the best k candidates were measured
for code bytes, and the attributed service -Oz object were retained as a
fallback.  The calculation is independent of the campaign reporter.
"""

from __future__ import annotations

import glob
import json
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD_GLOB = ROOT / "results" / "selector_audit" / "records" / "*.json"
OUT = ROOT / "results" / "budgeted_selector_audit"
GENERATORS = OrderedDict(
    [
        ("gnn42", ("gnn", "42")),
        ("gnn123", ("gnn", "123")),
        ("gnn456", ("gnn", "456")),
        ("random42", ("random", "42")),
        ("random43", ("random", "43")),
        ("random44", ("random", "44")),
        ("random45", ("random", "45")),
        ("random46", ("random", "46")),
    ]
)


def load_records():
    records = []
    for path in sorted(glob.glob(str(RECORD_GLOB))):
        data = json.loads(Path(path).read_text())
        if "uri" in data and "gnn" in data and "random" in data:
            records.append(data)
    if len(records) != 347:
        raise SystemExit(f"expected 347 selector records, found {len(records)}")
    return records


def choose(record, kind, seed, k, fallback):
    candidates = record[kind][seed]["candidates"]
    if not 1 <= k <= len(candidates):
        raise ValueError(k)
    # IC is the cheap prefilter; ties use the frozen candidate index rule.
    shortlist = sorted(candidates, key=lambda c: (c["ic"], c["index"]))[:k]
    candidate = min(shortlist, key=lambda c: (c["text_sec"], c["index"]))
    selected = candidate["text_sec"]
    baseline = record["baseline"]["text_sec"]
    returned = bool(fallback and baseline <= selected)
    if returned:
        selected = baseline
    return selected, returned


def summarize(records, kind, seed, k, fallback, subset_name, subset):
    rows = [r for r in records if subset(r)]
    ref = sum(r["baseline"]["text_sec"] for r in rows)
    selected_sum = 0
    returned = 0
    wins = ties = losses = 0
    for record in rows:
        selected, did_return = choose(record, kind, seed, k, fallback)
        selected_sum += selected
        returned += int(did_return)
        baseline = record["baseline"]["text_sec"]
        if selected < baseline:
            wins += 1
        elif selected == baseline:
            ties += 1
        else:
            losses += 1
    return {
        "subset": subset_name,
        "n": len(rows),
        "baseline_text_sec_sum": ref,
        "selected_text_sec_sum": selected_sum,
        "gain_pct": 100.0 * (ref - selected_sum) / ref,
        "baseline_returned": returned,
        "w_t_l_vs_baseline": [wins, ties, losses],
        "candidate_codegen_fraction": k / 8.0,
        "prefilter": "minimum IC, first candidate on ties",
        "final_selector": "minimum code-section bytes, first candidate on ties",
        "fallback": fallback,
    }


def main():
    records = load_records()
    subsets = OrderedDict(
        [
            ("all", lambda r: True),
            ("without_npb", lambda r: r["suite"] != "npb-v0"),
        ]
    )
    results = []
    for name, (kind, seed) in GENERATORS.items():
        for k in (1, 2, 3, 4, 6, 8):
            for fallback in (False, True):
                for subset_name, subset in subsets.items():
                    row = summarize(records, kind, seed, k, fallback, subset_name, subset)
                    row.update({"generator": name, "kind": kind, "seed": int(seed), "k": k})
                    results.append(row)
    payload = {
        "schema": 1,
        "scope": "Retrospective recomputation from frozen selector records; no compiler executions",
        "records": len(records),
        "objective": "code-section bytes",
        "baseline": "attributed CompilerGym LLVM 10 service -Oz",
        "definition": "IC prefilter to top-k, then code-section selection, with optional -Oz fallback",
        "results": results,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# Budgeted baseline-safe selector",
        "",
        "Retrospective recomputation from the frozen 347-program selector records; no compiler executions.",
        "The selector first retains the k candidates with minimum IC, then chooses the minimum code-section bytes.",
        "The attributed service `-Oz` object is optionally included as a fallback.",
        "",
        "## Code-section savings with baseline fallback",
        "",
        "| generator | k/8 measured | all 347 | without NPB | baseline returned (all) |",
        "|---|---:|---:|---:|---:|",
    ]
    for name in GENERATORS:
        row2 = next(r for r in results if r["generator"] == name and r["k"] == 2 and r["fallback"] and r["subset"] == "all")
        row4 = next(r for r in results if r["generator"] == name and r["k"] == 4 and r["fallback"] and r["subset"] == "all")
        row2_no = next(r for r in results if r["generator"] == name and r["k"] == 2 and r["fallback"] and r["subset"] == "without_npb")
        row4_no = next(r for r in results if r["generator"] == name and r["k"] == 4 and r["fallback"] and r["subset"] == "without_npb")
        lines.append(f"| {name} | 2/8 | {row2['gain_pct']:.2f}% | {row2_no['gain_pct']:.2f}% | {row2['baseline_returned']} |")
        lines.append(f"| {name} | 4/8 | {row4['gain_pct']:.2f}% | {row4_no['gain_pct']:.2f}% | {row4['baseline_returned']} |")
    lines += [
        "",
        "The 2/8 and 4/8 rows are the proposed budgeted selector; k=8 is the full byte-first selector.",
        "The fallback guarantees no selected code-section regression relative to the attributed service baseline.",
    ]
    (OUT / "README.md").write_text("\n".join(lines) + "\n")
    print((OUT / "README.md").read_text())


if __name__ == "__main__":
    main()

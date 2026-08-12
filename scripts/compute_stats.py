#!/usr/bin/env python3
"""
Formal statistics for the paper.

1. Sign test: across every (suite, seed) pair, does the agent's best-of-k
   total beat the best-of-k random null? Exact binomial p-value.
2. Wilcoxon signed-rank per suite: per-benchmark best-of-k ICs of the
   agent vs. the paired per-benchmark null (median seed).

Inputs: results/sampling_evaluation.json (cBench) and, when present,
results/battery_policy/_aggregate_*.json + per-program JSONs (battery).
"""

import glob
import json
import os
import sys
from math import comb

import numpy as np
from scipy import stats


def sign_test_p(wins, n):
    """Exact one-sided binomial P(X >= wins | p=0.5)."""
    return sum(comb(n, i) for i in range(wins, n + 1)) / 2 ** n


def cbench_pairs():
    """(label, agent_total, null_total) for every seed on val+test splits."""
    with open("results/sampling_evaluation.json") as f:
        d = json.load(f)
    pairs = {"ppo_autophase": [], "ppo_gnn": []}
    per_benchmark = {"ppo_autophase": {}, "ppo_gnn": {}}
    for agent, seeds in d["agents"].items():
        for seed, per_bm in seeds.items():
            for split in ["validation", "test"]:
                rows = {n: r for n, r in per_bm.items() if r["split"] == split}
                a = sum(r["best_of_k_ic"] for r in rows.values())
                z = sum(r["random_best_of_k_ic"] for r in rows.values())
                pairs[agent].append((f"cbench-{split}-s{seed}", a, z))
        # median-seed per-benchmark vectors for Wilcoxon
        totals = {s: sum(r["best_of_k_ic"] for r in pb.values())
                  for s, pb in seeds.items()}
        med_seed = sorted(totals, key=totals.get)[len(totals) // 2]
        per_benchmark[agent]["cbench"] = [
            (r["best_of_k_ic"], r["random_best_of_k_ic"])
            for r in seeds[med_seed].values()
        ]
    return pairs, per_benchmark


def battery_pairs():
    pairs = {}
    per_benchmark = {}
    for agg_path in sorted(glob.glob(
            "results/battery_policy/_aggregate_*.json")):
        with open(agg_path) as f:
            d = json.load(f)
        agent = d["agent"]
        pairs.setdefault(agent, [])
        per_benchmark.setdefault(agent, {})
        for suite, seeds in d["per_suite"].items():
            for seed, b in seeds.items():
                pairs[agent].append(
                    (f"{suite}-s{seed}", b["best_of_k"], b["null_best_of_k"]))
            # median seed per suite -> per-program pairs
            med_seed = sorted(seeds, key=lambda s: seeds[s]["best_of_k"])[
                len(seeds) // 2]
            rows = []
            for p in glob.glob(os.path.join(
                    "results/battery_policy", suite,
                    f"{agent}_seed{med_seed}", "*.json")):
                with open(p) as f:
                    r = json.load(f)
                rows.append((r["best_of_k_ic"], r["random_null_best_of_k"]))
            per_benchmark[agent][suite] = rows
    return pairs, per_benchmark


def report(agent, pairs, per_benchmark):
    print(f"\n===== {agent}")
    wins = sum(1 for _, a, z in pairs if a < z)
    n = len(pairs)
    p = sign_test_p(wins, n)
    print(f"  sign test (best-of-k < null): {wins}/{n} wins, "
          f"one-sided p = {p:.2e}")
    for label, a, z in pairs:
        mark = "WIN " if a < z else ("tie " if a == z else "loss")
        print(f"    {mark} {label:<28} agent={a:>7} null={z:>7}")

    for suite, rows in per_benchmark.items():
        if len(rows) < 5:
            continue
        a = [x for x, _ in rows]
        z = [y for _, y in rows]
        diffs = [x - y for x, y in rows if x != y]
        if not diffs:
            print(f"  wilcoxon {suite}: all ties")
            continue
        try:
            stat, pw = stats.wilcoxon(a, z)
            print(f"  wilcoxon {suite} (median seed, n={len(rows)}): "
                  f"p = {pw:.4f}")
        except ValueError as e:
            print(f"  wilcoxon {suite}: {e}")


def main():
    cb_pairs, cb_pb = cbench_pairs()
    bt_pairs, bt_pb = battery_pairs()

    agents = sorted(set(cb_pairs) | set(bt_pairs))
    for agent in agents:
        pairs = cb_pairs.get(agent, []) + bt_pairs.get(agent, [])
        per_benchmark = {**cb_pb.get(agent, {}), **bt_pb.get(agent, {})}
        report(agent, pairs, per_benchmark)

    if not bt_pairs:
        print("\n(battery_policy data not present locally yet — "
              "cBench-only statistics above)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Formal statistics for the paper (revised after adversarial review).

Three levels, in decreasing conservatism:

1. UNIT-LEVEL EXACT SIGN TEST. The three seeds within a suite are
   compared against the same stored null episodes, so the 24 suite x seed
   pairs are not independent. The independent units are the 8
   suite/split groups (6 battery suites + cBench validation + cBench
   test). A unit counts as a win only if the agent beats its null under
   EVERY seed. Exact one-sided binomial on the 8 units.

2. PER-SUITE ONE-SIDED WILCOXON. Within a suite and seed, per-program
   (agent best-of-k, null best-of-k) pairs are independent across
   programs. We test the directional hypothesis agent < null
   (alternative='less') for the median seed, and report the effective n
   (non-zero differences) alongside the nominal n.

3. DESCRIPTIVE 24/24 + DISJOINT-SLICE ROBUSTNESS. The raw count of
   suite x seed wins is reported descriptively. As a robustness check,
   each seed is re-paired with a DISJOINT slice of the stored random
   episodes (seed 42 -> episodes 0-7, 123 -> 8-15, 456 -> 16-23), which
   restores independence across seeds; the win count is recomputed.
"""

import glob
import json
import os
import sys
from math import comb

import numpy as np
from scipy import stats

SEED_SLICE = {"42": 0, "123": 1, "456": 2}
K = 8


def sign_test_p(wins, n):
    """Exact one-sided binomial P(X >= wins | n, p=0.5)."""
    return sum(comb(n, i) for i in range(wins, n + 1)) / 2 ** n


# ---------------------------------------------------------------- loaders
def load_battery_episodes():
    """(suite_key, uri) -> stored random episode ICs (50 per program)."""
    episodes = {}
    for agg in sorted(glob.glob("results/battery/*/_aggregate.json")):
        suite_key = os.path.basename(os.path.dirname(agg))
        with open(agg) as f:
            for r in json.load(f)["benchmarks"]:
                if "random_reduced_episode_ics" in r:
                    episodes[(suite_key, r["uri"])] = \
                        r["random_reduced_episode_ics"]
    return episodes


def load_cbench_episodes():
    """short_name -> stored random episode ICs (cBench)."""
    with open("results/full_baselines_v2.json") as f:
        return {b["short_name"]: b["random_reduced_episode_ics"]
                for b in json.load(f)["baselines"]}


def battery_records(agent):
    """(suite, seed) -> list of per-program record dicts."""
    out = {}
    for path in sorted(glob.glob(
            f"results/battery_policy/*/{agent}_seed*/*.json")):
        parts = path.replace("\\", "/").split("/")
        suite, seed = parts[-3], parts[-2].split("seed")[-1]
        with open(path) as f:
            out.setdefault((suite, seed), []).append(json.load(f))
    return out


def cbench_records(agent):
    """(split, seed) -> list of per-benchmark records (with name)."""
    with open("results/sampling_evaluation.json") as f:
        d = json.load(f)
    out = {}
    for seed, per_bm in d["agents"][agent].items():
        for name, r in per_bm.items():
            rec = dict(r)
            rec["name"] = name
            out.setdefault((f"cbench-{r['split']}", seed), []).append(rec)
    return out


# ---------------------------------------------------------------- analysis
def analyze(agent):
    print(f"\n===== {agent}")
    bat = battery_records(agent)
    cb = cbench_records(agent)
    bat_eps = load_battery_episodes()
    cb_eps = load_cbench_episodes()

    # --- per (unit, seed): totals with shared null and sliced null
    units = {}
    for (suite, seed), rows in bat.items():
        a = sum(r["best_of_k_ic"] for r in rows)
        z_shared = sum(r["random_null_best_of_k"] for r in rows)
        s = SEED_SLICE.get(seed)
        z_slice = sum(
            min(bat_eps[(suite, r["uri"])][K * s: K * s + K])
            for r in rows) if s is not None else None
        units.setdefault(suite, {})[seed] = (a, z_shared, z_slice)
    for (unit, seed), rows in cb.items():
        a = sum(r["best_of_k_ic"] for r in rows)
        z_shared = sum(r["random_best_of_k_ic"] for r in rows)
        s = SEED_SLICE.get(seed)
        z_slice = sum(
            min(cb_eps[r["name"]][K * s: K * s + K]) for r in rows) \
            if s is not None else None
        units.setdefault(unit, {})[seed] = (a, z_shared, z_slice)

    # --- descriptive 24-pair counts (shared and sliced nulls)
    pair_wins = pair_n = slice_wins = slice_n = 0
    for unit, seeds in sorted(units.items()):
        for seed, (a, z, zs) in sorted(seeds.items()):
            pair_n += 1
            pair_wins += a < z
            if zs is not None:
                slice_n += 1
                slice_wins += a < zs
    print(f"  descriptive: {pair_wins}/{pair_n} suite-x-seed wins "
          f"(shared null); ROBUSTNESS with disjoint per-seed null "
          f"slices: {slice_wins}/{slice_n}")

    # --- unit-level exact sign test (win = beats null under EVERY seed)
    unit_wins = 0
    for unit, seeds in sorted(units.items()):
        win = all(a < z for a, z, _ in seeds.values())
        unit_wins += win
        detail = "  ".join(
            f"s{seed}:{a}{'<' if a < z else '>='}{z}"
            for seed, (a, z, _) in sorted(seeds.items()))
        print(f"    unit {unit:<20} {'WIN ' if win else 'loss'} {detail}")
    n_units = len(units)
    print(f"  UNIT SIGN TEST: {unit_wins}/{n_units} units won under every "
          f"seed; exact one-sided p = {sign_test_p(unit_wins, n_units):.2e}")

    # --- per-suite one-sided Wilcoxon (median seed, shared null)
    print("  one-sided Wilcoxon (agent < null), median seed:")
    all_records = {}
    for (suite, seed), rows in {**bat, **cb}.items():
        all_records.setdefault(suite, {})[seed] = rows
    # merge cbench val+test into one 'cbench' suite for the per-suite test
    merged = {}
    for suite, seeds in all_records.items():
        key = "cbench" if suite.startswith("cbench-") else suite
        for seed, rows in seeds.items():
            merged.setdefault(key, {}).setdefault(seed, []).extend(rows)
    for suite, seeds in sorted(merged.items()):
        totals = {s: sum(r["best_of_k_ic"] for r in rows)
                  for s, rows in seeds.items()}
        med = sorted(totals, key=totals.get)[len(totals) // 2]
        rows = seeds[med]
        a = [r["best_of_k_ic"] for r in rows]
        z = [r.get("random_null_best_of_k", r.get("random_best_of_k_ic"))
             for r in rows]
        nz = sum(1 for x, y in zip(a, z) if x != y)
        if nz == 0:
            print(f"    {suite:<14} all ties (n={len(rows)})")
            continue
        stat, p = stats.wilcoxon(a, z, alternative="less")
        print(f"    {suite:<14} seed {med:<4} n={len(rows):>3} "
              f"(effective n={nz:>3})  one-sided p = {p:.2e}")


def main():
    for agent in ["ppo_autophase", "ppo_gnn"]:
        analyze(agent)


if __name__ == "__main__":
    main()

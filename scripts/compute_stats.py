#!/usr/bin/env python3
"""
Formal statistics for the paper (revised after adversarial review).

Three levels, in decreasing conservatism:

1. UNIT-LEVEL EXACT SIGN TEST. The three seeds within a suite are
   compared against the same stored null episodes, so the suite x seed
   pairs are not independent. The independent units are the 12
   suite/split groups (10 battery suites + cBench validation + cBench
   test). A unit counts as a win only if the agent beats its null under
   EVERY seed. Exact one-sided binomial on the 12 units.

Convention for the four added sources (anghabench, github, linux,
llvm-stress): the GNN stores 16 samples per program there; the FIRST 8
are used everywhere (agent and paired null), so every number is a
best-of-8 comparison. See _pair() and e5().

2. PER-SUITE ONE-SIDED WILCOXON. Within a suite and seed, per-program
   (agent best-of-k, null best-of-k) pairs are independent across
   programs. We test the directional hypothesis agent < null
   (alternative='less') for the median seed, and report the effective n
   (non-zero differences) alongside the nominal n.

3. DESCRIPTIVE 33/36 + DISJOINT-SLICE ROBUSTNESS. The raw count of
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


def _pair(agent, suite, r, eps):
    """(agent best-of-8, paired null best-of-8) for one record."""
    if "random_best_of_k_ic" in r:  # cBench record
        return r["best_of_k_ic"], r["random_best_of_k_ic"]
    if agent == "ppo_gnn" and suite in NEW_SUITES:  # 16 stored, use 8
        return min(r["sample_ics"][:K]), min(eps[(suite, r["uri"])][:K])
    return r["best_of_k_ic"], r["random_null_best_of_k"]


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
        pairs = [_pair(agent, suite, r, bat_eps) for r in rows]
        a = sum(p[0] for p in pairs)
        z_shared = sum(p[1] for p in pairs)
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
        pairs = {s: [_pair(agent, suite, r, bat_eps) for r in rows]
                 for s, rows in seeds.items()}
        totals = {s: sum(p[0] for p in ps) for s, ps in pairs.items()}
        med = sorted(totals, key=totals.get)[len(totals) // 2]
        rows = seeds[med]
        a = [p[0] for p in pairs[med]]
        z = [p[1] for p in pairs[med]]
        nz = sum(1 for x, y in zip(a, z) if x != y)
        if nz == 0:
            print(f"    {suite:<14} all ties (n={len(rows)})")
            continue
        stat, p = stats.wilcoxon(a, z, alternative="less")
        print(f"    {suite:<14} seed {med:<4} n={len(rows):>3} "
              f"(effective n={nz:>3})  one-sided p = {p:.2e}")


# ------------------------------------------------------- reframe metrics
# Amortized-search reframe (REVIEW_2026-08-28.md section 7.2 / E2):
#   iso_k     smallest random-search k whose per-suite total (prefix-min
#             over the 50 stored episodes) matches the agent's best-of-8
#   oz_safe   per-program gain of min(best-of-8, Oz) vs Oz - zero
#             regression by construction - plus the strict-win share
#   wtl       per-program win/tie/loss of best-of-8 vs the paired null
#   npb_k32   robustness of suite totals under the independent k=32
#             resampling (prefix-8 and four disjoint 8-sample slices)

def reframe(agent="ppo_gnn"):
    bat = battery_records(agent)
    cb = cbench_records(agent)
    bat_eps = load_battery_episodes()
    cb_eps = load_cbench_episodes()
    suites = sorted({s for s, _ in bat})
    seeds = sorted({sd for _, sd in bat}, key=int)
    out = {"agent": agent, "k": K, "iso_k": {}, "oz_safe": {},
           "wtl": {}, "npb_k32": {}}

    # --- iso-quality k per suite x seed (battery), plus cBench val+test
    def iso_from(rows, suite, eps_of):
        best = sum(_pair(agent, suite, r, bat_eps)[0] for r in rows)
        for k in range(1, 51):
            if sum(min(eps_of(r)[:k]) for r in rows) <= best:
                return k
        return None  # ">50"
    for suite in suites:
        out["iso_k"][suite] = {
            sd: iso_from(bat[(suite, sd)], suite,
                         lambda r, s=suite: bat_eps[(s, r["uri"])])
            for sd in seeds}
    cb_all = {}
    for (unit, sd), rows in cb.items():
        cb_all.setdefault(sd, []).extend(rows)
    out["iso_k"]["cbench"] = {
        sd: iso_from(rows, "cbench", lambda r: cb_eps[r["name"]])
        for sd, rows in sorted(cb_all.items())}

    # --- -Oz-safe and win/tie/loss per suite x seed (battery)
    for suite in suites:
        oz_row, wtl_row = {}, {}
        for sd in seeds:
            rows = bat[(suite, sd)]
            pairs = [_pair(agent, suite, r, bat_eps) for r in rows]
            gains = [(r["oz"] - min(a, r["oz"])) / r["oz"]
                     for r, (a, _) in zip(rows, pairs) if r["oz"] > 0]
            strict = sum(a < r["oz"] for r, (a, _) in zip(rows, pairs))
            w = sum(a < z for a, z in pairs)
            t = sum(a == z for a, z in pairs)
            oz_row[sd] = {"mean_gain": float(np.mean(gains)),
                          "strict_win_share": strict / len(rows),
                          "n": len(rows)}
            wtl_row[sd] = {"win": w, "tie": t, "loss": len(rows) - w - t}
        out["oz_safe"][suite] = oz_row
        out["wtl"][suite] = wtl_row

    # --- NPB robustness under the independent k=32 resampling
    k32 = {}
    for path in sorted(glob.glob(
            f"results/battery_policy_k32/npb-v0/{agent}_seed*/*.json")):
        seed = path.replace("\\", "/").split("/")[-2].split("seed")[-1]
        with open(path) as f:
            k32.setdefault(seed, []).append(json.load(f))
    for sd, rows in sorted(k32.items(), key=lambda x: int(x[0])):
        null8 = sum(min(bat_eps[("npb-v0", r["uri"])][:K]) for r in rows)
        prefix8 = sum(min(r["sample_ics"][:K]) for r in rows)
        slices = []
        for i in range(4):
            a = sum(min(r["sample_ics"][K * i: K * i + K]) for r in rows)
            z = sum(min(bat_eps[("npb-v0", r["uri"])][K * i: K * i + K])
                    for r in rows)
            slices.append({"agent": a, "null": z, "win": a < z})
        out["npb_k32"][sd] = {"prefix8": prefix8, "null8": null8,
                              "prefix8_win": prefix8 < null8,
                              "slices": slices}

    # --- print + persist
    print(chr(10) + f"===== reframe metrics ({agent}, k={K})")
    print("  iso-quality k (random k needed to match best-of-8):")
    for suite, row in out["iso_k"].items():
        vals = "  ".join(f"s{sd}:{v if v else '>50'}"
                         for sd, v in row.items())
        print(f"    {suite:<14} {vals}")
    print("  -Oz-safe mean per-program gain / strict-win share "
          "(median seed by gain):")
    for suite, row in out["oz_safe"].items():
        med = sorted(row, key=lambda sd: row[sd]["mean_gain"])[len(row) // 2]
        r = row[med]
        print(f"    {suite:<14} seed {med}: {100 * r['mean_gain']:.1f}%  "
              f"strict {100 * r['strict_win_share']:.0f}%  (n={r['n']})")
    for sd in seeds:
        w = sum(out["wtl"][s][sd]["win"] for s in suites)
        t = sum(out["wtl"][s][sd]["tie"] for s in suites)
        l = sum(out["wtl"][s][sd]["loss"] for s in suites)
        print(f"  W/T/L vs null, seed {sd}: {w}/{t}/{l} of {w + t + l}")
    for sd, r in out["npb_k32"].items():
        wins = sum(x["win"] for x in r["slices"])
        print(f"  NPB k32 seed {sd}: prefix8 {r['prefix8']} vs "
              f"{r['null8']} ({'W' if r['prefix8_win'] else 'L'}), "
              f"slices {wins}/4")
    path = f"results/reframe_stats_{agent}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  -> {path}")


def controls():
    """Table IV inputs: per-suite totals for the E1/E3 control variants
    and the E4 portfolio, against the same stored nulls."""
    bat_eps = load_battery_episodes()
    variants = ["ppo_gnn", "ppo_gnn_untrained", "ppo_gnn_nodropout",
                "ppo_gnn_openloop"]
    print(chr(10) + "===== controls (battery, vs stored best-of-8 null)")
    for var in variants:
        rows = {}
        for path in sorted(glob.glob(
                f"results/battery_policy/*/{var}_seed*/*.json")):
            parts = path.replace(chr(92), "/").split("/")
            suite, seed = parts[-3], parts[-2].split("seed")[-1]
            with open(path) as f:
                rows.setdefault((suite, seed), []).append(json.load(f))
        if not rows:
            print(f"  {var:<24} (no data yet)")
            continue
        for (suite, seed), rs in sorted(rows.items()):
            a = sum(r["best_of_k_ic"] for r in rs)
            z = sum(r["random_null_best_of_k"] for r in rs)
            w = sum(r["best_of_k_ic"] < r["random_null_best_of_k"]
                    for r in rs)
            t = sum(r["best_of_k_ic"] == r["random_null_best_of_k"]
                    for r in rs)
            print(f"  {var:<24} {suite:<12} s{seed} n={len(rs):>3} "
                  f"total {a:>7} vs null {z:>7} "
                  f"({'W' if a < z else 'L'})  W/T/L "
                  f"{w}/{t}/{len(rs) - w - t}")
    # portfolio (separate record schema)
    rows = {}
    for path in sorted(glob.glob(
            "results/portfolio_eval/*/portfolio_seed0/*.json")):
        parts = path.replace(chr(92), "/").split("/")
        with open(path) as f:
            rows.setdefault(parts[-3], []).append(json.load(f))
    for suite, rs in sorted(rows.items()):
        for k, akey, zkey in ((8, "best_of_8_ic", "random_null_best_of_8"),
                              (16, "best_of_16_ic",
                               "random_null_best_of_16")):
            a = sum(r[akey] for r in rs)
            z = sum(r[zkey] for r in rs)
            print(f"  portfolio-{k:<15} {suite:<12} n={len(rs):>3} "
                  f"total {a:>7} vs null-{k} {z:>7} "
                  f"({'W' if a < z else 'L'})")
    if not rows:
        print("  portfolio (no data yet)")


NEW_SUITES = ["anghabench-v1", "github-v0", "linux-v0", "llvm-stress-v0"]


def e5():
    """Added-source evaluation: k=16 stored, first 8 used for
    comparability with the original battery; the disjoint second 8 is a
    built-in resampling check. Prints per suite x seed totals, Wilcoxon,
    iso-k / safe%% for the median seed, and the 12-unit sign test."""
    eps = load_battery_episodes()
    units = {}
    print(chr(10) + "===== added sources (best-of-8 = first 8 of 16)")
    for agent in ["ppo_gnn", "ppo_autophase"]:
        print(f"  == {agent}")
        for suite in NEW_SUITES:
            per = {}
            for path in sorted(glob.glob(
                    f"results/battery_policy/{suite}/{agent}_seed*/*.json")):
                seed = path.replace(chr(92), "/").split("/")[-2] \
                    .split("seed")[-1]
                with open(path) as f:
                    per.setdefault(seed, []).append(json.load(f))
            for seed, rows in sorted(per.items(), key=lambda x: int(x[0])):
                a = [min(r["sample_ics"][:8]) for r in rows]
                z = [min(eps[(suite, r["uri"])][:8]) for r in rows]
                nz = sum(1 for x, y in zip(a, z) if x != y)
                pv = stats.wilcoxon(a, z, alternative="less").pvalue \
                    if nz else float("nan")
                slice_b = ""
                if all(len(r["sample_ics"]) >= 16 for r in rows):
                    a2 = sum(min(r["sample_ics"][8:16]) for r in rows)
                    z2 = sum(min(eps[(suite, r["uri"])][8:16])
                             for r in rows)
                    slice_b = f"  sliceB {'W' if a2 < z2 else 'L'}"
                print(f"    {suite:<16} s{seed} n={len(rows):3d} "
                      f"bo8 {sum(a):>7} null {sum(z):>7} "
                      f"({'W' if sum(a) < sum(z) else 'L'}) "
                      f"p={pv:.2g}{slice_b}")
                if agent == "ppo_gnn":
                    units.setdefault(suite, {})[seed] = \
                        (sum(a), sum(z))
    # 12-unit sign test (8 original units assumed won: verified by analyze)
    new_unit_wins = sum(
        all(a < z for a, z in seeds.values()) for seeds in units.values())
    wins = 8 + new_unit_wins
    print(f"  GNN units: {wins}/12 won under every seed "
          f"(8 original + {new_unit_wins} of {len(units)} added); "
          f"exact one-sided sign p = {sign_test_p(wins, 12):.2g}")
    pair_w = sum(a < z for seeds in units.values()
                 for a, z in seeds.values())
    print(f"  GNN added-source pairs: {pair_w}/12 "
          f"(descriptive total 24+{pair_w} of 36)")


def main():
    if "--e5" in sys.argv:
        e5()
        return
    if "--controls" in sys.argv:
        controls()
        return
    if "--reframe" in sys.argv:
        for agent in ["ppo_gnn", "ppo_autophase"]:
            reframe(agent)
        return
    for agent in ["ppo_autophase", "ppo_gnn"]:
        analyze(agent)


if __name__ == "__main__":
    main()

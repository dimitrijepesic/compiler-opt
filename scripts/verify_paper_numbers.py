#!/usr/bin/env python3
"""
Reproducibility check for every headline number in paper/telfor_paper.tex.

Recomputes each figure from the raw JSON in results/ (independently of
compute_stats.py's printed output, though it reuses its loaders) and
diffs it against the value quoted in the paper. Exits non-zero if any
check fails, so it can gate a release the way a test suite does.

  python scripts/verify_paper_numbers.py
  python scripts/verify_paper_numbers.py -v      # print every check
"""

import glob
import json
import os
import sys

from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
import compute_stats as cs  # noqa: E402

VERBOSE = "-v" in sys.argv
CHECKS = []


def check(name, expected, actual, tol=0.05, unit=""):
    """tol: relative tolerance for floats; exact match for int/str."""
    if isinstance(expected, str) or isinstance(actual, str):
        ok = str(expected) == str(actual)
    elif isinstance(expected, (list, tuple)) or isinstance(actual, (list, tuple)):
        ok = list(expected) == list(actual)
    elif isinstance(expected, int) and isinstance(actual, int):
        ok = expected == actual
    else:
        actual = float(actual)
        ok = abs(expected - actual) <= max(tol * abs(expected), 1e-9)
    CHECKS.append((ok, name, expected, actual, unit))
    return ok


# --------------------------------------------------------------- Table I
def table_i():
    cbench = json.load(open("results/full_baselines_v2.json"))["baselines"]
    cbench = [b for b in cbench if b.get("split") in ("validation", "test")]
    suites = {
        "AnghaBench (150)": ("anghabench-v1", 150),
        "GitHub (150)": ("github-v0", 150),
        "MiBench (40)": ("mibench-v1", 40),
        "Linux (150)": ("linux-v0", 150),
        "BLAS (50)": ("blas-v0", 50),
        "CHStone (12)": ("chstone-v0", 12),
        "POJ-104 (97)": ("poj104-v1", 97),
        "NPB (122)": ("npb-v0", 122),
        "csmith (50)": ("csmith-v0", 50),
        "llvm-stress (50)": ("llvm-stress-v0", 50),
    }
    expected = {
        "AnghaBench (150)": (8902, 4193, 4043, 4006, 0.9),
        "GitHub (150)": (224490, 222369, 224171, 221297, 1.3),
        "MiBench (40)": (12270, 6317, 4841, 4765, 1.6),
        "Linux (150)": (255140, 250862, 252031, 246983, 2.0),
        "BLAS (50)": (40745, 39141, 37838, 36757, 2.9),
        "cBench (9)": (232442, 163834, 115987, 111006, 4.3),
        "CHStone (12)": (19857, 14182, 9834, 9097, 7.5),
        "POJ-104 (97)": (21099, 11083, 8334, 7622, 8.5),
        "NPB (122)": (130327, 70659, 59542, 44981, 24.5),
        "csmith (50)": (352963, 82950, 57625, 60626, -5.2),
        "llvm-stress (50)": (5739, 238, 234, 238, -1.7),
    }
    for label, (suite, n) in suites.items():
        agg = json.load(open(f"results/battery/{suite}/_aggregate.json"))
        rows = agg["benchmarks"]
        o0 = sum(r["o0"] for r in rows)
        o3 = sum(r["o3"] for r in rows)
        oz = sum(r["oz"] for r in rows)
        rnd50 = sum(min(r["random_reduced_episode_ics"]) for r in rows)
        dOz = (oz - rnd50) / oz * 100
        e = expected[label]
        check(f"Table I {label} O0", e[0], o0, tol=0)
        check(f"Table I {label} O3", e[1], o3, tol=0)
        check(f"Table I {label} Oz", e[2], oz, tol=0)
        check(f"Table I {label} Rnd-50", e[3], rnd50, tol=0)
        check(f"Table I {label} dOz%", e[4], dOz, tol=0.05, unit="%")

    o0 = sum(b["o0"] for b in cbench)
    o3 = sum(b["o3"] for b in cbench)
    oz = sum(b["oz"] for b in cbench)
    rnd50 = sum(min(b["random_reduced_episode_ics"]) for b in cbench)
    dOz = (oz - rnd50) / oz * 100
    e = expected["cBench (9)"]
    check("Table I cBench (9) O0", e[0], o0, tol=0)
    check("Table I cBench (9) O3", e[1], o3, tol=0)
    check("Table I cBench (9) Oz", e[2], oz, tol=0)
    check("Table I cBench (9) Rnd-50", e[3], rnd50, tol=0)
    check("Table I cBench (9) dOz%", e[4], dOz, tol=0.05, unit="%")


# -------------------------------------------------------------- Table II
def table_ii():
    def median_seed_total(rows_by_seed, key):
        totals = {s: sum(r[key] for r in rs) for s, rs in rows_by_seed.items()}
        med = sorted(totals, key=totals.get)[len(totals) // 2]
        return totals[med]

    suites = {
        "MiBench (40)": ("mibench-v1", 4828, 4841, 4783, 4782),
        "CHStone (12)": ("chstone-v0", 9241, 9834, 9133, 9120),
        "BLAS (50)": ("blas-v0", 37099, 37838, 36998, 36847),
        "csmith (28)": ("csmith-v0", 17555, 20226, 17179, 17064),
        "NPB (120)": ("npb-v0", 40301, 53085, 40822, 39909),
        "POJ-104 (97)": ("poj104-v1", 7853, 8334, 7917, 7730),
        "AnghaB. (150)": ("anghabench-v1", 4049, 4043, 4052, 4027),
        "GitHub (140)": ("github-v0", 79713, 80661, 79738, 79676),
        "Linux (136)": ("linux-v0", 147216, 148029, 147278, 147378),
        "llvm-str. (50)": ("llvm-stress-v0", 255, 234, 245, 240),
    }
    # GNN stores k=16 for the four added sources (first 8 used for
    # comparability with the original battery, per e5()); ppo_autophase
    # was run at k=8 there directly, same field as the original suites.
    eps = cs.load_battery_episodes()
    for label, (suite, e_null, e_oz, e_ap, e_gnn) in suites.items():
        rows_by_seed = {}
        for path in sorted(glob.glob(
                f"results/battery_policy/{suite}/ppo_autophase_seed*/*.json")):
            seed = path.replace("\\", "/").split("/")[-2].split("seed")[-1]
            rows_by_seed.setdefault(seed, []).append(json.load(open(path)))
        check(f"Table II {label} ppo_autophase", e_ap,
              median_seed_total(rows_by_seed, "best_of_k_ic"), tol=0)

        rows_by_seed = {}
        for path in sorted(glob.glob(
                f"results/battery_policy/{suite}/ppo_gnn_seed*/*.json")):
            seed = path.replace("\\", "/").split("/")[-2].split("seed")[-1]
            rows_by_seed.setdefault(seed, []).append(json.load(open(path)))
        if suite in cs.NEW_SUITES:
            bo8_by_seed = {s: sum(min(r["sample_ics"][:8]) for r in rs)
                          for s, rs in rows_by_seed.items()}
            med_seed = sorted(bo8_by_seed, key=bo8_by_seed.get)[
                len(bo8_by_seed) // 2]
            check(f"Table II {label} ppo_gnn", e_gnn,
                  bo8_by_seed[med_seed], tol=0)
            null_total = sum(min(eps[(suite, r["uri"])][:8])
                             for r in rows_by_seed[med_seed])
            oz_total = sum(r["oz"] for r in rows_by_seed[med_seed])
        else:
            check(f"Table II {label} ppo_gnn", e_gnn,
                  median_seed_total(rows_by_seed, "best_of_k_ic"), tol=0)
            null_total = median_seed_total(rows_by_seed, "random_null_best_of_k")
            oz_total = median_seed_total(rows_by_seed, "oz")
        check(f"Table II {label} Null", e_null, null_total, tol=0)
        check(f"Table II {label} -Oz", e_oz, oz_total, tol=0)


# ------------------------------------------------------------- Table III
def table_iii():
    variants = {
        "Untrained policy, best-of-8": ("ppo_gnn_untrained", 116941),
        "Open-loop pi(.|s0), best-of-8": ("ppo_gnn_openloop", 116377),
        "GNN best-of-8": ("ppo_gnn", 115451),
    }
    orig = ["mibench-v1", "chstone-v0", "blas-v0", "csmith-v0",
            "npb-v0", "poj104-v1"]
    for label, (variant, expected) in variants.items():
        total = 0
        for suite in orig:
            for path in glob.glob(
                    f"results/battery_policy/{suite}/{variant}_seed42/*.json"):
                total += json.load(open(path))["best_of_k_ic"]
        check(f"Table III {label}", expected, total, tol=0)
    total_nd = sum(
        json.load(open(p))["best_of_k_ic"]
        for suite in orig
        for p in glob.glob(
            f"results/battery_policy/{suite}/ppo_gnn_nodropout_seed42/*.json"))
    check("Table III GNN no-dropout", 115761, total_nd, tol=0)
    null8 = sum(
        json.load(open(p))["random_null_best_of_k"]
        for suite in orig
        for p in glob.glob(
            f"results/battery_policy/{suite}/ppo_gnn_seed42/*.json"))
    check("Table III stored best-of-8 null", 116877, null8, tol=0)
    port8 = sum(
        json.load(open(p))["best_of_8_ic"]
        for suite in orig
        for p in glob.glob(f"results/portfolio_eval/{suite}/portfolio_seed0/*.json"))
    port16 = sum(
        json.load(open(p))["best_of_16_ic"]
        for suite in orig
        for p in glob.glob(f"results/portfolio_eval/{suite}/portfolio_seed0/*.json"))
    null16 = sum(
        json.load(open(p))["random_null_best_of_16"]
        for suite in orig
        for p in glob.glob(f"results/portfolio_eval/{suite}/portfolio_seed0/*.json"))
    check("Table III Portfolio-8", 115972, port8, tol=0)
    check("Table III Portfolio-16", 114407, port16, tol=0)
    check("Table III best-of-16 null", 115158, null16, tol=0)


# -------------------------------------------------------- sign test / wilcoxon
def suite_seed_win(agent, suite, seed, rows, eps):
    """(win, a, z) for one (suite, seed): GNN on the four added sources
    compares first-8-of-16 (e5's convention); everything else uses the
    stored best_of_k_ic field directly."""
    if agent == "ppo_gnn" and suite in cs.NEW_SUITES:
        a = sum(min(r["sample_ics"][:8]) for r in rows)
        z = sum(min(eps[(suite, r["uri"])][:8]) for r in rows)
    else:
        a = sum(r["best_of_k_ic"] for r in rows)
        z = sum(r["random_null_best_of_k"] for r in rows)
    return a < z


def sampling_stats():
    eps = cs.load_battery_episodes()
    for agent, e_pairs in [("ppo_gnn", 33), ("ppo_autophase", 21)]:
        bat = cs.battery_records(agent)
        cb = cs.cbench_records(agent)
        n_pairs = n_wins = 0
        for (suite, seed), rows in bat.items():
            n_pairs += 1
            n_wins += suite_seed_win(agent, suite, seed, rows, eps)
        for (unit, seed), rows in cb.items():
            a = sum(r["best_of_k_ic"] for r in rows)
            z = sum(r["random_best_of_k_ic"] for r in rows)
            n_pairs += 1
            n_wins += a < z
        check(f"{agent} suite-seed wins (of {n_pairs})", e_pairs, n_wins, tol=0)

    bat = cs.battery_records("ppo_gnn")
    cb = cs.cbench_records("ppo_gnn")
    units = {}
    for (suite, seed), rows in bat.items():
        units.setdefault(suite, {})[seed] = \
            suite_seed_win("ppo_gnn", suite, seed, rows, eps)
    for (unit, seed), rows in cb.items():
        a = sum(r["best_of_k_ic"] for r in rows)
        z = sum(r["random_best_of_k_ic"] for r in rows)
        units.setdefault(unit, {})[seed] = a < z
    wins = sum(all(v.values()) for v in units.values())
    n = len(units)
    p = cs.sign_test_p(wins, n)
    check("GNN units won under every seed (of 12)", 10, wins, tol=0)
    check("GNN unit sign test p", 0.019, p, tol=0.05)


# --------------------------------------------------------------- k=32 Pareto
def k32():
    """The paper quotes each agent's three k=32 seed totals but does not
    bind them to specific seed numbers, so the multiset of values (not
    the seed labels) is what is checked here."""
    d = json.load(open("results/sampling_evaluation_k32.json"))
    null_total = sum(d["random_null"].values())
    check("k=32 random null total", 111023, null_total, tol=0)
    e_gnn = [110494, 110527, 110787]
    e_ap = [110338, 111056, 111108]
    for agent, expected in (("ppo_gnn", e_gnn), ("ppo_autophase", e_ap)):
        actual = []
        for seed in ("42", "123", "456"):
            val = d["summary"][agent][f"validation_seed{seed}"]
            test = d["summary"][agent][f"test_seed{seed}"]
            actual.append(val["best_of_k_total"] + test["best_of_k_total"])
        check(f"k=32 {agent} seed totals (as a set)",
              sorted(expected), sorted(actual), tol=0)


# --------------------------------------------------------------- Pearson
def pearson():
    d = json.load(open("results/text_size_anchor.json"))
    xs, ys, progs = [], [], set()
    for p in d["programs"]:
        c = p["conditions"]
        o0 = c["o0"]
        if o0["ic"] < 1000:
            continue
        for k in ("oz", "random36_best"):
            xs.append(1 - c[k]["ic"] / o0["ic"])
            ys.append(1 - c[k]["text"] / o0["text"])
            progs.add(p["uri"])
    r, p_val = stats.pearsonr(xs, ys)
    check("Pearson n (points)", 26, len(xs), tol=0)
    check("Pearson n (programs)", 13, len(progs), tol=0)
    check("Pearson r", 0.78, r, tol=0.02)
    check("Pearson p", 2.2e-6, p_val, tol=0.3)


# ---------------------------------------------------------- binary metrics
def binary_metrics():
    d = json.load(open("results/binary_metrics/_aggregate.json"))["summary"]
    p = d["paired_gnn_subset"]
    check("bytes: n paired (347)", 347, d["gnn_bo8"]["n"], tol=0)
    check("bytes: -Oz total (paired 347)", 967878, p["oz_text"], tol=0)
    check("bytes: GNN best-of-8 total", 864887, p["gnn_text"], tol=0)
    check("bytes: GNN vs -Oz %", 10.6,
          (1 - p["gnn_text"] / p["oz_text"]) * 100, tol=0.02)
    check("bytes: random-null (paired) vs -Oz %", 10.4,
          (1 - p["rnd_text"] / p["oz_text"]) * 100, tol=0.02)
    check("bytes: n all (371)", 371, d["rnd_bo8"]["n"], tol=0)
    check("bytes: random-null (all 371) vs -Oz %", 4.0,
          (1 - d["rnd_bo8"]["text_total"] / d["oz"]["text_total"]) * 100,
          tol=0.05)
    check("opt time -Oz median ms", 19.5, d["oz"]["opt_ms_median"], tol=0.05)
    check("opt time random median ms", 15.8, d["rnd_bo8"]["opt_ms_median"],
          tol=0.05)
    check("opt time GNN median ms", 15.0, d["gnn_bo8"]["opt_ms_median"],
          tol=0.05)

    arm = json.load(open("results/binary_metrics_arm/_aggregate.json"))["summary"]
    ap = arm["paired_gnn_subset_arm"]
    check("ARM: -Oz total kB", 986, round(ap["oz_text"] / 1000), tol=0.02)
    check("ARM: GNN best-of-8 total kB", 839, round(ap["gnn_text"] / 1000),
          tol=0.02)
    check("ARM: GNN vs -Oz %", 14.9,
          (1 - ap["gnn_text"] / ap["oz_text"]) * 100, tol=0.05)
    check("ARM: random-null vs -Oz %", 15.0,
          (1 - ap["rnd_text"] / ap["oz_text"]) * 100, tol=0.05)


# ---------------------------------------------------------- pretraining
def pretraining():
    import torch
    scratch = json.load(open("results/final_evaluation.json"))
    pre = json.load(open("results/final_evaluation_pretrained.json"))

    check("from-scratch GNN validation mean argmax",
          64550, scratch["splits"]["validation"]["agents"]["ppo_gnn"]
          ["summary"]["mean_total_ic"], tol=0.001)
    check("from-scratch GNN test mean argmax",
          69180, scratch["splits"]["test"]["agents"]["ppo_gnn"]
          ["summary"]["mean_total_ic"], tol=0.001)
    val_mean = pre["splits"]["validation"]["agents"]["ppo_gnn"]["summary"]["mean_total_ic"]
    test_mean = pre["splits"]["test"]["agents"]["ppo_gnn"]["summary"]["mean_total_ic"]
    check("pretrained GNN validation mean argmax", 57980, val_mean, tol=0.001)
    check("pretrained GNN test mean argmax", 63229, test_mean, tol=0.001)
    check("pretrained improvement, validation %",
          10.2, (1 - val_mean / 64550) * 100, tol=0.02)
    check("pretrained improvement, test %",
          8.6, (1 - test_mean / 69180) * 100, tol=0.02)

    for seed, expected in (("seed42", 651), ("seed123", 668)):
        ckpt = torch.load(f"results/ppo_gnn_pretrained/checkpoint_best_{seed}.pt",
                          map_location="cpu", weights_only=False)
        check(f"pretrained {seed} best val-small IC", expected,
              ckpt["best_val_score"], tol=0)


def mixed_arm():
    """Three-seed mixed-size GNN arm (results/ppo_gnn_mixed_v2/PROTOCOL.md)."""
    scratch = json.load(open("results/final_evaluation.json"))
    mixed = json.load(open("results/final_evaluation_mixed_v2.json"))

    def per_program(d):
        out = {}
        for split in ("validation", "test"):
            for run in d["splits"][split]["agents"]["ppo_gnn"]["runs"]:
                for det in run["details"]:
                    out.setdefault((split, det["short_name"]), {})[run["seed"]] = det["final_ic"]
        return out

    for split, expected in (("validation", 64797), ("test", 69748)):
        check(f"mixed-size GNN {split} mean argmax", expected,
              mixed["splits"][split]["agents"]["ppo_gnn"]["summary"]["mean_total_ic"],
              tol=0.001)
    a, b = per_program(scratch), per_program(mixed)
    keys = sorted(a)
    mean_a = [sum(a[k].values()) / 3 for k in keys]
    mean_b = [sum(b[k].values()) / 3 for k in keys]
    p = stats.wilcoxon(mean_b, mean_a, alternative="less").pvalue
    check("mixed-size vs from-scratch one-sided Wilcoxon p", 0.41, p, tol=0.02)
    seeds = sorted({s for k in keys for s in b[k]})
    # "one seed improved both splits": compare each seed's totals with the
    # from-scratch mean on that split (the number the sentence quotes).
    better = [s for s in seeds
              if all(sum(b[k][s] for k in keys if k[0] == sp)
                     < scratch["splits"][sp]["agents"]["ppo_gnn"]["summary"]["mean_total_ic"]
                     for sp in ("validation", "test"))]
    check("mixed-size seeds improving both splits", 1, len(better), tol=0)
    for sp, expected in (("validation", 60211), ("test", 65239)):
        check(f"mixed-size seed 42 {sp} argmax", expected,
              sum(b[k][42] for k in keys if k[0] == sp), tol=0)


def gnn_cost():
    import re
    times = {}
    for agent, key in (("gnn", "ppo_gnn"), ("ap", "ppo_autophase")):
        mins = []
        for seed in (42, 123, 456):
            path = f"results/train_{agent}_seed{seed}_log.txt"
            for line in open(path):
                m = re.search(r"Training complete in ([\d.]+) minutes", line)
                if m:
                    mins.append(float(m.group(1)))
        times[key] = mins
    ratios = [g / a for g, a in zip(times["ppo_gnn"], times["ppo_autophase"])]
    pooled = sum(times["ppo_gnn"]) / sum(times["ppo_autophase"])
    check("GNN/AP wall-clock pooled", 19, pooled, tol=0.1)
    check("GNN/AP wall-clock min seed ratio", 17, min(ratios), tol=0.1)
    check("GNN/AP wall-clock max seed ratio", 23, max(ratios), tol=0.1)


def main():
    table_i()
    table_ii()
    table_iii()
    sampling_stats()
    k32()
    pearson()
    binary_metrics()
    pretraining()
    mixed_arm()
    gnn_cost()

    n_fail = sum(1 for ok, *_ in CHECKS if not ok)
    for ok, name, exp, act, unit in CHECKS:
        if ok and not VERBOSE:
            continue
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name:<42} expected={exp!r:>12} "
              f"actual={act!r:>12} {unit}")
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed"
          + (f", {n_fail} FAILED" if n_fail else ""))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()

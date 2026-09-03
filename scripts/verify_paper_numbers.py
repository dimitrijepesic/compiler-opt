#!/usr/bin/env python3
"""
Reproducibility check for every headline number in paper/telfor_paper.tex
(tables, and the numbers quoted in the running text: prose_claims()).

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

import numpy as np
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


# ------------------------------------------------------------ prose claims
def _median_seed(totals):
    """The seed whose total is the median of the three (compute_stats)."""
    return sorted(totals, key=totals.get)[len(totals) // 2]


def _battery_pairs(agent, eps):
    """suite -> seed -> list of (agent best-of-8, null best-of-8, record).
    Same convention as compute_stats._pair: on the four added sources the
    GNN stores 16 samples and the first 8 are used."""
    out = {}
    for (suite, seed), rows in cs.battery_records(agent).items():
        out.setdefault(suite, {})[seed] = [
            cs._pair(agent, suite, r, eps) + (r,) for r in rows]
    return out


ORIG6 = ["mibench-v1", "chstone-v0", "blas-v0", "csmith-v0", "npb-v0",
         "poj104-v1"]


def prose_claims():
    import re
    eps = cs.load_battery_episodes()
    rows = [r for agg in sorted(glob.glob("results/battery/*/_aggregate.json"))
            for r in json.load(open(agg))["benchmarks"]]

    # ---- Sec. IV-A -----------------------------------------------------
    npb = json.load(open("results/battery/npb-v0/_aggregate.json"))["benchmarks"]
    oz = sum(r["oz"] for r in npb)
    single = sum(r["random_reduced_policy"]["mean"] for r in npb)
    check("NPB single random episodes below -Oz %", 11.5,
          (oz - single) / oz * 100, tol=0.02)
    ep = [(ic, r["oz"]) for r in npb for ic in r["random_reduced_episode_ics"]]
    check("NPB share of single episodes beating -Oz %", 32,
          100 * sum(ic < z for ic, z in ep) / len(ep), tol=0.02)
    small = [r for r in rows if r["o0"] < 500]
    check("-O3 above -O0 on programs under 500 IC %", 6,
          100 * sum(r["o3"] > r["o0"] for r in small) / len(small), tol=0.1)
    gh = json.load(open("results/battery/github-v0/_aggregate.json"))["totals"]
    check("GitHub: -Oz removes % of -O0 IC", 0.14,
          (gh["o0"] - gh["oz"]) / gh["o0"] * 100, tol=0.05)
    check("programs up to 6000 IC (eligible)", 831,
          sum(r["o0"] <= 6000 for r in rows), tol=0)
    import yaml
    passes = yaml.safe_load(open("configs/passes.yaml"))
    check("36-pass space: passes improving none", 88,
          passes["total_original"] - len(passes["passes"]), tol=0)

    # ---- Sec. IV-B -----------------------------------------------------
    gnn = _battery_pairs("ppo_gnn", eps)
    ap = _battery_pairs("ppo_autophase", eps)
    npb_arg = {s: sum(p[2]["argmax_ic"] for p in ps) for s, ps in gnn["npb-v0"].items()}
    check("NPB GNN argmax total (median seed)", 79686,
          npb_arg[_median_seed(npb_arg)], tol=0)

    def median_seed_p(pairs, cb_agent):
        per = {}
        for suite, seeds in pairs.items():
            per[suite] = {s: ([p[0] for p in ps], [p[1] for p in ps])
                          for s, ps in seeds.items()}
        for (unit, seed), rs in cs.cbench_records(cb_agent).items():
            a, z = per.setdefault("cbench", {}).setdefault(seed, ([], []))
            a.extend(r["best_of_k_ic"] for r in rs)
            z.extend(r["random_best_of_k_ic"] for r in rs)
        out = {}
        for suite, seeds in per.items():
            med = _median_seed({s: sum(a) for s, (a, z) in seeds.items()})
            a, z = seeds[med]
            out[suite] = stats.wilcoxon(a, z, alternative="less").pvalue
        return out
    p_gnn = median_seed_p(gnn, "ppo_gnn")
    p_ap = median_seed_p(ap, "ppo_autophase")
    sig = {s: p for s, p in p_gnn.items() if p < 0.05}
    check("GNN sources significant (median seed, of 11)", 10, len(sig), tol=0)
    check("GNN largest significant p (MiBench)", 0.025, max(sig.values()), tol=0.05)
    check("GNN largest significant p is MiBench", "mibench-v1",
          max(sig, key=sig.get))
    check("GNN non-significant source is Linux", "linux-v0",
          [s for s in p_gnn if s not in sig][0])
    check("Autophase sources significant (of 11)", 5,
          sum(p < 0.05 for p in p_ap.values()), tol=0)

    def seed_p(ps):
        return stats.wilcoxon([p[0] for p in ps], [p[1] for p in ps],
                              alternative="less").pvalue
    lin = gnn["linux-v0"]
    check("Linux: GNN seeds with per-program p >= 0.24", 2,
          sum(seed_p(ps) >= 0.24 for ps in lin.values()), tol=0)
    slice_b = sum(
        sum(min(p[2]["sample_ics"][8:16]) for p in ps)
        < sum(min(eps[("linux-v0", p[2]["uri"])][8:16]) for p in ps)
        for ps in lin.values())
    check("Linux: second-slice wins (of 3)", 0, slice_b, tol=0)
    git = gnn["github-v0"]
    losses = [sum(p[0] for p in ps) - sum(p[1] for p in ps)
              for ps in git.values()]
    check("GitHub: seeds losing the summed IC", 1, sum(d > 0 for d in losses), tol=0)
    check("GitHub: losing margin (IC)", 17, max(losses), tol=0)
    check("GitHub: all seeds p <= 2e-3", True,
          bool(max(seed_p(ps) for ps in git.values()) <= 2e-3))

    # margin over the null on the original battery (Table II medians)
    margins = []
    for suite in ORIG6:
        tot = {s: sum(p[0] for p in ps) for s, ps in gnn[suite].items()}
        med = _median_seed(tot)
        null = sum(p[1] for p in gnn[suite][med])
        margins.append((null - tot[med]) / null * 100)
    check("margin over null, original battery, min %", "0.7", f"{min(margins):.1f}")
    check("margin over null, original battery, max %", "2.8", f"{max(margins):.1f}")
    cs_tot = {s: sum(p[0] for p in ps) for s, ps in gnn["csmith-v0"].items()}
    med = _median_seed(cs_tot)
    cs_oz = sum(p[2]["oz"] for p in gnn["csmith-v0"][med])
    check("csmith: sampled GNN below -Oz %", 16,
          (cs_oz - cs_tot[med]) / cs_oz * 100, tol=0.05)

    # iso-k and safe% (Table II), median over seeds / median seed by gain
    iso_expected = {"mibench-v1": 23, "chstone-v0": 32, "blas-v0": 20,
                    "csmith-v0": ">50", "npb-v0": 11, "poj104-v1": 12,
                    "anghabench-v1": 17, "github-v0": 17, "linux-v0": 2,
                    "llvm-stress-v0": 49}
    safe_expected = {"mibench-v1": "1.8", "chstone-v0": "7.3", "blas-v0": "2.0",
                     "csmith-v0": "18.2", "npb-v0": "10.0", "poj104-v1": "7.9",
                     "anghabench-v1": "1.1", "github-v0": "1.2",
                     "linux-v0": "0.6", "llvm-stress-v0": "3.1"}
    iso_all = {}
    for suite, seeds in gnn.items():
        per_seed = {}
        for s, ps in seeds.items():
            best = sum(p[0] for p in ps)
            per_seed[s] = next(
                (k for k in range(1, 51)
                 if sum(min(eps[(suite, p[2]["uri"])][:k]) for p in ps) <= best),
                51)
        iso_all[suite] = per_seed
        med = sorted(per_seed.values())[1]
        check(f"Table II iso-k {suite}", iso_expected[suite],
              ">50" if med > 50 else med, tol=0)
        gains = {s: 100 * sum((p[2]["oz"] - min(p[0], p[2]["oz"])) / p[2]["oz"]
                              for p in ps) / len(ps) for s, ps in seeds.items()}
        med_gain = gains[_median_seed(gains)]
        check(f"Table II safe% {suite}", safe_expected[suite], f"{med_gain:.1f}")
    check("csmith: seeds matched within 50 episodes", 1,
          sum(v <= 50 for v in iso_all["csmith-v0"].values()), tol=0)
    cb_iso = json.load(open("results/reframe_stats_ppo_gnn.json"))["iso_k"]["cbench"]
    check("cBench: seeds matched within 50 episodes", 0,
          sum(v is not None for v in cb_iso.values()), tol=0)
    eight = [v for s, v in iso_expected.items()
             if s not in ("csmith-v0", "linux-v0")]
    check("iso-k range on the eight sources, min", 11, min(eight), tol=0)
    check("iso-k range on the eight sources, max", 49, max(eight), tol=0)

    # per-program W/T/L on the original 347 (seed 42) and the 88-92% range
    shares = {}
    for s in ("42", "123", "456"):
        w = t = l = 0
        for suite in ORIG6:
            for a, z, _ in gnn[suite][s]:
                w += a < z
                t += a == z
                l += a > z
        shares[s] = (w, t, l)
    check("W/T/L vs null, original 347, seed 42", [175, 145, 27], list(shares["42"]))
    good = [100 * (w + t) / (w + t + l) for w, t, l in shares.values()]
    check("at least as good as null, min %", 88, min(good), tol=0.01)
    check("at least as good as null, max %", 92, max(good), tol=0.01)

    # k=32 rerun on NPB: prefix-8 and four disjoint eight-sample slices
    k32 = {}
    for path in sorted(glob.glob("results/battery_policy_k32/npb-v0/ppo_gnn_seed*/*.json")):
        seed = path.replace("\\", "/").split("/")[-2].split("seed")[-1]
        k32.setdefault(seed, []).append(json.load(open(path)))
    prefix_wins = slice_wins = slices_sig = prefix_sig = 0
    for seed, rs in k32.items():
        for i in range(4):
            a = [min(r["sample_ics"][8 * i: 8 * i + 8]) for r in rs]
            z = [min(eps[("npb-v0", r["uri"])][8 * i: 8 * i + 8]) for r in rs]
            p = stats.wilcoxon(a, z, alternative="less").pvalue
            slice_wins += sum(a) < sum(z)
            slices_sig += p < 0.05
            if i == 0:
                prefix_wins += sum(a) < sum(z)
                prefix_sig += p < 1e-3
    check("NPB k=32: seeds reproducing the suite-total win", 1, prefix_wins, tol=0)
    check("NPB k=32: slices flipping the total (of 12)", 7, 12 - slice_wins, tol=0)
    check("NPB k=32: slices with p<0.05 (of 12)", 12, slices_sig, tol=0)
    check("NPB k=32: first-eight p<1e-3 (of 3 seeds)", 3, prefix_sig, tol=0)

    # cBench k=8 vs greedy; budgets
    fe = json.load(open("results/final_evaluation.json"))["splits"]
    greedy = sum(sum(fe[s]["method_ics"]["greedy"]) for s in ("validation", "test"))
    samp = json.load(open("results/sampling_evaluation.json"))["summary"]["ppo_gnn"]
    gaps = [100 * ((samp[f"validation_seed{s}"]["best_of_k_total"]
                    + samp[f"test_seed{s}"]["best_of_k_total"]) / greedy - 1)
            for s in ("42", "123", "456")]
    check("cBench k=8 GNN vs greedy, min gap %", 0.06, min(gaps), tol=0.1)
    check("cBench k=8 GNN vs greedy, max gap %", 0.35, max(gaps), tol=0.05)
    check("cBench k=8 GNN within 0.4% of greedy", True, bool(max(gaps) < 0.4))
    cb = json.load(open("results/full_baselines_v2.json"))["baselines"]
    steps = [len(b["greedy_actions"]) for b in cb if b["split"] in ("validation", "test")]
    comp = (sum(steps) / len(steps) + 1) * 124
    check("greedy compilations per cBench program", 1970, comp, tol=0.01)
    check("k=32 budget as % of greedy", 73, 32 * 45 / comp * 100, tol=0.01)
    check("k=8 budget as % of greedy (README ~18%)", 18, 8 * 45 / comp * 100, tol=0.03)
    k32c = json.load(open("results/sampling_evaluation_k32.json"))
    null32 = sum(k32c["random_null"].values())
    ap32 = [k32c["summary"]["ppo_autophase"][f"validation_seed{s}"]["best_of_k_total"]
            + k32c["summary"]["ppo_autophase"][f"test_seed{s}"]["best_of_k_total"]
            for s in ("42", "123", "456")]
    check("k=32 Autophase seeds surpassing greedy", 1, sum(v < greedy for v in ap32), tol=0)
    check("k=32 Autophase seeds trailing the null", 2, sum(v > null32 for v in ap32), tol=0)
    check("argmax Wilcoxon AP vs GNN, validation p", 0.625,
          fe["validation"]["wilcoxon_ap_vs_gnn"]["p_value"], tol=0.01)
    check("argmax Wilcoxon AP vs GNN, test p", 0.875,
          fe["test"]["wilcoxon_ap_vs_gnn"]["p_value"], tol=0.01)

    # ---- Sec. IV-C: controls (seed 42, original six suites) ------------
    def load(var, suite, seed=42):
        return {json.load(open(p))["uri"]: json.load(open(p)) for p in glob.glob(
            f"results/battery_policy/{suite}/{var}_seed{seed}/*.json")}
    ps_untr, ps_nd, gains_ol, wtl = [], [], {}, [0, 0, 0]
    for suite in ORIG6:
        base = load("ppo_gnn", suite)
        for var, sink in (("ppo_gnn_untrained", ps_untr), ("ppo_gnn_nodropout", ps_nd)):
            d = load(var, suite)
            sink.append(stats.wilcoxon([r["best_of_k_ic"] for r in d.values()],
                                       [r["random_null_best_of_k"] for r in d.values()],
                                       alternative="less").pvalue)
        nd = load("ppo_gnn_nodropout", suite)
        for u in nd:
            a, b = nd[u]["best_of_k_ic"], base[u]["best_of_k_ic"]
            wtl[0 if a < b else 1 if a == b else 2] += 1
        ol = load("ppo_gnn_openloop", suite)
        null = sum(r["random_null_best_of_k"] for r in base.values())
        closed = null - sum(r["best_of_k_ic"] for r in base.values())
        gains_ol[suite] = (null - sum(r["best_of_k_ic"] for r in ol.values())) / closed
    check("untrained: min one-sided p >= 0.12", True, bool(min(ps_untr) >= 0.12))
    check("no-dropout: largest one-sided p", 0.016, max(ps_nd), tol=0.05)
    check("no-dropout vs dropout W/T/L", [58, 226, 63], wtl)
    easy = [gains_ol[s] for s in ("mibench-v1", "blas-v0", "chstone-v0")]
    check("open-loop share of closed-loop gain, min (CHStone)", 0.90, min(easy), tol=0.02)
    check("open-loop share of closed-loop gain, max (MiBench)", 1.41, max(easy), tol=0.02)
    check("open-loop loses on NPB and POJ-104", True,
          bool(gains_ol["npb-v0"] < 0 and gains_ol["poj104-v1"] < 0))
    tot = {v: sum(json.load(open(p))["best_of_k_ic"] for s in ORIG6 for p in glob.glob(
        f"results/battery_policy/{s}/{v}_seed42/*.json"))
           for v in ("ppo_gnn", "ppo_gnn_openloop")}
    null8 = sum(json.load(open(p))["random_null_best_of_k"] for s in ORIG6 for p in glob.glob(
        f"results/battery_policy/{s}/ppo_gnn_seed42/*.json"))
    check("open-loop share of the gain overall", 0.35,
          (null8 - tot["ppo_gnn_openloop"]) / (null8 - tot["ppo_gnn"]), tol=0.05)
    port_p, port_wins = [], 0
    csmith_p = None
    for suite in ORIG6:
        port = {json.load(open(p))["uri"]: json.load(open(p)) for p in glob.glob(
            f"results/portfolio_eval/{suite}/portfolio_seed0/*.json")}
        base = load("ppo_gnn", suite)
        a = [port[u]["best_of_8_ic"] for u in base]
        b = [base[u]["best_of_k_ic"] for u in base]
        port_wins += sum(a) < sum(port[u]["random_null_best_of_8"] for u in base)
        if suite in ("mibench-v1", "blas-v0", "chstone-v0"):
            port_p.append(stats.wilcoxon(a, b, alternative="less").pvalue)
        if suite == "csmith-v0":
            per = {}
            for seed in (42, 123, 456):
                for u, r in load("ppo_gnn", suite, seed).items():
                    per.setdefault(u, []).append(r["best_of_k_ic"])
            csmith_p = stats.wilcoxon([float(np.median(per[u])) for u in per],
                                      [port[u]["best_of_8_ic"] for u in per],
                                      alternative="less").pvalue
    check("portfolio-8 beats the null on suites (of 6)", 5, port_wins, tol=0)
    check("portfolio-8 < GNN on MiBench/BLAS/CHStone, largest p", 0.006,
          max(port_p), tol=0.1)
    check("csmith: GNN (median seeds) < portfolio-8 p", 0.004, csmith_p, tol=0.1)

    # ---- Sec. IV-D: plateau timing and pretraining data -----------------
    fracs = []
    for seed in (42, 123, 456):
        steps, first = 0, None
        for line in open(f"results/train_gnn_seed{seed}_log.txt", errors="ignore"):
            m = re.search(r"Steps:\s+(\d+)/(\d+)", line)
            if m:
                steps, budget = int(m.group(1)), int(m.group(2))
            if first is None and re.search(r"VAL \| Total IC: 689\b", line):
                first = steps
        fracs.append(100 * first / budget)
    check("GNN plateau reached, earliest % of budget", 10, int(min(fracs)), tol=0)
    check("GNN plateau reached, latest % of budget", 17, -(-max(fracs) // 1), tol=0)
    pre = json.load(open("results/gnn_pretrained/pretrain_log.json"))
    check("pretraining states", 2430, pre["num_samples"], tol=0)
    check("pretraining program cap (IC)", 20000, pre["config"]["max_ic"], tol=0)

    # ---- Sec. IV-E: binary metrics ---------------------------------------
    anchor = json.load(open("results/text_size_anchor.json"))
    check("Pearson r over all 36 programs", 0.19, anchor["pearson_r"], tol=0.05)
    check("Pearson n (all programs)", 36, anchor["n_programs"], tol=0)
    x86 = json.load(open("results/binary_metrics/_aggregate.json"))
    arm = json.load(open("results/binary_metrics_arm/_aggregate.json"))
    for k in ("o0", "oz", "rnd_bo8", "gnn_bo8"):
        d = x86["summary"][k]
        check(f"footprint: .text share of {k} < 0.1%", True,
              bool(100 * d["text_total"] / d["footprint_total"] < 0.1))
    s = x86["summary"]
    check("footprint: -Oz vs random delta < 0.03%", True,
          bool(abs(s["oz"]["footprint_total"] - s["rnd_bo8"]["footprint_total"])
               / s["oz"]["footprint_total"] * 100 < 0.03))
    pa = {p["uri"]: p for p in x86["programs"]}
    pb = {p["uri"]: p for p in arm["programs"]}
    big = [u for u in pa if "gnn_bo8" not in pa[u]]
    check("programs above 6000 IC in the binary battery", 24, len(big), tol=0)
    check("large programs all above 6000 IC", True,
          bool(min(pa[u]["o0"]["ic"] for u in big) > 6000))
    oz_big = sum(pa[u]["oz"]["text"] for u in big)
    draws = [100 * (sum(d[u]["rnd_bo8"]["text"] for u in big) / oz_big - 1)
             for d in (pa, pb)]
    check("large 24: random best-of-8 above -Oz, draw min %", 12, min(draws), tol=0.05)
    check("large 24: random best-of-8 above -Oz, draw max %", 29, max(draws), tol=0.05)
    oz_all = sum(pa[u]["oz"]["text"] for u in pa)
    all_draws = [100 * (1 - sum(d[u]["rnd_bo8"]["text"] for u in pa) / oz_all)
                 for d in (pa, pb)]
    check("all 371: random best-of-8 below -Oz, draw 1 %", 4.0, max(all_draws), tol=0.02)
    check("all 371: random best-of-8 above -Oz, draw 2 %", "0.1",
          f"{-min(all_draws):.1f}")
    check("GNN x86 .text identical across the two runs", True,
          bool(all(pa[u]["gnn_bo8"]["text"] == pb[u]["gnn_bo8"]["text"]
                   for u in pa if u not in big)))

    # ---- Sec. V: LLVM 18 transfer (csmith excluded) ---------------------
    recs = [json.load(open(p)) for p in glob.glob("results/llvm18_transfer/*/*.json")]
    five = [r for r in recs if r["suite"] != "csmith-v0"]
    check("LLVM 18: programs that port (csmith excluded)", 314, len(five), tol=0)
    attempted = sum(len(glob.glob(f"results/battery_policy/{s}/ppo_gnn_seed42/*.json"))
                    for s in ORIG6 if s != "csmith-v0")
    check("LLVM 18: programs attempted (five suites)", 319, attempted, tol=0)
    check("LLVM 18: csmith programs that port (of 28)", 8,
          sum(r["suite"] == "csmith-v0" for r in recs), tol=0)
    oz18 = sum(r["oz"]["text"] for r in five)
    for key, pct, wins, losses in (("portfolio_bo8", 10.6, 169, 89),
                                   ("portfolio_bo16", 10.9, 174, 83)):
        a = [r[key]["text"] for r in five]
        z = [r["oz"]["text"] for r in five]
        check(f"LLVM 18 {key} below -Oz %", pct, 100 * (1 - sum(a) / oz18), tol=0.01)
        check(f"LLVM 18 {key} per-program wins", wins, sum(x < y for x, y in zip(a, z)), tol=0)
        check(f"LLVM 18 {key} per-program losses", losses, sum(x > y for x, y in zip(a, z)), tol=0)
        check(f"LLVM 18 {key} one-sided p < 1e-11", True,
              bool(stats.wilcoxon(a, z, alternative="less").pvalue < 1e-11))
    check("LLVM 18 approximated passes", 3,
          len(json.load(open("results/llvm18_transfer/_aggregate.json"))["approximated_passes"]),
          tol=0)


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
    prose_claims()

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

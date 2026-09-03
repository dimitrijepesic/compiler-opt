#!/usr/bin/env python3
"""
Fig. 1 for the paper: quality vs. compilation budget on the 347-program
original battery (MiBench, CHStone, BLAS, csmith, NPB, POJ-104), the
programs with a stored best-of-32 GNN evaluation.

Curves are summed IC over the 347 programs, relative to -Oz:
  * random search: expected best-of-k of the 50 stored random episodes
    per program (k = 1..50, resampled);
  * PPO+Autophase: expected best-of-k of the 8 stored samples (k <= 8),
    mean over three seeds;
  * PPO+GNN: expected best-of-k of the 32 stored samples from the k=32
    rerun (k <= 32), mean over three seeds.

Outputs paper/figures/battery.pdf (+ .png preview) and prints the plotted
values.
"""

import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = "paper/figures"
EPISODE_STEPS = 45
SUITES = ["mibench-v1", "chstone-v0", "blas-v0", "csmith-v0", "npb-v0",
          "poj104-v1"]

C_AP = "#2a78d6"
C_GNN = "#eb6834"
MUTED = "#898781"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e1e0d9"
SURFACE = "#ffffff"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "axes.edgecolor": "#c3c2b7",
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK_2, "ytick.color": INK_2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "sans-serif", "font.size": 9,
})


def expected_best_of_k(ics, k, rng, n_resample=1000):
    ics = np.asarray(ics)
    if k >= len(ics):
        return float(ics.min())
    idx = np.array([rng.choice(len(ics), size=k, replace=False)
                    for _ in range(n_resample)])
    return float(ics[idx].min(axis=1).mean())


def load_records(root, agent, seed):
    out = {}
    for suite in SUITES:
        for path in glob.glob(os.path.join(root, suite, f"{agent}_seed{seed}",
                                           "*.json")):
            with open(path) as f:
                r = json.load(f)
            out[r["uri"]] = r
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = np.random.default_rng(42)

    episodes, oz = {}, {}
    for suite in SUITES:
        with open(os.path.join("results/battery", suite, "_aggregate.json")) as f:
            for r in json.load(f)["benchmarks"]:
                if "random_reduced_episode_ics" in r:
                    episodes[r["uri"]] = r["random_reduced_episode_ics"]
                    oz[r["uri"]] = r["oz"]

    gnn32 = {s: load_records("results/battery_policy_k32", "ppo_gnn", s)
             for s in (42, 123, 456)}
    ap8 = {s: load_records("results/battery_policy", "ppo_autophase", s)
           for s in (42, 123, 456)}
    uris = sorted(set.intersection(*(set(d) for d in gnn32.values())))
    uris = [u for u in uris if all(u in d for d in ap8.values())]
    n = len(uris)
    oz_total = sum(oz[u] for u in uris)
    print(f"programs: {n}, -Oz total {oz_total}")

    ks_null = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 50]
    null_curve = [sum(expected_best_of_k(episodes[u], k, rng) for u in uris)
                  for k in ks_null]

    def policy_curve(recs_by_seed, ks):
        seed_curves = []
        for recs in recs_by_seed.values():
            seed_curves.append([
                sum(expected_best_of_k(recs[u]["sample_ics"], k, rng)
                    for u in uris) for k in ks])
        return np.mean(seed_curves, axis=0)

    ks_gnn = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
    ks_ap = [1, 2, 3, 4, 6, 8]
    gnn_curve = policy_curve(gnn32, ks_gnn)
    ap_curve = policy_curve(ap8, ks_ap)

    def rel(v):
        return 100.0 * (np.asarray(v) / oz_total - 1.0)

    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    ax.plot([k * EPISODE_STEPS for k in ks_null], rel(null_curve),
            color=MUTED, linewidth=1.6, marker="s", markersize=3,
            label="Random search (36-pass space)")
    ax.plot([k * EPISODE_STEPS for k in ks_ap], rel(ap_curve), color=C_AP,
            linewidth=1.8, marker="o", markersize=3.5,
            label="PPO+Autophase (best-of-k samples)")
    ax.plot([k * EPISODE_STEPS for k in ks_gnn], rel(gnn_curve), color=C_GNN,
            linewidth=1.8, marker="o", markersize=3.5,
            label="PPO+GNN (best-of-k samples)")
    ax.axhline(0.0, color=MUTED, linestyle="--", linewidth=1.1)
    ax.annotate("-Oz", xy=(0.02, 0.0), xycoords=("axes fraction", "data"),
                xytext=(0, 3), textcoords="offset points", ha="left",
                fontsize=8, color=INK_2)
    ax.set_xscale("log")
    ax.set_xlabel("Compilations per program (log scale)", labelpad=1.5)
    ax.set_ylabel("Total IC vs. -Oz (%)", labelpad=1.5)
    ax.tick_params(pad=1.5)
    ax.legend(frameon=True, framealpha=0.95, edgecolor="none", fontsize=7.2,
              loc="upper right", borderpad=0.4, handlelength=1.6,
              labelspacing=0.35)
    fig.tight_layout(pad=0.25)
    fig.savefig(os.path.join(OUT_DIR, "battery.pdf"), bbox_inches="tight",
                pad_inches=0.02)
    fig.savefig(os.path.join(OUT_DIR, "battery.png"), dpi=300,
                bbox_inches="tight", pad_inches=0.02)

    print("k, random, AP, GNN (total IC; % vs -Oz)")
    for k in ks_null:
        row = [f"k={k:>2}", f"{null_curve[ks_null.index(k)]:.0f}"
               f" ({rel(null_curve[ks_null.index(k)]):+.1f}%)"]
        row.append(f"{ap_curve[ks_ap.index(k)]:.0f} "
                   f"({rel(ap_curve[ks_ap.index(k)]):+.1f}%)"
                   if k in ks_ap else "-")
        row.append(f"{gnn_curve[ks_gnn.index(k)]:.0f} "
                   f"({rel(gnn_curve[ks_gnn.index(k)]):+.1f}%)"
                   if k in ks_gnn else "-")
        print("  " + "  ".join(row))
    # iso-quality budget: smallest random k whose expected total matches GNN k=8
    g8 = gnn_curve[ks_gnn.index(8)]
    fine = list(range(1, 51))
    fine_null = [sum(expected_best_of_k(episodes[u], k, rng, 300) for u in uris)
                 for k in fine]
    iso = next((k for k, v in zip(fine, fine_null) if v <= g8), None)
    print(f"GNN k=8 total {g8:.0f}; random search matches it at k={iso}")
    g32 = gnn_curve[ks_gnn.index(32)]
    iso32 = next((k for k, v in zip(fine, fine_null) if v <= g32), None)
    print(f"GNN k=32 total {g32:.0f}; random search matches it at k={iso32}")
    print(f"Saved: {OUT_DIR}/battery.pdf + .png")


if __name__ == "__main__":
    main()

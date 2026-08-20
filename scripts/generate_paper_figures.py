#!/usr/bin/env python3
"""
Publication figures for the TELFOR paper.

Fig P1 (the centerpiece): quality vs. compilation budget on the cBench
validation+test programs. Best-of-k policy sampling curves (k=1..8, mean
across seeds) against the expected best-of-k of random episodes in the
same 36-pass space (k=1..50, resampled from the stored per-episode ICs)
and the measured greedy-search points (cost = (steps+1) x |full action
space| compilations, from the recorded greedy runs).

Outputs paper/figures/pareto.pdf (vector, for the IEEE manuscript) and
a PNG preview.
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

OUT_DIR = "paper/figures"
EPISODE_STEPS = 45
FULL_ACTION_SPACE = 124  # greedy searched the full action space

# palette (light mode, print-safe)
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


def expected_best_of_k(episode_ics, k, rng, n_resample=2000):
    """Expected min of k episodes drawn without replacement, by resampling."""
    ics = np.array(episode_ics)
    if k >= len(ics):
        return float(ics.min())
    mins = [
        rng.choice(ics, size=k, replace=False).min()
        for _ in range(n_resample)
    ]
    return float(np.mean(mins))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Prefer the k=32 evaluation (longer curves) when available
    sampling_path = "results/sampling_evaluation_k32.json"
    if not os.path.exists(sampling_path):
        sampling_path = "results/sampling_evaluation.json"
    with open(sampling_path) as f:
        sampling = json.load(f)
    max_k = sampling.get("k", 8)
    policy_ks = [k for k in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32] if k <= max_k]
    with open("results/full_baselines_v2.json") as f:
        baselines = {b["short_name"]: b for b in json.load(f)["baselines"]}

    # Benchmarks: cBench val+test as used in the sampling evaluation
    bench_names = list(next(iter(
        sampling["agents"]["ppo_autophase"].values())).keys())
    print(f"benchmarks: {bench_names}")

    rng = np.random.default_rng(42)

    # --- Policy curves: mean over seeds of sum-over-benchmarks best-of-k
    curves = {}
    for agent_key, color, label in [
        ("ppo_autophase", C_AP, "PPO+Autophase (best-of-k samples)"),
        ("ppo_gnn", C_GNN, "PPO+GNN (best-of-k samples)"),
    ]:
        seed_curves = []
        for seed, per_bm in sampling["agents"][agent_key].items():
            totals = []
            for k in policy_ks:
                # expected best-of-k from the stored samples (resampled)
                total = sum(
                    expected_best_of_k(r["sample_ics"], k, rng)
                    for r in per_bm.values()
                )
                totals.append(total)
            seed_curves.append(totals)
        curves[agent_key] = (np.array(seed_curves).mean(axis=0), color, label)

    # --- Random null curve: expected best-of-k for k=1..50
    ks_null = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 50]
    null_curve = []
    for k in ks_null:
        total = sum(
            expected_best_of_k(
                baselines[n]["random_reduced_episode_ics"], k, rng)
            for n in bench_names
        )
        null_curve.append(total)

    # --- Greedy point: measured IC total and measured compilation cost
    greedy_total = sum(baselines[n]["greedy"] for n in bench_names)
    greedy_cost = sum(
        (baselines[n]["greedy_num_steps"] + 1) * FULL_ACTION_SPACE
        for n in bench_names
    ) / len(bench_names)  # avg per program

    oz_total = sum(baselines[n]["oz"] for n in bench_names)

    # --- Plot
    fig, ax = plt.subplots(figsize=(3.5, 2.7))  # IEEE single-column size

    x_null = [k * EPISODE_STEPS for k in ks_null]
    ax.plot(x_null, null_curve, color=MUTED, linewidth=1.6, marker="s",
            markersize=3, label="Random search (36-pass space)")

    for agent_key in ["ppo_autophase", "ppo_gnn"]:
        totals, color, label = curves[agent_key]
        x = [k * EPISODE_STEPS for k in policy_ks]
        ax.plot(x, totals, color=color, linewidth=1.8, marker="o",
                markersize=3.5, label=label)

    ax.scatter([greedy_cost], [greedy_total], color=INK, marker="*",
               s=90, zorder=5, label="Greedy search (measured)")
    ax.axhline(oz_total, color=MUTED, linestyle="--", linewidth=1.1)
    ax.annotate("-Oz", xy=(0.02, oz_total), xycoords=("axes fraction", "data"),
                xytext=(0, 3), textcoords="offset points",
                ha="left", fontsize=8, color=INK_2)

    ax.set_xscale("log")
    ax.set_xlabel("Compilations per program (log scale)", labelpad=1.5)
    ax.set_ylabel("Total instruction count", labelpad=1.5)
    ax.tick_params(pad=1.5)
    ax.legend(frameon=True, framealpha=0.95, edgecolor="none",
              fontsize=7.2, loc="upper right", borderpad=0.4,
              handlelength=1.6, labelspacing=0.35)
    fig.tight_layout(pad=0.25)
    fig.savefig(os.path.join(OUT_DIR, "pareto.pdf"),
                bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(OUT_DIR, "pareto.png"), dpi=300,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    print(f"greedy: total={greedy_total} avg cost={greedy_cost:.0f} compiles")
    print(f"oz total: {oz_total}")
    for agent_key, (totals, _, _) in curves.items():
        print(f"{agent_key}: k=1 {totals[0]:.0f} ... k=8 {totals[-1]:.0f} "
              f"(cost {8 * EPISODE_STEPS}/program)")
    print(f"null: k=8 {null_curve[ks_null.index(8)]:.0f} "
          f"k=50 {null_curve[-1]:.0f}")
    print(f"Saved: {OUT_DIR}/pareto.pdf + .png")


if __name__ == "__main__":
    main()

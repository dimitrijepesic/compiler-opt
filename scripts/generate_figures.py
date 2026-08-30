#!/usr/bin/env python3
"""
Generate paper figures from training logs + evaluation results.

fig1: training curves (avg episode reward vs steps), per-seed + mean
fig2: validation curves (val-small total IC vs steps) with baseline
       reference lines: the data-efficiency figure
fig3: policy entropy and approx KL (small multiples, shared x)
fig4: final comparison bars on validation-full and test splits

Inputs (all optional, missing ones skip their figure):
  results/ppo_autophase/training_log_seed*.json
  results/ppo_gnn/training_log_seed*.json
  results/full_baselines_v2.json
  results/final_evaluation.json
"""

import glob
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

FIG_DIR = "results/figures"

# Palette (light mode): categorical slots in fixed order; chrome inks.
C_AP = "#2a78d6"       # slot 1 blue, PPO + Autophase
C_GNN = "#eb6834"      # slot 2 orange, PPO + GNN
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE_AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "axes.edgecolor": BASELINE_AXIS,
    "axes.labelcolor": INK_2,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "sans-serif",
    "font.size": 11,
})

AGENTS = [
    ("ppo_autophase", "PPO + Autophase", C_AP, "results/ppo_autophase"),
    ("ppo_gnn", "PPO + GNN", C_GNN, "results/ppo_gnn"),
]


def load_logs(log_dir):
    """Return {seed: log_dict} for all training logs in a directory."""
    logs = {}
    for path in sorted(glob.glob(os.path.join(log_dir, "training_log_seed*.json"))):
        with open(path) as f:
            d = json.load(f)
        logs[d["seed"]] = d
    return logs


def series(log, key):
    """(steps, values) for entries of a training log containing `key`."""
    xs, ys = [], []
    for e in log["log"]:
        if key in e:
            xs.append(e["total_steps"])
            ys.append(e[key])
    return np.array(xs), np.array(ys)


def mean_curve(logs, key):
    """Interpolate each seed's curve onto a common step grid, return
    (grid, mean, min, max). Assumes same cadence across seeds."""
    curves = [series(log, key) for log in logs.values()]
    curves = [(x, y) for x, y in curves if len(x) > 0]
    if not curves:
        return None
    grid = curves[0][0]
    ys = np.stack([np.interp(grid, x, y) for x, y in curves])
    return grid, ys.mean(axis=0), ys.min(axis=0), ys.max(axis=0)


def fig1_training(all_logs):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for key, label, color, _ in AGENTS:
        logs = all_logs.get(key, {})
        if not logs:
            continue
        for seed, log in logs.items():
            x, y = series(log, "avg_episode_reward")
            ax.plot(x, y, color=color, linewidth=0.9, alpha=0.30)
        mc = mean_curve(logs, "avg_episode_reward")
        if mc:
            grid, mean, _, _ = mc
            ax.plot(grid, mean, color=color, linewidth=2,
                    label=f"{label} (mean of {len(logs)} seeds)")
    ax.set_xlabel("Environment steps")
    ax.set_ylabel("Avg episode reward")
    ax.set_title("Training reward, identical budget and training set", color=INK)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig1_training_curves.png"), dpi=200)
    plt.close(fig)
    print("  fig1_training_curves.png")


def fig2_validation(all_logs, baselines):
    fig, ax = plt.subplots(figsize=(8, 4.5))

    for key, label, color, _ in AGENTS:
        logs = all_logs.get(key, {})
        if not logs:
            continue
        mc = mean_curve(logs, "val_total_ic")
        if mc:
            grid, mean, lo, hi = mc
            ax.fill_between(grid, lo, hi, color=color, alpha=0.15, linewidth=0)
            ax.plot(grid, mean, color=color, linewidth=2, marker="o",
                    markersize=4, label=f"{label} (mean, {len(logs)} seeds)")

    # Baseline reference lines on the SAME val-small benchmarks
    if baselines:
        val_small = ["crc32", "qsort", "stringsearch2"]
        rows = {b["short_name"]: b for b in baselines["baselines"]}
        refs = [
            ("Greedy", sum(rows[n]["greedy"] for n in val_small), "-"),
            ("O3 (real)", sum(rows[n]["o3"] for n in val_small), "--"),
            ("Random-36 (best of 50)",
             sum(rows[n]["random_reduced_search"] for n in val_small), ":"),
        ]
        # Merge references that share a value so their labels don't collide
        merged = {}
        for name, total, style in refs:
            if total in merged:
                merged[total] = (f"{merged[total][0]} = {name}", merged[total][1])
            else:
                merged[total] = (name, style)
        refs = [(name, total, style) for total, (name, style) in merged.items()]
        for name, total, style in refs:
            ax.axhline(total, color=MUTED, linestyle=style, linewidth=1.2)
            ax.annotate(f"{name} = {total}", xy=(1.0, total),
                        xycoords=("axes fraction", "data"),
                        xytext=(-4, 3), textcoords="offset points",
                        ha="right", fontsize=9, color=INK_2)

    ax.set_xlabel("Environment steps")
    ax.set_ylabel("Validation total IC (lower = better)")
    ax.set_title("Validation performance vs training steps (val-small)", color=INK)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig2_validation_curves.png"), dpi=200)
    plt.close(fig)
    print("  fig2_validation_curves.png")


def fig3_entropy_kl(all_logs):
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    panels = [("entropy", "Policy entropy"), ("approx_kl", "Approx. KL per update")]
    for ax, (key_metric, title) in zip(axes, panels):
        for key, label, color, _ in AGENTS:
            logs = all_logs.get(key, {})
            if not logs:
                continue
            mc = mean_curve(logs, key_metric)
            if mc:
                grid, mean, lo, hi = mc
                ax.fill_between(grid, lo, hi, color=color, alpha=0.15, linewidth=0)
                ax.plot(grid, mean, color=color, linewidth=2, label=label)
        ax.set_ylabel(title)
        ax.legend(frameon=False)
    if all_logs.get("ppo_autophase") or all_logs.get("ppo_gnn"):
        # Uniform-policy entropy over 36 actions, for reference
        axes[0].axhline(np.log(36), color=MUTED, linestyle="--", linewidth=1)
        axes[0].annotate("uniform ln(36)", xy=(1.0, np.log(36)),
                         xycoords=("axes fraction", "data"),
                         xytext=(-4, 3), textcoords="offset points",
                         ha="right", fontsize=9, color=INK_2)
    axes[1].set_xlabel("Environment steps")
    fig.suptitle("Optimization diagnostics", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig3_entropy.png"), dpi=200)
    plt.close(fig)
    print("  fig3_entropy.png")


def fig4_final(final_eval):
    methods = [
        ("o3", "O3 (real)", MUTED),
        ("oz", "Oz (real)", MUTED),
        ("random_reduced_search", "RndRed-50", MUTED),
        ("greedy", "Greedy", INK_2),
        ("ppo_autophase", "PPO+AP", C_AP),
        ("ppo_gnn", "PPO+GNN", C_GNN),
    ]
    splits = [s for s in ["validation", "test"] if s in final_eval["splits"]]
    fig, axes = plt.subplots(1, len(splits), figsize=(6 * len(splits), 4.5))
    if len(splits) == 1:
        axes = [axes]

    for ax, split in zip(axes, splits):
        data = final_eval["splits"][split]
        labels, totals, colors, errs = [], [], [], []
        for m, label, color in methods:
            if m in data["method_ics"]:
                total = sum(data["method_ics"][m])
            elif m in data.get("agents", {}):
                total = data["agents"][m]["summary"]["mean_total_ic"]
            else:
                continue
            err = 0
            if m in data.get("agents", {}):
                summary = data["agents"][m]["summary"]
                total = summary["mean_total_ic"]
                err = summary["std_total_ic"]
            labels.append(label)
            totals.append(total)
            colors.append(color)
            errs.append(err)

        x = np.arange(len(labels))
        bars = ax.bar(x, totals, width=0.62, color=colors,
                      yerr=[e if e else 0 for e in errs],
                      error_kw={"ecolor": INK_2, "capsize": 3, "linewidth": 1})
        for xi, total in zip(x, totals):
            ax.annotate(f"{total:,.0f}", xy=(xi, total),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", fontsize=9, color=INK_2)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20, ha="right")
        ax.set_ylabel("Total IC (lower = better)")
        ax.set_title(f"{split} split", color=INK)
        ax.grid(axis="x", visible=False)

    fig.suptitle("Final comparison, agents show mean ± std across seeds",
                 color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig4_best_val_comparison.png"), dpi=200)
    plt.close(fig)
    print("  fig4_best_val_comparison.png")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    print("Generating figures:")

    all_logs = {}
    for key, _, _, log_dir in AGENTS:
        all_logs[key] = load_logs(log_dir)

    baselines = None
    if os.path.exists("results/full_baselines_v2.json"):
        with open("results/full_baselines_v2.json") as f:
            baselines = json.load(f)

    final_eval = None
    if os.path.exists("results/final_evaluation.json"):
        with open("results/final_evaluation.json") as f:
            final_eval = json.load(f)

    if any(all_logs.values()):
        fig1_training(all_logs)
        fig2_validation(all_logs, baselines)
        fig3_entropy_kl(all_logs)
    else:
        print("  (no training logs found, skipping fig1-3)")

    if final_eval:
        fig4_final(final_eval)
    else:
        print("  (no final_evaluation.json, skipping fig4)")


if __name__ == "__main__":
    main()

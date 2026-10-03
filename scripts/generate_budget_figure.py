#!/usr/bin/env python3
"""Budget-quality figure for paper/telfor_safe_selector.tex (figure*, full width).

Input: results/budgeted_selector_review/verification.json, which
scripts/verify_budgeted_selector.py recomputes from the frozen per-program
records. No value is typed into the plotting code. Bands are min-max over
checkpoints/realizations, never confidence intervals.

Run from the repository root:  python3 scripts/generate_budget_figure.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
})
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "results/budgeted_selector_review/verification.json"
OUT = ROOT / "paper/figures"
STEM = "budget_curve"
KS = list(range(1, 9))
GNN = ["gnn42", "gnn123", "gnn456"]
RND = [f"rnd{s}" for s in range(42, 47)]
BLUE, ORANGE, GRAY, INK, GRID = "#2c6eaa", "#d9772a", "#7a7a7a", "#1a1a1a", "#dddddd"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def band(curves, pools, rule):
    lo, hi = [], []
    for k in KS:
        vals = []
        for p in pools:
            v = curves[p][rule][str(k)]
            vals.append(v if isinstance(v, float) else v["gain_code_pct"])
        lo.append(min(vals)); hi.append(max(vals))
    return lo, hi


def series(curves, pool, rule):
    out = []
    for k in KS:
        v = curves[pool][rule][str(k)]
        out.append(v if isinstance(v, float) else v["gain_code_pct"])
    return out


def panel(ax, curves, title, ylim, labels):
    plotted = {}
    # Reference rules: pooled min-max bands over all eight pools.
    for rule, alpha, ls, name in (
            ("none", 0.14, ":", "IC shortlist, no fallback (8 pools)"),
            ("plain_best_of_k_code", 0.30, "--", "k arbitrary candidates + fallback (8 pools)")):
        lo, hi = band(curves, GNN + RND, rule)
        ax.fill_between(KS, lo, hi, color=GRAY, alpha=alpha, linewidth=0, zorder=2)
        for edge in (lo, hi):
            ax.plot(KS, edge, color=GRAY, linewidth=0.8, linestyle=ls, zorder=3)
        plotted[name] = {"min": [round(x, 2) for x in lo], "max": [round(x, 2) for x in hi]}
    # Proposed rule: one line per checkpoint / realization.
    for pools, color, marker, name in ((RND, ORANGE, "D", "random, 5 realizations"),
                                       (GNN, BLUE, "o", "GNN, 3 checkpoints")):
        for i, pool in enumerate(pools):
            ax.plot(KS, series(curves, pool, "code"), color=color, linewidth=1.1, marker=marker,
                    markersize=2.6, markeredgewidth=0, zorder=4, label=name if i == 0 else None)
        lo, hi = band(curves, pools, "code")
        plotted[f"IC shortlist + fallback, {name}"] = {"min": [round(x, 2) for x in lo],
                                                        "max": [round(x, 2) for x in hi]}
    for text, xy in labels:
        ax.text(*xy, text, fontsize=7, color="#333333", ha="left", va="center", zorder=5,
                bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none", "pad": 0.8})
    ax.axhline(0, color="#555555", linewidth=0.7, zorder=1)
    ax.set_xticks(KS)
    ax.set_xlim(0.8, 8.2)
    ax.set_ylim(*ylim)
    ax.set_xlabel("k = candidates measured in native bytes (of 8)")
    ax.set_title(title, fontsize=8, loc="left", pad=4)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=2.5, colors=INK)
    return plotted


def main() -> None:
    curves = json.loads(SRC.read_text())["curves"]
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(7.16, 2.45))
    plt.subplots_adjust(left=0.07, right=0.995, bottom=0.17, top=0.9, wspace=0.17)
    a = panel(ax0, curves["S347_all"], "(a) All 347 programs", (0, 5.9), [
        ("IC shortlist + -Oz fallback", (1.1, 4.75)),
        ("k arbitrary candidates + -Oz fallback", (2.15, 2.62)),
        ("IC shortlist, no fallback", (4.3, 1.75)),
    ])
    b = panel(ax1, curves["S347_without_npb"], "(b) 227 programs without NPB", (-2.4, 2.9), [
        ("IC shortlist + -Oz fallback", (1.1, 2.0)),
        ("k arbitrary candidates + -Oz fallback", (2.3, 0.75)),
        ("IC shortlist, no fallback", (3.4, -1.3)),
    ])
    ax0.legend(frameon=False, fontsize=7, loc="upper right", ncol=2, handlelength=1.6,
               columnspacing=1.2, borderaxespad=0.0)
    ax0.set_ylabel("Code-section saving vs -Oz (%)")
    OUT.mkdir(parents=True, exist_ok=True)
    pdf, png = OUT / f"{STEM}.pdf", OUT / f"{STEM}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    manifest = {
        "script": str(Path(__file__).relative_to(ROOT)),
        "command": "python3 scripts/verify_budgeted_selector.py && python3 scripts/generate_budget_figure.py",
        "inputs": {str(SRC.relative_to(ROOT)): digest(SRC)},
        "outputs": {str(p.relative_to(ROOT)): digest(p) for p in (pdf, png)},
        "plotted_min_max_gain_pct_k1_to_k8": {"panel_a_347": a, "panel_b_227_without_npb": b},
        "notes": "Bands are min-max over 3 GNN checkpoints / 5 random realizations (gray bands: all 8 pools). "
                 "Retrospective recomputation from frozen records; reference = attributed service -Oz.",
    }
    (OUT / f"{STEM}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest["plotted_min_max_gain_pct_k1_to_k8"]["panel_a_347"], indent=1))


if __name__ == "__main__":
    main()

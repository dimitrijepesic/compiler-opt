#!/usr/bin/env python3
"""Two-panel figure for paper/telfor_revised.tex (full text width, figure*).

Same frozen inputs and same two panels as generate_final_figures.py, laid out
for print: no suptitle or in-figure footnotes (the caption carries them), every
random realization drawn as its own point, TrueType fonts embedded. No value is
typed into the plotting code; the manifest records input and output hashes.

Run from the repository root:  python3 scripts/generate_telfor_revised_figure.py
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
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAUSAL = ROOT / "results/causal_baseline_audit/summary.json"
SELECTOR = ROOT / "results/selector_audit/summary.json"
OUT = ROOT / "paper/figures"
STEM = "evaluation_choices_revised"

BLUE, ORANGE = "#2c6eaa", "#d9772a"   # IC / code bytes in both panels
INK, MUTED, GRID = "#1a1a1a", "#555555", "#dddddd"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def style(ax) -> None:
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=2.5, colors=INK)


def main() -> None:
    causal = json.loads(CAUSAL.read_text())["campaign"]
    selector = json.loads(SELECTOR.read_text())["cohorts"]["ALL"]
    assert causal["programs"] == 120 and selector["n"] == 347

    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(7.16, 2.25), gridspec_kw={"width_ratios": [1.0, 1.35]})
    plt.subplots_adjust(left=0.075, right=0.995, bottom=0.17, top=0.89, wspace=0.24)

    # (a) P/U/A, each metric indexed to its own plain reference P = 100.
    states = ["P", "U", "A"]
    x = np.arange(3)
    width = 0.36
    plotted = {}
    for i, (metric, label, color) in enumerate(
            (("ic", "IR instructions (IC)", BLUE), ("text_sec", "code-section bytes", ORANGE))):
        sums = causal["totals"][metric]["sums"]
        vals = np.array([sums[s] for s in states], dtype=float)
        norm = vals / vals[0] * 100.0
        plotted[metric] = {s: round(float(v), 2) for s, v in zip(states, norm)}
        bars = ax0.bar(x + (i - 0.5) * (width + 0.03), norm, width, label=label, color=color)
        for bar, value in zip(bars, norm):
            ax0.text(bar.get_x() + bar.get_width() / 2, value + 1.5, f"{value:.1f}",
                     ha="center", va="bottom", fontsize=7, color=INK)
    ax0.set_xticks(x, ["P: plain", "U: plain,\nunrolling off", "A: size\nattributes"])
    ax0.set_ylim(0, 128)
    ax0.set_yticks([0, 25, 50, 75, 100])
    ax0.set_ylabel("Sum relative to P (%)")
    ax0.set_title("(a) Reference preparation: NPB, 120 modules", fontsize=8, loc="left", pad=4)
    ax0.legend(frameon=False, fontsize=7, loc="upper right", ncol=2,
               handlelength=1.0, columnspacing=1.0, borderaxespad=0.0)
    style(ax0)

    # (b) generator x selector; every checkpoint and realization is one point.
    gens = selector["generators"]
    groups = [
        ("GNN", [f"gnn{s}" for s in (42, 123, 456)], "o"),
        ("random", [f"rnd{s}" for s in range(42, 47)], "D"),
    ]
    selectors = [("ic_first", "select by IC", BLUE), ("code_first", "select by code bytes", ORANGE)]
    pos, ticks, ranges = 0.0, [], {}
    for sel, sel_label, color in selectors:
        for gen_label, keys, marker in groups:
            vals = [gens[k][sel]["text_sec"]["gain_pct"] for k in keys]
            lo, hi = min(vals), max(vals)
            ranges[f"{gen_label}/{sel}"] = [round(lo, 2), round(hi, 2)]
            # Min-max band behind the points; points are spread sideways in seed
            # order so that near-identical values stay individually visible.
            half = 0.2
            ax1.add_patch(plt.Rectangle((pos - half, lo), 2 * half, hi - lo, facecolor=color,
                                        alpha=0.22, edgecolor="none", zorder=2))
            offsets = np.linspace(-half + 0.06, half - 0.06, len(vals))
            ax1.scatter(pos + offsets, vals, s=20, marker=marker, facecolor=color,
                        edgecolor="white", linewidth=0.6, zorder=3)
            ax1.text(pos, lo - 0.2, f"{lo:.2f}–{hi:.2f}", ha="center",
                     va="top", fontsize=7, color=INK)
            ticks.append((pos, f"{gen_label}\n(n = {len(vals)})"))
            pos += 1.0
        pos += 0.35
    ax1.set_xticks([t[0] for t in ticks], [t[1] for t in ticks])
    ax1.set_xlim(-0.55, ticks[-1][0] + 0.55)
    ax1.set_ylim(0, 4.6)
    ax1.set_yticks([0, 1, 2, 3, 4])
    ax1.set_ylabel("Code-section saving (%)")
    ax1.set_title("(b) Candidate selection: 347 programs, same 8 candidates", fontsize=8,
                  loc="left", pad=4)
    for (sel, sel_label, color), centre in zip(selectors, (0.5, 2.85)):
        ax1.text(centre, 4.45, sel_label, ha="center", va="top", fontsize=7.5, color=INK,
                 bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": color,
                       "linewidth": 1.0})
    style(ax1)

    OUT.mkdir(parents=True, exist_ok=True)
    pdf, png = OUT / f"{STEM}.pdf", OUT / f"{STEM}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    manifest = {
        "script": str(Path(__file__).relative_to(ROOT)),
        "command": "python3 scripts/generate_telfor_revised_figure.py",
        "inputs": {str(p.relative_to(ROOT)): digest(p) for p in (CAUSAL, SELECTOR)},
        "outputs": {str(p.relative_to(ROOT)): digest(p) for p in (pdf, png)},
        "plotted": {"panel_a_percent_of_P": plotted, "panel_b_min_max_gain_pct": ranges},
        "notes": "Panel (b) ranges are min-max over separate checkpoints/realizations, "
                 "not confidence intervals. Gains are ratio-of-sums vs the attributed service -Oz.",
    }
    (OUT / f"{STEM}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

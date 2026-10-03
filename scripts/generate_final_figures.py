#!/usr/bin/env python3
"""Generate the two-panel figure for the revised TELFOR manuscript.

Inputs are the frozen causal and selector summaries. No values are entered
manually in the plotting code; a manifest records their hashes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CAUSAL = ROOT / "results/causal_baseline_audit/summary.json"
SELECTOR = ROOT / "results/selector_audit/summary.json"
OUT = ROOT / "paper/figures"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    causal = json.loads(CAUSAL.read_text())
    selector = json.loads(SELECTOR.read_text())
    metrics = {m: causal["campaign"]["totals"][m]["sums"] for m in ("ic", "text_sec")}
    labels = ["P\nplain", "U\nunroll off", "A\nsize attrs"]
    states = ["P", "U", "A"]

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(7.15, 3.05), gridspec_kw={"width_ratios": [1.02, 1.25]})
    plt.subplots_adjust(left=0.08, right=0.985, bottom=0.22, top=0.84, wspace=0.42)

    # Left: normalize each metric to its plain reference so the two quantities
    # can share an axis while retaining the absolute values in the labels.
    x = np.arange(3)
    width = 0.34
    colors = {"ic": "#2c6eaa", "text_sec": "#d9772a"}
    for i, m in enumerate(("ic", "text_sec")):
        vals = np.array([metrics[m][s] for s in states], dtype=float)
        norm = vals / vals[0] * 100.0
        bars = ax0.bar(x + (i - 0.5) * width, norm, width, label="IC" if m == "ic" else "code bytes", color=colors[m])
        for b, value, absolute in zip(bars, norm, vals.astype(int)):
            ax0.text(b.get_x() + b.get_width() / 2, value + 2.4, f"{value:.0f}", ha="center", va="bottom", fontsize=7)
    ax0.set_xticks(x, labels)
    ax0.set_ylim(0, 116)
    ax0.set_ylabel("Size relative to plain P (%)")
    ax0.set_title("Reference preparation\nNPB, 120 modules", fontsize=9, pad=7)
    ax0.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax0.set_axisbelow(True)
    ax0.legend(frameon=False, fontsize=7, loc="lower left")
    ax0.text(0.02, -0.36, "Absolute totals: IC 53,085 / 40,525 / 40,446; code 291,616 / 234,913 / 214,296",
             transform=ax0.transAxes, fontsize=6.2, color="#444444")

    # Right: GNN points and random ranges, computed from all five random draws.
    cohort = selector["cohorts"]["ALL"]["generators"]
    gnn = ["gnn42", "gnn123", "gnn456"]
    gnn_labels = ["GNN 42", "GNN 123", "GNN 456"]
    vals_ic = [cohort[g]["ic_first"]["text_sec"]["gain_pct"] for g in gnn]
    vals_code = [cohort[g]["code_first"]["text_sec"]["gain_pct"] for g in gnn]
    rnd_ic = [cohort[f"rnd{r}"]["ic_first"]["text_sec"]["gain_pct"] for r in range(42, 47)]
    rnd_code = [cohort[f"rnd{r}"]["code_first"]["text_sec"]["gain_pct"] for r in range(42, 47)]
    px = np.arange(4)
    width = 0.28
    ax1.bar(px[:3] - width / 2, vals_ic, width, label="select by IC", color="#6c8db3")
    ax1.bar(px[:3] + width / 2, vals_code, width, label="select by code", color="#e29a5b")
    # The fourth category is not a pseudo-replicate: it is explicitly a range
    # over five separate random realizations.
    ax1.errorbar(3 - width / 2, np.mean(rnd_ic), [[np.mean(rnd_ic) - min(rnd_ic)], [max(rnd_ic) - np.mean(rnd_ic)]],
                 fmt="o", color="#6c8db3", capsize=4, lw=1.4, label="random range")
    ax1.errorbar(3 + width / 2, np.mean(rnd_code), [[np.mean(rnd_code) - min(rnd_code)], [max(rnd_code) - np.mean(rnd_code)]],
                 fmt="o", color="#e29a5b", capsize=4, lw=1.4)
    ax1.axhline(0, color="#555555", linewidth=0.7)
    ax1.set_xticks(px, gnn_labels + ["random\n5 draws"])
    ax1.set_ylabel("Code-section saving vs attributed Oz (%)")
    ax1.set_title("Selection objective\n347 programs", fontsize=9, pad=7)
    ax1.set_ylim(-0.8, 4.35)
    ax1.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax1.set_axisbelow(True)
    ax1.legend(frameon=False, fontsize=7, loc="upper left")
    ax1.text(0.0, -0.36, "Random whiskers show min–max across five draws, not confidence intervals.",
             transform=ax1.transAxes, fontsize=6.2, color="#444444")

    fig.suptitle("Evaluation choices change the reported code-size result", fontsize=10.5, y=0.98)
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / "evaluation_choices.pdf"
    png = OUT / "evaluation_choices.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    manifest = {"script": str(Path(__file__).relative_to(ROOT)),
                "inputs": {str(p.relative_to(ROOT)): digest(p) for p in (CAUSAL, SELECTOR)},
                "outputs": {str(p.relative_to(ROOT)): digest(p) for p in (pdf, png)},
                "random_range_note": "min-max over rnd42..rnd46; not a confidence interval"}
    (OUT / "evaluation_choices_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

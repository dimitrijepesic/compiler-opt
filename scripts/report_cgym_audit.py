#!/usr/bin/env python3
"""Generate a checked table and scientific figure from a complete service audit."""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    args = p.parse_args()
    root = args.directory
    manifest = json.loads((root / "manifest.json").read_text())
    report = json.loads((root / "summary.json").read_text())
    records = [json.loads(f.read_text()) for f in sorted((root / "records").glob("*.json"))]
    assert len(records) == len(manifest["sources"]) == report["summary"]["complete_paired"]
    assert {r["uri"] for r in records} == set(manifest["sources"])
    assert all(r["fingerprint"] == manifest["fingerprint"] for r in records)
    assert report["fingerprint"] == manifest["fingerprint"]
    assert not report["summary"]["excluded"] and not report["summary"]["candidate_failures"]
    # Independent recomputation of all headline sums from individual records.
    for suite, summary in report["suites"].items():
        rows = [r for r in records if r["suite"] == suite]
        assert len(rows) == summary["complete_paired"]
        for r in rows:
            assert r["plain"]["o0_ic"] == r["attr"]["o0_ic"] == r["paper_reference"]["o0"]
            assert r["plain"]["oz"]["ic"] == r["paper_reference"]["oz"]
            if "portfolio_ics" in r["paper_reference"]:
                assert [e["ic"] for e in r["plain"]["portfolio"]] == r["paper_reference"]["portfolio_ics"]
        for variant in ("plain", "attr"):
            for method in ("portfolio", "random"):
                for metric in ("ic", "text", "text_sec"):
                    baseline = sum(r[variant]["oz"][metric] for r in rows)
                    chosen = [min(enumerate(r[variant][method]), key=lambda x: (x[1]["ic"], x[0]))[1]
                              for r in rows]
                    candidate = sum(c[metric] for c in chosen)
                    saved = summary[variant][method][metric]
                    assert baseline == saved["baseline_sum"] and candidate == saved["candidate_sum"]
                    assert abs(saved["gain_pct"] - 100 * (1 - candidate / baseline)) < 1e-10

    order = [s for s in ("npb-v0", "mibench-v1", "blas-v0") if s in report["suites"]]
    names = {"npb-v0": "NPB", "mibench-v1": "MiBench", "blas-v0": "BLAS"}
    lines = ["# Verified CompilerGym audit results", "",
             f"Complete paired matrix: **{len(records)} programs**, eight fixed portfolio sequences and "
             "eight paired random sequences per program, with and without function size attributes. "
             "No failed programs or candidates. All original O0/Oz counts and available portfolio "
             "candidate ICs reproduced exactly.", "",
             "Positive gains mean smaller than that condition's service -Oz reference. "
             "The candidate is selected by final IC in every column; byte selection is not substituted. "
             "Each percentage is a reduction in summed costs, not the mean per-program reduction.", "",
             "| Suite | Method | IC gain, original | IC gain, attributes | Code bytes gain, original | Code bytes gain, attributes |",
             "|---|---|---:|---:|---:|---:|"]
    for suite in order:
        s = report["suites"][suite]
        for method in ("portfolio", "random"):
            vals = [s[v][method][metric]["gain_pct"] for metric in ("ic", "text_sec") for v in ("plain", "attr")]
            lines.append(f'| {names[suite]} ({s["complete_paired"]}) | {method}-8 | ' +
                         " | ".join(f"{v:+.2f}%" for v in vals) + " |")
    lines += ["", "## Baseline changes and command-line diagnostics", "",
              "| Suite | Service -Oz IC, original → attributes | Code bytes, original → attributes | Modules where CLI Oz IC differs from service, original / attributes |",
              "|---|---:|---:|---:|"]
    for suite in order:
        rows = [r for r in records if r["suite"] == suite]
        counts = [sum(r[v]["cli_oz_diagnostic"]["ic"] != r[v]["oz"]["ic"] for r in rows) for v in ("plain", "attr")]
        pairs = [" → ".join(f'{sum(r[v]["oz"][metric] for r in rows):,}' for v in ("plain", "attr"))
                 for metric in ("ic", "text_sec")]
        lines.append(f'| {names[suite]} | {pairs[0]} | {pairs[1]} | {counts[0]} / {counts[1]} |')
    lines += ["", "## Portfolio outcomes after adding attributes", "",
              "| Suite | IC wins / ties / losses | Code-byte wins / ties / losses |",
              "|---|---:|---:|"]
    for suite in order:
        s = report["suites"][suite]["attr"]["portfolio"]
        cells = [" / ".join(str(s[m][key]) for key in ("wins", "ties", "losses")) for m in ("ic", "text_sec")]
        lines.append(f'| {names[suite]} | {cells[0]} | {cells[1]} |')
    lines += ["", "![Paired baseline audit](audit_gain.png)", "",
              "## Scope", "",
              "This establishes the effect of size attributes in the original CompilerGym service "
              "protocol for these three suites. It does not establish equivalence to a full clang -Oz "
              "build, runtime improvement, semantic validation, a learned-policy result under the "
              "new protocol, or effects on unexamined papers. Random-8 uses one newly drawn seed; "
              "its old-protocol numbers need not match the paper's random samples. Related modules "
              "within a suite are not independent projects. See README.md for the full protocol.", "",
              f'Protocol fingerprint: `{manifest["fingerprint"]}`.', ""]
    (root / "RESULTS.md").write_text("\n".join(lines))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "savefig.dpi": 180})
    fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True)
    x = np.arange(len(order))
    for row, method in enumerate(("portfolio", "random")):
        for col, metric in enumerate(("ic", "text_sec")):
            ax = axes[row, col]
            for v, offset, color, label in (("plain", -.18, "#64748b", "Original input"),
                                            ("attr", .18, "#007f82", "+ minsize / optsize")):
                values = [report["suites"][s][v][method][metric]["gain_pct"] for s in order]
                bars = ax.bar(x + offset, values, .34, color=color, label=label)
                ax.bar_label(bars, labels=[f"{v:.1f}" for v in values], fontsize=9, padding=3)
            ax.axhline(0, color="#334155", linewidth=.7)
            ax.set_xticks(x, [f'{names[s]}\n(n={report["suites"][s]["complete_paired"]})' for s in order])
            ax.set_title(f'{method.capitalize()}-8 · {"IR instructions" if metric == "ic" else "code-section bytes"}')
            ax.set_ylabel("Reduction vs service -Oz (%)")
            ax.margins(y=.25)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    fig.text(.5, .01, "Same 8 candidates per condition; selection by IC; positive = smaller than baseline", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, .93))
    for ext in ("png", "pdf", "svg"):
        fig.savefig(root / f"audit_gain.{ext}")
    plt.close(fig)
    print(f"Verified {len(records)} records; wrote RESULTS.md and audit_gain PNG/PDF/SVG")


if __name__ == "__main__":
    main()

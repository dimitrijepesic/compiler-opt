#!/usr/bin/env python3
"""Post-hoc selection and concentration analysis of the frozen service audit.

No compilers, trained policies, candidate generation or sequence tuning are
invoked. Requires the complete 210-program audit. All byte selection uses
pure code-section bytes, with first-candidate ties unless stated otherwise.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
SUITES = ("npb-v0", "mibench-v1", "blas-v0")
LABELS = {"npb-v0": "NPB", "mibench-v1": "MiBench", "blas-v0": "BLAS",
          "all": "All three suites", "without_npb": "MiBench + BLAS"}
SELECTORS = ("ic_first", "ic_then_bytes", "bytes", "bytes_with_oz")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def choose(row, variant, method, selector, k=8):
    entries = row[variant][method][:k]
    assert len(entries) == k and all(e["ok"] for e in entries)
    if selector == "ic_first":
        key = lambda pair: (pair[1]["ic"], pair[0])
    elif selector == "ic_then_bytes":
        key = lambda pair: (pair[1]["ic"], pair[1]["text_sec"], pair[0])
    else:
        key = lambda pair: (pair[1]["text_sec"], pair[0])
    index, selected = min(enumerate(entries), key=key)
    baseline = row[variant]["oz"]
    if selector == "bytes_with_oz" and baseline["text_sec"] <= selected["text_sec"]:
        return {**baseline, "index": "oz"}
    return {**selected, "index": index}


def aggregate(rows, variant, method, selector, k=8):
    choices = [choose(r, variant, method, selector, k) for r in rows]
    out = {"programs": len(rows), "k_search": k,
           "baseline_returned": sum(c["index"] == "oz" for c in choices)}
    for metric in ("ic", "text", "text_sec"):
        bases = [r[variant]["oz"][metric] for r in rows]
        vals = [c[metric] for c in choices]
        b, c = sum(bases), sum(vals)
        out[metric] = {"baseline_sum": b, "selected_sum": c,
                       "saved": b-c, "gain_pct": 100*(1-c/b),
                       "wins": sum(x < y for x, y in zip(vals, bases)),
                       "ties": sum(x == y for x, y in zip(vals, bases)),
                       "losses": sum(x > y for x, y in zip(vals, bases)),
                       "median_program_gain_pct": median(100*(1-x/y) for x, y in zip(vals, bases))}
    return out


def sign(candidate, baseline):
    return "win" if candidate < baseline else "loss" if candidate > baseline else "tie"


def details(rows, variant, method):
    points = []
    for row in rows:
        b = row[variant]["oz"]
        choices = {s: choose(row, variant, method, s) for s in SELECTORS}
        ic, tie, byte = [choices[s] for s in ("ic_first", "ic_then_bytes", "bytes")]
        assert byte["text_sec"] <= tie["text_sec"] <= ic["text_sec"]
        assert tie["ic"] == ic["ic"]
        assert choices["bytes_with_oz"]["text_sec"] <= min(byte["text_sec"], b["text_sec"])
        points.append({"uri": row["uri"], "suite": row["suite"],
                       "baseline_code_bytes": b["text_sec"],
                       "ic_choice_code_bytes": ic["text_sec"],
                       "ic_choice_saved_bytes": b["text_sec"]-ic["text_sec"],
                       "byte_choice_saved_bytes": b["text_sec"]-byte["text_sec"],
                       "ic_gain_pct": 100*(1-ic["ic"]/b["ic"]),
                       "code_gain_pct": 100*(1-ic["text_sec"]/b["text_sec"]),
                       "ic_outcome": sign(ic["ic"], b["ic"]),
                       "code_outcome": sign(ic["text_sec"], b["text_sec"]),
                       "selector_regret_bytes": ic["text_sec"]-byte["text_sec"],
                       "regret_resolved_by_ic_ties": ic["text_sec"]-tie["text_sec"],
                       "indices": {s: c["index"] for s, c in choices.items()}})
    return points


def concentration(rows, points, variant, method):
    ranked = sorted(points, key=lambda p: (-p["ic_choice_saved_bytes"], p["uri"]))
    net = sum(p["ic_choice_saved_bytes"] for p in points)
    gross = sum(max(p["ic_choice_saved_bytes"], 0) for p in points)
    top = ranked[:5]
    top_sum = sum(p["ic_choice_saved_bytes"] for p in top)
    omit = {p["uri"] for p in top}
    retained = [r for r in rows if r["uri"] not in omit]
    return {"net_saved_bytes": net, "gross_saved_bytes": gross,
            "gross_regression_bytes": gross-net,
            "top5_positive_bytes": top_sum,
            "top5_share_of_net_pct": 100*top_sum/net if net else None,
            "top5_share_of_gross_pct": 100*top_sum/gross if gross else None,
            "top5_uris": [p["uri"] for p in top],
            "after_omitting_top5_ic_savers": {
                s: aggregate(retained, variant, method, s)["text_sec"] for s in ("ic_first", "bytes")}}


def analyze(rows):
    groups = {s: [r for r in rows if r["suite"] == s] for s in SUITES}
    groups["all"] = rows
    groups["without_npb"] = [r for r in rows if r["suite"] != "npb-v0"]
    result = {}
    for name, group in groups.items():
        result[name] = {}
        for variant in ("plain", "attr"):
            result[name][variant] = {}
            for method in ("portfolio", "random"):
                points = details(group, variant, method)
                d = {"selectors": {s: aggregate(group, variant, method, s) for s in SELECTORS},
                     "byte_budget_curve": {str(k): aggregate(group, variant, method, "bytes_with_oz", k)
                                           for k in range(1, 9)},
                     "programs_helped_by_byte_selection": sum(p["selector_regret_bytes"] > 0 for p in points),
                     "programs_helped_by_ic_tie_break": sum(p["regret_resolved_by_ic_ties"] > 0 for p in points),
                     "selection_regret_bytes": sum(p["selector_regret_bytes"] for p in points),
                     "regret_resolved_by_ic_ties": sum(p["regret_resolved_by_ic_ties"] for p in points),
                     "ic_vs_code_outcomes": {f"{a}/{b}": sum(p["ic_outcome"] == a and p["code_outcome"] == b for p in points)
                                             for a in ("win", "tie", "loss") for b in ("win", "tie", "loss")},
                     "concentration": concentration(group, points, variant, method)}
                curve = [d["byte_budget_curve"][str(k)]["text_sec"]["selected_sum"] for k in range(1, 9)]
                assert all(b <= a for a, b in zip(curve, curve[1:]))
                result[name][variant][method] = d
    return result


def write_report(out, result):
    g = result["groups"]
    lines = ["# Selection objective and concentration audit", "",
             "Analysis of the frozen 210-program CompilerGym service matrix. All headline rows below "
             "use size attributes on both baseline and candidates, the original target per module, "
             "and the same eight recorded candidate sequences. No new search, fitting or compilation was performed.", "",
             "Positive percentages mean reductions in summed pure code-section bytes. These are "
             "post-hoc, exact finite-cohort comparisons, not estimates of new-project performance.", "",
             "## What changing the selector buys", "",
             "| Cohort | Method | Choose by IC | IC, byte tie-break | Choose by bytes | Bytes + Oz fallback |",
             "|---|---|---:|---:|---:|---:|"]
    for group in (*SUITES, "all", "without_npb"):
        for method in ("portfolio", "random"):
            d = g[group]["attr"][method]
            vals = [d["selectors"][s]["text_sec"]["gain_pct"] for s in SELECTORS]
            n = d["selectors"]["ic_first"]["programs"]
            lines.append(f"| {LABELS[group]} ({n}) | {method}-8 | " + " | ".join(f"{v:+.2f}%" for v in vals) + " |")
    lines += ["", "The original IC rule resolves ties by sequence order. The intermediate selector changes "
              "only ties at minimum IC. Direct byte selection chooses the smallest measured code section "
              "among all eight candidates; it is optimal only within that recorded candidate pool.", "",
              "Oz fallback chooses the baseline on byte ties as well as regressions. Its no-regression "
              "property is guaranteed by the selection rule for this measured size metric; it is not "
              "an empirical discovery or a runtime/correctness guarantee.", "",
              "## Cost accounting", "",
              "| Selector | Optimized IR candidates | Candidate code-generation measurements | Baseline for comparison/fallback |",
              "|---|---:|---:|---|",
              "| IC | 8 | 1, after selection | 1 additional baseline optimization and object measurement |",
              "| IC, byte tie-break | 8 | Number of tied minimum-IC candidates | Same baseline |",
              "| Bytes | 8 | 8 | Same baseline |",
              "| Bytes + Oz fallback | 8 | 8 | Baseline may also be returned |", "",
              "A deployment that tries eight sequences and Oz considers nine candidates. Equal numbers "
              "of IR sequences do not imply equal wall time: direct byte selection adds code generation. "
              "The existing audit timed whole program jobs under emulation; it cannot establish selector latency.", "",
              "## Where IC and code disagree", "",
              "The selected candidate is the original IC-minimum in both columns of each outcome pair.", "",
              "| Cohort | Method | IC improves, code grows | IC grows, code improves | Byte selection helps | Tie-breaking alone helps |",
              "|---|---|---:|---:|---:|---:|"]
    for group in (*SUITES, "all"):
        for method in ("portfolio", "random"):
            d = g[group]["attr"][method]; q = d["ic_vs_code_outcomes"]
            lines.append(f"| {LABELS[group]} | {method} | {q['win/loss']} | {q['loss/win']} | "
                         f"{d['programs_helped_by_byte_selection']} | {d['programs_helped_by_ic_tie_break']} |")
    lines += ["", "## Concentration and sensitivity", "",
              "Top five means the five largest positive savings under the IC selector, selected after "
              "observing outcomes. Both retained-cohort columns remove those same five modules. "
              "This is a stress test, not an unbiased robustness estimate. Shares of net savings "
              "may exceed 100% because regressions elsewhere cancel positive savings.", "",
              "| Cohort | Method | Top five / net savings | Gain after omitting top five: IC selection | Same subset: byte selection |",
              "|---|---|---:|---:|---:|"]
    for group in (*SUITES, "all", "without_npb"):
        for method in ("portfolio", "random"):
            c = g[group]["attr"][method]["concentration"]
            retained = c["after_omitting_top5_ic_savers"]
            lines.append(f"| {LABELS[group]} | {method} | {c['top5_share_of_net_pct']:.1f}% | "
                         f"{retained['ic_first']['gain_pct']:+.2f}% | {retained['bytes']['gain_pct']:+.2f}% |")
    lines += ["", "## Fixed prefix budgets", "",
              "The portfolio order was fixed on training data before this audit. Random prefixes use "
              "the already recorded draw order. No budget, ordering or sequence is selected using these results. "
              "Each cell uses byte selection and includes Oz as an additional candidate.", "",
              "| Cohort | Method | 1 sequence + Oz | 3 + Oz | 8 + Oz |",
              "|---|---|---:|---:|---:|"]
    for group in (*SUITES, "all", "without_npb"):
        for method in ("portfolio", "random"):
            d = g[group]["attr"][method]["byte_budget_curve"]
            lines.append(f"| {LABELS[group]} | {method} | " + " | ".join(f"{d[str(k)]['text_sec']['gain_pct']:+.2f}%" for k in (1, 3, 8)) + " |")
    lines += ["", "![Selection and disagreement](selection.png)", "",
              "## Limits", "",
              "This is a diagnostic of a fixed candidate pool. Measuring the target cost and choosing "
              "its minimum is not proposed as a novel algorithm. One random draw set is insufficient "
              "to rank random search and the portfolio as general methods. There is no new test set, "
              "runtime measurement, semantic validation, retraining or GNN evaluation here. "
              "NPB modules are correlated; 120 modules do not represent 120 independent applications. "
              "All results concern relocatable code sections, not full firmware footprints or linked executables.", "",
              f"Input protocol fingerprint: `{result['input_fingerprint']}`.", "",
              "Reproduce: `python3 scripts/analyze_cgym_selection.py` (matplotlib required for the figure).", ""]
    (out / "REPORT.md").write_text("\n".join(lines))


def plot(out, rows, result):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "pdf.fonttype": 42})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
    colors = {"npb-v0": "#007f82", "mibench-v1": "#c77d27", "blas-v0": "#6c62a8"}
    pts = details(rows, "attr", "portfolio")
    for suite in SUITES:
        sub = [p for p in pts if p["suite"] == suite]
        axes[0].scatter([p["ic_gain_pct"] for p in sub], [p["code_gain_pct"] for p in sub],
                        s=20, alpha=.65, color=colors[suite], label=LABELS[suite])
    axes[0].axhline(0, color="#64748b", lw=.7)
    axes[0].axvline(0, color="#64748b", lw=.7)
    axes[0].set(xlabel="IR instruction reduction vs -Oz (%)", ylabel="Code-byte reduction vs -Oz (%)",
                title="Same IC-selected portfolio candidate")
    axes[0].legend(frameon=False, fontsize=9)
    for group, color in (("all", "#007f82"), ("without_npb", "#c77d27")):
        for method, style in (("portfolio", "-"), ("random", "--")):
            curve = result["groups"][group]["attr"][method]["byte_budget_curve"]
            axes[1].plot(range(2, 10), [curve[str(k)]["text_sec"]["gain_pct"] for k in range(1, 9)],
                         style, marker="o", markersize=3, color=color,
                         label=f'{LABELS[group]} · {method}')
    axes[1].set(xlabel="Candidates measured (search sequences + Oz)", ylabel="Reduction in summed code bytes (%)",
                title="Choose by measured bytes, with Oz fallback", xticks=(2, 4, 6, 9), ylim=(0, None))
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Size attributes on both sides; fixed candidates; LLVM 10 service protocol", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, .94))
    for ext in ("png", "pdf", "svg"):
        fig.savefig(out / f"selection.{ext}", dpi=180)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=ROOT / "results/baseline_audit/llvm10_canonical")
    p.add_argument("--out", type=Path, default=ROOT / "results/baseline_selection_audit")
    args = p.parse_args()
    manifest = json.loads((args.input / "manifest.json").read_text())
    prior = json.loads((args.input / "summary.json").read_text())
    paths = sorted((args.input / "records").glob("*.json"))
    rows = sorted([json.loads(f.read_text()) for f in paths], key=lambda r: r["uri"])
    assert len(rows) == 210 == prior["summary"]["complete_paired"]
    assert {r["uri"] for r in rows} == set(manifest["sources"])
    assert all(r["fingerprint"] == manifest["fingerprint"] and "failed" not in r for r in rows)
    for row in rows:
        for variant in ("plain", "attr"):
            for method in ("portfolio", "random"):
                assert len(row[variant][method]) == 8 and all(e["ok"] for e in row[variant][method])
                for selector, saved in (("ic_first", "by_ic"), ("bytes", "by_text_sec")):
                    c = choose(row, variant, method, selector)
                    assert c["index"] == row[variant][method + "_best"][saved]["index"]
    groups = analyze(rows)
    for suite in SUITES:
        for variant in ("plain", "attr"):
            for method in ("portfolio", "random"):
                for metric in ("ic", "text", "text_sec"):
                    recomputed = groups[suite][variant][method]["selectors"]["ic_first"][metric]
                    assert recomputed["selected_sum"] == prior["suites"][suite][variant][method][metric]["candidate_sum"]
    result = {"timestamp": datetime.now(timezone.utc).isoformat(), "script_sha256": sha(__file__),
              "input_fingerprint": manifest["fingerprint"],
              "input_record_hashes": {f.name: sha(f) for f in paths},
              "groups": groups,
              "attribute_condition_program_details": {m: details(rows, "attr", m) for m in ("portfolio", "random")},
              "validation": {"records": len(rows), "prior_selection_indices_match": True,
                             "prior_totals_match": True, "selection_ordering_and_budget_monotonicity": True}}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    write_report(args.out, result)
    plot(args.out, rows, result)
    print(f"Verified {len(rows)} records; wrote {args.out}/REPORT.md, analysis.json, selection PNG/PDF/SVG")


if __name__ == "__main__":
    main()

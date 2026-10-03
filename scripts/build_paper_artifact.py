#!/usr/bin/env python3
"""Derive the manuscript's numbers from per-program records, without LLVM."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
INPUTS = {}


def read(path):
    path = ROOT / path
    data = path.read_bytes()
    INPUTS[str(path.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
    return json.loads(data)


def records(directory):
    values = [read(p.relative_to(ROOT)) for p in sorted((ROOT / directory).glob("*.json"))
              if p.name != "run_manifest.json"]
    assert len(values) == len({v["uri"] for v in values})
    return values


def gain(reference, candidate):
    return 100 * (1 - candidate / reference)


def derive():
    values = {}

    def put(name, value, source, digits=None):
        values[name] = {"value": value, "display": f"{value:,.0f}" if digits is None
                        else f"{value:.{digits}f}", "source": source}

    baseline_path = "results/baseline_audit/llvm10_canonical/records"
    baseline = records(baseline_path)
    assert Counter(r["suite"] for r in baseline) == {
        "npb-v0": 120, "mibench-v1": 40, "blas-v0": 50}
    put("AuditCount", len(baseline), baseline_path)
    paired = []
    for suite, title, prefix in [("npb-v0", "NPB", "Npb"),
                                  ("mibench-v1", "MiBench", "Mibench"),
                                  ("blas-v0", "BLAS", "Blas")]:
        cohort = [r for r in baseline if r["suite"] == suite]
        put(prefix + "Count", len(cohort), baseline_path)
        for method, label in [("portfolio", "Portfolio"), ("random", "Random")]:
            row = {"suite": title, "n": len(cohort), "method": label, "gains": {}}
            for variant, vlabel in [("plain", "Plain"), ("attr", "Attr")]:
                for metric, mlabel in [("ic", "Ic"), ("text_sec", "Code")]:
                    assert all(len(r[variant][method]) == 8 and
                               all(c["ok"] for c in r[variant][method]) for r in cohort)
                    selected = [min(r[variant][method], key=lambda c: c["ic"]) for r in cohort]
                    b = sum(r[variant]["oz"][metric] for r in cohort)
                    c = sum(x[metric] for x in selected)
                    row["gains"][variant + "_" + metric] = gain(b, c)
                    if method == "portfolio":
                        put(prefix + vlabel + mlabel + "Gain", gain(b, c), baseline_path, 2)
                        if suite == "npb-v0" and variant == "attr":
                            outcomes = Counter("Wins" if x[metric] < r[variant]["oz"][metric]
                                               else "Ties" if x[metric] == r[variant]["oz"][metric]
                                               else "Losses" for x, r in zip(selected, cohort))
                            for outcome in ("Wins", "Ties", "Losses"):
                                put("Npb" + mlabel + outcome, outcomes[outcome], baseline_path)
            paired.append(row)

    causal_path = "results/causal_baseline_audit/campaign/records"
    causal = records(causal_path)
    assert len(causal) == 120 and all(r["complete"] and all(r["checks"].values()) for r in causal)
    assert {r["uri"] for r in causal} == {r["uri"] for r in baseline if r["suite"] == "npb-v0"}
    cells = {"Plain": "plain/service_original", "Unroll": "plain/service_marked", "Attr": "attr/service_original"}
    totals = {}
    for label, cell in cells.items():
        totals[label] = {}
        for metric, name in [("ic", "Ic"), ("text_sec", "Code"), ("text", "Berkeley")]:
            total = sum(r["cells"][cell][metric] for r in causal)
            put(label + name, total, causal_path)
            totals[label][metric] = total
    for label in ("Unroll", "Attr"):
        put(label + "IcDelta", totals["Plain"]["ic"] - totals[label]["ic"], causal_path)
    put("ResidualIc", totals["Unroll"]["ic"] - totals["Attr"]["ic"], causal_path)
    remarked = [r for r in causal if r["cells"]["plain/replica_service"]["unroll_remarks"]["total"]]
    put("UnrolledModules", len(remarked), causal_path)
    put("UnrolledLoops", sum(r["cells"]["plain/replica_service"]["unroll_remarks"]["total"] for r in remarked), causal_path)
    put("ResidualModules", sum(r["cells"]["plain/service_marked"]["ic"] != r["cells"]["attr/service_original"]["ic"] for r in causal), causal_path)
    put("SameIrModules", sum(r["cells"]["plain/service_marked"]["ir_nosize_sha256"] == r["cells"]["attr/service_original"]["ir_nosize_sha256"] for r in causal), causal_path)
    late = sum(r["codegen_control"]["plain_marked_oz_late_attr"]["text_sec"] for r in causal)
    put("LateCodeDelta", totals["Unroll"]["text_sec"] - late, causal_path)
    put("LateCodeResidual", late - totals["Attr"]["text_sec"], causal_path)
    put("PlainLateCodeDelta", totals["Plain"]["text_sec"] - sum(r["codegen_control"]["plain_oz_late_attr"]["text_sec"] for r in causal), causal_path)
    totals["UnrollLate"] = {"ic": totals["Unroll"]["ic"], "text_sec": late}

    example_path = "results/causal_baseline_audit/example_npb116_transfb_nc0/example.json"
    example = read(example_path)
    assert all(example["checks"].values())
    for label, cell in cells.items():
        put("Example" + label + "Ic", example["cells"][cell]["ic"], example_path)
        put("Example" + label + "Bytes", example["function_bytes"]["example"][cell.replace("/", "-")], example_path)

    source_path = "results/baseline_audit/llvm10_source_check/summary.json"
    source = read(source_path)["records"]
    assert len(source) == 12
    put("SourceCount", len(source), source_path)
    for label, method in [("Plain", "plain_service_oz"), ("Attr", "attr_service_oz"), ("Clang", "real_clang_oz")]:
        put("Source" + label + "Bytes", sum(r[method]["text_sec"] for r in source), source_path)
    put("SourceAttrOverClang", -gain(values["SourceClangBytes"]["value"], values["SourceAttrBytes"]["value"]), source_path, 2)
    gsm = next(r for r in source if r["uri"].endswith("/gsm"))
    put("GsmOverClang", -gain(gsm["real_clang_oz"]["text_sec"], gsm["attr_service_oz"]["text_sec"]), source_path, 2)

    selector_path = "results/selector_audit/records"
    selector = records(selector_path)
    assert len(selector) == 347
    put("SelectorCount", len(selector), selector_path)
    ranges = {}
    for group, seeds in [("gnn", (42, 123, 456)), ("random", (42, 43, 44, 45, 46))]:
        for metric, suffix, cohort in [("text_sec", "Code", selector),
                                       ("text", "BerkeleyWithout", [r for r in selector if r["suite"] != "npb-v0"])]:
            result = []
            for seed in seeds:
                cs = [r[group][str(seed)]["candidates"] for r in cohort]
                assert all(len(c) == 8 and all(x["ok"] for x in c) for c in cs)
                result.append(gain(sum(r["baseline"][metric] for r in cohort), sum(min(c, key=lambda x: x[metric])[metric] for c in cs)))
            name = "Gnn" if group == "gnn" else "Random"
            put(name + suffix + "Min", min(result), selector_path, 2)
            put(name + suffix + "Max", max(result), selector_path, 2)
            ranges[name + suffix] = result
    return {"values": values, "paired": paired, "reference_totals": totals,
            "selector_ranges": ranges, "inputs": dict(sorted(INPUTS.items()))}


def outputs(data):
    macros = "% Generated by scripts/build_paper_artifact.py; do not edit.\n"
    macros += "".join("\\newcommand{\\" + k + "}{" + v["display"] + "}\n" for k, v in data["values"].items())
    rows = []
    for row in data["paired"]:
        g = row["gains"]
        vals = [g[k] for k in ("plain_ic", "attr_ic", "plain_text_sec", "attr_text_sec")]
        rows.append(f"{row['suite']} ({row['n']}) & {row['method']} & " + " & ".join(f"{v:.2f}" for v in vals) + r" \\")
    return {PAPER / "generated/results.tex": macros,
            PAPER / "generated/paired_rows.tex": "\\newcommand{\\PairedRows}{%\n" + "\n".join(rows) + "\n}\n",
            PAPER / "generated/claims.json": json.dumps(data, indent=2) + "\n"}


def figure(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.05, 2.35), layout="constrained")
    colors = ["#345f8c", "#cf742f"]
    g = data["paired"][0]["gains"]
    for i, (variant, label) in enumerate((("plain", "Plain input (P)"), ("attr", "Size attributes (A)"))):
        bars = a.bar([x + (i - .5) * .32 for x in range(2)], [g[variant + "_ic"], g[variant + "_text_sec"]], .3, label=label, color=colors[i])
        a.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
    a.set(xticks=[0, 1], xticklabels=["IR instructions", "Code-section bytes"], ylim=(0, 34), ylabel="Saving over service -Oz (%)", title="(a) Portfolio-8, NPB")
    a.legend(loc="upper right", frameon=False, fontsize=8)
    t = data["reference_totals"]
    for metric, label, color, marker in [("ic", "IR instructions", colors[0], "o"), ("text_sec", "Code-section bytes", colors[1], "s")]:
        v = [100*t[k][metric]/t["Plain"][metric] for k in ("Plain", "Unroll", "UnrollLate", "Attr")]
        b.plot(range(4), v, label=label, color=color, marker=marker, linewidth=1.6, markersize=4)
    b.set(xticks=range(4), xticklabels=["P", "U", r"U$^+$", "A"], ylim=(68, 110), ylabel="Reference cost (P = 100)", title="(b) Reference interventions, NPB")
    b.legend(loc="upper right", frameon=False, fontsize=8)
    for ax in (a, b):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.18)
        ax.set_axisbelow(True)
    path = PAPER / "figures/baseline_audit.pdf"
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(path.with_suffix(".png"), dpi=220)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail if generated numbers differ; writes nothing")
    ap.add_argument("--figure", action="store_true")
    args = ap.parse_args()
    data = derive()
    for path, content in outputs(data).items():
        if args.check:
            assert path.read_text() == content, f"Stale generated artifact: {path.relative_to(ROOT)}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if args.figure:
        figure(data)
    print(f"{'Verified' if args.check else 'Generated'} {len(data['values'])} numerical macros from {len(INPUTS)} source files.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Report for the matched-budget byte-search pilot (contract v2).  Reads records only.

Primary quantity per start s:
    A_s = 100 * sum_p(control24_bytes - local24_bytes) / sum_p(Oz_bytes)     (positive: local arm better)
with delivered bytes after 24 attempts and the -Oz fallback.  Starts are never
pooled into a larger budget; the mean over starts is reported only because the
continuation criteria are defined on it.  Criteria are engineering screening
thresholds, not significance tests.  The hash of this file is part of the
frozen manifest, so the computation below was fixed before any result existed.

Usage (host or container):  python3 scripts/report_byte_local_search_v2.py [--out DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DEFAULT = ROOT / "results" / "byte_local_search_v2"
SUITES = ["npb-v0", "mibench-v1", "blas-v0", "chstone-v0", "csmith-v0", "poj104-v1"]
COMPONENTS = ["reset_s", "optimize_s", "export_s", "codegen_s", "metric_s", "hash_s", "total_s"]


def key(uri):
    return hashlib.sha256(uri.encode()).hexdigest()


def fingerprint_of(m):
    return hashlib.sha256(json.dumps({k: v for k, v in m.items() if k not in ("created", "fingerprint")},
                                     sort_keys=True).encode()).hexdigest()


def pct(num, den):
    return 100.0 * num / den if den else float("nan")


def advantage(recs, seed, rule="curve", n="24"):
    oz = sum(r["reference"]["text_sec"] for r in recs)
    diff = sum(r["runs"][seed]["control"][rule][n]["text_sec"] - r["runs"][seed]["local"][rule][n]["text_sec"] for r in recs)
    return pct(diff, oz), diff, oz


def arm_gain(recs, seed, arm, rule, n):
    oz = sum(r["reference"]["text_sec"] for r in recs)
    return pct(oz - sum(r["runs"][seed][arm][rule][n]["text_sec"] for r in recs), oz)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()
    manifest = json.loads((args.out / "manifest.json").read_text())
    assert manifest["fingerprint"] == fingerprint_of(manifest), "manifest edited after --prepare"
    assert manifest["sources"]["report_script_sha256"] == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), \
        "report script differs from the one frozen in the manifest"
    seeds = [str(s) for s in manifest["protocol"]["starts"]]
    recs, problems = [], []
    for prog in manifest["programs"]:
        path = args.out / "records" / f"{key(prog['uri'])}.json"
        if not path.exists():
            problems.append(f"{prog['uri']}: no record")
            continue
        r = json.loads(path.read_text())
        if r.get("fingerprint") != manifest["fingerprint"]:
            problems.append(f"{prog['uri']}: record of another manifest")
        elif "failed" in r:
            problems.append(f"{prog['uri']}: failed: {r['failed'][:200]}")
        elif r.get("blocked"):
            problems.append(f"{prog['uri']}: BLOCKED: {'; '.join(r['block_reasons'])}")
        elif not r.get("complete"):
            problems.append(f"{prog['uri']}: incomplete")
        else:
            recs.append(r)
    summary = {"manifest_fingerprint": manifest["fingerprint"], "programs_expected": len(manifest["programs"]),
               "programs_usable": len(recs), "problems": problems, "timing_label": manifest["protocol"]["timing_label"]}
    L = ["# Matched-budget byte-search pilot v2: report", "",
         f"Manifest `{manifest['fingerprint'][:16]}`; {len(recs)} of {len(manifest['programs'])} program records usable.",
         "Twelve previously examined development programs; three random starts reported separately; not a test set.", ""]
    if problems:
        L += ["## INTERPRETATION BLOCKED", "", *[f"- {p}" for p in problems], "",
              "The contract forbids interpreting the pilot while an input, reference or start mismatch, a failure or a missing record exists.", ""]
        summary["criteria"] = None
    if recs:
        non_npb = [r for r in recs if r["suite"] != "npb-v0"]
        # ---- primary quantity
        prim = {}
        for label, sub in [("all", recs), ("without_npb", non_npb)] + [(s, [r for r in recs if r["suite"] == s]) for s in SUITES]:
            prim[label] = {}
            for rule in ("curve", "curve_strict"):
                per = {s: advantage(sub, s, rule)[0] for s in seeds} if sub else {}
                prim[label][rule] = {"n": len(sub), "per_start": per, "mean_over_starts": statistics.mean(per.values()) if per else None,
                                     "bytes_diff_per_start": {s: advantage(sub, s, rule)[1] for s in seeds} if sub else {},
                                     "oz_bytes": advantage(sub, seeds[0], rule)[2] if sub else 0}
        summary["paired_advantage_pct_of_oz"] = prim
        L += ["## Primary quantity: 100 * sum(control24 - local24) / sum(Oz), positive = local arm better", "",
              "| cohort | n | " + " | ".join(f"start {s}" for s in seeds) + " | mean over starts | strict rule, mean |", "|---|---:|" + "---:|" * (len(seeds) + 2)]
        for label, v in prim.items():
            c, st = v["curve"], v["curve_strict"]
            if not c["n"]:
                L.append(f"| {label} | 0 | " + " | ".join("-" for _ in seeds) + " | - | - |")
                continue
            L.append(f"| {label} | {c['n']} | " + " | ".join(f"{c['per_start'][s]:+.3f} ({c['bytes_diff_per_start'][s]:+d} B)" for s in seeds)
                     + f" | {c['mean_over_starts']:+.3f} | {st['mean_over_starts']:+.3f} |")
        # ---- W/T/L and medians
        L += ["", "## Paired outcomes per start (local vs control at 24 attempts, delivered bytes)", "",
              "| start | local smaller / tie / control smaller | median paired difference (% of program Oz) | median local gain vs Oz | median control gain vs Oz |",
              "|---|---:|---:|---:|---:|"]
        wtl = {}
        for s in seeds:
            d = [r["runs"][s]["control"]["curve"]["24"]["text_sec"] - r["runs"][s]["local"]["curve"]["24"]["text_sec"] for r in recs]
            dp = [pct(x, r["reference"]["text_sec"]) for x, r in zip(d, recs)]
            g = {arm: [pct(r["reference"]["text_sec"] - r["runs"][s][arm]["curve"]["24"]["text_sec"], r["reference"]["text_sec"]) for r in recs]
                 for arm in ("local", "control")}
            wtl[s] = {"W": sum(x > 0 for x in d), "T": sum(x == 0 for x in d), "L": sum(x < 0 for x in d),
                      "median_paired_pct": statistics.median(dp), "median_local_gain_pct": statistics.median(g["local"]),
                      "median_control_gain_pct": statistics.median(g["control"])}
            w = wtl[s]
            L.append(f"| {s} | {w['W']} / {w['T']} / {w['L']} | {w['median_paired_pct']:+.3f} | {w['median_local_gain_pct']:.3f} | {w['median_control_gain_pct']:.3f} |")
        summary["paired_outcomes"] = wtl
        # ---- curves
        L += ["", "## Each arm vs the same attributed -Oz (ratio of sums, %, with fallback)", "",
              "| cohort | start | local 8 | local 16 | local 24 | control 8 | control 16 | control 24 |", "|---|---|" + "---:|" * 6]
        curves = {}
        for label, sub in (("all", recs), ("without_npb", non_npb)):
            curves[label] = {}
            for s in seeds:
                curves[label][s] = {arm: {n: arm_gain(sub, s, arm, "curve", n) for n in ("8", "16", "24")} for arm in ("local", "control")}
                c = curves[label][s]
                L.append(f"| {label} | {s} | " + " | ".join(f"{c[a][n]:.3f}" for a in ("local", "control") for n in ("8", "16", "24")) + " |")
        summary["arm_gain_vs_oz_pct"] = curves
        strict = {label: {s: {arm: arm_gain(sub, s, arm, "curve_strict", "24") for arm in ("local", "control")} for s in seeds}
                  for label, sub in (("all", recs), ("without_npb", non_npb))}
        summary["arm_gain_vs_oz_pct_strict_24"] = strict
        L += ["", "Strict two-metric fallback at 24 attempts (secondary; search objective unchanged):", "",
              "| cohort | start | local | control |", "|---|---|---:|---:|"]
        for label in strict:
            for s in seeds:
                L.append(f"| {label} | {s} | {strict[label][s]['local']:.3f} | {strict[label][s]['control']:.3f} |")
        # ---- every program and start
        L += ["", "## Every program and start (delivered code-section bytes; Oz = attributed service reference)", "",
              "| program | start | Oz | local 8/16/24 | control 8/16/24 | control24 - local24 | failed L/C | start hashes equal L/C |",
              "|---|---|---:|---|---|---:|---|---|"]
        for r in recs:
            for s in seeds:
                run = r["runs"][s]
                lc = "/".join(str(run["local"]["curve"][n]["text_sec"]) for n in ("8", "16", "24"))
                cc = "/".join(str(run["control"]["curve"][n]["text_sec"]) for n in ("8", "16", "24"))
                d = run["control"]["curve"]["24"]["text_sec"] - run["local"]["curve"]["24"]["text_sec"]
                L.append(f"| {r['uri'].split('//')[1]} | {s} | {r['reference']['text_sec']} | {lc} | {cc} | {d:+d} | "
                         f"{run['local']['failed']}/{run['control']['failed']} | "
                         f"{run['local']['start_verification']['hashes_match']}/{run['control']['start_verification']['hashes_match']} |")
        # ---- cost
        cost = {arm: {"accounting_attempts": 0, "executed": 0, "failed": 0, **{c: 0.0 for c in COMPONENTS}, "generation_s": 0.0, "wall_s": 0.0}
                for arm in ("local", "control")}
        for r in recs:
            for s in seeds:
                for arm in ("local", "control"):
                    a = r["runs"][s][arm]
                    cost[arm]["accounting_attempts"] += a["attempt_count"]
                    cost[arm]["executed"] += a["executed"]
                    cost[arm]["failed"] += a["failed"]
                    cost[arm]["wall_s"] += a["wall_s"]
                    for att in a["attempts"]:
                        for c in COMPONENTS:
                            cost[arm][c] += att.get("timing", {}).get(c, 0.0)
                        cost[arm]["generation_s"] += att.get("generation_s", 0.0)
                cost["control"]["generation_s"] += r["runs"][s].get("control_generation_s", 0.0)
        ref_cost = {c: sum(r["reference"]["timing"].get(c, 0.0) for r in recs) for c in ("optimize_s", "export_s", "codegen_s", "metric_s", "hash_s")}
        summary["cost"] = {"arms": cost, "reference_executions": len(recs), "reference_accounting": len(recs) * len(seeds) * 2,
                           "reference_timing_s": ref_cost, "input_and_reference_s": sum(r["input_and_reference_s"] for r in recs),
                           "program_wall_s": sum(r["seconds"] for r in recs)}
        L += ["", f"## Cost ({manifest['protocol']['timing_label']})", "",
              "| arm | accounting attempts | executed | failed | generation s | reset s | optimize s | export s | codegen s | metric s | hash s | attempt total s | arm wall s |",
              "|---|---:|---:|---:|" + "---:|" * 9]
        for arm, c in cost.items():
            L.append(f"| {arm} | {c['accounting_attempts']} | {c['executed']} | {c['failed']} | {c['generation_s']:.3f} | "
                     + " | ".join(f"{c[k]:.1f}" for k in COMPONENTS) + f" | {c['wall_s']:.1f} |")
        L += ["", f"Reference: {len(recs)} executions (one per program, shared by its six runs; accounting {len(recs) * len(seeds) * 2}); "
                  f"optimize {ref_cost['optimize_s']:.1f} s, codegen {ref_cost['codegen_s']:.1f} s, metrics {ref_cost['metric_s']:.1f} s. "
                  f"Input preparation and reference together {summary['cost']['input_and_reference_s']:.1f} s; all programs {summary['cost']['program_wall_s']:.1f} s wall."]
        # ---- verification and functional checks
        hv = [f"{r['uri']} start {s} {arm} attempts {[x['attempt'] for x in r['runs'][s][arm]['start_verification']['rows'] if not x['hashes_match']]}"
              for r in recs for s in seeds for arm in ("local", "control") if not r["runs"][s][arm]["start_verification"]["hashes_match"]]
        summary["start_hash_variations"] = hv
        L += ["", "## Replay of the frozen starts", "",
              f"Metrics (IC, Berkeley text, code bytes) of all {len(recs) * len(seeds) * 2 * 8} start replays equal the frozen records (otherwise the program would be blocked above).",
              "Hash-only differences: " + ("none." if not hv else ""), *[f"- {x}" for x in hv]]
        fun = {r["uri"]: r["functional"] for r in recs}
        summary["functional"] = {u: {k: v for k, v in f.items() if k in ("status", "reason", "reference_stdout_equals_source_build_stdout")} for u, f in fun.items()}
        L += ["", "## Functional checks of delivered objects", "", "| program | status | detail |", "|---|---|---|"]
        for u, f in fun.items():
            det = f.get("reason") or ", ".join(f"{k}: {'pass' if v['passes'] else 'FAIL'}" for k, v in f.get("delivered", {}).items())
            L.append(f"| {u.split('//')[1]} | {f['status']} | {det} |")
        # ---- criteria
        if not problems:
            a_all, a_non = prim["all"]["curve"], prim["without_npb"]["curve"]
            suites_pos = {s: prim[s]["curve"]["mean_over_starts"] for s in SUITES if s != "npb-v0" and prim[s]["curve"]["n"]}
            over = [f"{r['uri']} start {s} {arm} n={n}" for r in recs for s in seeds for arm in ("local", "control") for n in ("8", "16", "24")
                    if r["runs"][s][arm]["curve"][n]["text_sec"] > r["reference"]["text_sec"]]
            ffail = [u for u, f in fun.items() if f["status"] == "fail"]
            crit = {
                "C1": {"pass": a_all["mean_over_starts"] >= 0.5, "value": a_all["mean_over_starts"], "threshold": ">= 0.5"},
                "C2": {"pass": sum(v > 0 for v in a_all["per_start"].values()) >= 2, "value": a_all["per_start"], "threshold": "> 0 in at least 2 of 3 starts"},
                "C3": {"pass": bool(non_npb) and a_non["mean_over_starts"] > 0 and sum(v > 0 for v in suites_pos.values()) >= 2,
                       "value": {"without_npb_mean": a_non["mean_over_starts"], "suite_means": suites_pos}, "threshold": "> 0 and at least 2 non-NPB suites > 0"},
                "C4": {"pass": not over and not ffail, "value": {"delivered_above_oz": over, "functional_failures": ffail,
                                                                  "unchecked": [u for u, f in fun.items() if f["status"] == "unchecked"]},
                       "threshold": "no delivered object above Oz; all available functional checks pass"}}
            crit["continue"] = all(c["pass"] for c in crit.values())
            summary["criteria"] = crit
            L += ["", "## Continuation criteria (engineering screening thresholds, not significance tests)", ""]
            for k in ("C1", "C2", "C3", "C4"):
                L.append(f"- **{k}: {'PASS' if crit[k]['pass'] else 'FAIL'}** ({crit[k]['threshold']}): `{json.dumps(crit[k]['value'])}`")
            L += ["", f"**Verdict: {'all criteria pass' if crit['continue'] else 'at least one criterion fails; the contract says to stop this optimizer branch'}.**"]
    (args.out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (args.out / "REPORT.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

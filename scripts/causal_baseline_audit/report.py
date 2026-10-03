#!/usr/bin/env python3
"""Report of the causal baseline audit. Standard library only; run on the host:

  python3 scripts/causal_baseline_audit/report.py

Recomputes everything from the individual records (pilot and campaign),
re-validates every record with its own copy of the validity rules, and writes
results/causal_baseline_audit/summary.json and REPORT.md.
"""

import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/causal_baseline_audit"
METRICS = (("ic", "IC"), ("text_sec", "code bytes"), ("text", "Berkeley text"))
MAIN = (("P", "plain/service_original"), ("U", "plain/service_marked"),
        ("A", "attr/service_original"), ("AU", "attr/service_marked"))
REPLICA = ("replica_service", "replica_service_marked", "replica_disable_unroll", "replica_threshold0")
CONTROLS = ("plain_oz_late_attr", "plain_marked_oz_late_attr", "attr_oz_stripped")


def key(uri):
    return hashlib.sha256(uri.encode()).hexdigest()


def load(stage, uris, fingerprint):
    records, problems = {}, {}
    for uri in uris:
        path = OUT / stage / "records" / f"{key(uri)}.json"
        if not path.exists():
            problems[uri] = "missing record"
            continue
        r = json.loads(path.read_text())
        if r.get("fingerprint") != fingerprint or r.get("uri") != uri:
            problems[uri] = "fingerprint or URI mismatch"
        elif "failed" in r:
            problems[uri] = r["failed"]
        elif not r.get("complete") or not r.get("checks") or not all(r["checks"].values()):
            problems[uri] = "incomplete record or failed hard check"
        elif any(f"{v}/{c}" not in r["cells"] for v in ("plain", "attr") for c in ("service_original", "service_marked", *REPLICA)) \
                or any(c not in r.get("codegen_control", {}) for c in CONTROLS):
            problems[uri] = "cells missing"
        else:
            records[uri] = r
    return records, problems


def pct(a, b):
    return None if not b else 100.0 * a / b


def fmt(x, digits=2):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        return f"{x + 0.0:.{digits}f}".replace("-0." + "0" * digits, "0." + "0" * digits)
    return f"{x:,}"


def totals(records):
    out = {}
    for m, _ in METRICS:
        t = {name: sum(r["cells"][cell][m] for r in records.values()) for name, cell in MAIN}
        for c in CONTROLS:
            t[c] = sum(r["codegen_control"][c][m] for r in records.values())
        for rep in ("replica_disable_unroll", "replica_threshold0"):
            t["plain/" + rep] = sum(r["cells"]["plain/" + rep][m] for r in records.values())
            t["attr/" + rep] = sum(r["cells"]["attr/" + rep][m] for r in records.values())
        d = {"P-A": t["P"] - t["A"], "P-U": t["P"] - t["U"], "U-A": t["U"] - t["A"], "A-AU": t["A"] - t["AU"],
             "P-P_late_attr": t["P"] - t["plain_oz_late_attr"], "U-U_late_attr": t["U"] - t["plain_marked_oz_late_attr"],
             "A_stripped-A": t["attr_oz_stripped"] - t["A"], "P_late_attr-A": t["plain_oz_late_attr"] - t["A"]}
        out[m] = {"sums": t, "differences": d,
                  "P_to_A_pct_of_P": pct(d["P-A"], t["P"]), "P_to_U_pct_of_P": pct(d["P-U"], t["P"]),
                  "ratio_of_sums_(P-U)/(P-A)": (d["P-U"] / d["P-A"]) if d["P-A"] else None,
                  "ratio_of_sums_numerator_P-U": d["P-U"], "ratio_of_sums_denominator_P-A": d["P-A"]}
    return out


def per_program(records):
    rows = []
    for uri, r in sorted(records.items(), key=lambda kv: (kv[0].split("/")[2], int(kv[0].rsplit("/", 1)[1]))):
        row = {"uri": uri, "o0": r["environment"]["o0"], "marked_loops": r["inputs"]["plain_marked"]["marked_loops"],
               "unroll_remarks_plain": r["cells"]["plain/replica_service"]["unroll_remarks"]["total"],
               "unroll_remarks_attr": r["cells"]["attr/replica_service"]["unroll_remarks"]["total"]}
        for m, _ in METRICS:
            v = {name: r["cells"][cell][m] for name, cell in MAIN}
            for c in CONTROLS:
                v[c] = r["codegen_control"][c][m]
            num, den = v["P"] - v["U"], v["P"] - v["A"]
            v["share_numerator_P-U"], v["share_denominator_P-A"] = num, den
            v["share_(P-U)/(P-A)"] = (num / den) if den else None
            row[m] = v
        row["soft"] = r["soft"]
        rows.append(row)
    return rows


def share_distribution(rows, m):
    defined = [x[m]["share_(P-U)/(P-A)"] for x in rows if x[m]["share_denominator_P-A"] != 0]
    zero_den = [x for x in rows if x[m]["share_denominator_P-A"] == 0]
    out = {"programs": len(rows), "denominator_zero": len(zero_den),
           "denominator_zero_with_nonzero_numerator": sum(x[m]["share_numerator_P-U"] != 0 for x in zero_den),
           "defined": len(defined)}
    if defined:
        q = statistics.quantiles(defined, n=4) if len(defined) > 1 else [defined[0]] * 3
        out.update({"exactly_1": sum(s == 1 for s in defined), "below_0": sum(s < 0 for s in defined),
                    "above_1": sum(s > 1 for s in defined), "min": min(defined), "q1": q[0],
                    "median": statistics.median(defined), "q3": q[2], "max": max(defined),
                    "mean": statistics.fmean(defined)})
    return out


def soft_summary(records):
    names = sorted({k for r in records.values() for k in r["soft"]})
    return {n: {"true": sum(bool(r["soft"].get(n)) for r in records.values()),
                "false": sorted(u for u, r in records.items() if not r["soft"].get(n))} for n in names}


def remarks_summary(records):
    out = {}
    for v in ("plain", "attr"):
        by_name, by_msg, programs = {}, {}, 0
        for r in records.values():
            rem = r["cells"][f"{v}/replica_service"]["unroll_remarks"]
            programs += rem["total"] > 0
            for k, n in rem["by_name"].items():
                by_name[k] = by_name.get(k, 0) + n
            for k, n in rem["by_message"].items():
                by_msg[k] = by_msg.get(k, 0) + n
        out[v] = {"programs_with_unrolling": programs, "by_name": by_name,
                  "by_message": dict(sorted(by_msg.items(), key=lambda kv: -kv[1])),
                  "total": sum(by_name.values()),
                  "after_intervention_total": sum(r["cells"][f"{v}/{c}"]["unroll_remarks"]["total"] for r in records.values()
                                                  for c in ("replica_service_marked", "replica_disable_unroll"))}
    return out


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" if i == 0 else "---:" for i in range(len(headers))) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def main():
    inputs = json.loads((OUT / "inputs.json").read_text())
    summary = {"inputs_sha256": hashlib.sha256((OUT / "inputs.json").read_bytes()).hexdigest()}
    md = ["# Causal baseline audit: report", "",
          "Generated by `scripts/causal_baseline_audit/report.py` from the individual records. "
          "Protocol: `PROTOCOL.md`. P = plain input, original service `-Oz`; U = plain input with "
          "`llvm.loop.unroll.disable` on every loop, original service `-Oz`; A = attr input (`minsize optsize` on "
          "definitions), original service; AU = attr input with the same marking. All four are executed by the "
          "original CompilerGym 0.2.5 service. Sums are over the valid set; shares of sums and per-program shares "
          "are different measures; none of the shares is a unique additive decomposition.", ""]
    stages = {}
    for stage in ("pilot", "campaign"):
        manifest = OUT / stage / "manifest.json"
        if not manifest.exists():
            continue
        fp = json.loads(manifest.read_text())["fingerprint"]
        records, problems = load(stage, inputs[stage], fp)
        stages[stage] = (records, problems)
        rows = per_program(records)
        s = summary[stage] = {"fingerprint": fp, "programs": len(inputs[stage]), "valid": len(records),
                              "not_valid": problems, "per_program": rows, "soft_checks": soft_summary(records),
                              "unroll_remarks": remarks_summary(records)}
        if stage == "campaign":
            s["totals"] = totals(records)
            s["share_distribution"] = {m: share_distribution(rows, m) for m, _ in METRICS}
            s["identity_counts"] = {
                "U_ir_equals_A_modulo_size_attrs": sum(r["soft"]["plain_marked_ir_equals_attr_original_modulo_size_attrs"] for r in records.values()),
                "AU_ir_equals_A_modulo_loop_metadata": sum(r["soft"]["attr_marked_ir_equals_attr_original_modulo_loop_metadata"] for r in records.values()),
                "P_ir_equals_A_modulo_size_attrs": sum(r["cells"]["plain/service_original"]["ir_nosize_sha256"] == r["cells"]["attr/service_original"]["ir_nosize_sha256"] for r in records.values()),
                "U_late_attr_object_equals_A_object": sum(r["codegen_control"]["plain_marked_oz_late_attr"]["object_sha256"] == r["cells"]["attr/service_original"]["object_sha256"] for r in records.values()),
                "A_stripped_object_equals_U_object": sum(r["codegen_control"]["attr_oz_stripped"]["object_sha256"] == r["cells"]["plain/service_marked"]["object_sha256"] for r in records.values()),
                "programs_P_ic_equals_A_ic": sum(x["ic"]["P"] == x["ic"]["A"] for x in rows),
                "programs_U_ic_equals_A_ic": sum(x["ic"]["U"] == x["ic"]["A"] for x in rows),
                "programs_U_ic_differs_from_A_ic": [x["uri"] for x in rows if x["ic"]["U"] != x["ic"]["A"]]}
            s["split_by_unrolling"] = {}
            for label, keep in (("programs_with_unrolled_loops", lambda x: x["unroll_remarks_plain"] > 0),
                                ("programs_without_unrolled_loops", lambda x: x["unroll_remarks_plain"] == 0)):
                sel = [x for x in rows if keep(x)]
                s["split_by_unrolling"][label] = {"programs": len(sel), **{m: {n: sum(x[m][n] for x in sel) for n in ("P", "U", "A", "AU")} for m, _ in METRICS}}
            s["code_bytes_larger_without_unrolling"] = [{"uri": x["uri"], **{n: x["text_sec"][n] for n in ("P", "U", "A")}} for x in rows if x["text_sec"]["U"] > x["text_sec"]["P"]]
            s["intervention_disagreements"] = [
                {"uri": u, "cell": f"{v}/{rep}", **{m: {"service_marked": r["cells"][f"{v}/service_marked"][m], rep: r["cells"][f"{v}/{rep}"][m]} for m, _ in METRICS}}
                for u, r in sorted(records.items()) for v in ("plain", "attr") for rep in ("replica_disable_unroll", "replica_threshold0")
                if not r["soft"][f"{v}/{rep}_ir_equals_marked_modulo_loop_metadata"]]
            canon = json.loads((ROOT / "results/baseline_audit/llvm10_canonical/summary.json").read_text())["suites"]["npb-v0"]
            s["canonical_cross_check"] = {m: {"P_sum_here": s["totals"][m]["sums"]["P"], "canonical_plain_baseline_sum": canon["plain"]["portfolio"][m]["baseline_sum"],
                                              "A_sum_here": s["totals"][m]["sums"]["A"], "canonical_attr_baseline_sum": canon["attr"]["portfolio"][m]["baseline_sum"]}
                                          for m, _ in METRICS}

    # ---------- campaign ----------
    if "campaign" in stages:
        records, problems = stages["campaign"]
        s = summary["campaign"]
        md += [f"## Campaign: {s['valid']} of {s['programs']} NPB programs valid", "",
               f"Fingerprint `{s['fingerprint'][:16]}`. Not valid: {len(problems)}" + ("" if not problems else ": " + "; ".join(f"{u}: {p}" for u, p in problems.items())) + ".", ""]
        md += ["### Sums over the valid set", ""]
        rows = []
        for m, label in METRICS:
            t = s["totals"][m]["sums"]
            rows.append([label, fmt(t["P"]), fmt(t["U"]), fmt(t["A"]), fmt(t["AU"])])
        md += [table(["Metric", "P plain", "U plain, no unrolling", "A attr", "AU attr, no unrolling"], rows), ""]
        rows = []
        for m, label in METRICS:
            d, t = s["totals"][m]["differences"], s["totals"][m]
            ratio = t["ratio_of_sums_(P-U)/(P-A)"]
            rows.append([label, fmt(d["P-A"]), fmt(t["P_to_A_pct_of_P"]) + "%", fmt(d["P-U"]), fmt(t["P_to_U_pct_of_P"]) + "%",
                         fmt(d["U-A"]), fmt(d["A-AU"]), "n/a" if ratio is None else f"{fmt(d['P-U'])} / {fmt(d['P-A'])} = {ratio:.4f}"])
        md += [table(["Metric", "P-A", "% of P", "P-U", "% of P", "U-A (residual)", "A-AU", "ratio of sums (P-U)/(P-A)"], rows), "",
               "The ratio is printed with its numerator and denominator, is not clamped, and is not a unique additive "
               "decomposition of causes (see the code generation control for the path dependence).", ""]
        md += ["### Programs with and without unrolled loops on the plain input", ""]
        rows = []
        for label, d in s["split_by_unrolling"].items():
            for m, mlabel in METRICS:
                rows.append([f"{label.replace('_', ' ')} ({d['programs']})", mlabel, fmt(d[m]["P"]), fmt(d[m]["U"]), fmt(d[m]["A"]), fmt(d[m]["P"] - d[m]["U"]), fmt(d[m]["P"] - d[m]["A"]), fmt(d[m]["U"] - d[m]["A"])])
        md += [table(["Set", "Metric", "P", "U", "A", "P-U", "P-A", "U-A"], rows), "",
               "Programs where switching unrolling off makes the code section larger (U > P): " +
               ("; ".join(f"{x['uri'].split('//')[1]} P {x['P']:,} U {x['U']:,} A {x['A']:,}" for x in s["code_bytes_larger_without_unrolling"]) or "none") + ".", ""]
        md += ["### Per-program shares (P-U)/(P-A)", ""]
        rows = []
        for m, label in METRICS:
            d = s["share_distribution"][m]
            rows.append([label, d["programs"], d["denominator_zero"], d["denominator_zero_with_nonzero_numerator"], d.get("exactly_1", 0),
                         d.get("below_0", 0), d.get("above_1", 0), fmt(d.get("min"), 4), fmt(d.get("q1"), 4), fmt(d.get("median"), 4),
                         fmt(d.get("q3"), 4), fmt(d.get("max"), 4), fmt(d.get("mean"), 4)])
        md += [table(["Metric", "n", "P=A (undefined)", "of those, P!=U", "share = 1", "< 0", "> 1", "min", "Q1", "median", "Q3", "max", "mean"], rows), ""]
        ident = s["identity_counts"]
        md += ["### IR identities", "",
               f"- U has the same complete IR as A once `minsize`/`optsize` and loop metadata are normalized away: **{ident['U_ir_equals_A_modulo_size_attrs']} of {s['valid']}** programs.",
               f"- P has the same IR as A (attributes change nothing in the IR): {ident['P_ir_equals_A_modulo_size_attrs']} programs; P IC = A IC on {ident['programs_P_ic_equals_A_ic']}.",
               f"- AU has the same IR as A up to loop metadata: {ident['AU_ir_equals_A_modulo_loop_metadata']} programs.",
               f"- U IC = A IC on {ident['programs_U_ic_equals_A_ic']} programs; differs on: {', '.join(ident['programs_U_ic_differs_from_A_ic']) or 'none'}.",
               f"- Object of `U + late attributes` is byte-identical to the object of A: {ident['U_late_attr_object_equals_A_object']} programs; object of `A stripped` identical to U: {ident['A_stripped_object_equals_U_object']} programs.", ""]
        rem = s["unroll_remarks"]
        md += ["### Unrolling actually performed (replica remarks; replica IR is identical to the service IR on every valid program)", "",
               table(["Input", "programs with unrolling", "loops unrolled", "by kind", "remarks after the interventions"],
                     [[v, rem[v]["programs_with_unrolling"], fmt(rem[v]["total"]), json.dumps(rem[v]["by_name"]), rem[v]["after_intervention_total"]] for v in ("plain", "attr")]), "",
               "Trip counts on the plain input: " + "; ".join(f"{k}: {n}" for k, n in list(rem["plain"]["by_message"].items())[:8]) + ".", ""]
        md += ["### Code generation control (fixed optimized IR, attributes changed only before `llc`)", ""]
        rows = []
        for m, label in METRICS:
            t, d = s["totals"][m]["sums"], s["totals"][m]["differences"]
            rows.append([label, fmt(t["P"]), fmt(t["plain_oz_late_attr"]), fmt(d["P-P_late_attr"]), fmt(t["U"]), fmt(t["plain_marked_oz_late_attr"]),
                         fmt(d["U-U_late_attr"]), fmt(t["attr_oz_stripped"]), fmt(t["A"]), fmt(d["A_stripped-A"])])
        md += [table(["Metric", "P", "P + late attrs", "diff", "U", "U + late attrs", "diff", "A stripped", "A", "diff"], rows), "",
               "Two orders of the same two changes, in code bytes: unrolling off first (P-U) then attributes in code "
               f"generation (U-A): {fmt(s['totals']['text_sec']['differences']['P-U'])} + {fmt(s['totals']['text_sec']['differences']['U-A'])}; attributes in code generation first "
               f"(P - P+late): {fmt(s['totals']['text_sec']['differences']['P-P_late_attr'])}, then the rest (P+late - A): {fmt(s['totals']['text_sec']['differences']['P_late_attr-A'])}. "
               "The split depends on the order, so the two effects interact.", ""]
        md += ["### Agreement of the three interventions and replica hashes (soft checks)", ""]
        rows = [[n, v["true"], len(v["false"]), ", ".join(u.split("//")[1] for u in v["false"][:6]) + (" ..." if len(v["false"]) > 6 else "")]
                for n, v in s["soft_checks"].items()]
        md += [table(["Soft check", "true", "false", "false on"], rows), ""]
        md += ["Cells where a replica intervention does not give the IR of the primary intervention (U or AU) up to loop metadata:", ""]
        md += [table(["Program", "Cell", "IC primary / replica", "code bytes", "Berkeley text"],
                     [[d["uri"].split("//")[1], d["cell"], *[" / ".join(fmt(x) for x in d[m].values()) for m, _ in METRICS]] for d in s["intervention_disagreements"]] or [["none", "", "", "", ""]]), ""]
        cc = s["canonical_cross_check"]
        md += ["### Cross-check against the canonical audit sums (NPB 120)", "",
               table(["Metric", "P here", "canonical plain -Oz", "A here", "canonical attr -Oz"],
                     [[label, fmt(cc[m]["P_sum_here"]), fmt(cc[m]["canonical_plain_baseline_sum"]), fmt(cc[m]["A_sum_here"]), fmt(cc[m]["canonical_attr_baseline_sum"])] for m, label in METRICS]), ""]

    # ---------- pilot ----------
    if "pilot" in stages:
        records, problems = stages["pilot"]
        s = summary["pilot"]
        md += [f"## Pilot: {s['valid']} of {s['programs']} valid (deliberately chosen explanatory programs)", ""]
        rows = []
        for x in s["per_program"]:
            for m, label in METRICS:
                v = x[m]
                share = v["share_(P-U)/(P-A)"]
                rows.append([x["uri"].split("//")[1], label, fmt(v["P"]), fmt(v["U"]), fmt(v["A"]), fmt(v["AU"]), fmt(v["plain_oz_late_attr"]),
                             fmt(v["plain_marked_oz_late_attr"]), fmt(v["attr_oz_stripped"]),
                             "undefined (P=A)" if share is None else f"{v['share_numerator_P-U']:,} / {v['share_denominator_P-A']:,} = {fmt(share, 4)}"])
        md += [table(["Program", "Metric", "P", "U", "A", "AU", "P + late attrs", "U + late attrs", "A stripped", "(P-U)/(P-A)"], rows), ""]
        if "campaign" in stages:
            rep = summary["pilot_vs_campaign"] = {}
            for uri, r in records.items():
                c = stages["campaign"][0].get(uri)
                if c:
                    rep[uri] = {cell: {h: r["cells"][cell][h] == c["cells"][cell][h] for h in ("ic", "text", "text_sec", "ir_sha256", "bitcode_sha256", "object_sha256")}
                                for cell in r["cells"]}
            allsame = all(all(v.values()) for cells in rep.values() for v in cells.values())
            md += [f"Repeatability: {len(rep)} NPB pilot programs were executed again by the campaign in another process; "
                   f"all metrics and all IR, bitcode and object hashes of all twelve cells identical: **{allsame}**.", ""]

    example = OUT / "example_npb116_transfb_nc0/example.json"
    if example.exists():
        e = json.loads(example.read_text())
        summary["example"] = {k: e[k] for k in ("function", "checks", "shape", "behaviour")}
        summary["example"]["function_bytes"] = {k: e["function_bytes"][k] for k in ("full_module_pilot", "example")}
        summary["example"]["cells"] = {k: {m: c[m] for m in ("ic", "text_sec", "text")} for k, c in e["cells"].items()}
        fb = e["function_bytes"]["full_module_pilot"]
        md += ["## Small example: `transfb_nc0` of npb-v0/116", "",
               "One function, extracted unchanged with `llvm-extract` (LLVM 10.0.0) from the canonical service input; the original C source is not available and none is invented. "
               "All checks true: " + str(all(e["checks"].values())) + ".", "",
               table(["Cell", "IC", "function bytes (same in the full module object)", "fmul copies", "conditional branches", "basic blocks"],
                     [["O0 input", e["cells"]["plain/replica_service"]["function_before"]["ic"], "", e["shape"]["plain"]["fmul"], e["shape"]["plain"]["conditional_branches"], e["shape"]["plain"]["basic_blocks"]],
                      ["P: plain, service -Oz", e["cells"]["plain/service_original"]["ic"], fb["plain-service_original"], e["shape"]["plain-service_original"]["fmul"], e["shape"]["plain-service_original"]["conditional_branches"], e["shape"]["plain-service_original"]["basic_blocks"]],
                      ["U: plain, unrolling off", e["cells"]["plain/service_marked"]["ic"], fb["plain-service_marked"], e["shape"]["plain-service_marked"]["fmul"], e["shape"]["plain-service_marked"]["conditional_branches"], e["shape"]["plain-service_marked"]["basic_blocks"]],
                      ["A: attr, service -Oz", e["cells"]["attr/service_original"]["ic"], fb["attr-service_original"], e["shape"]["attr-service_original"]["fmul"], e["shape"]["attr-service_original"]["conditional_branches"], e["shape"]["attr-service_original"]["basic_blocks"]],
                      ["P + late attrs (codegen only)", e["codegen_control"]["plain_oz_late_attr"]["ic"], fb["control-plain_oz_late_attr"], "", "", ""],
                      ["U + late attrs (codegen only)", e["codegen_control"]["plain_marked_oz_late_attr"]["ic"], fb["control-plain_marked_oz_late_attr"], "", "", ""],
                      ["A stripped (codegen only)", e["codegen_control"]["attr_oz_stripped"]["ic"], fb["control-attr_oz_stripped"], "", "", ""]]), "",
               f"Behaviour check: {e['behaviour']['scope']}; all variants identical to the unoptimized input: {e['checks']['behaviour_all_variants_identical']}.", ""]

    if "campaign" in stages:
        md += ["## Per-program table (campaign)", ""]
        rows = []
        for x in summary["campaign"]["per_program"]:
            share = x["ic"]["share_(P-U)/(P-A)"]
            rows.append([x["uri"].rsplit("/", 1)[1], x["unroll_remarks_plain"], x["unroll_remarks_attr"],
                         *[fmt(x["ic"][n]) for n in ("P", "U", "A", "AU")], "P=A" if share is None else f"{share:.3f}",
                         *[fmt(x["text_sec"][n]) for n in ("P", "U", "A")], *[fmt(x["text"][n]) for n in ("P", "U", "A")]])
        md += [table(["npb", "unrolled loops plain", "attr", "IC P", "IC U", "IC A", "IC AU", "IC share", "code P", "code U", "code A", "Berk P", "Berk U", "Berk A"], rows), ""]

    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text("\n".join(md))
    print("\n".join(md[:60]))


if __name__ == "__main__":
    main()

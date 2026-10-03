"""Independent recomputation of the canonical audit (results/baseline_audit/llvm10_canonical)
and the selection analysis, from the individual records only."""
import json, glob, hashlib, os, sys
from statistics import median
R = "results/baseline_audit/llvm10_canonical"
man = json.load(open(f"{R}/manifest.json")); summ = json.load(open(f"{R}/summary.json"))
recs = [json.load(open(f)) for f in sorted(glob.glob(f"{R}/records/*.json"))]
out = {}
def note(k, v): out[k] = v; print(f"{k}: {v}")
note("records", len(recs)); note("manifest_sources", len(man["sources"]))
note("fingerprints_match_manifest", all(r["fingerprint"] == man["fingerprint"] for r in recs))
note("record_uris_equal_sources", {r["uri"] for r in recs} == set(man["sources"]))
note("failed_records", sum("failed" in r for r in recs))
note("suite_counts", {s: sum(r["suite"] == s for r in recs) for s in ("npb-v0", "mibench-v1", "blas-v0")})
note("excluded_above_cap", len(man["excluded_above_cap"]))
note("max_o0_in_records", max(r["original_environment"]["o0"] for r in recs))
# membership vs original battery files (o0 <= 6000, oz present)
batt = {}
for s in ("npb-v0", "mibench-v1", "blas-v0"):
    for f in glob.glob(f"results/battery/{s}/*.json"):
        if f.endswith("_aggregate.json"): continue
        b = json.load(open(f))
        if "oz" in b and b["o0"] <= 6000: batt[b["uri"]] = b
note("membership_equals_battery_le6000", set(batt) == {r["uri"] for r in recs})
# O0/Oz reproduction, portfolio IC reproduction
note("o0_oz_reproduced", sum(r["original_environment"]["o0"] == batt[r["uri"]]["o0"] and r["original_environment"]["oz"] == batt[r["uri"]]["oz"] for r in recs))
pm = 0; pn = 0
for r in recs:
    src = r["paper_reference"]
    if "portfolio_ics" in src:
        pn += 1; pm += [e["ic"] for e in r["plain"]["portfolio"]] == src["portfolio_ics"]
note("portfolio_ic_reproduced", f"{pm}/{pn} programs (1680 candidate ICs expected: {pm*8})")
# attributes: definitions annotated, IC unchanged, unique URIs by content
note("attr_o0_unchanged", all(r["attr"]["o0_ic"] == r["plain"]["o0_ic"] == r["original_environment"]["o0"] for r in recs))
note("all_definitions_annotated", all(r["attribute_info"]["definitions"] == r["attribute_info"]["verified_size_definitions"] for r in recs))
note("input_sha_distinct_plain_vs_attr", all(r["plain"]["input_sha256"] != r["attr"]["input_sha256"] for r in recs))
note("ir_identity_on_reload_recorded", all("ir_sha256" in r[v] for r in recs for v in ("plain", "attr")))
# service Oz vs observation and vs CLI
note("service_oz_equals_observation_plain", all(r["plain"]["oz"]["ic"] == r["original_environment"]["oz"] for r in recs))
cli_diff = {s: {v: sum(r[v]["cli_oz_diagnostic"]["ic"] != r[v]["oz"]["ic"] for r in recs if r["suite"] == s) for v in ("plain", "attr")} for s in ("npb-v0", "mibench-v1", "blas-v0")}
note("cli_oz_ic_differs_from_service", cli_diff)
# candidate completeness
note("all_candidates_ok", all(len(r[v][m]) == 8 and all(e["ok"] for e in r[v][m]) for r in recs for v in ("plain", "attr") for m in ("portfolio", "random")))
note("total_candidate_measurements", sum(len(r[v][m]) for r in recs for v in ("plain", "attr") for m in ("portfolio", "random")))
# selection rule: min IC, first on ties; bytes of that same candidate
def sel(entries, key):
    return min(enumerate(entries), key=lambda p: (p[1][key], p[0]))
bad = 0
for r in recs:
    for v in ("plain", "attr"):
        for m in ("portfolio", "random"):
            i, e = sel(r[v][m], "ic"); b = r[v][m + "_best"]["by_ic"]
            if b["index"] != i or b["text_sec"] != e["text_sec"] or b["text"] != e["text"]: bad += 1
note("selection_by_ic_and_same_candidate_bytes_ok", bad == 0)
# totals
def tot(rows, v, m, key, selkey="ic"):
    return sum(r[v]["oz"][key] for r in rows), sum(sel(r[v][m], selkey)[1][key] for r in rows)
def gain(b, c): return 100 * (1 - c / b)
table = {}
for s in ("npb-v0", "mibench-v1", "blas-v0"):
    rows = [r for r in recs if r["suite"] == s]
    for m in ("portfolio", "random"):
        for v in ("plain", "attr"):
            for key in ("ic", "text", "text_sec"):
                b, c = tot(rows, v, m, key)
                w = sum(sel(r[v][m], "ic")[1][key] < r[v]["oz"][key] for r in rows); t = sum(sel(r[v][m], "ic")[1][key] == r[v]["oz"][key] for r in rows)
                table[f"{s}/{m}/{v}/{key}"] = {"oz": b, "cand": c, "gain_pct": round(gain(b, c), 2), "wtl": f"{w}/{t}/{len(rows)-w-t}",
                                             "summary_json_gain": round(summ["suites"][s][v][m][key]["gain_pct"], 2)}
for k, v in table.items(): print(f"  {k:<32} oz {v['oz']:>8} cand {v['cand']:>8} gain {v['gain_pct']:+6.2f}% (summary {v['summary_json_gain']:+6.2f}%) W/T/L {v['wtl']}")
out["table"] = table
# per-program medians vs sum-based percentages (attr, portfolio, code bytes)
for s in ("npb-v0", "mibench-v1", "blas-v0", "all"):
    rows = recs if s == "all" else [r for r in recs if r["suite"] == s]
    g = [100 * (1 - sel(r["attr"]["portfolio"], "ic")[1]["text_sec"] / r["attr"]["oz"]["text_sec"]) for r in rows]
    print(f"  attr portfolio code bytes {s}: sum-based {gain(*tot(rows,'attr','portfolio','text_sec')):+.2f}%  median per program {median(g):+.2f}%  mean {sum(g)/len(g):+.2f}%")
# sign disagreement (attr, portfolio, IC-selected): IC win & code loss, IC loss & code win
def sign(c, b): return "win" if c < b else "loss" if c > b else "tie"
q = {}
for r in recs:
    e = sel(r["attr"]["portfolio"], "ic")[1]; b = r["attr"]["oz"]
    key = sign(e["ic"], b["ic"]) + "/" + sign(e["text_sec"], b["text_sec"]); q[key] = q.get(key, 0) + 1
note("attr_portfolio_ic_vs_code_outcomes", q); note("opposite_sign_total", q.get("win/loss", 0) + q.get("loss/win", 0))
# selection by IC vs by bytes (attr, portfolio), all and without NPB
for name, rows in (("all", recs), ("without_npb", [r for r in recs if r["suite"] != "npb-v0"])):
    b, c_ic = tot(rows, "attr", "portfolio", "text_sec", "ic"); _, c_by = tot(rows, "attr", "portfolio", "text_sec", "text_sec")
    helped = sum(sel(r["attr"]["portfolio"], "ic")[1]["text_sec"] > sel(r["attr"]["portfolio"], "text_sec")[1]["text_sec"] for r in rows)
    print(f"  attr portfolio code bytes {name}: choose by IC {gain(b,c_ic):+.2f}%  choose by bytes {gain(b,c_by):+.2f}%  programs helped {helped}/{len(rows)}")
    # bytes + Oz fallback with prefix k
    for k in (1, 3, 8):
        c = 0; wins = ties = 0
        for r in rows:
            i, e = sel(r["attr"]["portfolio"][:k], "text_sec"); bb = r["attr"]["oz"]["text_sec"]
            v = min(e["text_sec"], bb); c += v; wins += v < bb; ties += v == bb
        print(f"     {k} sequences + Oz (bytes, fallback): {gain(b,c):+.2f}%  wins {wins} ties {ties} of {len(rows)}")
# concentration: top-5 positive IC-selected savers (attr portfolio code bytes), all
pts = sorted(((r["attr"]["oz"]["text_sec"] - sel(r["attr"]["portfolio"], "ic")[1]["text_sec"], r["uri"]) for r in recs), key=lambda p: (-p[0], p[1]))
net = sum(p[0] for p in pts); top = pts[:5]; top_sum = sum(p[0] for p in top)
print(f"  concentration (all, attr, portfolio, IC-selected code bytes): net saved {net}, top5 {top_sum} ({100*top_sum/net:.1f}% of net), top5 uris {[p[1] for p in top]}")
omit = {p[1] for p in top}; rest = [r for r in recs if r["uri"] not in omit]
b, c_ic = tot(rest, "attr", "portfolio", "text_sec", "ic"); _, c_by = tot(rest, "attr", "portfolio", "text_sec", "text_sec")
print(f"  after omitting top5: choose by IC {gain(b,c_ic):+.2f}%, by bytes {gain(b,c_by):+.2f}% (n={len(rest)})")
# compare with analysis.json
try:
    an = json.load(open("results/baseline_selection_audit/analysis.json"))
    g = an["groups"]
    print("  analysis.json: all attr portfolio ic_first %.2f%% bytes %.2f%%; without_npb %.2f%% -> %.2f%%; budget 3+Oz all %.2f%%, 8+Oz %.2f%%; opposite-sign %s" % (
        g["all"]["attr"]["portfolio"]["selectors"]["ic_first"]["text_sec"]["gain_pct"], g["all"]["attr"]["portfolio"]["selectors"]["bytes"]["text_sec"]["gain_pct"],
        g["without_npb"]["attr"]["portfolio"]["selectors"]["ic_first"]["text_sec"]["gain_pct"], g["without_npb"]["attr"]["portfolio"]["selectors"]["bytes"]["text_sec"]["gain_pct"],
        g["all"]["attr"]["portfolio"]["byte_budget_curve"]["3"]["text_sec"]["gain_pct"], g["all"]["attr"]["portfolio"]["byte_budget_curve"]["8"]["text_sec"]["gain_pct"],
        {k: v for k, v in g["all"]["attr"]["portfolio"]["ic_vs_code_outcomes"].items() if k in ("win/loss", "loss/win")}))
    print("  analysis.json concentration all attr portfolio:", {k: v for k, v in g["all"]["attr"]["portfolio"]["concentration"].items() if k != "top5_uris"})
except Exception as e:
    print("analysis.json check failed:", e)
json.dump(out, open("results/gnn_attribute_audit/verification/verify_canonical.json", "w"), indent=1)

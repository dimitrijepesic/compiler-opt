"""Independent recomputation of the CHStone source-build check, the source-aware
portfolio validation, the size-portfolio demo and the CLI audits, from records."""
import json, glob, os
print("=== CHStone source-build check (results/baseline_audit/llvm10_source_check) ===")
S = json.load(open("results/baseline_audit/llvm10_source_check/summary.json"))
recs = S["records"]; assert len(recs) == 12 and all("failed" not in r for r in recs)
per = [json.load(open(f"results/baseline_audit/llvm10_source_check/{r['uri'].split('/')[-1]}.json")) for r in recs]
assert all(a == b for a, b in zip(recs, per)), "summary records differ from per-program files"
variants = ("real_clang_oz", "clang_size_attributes_cli_oz", "plain_service_oz", "attr_service_oz", "attr_cli_oz")
tot = {v: {m: sum(r[v][m] for r in recs) for m in ("ic", "text", "text_sec")} for v in variants}
for v in variants: print(f"  {v:<30} IC {tot[v]['ic']:>6}  Berkeley text {tot[v]['text']:>6}  code {tot[v]['text_sec']:>6}  ({100*(tot[v]['text_sec']/tot['real_clang_oz']['text_sec']-1):+.2f}% vs real clang -Oz)")
print("  summary.json totals agree:", all(S["totals"][v][m] == tot[v][m] for v in variants for m in ("ic", "text", "text_sec")))
ident = [r["manual_vs_frontend_attributes"] for r in recs]
print("  manual-vs-frontend attributes: identical code bytes on", sum(i["identical_code_bytes"] for i in ident), "/12; identical whole objects on", sum(i["identical_object_bytes"] for i in ident), "/12; equal IC on", sum(i["equal_ic"] for i in ident))
print("  per program code bytes (real / attr_service / plain_service):")
for r in recs:
    n = r["uri"].split("/")[-1]; a, p, x = r["real_clang_oz"]["text_sec"], r["attr_service_oz"]["text_sec"], r["plain_service_oz"]["text_sec"]
    print(f"    {n:<9} {a:>6} {p:>6} ({100*(p/a-1):+6.2f}%) {x:>6} ({100*(x/a-1):+6.2f}%)")
print("  clang:", S["clang_version"].strip().splitlines()[0], "| cgym", S["compiler_gym"], "| source files hashed per program:", [len(r["source_files"]) for r in recs])

print("\n=== Source-aware portfolio validation (results/size_portfolio_source_check) ===")
F = json.load(open("results/size_portfolio_source_check/functional_checks.json"))
P = F["programs"]; assert len(P) == 12
print("  all passed:", all(p["passed"] for p in P), "| execution note:", F["execution"])
real = sum(p["real_clang_oz_object"]["text_sec"] for p in P); sel = sum(p["source_selected_code_bytes"] for p in P)
wins = sum(p["source_selected"] != "reference_clang_oz" for p in P)
print(f"  real clang -Oz code bytes {real}, source-aware selected {sel}, saving {100*(1-sel/real):.2f}%, portfolio chosen on {wins}/12, reference returned on {12-wins}/12")
# reference matches source check; selected artifacts identity; tests
byname = {r["uri"].split("/")[-1]: r for r in recs}
ok_ref = all(p["real_clang_oz_object"]["text_sec"] == byname[p["name"]]["real_clang_oz"]["text_sec"] and p["real_clang_oz_object"]["code_sha256"] == byname[p["name"]]["real_clang_oz"]["code_sha256"] for p in P)
print("  reference object code bytes and code hash equal the source-build check on all 12:", ok_ref)
n_exec = 0; n_ok = 0; same_out = 0
for p in P:
    ref = p["tests"]["real_clang_oz"]
    for k, t in p["tests"].items():
        n_exec += 1; n_ok += t["exit_code"] == 0; same_out += (t["stdout"] == ref["stdout"])
    sel_exe = p["tests"]["source_selected"]["executable_sha256"]
    expect = p["tests"]["real_clang_oz" if p["source_selected"] == "reference_clang_oz" else p["source_selected"]]["executable_sha256"]
    assert sel_exe == expect, (p["name"], "source_selected executable differs from the chosen candidate's executable")
    if p["selected"] != "oz":
        assert p["tests"]["selected"]["executable_sha256"] == p["tests"][p["selected"]]["executable_sha256"]
    # service-selected vs service baseline
    d = json.load(open(f"results/size_portfolio_source_check/{p['name']}/selection.json"))
    assert d["selected"] == p["selected"] and d["candidates"][0]["text_sec"] == byname[p["name"]]["attr_service_oz"]["text_sec"]
    assert [c["label"] for c in d["candidates"]] == ["oz", "portfolio_1", "portfolio_2", "portfolio_3"]
    chosen = min(d["candidates"], key=lambda c: (c["text_sec"], d["candidates"].index(c)))
    assert chosen["label"] == d["selected"]
    for lab in ("selected", "source_selected"):
        assert os.path.exists(f"results/size_portfolio_source_check/{p['name']}/{lab}.o")
print(f"  executions {n_exec} (12 x 7), exit 0: {n_ok}, stdout equal to real clang -Oz reference: {same_out}; selected artifacts identical to the chosen candidate's executable: yes; service selection.json consistent: yes")
print("  per program (real / source-selected / artifact / service-baseline / service-selected):")
for p in P:
    print(f"    {p['name']:<9} {p['real_clang_oz_object']['text_sec']:>6} {p['source_selected_code_bytes']:>6} {p['source_selected']:<18} {p['baseline_code_bytes']:>6} {p['selected_code_bytes']:>6} ({p['selected']})")

print("\n=== size_portfolio_demo npb-116 ===")
d = json.load(open("results/size_portfolio_demo/npb-116/selection.json"))
print("  candidates:", [(c["label"], c["ic"], c["text_sec"]) for c in d["candidates"]], "| selected", d["selected"], f"| saving {d['code_bytes_saved']} bytes ({d['code_gain_pct']:.2f}%)", "| Oz IC", d["original_oz_ic"])

print("\n=== CLI audits (results/baseline_audit/llvm10 and llvm18): recompute NPB attr portfolio by IC ===")
for tc in ("llvm10", "llvm18"):
    for suite in ("npb-v0", "mibench-v1", "blas-v0"):
        D = json.load(open(f"results/baseline_audit/{tc}/{suite}.json")); rows = [r for r in D["records"] if "failed" not in r and all(r[v]["portfolio_best"] and r[v]["random_best"] for v in ("plain", "attr", "attr_fp"))]
        line = f"  {tc} {suite:<11} n={len(rows):>3} of {len(D['records'])}"
        for v in ("plain", "attr"):
            oz_ic = sum(r[v]["oz"]["ic"] for r in rows); p_ic = sum(r[v]["portfolio_best"]["by_ic"]["ic"] for r in rows)
            oz_c = sum(r[v]["oz"]["text_sec"] for r in rows); p_c = sum(r[v]["portfolio_best"]["by_ic"]["text_sec"] for r in rows)
            line += f" | {v}: IC {100*(1-p_ic/oz_ic):+.2f}% code {100*(1-p_c/oz_c):+.2f}%"
        s = D["summary"]["variants"]
        line += f" || summary: plain IC {s['plain']['ic']['portfolio_best_by_ic']['gain_pct']:+.2f}% attr IC {s['attr']['ic']['portfolio_best_by_ic']['gain_pct']:+.2f}% attr code {s['attr']['text_sec']['portfolio_best_by_ic']['gain_pct']:+.2f}%"
        print(line)

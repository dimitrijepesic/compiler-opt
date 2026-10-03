#!/usr/bin/env python3
"""Final tables for the GNN attribute audit, computed from the individual
records only (records_null + records_gnn_seed*). Independent of the campaign
script's summarize(); every number here is recomputed from raw fields.

Definitions (per suite, seed, condition c in {plain, attr}, over the paired
common set S of programs where the null record and that seed's GNN record are
complete, i.e. all 8 random candidates, all 8 GNN samples and the argmax
rollout succeeded in BOTH conditions):
  Oz_c      = sum over S of the service -Oz cost in condition c
  GNN_c     = sum over S of the cost of the GNN sample with minimum final IC
              (first sample on ties); bytes are those of that same sample
  RND_c     = same for the 8 random sequences (identical sequences in both
              conditions)
  gain(X)   = 100 * (1 - X_c / Oz_c)                (positive = smaller than -Oz)
  advantage = GNN_c - RND_c   (negative = GNN smaller than random null)
  adv%      = 100 * (GNN_c - RND_c) / Oz_c
  W/T/L     = per-program GNN cost < / = / > random cost
"""
import glob, hashlib, json, os, sys
from datetime import datetime, timezone

MAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# optional argv[1]: another campaign directory (e.g. npb_offset78); its null records fall back to the main campaign
_skip = {sys.argv.index("--npb-from") + 1} if "--npb-from" in sys.argv else set()
ARGS = [a for i, a in enumerate(sys.argv) if i > 0 and i not in _skip and not a.startswith("--")]
OUT = ARGS[0] if ARGS else MAIN
# --npb-from DIR: take the NPB GNN records (and program list entries) from another campaign directory
NPB_FROM = sys.argv[sys.argv.index("--npb-from") + 1] if "--npb-from" in sys.argv else None
SUFFIX = "_merged" if NPB_FROM else ""
NULL_DIR = os.path.join(OUT, "records_null") if os.path.isdir(os.path.join(OUT, "records_null")) else os.path.join(MAIN, "records_null")
SUITES = ["npb-v0", "mibench-v1", "blas-v0", "chstone-v0", "csmith-v0", "poj104-v1"]
SEEDS = [42, 123, 456]
K = 8
METRICS = (("ic", "IC"), ("text_sec", "code section bytes"), ("text", "Berkeley text bytes"))


def load(pattern):
    out = {}
    for f in glob.glob(pattern):
        if "manifest" in f:
            continue
        r = json.load(open(f))
        out[r["uri"]] = r
    return out


def null_ok(r):
    return "failed" not in r and all(r[v].get("random_best") and r[v]["random_best"]["n_fail"] == 0
                                    and len(r[v]["random"]) == K for v in ("plain", "attr"))


def gnn_ok(r):
    return "failed" not in r and all("best_by_ic" in r[v] and r[v]["n_fail"] == 0 and len(r[v]["samples"]) == K
                                    and "argmax" in r[v] for v in ("plain", "attr"))


def sel(entries, key="ic"):
    ok = [(i, e) for i, e in enumerate(entries) if e.get("ok")]
    return min(ok, key=lambda p: (p[1][key], p[0]))


def main():
    programs = {p["uri"]: p for p in json.load(open(os.path.join(OUT, "programs.json")))["programs"]}
    null = load(os.path.join(NULL_DIR, "*.json"))
    gnn = {s: load(os.path.join(OUT, f"records_gnn_seed{s}", "*.json")) for s in SEEDS}
    if NPB_FROM:
        npb_programs = {p["uri"]: p for p in json.load(open(os.path.join(NPB_FROM, "programs.json")))["programs"] if p["suite"] == "npb-v0"}
        programs.update(npb_programs)
        for s in SEEDS:
            repl = {u: r for u, r in load(os.path.join(NPB_FROM, f"records_gnn_seed{s}", "*.json")).items() if r["suite"] == "npb-v0"}
            gnn[s] = {u: r for u, r in gnn[s].items() if r["suite"] != "npb-v0"}
            gnn[s].update(repl)
    rep = {"timestamp": datetime.now(timezone.utc).isoformat(), "programs": len(programs), "null": {}, "seeds": {}, "rows": []}
    rep["null"] = {"records": len(null), "ok": sum(null_ok(r) for r in null.values()),
                   "failures": [{"uri": u, "error": r.get("failed", "candidate failure")[:200]} for u, r in null.items() if not null_ok(r)]}
    lines = ["# GNN sampler vs paired random null with and without size attributes: final tables" + (f" (NPB GNN records from {os.path.relpath(NPB_FROM, OUT)})" if NPB_FROM else ""), "",
             f"Generated {rep['timestamp']}. Programs in the list: {len(programs)}. Null records: {rep['null']['ok']} ok of {rep['null']['records']} "
             f"(failures: {len(rep['null']['failures'])}).", ""]
    # completeness and reproduction per seed
    lines += ["## Attempts, successes, reproduction of the stored original run (plain condition)", "",
              "| seed | GNN records | complete (both cond.) | paired with null | failed/incomplete | stored 8 samples reproduced | argmax reproduced | best-of-8 reproduced |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    common = {}
    for s in SEEDS:
        recs = gnn[s]
        ok = {u: r for u, r in recs.items() if gnn_ok(r)}
        common[s] = sorted(u for u in ok if u in null and null_ok(null[u]))
        rp = [r["plain"]["reproduction"] for r in ok.values()]
        fails = [{"uri": u, "error": r.get("failed", "sample failure")[:200]} for u, r in recs.items() if not gnn_ok(r)]
        rep["seeds"][str(s)] = {"records": len(recs), "complete": len(ok), "paired": len(common[s]), "failures": fails,
                                "missing": sorted(set(programs) - set(recs)),
                                "repro_all8": sum(x["sample_ics_match"] for x in rp), "repro_argmax": sum(x["argmax_match"] for x in rp),
                                "repro_bo8": sum(x["best_of_k_match"] for x in rp), "repro_samples": sum(x["n_sample_matches"] for x in rp)}
        d = rep["seeds"][str(s)]
        lines.append(f"| {s} | {d['records']} | {d['complete']} | {d['paired']} | {len(fails)} (+{len(d['missing'])} not run) | "
                     f"{d['repro_all8']}/{d['complete']} ({d['repro_samples']}/{K*max(d['complete'],1)} samples) | {d['repro_argmax']}/{d['complete']} | {d['repro_bo8']}/{d['complete']} |")
    # per-suite reproduction breakdown
    lines += ["", "Reproduction by suite (programs with all 8 stored sample ICs identical / complete programs):", ""]
    for s in SEEDS:
        parts = []
        for suite in SUITES:
            us = [u for u in common[s] if programs[u]["suite"] == suite]
            parts.append(f"{suite} {sum(gnn[s][u]['plain']['reproduction']['sample_ics_match'] for u in us)}/{len(us)}")
        lines.append(f"- seed {s}: " + ", ".join(parts))
    # attribute sensitivity of the sequences themselves
    lines += ["", "Are the executed sequences' ICs attribute-sensitive? Programs where the 8 GNN sample ICs are identical in both conditions "
              "(the GNN re-samples actions from the new state, so identity is not guaranteed) and where the 8 random-sequence ICs are identical:", ""]
    for s in SEEDS:
        same_g = sum([x["ic"] for x in gnn[s][u]["plain"]["samples"]] == [x["ic"] for x in gnn[s][u]["attr"]["samples"]] for u in common[s])
        same_act = sum([x["actions"] for x in gnn[s][u]["plain"]["samples"]] == [x["actions"] for x in gnn[s][u]["attr"]["samples"]] for u in common[s])
        same_r = sum([x["ic"] for x in null[u]["plain"]["random"]] == [x["ic"] for x in null[u]["attr"]["random"]] for u in common[s])
        lines.append(f"- seed {s}: GNN sample ICs identical on {same_g}/{len(common[s])}, identical action sequences on {same_act}/{len(common[s])}; random ICs identical on {same_r}/{len(common[s])}")
    # baseline change (null records, all programs with complete null; also on each seed's common set below)
    lines += ["", "## Baseline change alone: service -Oz with attributes vs plain (all programs with a complete null record)", "",
              "| suite | n | Oz IC plain | Oz IC attr | change | Oz code plain | Oz code attr | change | Oz Berkeley plain | Oz Berkeley attr | change |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for suite in SUITES + ["ALL"]:
        us = [u for u, r in null.items() if null_ok(r) and (suite == "ALL" or programs[u]["suite"] == suite)]
        if not us:
            continue
        cells = []
        for m, _ in (("ic", ""), ("text_sec", ""), ("text", "")):
            a = sum(null[u]["plain"]["oz"][m] for u in us); b = sum(null[u]["attr"]["oz"][m] for u in us)
            cells.append(f"{a:,} | {b:,} | {100*(b/a-1):+.1f}%")
        lines.append(f"| {suite} | {len(us)} | " + " | ".join(cells) + " |")
    # main tables
    for m, label in METRICS:
        lines += ["", f"## {label}: GNN best-of-8 (selected by final IC) vs paired random best-of-8 (selected by final IC), per suite, seed and condition", "",
                  "| suite | seed | n | cond. | Oz | GNN | random | GNN gain vs Oz | random gain vs Oz | GNN - random | adv% of Oz | W/T/L (GNN vs random) | argmax |",
                  "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|"]
        for suite in SUITES + ["ALL"]:
            for s in SEEDS:
                us = [u for u in common[s] if suite == "ALL" or programs[u]["suite"] == suite]
                if not us:
                    continue
                for v in ("plain", "attr"):
                    oz = sum(null[u][v]["oz"][m] for u in us)
                    g = sum(gnn[s][u][v]["best_by_ic"][m] for u in us)
                    rn = sum(sel(null[u][v]["random"])[1][m] for u in us)
                    am = sum(gnn[s][u][v]["argmax"][m] for u in us)
                    w = sum(gnn[s][u][v]["best_by_ic"][m] < sel(null[u][v]["random"])[1][m] for u in us)
                    t = sum(gnn[s][u][v]["best_by_ic"][m] == sel(null[u][v]["random"])[1][m] for u in us)
                    row = {"metric": m, "suite": suite, "seed": s, "n": len(us), "cond": v, "oz": oz, "gnn": g, "random": rn, "argmax": am,
                           "gnn_gain_pct": 100 * (1 - g / oz) if oz else None, "random_gain_pct": 100 * (1 - rn / oz) if oz else None,
                           "gnn_minus_random": g - rn, "adv_pct_of_oz": 100 * (g - rn) / oz if oz else None, "wtl": f"{w}/{t}/{len(us)-w-t}"}
                    rep["rows"].append(row)
                    lines.append(f"| {suite} | {s} | {len(us)} | {v} | {oz:,} | {g:,} | {rn:,} | {row['gnn_gain_pct']:+.2f}% | {row['random_gain_pct']:+.2f}% | "
                                 f"{g-rn:+,} | {row['adv_pct_of_oz']:+.2f}% | {row['wtl']} | {am:,} |")
    lines += ["", "Notes. Sums are over the paired common set of each seed; percentages are ratios of sums, not means of per-program ratios. "
              "The random null is one fresh draw of 8 sequences per program (seed 42 + per-URI hash; the same draw as results/baseline_audit/llvm10_canonical "
              "on its 210 programs), used unchanged for all three GNN seeds, so the three seed rows share the null and are not independent replicates of the null. "
              "Programs within a suite are related modules, not independent applications. No p-values are reported here.",
              "", "The attribute condition adds `minsize optsize` to function definitions of the service module on both sides; it is not a source-level `clang -Oz` build."]
    os.makedirs(os.path.join(OUT, "verification"), exist_ok=True)
    json.dump(rep, open(os.path.join(OUT, "verification", f"report_gnn{SUFFIX}.json"), "w"), indent=1)
    open(os.path.join(OUT, "verification", f"report_gnn{SUFFIX}.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Transfer check on a modern compiler: the fixed portfolio sequences mined
from random search (results/portfolio_selection.json, no model at
inference) are applied with LLVM 18's new pass manager and compared with
LLVM 18's own -Oz on the paired battery programs.

CompilerGym (LLVM 10) is used only to export each program's O0 bitcode;
optimization and code generation run entirely in the system LLVM 18
(`opt-18`, `llc-18`, `llvm-size-18`). The 36 legacy pass names are mapped
to their new-PM equivalents; three passes removed since LLVM 10 are
approximated by their closest successor (PASS_MAP).

Resumable: one JSON per program under <out-dir>/<suite>/, skipped when
present. Run inside the WSL environment:

  python scripts/llvm18_transfer.py --check-passes
  python scripts/llvm18_transfer.py
  python scripts/llvm18_transfer.py --aggregate
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

import numpy as np
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

LLVM_VERSION = "18"
OPT = f"opt-{LLVM_VERSION}"
LLC = f"llc-{LLVM_VERSION}"
SIZE = f"llvm-size-{LLVM_VERSION}"

# legacy LLVM 10 name -> (new-PM name, pipeline level)
# level: "module" | "cgscc" | "function" | "loop"
PASS_MAP = {
    "-adce": ("adce", "function"),
    "-aggressive-instcombine": ("aggressive-instcombine", "function"),
    "-bdce": ("bdce", "function"),
    "-constprop": ("instsimplify", "function"),        # removed in LLVM 12
    "-correlated-propagation": ("correlated-propagation", "function"),
    "-dce": ("dce", "function"),
    "-die": ("dce", "function"),                       # merged into dce
    "-dse": ("dse", "function"),
    "-early-cse": ("early-cse", "function"),
    "-early-cse-memssa": ("early-cse<memssa>", "function"),
    "-elim-avail-extern": ("elim-avail-extern", "module"),
    "-flattencfg": ("flattencfg", "function"),
    "-globalopt": ("globalopt", "module"),
    "-gvn": ("gvn", "function"),
    "-gvn-hoist": ("gvn-hoist", "function"),
    "-instcombine": ("instcombine", "function"),
    "-instsimplify": ("instsimplify", "function"),
    "-ipsccp": ("ipsccp", "module"),
    "-jump-threading": ("jump-threading", "function"),
    "-load-store-vectorizer": ("load-store-vectorizer", "function"),
    "-loop-instsimplify": ("loop-instsimplify", "loop"),
    "-loop-simplifycfg": ("loop-simplifycfg", "loop"),
    "-lower-constant-intrinsics": ("lower-constant-intrinsics", "function"),
    "-mem2reg": ("mem2reg", "function"),
    "-memcpyopt": ("memcpyopt", "function"),
    "-mergefunc": ("mergefunc", "module"),
    "-mldst-motion": ("mldst-motion", "function"),
    "-nary-reassociate": ("nary-reassociate", "function"),
    "-newgvn": ("newgvn", "function"),
    "-prune-eh": ("function-attrs", "cgscc"),          # removed in LLVM 15
    "-reassociate": ("reassociate", "function"),
    "-sccp": ("sccp", "function"),
    "-simplifycfg": ("simplifycfg", "function"),
    "-slp-vectorizer": ("slp-vectorizer", "function"),
    "-slsr": ("slsr", "function"),
    "-sroa": ("sroa", "function"),
}
APPROXIMATED = {"-constprop", "-die", "-prune-eh"}


def pipeline_text(legacy_names):
    """Nest a legacy pass sequence into a valid new-PM module pipeline,
    preserving order: consecutive function/loop passes share one
    function(...) adaptor, module passes stay at top level."""
    parts = []
    fn_group = []

    def flush():
        if fn_group:
            parts.append("function(" + ",".join(fn_group) + ")")
            fn_group.clear()

    for name in legacy_names:
        new, level = PASS_MAP[name]
        if level == "function":
            fn_group.append(new)
        elif level == "loop":
            fn_group.append(f"loop({new})")
        else:
            flush()
            parts.append(f"cgscc({new})" if level == "cgscc" else new)
    flush()
    return ",".join(parts)


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def opt(in_bc, out_bc, passes):
    r = run([OPT, f"-passes={passes}", in_bc, "-o", out_bc])
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip().splitlines()[-1][:200]
                           if r.stderr.strip() else "opt failed")


def text_bytes(bc, workdir):
    obj = os.path.join(workdir, "out.o")
    r = run([LLC, "-filetype=obj", "-o", obj, bc])
    if r.returncode != 0:
        raise RuntimeError("llc: " + r.stderr.strip()[-200:])
    out = run([SIZE, obj]).stdout.strip().splitlines()[1].split()
    return int(out[0])


def load_portfolio(passes_yaml="configs/passes.yaml",
                   portfolio_json="results/portfolio_selection.json"):
    with open(passes_yaml) as f:
        names = {p["action_id"]: p["name"] for p in yaml.safe_load(f)["passes"]}
    with open(portfolio_json) as f:
        seqs = json.load(f)["portfolio"]
    return [[names[a] for a in s["actions"]] for s in seqs]


def paired_programs(metrics_dir="results/binary_metrics"):
    """Programs of the paired 347-program subset (those with a GNN
    condition in the LLVM 10 binary metrics), with their LLVM 10 sizes."""
    out = []
    for path in sorted(glob.glob(os.path.join(metrics_dir, "*", "*.json"))):
        if path.endswith("_aggregate.json"):
            continue
        with open(path) as f:
            r = json.load(f)
        if "gnn_bo8" in r:
            out.append(r)
    return out


def safe_name(uri):
    return uri.split("/")[-1].replace(":", "_")


def check_passes():
    """Run every mapped pass alone on a small module and report."""
    import compiler_gym
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark="benchmark://cBench-v1/crc32")
    with tempfile.TemporaryDirectory() as wd:
        bc = os.path.join(wd, "o0.bc")
        env.write_bitcode(bc)
        ok = 0
        for legacy, (new, level) in PASS_MAP.items():
            try:
                opt(bc, os.path.join(wd, "x.bc"), pipeline_text([legacy]))
                status = "ok"
                ok += 1
            except RuntimeError as e:
                status = f"FAIL {e}"
            flag = " (approximated)" if legacy in APPROXIMATED else ""
            print(f"  {legacy:<28} -> {new:<26} {status}{flag}")
        print(f"{ok}/{len(PASS_MAP)} passes parse and run under {OPT}")
        opt(bc, os.path.join(wd, "oz.bc"), "default<Oz>")
        print("Oz text bytes:", text_bytes(os.path.join(wd, "oz.bc"), wd))
    env.close()


def aggregate(out_dir):
    from scipy import stats
    recs = []
    for path in sorted(glob.glob(os.path.join(out_dir, "*", "*.json"))):
        if path.endswith("_aggregate.json"):
            continue
        with open(path) as f:
            recs.append(json.load(f))
    n = len(recs)

    def tot(key):
        return sum(r[key]["text"] for r in recs)

    oz = tot("oz")
    summary = {
        "llvm": LLVM_VERSION, "n": n, "timestamp": datetime.now().isoformat(),
        "approximated_passes": sorted(APPROXIMATED),
        "text_total": {"o0": tot("o0"), "oz": oz,
                       "portfolio_bo8": tot("portfolio_bo8"),
                       "portfolio_bo16": tot("portfolio_bo16"),
                       "oz_llvm10": sum(r["llvm10"]["oz_text"] for r in recs),
                       "gnn_bo8_llvm10": sum(r["llvm10"]["gnn_text"] for r in recs)},
        "sequence_failures": sum(len(r["failed_sequences"]) for r in recs),
    }
    for key in ("portfolio_bo8", "portfolio_bo16"):
        a = [r[key]["text"] for r in recs]
        z = [r["oz"]["text"] for r in recs]
        w = sum(x < y for x, y in zip(a, z))
        t = sum(x == y for x, y in zip(a, z))
        l = n - w - t
        p = stats.wilcoxon(a, z, alternative="less").pvalue if w + l else 1.0
        summary[key] = {"text_vs_oz_pct": round(100 * (1 - sum(a) / oz), 2),
                        "wins": w, "ties": t, "losses": l,
                        "wilcoxon_one_sided_p": float(p),
                        "safe_text_total": sum(min(x, y) for x, y in zip(a, z))}
    per_suite = {}
    for r in recs:
        b = per_suite.setdefault(r["suite"], {"n": 0, "oz": 0, "bo8": 0,
                                              "bo16": 0, "oz10": 0, "gnn10": 0})
        b["n"] += 1
        b["oz"] += r["oz"]["text"]
        b["bo8"] += r["portfolio_bo8"]["text"]
        b["bo16"] += r["portfolio_bo16"]["text"]
        b["oz10"] += r["llvm10"]["oz_text"]
        b["gnn10"] += r["llvm10"]["gnn_text"]
    summary["per_suite"] = per_suite
    with open(os.path.join(out_dir, "_aggregate.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="results/llvm18_transfer")
    p.add_argument("--check-passes", action="store_true")
    p.add_argument("--aggregate", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    if args.check_passes:
        check_passes()
        return
    if args.aggregate:
        aggregate(args.out_dir)
        return

    import compiler_gym
    seqs = load_portfolio()
    pipelines = [pipeline_text(s) for s in seqs]
    programs = paired_programs()
    if args.limit:
        programs = programs[:args.limit]
    print(f"{len(programs)} programs, {len(seqs)} sequences, {OPT}")

    env = compiler_gym.make("llvm-ic-v0")
    done = 0
    for i, rec in enumerate(programs):
        uri, suite = rec["uri"], rec["suite"]
        suite_dir = os.path.join(args.out_dir, suite)
        os.makedirs(suite_dir, exist_ok=True)
        out_path = os.path.join(suite_dir, f"{safe_name(uri)}.json")
        if os.path.exists(out_path):
            continue
        with tempfile.TemporaryDirectory() as wd:
            try:
                env.reset(benchmark=uri)
                o0 = os.path.join(wd, "o0.bc")
                env.write_bitcode(o0)
                oz = os.path.join(wd, "oz.bc")
                opt(o0, oz, "default<Oz>")
                result = {
                    "uri": uri, "suite": suite, "llvm": LLVM_VERSION,
                    "o0": {"text": text_bytes(o0, wd)},
                    "oz": {"text": text_bytes(oz, wd)},
                    "sequences": [], "failed_sequences": [],
                    "llvm10": {"oz_text": rec["oz"]["text"],
                               "rnd_text": rec["rnd_bo8"]["text"],
                               "gnn_text": rec["gnn_bo8"]["text"]},
                }
                for j, pl in enumerate(pipelines):
                    out_bc = os.path.join(wd, f"s{j}.bc")
                    try:
                        opt(o0, out_bc, pl)
                        result["sequences"].append(
                            {"rank": j + 1, "text": text_bytes(out_bc, wd)})
                    except RuntimeError as e:
                        result["failed_sequences"].append(
                            {"rank": j + 1, "error": str(e)})
                if not result["sequences"]:
                    raise RuntimeError("all sequences failed")
                first8 = [s for s in result["sequences"] if s["rank"] <= 8]
                if not first8:
                    raise RuntimeError("all of the first 8 sequences failed")
                best8 = min(first8, key=lambda s: s["text"])
                best16 = min(result["sequences"], key=lambda s: s["text"])
                result["portfolio_bo8"] = {"text": best8["text"],
                                           "rank": best8["rank"]}
                result["portfolio_bo16"] = {"text": best16["text"],
                                            "rank": best16["rank"]}
            except Exception as e:
                print(f"  [{i + 1}] {uri}: FAILED ({e})", flush=True)
                continue
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        done += 1
        print(f"  [{i + 1}/{len(programs)}] {uri}: Oz {result['oz']['text']} "
              f"bo8 {result['portfolio_bo8']['text']} "
              f"bo16 {result['portfolio_bo16']['text']} "
              f"(LLVM10 Oz {rec['oz']['text']})", flush=True)
    env.close()
    print(f"done: {done} new records")
    aggregate(args.out_dir)


if __name__ == "__main__":
    main()

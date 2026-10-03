#!/usr/bin/env python3
"""
Baseline audit: does the -Oz reference change when the input IR carries
the function attributes a real size-optimizing build would have?

CompilerGym benchmarks are -O0 bitcode without `minsize`/`optsize`
(and with "frame-pointer"="all"). The -Oz pipeline applied to such IR
(CompilerGym's IrInstructionCountOz, and `opt -Oz` in this paper's binary
metrics) keeps the loop unroller active and generates code without size
tuning. This script measures, per module and per variant of the input IR,

  plain     the bitcode as shipped (this paper's and CompilerGym's protocol)
  attr      + minsize optsize on every function attribute group
  attr_fp   + "frame-pointer"="none" as well (closer to clang -Oz output)

the following conditions:

  o0            the module itself
  oz            -Oz pipeline
  oz_nounroll   -Oz with -disable-loop-unrolling (plain only; mechanism)
  portfolio[i]  the first K fixed portfolio sequences (results/portfolio_selection.json)
  random[i]     K random 45-step sequences from the curated 36-pass space,
                seeded per module so the same sequences are used in every
                variant

and records instruction count (exact, via the LLVM API tool ic.cpp),
Berkeley `text` and the summed code sections (`.text*` on ELF, `__text` on
Mach-O; MiBench bitcode in CompilerGym targets x86_64-apple-macosx) of the
llc object, generated for the module's own target triple as in the paper.

Selection convention (main comparison): the best-of-K sequence is chosen
by IC, as in the paper's protocol, and its bytes are reported for that
same sequence; selection by bytes is stored separately as a control.
Failed sequences and failed modules are kept in the output; totals are
reported on the common set of modules where every variant succeeded, and
the counts of attempts and failures are printed and stored.

Works with the new pass manager (LLVM >= 13, --pm new, default) through
scripts/llvm18_transfer.py's pass map, and with the legacy pass manager
(LLVM 10, e.g. CompilerGym's bundled toolchain, --pm legacy) where the
36 legacy pass flags are passed to opt directly.

Examples (native macOS, Homebrew llvm@18):
  python scripts/baseline_audit.py --bitcode-dir /path/npb-v0 --suite npb-v0 \
      --llvm-bin /opt/homebrew/opt/llvm@18/bin --out results/baseline_audit/llvm18/npb-v0.json
  python scripts/baseline_audit.py --summarize results/baseline_audit/llvm18/npb-v0.json
"""

import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import multiprocessing
import tempfile
import types
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
if "yaml" not in sys.modules:
    try:
        import yaml  # noqa: F401
    except ImportError:  # llvm18_transfer imports yaml; only load_portfolio uses it
        sys.modules["yaml"] = types.ModuleType("yaml")
from llvm18_transfer import PASS_MAP, pipeline_text  # noqa: E402

EPISODE_STEPS = 45
VARIANTS = ("plain", "attr", "attr_fp")

# set in main() and handed to every worker through the pool initializer
# (macOS spawns workers, so module globals are not inherited)
CFG = {}


def _init_worker(cfg):
    CFG.update(cfg)


# ------------------------------------------------------------------ helpers
def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def tool(name):
    return os.path.join(CFG["llvm_bin"], name)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_pass_names(passes_yaml):
    txt = open(passes_yaml).read()
    names = {}
    for m in re.finditer(r"action_id: (\d+)\n  name: (\S+)", txt):
        names[int(m.group(1))] = m.group(2)
    return names


def load_portfolio(portfolio_json, names, k):
    seqs = json.load(open(portfolio_json))["portfolio"]
    return [[names[a] for a in s["actions"]] for s in seqs[:k]]


def random_sequences(name, k, seed, pass_list):
    h = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng((seed * 1000003 + h) % (2 ** 32))
    return [[pass_list[i] for i in rng.integers(len(pass_list), size=EPISODE_STEPS)]
            for _ in range(k)]


def opt(in_bc, out_bc, seq_names=None, oz=False, extra=()):
    """Apply -Oz or a legacy-named pass sequence; raise on failure."""
    if CFG["pm"] == "legacy":
        args = ["-Oz"] if oz else list(seq_names)
    else:
        args = ["-passes=" + ("default<Oz>" if oz else pipeline_text(seq_names))]
    r = run([tool("opt"), *args, *extra, in_bc, "-o", out_bc])
    if r.returncode:
        msg = r.stderr.strip().splitlines()[-1][:160] if r.stderr.strip() else "opt failed"
        raise RuntimeError(msg)


def sizes(bc, wd):
    obj = os.path.join(wd, "o.o")
    r = run([tool("llc"), "-filetype=obj", "-o", obj, bc])
    if r.returncode:
        raise RuntimeError("llc: " + r.stderr.strip()[-160:])
    berk = int(run([tool("llvm-size"), obj]).stdout.strip().splitlines()[1].split()[0])
    sec = 0
    for line in run([tool("llvm-size"), "-A", obj]).stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and (p[0] in (".text", "__text") or p[0].startswith(".text.")):
            sec += int(p[1])
    return {"text": berk, "text_sec": sec}


def ic(bc):
    r = run([CFG["ic_tool"], bc])
    return int(r.stdout.strip()) if r.returncode == 0 else None


def measure(bc, wd):
    d = sizes(bc, wd)
    d["ic"] = ic(bc)
    return d


def with_attributes(in_bc, out_bc, frame_pointer_none=False):
    """Textual attribute insertion (works on every LLVM version): add
    `minsize optsize` to every function attribute group. Returns the
    number of `define` lines that carry no attribute group (untouched)."""
    ll = run([tool("llvm-dis"), in_bc, "-o", "-"]).stdout
    ll, n_groups = re.subn(r"^(attributes #\d+ = \{)", r"\1 minsize optsize", ll, flags=re.M)
    if frame_pointer_none:
        ll = ll.replace('"frame-pointer"="all"', '"frame-pointer"="none"')
    no_group = sum(1 for line in ll.splitlines()
                   if line.startswith("define ") and not re.search(r"#\d+\s*(\{|personality)", line))
    r = subprocess.run([tool("llvm-as"), "-o", out_bc], input=ll, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError("llvm-as: " + r.stderr.strip()[-160:])
    return {"attribute_groups": n_groups, "defines_without_group": no_group}


def apply_all(src, wd, tag, seqs):
    out = []
    for i, seq in enumerate(seqs):
        bc = os.path.join(wd, f"{tag}{i}.bc")
        try:
            opt(src, bc, seq_names=seq)
            out.append({"ok": True, **measure(bc, wd)})
        except RuntimeError as e:
            out.append({"ok": False, "error": str(e)})
    return out


def select(entries):
    ok = [(e, i) for i, e in enumerate(entries) if e.get("ok") and e.get("ic") is not None]
    if not ok:
        return None
    by_ic = min(ok, key=lambda x: (x[0]["ic"], x[1]))
    by_text = min(ok, key=lambda x: (x[0]["text"], x[1]))
    return {"n_ok": len(ok), "n_fail": len(entries) - len(ok),
            "by_ic": {"index": by_ic[1], "ic": by_ic[0]["ic"], "text": by_ic[0]["text"],
                      "text_sec": by_ic[0]["text_sec"]},
            "by_text": {"index": by_text[1], "ic": by_text[0]["ic"], "text": by_text[0]["text"],
                        "text_sec": by_text[0]["text_sec"]}}


def one(bc_path):
    name = os.path.basename(bc_path)[:-3]
    rec = {"name": name, "sha256": sha256(bc_path)}
    seqs_p = CFG["portfolio"]
    seqs_r = random_sequences(name, CFG["k"], CFG["seed"], CFG["pass_list"])
    rec["random_sequences"] = seqs_r
    try:
        with tempfile.TemporaryDirectory() as wd:
            inputs = {"plain": bc_path}
            attr = os.path.join(wd, "attr.bc")
            rec["attr_info"] = with_attributes(bc_path, attr)
            inputs["attr"] = attr
            fp = os.path.join(wd, "attr_fp.bc")
            with_attributes(bc_path, fp, frame_pointer_none=True)
            inputs["attr_fp"] = fp
            for var in VARIANTS:
                src = inputs[var]
                d = rec[var] = {}
                d["o0"] = measure(src, wd)
                oz = os.path.join(wd, f"{var}_oz.bc")
                opt(src, oz, oz=True)
                d["oz"] = measure(oz, wd)
                if var == "plain":
                    nu = os.path.join(wd, "nounroll.bc")
                    try:
                        opt(src, nu, oz=True, extra=("-disable-loop-unrolling",))
                        d["oz_nounroll"] = measure(nu, wd)
                    except RuntimeError as e:
                        d["oz_nounroll"] = {"error": str(e)}
                d["portfolio"] = apply_all(src, wd, f"{var}_p", seqs_p)
                d["random"] = apply_all(src, wd, f"{var}_r", seqs_r)
                d["portfolio_best"] = select(d["portfolio"])
                d["random_best"] = select(d["random"])
    except Exception as e:  # keep the failure visible
        rec["failed"] = repr(e)[:300]
    return rec


# ------------------------------------------------------------------ summary
def summarize(data, print_rows=True):
    rows = data["records"]
    attempted = len(rows)
    failed_modules = [r["name"] for r in rows if "failed" in r]
    ok_rows = [r for r in rows if "failed" not in r]

    def complete(r):
        return all(r[v]["portfolio_best"] and r[v]["random_best"] for v in VARIANTS)
    common = [r for r in ok_rows if complete(r)]
    seq_attempts = sum(len(r[v][kind]) for r in ok_rows for v in VARIANTS for kind in ("portfolio", "random"))
    seq_fail = sum(1 for r in ok_rows for v in VARIANTS for kind in ("portfolio", "random")
                   for e in r[v][kind] if not e.get("ok"))
    out = {"attempted_modules": attempted, "failed_modules": failed_modules,
           "common_set": len(common), "sequence_runs": seq_attempts,
           "sequence_failures": seq_fail, "variants": {}}
    lines = [f"--- {data['suite']}: LLVM {data['llvm_version']}, pm={data['pm']}, "
             f"attempted {attempted}, failed modules {len(failed_modules)}, common set {len(common)}, "
             f"sequence runs {seq_attempts}, sequence failures {seq_fail}"]

    def pct(x):
        return f"{x:+5.1f}%" if x is not None else "  n/a "

    def tot(var, cond, key, sel=None):
        if sel:
            return sum(r[var][cond][sel][key] for r in common)
        return sum(r[var][cond][key] for r in common)

    def wtl(var, cond, sel, key):
        w = sum(r[var][cond][sel][key] < r[var]["oz"][key] for r in common)
        t = sum(r[var][cond][sel][key] == r[var]["oz"][key] for r in common)
        return f"{w}/{t}/{len(common) - w - t}"

    for var in VARIANTS:
        v = out["variants"][var] = {}
        for key in ("ic", "text", "text_sec"):
            o0 = tot(var, "o0", key)
            oz = tot(var, "oz", key)
            v[key] = {"o0": o0, "oz": oz}
            for cond in ("portfolio_best", "random_best"):
                for sel in ("by_ic", "by_text"):
                    val = tot(var, cond, key, sel)
                    v[key][f"{cond}_{sel}"] = {"total": val, "gain_pct": round(100 * (oz - val) / oz, 2) if oz else None,
                                               "wtl": wtl(var, cond, sel, key)}
        if print_rows:
            for key, label in (("ic", "IC"), ("text", "text"), ("text_sec", ".text")):
                d = v[key]
                p = d["portfolio_best_by_ic"]
                q = d["random_best_by_ic"]
                pb = d["portfolio_best_by_text"]
                lines.append(
                    f"  [{var:<7}] {label:<5} O0 {d['o0']:>8} Oz {d['oz']:>8} | portfolio-{data['k']} (by IC) "
                    f"{p['total']:>8} ({pct(p['gain_pct'])}, W/T/L {p['wtl']}) | random-{data['k']} (by IC) "
                    f"{q['total']:>8} ({pct(q['gain_pct'])}, W/T/L {q['wtl']})"
                    + (f" | portfolio by bytes {pb['total']:>8} ({pct(pb['gain_pct'])})" if key != "ic" else ""))
    nu = [r for r in common if "error" not in r["plain"].get("oz_nounroll", {"error": 1})]
    if not common:
        lines.append("  (empty common set; per-module failures:)")
        for r in ok_rows[:10]:
            lines.append("    " + r["name"] + ": " + "; ".join(
                f"{v}: portfolio {r[v]['portfolio_best'] and r[v]['portfolio_best']['n_ok']}/{len(r[v]['portfolio'])} ok, "
                f"random {r[v]['random_best'] and r[v]['random_best']['n_ok']}/{len(r[v]['random'])} ok, "
                f"first error: {next((e.get('error') for e in r[v]['portfolio'] + r[v]['random'] if not e.get('ok')), '-')}"
                for v in VARIANTS))
        for name in failed_modules[:10]:
            lines.append("    failed module " + name + ": " + next(r["failed"] for r in rows if r["name"] == name))
    if nu and common:
        m = out["mechanism_plain"] = {}
        for key in ("ic", "text"):
            oz = sum(r["plain"]["oz"][key] for r in nu)
            n = sum(r["plain"]["oz_nounroll"][key] for r in nu)
            a = sum(r["attr"]["oz"][key] for r in nu)
            m[key] = {"oz_plain": oz, "oz_plain_nounroll": n, "oz_attr": a}
            lines.append(f"  mechanism ({key}): Oz(plain) {oz} -> -disable-loop-unrolling {n} "
                         f"({100 * (oz - n) / oz:+.1f}%) vs Oz(attr) {a} ({100 * (oz - a) / oz:+.1f}%)")
    cross = {}
    for key in (("ic", "text") if common else ()):
        a = sum(r["plain"]["portfolio_best"]["by_ic"][key] for r in common)
        b = sum(r["attr"]["oz"][key] for r in common)
        w = sum(r["plain"]["portfolio_best"]["by_ic"][key] < r["attr"]["oz"][key] for r in common)
        t = sum(r["plain"]["portfolio_best"]["by_ic"][key] == r["attr"]["oz"][key] for r in common)
        cross[key] = {"portfolio_plain": a, "oz_attr": b, "wtl": f"{w}/{t}/{len(common) - w - t}"}
        lines.append(f"  cross-check ({key}): paper-protocol portfolio {a} vs attribute-correct Oz {b} "
                     f"({100 * (b - a) / b:+.1f}%, W/T/L {w}/{t}/{len(common) - w - t})")
    out["cross_check"] = cross
    infl = sum(r["plain"]["oz"]["text"] > r["plain"]["o0"]["text"] for r in common) if common else 0
    infl_a = sum(r["attr"]["oz"]["text"] > r["attr"]["o0"]["text"] for r in common) if common else 0
    out["oz_text_above_o0"] = {"plain": infl, "attr": infl_a}
    lines.append(f"  modules where Oz text > O0 text: plain {infl}, attr {infl_a} (of {len(common)})")
    if print_rows:
        print("\n".join(lines))
    return out


# ------------------------------------------------------------------ main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bitcode-dir")
    p.add_argument("--suite", default="")
    p.add_argument("--llvm-bin", default=os.environ.get("LLVM_BIN", "/opt/homebrew/opt/llvm@18/bin"))
    p.add_argument("--pm", choices=["new", "legacy"], default="new")
    p.add_argument("--ic-tool", default=os.path.join(REPO, "scripts", "baseline_audit", "ic"))
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    p.add_argument("--limit", type=int, default=0, help="only the first N modules (smoke test)")
    p.add_argument("--only", default="", help="comma-separated module names to run")
    p.add_argument("--passes", default=os.path.join(REPO, "configs", "passes.yaml"))
    p.add_argument("--portfolio", default=os.path.join(REPO, "results", "portfolio_selection.json"))
    p.add_argument("--out", default="")
    p.add_argument("--summarize", default="", help="print the summary of an existing output file")
    args = p.parse_args()

    if args.summarize:
        data = json.load(open(args.summarize))
        summarize(data)
        return

    if not args.bitcode_dir:
        p.error("--bitcode-dir is required")
    if not os.path.exists(args.ic_tool):
        sys.exit(f"instruction counter not found at {args.ic_tool}; build scripts/baseline_audit/ic.cpp first")
    names = load_pass_names(args.passes)
    CFG.update({"llvm_bin": args.llvm_bin, "pm": args.pm, "ic_tool": args.ic_tool, "k": args.k,
                "seed": args.seed, "portfolio": load_portfolio(args.portfolio, names, args.k),
                "pass_list": [names[i] for i in sorted(names)]})
    version = run([tool("opt"), "--version"]).stdout.strip().splitlines()
    version = next((l.strip() for l in version if "version" in l), "?")
    bcs = sorted(glob.glob(os.path.join(args.bitcode_dir, "*.bc")),
                 key=lambda q: (len(os.path.basename(q)), os.path.basename(q)))
    if args.only:
        keep = set(args.only.split(","))
        bcs = [b for b in bcs if os.path.basename(b)[:-3] in keep]
    if args.limit:
        bcs = bcs[:args.limit]
    suite = args.suite or os.path.basename(os.path.normpath(args.bitcode_dir))
    print(f"{suite}: {len(bcs)} modules, {version}, pm={args.pm}, k={args.k}, workers={args.workers}", flush=True)
    with ProcessPoolExecutor(args.workers, initializer=_init_worker, initargs=(dict(CFG),)) as ex:
        records = list(ex.map(one, bcs))
    data = {"suite": suite, "timestamp": datetime.now().isoformat(), "llvm_version": version,
            "llvm_bin": args.llvm_bin, "pm": args.pm, "k": args.k, "seed": args.seed,
            "attribute_method": "llvm-dis; add 'minsize optsize' to every 'attributes #N = {' group"
                                " (attr_fp: also \"frame-pointer\"=\"all\" -> \"none\"); llvm-as",
            "oz_command": ("opt -Oz" if args.pm == "legacy" else "opt -passes='default<Oz>'"),
            "sequence_command": ("opt <legacy pass flags>" if args.pm == "legacy"
                                 else "opt -passes=<llvm18_transfer.pipeline_text(seq)>"),
            "size_command": "llc -filetype=obj; llvm-size (Berkeley text) and llvm-size -A (.text* sections)",
            "ic_command": "scripts/baseline_audit/ic (LLVM API instruction count)",
            "portfolio": CFG["portfolio"], "records": records}
    out = args.out or os.path.join(REPO, "results", "baseline_audit", f"{suite}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(data, f, indent=1)
    data["summary"] = summarize(data)
    with open(out, "w") as f:
        json.dump(data, f, indent=1)
    print(f"-> {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Does `opt -Oz` on attribute-corrected IR reproduce a real `clang -Oz` build?

CHStone ships as C sources inside CompilerGym's dataset cache, so each
program can be compiled both ways with the bundled LLVM 10 toolchain:

  real       clang -Oz -c main.c                    (a real size build)
  cgym_attr  clang -Oz -Xclang -disable-llvm-passes -Xclang -disable-llvm-optzns
             (unoptimized IR carrying clang's own -Oz attributes) -> opt -Oz
  plain      the environment's module (ClangInvocation: -O1 with passes
             disabled) -> opt -Oz                    (this paper's protocol)
  attr       the environment's module + minsize optsize (textual) -> opt -Oz
  attr_fp    attr + "frame-pointer"="none"

Sizes come from llc + llvm-size of the same LLVM 10; IC from the ic tool.
Run inside the CompilerGym environment:
  python scripts/baseline_audit_clang.py --out results/baseline_audit/llvm10/chstone_clang_oz.json
"""

import argparse
import glob
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime

import compiler_gym
from compiler_gym.envs.llvm.llvm_benchmark import get_system_library_flags

LLVM_BIN = os.path.expanduser("~/.local/share/compiler_gym/llvm-v0/bin")
CHSTONE_MAIN = {"blowfish": "bf.c", "motion": "mpeg2.c", "sha": "sha_driver.c", "jpeg": "main.c"}


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(f"{os.path.basename(cmd[0])}: " + r.stderr.strip()[-200:])
    return r


def tool(name):
    return os.path.join(LLVM_BIN, name)


def sizes(obj):
    out = run([tool("llvm-size"), obj]).stdout.strip().splitlines()[1].split()
    sec = 0
    for line in run([tool("llvm-size"), "-A", obj]).stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and (p[0] in (".text", "__text") or p[0].startswith(".text.")):
            sec += int(p[1])
    return {"text": int(out[0]), "text_sec": sec}


def ic_of(bc):
    r = subprocess.run(["ic", bc], capture_output=True, text=True)
    return int(r.stdout.strip()) if r.returncode == 0 else None


def measure_bc(bc, wd, tag):
    obj = os.path.join(wd, tag + ".o")
    run([tool("llc"), "-filetype=obj", "-o", obj, bc])
    return {"ic": ic_of(bc), **sizes(obj)}


def opt_oz(in_bc, out_bc):
    run([tool("opt"), "-Oz", in_bc, "-o", out_bc])


def with_attributes(in_bc, out_bc, frame_pointer_none=False):
    ll = run([tool("llvm-dis"), in_bc, "-o", "-"]).stdout
    ll = re.sub(r"^(attributes #\d+ = \{)", r"\1 minsize optsize", ll, flags=re.M)
    if frame_pointer_none:
        ll = ll.replace('"frame-pointer"="all"', '"frame-pointer"="none"')
    r = subprocess.run([tool("llvm-as"), "-o", out_bc], input=ll, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError("llvm-as: " + r.stderr[-200:])


def attr_group_0(bc):
    ll = run([tool("llvm-dis"), bc, "-o", "-"]).stdout
    m = re.search(r"^attributes #0 = \{([^}]*)\}", ll, flags=re.M)
    return " ".join(t for t in m.group(1).split() if not t.startswith('"') or "frame-pointer" in t) if m else "?"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="results/baseline_audit/llvm10/chstone_clang_oz.json")
    args = p.parse_args()
    env = compiler_gym.make("llvm-v0")
    ds = env.datasets["benchmark://chstone-v0"]
    ds.install()
    root = glob.glob(os.path.join(str(ds.site_data_path), "contents", "patmos_HLS-*", "benchmarks", "CHStone"))[0]
    sys_flags = get_system_library_flags()
    clang = tool("clang")
    records = []
    print(f"{'program':<9} {'real clang -Oz':>16} {'cgym-attrs IR':>14} {'plain':>10} {'attr':>10} {'attr_fp':>10}   (.text bytes; IC in brackets)")
    for uri in ds.benchmark_uris():
        name = uri.split("/")[-1]
        src = os.path.join(root, name, CHSTONE_MAIN.get(name, f"{name}.c"))
        rec = {"uri": uri, "source": src}
        with tempfile.TemporaryDirectory() as wd:
            try:
                # real size build
                obj = os.path.join(wd, "real.o")
                run([clang, "-Oz", "-c", *sys_flags, src, "-o", obj])
                bc = os.path.join(wd, "real.bc")
                run([clang, "-Oz", "-c", "-emit-llvm", *sys_flags, src, "-o", bc])
                rec["real"] = {"ic": ic_of(bc), **sizes(obj)}
                # clang's own -Oz attributes, optimizer disabled, then opt -Oz
                cg = os.path.join(wd, "cgattr.bc")
                run([clang, "-Oz", "-Xclang", "-disable-llvm-passes", "-Xclang", "-disable-llvm-optzns",
                     "-c", "-emit-llvm", *sys_flags, src, "-o", cg])
                rec["clang_oz_attributes"] = attr_group_0(cg)
                cgo = os.path.join(wd, "cgattr_oz.bc")
                opt_oz(cg, cgo)
                rec["cgym_attr"] = measure_bc(cgo, wd, "cgattr")
                # the environment's module (paper protocol) and its corrected variants
                env.reset(benchmark=uri)
                plain = os.path.join(wd, "plain.bc")
                env.write_bitcode(plain)
                rec["env_attributes"] = attr_group_0(plain)
                rec["o0_ic"] = int(env.observation["IrInstructionCount"])
                rec["cgym_oz_ic"] = int(env.observation["IrInstructionCountOz"])
                variants = {"plain": plain}
                a = os.path.join(wd, "attr.bc")
                with_attributes(plain, a)
                variants["attr"] = a
                f = os.path.join(wd, "attr_fp.bc")
                with_attributes(plain, f, frame_pointer_none=True)
                variants["attr_fp"] = f
                for v, path in variants.items():
                    o = os.path.join(wd, v + "_oz.bc")
                    opt_oz(path, o)
                    rec[v] = measure_bc(o, wd, v)
            except Exception as e:
                rec["failed"] = repr(e)[:300]
                print(f"{name:<9} FAILED {rec['failed']}")
                records.append(rec)
                continue
        records.append(rec)
        print(f"{name:<9} {rec['real']['text_sec']:>8} [{rec['real']['ic']:>5}] {rec['cgym_attr']['text_sec']:>7} [{rec['cgym_attr']['ic']:>5}] "
              f"{rec['plain']['text_sec']:>5} [{rec['plain']['ic']:>4}] {rec['attr']['text_sec']:>5} [{rec['attr']['ic']:>4}] "
              f"{rec['attr_fp']['text_sec']:>5} [{rec['attr_fp']['ic']:>4}]", flush=True)
    env.close()
    ok = [r for r in records if "failed" not in r]
    tot = {k: sum(r[k]["text_sec"] for r in ok) for k in ("real", "cgym_attr", "plain", "attr", "attr_fp")}
    tot_ic = {k: sum(r[k]["ic"] for r in ok) for k in ("real", "cgym_attr", "plain", "attr", "attr_fp")}
    print("totals .text:", tot)
    print("totals IC:   ", tot_ic)
    print("attributes: env =", ok[0]["env_attributes"] if ok else "?")
    print("            clang -Oz =", ok[0]["clang_oz_attributes"] if ok else "?")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump({"timestamp": datetime.now().isoformat(), "compiler_gym": compiler_gym.__version__,
                   "llvm_bin": LLVM_BIN, "system_flags": sys_flags, "totals_text_sec": tot,
                   "totals_ic": tot_ic, "records": records}, fh, indent=1)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()

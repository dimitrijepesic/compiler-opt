#!/usr/bin/env python3
"""
Confirm the -Oz baseline artifact inside the original environment
(CompilerGym 0.2.5, LLVM 10): for each benchmark URI, read the
environment's own IrInstructionCountOz on the shipped bitcode and on the
same bitcode with `minsize optsize` added to every function attribute
group (loaded back through a file:// benchmark). Also re-measures both
with the bundled LLVM 10 `opt -Oz` + `llc` + `llvm-size`, so the numbers
line up with scripts/baseline_audit.py.

Run inside the CompilerGym environment:
  python scripts/baseline_audit_cgym.py benchmark://npb-v0/116 benchmark://npb-v0/94 \
      --out results/baseline_audit/llvm10/cgym_confirmation.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime

import compiler_gym

LLVM_BIN = os.path.expanduser("~/.local/share/compiler_gym/llvm-v0/bin")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def tool(name):
    return os.path.join(LLVM_BIN, name)


def with_attributes(in_bc, out_bc, frame_pointer_none=False):
    ll = run([tool("llvm-dis"), in_bc, "-o", "-"]).stdout
    ll, n = re.subn(r"^(attributes #\d+ = \{)", r"\1 minsize optsize", ll, flags=re.M)
    if frame_pointer_none:
        ll = ll.replace('"frame-pointer"="all"', '"frame-pointer"="none"')
    r = subprocess.run([tool("llvm-as"), "-o", out_bc], input=ll, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-200:])
    return n


def sizes(bc, wd):
    obj = os.path.join(wd, "o.o")
    r = run([tool("llc"), "-filetype=obj", "-o", obj, bc])
    if r.returncode:
        raise RuntimeError("llc: " + r.stderr[-200:])
    out = run([tool("llvm-size"), obj]).stdout.strip().splitlines()[1].split()
    sec = 0
    for line in run([tool("llvm-size"), "-A", obj]).stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and (p[0] in (".text", "__text") or p[0].startswith(".text.")):
            sec += int(p[1])
    return {"text": int(out[0]), "text_sec": sec}


def opt_oz(in_bc, out_bc, extra=()):
    r = run([tool("opt"), "-Oz", *extra, in_bc, "-o", out_bc])
    if r.returncode:
        raise RuntimeError("opt: " + r.stderr[-200:])


def ic_of(bc):
    r = run(["ic", bc])
    return int(r.stdout.strip()) if r.returncode == 0 else None


def measure_uri(env, uri, wd):
    env.reset(benchmark=uri)
    rec = {"uri": uri, "o0_ic": int(env.observation["IrInstructionCount"]),
           "cgym_oz_ic": int(env.observation["IrInstructionCountOz"]),
           "cgym_o3_ic": int(env.observation["IrInstructionCountO3"])}
    plain = os.path.join(wd, "plain.bc")
    env.write_bitcode(plain)
    variants = {"plain": plain}
    attr = os.path.join(wd, "attr.bc")
    rec["attribute_groups"] = with_attributes(plain, attr)
    variants["attr"] = attr
    fp = os.path.join(wd, "attr_fp.bc")
    with_attributes(plain, fp, frame_pointer_none=True)
    variants["attr_fp"] = fp
    for name, bc in variants.items():
        d = rec[name] = {}
        if name != "plain":
            env.reset(benchmark=f"file://{os.path.abspath(bc)}")
            d["cgym_o0_ic"] = int(env.observation["IrInstructionCount"])
            d["cgym_oz_ic"] = int(env.observation["IrInstructionCountOz"])
        oz = os.path.join(wd, f"{name}_oz.bc")
        opt_oz(bc, oz)
        d["opt_oz"] = {"ic": ic_of(oz), **sizes(oz, wd)}
        d["o0"] = {"ic": ic_of(bc), **sizes(bc, wd)}
        if name == "plain":
            nu = os.path.join(wd, "nounroll.bc")
            try:
                opt_oz(bc, nu, extra=("-disable-loop-unrolling",))
                d["opt_oz_nounroll"] = {"ic": ic_of(nu), **sizes(nu, wd)}
            except RuntimeError as e:
                d["opt_oz_nounroll"] = {"error": str(e)}
    return rec


def main():
    p = argparse.ArgumentParser()
    p.add_argument("uris", nargs="+")
    p.add_argument("--out", default="results/baseline_audit/llvm10/cgym_confirmation.json")
    args = p.parse_args()
    env = compiler_gym.make("llvm-v0")
    version = run([tool("opt"), "--version"]).stdout.strip().splitlines()
    records = []
    try:
        for uri in args.uris:
            with tempfile.TemporaryDirectory() as wd:
                try:
                    rec = measure_uri(env, uri, wd)
                except Exception as e:
                    rec = {"uri": uri, "failed": repr(e)[:300]}
                    try:
                        env.close()
                    except Exception:
                        pass
                    env = compiler_gym.make("llvm-v0")
            records.append(rec)
            if "failed" in rec:
                print(f"{uri}: FAILED {rec['failed']}", flush=True)
                continue
            a, f = rec["attr"], rec["attr_fp"]
            print(f"{uri}: O0 IC {rec['o0_ic']} | cgym Oz IC plain {rec['cgym_oz_ic']} -> attr {a['cgym_oz_ic']} "
                  f"| opt -Oz IC plain {rec['plain']['opt_oz']['ic']} nounroll "
                  f"{rec['plain'].get('opt_oz_nounroll', {}).get('ic')} attr {a['opt_oz']['ic']} "
                  f"| text plain {rec['plain']['opt_oz']['text']} attr {a['opt_oz']['text']} attr_fp {f['opt_oz']['text']} "
                  f"| .text plain {rec['plain']['opt_oz']['text_sec']} attr {a['opt_oz']['text_sec']}", flush=True)
    finally:
        env.close()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump({"timestamp": datetime.now().isoformat(), "compiler_gym": compiler_gym.__version__,
                   "llvm_version": version, "llvm_bin": LLVM_BIN, "records": records}, fh, indent=1)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()

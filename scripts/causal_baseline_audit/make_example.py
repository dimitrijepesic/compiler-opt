#!/usr/bin/env python3
"""Small example for the paper: one function of npb-v0/116, extracted unchanged.

Takes the canonical service input of npb-v0/116 saved by the pilot, extracts
one function with LLVM 10.0.0 `llvm-extract` (no edit of its body), and runs
the same four reference cells (original service; input-level unroll.disable
marking), the replica cross-check and the code generation control on that
one-function module. Also reports the size of the same function inside the
full-module objects of the pilot, and runs a fixed-vector behaviour check of
every object variant against a C driver. Run inside the `causal-audit`
container:

  python scripts/causal_baseline_audit/make_example.py [--function transfb_nc0]
"""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import compiler_gym  # noqa: E402
import run_audit as R  # noqa: E402
from run_audit import LLVM, add_attributes, atomic_json, command, digest  # noqa: E402

LLVM10 = Path("/opt/llvm10/bin")  # same 10.0.0 release archive the service links
PILOT = R.OUT / "pilot/artifacts/npb-v0_116"

DRIVER = r"""
// Fixed-vector behaviour check for transfb_nc0 (not a proof of equivalence).
// r_init and qbnew are external to the extracted function in the original
// module as well; their definitions here are written for this test only.
#include <stdio.h>
#include <string.h>
double qbnew[2][5][3];
void r_init(double *a, int n, double v) { for (int i = 0; i < n; ++i) a[i] = v; }
void transfb_nc0(double *tmor, double *tx);
int main(void) {
  double tmor[25], tx[25];
  unsigned long long s = 88172645463325252ULL;
  for (int round = 0; round < 4; ++round) {
    for (int i = 0; i < 25; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; tmor[i] = (double)(s % 2000003) / 977.0 - 1000.0; }
    for (int i = 0; i < 25; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; tx[i] = (double)(s % 1000003) / 313.0 - 1500.0; }
    for (int i = 0; i < 30; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; ((double *)qbnew)[i] = (double)(s % 500009) / 127.0 - 2000.0; }
    transfb_nc0(tmor, tx);
    for (int i = 0; i < 25; ++i) { unsigned long long b; memcpy(&b, &tmor[i], 8); printf("%d %d %016llx\n", round, i, b); }
  }
  return 0;
}
"""


def body(ll, fn):
    m = re.search(rf"^define [^\n]*@{re.escape(fn)}\(.*?^}}$", ll, re.M | re.S)
    if not m:
        raise AssertionError(f"{fn} not found")
    text = re.sub(r" #\d+", "", m.group(0))  # attribute group numbers differ between modules
    return re.sub(r"!llvm\.loop !\d+", "!llvm.loop", text)  # and so do loop id node numbers


def symbol_sizes(obj):
    sizes = {}
    for line in command([LLVM10 / "llvm-nm", "--print-size", "--defined-only", obj]).splitlines():
        p = line.split()
        if len(p) == 4 and p[2] in "Tt":
            sizes[p[3]] = int(p[1], 16)
    return sizes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--function", default="transfb_nc0")
    args = ap.parse_args()
    fn = args.function
    out = R.OUT / f"example_npb116_{fn}"
    if out.exists():
        raise SystemExit(f"{out} exists; refusing to overwrite")
    out.mkdir(parents=True)
    commands = []

    def run(argv, **kw):
        commands.append(" ".join(str(a) for a in argv))
        return command(argv, **kw)

    result = {"function": fn, "source_module": "benchmark://npb-v0/116", "source_input": str((PILOT / "plain.bc").relative_to(R.ROOT)),
              "source_input_sha256": digest(PILOT / "plain.bc"), "llvm_extract": str(LLVM10 / "llvm-extract"),
              "note": "The original C source of this CompilerGym module is not available; nothing here is reconstructed C."}

    plain = out / "plain.bc"
    run([LLVM10 / "llvm-extract", f"-func={fn}", PILOT / "plain.bc", "-o", plain])
    run([LLVM / "opt", "-verify", plain, "-disable-output"])
    result["extraction_body_identical_to_full_module"] = body(R.dis(plain), fn) == body((PILOT / "plain.ll").read_text(), fn)
    attr = out / "attr.bc"
    add_attributes(plain, attr)
    commands.append("add_attributes(plain.bc, attr.bc)  # scripts/baseline_audit_cgym_matrix.py")

    cells = result["cells"] = {}
    with compiler_gym.make("llvm-v0") as env:
        for v, src in (("plain", plain), ("attr", attr)):
            (out / f"{v}.ll").write_text(R.dis(src))
            marked = out / f"{v}-marked.bc"
            R.run_replica(src, marked, "--mark-unroll-disable", f"--stats={out / (v + '-marked.stats.json')}")
            commands.append(f"replica_oz --mark-unroll-disable {v}.bc {v}-marked.bc")
            (out / f"{v}-marked.ll").write_text(R.dis(marked))
            for cell, inp in (("service_original", src), ("service_marked", marked)):
                unique = out / f"input-{digest(inp)}.bc"
                shutil.copyfile(inp, unique)
                env.reset(benchmark=unique.as_uri())
                oz = int(env.observation["IrInstructionCountOz"])
                o0 = int(env.observation["IrInstructionCount"])
                env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                dst = out / f"{v}-{cell}.bc"
                env.write_bitcode(str(dst))
                commands.append(f'service: reset(file://{unique.name}); send_param("llvm.apply_baseline_optimizations","-Oz"); write_bitcode({dst.name})')
                d = cells[f"{v}/{cell}"] = {"observation_o0": o0, "observation_oz": oz, **R.full_measure(dst, out, dst)}
                assert d["ic"] == oz
                unique.unlink()
            for cell, (which, mode) in R.REPLICA_CELLS.items():
                inp = src if which == "input" else marked
                dst = out / f"{v}-{cell}.bc"
                n, err = R.run_replica(inp, dst, mode, "--remarks", f"--stats={out / (v + '-' + cell + '.stats.json')}")
                commands.append(f"replica_oz {mode} --remarks --stats=... {inp.name} {dst.name}")
                (out / f"{v}-{cell}.remarks.txt").write_text(err)
                stats = json.loads((out / f"{v}-{cell}.stats.json").read_text())
                cells[f"{v}/{cell}"] = {"unroll_remarks": R.parse_remarks(err), **R.full_measure(dst, out, dst),
                                       "function_before": next(f for f in stats["before"]["functions"] if f["name"] == fn),
                                       "function_after": next(f for f in stats["after"]["functions"] if f["name"] == fn)}
    controls = result["codegen_control"] = {}
    for name, base, f in (("plain_oz_late_attr", "plain-service_original", add_attributes),
                          ("plain_marked_oz_late_attr", "plain-service_marked", add_attributes),
                          ("attr_oz_stripped", "attr-service_original", R.remove_size_attributes)):
        dst = out / f"control-{name}.bc"
        f(out / f"{base}.bc", dst)
        controls[name] = {"base": base, **R.full_measure(dst, out, dst),
                          "ir_identical_modulo_size_attrs": R.normalize_size_attrs(R.dis(out / f"{base}.bc")) == R.normalize_size_attrs(R.dis(dst))}
    (out / "measurement.o").unlink()

    checks = result["checks"] = {}
    for v in ("plain", "attr"):
        checks[f"{v}/replica_service_reproduces_service_ir"] = cells[f"{v}/replica_service"]["ir_sha256"] == cells[f"{v}/service_original"]["ir_sha256"]
        checks[f"{v}/replica_service_marked_reproduces_service_ir"] = cells[f"{v}/replica_service_marked"]["ir_sha256"] == cells[f"{v}/service_marked"]["ir_sha256"]
        checks[f"{v}/marked_no_unroll_remarks"] = cells[f"{v}/replica_service_marked"]["unroll_remarks"]["total"] == 0
    checks["U_ir_equals_A_modulo_size_attrs"] = cells["plain/service_marked"]["ir_nosize_sha256"] == cells["attr/service_original"]["ir_nosize_sha256"]
    # Is the function optimized the same way alone and inside the full module?
    for cell in ("plain-service_original", "plain-service_marked", "attr-service_original", "attr-service_marked"):
        checks[f"{cell}_function_body_same_as_in_full_module"] = \
            body((out / f"{cell}.ll").read_text(), fn) == body((PILOT / f"{cell}.ll").read_text(), fn)

    # Function size inside the FULL module objects of the pilot, and in the example objects.
    result["function_bytes"] = {"full_module_pilot": {}, "example": {}}
    for label in ("plain-service_original", "plain-service_marked", "attr-service_original", "attr-service_marked",
                  "control-plain_oz_late_attr", "control-plain_marked_oz_late_attr", "control-attr_oz_stripped"):
        result["function_bytes"]["full_module_pilot"][label] = symbol_sizes(PILOT / f"{label}.o").get(fn)
        result["function_bytes"]["example"][label] = symbol_sizes(out / f"{label}.o").get(fn)
    result["function_bytes"]["all_functions_full_module"] = {
        label: symbol_sizes(PILOT / f"{label}.o") for label in ("plain-service_original", "plain-service_marked", "attr-service_original")}

    # Shape of the function in each cell.
    shape = result["shape"] = {}
    for label in ("plain", "plain-service_original", "plain-service_marked", "attr-service_original"):
        text = body((out / f"{label}.ll").read_text(), fn)
        shape[label] = {"fmul": len(re.findall(r"= fmul ", text)), "store": len(re.findall(r"^\s+store ", text, re.M)),
                        "conditional_branches": len(re.findall(r"^\s+br i1 ", text, re.M)),
                        "basic_blocks": 1 + len(re.findall(r"^[\w.]+:", text, re.M))}

    # Behaviour on fixed vectors: every object variant linked with the same driver.
    (out / "driver.c").write_text(DRIVER)
    outputs = {}
    for obj in sorted(out.glob("*.o")):
        exe = out / (obj.stem + ".test")
        run(["clang-14", "-O0", "-no-pie", out / "driver.c", obj, "-o", exe])
        outputs[obj.name] = subprocess.run([str(exe)], capture_output=True, text=True, timeout=60, check=True).stdout
        exe.unlink()
    reference = outputs["plain.o"] if "plain.o" in outputs else None
    if reference is None:  # unoptimized input as the behavioural reference
        obj = out / "plain.o"
        run([LLVM / "llc", "-filetype=obj", plain, "-o", obj])
        exe = out / "plain.test"
        run(["clang-14", "-O0", "-no-pie", out / "driver.c", obj, "-o", exe])
        reference = subprocess.run([str(exe)], capture_output=True, text=True, timeout=60, check=True).stdout
        exe.unlink()
    (out / "behaviour_reference_output.txt").write_text(reference)
    result["behaviour"] = {"reference": "unoptimized extracted input (plain.o)", "lines": len(reference.splitlines()),
                           "reference_sha256": R.sha(reference),
                           "variants_identical_to_reference": {k: v == reference for k, v in outputs.items()},
                           "scope": "4 pseudo-random fixed input vectors, bit-exact comparison of all 25 outputs; not a proof of semantic equivalence"}
    checks["behaviour_all_variants_identical"] = all(result["behaviour"]["variants_identical_to_reference"].values())
    result["commands"] = commands
    result["files_sha256"] = {p.name: digest(p) for p in sorted(out.iterdir()) if p.is_file()}
    atomic_json(out / "example.json", result)
    summary = {k: {m: c[m] for m in ("ic", "text_sec", "text")} for k, c in cells.items()}
    print(json.dumps({"cells": summary, "controls": {k: {m: c[m] for m in ("ic", "text_sec", "text")} for k, c in controls.items()},
                      "checks": checks, "shape": shape, "function_bytes": {k: v for k, v in result["function_bytes"].items() if k != "all_functions_full_module"}}, indent=1))


if __name__ == "__main__":
    main()

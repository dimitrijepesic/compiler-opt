#!/usr/bin/env python3
"""Recompile the published example through the original service in a fresh directory."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/causal_baseline_audit"))
import run_audit as audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "tmp/reproduce-example")
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        raise SystemExit(f"Refusing to overwrite {out}; choose a new --out directory.")
    out.mkdir(parents=True)
    source = ROOT / "results/causal_baseline_audit/example_npb116_transfb_nc0"
    expected = json.loads((source / "example.json").read_text())
    plain = out / "plain.bc"
    shutil.copyfile(source / "plain.bc", plain)
    assert audit.digest(plain) == expected["files_sha256"]["plain.bc"]
    assert audit.digest(audit.SERVICE) == "60178fbf497cb79f01aa567dc16765d04579dd88b3137e47769b5757067d37ee"
    # Initializing an environment also installs the bundled LLVM tools if needed.
    with audit.compiler_gym.make("llvm-v0") as env:
        attr, marked = out / "attr.bc", out / "marked.bc"
        audit.add_attributes(plain, attr)
        audit.run_replica(plain, marked, "--mark-unroll-disable")
        result = {"input_sha256": audit.digest(plain), "service_sha256": audit.digest(audit.SERVICE),
                  "compiler_gym": audit.compiler_gym.__version__, "cells": {}}
        paths = {}
        for label, inp, key in [("P", plain, "plain/service_original"),
                                 ("U", marked, "plain/service_marked"),
                                 ("A", attr, "attr/service_original")]:
            unique = out / (audit.digest(inp) + ".bc")
            shutil.copyfile(inp, unique)
            env.reset(benchmark=unique.as_uri())
            reference_ic = int(env.observation["IrInstructionCountOz"])
            env.send_param("llvm.apply_baseline_optimizations", "-Oz")
            dst = out / (label + ".bc")
            env.write_bitcode(str(dst))
            measured = audit.full_measure(dst, out, dst)
            assert measured["ic"] == reference_ic == expected["cells"][key]["ic"]
            for metric in ("ic", "text_sec", "text", "ir_sha256"):
                assert measured[metric] == expected["cells"][key][metric], (label, metric)
            result["cells"][label] = measured
            paths[label] = dst
        late = out / "U-plus.bc"
        audit.add_attributes(paths["U"], late)
        result["cells"]["U+"] = audit.full_measure(late, out, late)
        control = expected["codegen_control"]["plain_marked_oz_late_attr"]
        for metric in ("ic", "text_sec", "text", "ir_sha256"):
            assert result["cells"]["U+"][metric] == control[metric], metric
        paths["U+"] = late

    outputs = {}
    for label, bc in {"O0": plain, **paths}.items():
        obj = out / (label + "-test.o")
        exe = out / (label + "-test")
        audit.command([audit.LLVM / "llc", "-filetype=obj", bc, "-o", obj])
        audit.command(["/opt/llvm10/bin/clang", "-O0", "-no-pie", source / "driver.c", obj, "-o", exe])
        outputs[label] = audit.command([exe])
    assert len(set(outputs.values())) == 1, "Fixed-vector behavior differs"
    result["fixed_vector_outputs_equal"] = True
    result["output_sha256"] = hashlib.sha256(outputs["O0"].encode()).hexdigest()
    result["scope"] = "Fresh service execution; recorded IR and size agreement; fixed-vector regression only."
    (out / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Case   IR instructions   Code-section bytes")
    for name, cell in result["cells"].items():
        print(f"{name:4} {cell['ic']:17} {cell['text_sec']:20}")
    print("PASS: saved IR and sizes reproduced; all fixed-vector outputs agree.")


if __name__ == "__main__":
    main()

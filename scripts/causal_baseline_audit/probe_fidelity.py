#!/usr/bin/env python3
"""Phase 1 probe: does the replica reproduce the original service -Oz output?

Exploratory, kept as evidence. Run inside the `causal-audit` container:
  python scripts/causal_baseline_audit/probe_fidelity.py OUT_DIR URI [URI...]
For every URI and for the plain/attr inputs it stores the service -Oz export,
the replica output in every mode, the input with llvm.loop.unroll.disable on
every loop, and the ORIGINAL service -Oz on that marked input.
"""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import compiler_gym

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baseline_audit_cgym_matrix import LLVM, add_attributes, command, digest, ic, ir_digest  # noqa: E402


def dis(path):
    ll = command([LLVM / "llvm-dis", path, "-o", "-"])
    return re.sub(r"^; ModuleID = .*\n", "", ll, count=1)


def replica(src, dst, *flags):
    p = subprocess.run(["replica_oz", *flags, str(src), str(dst)], capture_output=True, text=True, timeout=600)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    return int(p.stdout.strip()), p.stderr


def main():
    out = Path(sys.argv[1]).resolve()
    result = {}
    with compiler_gym.make("llvm-v0") as env:
        for uri in sys.argv[2:]:
            wd = out / uri.split("//")[1].replace("/", "_")
            wd.mkdir(parents=True, exist_ok=True)
            env.reset(benchmark=uri)
            r = result[uri] = {"o0": int(env.observation["IrInstructionCount"]),
                               "oz": int(env.observation["IrInstructionCountOz"])}
            plain = wd / "plain.bc"
            env.write_bitcode(str(plain))
            attr = wd / "attr.bc"
            add_attributes(plain, attr)
            for variant, src in (("plain", plain), ("attr", attr)):
                d = r[variant] = {}
                # Marked copy: llvm.loop.unroll.disable on every natural loop of the input.
                marked = wd / f"{variant}-marked.bc"
                _, _ = replica(src, marked, "--mark-unroll-disable", f"--stats={wd / (variant + '-marked.stats.json')}")
                d["marked_loops"] = json.loads((wd / f"{variant}-marked.stats.json").read_text())["marked_loops"]
                for label, inp in (("service", src), ("service_marked", marked)):
                    unique = wd / f"input-{digest(inp)}.bc"
                    unique.write_bytes(inp.read_bytes())
                    env.reset(benchmark=unique.as_uri())
                    loaded = wd / f"{variant}-{label}-loaded.bc"
                    env.write_bitcode(str(loaded))
                    d[f"{label}_load_ir_identical"] = ir_digest(loaded) == ir_digest(inp)
                    oz_obs = int(env.observation["IrInstructionCountOz"])
                    env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                    svc = wd / f"{variant}-{label}-oz.bc"
                    env.write_bitcode(str(svc))
                    assert ic(svc) == oz_obs, (ic(svc), oz_obs)
                    d[label] = {"ic": oz_obs, "ir": ir_digest(svc)}
                    (wd / f"{variant}-{label}-oz.ll").write_text(dis(svc))
                for mode in ("service", "disable-unroll", "unroll-threshold-0"):
                    dst = wd / f"{variant}-replica-{mode}.bc"
                    n, err = replica(src, dst, f"--mode={mode}", "--remarks")
                    (wd / f"{variant}-replica-{mode}.remarks.txt").write_text(err)
                    (wd / f"{variant}-replica-{mode}.ll").write_text(dis(dst))
                    d[f"replica_{mode}"] = {"ic": n, "ir": ir_digest(dst),
                                            "unroll_remarks": sum(l.startswith("remark\t") for l in err.splitlines())}
                dst = wd / f"{variant}-replica-service-on-marked.bc"
                n, err = replica(marked, dst, "--mode=service", "--remarks")
                (wd / f"{variant}-replica-service-on-marked.remarks.txt").write_text(err)
                d["replica_service_on_marked"] = {"ic": n, "ir": ir_digest(dst),
                                                  "unroll_remarks": sum(l.startswith("remark\t") for l in err.splitlines())}
                d["replica_reproduces_service_ir"] = d["replica_service"]["ir"] == d["service"]["ir"]
                d["replica_reproduces_service_marked_ir"] = d["replica_service_on_marked"]["ir"] == d["service_marked"]["ir"]
            print(uri, json.dumps(r, indent=1), flush=True)
    (out / "probe.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()

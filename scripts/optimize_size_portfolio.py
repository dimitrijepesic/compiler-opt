#!/usr/bin/env python3
"""Apply a frozen portfolio and return the smallest measured code section.

LLVM 10 / CompilerGym 0.2.5 demonstrator. Both the service -Oz reference and
portfolio receive definition-level minsize/optsize attributes. Preserves the
input target and frame-pointer policy. This is not a full clang -Oz build.
Outputs every measured candidate and the selected .bc/.o pair for inspection.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tempfile

import compiler_gym
import yaml

import baseline_audit_cgym_matrix as audit


def optimize(benchmark, bitcode, out, k):
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"Output directory is not empty: {out}")
    out.mkdir(parents=True, exist_ok=True)
    portfolio_path = audit.ROOT / "results/portfolio_selection.json"
    portfolio = json.loads(portfolio_path.read_text())["portfolio"][:k]
    assert len(portfolio) == k
    pass_names = {p["action_id"]: p["name"] for p in yaml.safe_load(
        (audit.ROOT / "configs/passes.yaml").read_text())["passes"]}
    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "benchmark": benchmark, "bitcode_input": str(bitcode) if bitcode else None,
              "script_sha256": audit.digest(__file__), "helper_sha256": audit.digest(audit.__file__),
              "portfolio_sha256": audit.digest(portfolio_path), "portfolio_k": k,
              "compiler_gym": compiler_gym.__version__,
              "llvm_version": audit.command([audit.LLVM / "opt", "--version"]),
              "selection": "minimum pure code-section bytes; baseline wins ties; then earlier rank",
              "baseline": "service -Oz on canonical input with minsize/optsize",
              "target": "unchanged from input; default llc code generation",
              "candidates": []}
    with tempfile.TemporaryDirectory(prefix="size-portfolio-") as temp, compiler_gym.make("llvm-v0") as env:
        wd = Path(temp)
        if bitcode:
            src = wd / (audit.digest(bitcode) + ".bc")
            shutil.copyfile(bitcode, src)
            uri = src.as_uri()
        else:
            uri = benchmark
        env.reset(benchmark=uri)
        plain = out / "input_canonical.bc"
        env.write_bitcode(str(plain))
        report["original_o0_ic"] = int(env.observation["IrInstructionCount"])
        report["original_oz_ic"] = int(env.observation["IrInstructionCountOz"])
        annotated = out / "input_size_attributes.bc"
        report["attribute_info"] = audit.add_attributes(plain, annotated)
        unique = wd / (audit.digest(annotated) + ".bc")
        shutil.copyfile(annotated, unique)
        env.reset(benchmark=unique.as_uri())
        assert int(env.observation["IrInstructionCount"]) == report["original_o0_ic"]
        loaded = wd / "loaded.bc"
        env.write_bitcode(str(loaded))
        assert audit.ir_digest(loaded) == audit.ir_digest(unique)
        for action, name in pass_names.items():
            assert env.action_space.flags[action] == name
        for i in range(k + 1):
            env.reset(benchmark=unique.as_uri())
            expected_oz = int(env.observation["IrInstructionCountOz"])
            label = "oz" if i == 0 else f"portfolio_{i}"
            actions = None if i == 0 else portfolio[i-1]["actions"]
            if i == 0:
                env.send_param("llvm.apply_baseline_optimizations", "-Oz")
            else:
                assert all(action in pass_names for action in actions)
                _, _, done, info = env.multistep(actions, timeout=120)
                if done:
                    raise RuntimeError(f"Candidate {label} ended early: {info}")
            bc = out / f"{label}.bc"
            metrics = audit.export_measure(env, bc, wd)
            if i == 0:
                assert metrics["ic"] == expected_oz
            obj = out / f"{label}.o"
            shutil.copyfile(wd / "measurement.o", obj)
            assert audit.digest(obj) == metrics["object_sha256"]
            report["candidates"].append({"label": label, "actions": actions, **metrics})
            print(f'{label}: IC {metrics["ic"]}, code bytes {metrics["text_sec"]}', flush=True)
    candidates = report["candidates"]
    index, chosen = min(enumerate(candidates), key=lambda x: (x[1]["text_sec"], x[0]))
    baseline = candidates[0]
    report["selected"] = chosen["label"]
    report["code_bytes_saved"] = baseline["text_sec"] - chosen["text_sec"]
    report["code_gain_pct"] = 100 * report["code_bytes_saved"] / baseline["text_sec"]
    report["candidate_optimizations"] = k + 1
    report["candidate_codegen_measurements"] = k + 1
    for suffix in ("bc", "o"):
        shutil.copyfile(out / f'{chosen["label"]}.{suffix}', out / f"selected.{suffix}")
    assert audit.digest(out / "selected.o") == chosen["object_sha256"]
    audit.atomic_json(out / "selection.json", report)
    print(f'Selected {chosen["label"]}: {report["code_bytes_saved"]} bytes saved ({report["code_gain_pct"]:.2f}%)', flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--benchmark")
    src.add_argument("--bitcode", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--k", type=int, choices=range(1, 9), default=3)
    args = p.parse_args()
    optimize(args.benchmark, args.bitcode, args.out.resolve(), args.k)


if __name__ == "__main__":
    main()

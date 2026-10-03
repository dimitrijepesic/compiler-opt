#!/usr/bin/env python3
"""Check service/CLI size baselines against actual CHStone clang -Oz builds.

Keep full-object and pure-code hashes distinct: equal lengths do not prove
byte identity, and object metadata may differ even when code bytes match.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

import compiler_gym
from compiler_gym.envs.llvm.llvm_benchmark import get_system_library_flags

import baseline_audit_cgym_matrix as audit

MAIN = {"blowfish": "bf.c", "motion": "mpeg2.c", "sha": "sha_driver.c", "jpeg": "main.c"}


def object_metrics(obj, wd):
    code = wd / "code.bin"
    audit.command(["llvm-objcopy-14", f"--dump-section=.text={code}", obj, wd / "copy.o"])
    return {"object_sha256": audit.digest(obj), "code_sha256": audit.digest(code),
            "text_sec": code.stat().st_size,
            "text": int(audit.command([audit.LLVM / "llvm-size", obj]).splitlines()[1].split()[0])}


def bc_metrics(bc, wd):
    obj = wd / "generated.o"
    audit.command([audit.LLVM / "llc", "-filetype=obj", bc, "-o", obj])
    return {"ic": audit.ic(bc), "bitcode_sha256": audit.digest(bc), **object_metrics(obj, wd)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=audit.ROOT / "results/baseline_audit/llvm10_source_check")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    flags = list(get_system_library_flags())
    records = []
    with compiler_gym.make("llvm-v0") as env:
        ds = env.datasets["benchmark://chstone-v0"]
        ds.install()
        root = next(Path(ds.site_data_path).glob("contents/patmos_HLS-*/benchmarks/CHStone"))
        for uri in ds.benchmark_uris():
            name = uri.split("/")[-1]
            srcdir = root / name
            source = srcdir / MAIN.get(name, name + ".c")
            rec = {"uri": uri, "source": str(source),
                   "source_files": {str(f.relative_to(srcdir)): audit.digest(f)
                                    for f in sorted(srcdir.rglob("*")) if f.is_file()}}
            try:
                with tempfile.TemporaryDirectory(prefix="cgym-source-") as temp:
                    wd = Path(temp)
                    real, realbc = wd / "real.o", wd / "real.bc"
                    audit.command([audit.LLVM / "clang", "-Oz", "-c", *flags, source, "-o", real])
                    audit.command([audit.LLVM / "clang", "-Oz", "-c", "-emit-llvm", *flags, source, "-o", realbc])
                    rec["real_clang_oz"] = {"ic": audit.ic(realbc), **object_metrics(real, wd)}
                    front, optimized = wd / "frontend.bc", wd / "optimized.bc"
                    audit.command([audit.LLVM / "clang", "-Oz", "-Xclang", "-disable-llvm-passes",
                                   "-Xclang", "-disable-llvm-optzns", "-c", "-emit-llvm", *flags, source, "-o", front])
                    audit.command([audit.LLVM / "opt", "-Oz", front, "-o", optimized])
                    rec["clang_size_attributes_cli_oz"] = bc_metrics(optimized, wd)
                    env.reset(benchmark=uri)
                    plain, attr = wd / "plain.bc", wd / "attr.bc"
                    env.write_bitcode(str(plain))
                    rec["attribute_info"] = audit.add_attributes(plain, attr)
                    for variant, src in (("plain", plain), ("attr", attr)):
                        env.reset(benchmark=src.as_uri())  # unique temp directory per program
                        expected = int(env.observation["IrInstructionCountOz"])
                        env.send_param("llvm.apply_baseline_optimizations", "-Oz")
                        env.write_bitcode(str(optimized))
                        rec[variant + "_service_oz"] = bc_metrics(optimized, wd)
                        assert rec[variant + "_service_oz"]["ic"] == expected
                    audit.command([audit.LLVM / "opt", "-Oz", attr, "-o", optimized])
                    rec["attr_cli_oz"] = bc_metrics(optimized, wd)
                    a, b = rec["attr_cli_oz"], rec["clang_size_attributes_cli_oz"]
                    rec["manual_vs_frontend_attributes"] = {
                        "equal_ic": a["ic"] == b["ic"],
                        "equal_code_length": a["text_sec"] == b["text_sec"],
                        "identical_code_bytes": a["code_sha256"] == b["code_sha256"],
                        "identical_object_bytes": a["object_sha256"] == b["object_sha256"]}
            except Exception as e:
                rec["failed"] = repr(e)
            records.append(rec)
            audit.atomic_json(args.out / (name + ".json"), rec)
            print(name, rec.get("failed", rec.get("manual_vs_frontend_attributes")), flush=True)
    ok = [r for r in records if "failed" not in r]
    variants = ("real_clang_oz", "clang_size_attributes_cli_oz", "plain_service_oz", "attr_service_oz", "attr_cli_oz")
    result = {"timestamp": datetime.now(timezone.utc).isoformat(), "script_sha256": audit.digest(__file__),
              "helper_sha256": audit.digest(audit.__file__), "system_flags": flags,
              "compiler_gym": compiler_gym.__version__,
              "clang_version": audit.command([audit.LLVM / "clang", "--version"]),
              "section_extractor_version": audit.command(["llvm-objcopy-14", "--version"]),
              "attempted": len(records), "complete": len(ok),
              "totals": {v: {metric: sum(r[v][metric] for r in ok) for metric in ("ic", "text", "text_sec")}
                         for v in variants}, "records": records}
    audit.atomic_json(args.out / "summary.json", result)
    print(json.dumps(result["totals"], indent=2), flush=True)
    if len(ok) != len(records):
        raise SystemExit("Source check incomplete; inspect failures")


if __name__ == "__main__":
    main()

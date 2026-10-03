#!/usr/bin/env python3
"""Run CHStone's fixed self-tests for each candidate and a real clang -Oz build.

These input-vector tests are a bounded functional check, not a proof of
semantic equivalence or a runtime benchmark. Executed under amd64 emulation.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess

from compiler_gym.envs.llvm.llvm_benchmark import get_system_library_flags

import baseline_audit_cgym_matrix as audit
from optimize_size_portfolio import optimize
from check_cgym_source_baseline import object_metrics


def execute(path):
    r = subprocess.run([str(path)], capture_output=True, text=True, timeout=30)
    return {"exit_code": r.returncode, "stdout": r.stdout, "stderr": r.stderr,
            "executable_sha256": audit.digest(path)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=audit.ROOT / "results/size_portfolio_demo")
    p.add_argument("--all", action="store_true", help="Use all 12 CHStone source programs")
    args = p.parse_args()
    out = args.out.resolve()
    if (out / "functional_checks.json").exists():
        p.error("Existing validation report: choose a fresh --out directory")
    source_index = audit.ROOT / "results/baseline_audit/llvm10_source_check/summary.json"
    sources = json.loads(source_index.read_text())["records"]
    flags = list(get_system_library_flags())
    records = []
    names = [r["uri"].split("/")[-1] for r in sources] if args.all else ["adpcm", "aes", "gsm", "sha"]
    for name in names:
        old = next(r for r in sources if r["uri"].endswith("/" + name))
        src = Path(old["source"])
        rec = {"name": name, "uri": old["uri"], "source_sha256": audit.digest(src),
               "fixed_test_vectors": True, "tests": {}}
        try:
            for relative, expected in old["source_files"].items():
                assert audit.digest(src.parent / relative) == expected
            program_out = out / name
            optimize(old["uri"], None, program_out, 3)
            selection = json.loads((program_out / "selection.json").read_text())
            assert selection["candidates"][0]["text_sec"] == old["attr_service_oz"]["text_sec"]
            reference = program_out / "reference_clang_oz.elf"
            reference_obj = program_out / "reference_clang_oz.o"
            audit.command([audit.LLVM / "clang", "-Oz", "-c", *flags, src, "-o", reference_obj])
            rec["real_clang_oz_object"] = object_metrics(reference_obj, program_out)
            assert rec["real_clang_oz_object"]["text_sec"] == old["real_clang_oz"]["text_sec"]
            audit.command([audit.LLVM / "clang", "-no-pie", reference_obj, "-o", reference])
            rec["tests"]["real_clang_oz"] = execute(reference)
            for label in ("oz", "portfolio_1", "portfolio_2", "portfolio_3", "selected"):
                exe = program_out / f"{label}.elf"
                audit.command([audit.LLVM / "clang", "-no-pie", program_out / f"{label}.o", "-o", exe])
                rec["tests"][label] = execute(exe)
            # Real clang -Oz and three portfolio candidates are eligible.
            # Service -Oz is a separate diagnostic, not a fifth candidate.
            pool = [{"label": "reference_clang_oz", **rec["real_clang_oz_object"]}] + selection["candidates"][1:]
            _, chosen = min(enumerate(pool), key=lambda x: (x[1]["text_sec"], x[0]))
            shutil.copyfile(program_out / (chosen["label"] + ".o"), program_out / "source_selected.o")
            source_exe = program_out / "source_selected.elf"
            audit.command([audit.LLVM / "clang", "-no-pie", program_out / "source_selected.o", "-o", source_exe])
            rec["tests"]["source_selected"] = execute(source_exe)
            rec["source_selected"] = chosen["label"]
            rec["source_selected_code_bytes"] = chosen["text_sec"]
            rec["source_gain_pct"] = 100*(1-chosen["text_sec"]/rec["real_clang_oz_object"]["text_sec"])
            rec["source_eligible_candidates"] = 4
            rec["additional_service_baseline_diagnostic"] = 1
            reference_result = rec["tests"]["real_clang_oz"]
            assert reference_result["exit_code"] == 0, "Reference self-test failed"
            assert all(t["exit_code"] == 0 and t["stdout"] == reference_result["stdout"]
                       for t in rec["tests"].values()), "Candidate self-test failed or output differs"
            rec["selected"] = selection["selected"]
            rec["code_gain_pct_vs_service_oz"] = selection["code_gain_pct"]
            rec["baseline_code_bytes"] = selection["candidates"][0]["text_sec"]
            rec["selected_code_bytes"] = next(c["text_sec"] for c in selection["candidates"] if c["label"] == selection["selected"])
            rec["passed"] = True
        except Exception as e:
            rec["passed"] = False
            rec["error"] = repr(e)
        records.append(rec)
        audit.atomic_json(out / "functional_checks.json", {
            "script_sha256": audit.digest(__file__), "source_index_sha256": audit.digest(source_index),
            "system_flags": flags, "reference_compile_flags": ["-Oz", "-c"],
            "object_link_flags": ["-no-pie"], "execution": "amd64 container under Rosetta; no timing claim",
            "programs": records})
        print(name, "PASS" if rec["passed"] else rec["error"], flush=True)
    if not all(r["passed"] for r in records):
        raise SystemExit("Functional validation incomplete; see functional_checks.json")


if __name__ == "__main__":
    main()

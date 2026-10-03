#!/usr/bin/env python3
"""Measure already linked CHStone artifacts; no compilation or execution.

The primary selection is frozen: source_selected.elf was chosen using object
.text bytes. Read all 12 reference/selected pairs, verify their recorded
executable hashes and fixed-vector test results, and measure with llvm-size.
File bytes include ELF metadata/padding and exclude shared-library contents.
No new selector is fitted and no claim of total deployment footprint is made.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sizes(path, tool):
    berkeley = subprocess.run([str(tool), str(path)], check=True, text=True,
                              capture_output=True).stdout.splitlines()[1].split()
    sections = subprocess.run([str(tool), "-A", str(path)], check=True,
                              text=True, capture_output=True).stdout.splitlines()
    code = 0
    for line in sections:
        fields = line.split()
        if len(fields) >= 2 and (fields[0] == ".text" or fields[0].startswith(".text.")):
            code += int(fields[1])
    return {"text_section_bytes": code, "berkeley_text_bytes": int(berkeley[0]),
            "berkeley_data_bytes": int(berkeley[1]), "berkeley_bss_bytes": int(berkeley[2]),
            "file_bytes": path.stat().st_size, "sha256": sha(path)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=ROOT / "results/size_portfolio_source_check")
    p.add_argument("--out", type=Path, default=ROOT / "results/budgeted_selector_review/linked")
    p.add_argument("--llvm-size", type=Path,
                   default=Path.home() / ".local/share/compiler_gym/llvm-v0/bin/llvm-size")
    args = p.parse_args()
    report_path = args.source / "functional_checks.json"
    frozen = json.loads(report_path.read_text())
    assert sha(ROOT / "scripts/validate_size_portfolio_demo.py") == frozen["script_sha256"]
    assert sha(ROOT / "results/baseline_audit/llvm10_source_check/summary.json") == frozen["source_index_sha256"]
    assert len(frozen["programs"]) == len({x["name"] for x in frozen["programs"]}) == 12
    assert frozen["object_link_flags"] == ["-no-pie"]
    records = []
    for old in frozen["programs"]:
        assert old["passed"] and old["fixed_test_vectors"]
        directory = args.source / old["name"]
        artifacts = {}
        for label, stem in [("reference", "reference_clang_oz"), ("selected", "source_selected")]:
            test = old["tests"]["real_clang_oz" if label == "reference" else "source_selected"]
            assert test["exit_code"] == 0
            assert test["stdout"] == old["tests"]["real_clang_oz"]["stdout"]
            measured = sizes(directory / (stem + ".elf"), args.llvm_size)
            assert measured["sha256"] == test["executable_sha256"], (old["name"], stem)
            artifacts[label] = measured
        # Verify the original object-size selection and its attribution.
        ref_obj = sizes(directory / "reference_clang_oz.o", args.llvm_size)
        sel_obj = sizes(directory / "source_selected.o", args.llvm_size)
        assert ref_obj["sha256"] == old["real_clang_oz_object"]["object_sha256"]
        assert ref_obj["text_section_bytes"] == old["real_clang_oz_object"]["text_sec"]
        assert sel_obj["text_section_bytes"] == old["source_selected_code_bytes"]
        assert sel_obj["sha256"] == sha(directory / (old["source_selected"] + ".o"))
        records.append({"name": old["name"], "chosen_by_object_code": old["source_selected"],
                        **artifacts, "reference_object": ref_obj, "selected_object": sel_obj})
    summary = {}
    for metric in ("text_section_bytes", "berkeley_text_bytes", "berkeley_data_bytes",
                   "berkeley_bss_bytes", "file_bytes"):
        ref = sum(r["reference"][metric] for r in records)
        sel = sum(r["selected"][metric] for r in records)
        summary[metric] = {"reference_sum": ref, "selected_sum": sel, "saved_bytes": ref - sel,
                           "saving_pct": 100 * (ref - sel) / ref if ref else None,
                           "wtl": [sum(r["selected"][metric] < r["reference"][metric] for r in records),
                                   sum(r["selected"][metric] == r["reference"][metric] for r in records),
                                   sum(r["selected"][metric] > r["reference"][metric] for r in records)]}
    out = {"scope": __doc__, "script_sha256": sha(__file__), "input_sha256": sha(report_path),
           "llvm_size_sha256": sha(args.llvm_size), "object_link_flags": frozen["object_link_flags"],
           "records": records, "summary": summary}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
    lines = ["# Existing linked CHStone artifacts: independent size check", "",
             "All 24 ELF hashes match the previously executed fixed-vector checks. "
             "No compiler, linker or executable was run. Selection remains the frozen object-code rule.", "",
             "| Linked metric | Reference sum | Selected sum | Saving | W/T/L |",
             "|---|---:|---:|---:|---:|"]
    for metric, d in summary.items():
        gain = "n/a" if d["saving_pct"] is None else f'{d["saving_pct"]:.3f}%'
        lines.append(f'| {metric} | {d["reference_sum"]:,} | {d["selected_sum"]:,} | {gain} | '
                     + "/".join(map(str, d["wtl"])) + " |")
    lines.extend(["", "These are dynamically linked, unstripped x86-64 ELF files linked with -no-pie. "
                  "File bytes include metadata and padding; shared-library contents are not included. "
                  "The object-code fallback gives no guarantee for these linked metrics. "
                  "The existing fixed-vector checks are not a semantic proof or a runtime measurement.", "",
                  "Reproduce in the existing container:", "", "```sh",
                  "docker exec cgym-audit python scripts/audit_linked_selector.py", "```", ""])
    (args.out / "README.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

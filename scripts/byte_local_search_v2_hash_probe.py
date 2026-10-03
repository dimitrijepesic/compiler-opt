#!/usr/bin/env python3
"""Targeted replay of the start sequences whose hashes varied in the v2 pilot.

Diagnostic only: it re-executes existing frozen start sequences of
generator://csmith-v0/40 a few times from the same attributed input and
records which bitcode/object variants appear and how their IR differs. It
imports the frozen runner without modifying it and writes only to
results/byte_local_search_v2/hash_probe/ (refuses to overwrite).
Run inside the container:  python scripts/byte_local_search_v2_hash_probe.py
"""
import difflib
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import byte_local_search_v2 as B  # noqa: E402

URI = "generator://csmith-v0/40"
TARGETS = [("42", 7), ("44", 3)]          # (start, start index) reported by the pilot
REPEATS = 8
OUT = B.OUT_DEFAULT / "hash_probe"


def main():
    if OUT.exists():
        raise SystemExit(f"{OUT} exists: refusing to overwrite")
    manifest = B.load_json(B.OUT_DEFAULT / "manifest.json")
    prog = next(p for p in manifest["programs"] if p["uri"] == URI)
    cg = B.Cgym()
    audit, env = cg.audit, cg.env
    OUT.mkdir(parents=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="hash-probe-") as temp:
        wd = Path(temp)
        env.reset(benchmark=URI)
        plain, attr = wd / "plain.bc", wd / "attr.bc"
        env.write_bitcode(str(plain))
        audit.add_attributes(plain, attr)
        src = wd / f"input-attr-{B.digest(attr)}.bc"
        attr.rename(src)
        assert B.digest(src) == prog["identity"]["input_sha256"], "input differs from the frozen identity"
        for start, idx in TARGETS:
            actions = prog["starts"][start]["sequences"][idx]
            frozen = prog["starts"][start]["frozen_candidates"][idx]
            variants = {}
            for rep in range(REPEATS):
                env.reset(benchmark=src.as_uri())
                _, _, done, info = env.multistep([int(a) for a in actions], timeout=120)
                assert not done, info
                bc, obj = wd / "c.bc", wd / "c.o"
                env.write_bitcode(str(bc))
                m, _ = cg.measure_timed(bc, obj)
                ll = re.sub(r"^; ModuleID = .*\n", "", audit.command([audit.LLVM / "llvm-dis", bc, "-o", "-"]), count=1)
                key = (m["bitcode_sha256"], m["object_sha256"])
                if key not in variants:
                    name = f"s{start}_i{idx}_variant{len(variants)}"
                    (OUT / f"{name}.ll").write_text(ll)
                    variants[key] = {"name": name, "ir_sha256": B.sha_text(ll), "repeats": [], **m}
                variants[key]["repeats"].append(rep)
            vs = list(variants.values())
            diffs = {}
            for a in vs[1:]:
                d = list(difflib.unified_diff((OUT / f"{vs[0]['name']}.ll").read_text().splitlines(),
                                              (OUT / f"{a['name']}.ll").read_text().splitlines(), lineterm="", n=0))
                (OUT / f"{vs[0]['name']}_vs_{a['name']}.diff").write_text("\n".join(d) + "\n")
                diffs[a["name"]] = {"changed_lines": sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---")), "sample": d[:12]}
            results.append({"start": start, "start_index": idx, "repeats": REPEATS, "frozen": frozen,
                            "metrics_identical_across_variants": len({(v["ic"], v["text"], v["text_sec"]) for v in vs}) == 1,
                            "variants": vs, "frozen_variant": next((v["name"] for v in vs if v["object_sha256"] == frozen["object_sha256"]), None),
                            "ir_diff_vs_first_variant": diffs})
    cg.close()
    B.atomic_json(OUT / "results.json", {"uri": URI, "scope": "diagnostic replay of frozen start sequences; not part of the pilot budget or results",
                                         "manifest_fingerprint": manifest["fingerprint"], "targets": results})
    print(json.dumps([{k: (v if k != "variants" else [{x: w[x] for x in ("name", "repeats", "ic", "text", "text_sec")} for w in v])
                       for k, v in r.items() if k in ("start", "start_index", "metrics_identical_across_variants", "variants", "frozen_variant", "ir_diff_vs_first_variant")}
                      for r in results], indent=1))


if __name__ == "__main__":
    main()

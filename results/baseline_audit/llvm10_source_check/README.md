# CHStone source-build cross-check

All 12 of 12 source programs completed with bundled clang/LLVM 10.

| Build path | IC | Code bytes | Code bytes relative to real clang -Oz |
|---|---:|---:|---:|
| real_clang_oz | 9,062 | 32,123 | +0.00% |
| clang_size_attributes_cli_oz | 9,216 | 32,468 | +1.07% |
| plain_service_oz | 9,834 | 38,315 | +19.28% |
| attr_service_oz | 9,137 | 32,410 | +0.89% |
| attr_cli_oz | 9,216 | 32,468 | +1.07% |

## Identity and equivalence

All 12 programs have identical `.text` byte hashes between (1) canonical CompilerGym IR with manually added definition attributes followed by CLI `opt -Oz` and (2) IR emitted by clang with `-Oz` and LLVM passes disabled, followed by the same CLI `opt -Oz`. Full-object hashes differ for all 12. The recorded code hashes establish identity of section contents, not equivalence of all object contents or linked executables.

The attribute-controlled **service** baseline is only 0.89% above real clang -Oz in the pooled code-byte sum, but that does not imply per-program equivalence. GSM is 2,651 versus 2,350 bytes (+12.81%). Other differences include adpcm at -1.82% and jpeg at -1.20%. Source-level clang -Oz remains a separate reference.

## Reproduce

```sh
docker start cgym-audit
docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/check_cgym_source_baseline.py
```

The script records all source-directory file hashes, compiler/version flags, input/output hashes, and individual results. Only function definitions receive minsize/optsize, using the verified helper from baseline_audit_cgym_matrix.py. The environment service baseline is checked against its own IC observation. LLVM 14 objcopy is used solely to extract the `.text` bytes; all optimization and code generation use bundled LLVM 10.

No runtime or semantic-equivalence test is performed here. Measurements are relocatable objects, without whole-program linking or LTO. Earlier raw CLI matrices are a different protocol and must not be relabeled as this service result.

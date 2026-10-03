# CompilerGym service-path audit

This audit is separate from the raw-bitcode / `opt -Oz` matrices in
`../llvm10` and `../llvm18`. Those matrices are useful diagnostics, but do
not reproduce the original instruction-count evaluation path.

## Protocol

- CompilerGym 0.2.5, its bundled LLVM 10, amd64 container under Rosetta.
- Membership comes from the original per-program `results/battery` files,
  with the original policy evaluation's O0 IC cap of 6,000. NPB: 120;
  MiBench: 40; BLAS: 50. Above-cap records are listed in the manifest.
- Reset the original benchmark URI, export its canonical bitcode, and
  require O0 and Oz counts to match the original battery exactly.
- Add only `minsize optsize` to function definitions, including definitions
  without attribute groups. Preserve declarations, call-site attributes,
  target layout, triple and frame-pointer policy. Verify the resulting IR
  and check that every definition has both attributes.
- Use content-specific file URIs. CompilerGym caches benchmarks by URI;
  overwriting a file and reusing its URI can silently reuse old contents.
- Check complete disassembled IR identity when reloading, ignoring only
  the disassembler's path-derived `ModuleID` comment. Retain both bitcode
  hashes: llvm-as and the service can serialize identical IR differently.
- Apply the service's own `llvm.apply_baseline_optimizations=-Oz` and
  require its exported instruction count to match `IrInstructionCountOz`.
  Separately record CLI `opt -Oz` as a diagnostic, not as the reference.
- Execute the first eight existing portfolio sequences through service
  actions; require their original-condition ICs to match the saved
  portfolio results wherever available. A self-test checks that batched
  actions yield identical bitcode to individual `step` calls.
- Compare with eight new random 45-action sequences per program. Seed 42
  and a SHA-256-derived per-URI seed determine the draws. The exact same
  draws are used with and without attributes; every sequence is recorded.
  These are fresh draws, not reproduction of the old random-null samples.
- Both methods use the unchanged 36-action space. No retraining, portfolio
  reselection, or Oz fallback. Choose the final candidate with minimum IC
  (first candidate on ties) and report that candidate's bytes. Store
  selection by Berkeley text and by code-section size as separate controls.
- Generate objects with the bundled llc using the input's existing target.
  Record IC, Berkeley text, pure code-section size, and object/bitcode
  hashes for every candidate and baseline. These are object measurements,
  not linked executable size or runtime measurements.
- Save each program atomically. Resume only under an identical protocol,
  script, tool version, and input-reference fingerprint. Report all failures;
  primary totals use only programs with all eight candidates successful
  for both methods in both conditions.

`manifest.json` records actions, reference hashes, versions and membership.
`records/*.json` contain individual results. `summary.json` gives per-suite
and pooled totals, wins/ties/losses and completeness. Gains are reductions
in summed costs: `100 * (1 - candidate_sum / baseline_sum)`.

## Reproduction

In the existing container (substitute its name as necessary):

```sh
docker start cgym-audit
docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/baseline_audit_cgym_matrix.py --self-test

docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/baseline_audit_cgym_matrix.py \
  --suite npb-v0 --suite mibench-v1 --suite blas-v0 --workers 8 \
  --out results/baseline_audit/llvm10_canonical

docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/report_cgym_audit.py results/baseline_audit/llvm10_canonical
```

Smoke results live separately in `../llvm10_canonical_smoke_v2` and
`../llvm10_canonical_smoke_v3`. The interrupted first matrix attempt is
retained in `../validation_attempts/llvm10_canonical_attempt1`; it exposed the need to place
function attributes after LLVM address markers such as `local_unnamed_addr`.
The regression fixture now covers that syntax. Concurrent writers are
prevented with a directory lock.
`../validation_attempts/llvm10_canonical_smoke` retains a failed byte-identity assertion: this
led to comparing complete IR instead of demanding identical bitcode
serialization. Do not use that incomplete run for scientific totals.

## Interpretation limits

This isolates function size attributes in the original service protocol.
It does not establish full equivalence to a source-level `clang -Oz` build,
or test runtime, semantic correctness, ARM retargeting, learned policies,
other random seeds, or the rest of the battery. The portfolio was selected
on training programs without size attributes and is deliberately frozen.
NPB modules are correlated parts of a suite; program counts alone do not
establish independent replication or generalization to other projects.

The raw diagnostic matrices and this audit must not be pooled. For example,
on NPB/116 the original environment baseline is 4,316 IC, whereas CLI
`opt -Oz` on its canonical export gives 4,762; raw archive input gives
6,061. The old confirmation file already contains the first two numbers.

## Implementation sources

- [CompilerGym 0.2.5 baseline implementation](https://github.com/facebookresearch/CompilerGym/blob/v0.2.5/compiler_gym/envs/llvm/service/Cost.cc#L240-L260)
  constructs its own module and function pass managers; it is not a call
  to the standalone `opt -Oz` command.
- [Benchmark canonicalization](https://github.com/facebookresearch/CompilerGym/blob/v0.2.5/compiler_gym/envs/llvm/service/Benchmark.cc#L113-L125)
  strips debug information and named metadata on module creation.
- [Baseline service parameter](https://github.com/facebookresearch/CompilerGym/blob/v0.2.5/compiler_gym/envs/llvm/service/LlvmSession.cc#L198-L204)
  exposes the baseline implementation used in this audit.

## Source-build control

A separate [CHStone source-build check](../llvm10_source_check/README.md)
compares 12 actual clang -Oz builds with both the service and CLI baselines.
It records section-content hashes in addition to sizes; matching pooled
size alone is not evidence of per-program equivalence.

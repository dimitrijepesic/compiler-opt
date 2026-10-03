# Selector audit protocol (frozen before any new result was inspected)

Written 2026-09-17, before running the pilot. Independent verification in
`results/selector_audit_review/` (not touched).

## Question

Does the GNN policy generate better candidates than random search while
selection by IR instruction count (IC) fails to pass their advantage on to
code-section bytes? Design: generator {GNN, random} x selector {IC, code
bytes} on the same eight candidates per generator, program and seed or
replicate. The outcome may be positive, negative or inconclusive.

## Fixed scope

- Condition: `attr` only (minsize/optsize added to function definitions of
  the canonical CompilerGym service module by the unchanged helper
  `scripts/baseline_audit_cgym_matrix.py::add_attributes`).
- Environment: CompilerGym 0.2.5, bundled LLVM 10 service, `opt`, `llc`,
  `llvm-size`; the `ic` tool of the audit for instruction counts.
- Programs: the 347 of `results/gnn_attribute_audit/programs.json` (NPB 120,
  MiBench 40, BLAS 50, CHStone 12, csmith 28, POJ-104 97).
- No training, no policy sampling, no action-space change, no new
  benchmarks, no ARM, no LLVM 18, no TeX edits.

## Inputs

- GNN candidates: the stored `attr` action traces of the three from-scratch
  checkpoints (seeds 42, 123, 456). NPB exclusively from
  `results/gnn_attribute_audit/npb_offset78/records_gnn_seed*/` (120 per
  seed); the other five suites from
  `results/gnn_attribute_audit/records_gnn_seed*/` (227 per seed). 347 x 3
  x 8 = 8,328 candidates. Every trace must contain 45 steps with
  `success == 1` and `done == 0`; `--prepare` refuses otherwise.
- Random replicate 42: the stored `attr` candidates and metrics of
  `results/gnn_attribute_audit/records_null/` (2,776 candidates), reused
  with source file hashes; replayed and compared only in the pilot.
- Random replicates 43, 44, 45, 46: new sequences from
  `seed = int.from_bytes(sha256(f"{rep}:{uri}").digest()[:8], "big")`,
  `numpy.random.default_rng(seed).choice(sorted 36 action ids, size=(8, 45))`.
  `--prepare` checks that replicate 42 regenerates the stored actions of
  every program. 347 x 4 x 8 = 11,104 new candidates.
- Baseline: service `llvm.apply_baseline_optimizations=-Oz` on the
  attributed module, compared with the stored `attr.oz` of the null records.

## Per-program procedure

1. Reset the original benchmark URI; check O0/Oz against the battery.
2. Export the canonical module; add attributes; load through a
   content-hashed `file://` URI; check `ir_sha256`, `input_sha256`,
   attribute counts, unchanged O0, `IrInstructionCountOz`, and that the
   target triple and datalayout lines are identical before and after the
   attributes, all against the stored records.
3. Apply the service `-Oz`; export; measure; compare IC, Berkeley text,
   code section, bitcode and object hashes with the stored baseline.
4. For every GNN trace and every new random sequence: reset to the
   attributed input, apply the 45 action ids through the service (pilot:
   sequential `env.step`; campaign: `multistep` only if the pilot shows
   identical bitcode and object hashes on one GNN trace and one random
   sequence per pilot program), export the final module and measure IC
   (tool and environment), Berkeley `text`, code sections `text_sec`,
   bitcode and object SHA-256. Replayed IC must equal the stored IC of the
   trace; for the stored IC winner, bytes and hashes are compared too.
5. Record every failure, done flag, applied-step count and mismatch; never
   skip. Record replay, export and measurement times separately.
6. Atomic per-program JSON; resume skips finished records with the same
   fingerprint; a directory written under another fingerprint is refused.

## Selectors (all recomputed by the reporting script from the candidates)

1. `ic_first`: minimum IC, first candidate on ties (the paper's rule).
2. `code_first`: minimum code-section bytes, first candidate on ties.
Diagnostics: `ic_then_code` (IC, ties by code bytes, then first);
`berkeley_first`. Oz fallback only in a separately labelled table where the
baseline is an additional candidate; its no-regression property holds only
in the metric selected on. For every selected candidate all three metrics
are reported.

## Metrics (per suite, all, and without NPB)

Full sums; `gain = 100 (Oz - X) / Oz`; `GNN - random` as % of Oz; W/T/L vs
Oz and GNN vs random per program; median per-program relative saving;
selection regret `code(IC winner) - min(code(all 8))`; per-suite
contribution to the pooled saving. Every GNN seed against every random
replicate, plus mean and range over the four or five replicates (a range is
not a confidence interval). No p-values or bootstrap: modules of a suite
are not independent applications, three checkpoints and five replicates
are not fifteen independent experiments, and checkpoint inference was not
repeated, so GNN variance is not estimated.

## Common set

Primary tables use programs where every identity and baseline check
passed, all 24 GNN candidates replayed with IC equal to the stored IC and
all 40 random candidates are present (8 reused + 32 replayed). Every
excluded URI and the reason are listed with the full attempt counts. Fewer
than eight successful candidates is never called best-of-8.

## Pilot

The smallest and largest O0 IC program of each suite (URI lexicographic
tie-break): blas-v0/288, blas-v0/25, chstone-v0/mips, chstone-v0/aes,
csmith-v0/21, csmith-v0/40, mibench-v1/qsort1, mibench-v1/susan-e-2,
npb-v0/16, npb-v0/119, poj104-v1/54/59, poj104-v1/102/1409. The pilot
replays replicate 42 as well and runs the multistep equivalence check.
Results in `pilot/`, summary in `PILOT.md`. The campaign starts only if
every pilot check passes.

## Timing caveat

All runs are in an amd64 container under Rosetta 2 on an Apple M5 Pro.
GNN replay without the model is not GNN inference time; campaign wall time
with parallel workers is not a deployment latency.

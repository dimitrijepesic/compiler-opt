# Post-hoc diagnostic: what changes the reference when no loop is unrolled

Not part of the frozen matrix. Run after the campaign on eight programs
selected from its results: the six NPB programs where U (plain input,
unrolling switched off) does not have the IR of A (attr input), and the two
where switching unrolling off makes the code section larger. Script:
`scripts/causal_baseline_audit/probe_residual.py` (calls the unchanged
`run_audit.one()` with artifacts kept). All eight records pass every hard
check and repeat the campaign numbers. Artifacts: `artifacts/npb-v0_<n>/`.

## Residual IC difference (79 IC in total, all on programs without unrolling)

| Program | IC P = U | IC A | What differs in the service `-Oz` IR |
|---|---:|---:|---|
| npb-v0/3 | 248 | 238 | inliner: `ilog2` is inlined on plain, called once with `minsize` |
| npb-v0/30 | 1,831 | 1,831 | inliner: `AdcFileName` inlined on plain, 7 calls with `minsize`; IC happens to be equal |
| npb-v0/61 | 411 | 417 | inliner: `dcmplx_div` inlined and deleted on plain, kept and called with `minsize` (A is larger in IC) |
| npb-v0/66 | 1,064 | 1,005 | inliner: `setLeadingOnes32` (3 calls), `countTupleOnes`, `Mlo32` |
| npb-v0/4 | 624 | 615 | InstCombine under `minsize` removes the null test in front of `free` (`if (p) free(p)` -> `free(p)`) |
| npb-v0/29 | 1,004 | 997 | the same `free` transformation |

Found by diffing `plain-service_original.ll` against `attr-service_original.ll`
and by counting calls to functions defined in the module. The pass that
makes each change was read off the IR difference, not isolated by a pass
ablation.

## Unrolling that reduces machine code

npb-v0/34 (8 loops unrolled) and npb-v0/78 (2 loops): code section P 3,968 /
870, U 3,991 / 966, A 3,527 / 860. Full unrolling of these short
constant-trip-count loops increases IC (P > U in IC on both) while the
unrolled straight-line code is smaller than the loop once compiled without
size attributes. With the attributes (A) the loop version is the smallest.

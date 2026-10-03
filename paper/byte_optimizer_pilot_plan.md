# Pilot plan v2: byte-aware local search at a matched budget

Revised 2026-09-20 before any local-search pilot was run. The previous
proposal compared 24 candidates against eight and required a nonnegative
result outside NPB despite always keeping the baseline. Neither condition
demonstrates a better search algorithm. That proposal is superseded here.
This is an engineering pilot of standard local-search ingredients, not a
claim that local search or baseline fallback is new.

## Objective

Test whether byte-guided local mutations find smaller code than spending
the same compilation budget on fresh random sequences. The selected result
always includes the attributed service `-Oz` object. This only prevents
regression in the protected metric; it does not prove algorithmic value,
semantic correctness, faster execution, or a smaller linked executable.

## Frozen algorithm before the pilot

For each pilot program, use three paired random starts (replicates 42, 43,
44 of the frozen selector audit). Random initialization is primary because
the current evidence does not establish a byte-size advantage for GNNs.

1. Start with the eight recorded random sequences and the attributed `-Oz`
   baseline. Replay and measure all eight candidates using code-section
   bytes; match the frozen metrics before proceeding.
2. Keep the four smallest candidates by code-section bytes, breaking ties by
   original candidate index.
3. For two rounds, generate eight mutations from the four survivors:
   - four single-position replacements, with the replacement pass drawn from
     the fixed 36-pass action list using a URI-seeded generator;
   - two adjacent swaps;
   - one two-position replacement;
   - one replacement plus adjacent swap.
   Sequence length stays 45. Use parents 0,1,2,3 for the four replacements,
   parents 0,1 for the swaps, parent 2 for the double replacement, and parent
   3 for the combined mutation. Mutations are deterministic from
   `sha256("byte-local-v2:{seed}:{uri}:{round}:{parent}:{mutation}")`,
   first eight digest bytes as a big-endian integer for NumPy default_rng.
   Replacement positions are distinct and replacement passes differ from
   the original. An adjacent swap samples an unequal adjacent pair when
   available. Duplicate/ineffective candidates still consume an attempt;
   no free retries based on observed quality are allowed.
4. Measure every new sequence by native code-section bytes, add it to the
   pool, and retain the four smallest. The final answer is the smallest of the
   retained pool and `-Oz`.

For every program/start pair, run the matched control from the exact same
initial eight candidates: add 16 fresh uniformly random sequences of 45
actions, select by the same bytes, and include the same baseline. Generate
these with the same sorted action list and NumPy default_rng seeded from
`sha256("byte-random-control-v2:{seed}:{uri}")`, using the first eight bytes
as above. Both arms therefore spend 24 candidate attempts plus one baseline
measurement per run. Do not pool the seeds to give the method a larger
budget. The initial best-of-eight is only a secondary progress baseline.

Record the complete curve at 8, 16 and 24 attempts, per-candidate actions,
bytes, IC, failures, timing, and bitcode/object hashes. Replay from the same
attributed input through the original service. A failed candidate consumes
budget and cannot win; never drop its program from the reported denominator.
Pilot input/baseline mismatches block interpretation and must be fixed.
Initially do not cache across arms; distinguish accounting budget from
actual executions if shared initial measurements are reused for execution.

Keep a secondary version of the selection that also rejects any candidate
with Berkeley text above the reference, using the same measurements. Do not
switch the primary objective after viewing the outcome. GNN initialization
and more mutation types are optional follow-ups, not pilot rescue knobs.

## Pilot programs and go/no-go rule

Use the existing 12-program selector pilot: the smallest and largest O0
program from each of the six suites. This is an already examined development
set, not a fresh test set or a representative performance estimate. Freeze
the actual URI list, algorithm version and source hashes before execution.

Continue to a larger validation only if all conditions hold:

- The mean paired advantage over random-24, as a percentage of summed
  attributed `-Oz` bytes, is at least 0.5 percentage points across all three
  starts. This is a practical continuation threshold, not a significance test.
- That paired advantage is positive for at least two of the three starts.
- The mean paired advantage remains strictly positive after excluding NPB,
  with positive mean advantages in at least two non-NPB suites. Positivity
  against `-Oz` alone is not enough because the fallback supplies it.
- Every delivered result respects the declared metric constraint and all
  available selected-program functional checks pass. Report unchecked
  programs separately; fixed-vector checks do not prove equivalence.

If a criterion fails, stop this optimizer branch after reporting every
start and failure. Keep the corrected selector/audit manuscript. Do not tune
until the pilot looks good and then describe the same pilot as confirmation.

If it passes, freeze this algorithm before running the 347-program campaign.
Those programs have already informed the project, so label that campaign as
broader within-project validation. A claim of generalization additionally
needs a source-based cohort whose new search outcomes have not been inspected;
freeze its suite/version, inclusion rules, linking flags, tests and objective
before compiling. Compare both arms against actual source `clang -Oz` there.
Do not label an expanded subset of already inspected modules a new test set.

Measure end-to-end optimization wall time separately from executable runtime.
Rosetta measurements describe that host only. A native x86-64 run is needed
for claims about native optimization cost, and must include candidate
generation, baseline optimization, code generation and selection.

## Claims allowed if the full campaign passes

The paper may describe the implemented byte-aware optimizer and its measured
advantage over random search at the same budget, on the cohorts actually
tested. Any novelty claim requires a specific distinction from prior local
and evolutionary phase-ordering searches. The fallback property itself is
not novel. Report native candidate counts separately from wall time.

## Claims not allowed

Do not call the method globally optimal, do not claim GNN superiority, do not
generalize to linked executables or other LLVM versions, and do not use pilot
results as a final headline without the predeclared full-campaign rule.

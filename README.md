# Null Models and Sampling-Based Evaluation of Reinforcement Learning for LLVM Pass Ordering

Reinforcement learning for LLVM pass ordering (PPO with a flat Autophase
state vs. a GraphSAGE encoder over the program graph), measured against
random-search null models in the same 36-pass action space and evaluated
both by deterministic rollout and by best-of-k sampling. Paper source:
`paper/telfor_paper.tex` (TELFOR 2026).

> **Summary of the paper.** 880 programs from 11 independent sources,
> two null models in the curated 36-pass space, sampling-based (best-of-k)
> policy evaluation, and four controls (untrained policy, dropout-off,
> open-loop, fixed-portfolio). Best-of-50 random search in the curated
> space beats `-Oz` on all nine real-code sources (0.9-24.5%); the sampled
> GNN policy beats the budget-matched random null on 33/36 suite-seed
> totals (significant on 10/11 sources; Linux kernel code is the measured
> boundary) and matches greedy-search quality at 73% of its compilation
> budget in every seed. Best-of-8 sequences from the curated space, learned
> or random, give `.text` sections 10.6% smaller than `-Oz` on x86 (random
> null: 10.4%) and 14.9-15.0% smaller cross-compiled for a Cortex-M target
> (policy and null equal); the mined portfolio still beats LLVM 18's own
> `-Oz` by 10.6-10.9% when ported to its new pass manager, on 314 of 319
> attempted programs (`scripts/llvm18_transfer.py`, run under a separately
> installed LLVM 18 toolchain). Reproduce with `scripts/benchmark_battery.py`,
> `scripts/evaluate_policy_battery.py` (`--untrained/--no-dropout/`
> `--open-loop`), `scripts/mine_portfolio.py`,
> `scripts/measure_binary_metrics.py --mtriple`,
> `scripts/generate_battery_figure.py` (the paper's Fig. 1), and
> `scripts/compute_stats.py` (`--reframe/--controls/--e5`), which
> regenerates every number in the paper; `scripts/verify_paper_numbers.py`
> (or `pytest scripts/test_paper_numbers.py`) checks all of them against
> the tex source in one command, and `scripts/nullcheck.py` applies the
> same protocol (null models plus, optionally, a trained policy) to
> any CompilerGym benchmark set.
> The controlled two-representation comparison below is unchanged.

## Overview

This project trains reinforcement-learning agents to choose LLVM optimization
pass orderings that minimize IR instruction count (IC), and asks a specific
question under a controlled protocol:

> Does a GraphSAGE encoder over the program's control-flow + data-flow graph
> make PPO more data-efficient than the flat 56-dim Autophase feature vector?

**Answer, under this protocol: no.** The two representations are statistically
indistinguishable on both validation and test splits (Wilcoxon p = 0.63 / 0.88),
the GNN costs ~19× more wall-clock per environment step (17-23× per seed), and most of the
end-to-end IC reduction is attributable to the curated 36-pass action space
rather than to learning. An earlier version of this README claimed the
opposite; see [What changed and why](#what-changed-and-why).

## Controlled protocol

Everything that differs between the two agents is the state representation.

| Protocol element | Value (identical for both agents) |
|---|---|
| Training benchmarks | dijkstra, adpcm, bitcount, stringsearch (cBench-v1, O0 IC < 3000) |
| Budget | 100K env steps per seed |
| Seeds | 42, 123, 456 (3 per agent) |
| Checkpoint selection | val-small (crc32, qsort, stringsearch2) every 5K steps |
| Final evaluation | full validation split (5) + held-out test split (4), once, from best checkpoints |
| Action space | 36 passes (profiled subset of 124) |
| PPO | clip 0.2, GAE λ=0.95, γ=0.99, KL early-stop (target 0.02), entropy coeff 0.01→0.001 |

Null models measured in the same 36-pass space: a single random 45-step
episode (mean of 20), and best-of-50 random episodes.

## Results

Total IC, lower is better. `-O3`/`-Oz` are the **real** optimization levels
(CompilerGym `IrInstructionCountO3/Oz` observations), not hand-picked pass
lists. Agents report the median seed; mean ± std across seeds in parentheses.

| Method | Validation (5) | Test (4) |
|---|---|---|
| O0 | 111,758 | 120,684 |
| -O3 (real) | 77,853 | 85,981 |
| -Oz (real) | 55,412 | 60,575 |
| Random search, full 124-pass space (50×50) | 59,572 | 63,938 |
| Random single episode, 36-pass space | 56,229 | 62,436 |
| **Random search, 36-pass space (50×45)** | **52,725** | **58,281** |
| **Greedy search** | **52,481** | **58,069** |
| PPO + Autophase | 64,837 (73,922 ± 15,724) | 68,922 (76,040 ± 12,439) |
| PPO + GNN | 64,568 (64,550 ± 25) | 68,620 (69,180 ± 792) |

In-training validation (val-small; best per seed; nulls: Oz 643,
random-1-episode 640, greedy = random-50 604):

| Agent | seed 42 | seed 123 | seed 456 |
|---|---|---|---|
| PPO + Autophase | 685 | 681 | **629** |
| PPO + GNN | 689 | 689 | 689 |

### Findings

1. **The curated action space, not RL, does the heavy lifting.** Best-of-50
   random search inside the 36-pass space matches greedy search (within 0.5%)
   and beats -Oz by ~5% on both splits. A *single* random episode already
   roughly matches -Oz. The 36-pass profiling step distills most of the
   available signal.

2. **GNN is not more data-efficient: the representations are indistinguishable.**
   With identical data, budget, and PPO loop, per-benchmark ICs differ
   insignificantly (Wilcoxon p = 0.625 validation, p = 0.875 test). The GNN's
   striking seed-consistency (std 25 vs 15,724) is not learned structure: all
   three GNN seeds converge to the same near-uniform-policy plateau (689 on
   val-small, the same value a barely-trained policy reaches).

3. **Neither representation generalizes across program scale.** Trained on
   programs with < 3,000 instructions, both agents underperform even a single
   random 36-pass episode on the 50K-60K-instruction validation/test programs.
   A deterministic argmax rollout transfers a degenerate behavior; random
   sampling is more robust on out-of-scale inputs.

4. **Learning is possible but fragile.** With the fixed PPO loop
   (truncation-aware GAE, KL early-stop), Autophase seed 456 genuinely
   learned: 629 on val-small, beating -Oz (643) and the single-episode null
   (640), approaching greedy (604). One seed in three; no GNN seed did.

5. **-O3 is the wrong yardstick for code size.** On the three small validation
   programs real -O3 *increases* IC above O0 (1,608 vs 1,362, from inlining
   and unrolling). Any size result advertised as "beats -O3" should be read as
   "beats a speed-oriented baseline at a size game." The honest compiler
   baseline is -Oz, and no learned policy here beats it on the full splits.

6. **The GNN pays ~19× wall-clock per step** (17-23× per seed; 51-68 min vs
   3 min per 100K steps), dominated by IR→graph extraction, despite an
   on-disk graph cache.

### What changed and why

The original README reported that both agents "significantly outperform -O3"
(~50% vs ~48% reduction) and that the GNN "matches Autophase with 75% fewer
training steps." Re-examination showed: the "-O3" baseline was a hand-crafted
15-pass list; its own recorded value (644 on the 3-benchmark validation
subset) *beat* both agents (680/689); the agents' best scores were reached
within 10-40K steps, not at their nominal budgets; the two agents trained on
different benchmark sets; and the test split had never been evaluated. All
claims were re-derived from a controlled rerun with fixed code. The original
artifacts are preserved in `results/archive_2026-04_original/`.

Fixes applied before the rerun (all in this repo's history):

- **PPO**: GAE now bootstraps V(s_next) at truncations (episodes here never
  truly terminate) and no longer leaks advantages across episode boundaries at
  rollout cuts; KL-based epoch early stopping; linear entropy-coefficient
  decay; lower encoder learning rate for the GNN stack.
- **GNN**: edge-type-aware GraphSAGE (separate CFG/DFG convolutions per
  layer; `edge_type` was previously computed and ignored); node features
  extended with is-terminator / operand-count / defines-value / is-memory-op
  scalars; versioned graph cache.
- **Baselines**: real -O3/-Oz observations; random null models in the reduced
  action space; all baselines recorded per benchmark in
  `results/full_baselines_v2.json`.
- **Evaluation**: `scripts/evaluate_all.py` now actually runs (test split was
  previously never evaluated) and reports per-seed results, bootstrap CIs and
  a paired Wilcoxon test; `scripts/generate_figures.py` (referenced but
  missing before) exists.

## Figures

![Training curves](results/figures/fig1_training_curves.png)
![Validation curves](results/figures/fig2_validation_curves.png)
![Diagnostics](results/figures/fig3_entropy.png)
![Final comparison](results/figures/fig4_best_val_comparison.png)

## Repository structure

```
compiler-opt/
├── configs/
│   ├── benchmarks.yaml          # Fixed train/val/test split + val-small subset
│   ├── hyperparams.yaml         # Controlled-protocol hyperparameters
│   └── passes.yaml              # Reduced 36-pass action space
├── src/
│   ├── agents/ppo_autophase.py  # PPO + flat Autophase features
│   ├── agents/ppo_gnn.py        # PPO + GraphSAGE encoder
│   ├── agents/greedy.py, base_agent.py  # Used by scripts/demo_runner.py only
│   ├── features/autophase.py    # 56-dim feature extraction
│   ├── features/programl.py     # Custom LLVM IR → PyG graph parser + cache
│   └── models/                  # policy_mlp, value_head, gnn_encoder
├── legacy/                      # Pre-study prototypes, not part of the paper's
│                                 # pipeline; see legacy/README.md
├── demo/test.c                  # scripts/demo_runner.py: a two-minute demo
├── scripts/
│   ├── setup_wsl_env.sh         # One-time environment setup (WSL/Ubuntu 22.04)
│   ├── run_experiment.sh        # Full pipeline: baselines → training → eval → figures
│   ├── augment_baselines.py     # Real O3/Oz + random-in-reduced-space nulls
│   ├── train_ppo_autophase.py   # --seed N
│   ├── train_ppo_gnn.py         # --seed N [--init-encoder]
│   ├── pretrain_gnn.py          # Autophase-distillation pretraining of the encoder
│   ├── evaluate_all.py          # Final argmax eval: full val + test, stats
│   ├── evaluate_sampling.py     # Best-of-k sampling on cBench (k=8, k=32)
│   ├── benchmark_battery.py     # Null models on the 11-source battery
│   ├── evaluate_policy_battery.py  # Best-of-k policies on the battery (+ controls)
│   ├── mine_portfolio.py        # Fixed-portfolio control (greedy set cover)
│   ├── measure_binary_metrics.py   # .text/footprint/opt-time, --mtriple for ARM
│   ├── compute_stats.py         # Every statistic in the paper
│   ├── verify_paper_numbers.py, test_paper_numbers.py  # reproducibility check
│   ├── nullcheck.py             # apply the protocol to any CompilerGym suite
│   ├── llvm18_transfer.py       # portfolio ported to LLVM 18's new pass manager
│   ├── generate_battery_figure.py  # the paper's Fig. 1 (347-program battery)
│   └── generate_figures.py, generate_paper_figures.py  # cBench-only companion
├── data/                        # benchmark inventory, pass profiles
├── paper/                       # telfor_paper.tex, refs.bib, figures/
└── results/
    ├── full_baselines_v2.json   # cBench baselines incl. real O3/Oz + nulls
    ├── final_evaluation*.json   # Argmax results (controlled, mixed, pretrained)
    ├── sampling_evaluation*.json   # Best-of-8 / best-of-32 on cBench
    ├── battery/                 # Null models per source
    ├── battery_policy/          # Best-of-k policy runs per source, seed, variant
    ├── portfolio_eval/, binary_metrics/, binary_metrics_arm/
    ├── llvm18_transfer/         # Portfolio reapplied under LLVM 18
    ├── ppo_autophase/, ppo_gnn/, ppo_gnn_pretrained/  # Checkpoints + logs
    ├── figures/
    └── archive_2026-04_original/  # Pre-rerun artifacts, kept for provenance
```

## Reproduce

Linux (or WSL2 Ubuntu 22.04) required: CompilerGym 0.2.5 is Linux-only.

```bash
bash scripts/setup_wsl_env.sh     # venv + pinned deps + smoke test (~10 min)
bash scripts/run_experiment.sh    # baselines + 6 trainings + eval + figures
```

Wall-clock on a laptop CPU: baselines ~35 min, PPO+Autophase ~3 min/seed,
PPO+GNN ~50-70 min/seed, final evaluation ~15 min.

## Follow-up experiments (three tracks, run in parallel)

The controlled study left three open leads. All three were run; two changed
the conclusions materially.

### Track A: sampling evaluation (best-of-8) finds the GNN's first real win

Argmax rollouts measure a policy's *mode*; sampling measures its
*distribution*. Eight sampled rollouts per benchmark, best kept, against a
best-of-8 random null from the same 36-pass space:

| Best-of-8 totals | Validation (5) | Test (4) |
|---|---|---|
| Random null (best-of-8) | 53,539 | 58,717 |
| Greedy | 52,481 | 58,069 |
| PPO + Autophase (3 seeds) | 52,777 / 54,349 / 52,821 | 58,325 / 59,697 / 58,292 |
| **PPO + GNN (3 seeds)** | **52,748 / 52,731 / 52,670** | **58,065 / 58,210 / 57,943** |

Every GNN seed beats every Autophase seed on both splits, beats the null
6/6, decisively beats -Oz, and the best test seed **beats greedy search**
(57,943 vs 58,069) at roughly 5.5× fewer compilations (8×45 = 360 vs
greedy's measured ≈1,970 per program: (steps+1)×124 passes tried). The
"plateau" policies were good *samplers* with a degenerate mode.

### Track C: encoder pretraining breaks the plateau

Distilling Autophase into the encoder (regress log1p(Autophase) from the
graph; 2,430 states; val MSE 0.025) before RL fine-tuning:

- val-small best per seed: **651 / 668**, both below the 689 plateau that
  0/3 from-scratch seeds escaped;
- full-split argmax (best seed): validation **55,593**, test **61,015**,
  vs 64,550 / 69,180 from scratch. First argmax policy in the study to beat
  the single-episode random null on both splits, and within 0.3-0.8% of -Oz
  (mean over the two seeds: 57,980 / 63,229).

RL gradients alone could not train the encoder; a pretrained encoder + RL
can. The representation was never the bottleneck; encoder optimization was.

### Track B: mixed-size training does not fix scale generalization

Training on 9 benchmarks (O0 IC 450-15,184) instead of 4 tiny ones:
Autophase became *worse and less stable* (argmax validation totals 82,935 /
60,798 / 111,077). The GNN arm was rerun with three seeds under a
pre-registered protocol (`results/ppo_gnn_mixed_v2/PROTOCOL.md`: same
config, budget, seeds, checkpoint selection and evaluation; encoder and PPO
batches on the GPU with gradient accumulation). Mean argmax totals
**64,797 / 69,748** (validation / test) vs 64,550 / 69,180 from scratch,
per-benchmark one-sided Wilcoxon p = 0.41: by the decision rule, no
improvement. One seed (42) did improve both splits (60,211 / 65,239; 7 wins,
2 ties, 0 losses over the nine programs) and was the only run without
pretraining to leave the 689 val-small plateau (651); the other two seeds
regressed (69,250 / 73,028 and 64,931 / 70,977). Mixed-size training thus
reproduces the seed fragility the flat policy shows rather than fixing scale
generalization. Results: `results/final_evaluation_mixed_v2.json` (the
earlier single interrupted seed, 64,958 / 69,104, is kept in
`final_evaluation_mixed.json`).

### Revised conclusion

The graph representation is not the problem; measurement and optimization
were. Evaluate the policy as a sampler (Track A) or give the encoder a
pretrained start (Track C), and the GNN is the strongest agent in the
study; train on bigger programs (Track B) and the three-seed mean does not
move (one seed of three improves).
The data-efficiency claim stays dead; the amortized-search claim is now
alive and supported: 8 sampled rollouts from the GNN policy come within
0.4% of greedy quality at ~18% of greedy's compile cost, and 32 rollouts
match it at 73%.

## Limitations

- The objective is IR instruction count. Its correlation with `.text` size is
  validated only for programs above ~1,000 instructions (Pearson r = 0.78,
  n = 26 points from 13 programs); runtime is not measured.
- Training uses four small cBench programs by design (the experimental
  control). A three-seed mixed-size arm (Track B) did not improve
  generalization on average (one seed of three did); scaling training up
  further is left to future work.
- The GNN receives opcode-level features only (no value/type information, mean
  pooling); the encoder trains only after Autophase-distillation pretraining.
- The margin of the sampled GNN policy over the budget-matched random null is
  small in IC terms (0.7-2.8% of suite totals) and absent on Linux kernel
  code; in bytes, the learned policy and the random null are within 0.2% of
  each other on x86 and equal on the ARM target. The policy's value is as an
  amortized searcher (fewer compilations for the same quality), not as a
  source of large additional gains.
- The "24 of 24" suite-seed win count on the original battery is not robust to
  resampling on NPB (totals there are dominated by a few large programs); the
  per-suite Wilcoxon tests are the primary evidence.
- The stack is CompilerGym 0.2.5 / LLVM 10; the GNN costs ~19× more wall-clock
  per training step than the flat-feature agent. As a check against compiler
  drift, the mined portfolio was ported to LLVM 18's new pass manager (three
  of 36 passes approximated by their closest successor) and reapplied outside
  CompilerGym: it still beats LLVM 18's own `-Oz` by 10.6% (best-of-8) to
  10.9% (best-of-16) in `.text` bytes on 314 of 319 attempted programs from
  five suites (p < 1e-11). csmith is excluded: 20 of its 28 programs fail to
  compile at all under the ported sequences, a version-robustness boundary in
  its own right rather than a property of the curated space.

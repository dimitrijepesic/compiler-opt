# Track B rerun: pre-registered protocol

Written before the runs start (2026-08-30).

**Question.** Does training the GNN agent on nine mixed-size cBench
programs (O0 IC 450 to 15,184; `configs/hyperparams_mixed.yaml`) instead of
the four small ones (< 3,000) improve deterministic-rollout generalization
to the full validation (5) and test (4) splits?

**What changes vs. the paper's mixed arm.** Nothing in the protocol: same
config, budget (100K env steps), seeds (42, 123, 456), checkpoint selection
(val-small every 5K steps) and final evaluation (`scripts/evaluate_all.py`,
argmax, once, from the best checkpoint). The only differences are
engineering: the encoder and PPO batches run on the GPU, and each PPO batch
of 64 is processed as 8 micro-batches with gradient accumulation (the
gradient is the full-batch gradient up to floating-point order; checked
numerically to 2e-8 on a synthetic model). Run-to-run numerics differ from
a CPU run the way any two hardware backends differ; the seeds are kept so
the comparison is like-for-like in every other respect.

**Comparators.** From-scratch GNN (four small programs, 3 seeds): argmax
totals 64,550 (validation) / 69,180 (test), mean over seeds. Autophase
mixed arm (3 seeds, already complete): 82,935 / 60,798 / 111,077
(validation). The paper's single interrupted GNN mixed seed: 64,958 / 69,104.

**Decision rule.** The mixed arm "improves generalization" only if the
3-seed mean argmax total is lower than the from-scratch mean on BOTH
splits and the per-benchmark paired Wilcoxon (9 programs, one-sided) is
p < 0.05 on the pooled splits. Anything else is reported as "no
improvement" with the numbers, and the paper's current sentence
("a single-seed mixed-size arm did not improve generalization") is
replaced by the three-seed statement either way. Sampling (best-of-k)
evaluation of the mixed checkpoints is a secondary, separately reported
analysis, not part of this rule.

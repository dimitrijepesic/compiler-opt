# Legacy code

Early prototypes from before the project settled on the controlled PPO
study described in the paper: a genetic algorithm, a DQN agent, two
traditional-ML agents, a RISC-V cross-compilation validator, and the
hand-picked `-O3`/`-Oz` pass lists the paper's own "What changed and why"
section explicitly disowns.

None of this is imported by, or required to reproduce, anything in the
paper. It is kept for provenance, the way `results/archive_2026-04_original/`
keeps the pre-rerun results. Some scripts here (`run_ml_comparison.py`)
do not run as-is; they were already broken before being archived.

For the current pipeline, see the root `README.md`.

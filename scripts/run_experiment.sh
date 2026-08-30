#!/usr/bin/env bash
# Full controlled-experiment pipeline. Run inside WSL from the repo root:
#   bash scripts/run_experiment.sh
#
# Protocol (fixed before the run, see configs/hyperparams.yaml):
#   1. Augment baselines with real O3/Oz + random-in-reduced-space nulls
#   2. Train PPO+Autophase and PPO+GNN: SAME training set, SAME budget
#      (100K steps), 3 seeds each
#   3. Final evaluation on full validation + held-out test splits
#   4. Regenerate figures
set -euo pipefail
cd "$(dirname "$0")/.."

VENV="${VENV:-$HOME/venv-cgym}"
source "$VENV/bin/activate"

# Keep the graph cache off /mnt/c: many small files are slow over 9P
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"

mkdir -p results

echo "=== Step 1/4: augment baselines ==="
python scripts/augment_baselines.py 2>&1 | tee results/augment_baselines_log.txt

echo "=== Step 2/4: train agents (3 seeds each) ==="
for seed in 42 123 456; do
  python scripts/train_ppo_autophase.py --seed "$seed" 2>&1 \
    | tee "results/train_ap_seed${seed}_log.txt"
done
for seed in 42 123 456; do
  python scripts/train_ppo_gnn.py --seed "$seed" 2>&1 \
    | tee "results/train_gnn_seed${seed}_log.txt"
done

echo "=== Step 3/4: final evaluation ==="
python scripts/evaluate_all.py 2>&1 | tee results/final_evaluation_log.txt

echo "=== Step 4/4: figures ==="
python scripts/generate_figures.py

echo "=== DONE ==="

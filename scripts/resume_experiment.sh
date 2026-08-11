#!/usr/bin/env bash
# Resume the pipeline after interruption: only the missing GNN seed,
# then final evaluation and figures.
set -euo pipefail
cd "$(dirname "$0")/.."

VENV="${VENV:-$HOME/venv-cgym}"
source "$VENV/bin/activate"
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"

echo "=== Resume: train GNN seed 456 ==="
python scripts/train_ppo_gnn.py --seed 456 2>&1 \
  | tee "results/train_gnn_seed456_log.txt"

echo "=== Final evaluation ==="
python scripts/evaluate_all.py 2>&1 | tee results/final_evaluation_log.txt

echo "=== Figures ==="
python scripts/generate_figures.py

echo "=== RESUME-DONE ==="

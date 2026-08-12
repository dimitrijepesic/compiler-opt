#!/usr/bin/env bash
# Track C: Autophase-distillation pretraining, then RL fine-tune.
set -euo pipefail
cd "$(dirname "$0")/.."
source "${VENV:-$HOME/venv-cgym}/bin/activate"
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"

python scripts/pretrain_gnn.py

for seed in 42 123; do
  python scripts/train_ppo_gnn.py --seed "$seed" \
    --init-encoder results/gnn_pretrained/encoder.pt \
    --save-dir results/ppo_gnn_pretrained
done

python scripts/evaluate_all.py \
  --ppo-gnn-dir results/ppo_gnn_pretrained \
  --seeds 42 123 \
  --output results/final_evaluation_pretrained.json
echo "=== TRACK-C-DONE ==="

#!/usr/bin/env bash
# Track B: mixed-size training (9 benchmarks, O0 IC < 20000).
set -euo pipefail
cd "$(dirname "$0")/.."
source "${VENV:-$HOME/venv-cgym}/bin/activate"
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"

for seed in 42 123 456; do
  python scripts/train_ppo_autophase.py --seed "$seed" \
    --config configs/hyperparams_mixed.yaml \
    --save-dir results/ppo_autophase_mixed
done

for seed in 42 123; do
  python scripts/train_ppo_gnn.py --seed "$seed" \
    --config configs/hyperparams_mixed.yaml \
    --save-dir results/ppo_gnn_mixed
done

python scripts/evaluate_all.py \
  --ppo-ap-dir results/ppo_autophase_mixed \
  --ppo-gnn-dir results/ppo_gnn_mixed \
  --output results/final_evaluation_mixed.json
echo "=== TRACK-B-DONE ==="

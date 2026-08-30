#!/bin/bash
# Track B rerun: the mixed-size GNN arm with full statistical power.
#
# The original arm (results/ppo_gnn_mixed) is a single seed, interrupted at
# 90K/100K steps by a forced reboot, trained on the CPU at ~2.5 steps/s.
# This rerun trains all three seeds on the GPU (same config, same budget,
# same seeds as the controlled study) and evaluates them with the
# unchanged evaluate_all.py protocol. The Autophase mixed arm already has
# three complete seeds (results/ppo_autophase_mixed) and is reused as is.
#
# Resumable: a seed whose final checkpoint exists is skipped. Launch
# detached so a killed Windows-side wrapper cannot take it down:
#   wsl -d ubuntu-cgym -- bash -c 'setsid nohup bash \
#     /mnt/c/everything/projekti/compiler-opt/scripts/track_b_rerun.sh \
#     > /dev/null 2>&1 < /dev/null &'
cd "$(dirname "$0")/.."
source "${VENV:-$HOME/venv-cgym}/bin/activate"
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export COMPILER_OPT_MICRO_BATCH="${COMPILER_OPT_MICRO_BATCH:-8}"
OUT=results/ppo_gnn_mixed_v2
mkdir -p "$OUT"

for seed in 42 123 456; do
  if [ -f "$OUT/checkpoint_final_seed$seed.pt" ]; then
    echo "seed $seed already complete, skipping" >> "$OUT/rerun_log.txt"
    continue
  fi
  echo "=== $(date -Is) seed $seed start ===" >> "$OUT/rerun_log.txt"
  python -u scripts/train_ppo_gnn.py --seed "$seed" \
    --config configs/hyperparams_mixed.yaml --device cuda \
    --save-dir "$OUT" >> "$OUT/train_gnn_mixed_seed${seed}_log.txt" 2>&1
  echo "=== $(date -Is) seed $seed exit=$? ===" >> "$OUT/rerun_log.txt"
done

python -u scripts/evaluate_all.py \
  --ppo-ap-dir results/ppo_autophase_mixed \
  --ppo-gnn-dir "$OUT" \
  --output results/final_evaluation_mixed_v2.json \
  >> "$OUT/eval_log.txt" 2>&1
echo "=== $(date -Is) TRACK-B-RERUN-DONE exit=$? ===" >> "$OUT/rerun_log.txt"
touch "$OUT/DONE"

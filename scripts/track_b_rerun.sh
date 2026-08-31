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
# Up to three passes over the seeds: a seed whose final checkpoint exists
# is skipped, so a crashed seed (the CompilerGym service can be OOM-killed
# on long mixed-size runs) is retried on the next pass. The final
# evaluation runs only once all three seeds are complete. Launch detached
# so a killed Windows-side wrapper cannot take it down:
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

# The graph cache is rebuild-on-demand scratch, not a result: it grew by
# ~40 GB per seed and once filled the host disk. Purge it after every
# seed and after the final evaluation; everything worth keeping
# (checkpoints, logs, the evaluation JSON) lives in $OUT.
purge_cache() {
  du -sh "$COMPILER_OPT_CACHE_DIR" 2>/dev/null |     sed "s/^/=== $(date -Is) cache before purge: /" >> "$OUT/rerun_log.txt"
  rm -rf "$COMPILER_OPT_CACHE_DIR"
  mkdir -p "$COMPILER_OPT_CACHE_DIR"
}

for pass in 1 2 3; do
  for seed in 42 123 456; do
    if [ -f "$OUT/checkpoint_final_seed$seed.pt" ]; then
      continue
    fi
    echo "=== $(date -Is) pass $pass seed $seed start ===" >> "$OUT/rerun_log.txt"
    python -u scripts/train_ppo_gnn.py --seed "$seed" \
      --config configs/hyperparams_mixed.yaml --device cuda \
      --save-dir "$OUT" >> "$OUT/train_gnn_mixed_seed${seed}_log.txt" 2>&1
    rc=$?
    echo "=== $(date -Is) pass $pass seed $seed exit=$rc ===" >> "$OUT/rerun_log.txt"
    purge_cache
  done
done

if [ -f "$OUT/checkpoint_final_seed42.pt" ] \
   && [ -f "$OUT/checkpoint_final_seed123.pt" ] \
   && [ -f "$OUT/checkpoint_final_seed456.pt" ]; then
  python -u scripts/evaluate_all.py \
    --ppo-ap-dir results/ppo_autophase_mixed \
    --ppo-gnn-dir "$OUT" \
    --output results/final_evaluation_mixed_v2.json \
    >> "$OUT/eval_log.txt" 2>&1
  rc=$?
  echo "=== $(date -Is) TRACK-B-RERUN-DONE exit=$rc ===" >> "$OUT/rerun_log.txt"
  purge_cache
else
  echo "=== $(date -Is) TRACK-B-RERUN-INCOMPLETE: missing final checkpoints ===" >> "$OUT/rerun_log.txt"
fi
touch "$OUT/DONE"

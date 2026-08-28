#!/bin/bash
# Queue A: E5 policy eval on the four new suites (survives client kills).
cd /mnt/c/everything/projekti/compiler-opt
P=/root/venv-cgym/bin/python
$P scripts/evaluate_policy_battery.py --agent ppo_gnn --k 16 --seeds 42 123 456 \
  --suites linux-v0,github-v0,anghabench-v1,llvm-stress-v0 \
  >> results/e5_policy_gnn_log.txt 2>&1
$P scripts/evaluate_policy_battery.py --agent ppo_autophase --k 8 --seeds 42 123 456 \
  --suites linux-v0,github-v0,anghabench-v1,llvm-stress-v0 \
  >> results/e5_policy_ap_log.txt 2>&1
touch results/QUEUE_A.done

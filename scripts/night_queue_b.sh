#!/bin/bash
# Queue B: E1 controls -> E3 open-loop -> E4 portfolio -> ARM metrics.
cd /mnt/c/everything/projekti/compiler-opt
P=/root/venv-cgym/bin/python
ORIG=blas-v0,chstone-v0,csmith-v0,mibench-v1,npb-v0,poj104-v1
$P scripts/evaluate_policy_battery.py --agent ppo_gnn --untrained --seeds 42 \
  --suites $ORIG >> results/e1a_untrained_log.txt 2>&1
touch results/E1A.done
$P scripts/evaluate_policy_battery.py --agent ppo_gnn --no-dropout --seeds 42 \
  --suites $ORIG >> results/e1b_nodropout_log.txt 2>&1
touch results/E1B.done
$P scripts/evaluate_policy_battery.py --agent ppo_gnn --open-loop --seeds 42 \
  --suites $ORIG >> results/e3_openloop_log.txt 2>&1
touch results/E3.done
$P scripts/mine_portfolio.py mine   >> results/e4_portfolio_log.txt 2>&1
$P scripts/mine_portfolio.py select >> results/e4_portfolio_log.txt 2>&1
$P scripts/mine_portfolio.py eval   >> results/e4_portfolio_log.txt 2>&1
touch results/E4.done
$P scripts/measure_binary_metrics.py --mtriple thumbv7m-none-eabi \
  --suites $ORIG --out-dir results/binary_metrics_arm \
  >> results/arm_metrics_log.txt 2>&1
touch results/QUEUE_B.done

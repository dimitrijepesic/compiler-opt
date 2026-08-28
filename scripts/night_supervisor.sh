#!/bin/bash
# Keeps queue A alive until its marker exists: if the eval dies for any
# reason (OOM, VM restart), relaunch it. Detached, survives client kills.
cd /mnt/c/everything/projekti/compiler-opt
while [ ! -e results/QUEUE_A.done ]; do
  if ! pgrep -f "night_queue_a.sh" > /dev/null \
     && ! pgrep -f "evaluate_policy_battery" > /dev/null; then
    echo "$(date -Is) relaunching queue A" >> results/supervisor.log
    setsid nohup bash scripts/night_queue_a.sh >> results/queue_a_wrap.log 2>&1 < /dev/null &
  fi
  sleep 120
done
echo "$(date -Is) queue A finished" >> results/supervisor.log

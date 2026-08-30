#!/usr/bin/env python3
"""
Augment the existing baselines with the measurements the original run
was missing:

1. REAL -O3 / -Oz instruction counts via CompilerGym's
   IrInstructionCountO3 / IrInstructionCountOz observations (the old
   "o3"/"oz" fields were hand-crafted approximate pass sequences and are
   kept under o3_seq/oz_seq).

2. Random null models in the REDUCED 36-pass action space, which is what
   the RL agents actually act in:
     - random_reduced_policy: mean final IC of N single 45-step random
       episodes: the null model for a trained policy rollout.
     - random_reduced_search: best of N episodes: the null model for
       search-style baselines.

Existing expensive fields (greedy, random over the full action space)
are carried over unchanged from results/full_baselines.json.

Output: results/full_baselines_v2.json
"""

import compiler_gym
import json
import os
import sys
import time
import numpy as np
import yaml
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

POLICY_TRIALS = 20      # single-episode random policy trials
SEARCH_EPISODES = 50    # best-of-N random search episodes
EPISODE_STEPS = 45      # matches max_episode_steps of the RL agents
SEED = 42


def random_reduced(env, uri, action_map, rng):
    """Run random episodes in the reduced action space.

    Returns (policy_stats, search_best, per_episode_ics).
    """
    finals = []
    n_episodes = max(POLICY_TRIALS, SEARCH_EPISODES)
    for _ in range(n_episodes):
        env.reset(benchmark=uri)
        for _ in range(EPISODE_STEPS):
            action = action_map[rng.integers(len(action_map))]
            try:
                env.step(action)
            except Exception:
                break
        finals.append(int(env.observation["IrInstructionCount"]))

    policy_sample = finals[:POLICY_TRIALS]
    search_sample = finals[:SEARCH_EPISODES]

    policy_stats = {
        "mean": round(float(np.mean(policy_sample)), 1),
        "std": round(float(np.std(policy_sample)), 1),
        "min": int(np.min(policy_sample)),
        "max": int(np.max(policy_sample)),
        "trials": POLICY_TRIALS,
    }
    return policy_stats, int(np.min(search_sample)), finals


def main():
    with open("results/full_baselines.json") as f:
        old = json.load(f)

    with open("configs/passes.yaml") as f:
        passes_config = yaml.safe_load(f)
    action_map = [p["action_id"] for p in passes_config["passes"]]

    rng = np.random.default_rng(SEED)
    env = compiler_gym.make("llvm-ic-v0")

    results = []
    start_total = time.time()

    header = (f"{'Benchmark':<15} {'Split':<11} {'O0':>7} {'O3real':>7} "
              f"{'Ozreal':>7} {'O3seq':>7} {'Greedy':>7} {'RndRedP':>8} "
              f"{'RndRedS':>8} {'Time':>6}")
    print(header)
    print("-" * len(header))

    for entry in old["baselines"]:
        uri = entry["uri"]
        t0 = time.time()

        env.reset(benchmark=uri)
        o3_real = int(env.observation["IrInstructionCountO3"])
        oz_real = int(env.observation["IrInstructionCountOz"])

        policy_stats, search_best, episode_ics = random_reduced(
            env, uri, action_map, rng
        )

        new_entry = dict(entry)
        # The old fields were approximations; keep them, clearly labeled.
        new_entry["o3_seq"] = new_entry.pop("o3")
        new_entry["oz_seq"] = new_entry.pop("oz")
        new_entry["o3"] = o3_real
        new_entry["oz"] = oz_real
        new_entry["random_reduced_policy"] = policy_stats
        new_entry["random_reduced_search"] = search_best
        new_entry["random_reduced_episode_ics"] = episode_ics
        results.append(new_entry)

        elapsed = time.time() - t0
        print(
            f"{entry['short_name']:<15} {entry['split']:<11} "
            f"{entry['o0']:>7} {o3_real:>7} {oz_real:>7} "
            f"{new_entry['o3_seq']:>7} {entry['greedy']:>7} "
            f"{policy_stats['mean']:>8.1f} {search_best:>8} {elapsed:>5.0f}s"
        )

    env.close()

    output = {
        "timestamp": datetime.now().isoformat(),
        "compiler_gym_version": compiler_gym.__version__,
        "source": "results/full_baselines.json + augment_baselines.py",
        "random_reduced_config": {
            "policy_trials": POLICY_TRIALS,
            "search_episodes": SEARCH_EPISODES,
            "episode_steps": EPISODE_STEPS,
            "seed": SEED,
        },
        "total_time_seconds": round(time.time() - start_total, 1),
        "baselines": results,
    }

    out_path = "results/full_baselines_v2.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved: {out_path}")

    # Per-split summary against the real O3
    for split in ["train", "validation", "test"]:
        rows = [r for r in results if r["split"] == split]
        if not rows:
            continue
        print(f"\n{split.upper()} totals: "
              f"O0={sum(r['o0'] for r in rows)} "
              f"O3real={sum(r['o3'] for r in rows)} "
              f"Ozreal={sum(r['oz'] for r in rows)} "
              f"Greedy={sum(r['greedy'] for r in rows)} "
              f"RndRedSearch={sum(r['random_reduced_search'] for r in rows)}")


if __name__ == "__main__":
    main()

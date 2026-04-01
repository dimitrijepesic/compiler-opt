#!/usr/bin/env python3

import compiler_gym
import json
import os
import sys
import time
import random as rand_module
import yaml
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# --- O3 / Oz approximate pass sequences ---
O3_PASSES = [
    "-mem2reg", "-instcombine", "-simplifycfg", "-reassociate",
    "-gvn", "-licm", "-indvars", "-loop-simplify", "-loop-rotate",
    "-loop-unroll", "-sccp", "-dce", "-adce", "-simplifycfg", "-instcombine",
]

OZ_PASSES = [
    "-mem2reg", "-instcombine", "-simplifycfg", "-gvn", "-sccp",
    "-dce", "-adce", "-simplifycfg", "-instcombine",
    "-loop-deletion", "-strip-dead-prototypes",
]


def get_o0(env, benchmark_uri):
    """Return unoptimized IR instruction count."""
    env.reset(benchmark=benchmark_uri)
    return int(env.observation["IrInstructionCount"])


def apply_pass_sequence(env, benchmark_uri, passes):
    """Apply a named pass sequence and return final IC."""
    env.reset(benchmark=benchmark_uri)
    for pass_name in passes:
        try:
            action = env.action_space.flags.index(pass_name)
            env.step(action)
        except (ValueError, Exception):
            continue
    return int(env.observation["IrInstructionCount"])


def run_greedy(env, benchmark_uri, max_steps=45):
    """Greedy search: pick best single-action improvement at each step."""
    env.reset(benchmark=benchmark_uri)
    best_ic = int(env.observation["IrInstructionCount"])
    actions_taken = []

    for step in range(max_steps):
        best_action = None
        best_new_ic = best_ic

        for action in range(env.action_space.n):
            try:
                with env.fork() as forked:
                    forked.step(action)
                    ic = int(forked.observation["IrInstructionCount"])
                    if ic < best_new_ic:
                        best_new_ic = ic
                        best_action = action
            except Exception:
                continue

        if best_action is None or best_new_ic >= best_ic:
            break

        env.step(best_action)
        best_ic = best_new_ic
        actions_taken.append(int(best_action))

    return best_ic, actions_taken


def run_random(env, benchmark_uri, episodes=50, steps_per_episode=50):
    """Random search: best of N random episodes."""
    best_ic = None
    best_actions = []

    for ep in range(episodes):
        env.reset(benchmark=benchmark_uri)
        actions = []
        for step in range(steps_per_episode):
            action = env.action_space.sample()
            try:
                env.step(action)
                actions.append(int(action))
            except Exception:
                continue

        ic = int(env.observation["IrInstructionCount"])
        if best_ic is None or ic < best_ic:
            best_ic = ic
            best_actions = actions[:]

    return best_ic, best_actions


def load_benchmarks_config(config_path="configs/benchmarks.yaml"):
    """Load benchmark split config and return flat list of all URIs with split labels."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    benchmarks = []
    for split_name in ["train", "validation", "test"]:
        for uri in config[split_name]:
            benchmarks.append({"uri": uri, "split": split_name})
    return benchmarks


def main():
    print("=" * 70)
    print("FULL BASELINES COLLECTION")
    print("=" * 70)

    config_path = "configs/benchmarks.yaml"
    if not os.path.exists(config_path):
        print(f"ERROR: {config_path} not found. Run step 2 first.")
        sys.exit(1)

    benchmarks = load_benchmarks_config(config_path)
    total = len(benchmarks)
    print(f"Loaded {total} benchmarks from {config_path}\n")

    env = compiler_gym.make("llvm-ic-v0")

    results = []
    start_total = time.time()

    header = f"{'#':<4} {'Benchmark':<20} {'Split':<6} {'O0':>7} {'O3':>7} {'Oz':>7} {'Greedy':>7} {'Random':>7} {'Time':>6}"
    print(header)
    print("-" * len(header))

    for i, bm in enumerate(benchmarks):
        uri = bm["uri"]
        split = bm["split"]
        short_name = uri.split("/")[-1]
        start_bm = time.time()

        # O0
        o0 = get_o0(env, uri)

        # O3
        o3 = apply_pass_sequence(env, uri, O3_PASSES)

        # Oz
        oz = apply_pass_sequence(env, uri, OZ_PASSES)

        # Greedy
        greedy_ic, greedy_actions = run_greedy(env, uri, max_steps=45)

        # Random
        random_ic, random_actions = run_random(env, uri, episodes=50, steps_per_episode=50)

        elapsed = time.time() - start_bm

        entry = {
            "uri": uri,
            "short_name": short_name,
            "split": split,
            "o0": o0,
            "o3": o3,
            "oz": oz,
            "greedy": greedy_ic,
            "greedy_actions": greedy_actions,
            "greedy_num_steps": len(greedy_actions),
            "random": random_ic,
            "random_actions": random_actions,
            "time_seconds": round(elapsed, 1),
        }
        results.append(entry)

        print(
            f"{i+1:<4} {short_name:<20} {split:<6} {o0:>7} {o3:>7} {oz:>7} "
            f"{greedy_ic:>7} {random_ic:>7} {elapsed:>5.0f}s"
        )

    env.close()
    total_time = time.time() - start_total

    # --- Compute summary stats ---
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for split_name in ["train", "validation", "test"]:
        split_results = [r for r in results if r["split"] == split_name]
        if not split_results:
            continue

        sum_o3 = sum(r["o3"] for r in split_results)
        sum_greedy = sum(r["greedy"] for r in split_results)
        greedy_vs_o3 = (sum_o3 - sum_greedy) / sum_o3 * 100 if sum_o3 > 0 else 0

        print(f"\n  {split_name.upper()} ({len(split_results)} benchmarks):")
        print(f"    Total O3:     {sum_o3}")
        print(f"    Total Greedy: {sum_greedy}")
        print(f"    Greedy vs O3: {greedy_vs_o3:+.2f}%")

    print(f"\n  Total wall time: {total_time/60:.1f} minutes")

    # --- Save ---
    os.makedirs("results", exist_ok=True)
    output = {
        "timestamp": datetime.now().isoformat(),
        "compiler_gym_version": compiler_gym.__version__,
        "total_benchmarks": total,
        "total_time_seconds": round(total_time, 1),
        "baselines": results,
    }

    out_path = "results/full_baselines.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  Results saved to: {out_path}")


if __name__ == "__main__":
    main()
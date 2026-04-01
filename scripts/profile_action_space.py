#!/usr/bin/env python3

import compiler_gym
import json
import os
import sys
import time
import yaml
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def load_train_benchmarks(config_path="configs/benchmarks.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["train"]


def profile_all_passes(train_uris):
    env = compiler_gym.make("llvm-ic-v0")
    num_actions = env.action_space.n
    pass_names = list(env.action_space.flags)

    print(f"Profiling {num_actions} passes on {len(train_uris)} training benchmarks...\n")

    profiles = {}

    for action_id in range(num_actions):
        name = pass_names[action_id]
        deltas = {}
        benchmarks_improved = 0
        total_improvement = 0

        for uri in train_uris:
            short_name = uri.split("/")[-1]
            try:
                env.reset(benchmark=uri)
                baseline_ic = int(env.observation["IrInstructionCount"])

                with env.fork() as forked:
                    forked.step(action_id)
                    new_ic = int(forked.observation["IrInstructionCount"])

                delta = new_ic - baseline_ic 
                deltas[short_name] = delta

                if delta < 0:
                    benchmarks_improved += 1
                    total_improvement += abs(delta)

            except Exception:
                deltas[short_name] = 0

        avg_improvement = total_improvement / len(train_uris) if train_uris else 0
        max_improvement = abs(min(deltas.values())) if deltas else 0

        profiles[action_id] = {
            "action_id": action_id,
            "name": name,
            "benchmarks_improved": benchmarks_improved,
            "total_improvement": total_improvement,
            "avg_improvement": round(avg_improvement, 2),
            "max_improvement": max_improvement,
            "per_benchmark": deltas,
        }

        # Progress
        if (action_id + 1) % 10 == 0 or action_id == num_actions - 1:
            print(f"  [{action_id + 1:>3}/{num_actions}] {name:<35} improved {benchmarks_improved}/{len(train_uris)} benchmarks")

    env.close()
    return profiles, pass_names


def select_reduced_action_space(profiles, min_benchmarks=1):
    useful = []
    for action_id, p in profiles.items():
        if p["benchmarks_improved"] >= min_benchmarks:
            useful.append(p)

    # Sort by total improvement descending
    useful.sort(key=lambda x: x["total_improvement"], reverse=True)
    return useful


def main():
    print("=" * 70)
    print("ACTION SPACE PROFILING")
    print("=" * 70)

    config_path = "configs/benchmarks.yaml"
    if not os.path.exists(config_path):
        print(f"ERROR: {config_path} not found.")
        sys.exit(1)

    train_uris = load_train_benchmarks(config_path)
    start = time.time()

    profiles, pass_names = profile_all_passes(train_uris)

    reduced = select_reduced_action_space(profiles, min_benchmarks=1)
    total_passes = len(profiles)
    reduced_count = len(reduced)

    
    total_possible_improvement = sum(p["total_improvement"] for p in profiles.values())
    reduced_improvement = sum(p["total_improvement"] for p in reduced)
    coverage = (reduced_improvement / total_possible_improvement * 100) if total_possible_improvement > 0 else 0

    elapsed = time.time() - start

    print(f"\n{'=' * 70}")
    print("PROFILING RESULTS")
    print(f"{'=' * 70}")
    print(f"  Total passes profiled:  {total_passes}")
    print(f"  Passes with any effect: {reduced_count}")
    print(f"  Passes with no effect:  {total_passes - reduced_count}")
    print(f"  Coverage of total improvement: {coverage:.1f}%")
    print(f"  Profiling time: {elapsed / 60:.1f} minutes")

    print(f"\n  Top 20 most impactful passes:")
    print(f"  {'#':<4} {'Pass':<35} {'Improved':>9} {'Total':>8} {'Avg':>8} {'Max':>8}")
    print(f"  {'-' * 75}")
    for i, p in enumerate(reduced[:20]):
        print(
            f"  {i+1:<4} {p['name']:<35} {p['benchmarks_improved']:>5}/{len(train_uris):<3} "
            f"{p['total_improvement']:>8} {p['avg_improvement']:>8.1f} {p['max_improvement']:>8}"
        )

    os.makedirs("data", exist_ok=True)
    profiles_out = {
        "timestamp": datetime.now().isoformat(),
        "total_passes": total_passes,
        "reduced_count": reduced_count,
        "coverage_pct": round(coverage, 2),
        "train_benchmarks": train_uris,
        "profiles": {str(k): v for k, v in profiles.items()},
    }
    with open("data/pass_profiles.json", "w") as f:
        json.dump(profiles_out, f, indent=2)
    print(f"\n  Full profiles saved to: data/pass_profiles.json")

    passes_config = {
        "description": (
            f"Reduced action space: {reduced_count} passes that improve at least 1 "
            f"training benchmark (out of {total_passes} total). "
            f"Covers {coverage:.1f}% of total single-pass improvement."
        ),
        "total_original": total_passes,
        "total_reduced": reduced_count,
        "coverage_pct": round(coverage, 2),
        "passes": [
            {
                "action_id": p["action_id"],
                "name": p["name"],
                "benchmarks_improved": p["benchmarks_improved"],
                "total_improvement": p["total_improvement"],
                "avg_improvement": p["avg_improvement"],
                "max_improvement": p["max_improvement"],
            }
            for p in reduced
        ],
    }

    with open("configs/passes.yaml", "w") as f:
        yaml.dump(passes_config, f, default_flow_style=False, sort_keys=False)
    print(f"  Reduced action space saved to: configs/passes.yaml")


if __name__ == "__main__":
    main()
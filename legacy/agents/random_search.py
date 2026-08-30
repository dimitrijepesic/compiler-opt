# Legacy standalone random-search script (single benchmark, old llvm-v0
# API). Superseded by the null models in scripts/benchmark_battery.py.
# Kept for provenance only.
import compiler_gym
import numpy as np
import sys


def main():
    print("--- STARTING RANDOM SEARCH EXPERIMENT ---")

    BENCHMARK = "cbench-v1/qsort"
    EPISODES = 20       # How many times to restart from scratch
    STEPS_PER_EP = 50   # How many optimizations to apply per episode

    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"

    baseline = 638  # From an earlier run
    global_best_size = baseline
    best_actions = []

    print(f"Target Benchmark: {BENCHMARK}")
    print(f"Baseline Size: {baseline}")
    print("-" * 40)

    for ep in range(1, EPISODES + 1):
        env.reset()  # Back to 638
        episode_actions = []

        for step in range(STEPS_PER_EP):
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            episode_actions.append(action)

            current_size = observation
            if current_size < global_best_size:
                print(f"[NEW RECORD] Episode {ep}, Step {step}: {global_best_size} -> {current_size}")
                global_best_size = current_size
                best_actions = list(episode_actions)

            if done:
                break

    print("-" * 40)
    print("EXPERIMENT RESULTS:")
    print(f"Start: {baseline}")
    print(f"Best found (Random): {global_best_size}")

    improvement = (baseline - global_best_size) / baseline * 100
    print(f"Improvement: {improvement:.2f}%")
    print(f"Winning action sequence (first 10): {best_actions[:10]}...")

    env.close()


if __name__ == "__main__":
    main()

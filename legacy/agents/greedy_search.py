# Legacy standalone greedy-search script (single benchmark, old llvm-v0
# API). Superseded by scripts/run_full_baselines.py, which runs the same
# idea across the real benchmark splits. Kept for provenance only.
import compiler_gym
import sys
import copy

BENCHMARK = "cbench-v1/qsort"
STEPS = 15  # Fewer steps since it's slow (15 * 124 forks per run!)


def main():
    print(f"--- STARTING GREEDY SEARCH ON {BENCHMARK} ---")

    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"

    current_size = env.reset()
    print(f"Start: {current_size}")

    actions_taken = []

    for step in range(1, STEPS + 1):
        print(f"\n--- Step {step}/{STEPS} ---")
        best_action = None
        best_reduction = 0
        best_new_size = current_size

        # Try each of the 124 actions; fork so the main state stays untouched
        for action in range(env.action_space.n):
            with env.fork() as temp_env:
                observation, reward, done, info = temp_env.step(action)

                if observation < best_new_size:
                    best_new_size = observation
                    best_action = action
                    best_reduction = current_size - best_new_size

        if best_action is not None:
            print(f"  Best action: {env.action_space.to_string(best_action)}")
            print(f"  Reduction: {current_size} -> {best_new_size} (delta: -{best_reduction})")

            observation, reward, done, info = env.step(best_action)
            current_size = observation
            actions_taken.append(best_action)
        else:
            print("  No action reduces the code further. Local minimum.")
            break

    print("\n" + "=" * 40)
    print("FINAL RESULTS (Greedy):")
    print("Start: 638")  # From an earlier run
    print(f"End:   {current_size}")

    improvement = (638 - current_size) / 638 * 100
    print(f"Improvement: {improvement:.2f}%")
    print(f"Sequence: {actions_taken}")

    env.close()


if __name__ == "__main__":
    main()

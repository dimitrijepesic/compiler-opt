# Legacy smoke test from an early prototype (uses the old llvm-v0 API;
# the current pipeline's smoke test is scripts/smoke_test.py).
import compiler_gym
import sys


def main():
    print("--- Running CompilerGym experiment ---")

    try:
        env = compiler_gym.make("llvm-v0")
        print("[SUCCESS] Environment created.")

        env.reset(benchmark="cbench-v1/qsort")
        print("[SUCCESS] Benchmark 'qsort' loaded.")

        env.observation_space = "IrInstructionCount"

        initial_count = env.reset()
        print(f"\n>>> BASELINE INSTRUCTION COUNT: {initial_count}")

        num_actions = env.action_space.n
        print(f">>> ACTION SPACE SIZE: {num_actions}")

        env.close()
        print("\n--- Experiment finished successfully ---")

    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

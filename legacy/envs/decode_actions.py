# Legacy scratch script for turning a saved action-id sequence back into
# pass names (old llvm-v0 API). Kept for provenance only.
import compiler_gym


def main():
    # Only the environment is needed to look up action names; no benchmark reset required
    env = compiler_gym.make("llvm-v0")

    # Winning sequence from an earlier random-search run
    winning_sequence = [100, 16, 37, 48, 9, 50, 72, 73, 44, 61]

    print(f"\n{'ID':<5} | {'OPTIMIZATION (LLVM PASS)':<40}")
    print("-" * 50)

    names = env.action_space.names

    for action_id in winning_sequence:
        if action_id < len(names):
            action_name = names[action_id]
            print(f"{action_id:<5} | {action_name:<40}")
        else:
            print(f"{action_id:<5} | [UNKNOWN ID]")

    env.close()


if __name__ == "__main__":
    main()

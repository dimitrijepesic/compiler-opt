# Legacy environment factory (old llvm-v0 API), used by the RISC-V
# prototype in legacy/main.py. Kept for provenance only.
import compiler_gym


def make_env(benchmark="cbench-v1/qsort", reward_type="space"):
    """Factory that creates and configures the environment.

    Centralized place for all CompilerGym settings.
    """
    env = compiler_gym.make("llvm-v0")

    try:
        env.reset(benchmark=benchmark)
    except ValueError:
        print(f"[ERROR] Benchmark '{benchmark}' not found. Falling back to 'cbench-v1/qsort'.")
        env.reset(benchmark="cbench-v1/qsort")

    if reward_type == "space":
        env.observation_space = "IrInstructionCount"
    elif reward_type == "execution":
        print("[INFO] Execution mode is not implemented yet. Using IrInstructionCount as a placeholder.")
        env.observation_space = "IrInstructionCount"
    else:
        raise ValueError(f"Unknown reward type: {reward_type}. Use 'space' or 'execution'.")

    return env

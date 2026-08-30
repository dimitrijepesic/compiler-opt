# Legacy scratch script for poking at a single benchmark's IR (old llvm-v0
# API). Kept for provenance only.
import compiler_gym


def main():
    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark="cbench-v1/qsort")

    print("1. metadata")
    print(f"Benchmark URI: {env.benchmark}")

    print()
    print("2. first 20 lines of LLVM IR")
    env.observation_space = "Ir"

    ir_code = env.reset()

    print("\n".join(ir_code.splitlines()[:20]))

    print("\ndone")
    env.close()


if __name__ == "__main__":
    main()

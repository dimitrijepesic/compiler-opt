"""Two-minute demo: compile demo/test.c, run the greedy agent on it, and
compare the optimized binary's output and size against the unoptimized
baseline. Not part of the paper's evaluation pipeline; see README.md for
that.

  python scripts/demo_runner.py
"""
import compiler_gym
import subprocess
import os
import sys
from src.agents.greedy import GreedyAgent

# clang shipped with CompilerGym's LLVM; override with COMPILER_OPT_CLANG if needed
CLANG_CMD = os.environ.get(
    "COMPILER_OPT_CLANG",
    os.path.expanduser("~/.local/share/compiler_gym/llvm-v0/bin/clang"),
)

SOURCE_FILE = "demo/test.c"
BC_FILE = "demo/test.bc"
ABS_PATH_BC = os.path.abspath(BC_FILE)


def main():
    print(f"\nRUNNING DEMO ON: {SOURCE_FILE}")

    if not os.path.exists(CLANG_CMD):
        print(f"ERROR: clang not found at: {CLANG_CMD}")
        sys.exit(1)

    print("[1/5] Compiling the source with the bundled clang...")
    try:
        subprocess.run([CLANG_CMD, "-O0", "-Xclang", "-disable-O0-optnone",
                        "-emit-llvm", "-c", SOURCE_FILE, "-o", BC_FILE], check=True)
    except Exception as e:
        print(f"Compilation failed: {e}")
        sys.exit(1)

    print("[2/5] Loading the bitcode into CompilerGym...")
    env = compiler_gym.make("llvm-v0")

    try:
        env.reset(benchmark=f"file://{ABS_PATH_BC}")
    except ValueError as e:
        print(f"Failed to load the bitcode: {e}")
        sys.exit(1)

    print(f"   Initial instruction count: {env.observation['IrInstructionCount']}")

    print("[3/5] The greedy agent is optimizing the code...")
    agent = GreedyAgent(env)
    agent.train(steps=15)

    env.write_bitcode("demo/optimized.bc")

    print("[4/5] Building executables (.bin)...")

    # Uses the system clang (not CompilerGym's), which knows where the
    # standard libraries are. Requires `clang` on PATH (e.g. apt install clang).
    SYSTEM_CLANG = "clang"
    subprocess.run([SYSTEM_CLANG, BC_FILE, "-o", "demo/baseline_bin", "-lm"], check=True)
    subprocess.run([SYSTEM_CLANG, "demo/optimized.bc", "-o", "demo/optimized_bin", "-lm"], check=True)

    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)

    print("\n--- 1. ORIGINAL CODE OUTPUT ---")
    out_base = subprocess.run(["./demo/baseline_bin"], capture_output=True, text=True)
    print(out_base.stdout.strip())

    print("\n--- 2. OPTIMIZED CODE OUTPUT ---")
    out_opt = subprocess.run(["./demo/optimized_bin"], capture_output=True, text=True)
    print(out_opt.stdout.strip())

    if out_base.stdout == out_opt.stdout:
        print("\nVALIDATION PASSED: outputs are IDENTICAL!")
    else:
        print("\nERROR: the agent broke the program!")

    bc_size_base = os.path.getsize(BC_FILE)
    bc_size_opt = os.path.getsize("demo/optimized.bc")

    print("\n--- SIZE STATISTICS (BITCODE) ---")
    print(f"Original:  {bc_size_base} bytes")
    print(f"Optimized: {bc_size_opt} bytes")
    print(f"SAVED:     {bc_size_base - bc_size_opt} bytes")

    env.close()


if __name__ == "__main__":
    main()

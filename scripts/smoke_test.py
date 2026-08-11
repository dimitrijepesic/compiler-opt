#!/usr/bin/env python3
"""Quick environment smoke test: CompilerGym + real O3/Oz observations."""
import compiler_gym

env = compiler_gym.make("llvm-ic-v0")
env.reset(benchmark="benchmark://cBench-v1/crc32")
print("O0 IC:", env.observation["IrInstructionCount"])
print("real O3 IC:", env.observation["IrInstructionCountO3"])
print("real Oz IC:", env.observation["IrInstructionCountOz"])
env.close()
print("SMOKE-OK")

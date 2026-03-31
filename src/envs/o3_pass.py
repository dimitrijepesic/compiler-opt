# src/get_o3_baselines.py

import compiler_gym

BENCHMARKS = [
    "benchmark://cbench-v1/adpcm",
    "benchmark://cbench-v1/bitcount",
    "benchmark://cbench-v1/blowfish",
    "benchmark://cbench-v1/crc32",
    "benchmark://cbench-v1/dijkstra",
    "benchmark://cbench-v1/gsm",
    "benchmark://cbench-v1/jpeg-c",
    "benchmark://cbench-v1/jpeg-d",
    "benchmark://cbench-v1/patricia",
    "benchmark://cbench-v1/qsort",
    "benchmark://cbench-v1/sha",
    "benchmark://cbench-v1/stringsearch",
    "benchmark://cbench-v1/susan",
]

O3_PASSES = [
    "-mem2reg", "-instcombine", "-simplifycfg", "-reassociate",
    "-gvn", "-licm", "-indvars", "-loop-simplify", "-loop-rotate",
    "-loop-unroll", "-sccp", "-dce", "-adce", "-simplifycfg", "-instcombine",
]

# Your greedy results
greedy_results = {
    "adpcm": 218, "bitcount": 399, "blowfish": 1873, "crc32": 114,
    "dijkstra": 258, "gsm": 6009, "jpeg-c": 28989, "jpeg-d": 27671,
    "patricia": 401, "qsort": 271, "sha": 358, "stringsearch": 608, "susan": 5431,
}

print(f"{'Benchmark':<15} {'O0':>8} {'O3':>8} {'Greedy':>8} {'vs O3':>10}")
print("-" * 55)

for benchmark in BENCHMARKS:
    name = benchmark.split("/")[-1]
    
    env = compiler_gym.make("llvm-ic-v0")
    
    # Get O0
    env.reset(benchmark=benchmark)
    o0 = env.observation["IrInstructionCount"]
    
    # Get O3
    env.reset(benchmark=benchmark)
    for pass_name in O3_PASSES:
        try:
            action = env.action_space.flags.index(pass_name)
            env.step(action)
        except ValueError:
            continue
    o3 = env.observation["IrInstructionCount"]
    
    env.close()
    
    greedy = greedy_results.get(name, 0)
    
    if o3 > 0:
        vs_o3 = (o3 - greedy) / o3 * 100
        vs_o3_str = f"{vs_o3:+.1f}%"
    else:
        vs_o3_str = "N/A"
    
    print(f"{name:<15} {o0:>8} {o3:>8} {greedy:>8} {vs_o3_str:>10}")

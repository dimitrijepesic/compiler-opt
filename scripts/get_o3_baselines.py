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

# Your greedy results from earlier
GREEDY_RESULTS = {
    "adpcm": 218,
    "bitcount": 399,
    "blowfish": 1873,
    "crc32": 114,
    "dijkstra": 258,
    "gsm": 6009,
    "jpeg-c": 28989,
    "jpeg-d": 27671,
    "patricia": 401,
    "qsort": 271,
    "sha": 358,
    "stringsearch": 608,
    "susan": 5431,
}

def get_o3_instruction_count(benchmark):
    """
    Apply standard -O3 passes and return instruction count.
    """
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark=benchmark)
    
    # Standard O3 pass sequence (approximate)
    o3_passes = [
        "-mem2reg",
        "-instcombine",
        "-simplifycfg", 
        "-early-cse",
        "-gvn",
        "-sccp",
        "-licm",
        "-indvars",
        "-loop-simplify",
        "-loop-rotate",
        "-loop-unroll",
        "-dce",
        "-adce",
        "-simplifycfg",
        "-instcombine",
    ]
    
    for pass_name in o3_passes:
        try:
            action = env.action_space.flags.index(pass_name)
            env.step(action)
        except (ValueError, Exception):
            # Pass not found or failed, skip
            continue
    
    result = env.observation["IrInstructionCount"]
    env.close()
    return result


def get_oz_instruction_count(benchmark):
    """
    Apply -Oz (size optimization) passes.
    """
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark=benchmark)
    
    # -Oz focuses on size
    oz_passes = [
        "-mem2reg",
        "-instcombine",
        "-simplifycfg",
        "-gvn",
        "-sccp",
        "-dce",
        "-adce",
        "-simplifycfg",
        "-instcombine",
        "-loop-deletion",
        "-strip-dead-prototypes",
    ]
    
    for pass_name in oz_passes:
        try:
            action = env.action_space.flags.index(pass_name)
            env.step(action)
        except (ValueError, Exception):
            continue
    
    result = env.observation["IrInstructionCount"]
    env.close()
    return result


def main():
    print("=" * 75)
    print("COMPILER OPTIMIZATION COMPARISON: -O0 vs -O3 vs -Oz vs Greedy")
    print("=" * 75)
    print()
    
    print(f"{'Benchmark':<15} {'O0':>8} {'O3':>8} {'Oz':>8} {'Greedy':>8} {'vs O3':>10} {'vs Oz':>10}")
    print("-" * 75)
    
    total_o0 = 0
    total_o3 = 0
    total_oz = 0
    total_greedy = 0
    
    wins_vs_o3 = 0
    wins_vs_oz = 0
    
    results = []
    
    for benchmark in BENCHMARKS:
        name = benchmark.split("/")[-1]
        
        # Get O0 baseline
        env = compiler_gym.make("llvm-ic-v0")
        env.reset(benchmark=benchmark)
        o0 = env.observation["IrInstructionCount"]
        env.close()
        
        # Get O3
        o3 = get_o3_instruction_count(benchmark)
        
        # Get Oz
        oz = get_oz_instruction_count(benchmark)
        
        # Get greedy (from saved results)
        greedy = GREEDY_RESULTS.get(name, 0)
        
        # Calculate improvements
        vs_o3 = ((o3 - greedy) / o3 * 100) if o3 > 0 else 0
        vs_oz = ((oz - greedy) / oz * 100) if oz > 0 else 0
        
        vs_o3_str = f"{vs_o3:+.1f}%"
        vs_oz_str = f"{vs_oz:+.1f}%"
        
        if greedy < o3:
            wins_vs_o3 += 1
        if greedy < oz:
            wins_vs_oz += 1
        
        print(f"{name:<15} {o0:>8} {o3:>8} {oz:>8} {greedy:>8} {vs_o3_str:>10} {vs_oz_str:>10}")
        
        total_o0 += o0
        total_o3 += o3
        total_oz += oz
        total_greedy += greedy
        
        results.append({
            "benchmark": name,
            "o0": o0,
            "o3": o3,
            "oz": oz,
            "greedy": greedy,
            "vs_o3_pct": vs_o3,
            "vs_oz_pct": vs_oz,
        })
    
    # Summary
    print("-" * 75)
    avg_vs_o3 = (total_o3 - total_greedy) / total_o3 * 100
    avg_vs_oz = (total_oz - total_greedy) / total_oz * 100
    
    print(f"{'TOTAL':<15} {total_o0:>8} {total_o3:>8} {total_oz:>8} {total_greedy:>8} {avg_vs_o3:>+9.1f}% {avg_vs_oz:>+9.1f}%")
    print()
    print(f"Greedy beats -O3 on {wins_vs_o3}/{len(BENCHMARKS)} benchmarks")
    print(f"Greedy beats -Oz on {wins_vs_oz}/{len(BENCHMARKS)} benchmarks")
    
    # Save results
    import json
    import os
    
    os.makedirs("results", exist_ok=True)
    with open("results/o3_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to results/o3_comparison.json")
    
    return results


if __name__ == "__main__":
    main()

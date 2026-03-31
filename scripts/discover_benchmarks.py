import compiler_gym
import json
import os
from tqdm import tqdm

def discover_cbench():
    print("Starting cBench discovery and validation...")
    valid_benchmarks = []
    failed_benchmarks = {}

    env = compiler_gym.make("llvm-v0")
    dataset = env.datasets["cBench-v1"]
    
    os.makedirs("data", exist_ok=True)

    benchmarks = list(dataset.benchmarks())
    for benchmark in tqdm(benchmarks, desc="Validating Benchmarks"):
        try:
            env.reset(benchmark=benchmark)
            forked_env = env.fork()
            forked_env.close()
            valid_benchmarks.append(str(benchmark.uri))
        except Exception as e:
            failed_benchmarks[str(benchmark.uri)] = str(e)
    
    env.close()

    inventory = {
        "total_valid": len(valid_benchmarks),
        "total_failed": len(failed_benchmarks),
        "valid_uris": valid_benchmarks,
        "failed_uris": failed_benchmarks
    }

    output_path = "data/benchmark_inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=4)

    print(f"\nDiscovery complete!")
    print(f"Found {len(valid_benchmarks)} valid benchmarks.")
    print(f"Failed {len(failed_benchmarks)} benchmarks.")
    print(f"Saved inventory to {output_path}")

if __name__ == "__main__":
    discover_cbench()
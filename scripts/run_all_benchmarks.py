# src/run_all_benchmarks.py

import compiler_gym
import json
from datetime import datetime

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

def run_greedy(env, max_steps=45):
    """Greedy search - pick best action at each step"""
    best_ic = env.observation["IrInstructionCount"]
    actions_taken = []
    
    for step in range(max_steps):
        best_action = None
        best_reward = 0
        
        # Try each action
        for action in range(env.action_space.n):
            # Fork environment to test action
            with env.fork() as env_copy:
                _, reward, _, _ = env_copy.step(action)
                if reward > best_reward:
                    best_reward = reward
                    best_action = action
        
        # If no improving action found, stop
        if best_action is None or best_reward <= 0:
            break
        
        # Apply best action
        env.step(best_action)
        actions_taken.append(best_action)
        best_ic = env.observation["IrInstructionCount"]
    
    return best_ic, actions_taken

def main():
    results = {}
    
    for benchmark in BENCHMARKS:
        print(f"\nRunning {benchmark}...")
        
        try:
            # Create environment - THIS IS THE KEY FIX
            env = compiler_gym.make("llvm-ic-v0")
            
            # Reset with benchmark
            env.reset(benchmark=benchmark)
            
            # Get baseline (-O0)
            baseline_o0 = env.observation["IrInstructionCount"]
            print(f"  -O0 baseline: {baseline_o0}")
            
            # Reset and run greedy
            env.reset(benchmark=benchmark)
            greedy_result, actions = run_greedy(env)
            print(f"  Greedy result: {greedy_result}")
            
            # Calculate improvement
            improvement = (baseline_o0 - greedy_result) / baseline_o0 * 100
            print(f"  Improvement: {improvement:.1f}%")
            
            results[benchmark.split("/")[-1]] = {
                "baseline_O0": int(baseline_o0),
                "greedy": int(greedy_result),
                "improvement_pct": round(improvement, 2),
                "num_actions": len(actions)
            }
            
            env.close()
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[benchmark.split("/")[-1]] = {"error": str(e)}
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/benchmarks_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to {filename}")
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'Benchmark':<20} {'O0':>10} {'Greedy':>10} {'Improv%':>10}")
    print("-"*60)
    
    for name, data in results.items():
        if "error" not in data:
            print(f"{name:<20} {data['baseline_O0']:>10} {data['greedy']:>10} {data['improvement_pct']:>10.1f}%")

if __name__ == "__main__":
    main()

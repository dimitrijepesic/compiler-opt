# src/data/collect_and_save.py

import compiler_gym
import numpy as np
import json
import os

BENCHMARKS = [
    "benchmark://cbench-v1/qsort",
    "benchmark://cbench-v1/crc32",
    "benchmark://cbench-v1/dijkstra",
    "benchmark://cbench-v1/adpcm",
    "benchmark://cbench-v1/sha",
    "benchmark://cbench-v1/bitcount",
    "benchmark://cbench-v1/blowfish",
    "benchmark://cbench-v1/stringsearch",
    "benchmark://cbench-v1/susan",
    "benchmark://cbench-v1/patricia",
    "benchmark://cbench-v1/gsm",
    "benchmark://cbench-v1/jpeg-c",
    "benchmark://cbench-v1/jpeg-d",
]


def collect_greedy_data(num_trajectories=5, steps_per_trajectory=45):
    """Collect greedy trajectories and save to file."""
    
    env = compiler_gym.make("llvm-ic-v0")
    num_actions = env.action_space.n
    
    all_data = []
    
    print(f"Collecting {num_trajectories} trajectories from {len(BENCHMARKS)} benchmarks...")
    
    for benchmark in BENCHMARKS:
        name = benchmark.split('/')[-1]
        samples_before = len(all_data)
        
        for traj in range(num_trajectories):
            try:
                env.reset(benchmark=benchmark)
            except:
                continue
            
            for step in range(steps_per_trajectory):
                # Get features
                try:
                    autophase = env.observation["Autophase"]
                    features = np.log1p(np.array(autophase, dtype=np.float32))
                except:
                    break
                
                current_ic = env.observation["IrInstructionCount"]
                
                # Find best action
                best_action = None
                best_ic = current_ic
                
                for action in range(num_actions):
                    try:
                        with env.fork() as temp_env:
                            temp_env.step(action)
                            new_ic = temp_env.observation["IrInstructionCount"]
                            if new_ic is not None and new_ic < best_ic:
                                best_ic = new_ic
                                best_action = action
                    except:
                        continue
                
                if best_action is not None:
                    all_data.append({
                        "features": features.tolist(),
                        "action": best_action,
                        "benchmark": name,
                    })
                    env.step(best_action)
                else:
                    break
        
        print(f"   {name}: +{len(all_data) - samples_before} samples")
    
    env.close()
    
    # Save to file
    os.makedirs("data", exist_ok=True)
    
    with open("data/greedy_trajectories.json", "w") as f:
        json.dump(all_data, f)
    
    print(f"\nTotal: {len(all_data)} samples saved to data/greedy_trajectories.json")
    
    return all_data


if __name__ == "__main__":
    collect_greedy_data(num_trajectories=5, steps_per_trajectory=45)
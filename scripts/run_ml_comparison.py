# src/run_ml_comparison.py

import compiler_gym
import json
import os
from datetime import datetime

# Agents
from agents.greedy import GreedyAgent
from agents.random_agent import RandomAgent
from agents.nn_agent import NeuralNetworkAgent
from agents.dqn_agent import DQNAgent

BENCHMARKS = [
    "benchmark://cbench-v1/qsort",
    "benchmark://cbench-v1/crc32",
    "benchmark://cbench-v1/dijkstra",
    "benchmark://cbench-v1/adpcm",
    "benchmark://cbench-v1/sha",
]

O3_BASELINES = {
    "qsort": 289,
    "crc32": 122,
    "dijkstra": 275,
    "adpcm": 221,
    "sha": 427,
}


def get_o0(benchmark):
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark=benchmark)
    ic = env.observation["IrInstructionCount"]
    env.close()
    return ic


def run_greedy(benchmark):
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark=benchmark)
    agent = GreedyAgent(env)
    score, _ = agent.train(steps=45)
    env.close()
    return score


def run_random(benchmark):
    env = compiler_gym.make("llvm-ic-v0")
    env.reset(benchmark=benchmark)
    agent = RandomAgent(env)
    score, _ = agent.train(steps=45, episodes=50)
    env.close()
    return score


def run_nn(benchmark):
    agent = NeuralNetworkAgent(benchmark)
    score, _ = agent.train(num_trajectories=5, epochs=50)
    agent.close()
    return score


def run_dqn(benchmark):
    agent = DQNAgent(benchmark)
    score, _ = agent.train(episodes=50, steps_per_episode=30)
    agent.close()
    return score


def main():
    print("=" * 90)
    print("ML COMPARISON: Random vs Greedy vs Neural Network vs DQN vs -O3")
    print("=" * 90)
    
    results = []
    
    for benchmark in BENCHMARKS:
        name = benchmark.split("/")[-1]
        print(f"\n{'='*90}")
        print(f"BENCHMARK: {name}")
        print(f"{'='*90}")
        
        o0 = get_o0(benchmark)
        o3 = O3_BASELINES.get(name, 0)
        
        print("\n[1/4] Random...")
        random_score = run_random(benchmark)
        
        print("\n[2/4] Greedy...")
        greedy_score = run_greedy(benchmark)
        
        print("\n[3/4] Neural Network...")
        nn_score = run_nn(benchmark)
        
        print("\n[4/4] DQN...")
        dqn_score = run_dqn(benchmark)
        
        # Results
        print(f"\n{'Method':<15} {'IC':>8} {'vs O3':>10}")
        print("-" * 35)
        print(f"{'-O0':<15} {o0:>8}")
        print(f"{'-O3':<15} {o3:>8} {'baseline':>10}")
        print(f"{'Random':<15} {random_score:>8} {(o3-random_score)/o3*100:>+9.1f}%")
        print(f"{'Greedy':<15} {greedy_score:>8} {(o3-greedy_score)/o3*100:>+9.1f}%")
        print(f"{'NN':<15} {nn_score:>8} {(o3-nn_score)/o3*100:>+9.1f}%")
        print(f"{'DQN':<15} {dqn_score:>8} {(o3-dqn_score)/o3*100:>+9.1f}%")
        
        best = min(random_score, greedy_score, nn_score, dqn_score)
        best_method = {random_score: "Random", greedy_score: "Greedy", nn_score: "NN", dqn_score: "DQN"}[best]
        print(f"\nBest: {best_method} ({best})")
        
        results.append({
            "benchmark": name,
            "o0": o0,
            "o3": o3,
            "random": random_score,
            "greedy": greedy_score,
            "nn": nn_score,
            "dqn": dqn_score,
            "best": best,
            "best_method": best_method,
        })
    
    # Final summary
    print("\n" + "=" * 90)
    print("FINAL SUMMARY")
    print("=" * 90)
    
    print(f"\n{'Benchmark':<12} {'O3':>8} {'Random':>8} {'Greedy':>8} {'NN':>8} {'DQN':>8} {'Best':>10}")
    print("-" * 75)
    
    for r in results:
        print(f"{r['benchmark']:<12} {r['o3']:>8} {r['random']:>8} {r['greedy']:>8} {r['nn']:>8} {r['dqn']:>8} {r['best_method']:>10}")
    
    # Totals
    print("-" * 75)
    total_o3 = sum(r["o3"] for r in results)
    total_random = sum(r["random"] for r in results)
    total_greedy = sum(r["greedy"] for r in results)
    total_nn = sum(r["nn"] for r in results)
    total_dqn = sum(r["dqn"] for r in results)
    
    print(f"{'TOTAL':<12} {total_o3:>8} {total_random:>8} {total_greedy:>8} {total_nn:>8} {total_dqn:>8}")
    print(f"{'vs O3':<12} {'':>8} {(total_o3-total_random)/total_o3*100:>+7.1f}% {(total_o3-total_greedy)/total_o3*100:>+7.1f}% {(total_o3-total_nn)/total_o3*100:>+7.1f}% {(total_o3-total_dqn)/total_o3*100:>+7.1f}%")
    
    # Save
    os.makedirs("results", exist_ok=True)
    with open(f"results/ml_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
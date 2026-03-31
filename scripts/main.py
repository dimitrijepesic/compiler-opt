import argparse
import sys
import traceback
from src.envs.compiler_env import make_env
from src.agents.greedy import GreedyAgent
from src.agents.genetic import GeneticAgent
from src.utils.validator import verify_optimization

def main():
    parser = argparse.ArgumentParser(description="RISC-V Optimization Arena")
    
    parser.add_argument("--benchmark", type=str, default="cbench-v1/qsort", help="Benchmark to optimize")
    parser.add_argument("--model", type=str, required=True, choices=["greedy", "genetic"], help="Optimization model")
    parser.add_argument("--target", type=str, default="space", choices=["space", "execution"], help="Optimization target")
    
    args = parser.parse_args()

    print(f"--- POKRETANJE: Model={args.model} | Benchmark={args.benchmark} | Target={args.target} ---")

    try:
        env = make_env(args.benchmark, args.target)

        if args.model == "greedy":
            agent = GreedyAgent(env)
        elif args.model == "genetic":
            agent = GeneticAgent(env)
        
        agent.train()
        agent.save_results()
        
        if agent.best_sequence:
            verify_optimization(args.benchmark, agent.best_sequence)
        
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        if 'env' in locals():
            env.close()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.ppo_autophase import PPOAutophaseAgent


def main():
    parser = argparse.ArgumentParser(description="Train PPO + Autophase")
    parser.add_argument("--seed", type=int, default=None,
                        help="Single seed to run. If not set, runs all 3 seeds.")
    parser.add_argument("--config", type=str, default="configs/hyperparams.yaml")
    parser.add_argument("--passes", type=str, default="configs/passes.yaml")
    parser.add_argument("--benchmarks", type=str, default="configs/benchmarks.yaml")
    parser.add_argument("--save-dir", type=str, default="results/ppo_autophase")
    args = parser.parse_args()

    seeds = [args.seed] if args.seed is not None else [42, 123, 456]

    for seed in seeds:
        print(f"\n{'#' * 70}")
        print(f"# SEED {seed}")
        print(f"{'#' * 70}\n")

        agent = PPOAutophaseAgent(
            config_path=args.config,
            passes_path=args.passes,
            benchmarks_path=args.benchmarks,
            seed=seed,
        )

        try:
            agent.train(save_dir=args.save_dir)
        finally:
            agent.close()


if __name__ == "__main__":
    main()
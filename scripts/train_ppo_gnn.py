#!/usr/bin/env python3
"""
Step 5: Train PPO + GNN Agent
Trains the PPO agent with the GraphSAGE encoder on program graphs.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.ppo_gnn import PPOGNNAgent


def main():
    parser = argparse.ArgumentParser(description="Train PPO + GNN")
    parser.add_argument("--seed", type=int, default=None,
                        help="Single seed to run. If not set, runs all 3 seeds.")
    parser.add_argument("--config", type=str, default="configs/hyperparams.yaml")
    parser.add_argument("--passes", type=str, default="configs/passes.yaml")
    parser.add_argument("--benchmarks", type=str, default="configs/benchmarks.yaml")
    parser.add_argument("--save-dir", type=str, default="results/ppo_gnn")
    parser.add_argument("--init-encoder", type=str, default=None,
                        help="Path to pretrained encoder checkpoint "
                             "(scripts/pretrain_gnn.py output)")
    parser.add_argument("--device", type=str, default=None,
                        help="cpu (default) or cuda; falls back to the "
                             "COMPILER_OPT_DEVICE environment variable")
    parser.add_argument("--total-steps", type=int, default=None,
                        help="Override the config's total_env_steps "
                             "(timing probes only)")
    args = parser.parse_args()

    seeds = [args.seed] if args.seed is not None else [42, 123, 456]

    for seed in seeds:
        print(f"\n{'#' * 70}")
        print(f"# SEED {seed}")
        print(f"{'#' * 70}\n")

        agent = PPOGNNAgent(
            config_path=args.config,
            passes_path=args.passes,
            benchmarks_path=args.benchmarks,
            seed=seed,
            init_encoder_path=args.init_encoder,
            device=args.device,
            total_env_steps=args.total_steps,
        )

        try:
            agent.train(save_dir=args.save_dir)
        finally:
            agent.close()


if __name__ == "__main__":
    main()
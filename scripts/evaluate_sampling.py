#!/usr/bin/env python3
"""
Track A: best-of-k sampling evaluation.

Argmax rollouts measure a policy's mode, which we saw transfer badly.
Here each (agent, seed, benchmark) runs k stochastic rollouts (actions
sampled from the policy distribution) and keeps the best final IC.
The fair null is best-of-k RANDOM episodes in the same 36-pass space,
computed from the per-episode ICs stored in full_baselines_v2.json.

Output: results/sampling_evaluation.json
"""

import sys
import os
import json
import argparse
import numpy as np
import torch
import yaml
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.ppo_autophase import PPOAutophaseAgent
from src.agents.ppo_gnn import PPOGNNAgent


def sample_rollout(agent, uri, is_gnn, rng_seed):
    """One stochastic 45-step rollout; returns final IC."""
    torch.manual_seed(rng_seed)
    agent.env.reset(benchmark=uri)

    if is_gnn:
        state = agent._get_graph()
    else:
        state = agent._get_state()

    for _ in range(agent.max_episode_steps):
        with torch.no_grad():
            if is_gnn:
                embedding = agent.gnn(state)
                logits = agent.policy(embedding)
            else:
                logits = agent.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(logits=logits)
            action_idx = dist.sample().item()

        try:
            agent.env.step(agent.action_map[action_idx])
        except Exception:
            continue

        state = agent._get_graph() if is_gnn else agent._get_state()

    return int(agent.env.observation["IrInstructionCount"])


def argmax_rollout(agent, uri, is_gnn):
    """Deterministic rollout for reference (same as evaluate())."""
    total, _, details = agent.evaluate([uri], "ref")
    return details[0]["final_ic"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    parser.add_argument("--ppo-ap-dir", type=str, default="results/ppo_autophase")
    parser.add_argument("--ppo-gnn-dir", type=str, default="results/ppo_gnn")
    parser.add_argument("--benchmarks", type=str, default="configs/benchmarks.yaml")
    parser.add_argument("--baselines", type=str,
                        default="results/full_baselines_v2.json")
    parser.add_argument("--output", type=str,
                        default="results/sampling_evaluation.json")
    args = parser.parse_args()

    with open(args.benchmarks) as f:
        bm_config = yaml.safe_load(f)
    uris = bm_config["validation"] + bm_config["test"]
    split_of = {}
    for u in bm_config["validation"]:
        split_of[u] = "validation"
    for u in bm_config["test"]:
        split_of[u] = "test"

    with open(args.baselines) as f:
        baselines = {b["short_name"]: b for b in json.load(f)["baselines"]}

    results = {"k": args.k, "agents": {}, "random_null": {}}

    # Fair null: best of first k stored random-reduced episodes
    for uri in uris:
        name = uri.split("/")[-1]
        ics = baselines[name]["random_reduced_episode_ics"][:args.k]
        results["random_null"][name] = int(min(ics))

    for agent_key, agent_class, ckpt_dir, is_gnn in [
        ("ppo_autophase", PPOAutophaseAgent, args.ppo_ap_dir, False),
        ("ppo_gnn", PPOGNNAgent, args.ppo_gnn_dir, True),
    ]:
        results["agents"][agent_key] = {}
        for seed in args.seeds:
            ckpt = os.path.join(ckpt_dir, f"checkpoint_best_seed{seed}.pt")
            if not os.path.exists(ckpt):
                print(f"[{agent_key}] seed {seed}: no checkpoint, skipping")
                continue

            agent = agent_class(seed=seed)
            try:
                agent.load_checkpoint(ckpt)
                if hasattr(agent, "gnn"):
                    agent.gnn.train()  # sample with dropout active (paper Sec. III)
                per_bm = {}
                for uri in uris:
                    name = uri.split("/")[-1]
                    samples = [
                        sample_rollout(agent, uri, is_gnn,
                                       rng_seed=seed * 1000 + i)
                        for i in range(args.k)
                    ]
                    am = argmax_rollout(agent, uri, is_gnn)
                    per_bm[name] = {
                        "split": split_of[uri],
                        "argmax_ic": int(am),
                        "sample_ics": [int(s) for s in samples],
                        "best_of_k_ic": int(min(samples)),
                        "random_best_of_k_ic": results["random_null"][name],
                    }
                    print(f"[{agent_key} seed {seed}] {name}: "
                          f"argmax={am} best-of-{args.k}={min(samples)} "
                          f"random-null={results['random_null'][name]}",
                          flush=True)
            finally:
                agent.close()

            results["agents"][agent_key][str(seed)] = per_bm

    # Split totals
    summary = {}
    for agent_key, seeds_data in results["agents"].items():
        summary[agent_key] = {}
        for seed, per_bm in seeds_data.items():
            for split in ["validation", "test"]:
                rows = {n: r for n, r in per_bm.items() if r["split"] == split}
                key = f"{split}_seed{seed}"
                summary[agent_key][key] = {
                    "argmax_total": sum(r["argmax_ic"] for r in rows.values()),
                    "best_of_k_total": sum(r["best_of_k_ic"] for r in rows.values()),
                    "random_null_total": sum(r["random_best_of_k_ic"]
                                             for r in rows.values()),
                }
    results["summary"] = summary
    results["timestamp"] = datetime.now().isoformat()

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {args.output}", flush=True)

    print("\nSPLIT TOTALS (best-of-k vs argmax vs random-null):")
    for agent_key, rows in summary.items():
        for key, r in sorted(rows.items()):
            print(f"  {agent_key:<14} {key:<20} "
                  f"argmax={r['argmax_total']:>7} "
                  f"best-of-{args.k}={r['best_of_k_total']:>7} "
                  f"null={r['random_null_total']:>7}")


if __name__ == "__main__":
    main()

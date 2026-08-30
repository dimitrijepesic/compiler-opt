#!/usr/bin/env python3
"""
Policy evaluation over the multi-suite battery.

For every battery program (measured by benchmark_battery.py) and every
requested agent/seed, runs one argmax rollout and K sampled rollouts, and
pairs them with the best-of-K random null computed from the episode ICs
already stored in the battery JSONs (same programs, same action space,
same K, a fair null by construction).

Interruption-proof like the battery itself: one JSON per
(suite, agent, seed, program), skipped when present.

Examples:
  python scripts/evaluate_policy_battery.py --agent ppo_autophase
  python scripts/evaluate_policy_battery.py --agent ppo_gnn
  python scripts/evaluate_policy_battery.py --agent ppo_gnn_pretrained --seeds 42 123
  python scripts/evaluate_policy_battery.py --agent ppo_gnn --aggregate
"""

import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime

import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.ppo_autophase import PPOAutophaseAgent
from src.agents.ppo_gnn import PPOGNNAgent

AGENTS = {
    "ppo_autophase": (PPOAutophaseAgent, "results/ppo_autophase", False),
    "ppo_gnn": (PPOGNNAgent, "results/ppo_gnn", True),
    "ppo_gnn_pretrained": (PPOGNNAgent, "results/ppo_gnn_pretrained", True),
}


def sample_rollout(agent, uri, is_gnn, rng_seed, no_dropout=False,
                   open_loop=False):
    torch.manual_seed(rng_seed)
    if is_gnn:
        # Default sampling runs in train mode (encoder dropout active);
        # --no-dropout is the E1b ablation that samples in eval mode.
        (agent.gnn.eval() if no_dropout else agent.gnn.train())
        (agent.policy.eval() if no_dropout else agent.policy.train())
    agent.env.reset(benchmark=uri)
    state = agent._get_graph() if is_gnn else agent._get_state()

    if open_loop:
        # E3: one state, one forward pass; 45 actions sampled i.i.d. from
        # pi(.|s0); the environment is stepped only to apply them.
        with torch.no_grad():
            if is_gnn:
                logits = agent.policy(agent.gnn(state))
            else:
                logits = agent.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(logits=logits)
            for _ in range(agent.max_episode_steps):
                try:
                    agent.env.step(agent.action_map[dist.sample().item()])
                except Exception:
                    continue
        return int(agent.env.observation["IrInstructionCount"])

    for _ in range(agent.max_episode_steps):
        with torch.no_grad():
            if is_gnn:
                logits = agent.policy(agent.gnn(state))
            else:
                logits = agent.policy(state.unsqueeze(0))
            action_idx = torch.distributions.Categorical(
                logits=logits).sample().item()
        try:
            agent.env.step(agent.action_map[action_idx])
        except Exception:
            continue
        state = agent._get_graph() if is_gnn else agent._get_state()

    return int(agent.env.observation["IrInstructionCount"])


def load_battery_programs(battery_dir, max_ic, suites=None):
    """Yield (suite_key, record) for measured programs under the IC cap."""
    for agg in sorted(glob.glob(os.path.join(battery_dir, "*", "_aggregate.json"))):
        suite_key = os.path.basename(os.path.dirname(agg))
        if suites and suite_key not in suites:
            continue
        with open(agg) as f:
            data = json.load(f)
        for r in data["benchmarks"]:
            if "oz" in r and r.get("o0", 10**9) <= max_ic:
                yield suite_key, r


def aggregate(out_dir, agent_key):
    per_suite = {}
    for path in sorted(glob.glob(os.path.join(
            out_dir, "*", f"{agent_key}_seed*", "*.json"))):
        parts = path.replace("\\", "/").split("/")
        suite, seed_dir = parts[-3], parts[-2]
        seed = seed_dir.split("seed")[-1]
        with open(path) as f:
            r = json.load(f)
        bucket = per_suite.setdefault(suite, {}).setdefault(seed, {
            "n": 0, "argmax": 0, "best_of_k": 0, "null_best_of_k": 0, "oz": 0})
        bucket["n"] += 1
        bucket["argmax"] += r["argmax_ic"]
        bucket["best_of_k"] += r["best_of_k_ic"]
        bucket["null_best_of_k"] += r["random_null_best_of_k"]
        bucket["oz"] += r["oz"]

    out = {"agent": agent_key, "timestamp": datetime.now().isoformat(),
           "per_suite": per_suite}
    path = os.path.join(out_dir, f"_aggregate_{agent_key}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Aggregated -> {path}")
    for suite, seeds in per_suite.items():
        for seed, b in sorted(seeds.items()):
            print(f"  {suite:<14} seed {seed:<4} n={b['n']:>3} "
                  f"argmax={b['argmax']:>7} best-of-k={b['best_of_k']:>7} "
                  f"null={b['null_best_of_k']:>7} oz={b['oz']:>7}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, choices=list(AGENTS))
    p.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    p.add_argument("--k", type=int, default=8)
    p.add_argument("--max-ic-policy", type=int, default=6000,
                   help="skip programs larger than this (GNN rollout cost)")
    p.add_argument("--battery-dir", type=str, default="results/battery")
    p.add_argument("--out-dir", type=str, default="results/battery_policy")
    p.add_argument("--aggregate", action="store_true")
    p.add_argument("--suites", type=str, default="",
                   help="comma-separated battery suite dirs to evaluate "
                        "(default: all present)")
    p.add_argument("--untrained", action="store_true",
                   help="E1a control: skip checkpoint loading and evaluate "
                        "the randomly initialized policy (untrained-policy "
                        "null)")
    p.add_argument("--no-dropout", action="store_true",
                   help="E1b ablation: sample with the encoder in eval mode "
                        "(dropout off)")
    p.add_argument("--open-loop", action="store_true",
                   help="E3: sample all 45 actions i.i.d. from pi(.|s0) "
                        "computed once at the initial state")
    args = p.parse_args()

    variant = args.agent \
        + ("_untrained" if args.untrained else "") \
        + ("_nodropout" if args.no_dropout else "") \
        + ("_openloop" if args.open_loop else "")

    if args.aggregate:
        aggregate(args.out_dir, variant)
        return

    agent_class, ckpt_dir, is_gnn = AGENTS[args.agent]
    suites = [x for x in args.suites.split(",") if x] or None
    programs = list(load_battery_programs(args.battery_dir,
                                          args.max_ic_policy, suites))
    print(f"{args.agent}: {len(programs)} eligible programs "
          f"(max-ic {args.max_ic_policy}), k={args.k}", flush=True)

    for seed in args.seeds:
        ckpt = os.path.join(ckpt_dir, f"checkpoint_best_seed{seed}.pt")
        if not args.untrained and not os.path.exists(ckpt):
            print(f"seed {seed}: no checkpoint at {ckpt}, skipping", flush=True)
            continue

        agent = agent_class(seed=seed)
        try:
            if not args.untrained:
                agent.load_checkpoint(ckpt)
            t_start = time.time()
            done = 0
            for i, (suite_key, rec) in enumerate(programs):
                uri = rec["uri"]
                name = os.path.basename(uri.split("/")[-1]) or "unnamed"
                out_sub = os.path.join(args.out_dir, suite_key,
                                       f"{variant}_seed{seed}")
                os.makedirs(out_sub, exist_ok=True)
                out_path = os.path.join(out_sub, f"{name}.json")
                if os.path.exists(out_path):
                    done += 1
                    continue

                try:
                    samples = [
                        sample_rollout(agent, uri, is_gnn,
                                       rng_seed=seed * 100000 + i * 100 + j,
                                       no_dropout=args.no_dropout,
                                       open_loop=args.open_loop)
                        for j in range(args.k)
                    ]
                    _, _, details = agent.evaluate([uri], "ref")
                    argmax_ic = details[0]["final_ic"]
                except Exception as e:
                    print(f"  [{i + 1}/{len(programs)}] {name}: FAILED {e!r}",
                          flush=True)
                    try:
                        agent.env.close()
                    except Exception:
                        pass
                    agent.env = __import__("compiler_gym").make("llvm-ic-v0")
                    continue

                record = {
                    "uri": uri, "suite": suite_key, "seed": seed,
                    "variant": variant,
                    "o0": rec["o0"], "oz": rec["oz"],
                    "argmax_ic": int(argmax_ic),
                    "sample_ics": [int(s) for s in samples],
                    "best_of_k_ic": int(min(samples)),
                    "random_null_best_of_k": int(
                        min(rec["random_reduced_episode_ics"][:args.k])),
                }
                with open(out_path, "w") as f:
                    json.dump(record, f, indent=2)
                done += 1
                if done % 20 == 0:
                    print(f"  [{done}/{len(programs)}] seed {seed} "
                          f"({(time.time() - t_start) / 60:.0f}m)", flush=True)
        finally:
            agent.close()
        print(f"seed {seed} complete "
              f"({(time.time() - t_start) / 60:.0f}m)", flush=True)

    aggregate(args.out_dir, variant)


if __name__ == "__main__":
    main()

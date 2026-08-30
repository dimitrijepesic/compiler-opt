#!/usr/bin/env python3
"""
nullcheck: apply this paper's evaluation protocol to any CompilerGym
benchmark set in one command.

Given a suite (any CompilerGym dataset or generator URI) it reports the
null-model row of Table I (O0/O3/Oz vs. best-of-N random search in the
curated 36-pass space) and, if a trained checkpoint is given, the
Table II row for that suite: best-of-k policy sampling vs. the paired
best-of-k random null, with a one-sided Wilcoxon test, the iso-quality
search budget, and the -Oz-safe per-program gain.

It is a thin composition of benchmark_battery.py's null-model measurement
and evaluate_policy_battery.py's policy sampling; no protocol logic is
reimplemented, so a result from this tool is directly comparable with the
paper's tables.

Examples:
  python scripts/nullcheck.py --suite mibench-v1
  python scripts/nullcheck.py --suite poj104-v1 --sample-n 100 --k 16
  python scripts/nullcheck.py --suite csmith-v0 --sample-n 50 \\
      --agent ppo_gnn --checkpoint results/ppo_gnn/checkpoint_best_seed42.pt

Output: a report on stdout and the per-program records as JSON
(--out, default results/nullcheck_<suite>.json).
"""

import argparse
import itertools
import json
import os
import sys
import time
from datetime import datetime

import numpy as np
import yaml
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

import compiler_gym
from benchmark_battery import measure, resolve_suite, safe_name
from evaluate_policy_battery import sample_rollout

AGENTS = {}


def _agent_class(name):
    if not AGENTS:
        from src.agents.ppo_autophase import PPOAutophaseAgent
        from src.agents.ppo_gnn import PPOGNNAgent
        AGENTS["ppo_autophase"] = (PPOAutophaseAgent, False)
        AGENTS["ppo_gnn"] = (PPOGNNAgent, True)
    return AGENTS[name]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--suite", required=True)
    p.add_argument("--sample-n", type=int, default=0,
                   help="random sample size; 0 = all (finite suites only)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-ic", type=int, default=120000)
    p.add_argument("--max-ic-policy", type=int, default=6000,
                   help="skip programs above this size for policy rollouts")
    p.add_argument("--k", type=int, default=8,
                   help="best-of-k for the policy and its paired null")
    p.add_argument("--agent", choices=["ppo_autophase", "ppo_gnn"])
    p.add_argument("--checkpoint", type=str)
    p.add_argument("--passes", type=str, default="configs/passes.yaml")
    p.add_argument("--out", type=str, default="")
    args = p.parse_args()

    if bool(args.agent) != bool(args.checkpoint):
        raise SystemExit("--agent and --checkpoint must be given together")

    with open(args.passes) as f:
        action_map = [x["action_id"] for x in yaml.safe_load(f)["passes"]]

    suite = resolve_suite(args.suite)
    rng = np.random.default_rng(args.seed)
    env = compiler_gym.make("llvm-ic-v0")

    if suite.startswith("generator://"):
        if not args.sample_n:
            raise SystemExit("--sample-n is required for generator suites")
        uris = list(itertools.islice(env.datasets[suite].benchmark_uris(),
                                     args.sample_n))
    else:
        uris = list(env.datasets[suite].benchmark_uris())
        if args.sample_n and args.sample_n < len(uris):
            idx = rng.choice(len(uris), size=args.sample_n, replace=False)
            uris = [uris[i] for i in sorted(idx)]

    print(f"nullcheck: {suite}, {len(uris)} programs, seed {args.seed}, "
          f"k={args.k}" + (f", agent={args.agent}" if args.agent else ""),
          flush=True)

    agent = None
    is_gnn = False
    if args.agent:
        cls, is_gnn = _agent_class(args.agent)
        agent = cls(seed=args.seed)
        agent.load_checkpoint(args.checkpoint)

    records = []
    t0 = time.time()
    for i, uri in enumerate(uris):
        rec = {"uri": uri}
        rec.update(measure(env, uri, action_map, rng, args.max_ic))
        if "skipped" in rec or "failed" in rec:
            records.append(rec)
            continue

        if agent is not None and rec["o0"] <= args.max_ic_policy:
            try:
                samples = [sample_rollout(agent, uri, is_gnn,
                                          rng_seed=args.seed * 100000 + i * 100 + j)
                          for j in range(args.k)]
                rec["policy_sample_ics"] = [int(s) for s in samples]
                rec["policy_best_of_k"] = int(min(samples))
                rec["null_best_of_k"] = int(
                    min(rec["random_reduced_episode_ics"][:args.k]))
            except Exception as e:
                rec["policy_failed"] = repr(e)

        records.append(rec)
        if (i + 1) % 20 == 0:
            print(f"  [{i + 1}/{len(uris)}] "
                  f"({(time.time() - t0) / 60:.1f}m)", flush=True)

    if agent is not None:
        agent.close()
    env.close()

    ok = [r for r in records if "oz" in r]
    n = len(ok)
    o0, o3, oz = (sum(r[k] for r in ok) for k in ("o0", "o3", "oz"))
    rndN = sum(r["random_reduced_search"] for r in ok)
    dOz = (oz - rndN) / oz * 100 if oz else float("nan")

    print(f"\n=== Table I row: {args.suite} (n={n}) ===")
    print(f"  O0={o0}  O3={o3}  Oz={oz}  Rnd-50={rndN}  dOz={dOz:+.1f}%")

    report = {"suite": suite, "n": n, "seed": args.seed,
             "table_i": {"o0": o0, "o3": o3, "oz": oz, "rnd50": rndN,
                         "dOz_pct": round(dOz, 2)}}

    policy_rows = [r for r in ok if "policy_best_of_k" in r]
    if agent is not None:
        if not policy_rows:
            print(f"\n=== Table II row: {args.suite} ===\n  no eligible "
                  f"programs (<= {args.max_ic_policy} IC)")
        else:
            a = [r["policy_best_of_k"] for r in policy_rows]
            z = [r["null_best_of_k"] for r in policy_rows]
            a_tot, z_tot = sum(a), sum(z)
            oz_tot = sum(r["oz"] for r in policy_rows)
            wins = sum(x < y for x, y in zip(a, z))
            ties = sum(x == y for x, y in zip(a, z))
            nz = sum(1 for x, y in zip(a, z) if x != y)
            p_val = (stats.wilcoxon(a, z, alternative="less").pvalue
                     if nz else float("nan"))
            safe_gain = np.mean([(oz_v - min(a_v, oz_v)) / oz_v
                                 for a_v, oz_v in zip(a, (r["oz"] for r in policy_rows))
                                 if oz_v]) * 100

            def iso_k(eps_list, target, kmax=50):
                for kk in range(1, kmax + 1):
                    if sum(min(r["random_reduced_episode_ics"][:kk])
                          for r in policy_rows) <= target:
                        return kk
                return f">{kmax}"

            iso = iso_k(None, a_tot)
            print(f"\n=== Table II row: {args.suite} (n={len(policy_rows)}, "
                  f"k={args.k}) ===")
            print(f"  Null={z_tot}  -Oz={oz_tot}  Policy={a_tot}  "
                  f"win/tie/loss={wins}/{ties}/{len(a) - wins - ties}  "
                  f"one-sided p={p_val:.2g}  iso-k={iso}  safe%={safe_gain:.1f}")
            report["table_ii"] = {
                "k": args.k, "n": len(policy_rows), "null": z_tot,
                "oz": oz_tot, "policy": a_tot, "wins": wins, "ties": ties,
                "losses": len(a) - wins - ties, "wilcoxon_p": float(p_val),
                "iso_k": iso, "safe_pct": round(float(safe_gain), 2),
            }

    out_path = args.out or f"results/nullcheck_{args.suite.replace('://', '_')}.json"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    report["timestamp"] = datetime.now().isoformat()
    report["programs"] = records
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nSaved -> {out_path}")


if __name__ == "__main__":
    main()

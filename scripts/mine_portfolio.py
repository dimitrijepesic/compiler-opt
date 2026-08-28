#!/usr/bin/env python3
"""
Portfolio null (E4, REVIEW_2026-08-28.md section 7.3): a fixed set of
pass sequences mined from random search on the cBench TRAINING split
only -- no learning, no held-out data. Tests whether a learned sampler
carries more than a fixed sequence list (the premise behind coreset-
style approaches).

Stages (run in order; each is interruption-proof):
  mine    50 random 45-step episodes on each of the 14 train programs,
          recording the action sequence and final IC
          -> results/portfolio_mining.json
  select  cross-evaluate the top-3 sequences per program on all 14
          train programs, then greedy set-cover: repeatedly add the
          sequence that most reduces the summed per-program minimum.
          Selection order makes portfolios nested (first 8 = the
          8-sequence portfolio).
          -> results/portfolio_selection.json
  eval    apply the 16 selected sequences to every battery program
          under the IC cap; per-program JSON like the policy eval
          -> results/portfolio_eval/<suite>/portfolio_seed0/<name>.json

Mining RNG seed is fixed at 7 (pre-registered before any results).
"""

import argparse
import glob
import json
import os
import sys
import time

import numpy as np
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import compiler_gym

EPISODE_STEPS = 45
MINE_EPISODES = 50
TOP_PER_PROGRAM = 3
PORTFOLIO_SIZE = 16
MINE_SEED = 7

ORIG_SUITES = ["blas-v0", "chstone-v0", "csmith-v0",
               "mibench-v1", "npb-v0", "poj104-v1"]


def load_action_map():
    with open("configs/passes.yaml") as f:
        return [x["action_id"] for x in yaml.safe_load(f)["passes"]]


def load_train_uris():
    with open("configs/benchmarks.yaml") as f:
        return yaml.safe_load(f)["train"]


def run_sequence(env, uri, action_ids):
    env.reset(benchmark=uri)
    for a in action_ids:
        try:
            env.step(a)
        except Exception:
            continue
    return int(env.observation["IrInstructionCount"])


def mine(env, action_map):
    rng = np.random.default_rng(MINE_SEED)
    out = {"seed": MINE_SEED, "episodes": {}}
    path = "results/portfolio_mining.json"
    for uri in load_train_uris():
        eps = []
        t0 = time.time()
        for _ in range(MINE_EPISODES):
            idxs = rng.integers(0, len(action_map), EPISODE_STEPS)
            seq = [action_map[i] for i in idxs]
            ic = run_sequence(env, uri, seq)
            eps.append({"actions": seq, "final_ic": ic})
        out["episodes"][uri] = eps
        best = min(e["final_ic"] for e in eps)
        print(f"  {uri}: best {best} "
              f"({time.time() - t0:.0f}s)", flush=True)
        with open(path, "w") as f:
            json.dump(out, f)
    print(f"-> {path}")


def select(env, action_map):
    with open("results/portfolio_mining.json") as f:
        mined = json.load(f)["episodes"]
    uris = list(mined)
    # candidate pool: top sequences per program
    cands = []
    for uri, eps in mined.items():
        for e in sorted(eps, key=lambda x: x["final_ic"])[:TOP_PER_PROGRAM]:
            cands.append({"origin": uri, "actions": e["actions"],
                          "origin_ic": e["final_ic"]})
    print(f"{len(cands)} candidates x {len(uris)} programs", flush=True)
    # cross matrix
    M = np.zeros((len(cands), len(uris)), dtype=np.int64)
    for ci, c in enumerate(cands):
        for pi, uri in enumerate(uris):
            M[ci, pi] = run_sequence(env, uri, c["actions"])
        print(f"  candidate {ci + 1}/{len(cands)} "
              f"(origin {c['origin'].split('/')[-1]})", flush=True)
    # greedy set-cover on summed per-program minima
    chosen = []
    best = np.full(len(uris), np.iinfo(np.int64).max)
    for _ in range(min(PORTFOLIO_SIZE, len(cands))):
        totals = [np.minimum(best, M[ci]).sum() if ci not in chosen
                  else np.iinfo(np.int64).max for ci in range(len(cands))]
        ci = int(np.argmin(totals))
        chosen.append(ci)
        best = np.minimum(best, M[ci])
    out = {"portfolio": [
        {"rank": r + 1, "origin": cands[ci]["origin"],
         "actions": cands[ci]["actions"],
         "train_total_after": int(np.minimum.reduce(
             [M[c] for c in chosen[:r + 1]]).sum())}
        for r, ci in enumerate(chosen)],
        "train_uris": uris}
    path = "results/portfolio_selection.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    for e in out["portfolio"]:
        print(f"  rank {e['rank']:>2} from {e['origin'].split('/')[-1]:<14}"
              f" train total {e['train_total_after']}")
    print(f"-> {path}")


def evaluate(env, max_ic):
    with open("results/portfolio_selection.json") as f:
        seqs = [e["actions"] for e in json.load(f)["portfolio"]]
    programs = []
    for agg in sorted(glob.glob("results/battery/*/_aggregate.json")):
        suite = os.path.basename(os.path.dirname(agg))
        if suite not in ORIG_SUITES:
            continue
        with open(agg) as f:
            for r in json.load(f)["benchmarks"]:
                if "oz" in r and r.get("o0", 10**9) <= max_ic:
                    programs.append((suite, r))
    print(f"{len(programs)} programs x {len(seqs)} sequences", flush=True)
    t0 = time.time()
    for i, (suite, rec) in enumerate(programs):
        name = os.path.basename(rec["uri"].split("/")[-1]) or "unnamed"
        out_sub = os.path.join("results/portfolio_eval", suite,
                               "portfolio_seed0")
        os.makedirs(out_sub, exist_ok=True)
        out_path = os.path.join(out_sub, f"{name}.json")
        if os.path.exists(out_path):
            continue
        ics = [run_sequence(env, rec["uri"], seq) for seq in seqs]
        record = {
            "uri": rec["uri"], "suite": suite, "variant": "portfolio",
            "o0": rec["o0"], "oz": rec["oz"],
            "sample_ics": [int(x) for x in ics],
            "best_of_8_ic": int(min(ics[:8])),
            "best_of_16_ic": int(min(ics)),
            "random_null_best_of_8": int(
                min(rec["random_reduced_episode_ics"][:8])),
            "random_null_best_of_16": int(
                min(rec["random_reduced_episode_ics"][:16])),
        }
        with open(out_path, "w") as f:
            json.dump(record, f, indent=2)
        if (i + 1) % 20 == 0:
            print(f"  [{i + 1}/{len(programs)}] "
                  f"({(time.time() - t0) / 60:.0f}m)", flush=True)
    print("portfolio eval complete", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=["mine", "select", "eval"])
    p.add_argument("--max-ic-policy", type=int, default=6000)
    args = p.parse_args()
    env = compiler_gym.make("llvm-ic-v0")
    try:
        if args.stage == "mine":
            mine(env, load_action_map())
        elif args.stage == "select":
            select(env, load_action_map())
        else:
            evaluate(env, args.max_ic_policy)
    finally:
        env.close()


if __name__ == "__main__":
    main()

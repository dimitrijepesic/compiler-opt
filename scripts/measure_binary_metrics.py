#!/usr/bin/env python3
"""
Binary-level metrics over the battery: .text bytes, total object
footprint (text+data+bss), and sequence application time.

Conditions per program:
  o0        baseline module
  oz        opt -Oz            (sizes + timed opt run)
  rnd_bo8   best of 8 random 45-step episodes in the 36-pass space
            (selected by final IC, replayed in-env for the module,
             timed via the equivalent opt CLI invocation)
  gnn_bo8   best of 8 sampled rollouts of the GNN policy (median seed),
            same selection/replay/timing; only for programs with
            O0 IC <= --max-ic-policy (rollout cost)

Sizes come from the CompilerGym runtime's own llc + llvm-size
(version-matched LLVM 10). Timing is the median of 3 runs of the
runtime's opt binary applying the pass flags directly - this also
demonstrates the sequences work outside the gym.

Resumable per program. Output: results/binary_metrics/<suite>/<name>.json
plus _aggregate.json via --aggregate.
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime

import numpy as np
import torch
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import compiler_gym
from src.agents.ppo_gnn import PPOGNNAgent

LLVM_BIN = os.path.expanduser("~/.local/share/compiler_gym/llvm-v0/bin")
EPISODE_STEPS = 45
K = 8


def sizes(bc_path, workdir):
    obj = os.path.join(workdir, "out.o")
    subprocess.run([os.path.join(LLVM_BIN, "llc"), "-filetype=obj",
                    "-o", obj, bc_path], check=True, capture_output=True)
    out = subprocess.run([os.path.join(LLVM_BIN, "llvm-size"), obj],
                         check=True, capture_output=True, text=True).stdout
    parts = out.strip().splitlines()[1].split()
    text, data, bss = int(parts[0]), int(parts[1]), int(parts[2])
    return {"text": text, "total": text + data + bss}


def timed_opt(flags, in_bc, out_bc, runs=3):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        subprocess.run([os.path.join(LLVM_BIN, "opt")] + flags
                       + [in_bc, "-o", out_bc],
                       check=True, capture_output=True)
        times.append((time.perf_counter() - t0) * 1000)
    return round(float(np.median(times)), 1)


def run_episode(env, uri, actions):
    env.reset(benchmark=uri)
    applied = []
    for a in actions:
        try:
            env.step(a)
            applied.append(a)
        except Exception:
            break
    return int(env.observation["IrInstructionCount"]), applied


def gnn_sample_actions(agent, uri, rng_seed):
    torch.manual_seed(rng_seed)
    agent.env.reset(benchmark=uri)
    graph = agent._get_graph()
    actions = []
    for _ in range(agent.max_episode_steps):
        with torch.no_grad():
            logits = agent.policy(agent.gnn(graph))
            idx = torch.distributions.Categorical(logits=logits).sample().item()
        a = agent.action_map[idx]
        try:
            agent.env.step(a)
            actions.append(a)
        except Exception:
            continue
        graph = agent._get_graph()
    return int(agent.env.observation["IrInstructionCount"]), actions


def aggregate(out_dir):
    rows = []
    for path in sorted(glob.glob(os.path.join(out_dir, "*", "*.json"))):
        if os.path.basename(path).startswith("_"):
            continue
        with open(path) as f:
            rows.append(json.load(f))

    def totals(cond, key):
        return sum(r[cond][key] for r in rows if cond in r)

    summary = {"n_programs": len(rows), "timestamp": datetime.now().isoformat()}
    for cond in ["o0", "oz", "rnd_bo8", "gnn_bo8"]:
        n = sum(1 for r in rows if cond in r)
        if not n:
            continue
        summary[cond] = {
            "n": n,
            "text_total": totals(cond, "text"),
            "footprint_total": totals(cond, "total"),
        }
        if cond != "o0":
            times = [r[cond]["opt_ms"] for r in rows
                     if cond in r and "opt_ms" in r[cond]]
            if times:
                summary[cond]["opt_ms_median"] = round(
                    float(np.median(times)), 1)
    # paired subsets for honest comparisons
    both = [r for r in rows if "gnn_bo8" in r]
    if both:
        summary["paired_gnn_subset"] = {
            "n": len(both),
            "oz_text": sum(r["oz"]["text"] for r in both),
            "rnd_text": sum(r["rnd_bo8"]["text"] for r in both),
            "gnn_text": sum(r["gnn_bo8"]["text"] for r in both),
        }
    path = os.path.join(out_dir, "_aggregate.json")
    with open(path, "w") as f:
        json.dump({"summary": summary, "programs": rows}, f, indent=2)
    print(json.dumps(summary, indent=1))
    print(f"Saved: {path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--battery-dir", type=str, default="results/battery")
    p.add_argument("--out-dir", type=str, default="results/binary_metrics")
    p.add_argument("--gnn-seed", type=int, default=123,
                   help="GNN checkpoint seed used for gnn_bo8 (cBench median)")
    p.add_argument("--max-ic-policy", type=int, default=6000)
    p.add_argument("--max-ic", type=int, default=120000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--aggregate", action="store_true")
    args = p.parse_args()

    if args.aggregate:
        aggregate(args.out_dir)
        return

    with open("configs/passes.yaml") as f:
        passes = yaml.safe_load(f)["passes"]
    action_map = [x["action_id"] for x in passes]
    id_to_flag = {x["action_id"]: x["name"] for x in passes}

    programs = []
    for agg in sorted(glob.glob(os.path.join(args.battery_dir, "*",
                                             "_aggregate.json"))):
        suite_key = os.path.basename(os.path.dirname(agg))
        with open(agg) as f:
            for r in json.load(f)["benchmarks"]:
                if "oz" in r and r.get("o0", 10**9) <= args.max_ic:
                    programs.append((suite_key, r["uri"], r["o0"]))
    print(f"{len(programs)} programs", flush=True)

    rng = np.random.default_rng(args.seed)
    agent = PPOGNNAgent(seed=args.gnn_seed)
    ckpt = f"results/ppo_gnn/checkpoint_best_seed{args.gnn_seed}.pt"
    agent.load_checkpoint(ckpt)
    env = agent.env  # reuse the agent's env for everything

    t_start = time.time()
    with tempfile.TemporaryDirectory() as workdir:
        for i, (suite_key, uri, o0_ic) in enumerate(programs):
            name = uri.split("/")[-1] or "unnamed"
            out_sub = os.path.join(args.out_dir, suite_key)
            os.makedirs(out_sub, exist_ok=True)
            out_path = os.path.join(out_sub, f"{name}.json")
            if os.path.exists(out_path):
                continue

            try:
                record = {"uri": uri, "suite": suite_key}

                env.reset(benchmark=uri)
                o0_bc = os.path.join(workdir, "o0.bc")
                env.write_bitcode(o0_bc)
                record["o0"] = {"ic": o0_ic, **sizes(o0_bc, workdir)}

                oz_bc = os.path.join(workdir, "oz.bc")
                oz_ms = timed_opt(["-Oz"], o0_bc, oz_bc)
                env.reset(benchmark=uri)
                record["oz"] = {
                    "ic": int(env.observation["IrInstructionCountOz"]),
                    **sizes(oz_bc, workdir), "opt_ms": oz_ms}

                # random best-of-8 (by IC), replay best, export, time CLI
                best = None
                for _ in range(K):
                    acts = [int(action_map[rng.integers(len(action_map))])
                            for _ in range(EPISODE_STEPS)]
                    ic, applied = run_episode(env, uri, acts)
                    if best is None or ic < best[0]:
                        best = (ic, applied)
                ic, applied = run_episode(env, uri, best[1])
                rnd_bc = os.path.join(workdir, "rnd.bc")
                env.write_bitcode(rnd_bc)
                flags = [id_to_flag[a] for a in applied]
                record["rnd_bo8"] = {
                    "ic": ic, **sizes(rnd_bc, workdir),
                    "opt_ms": timed_opt(flags, o0_bc,
                                        os.path.join(workdir, "x.bc"))}

                if o0_ic <= args.max_ic_policy:
                    best = None
                    for j in range(K):
                        ic, acts = gnn_sample_actions(
                            agent, uri, rng_seed=args.gnn_seed * 7919 + i * 100 + j)
                        if best is None or ic < best[0]:
                            best = (ic, acts)
                    ic, applied = run_episode(env, uri, best[1])
                    gnn_bc = os.path.join(workdir, "gnn.bc")
                    env.write_bitcode(gnn_bc)
                    flags = [id_to_flag[a] for a in applied]
                    record["gnn_bo8"] = {
                        "ic": ic, **sizes(gnn_bc, workdir),
                        "opt_ms": timed_opt(flags, o0_bc,
                                            os.path.join(workdir, "x.bc"))}

                with open(out_path, "w") as f:
                    json.dump(record, f, indent=2)
                msg = (f"[{i + 1}/{len(programs)}] {name}: "
                       f"oz_text={record['oz']['text']} "
                       f"rnd_text={record['rnd_bo8']['text']}")
                if "gnn_bo8" in record:
                    msg += f" gnn_text={record['gnn_bo8']['text']}"
                print(msg + f" ({(time.time() - t_start) / 60:.0f}m)",
                      flush=True)
            except Exception as e:
                print(f"[{i + 1}/{len(programs)}] {name}: FAILED {e!r}",
                      flush=True)
                try:
                    env.close()
                except Exception:
                    pass
                agent.env = compiler_gym.make("llvm-ic-v0")
                env = agent.env

    agent.close()
    aggregate(args.out_dir)


if __name__ == "__main__":
    main()

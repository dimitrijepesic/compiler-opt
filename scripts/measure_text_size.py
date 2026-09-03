#!/usr/bin/env python3
"""
IC -> .text sanity anchor.

For a subset of programs, measures actual .text section size (bytes) of
the compiled object under three conditions: O0, opt -Oz, and the best of
N random episodes in the 36-pass space. Reports the correlation between
relative IC reduction and relative .text reduction: the one number that
defuses "IR instruction count is just a proxy".

Uses the CompilerGym runtime's own llc/llvm-size (version-matched to the
generated bitcode).

Output: results/text_size_anchor.json
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

import numpy as np
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import compiler_gym

LLVM_BIN = os.path.expanduser("~/.local/share/compiler_gym/llvm-v0/bin")
RANDOM_EPISODES = 10
EPISODE_STEPS = 45


def text_size(bc_path, workdir):
    obj = os.path.join(workdir, "out.o")
    subprocess.run([os.path.join(LLVM_BIN, "llc"), "-filetype=obj",
                    "-o", obj, bc_path], check=True, capture_output=True)
    out = subprocess.run([os.path.join(LLVM_BIN, "llvm-size"), obj],
                         check=True, capture_output=True, text=True).stdout
    # header line, then: text data bss dec hex filename
    return int(out.strip().splitlines()[1].split()[0])


def measure_program(env, uri, action_map, rng, workdir):
    rows = {}

    # O0
    env.reset(benchmark=uri)
    ic0 = int(env.observation["IrInstructionCount"])
    bc = os.path.join(workdir, "m.bc")
    env.write_bitcode(bc)
    rows["o0"] = {"ic": ic0, "text": text_size(bc, workdir)}

    # opt -Oz on the O0 module
    oz_bc = os.path.join(workdir, "oz.bc")
    subprocess.run([os.path.join(LLVM_BIN, "opt"), "-Oz", bc, "-o", oz_bc],
                   check=True, capture_output=True)
    # The Oz module's IC is the env's IrInstructionCountOz observation.
    env.reset(benchmark=uri)
    rows["oz"] = {"ic": int(env.observation["IrInstructionCountOz"]),
                  "text": text_size(oz_bc, workdir)}

    # Best of N random episodes (replay best action sequence, then export)
    best = None
    for _ in range(RANDOM_EPISODES):
        env.reset(benchmark=uri)
        actions = []
        for _ in range(EPISODE_STEPS):
            a = int(action_map[rng.integers(len(action_map))])
            try:
                env.step(a)
                actions.append(a)
            except Exception:
                break
        ic = int(env.observation["IrInstructionCount"])
        if best is None or ic < best[0]:
            best = (ic, actions)

    env.reset(benchmark=uri)
    for a in best[1]:
        try:
            env.step(a)
        except Exception:
            break
    rnd_bc = os.path.join(workdir, "rnd.bc")
    env.write_bitcode(rnd_bc)
    rows["random36_best"] = {
        "ic": int(env.observation["IrInstructionCount"]),
        "text": text_size(rnd_bc, workdir),
    }
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mibench-n", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="results/text_size_anchor.json")
    args = parser.parse_args()

    with open("configs/passes.yaml") as f:
        action_map = [x["action_id"] for x in yaml.safe_load(f)["passes"]]
    with open("configs/benchmarks.yaml") as f:
        bm = yaml.safe_load(f)

    rng = np.random.default_rng(args.seed)
    env = compiler_gym.make("llvm-ic-v0")

    uris = list(bm["validation"]) + list(bm["test"])
    chstone = list(env.datasets["benchmark://chstone-v0"].benchmark_uris())
    mib = list(env.datasets["benchmark://mibench-v1"].benchmark_uris())
    idx = rng.choice(len(mib), size=min(args.mibench_n, len(mib)),
                     replace=False)
    uris += chstone + [mib[i] for i in sorted(idx)]

    results = []
    with tempfile.TemporaryDirectory() as workdir:
        for i, uri in enumerate(uris):
            name = uri.split("/")[-1]
            try:
                rows = measure_program(env, uri, action_map, rng, workdir)
            except Exception as e:
                print(f"[{i + 1}/{len(uris)}] {name}: FAILED {e!r}",
                      flush=True)
                continue
            results.append({"uri": uri, "conditions": rows})
            print(f"[{i + 1}/{len(uris)}] {name}: "
                  + " ".join(f"{c}: ic={v['ic']} text={v['text']}"
                             for c, v in rows.items()),
                  flush=True)
    env.close()

    # Correlation: relative reduction O0->X in IC vs in .text
    ic_deltas, text_deltas = [], []
    for r in results:
        o0 = r["conditions"]["o0"]
        for cond in ["oz", "random36_best"]:
            c = r["conditions"][cond]
            if o0["ic"] > 0 and o0["text"] > 0:
                ic_deltas.append(1 - c["ic"] / o0["ic"])
                text_deltas.append(1 - c["text"] / o0["text"])

    from scipy import stats as st
    pearson = st.pearsonr(ic_deltas, text_deltas)
    spearman = st.spearmanr(ic_deltas, text_deltas)

    out = {
        "timestamp": datetime.now().isoformat(),
        "n_programs": len(results),
        "n_points": len(ic_deltas),
        "pearson_r": round(float(pearson[0]), 4),
        "pearson_p": float(pearson[1]),
        "spearman_r": round(float(spearman[0]), 4),
        "spearman_p": float(spearman[1]),
        "programs": results,
    }
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nIC vs .text relative reduction: Pearson r={out['pearson_r']} "
          f"(p={out['pearson_p']:.1e}), Spearman rho={out['spearman_r']}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()

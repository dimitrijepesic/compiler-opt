#!/usr/bin/env python3
"""
Multi-suite benchmark battery: baselines + random null models per program.

Designed to be interruption-proof (Colab sessions, reboots): every program
writes its own JSON under <out-dir>/<suite>/<name>.json and is skipped on
the next run if that file already exists. Aggregate afterwards with
--aggregate.

Per program it records:
  o0, o3, oz          real instruction counts (IrInstructionCount[O3|Oz])
  random_reduced      null models in the 36-pass space:
                        policy: mean/std/min of POLICY_TRIALS single episodes
                        search: best of SEARCH_EPISODES episodes
  episode ICs         raw per-episode finals (for best-of-k nulls later)

Examples:
  python scripts/benchmark_battery.py --suite mibench-v1
  python scripts/benchmark_battery.py --suite poj104-v1 --sample-n 100
  python scripts/benchmark_battery.py --suite csmith-v0 --sample-n 50
  python scripts/benchmark_battery.py --suite mibench-v1 --aggregate
"""

import argparse
import itertools
import json
import os
import re
import sys
import time
from datetime import datetime

import numpy as np
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import compiler_gym

POLICY_TRIALS = 20
SEARCH_EPISODES = 50
EPISODE_STEPS = 45


def resolve_suite(name):
    if "://" in name:
        return name
    if name.startswith("csmith") or name.startswith("llvm-stress"):
        return f"generator://{name}"
    return f"benchmark://{name}"


def safe_name(uri):
    return re.sub(r"[^A-Za-z0-9._-]", "_", uri.split("/")[-1]) or "unnamed"


def measure(env, uri, action_map, rng, max_ic):
    env.reset(benchmark=uri)
    o0 = int(env.observation["IrInstructionCount"])
    if o0 > max_ic:
        return {"skipped": f"o0 IC {o0} > max-ic {max_ic}", "o0": o0}

    o3 = int(env.observation["IrInstructionCountO3"])
    oz = int(env.observation["IrInstructionCountOz"])

    finals = []
    for _ in range(max(POLICY_TRIALS, SEARCH_EPISODES)):
        env.reset(benchmark=uri)
        for _ in range(EPISODE_STEPS):
            try:
                env.step(action_map[rng.integers(len(action_map))])
            except Exception:
                break
        finals.append(int(env.observation["IrInstructionCount"]))

    policy_sample = finals[:POLICY_TRIALS]
    return {
        "o0": o0, "o3": o3, "oz": oz,
        "random_reduced_policy": {
            "mean": round(float(np.mean(policy_sample)), 1),
            "std": round(float(np.std(policy_sample)), 1),
            "min": int(np.min(policy_sample)),
        },
        "random_reduced_search": int(np.min(finals[:SEARCH_EPISODES])),
        "random_reduced_episode_ics": finals,
    }


def aggregate(suite_dir, suite):
    rows = []
    for f in sorted(os.listdir(suite_dir)):
        if f.endswith(".json") and f != "_aggregate.json":
            with open(os.path.join(suite_dir, f)) as fh:
                rows.append(json.load(fh))
    ok = [r for r in rows if "oz" in r]
    out = {
        "suite": suite,
        "timestamp": datetime.now().isoformat(),
        "num_measured": len(ok),
        "num_skipped_or_failed": len(rows) - len(ok),
        "totals": {
            k: sum(r[k] for r in ok) for k in ["o0", "o3", "oz"]
        } | {
            "random_reduced_search": sum(r["random_reduced_search"] for r in ok),
            "random_reduced_policy_mean": round(
                sum(r["random_reduced_policy"]["mean"] for r in ok), 1),
        },
        "benchmarks": rows,
    }
    path = os.path.join(suite_dir, "_aggregate.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Aggregated {len(ok)} measured ({len(rows) - len(ok)} skipped/failed) "
          f"-> {path}")
    if ok:
        t = out["totals"]
        print(f"  totals: O0={t['o0']} O3={t['o3']} Oz={t['oz']} "
              f"RndRed50={t['random_reduced_search']}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--suite", required=True,
                   help="e.g. mibench-v1, chstone-v0, csmith-v0")
    p.add_argument("--sample-n", type=int, default=0,
                   help="random sample size; 0 = all (finite suites only)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-ic", type=int, default=120000,
                   help="skip programs with O0 IC above this")
    p.add_argument("--out-dir", type=str, default="results/battery")
    p.add_argument("--passes", type=str, default="configs/passes.yaml")
    p.add_argument("--aggregate", action="store_true",
                   help="only aggregate existing per-program files")
    args = p.parse_args()

    suite = resolve_suite(args.suite)
    suite_dir = os.path.join(args.out_dir, args.suite.replace("://", "_"))
    os.makedirs(suite_dir, exist_ok=True)

    if args.aggregate:
        aggregate(suite_dir, suite)
        return

    with open(args.passes) as f:
        action_map = [x["action_id"] for x in yaml.safe_load(f)["passes"]]

    rng = np.random.default_rng(args.seed)
    env = compiler_gym.make("llvm-ic-v0")
    dataset = env.datasets[suite]

    if suite.startswith("generator://"):
        if not args.sample_n:
            raise SystemExit("--sample-n is required for generator suites")
        uris = list(itertools.islice(dataset.benchmark_uris(), args.sample_n))
    else:
        uris = list(dataset.benchmark_uris())
        if args.sample_n and args.sample_n < len(uris):
            idx = rng.choice(len(uris), size=args.sample_n, replace=False)
            uris = [uris[i] for i in sorted(idx)]

    print(f"Suite {suite}: {len(uris)} programs "
          f"(seed {args.seed}, max-ic {args.max_ic})", flush=True)

    done = skipped = failed = 0
    t_start = time.time()
    for i, uri in enumerate(uris):
        out_path = os.path.join(suite_dir, f"{safe_name(uri)}.json")
        if os.path.exists(out_path):
            done += 1
            continue

        t0 = time.time()
        record = {"uri": uri, "suite": suite,
                  "timestamp": datetime.now().isoformat()}
        try:
            record.update(measure(env, uri, action_map, rng, args.max_ic))
        except Exception as e:
            record["failed"] = repr(e)
            # A dead service can poison later benchmarks; recreate.
            try:
                env.close()
            except Exception:
                pass
            env = compiler_gym.make("llvm-ic-v0")

        with open(out_path, "w") as f:
            json.dump(record, f, indent=2)

        if "failed" in record:
            failed += 1
            tag = "FAILED"
        elif "skipped" in record:
            skipped += 1
            tag = "skipped"
        else:
            done += 1
            tag = f"Oz={record['oz']} RndRed50={record['random_reduced_search']}"
        print(f"[{i + 1}/{len(uris)}] {safe_name(uri)}: {tag} "
              f"({time.time() - t0:.0f}s, total {(time.time() - t_start) / 60:.0f}m)",
              flush=True)

    env.close()
    print(f"\nDone: {done} measured/existing, {skipped} skipped, {failed} failed",
          flush=True)
    aggregate(suite_dir, suite)


if __name__ == "__main__":
    main()

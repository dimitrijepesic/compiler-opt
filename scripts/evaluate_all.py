#!/usr/bin/env python3
"""
Final evaluation: trained agents vs baselines on the FULL declared
validation split and the held-out test split.

- Baselines come from results/full_baselines_v2.json (real -O3/-Oz via
  IrInstructionCountO3/Oz observations, greedy, random over the full
  action space, and random null models in the reduced 36-pass space).
- Agents are evaluated from their best checkpoints for every seed that
  has one; per-seed results are reported, plus mean/std, bootstrap CI,
  and a paired Wilcoxon test between the two agents.

Output: results/final_evaluation.json
"""

import sys
import os
import json
import argparse
import numpy as np
import yaml
from datetime import datetime
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.ppo_autophase import PPOAutophaseAgent
from src.agents.ppo_gnn import PPOGNNAgent

METHOD_LABELS = {
    "o0": "O0", "o3": "O3 (real)", "oz": "Oz (real)", "o3_seq": "O3-seq",
    "greedy": "Greedy", "random": "Rnd-full",
    "random_reduced_policy": "RndRed-1ep", "random_reduced_search": "RndRed-50",
    "ppo_autophase": "PPO+AP", "ppo_gnn": "PPO+GNN",
}


def geometric_mean_ratio(method_ics, baseline_ics):
    """Geometric mean of per-benchmark baseline/method ratios (>1 = better)."""
    ratios = [b / m for m, b in zip(method_ics, baseline_ics) if m > 0 and b > 0]
    if not ratios:
        return 1.0
    return float(np.exp(np.mean(np.log(ratios))))


def bootstrap_ci(data, n_bootstrap=10000, ci=0.95, seed=42):
    rng = np.random.RandomState(seed)
    data = np.array(data, dtype=float)
    means = [
        np.mean(rng.choice(data, size=len(data), replace=True))
        for _ in range(n_bootstrap)
    ]
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return float(lower), float(upper)


def evaluate_agent_all_seeds(agent_class, checkpoint_dir, seeds, uris, label):
    """Evaluate every seed that has a best (or final) checkpoint."""
    runs = []
    for seed in seeds:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_best_seed{seed}.pt")
        if not os.path.exists(ckpt_path):
            ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_final_seed{seed}.pt")
        if not os.path.exists(ckpt_path):
            print(f"  [{label}] seed {seed}: no checkpoint, skipping")
            continue

        agent = agent_class(seed=seed)
        try:
            agent.load_checkpoint(ckpt_path)
            total_ic, reduction, details = agent.evaluate(uris, "final")
        finally:
            agent.close()

        print(f"  [{label}] seed {seed}: total IC {total_ic} "
              f"({reduction:.2f}% reduction)")
        runs.append({
            "seed": seed,
            "checkpoint": os.path.basename(ckpt_path),
            "total_ic": int(total_ic),
            "reduction_pct": round(float(reduction), 2),
            "ics": [d["final_ic"] for d in details],
            "details": details,
        })
    return runs


def summarize_runs(runs):
    if not runs:
        return None
    totals = [r["total_ic"] for r in runs]
    summary = {
        "seeds": [r["seed"] for r in runs],
        "total_ics": totals,
        "mean_total_ic": round(float(np.mean(totals)), 1),
        "std_total_ic": round(float(np.std(totals)), 1),
    }
    if len(totals) >= 2:
        lo, hi = bootstrap_ci(totals)
        summary["bootstrap_ci_95"] = [round(lo, 1), round(hi, 1)]
    # Median seed (by total IC) is used for per-benchmark comparisons
    runs_sorted = sorted(runs, key=lambda r: r["total_ic"])
    summary["median_seed"] = runs_sorted[len(runs_sorted) // 2]["seed"]
    return summary


def median_run(runs):
    runs_sorted = sorted(runs, key=lambda r: r["total_ic"])
    return runs_sorted[len(runs_sorted) // 2]


def print_split_table(split_name, uris, baselines, agent_runs):
    """Per-benchmark table + geomean-vs-real-O3 row for one split."""
    baseline_methods = ["o0", "o3", "oz", "greedy", "random",
                        "random_reduced_search"]
    agent_methods = [m for m in ["ppo_autophase", "ppo_gnn"] if agent_runs.get(m)]

    print(f"\n{'=' * 90}")
    print(f"{split_name.upper()} SPLIT")
    print(f"{'=' * 90}")

    header = f"{'Benchmark':<15}"
    for m in baseline_methods + agent_methods:
        header += f" {METHOD_LABELS[m]:>10}"
    print(header)
    print("-" * len(header))

    columns = {}
    for m in baseline_methods:
        columns[m] = []
        for uri in uris:
            name = uri.split("/")[-1]
            columns[m].append(int(baselines[name][m]))
    for m in agent_methods:
        columns[m] = median_run(agent_runs[m])["ics"]

    for i, uri in enumerate(uris):
        row = f"{uri.split('/')[-1]:<15}"
        for m in baseline_methods + agent_methods:
            row += f" {columns[m][i]:>10}"
        print(row)

    print("-" * len(header))
    totals_row = f"{'TOTAL':<15}"
    for m in baseline_methods + agent_methods:
        totals_row += f" {sum(columns[m]):>10}"
    print(totals_row)

    o3_ics = columns["o3"]
    geo_row = f"{'Geo vs O3':<15}"
    geomeans = {}
    for m in baseline_methods + agent_methods:
        gm = geometric_mean_ratio(columns[m], o3_ics)
        geomeans[m] = gm
        geo_row += f" {(gm - 1) * 100:>+9.2f}%"
    print(geo_row)

    return columns, geomeans


def main():
    parser = argparse.ArgumentParser(description="Final evaluation on val+test")
    parser.add_argument("--baselines", type=str,
                        default="results/full_baselines_v2.json")
    parser.add_argument("--ppo-ap-dir", type=str, default="results/ppo_autophase")
    parser.add_argument("--ppo-gnn-dir", type=str, default="results/ppo_gnn")
    parser.add_argument("--benchmarks", type=str, default="configs/benchmarks.yaml")
    parser.add_argument("--output", type=str, default="results/final_evaluation.json")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 456])
    args = parser.parse_args()

    with open(args.benchmarks) as f:
        bm_config = yaml.safe_load(f)
    val_uris = bm_config["validation"]
    test_uris = bm_config["test"]

    with open(args.baselines) as f:
        baselines_data = json.load(f)
    baselines = {e["short_name"]: e for e in baselines_data["baselines"]}
    # Flatten the random_reduced_policy dict to its mean for table use
    for e in baselines.values():
        if isinstance(e.get("random_reduced_policy"), dict):
            e["random_reduced_policy"] = e["random_reduced_policy"]["mean"]

    print("=" * 90)
    print("FINAL EVALUATION (full validation split + held-out test split)")
    print("=" * 90)

    agent_runs = {"validation": {}, "test": {}}
    for split_name, uris in [("validation", val_uris), ("test", test_uris)]:
        print(f"\nEvaluating agents on {split_name} "
              f"({[u.split('/')[-1] for u in uris]})")
        agent_runs[split_name]["ppo_autophase"] = evaluate_agent_all_seeds(
            PPOAutophaseAgent, args.ppo_ap_dir, args.seeds, uris, "PPO+AP")
        agent_runs[split_name]["ppo_gnn"] = evaluate_agent_all_seeds(
            PPOGNNAgent, args.ppo_gnn_dir, args.seeds, uris, "PPO+GNN")

    output = {
        "timestamp": datetime.now().isoformat(),
        "baselines_file": args.baselines,
        "splits": {},
    }

    for split_name, uris in [("validation", val_uris), ("test", test_uris)]:
        columns, geomeans = print_split_table(
            split_name, uris, baselines, agent_runs[split_name])

        split_out = {
            "benchmarks": [u.split("/")[-1] for u in uris],
            "method_ics": {m: [int(v) for v in ics] for m, ics in columns.items()},
            "geomean_vs_o3": {m: round(g, 4) for m, g in geomeans.items()},
            "agents": {},
        }

        # Seed-level statistics
        for m in ["ppo_autophase", "ppo_gnn"]:
            runs = agent_runs[split_name][m]
            if runs:
                split_out["agents"][m] = {
                    "runs": runs,
                    "summary": summarize_runs(runs),
                }

        ap_runs = agent_runs[split_name]["ppo_autophase"]
        gnn_runs = agent_runs[split_name]["ppo_gnn"]
        if ap_runs and gnn_runs:
            ap_ics = median_run(ap_runs)["ics"]
            gnn_ics = median_run(gnn_runs)["ics"]
            try:
                stat, p = stats.wilcoxon(ap_ics, gnn_ics)
                split_out["wilcoxon_ap_vs_gnn"] = {
                    "statistic": float(stat), "p_value": round(float(p), 4)}
                print(f"\nWilcoxon PPO+AP vs PPO+GNN (median seeds, "
                      f"per-benchmark): p={p:.4f}")
            except ValueError as e:
                # identical ICs on every benchmark -> no test possible
                split_out["wilcoxon_ap_vs_gnn"] = {"error": str(e)}
                print(f"\nWilcoxon PPO+AP vs PPO+GNN: not computable ({e})")

        output["splits"][split_name] = split_out

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nSaved: {args.output}")


if __name__ == "__main__":
    main()

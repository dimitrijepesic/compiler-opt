#!/usr/bin/env python3
"""
Step 6: Evaluate All Methods on Test Set
Loads trained PPO+Autophase and PPO+GNN checkpoints,
evaluates on test benchmarks, computes statistics.
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


def geometric_mean_improvement(method_ics, baseline_ics):
    """Compute geometric mean of per-benchmark improvement ratios vs baseline."""
    ratios = []
    for m, b in zip(method_ics, baseline_ics):
        if b > 0:
            ratios.append(b / m)  # >1 means method is better
    if not ratios:
        return 1.0
    return np.exp(np.mean(np.log(ratios)))


def bootstrap_ci(data, n_bootstrap=10000, ci=0.95, seed=42):
    """Compute bootstrap confidence interval for the mean."""
    rng = np.random.RandomState(seed)
    means = []
    data = np.array(data)
    for _ in range(n_bootstrap):
        sample = rng.choice(data, size=len(data), replace=True)
        means.append(np.mean(sample))
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return lower, upper


def evaluate_agent(agent_class, checkpoint_dir, seed, test_uris, label):
    """Evaluate a trained agent on test benchmarks."""
    agent = agent_class(seed=seed)

    ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_best_seed{seed}.pt")
    if not os.path.exists(ckpt_path):
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_final_seed{seed}.pt")

    if not os.path.exists(ckpt_path):
        print(f"  WARNING: No checkpoint found for {label} seed={seed}")
        agent.close()
        return None

    agent.load_checkpoint(ckpt_path)
    total_ic, reduction, details = agent.evaluate(test_uris, "test")
    agent.close()

    return {
        "seed": seed,
        "total_ic": total_ic,
        "reduction_pct": reduction,
        "details": details,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate all methods on test set")
    parser.add_argument("--baselines", type=str, default="results/full_baselines.json")
    parser.add_argument("--ppo-ap-dir", type=str, default="results/ppo_autophase")
    parser.add_argument("--ppo-gnn-dir", type=str, default="results/ppo_gnn")
    parser.add_argument("--benchmarks", type=str, default="configs/benchmarks.yaml")
    parser.add_argument("--output", type=str, default="results/final_evaluation.json")
    args = parser.parse_args()

    # Load test benchmarks
    with open(args.benchmarks) as f:
        bm_config = yaml.safe_load(f)
    test_uris = bm_config["test"]

    print("=" * 80)
    print("FINAL TEST SET EVALUATION")
    print("=" * 80)
    print(f"  Test benchmarks: {[u.split('/')[-1] for u in test_uris]}")

    # Load baselines
    with open(args.baselines) as f:
        baselines_data = json.load(f)

    test_baselines = {}
    for entry in baselines_data["baselines"]:
        if entry["split"] == "test":
            name = entry["short_name"]
            test_baselines[name] = entry

    # --- Collect results from all methods ---
    all_results = {}

    # Baselines (from pre-computed data)
    for method in ["o0", "o3", "oz", "greedy", "random"]:
        ics = []
        for uri in test_uris:
            name = uri.split("/")[-1]
            ics.append(test_baselines[name][method])
        all_results[method] = {"ics": ics, "seeds": [None]}

    # PPO + Autophase (3 seeds)
    seeds = [42, 123, 456]
    ppo_ap_runs = []
    for seed in seeds:
        result = evaluate_agent(PPOAutophaseAgent, args.ppo_ap_dir, seed, test_uris, "PPO+AP")
        if result:
            ppo_ap_runs.append(result)

    if ppo_ap_runs:
        # Use median seed's results
        ppo_ap_runs.sort(key=lambda r: r["total_ic"])
        median_run = ppo_ap_runs[len(ppo_ap_runs) // 2]
        all_results["ppo_autophase"] = {
            "ics": [d["final_ic"] for d in median_run["details"]],
            "all_runs": ppo_ap_runs,
            "seeds": seeds,
        }

    # PPO + GNN (3 seeds)
    ppo_gnn_runs = []
    for seed in seeds:
        result = evaluate_agent(PPOGNNAgent, args.ppo_gnn_dir, seed, test_uris, "PPO+GNN")
        if result:
            ppo_gnn_runs.append(result)

    if ppo_gnn_runs:
        ppo_gnn_runs.sort(key=lambda r: r["total_ic"])
        median_run = ppo_gnn_runs[len(ppo_gnn_runs) // 2]
        all_results["ppo_gnn"] = {
            "ics": [d["final_ic"] for d in median_run["details"]],
            "all_runs": ppo_gnn_runs,
            "seeds": seeds,
        }

    # --- Print results table ---
    print(f"\n{'Benchmark':<15}", end="")
    for method in ["o0", "o3", "oz", "greedy", "random", "ppo_autophase", "ppo_gnn"]:
        if method in all_results:
            label = {"o0": "O0", "o3": "O3", "oz": "Oz", "greedy": "Greedy",
                     "random": "Random", "ppo_autophase": "PPO+AP", "ppo_gnn": "PPO+GNN"}[method]
            print(f" {label:>10}", end="")
    print()
    print("-" * 100)

    o3_ics = all_results["o3"]["ics"]

    for i, uri in enumerate(test_uris):
        name = uri.split("/")[-1]
        print(f"{name:<15}", end="")
        for method in ["o0", "o3", "oz", "greedy", "random", "ppo_autophase", "ppo_gnn"]:
            if method in all_results:
                ic = all_results[method]["ics"][i]
                print(f" {ic:>10}", end="")
        print()

    # Geomean vs O3
    print("-" * 100)
    print(f"{'Geomean vs O3':<15}", end="")
    for method in ["o0", "o3", "oz", "greedy", "random", "ppo_autophase", "ppo_gnn"]:
        if method in all_results:
            gm = geometric_mean_improvement(all_results[method]["ics"], o3_ics)
            pct = (gm - 1) * 100
            print(f" {pct:>+9.2f}%", end="")
    print()

    # --- Statistical tests ---
    if "ppo_autophase" in all_results and "ppo_gnn" in all_results:
        print(f"\n{'=' * 80}")
        print("STATISTICAL ANALYSIS")
        print(f"{'=' * 80}")

        ap_total_ics = [r["total_ic"] for r in all_results["ppo_autophase"]["all_runs"]]
        gnn_total_ics = [r["total_ic"] for r in all_results["ppo_gnn"]["all_runs"]]

        print(f"\n  PPO+Autophase total ICs across seeds: {ap_total_ics}")
        print(f"  PPO+GNN total ICs across seeds:       {gnn_total_ics}")

        if len(ap_total_ics) >= 3 and len(gnn_total_ics) >= 3:
            # Wilcoxon on per-benchmark ICs (paired)
            ap_ics = all_results["ppo_autophase"]["ics"]
            gnn_ics = all_results["ppo_gnn"]["ics"]

            try:
                stat, p_value = stats.wilcoxon(ap_ics, gnn_ics)
                print(f"\n  Wilcoxon signed-rank test (per-benchmark, median seed):")
                print(f"    Statistic: {stat}")
                print(f"    p-value: {p_value:.4f}")
                print(f"    Significant (p<0.05): {'YES' if p_value < 0.05 else 'NO'}")
            except Exception as e:
                print(f"\n  Wilcoxon test failed: {e}")

        # Bootstrap CIs
        for label, runs in [("PPO+AP", all_results.get("ppo_autophase", {}).get("all_runs", [])),
                            ("PPO+GNN", all_results.get("ppo_gnn", {}).get("all_runs", []))]:
            if runs:
                total_ics = [r["total_ic"] for r in runs]
                if len(total_ics) >= 2:
                    lo, hi = bootstrap_ci(total_ics)
                    print(f"\n  {label} 95% CI for total IC: [{lo:.0f}, {hi:.0f}]")

    # --- Save full results ---
    output = {
        "timestamp": datetime.now().isoformat(),
        "test_benchmarks": test_uris,
        "results": {
            method: {
                "ics": data["ics"],
                "total_ic": sum(data["ics"]),
            }
            for method, data in all_results.items()
        },
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Results saved to: {args.output}")


if __name__ == "__main__":
    main()
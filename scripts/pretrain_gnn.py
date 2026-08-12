#!/usr/bin/env python3
"""
Track C: pretrain the GNN encoder by distilling Autophase features.

Rationale: the from-scratch GNN never escaped the near-uniform-policy
plateau, i.e. RL gradients alone did not teach the encoder useful program
features. Autophase is a known-useful hand-crafted summary of the IR, and
it is available for free at every state. Regressing log1p(Autophase) from
the graph forces the encoder to represent at least that information, so
the RL fine-tune starts from an encoder that provably encodes something.

Phase 1 (collect): random episodes in the reduced action space over the
  <=20K-IC training benchmarks; at every state store (PyG graph, autophase).
Phase 2 (train): GNNEncoder + Linear(128 -> 56) head, MSE, with a held-out
  split for early stopping. Saves encoder weights only.

Output: results/gnn_pretrained/encoder.pt (+ pretrain_log.json)
"""

import sys
import os
import json
import argparse
import time
import numpy as np
import torch
import torch.nn as nn
import yaml
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import compiler_gym
from torch_geometric.data import Batch
from src.features.programl import ir_to_pyg_data, NODE_FEATURE_DIM
from src.features.autophase import extract_autophase, AUTOPHASE_DIM
from src.models.gnn_encoder import GNNEncoder


def collect(episodes_per_benchmark, max_ic, episode_steps, seed):
    with open("configs/benchmarks.yaml") as f:
        bm_config = yaml.safe_load(f)
    with open("configs/passes.yaml") as f:
        passes_config = yaml.safe_load(f)
    action_map = [p["action_id"] for p in passes_config["passes"]]

    rng = np.random.default_rng(seed)
    env = compiler_gym.make("llvm-ic-v0")

    samples = []  # (Data, autophase float32[56])
    for uri in bm_config["train"]:
        env.reset(benchmark=uri)
        if int(env.observation["IrInstructionCount"]) > max_ic:
            continue
        name = uri.split("/")[-1]
        t0 = time.time()
        for ep in range(episodes_per_benchmark):
            env.reset(benchmark=uri)
            for _ in range(episode_steps):
                graph = ir_to_pyg_data(env.observation["Ir"])
                target = extract_autophase(env).astype(np.float32)
                samples.append((graph, torch.from_numpy(target)))
                try:
                    env.step(action_map[rng.integers(len(action_map))])
                except Exception:
                    break
        print(f"  collected {name}: {len(samples)} total samples "
              f"({time.time()-t0:.0f}s)", flush=True)

    env.close()
    return samples


def train(samples, out_dir, epochs, batch_size, lr, seed):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(samples))
    n_val = max(len(samples) // 10, 1)
    val_idx, train_idx = idx[:n_val], idx[n_val:]

    encoder = GNNEncoder(input_dim=NODE_FEATURE_DIM)
    head = nn.Linear(128, AUTOPHASE_DIM)
    params = list(encoder.parameters()) + list(head.parameters())
    opt = torch.optim.Adam(params, lr=lr)

    # Normalize targets over the training split for a well-scaled MSE
    t_train = torch.stack([samples[i][1] for i in train_idx])
    t_mean, t_std = t_train.mean(0), t_train.std(0).clamp(min=1e-3)

    def run_epoch(indices, train_mode):
        encoder.train(train_mode)
        head.train(train_mode)
        total, nb = 0.0, 0
        order = rng.permutation(indices) if train_mode else indices
        for start in range(0, len(order), batch_size):
            chunk = order[start:start + batch_size]
            batch = Batch.from_data_list([samples[i][0] for i in chunk])
            targets = torch.stack([samples[i][1] for i in chunk])
            targets = (targets - t_mean) / t_std
            with torch.set_grad_enabled(train_mode):
                pred = head(encoder(batch))
                loss = nn.functional.mse_loss(pred, targets)
                if train_mode:
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
            total += loss.item()
            nb += 1
        return total / max(nb, 1)

    log = []
    best_val = float("inf")
    os.makedirs(out_dir, exist_ok=True)
    for epoch in range(1, epochs + 1):
        tr = run_epoch(train_idx, True)
        va = run_epoch(val_idx, False)
        log.append({"epoch": epoch, "train_mse": round(tr, 5),
                    "val_mse": round(va, 5)})
        marker = ""
        if va < best_val:
            best_val = va
            torch.save({"encoder_state_dict": encoder.state_dict(),
                        "val_mse": va, "epoch": epoch},
                       os.path.join(out_dir, "encoder.pt"))
            marker = "  <- saved"
        print(f"  epoch {epoch:>3}  train MSE {tr:.4f}  val MSE {va:.4f}{marker}",
              flush=True)
    return log, best_val


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes-per-benchmark", type=int, default=6)
    parser.add_argument("--episode-steps", type=int, default=45)
    parser.add_argument("--max-ic", type=int, default=20000)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", type=str, default="results/gnn_pretrained")
    args = parser.parse_args()

    print("Phase 1: collecting (graph, autophase) samples", flush=True)
    samples = collect(args.episodes_per_benchmark, args.max_ic,
                      args.episode_steps, args.seed)
    print(f"Total samples: {len(samples)}", flush=True)

    print("Phase 2: distillation training", flush=True)
    log, best_val = train(samples, args.out_dir, args.epochs,
                          args.batch_size, args.lr, args.seed)

    with open(os.path.join(args.out_dir, "pretrain_log.json"), "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "num_samples": len(samples),
            "config": vars(args),
            "best_val_mse": best_val,
            "log": log,
        }, f, indent=2)
    print(f"Best val MSE: {best_val:.4f}. Encoder saved to "
          f"{args.out_dir}/encoder.pt", flush=True)


if __name__ == "__main__":
    main()

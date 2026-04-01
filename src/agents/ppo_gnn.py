"""
PPO + GNN Agent
Proximal Policy Optimization with GraphSAGE encoder on LLVM IR graphs.
This is the novel contribution — structural program representation for pass ordering.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import compiler_gym
import json
import os
import sys
import time
import yaml
from datetime import datetime
from torch_geometric.data import Batch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.policy_mlp import PolicyMLP
from src.models.value_head import ValueMLP
from src.models.gnn_encoder import GNNEncoder
from src.features.programl import ir_to_pyg_data, IRGraphCache, NUM_OPCODES


class GNNRolloutBuffer:
    """Stores transitions with graph states instead of flat vectors."""

    def __init__(self):
        self.graphs = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []

    def add(self, graph, action, log_prob, reward, value, done):
        self.graphs.append(graph)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def clear(self):
        self.graphs.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.values.clear()
        self.dones.clear()

    def __len__(self):
        return len(self.graphs)


class PPOGNNAgent:
    """PPO agent using GNN encoder on program graphs for pass ordering."""

    def __init__(self, config_path="configs/hyperparams.yaml",
                 passes_path="configs/passes.yaml",
                 benchmarks_path="configs/benchmarks.yaml",
                 seed=42):

        # Load configs
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        with open(passes_path) as f:
            passes_config = yaml.safe_load(f)
        with open(benchmarks_path) as f:
            benchmarks_config = yaml.safe_load(f)

        self.seed = seed
        torch.manual_seed(seed)
        np.random.seed(seed)

        # PPO hyperparameters
        ppo_cfg = self.config["ppo"]
        self.clip_ratio = ppo_cfg["clip_ratio"]
        self.gae_lambda = ppo_cfg["gae_lambda"]
        self.entropy_coeff = ppo_cfg["entropy_coeff"]
        self.lr = ppo_cfg["learning_rate"]
        self.batch_size = ppo_cfg["batch_size"]
        self.ppo_epochs = ppo_cfg["ppo_epochs"]
        self.collect_steps = ppo_cfg["collect_steps"]
        self.max_episode_steps = ppo_cfg["max_episode_steps"]
        self.gamma = ppo_cfg["gamma"]
        self.total_env_steps = ppo_cfg["total_env_steps"]
        self.val_interval = ppo_cfg["val_interval_steps"]

        # Reduced action space
        self.reduced_passes = passes_config["passes"]
        self.num_actions = len(self.reduced_passes)
        self.action_map = [p["action_id"] for p in self.reduced_passes]

        # Environment (created early so _filter_benchmarks can use it)
        self.env = compiler_gym.make("llvm-ic-v0")

        # Benchmark URIs — filter out benchmarks too large for RL loop
        max_ic_for_training = self.config.get("rl_max_benchmark_ic", 20000)
        self.train_uris = self._filter_benchmarks(
            benchmarks_config["train"], max_ic_for_training
        )
        self.val_uris = self._filter_benchmarks(
            benchmarks_config["validation"], max_ic_for_training
        )

        # GNN encoder
        gnn_cfg = self.config["gnn"]
        self.gnn = GNNEncoder(
            input_dim=NUM_OPCODES,
            hidden_dim=gnn_cfg["hidden_dim"],
            output_dim=gnn_cfg["hidden_dim"],  # output feeds into policy/value MLPs
            num_layers=gnn_cfg["num_layers"],
            dropout=gnn_cfg["dropout"],
            aggregation=gnn_cfg["aggregation"],
        )

        # Policy and value heads take GNN output as input
        gnn_output_dim = gnn_cfg["hidden_dim"]

        mlp_cfg = self.config["policy_mlp"]
        self.policy = PolicyMLP(
            input_dim=gnn_output_dim,
            num_actions=self.num_actions,
            hidden_dim=mlp_cfg["hidden_dim"],
            num_layers=mlp_cfg["num_layers"],
        )

        val_cfg = self.config["value_mlp"]
        self.value_fn = ValueMLP(
            input_dim=gnn_output_dim,
            hidden_dim=val_cfg["hidden_dim"],
            num_layers=val_cfg["num_layers"],
        )

        # Single optimizer for all parameters (GNN + policy + value)
        # Joint training is important — GNN learns features guided by RL objective
        all_params = (
            list(self.gnn.parameters()) +
            list(self.policy.parameters()) +
            list(self.value_fn.parameters())
        )
        self.optimizer = optim.Adam(all_params, lr=self.lr)

        total_updates = self.total_env_steps // self.collect_steps
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=total_updates
        )

        # Graph cache (speeds up repeated states)
        self.graph_cache = IRGraphCache()

        # Rollout buffer
        self.buffer = GNNRolloutBuffer()

        # Tracking
        self.total_steps = 0
        self.episode_count = 0
        self.best_val_score = float("inf")
        self.training_log = []

        # Track graph extraction time for overhead reporting
        self.total_graph_time = 0
        self.total_graph_extractions = 0

    def _filter_benchmarks(self, uris, max_ic):
        """Filter out benchmarks with O0 instruction count above max_ic."""
        filtered = []
        for uri in uris:
            try:
                self.env.reset(benchmark=uri)
                ic = int(self.env.observation["IrInstructionCount"])
                if ic <= max_ic:
                    filtered.append(uri)
                else:
                    print(f"    Skipping {uri.split('/')[-1]} (IC={ic} > {max_ic})")
            except Exception as e:
                print(f"    Skipping {uri.split('/')[-1]} (error: {e})")
        return filtered

    def _get_graph(self):
        """Extract program graph from current env state."""
        t0 = time.time()
        ir_text = self.env.observation["Ir"]
        graph = self.graph_cache.get_or_extract(ir_text)
        self.total_graph_time += time.time() - t0
        self.total_graph_extractions += 1
        return graph

    def _encode_graph(self, graph):
        """Run GNN encoder on a single graph, return embedding vector."""
        with torch.no_grad():
            embedding = self.gnn(graph)
        return embedding.squeeze(0)  # [output_dim]

    def _select_action(self, graph):
        """Sample action from policy given a program graph."""
        with torch.no_grad():
            embedding = self.gnn(graph)  # [1, output_dim]
            logits = self.policy(embedding)
            dist = torch.distributions.Categorical(logits=logits)
            action_idx = dist.sample()
            log_prob = dist.log_prob(action_idx)
            value = self.value_fn(embedding)

        return action_idx.item(), log_prob.item(), value.item()

    def _compute_gae(self, rewards, values, dones):
        """Compute Generalized Advantage Estimation."""
        advantages = []
        gae = 0
        values = values + [0]

        for t in reversed(range(len(rewards))):
            if dones[t]:
                delta = rewards[t] - values[t]
                gae = delta
            else:
                delta = rewards[t] + self.gamma * values[t + 1] - values[t]
                gae = delta + self.gamma * self.gae_lambda * gae
            advantages.insert(0, gae)

        advantages = torch.tensor(advantages, dtype=torch.float32)
        returns = advantages + torch.tensor(values[:-1], dtype=torch.float32)
        return advantages, returns

    def collect_rollouts(self):
        """Collect transitions using graph states."""
        self.buffer.clear()
        steps_collected = 0
        episode_rewards = []

        self.gnn.eval()  # No grad during collection

        while steps_collected < self.collect_steps:
            uri = self.train_uris[np.random.randint(len(self.train_uris))]
            self.env.reset(benchmark=uri)
            initial_ic = int(self.env.observation["IrInstructionCount"])
            prev_ic = initial_ic

            graph = self._get_graph()
            episode_reward = 0

            for step in range(self.max_episode_steps):
                action_idx, log_prob, value = self._select_action(graph)

                cg_action = self.action_map[action_idx]

                try:
                    self.env.step(cg_action)
                except Exception:
                    self.buffer.add(graph, action_idx, log_prob, 0.0, value, False)
                    steps_collected += 1
                    self.total_steps += 1
                    continue

                current_ic = int(self.env.observation["IrInstructionCount"])
                reward = (prev_ic - current_ic) / initial_ic
                prev_ic = current_ic
                episode_reward += reward

                done = (step == self.max_episode_steps - 1)

                next_graph = self._get_graph()
                self.buffer.add(graph, action_idx, log_prob, reward, value, done)

                graph = next_graph
                steps_collected += 1
                self.total_steps += 1

                if steps_collected >= self.collect_steps:
                    break

            self.episode_count += 1
            episode_rewards.append(episode_reward)

        self.gnn.train()
        return episode_rewards

    def update(self):
        """Run PPO update with batched graph processing."""
        advantages, returns = self._compute_gae(
            self.buffer.rewards, self.buffer.values, self.buffer.dones
        )

        actions = torch.tensor(self.buffer.actions, dtype=torch.long)
        old_log_probs = torch.tensor(self.buffer.log_probs, dtype=torch.float32)
        graphs = self.buffer.graphs

        if len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        num_batches = 0

        dataset_size = len(graphs)

        for epoch in range(self.ppo_epochs):
            indices = torch.randperm(dataset_size)

            for start in range(0, dataset_size, self.batch_size):
                end = min(start + self.batch_size, dataset_size)
                batch_idx = indices[start:end].tolist()

                # Batch graphs using PyG
                batch_graphs = Batch.from_data_list([graphs[i] for i in batch_idx])
                batch_actions = actions[batch_idx]
                batch_old_log_probs = old_log_probs[batch_idx]
                batch_advantages = advantages[batch_idx]
                batch_returns = returns[batch_idx]

                # Forward pass through GNN + policy + value
                embeddings = self.gnn(batch_graphs)  # [batch, output_dim]

                logits = self.policy(embeddings)
                dist = torch.distributions.Categorical(logits=logits)
                new_log_probs = dist.log_prob(batch_actions)
                entropy = dist.entropy().mean()

                ratio = torch.exp(new_log_probs - batch_old_log_probs)
                clipped_ratio = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)

                policy_loss = -torch.min(
                    ratio * batch_advantages,
                    clipped_ratio * batch_advantages,
                ).mean()
                policy_loss = policy_loss - self.entropy_coeff * entropy

                values = self.value_fn(embeddings)
                value_loss = nn.MSELoss()(values, batch_returns)

                # Combined loss, single backward pass
                total_loss = policy_loss + 0.5 * value_loss

                self.optimizer.zero_grad()
                total_loss.backward()
                nn.utils.clip_grad_norm_(
                    list(self.gnn.parameters()) +
                    list(self.policy.parameters()) +
                    list(self.value_fn.parameters()),
                    0.5,
                )
                self.optimizer.step()

                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                num_batches += 1

        self.scheduler.step()

        return {
            "policy_loss": total_policy_loss / max(num_batches, 1),
            "value_loss": total_value_loss / max(num_batches, 1),
            "entropy": total_entropy / max(num_batches, 1),
        }

    def evaluate(self, uris, label="val"):
        """Evaluate current policy on benchmarks."""
        results = []
        self.gnn.eval()
        self.policy.eval()

        for uri in uris:
            self.env.reset(benchmark=uri)
            initial_ic = int(self.env.observation["IrInstructionCount"])

            graph = self._get_graph()

            for step in range(self.max_episode_steps):
                with torch.no_grad():
                    embedding = self.gnn(graph)
                    logits = self.policy(embedding)
                    action_idx = torch.argmax(logits, dim=-1).item()

                cg_action = self.action_map[action_idx]
                try:
                    self.env.step(cg_action)
                except Exception:
                    continue

                graph = self._get_graph()

            final_ic = int(self.env.observation["IrInstructionCount"])
            reduction_pct = (initial_ic - final_ic) / initial_ic * 100
            results.append({
                "uri": uri,
                "short_name": uri.split("/")[-1],
                "initial_ic": initial_ic,
                "final_ic": final_ic,
                "reduction_pct": round(reduction_pct, 2),
            })

        self.gnn.train()
        self.policy.train()

        total_initial = sum(r["initial_ic"] for r in results)
        total_final = sum(r["final_ic"] for r in results)
        avg_reduction = (total_initial - total_final) / total_initial * 100

        return total_final, avg_reduction, results

    def train(self, save_dir="results/ppo_gnn"):
        """Full training loop."""
        os.makedirs(save_dir, exist_ok=True)

        print("=" * 70)
        print(f"PPO + GNN TRAINING (seed={self.seed})")
        print("=" * 70)
        print(f"  Action space: {self.num_actions} passes (reduced)")
        print(f"  GNN: {self.config['gnn']['num_layers']} layers, "
              f"hidden={self.config['gnn']['hidden_dim']}")
        print(f"  Train benchmarks: {len(self.train_uris)}")
        print(f"  Val benchmarks: {len(self.val_uris)}")
        print(f"  Total budget: {self.total_env_steps} steps")
        print()

        start_time = time.time()
        update_num = 0

        while self.total_steps < self.total_env_steps:
            update_num += 1
            t0 = time.time()

            episode_rewards = self.collect_rollouts()
            avg_ep_reward = np.mean(episode_rewards) if episode_rewards else 0

            losses = self.update()

            elapsed = time.time() - t0
            steps_per_sec = self.collect_steps / elapsed

            # Graph extraction overhead
            avg_graph_ms = (
                (self.total_graph_time / max(self.total_graph_extractions, 1)) * 1000
            )

            print(
                f"  Update {update_num:>3} | Steps: {self.total_steps:>7}/{self.total_env_steps} | "
                f"Ep reward: {avg_ep_reward:>+.4f} | "
                f"P loss: {losses['policy_loss']:.4f} | V loss: {losses['value_loss']:.4f} | "
                f"Ent: {losses['entropy']:.3f} | {steps_per_sec:.1f} sps | "
                f"Graph: {avg_graph_ms:.0f}ms"
            )

            log_entry = {
                "update": update_num,
                "total_steps": self.total_steps,
                "episodes": self.episode_count,
                "avg_episode_reward": round(avg_ep_reward, 6),
                "policy_loss": round(losses["policy_loss"], 6),
                "value_loss": round(losses["value_loss"], 6),
                "entropy": round(losses["entropy"], 4),
                "avg_graph_extraction_ms": round(avg_graph_ms, 1),
            }

            # Validation
            if self.total_steps % self.val_interval < self.collect_steps:
                val_ic, val_reduction, val_results = self.evaluate(self.val_uris, "val")
                print(f"         VAL | Total IC: {val_ic} | Reduction: {val_reduction:.2f}%")

                log_entry["val_total_ic"] = val_ic
                log_entry["val_reduction_pct"] = round(val_reduction, 2)
                log_entry["val_details"] = val_results

                if val_ic < self.best_val_score:
                    self.best_val_score = val_ic
                    self._save_checkpoint(save_dir, "best")
                    print(f"         NEW BEST val IC: {val_ic}")

            self.training_log.append(log_entry)

        total_time = time.time() - start_time
        self._save_checkpoint(save_dir, "final")

        # Save training log
        log_output = {
            "timestamp": datetime.now().isoformat(),
            "seed": self.seed,
            "total_steps": self.total_steps,
            "total_episodes": self.episode_count,
            "total_time_seconds": round(total_time, 1),
            "best_val_ic": self.best_val_score,
            "total_graph_extractions": self.total_graph_extractions,
            "total_graph_time_seconds": round(self.total_graph_time, 1),
            "config": self.config,
            "num_actions": self.num_actions,
            "log": self.training_log,
        }
        with open(os.path.join(save_dir, f"training_log_seed{self.seed}.json"), "w") as f:
            json.dump(log_output, f, indent=2)

        print(f"\n  Training complete in {total_time / 60:.1f} minutes")
        print(f"  Best validation IC: {self.best_val_score}")
        print(f"  Graph extractions: {self.total_graph_extractions} "
              f"({self.total_graph_time:.1f}s total)")

        return self.best_val_score

    def _save_checkpoint(self, save_dir, tag):
        """Save model checkpoint."""
        path = os.path.join(save_dir, f"checkpoint_{tag}_seed{self.seed}.pt")
        torch.save({
            "gnn_state_dict": self.gnn.state_dict(),
            "policy_state_dict": self.policy.state_dict(),
            "value_state_dict": self.value_fn.state_dict(),
            "total_steps": self.total_steps,
            "best_val_score": self.best_val_score,
            "seed": self.seed,
        }, path)

    def load_checkpoint(self, path):
        """Load model checkpoint."""
        ckpt = torch.load(path, weights_only=True)
        self.gnn.load_state_dict(ckpt["gnn_state_dict"])
        self.policy.load_state_dict(ckpt["policy_state_dict"])
        self.value_fn.load_state_dict(ckpt["value_state_dict"])
        self.total_steps = ckpt["total_steps"]
        self.best_val_score = ckpt["best_val_score"]

    def close(self):
        self.env.close()
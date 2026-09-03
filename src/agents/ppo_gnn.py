"""
PPO + GNN Agent
Proximal Policy Optimization with GraphSAGE encoder on LLVM IR graphs.
The graph representation is the variable under test in the controlled comparison.
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
from src.features.programl import ir_to_pyg_data, IRGraphCache, NODE_FEATURE_DIM


class GNNRolloutBuffer:
    """Stores transitions with graph states instead of flat vectors.

    bootstraps[t] is V(s_{t+1}) for transitions where done=True: every
    episode here ends by truncation (time limit or collect boundary), so
    the return must bootstrap from the next state's value, not from 0.
    """

    def __init__(self):
        self.graphs = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []
        self.bootstraps = []

    def add(self, graph, action, log_prob, reward, value, done, bootstrap=0.0):
        self.graphs.append(graph)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)
        self.bootstraps.append(bootstrap)

    def clear(self):
        self.graphs.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.values.clear()
        self.dones.clear()
        self.bootstraps.clear()

    def __len__(self):
        return len(self.graphs)


class PPOGNNAgent:
    """PPO agent using GNN encoder on program graphs for pass ordering."""

    def __init__(self, config_path="configs/hyperparams.yaml",
                 passes_path="configs/passes.yaml",
                 benchmarks_path="configs/benchmarks.yaml",
                 seed=42, init_encoder_path=None, device=None,
                 total_env_steps=None):
        # device: "cpu" (default, the paper's setting) or "cuda". The
        # encoder, heads and PPO batches live on it; graph extraction and
        # the rollout buffer stay on the CPU. COMPILER_OPT_DEVICE overrides
        # the default when the argument is not given.
        # total_env_steps: optional override of the config budget (used
        # for short timing probes; leave None for real runs).

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
        self.total_env_steps = (total_env_steps if total_env_steps
                                else ppo_cfg["total_env_steps"])
        self.val_interval = ppo_cfg["val_interval_steps"]
        self.device = torch.device(
            device or os.environ.get("COMPILER_OPT_DEVICE", "cpu"))
        # Memory knob for small GPUs: each PPO batch of batch_size graphs
        # is processed in micro-batches of this size with gradient
        # accumulation. Losses are rescaled so the gradient equals the
        # full-batch gradient; the default (= batch_size) is the plain
        # single-pass update used on the CPU.
        self.micro_batch_size = int(os.environ.get(
            "COMPILER_OPT_MICRO_BATCH", ppo_cfg.get("micro_batch_size",
                                                    self.batch_size)))

        # KL guard: stop PPO epochs early once the policy has moved too far
        # from the rollout policy. This is what prevents the collapse seen
        # in the original runs (val IC 689 -> 1059).
        self.target_kl = ppo_cfg.get("target_kl", 0.02)

        # Entropy coefficient decays linearly across updates so exploration
        # is high early but the policy is allowed to commit late.
        self.entropy_coeff_final = ppo_cfg.get("entropy_coeff_final",
                                               self.entropy_coeff)
        self.current_entropy_coeff = self.entropy_coeff

        # Reduced action space
        self.reduced_passes = passes_config["passes"]
        self.num_actions = len(self.reduced_passes)
        self.action_map = [p["action_id"] for p in self.reduced_passes]

        # Environment (created early so _filter_benchmarks can use it)
        self.env = compiler_gym.make("llvm-ic-v0")

        # Benchmark URIs, filter out benchmarks too large for RL loop
        max_ic_for_training = self.config.get("rl_max_benchmark_ic", 20000)
        self.train_uris = self._filter_benchmarks(
            benchmarks_config["train"], max_ic_for_training
        )
        # Checkpoint selection uses the explicit cheap validation subset if
        # declared; the full validation set is reserved for final evaluation.
        if "validation_small" in benchmarks_config:
            self.val_uris = list(benchmarks_config["validation_small"])
        else:
            self.val_uris = self._filter_benchmarks(
                benchmarks_config["validation"], max_ic_for_training
            )

        # GNN encoder
        gnn_cfg = self.config["gnn"]
        self.gnn = GNNEncoder(
            input_dim=NODE_FEATURE_DIM,
            hidden_dim=gnn_cfg["hidden_dim"],
            output_dim=gnn_cfg["hidden_dim"],  # output feeds into policy/value MLPs
            num_layers=gnn_cfg["num_layers"],
            dropout=gnn_cfg["dropout"],
            aggregation=gnn_cfg["aggregation"],
        )

        # Optionally warm-start the encoder from a pretrained checkpoint
        # (e.g. Autophase distillation, scripts/pretrain_gnn.py)
        if init_encoder_path:
            ckpt = torch.load(init_encoder_path, weights_only=True,
                              map_location="cpu")
            self.gnn.load_state_dict(ckpt["encoder_state_dict"])
            print(f"  Initialized encoder from {init_encoder_path} "
                  f"(pretrain val MSE {ckpt.get('val_mse', '?')})")

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
        self.gnn.to(self.device)
        self.policy.to(self.device)
        self.value_fn.to(self.device)

        # Single optimizer, two param groups: the encoder gets a lower lr
        # than the heads so RL gradients refine its features without
        # destabilizing them. Joint training is still important: the GNN
        # learns features guided by the RL objective.
        encoder_lr = gnn_cfg.get("encoder_lr", self.lr)
        self.optimizer = optim.Adam([
            {"params": self.gnn.parameters(), "lr": encoder_lr},
            {"params": list(self.policy.parameters()) +
                       list(self.value_fn.parameters()), "lr": self.lr},
        ])

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

    def _recycle_env(self):
        """Replace the CompilerGym environment with a fresh one. The
        long-lived service leaks memory across many steps on large
        programs (observed OOM-killed at 11.5 GB RSS mid-training), so
        the training loop recycles it periodically and after any
        service failure."""
        try:
            self.env.close()
        except Exception:
            pass
        self.env = compiler_gym.make("llvm-ic-v0")

    def _get_graph(self):
        """Extract program graph from current env state."""
        t0 = time.time()
        ir_text = self.env.observation["Ir"]
        graph = self.graph_cache.get_or_extract(ir_text)
        self.total_graph_time += time.time() - t0
        self.total_graph_extractions += 1
        return graph

    def _on_device(self, graph):
        """Copy of a graph on the compute device. PyG's Data.to() moves
        tensors in place, so a clone keeps the cached/buffered graph on
        the CPU; on the CPU device the graph is returned untouched."""
        if self.device.type == "cpu":
            return graph
        return graph.clone().to(self.device)

    def _select_action(self, graph):
        """Sample action from policy given a program graph."""
        with torch.no_grad():
            embedding = self.gnn(self._on_device(graph))  # [1, output_dim]
            logits = self.policy(embedding)
            dist = torch.distributions.Categorical(logits=logits)
            action_idx = dist.sample()
            log_prob = dist.log_prob(action_idx)
            value = self.value_fn(embedding)

        return action_idx.item(), log_prob.item(), value.item()

    def _state_value(self, graph):
        """Value estimate for a single graph state (no grad)."""
        with torch.no_grad():
            embedding = self.gnn(self._on_device(graph))
            return self.value_fn(embedding).item()

    def _compute_gae(self, rewards, values, dones, bootstraps):
        """Compute GAE. Episodes here never truly terminate; they are
        truncated (time limit / collect boundary), so at done steps the
        delta bootstraps from V(s_next) instead of 0, and the advantage
        accumulator resets so nothing leaks across episode boundaries."""
        advantages = []
        gae = 0
        values = values + [0]

        for t in reversed(range(len(rewards))):
            if dones[t]:
                delta = rewards[t] + self.gamma * bootstraps[t] - values[t]
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
            try:
                self.env.reset(benchmark=uri)
                initial_ic = int(self.env.observation["IrInstructionCount"])
                prev_ic = initial_ic
                graph = self._get_graph()
            except Exception:
                # Service died between episodes; replace it and try the
                # next episode.
                self._recycle_env()
                continue
            episode_reward = 0

            for step in range(self.max_episode_steps):
                action_idx, log_prob, value = self._select_action(graph)

                cg_action = self.action_map[action_idx]

                try:
                    self.env.step(cg_action)
                    current_ic = int(self.env.observation["IrInstructionCount"])
                    next_graph = self._get_graph()
                except Exception:
                    # Session died (the step itself, the observation read,
                    # or the graph extraction); end the episode with a
                    # bootstrap from the last known state's value and
                    # replace the dead service.
                    self.buffer.add(graph, action_idx, log_prob, 0.0, value,
                                    True, bootstrap=value)
                    steps_collected += 1
                    self.total_steps += 1
                    self._recycle_env()
                    break

                reward = (prev_ic - current_ic) / initial_ic
                prev_ic = current_ic
                episode_reward += reward

                # Episode ends by truncation at the time limit or when the
                # rollout budget is exhausted mid-episode. Both must
                # bootstrap from V(s_next) and reset the GAE accumulator.
                truncated = (
                    step == self.max_episode_steps - 1
                    or steps_collected + 1 >= self.collect_steps
                )
                bootstrap = self._state_value(next_graph) if truncated else 0.0
                self.buffer.add(graph, action_idx, log_prob, reward, value,
                                truncated, bootstrap=bootstrap)

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
            self.buffer.rewards, self.buffer.values, self.buffer.dones,
            self.buffer.bootstraps
        )

        actions = torch.tensor(self.buffer.actions, dtype=torch.long)
        old_log_probs = torch.tensor(self.buffer.log_probs, dtype=torch.float32)
        graphs = self.buffer.graphs

        if len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        total_kl = 0
        num_batches = 0
        epochs_ran = 0

        dataset_size = len(graphs)

        for epoch in range(self.ppo_epochs):
            epoch_kl = 0
            epoch_batches = 0
            indices = torch.randperm(dataset_size)

            for start in range(0, dataset_size, self.batch_size):
                end = min(start + self.batch_size, dataset_size)
                batch_idx = indices[start:end].tolist()

                n_batch = len(batch_idx)
                self.optimizer.zero_grad()
                policy_loss_acc = value_loss_acc = entropy_acc = kl_acc = 0.0

                # Micro-batches with gradient accumulation; every loss is a
                # per-sample mean, so weighting each chunk by its share of
                # the batch reproduces the single-pass full-batch gradient.
                for mb_start in range(0, n_batch, self.micro_batch_size):
                    mb_idx = batch_idx[mb_start:mb_start + self.micro_batch_size]
                    w = len(mb_idx) / n_batch

                    batch_graphs = Batch.from_data_list(
                        [graphs[i] for i in mb_idx]).to(self.device)
                    batch_actions = actions[mb_idx].to(self.device)
                    batch_old_log_probs = old_log_probs[mb_idx].to(self.device)
                    batch_advantages = advantages[mb_idx].to(self.device)
                    batch_returns = returns[mb_idx].to(self.device)

                    # Forward pass through GNN + policy + value
                    embeddings = self.gnn(batch_graphs)  # [mb, output_dim]

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
                    policy_loss = policy_loss - self.current_entropy_coeff * entropy

                    values = self.value_fn(embeddings)
                    value_loss = nn.MSELoss()(values, batch_returns)

                    # Combined loss; the backward passes accumulate
                    total_loss = (policy_loss + 0.5 * value_loss) * w
                    total_loss.backward()

                    with torch.no_grad():
                        kl_acc += (batch_old_log_probs - new_log_probs).mean().item() * w
                    policy_loss_acc += policy_loss.item() * w
                    value_loss_acc += value_loss.item() * w
                    entropy_acc += entropy.item() * w

                nn.utils.clip_grad_norm_(
                    list(self.gnn.parameters()) +
                    list(self.policy.parameters()) +
                    list(self.value_fn.parameters()),
                    0.5,
                )
                self.optimizer.step()

                approx_kl = kl_acc
                total_policy_loss += policy_loss_acc
                total_value_loss += value_loss_acc
                total_entropy += entropy_acc
                total_kl += approx_kl
                epoch_kl += approx_kl
                num_batches += 1
                epoch_batches += 1

            epochs_ran += 1
            # KL early stop: once the new policy drifts too far from the
            # rollout policy, further epochs on this stale data hurt.
            if epoch_batches > 0 and epoch_kl / epoch_batches > 1.5 * self.target_kl:
                break

        self.scheduler.step()

        return {
            "policy_loss": total_policy_loss / max(num_batches, 1),
            "value_loss": total_value_loss / max(num_batches, 1),
            "entropy": total_entropy / max(num_batches, 1),
            "approx_kl": total_kl / max(num_batches, 1),
            "epochs_ran": epochs_ran,
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
                    embedding = self.gnn(self._on_device(graph))
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
        print(f"  Device: {self.device}")
        print()

        start_time = time.time()
        update_num = 0

        total_updates = max(self.total_env_steps // self.collect_steps, 1)

        while self.total_steps < self.total_env_steps:
            update_num += 1
            t0 = time.time()

            # Recycle the CompilerGym service periodically; it leaks
            # memory across long runs (see _recycle_env).
            if update_num > 1 and update_num % 5 == 1:
                self._recycle_env()

            # Linear entropy coefficient decay across the training run
            frac = min((update_num - 1) / total_updates, 1.0)
            self.current_entropy_coeff = (
                self.entropy_coeff
                + frac * (self.entropy_coeff_final - self.entropy_coeff)
            )

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
                f"Ent: {losses['entropy']:.3f} | KL: {losses['approx_kl']:.4f} "
                f"({losses['epochs_ran']}ep) | {steps_per_sec:.1f} sps | "
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
                "approx_kl": round(losses["approx_kl"], 6),
                "epochs_ran": losses["epochs_ran"],
                "entropy_coeff": round(self.current_entropy_coeff, 6),
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

        def on_cpu(module):
            return {k: v.detach().cpu() for k, v in module.state_dict().items()}

        # Checkpoints are always stored on the CPU so that a GPU-trained
        # policy loads on a CPU-only evaluation machine.
        torch.save({
            "gnn_state_dict": on_cpu(self.gnn),
            "policy_state_dict": on_cpu(self.policy),
            "value_state_dict": on_cpu(self.value_fn),
            "total_steps": self.total_steps,
            "best_val_score": self.best_val_score,
            "seed": self.seed,
        }, path)

    def load_checkpoint(self, path):
        """Load model checkpoint."""
        ckpt = torch.load(path, weights_only=True, map_location=self.device)
        self.gnn.load_state_dict(ckpt["gnn_state_dict"])
        self.policy.load_state_dict(ckpt["policy_state_dict"])
        self.value_fn.load_state_dict(ckpt["value_state_dict"])
        self.total_steps = ckpt["total_steps"]
        self.best_val_score = ckpt["best_val_score"]

    def close(self):
        self.env.close()
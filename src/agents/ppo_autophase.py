"""
PPO + Autophase Agent
Proximal Policy Optimization with 56-dim Autophase features.
This is the baseline RL agent — the GNN agent replaces the feature extractor.
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.policy_mlp import PolicyMLP
from src.models.value_head import ValueMLP
from src.features.autophase import extract_autophase, AUTOPHASE_DIM


class RolloutBuffer:
    """Stores transitions collected during rollout phase."""

    def __init__(self):
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.dones = []

    def add(self, state, action, log_prob, reward, value, done):
        self.states.append(state)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.dones.append(done)

    def clear(self):
        self.states.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.values.clear()
        self.dones.clear()

    def __len__(self):
        return len(self.states)


class PPOAutophaseAgent:
    """PPO agent using Autophase features for compiler pass ordering."""

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

        # Build reduced action space mapping: index -> CompilerGym action_id
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

        # Networks (separate policy and value)
        mlp_cfg = self.config["policy_mlp"]
        self.policy = PolicyMLP(
            input_dim=AUTOPHASE_DIM,
            num_actions=self.num_actions,
            hidden_dim=mlp_cfg["hidden_dim"],
            num_layers=mlp_cfg["num_layers"],
        )
        val_cfg = self.config["value_mlp"]
        self.value_fn = ValueMLP(
            input_dim=AUTOPHASE_DIM,
            hidden_dim=val_cfg["hidden_dim"],
            num_layers=val_cfg["num_layers"],
        )

        # Optimizers (separate, as spec recommends)
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=self.lr)
        self.value_optimizer = optim.Adam(self.value_fn.parameters(), lr=self.lr)

        # LR schedulers
        total_updates = self.total_env_steps // self.collect_steps
        self.policy_scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.policy_optimizer, T_max=total_updates
        )
        self.value_scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.value_optimizer, T_max=total_updates
        )

        # Rollout buffer
        self.buffer = RolloutBuffer()

        # Tracking
        self.total_steps = 0
        self.episode_count = 0
        self.best_val_score = float("inf")
        self.training_log = []

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

    def _get_state(self):
        """Extract Autophase state as torch tensor."""
        features = extract_autophase(self.env)
        return torch.tensor(features, dtype=torch.float32)

    def _select_action(self, state):
        """Sample action from policy, return (action_index, log_prob, value)."""
        with torch.no_grad():
            logits = self.policy(state.unsqueeze(0))
            dist = torch.distributions.Categorical(logits=logits)
            action_idx = dist.sample()
            log_prob = dist.log_prob(action_idx)
            value = self.value_fn(state.unsqueeze(0))

        return action_idx.item(), log_prob.item(), value.item()

    def _compute_gae(self, rewards, values, dones):
        """Compute Generalized Advantage Estimation."""
        advantages = []
        gae = 0
        # Append 0 as bootstrap value for terminal states
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
        """Collect transitions by running episodes across training benchmarks."""
        self.buffer.clear()
        steps_collected = 0
        episode_rewards = []

        while steps_collected < self.collect_steps:
            # Pick a random training benchmark
            uri = self.train_uris[np.random.randint(len(self.train_uris))]
            self.env.reset(benchmark=uri)
            initial_ic = int(self.env.observation["IrInstructionCount"])
            prev_ic = initial_ic

            state = self._get_state()
            episode_reward = 0

            for step in range(self.max_episode_steps):
                action_idx, log_prob, value = self._select_action(state)

                # Map reduced action index to CompilerGym action id
                cg_action = self.action_map[action_idx]

                try:
                    self.env.step(cg_action)
                    current_ic = int(self.env.observation["IrInstructionCount"])
                except Exception:
                    # Session died — end this episode
                    self.buffer.add(state.numpy(), action_idx, log_prob, 0.0, value, True)
                    steps_collected += 1
                    self.total_steps += 1
                    break

                # Reward: relative IC reduction
                reward = (prev_ic - current_ic) / initial_ic
                prev_ic = current_ic
                episode_reward += reward

                done = (step == self.max_episode_steps - 1)

                next_state = self._get_state()
                self.buffer.add(state.numpy(), action_idx, log_prob, reward, value, done)

                state = next_state
                steps_collected += 1
                self.total_steps += 1

                if steps_collected >= self.collect_steps:
                    break

            self.episode_count += 1
            episode_rewards.append(episode_reward)

        return episode_rewards

    def update(self):
        """Run PPO update on collected rollout data."""
        # Compute advantages
        advantages, returns = self._compute_gae(
            self.buffer.rewards, self.buffer.values, self.buffer.dones
        )

        # Convert buffer to tensors
        states = torch.tensor(np.array(self.buffer.states), dtype=torch.float32)
        actions = torch.tensor(self.buffer.actions, dtype=torch.long)
        old_log_probs = torch.tensor(self.buffer.log_probs, dtype=torch.float32)

        # Normalize advantages
        if len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # PPO epochs
        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        num_batches = 0

        dataset_size = len(states)

        for epoch in range(self.ppo_epochs):
            indices = torch.randperm(dataset_size)

            for start in range(0, dataset_size, self.batch_size):
                end = min(start + self.batch_size, dataset_size)
                batch_idx = indices[start:end]

                batch_states = states[batch_idx]
                batch_actions = actions[batch_idx]
                batch_old_log_probs = old_log_probs[batch_idx]
                batch_advantages = advantages[batch_idx]
                batch_returns = returns[batch_idx]

                # Policy loss
                logits = self.policy(batch_states)
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

                self.policy_optimizer.zero_grad()
                policy_loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
                self.policy_optimizer.step()

                # Value loss
                values = self.value_fn(batch_states)
                value_loss = nn.MSELoss()(values, batch_returns)

                self.value_optimizer.zero_grad()
                value_loss.backward()
                nn.utils.clip_grad_norm_(self.value_fn.parameters(), 0.5)
                self.value_optimizer.step()

                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                num_batches += 1

        self.policy_scheduler.step()
        self.value_scheduler.step()

        return {
            "policy_loss": total_policy_loss / max(num_batches, 1),
            "value_loss": total_value_loss / max(num_batches, 1),
            "entropy": total_entropy / max(num_batches, 1),
        }

    def evaluate(self, uris, label="val"):
        """Evaluate current policy on a set of benchmarks. Returns avg IC."""
        results = []
        self.policy.eval()

        for uri in uris:
            self.env.reset(benchmark=uri)
            initial_ic = int(self.env.observation["IrInstructionCount"])

            state = self._get_state()

            for step in range(self.max_episode_steps):
                with torch.no_grad():
                    logits = self.policy(state.unsqueeze(0))
                    action_idx = torch.argmax(logits, dim=-1).item()

                cg_action = self.action_map[action_idx]
                try:
                    self.env.step(cg_action)
                except Exception:
                    continue

                state = self._get_state()

            final_ic = int(self.env.observation["IrInstructionCount"])
            reduction_pct = (initial_ic - final_ic) / initial_ic * 100
            results.append({
                "uri": uri,
                "short_name": uri.split("/")[-1],
                "initial_ic": initial_ic,
                "final_ic": final_ic,
                "reduction_pct": round(reduction_pct, 2),
            })

        self.policy.train()

        total_initial = sum(r["initial_ic"] for r in results)
        total_final = sum(r["final_ic"] for r in results)
        avg_reduction = (total_initial - total_final) / total_initial * 100

        return total_final, avg_reduction, results

    def train(self, save_dir="results/ppo_autophase"):
        """Full training loop."""
        os.makedirs(save_dir, exist_ok=True)

        print("=" * 70)
        print(f"PPO + AUTOPHASE TRAINING (seed={self.seed})")
        print("=" * 70)
        print(f"  Action space: {self.num_actions} passes (reduced)")
        print(f"  Train benchmarks: {len(self.train_uris)}")
        print(f"  Val benchmarks: {len(self.val_uris)}")
        print(f"  Total budget: {self.total_env_steps} steps")
        print(f"  Collect per update: {self.collect_steps} steps")
        print()

        start_time = time.time()
        update_num = 0

        while self.total_steps < self.total_env_steps:
            update_num += 1
            t0 = time.time()

            # Collect rollouts
            episode_rewards = self.collect_rollouts()
            avg_ep_reward = np.mean(episode_rewards) if episode_rewards else 0

            # PPO update
            losses = self.update()

            elapsed = time.time() - t0
            steps_per_sec = self.collect_steps / elapsed

            print(
                f"  Update {update_num:>3} | Steps: {self.total_steps:>7}/{self.total_env_steps} | "
                f"Ep reward: {avg_ep_reward:>+.4f} | "
                f"P loss: {losses['policy_loss']:.4f} | V loss: {losses['value_loss']:.4f} | "
                f"Entropy: {losses['entropy']:.3f} | {steps_per_sec:.0f} steps/s"
            )

            log_entry = {
                "update": update_num,
                "total_steps": self.total_steps,
                "episodes": self.episode_count,
                "avg_episode_reward": round(avg_ep_reward, 6),
                "policy_loss": round(losses["policy_loss"], 6),
                "value_loss": round(losses["value_loss"], 6),
                "entropy": round(losses["entropy"], 4),
            }

            # Validation check
            if self.total_steps % self.val_interval < self.collect_steps:
                val_ic, val_reduction, val_results = self.evaluate(self.val_uris, "val")
                print(f"         VAL | Total IC: {val_ic} | Reduction: {val_reduction:.2f}%")

                log_entry["val_total_ic"] = val_ic
                log_entry["val_reduction_pct"] = round(val_reduction, 2)
                log_entry["val_details"] = val_results

                # Save best checkpoint
                if val_ic < self.best_val_score:
                    self.best_val_score = val_ic
                    self._save_checkpoint(save_dir, "best")
                    print(f"         NEW BEST val IC: {val_ic}")

            self.training_log.append(log_entry)

        # Final save
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
            "config": self.config,
            "num_actions": self.num_actions,
            "log": self.training_log,
        }
        with open(os.path.join(save_dir, f"training_log_seed{self.seed}.json"), "w") as f:
            json.dump(log_output, f, indent=2)

        print(f"\n  Training complete in {total_time / 60:.1f} minutes")
        print(f"  Best validation IC: {self.best_val_score}")

        return self.best_val_score

    def _save_checkpoint(self, save_dir, tag):
        """Save model checkpoint."""
        path = os.path.join(save_dir, f"checkpoint_{tag}_seed{self.seed}.pt")
        torch.save({
            "policy_state_dict": self.policy.state_dict(),
            "value_state_dict": self.value_fn.state_dict(),
            "total_steps": self.total_steps,
            "best_val_score": self.best_val_score,
            "seed": self.seed,
        }, path)

    def load_checkpoint(self, path):
        """Load model checkpoint."""
        ckpt = torch.load(path, weights_only=True)
        self.policy.load_state_dict(ckpt["policy_state_dict"])
        self.value_fn.load_state_dict(ckpt["value_state_dict"])
        self.total_steps = ckpt["total_steps"]
        self.best_val_score = ckpt["best_val_score"]

    def close(self):
        self.env.close()
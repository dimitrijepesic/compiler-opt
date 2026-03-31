# src/agents/nn_agent_fast.py

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import compiler_gym
import json
import os


class NeuralNetwork(nn.Module):
    """Neural network for pass prediction."""

    def __init__(self, input_dim=56, hidden_dim=256, num_actions=124):
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, num_actions)
        )
    
    def forward(self, x):
        return self.network(x)
    
    def predict(self, x):
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            return torch.argmax(logits, dim=-1)


class NNAgentFast:
    """
    Fast Neural Network agent that loads pre-collected data.
    """

    def __init__(self, benchmark, hidden_dim=256, lr=3e-4):
        self.benchmark = benchmark
        self.hidden_dim = hidden_dim
        self.lr = lr

        # Create environment
        self.env = compiler_gym.make("llvm-ic-v0")
        self.env.reset(benchmark=benchmark)

        self.num_actions = self.env.action_space.n
        self.input_dim = 56

        # Create model
        self.model = NeuralNetwork(
            input_dim=self.input_dim,
            hidden_dim=self.hidden_dim,
            num_actions=self.num_actions
        )

        self.criterion = nn.CrossEntropyLoss()
        
        self.best_score = None
        self.best_sequence = []

    def load_data(self, data_path="data/greedy_trajectories.json"):
        """Load pre-collected training data."""
        print(f"   Loading data from {data_path}...")
        
        with open(data_path, "r") as f:
            raw_data = json.load(f)
        
        features = np.array([d["features"] for d in raw_data], dtype=np.float32)
        actions = np.array([d["action"] for d in raw_data], dtype=np.int64)
        
        print(f"   Loaded {len(features)} samples")
        
        return features, actions

    def train_network(self, features, actions, epochs=300, batch_size=64):
        """Train the neural network."""
        print(f"   Training for {epochs} epochs...")

        # Convert to tensors
        all_features = torch.tensor(features, dtype=torch.float32)
        all_actions = torch.tensor(actions, dtype=torch.long)

        # Split train/val (80/20)
        data_size = len(features)
        split_idx = int(data_size * 0.8)
        indices = torch.randperm(data_size)

        train_features = all_features[indices[:split_idx]]
        train_actions = all_actions[indices[:split_idx]]
        val_features = all_features[indices[split_idx:]]
        val_actions = all_actions[indices[split_idx:]]

        print(f"   Train: {len(train_features)}, Val: {len(val_features)}")

        # Optimizer with weight decay (regularization)
        optimizer = optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=1e-4)
        
        # Learning rate scheduler
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

        best_val_acc = 0
        best_model_state = None

        for epoch in range(epochs):
            self.model.train()
            
            # Shuffle
            perm = torch.randperm(len(train_features))
            train_f = train_features[perm]
            train_a = train_actions[perm]

            # Mini-batch training
            epoch_loss = 0
            num_batches = 0

            for i in range(0, len(train_f), batch_size):
                batch_f = train_f[i:i+batch_size]
                batch_a = train_a[i:i+batch_size]
                
                if len(batch_f) < 2:  # BatchNorm needs at least 2 samples
                    continue

                logits = self.model(batch_f)
                loss = self.criterion(logits, batch_a)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
                num_batches += 1

            scheduler.step()
            
            # Evaluate every 30 epochs
            if (epoch + 1) % 30 == 0:
                self.model.eval()
                with torch.no_grad():
                    train_preds = self.model(train_features).argmax(dim=-1)
                    train_acc = (train_preds == train_actions).float().mean()

                    val_preds = self.model(val_features).argmax(dim=-1)
                    val_acc = (val_preds == val_actions).float().mean()

                    if val_acc > best_val_acc:
                        best_val_acc = val_acc
                        best_model_state = self.model.state_dict().copy()

                avg_loss = epoch_loss / max(num_batches, 1)
                lr_now = scheduler.get_last_lr()[0]
                print(f"      Epoch {epoch+1:>3}/{epochs}, Loss: {avg_loss:.4f}, "
                      f"Train: {train_acc:.1%}, Val: {val_acc:.1%}, LR: {lr_now:.6f}")

        # Load best model
        if best_model_state:
            self.model.load_state_dict(best_model_state)
        
        print(f"   Best validation accuracy: {best_val_acc:.1%}")

    def evaluate(self, steps=45):
        """Run trained network on target benchmark."""
        print("   Evaluating...")

        self.model.eval()
        self.env.reset(benchmark=self.benchmark)

        initial_ic = self.env.observation["IrInstructionCount"]
        actions_taken = []

        for step in range(steps):
            try:
                autophase = self.env.observation["Autophase"]
                features = np.log1p(np.array(autophase, dtype=np.float32))
            except:
                break

            features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            action = self.model.predict(features_tensor).item()

            try:
                self.env.step(action)
                actions_taken.append(action)
            except:
                continue

        final_ic = self.env.observation["IrInstructionCount"]
        return final_ic, actions_taken, initial_ic

    def train(self, data_path="data/greedy_trajectories.json", epochs=300):
        """Full training pipeline."""
        print(f"-- NN Agent (Fast) na {self.benchmark}")

        # Load data
        features, actions = self.load_data(data_path)

        # Train
        self.train_network(features, actions, epochs=epochs)

        # Evaluate
        final_ic, actions_taken, initial_ic = self.evaluate()

        self.best_score = final_ic
        self.best_sequence = actions_taken

        reduction = (initial_ic - final_ic) / initial_ic * 100
        print(f"\n   Rezultat: {initial_ic} -> {final_ic} ({reduction:.1f}% redukcija)")

        return self.best_score, self.best_sequence

    def close(self):
        self.env.close()


if __name__ == "__main__":
    # First collect data (run once)
    if not os.path.exists("data/greedy_trajectories.json"):
        print("Data not found. Run: python src/data/collect_and_save.py")
        exit(1)
    
    agent = NNAgentFast("benchmark://cbench-v1/qsort")
    score, _ = agent.train(epochs=300)
    print(f"\nFinal: {score}")
    agent.close()
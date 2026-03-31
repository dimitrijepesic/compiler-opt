import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import compiler_gym
from collections import deque
import random


class QNetwork(nn.Module):
    """
    Q-Network: predicts Q-value for each action given state.
    """
    
    def __init__(self, state_dim=56, hidden_dim=128, num_actions=124):
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_actions),
        )
    
    def forward(self, x):
        return self.network(x)


class DQNAgent:
    """
    Deep Q-Network agent for compiler optimization.
    """
    
    def __init__(self, benchmark, hidden_dim=128, lr=1e-3, gamma=0.99, epsilon=0.3):
        self.benchmark = benchmark
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995
        
        # Environment
        self.env = compiler_gym.make("llvm-ic-v0")
        self.env.reset(benchmark=benchmark)
        
        self.num_actions = self.env.action_space.n
        self.state_dim = 56
        
        # Networks
        self.q_network = QNetwork(self.state_dim, hidden_dim, self.num_actions)
        self.target_network = QNetwork(self.state_dim, hidden_dim, self.num_actions)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        
        # Replay buffer
        self.replay_buffer = deque(maxlen=10000)
        
        self.best_score = float('inf')
        self.best_sequence = []
        
    def _get_state(self, env=None):
        """Get Autophase features as state."""
        if env is None:
            env = self.env
        try:
            autophase = env.observation["Autophase"]
            state = np.array(autophase, dtype=np.float32)
            state = np.log1p(state)  # Normalize
            return state
        except:
            return np.zeros(self.state_dim, dtype=np.float32)
    
    def select_action(self, state, training=True):
        """Epsilon-greedy action selection."""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        
        with torch.no_grad():
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            q_values = self.q_network(state_tensor)
            return torch.argmax(q_values, dim=-1).item()
    
    def train_step(self, batch_size=64):
        """One training step on a batch from replay buffer."""
        if len(self.replay_buffer) < batch_size:
            return 0
        
        batch = random.sample(self.replay_buffer, batch_size)
        
        states = torch.tensor([x[0] for x in batch], dtype=torch.float32)
        actions = torch.tensor([x[1] for x in batch], dtype=torch.long)
        rewards = torch.tensor([x[2] for x in batch], dtype=torch.float32)
        next_states = torch.tensor([x[3] for x in batch], dtype=torch.float32)
        dones = torch.tensor([x[4] for x in batch], dtype=torch.float32)
        
        # Current Q values
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze()
        
        # Target Q values
        with torch.no_grad():
            next_q = self.target_network(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)
        
        # Loss
        loss = nn.MSELoss()(current_q, target_q)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def train(self, episodes=100, steps_per_episode=30, batch_size=64):
        """Train the DQN agent."""
        print(f"-- DQN agent na {self.benchmark}")
        print(f"   Episodes: {episodes}, Steps: {steps_per_episode}")
        
        self.env.reset(benchmark=self.benchmark)
        initial_ic = self.env.observation["IrInstructionCount"]
        print(f"   Pocetna velicina: {initial_ic}")
        
        episode_rewards = []
        
        for episode in range(episodes):
            self.env.reset(benchmark=self.benchmark)
            state = self._get_state()
            
            episode_reward = 0
            prev_ic = initial_ic
            actions_taken = []
            
            for step in range(steps_per_episode):
                # Select action
                action = self.select_action(state, training=True)
                
                # Take action
                try:
                    self.env.step(action)
                    actions_taken.append(action)
                except:
                    continue
                
                # Get new state and reward
                next_state = self._get_state()
                current_ic = self.env.observation["IrInstructionCount"]
                
                # Reward: improvement in IC (normalized)
                reward = (prev_ic - current_ic) / initial_ic
                prev_ic = current_ic
                
                done = (step == steps_per_episode - 1)
                
                # Store transition
                self.replay_buffer.append((state, action, reward, next_state, done))
                
                state = next_state
                episode_reward += reward
                
                # Train
                self.train_step(batch_size)
            
            # Update target network periodically
            if episode % 10 == 0:
                self.target_network.load_state_dict(self.q_network.state_dict())
            
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
            # Track best
            final_ic = self.env.observation["IrInstructionCount"]
            if final_ic < self.best_score:
                self.best_score = final_ic
                self.best_sequence = actions_taken.copy()
            
            episode_rewards.append(episode_reward)
            
            if (episode + 1) % 20 == 0:
                avg_reward = np.mean(episode_rewards[-20:])
                print(f"   Episode {episode + 1}/{episodes}, Avg Reward: {avg_reward:.4f}, Best IC: {self.best_score}, Epsilon: {self.epsilon:.3f}")
        
        print(f"\nDQN ZAVRSIO. Najbolji: {self.best_score}")
        return self.best_score, self.best_sequence
    
    def close(self):
        self.env.close()


if __name__ == "__main__":
    agent = DQNAgent("benchmark://cbench-v1/qsort")
    score, actions = agent.train(episodes=50, steps_per_episode=30)
    print(f"\nFinal score: {score}")
    agent.close()
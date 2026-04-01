import torch
import torch.nn as nn


class ValueMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, num_layers=2):
        super().__init__()

        layers = []
        in_dim = input_dim
        for _ in range(num_layers):
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.ReLU())
            in_dim = hidden_dim
        layers.append(nn.Linear(hidden_dim, 1))

        self.network = nn.Sequential(*layers)

    def forward(self, state):
        return self.network(state).squeeze(-1)
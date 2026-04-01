import torch
import torch.nn as nn
from torch_geometric.nn import SAGEConv, global_mean_pool
from torch_geometric.data import Data, Batch


class GNNEncoder(nn.Module):
    """
    GraphSAGE encoder for program graphs.

    Input: PyG Data with one-hot opcode node features
    Output: fixed-size program embedding vector
    """

    def __init__(self, input_dim, hidden_dim=128, output_dim=128,
                 num_layers=3, dropout=0.1, aggregation="mean"):
        super().__init__()

        self.num_layers = num_layers
        self.dropout = dropout

        # Input projection from one-hot opcodes to embedding space
        self.input_proj = nn.Linear(input_dim, hidden_dim)

        # GraphSAGE convolution layers
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()

        for i in range(num_layers):
            self.convs.append(SAGEConv(hidden_dim, hidden_dim, aggr=aggregation))
            self.norms.append(nn.LayerNorm(hidden_dim))

        # Output projection
        self.output_proj = nn.Linear(hidden_dim, output_dim)

        self.drop = nn.Dropout(dropout)

    def forward(self, data):
        x = data.x
        edge_index = data.edge_index
        batch = data.batch if hasattr(data, "batch") and data.batch is not None else None

        # Input projection
        x = self.input_proj(x)
        x = torch.relu(x)

        # Message passing layers
        for i in range(self.num_layers):
            residual = x
            x = self.convs[i](x, edge_index)
            x = self.norms[i](x)
            x = torch.relu(x)
            x = self.drop(x)
            # Residual connection
            x = x + residual

        # Global mean pooling: aggregate all node embeddings into one vector
        if batch is None:
            # Single graph — mean over all nodes
            x = x.mean(dim=0, keepdim=True)
        else:
            x = global_mean_pool(x, batch)

        # Output projection
        embedding = self.output_proj(x)

        return embedding

    @staticmethod
    def batch_graphs(graph_list):
        return Batch.from_data_list(graph_list)
import torch
import torch.nn as nn
from torch_geometric.nn import SAGEConv, global_mean_pool
from torch_geometric.data import Data, Batch


class GNNEncoder(nn.Module):
    """
    Edge-type-aware GraphSAGE encoder for program graphs.

    Each layer runs two SAGEConv convolutions — one over control-flow
    edges (edge_type == 0), one over data-flow edges (edge_type == 1) —
    and sums their outputs. This lets the encoder treat "next instruction"
    and "value dependency" as distinct relations instead of collapsing
    them into a single edge set.

    Input: PyG Data with node features and edge_type vector
    Output: fixed-size program embedding vector
    """

    NUM_EDGE_TYPES = 2  # 0 = CFG, 1 = DFG

    def __init__(self, input_dim, hidden_dim=128, output_dim=128,
                 num_layers=3, dropout=0.1, aggregation="mean"):
        super().__init__()

        self.num_layers = num_layers
        self.dropout = dropout

        # Input projection from raw node features to embedding space
        self.input_proj = nn.Linear(input_dim, hidden_dim)

        # Per-layer, per-edge-type GraphSAGE convolutions
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()

        for _ in range(num_layers):
            self.convs.append(nn.ModuleList([
                SAGEConv(hidden_dim, hidden_dim, aggr=aggregation)
                for _ in range(self.NUM_EDGE_TYPES)
            ]))
            self.norms.append(nn.LayerNorm(hidden_dim))

        # Output projection
        self.output_proj = nn.Linear(hidden_dim, output_dim)

        self.drop = nn.Dropout(dropout)

    def forward(self, data):
        x = data.x
        edge_index = data.edge_index
        edge_type = data.edge_type
        batch = data.batch if hasattr(data, "batch") and data.batch is not None else None

        # Split edges by type once, reuse across layers
        typed_edges = []
        for t in range(self.NUM_EDGE_TYPES):
            mask = edge_type == t
            typed_edges.append(edge_index[:, mask])

        # Input projection
        x = self.input_proj(x)
        x = torch.relu(x)

        # Message passing layers
        for i in range(self.num_layers):
            residual = x
            out = None
            for t in range(self.NUM_EDGE_TYPES):
                h = self.convs[i][t](x, typed_edges[t])
                out = h if out is None else out + h
            x = self.norms[i](out)
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

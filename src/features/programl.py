import re
import hashlib
import os
import json
import torch
import numpy as np
from torch_geometric.data import Data


# --- LLVM opcode vocabulary ---
# Common LLVM IR opcodes. Unknown opcodes map to index 0.
OPCODES = [
    "<unknown>",
    # Terminator
    "ret", "br", "switch", "unreachable", "invoke", "resume",
    # Binary
    "add", "fadd", "sub", "fsub", "mul", "fmul",
    "udiv", "sdiv", "fdiv", "urem", "srem", "frem",
    # Bitwise
    "shl", "lshr", "ashr", "and", "or", "xor",
    # Memory
    "alloca", "load", "store", "getelementptr", "fence",
    "atomicrmw", "cmpxchg",
    # Cast
    "trunc", "zext", "sext", "fptrunc", "fpext",
    "fptoui", "fptosi", "uitofp", "sitofp",
    "ptrtoint", "inttoptr", "bitcast", "addrspacecast",
    # Other
    "icmp", "fcmp", "phi", "call", "select",
    "extractelement", "insertelement", "shufflevector",
    "extractvalue", "insertvalue", "landingpad",
    # Aggregate
    "va_arg",
]

OPCODE_TO_IDX = {op: i for i, op in enumerate(OPCODES)}
NUM_OPCODES = len(OPCODES)


def _parse_opcode(line):
    """Extract the LLVM opcode from an instruction line."""
    line = line.strip()

    # Skip non-instruction lines
    if not line or line.startswith(";") or line.startswith("!"):
        return None

    # Handle assignment: %var = opcode ...
    if "=" in line:
        rhs = line.split("=", 1)[1].strip()
    else:
        rhs = line

    # First word of RHS is the opcode
    # Handle special cases like "tail call", "musttail call"
    rhs = re.sub(r"^(tail|musttail|notail)\s+", "", rhs)

    match = re.match(r"([a-z_][a-z0-9_]*)", rhs)
    if match:
        return match.group(1)
    return None


def _parse_ssa_defs_uses(line):
    """Extract SSA definitions and uses from an instruction line."""
    line = line.strip()
    defs = []
    uses = []

    # Definition: %var = ...
    if "=" in line:
        lhs = line.split("=", 1)[0].strip()
        def_match = re.match(r"(%[\w.]+)", lhs)
        if def_match:
            defs.append(def_match.group(1))

    # Uses: all %var references on the RHS (or whole line if no =)
    rhs = line.split("=", 1)[1] if "=" in line else line

    # Find all %name references (SSA values)
    uses = re.findall(r"%[\w.]+", rhs)

    # Remove the def from uses if it accidentally appears
    uses = [u for u in uses if u not in defs]

    return defs, uses


def parse_llvm_ir(ir_text):
    """
    Parse LLVM IR text into a graph structure.

    Returns:
        nodes: list of {"opcode": str, "opcode_idx": int, "block": str}
        cfg_edges: list of (src_idx, dst_idx) — control flow
        dfg_edges: list of (src_idx, dst_idx) — data flow
    """
    lines = ir_text.split("\n")

    nodes = []
    cfg_edges = []
    dfg_edges = []

    # Track which block we're in
    current_block = None
    block_first_node = {}   # block_label -> first node index in that block
    block_last_node = {}    # block_label -> last node index
    prev_node_idx = None

    # SSA def->node mapping for data flow edges
    ssa_def_node = {}  # %var_name -> node_index

    # Collect branch targets for cross-block CFG edges
    branch_targets = []  # (from_node_idx, target_block_label)

    in_function = False

    for line in lines:
        stripped = line.strip()

        # Track function boundaries
        if re.match(r"define\s+", stripped):
            in_function = True
            current_block = "entry"
            prev_node_idx = None
            continue

        if stripped == "}" and in_function:
            in_function = False
            current_block = None
            prev_node_idx = None
            continue

        if not in_function:
            continue

        # Basic block label: "name:" or ";<label>:N"
        block_match = re.match(r"^([\w.]+):\s*", stripped)
        if block_match:
            current_block = block_match.group(1)
            prev_node_idx = None
            continue

        # Also catch numeric labels like "3:" at the start of a line
        num_label_match = re.match(r"^(\d+):\s*", stripped)
        if num_label_match:
            current_block = num_label_match.group(1)
            prev_node_idx = None
            continue

        # Skip non-instructions
        if stripped.startswith(";") or stripped.startswith("!") or not stripped:
            continue

        # Parse opcode
        opcode = _parse_opcode(stripped)
        if opcode is None:
            continue

        opcode_idx = OPCODE_TO_IDX.get(opcode, 0)

        node_idx = len(nodes)
        nodes.append({
            "opcode": opcode,
            "opcode_idx": opcode_idx,
            "block": current_block or "unknown",
        })

        # Track block boundaries
        if current_block:
            if current_block not in block_first_node:
                block_first_node[current_block] = node_idx
            block_last_node[current_block] = node_idx

        # Intra-block CFG edge: sequential instructions in same block
        if prev_node_idx is not None:
            cfg_edges.append((prev_node_idx, node_idx))

        prev_node_idx = node_idx

        # Parse SSA defs and uses for data flow
        defs, uses = _parse_ssa_defs_uses(stripped)

        for d in defs:
            ssa_def_node[d] = node_idx

        for u in uses:
            if u in ssa_def_node:
                # Data flow edge: from definition to use
                dfg_edges.append((ssa_def_node[u], node_idx))

        # Track branch targets for cross-block CFG edges
        if opcode == "br":
            # Unconditional: br label %target
            # Conditional: br i1 %cond, label %true, label %false
            targets = re.findall(r"label\s+%?([\w.]+)", stripped)
            for t in targets:
                branch_targets.append((node_idx, t))

        elif opcode == "switch":
            targets = re.findall(r"label\s+%?([\w.]+)", stripped)
            for t in targets:
                branch_targets.append((node_idx, t))

        elif opcode == "invoke":
            # invoke has normal and unwind destinations
            targets = re.findall(r"label\s+%?([\w.]+)", stripped)
            for t in targets:
                branch_targets.append((node_idx, t))

    # Resolve cross-block CFG edges
    for from_idx, target_label in branch_targets:
        if target_label in block_first_node:
            cfg_edges.append((from_idx, block_first_node[target_label]))

    return nodes, cfg_edges, dfg_edges


def ir_to_pyg_data(ir_text):
    """
    Convert LLVM IR text to a PyTorch Geometric Data object.

    Node features: one-hot opcode encoding (NUM_OPCODES dims)
    Edge index: combined CFG + DFG edges
    Edge attr: 0 for CFG, 1 for DFG

    Returns:
        Data object with:
            x: [num_nodes, NUM_OPCODES] float tensor
            edge_index: [2, num_edges] long tensor
            edge_type: [num_edges] long tensor (0=CFG, 1=DFG)
    """
    nodes, cfg_edges, dfg_edges = parse_llvm_ir(ir_text)

    if len(nodes) == 0:
        # Return minimal valid graph
        return Data(
            x=torch.zeros(1, NUM_OPCODES),
            edge_index=torch.zeros(2, 0, dtype=torch.long),
            edge_type=torch.zeros(0, dtype=torch.long),
            num_nodes=1,
        )

    # Node features: one-hot opcode
    x = torch.zeros(len(nodes), NUM_OPCODES)
    for i, node in enumerate(nodes):
        x[i, node["opcode_idx"]] = 1.0

    # Combine edges
    all_edges = []
    edge_types = []

    for src, dst in cfg_edges:
        all_edges.append((src, dst))
        edge_types.append(0)

    for src, dst in dfg_edges:
        all_edges.append((src, dst))
        edge_types.append(1)

    if all_edges:
        edge_index = torch.tensor(all_edges, dtype=torch.long).t().contiguous()
        edge_type = torch.tensor(edge_types, dtype=torch.long)
    else:
        edge_index = torch.zeros(2, 0, dtype=torch.long)
        edge_type = torch.zeros(0, dtype=torch.long)

    return Data(
        x=x,
        edge_index=edge_index,
        edge_type=edge_type,
        num_nodes=len(nodes),
    )


class IRGraphCache:
    """Disk cache for parsed IR graphs to avoid re-extraction during training."""

    def __init__(self, cache_dir="data/cached_graphs"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _key(self, ir_text):
        """Hash the IR text to get a cache key."""
        return hashlib.md5(ir_text.encode()).hexdigest()

    def get(self, ir_text):
        """Try to load cached graph. Returns Data or None."""
        key = self._key(ir_text)
        path = os.path.join(self.cache_dir, f"{key}.pt")
        if os.path.exists(path):
            return torch.load(path, weights_only=False)
        return None

    def put(self, ir_text, data):
        """Cache a graph to disk."""
        key = self._key(ir_text)
        path = os.path.join(self.cache_dir, f"{key}.pt")
        torch.save(data, path)

    def get_or_extract(self, ir_text):
        """Get from cache or extract and cache."""
        cached = self.get(ir_text)
        if cached is not None:
            return cached

        data = ir_to_pyg_data(ir_text)
        self.put(ir_text, data)
        return data
import re
import hashlib
import os
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

# Scalar node features appended after the one-hot opcode block:
#   is_terminator, log1p(num_uses)/3, has_def, is_memory_op
NUM_SCALAR_FEATURES = 4
NODE_FEATURE_DIM = NUM_OPCODES + NUM_SCALAR_FEATURES

# Bump when node features or graph structure change, so stale cached
# graphs from older feature layouts are never reused.
FEATURE_VERSION = "v2"

TERMINATOR_OPCODES = {"ret", "br", "switch", "unreachable", "invoke", "resume"}
MEMORY_OPCODES = {"alloca", "load", "store", "getelementptr", "fence",
                  "atomicrmw", "cmpxchg"}


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
        cfg_edges: list of (src_idx, dst_idx), control flow
        dfg_edges: list of (src_idx, dst_idx), data flow
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

        # Parse SSA defs and uses (also feeds scalar node features)
        defs, uses = _parse_ssa_defs_uses(stripped)

        node_idx = len(nodes)
        nodes.append({
            "opcode": opcode,
            "opcode_idx": opcode_idx,
            "block": current_block or "unknown",
            "is_terminator": opcode in TERMINATOR_OPCODES,
            "num_uses": len(uses),
            "has_def": len(defs) > 0,
            "is_memory_op": opcode in MEMORY_OPCODES,
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

    Node features: one-hot opcode (NUM_OPCODES dims) + scalar features
    (is_terminator, log1p(num_uses)/3, has_def, is_memory_op)
    Edge index: combined CFG + DFG edges
    Edge attr: 0 for CFG, 1 for DFG

    Returns:
        Data object with:
            x: [num_nodes, NODE_FEATURE_DIM] float tensor
            edge_index: [2, num_edges] long tensor
            edge_type: [num_edges] long tensor (0=CFG, 1=DFG)
    """
    nodes, cfg_edges, dfg_edges = parse_llvm_ir(ir_text)

    if len(nodes) == 0:
        # Return minimal valid graph
        return Data(
            x=torch.zeros(1, NODE_FEATURE_DIM),
            edge_index=torch.zeros(2, 0, dtype=torch.long),
            edge_type=torch.zeros(0, dtype=torch.long),
            num_nodes=1,
        )

    x = torch.zeros(len(nodes), NODE_FEATURE_DIM)
    for i, node in enumerate(nodes):
        x[i, node["opcode_idx"]] = 1.0
        x[i, NUM_OPCODES + 0] = 1.0 if node["is_terminator"] else 0.0
        x[i, NUM_OPCODES + 1] = np.log1p(node["num_uses"]) / 3.0
        x[i, NUM_OPCODES + 2] = 1.0 if node["has_def"] else 0.0
        x[i, NUM_OPCODES + 3] = 1.0 if node["is_memory_op"] else 0.0

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
    """Disk cache for parsed IR graphs to avoid re-extraction during training.

    Cache dir resolution order: explicit arg, COMPILER_OPT_CACHE_DIR env var
    (useful to keep the cache on a fast native filesystem under WSL),
    then the in-repo default. Keys embed FEATURE_VERSION so graphs cached
    under an older feature layout are never reused.
    """

    def __init__(self, cache_dir=None):
        if cache_dir is None:
            cache_dir = os.environ.get(
                "COMPILER_OPT_CACHE_DIR",
                os.path.join("data", f"cached_graphs_{FEATURE_VERSION}"),
            )
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        # Growth guards (the cache once grew by ~40 GB per training run and
        # filled the host disk): stop writing new entries when the Windows
        # host drive backing /mnt/c runs low, or after this process has
        # written its cap. Reads are never blocked.
        self._min_host_free = float(os.environ.get(
            "COMPILER_OPT_CACHE_MIN_HOST_FREE_GB", 15)) * 1e9
        self._write_cap = float(os.environ.get(
            "COMPILER_OPT_CACHE_WRITE_CAP_GB", 30)) * 1e9
        self._bytes_written = 0
        self._write_guard_tripped = False

    def _key(self, ir_text):
        """Hash the IR text (+ feature version) to get a cache key."""
        return hashlib.md5(
            (FEATURE_VERSION + ir_text).encode()
        ).hexdigest()

    def get(self, ir_text):
        """Try to load cached graph. Returns Data or None."""
        key = self._key(ir_text)
        path = os.path.join(self.cache_dir, f"{key}.pt")
        if os.path.exists(path):
            return torch.load(path, weights_only=False)
        return None

    def _write_allowed(self):
        if self._write_guard_tripped:
            return False
        if self._bytes_written > self._write_cap:
            self._write_guard_tripped = True
            print("[IRGraphCache] write cap reached; caching disabled "
                  "for the rest of this process")
            return False
        try:
            st = os.statvfs("/mnt/c")
            if st.f_bavail * st.f_frsize < self._min_host_free:
                return False
        except OSError:
            pass
        return True

    def put(self, ir_text, data):
        """Cache a graph to disk (skipped when the growth guards trip)."""
        if not self._write_allowed():
            return
        key = self._key(ir_text)
        path = os.path.join(self.cache_dir, f"{key}.pt")
        torch.save(data, path)
        try:
            self._bytes_written += os.path.getsize(path)
        except OSError:
            pass

    def get_or_extract(self, ir_text):
        """Get from cache or extract and cache."""
        cached = self.get(ir_text)
        if cached is not None:
            return cached

        data = ir_to_pyg_data(ir_text)
        self.put(ir_text, data)
        return data
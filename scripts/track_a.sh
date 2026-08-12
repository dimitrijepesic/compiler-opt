#!/usr/bin/env bash
# Track A: best-of-k sampling evaluation of the existing checkpoints.
set -euo pipefail
cd "$(dirname "$0")/.."
source "${VENV:-$HOME/venv-cgym}/bin/activate"
export COMPILER_OPT_CACHE_DIR="${COMPILER_OPT_CACHE_DIR:-$HOME/compiler_opt_graph_cache}"
python scripts/evaluate_sampling.py --k 8
echo "=== TRACK-A-DONE ==="

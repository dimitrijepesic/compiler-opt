#!/bin/bash
# Runs llvm18_transfer.py inside the ubuntu-cgym WSL environment, with a
# separately apt-installed LLVM 18 toolchain (apt.llvm.org's llvm.sh 18)
# ahead of CompilerGym's bundled LLVM 10 on PATH.
#
#   wsl -d ubuntu-cgym -- bash scripts/run_llvm18_transfer.sh
set -e
cd "$(dirname "$0")/.."
export PATH="/usr/lib/llvm-18/bin:$PATH"
source "${VENV:-$HOME/venv-cgym}/bin/activate"
python scripts/llvm18_transfer.py --check-passes
python scripts/llvm18_transfer.py --out-dir results/llvm18_transfer

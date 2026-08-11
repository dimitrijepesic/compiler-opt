#!/usr/bin/env bash
# One-time environment setup inside WSL Ubuntu 22.04.
# Creates the venv in the Linux home dir (fast filesystem) and installs
# the pinned dependency stack CompilerGym 0.2.5 needs.
set -euo pipefail

VENV="${VENV:-$HOME/venv-cgym}"

sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv libtinfo5

python3.10 -m venv "$VENV"
source "$VENV/bin/activate"

# Order matters: old gym needs old pip/setuptools/wheel
pip install "pip<24.1" setuptools==65.5.0 wheel==0.38.4
pip install gym==0.21.0
pip install compiler-gym==0.2.5 "numpy<2" pyyaml tqdm scipy matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install torch-geometric

python - <<'EOF'
import compiler_gym
env = compiler_gym.make("llvm-ic-v0")
env.reset(benchmark="benchmark://cBench-v1/crc32")
print("smoke test OK — crc32 O0 IC:", env.observation["IrInstructionCount"])
print("real O3 IC:", env.observation["IrInstructionCountO3"])
env.close()
EOF

echo "Environment ready: source $VENV/bin/activate"

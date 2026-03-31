# RISC-V Code Density Optimization using RL

## Overview
This project explores the use of **Reinforcement Learning**, **Genetic Algorithms**, and **Greedy Search** to optimize code size (Code Density) for LLVM-based compilers using the `CompilerGym` environment.

## Experiments
1. **Baseline:** Standard `-O0` compilation.
2. **Random Search:** Stochastic exploration of the optimization space.
3. **Greedy Search:** Deterministic, step-wise optimization.
4. **Genetic Algorithm:** Evolutionary approach to escape local minima.

## Results so far (cBench/qsort)
* **Baseline:** 638 instructions
* **Random Search:** 287 instructions
* **Greedy Search:** 271 instructions

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run experiments
python src/baseline_check.py
python src/greedy_search.py

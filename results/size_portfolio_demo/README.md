# Measured-size portfolio demonstrator

`scripts/optimize_size_portfolio.py` produces optimized bitcode and an
object file, selecting by measured pure code-section bytes from a fixed
portfolio and the attribute-controlled CompilerGym service -Oz baseline.
It preserves the input triple, layout and frame-pointer policy. It adds
minsize/optsize only to definitions and verifies every exported IC.

This tool's baseline is an IR-service baseline, not a full source-level
clang -Oz build. See the separate [all-CHStone source check](../size_portfolio_source_check/README.md)
for that stronger reference and fixed-vector executable tests.

## Confirmed examples

- NPB/116, first three sequences plus service -Oz: code section decreases
  from 8,593 to 8,254 bytes (3.95%). Portfolio rank 3 wins even though its
  IC is 2,145 versus the baseline's 1,911. Files: `npb-116/selected.bc`
  and `npb-116/selected.o`. This module was not executed.
- The same canonical bitcode passed through `--bitcode`, with k=1,
  selects rank 1 at 8,294 bytes and reproduces the URI-based candidate.
- The initial four-program functional pilot (adpcm, aes, gsm, sha) passed
  the fixed-vector tests for the baseline, candidates and selected output.
  Its `functional_checks.json` predates the extension that adds a separate
  real-source selection rule; use the all-CHStone report for final claims.

## Usage

Run in the existing LLVM 10 / CompilerGym container, using a fresh output
directory:

```sh
docker start cgym-audit
docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/optimize_size_portfolio.py \
  --benchmark benchmark://npb-v0/116 --k 3 \
  --out results/size_portfolio_demo_repeat/npb-116
```

Use `--bitcode /path/visible/inside/container.bc` instead of `--benchmark`
for an existing LLVM 10-readable input. Both inputs first pass through
CompilerGym canonicalization. Nonempty output directories are rejected.
The tool aborts on failed candidates instead of quietly reducing the budget.

Each directory contains original/annotated input, all candidate bitcode
and objects, `selected.bc`, `selected.o`, and `selection.json`. The JSON
records action sequences, measured sizes, exact ICs, input/tool/portfolio
hashes and the chosen candidate. Baseline wins byte ties.

For k sequences this procedure performs k+1 candidate optimizations and
k+1 object-code measurements, including the baseline. It is not a claim
that k+1 individual compiler passes suffice. A 45-step episode is one
candidate sequence. Wall-time efficiency has not been established.

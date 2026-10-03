# Source-aware portfolio check: all 12 CHStone programs

Three frozen portfolio sequences plus a real source-level clang -Oz reference reduce summed code sections from **32,123 to 31,729 bytes (1.23%)**. Five programs improve and seven return the source-built reference. The no-regression property follows from including that reference, not from universal superiority of the portfolio.

All candidates, the service baseline, the source-built reference, and both selected outputs passed the bundled fixed-vector tests on all 12 programs. This is 7 executions per program (84 total), including duplicate executions of selected candidates; it is not 84 independent test inputs or a proof of semantic equivalence. No runtime performance was measured.

| Program | Real clang -Oz code bytes | Selected code bytes | Reduction | Selected artifact |
|---|---:|---:|---:|---|
| adpcm | 2,908 | 2,841 | +2.30% | portfolio_1 |
| aes | 7,053 | 7,010 | +0.61% | portfolio_1 |
| blowfish | 3,118 | 3,117 | +0.03% | portfolio_1 |
| dfadd | 1,597 | 1,597 | +0.00% | reference_clang_oz |
| dfdiv | 1,581 | 1,581 | +0.00% | reference_clang_oz |
| dfmul | 1,290 | 1,290 | +0.00% | reference_clang_oz |
| dfsin | 3,321 | 3,321 | +0.00% | reference_clang_oz |
| gsm | 2,350 | 2,350 | +0.00% | reference_clang_oz |
| jpeg | 5,744 | 5,483 | +4.54% | portfolio_1 |
| mips | 785 | 763 | +2.80% | portfolio_2 |
| motion | 1,487 | 1,487 | +0.00% | reference_clang_oz |
| sha | 889 | 889 | +0.00% | reference_clang_oz |

## Selection and budgets

Eligible candidates are the actual clang -Oz object and the first three sequences from the existing training-selected portfolio. Portfolio sequences operate on canonical CompilerGym IR with definition-level minsize/optsize. The service baseline is also measured as a diagnostic; it is not eligible in the four-candidate source-aware rule. The validation campaign therefore measured five objects per program even though the source-aware selector has four eligible candidates.

The fixed k=3 choice follows the preceding exploratory analysis on NPB, MiBench and BLAS. This CHStone check was added after seeing that service gains on GSM did not survive comparison against a real source build. It is an exploratory cross-suite control, not a preregistered trial or a new algorithm.

Both choices are retained: `selected.o`/`selected.bc` use the service reference; `source_selected.o`/`source_selected.elf` use the real clang -Oz reference. For source-aware selection there is no exported `source_selected.bc`: the real baseline is a directly compiled object. Do not confuse these artifact pairs.

All comparisons concern relocatable code sections, not the total size of linked executables. Tests run in an amd64 container under Rosetta, using CHStone fixed inputs and expected outputs. Every source-directory file hash was checked against the previous source-build audit. Reference object sizes also reproduced that audit exactly.

The basic IR optimizer is `scripts/optimize_size_portfolio.py`. The source-aware check and executable tests are implemented in `scripts/validate_size_portfolio_demo.py`.

## Reproduce into a fresh directory

```sh
docker start cgym-audit
docker exec -e PYTHONWARNINGS=ignore cgym-audit \
  python scripts/validate_size_portfolio_demo.py --all \
  --out results/size_portfolio_source_check_repeat
```

Existing validation reports and nonempty per-program output directories are rejected to avoid overwriting evidence. Inspect `functional_checks.json` for hashes, flags, outputs and exit codes.

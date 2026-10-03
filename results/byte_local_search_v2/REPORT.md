# Matched-budget byte-search pilot v2: report

Manifest `7807d8ec65bc91d4`; 12 of 12 program records usable.
Twelve previously examined development programs; three random starts reported separately; not a test set.

## Primary quantity: 100 * sum(control24 - local24) / sum(Oz), positive = local arm better

| cohort | n | start 42 | start 43 | start 44 | mean over starts | strict rule, mean |
|---|---:|---:|---:|---:|---:|---:|
| all | 12 | +0.179 (+68 B) | -1.022 (-389 B) | -0.794 (-302 B) | -0.546 | -0.540 |
| without_npb | 10 | +0.239 (+68 B) | -1.368 (-389 B) | -1.062 (-302 B) | -0.731 | -0.723 |
| npb-v0 | 2 | +0.000 (+0 B) | +0.000 (+0 B) | +0.000 (+0 B) | +0.000 | +0.000 |
| mibench-v1 | 2 | +0.000 (+0 B) | -10.110 (-359 B) | -2.844 (-101 B) | -4.318 | -4.318 |
| blas-v0 | 2 | +0.519 (+73 B) | +0.000 (+0 B) | -1.053 (-148 B) | -0.178 | -0.178 |
| chstone-v0 | 2 | -0.064 (-5 B) | -0.382 (-30 B) | -0.599 (-47 B) | -0.348 | -0.348 |
| csmith-v0 | 2 | +0.000 (+0 B) | +0.000 (+0 B) | +0.000 (+0 B) | +0.000 | +0.000 |
| poj104-v1 | 2 | +0.000 (+0 B) | +0.000 (+0 B) | -0.842 (-6 B) | -0.281 | +0.000 |

## Paired outcomes per start (local vs control at 24 attempts, delivered bytes)

| start | local smaller / tie / control smaller | median paired difference (% of program Oz) | median local gain vs Oz | median control gain vs Oz |
|---|---:|---:|---:|---:|
| 42 | 1 / 10 / 1 | +0.000 | 0.000 | 0.000 |
| 43 | 0 / 10 / 2 | +0.000 | 0.000 | 0.000 |
| 44 | 0 / 7 / 5 | +0.000 | 0.000 | 0.000 |

## Each arm vs the same attributed -Oz (ratio of sums, %, with fallback)

| cohort | start | local 8 | local 16 | local 24 | control 8 | control 16 | control 24 |
|---|---|---:|---:|---:|---:|---:|---:|
| all | 42 | 3.261 | 3.261 | 3.453 | 3.261 | 3.274 | 3.274 |
| all | 43 | 1.821 | 1.926 | 1.929 | 1.821 | 2.948 | 2.951 |
| all | 44 | 1.487 | 1.705 | 2.092 | 1.487 | 2.084 | 2.885 |
| without_npb | 42 | 4.366 | 4.366 | 4.622 | 4.366 | 4.383 | 4.383 |
| without_npb | 43 | 2.438 | 2.579 | 2.582 | 2.438 | 3.947 | 3.950 |
| without_npb | 44 | 1.991 | 2.283 | 2.800 | 1.991 | 2.790 | 3.863 |

Strict two-metric fallback at 24 attempts (secondary; search objective unchanged):

| cohort | start | local | control |
|---|---|---:|---:|
| all | 42 | 3.453 | 3.274 |
| all | 43 | 1.929 | 2.951 |
| all | 44 | 2.092 | 2.869 |
| without_npb | 42 | 4.622 | 4.383 |
| without_npb | 43 | 2.582 | 3.950 |
| without_npb | 44 | 2.800 | 3.841 |

## Every program and start (delivered code-section bytes; Oz = attributed service reference)

| program | start | Oz | local 8/16/24 | control 8/16/24 | control24 - local24 | failed L/C | start hashes equal L/C |
|---|---|---:|---|---|---:|---|---|
| blas-v0/25 | 42 | 14036 | 13613/13613/13540 | 13613/13613/13613 | +73 | 0/0 | True/True |
| blas-v0/25 | 43 | 14036 | 13856/13856/13856 | 13856/13856/13856 | +0 | 0/0 | True/True |
| blas-v0/25 | 44 | 14036 | 14015/14015/13868 | 14015/13955/13720 | -148 | 0/0 | True/True |
| blas-v0/288 | 42 | 22 | 22/22/22 | 22/22/22 | +0 | 0/0 | True/True |
| blas-v0/288 | 43 | 22 | 22/22/22 | 22/22/22 | +0 | 0/0 | True/True |
| blas-v0/288 | 44 | 22 | 22/22/22 | 22/22/22 | +0 | 0/0 | True/True |
| chstone-v0/aes | 42 | 7062 | 6886/6886/6886 | 6886/6886/6886 | +0 | 0/0 | True/True |
| chstone-v0/aes | 43 | 7062 | 6993/6953/6953 | 6993/6923/6923 | -30 | 0/0 | True/True |
| chstone-v0/aes | 44 | 7062 | 6962/6962/6962 | 6962/6921/6921 | -41 | 0/0 | True/True |
| chstone-v0/mips | 42 | 785 | 762/762/762 | 762/757/757 | -5 | 0/0 | True/True |
| chstone-v0/mips | 43 | 785 | 759/759/758 | 759/759/758 | +0 | 0/0 | True/True |
| chstone-v0/mips | 44 | 785 | 762/762/762 | 762/757/756 | -6 | 0/0 | True/True |
| mibench-v1/qsort1 | 42 | 293 | 293/293/293 | 293/293/293 | +0 | 0/0 | True/True |
| mibench-v1/qsort1 | 43 | 293 | 293/293/293 | 293/293/293 | +0 | 0/0 | True/True |
| mibench-v1/qsort1 | 44 | 293 | 293/293/293 | 293/293/293 | +0 | 0/0 | True/True |
| mibench-v1/susan-e-2 | 42 | 3258 | 2639/2639/2639 | 2639/2639/2639 | +0 | 0/0 | True/True |
| mibench-v1/susan-e-2 | 43 | 3258 | 2840/2840/2840 | 2840/2481/2481 | -359 | 0/0 | True/True |
| mibench-v1/susan-e-2 | 44 | 3258 | 2836/2753/2753 | 2836/2715/2652 | -101 | 0/0 | True/True |
| npb-v0/119 | 42 | 9589 | 9589/9589/9589 | 9589/9589/9589 | +0 | 0/0 | True/True |
| npb-v0/119 | 43 | 9589 | 9589/9589/9589 | 9589/9589/9589 | +0 | 0/0 | True/True |
| npb-v0/119 | 44 | 9589 | 9589/9589/9589 | 9589/9589/9589 | +0 | 0/0 | True/True |
| npb-v0/16 | 42 | 40 | 40/40/40 | 40/40/40 | +0 | 0/0 | True/True |
| npb-v0/16 | 43 | 40 | 40/40/40 | 40/40/40 | +0 | 0/0 | True/True |
| npb-v0/16 | 44 | 40 | 40/40/40 | 40/40/40 | +0 | 0/0 | True/True |
| poj104-v1/102/1409 | 42 | 562 | 562/562/562 | 562/562/562 | +0 | 0/0 | True/True |
| poj104-v1/102/1409 | 43 | 562 | 562/562/562 | 562/562/562 | +0 | 0/0 | True/True |
| poj104-v1/102/1409 | 44 | 562 | 562/562/562 | 562/562/562 | +0 | 0/0 | True/True |
| poj104-v1/54/59 | 42 | 151 | 151/151/151 | 151/151/151 | +0 | 0/0 | True/True |
| poj104-v1/54/59 | 43 | 151 | 151/151/151 | 151/151/151 | +0 | 0/0 | True/True |
| poj104-v1/54/59 | 44 | 151 | 151/151/151 | 151/151/145 | -6 | 0/0 | True/True |
| csmith-v0/21 | 42 | 243 | 243/243/243 | 243/243/243 | +0 | 0/0 | True/True |
| csmith-v0/21 | 43 | 243 | 243/243/243 | 243/243/243 | +0 | 0/0 | True/True |
| csmith-v0/21 | 44 | 243 | 243/243/243 | 243/243/243 | +0 | 0/0 | True/True |
| csmith-v0/40 | 42 | 2015 | 2015/2015/2015 | 2015/2015/2015 | +0 | 0/0 | True/False |
| csmith-v0/40 | 43 | 2015 | 2015/2015/2015 | 2015/2015/2015 | +0 | 0/0 | True/True |
| csmith-v0/40 | 44 | 2015 | 2015/2015/2015 | 2015/2015/2015 | +0 | 0/0 | False/True |

## Cost (amd64 container under Rosetta 2 on Apple silicon; describes this host only, not native optimization speed)

| arm | accounting attempts | executed | failed | generation s | reset s | optimize s | export s | codegen s | metric s | hash s | attempt total s | arm wall s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| local | 864 | 864 | 0 | 0.275 | 3.4 | 20.6 | 1.2 | 269.3 | 180.6 | 0.2 | 475.3 | 475.6 |
| control | 864 | 864 | 0 | 0.023 | 3.4 | 23.7 | 1.2 | 270.9 | 180.7 | 0.2 | 480.2 | 480.2 |

Reference: 12 executions (one per program, shared by its six runs; accounting 72); optimize 0.3 s, codegen 3.7 s, metrics 2.5 s. Input preparation and reference together 57.3 s; all programs 1017.8 s wall.

## Replay of the frozen starts

Metrics (IC, Berkeley text, code bytes) of all 576 start replays equal the frozen records (otherwise the program would be blocked above).
Hash-only differences: 
- generator://csmith-v0/40 start 42 control attempts [7]
- generator://csmith-v0/40 start 44 local attempts [3]

## Functional checks of delivered objects

| program | status | detail |
|---|---|---|
| blas-v0/25 | unchecked | no functional harness for this suite |
| blas-v0/288 | unchecked | no functional harness for this suite |
| chstone-v0/aes | pass | s42_local_primary: pass, s42_local_strict: pass, s42_control_primary: pass, s42_control_strict: pass, s43_local_primary: pass, s43_local_strict: pass, s43_control_primary: pass, s43_control_strict: pass, s44_local_primary: pass, s44_local_strict: pass, s44_control_primary: pass, s44_control_strict: pass |
| chstone-v0/mips | pass | s42_local_primary: pass, s42_local_strict: pass, s42_control_primary: pass, s42_control_strict: pass, s43_local_primary: pass, s43_local_strict: pass, s43_control_primary: pass, s43_control_strict: pass, s44_local_primary: pass, s44_local_strict: pass, s44_control_primary: pass, s44_control_strict: pass |
| mibench-v1/qsort1 | unchecked | no functional harness for this suite |
| mibench-v1/susan-e-2 | unchecked | no functional harness for this suite |
| npb-v0/119 | unchecked | no functional harness for this suite |
| npb-v0/16 | unchecked | no functional harness for this suite |
| poj104-v1/102/1409 | unchecked | no functional harness for this suite |
| poj104-v1/54/59 | unchecked | no functional harness for this suite |
| csmith-v0/21 | not_needed | every run delivered the reference object |
| csmith-v0/40 | not_needed | every run delivered the reference object |

## Continuation criteria (engineering screening thresholds, not significance tests)

- **C1: FAIL** (>= 0.5): `-0.5456870576693995`
- **C2: FAIL** (> 0 in at least 2 of 3 starts): `{"42": 0.17868404456590287, "43": -1.0221778431784738, "44": -0.7935673743956275}`
- **C3: FAIL** (> 0 and at least 2 non-NPB suites > 0): `{"without_npb_mean": -0.7305261429861283, "suite_means": {"mibench-v1": -4.318032479113865, "blas-v0": -0.17783468487693843, "chstone-v0": -0.34832844823924214, "csmith-v0": 0.0, "poj104-v1": -0.2805049088359046}}`
- **C4: PASS** (no delivered object above Oz; all available functional checks pass): `{"delivered_above_oz": [], "functional_failures": [], "unchecked": ["benchmark://blas-v0/25", "benchmark://blas-v0/288", "benchmark://mibench-v1/qsort1", "benchmark://mibench-v1/susan-e-2", "benchmark://npb-v0/119", "benchmark://npb-v0/16", "benchmark://poj104-v1/102/1409", "benchmark://poj104-v1/54/59"]}`

**Verdict: at least one criterion fails; the contract says to stop this optimizer branch.**

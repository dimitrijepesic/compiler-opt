# GNN sampler vs paired random null with and without size attributes: final tables

Generated 2026-09-16T21:12:09.670367+00:00. Programs in the list: 347. Null records: 347 ok of 347 (failures: 0).

## Attempts, successes, reproduction of the stored original run (plain condition)

| seed | GNN records | complete (both cond.) | paired with null | failed/incomplete | stored 8 samples reproduced | argmax reproduced | best-of-8 reproduced |
|---|---:|---:|---:|---:|---:|---:|---:|
| 42 | 120 | 120 | 120 | 0 (+227 not run) | 120/120 (960/960 samples) | 120/120 | 120/120 |
| 123 | 120 | 120 | 120 | 0 (+227 not run) | 120/120 (960/960 samples) | 120/120 | 120/120 |
| 456 | 120 | 120 | 120 | 0 (+227 not run) | 120/120 (960/960 samples) | 120/120 | 120/120 |

Reproduction by suite (programs with all 8 stored sample ICs identical / complete programs):

- seed 42: npb-v0 120/120, mibench-v1 0/0, blas-v0 0/0, chstone-v0 0/0, csmith-v0 0/0, poj104-v1 0/0
- seed 123: npb-v0 120/120, mibench-v1 0/0, blas-v0 0/0, chstone-v0 0/0, csmith-v0 0/0, poj104-v1 0/0
- seed 456: npb-v0 120/120, mibench-v1 0/0, blas-v0 0/0, chstone-v0 0/0, csmith-v0 0/0, poj104-v1 0/0

Are the executed sequences' ICs attribute-sensitive? Programs where the 8 GNN sample ICs are identical in both conditions (the GNN re-samples actions from the new state, so identity is not guaranteed) and where the 8 random-sequence ICs are identical:

- seed 42: GNN sample ICs identical on 118/120, identical action sequences on 118/120; random ICs identical on 117/120
- seed 123: GNN sample ICs identical on 116/120, identical action sequences on 116/120; random ICs identical on 117/120
- seed 456: GNN sample ICs identical on 116/120, identical action sequences on 116/120; random ICs identical on 117/120

## Baseline change alone: service -Oz with attributes vs plain (all programs with a complete null record)

| suite | n | Oz IC plain | Oz IC attr | change | Oz code plain | Oz code attr | change | Oz Berkeley plain | Oz Berkeley attr | change |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| npb-v0 | 120 | 53,085 | 40,446 | -23.8% | 291,616 | 214,296 | -26.5% | 348,878 | 267,814 | -23.2% |
| mibench-v1 | 40 | 4,841 | 4,714 | -2.6% | 27,791 | 25,629 | -7.8% | 40,942 | 38,796 | -5.2% |
| blas-v0 | 50 | 37,838 | 37,838 | +0.0% | 180,277 | 173,661 | -3.7% | 184,299 | 188,019 | +2.0% |
| chstone-v0 | 12 | 9,834 | 9,137 | -7.1% | 38,315 | 32,410 | -15.4% | 120,467 | 114,722 | -4.8% |
| csmith-v0 | 28 | 20,226 | 15,617 | -22.8% | 141,400 | 92,686 | -34.5% | 209,817 | 165,164 | -21.3% |
| poj104-v1 | 97 | 8,334 | 7,541 | -9.5% | 39,058 | 29,635 | -24.1% | 51,865 | 44,394 | -14.4% |
| ALL | 347 | 134,158 | 115,293 | -14.1% | 718,457 | 568,317 | -20.9% | 956,268 | 818,909 | -14.4% |

## IC: GNN best-of-8 (selected by final IC) vs paired random best-of-8 (selected by final IC), per suite, seed and condition

| suite | seed | n | cond. | Oz | GNN | random | GNN gain vs Oz | random gain vs Oz | GNN - random | adv% of Oz | W/T/L (GNN vs random) | argmax |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| npb-v0 | 42 | 120 | plain | 53,085 | 39,909 | 41,220 | +24.82% | +22.35% | -1,311 | -2.47% | 46/62/12 | 79,240 |
| npb-v0 | 42 | 120 | attr | 40,446 | 39,898 | 41,204 | +1.35% | -1.87% | -1,306 | -3.23% | 46/62/12 | 79,240 |
| npb-v0 | 123 | 120 | plain | 53,085 | 39,457 | 41,220 | +25.67% | +22.35% | -1,763 | -3.32% | 44/66/10 | 79,943 |
| npb-v0 | 123 | 120 | attr | 40,446 | 39,445 | 41,204 | +2.47% | -1.87% | -1,759 | -4.35% | 44/66/10 | 79,943 |
| npb-v0 | 456 | 120 | plain | 53,085 | 40,264 | 41,220 | +24.15% | +22.35% | -956 | -1.80% | 44/62/14 | 79,686 |
| npb-v0 | 456 | 120 | attr | 40,446 | 40,246 | 41,204 | +0.49% | -1.87% | -958 | -2.37% | 44/62/14 | 79,686 |
| ALL | 42 | 120 | plain | 53,085 | 39,909 | 41,220 | +24.82% | +22.35% | -1,311 | -2.47% | 46/62/12 | 79,240 |
| ALL | 42 | 120 | attr | 40,446 | 39,898 | 41,204 | +1.35% | -1.87% | -1,306 | -3.23% | 46/62/12 | 79,240 |
| ALL | 123 | 120 | plain | 53,085 | 39,457 | 41,220 | +25.67% | +22.35% | -1,763 | -3.32% | 44/66/10 | 79,943 |
| ALL | 123 | 120 | attr | 40,446 | 39,445 | 41,204 | +2.47% | -1.87% | -1,759 | -4.35% | 44/66/10 | 79,943 |
| ALL | 456 | 120 | plain | 53,085 | 40,264 | 41,220 | +24.15% | +22.35% | -956 | -1.80% | 44/62/14 | 79,686 |
| ALL | 456 | 120 | attr | 40,446 | 40,246 | 41,204 | +0.49% | -1.87% | -958 | -2.37% | 44/62/14 | 79,686 |

## code section bytes: GNN best-of-8 (selected by final IC) vs paired random best-of-8 (selected by final IC), per suite, seed and condition

| suite | seed | n | cond. | Oz | GNN | random | GNN gain vs Oz | random gain vs Oz | GNN - random | adv% of Oz | W/T/L (GNN vs random) | argmax |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| npb-v0 | 42 | 120 | plain | 291,616 | 220,643 | 220,090 | +24.34% | +24.53% | +553 | +0.19% | 33/50/37 | 248,462 |
| npb-v0 | 42 | 120 | attr | 214,296 | 200,220 | 200,450 | +6.57% | +6.46% | -230 | -0.11% | 37/50/33 | 226,835 |
| npb-v0 | 123 | 120 | plain | 291,616 | 217,725 | 220,090 | +25.34% | +24.53% | -2,365 | -0.81% | 30/60/30 | 251,711 |
| npb-v0 | 123 | 120 | attr | 214,296 | 197,773 | 200,450 | +7.71% | +6.46% | -2,677 | -1.25% | 35/57/28 | 230,109 |
| npb-v0 | 456 | 120 | plain | 291,616 | 221,294 | 220,090 | +24.11% | +24.53% | +1,204 | +0.41% | 36/53/31 | 251,655 |
| npb-v0 | 456 | 120 | attr | 214,296 | 201,181 | 200,450 | +6.12% | +6.46% | +731 | +0.34% | 39/55/26 | 230,227 |
| ALL | 42 | 120 | plain | 291,616 | 220,643 | 220,090 | +24.34% | +24.53% | +553 | +0.19% | 33/50/37 | 248,462 |
| ALL | 42 | 120 | attr | 214,296 | 200,220 | 200,450 | +6.57% | +6.46% | -230 | -0.11% | 37/50/33 | 226,835 |
| ALL | 123 | 120 | plain | 291,616 | 217,725 | 220,090 | +25.34% | +24.53% | -2,365 | -0.81% | 30/60/30 | 251,711 |
| ALL | 123 | 120 | attr | 214,296 | 197,773 | 200,450 | +7.71% | +6.46% | -2,677 | -1.25% | 35/57/28 | 230,109 |
| ALL | 456 | 120 | plain | 291,616 | 221,294 | 220,090 | +24.11% | +24.53% | +1,204 | +0.41% | 36/53/31 | 251,655 |
| ALL | 456 | 120 | attr | 214,296 | 201,181 | 200,450 | +6.12% | +6.46% | +731 | +0.34% | 39/55/26 | 230,227 |

## Berkeley text bytes: GNN best-of-8 (selected by final IC) vs paired random best-of-8 (selected by final IC), per suite, seed and condition

| suite | seed | n | cond. | Oz | GNN | random | GNN gain vs Oz | random gain vs Oz | GNN - random | adv% of Oz | W/T/L (GNN vs random) | argmax |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| npb-v0 | 42 | 120 | plain | 348,878 | 284,856 | 284,463 | +18.35% | +18.46% | +393 | +0.11% | 42/43/35 | 302,466 |
| npb-v0 | 42 | 120 | attr | 267,814 | 262,201 | 262,591 | +2.10% | +1.95% | -390 | -0.15% | 44/43/33 | 280,063 |
| npb-v0 | 123 | 120 | plain | 348,878 | 282,328 | 284,463 | +19.08% | +18.46% | -2,135 | -0.61% | 38/49/33 | 305,715 |
| npb-v0 | 123 | 120 | attr | 267,814 | 260,136 | 262,591 | +2.87% | +1.95% | -2,455 | -0.92% | 42/46/32 | 283,337 |
| npb-v0 | 456 | 120 | plain | 348,878 | 285,023 | 284,463 | +18.30% | +18.46% | +560 | +0.16% | 40/45/35 | 305,675 |
| npb-v0 | 456 | 120 | attr | 267,814 | 262,670 | 262,591 | +1.92% | +1.95% | +79 | +0.03% | 43/45/32 | 283,471 |
| ALL | 42 | 120 | plain | 348,878 | 284,856 | 284,463 | +18.35% | +18.46% | +393 | +0.11% | 42/43/35 | 302,466 |
| ALL | 42 | 120 | attr | 267,814 | 262,201 | 262,591 | +2.10% | +1.95% | -390 | -0.15% | 44/43/33 | 280,063 |
| ALL | 123 | 120 | plain | 348,878 | 282,328 | 284,463 | +19.08% | +18.46% | -2,135 | -0.61% | 38/49/33 | 305,715 |
| ALL | 123 | 120 | attr | 267,814 | 260,136 | 262,591 | +2.87% | +1.95% | -2,455 | -0.92% | 42/46/32 | 283,337 |
| ALL | 456 | 120 | plain | 348,878 | 285,023 | 284,463 | +18.30% | +18.46% | +560 | +0.16% | 40/45/35 | 305,675 |
| ALL | 456 | 120 | attr | 267,814 | 262,670 | 262,591 | +1.92% | +1.95% | +79 | +0.03% | 43/45/32 | 283,471 |

Notes. Sums are over the paired common set of each seed; percentages are ratios of sums, not means of per-program ratios. The random null is one fresh draw of 8 sequences per program (seed 42 + per-URI hash; the same draw as results/baseline_audit/llvm10_canonical on its 210 programs), used unchanged for all three GNN seeds, so the three seed rows share the null and are not independent replicates of the null. Programs within a suite are related modules, not independent applications. No p-values are reported here.

The attribute condition adds `minsize optsize` to function definitions of the service module on both sides; it is not a source-level `clang -Oz` build.

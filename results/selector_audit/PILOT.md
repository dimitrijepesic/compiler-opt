# Selector audit pilot (12 programs)

Run 2026-09-16 23:30 CEST in an amd64 CompilerGym 0.2.5 container under
Rosetta (image `cgym:0.2.5`, 4 workers, sequential `env.step` replay).
Records: `pilot/*.json`, run manifest `pilot/run_manifest.json`
(fingerprint of manifest `54393ce307c20db7…` + `replay=step|pilot=1`).

Programs (smallest and largest O0 IC per suite, URI tie-break):
blas-v0/288 (7), blas-v0/25 (3,219), chstone-v0/mips (636), chstone-v0/aes
(4,048), csmith-v0/21 (187), csmith-v0/40 (5,697), mibench-v1/qsort1 (114),
mibench-v1/susan-e-2 (1,629), npb-v0/16 (6), npb-v0/119 (5,705),
poj104-v1/54/59 (85), poj104-v1/102/1409 (730).

## Checks (all 12 programs)

| Check | Result |
|---|---|
| O0 and Oz observations equal the battery values | 12/12 |
| Attributed input: `input_sha256` and `ir_sha256` equal the stored GNN and null records; IR unchanged after `file://` load; every definition annotated; attribute counts equal stored; O0 unchanged; `IrInstructionCountOz` equal stored; target triple and datalayout identical before/after attributes | 12/12 |
| Service `-Oz`: IC equals observation and stored; Berkeley text, code section, bitcode and object SHA-256 equal the stored `attr.oz` | 12/12 |
| GNN traces: 3 seeds x 8 candidates replayed, no failed step, no done flag, replayed IC equals stored IC (tool and environment) | 288/288 |
| Stored IC-winner of each seed: replayed Berkeley text, code section, bitcode and object hashes equal the stored values | 36/36 |
| Random replicate 42: all 8 stored candidates re-replayed; IC, text, code section, bitcode and object hashes equal | 96/96 |
| Random replicates 43-46: 8 candidates each replayed and measured, no failure | 384/384 |
| `multistep` vs sequential `step`: identical bitcode and object hashes on one GNN trace and one new random sequence per program | 24/24 |

`--prepare` also verified, for all 347 programs, that every stored GNN trace
has 45 successful non-terminating steps (8,328 traces), that the input
identity of the three GNN records and the null record agree, and that
replicate 42 regenerates the stored random actions exactly (0 problems).

## Timing (per program, one worker, emulated)

Total 23 to 47 s. Replay of 64 sequences (2,880 service steps): 1 to 5 s,
i.e. 0.2 to 1.7 ms per step; export: about 0.1 s; measurement (llc,
llvm-size twice, ic, two SHA-256) 18 to 35 s for 64 candidates plus
baseline, about 0.4 s per candidate. Measurement, not replay, dominates.
None of this is GNN inference time.

## Decision

All checks passed. The campaign runs on all 347 programs with `multistep`
replay (validated above), 6 workers, into `records/`; replicate 42 is reused
from the stored candidates (validated here), replicates 43-46 are replayed.

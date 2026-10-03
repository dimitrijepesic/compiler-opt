# Budgeted baseline-safe selector

Retrospective recomputation from the frozen 347-program selector records; no compiler executions.
The selector first retains the k candidates with minimum IC, then chooses the minimum code-section bytes.
The attributed service `-Oz` object is optionally included as a fallback.

## Code-section savings with baseline fallback

| generator | k/8 measured | all 347 | without NPB | baseline returned (all) |
|---|---:|---:|---:|---:|
| gnn42 | 2/8 | 3.71% | 1.48% | 176 |
| gnn42 | 4/8 | 3.94% | 1.64% | 161 |
| gnn123 | 2/8 | 4.29% | 1.59% | 174 |
| gnn123 | 4/8 | 4.45% | 1.71% | 161 |
| gnn456 | 2/8 | 3.60% | 1.52% | 170 |
| gnn456 | 4/8 | 3.77% | 1.63% | 157 |
| random42 | 2/8 | 3.88% | 1.60% | 177 |
| random42 | 4/8 | 4.21% | 1.75% | 160 |
| random43 | 2/8 | 3.46% | 1.34% | 184 |
| random43 | 4/8 | 3.78% | 1.51% | 167 |
| random44 | 2/8 | 4.28% | 1.37% | 183 |
| random44 | 4/8 | 4.57% | 1.58% | 168 |
| random45 | 2/8 | 4.33% | 1.50% | 179 |
| random45 | 4/8 | 4.60% | 1.72% | 158 |
| random46 | 2/8 | 3.99% | 1.39% | 181 |
| random46 | 4/8 | 4.24% | 1.67% | 167 |

The 2/8 and 4/8 rows are the proposed budgeted selector; k=8 is the full byte-first selector.
The fallback guarantees no selected code-section regression relative to the attributed service baseline.

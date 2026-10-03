# Baseline audit: is the paper's `-Oz` reference a real size build?

Started 2026-09-16. Question: the paper compares every method against an
`-Oz` reference computed by applying the `-Oz` pipeline to CompilerGym's
benchmark bitcode (`IrInstructionCountOz` in the environment; `opt -Oz` in
`scripts/measure_binary_metrics.py` and `scripts/llvm18_transfer.py`).
That bitcode is built by CompilerGym with `-O1 -Xclang -disable-llvm-passes
-Xclang -disable-llvm-optzns` (`ClangInvocation` in
`compiler_gym/envs/llvm/llvm_benchmark.py`), so its functions carry no
`minsize`/`optsize` attributes. A real `clang -Oz` build sets both. Without
them the loop unroller stays active inside the `-Oz` pipeline and code
generation is not size-tuned, so the reference is larger than a real size
build on loop-heavy code, while the 45-pass sequences (no unrolling pass in
the curated space) are unaffected. This directory holds the measurements.

## Status and relation to the canonical audit (read first)

The two matrices in `llvm18/` and `llvm10/` are **command-line diagnostics
on the raw archive bitcode**: the `.bc` files from CompilerGym's dataset
tarballs, optimized with `opt`, not the modules the environment actually
operates on. The environment canonicalizes every benchmark on load (debug
information and named metadata are stripped, see `Benchmark.cc` in
CompilerGym 0.2.5), so the raw archive module and the service module
differ: on npb-v0/116 the raw O0 IC is 5,191 and the service O0 IC is
5,075, and the raw-vs-service O0 IC differs on 113 of the 120 NPB modules.
The service's own `-Oz` is also a PassManagerBuilder pipeline inside the
service, not the `opt -Oz` command (npb-v0/116: raw archive `opt -Oz`
6,061 IC; canonical export `opt -Oz` 4,762; service 4,316; all three drop
to 1,911 or 2,461 once the attributes are present). The numbers of the
two protocols must not be pooled.

The scientifically primary measurement of the attribute effect is the
**service-path audit in `llvm10_canonical/`** (paired, 210 programs,
original URIs, service `-Oz`, exact reproduction of the stored O0/Oz and
portfolio ICs). The CLI matrices below are retained because they were the
first evidence, cover a second LLVM version and 300 BLAS modules, and
include a `-disable-loop-unrolling` ablation that the service path does
not have; they agree with the canonical audit in direction and rough size
(NPB portfolio-8 IC margin +25.6% -> +2.2% here vs +23.84% -> +0.08% there;
code section +22.8% -> +6.3% vs +23.71% -> +5.76%).

The mechanism statement ("loop unrolling explains most of the IC
inflation") rests on the CLI ablation (`opt -Oz -disable-loop-unrolling`
on raw bitcode) and on the CompilerGym confirmation below (npb-v0/116:
the environment's `IrInstructionCountOz` 4,316 -> 1,911 with attributes,
and bundled `opt -Oz -disable-loop-unrolling` 1,911); a service-side
ablation of unrolling alone has not been run.

## Files

| File | Toolchain | What |
|---|---|---|
| `llvm18/npb-v0.json`, `llvm18/mibench-v1.json`, `llvm18/blas-v0.json` | Homebrew LLVM 18.1.8, native macOS arm64, new pass manager | `scripts/baseline_audit.py`: per module and per IR variant (`plain`, `attr`, `attr_fp`), `-Oz`, `-Oz -disable-loop-unrolling`, the first 8 portfolio sequences and 8 seeded random sequences; IC (exact, `scripts/baseline_audit/ic.cpp`), Berkeley `text`, summed code sections |
| `llvm10/npb-v0.json`, `llvm10/mibench-v1.json`, `llvm10/blas-v0.json` | CompilerGym 0.2.5 bundled LLVM 10, legacy pass manager, amd64 container | same script with `--pm legacy` on the raw archive bitcode in CompilerGym's download cache (not the canonicalized service module; see the status section) |
| `llvm10/cgym_confirmation.json` | CompilerGym 0.2.5 | `scripts/baseline_audit_cgym.py`: the environment's own `IrInstructionCountOz` on the shipped module and on the same module with attributes added, loaded through `file://` |
| `llvm10/chstone_clang_oz.json` | CompilerGym 0.2.5 bundled clang/LLVM 10 | `scripts/baseline_audit_clang.py`: a real `clang -Oz -c` build of the 12 CHStone sources vs `opt -Oz` on (a) IR with clang's own `-Oz` attributes, (b) the environment's module (paper protocol), (c) the module with textual attributes |

Input identity: every record stores the SHA-256 of its input bitcode. The
native runs used CompilerGym's dataset tarballs from
`dl.fbaipublicfiles.com/compiler_gym/llvm_bitcodes-10.0.0-<suite>.tar.bz2`
(npb-v0 793ac2e7…bb1f2, mibench-v1 795b80d3…2bb5, blas-v0 e724a811…096d).
MiBench bitcode targets `x86_64-apple-macosx10.15.0` (Mach-O, code section
`__text`); NPB and BLAS target `x86_64-pc-linux-gnu`. Objects are generated
for the module's own triple, as in the paper.

IR variants. `attr`: `llvm-dis`, add `minsize optsize` to every
`attributes #N = {` group, `llvm-as`. `attr_fp`: also `"frame-pointer"="all"`
to `"none"` (NPB/BLAS/MiBench tarball bitcode has `all`; modules built by
`ClangInvocation`, e.g. CHStone, already have `none`). On CHStone the textual
insertion gives byte-identical results to IR that clang itself emits with
`-Oz -Xclang -disable-llvm-passes -Xclang -disable-llvm-optzns`.

Selection convention. The best-of-8 sequence is chosen by IC (the paper's
protocol) and its bytes are those of that same sequence (`*_by_ic`);
selection by bytes is stored separately (`*_by_text`). Failed sequence runs
and failed modules are kept; totals are over the common set of modules on
which every variant succeeded, and the counts are stored in `summary`.

## Results of the CLI diagnostics (raw archive bitcode; totals; W/T/L = per-module wins/ties/losses vs `-Oz`)

"Berkeley text" is the first column of `llvm-size` (code plus read-only
data); "code section" is the sum of `.text*` (ELF) or `__text` (Mach-O)
sections. The two can move differently (NPB attr: +1.4% vs +6.4%).

LLVM 18, portfolio-8 selected by IC, margin over `-Oz`:

| Suite (n) | IR | IC | Berkeley text | code section |
|---|---|---:|---:|---:|
| NPB (120) | plain (paper) | +25.5% (72/26/22) | +15.5% (64/14/42) | +21.5% (78/14/28) |
| NPB (120) | attr | +2.2% (55/26/39) | +1.4% (53/13/54) | +6.4% (69/13/38) |
| NPB (120) | attr_fp | +2.2% | +1.4% | +6.7% (72/13/35) |
| MiBench (40) | plain (paper) | +10.2% (25/12/3) | +2.3% (12/19/9) | +3.8% (12/19/9) |
| MiBench (40) | attr | +0.2% (17/14/9) | +1.0% (16/11/13) | +1.9% (16/11/13) |
| MiBench (40) | attr_fp | +0.2% | -0.3% (16/11/13) | -0.0% (17/11/12) |
| BLAS (299) | plain (paper) | +1.5% (160/54/85) | +1.1% (165/41/93) | +1.1% |
| BLAS (299) | attr | +1.5% | +1.1% (175/26/98) | +1.1% |

Random-8 selected by IC behaves like the portfolio in every cell (NPB attr:
IC +1.4%, code section +4.2%; MiBench attr: IC -1.2%, code section +3.2%).

Mechanism (LLVM 18, NPB, plain IR): `-Oz` IC 69,192; `-Oz
-disable-loop-unrolling` 53,174 (-23.2%); `-Oz` with attributes 52,672
(-23.9%). Berkeley text 393,560 / 339,766 / 310,514: unrolling explains the
IC inflation almost entirely and about two thirds of the byte inflation;
the rest is size-tuned code generation. On NPB, 53 of 120 modules have a
paper-protocol `-Oz` Berkeley text larger than the `-O0` Berkeley text; with attributes, 26.

Cross-check: the paper-protocol portfolio result on NPB (Berkeley text
332,421) is 7.1% *larger* than the attribute-correct `-Oz` alone (310,514;
30/1/89 per module).

LLVM 10 (CompilerGym's bundled toolchain, legacy pass manager, the bitcode
the environment downloads; no sequence failures, every module in the
common set), portfolio-8 selected by IC, margin over `-Oz`:

| Suite (n) | IR | IC | Berkeley text | code section |
|---|---|---:|---:|---:|
| NPB (122) | plain (paper) | +25.6% (66/29/27) | +16.2% (65/13/44) | +22.8% (80/13/29) |
| NPB (122) | attr | +2.2% (46/31/45) | +0.7% (52/13/57) | +6.3% (82/13/27) |
| NPB (122) | attr_fp | +2.2% | +0.8% (51/13/58) | +6.3% (81/13/28) |
| MiBench (40) | plain (paper) | +3.2% (16/19/5) | +3.1% (12/20/8) | +4.7% (11/20/9) |
| MiBench (40) | attr | -1.4% (10/21/9) | +1.0% (9/14/17) | +1.6% (9/14/17) |
| MiBench (40) | attr_fp | -1.4% | +0.8% (9/14/17) | +1.4% (10/14/16) |
| BLAS (300) | plain (paper) | +3.6% (224/62/14) | +2.1% (177/46/77) | +2.2% |
| BLAS (300) | attr | +3.6% | +2.1% (178/45/77) | +2.2% |

Random-8 selected by IC again tracks the portfolio (NPB attr: IC +2.0%,
code section +6.1%; MiBench attr: IC -2.1%, code section +1.2%; BLAS
+2.6% / +1.8%). Mechanism under LLVM 10 (NPB, plain IR): `-Oz` IC 72,517;
`-disable-loop-unrolling` 55,361 (-23.7%); with attributes 55,150 (-23.9%);
Berkeley text 383,177 / 322,891 / 296,957. Paper-protocol `-Oz` text
exceeds `-O0` text on 54 of 122 NPB modules (34 with attributes). The
paper-protocol portfolio result on NPB (321,076) is 8.1% larger than the
attribute-correct `-Oz` alone (296,957; 31/1/90 per module). On BLAS the
attributes change nothing and the sequences keep a small, real margin.

LLVM 10 inside CompilerGym (`cgym_confirmation.json`), the environment's
own `IrInstructionCountOz`, plain -> attributes: npb-v0/116 4,316 -> 1,911
(`-disable-loop-unrolling`: 1,911); 94 2,234 -> 1,284; 96 2,316 -> 1,308;
39 2,072 -> 1,269; 12 2,269 -> 1,242; cBench qsort 315 -> 274; unchanged on
npb 61/115/117, mibench bitcount-1, blas 101, cBench crc32/adpcm.

Real build check (CHStone, 12 programs, LLVM 10 clang, summed code
section): `clang -Oz -c` 32,123 bytes; `opt -Oz` on attribute-corrected IR
32,468 (+1.1%); paper protocol 39,745 (+23.7%). IC: 9,062 / 9,216 / 10,304.

## Reproduce

Native (macOS, Homebrew `llvm@18`):

```
clang++ -std=c++17 scripts/baseline_audit/ic.cpp -o scripts/baseline_audit/ic \
    $(llvm-config --cxxflags --ldflags) $(llvm-config --libs core irreader bitreader support) $(llvm-config --system-libs)
python3 scripts/baseline_audit.py --bitcode-dir <dir with the suite's .bc files> --suite npb-v0 \
    --llvm-bin /opt/homebrew/opt/llvm@18/bin --out results/baseline_audit/llvm18/npb-v0.json
python3 scripts/baseline_audit.py --summarize results/baseline_audit/llvm18/npb-v0.json
```

CompilerGym (amd64 container; on Apple silicon via Colima with Rosetta:
`colima start --vm-type vz --vz-rosetta`):

```
docker build --platform linux/amd64 -t cgym:0.2.5 -f scripts/baseline_audit/Dockerfile .
docker run --rm --platform linux/amd64 -v cgym-share:/root/.local/share/compiler_gym \
    -v cgym-cache:/root/.cache/compiler_gym -v "$PWD":/work -w /work cgym:0.2.5 \
    python scripts/baseline_audit_cgym.py benchmark://npb-v0/116 --out results/baseline_audit/llvm10/cgym_confirmation.json
# full matrix on a downloaded suite, legacy pass manager:
docker run ... cgym:0.2.5 python scripts/baseline_audit.py --pm legacy \
    --llvm-bin /root/.local/share/compiler_gym/llvm-v0/bin --ic-tool /usr/local/bin/ic \
    --bitcode-dir /root/.local/share/compiler_gym/llvm-v0/benchmark/npb-v0/contents/npb-v0 --suite npb-v0 \
    --out results/baseline_audit/llvm10/npb-v0.json
docker run ... cgym:0.2.5 python scripts/baseline_audit_clang.py --out results/baseline_audit/llvm10/chstone_clang_oz.json
```

## Scope of the claim

The attributes are the mechanism, the effect size depends on the program
(loop-heavy code), the LLVM version and the exact protocol. The safe
statement is that this protocol (and any evaluation that reads
`IrInstructionCountOz` or applies `opt -Oz` to CompilerGym's bitcode) can
produce a weaker size reference than a size build of the same source,
and that on NPB and CHStone the gap is large enough to reverse the sign of
the paper's headline comparisons. The 36-pass action space is held fixed
throughout; it was profiled on attribute-less IR, and several of its passes
read `optsize`, which is why the sequences are re-measured under every
variant rather than only the reference.

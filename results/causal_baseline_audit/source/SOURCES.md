# Upstream sources read for the causal baseline audit

Fetched 2026-09-19 into `upstream/`. File name = repository path with `/`
replaced by `_`.

| Saved file | Origin |
|---|---|
| `compiler_gym_envs_llvm_service_Cost.cc`, `Cost.h`, `Benchmark.cc`, `LlvmSession.cc`, `LlvmSession.h`, `RunService.cc`, `BUILD` | <https://github.com/facebookresearch/CompilerGym/tree/v0.2.5/compiler_gym/envs/llvm/service> |
| `compiler_gym_service_runtime_Runtime.h`, `CreateAndRunCompilerGymServiceImpl.h` | <https://github.com/facebookresearch/CompilerGym/tree/v0.2.5/compiler_gym/service/runtime> |
| `compiler_gym_third_party_llvm___init__.py`, `WORKSPACE` | <https://github.com/facebookresearch/CompilerGym/tree/v0.2.5> |
| `bazel_llvm_tools_bzl_deps.bzl` | <https://github.com/ChrisCummins/bazel_llvm/blob/9481d3c85247bbc284d8283aa5b6b8b517301262/tools/bzl/deps.bzl> |
| `llvm10_PassManagerBuilder.cpp`, `llvm10_PassManagerBuilder.h` | <https://github.com/llvm/llvm-project/tree/llvmorg-10.0.0/llvm> (`lib/Transforms/IPO/`, `include/llvm/Transforms/IPO/`) |
| `llvm10_LoopUnrollPass.cpp` | `llvm/lib/Transforms/Scalar/LoopUnrollPass.cpp` at `llvmorg-10.0.0` |
| `llvm10_opt.cpp` | `llvm/tools/opt/opt.cpp` at `llvmorg-10.0.0` |

## Lines that matter

- `Cost.cc` L264-287 `applyBaselineOptimizationsToModule`: legacy
  `PassManagerBuilder`, `OptLevel`/`SizeLevel` and an inliner, nothing else;
  module pass manager first, then the function pass manager. L322-332: `-Oz`
  = `(2, 2)` on a clone of the unoptimized module.
- `LlvmSession.cc` L198-204: session parameter
  `llvm.apply_baseline_optimizations=-Oz` applies the same function to the
  session module. L162-210 is the complete list of session parameters; none
  controls unrolling.
- `Benchmark.cc` L124-137: module id and source file name set to `-`,
  `StripDebugInfo`, all named metadata erased. Instruction-level metadata
  such as `!llvm.loop` is kept, which is what makes the input-level
  intervention possible.
- `RunService.cc` L18-54 `initLlvm`; the service parses gflags only
  (`-port`, `-working_dir`, logging), never LLVM `cl::opt`s.
- `PassManagerBuilder.cpp` L160-163 builder defaults
  (`DisableUnrollLoops = false`, `LoopVectorize = EnableLoopVectorization`);
  L400 and L714 `createLoopRotatePass(SizeLevel == 2 ? 0 : -1)`; L422
  `createSimpleLoopUnrollPass(OptLevel, DisableUnrollLoops, ...)`; L775
  `createLoopUnrollPass(...)`; L778-786 InstCombine + LICM only
  `if (!DisableUnrollLoops)`.
- `LoopUnrollPass.cpp` L190-192 `OptSizeThreshold = 0`; L215-220 functions
  with `optsize` use it; L1028 `llvm.loop.unroll.disable` returns before
  anything else; L1038 `OnlyWhenForced`; L1053-1055 early exit for threshold 0
  without `optsize`.
- `opt.cpp` L389-402: `opt` sets `DisableUnrollLoops`, `LoopVectorize =
  OptLevel > 1 && SizeLevel < 2`, `SLPVectorize`, and adds TLI/TTI; the
  service does none of that, so `opt -Oz` is a different pipeline.
- Service binary: PyPI wheel `compiler_gym==0.2.5`, sha256
  `60178fbf497cb79f01aa567dc16765d04579dd88b3137e47769b5757067d37ee`, equal to
  the wheel's `RECORD` entry (`YBePv0l8t58BqlZ9wWdl0EV53YizE35HdptXVwZ9N-4`).

// Replica of the CompilerGym v0.2.5 service baseline pipeline, with switches.
//
// This is NOT the original service. It is a helper program that links the
// same LLVM 10.0.0 release libraries the service links
// (clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04, bazel_llvm deps.bzl,
// sha256 b25f592a...) and copies the service code verbatim:
//   - initLlvm()                          compiler_gym/envs/llvm/service/RunService.cc L18-54
//   - makeModule() canonicalization       compiler_gym/envs/llvm/service/Benchmark.cc  L124-137
//   - applyBaselineOptimizationsToModule  compiler_gym/envs/llvm/service/Cost.cc       L264-287
// (all at tag v0.2.5). Mode "service" adds nothing to that code path. Its
// output must reproduce the service before any other mode is interpreted.
//
// Modes:
//   --mode=service             verbatim pipeline (fidelity check against the service)
//   --mode=disable-unroll      builder.DisableUnrollLoops = true. In LLVM 10 this makes
//                              both unroll passes (createSimpleLoopUnrollPass in the
//                              function simplification pipeline, createLoopUnrollPass
//                              late) run with OnlyWhenForced=true, i.e. only loops with
//                              explicit llvm.loop.unroll.enable/count metadata are
//                              unrolled, and it removes the InstCombine+LICM cleanup
//                              that follows the late unroll pass
//                              (PassManagerBuilder.cpp L422, L775-786). Same builder
//                              field that `opt -disable-loop-unrolling` sets.
//   --mode=unroll-threshold-0  keeps the pipeline unchanged and sets the cl::opt
//                              -unroll-threshold=0, so the unroll passes still run with
//                              their cleanup but exit early on functions without
//                              optsize (LoopUnrollPass.cpp L225-226, L1051-1055).
//                              Functions with optsize are unaffected (L1072-1073).
//   --mark-unroll-disable      no pipeline: add llvm.loop.unroll.disable to the loop id
//                              of every natural loop of the input (existing loop
//                              properties are kept) and write it out (input-level
//                              intervention that can then be executed by the
//                              ORIGINAL service).
// Options:
//   --remarks        print loop-unroll optimization remarks to stderr
//   --debug-pass     print the legacy pass manager structure to stderr (-debug-pass=Structure)
//   --stats=FILE     write per-function instruction/block/loop counts before and after (JSON)
//
// Usage: replica_oz [options] <in.bc> <out.bc>

#include "llvm/ADT/StringRef.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Bitcode/BitcodeReader.h"
#include "llvm/Bitcode/BitcodeWriter.h"
#include "llvm/IR/DebugInfo.h"
#include "llvm/IR/DiagnosticInfo.h"
#include "llvm/IR/Dominators.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/MDBuilder.h"
#include "llvm/IR/Module.h"
#include "llvm/InitializePasses.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/IPO.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"

#include <cstdio>
#include <cstring>
#include <memory>
#include <string>
#include <vector>

namespace {

// ---- verbatim from compiler_gym/envs/llvm/service/RunService.cc (v0.2.5) ----
void initLlvm() {
  llvm::InitializeNativeTarget();

  // Initialize passes.
  llvm::PassRegistry& Registry = *llvm::PassRegistry::getPassRegistry();
  llvm::initializeCore(Registry);
  llvm::initializeCoroutines(Registry);
  llvm::initializeScalarOpts(Registry);
  llvm::initializeObjCARCOpts(Registry);
  llvm::initializeVectorization(Registry);
  llvm::initializeIPO(Registry);
  llvm::initializeAnalysis(Registry);
  llvm::initializeTransformUtils(Registry);
  llvm::initializeInstCombine(Registry);
  llvm::initializeAggressiveInstCombine(Registry);
  llvm::initializeInstrumentation(Registry);
  llvm::initializeTarget(Registry);
  llvm::initializeExpandMemCmpPassPass(Registry);
  llvm::initializeScalarizeMaskedMemIntrinPass(Registry);
  llvm::initializeCodeGenPreparePass(Registry);
  llvm::initializeAtomicExpandPass(Registry);
  llvm::initializeRewriteSymbolsLegacyPassPass(Registry);
  llvm::initializeWinEHPreparePass(Registry);
  llvm::initializeDwarfEHPreparePass(Registry);
  llvm::initializeSafeStackLegacyPassPass(Registry);
  llvm::initializeSjLjEHPreparePass(Registry);
  llvm::initializePreISelIntrinsicLoweringLegacyPassPass(Registry);
  llvm::initializeGlobalMergePass(Registry);
  llvm::initializeIndirectBrExpandPassPass(Registry);
  llvm::initializeInterleavedAccessPass(Registry);
  llvm::initializeEntryExitInstrumenterPass(Registry);
  llvm::initializePostInlineEntryExitInstrumenterPass(Registry);
  llvm::initializeUnreachableBlockElimLegacyPassPass(Registry);
  llvm::initializeExpandReductionsPass(Registry);
  llvm::initializeWasmEHPreparePass(Registry);
  llvm::initializeWriteBitcodePassPass(Registry);
}
// ---- end verbatim ----

// ---- from compiler_gym/envs/llvm/service/Benchmark.cc makeModule() (v0.2.5) ----
void canonicalize(llvm::Module& module) {
  // Strip the module identifiers and source file names from the module to
  // anonymize them. This is to deter learning algorithms from overfitting to
  // benchmarks by their name.
  module.setModuleIdentifier("-");
  module.setSourceFileName("-");

  // Strip module debug info.
  llvm::StripDebugInfo(module);

  // Erase module-level named metadata.
  while (!module.named_metadata_empty()) {
    llvm::NamedMDNode* nmd = &*module.named_metadata_begin();
    module.eraseNamedMetadata(nmd);
  }
}
// ---- end ----

// ---- verbatim from compiler_gym/envs/llvm/service/Cost.cc (v0.2.5), plus the
// single added line marked INTERVENTION ----
bool applyBaselineOptimizationsToModule(llvm::Module* module, unsigned optLevel,
                                        unsigned sizeLevel, bool disableUnrollLoops) {
  llvm::legacy::PassManager passManager;
  llvm::legacy::FunctionPassManager functionPassManager(module);

  llvm::PassManagerBuilder builder;
  builder.OptLevel = optLevel;
  builder.SizeLevel = sizeLevel;
  if (optLevel > 1) {
    builder.Inliner = llvm::createFunctionInliningPass(optLevel, sizeLevel, false);
  }
  if (disableUnrollLoops) {                    // INTERVENTION (not in the service)
    builder.DisableUnrollLoops = true;         // INTERVENTION (not in the service)
  }                                            // INTERVENTION (not in the service)

  builder.populateFunctionPassManager(functionPassManager);
  builder.populateModulePassManager(passManager);

  bool changed = passManager.run(*module);
  changed |= (functionPassManager.doInitialization() ? 1 : 0);
  for (auto& function : *module) {
    changed |= (functionPassManager.run(function) ? 1 : 0);
  }
  changed |= (functionPassManager.doFinalization() ? 1 : 0);

  return changed;
}
// ---- end verbatim ----

struct RemarkHandler : public llvm::DiagnosticHandler {
  bool handleDiagnostics(const llvm::DiagnosticInfo& DI) override {
    if (auto* R = llvm::dyn_cast<llvm::DiagnosticInfoOptimizationBase>(&DI)) {
      if (R->getPassName() != llvm::StringRef("loop-unroll")) return true;
      llvm::errs() << "remark\t" << R->getPassName() << "\t" << R->getRemarkName() << "\t"
                   << R->getFunction().getName() << "\t" << R->getMsg() << "\n";
      return true;
    }
    return false;
  }
  bool isAnalysisRemarkEnabled(llvm::StringRef) const override { return false; }
  bool isMissedOptRemarkEnabled(llvm::StringRef) const override { return false; }
  bool isPassedOptRemarkEnabled(llvm::StringRef PassName) const override {
    return PassName == "loop-unroll";
  }
  bool isAnyRemarkEnabled() const override { return true; }
};

void writeStats(llvm::raw_ostream& os, llvm::Module& M, const char* label) {
  os << "  \"" << label << "\": {\"ic\": " << M.getInstructionCount() << ", \"functions\": [";
  bool first = true;
  for (auto& F : M) {
    if (F.isDeclaration()) continue;
    llvm::DominatorTree DT(F);
    llvm::LoopInfo LI(DT);
    unsigned loops = 0, maxDepth = 0;
    for (llvm::Loop* L : LI.getLoopsInPreorder()) {
      ++loops;
      if (L->getLoopDepth() > maxDepth) maxDepth = L->getLoopDepth();
    }
    os << (first ? "\n" : ",\n") << "    {\"name\": \"" << F.getName() << "\", \"ic\": "
       << F.getInstructionCount() << ", \"blocks\": " << F.size() << ", \"loops\": " << loops
       << ", \"max_loop_depth\": " << maxDepth << ", \"optsize\": " << (F.hasOptSize() ? 1 : 0)
       << ", \"minsize\": " << (F.hasMinSize() ? 1 : 0) << "}";
    first = false;
  }
  os << "\n  ]}";
}

// Adds llvm.loop.unroll.disable to every natural loop. Properties that a loop
// id already carries (e.g. llvm.loop.isvectorized in the BLAS inputs) are
// kept: the new id is the old operand list plus the one new property.
unsigned markUnrollDisable(llvm::Module& M, unsigned& preexisting) {
  unsigned marked = 0;
  preexisting = 0;
  llvm::LLVMContext& C = M.getContext();
  for (auto& F : M) {
    if (F.isDeclaration()) continue;
    llvm::DominatorTree DT(F);
    llvm::LoopInfo LI(DT);
    for (llvm::Loop* L : LI.getLoopsInPreorder()) {
      llvm::MDNode* disable = llvm::MDNode::get(C, llvm::MDString::get(C, "llvm.loop.unroll.disable"));
      llvm::MDNode* old = L->getLoopID();
      if (old) ++preexisting;
      L->setLoopID(llvm::makePostTransformationMetadata(C, old, llvm::None, {disable}));
      ++marked;
    }
  }
  return marked;
}

}  // namespace

int main(int argc, char** argv) {
  std::string mode = "service", statsPath;
  bool remarks = false, debugPass = false, mark = false;
  std::vector<const char*> positional;
  for (int i = 1; i < argc; ++i) {
    if (!std::strncmp(argv[i], "--mode=", 7)) mode = argv[i] + 7;
    else if (!std::strncmp(argv[i], "--stats=", 8)) statsPath = argv[i] + 8;
    else if (!std::strcmp(argv[i], "--remarks")) remarks = true;
    else if (!std::strcmp(argv[i], "--debug-pass")) debugPass = true;
    else if (!std::strcmp(argv[i], "--mark-unroll-disable")) mark = true;
    else positional.push_back(argv[i]);
  }
  if (positional.size() != 2) {
    std::fprintf(stderr, "usage: replica_oz [--mode=service|disable-unroll|unroll-threshold-0] "
                         "[--remarks] [--debug-pass] [--stats=FILE] [--mark-unroll-disable] in.bc out.bc\n");
    return 2;
  }
  if (mode != "service" && mode != "disable-unroll" && mode != "unroll-threshold-0") {
    std::fprintf(stderr, "unknown mode %s\n", mode.c_str());
    return 2;
  }

  initLlvm();

  // Only the modes that need LLVM command-line options parse any. The
  // service parses none, so "service" mode parses none either.
  std::vector<const char*> clArgs{"replica_oz"};
  if (mode == "unroll-threshold-0") clArgs.push_back("-unroll-threshold=0");
  if (debugPass) clArgs.push_back("-debug-pass=Structure");
  if (clArgs.size() > 1) {
    if (!llvm::cl::ParseCommandLineOptions(static_cast<int>(clArgs.size()), clArgs.data(), "")) {
      return 2;
    }
  }

  llvm::LLVMContext ctx;
  if (remarks) ctx.setDiagnosticHandler(std::make_unique<RemarkHandler>(), /*RespectFilters=*/false);

  auto bufferOrErr = llvm::MemoryBuffer::getFile(positional[0]);
  if (!bufferOrErr) {
    std::fprintf(stderr, "cannot read %s\n", positional[0]);
    return 1;
  }
  auto moduleOrErr = llvm::parseBitcodeFile(bufferOrErr.get()->getMemBufferRef(), ctx);
  if (!moduleOrErr) {
    std::fprintf(stderr, "cannot parse bitcode %s\n", positional[0]);
    return 1;
  }
  std::unique_ptr<llvm::Module> module = std::move(moduleOrErr.get());
  canonicalize(*module);

  std::string statsBuf;
  llvm::raw_string_ostream stats(statsBuf);
  stats << "{\n";
  writeStats(stats, *module, "before");

  const uint64_t icBefore = module->getInstructionCount();
  bool changed = false;
  unsigned marked = 0, preexisting = 0;
  if (mark) {
    marked = markUnrollDisable(*module, preexisting);
  } else {
    changed = applyBaselineOptimizationsToModule(module.get(), /*optLevel=*/2, /*sizeLevel=*/2,
                                                 mode == "disable-unroll");
  }
  stats << ",\n";
  writeStats(stats, *module, "after");
  stats << ",\n  \"mode\": \"" << (mark ? "mark-unroll-disable" : mode) << "\", \"changed\": " << (changed ? 1 : 0)
        << ", \"marked_loops\": " << marked << ", \"preexisting_loop_ids\": " << preexisting
        << ", \"ic_before\": " << icBefore << ", \"ic_after\": "
        << module->getInstructionCount() << "\n}\n";
  stats.flush();

  std::error_code ec;
  llvm::raw_fd_ostream out(positional[1], ec, llvm::sys::fs::OF_None);
  if (ec) {
    std::fprintf(stderr, "cannot write %s\n", positional[1]);
    return 1;
  }
  llvm::WriteBitcodeToFile(*module, out);
  out.close();
  if (!statsPath.empty()) {
    llvm::raw_fd_ostream sf(statsPath, ec, llvm::sys::fs::OF_Text);
    if (ec) {
      std::fprintf(stderr, "cannot write %s\n", statsPath.c_str());
      return 1;
    }
    sf << statsBuf;
  }
  std::printf("%llu\n", static_cast<unsigned long long>(module->getInstructionCount()));
  return 0;
}

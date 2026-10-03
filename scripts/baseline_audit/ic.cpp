// Exact LLVM IR instruction count of a bitcode/IR file via the LLVM API.
// A line-based count of textual IR is wrong on multi-line instructions
// (switch cases, landingpad clauses); this is the reference counter used
// by scripts/baseline_audit.py.
//
// Build (any LLVM >= 10 with headers, e.g. Homebrew llvm@18):
//   clang++ -std=c++17 ic.cpp -o ic $(llvm-config --cxxflags --ldflags) \
//       $(llvm-config --libs core irreader bitreader support) \
//       $(llvm-config --system-libs)
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IRReader/IRReader.h"
#include "llvm/Support/SourceMgr.h"
#include <cstdio>

int main(int argc, char** argv) {
  if (argc < 2) {
    fprintf(stderr, "usage: ic <file.bc|file.ll>\n");
    return 2;
  }
  llvm::LLVMContext ctx;
  llvm::SMDiagnostic err;
  auto m = llvm::parseIRFile(argv[1], err, ctx);
  if (!m) {
    fprintf(stderr, "parse error: %s\n", err.getMessage().str().c_str());
    return 1;
  }
  unsigned long n = 0;
  for (auto& f : *m)
    for (auto& bb : f)
      n += bb.size();
  printf("%lu\n", n);
  return 0;
}

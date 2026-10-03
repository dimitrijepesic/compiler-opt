#!/bin/sh
# Download the checksum-pinned LLVM release, then build the audit toolchain.
set -eu
REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BUILD_DIR="$REPO_DIR/tmp/audit-image"
ARCHIVE=clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz
mkdir -p "$BUILD_DIR"
if [ ! -f "$BUILD_DIR/$ARCHIVE" ]; then
    curl --fail --location --retry 3 \
      "https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/$ARCHIVE" \
      --output "$BUILD_DIR/$ARCHIVE.part"
    mv "$BUILD_DIR/$ARCHIVE.part" "$BUILD_DIR/$ARCHIVE"
fi
python3 - "$BUILD_DIR/$ARCHIVE" <<'PY'
import hashlib, sys
from pathlib import Path
actual = hashlib.file_digest(Path(sys.argv[1]).open('rb'), 'sha256').hexdigest() if sys.version_info >= (3, 11) else hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()
assert actual == 'b25f592a0c00686f03e3b7db68ca6dc87418f681f4ead4df4745a01d9be63843', actual
PY
docker build --platform linux/amd64 -t cgym:0.2.5 \
  -f "$REPO_DIR/scripts/baseline_audit/Dockerfile" "$REPO_DIR"
sh "$REPO_DIR/scripts/causal_baseline_audit/build_image.sh" "$BUILD_DIR"

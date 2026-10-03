#!/bin/sh
# Build the separate image cgym-causal:0.2.5. Usage: build_image.sh <dir containing the LLVM archive>
set -eu
CTX="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
cp "$HERE/Dockerfile" "$HERE/replica_oz.cpp" "$CTX/"
docker build --platform linux/amd64 -t cgym-causal:0.2.5 -f "$CTX/Dockerfile" "$CTX"

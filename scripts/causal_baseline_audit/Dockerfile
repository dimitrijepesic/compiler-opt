# Separate image for the causal baseline audit. Extends the existing
# CompilerGym 0.2.5 image (scripts/baseline_audit/Dockerfile) with the exact
# LLVM 10.0.0 release archive that CompilerGym v0.2.5 links its service
# against (bazel_llvm tools/bzl/deps.bzl @ 9481d3c: clang+llvm-10.0.0-x86_64-
# linux-gnu-ubuntu-18.04, sha256 b25f592a...) and builds the replica tool.
# Build context must contain the archive next to this Dockerfile.
FROM cgym:0.2.5
COPY clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz /opt/llvm10.tar.xz
RUN echo "b25f592a0c00686f03e3b7db68ca6dc87418f681f4ead4df4745a01d9be63843  /opt/llvm10.tar.xz" | sha256sum -c - \
 && mkdir -p /opt/llvm10 && tar -xJf /opt/llvm10.tar.xz -C /opt/llvm10 --strip-components=1 \
 && rm /opt/llvm10.tar.xz && /opt/llvm10/bin/llvm-config --version
RUN apt-get update && apt-get install -y --no-install-recommends zlib1g-dev libtinfo-dev libxml2-dev \
 && rm -rf /var/lib/apt/lists/*
COPY replica_oz.cpp /opt/replica_oz.cpp
RUN clang++-14 -std=c++14 -O1 -fno-rtti -fno-exceptions -Wno-unused-command-line-argument \
      -I/opt/llvm10/include -D_GNU_SOURCE -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS \
      /opt/replica_oz.cpp -o /usr/local/bin/replica_oz \
      $(/opt/llvm10/bin/llvm-config --link-static --ldflags) \
      $(/opt/llvm10/bin/llvm-config --link-static --libs all) \
      $(/opt/llvm10/bin/llvm-config --link-static --system-libs) \
 && sha256sum /usr/local/bin/replica_oz

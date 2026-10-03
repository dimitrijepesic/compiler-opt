# CompilerGym 0.2.5 environment, mirrors colab/battery_colab.ipynb and scripts/setup_wsl_env.sh
FROM --platform=linux/amd64 ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.10 python3.10-venv python3-pip libtinfo5 build-essential git curl ca-certificates \
      clang-14 llvm-14 llvm-14-dev lld-14 \
    && rm -rf /var/lib/apt/lists/*
RUN python3.10 -m venv /opt/venv-cgym \
    && /opt/venv-cgym/bin/pip install -q "pip<24.1" setuptools==65.5.0 wheel==0.38.4 \
    && /opt/venv-cgym/bin/pip install -q gym==0.21.0 \
    && /opt/venv-cgym/bin/pip install -q compiler-gym==0.2.5 "numpy<2" pyyaml==6.0.3 tqdm==4.70.0 scipy==1.15.3 matplotlib==3.9.4 tabulate
COPY scripts/baseline_audit/ic.cpp /opt/ic.cpp
RUN clang++-14 -std=c++17 /opt/ic.cpp -o /usr/local/bin/ic $(llvm-config-14 --cxxflags --ldflags) $(llvm-config-14 --libs core irreader bitreader support) $(llvm-config-14 --system-libs)
ENV PATH=/opt/venv-cgym/bin:$PATH
WORKDIR /work
CMD ["bash"]

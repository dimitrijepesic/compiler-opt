import json, re, subprocess, sys, time, glob, os
BIN = "/root/memplan/idealloc/target/release/idealloc"
B = "/root/memplan/idealloc/benchmarks"
small = sorted(glob.glob(B + "/minimalloc/*.csv")) + [B + "/somas_tensors/resnet50.csv", B + "/iopddl/G_1.csv"]
big = [B + "/somas_tensors/pangu_2.6B.csv", B + "/iopddl/S_1.csv", B + "/iopddl/Y_1.csv"]
def run(path, lives, timeout):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([BIN, "--input", path, "ex-csv", "-l", str(lives)], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"timeout": True, "wall_s": time.perf_counter() - t0}
    out = p.stdout
    g = lambda pat: (re.search(pat, out) or [None, None])[1]
    return {"rc": p.returncode, "wall_s": time.perf_counter() - t0, "makespan": int(g(r"Makespan:\s+(\d+)") or -1),
            "load": int(g(r"LOAD:\s+(\d+)") or -1), "frag_pct": float(g(r"Fragmentation:\s+([\d.]+)%") or -1),
            "beat": re.findall(r"Beating heuristic by (\d+) bytes! \((\d+) iterations\)", out)[-1:] , "stderr": p.stderr[-200:]}
res = {}
which = sys.argv[1]
for path in (small if which == "small" else big):
    name = os.path.basename(path)
    res[name] = {}
    for lives in ([1, 100] if which == "small" else [1, 10]):
        runs = [run(path, lives, 900) for _ in range(3 if which == "small" else 1)]
        res[name][str(lives)] = runs
        print(name, lives, [(r.get("makespan"), r.get("load"), r.get("frag_pct"), round(r["wall_s"], 2)) for r in runs], flush=True)
json.dump(res, open(f"/root/memplan/probe/baseline_{which}.json", "w"), indent=1)

import glob, os, re, subprocess, time, json
MM = "/root/memplan/minimalloc/build/minimalloc"
B = "/root/memplan/idealloc/benchmarks"
out = {"minimalloc": {}, "big": {}}
for path in sorted(glob.glob(B + "/minimalloc/*.csv")):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([MM, "--capacity=1048576", "--input=" + path, "--output=/tmp/mm.csv", "--timeout=120s"], capture_output=True, text=True, timeout=150)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        rc = "timeout"
    w = time.perf_counter() - t0
    solved = rc == 0 and os.path.exists("/tmp/mm.csv") and os.path.getsize("/tmp/mm.csv") > 0
    out["minimalloc"][os.path.basename(path)] = {"rc": rc, "wall_s": round(w, 2), "solved_at_capacity_1048576": solved}
    print("minimalloc", os.path.basename(path), rc, round(w, 2), solved, flush=True)
    if os.path.exists("/tmp/mm.csv"): os.remove("/tmp/mm.csv")
# MiniMalloc on the two small real traces: capacity = lower bound (load) and +0.3 %
for name, load in (("somas_tensors/resnet50.csv", 1515472556), ("iopddl/G_1.csv", 3030937746)):
    for cap in (load, int(load * 1.003)):
        t0 = time.perf_counter()
        try:
            p = subprocess.run([MM, f"--capacity={cap}", "--input=" + B + "/" + name, "--output=/tmp/mm.csv", "--timeout=120s"], capture_output=True, text=True, timeout=150)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
        w = time.perf_counter() - t0
        solved = rc == 0 and os.path.exists("/tmp/mm.csv") and os.path.getsize("/tmp/mm.csv") > 0
        out["minimalloc"][f"{name}@{cap}"] = {"rc": rc, "wall_s": round(w, 2), "solved": solved}
        print("minimalloc", name, cap, rc, round(w, 2), solved, flush=True)
        if os.path.exists("/tmp/mm.csv"): os.remove("/tmp/mm.csv")
BIN = "/root/memplan/idealloc_patched/target/release/idealloc"
for name in ("somas_tensors/pangu_2.6B.csv", "iopddl/S_1.csv", "iopddl/Y_1.csv"):
    for lives in (1, 10):
        t0 = time.perf_counter()
        try:
            p = subprocess.run([BIN, "--input", B + "/" + name, "ex-csv", "-l", str(lives)], capture_output=True, text=True, timeout=1200)
        except subprocess.TimeoutExpired:
            print("idealloc", name, lives, "timeout", flush=True); out["big"][f"{name}@{lives}"] = "timeout"; continue
        w = time.perf_counter() - t0
        m = re.search(r"PROBE eps_\w+ ([\d.eE+-]+) interval \[([\d.eE+-]+), ([\d.eE+-]+)\]", p.stderr)
        frag = re.search(r"Fragmentation:\s+([\d.]+)%", p.stdout)
        mk = re.search(r"Makespan:\s+(\d+)", p.stdout); ld = re.search(r"LOAD:\s+(\d+)", p.stdout)
        rec = {"rc": p.returncode, "wall_s": round(w, 1), "eps": m and float(m[1]), "interval": m and [float(m[2]), float(m[3])],
               "frag_pct": frag and float(frag[1]), "makespan": mk and int(mk[1]), "load": ld and int(ld[1]), "tail": p.stdout[-200:] if not frag else ""}
        out["big"][f"{name}@{lives}"] = rec
        print("idealloc", name, lives, rec, flush=True)
json.dump(out, open("/root/memplan/probe/mm_and_big.json", "w"), indent=1)

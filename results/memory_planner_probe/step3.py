import csv, json, os, re, subprocess, sys, time
sys.path.insert(0, "/root/memplan/probe")
MM = "/root/memplan/minimalloc/build/minimalloc"; BIN = "/root/memplan/idealloc_patched/target/release/idealloc"
B = "/root/memplan/idealloc/benchmarks"
def check_mm(inp, outp):
    rows = list(csv.DictReader(open(outp)))
    items = sorted((int(r["lower"]), int(r["upper"]), int(r["offset"]), int(r["offset"]) + int(r["size"]), r["id"]) for r in rows)
    n_in = sum(1 for _ in open(inp)) - 1
    bad = 0
    for a in range(len(items)):
        la, ua, oa, ea, _ = items[a]
        for b in range(a + 1, len(items)):
            lb, ub, ob, eb, _ = items[b]
            if lb >= ua: break
            if oa < eb and ob < ea: bad += 1
    return {"buffers_in": n_in, "buffers_out": len(items), "overlaps": bad, "makespan": max(i[3] for i in items)}
out = {}
for name, cap in (("somas_tensors/resnet50.csv", 1515472556), ("iopddl/G_1.csv", 3030937746), ("minimalloc/I.1048576.csv", 1048576)):
    subprocess.run([MM, f"--capacity={cap}", "--input=" + B + "/" + name, "--output=/tmp/mm.csv", "--timeout=120s"], capture_output=True, text=True)
    out["validate_" + name] = check_mm(B + "/" + name, "/tmp/mm.csv"); print("minimalloc validated", name, cap, out["validate_" + name], flush=True)
for name, load, frag in (("somas_tensors/pangu_2.6B.csv", 5530099775, [0.0, 0.01, 0.0334]), ("iopddl/S_1.csv", 1498635932, [0.0, 0.0157]), ("iopddl/Y_1.csv", 497261190115, [0.0028])):
    for f in frag:
        cap = int(load * (1 + f)); t0 = time.perf_counter()
        try:
            p = subprocess.run([MM, f"--capacity={cap}", "--input=" + B + "/" + name, "--output=/tmp/mmbig.csv", "--timeout=300s"], capture_output=True, text=True, timeout=330); rc = p.returncode
        except subprocess.TimeoutExpired: rc = "timeout"
        w = time.perf_counter() - t0
        ok = rc == 0 and os.path.exists("/tmp/mmbig.csv") and os.path.getsize("/tmp/mmbig.csv") > 0
        out[f"mm_{name}@+{f}"] = {"rc": rc, "wall_s": round(w, 1), "solved": ok}; print("minimalloc big", name, f, rc, round(w, 1), ok, flush=True)
        if os.path.exists("/tmp/mmbig.csv"): os.remove("/tmp/mmbig.csv")
for name in ("somas_tensors/pangu_2.6B.csv", "iopddl/S_1.csv"):
    for frac in (None, 0.0, 0.1, 0.25, 0.5, 0.75, 0.99):
        runs = []
        for rep in range(3):
            env = dict(os.environ)
            if frac is not None: env["IDEALLOC_EPS_FRAC"] = str(frac)
            t0 = time.perf_counter()
            p = subprocess.run([BIN, "--input", B + "/" + name, "ex-csv", "-l", "20"], capture_output=True, text=True, env=env, timeout=1200)
            fr = re.search(r"Fragmentation:\s+([\d.]+)%", p.stdout)
            runs.append((float(fr[1]) if fr else None, round(time.perf_counter() - t0, 1)))
        out[f"eps_{name}@{frac}"] = runs; print("eps sweep", name, frac, runs, flush=True)
json.dump(out, open("/root/memplan/probe/step3.json", "w"), indent=1)

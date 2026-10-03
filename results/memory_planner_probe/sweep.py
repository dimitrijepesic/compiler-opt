import json, os, re, subprocess, sys, time, glob
sys.path.insert(0, "/root/memplan/probe")
from validate import validate
BIN = "/root/memplan/idealloc_patched/target/release/idealloc"
B = "/root/memplan/idealloc/benchmarks"
inputs = sorted(glob.glob(B + "/minimalloc/*.csv")) + [B + "/somas_tensors/resnet50.csv", B + "/iopddl/G_1.csv"]
FRACS = [None, 0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
LIVES, REPEATS = 100, 3
res = {}
for path in inputs:
    name = os.path.basename(path)
    res[name] = {}
    for frac in FRACS:
        runs = []
        for rep in range(REPEATS):
            env = dict(os.environ, IDEALLOC_DUMP="/tmp/dump.csv")
            if frac is not None: env["IDEALLOC_EPS_FRAC"] = str(frac)
            t0 = time.perf_counter()
            p = subprocess.run([BIN, "--input", path, "ex-csv", "-l", str(LIVES)], capture_output=True, text=True, env=env, timeout=900)
            wall = time.perf_counter() - t0
            m = re.search(r"PROBE eps_\w+ ([\d.eE+-]+) interval \[([\d.eE+-]+), ([\d.eE+-]+)\]", p.stderr)
            v = validate(path, "/tmp/dump.csv") if p.returncode == 0 else {"valid": False, "makespan": None}
            load = int(re.search(r"LOAD:\s+(\d+)", p.stdout)[1]) if p.returncode == 0 else None
            runs.append({"rc": p.returncode, "wall_s": wall, "eps": float(m[1]) if m else None,
                         "interval": [float(m[2]), float(m[3])] if m else None, "load": load,
                         "makespan": v["makespan"], "valid": v["valid"], "reported": v.get("reported"), "err": p.stderr[-150:] if p.returncode else ""})
        res[name]["default" if frac is None else str(frac)] = runs
        ok = [r for r in runs if r["rc"] == 0]
        print(name, "default" if frac is None else frac, "eps", ok[0]["eps"] if ok else None, "interval", ok[0]["interval"] if ok else None,
              "makespans", [r["makespan"] for r in runs], "valid", [r["valid"] for r in runs], "rc", [r["rc"] for r in runs], flush=True)
json.dump(res, open("/root/memplan/probe/sweep.json", "w"), indent=1)

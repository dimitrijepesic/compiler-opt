import sys, os, json, tempfile
sys.path.insert(0, "scripts"); sys.path.insert(0, ".")
import evaluate_gnn_attribute_audit as m
out = m.OUT_DEFAULT
cfg, programs = m.config(out, "gnn", 42)
m.init_gnn(cfg)
agent, torch = m.W["agent"], m.W["torch"]
P = {p["uri"]: p for p in programs}
tests = {
  "generator://csmith-v0/1": [62, 1, 0, 2],
  "benchmark://npb-v0/1": [130, 28, 0, 1],
  "benchmark://poj104-v1/10/1069": [258, 148, 0, 1],
}
with tempfile.TemporaryDirectory() as wd:
    for uri, cands in tests.items():
        stored = P[uri]["stored"]["42"]["sample_ics"]
        print(uri, "stored", stored, flush=True)
        for i in cands:
            got = [m.sample_rollout(agent, torch, uri, 42*100000 + i*100 + j, os.path.join(wd, "s.bc"))[0] for j in range(8)]
            print(f"   i={i:>3}: {got}  match {sum(a==b for a,b in zip(got,stored))}/8", flush=True)
agent.close()

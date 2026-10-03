"""Brute-force search for the torch-seed index i that reproduces the stored
sample ICs of the original evaluation (seed 42) on programs where the
six-suite global index and the per-suite index both fail."""
import sys, os, tempfile, time
sys.path.insert(0, "scripts"); sys.path.insert(0, ".")
import evaluate_gnn_attribute_audit as m
cfg, programs = m.config(m.OUT_DEFAULT, "gnn", 42)
m.init_gnn(cfg)
agent, torch = m.W["agent"], m.W["torch"]
P = {p["uri"]: p for p in programs}
uris = sys.argv[1:] or ["generator://csmith-v0/1", "benchmark://poj104-v1/10/1069", "generator://csmith-v0/12"]
with tempfile.TemporaryDirectory() as wd:
    for uri in uris:
        stored = P[uri]["stored"]["42"]["sample_ics"]
        t0 = time.time(); hits = []
        print(uri, "stored", stored, "global i", P[uri]["eligible_index"], flush=True)
        for i in range(0, 352):
            first = m.sample_rollout(agent, torch, uri, 42*100000 + i*100 + 0, os.path.join(wd, "s.bc"))[0]
            if first == stored[0]:
                got = [m.sample_rollout(agent, torch, uri, 42*100000 + i*100 + j, os.path.join(wd, "s.bc"))[0] for j in range(8)]
                n = sum(a == b for a, b in zip(got, stored))
                print(f"   i={i:>3}: j0 hit, full {got} match {n}/8", flush=True)
                if n == 8:
                    hits.append(i); break
        print(f"   -> exact hits {hits} ({time.time()-t0:.0f}s)", flush=True)
agent.close()

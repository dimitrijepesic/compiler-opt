"""Second reproduction test: NPB programs whose stored samples did not reproduce with offset 0.
Hypothesis: they were evaluated in the invocation over blas+csmith+npb+poj104 (offset 50+28=78)."""
import sys, os, json, tempfile
sys.path.insert(0, "scripts"); sys.path.insert(0, ".")
import evaluate_gnn_attribute_audit as m
cfg, programs = m.config(m.OUT_DEFAULT, "gnn", 42)
m.init_gnn(cfg)
agent, torch = m.W["agent"], m.W["torch"]
P = {p["uri"]: p for p in programs}
uris = sys.argv[1:]
with tempfile.TemporaryDirectory() as wd:
    for uri in uris:
        p = P[uri]; stored = p["stored"]["42"]["sample_ics"]; pos = p["position_in_suite"]
        print(uri, "pos", pos, "stored", stored, flush=True)
        for off in (130, 78, 0):
            i = off + pos
            got = [m.sample_rollout(agent, torch, uri, 42*100000 + i*100 + j, os.path.join(wd, "s.bc"))[0] for j in range(8)]
            print(f"   offset {off:>3} (i={i:>3}): {got} match {sum(a==b for a,b in zip(got,stored))}/8", flush=True)
agent.close()

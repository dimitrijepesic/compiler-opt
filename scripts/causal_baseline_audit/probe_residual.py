#!/usr/bin/env python3
"""Post-hoc diagnostic (after the campaign, not part of the frozen matrix):
re-run selected campaign programs with artifacts kept, to inspect programs
whose IC difference is not explained by unrolling, or where switching
unrolling off makes the code larger. Uses run_audit.one() unchanged.

  python scripts/causal_baseline_audit/probe_residual.py 3 4 29 30 61 66 34 78
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_audit as R  # noqa: E402

out = R.OUT / "residual_probe"
inputs = json.loads((R.OUT / "inputs.json").read_text())
for n in sys.argv[1:]:
    uri = f"benchmark://npb-v0/{n}"
    rec = R.one((uri, inputs["references"][uri], {"stage": "residual_probe", "fingerprint": "post-hoc diagnostic"},
                 str(out / "artifacts" / f"npb-v0_{n}")))
    R.atomic_json(out / "records" / f"npb-v0_{n}.json", rec)
    print(uri, rec.get("failed", "ok"), flush=True)

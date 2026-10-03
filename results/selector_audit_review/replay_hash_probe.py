"""Bounded replay of one pilot/campaign hash discrepancy; run in cgym image."""
import json
import sys
from pathlib import Path

sys.path.insert(0, '/work/scripts')
import compiler_gym
import baseline_audit_cgym_matrix as audit

root = Path('/work')
out = root / 'results/selector_audit_review/hash_probe'
out.mkdir(exist_ok=False)
uri = 'generator://csmith-v0/40'
inputs = json.loads((root / 'results/selector_audit/inputs.json').read_text())
prog = next(p for p in inputs['programs'] if p['uri'] == uri)
actions = prog['gnn']['456']['traces'][7]
rows = []
for mode in ('step', 'multistep'):
    for repeat in range(3):
        wd = out / f'{mode}_{repeat}'
        wd.mkdir()
        with compiler_gym.make('llvm-v0') as env:
            env.reset(benchmark=uri)
            env.write_bitcode(str(wd / 'plain.bc'))
            audit.add_attributes(wd / 'plain.bc', wd / 'attr.bc')
            assert audit.digest(wd / 'attr.bc') == prog['gnn']['456']['input_sha256']
            env.reset(benchmark=(wd / 'attr.bc').as_uri())
            if mode == 'step':
                for action in actions:
                    _, _, done, info = env.step(action)
                    assert not done, info
            else:
                _, _, done, info = env.multistep(actions)
                assert not done, info
            env.write_bitcode(str(wd / 'candidate.bc'))
            metrics = audit.measure(wd / 'candidate.bc', wd)
            (wd / 'candidate.ll').write_text(audit.command([audit.LLVM / 'llvm-dis', wd / 'candidate.bc', '-o', '-']))
            row = {'mode': mode, 'repeat': repeat, **metrics}
            rows.append(row)
            print(json.dumps(row), flush=True)
(out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')

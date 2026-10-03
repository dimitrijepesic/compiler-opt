#!/usr/bin/env python3
"""Independently check recorded causal-audit provenance and totals; no LLVM run."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/causal_baseline_audit'
OUT = ROOT / 'results/causal_baseline_review'
FIELDS = ('ic', 'text_sec', 'text', 'bitcode_sha256', 'object_sha256')
UNSHIPPED = {'PROTOCOL.md'}
CELLS = {'P': 'plain/service_original', 'U': 'plain/service_marked',
         'A': 'attr/service_original', 'AU': 'attr/service_marked'}


def read(p):
    return json.loads(p.read_text())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inputs = read(BASE / 'inputs.json')
    summary = read(BASE / 'summary.json')
    records = [read(p) for p in (BASE / 'campaign/records').glob('*.json')]
    assert len(records) == len({r['uri'] for r in records}) == 120
    assert {r['uri'] for r in records} == set(inputs['campaign'])
    manifest = read(BASE / 'campaign/manifest.json')
    local_files = 0
    for name, path in manifest['paths'].items():
        if path.startswith('/work/') and name not in UNSHIPPED:
            assert digest(ROOT / path[len('/work/'):]) == manifest['sha256'][name], name
            local_files += 1
    totals = {m: {label: sum(r['cells'][cell][m] for r in records) for label, cell in CELLS.items()}
              for m in ('ic', 'text_sec', 'text')}
    for m, sums in totals.items():
        for key, val in sums.items():
            assert val == summary['campaign']['totals'][m]['sums'][key]
    unrolled, ir_same, nonunroll_residual = [], [], []
    for r in records:
        assert r['complete'] and 'failed' not in r and all(r['checks'].values())
        assert r['fingerprint'] == manifest['fingerprint']
        ref = ROOT / r['reference']['canonical_record']
        assert digest(ref) == r['reference']['canonical_record_sha256']
        original = read(ref)
        for variant in ('plain', 'attr'):
            for metric in FIELDS:
                assert r['cells'][variant+'/service_original'][metric] == original[variant]['oz'][metric]
            for service, replica in [('service_original', 'replica_service'), ('service_marked', 'replica_service_marked')]:
                a,b = r['cells'][variant+'/'+service],r['cells'][variant+'/'+replica]
                assert a['ir_sha256'] == b['ir_sha256']
                for m in ('ic','text_sec','text','object_sha256'):
                    assert a[m] == b[m]
            assert r['cells'][variant+'/replica_service_marked']['unroll_remarks']['total'] == 0
        p,u,a,au = (r['cells'][CELLS[k]] for k in ('P','U','A','AU'))
        for m in ('ic','text_sec','text'):
            assert a[m] == au[m]
        assert r['cells']['attr/replica_service']['unroll_remarks']['total'] == 0
        remarks = r['cells']['plain/replica_service']['unroll_remarks']
        if remarks['total']:
            unrolled.append(r)
            assert remarks['by_name'] == {'FullyUnrolled': remarks['total']}
            assert u['ic'] == a['ic'] and u['ir_nosize_sha256'] == a['ir_nosize_sha256']
        elif u['ic'] != a['ic']:
            nonunroll_residual.append(r['uri'])
        if u['ir_nosize_sha256'] == a['ir_nosize_sha256']:
            ir_same.append(r)
            assert r['codegen_control']['plain_marked_oz_late_attr']['object_sha256'] == a['object_sha256']
            assert r['codegen_control']['attr_oz_stripped']['object_sha256'] == u['object_sha256']
        for control in r['codegen_control'].values():
            assert control['ic'] == r['cells'][control['base_cell']]['ic']
    controls = {m:{k:sum(r['codegen_control'][k][m] for r in records) for k in records[0]['codegen_control']}
                for m in ('ic','text_sec','text')}
    example_dir = BASE / 'example_npb116_transfb_nc0'
    example = read(example_dir / 'example.json')
    for name,h in example['files_sha256'].items():
        assert digest(example_dir / name) == h, name
    assert all(example['checks'].values())
    assert all(example['behaviour']['variants_identical_to_reference'].values())
    result = {'scope':'Independent saved-record, arithmetic, local-manifest and example-artifact verification; no new compiler executions.',
              'records':len(records),'local_manifest_files_checked':local_files,
              'totals':totals,'controls':controls,'programs_with_unrolling':len(unrolled),
              'unroll_remarks':sum(r['cells']['plain/replica_service']['unroll_remarks']['total'] for r in records),
              'same_ir_without_size_attrs':len(ir_same),'nonunroll_ic_residual_programs':nonunroll_residual,
              'ic_difference_on_unrolled_programs':sum(r['cells'][CELLS['P']]['ic']-r['cells'][CELLS['U']]['ic'] for r in unrolled),
              'codegen_on_U_saved_bytes':totals['text_sec']['U']-controls['text_sec']['plain_marked_oz_late_attr'],
              'U_late_attrs_minus_A_bytes':controls['text_sec']['plain_marked_oz_late_attr']-totals['text_sec']['A'],
              'example_artifact_hashes_checked':len(example['files_sha256'])}
    OUT.mkdir(exist_ok=True)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Independent, read-only verification of selector audit records and arithmetic.

Does not import the campaign/reporting code or run LLVM. Writes review outputs
only to results/selector_audit_review; original records remain unchanged.
"""
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/selector_audit'
REVIEW = ROOT / 'results/selector_audit_review'
METRICS = ('ic', 'text_sec', 'text')
FIELDS = (*METRICS, 'bitcode_sha256', 'object_sha256')
GENERATORS = [f'gnn{s}' for s in (42, 123, 456)] + [f'rnd{s}' for s in range(42, 47)]
KEYS = {'ic_first': ('ic',), 'code_first': ('text_sec',),
        'ic_then_code': ('ic', 'text_sec'), 'berkeley_first': ('text',)}
COUNTS = Counter()


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashed_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def equal(actual, expected):
    if isinstance(expected, dict):
        for k, value in expected.items():
            equal(actual[k], value)
    elif isinstance(expected, float):
        assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-10), (actual, expected)
    else:
        assert actual == expected, (actual, expected)


def load_records(directory):
    paths = sorted(p for p in directory.glob('*.json') if p.name != 'run_manifest.json')
    records = {read(p)['uri']: read(p) for p in paths}
    assert len(records) == len(paths), 'duplicate URI'
    for p in paths:
        assert p.stem == hashed_text(read(p)['uri'])
    return records, paths


def candidates(record, generator):
    return record['gnn' if generator.startswith('gnn') else 'random'][generator[3:]]['candidates']


def pick(record, generator, selector):
    cs = candidates(record, generator)
    return sorted(enumerate(cs), key=lambda pair: (*[pair[1][m] for m in KEYS[selector]], pair[0]))[0][1]


def compare_metrics(a, b):
    equal(a, {k: b[k] for k in FIELDS})


def main():
    snapshot = read(REVIEW / 'input_snapshot.json')
    for path, digest in snapshot['files'].items():
        assert sha(ROOT / path) == digest, f'frozen input changed: {path}'
    COUNTS['frozen_files_unchanged'] = len(snapshot['files'])
    frozen = read(BASE / 'inputs.json')
    manifest = read(BASE / 'manifest.json')
    run = read(BASE / 'records/run_manifest.json')
    summary = read(BASE / 'summary.json')
    assert manifest['script_sha256'] == sha(ROOT / 'scripts/evaluate_selector_audit.py')
    assert manifest['helper_sha256'] == sha(ROOT / manifest['helper'])
    assert manifest['passes_yaml_sha256'] == sha(ROOT / 'configs/passes.yaml')
    assert manifest['inputs_sha256'] == hashed_text(json.dumps(frozen['programs'], sort_keys=True))
    assert manifest['fingerprint'] == hashed_text(json.dumps({k: v for k, v in manifest.items() if k not in ('created', 'fingerprint')}, sort_keys=True))
    assert run['fingerprint'] == hashed_text(manifest['fingerprint'] + '|replay=multistep|pilot=0')
    assert summary['meta']['report_script_sha256'] == sha(ROOT / 'scripts/report_selector_audit.py')
    records, paths = load_records(BASE / 'records')
    pilots, _ = load_records(BASE / 'pilot')
    assert summary['meta']['record_hashes_sha256'] == hashed_text(''.join(sorted(sha(p) for p in paths)))
    original_programs = read(ROOT / 'results/gnn_attribute_audit/programs.json')['programs']
    expected = {p['uri']: p for p in original_programs}
    inputs = {p['uri']: p for p in frozen['programs']}
    assert len(expected) == len(inputs) == len(records) == 347
    assert set(expected) == set(inputs) == set(records)
    action_ids = sorted(map(int, re.findall(r'action_id: (\d+)\n  name: \S+', (ROOT / 'configs/passes.yaml').read_text())))
    assert len(action_ids) == 36 and action_ids == frozen['action_ids']
    for uri, r in records.items():
        assert 'failed' not in r and r['fingerprint'] == run['fingerprint']
        assert r['replay_mode'] == 'multistep' and not r['pilot']
        assert r['suite'] == expected[uri]['suite']
        assert set(r['gnn']) == {'42', '123', '456'}
        assert set(r['random']) == {'42', '43', '44', '45', '46'}
        assert all(r['input']['checks'].values()) and all(r['baseline']['checks'].values())
        original_null = ROOT / 'results/gnn_attribute_audit/records_null' / f'{hashed_text(uri)}.json'
        null = read(original_null)
        compare_metrics(r['baseline'], null['attr']['oz'])
        assert r['baseline']['ic'] == r['baseline']['ic_env'] == r['input']['attr_oz_ic_observation']
        equal(r['input'], {k: null['attr'][k] for k in ('input_sha256', 'ir_sha256', 'o0_ic')})
        assert r['input']['ir_sha256_after_load'] == r['input']['ir_sha256']
        assert r['input']['headers_plain'] == r['input']['headers_attr']
        for gen in GENERATORS:
            cs = candidates(r, gen)
            assert len(cs) == 8 and [c['index'] for c in cs] == list(range(8))
            assert all(c['ok'] and len(c['actions']) == 45 for c in cs)
            assert all(set(c['actions']) <= set(action_ids) for c in cs)
            for c in cs:
                assert all(isinstance(c[m], int) and c[m] >= 0 for m in METRICS)
                if gen != 'rnd42':
                    assert c['steps_applied'] == 45 and not c['done_seen']
                    assert c['ic'] == c['ic_env']
            if gen.startswith('gnn'):
                directory = ROOT / 'results/gnn_attribute_audit'
                if r['suite'] == 'npb-v0':
                    directory /= 'npb_offset78'
                source = directory / f'records_gnn_seed{gen[3:]}' / f'{hashed_text(uri)}.json'
                original = read(source)
                assert r['gnn'][gen[3:]]['source'] == str(source.relative_to(ROOT))
                assert r['gnn'][gen[3:]]['source_sha256'] == sha(source)
                for j, c in enumerate(cs):
                    smp = original['attr']['samples'][j]
                    assert all(a[1:] == [1, 0] for a in smp['actions'])
                    assert c['actions'] == [a[0] for a in smp['actions']]
                    assert c['ic'] == smp['ic'] == c['stored_ic']
                    COUNTS['gnn_candidate_ics_and_actions'] += 1
                winner = pick(r, gen, 'ic_first')
                assert winner['index'] == original['attr']['best_by_ic']['index']
                compare_metrics(winner, original['attr']['best_by_ic'])
                COUNTS['old_winners_metrics_and_hashes'] += 1
            else:
                rep = int(gen[3:])
                seed = int.from_bytes(hashlib.sha256(f'{rep}:{uri}'.encode()).digest()[:8], 'big')
                seqs = np.random.default_rng(seed).choice(action_ids, size=(8, 45)).tolist()
                assert r['random'][str(rep)]['seed_int'] == seed
                assert seqs == r['random'][str(rep)]['sequences'] == [c['actions'] for c in cs]
                if rep == 42:
                    assert seqs == null['random_actions']
                    assert r['random']['42']['source_sha256'] == sha(original_null)
                    for c, old in zip(cs, null['attr']['random']):
                        compare_metrics(c, old)
                COUNTS['random_candidates_reused' if rep == 42 else 'random_candidates_new'] += 8
            assert pick(r, gen, 'code_first')['text_sec'] <= pick(r, gen, 'ic_first')['text_sec']
            assert pick(r, gen, 'ic_first')['ic'] <= pick(r, gen, 'code_first')['ic']
    pilot_uris = set()
    for suite in {p['suite'] for p in original_programs}:
        ps = [p for p in original_programs if p['suite'] == suite]
        pilot_uris.update([min(ps, key=lambda p: (p['o0'], p['uri']))['uri'],
                           min(ps, key=lambda p: (-p['o0'], p['uri']))['uri']])
    assert set(pilots) == set(frozen['pilot_uris']) == pilot_uris and len(pilots) == 12
    hash_differences = []
    for uri, p in pilots.items():
        assert p['replay_mode'] == 'step' and 'failed' not in p
        assert all(p['input']['checks'].values()) and all(p['baseline']['checks'].values())
        for gen in GENERATORS:
            for a, b in zip(candidates(p, gen), candidates(records[uri], gen)):
                equal(a, {k: b[k] for k in METRICS})
                assert a['actions'] == b['actions']
                COUNTS['pilot_vs_campaign_candidates_metrics'] += 1
                differences = [k for k in FIELDS if a[k] != b[k]]
                if differences:
                    hash_differences.append({'uri': uri, 'generator': gen, 'index': a['index'],
                                             'different_fields': differences,
                                             'selected_by': [s for s in KEYS if pick(records[uri], gen, s)['index'] == a['index']]})
                else:
                    COUNTS['pilot_vs_campaign_candidates_full_hash_match'] += 1
        for c in p['random']['42']['pilot_replay']:
            assert c['ok'] and c['steps_applied'] == 45 and not c['done_seen']
            compare_metrics(c, candidates(records[uri], 'rnd42')[c['index']])
            COUNTS['pilot_random42_replays'] += 1
        assert all(e['equal'] and e['step'] == e['multistep'] for e in p['multistep_equivalence'].values())
    out_cohorts = {}
    for name, reported in summary['cohorts'].items():
        rs = [r for r in records.values() if name == 'ALL' or
              (name == 'without_npb' and r['suite'] != 'npb-v0') or r['suite'] == name]
        oz = {m: sum(r['baseline'][m] for r in rs) for m in METRICS}
        equal(reported['oz'], oz)
        assert len(rs) == reported['n']
        out_cohorts[name] = {}
        for gen in GENERATORS:
            out_cohorts[name][gen] = {}
            for selector in KEYS:
                chosen = [pick(r, gen, selector) for r in rs]
                out_cohorts[name][gen][selector] = {}
                for metric in METRICS:
                    vals = [c[metric] for c in chosen]
                    bases = [r['baseline'][metric] for r in rs]
                    total = sum(vals)
                    wtl = [sum(v < b for v, b in zip(vals, bases)), sum(v == b for v, b in zip(vals, bases)), sum(v > b for v, b in zip(vals, bases))]
                    stats = {'sum': total, 'gain_pct': 100 * (oz[metric] - total) / oz[metric], 'wtl_vs_oz': wtl,
                             'median_program_gain_pct': median(100 * (b-v)/b for b, v in zip(bases, vals) if b)}
                    equal(reported['generators'][gen][selector][metric], stats)
                    out_cohorts[name][gen][selector][metric] = stats
                    COUNTS['generator_selector_metric_cells'] += 1
            regrets = [pick(r, gen, 'ic_first')['text_sec'] - pick(r, gen, 'code_first')['text_sec'] for r in rs]
            equal(reported['generators'][gen]['regret_code_bytes'], {'sum': sum(regrets), 'programs_with_regret': sum(x > 0 for x in regrets), 'median_bytes': median(regrets), 'pct_of_oz_code': 100*sum(regrets)/oz['text_sec']})
            for metric in METRICS:
                total = sum(min([r['baseline'][metric]] + [c[metric] for c in candidates(r, gen)]) for r in rs)
                returned = sum(r['baseline'][metric] <= min(c[metric] for c in candidates(r, gen)) for r in rs)
                equal(reported['oz_fallback'][gen][metric], {'sum': total, 'gain_pct': 100*(oz[metric]-total)/oz[metric], 'baseline_returned': returned})
        for seed in (42, 123, 456):
            for selector in KEYS:
                for metric in METRICS:
                    diffs = []
                    for rep in range(42, 47):
                        pairs = [(pick(r, f'gnn{seed}', selector)[metric], pick(r, f'rnd{rep}', selector)[metric]) for r in rs]
                        diff = sum(a-b for a, b in pairs)
                        pct = 100*diff/oz[metric]
                        wtl = [sum(a < b for a,b in pairs), sum(a == b for a,b in pairs), sum(a > b for a,b in pairs)]
                        equal(reported['pairs'][f'gnn{seed}-rnd{rep}'][selector][metric], {'gnn_minus_random': diff, 'pct_of_oz': pct, 'wtl_gnn_vs_random': wtl})
                        diffs.append(pct)
                        COUNTS['pair_selector_metric_cells'] += 1
                    equal(reported['pair_summary'][f'gnn{seed}'][selector][metric], {'mean_pct': sum(diffs)/len(diffs), 'min_pct': min(diffs), 'max_pct': max(diffs), 'n_replicates': 5})
    for gen in GENERATORS:
        for selector in ('ic_first', 'code_first'):
            total = sum(r['baseline']['text_sec'] - pick(r, gen, selector)['text_sec'] for r in records.values())
            entry = summary['suite_contribution'][gen][selector]
            assert total == entry['total_saved_bytes']
            for suite in {r['suite'] for r in records.values()}:
                saved = sum(r['baseline']['text_sec']-pick(r, gen, selector)['text_sec'] for r in records.values() if r['suite'] == suite)
                equal(entry[suite], {'saved_bytes': saved, 'share_of_total_pct': 100*saved/total})
    result = {'verified_at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS numeric/provenance checks; see hash differences', 'checks': dict(COUNTS),
              'pilot_campaign_hash_differences': hash_differences,
              'numpy_for_independent_seed_regeneration': np.__version__, 'cohorts': out_cohorts,
              'limits': 'Independent verification of saved records, provenance, arithmetic and pilot/campaign agreement. No new LLVM replay or claim of general semantic equivalence.'}
    (REVIEW / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'checks': dict(COUNTS), 'hash_differences': hash_differences}, indent=2))


if __name__ == '__main__':
    main()

"""pytest wrapper around verify_paper_numbers.py: one test per paper claim,
so `pytest scripts/` reports exactly which number regressed instead of a
single pass/fail for the whole battery.

  pytest scripts/test_paper_numbers.py -v
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import verify_paper_numbers as vpn


def _collect():
    vpn.CHECKS.clear()
    vpn.table_i()
    vpn.table_ii()
    vpn.table_iii()
    vpn.sampling_stats()
    vpn.k32()
    vpn.pearson()
    vpn.binary_metrics()
    vpn.pretraining()
    vpn.gnn_cost()
    return list(vpn.CHECKS)


CASES = _collect()


@pytest.mark.parametrize(
    "ok,name,expected,actual,unit", CASES, ids=[c[1] for c in CASES])
def test_claim(ok, name, expected, actual, unit):
    assert ok, f"{name}: paper says {expected}{unit}, data says {actual}{unit}"

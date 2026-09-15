from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch10 as batch10_module
from tools.trading_breaks_recovery_batch10 import batch10_targets

EXPECTED_BATCH10 = [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2025, 1, 20), "MARTIN_LUTHER_KING_DAY"),
    (date(2025, 2, 17), "PRESIDENTS_DAY"),
    (date(2025, 4, 18), "GOOD_FRIDAY"),
]


def test_batch10_historical_frozen_identity_is_immutable_after_integration():
    assert batch10_targets() == EXPECTED_BATCH10


def test_batch10_accessor_remains_immutable_to_caller():
    altered = batch10_targets()
    altered.pop()
    assert batch10_targets() == EXPECTED_BATCH10


def test_batch10_frozen_module_remains_free_of_live_selection():
    source = inspect.getsource(batch10_module).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source

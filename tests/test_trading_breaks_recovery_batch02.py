from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch02 import BATCH_SIZE, batch02_targets
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH02 = [
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
    (
        date(2021, 12, 31),
        "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED",
    ),
    (date(2022, 1, 17), "MARTIN_LUTHER_KING_DAY"),
    (date(2022, 2, 21), "PRESIDENTS_DAY"),
    (date(2022, 4, 15), "GOOD_FRIDAY"),
]


def test_batch02_size_inherits_frozen_size_five():
    assert BATCH_SIZE == 5


def test_batch02_membership_is_frozen_exactly():
    assert batch02_targets() == EXPECTED_BATCH02


def test_batch02_was_mechanically_derived_from_current_queue_prefix():
    assert recovery_queue()[:BATCH_SIZE] == EXPECTED_BATCH02


def test_batch02_is_strictly_chronological_and_unique():
    days = [day for day, _ in batch02_targets()]
    assert days == sorted(days)
    assert len(days) == len(set(days))


def test_batch02_contains_only_currently_unresolved_dates():
    queue_days = {day for day, _ in recovery_queue()}
    resolved_days = set(SPECIAL_SESSION_EVIDENCE)
    for day, _ in batch02_targets():
        assert day in queue_days
        assert day not in resolved_days


def test_batch01_resolved_dates_cannot_be_reintroduced_into_batch02():
    batch02_days = {day for day, _ in batch02_targets()}
    assert date(2021, 11, 25) not in batch02_days
    assert date(2021, 11, 26) not in batch02_days
    assert date(2021, 12, 23) not in batch02_days


def test_current_queue_has_expected_post_batch01_scope():
    queue = recovery_queue()
    assert len(queue) == 63
    assert queue[0] == EXPECTED_BATCH02[0]
    assert queue[-1] == (date(2026, 7, 3), "INDEPENDENCE_DAY_OBSERVED")

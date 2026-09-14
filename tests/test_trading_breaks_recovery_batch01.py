from datetime import date

from tools.trading_breaks_recovery_batch01 import BATCH_SIZE, batch01_targets
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch_size_is_frozen_at_five():
    assert BATCH_SIZE == 5


def test_batch01_is_exact_governed_queue_prefix():
    assert batch01_targets() == recovery_queue()[:BATCH_SIZE]


def test_batch01_is_strictly_chronological():
    targets = batch01_targets()
    days = [day for day, _ in targets]
    assert days == sorted(days)
    assert len(days) == len(set(days))


def test_batch01_expected_membership_is_version_locked_before_execution():
    assert batch01_targets() == [
        (date(2021, 11, 25), "THANKSGIVING_DAY"),
        (date(2021, 11, 26), "THANKSGIVING_FRIDAY"),
        (date(2021, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
        (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
        (
            date(2021, 12, 31),
            "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED",
        ),
    ]


def test_batch01_does_not_reintroduce_resolved_in_window_dates():
    days = {day for day, _ in batch01_targets()}
    assert date(2021, 9, 6) not in days
    assert date(2025, 1, 9) not in days


def test_batch01_does_not_skip_the_first_unresolved_candidate():
    assert batch01_targets()[0] == recovery_queue()[0]

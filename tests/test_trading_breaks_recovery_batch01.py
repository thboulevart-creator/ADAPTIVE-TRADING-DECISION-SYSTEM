from datetime import date

from tools.trading_breaks_recovery_batch01 import BATCH_SIZE, batch01_targets
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH01 = [
    (date(2021, 11, 25), "THANKSGIVING_DAY"),
    (date(2021, 11, 26), "THANKSGIVING_FRIDAY"),
    (date(2021, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
    (
        date(2021, 12, 31),
        "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED",
    ),
]


def test_batch_size_is_frozen_at_five():
    assert BATCH_SIZE == 5


def test_batch01_membership_is_immutable_after_adjudication():
    assert batch01_targets() == EXPECTED_BATCH01


def test_batch01_is_strictly_chronological_and_unique():
    days = [day for day, _ in batch01_targets()]
    assert days == sorted(days)
    assert len(days) == len(set(days))


def test_recovery_queue_advances_without_rewriting_batch01_history():
    queue = recovery_queue()
    assert queue[0] == (date(2021, 12, 24), "CHRISTMAS_OBSERVED")
    assert date(2021, 11, 25) not in {day for day, _ in queue}
    assert date(2021, 11, 26) not in {day for day, _ in queue}
    assert date(2021, 12, 23) not in {day for day, _ in queue}
    assert date(2021, 12, 24) in {day for day, _ in queue}
    assert date(2021, 12, 31) in {day for day, _ in queue}

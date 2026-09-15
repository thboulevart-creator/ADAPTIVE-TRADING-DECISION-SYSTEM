from datetime import date

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


def test_batch02_size_remains_frozen_at_five():
    assert BATCH_SIZE == 5


def test_batch02_membership_is_immutable_after_adjudication():
    assert batch02_targets() == EXPECTED_BATCH02


def test_batch02_history_remains_chronological_and_unique():
    days = [day for day, _ in batch02_targets()]
    assert days == sorted(days)
    assert len(days) == len(set(days))


def test_recovery_queue_advances_without_rewriting_batch02_history():
    queue = recovery_queue()
    queue_days = {day for day, _ in queue}
    assert len(queue) == 26
    assert queue[0] == (date(2021, 12, 24), "CHRISTMAS_OBSERVED")
    assert queue[-1] == (date(2026, 7, 3), "INDEPENDENCE_DAY_OBSERVED")

    # Batch 02 PASS dates leave the unresolved queue.
    assert date(2022, 1, 17) not in queue_days
    assert date(2022, 2, 21) not in queue_days

    # Batch 02 BLOCKED dates remain unresolved; no negative-evidence promotion.
    assert date(2021, 12, 24) in queue_days
    assert date(2021, 12, 31) in queue_days
    assert date(2022, 4, 15) in queue_days

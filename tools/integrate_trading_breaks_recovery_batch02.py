from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
BATCH_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch02.py"
NEW_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2022_batch02.py"

RUN_ID = 34888022168
ARTIFACT_ID = 10364984459
ARTIFACT_SHA256 = "ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    if "SPECIAL_MARTIN_LUTHER_KING_DAY_2022" in text:
        return

    marker = "    date(2025, 1, 9): {\n"
    block = f'''    date(2022, 1, 17): {{
        "reason": "SPECIAL_MARTIN_LUTHER_KING_DAY_2022",
        # Broker-native Trading Breaks record 32811 starts at 17:59 UTC and
        # ends at 22:59 UTC; calibrated reopening is 23:00 UTC. Hour 17 is
        # partially tradable, therefore only 18-22 are fully closed.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1642377600000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch02_qualification.md"
        ),
    }},
    date(2022, 2, 21): {{
        "reason": "SPECIAL_PRESIDENTS_DAY_2022",
        # Broker-native Trading Breaks record 33515 starts at 17:59 UTC and
        # ends at 22:59 UTC; calibrated reopening is 23:00 UTC. Hour 17 is
        # partially tradable, therefore only 18-22 are fully closed.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1645401600000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch02_qualification.md"
        ),
    }},
'''
    CALENDAR.write_text(
        replace_once(text, marker, block + marker, "calendar Batch 02 insertion"),
        encoding="utf-8",
    )


def update_protocol_tests() -> None:
    text = PROTOCOL_TEST.read_text(encoding="utf-8")
    text = text.replace(
        "test_queue_scope_sorted_and_has_63_unresolved_candidates_after_batch01",
        "test_queue_scope_sorted_and_has_61_unresolved_candidates_after_batch02",
    )
    text = text.replace("assert len(queue) == 63", "assert len(queue) == 61")
    text = text.replace(
        '"start": "1640368800000",  # 2021-11-25 18:00:00Z',
        '"start": "1640368800000",  # 2021-12-24 18:00:00Z',
    )
    text = text.replace(
        '"end": "1640386740000",    # 2021-11-25 22:59:00Z',
        '"end": "1640386740000",    # 2021-12-24 22:59:00Z',
    )
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def rewrite_batch02_tests() -> None:
    BATCH_TEST.write_text('''from datetime import date

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
    assert len(queue) == 61
    assert queue[0] == (date(2021, 12, 24), "CHRISTMAS_OBSERVED")
    assert queue[-1] == (date(2026, 7, 3), "INDEPENDENCE_DAY_OBSERVED")

    # Batch 02 PASS dates leave the unresolved queue.
    assert date(2022, 1, 17) not in queue_days
    assert date(2022, 2, 21) not in queue_days

    # Batch 02 BLOCKED dates remain unresolved; no negative-evidence promotion.
    assert date(2021, 12, 24) in queue_days
    assert date(2021, 12, 31) in queue_days
    assert date(2022, 4, 15) in queue_days
''', encoding="utf-8")


def create_calendar_tests() -> None:
    NEW_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


def test_mlk_day_2022_exact_broker_break_is_integrated():
    day = date(2022, 1, 17)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_MARTIN_LUTHER_KING_DAY_2022"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_presidents_day_2022_exact_broker_break_is_integrated():
    day = date(2022, 2, 21)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_PRESIDENTS_DAY_2022"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_batch02_blocked_dates_are_not_silently_promoted():
    assert date(2021, 12, 24) not in SPECIAL_SESSION_EVIDENCE
    assert date(2021, 12, 31) not in SPECIAL_SESSION_EVIDENCE
    assert date(2022, 4, 15) not in SPECIAL_SESSION_EVIDENCE
''', encoding="utf-8")


def main() -> int:
    integrate_calendar()
    update_protocol_tests()
    rewrite_batch02_tests()
    create_calendar_tests()
    print(
        "Prepared Batch 02 integration: 2 PASS dates; 3 BLOCKED dates preserved; "
        f"run={RUN_ID}; artifact={ARTIFACT_ID}; sha256={ARTIFACT_SHA256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

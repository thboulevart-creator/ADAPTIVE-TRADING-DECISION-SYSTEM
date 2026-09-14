from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
DOWNLOADER_TEST = REPO / "tests" / "test_dukascopy_downloader_calendar_coverage_gate.py"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
BATCH_TOOL = REPO / "tools" / "trading_breaks_recovery_batch01.py"
BATCH_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch01.py"
BATCH_WORKFLOW = REPO / ".github" / "workflows" / "trading-breaks-recovery-batch01.yml"
CALENDAR_WORKFLOW = REPO / ".github" / "workflows" / "dukascopy-calendar-regression.yml"
NEW_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2021_batch01.py"

RUN_ID = 34885895206
ARTIFACT_ID = 10364872726
ARTIFACT_SHA256 = "95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    if "SPECIAL_THANKSGIVING_DAY_2021" in text:
        return

    marker = "    date(2025, 1, 9): {\n"
    block = f'''    date(2021, 11, 25): {{
        "reason": "SPECIAL_THANKSGIVING_DAY_2021",
        # Broker-native Trading Breaks record 30449 starts at 17:59 UTC and
        # ends at 22:59 UTC; calibrated reopening is 23:00 UTC. Hour 17 is
        # partially tradable, therefore only 18-22 are fully closed.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1637798400000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    }},
    date(2021, 11, 26): {{
        "reason": "SPECIAL_THANKSGIVING_FRIDAY_2021",
        # Broker-native record 30450 starts at 18:14 UTC. Hour 18 is partially
        # tradable. Hours 19-21 are additional whole-hour holiday closures;
        # Friday 22-23 are already governed by the regular weekly close.
        "fully_closed_hours_utc": frozenset(range(19, 22)),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1637884800000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    }},
    date(2021, 12, 23): {{
        "reason": "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2021",
        # Broker-native record 31532 starts at 21:14 UTC and remains closed
        # through the Christmas/weekend interval. Hour 21 remains partially
        # tradable; 22-23 are fully closed on this exact target date.
        "fully_closed_hours_utc": frozenset({{22, 23}}),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1640217600000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    }},
'''
    CALENDAR.write_text(replace_once(text, marker, block + marker, "calendar insertion"), encoding="utf-8")


def update_downloader_fixture() -> None:
    text = DOWNLOADER_TEST.read_text(encoding="utf-8")
    text = text.replace(
        "# Thanksgiving Day 2021 remains unresolved in the current coverage registry.",
        "# Christmas Observed 2021 remains unresolved after Batch 01 adjudication.",
    )
    text = text.replace('"2021-11-25"', '"2021-12-24"')
    DOWNLOADER_TEST.write_text(text, encoding="utf-8")


def update_protocol_tests() -> None:
    text = PROTOCOL_TEST.read_text(encoding="utf-8")
    text = text.replace("TARGET = date(2021, 11, 25)", "TARGET = date(2021, 12, 24)")
    text = text.replace('"1637863200000"', '"1640368800000"')
    text = text.replace('"1637881140000"', '"1640386740000"')
    text = text.replace('candidate_reason="THANKSGIVING_DAY"', 'candidate_reason="CHRISTMAS_OBSERVED"')
    text = text.replace(
        "test_queue_is_frozen_scope_sorted_and_has_66_unresolved_candidates",
        "test_queue_scope_sorted_and_has_63_unresolved_candidates_after_batch01",
    )
    text = text.replace("assert len(queue) == 66", "assert len(queue) == 63")
    text = text.replace("assert days[0] == date(2021, 11, 25)", "assert days[0] == date(2021, 12, 24)")
    text = text.replace(
        'assert result["reopen_utc"] == "2021-11-25T23:00:00Z"',
        'assert result["reopen_utc"] == "2021-12-24T23:00:00Z"',
    )
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def freeze_batch01_tool() -> None:
    text = BATCH_TOOL.read_text(encoding="utf-8")
    old = '''def batch01_targets() -> list[tuple[date, str]]:
    queue = recovery_queue()
    if len(queue) < BATCH_SIZE:
        raise RuntimeError("governed recovery queue shorter than fixed Batch 01 size")
    return queue[:BATCH_SIZE]
'''
    new = '''FROZEN_BATCH01_TARGETS: tuple[tuple[date, str], ...] = (
    (date(2021, 11, 25), "THANKSGIVING_DAY"),
    (date(2021, 11, 26), "THANKSGIVING_FRIDAY"),
    (date(2021, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
    (date(2021, 12, 31), "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED"),
)


def batch01_targets() -> list[tuple[date, str]]:
    """Return the immutable membership versioned before Batch 01 execution."""
    return list(FROZEN_BATCH01_TARGETS)
'''
    BATCH_TOOL.write_text(replace_once(text, old, new, "freeze Batch 01 targets"), encoding="utf-8")


def rewrite_batch01_tests() -> None:
    BATCH_TEST.write_text('''from datetime import date

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
''', encoding="utf-8")


def archive_batch01_workflow() -> None:
    text = BATCH_WORKFLOW.read_text(encoding="utf-8")
    start = text.index("on:\n")
    permissions = text.index("permissions:\n")
    text = text[:start] + "on:\n  workflow_dispatch:\n\n" + text[permissions:]
    BATCH_WORKFLOW.write_text(text, encoding="utf-8")


def update_calendar_regression_workflow() -> None:
    text = CALENDAR_WORKFLOW.read_text(encoding="utf-8")
    text = text.replace(
        "            tests/test_dukascopy_usatech_calendar_2021_labor_day.py \\\n",
        "            tests/test_dukascopy_usatech_calendar_2021_labor_day.py \\\n            tests/test_dukascopy_usatech_calendar_2021_batch01.py \\\n",
    )
    text = text.replace("after pilot integration", "after Batch 01 integration")
    text = text.replace("== 25", "== 28")
    text = text.replace("== 86", "== 83")
    CALENDAR_WORKFLOW.write_text(text, encoding="utf-8")


def create_calendar_tests() -> None:
    NEW_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


def test_thanksgiving_2021_exact_broker_break_is_integrated():
    day = date(2021, 11, 25)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_THANKSGIVING_DAY_2021"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_thanksgiving_friday_2021_preserves_regular_weekly_close_boundary():
    day = date(2021, 11, 26)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset({19, 20, 21})
    assert classify_slot(day, 18).status == EXPECTED_OPEN
    for hour in (19, 20, 21):
        assert classify_slot(day, hour).reason == "SPECIAL_THANKSGIVING_FRIDAY_2021"
    assert classify_slot(day, 22).reason == "WEEKLY_POST_CLOSE"
    assert classify_slot(day, 23).reason == "WEEKLY_POST_CLOSE"


def test_christmas_pre_holiday_2021_exact_start_date_is_integrated():
    day = date(2021, 12, 23)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset({22, 23})
    assert classify_slot(day, 21).status == EXPECTED_OPEN
    for hour in (22, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2021"


def test_blocked_batch01_dates_are_not_silently_promoted():
    assert date(2021, 12, 24) not in SPECIAL_SESSION_EVIDENCE
    assert date(2021, 12, 31) not in SPECIAL_SESSION_EVIDENCE
''', encoding="utf-8")


def main() -> int:
    integrate_calendar()
    update_downloader_fixture()
    update_protocol_tests()
    freeze_batch01_tool()
    rewrite_batch01_tests()
    archive_batch01_workflow()
    update_calendar_regression_workflow()
    create_calendar_tests()
    print(
        "Prepared atomic Batch 01 integration: 3 PASS dates; 2 BLOCKED dates preserved; "
        f"run={RUN_ID}; artifact={ARTIFACT_ID}; sha256={ARTIFACT_SHA256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

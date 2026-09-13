from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta

try:
    from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    from dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE


# Qualification envelope only. This is deliberately broader than the minimum
# five-year requirement and is NOT yet the frozen research/backtest window.
COVERAGE_START = date(2018, 5, 1)
COVERAGE_END = date(2026, 8, 14)
COVERAGE_CONTRACT = "DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1"

# A candidate date can be cleared in one of two ways:
# 1) SPECIAL_SESSION_EVIDENCE proves exact whole-hour closures; or
# 2) NO_SPECIAL_CHANGE_EVIDENCE proves that regular USATECH hours apply.
# Empty by design until a precise primary source is versioned.
NO_SPECIAL_CHANGE_EVIDENCE: dict[date, dict] = {}

# Known unscheduled U.S. equity-session disruptions inside the envelope.
UNSCHEDULED_SPECIAL_DATES = {
    date(2018, 12, 5): "NATIONAL_DAY_OF_MOURNING_GHWB_2018",
    date(2025, 1, 9): "NATIONAL_DAY_OF_MOURNING_CARTER_2025",
}


@dataclass(frozen=True, order=True)
class CandidateSpecialDate:
    day: date
    reason: str


def _nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (occurrence - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last = next_month - timedelta(days=1)
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def _observed_us_date(actual: date) -> date:
    # Saturday -> preceding Friday, Sunday -> following Monday.
    if actual.weekday() == 5:
        return actual - timedelta(days=1)
    if actual.weekday() == 6:
        return actual + timedelta(days=1)
    return actual


def _previous_business_day(day: date) -> date:
    candidate = day - timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate -= timedelta(days=1)
    return candidate


def _easter_sunday(year: int) -> date:
    """Gregorian Easter Sunday (Meeus/Jones/Butcher algorithm)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def candidate_special_dates(
    start: date = COVERAGE_START,
    end: date = COVERAGE_END,
) -> list[CandidateSpecialDate]:
    """Enumerate dates that require explicit session evidence before acquisition.

    This is intentionally conservative. It includes standard U.S. equity-index
    holidays plus adjacent sessions that commonly carry early closes. Being a
    candidate does NOT mean a closure is assumed. It means regular hours may not
    be trusted until exact Dukascopy/exchange evidence proves special or normal
    behavior for USATECH.
    """
    candidates: dict[date, set[str]] = {}

    def add(day: date, reason: str) -> None:
        if start <= day <= end and day.weekday() < 5:
            candidates.setdefault(day, set()).add(reason)

    for year in range(start.year, end.year + 1):
        new_year = _observed_us_date(date(year, 1, 1))
        add(new_year, "NEW_YEARS_OBSERVED")

        mlk = _nth_weekday(year, 1, 0, 3)
        add(mlk, "MARTIN_LUTHER_KING_DAY")

        presidents = _nth_weekday(year, 2, 0, 3)
        add(presidents, "PRESIDENTS_DAY")

        good_friday = _easter_sunday(year) - timedelta(days=2)
        add(good_friday, "GOOD_FRIDAY")

        memorial = _last_weekday(year, 5, 0)
        add(memorial, "MEMORIAL_DAY")

        if year >= 2022:
            juneteenth = _observed_us_date(date(year, 6, 19))
            add(juneteenth, "JUNETEENTH_OBSERVED")

        independence = _observed_us_date(date(year, 7, 4))
        add(independence, "INDEPENDENCE_DAY_OBSERVED")
        add(_previous_business_day(independence), "INDEPENDENCE_PRE_HOLIDAY_SESSION")

        labor = _nth_weekday(year, 9, 0, 1)
        add(labor, "LABOR_DAY")

        thanksgiving = _nth_weekday(year, 11, 3, 4)
        add(thanksgiving, "THANKSGIVING_DAY")
        add(thanksgiving + timedelta(days=1), "THANKSGIVING_FRIDAY")

        christmas = _observed_us_date(date(year, 12, 25))
        add(christmas, "CHRISTMAS_OBSERVED")
        add(_previous_business_day(christmas), "CHRISTMAS_PRE_HOLIDAY_SESSION")

        # New Year's Eve can have broker-specific or exchange-specific treatment.
        add(date(year, 12, 31), "NEW_YEARS_EVE_CANDIDATE")

    for day, reason in UNSCHEDULED_SPECIAL_DATES.items():
        add(day, reason)

    return [
        CandidateSpecialDate(day, "+".join(sorted(reasons)))
        for day, reasons in sorted(candidates.items())
    ]


def audit_calendar_coverage(
    start: date = COVERAGE_START,
    end: date = COVERAGE_END,
) -> dict:
    candidates = candidate_special_dates(start, end)
    candidate_days = {item.day for item in candidates}
    special_days = {
        day for day in SPECIAL_SESSION_EVIDENCE if start <= day <= end
    }
    no_change_days = {
        day for day in NO_SPECIAL_CHANGE_EVIDENCE if start <= day <= end
    }
    resolved_days = special_days | no_change_days

    unresolved = [
        {"date": item.day.isoformat(), "reason": item.reason}
        for item in candidates
        if item.day not in resolved_days
    ]

    orphan_special = sorted(special_days - candidate_days)
    overlap = sorted(special_days & no_change_days)

    evidence_shape_errors: list[dict] = []
    for day in sorted(special_days):
        record = SPECIAL_SESSION_EVIDENCE[day]
        hours = record.get("fully_closed_hours_utc")
        sources = [value for key, value in record.items() if key.endswith("_source")]
        if not record.get("reason") or not isinstance(hours, frozenset) or not sources:
            evidence_shape_errors.append(
                {"date": day.isoformat(), "reason": "MALFORMED_SPECIAL_EVIDENCE"}
            )
            continue
        if any((not isinstance(hour, int)) or hour < 0 or hour > 23 for hour in hours):
            evidence_shape_errors.append(
                {"date": day.isoformat(), "reason": "INVALID_CLOSED_HOUR"}
            )

    if overlap or evidence_shape_errors:
        verdict = "FAIL"
        reason = "CONTRADICTORY_OR_MALFORMED_CALENDAR_EVIDENCE"
    elif unresolved:
        verdict = "BLOCKED"
        reason = "SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE"
    else:
        verdict = "PASS"
        reason = "ALL_CANDIDATE_SPECIAL_SESSIONS_HAVE_VERSIONED_EVIDENCE"

    return {
        "schema": COVERAGE_CONTRACT,
        "instrument": "USATECHIDXUSD",
        "coverage_start": start.isoformat(),
        "coverage_end": end.isoformat(),
        "execution_window_frozen": False,
        "candidate_dates": len(candidates),
        "special_session_evidence_dates": len(special_days),
        "no_special_change_evidence_dates": len(no_change_days),
        "resolved_candidate_dates": len(candidate_days & resolved_days),
        "unresolved_candidate_dates": len(unresolved),
        "unresolved": unresolved,
        "orphan_special_evidence": [day.isoformat() for day in orphan_special],
        "contradictory_evidence_dates": [day.isoformat() for day in overlap],
        "evidence_shape_errors": evidence_shape_errors,
        "verdict": verdict,
        "reason": reason,
    }


def main() -> int:
    report = audit_calendar_coverage()
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["verdict"] == "PASS":
        return 0
    if report["verdict"] == "FAIL":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

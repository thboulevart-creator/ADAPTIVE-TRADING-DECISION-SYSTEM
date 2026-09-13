from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date, timedelta


EXPECTED_OPEN = "EXPECTED_OPEN"
EXPECTED_CLOSED = "EXPECTED_CLOSED"

# Official Dukascopy instrument schedule source for USATECH.IDX/USD.
# Summer: Sun-Fri 22:00-20:15 GMT; daily break 20:15-22:00.
# Winter: Sun-Fri 23:00-21:15 GMT; daily break 21:15-23:00.
CALENDAR_SOURCE_URL = (
    "https://www.dukascopy.com/europe/english/cfd/range-of-markets/"
)

# Explicit evidence for the January 9, 2025 U.S. National Day of Mourning.
# Dukascopy announced special U.S. market closures for that date. CME, whose
# U.S. equity-index futures schedule is the relevant underlying-session evidence,
# specified an 08:30 CT early close and normal 17:00 CT reopening. In January,
# CT is UTC-6, so this is 14:30 UTC -> 23:00 UTC. At hourly BI5 granularity,
# hour 14 remains EXPECTED_OPEN because 14:00-14:30 is tradable; hours 15-22
# are fully closed; hour 23 is open again.
SPECIAL_SESSION_EVIDENCE = {
    date(2025, 1, 9): {
        "reason": "SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025",
        "fully_closed_hours_utc": frozenset(range(15, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "us-market-closure-on-9th-of-january-2025"
        ),
        "cme_source": (
            "https://www.cmegroup.com/media-room/press-releases/2025/12/30/"
            "cme_group_announcestradinghoursforusnationaldayofmourningtohonor.html"
        ),
    }
}

CALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V2"


@dataclass(frozen=True)
class SlotClassification:
    status: str
    reason: str
    schedule: str


def _last_sunday(year: int, month: int) -> date:
    last_day = date(year, month, monthrange(year, month)[1])
    days_since_sunday = (last_day.weekday() + 1) % 7
    return last_day - timedelta(days=days_since_sunday)


def is_summer_schedule(day: date) -> bool:
    """Return whether Dukascopy's summer schedule applies on this date.

    The public instrument table expresses separate Summer Time / Winter Time
    schedules. We bind the seasonal switch to the European DST convention:
    last Sunday in March through the day before the last Sunday in October.
    """
    summer_start = _last_sunday(day.year, 3)
    winter_start = _last_sunday(day.year, 10)
    return summer_start <= day < winter_start


def classify_slot(day: date, hour: int) -> SlotClassification:
    """Classify one UTC/GMT hourly BI5 bucket before any network request.

    A bucket is EXPECTED_OPEN if any part of that hour intersects a proven
    trading session. Partial close hours therefore remain EXPECTED_OPEN.

    Regular weekly/daily hours are taken from Dukascopy. Explicit special
    sessions are applied only when they are versioned in SPECIAL_SESSION_EVIDENCE;
    no holiday is inferred merely from a date name or an HTTP response.
    """
    if not 0 <= hour <= 23:
        raise ValueError("hour must be between 0 and 23")

    summer = is_summer_schedule(day)
    schedule = "SUMMER" if summer else "WINTER"
    reopen_hour = 22 if summer else 23
    partial_close_hour = 20 if summer else 21
    weekday = day.weekday()  # Monday=0 ... Sunday=6

    if weekday == 5:  # Saturday
        return SlotClassification(
            EXPECTED_CLOSED, "WEEKLY_SATURDAY_CLOSED", schedule
        )

    if weekday == 6:  # Sunday: only the late weekly reopening is tradable.
        if hour >= reopen_hour:
            return SlotClassification(
                EXPECTED_OPEN, "WEEKLY_SUNDAY_REOPEN", schedule
            )
        return SlotClassification(
            EXPECTED_CLOSED, "WEEKLY_PRE_OPEN", schedule
        )

    special = SPECIAL_SESSION_EVIDENCE.get(day)
    if special and hour in special["fully_closed_hours_utc"]:
        return SlotClassification(EXPECTED_CLOSED, special["reason"], schedule)

    if weekday == 4:  # Friday: no late reopening after the weekly close.
        if hour <= partial_close_hour:
            return SlotClassification(
                EXPECTED_OPEN, "REGULAR_SESSION_OR_PARTIAL_CLOSE_HOUR", schedule
            )
        return SlotClassification(
            EXPECTED_CLOSED, "WEEKLY_POST_CLOSE", schedule
        )

    # Monday-Thursday: regular session, daily break, then late reopening.
    if hour <= partial_close_hour or hour >= reopen_hour:
        return SlotClassification(
            EXPECTED_OPEN, "REGULAR_SESSION_OR_PARTIAL_CLOSE_HOUR", schedule
        )

    return SlotClassification(EXPECTED_CLOSED, "DAILY_TRADING_BREAK", schedule)

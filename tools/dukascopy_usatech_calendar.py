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
CALENDAR_CONTRACT = "DUKASCOPY_USATECH_REGULAR_SESSION_V1"


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

    A bucket is EXPECTED_OPEN if any part of that hour intersects the published
    trading session. This deliberately keeps partial close hours (20:00-20:15
    in summer, 21:00-21:15 in winter) as EXPECTED_OPEN.

    This V1 classifier covers the regular weekly session and daily break only.
    Special holidays are intentionally not guessed here; they require explicit
    versioned evidence before being added as EXPECTED_CLOSED exceptions.
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

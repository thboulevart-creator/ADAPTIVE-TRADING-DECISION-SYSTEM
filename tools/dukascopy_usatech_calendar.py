from __future__ import annotations

from dataclasses import dataclass
from datetime import date


EXPECTED_OPEN = "EXPECTED_OPEN"
EXPECTED_CLOSED = "EXPECTED_CLOSED"

# Official Dukascopy instrument schedule source for USATECH.IDX/USD.
# Summer: Sun-Fri 22:00-20:15 GMT; daily break 20:15-22:00.
# Winter: Sun-Fri 23:00-21:15 GMT; daily break 21:15-23:00.
CALENDAR_SOURCE_URL = (
    "https://www.dukascopy.com/europe/english/cfd/range-of-markets/"
)

# Dukascopy explicitly applies the U.S. daylight-saving switch to USATECH.
# Example 2025 announcement: Summer Trading time applies from Sunday 9 March.
DUKASCOPY_US_DST_SOURCE_URL = (
    "https://www.dukascopy.com/europe/english/about/ournews/"
    "daylight-saving-time-2025-in-the-us"
)

# U.S. DST rule since 2007: second Sunday in March through the first Sunday
# in November. The current qualification envelope starts in 2018, so this
# statutory rule covers the entire intended historical range.
US_DST_RULE_SOURCE_URL = (
    "https://www.nist.gov/pml/time-and-frequency-division/popular-links/"
    "daylight-saving-time-dst"
)

# Only date-specific sessions supported by sufficiently precise evidence belong
# here. `fully_closed_hours_utc` contains only whole BI5 hours proven closed.
# A partially tradable hour MUST remain EXPECTED_OPEN.
SPECIAL_SESSION_EVIDENCE = {
    date(2018, 5, 28): {
        "reason": "SPECIAL_MEMORIAL_DAY_2018",
        # Dukascopy: USATECH closes 17:00 GMT and reopens 22:00 GMT.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "memorial-day-holiday-monday-28-may"
        ),
    },
    date(2018, 7, 3): {
        "reason": "SPECIAL_INDEPENDENCE_EVE_2018",
        # Dukascopy: closes 17:15 GMT and reopens 22:00 GMT. Hour 17 remains
        # open because its first 15 minutes are tradable.
        "fully_closed_hours_utc": frozenset(range(18, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "us-independence-day-on-wednesday-4th-july"
        ),
    },
    date(2018, 7, 4): {
        "reason": "SPECIAL_INDEPENDENCE_DAY_2018",
        # Dukascopy: closes 17:00 GMT and reopens 22:00 GMT.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "us-independence-day-on-wednesday-4th-july"
        ),
    },
    date(2018, 9, 3): {
        "reason": "SPECIAL_LABOR_DAY_2018",
        # Dukascopy: USATECH stops at 17:00 GMT. CME equity-index trading
        # resumes at 17:00 CT = 22:00 UTC during U.S. DST, so the fully closed
        # hourly BI5 buckets are 17-21 UTC.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "us-labor-day-holiday-dbl201120/"
        ),
        "cme_source": (
            "https://www.cmegroup.com/tools-information/holiday-calendar/files/"
            "2018-labor-day-advisory.pdf"
        ),
    },
    date(2018, 12, 5): {
        "reason": "SPECIAL_US_NATIONAL_DAY_OF_MOURNING_GHWB_2018",
        # CME U.S.-based equity products close after overnight trading at
        # 08:30 CT = 14:30 UTC and reopen at 17:00 CT = 23:00 UTC. Hour 14
        # remains partially tradable; only 15-22 UTC are fully closed buckets.
        "fully_closed_hours_utc": frozenset(range(15, 23)),
        "dukascopy_context_source": (
            "https://www.dukascopy.com/swiss/english/marketwatch/market-news/"
            "Trading-Ideas/GBP-USD/109292/"
        ),
        "cme_source": (
            "https://www.cmegroup.com/notices/ser/2018/12/SER-8289.pdf"
        ),
    },
    date(2020, 2, 17): {
        "reason": "SPECIAL_PRESIDENTS_DAY_2020",
        # Dukascopy: USATECH closes 18:00 GMT and reopens 23:00 GMT.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/pt/about/ournews/"
            "market-closures-on-president-s-day-dbl201738/"
        ),
    },
    date(2025, 1, 9): {
        "reason": "SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025",
        # CME U.S. equities close at 08:30 CT = 14:30 UTC and reopen at the
        # regular 17:00 CT = 23:00 UTC. Hour 14 remains partially tradable.
        "fully_closed_hours_utc": frozenset(range(15, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "us-market-closure-on-9th-of-january-2025"
        ),
        "cme_source": (
            "https://www.cmegroup.com/trading-hours/files/"
            "day-of-mourning-january-9-2024.pdf"
        ),
    },
}

CALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"


@dataclass(frozen=True)
class SlotClassification:
    status: str
    reason: str
    schedule: str


def _nth_sunday(year: int, month: int, occurrence: int) -> date:
    """Return the Nth Sunday (1-based) of a month."""
    if occurrence < 1:
        raise ValueError("occurrence must be >= 1")
    first = date(year, month, 1)
    days_to_sunday = (6 - first.weekday()) % 7
    day_number = 1 + days_to_sunday + 7 * (occurrence - 1)
    return date(year, month, day_number)


def us_dst_bounds(year: int) -> tuple[date, date]:
    """Return U.S. DST start/end dates for the qualification-era rule."""
    return _nth_sunday(year, 3, 2), _nth_sunday(year, 11, 1)


def is_summer_schedule(day: date) -> bool:
    """Return whether Dukascopy's USATECH summer schedule applies.

    USATECH follows the U.S. DST transition, not the European transition.
    For the 2018+ qualification envelope, U.S. DST starts on the second
    Sunday in March and ends on the first Sunday in November.
    """
    summer_start, winter_start = us_dst_bounds(day.year)
    return summer_start <= day < winter_start


def classify_slot(day: date, hour: int) -> SlotClassification:
    """Classify one UTC/GMT hourly BI5 bucket before any network request.

    A bucket is EXPECTED_OPEN if any part of that hour intersects a proven
    trading session. Partial close hours therefore remain EXPECTED_OPEN.

    Regular weekly/daily hours are taken from Dukascopy. Explicit special
    sessions are applied only when versioned in SPECIAL_SESSION_EVIDENCE;
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

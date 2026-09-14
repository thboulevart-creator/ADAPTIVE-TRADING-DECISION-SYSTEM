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
    date(2018, 11, 22): {
        "reason": "SPECIAL_THANKSGIVING_DAY_2018",
        # Dukascopy explicitly announced special CFD market closures for both
        # Thanksgiving Thursday and Friday. The archived CME Globex 2018
        # Thanksgiving schedule shows Equity Products HALT at 12:00 CT and
        # reopening at 17:00 CT. In winter, that is 18:00-23:00 UTC, so the
        # fully closed hourly BI5 buckets are 18-22 UTC.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/french/about/ournews/"
            "thanksgiving-holiday-in-us"
        ),
        # CME's official archived 2018 holiday page confirms a 2018 Globex
        # holiday calendar existed. The exact historical table is no longer
        # served there, so the preserved schedule image is transparently
        # recorded as a mirror rather than mislabelled as a primary-host URL.
        "cme_archive_source": (
            "https://www.cmegroup.com/es/tools-information/us-holidays.html"
        ),
        "cme_schedule_mirror_source": (
            "https://files.constantcontact.com/3dc00ef7001/"
            "d17def76-24ea-44af-a583-f6df03e741da.png"
        ),
    },
    date(2018, 11, 23): {
        "reason": "SPECIAL_THANKSGIVING_FRIDAY_2018",
        # The same CME schedule shows Equity Products early close at 12:15 CT
        # = 18:15 UTC on Friday. Hour 18 remains partially tradable. Hours
        # 19-21 UTC are additional whole-hour holiday closures; 22-23 UTC are
        # already closed by the regular Friday weekly-close rule.
        "fully_closed_hours_utc": frozenset(range(19, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/french/about/ournews/"
            "thanksgiving-holiday-in-us"
        ),
        "cme_archive_source": (
            "https://www.cmegroup.com/es/tools-information/us-holidays.html"
        ),
        "cme_schedule_mirror_source": (
            "https://files.constantcontact.com/3dc00ef7001/"
            "d17def76-24ea-44af-a583-f6df03e741da.png"
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
    date(2018, 12, 24): {
        "reason": "SPECIAL_CHRISTMAS_EVE_2018",
        # Dukascopy announced detailed Christmas/New-Year CFD closures. The
        # preserved CME Group 2018 Christmas table shows Equity Indices closing
        # at 12:15 CT = 18:15 UTC on Monday Dec 24 and remaining closed for
        # Christmas Day. Hour 18 is therefore partially tradable; hours 19-23
        # on Dec 24 are fully closed.
        "fully_closed_hours_utc": frozenset(range(19, 24)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "market-closures-on-christmas-and-new-year-/"
        ),
        "cme_archive_source": (
            "https://www.cmegroup.com/es/tools-information/us-holidays.html"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "wp-content/uploads/2018/12/CME-Group-2018-300x182.png"
        ),
    },
    date(2018, 12, 25): {
        "reason": "SPECIAL_CHRISTMAS_DAY_2018",
        # The preserved CME Globex Christmas schedule shows Equity Products
        # closed for Christmas Day and reopening at the regular 17:00 CT =
        # 23:00 UTC evening session for the Dec 26 trade date. Therefore every
        # complete UTC hour 00-22 is closed; 23:00 UTC is tradable again.
        "fully_closed_hours_utc": frozenset(range(0, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "market-closures-on-christmas-and-new-year-/"
        ),
        "cme_archive_source": (
            "https://www.cmegroup.com/es/tools-information/us-holidays.html"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "wp-content/uploads/2018/12/CME-Group-2018-300x182.png"
        ),
    },
    date(2018, 12, 31): {
        "reason": "SPECIAL_NEW_YEARS_EVE_2018",
        # CME's preserved New-Year schedule shows Equity Products taking their
        # regular 16:00 CT = 22:00 UTC close on Dec 31, followed by Globex
        # closed for Jan 1. Dukascopy's regular winter session would normally
        # reopen at 23:00 UTC after its 21:15-23:00 daily break; that reopening
        # is suppressed by the holiday. Thus 21h remains partially tradable,
        # 22h is already the regular daily break, and only 23h is an additional
        # whole-hour special closure on the Dec 31 calendar date.
        "fully_closed_hours_utc": frozenset({23}),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "market-closures-on-christmas-and-new-year-/"
        ),
        "cme_clearing_source": (
            "https://www.cmegroup.com/tools-information/holiday-calendar/files/"
            "2019-new-years-advisory.pdf"
        ),
        "cme_schedule_mirror_source": (
            "https://files.constantcontact.com/3dc00ef7001/"
            "30353065-d2d3-4ee6-870d-0a9a6b6acfaf.gif"
        ),
    },
    date(2019, 1, 1): {
        "reason": "SPECIAL_NEW_YEARS_DAY_2019",
        # This is the second calendar day of the exact Dec 31 2018-Jan 1 2019
        # holiday window already evidenced above: CME Globex remains closed on
        # Jan 1 and reopens at 17:00 CT = 23:00 UTC. Therefore 00-22 UTC are
        # fully closed and 23:00 UTC is tradable again.
        "fully_closed_hours_utc": frozenset(range(0, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/english/about/ournews/"
            "market-closures-on-christmas-and-new-year-/"
        ),
        "cme_clearing_source": (
            "https://www.cmegroup.com/tools-information/holiday-calendar/files/"
            "2019-new-years-advisory.pdf"
        ),
        "cme_schedule_mirror_source": (
            "https://files.constantcontact.com/3dc00ef7001/"
            "30353065-d2d3-4ee6-870d-0a9a6b6acfaf.gif"
        ),
    },
    date(2019, 1, 21): {
        "reason": "SPECIAL_MLK_DAY_2019",
        # Dukascopy announced special CFD trading breaks for this exact date.
        # The preserved CME Globex Control Center summary records a noon CST
        # halt followed by normal reopening; in winter this is 18:00-23:00 UTC.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "market-closures-on-martin-luther-king-jr-day"
        ),
        "cme_schedule_mirror_source": (
            "https://www.ampfutures.com/news/holiday-trading-schedule-mlk-2019"
        ),
    },
    date(2019, 2, 18): {
        "reason": "SPECIAL_PRESIDENTS_DAY_2019",
        # Dukascopy announced special CFD trading breaks for this exact date.
        # The preserved CME Globex Control Center summary records a noon CST
        # halt followed by normal reopening; in winter this is 18:00-23:00 UTC.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "market-closures-on-president-s-day-dbl201333"
        ),
        "cme_schedule_mirror_source": (
            "https://www.ampfutures.com/news/"
            "holiday-trading-schedule-us-presidents-day-2019"
        ),
    },
    date(2019, 4, 19): {
        "reason": "SPECIAL_GOOD_FRIDAY_2019",
        # Dukascopy announced Easter-weekend CFD closures for this exact
        # period. The preserved CME Globex schedule states that all Globex
        # markets were closed for the entire Good Friday session.
        "fully_closed_hours_utc": frozenset(range(0, 24)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/deutsch/about/ournews/"
            "easter-weekend-market-closures-dbl201441/"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "good-friday-2019-holiday-schedule-cme-globex-ice-exchange/"
        ),
    },
    date(2019, 5, 27): {
        "reason": "SPECIAL_MEMORIAL_DAY_2019",
        # Dukascopy identifies Memorial Day market closures on this exact date.
        # The preserved CME Globex Control Center summary records a noon Chicago
        # halt followed by normal reopening. Chicago is on CDT here, so the
        # fully closed hourly buckets are 17:00-22:00 UTC.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "bank-holidays-in-uk-and-us-on-monday-27-may"
        ),
        "cme_schedule_mirror_source": (
            "https://www.ampfutures.com/news/"
            "holiday-trading-schedule-us-memorial-day-2019"
        ),
    },
    date(2019, 7, 4): {
        "reason": "SPECIAL_INDEPENDENCE_DAY_2019",
        # Dukascopy announced special CFD trading breaks for 4 July 2019.
        # The preserved 2019 CME-derived ES/NQ/YM schedule shows a 12:00 CT
        # halt. Chicago is on CDT, so the full closure is 17:00-22:00 UTC.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/english/about/ournews/"
            "market-closures-on-independence-day/"
        ),
        "cme_schedule_mirror_source": (
            "https://www.paragonglobalmarkets.com/wp-content/uploads/2019/06/"
            "PGM_Independence-Day-Holiday-Schedule_2019.pdf"
        ),
        "cme_clearing_source": (
            "https://www.cmegroup.com/tools-information/holiday-calendar/files/"
            "2019-4th-of-july-advisory.pdf"
        ),
    },
    date(2019, 9, 2): {
        "reason": "SPECIAL_LABOR_DAY_2019",
        # Dukascopy states that several markets are subject to early or total
        # closure on Monday 2 September 2019. The preserved CME Globex Equity
        # schedule halts at 12:00 CT and resumes at 17:00 CT; in CDT that is
        # a fully closed 17:00-22:00 UTC window.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/pl/about/ournews/"
            "market-closures-on-us-labour-day/"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "labor-day-2019-holiday-schedule-cme-globex-ice-exchange/"
        ),
    },
    date(2019, 11, 28): {
        "reason": "SPECIAL_THANKSGIVING_DAY_2019",
        # Dukascopy explicitly points to special closures on both Nov 28 and
        # Nov 29. The preserved CME Globex Control Center summary gives a noon
        # CST halt on Thursday followed by normal reopening: 18:00-23:00 UTC.
        "fully_closed_hours_utc": frozenset(range(18, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/chinese/about/ournews/"
            "thanksgiving-day-in-the-us/"
        ),
        "cme_schedule_mirror_source": (
            "https://www.ampfutures.com/news/"
            "holiday-trading-schedule-thanksgiving-2019"
        ),
    },
    date(2019, 11, 29): {
        "reason": "SPECIAL_THANKSGIVING_FRIDAY_2019",
        # CME records a 12:15 CST = 18:15 UTC early close. Hour 18 remains
        # partially tradable; 19-21 UTC are whole-hour special closures, while
        # 22-23 UTC are already covered by Dukascopy's regular Friday close.
        "fully_closed_hours_utc": frozenset(range(19, 22)),
        "dukascopy_source": (
            "https://www.dukascopy.com/europe/chinese/about/ournews/"
            "thanksgiving-day-in-the-us/"
        ),
        "cme_schedule_mirror_source": (
            "https://www.ampfutures.com/news/"
            "holiday-trading-schedule-thanksgiving-2019"
        ),
    },
    date(2019, 12, 24): {
        "reason": "SPECIAL_CHRISTMAS_EVE_2019",
        # Dukascopy announced detailed CFD closures for the 2019 Christmas/
        # New-Year period. The preserved CME Globex schedule gives an Equity
        # early close at 12:15 CT = 18:15 UTC. Hour 18 remains tradable in
        # part; fully closed whole-hour buckets are 19-23 UTC.
        "fully_closed_hours_utc": frozenset(range(19, 24)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/arabic/about/ournews/"
            "market-closures-on-christmas-and-new-year-dbl201708"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "christmas-2019-holiday-schedule-cme-globex-ice-exchange/"
        ),
    },
    date(2019, 12, 25): {
        "reason": "SPECIAL_CHRISTMAS_DAY_2019",
        # The same exact 2019 CME Globex schedule shows Equity Products closed
        # for Christmas Day and reopening at 17:00 CT = 23:00 UTC. Therefore
        # 00-22 UTC are fully closed and the 23:00 UTC bucket is tradable.
        "fully_closed_hours_utc": frozenset(range(0, 23)),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/arabic/about/ournews/"
            "market-closures-on-christmas-and-new-year-dbl201708"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "christmas-2019-holiday-schedule-cme-globex-ice-exchange/"
        ),
    },
    date(2019, 12, 31): {
        "reason": "SPECIAL_NEW_YEARS_EVE_2019",
        # The exact 2019/2020 CME Globex schedule shows a normal 16:00 CT =
        # 22:00 UTC Dec 31 close followed by a Jan 1 closure. Dukascopy's
        # winter schedule would normally reopen at 23:00 UTC; that reopening
        # is suppressed. Hour 21 remains partially tradable, 22 is the regular
        # break, and only 23 is an additional whole-hour special closure.
        "fully_closed_hours_utc": frozenset({23}),
        "dukascopy_source": (
            "https://www.dukascopy.com/swiss/arabic/about/ournews/"
            "market-closures-on-christmas-and-new-year-dbl201708"
        ),
        "cme_schedule_mirror_source": (
            "https://www.cannontrading.com/tools/support-resistance-levels/"
            "new-years-2020-holiday-schedule-cme-globex-ice-exchange/"
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
    date(2021, 9, 6): {
        "reason": "SPECIAL_LABOR_DAY_2021",
        # Broker-native Trading Breaks history: USATECH.IDX/USD break starts
        # 17:00 UTC, final closed minute is 21:59 UTC, reopening at 22:00 UTC.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1630886400000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34866699952"
        ),
    },
    date(2021, 11, 25): {
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
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34885895206"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    },
    date(2021, 11, 26): {
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
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34885895206"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    },
    date(2021, 12, 23): {
        "reason": "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2021",
        # Broker-native record 31532 starts at 21:14 UTC and remains closed
        # through the Christmas/weekend interval. Hour 21 remains partially
        # tradable; 22-23 are fully closed on this exact target date.
        "fully_closed_hours_utc": frozenset({22, 23}),
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1640217600000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34885895206"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch01_qualification.md"
        ),
    },
    date(2022, 1, 17): {
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
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34888022168"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch02_qualification.md"
        ),
    },
    date(2022, 2, 21): {
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
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34888022168"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch02_qualification.md"
        ),
    },
    date(2022, 5, 30): {
        "reason": "SPECIAL_MEMORIAL_DAY_2022",
        # Broker-native Trading Breaks record 37019: 16:59-21:59 UTC.
        # Calibrated reopen is 22:00 UTC; hour 16 is partially tradable, so
        # only whole UTC hours 17-21 are proven fully closed.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "broker_record_id": "37019",
        "broker_reason": "Memorial Day",
        "artifact_id": 10367930592,
        "artifact_sha256": "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41",
        "probe_commit": "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1653868800000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34892253133"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch03_qualification.md"
        ),
    },
    date(2022, 6, 20): {
        "reason": "SPECIAL_JUNETEENTH_OBSERVED_2022",
        # Broker-native Trading Breaks record 38945: 16:59-21:59 UTC.
        # Calibrated reopen is 22:00 UTC; hour 16 is partially tradable, so
        # only whole UTC hours 17-21 are proven fully closed.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "broker_record_id": "38945",
        "broker_reason": "Juneteenth Holiday",
        "artifact_id": 10367930592,
        "artifact_sha256": "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41",
        "probe_commit": "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1655683200000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34892253133"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch03_qualification.md"
        ),
    },
    date(2022, 7, 4): {
        "reason": "SPECIAL_INDEPENDENCE_DAY_2022",
        # Broker-native Trading Breaks record 41225: 16:59-21:59 UTC.
        # Calibrated reopen is 22:00 UTC; hour 16 is partially tradable, so
        # only whole UTC hours 17-21 are proven fully closed.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "broker_record_id": "41225",
        "broker_reason": "Independence Day",
        "artifact_id": 10367930592,
        "artifact_sha256": "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41",
        "probe_commit": "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1656892800000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34892253133"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch03_qualification.md"
        ),
    },
    date(2022, 9, 5): {
        "reason": "SPECIAL_LABOR_DAY_2022",
        # Broker-native Trading Breaks record 42569: 16:59-21:59 UTC.
        # Calibrated reopen is 22:00 UTC; hour 16 is partially tradable, so
        # only whole UTC hours 17-21 are proven fully closed.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "broker_record_id": "42569",
        "broker_reason": "Labor Day",
        "artifact_id": 10367930592,
        "artifact_sha256": "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41",
        "probe_commit": "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date=1662336000000"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/34892253133"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch03_qualification.md"
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

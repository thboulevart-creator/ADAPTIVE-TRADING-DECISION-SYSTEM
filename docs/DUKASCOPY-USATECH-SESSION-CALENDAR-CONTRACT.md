# DUKASCOPY USATECH SESSION CALENDAR — QUALIFICATION CONTRACT

## Status

**Current qualification verdict: BLOCKED until the executable coverage audit returns PASS.**

This document defines the calendar/session contract required before any massive
multi-year Dukascopy BI5 acquisition for `USATECHIDXUSD`.

The qualification envelope is currently:

- start: `2018-05-01`
- end: `2026-08-14`
- purpose: calendar qualification envelope only
- frozen research/backtest window: **NO**

The final >=5-year research window MUST NOT be frozen merely because this broader
calendar envelope exists.

## 1. Objective

Prevent three invalid acquisition behaviours:

1. requesting BI5 files during proven market closures;
2. treating HTTP/transport failures as evidence that the market was closed;
3. silently assuming normal hours on a holiday or exceptional session whose exact
   instrument schedule has not been proven.

A calendar error can create false missing-data defects, waste thousands of network
calls, or silently remove real ticks. Therefore calendar qualification is a
pre-acquisition gate, not post-hoc cleanup.

## 2. Allowed verdicts

Only:

- `PASS`
- `FAIL`
- `BLOCKED`

`BLOCKED` MUST NOT be converted into `PASS` because an HTTP response is empty,
returns 503, times out, or because no BI5 file was downloaded.

## 3. Source hierarchy for session evidence

For `USATECHIDXUSD`, evidence is ranked as follows:

1. exact Dukascopy instrument schedule / Trading Breaks Calendar;
2. exact Dukascopy holiday notice plus primary underlying exchange/session evidence
   (for example CME equity-index trading hours) when Dukascopy's public notice does
   not expose the minute-level session boundary;
3. reproducible BI5 observations only as corroboration.

BI5 absence, `EMPTY_PAYLOAD`, `HTTP_503`, or `TRANSPORT_ERROR` alone can NEVER prove
`EXPECTED_CLOSED`.

## 4. Regular session contract

Official Dukascopy `USATECH.IDX/USD` regular schedule:

- Summer: Sunday-Friday `22:00-20:15 GMT`; daily break `20:15-22:00 GMT`.
- Winter: Sunday-Friday `23:00-21:15 GMT`; daily break `21:15-23:00 GMT`.

At hourly BI5 granularity, a bucket is `EXPECTED_OPEN` if **any tradable sub-interval**
exists inside that hour. Therefore the partial close hour remains open:

- summer `20h` bucket: open; `21h`: closed; `22h`: reopened;
- winter `21h` bucket: open; `22h`: closed; `23h`: reopened.

Saturday is fully closed. Sunday is closed until the seasonal weekly reopening.
Friday does not reopen after the weekly close.

Primary source:
`https://www.dukascopy.com/europe/english/cfd/range-of-markets/`

## 5. U.S. daylight-saving rule — critical correction

`USATECH` follows the U.S. daylight-saving transition, not the European transition.
For the qualification envelope (2018+), U.S. DST runs from the second Sunday in
March to the first Sunday in November.

This means the previous Europe-based implementation was architecturally wrong for
several weeks each year and has been replaced by a U.S.-DST rule in calendar V3.

Sources:

- Dukascopy US DST notice example:
  `https://www.dukascopy.com/europe/english/about/ournews/daylight-saving-time-2025-in-the-us`
- NIST DST rule:
  `https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst`

## 6. Special-session rule

A holiday name does not imply a specific closure.

Every potentially special date inside the qualification envelope must resolve to
one of two versioned evidence states:

### A. `SPECIAL_SESSION_EVIDENCE`

Exact whole BI5 hours proven closed for `USATECH` are stored explicitly.
Partial hours remain `EXPECTED_OPEN`.

### B. `NO_SPECIAL_CHANGE_EVIDENCE`

A primary source proves that the regular USATECH schedule remains applicable.

If neither A nor B exists, the date is unresolved and the coverage verdict is
`BLOCKED`.

## 7. Currently versioned special sessions

The executable registry currently contains exact evidence for:

- `2018-05-28` — Memorial Day: closed whole UTC hours `17-21`, reopen `22`;
- `2018-07-03` — Independence Eve: close `17:15`, therefore whole closed hours
  `18-21`, reopen `22`;
- `2018-07-04` — Independence Day: closed whole hours `17-21`, reopen `22`;
- `2020-02-17` — Presidents Day: closed whole hours `18-22`, reopen `23`;
- `2025-01-09` — U.S. National Day of Mourning: close `14:30 UTC`, therefore
  whole closed hours `15-22`, reopen `23`.

These entries do not imply that other years share the same exact boundaries.
Historical Dukascopy holiday schedules are not assumed invariant across years.

## 8. Candidate special-session coverage

`tools/dukascopy_usatech_calendar_coverage.py` generates conservative dates requiring
explicit proof, including:

- New Year / observed New Year;
- Martin Luther King Day;
- Presidents Day;
- Good Friday;
- Memorial Day;
- Juneteenth (from 2022);
- Independence Day and the preceding business session;
- Labor Day;
- Thanksgiving and Friday after Thanksgiving;
- Christmas and the preceding business session;
- New Year's Eve candidate;
- unscheduled national days of mourning known inside the envelope.

Candidate means **proof required**, not `EXPECTED_CLOSED`.

## 9. Fail-closed acquisition gate

`tools/download_dukascopy_tick_corpus.py` V1.4 executes the coverage audit before
network access.

Default behaviour:

- coverage `PASS` -> session classification and acquisition may proceed;
- coverage `FAIL` -> acquisition aborts with `FAIL`, zero network calls;
- coverage `BLOCKED` -> acquisition aborts with `BLOCKED`, zero network calls.

A controlled `--calendar-qualification-probe` mode exists only to gather evidence on
an unresolved date. Probe mode can perform acquisition, but it can NEVER upgrade the
run to `PASS` while the calendar coverage itself remains incomplete.

This prevents evidence laundering from a successful download into a false calendar
qualification.

## 10. Adversarial invariants

The tests must preserve all of the following:

- weekend -> zero network calls;
- proven daily break -> zero network calls;
- special full-hour closure -> zero network calls;
- partial hour -> remains `EXPECTED_OPEN`;
- U.S./Europe DST mismatch weeks -> U.S. schedule wins;
- unresolved holiday candidate -> `BLOCKED` before network;
- qualification probe -> may inspect but cannot return calendar `PASS`;
- file present inside `EXPECTED_CLOSED` -> `FAIL`, not silently accepted;
- `503`, timeout, transport error, empty payload -> never interpreted as closure.

## 11. Executable artifacts

- calendar: `tools/dukascopy_usatech_calendar.py`
- coverage audit: `tools/dukascopy_usatech_calendar_coverage.py`
- downloader: `tools/download_dukascopy_tick_corpus.py`
- calendar tests: `tests/test_dukascopy_usatech_calendar.py`
- coverage tests: `tests/test_dukascopy_usatech_calendar_coverage.py`
- downloader gate tests: `tests/test_dukascopy_downloader_calendar_coverage_gate.py`

## 12. Gate to massive acquisition

Massive multi-year acquisition is authorized only when all of the following are
true:

1. regular schedule tests PASS;
2. U.S. DST boundary tests PASS;
3. special-session evidence has no malformed or contradictory entries;
4. the coverage audit has zero unresolved candidate dates;
5. downloader pre-network coverage-gate tests PASS;
6. coverage verdict is `PASS` for the exact future frozen acquisition window.

Until then, multi-year acquisition remains **BLOCKED**.

Only after this gate passes may the exact >=5-year acquisition window be frozen and
the native BI5 corpus downloaded.

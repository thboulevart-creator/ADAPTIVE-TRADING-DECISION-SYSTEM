# SESSION BACKUP — 2026-09-13 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Evidence-state HEAD before this checkpoint write: `e9b8aceba1e5690ea1ff9d71325afac1f3a769cd`
- HEAD message: `test remaining 2018 Christmas and New Year session closures`
- Active objective: qualify the complete Dukascopy USATECH special-session calendar before massive native `.bi5` acquisition.
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`.
- Coverage envelope: `2018-05-01` through `2026-08-14`.
- Execution/backtest window: NOT frozen yet.

## Governing upstream state preserved

- B09 historical qualification remains locked PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- Actual 3.1.2 execution remains BLOCKED until a verified >=5-year native-tick execution corpus and realistic execution-cost environment are available.
- Do not rerun locked B02-B09 merely to reconstruct history.

## Current calendar/coverage contracts

- `tools/dukascopy_usatech_calendar.py`
  - calendar contract: `DUKASCOPY_USATECH_SESSION_CALENDAR_V3`
  - current blob SHA at evidence-state HEAD: `2b5a28c5d1eadbf651e784dbfcf5414f12ff7b8f`
- `tools/dukascopy_usatech_calendar_coverage.py`
  - coverage contract: `DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1`
  - current blob SHA: `dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`
- `tests/test_dukascopy_usatech_calendar.py`
  - current blob SHA: `826e6ece5d558d79b15642c91ac3b7a62b1136b5`
  - 22 calendar tests are versioned.
  - Important evidence discipline: do NOT claim `22 passed` unless a current run is explicitly observed. The latest user-provided test run before the final 2018 additions was `17 passed`; the latest coverage execution is newer than that test run.

## Latest observed coverage execution

User supplied the following current execution result after the 2018 evidence additions:

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **12**
- `special_session_evidence_dates`: **12**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **99**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

This is a clean BLOCKED, not a FAIL.

## Resolved evidence dates

### 2018 — all candidate dates inside the envelope are now resolved

1. `2018-05-28` — Memorial Day
2. `2018-07-03` — Independence pre-holiday session
3. `2018-07-04` — Independence Day
4. `2018-09-03` — Labor Day
5. `2018-11-22` — Thanksgiving Day
6. `2018-11-23` — Thanksgiving Friday
7. `2018-12-05` — George H. W. Bush National Day of Mourning
8. `2018-12-24` — Christmas Eve
9. `2018-12-25` — Christmas Day
10. `2018-12-31` — New Year's Eve

### Other already-resolved dates

11. `2020-02-17` — Presidents Day
12. `2025-01-09` — U.S. National Day of Mourning for Jimmy Carter

## 2018 exact whole-hour classification now versioned

- Memorial Day 2018: fully closed UTC hours `17-21`; reopen `22`.
- Independence Eve 2018: hour `17` partial/open; fully closed `18-21`; reopen `22`.
- Independence Day 2018: fully closed `17-21`; reopen `22`.
- Labor Day 2018: fully closed `17-21`; reopen `22`.
- Thanksgiving Day 2018: fully closed `18-22`; reopen `23`.
- Thanksgiving Friday 2018: hour `18` partial/open; special fully closed `19-21`; `22-23` already closed by regular Friday weekly-close rule.
- GHWB mourning 2018: hour `14` partial/open; fully closed `15-22`; reopen `23`.
- Christmas Eve 2018: hour `18` partial/open; fully closed `19-23`.
- Christmas Day 2018: fully closed `00-22`; reopen `23`.
- New Year's Eve 2018: hour `21` partial/open; `22` regular daily break; holiday suppresses normal `23` reopening, so `23` is the additional special whole-hour closure.

## Evidence provenance rule used for late-2018 recovery

The accepted pattern remains explicit and auditable:

- Dukascopy source establishes that the broker announced a special closure/event for the relevant period/date.
- CME/equity-index evidence supplies precise session timing when Dukascopy's old page no longer exposes the detailed table text.
- Where the exact historical CME table is no longer directly served on a primary CME URL, preserved schedule images are stored only as transparently labelled mirror sources (`cme_schedule_mirror_source`) plus an official CME archive/context source. Do not silently relabel mirror evidence as primary-host evidence.
- Partial hours remain EXPECTED_OPEN. Only complete UTC hourly BI5 buckets proven closed enter `fully_closed_hours_utc`.
- Absence of HTTP/BI5 data is never itself evidence of market closure.

## Historical Dukascopy widget route — CLOSED / DO NOT REPEAT

A large part of this session tested whether Dukascopy's Trading Breaks widget could recover historical broker-specific hours automatically.

What happened:

1. Direct headless navigation to `freeserv.dukascopy.com` returned explicit HTTP 403.
2. A Chrome DevTools Protocol path through the official Dukascopy page was built.
3. Chrome initially rejected the local CDP WebSocket Origin with 403; this was corrected with an exact `--remote-allow-origins=http://localhost` contract.
4. A false PASS was detected: the probe requested `2025-01-09` but actually read a stale/current frame showing `USATECH.IDX/USD` Labor Day `07-Sep-26`. That PASS was explicitly invalidated.
5. The probe was hardened so PASS requires the exact historical frame: `path=trading_breaks/index`, `currentDate=false`, exact requested `date=<epoch_ms>`, no stale-frame fallback, and date-relevant USATECH evidence.
6. Final strict witness for `2025-01-09` reached the correct frame URL:
   `https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index&...&currentDate=false&...&date=1736424000000`
   but returned a tiny empty DOM (`dom_length=333`, `visible_text_length=0`, `table_row_count=0`, no matching rows).
7. Repeated strict execution remained BLOCKED.

Conclusion: **historical Trading Breaks widget recovery is BLOCKED and is no longer the chosen qualification route. Do not spend another session rebuilding or retrying this path unless new external evidence materially changes the situation.**

## Important methodological invariants

- Verdicts only PASS / FAIL / BLOCKED.
- Never promote BLOCKED or missing evidence to PASS.
- Never infer a special closure only from a holiday name.
- Never infer closure from HTTP 404/403/503 or missing BI5 data.
- Never extrapolate one year's holiday hours to another without date-specific evidence.
- Use U.S. DST rules for USATECH since the instrument follows the U.S. DST switch.
- Partial close hour remains EXPECTED_OPEN at hourly BI5 granularity.
- Massive acquisition remains gated until calendar coverage reaches zero unresolved dates.
- The final multi-year acquisition must use native Dukascopy `.bi5` real ticks; no OHLC M1 substitution, interpolation, synthetic ticks, or copied substitutes.
- Backtest remains >=5 years, realistic costs/spread, OOS fixed before results, real-tick methodology.

## Current unresolved frontier

2018 is complete. The first unresolved date is now `2019-01-01`.

The 2019 unresolved candidate set is:

- `2019-01-01` — NEW_YEARS_OBSERVED
- `2019-01-21` — MARTIN_LUTHER_KING_DAY
- `2019-02-18` — PRESIDENTS_DAY
- `2019-04-19` — GOOD_FRIDAY
- `2019-05-27` — MEMORIAL_DAY
- `2019-07-03` — INDEPENDENCE_PRE_HOLIDAY_SESSION
- `2019-07-04` — INDEPENDENCE_DAY_OBSERVED
- `2019-09-02` — LABOR_DAY
- `2019-11-28` — THANKSGIVING_DAY
- `2019-11-29` — THANKSGIVING_FRIDAY
- `2019-12-24` — CHRISTMAS_PRE_HOLIDAY_SESSION
- `2019-12-25` — CHRISTMAS_OBSERVED
- `2019-12-31` — NEW_YEARS_EVE_CANDIDATE

## Exactly one next governed action

**Consolidate date-specific evidence for the 13 unresolved 2019 candidate sessions, using the same evidence threshold as 2018, commit only dates that actually meet the threshold, then rerun `tests/test_dukascopy_usatech_calendar.py` and `tools/dukascopy_usatech_calendar_coverage.py`.**

Target is to reduce `unresolved_candidate_dates` below 99 without any false PASS. Massive acquisition remains forbidden until the coverage verdict is PASS with zero unresolved dates.

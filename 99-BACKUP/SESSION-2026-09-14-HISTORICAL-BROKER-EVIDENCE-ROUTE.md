# SESSION BACKUP — 14 SEPTEMBRE 2026 — HISTORICAL BROKER EVIDENCE ROUTE

## 1. Starting point

Repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:

`feat/multi-year-dukascopy-acquisition`

Session-start checkpoint HEAD:

`adb291673be4e6f14dc2a39babcd51385fdd8362`

Branch was verified identical to that checkpoint before substantive work.

Execution-window candidate remains:

`2021-08-14` → `2026-08-14`

In-window calendar state at session start and end:

- candidates: 68;
- resolved: 1;
- unresolved: 67;
- FAIL: 0.

No window boundary was moved.

## 2. Objective

Determine whether a materially new Dukascopy-native historical broker evidence route exists that could resolve the 67 in-window calendar gaps without repeating the exhausted date-by-date generic holiday searches.

No date-level gap was reopened individually during this mechanism-level investigation.

## 3. New qualification gate

Created:

`04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Creation commit:

`41d68772575bdbed50e3c0360f3e45cc0c638be7`

A route can PASS only with:

- verified Dukascopy provenance;
- historical-date addressability;
- explicit `USATECH.IDX/USD` identity;
- exact special-session timing;
- reproducible retrieval;
- calibration against a known gold-standard Dukascopy witness;
- no contradiction with locked evidence.

Preferred calibration witness:

`2020-02-17 — PRESIDENTS_DAY`.

## 4. Candidate route A — official Trading Breaks widget

Official page:

`https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

Materially new observation:

The official widget configuration exposes both `currentDate` and a millisecond `date` parameter and loads Dukascopy widget infrastructure from `freeserv-static.dukascopy.com`.

This is a genuinely new technical route because it suggests date-addressable programmatic behavior behind the Trading Breaks UI.

However, this session did **not** prove that:

- historical state is retained;
- the `date` field actually requests historical state;
- `currentDate=false` is sufficient/valid for historical retrieval;
- the backend returns `USATECH.IDX/USD` for the requested historical date;
- exact historical close/reopen/break times are available;
- the request/response can be captured reproducibly.

Verdict:

**BLOCKED — `HISTORICAL_WIDGET_SEMANTICS_AND_PAYLOAD_NOT_VERIFIED`**

Do not promote the existence of a `date` parameter into historical evidence.

## 5. Candidate route B — JForex IDataService offline domains

Official current JForex API includes instrument-aware offline-time-domain methods such as:

- `getOfflineTimeDomain(Instrument instrument)`;
- `getOfflineTimeDomains(long from, long to, Instrument instrument)`.

This looked initially promising as broker-native historical session evidence.

Adversarial break:

An official Dukascopy API Support response to the exact question whether a holiday in the middle of the week is included by `getOfflineTimeDomains()` says:

**No.**

The follow-up says there was no such holiday functionality available at that time. Current Javadoc wording also characterizes these intervals as weekend offline domains.

Verdict:

**FAIL — `OFFLINE_TIME_DOMAIN_DOES_NOT_COVER_WEEKDAY_HOLIDAY_SESSIONS`**

This route must not be used to infer weekday holiday sessions unless materially new authoritative Dukascopy documentation explicitly changes the semantics and is separately qualified.

## 6. Candidate route C — Dukascopy Market News archive

Official archive:

`https://www.dukascopy.com/swiss/english/marketwatch/market-News/News/`

This is distinct from the `about/ournews` source family used heavily in the annual campaigns.

Recovered example:

`New Year’s trading breaks`, 30 December 2021, Dukascopy Bank SA.

It gives an exact broad interval in which various instruments/markets are scheduled for trading breaks, but delegates detailed instrument hours to the Trading Breaks Calendar.

The archive proves historical broker bulletins remain accessible, but tested in-window material did not provide:

`historical date + USATECH.IDX/USD + exact special-session timing`.

Verdict:

**BLOCKED — `OFFICIAL_ARCHIVE_EXISTS_BUT_TARGET_INSTRUMENT_TIMING_NOT_RECOVERED`**

Search-result absence is not proof that no qualifying bulletin exists.

## 7. Candidate route D — archived Trading Breaks/widget snapshots

No verifiable historical Trading Breaks payload/snapshot was recovered during this investigation.

Wayback/CDX/search access limitations are not evidence that no snapshot exists.

Verdict:

**BLOCKED — `NO_VERIFIED_ARCHIVED_TRADING_BREAKS_SNAPSHOT_RECOVERED`**

## 8. Candidate route E — direct/archived Dukascopy support witness

An exact official Dukascopy support response binding a target historical date to `USATECH.IDX/USD` and exact hours could potentially be admissible depending on provenance and specificity.

No such new witness was collected here.

Verdict:

**BLOCKED — `NO_TARGET_DATE_INSTRUMENT_SPECIFIC_SUPPORT_WITNESS_OBTAINED`**

## 9. Important historical pattern retained

Older official Dukascopy publications contain exact `USATECH.IDX/USD` holiday timings, including known examples from 2016–2020 and the locked PASS witness `2020-02-17`.

Later publications increasingly delegate detailed hours to the Trading Breaks Calendar.

This observation is contextual only. It does not prove either historical retention or historical loss of the Trading Breaks rows.

## 10. Overall route-exploration verdict

Report:

`reports/data-qualification/historical_broker_evidence_route_exploration_v1.md`

Creation commit:

`da26680ac7c887aa37df143af299b941bda1af5f`

Overall verdict:

**BLOCKED — `NO_NEW_HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFIED`**

One candidate route is definitively unsuitable for weekday holidays (JForex offline domains). Other routes remain technically possible but unqualified.

## 11. Boundary update

Updated:

`reports/data-qualification/current_coverage_execution_window_boundary_application.md`

Update commit:

`0e24d5788bf04813a43a1091b19f0f03d7054b66`

Current decisions remain:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`;
- `WINDOW_SELECTION_RULE = PASS`;
- `WINDOW_CANDIDATE_DEFINED = PASS`;
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = BLOCKED`;
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`;
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`;
- `REAL_BACKTEST = BLOCKED`.

## 12. What was NOT changed

- no `SPECIAL_SESSION_EVIDENCE` record;
- no `NO_SPECIAL_CHANGE_EVIDENCE` record;
- no candidate generator;
- no calendar executable code;
- no calendar test;
- no `.bi5` data;
- no execution-window boundary;
- no backtest protocol/result.

Therefore unchanged calendar tests were intentionally not rerun for timestamp freshness.

Latest observed calendar test state remains `34 PASS`.

## 13. Exactly one next governed action

**Technically qualify the official Dukascopy Trading Breaks widget historical-date mechanism against the locked `2020-02-17 — PRESIDENTS_DAY` gold-standard witness in a JavaScript/network-capable browser environment.**

Required sequence:

1. load the official Trading Breaks widget;
2. deliberately address `2020-02-17` rather than current date;
3. capture actual request endpoint/path and parameters;
4. capture response payload and/or rendered historical row;
5. prove historical-date semantics from observed behavior;
6. prove explicit `USATECH.IDX/USD` identity;
7. compare exact hours to the locked Dukascopy Presidents Day 2020 witness;
8. issue route PASS/FAIL/BLOCKED;
9. if and only if calibration PASS, test one unresolved in-window date;
10. do not enumerate/probe all 67 gaps before calibration PASS.

Do not repeat generic holiday searches. Do not use JForex offline domains for holidays. Do not move the window. Do not download `.bi5`. Do not start a real backtest.

# DUKASCOPY USATECH — 2024 ANNUAL CALENDAR AUDIT

## Scope

Audit the completed 2024 annual qualification batch against:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Qualification artifact:

`reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`

Candidate freeze commit:

`811976c584a0626e06d1012e9f90c9f9619c4ca2`

Completed qualification commit:

`343e179254291192843c070ff2832d71eaded04b`

## Frozen candidate-set integrity

The 2024 candidate set was frozen before outcome research from generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Exactly **14** candidates are accounted for:

1. `2024-01-01 — NEW_YEARS_OBSERVED`
2. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
3. `2024-02-19 — PRESIDENTS_DAY`
4. `2024-03-29 — GOOD_FRIDAY`
5. `2024-05-27 — MEMORIAL_DAY`
6. `2024-06-19 — JUNETEENTH_OBSERVED`
7. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`
9. `2024-09-02 — LABOR_DAY`
10. `2024-11-28 — THANKSGIVING_DAY`
11. `2024-11-29 — THANKSGIVING_FRIDAY`
12. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
13. `2024-12-25 — CHRISTMAS_OBSERVED`
14. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`

No candidate was added, removed or moved after evidence research began.

## Verdict-accounting audit

Qualification matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **14**
- total: **14**

Exactly one allowed verdict exists for every frozen candidate.

No candidate is silently omitted.

## Broker-evidence audit

The qualification recovered official Dukascopy 2024 exact-date/period context for multiple dates, including MLK, Easter, Memorial Day, Juneteenth, Labor Day, Thanksgiving and Christmas/New Year.

The audit confirms that these generic/exact-event notices were **not** promoted into target-instrument exact-session witnesses when their retrievable text only delegated the details to the Trading Breaks Calendar.

No date was awarded PASS merely because:

- Dukascopy published a holiday notice;
- the holiday identity was obvious;
- another year had an instrument-explicit schedule;
- the current regular `USATECH.IDX/USD` hours are known;
- same-year CME/reference evidence was strong;
- the historical Trading Breaks state could not be retrieved.

## Target-instrument identity audit

Official 2024 Dukascopy daylight-saving material explicitly names `USATECH.IDX/USD`, but only for normal seasonal schedule context.

The audit confirms that this instrument identity was not improperly converted into evidence that every 2024 U.S. holiday follows a particular special-session schedule.

## Adversarial false-lead audit

A Dukascopy Europe `General Features` page contains a U.S.-national-holiday footnote specifying non-tradable windows.

Inspection of its table proves the footnote is attached only to `XAU/USD` and `XAG/USD`.

The qualification correctly rejected the attempted extrapolation of that rule to `USATECH.IDX/USD`.

Therefore no false PASS-C mapping contract was created from unrelated instruments.

## Trading Breaks historical-route audit

The official current Trading Breaks Calendar states that it publishes holiday-special hours in GMT.

The qualification followed the linked current route and widget but did not recover an auditable historical `2024 + USATECH.IDX/USD + exact target-date hours` row.

The audit confirms this route limitation was classified only as **absence of proof**.

It was not used to infer that a market was open, closed or unchanged.

## Exchange/reference audit

Strong same-year official CME material exists for the 2024 holiday calendar and several specific sessions, including Independence, Labor Day, Thanksgiving and Christmas.

The qualification deliberately granted the exchange side the strongest favorable treatment where appropriate and still rejected PASS-C because the explicit Dukascopy `USATECH` special-session mapping chain is missing.

No exchange-only timing was promoted into broker truth.

## Cross-date and cross-year bypass audit

No verdict relies on:

- a neighboring holiday session;
- another candidate from the same holiday period;
- a schedule from 2018/2019/2020/2021/2022/2023;
- a later 2025/2026 Dukascopy notice;
- a source-count majority.

In particular:

- `2024-07-03` and `2024-07-04` remain independent;
- Thanksgiving Thursday and Friday remain independent;
- Christmas Eve, Christmas Day and New Year's Eve remain independent.

## Executable-artifact audit

No 2024 candidate earned PASS.

Therefore the following is correct:

- no 2024 record added to `SPECIAL_SESSION_EVIDENCE`;
- no `NO_SPECIAL_CHANGE_EVIDENCE` record added;
- no calendar/test expectation modified;
- `tools/dukascopy_usatech_calendar.py` unchanged;
- unchanged tests were not rerun merely to obtain a newer timestamp.

Latest observed executable state therefore remains:

- calendar suite: **34 PASS**;
- global `SPECIAL_SESSION_EVIDENCE`: **24 records**;
- global coverage: **111 candidates / 24 resolved / 87 unresolved / BLOCKED**.

## Boundary audit

Completion of the 2024 research batch does **not** authorize:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest execution;
- selection of a future execution window merely to avoid unresolved dates.

Those boundaries remain unchanged.

## Annual audit verdict

**PASS**

Reason:

`ALL_2024_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

This PASS certifies the integrity and completeness of the 2024 qualification process.

It does **not** certify complete 2024 broker-session coverage.

## Coverage distinction

- `2024_ANNUAL_AUDIT = PASS`
- `2024_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

2024 calendar coverage remains:

**BLOCKED — `2024_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

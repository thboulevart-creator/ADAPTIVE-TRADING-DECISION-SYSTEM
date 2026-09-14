# HISTORICAL TRADING BREAKS RECOVERY PROTOCOL

## Status

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`.**

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_protocol_qualification.md`

Qualified workflow run:

- run: `34880921889`
- job: `104099717727`
- head: `f699de1c9aa7b5726276f07d40c5fc8543bc9392`
- pytest: `20 passed in 0.05s`

## 1. Purpose

Define the only admissible systematic procedure for applying the already-qualified Dukascopy Trading Breaks historical route to the unresolved calendar candidates inside the already-selected execution-window candidate.

This protocol does **not** freeze the execution window, authorize `.bi5`, or authorize a real backtest.

## 2. Frozen scope

Execution-window candidate:

`2021-08-14` → `2026-08-14`

Candidate generator:

`tools.dukascopy_usatech_calendar_coverage.candidate_special_dates()`

Target instrument:

- name: `USATECH.IDX/USD`
- Dukascopy instrument ID: `9016`

The recovery queue is derived mechanically as:

`all in-window candidates - already resolved candidates`

It is sorted strictly ascending by date.

No manual date exclusion, insertion, reordering, window shift, window shortening, or window extension is permitted because of retrieval outcomes.

At qualification time the governed state is:

- in-window candidates: 68;
- already resolved: 2;
- recovery queue: 66;
- first unresolved: `2021-11-25 — THANKSGIVING_DAY`;
- last in-scope candidate: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`.

## 3. Exact-date addressing invariant

Every probe MUST bind one queue candidate to one historical date request.

The requested historical date may not be replaced by:

- adjacent date;
- same holiday in another year;
- current date;
- browser-local fallback date;
- range query whose returned record cannot be attributed to the exact candidate date.

A record is not promotable unless its broker-native interval is attributable to the exact addressed candidate date.

## 4. Positive-record evidence contract

A candidate may receive date-level PASS only from a **positive broker-native record** satisfying all of the following:

1. the request is for the exact candidate date;
2. the broker-native payload contains an explicit break record;
3. the record instrument is ID `9016`;
4. instrument identity is `USATECH.IDX/USD`;
5. `start` and `end` are valid historical epoch timestamps;
6. `end >= start`;
7. the record is attributable to the exact candidate date;
8. raw network payload is retained;
9. rendered DOM/equivalent is captured where available;
10. DOM and payload do not contradict each other;
11. workflow run identity is retained;
12. artifact ID is retained;
13. artifact SHA-256 is retained and syntactically valid;
14. the calibrated end-time representation is applied unchanged.

A positive record satisfying this contract is eligible for the existing date-level evidence gate, normally PASS-A.

Protocol PASS does not automatically promote any date.

## 5. Empty/no-record invariant

An empty response, missing record, HTTP failure, runtime failure, timeout, selector failure, DOM absence, or record for another instrument/date is **NOT evidence of normal trading**.

Such an outcome MUST remain:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

It MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

A separate negative-evidence/completeness contract would be required before absence can prove regular hours.

## 6. Calibrated time semantics

Locked calibration witness:

`2020-02-17 — PRESIDENTS_DAY`

For the minute-resolution Trading Breaks records used by this route:

- `start` = first closed minute;
- `end` = final closed minute;
- `reopen = end + 60 seconds`.

A fully closed UTC hour may be emitted only when all 60 minutes of that UTC hour are inside the closed interval.

Partial hourly buckets remain expected open for hourly-coverage purposes and MUST NOT be silently rounded into closure.

## 7. Provenance contract

Every attempted candidate recovery must retain at minimum:

- candidate date and reason label;
- requested historical date/epoch;
- instrument name and ID;
- probe code commit SHA;
- workflow run ID;
- job ID where available;
- artifact ID;
- artifact SHA-256;
- raw network request metadata;
- raw broker-native response payload;
- rendered DOM/equivalent capture where available;
- parsed target record or explicit no-positive-record outcome;
- protocol version;
- date-level verdict.

No date may be upgraded from an artifact whose identity cannot be reconstructed.

## 8. Deterministic processing order

The recovery queue is processed in strict ascending date order.

Parallel technical execution is permitted only if final adjudication remains deterministic and independent per candidate. Parallelism may not reorder the governed queue or make one candidate borrow evidence from another.

## 9. Independent date-level adjudication

Every candidate receives its own evidence verdict.

Forbidden:

- borrowing a record from another date;
- borrowing a record from another year;
- using a holiday-name match as proof;
- using exchange-only timing as broker truth;
- using route calibration itself as date evidence;
- promoting all dates because one pilot succeeded;
- majority/source-count inference;
- treating no-record as regular-hours proof.

## 10. Executable integration rule

Only a candidate that independently passes the date-level evidence gate may modify executable calendar evidence.

After any executable integration batch:

1. rerun dedicated date regression tests;
2. rerun calendar coverage audit;
3. rerun boundary regression;
4. verify no orphan evidence;
5. verify no contradiction;
6. verify no evidence-shape errors;
7. persist the new counts and run identity.

If no executable record changes, do not rerun tests merely for timestamp freshness.

## 11. Stop / failure behavior

A technical failure on one date does not license a false verdict on that date or any other date.

- valid positive record → submit to date-level gate;
- empty/no-record → BLOCKED;
- malformed/contradictory evidence → FAIL for that evidence attempt and no promotion;
- runtime inaccessible → BLOCKED;
- provenance incomplete → BLOCKED;
- wrong date/instrument → FAIL for that evidence attempt and no promotion.

No blind retry loop is permitted. Diagnose the failure mode before a materially justified retry.

## 12. Window immutability

Recovery outcomes are forbidden inputs to execution-window selection.

The execution-window candidate remains:

`2021-08-14` → `2026-08-14`

The window MUST NOT be moved, shortened, or extended to reduce unresolved count.

## 13. Downstream boundary

Even after protocol PASS:

- bulk recovery is not evidence by itself;
- each date still requires independent adjudication;
- window freeze remains BLOCKED until in-window unresolved = 0 and FAIL = 0;
- `.bi5` remains forbidden until the separate acquisition gate passes;
- real backtest remains forbidden until all mandatory upstream gates pass.

## 14. Adversarial qualification

The executable validator:

`tools/trading_breaks_recovery_protocol.py`

was challenged by:

`tests/test_trading_breaks_recovery_protocol.py`

under GitHub Actions workflow:

`.github/workflows/trading-breaks-recovery-protocol.yml`

Observed run:

- workflow run `34880921889`;
- job `104099717727`;
- conclusion: `success`;
- `20 passed in 0.05s`;
- queue count: `66`;
- first queue item: `2021-11-25 — THANKSGIVING_DAY`;
- last queue item: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`.

The executed attacks cover frozen queue integrity, out-of-window targets, resolved-date reintroduction, date mismatch, instrument mismatch, empty/no-record promotion, missing payload, malformed/negative intervals, adjacent-date records, DOM contradiction, missing provenance, invalid hashes/commit identity, calibrated reopen semantics, and partial-hour rounding.

Final protocol verdict:

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

## 15. Exactly one next governed action

Apply this qualified protocol to the **first deterministic recovery batch** of unresolved candidates in chronological order.

The batch size must be fixed and versioned before observing outcomes. It MUST NOT be chosen or changed to avoid difficult dates.

No `.bi5`. No real backtest.

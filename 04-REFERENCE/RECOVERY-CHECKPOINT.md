# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 01 PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Global calendar:** `111 candidates / 28 resolved / 83 unresolved / 0 FAIL`
- **Candidate window:** `68 candidates / 5 resolved / 63 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Latest persisted-HEAD calendar/boundary regression:** `67 PASS`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest executable-evidence integration commit:

`18271cec8c07a96c2ea0fb348ab042d3c72d0c7d`

Latest calendar-regression configuration/state commit before this checkpoint:

`4967130e1b2574833f242e0445b1eb857fb5809f`

Session backup created before this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH01-PASS.md`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH01-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch01_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch01_runtime.json`
8. `tools/trading_breaks_recovery_batch01.py`
9. `tests/test_trading_breaks_recovery_batch01.py`
10. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
11. `tools/trading_breaks_recovery_protocol.py`
12. `tests/test_trading_breaks_recovery_protocol.py`
13. `04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`
14. `LOCAL-EVIDENCE/README.md`
15. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
16. compare active branch HEAD against the containing checkpoint commit before any write.

GitHub/checkpoint remains the source of truth. Do not reconstruct this work from conversational memory.

## 3. EXECUTION-WINDOW STATE — UNCHANGED BOUNDARY

Window-selection contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Mechanically selected candidate:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **5**
- unresolved/BLOCKED: **63**
- FAIL: **0**

Resolved in-window dates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted, shortened, or extended because recovery remains incomplete.

## 4. HISTORICAL BROKER-EVIDENCE ROUTE — PASS

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

Target broker instrument remains:

- `USATECH.IDX/USD`
- Dukascopy instrument ID `9016`

Calibration witness `2020-02-17 — PRESIDENTS_DAY` and pilot `2021-09-06 — LABOR_DAY` remain valid and MUST NOT be rerun merely to continue batching.

## 5. SYSTEMATIC RECOVERY PROTOCOL — PASS

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

The protocol remains the mandatory date-level adjudication boundary. It rejects queue drift, date/instrument mismatch, empty-response promotion, absent raw payloads, malformed intervals, neighboring-date substitution, DOM/network contradiction, invalid provenance, wrong reopen semantics, and partial-hour rounding.

Negative-evidence boundary remains unchanged:

- positive exact broker records can qualify;
- empty/no-record outcomes remain **BLOCKED**;
- absence MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 6. BATCH 01 POLICY — FROZEN BEFORE OUTCOMES

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Frozen operational size:

`BATCH_SIZE = 5`

Immutable Batch 01 membership:

1. `2021-11-25 — THANKSGIVING_DAY`
2. `2021-11-26 — THANKSGIVING_FRIDAY`
3. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2021-12-24 — CHRISTMAS_OBSERVED`
5. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`

The size and membership were fixed before historical outcome observation and MUST NOT be rewritten after adjudication.

Batch 01 browser workflow is now archived to `workflow_dispatch` only, preventing accidental automatic replay when the current recovery queue changes.

## 7. BATCH 01 AUTHORITATIVE EXECUTION

- workflow run: `34885895206`
- job: `104116336235`
- probe commit: `479900e05eebc6e2c29e0f9f3bddfdfc78e78224`
- artifact: `10364872726`
- artifact SHA-256: `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`
- conclusion: `SUCCESS`

Independent adjudication:

- `2021-11-25` → **PASS** — record `30449`, `17:59Z → 22:59Z`, reopen `23:00Z`, full closed hours `18–22`
- `2021-11-26` → **PASS** — record `30450`, starts `18:14Z`; special whole-hour additions `19–21`; Friday `22–23` remain regular weekly close
- `2021-12-23` → **PASS** — record `31532`, starts `21:14Z`; target-date full closed hours `22–23`
- `2021-12-24` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `2021-12-31` → **BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

Overall:

**PASS — `BATCH01_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

Only the three PASS records were integrated.

## 8. POST-BATCH INTEGRATION AND REGRESSION

Combined pre-persistence integration gate:

- workflow run: `34887010102`
- conclusion: **SUCCESS**
- regression: **91 passed**
- global assertions: `111 / 28 / 83`
- window assertions: `68 / 5 / 63`

Persisted executable-evidence commit:

`18271cec8c07a96c2ea0fb348ab042d3c72d0c7d`

Independent regression against persisted HEAD:

- workflow run: `34887061155`
- job: `104120211534`
- conclusion: **SUCCESS**
- pytest: **67 passed in 0.52s**
- candidate dates: `111`
- resolved: `28`
- unresolved: `83`
- orphan evidence: `0`
- contradictory evidence: `0`
- evidence-shape errors: `0`

The global verdict therefore remains legitimately **BLOCKED** only because unresolved dates remain, not because of a regression or contradiction.

## 9. CURRENT RECOVERY QUEUE

In-window unresolved queue size:

`63`

First candidate:

`2021-12-24 — CHRISTMAS_OBSERVED`

Last candidate:

`2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

First five queue entries:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

These are the deterministic candidates for Batch 02 under the current `BATCH_SIZE = 5`; they are not selected by expected ease, likelihood of a break, or prior knowledge of outcomes.

## 10. CURRENT BOUNDARY MATRIX

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 11. WHAT MUST NOT BE REPEATED

- do not reopen Batch 01 dates manually;
- do not rerun calibration/pilot merely to continue;
- do not infer normal trading from empty widget/API responses;
- do not use adjacent-date records as exact-date proof;
- do not move the execution window;
- do not download massive `.bi5` data;
- do not start a real backtest.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 02 as exactly the next five entries of the current governed recovery queue, preserving `BATCH_SIZE = 5`, BEFORE observing any new Batch 02 outcomes; then execute those five dates chronologically under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.**

Batch 02 membership must therefore be derived mechanically from the post-Batch-01 queue and locked before browser execution. No candidate may be skipped, substituted, or reordered based on apparent ease/difficulty or expected outcome.

After Batch 02:

1. adjudicate each date independently;
2. integrate only true positive-record PASS dates;
3. keep no-record outcomes BLOCKED;
4. rerun calendar/boundary regression only if executable evidence changes;
5. persist run/job/artifact/SHA/commit provenance and updated counts;
6. update backup and this Recovery Checkpoint.

No `.bi5`. No real backtest.

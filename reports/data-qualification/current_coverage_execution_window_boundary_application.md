# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 04 atomic integration

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 37 resolved / 74 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 14 resolved / 54 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression contract: **PASS**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — atomically integrated**
- Historical attempt ledger entries: **20**
- Registered material capability changes: **0**
- Attempted BLOCKED / currently execution-ineligible: **6**
- Currently execution-eligible unresolved: **48**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

## Persisted executable calendar state

The execution-window candidate now contains exactly **14** resolved dates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2022-05-30 — MEMORIAL_DAY`
8. `2022-06-20 — JUNETEENTH_OBSERVED`
9. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
10. `2022-09-05 — LABOR_DAY`
11. `2022-11-24 — THANKSGIVING_DAY`
12. `2022-11-25 — THANKSGIVING_FRIDAY`
13. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
14. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

`BLOCKED` remains unresolved. Empty/no-record responses and cross-date overlaps MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 04 authoritative evidence chain

Frozen membership remained exactly:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

Browser execution:
- run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- pre-browser suite: `110 passed in 0.59s`

Independent adjudication:
- run: `34895985689`
- job: `104149952523`
- suite: `81 passed in 0.27s`
- final: **3 PASS / 2 BLOCKED / 0 FAIL**

Only these three exact-target records were authorized and integrated:
- `2022-11-24` → record `45119`, fully closed UTC hours `18–22`;
- `2022-11-25` → record `45120`, fully closed target-day UTC hours `19–23`;
- `2022-12-23` → record `46756`, fully closed target-day UTC hours `22–23`.

These two dates remain unresolved and were not promoted:
- `2022-12-26 — CHRISTMAS_OBSERVED` → `BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- `2023-01-02 — NEW_YEARS_OBSERVED` → `BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`.

## Batch 04 atomic integration

Final integration contract verdict:

**PASS — `BATCH04_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**

Authoritative integration:
- workflow run: `34896951616`
- job: `104153317098`
- pre-integration SHA: `7dd9a0dcc938d13b018be14436a35b6b79ed5146`
- atomic integration commit: `6cafa5337f28c5424cbcc25280c690de702061d9`
- pre-mutation adversarial suite: `79 passed in 0.35s`
- post-mutation adversarial/regression suite: `139 passed in 1.23s`

The single atomic integration commit changed the governed state together:
- three PASS calendar additions;
- all five factual Batch 04 attempts as sequences `16..20`;
- regenerated progression runtime;
- state-sensitive regression expectations and Batch 04 integration proofs.

No partial calendar/ledger state was accepted.

## Attempt-aware progression after Batch 04

Current deterministic state:
- calendar unresolved: **54**
- historical attempts: **20**
- registered material capability changes: **0**
- attempted BLOCKED / execution-ineligible: **6**
- execution-eligible unresolved: **48**
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The six same-capability attempted BLOCKED dates remain unresolved but are execution-ineligible:
- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each is classified:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

No retry is authorized without a separately qualified material capability change addressing the exact blocker.

## Independent persisted-HEAD proof

Authoritative read-only re-break:
- verified commit: `9ad19ede0052f37ce8aa2ccd30a117cd0525bc10`
- workflow run: `34897126921`
- job: `104153918828`
- conclusion: **SUCCESS**
- regression: **139 passed in 0.73s**
- exact persisted calendar / ledger / progression assertion: **PASS**
- read-only proof `git diff --exit-code`: **PASS**

The verifier checked out the exact triggering SHA in detached-HEAD mode with `contents: read` and made no repository-state mutation.

## Workflow closure

Completed Batch 04 execution, adjudication, integration and persisted-state workflows are archived/manual-only as appropriate. In particular:
- `.github/workflows/trading-breaks-recovery-batch04-integration.yml` → `workflow_dispatch` only;
- `.github/workflows/trading-breaks-recovery-batch04-persisted-head.yml` → `workflow_dispatch` only.

No normal push can silently repeat the completed Batch 04 integration or fixed-state re-break.

## Current boundary decisions

PASS:
- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 05 membership from the governed post-Batch04 `eligible_recovery_queue()`, then adversarially qualify that immutable membership before any browser observation.**

That next action must mechanically derive membership from the now-proven post-Batch04 state. It must not reuse Batch 04 membership, raw `recovery_queue()`, expected outcomes, source availability, manual preference, or any conversational projection.

No Chromium observation belongs to the membership-freeze step. No `.bi5` acquisition. No real backtest.

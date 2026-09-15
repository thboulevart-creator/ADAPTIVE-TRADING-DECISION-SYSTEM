# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 05 execution/adjudication PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 37 resolved / 74 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 14 resolved / 54 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware progression: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05 membership: **PASS — frozen before observation**
- Recovery Batch 05 execution/adjudication: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — NOT YET INTEGRATED**
- Historical attempt ledger entries: **20** until Batch 05 integration
- Registered material capability changes: **0**
- Attempted BLOCKED / execution-ineligible: **6**
- Execution-eligible unresolved: **48** until Batch 05 integration/progression regeneration
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 05 immutable membership

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

Selection was frozen from governed post-Batch04 `eligible_recovery_queue()[:5]` before observation. Execution consumed only `batch05_targets()` and did not recalculate membership.

## Batch 05 authoritative execution

- workflow run: `34947146056`
- job: `104309150262`
- probe commit: `33ae476c48372bce64421a411066db2ddea6125c`
- pre-browser suite: **134 passed in 0.58s**
- exact frozen identity gate: PASS
- no-live-membership-recalculation gate: PASS
- artifact: `10386998786`
- artifact SHA-256: `ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c`
- runtime persistence commit: `cda3eaa865a53e62fc5084bed692c3c904844c71`

Chromium was installed/opened only after all pre-browser gates passed.

## Batch 05 independent adjudication

- workflow run: `34947662443`
- job: `104310794052`
- adversarial suite: **83 passed in 0.28s**
- final accounting: **5 PASS / 0 BLOCKED / 0 FAIL**
- report persistence commit: `3300afc057967412b031ecc2134278cd7f66c858`
- adjudicator browser/probe/live-queue path: NONE

Date-level PASS records:

1. `2023-01-16` → record `49338`, fully closed UTC hours `18–22`.
2. `2023-02-20` → record `50456`, fully closed UTC hours `18–22`.
3. `2023-04-07` → record `52290`, exact target-day start `14:14Z`, target-day fully closed UTC hours `15–23`; the broker interval continues through the weekend and reopens `2023-04-09T22:00:00Z`.
4. `2023-05-29` → record `54373`, fully closed UTC hours `17–21`.
5. `2023-06-19` → record `55281`, fully closed UTC hours `17–21`.

All five passed exact target-date, instrument, raw-payload, DOM and immutable provenance validation under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.

## Critical pre-integration boundary

These five PASS verdicts are qualified evidence, but they have **not yet been integrated** into:
- `SPECIAL_SESSION_EVIDENCE`;
- the factual attempt ledger;
- regenerated progression state.

Therefore persisted executable calendar and progression counters remain the pre-integration values shown above. Do not project post-integration counters as authoritative before the atomic integration and persisted-HEAD re-break succeed.

Completed Batch 05 execution/adjudication workflows are archived to `workflow_dispatch` only.

## Current boundary decisions

PASS:
- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_EXECUTION_ADJUDICATION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Integrate Batch 05 atomically: add exactly the five independently adjudicated PASS records to the executable calendar, append all five factual Batch 05 attempts to the ledger, regenerate attempt-aware progression, then adversarially re-break and independently verify the persisted HEAD.**

No Batch 06 membership before that integration and persisted-HEAD re-break are PASS.

No `.bi5`. No real backtest.

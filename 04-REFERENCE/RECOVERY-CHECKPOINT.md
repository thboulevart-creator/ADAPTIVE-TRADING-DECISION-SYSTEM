# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS BATCH 03 PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Global calendar:** `111 candidates / 34 resolved / 77 unresolved / 0 FAIL`
- **Candidate window:** `68 candidates / 11 resolved / 57 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Attempt-aware recovery progression:** PASS
- **Batch 03 membership policy:** PASS
- **Batch 03 execution/adjudication:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`)
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Historical attempt ledger entries:** `15`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `4`
- **Execution-eligible unresolved:** `53`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest authoritative Batch 03 execution provenance:

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`

Latest persisted integration commit:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Latest persisted-HEAD regression:

- run: `34893976903`
- job: `104143235284`
- HEAD under test: `30f6d11bb51473211b9576bde92e85b405ed5606`
- conclusion: **SUCCESS**
- suite: **104 passed in 0.60s**

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
4. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH03-POLICY.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch03_qualification.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch03_adjudication.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
10. `tools/trading_breaks_recovery_batch03.py`
11. `tools/trading_breaks_recovery_batch03_execute.py`
12. `tools/trading_breaks_recovery_batch03_adjudication.py`
13. `tools/integrate_trading_breaks_recovery_batch03.py`
14. `tests/test_trading_breaks_recovery_batch03.py`
15. `tests/test_trading_breaks_recovery_batch03_adjudication.py`
16. `tests/test_trading_breaks_recovery_batch03_integration.py`
17. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
18. `tools/trading_breaks_recovery_progression.py`
19. `tests/test_trading_breaks_recovery_progression.py`
20. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
21. `tools/trading_breaks_recovery_protocol.py`
22. `tests/test_trading_breaks_recovery_protocol.py`
23. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. BATCH 03 — EXECUTED AND INDEPENDENTLY ADJUDICATED

Frozen immutable Batch 03 membership remained exactly:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

No membership recalculation was used during execution or adjudication.

Final date-level adjudication:

- `2022-05-30` → **PASS** — exact broker record `37019`, Memorial Day
- `2022-06-20` → **PASS** — exact broker record `38945`, Juneteenth Holiday
- `2022-07-01` → **BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**
- `2022-07-04` → **PASS** — exact broker record `41225`, Independence Day
- `2022-09-05` → **PASS** — exact broker record `42569`, Labor Day

All four PASS dates use exact `USATECH.IDX/USD` / instrument `9016` records, exact target-date evidence, calibrated reopen semantics, and matching DOM witnesses.

Batch accounting:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

Final verdict:

**PASS — `BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

`2022-07-01` remains unresolved/BLOCKED. It does not populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 4. ADVERSARIAL CORRECTIONS DURING BATCH 03

Two boundaries were corrected before final acceptance:

1. DOM instrument normalization was tightened so a wrong instrument cannot be accepted before normalization.
2. Live recovery eligibility was separated from immutable frozen-batch replay scope, so a historical Batch 03 replay/adjudication remains bound to the frozen membership even after integration changes current eligibility.

The corrected adjudication was rerun and the final integration used the replay-safe frozen scope.

## 5. INTEGRATED CALENDAR / PROGRESSION STATE

Only genuine PASS evidence was integrated.

Current calendar accounting:

- global: `111 / 34 / 77`
- execution window: `68 / 11 / 57`

Current progression accounting:

- unresolved calendar dates: `57`
- historical attempts: `15`
- registered material capability changes: `0`
- already-attempted BLOCKED / execution-ineligible: `4`
- execution-eligible unresolved: `53`

Currently BLOCKED and ineligible under unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

They remain unresolved in `recovery_queue()` and are excluded only from `eligible_recovery_queue()`.

## 6. PERSISTED-HEAD REGRESSION — PASS

Run `34893976903`, job `104143235284` independently re-broke the persisted branch state.

Results:

- `104 passed in 0.60s`
- global accounting `111 / 34 / 77`
- window accounting `68 / 11 / 57`
- evidence-shape errors `0`
- orphan special evidence `0`
- contradictory evidence dates `0`
- attempt ledger `15`
- unresolved queue `57`
- attempted BLOCKED / ineligible `4`
- eligible unresolved `53`
- progression verdict `PASS`

First current eligible candidate:

`2022-11-24 — THANKSGIVING_DAY`

## 7. CURRENT BOUNDARY MATRIX

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 8. WORKFLOW STATUS

Batch 03 execution, adjudication, integration and persisted-HEAD regression workflows are archived to `workflow_dispatch` only after PASS.

No automatic replay is authorized.

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 04 with `BATCH_SIZE = 5` as exactly the first five entries of the current governed `eligible_recovery_queue()`, BEFORE any Batch 04 historical observation.**

Current deterministic projection begins:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

These become Batch 04 only after mechanical derivation and versioned freeze. Do not treat this checkpoint listing as a substitute for that freeze.

No `.bi5`. No real backtest.

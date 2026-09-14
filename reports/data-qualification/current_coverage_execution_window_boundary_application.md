# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 04 membership qualification

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 34 resolved / 77 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 11 resolved / 57 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression: **PASS**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- Batch 04 membership policy: **PASS — frozen before observation**
- Historical attempt ledger entries: **15**
- Registered material capability changes: **0**
- Attempted BLOCKED / currently execution-ineligible: **4**
- Currently execution-eligible unresolved: **53**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

## Calendar evidence state — unchanged by Batch 04 freeze

The execution-window candidate contains exactly **11** resolved dates:

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
11. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Empty/no-record responses and neighboring-date overlaps still do not prove regular trading and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 03 closure remains authoritative

Batch 03 final accounting remains:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

Authoritative browser run:

- run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`

Only the four PASS dates were integrated. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION` remains unresolved/BLOCKED under `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`.

Final atomic integration:

- run: `34893854678`
- job: `104142824703`
- regression: `104 passed`
- integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Independent persisted-HEAD proof:

- run: `34893976903`
- job: `104143235284`
- conclusion: SUCCESS
- regression: `104 passed in 0.60s`

## Attempt-aware progression after Batch 03

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Current deterministic state used for the Batch 04 freeze:

- calendar unresolved dates: **57**
- historical attempts: **15**
- registered material capability changes: **0**
- attempted BLOCKED / currently execution-ineligible: **4**
- unresolved currently execution-eligible: **53**
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The four already-attempted BLOCKED dates remain unresolved but are not replay-eligible under the unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Each remains classified `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` until a separately versioned and qualified material evidence-capability change addresses its exact blocker.

## Batch 04 membership — frozen and qualified before observation

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Final verdict:

**PASS — `BATCH04_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Frozen `BATCH_SIZE = 5` membership:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

Selection rule at freeze:

`eligible_recovery_queue()[:5]`

The five entries were mechanically redriven from the governed repository state before freezing. Each was proven unresolved, execution-eligible, `INITIAL_ATTEMPT`, unattempted, unique and chronological. Raw `recovery_queue()[:5]` is explicitly not an admissible source.

Freeze provenance:

- pre-freeze checkpoint HEAD: `4d3c5db74ec31215b74799f27cdfe476d513014b`
- source progression/integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Authoritative membership qualification:

- run: `34894947834`
- job: `104146491103`
- trigger commit: `641b0e0369ed5a47c4adb69370e2b166b8088c06`
- conclusion: **SUCCESS**
- adversarial/regression suite: **104 passed in 0.35s**
- exact membership assertion: **PASS**
- no-browser/no-probe guard: **PASS**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_policy_qualification.md`

No Batch 04 historical broker observation has occurred. The freeze module contains no Playwright, Chromium, `probe_candidate`, or asyncio execution path.

The Batch 04 membership qualification workflow is archived to `workflow_dispatch` only.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Execute the already-frozen Batch 04 membership under the qualified Trading Breaks capture chain, with all parent/progression/Batch04 gates passing before Chromium opens, then independently adjudicate all five results.**

Execution MUST use exactly the five frozen dates above. Membership MUST NOT be recalculated from the then-current eligible queue, substituted, expanded, shortened, reordered, or influenced by observed/expected outcomes.

After execution, independently adjudicate all five dates under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`. Integrate only genuine PASS evidence, preserve BLOCKED as unresolved, record all factual attempts, and rerun the required coverage/progression regressions.

No `.bi5` acquisition. No real backtest.

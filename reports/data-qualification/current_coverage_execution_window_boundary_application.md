# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 30 resolved / 81 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 7 resolved / 61 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression: **PASS**
- Batch 03 membership policy: **PASS — frozen before observation**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14` and MUST NOT be moved to avoid unresolved dates.

## Calendar evidence state — unchanged

Resolved in-window dates remain:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Empty/no-record responses and neighboring-date overlaps still do not prove regular trading and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Attempt-aware progression state

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Verdict:

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

Current deterministic state:

- unresolved calendar dates: `61`
- historical attempts: `10`
- registered material capability changes: `0`
- already-attempted BLOCKED / execution-ineligible: `3`
- execution-eligible unresolved: `58`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The following remain unresolved but are not eligible for identical-capability replay:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

They remain in calendar accounting and are excluded only from `eligible_recovery_queue()`.

## Batch 03 membership — frozen and qualified before observation

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Final verdict:

**PASS — `BATCH03_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Selection rule:

`eligible_recovery_queue()[:5]`

Frozen `BATCH_SIZE = 5` membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Each member was proven at freeze time to be:

- unresolved in calendar evidence state;
- execution-eligible;
- `INITIAL_ATTEMPT`;
- absent from the historical attempt ledger;
- in exact chronological eligible-queue order.

Raw `recovery_queue()[:5]` is explicitly not the Batch 03 source because it contains already-attempted BLOCKED dates.

Freeze provenance:

- pre-freeze checkpoint HEAD: `d4dab0a10ba6bc782186159899f7b8225e7aab59`
- source progression runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch03_policy_qualification.md`

Corrected authoritative qualification run:

- run: `34891341634`
- job: `104134524746`
- trigger commit: `4260fd7c91fe855aeb0ff99c70ceb7458d593993`
- conclusion: **SUCCESS**
- adversarial/regression suite: **84 passed in 0.39s**
- exact frozen membership assertion: **PASS**
- no-browser/probe execution-path guard: **PASS**

The first run `34891254793` also produced `84 passed` and exact membership PASS, but a self-referential browser guard falsely failed because it searched for a literal string contained in its own assertion. The guard was corrected minimally and the complete suite was re-run.

No Batch 03 historical broker observation has yet occurred. The Batch 03 freeze tool contains no Playwright, Chromium, `probe_candidate`, or asyncio execution path.

The Batch 03 policy qualification workflow is archived to `workflow_dispatch` only.

## Local retained ZIP evidence

The three previously retained Trading Breaks ZIP archives remain correctly governed by the versioned manifest:

`LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

Their local placement and independent SHA-256 verification are recorded in `LOCAL-EVIDENCE/README.md`. The ZIP binaries themselves remain intentionally ignored by Git.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Execute the already-frozen Batch 03 membership under the qualified Trading Breaks capture/adjudication chain, with all parent and Batch 03 policy gates passing before Chromium opens.**

The execution MUST use exactly the five frozen dates above. Membership MUST NOT be recalculated, substituted, expanded, shortened, or reordered according to observed/expected outcomes.

After execution, independently adjudicate all five dates under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`, integrate only genuine PASS evidence, preserve BLOCKED as unresolved, update the attempt ledger, then rerun coverage/progression regressions as required.

No `.bi5` acquisition. No real backtest.

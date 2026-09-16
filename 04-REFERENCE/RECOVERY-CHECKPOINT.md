# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — BATCH 15 V2 FULLY CLOSED / CRITICAL PATH MUST BE RE-EVALUATED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests and qualified workflow evidence are authoritative. Do not reconstruct state from conversation memory.

Construction rule remains:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

A successful prior mechanism is not, by itself, evidence that the same mechanism is the next correct action.

## Batch 14 — FULLY CLOSED

- integration: `075b33b79c8de3b2f4f6201a7541c6555585a5e4`
- independent persisted-HEAD re-break trigger: `ceec67b5951c52564c3ce610c8347d0f46a721e4`
- run/job: `35063579495 / 104688908778`
- regression: `461 passed in 2.01s`
- verdict: `PASS — BATCH14_PERSISTED_HEAD_REBREAK_CONFIRMS_TERMINAL_INTEGRATION`

Durable report:

`reports/data-qualification/historical_trading_breaks_recovery_batch14_persisted_head_rebreak.md`

## Post-Batch14 critical-path pivot

The 17 unresolved dates were correctly separated into two different problems:

- Class A: 14 positive broker-native records spanning the target day but blocked by the old exact-start-date admissibility rule;
- Class B: 3 true no-positive-record cases.

Decision record:

`reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-15.md`

This rejected:

- continuing under unchanged V1 capability;
- searching for a new source for all 17 dates;
- bypassing calendar qualification to start `.bi5` acquisition.

## Target-day overlap semantic capability V2 — QUALIFIED

Contract:

`TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`

Current capability:

`TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`

Fingerprint:

`e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

Material change:

`TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_CHANGE_V1`

Qualification commit:

`061e97d90eed2c4c3f1d5f2a261e457fd796413f`

Qualified facts:

- target-day cross-date interval attribution: PASS;
- immutable binding to original historical V1 source attempts: PASS;
- V2 capability activation and persisted-HEAD re-break: PASS;
- all 14 Class-A cases offline readjudicated: `14 PASS / 0 BLOCKED / 0 FAIL`;
- no browser/probe/live recapture used for Class-A semantic readjudication.

Authoritative reports include:

- `reports/data-qualification/trading_breaks_target_day_overlap_semantics_qualification.md`
- `reports/data-qualification/trading_breaks_target_day_overlap_source_binding_qualification.md`
- `reports/data-qualification/trading_breaks_target_day_overlap_v2_activation_qualification.md`
- `reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`

## Batch 15 V2 — FULLY CLOSED

Policy:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH15_OVERLAP_V2_RETRY_POLICY_V1`

Frozen membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Freeze chain:

- baseline: `d6622e8da58e2d4218947ff3f2953fe8e19a2c96`
- qualification HEAD: `8066e82607db1f8de0b406ec36684a6856e0646d`
- qualification run/job: `35067822465 / 104702050599`
- persisted-membership re-break run/job: `35067904056 / 104702309977`

Offline execution/adjudication:

- execution selector HEAD: `f73d31e645bdc1ad4081a7cf3c104e3f3bd4848b`
- execution run/job: `35068035246 / 104702726720`
- adjudication trigger: `6dc134aa53a0904cda6c08108377dd8be8dd718c`
- adjudication run/job: `35068120024 / 104702999768`
- result: `5 PASS / 0 BLOCKED / 0 FAIL`

Atomic integration:

`4dee7e22af1402626341f76611926b108fd1d8c0`

The integration changed exactly:

- `tools/dukascopy_usatech_calendar.py`
- `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
- `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`

### Independent persisted-HEAD re-break

First verifier attempt:

- commit: `3befa42956f9d4013fced5623f283996f75a227e`
- run/job: `35085516084 / 104759279481`
- result: FAIL due verifier-scope error: a pre-integration adjudicator requiring exactly 68 attempts was incorrectly replayed against the legitimate 73-attempt post-integration state.
- this failure did not reveal a governed-state mutation or integration defect.

Corrected verifier:

- commit: `4bb7712bcab8b8930c4054e1500302621f881f4f`
- run/job: `35085635675 / 104759660665`
- permissions: `contents: read`
- durable post-state regression: `65 passed in 0.25s`
- integration ancestry and three-file atomic mutation: PASS
- historical attempts `1..68` immutable: PASS
- exact retry attempts `69..73`: PASS
- calendar/source-attempt/provenance binding: PASS
- capability registry: PASS
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE
- final workflow conclusion: success

Verdict:

**PASS — `BATCH15_V2_PERSISTED_HEAD_REBREAK_CONFIRMS_INTEGRATION`**

Durable report:

`reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`

Session backup:

`99-BACKUP/SESSION-2026-09-16-TRADING-BREAKS-BATCH15-V2-CLOSED.md`

## Current deterministic state after Batch 15 V2

Global calendar:

- candidates: `111`
- resolved: `79`
- unresolved: `32`
- FAIL: `0`

Execution-window candidate `2021-08-14 → 2026-08-14`:

- candidates: `68`
- resolved: `56`
- unresolved: `12`
- FAIL: `0`

Recovery state:

- attempt ledger: `73`
- registered material capability changes: `1`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- current unresolved queue: `12`
- execution-eligible unresolved: `9`
- unresolved/ineligible Class B: `3`
- execution window frozen: **NO**
- `.bi5`: **FORBIDDEN**
- real backtest: **NOT AUTHORIZED**

### Remaining Class A — 9 currently V2-eligible

1. `2023-12-25 — CHRISTMAS_OBSERVED`
2. `2024-01-01 — NEW_YEARS_OBSERVED`
3. `2024-03-29 — GOOD_FRIDAY`
4. `2024-12-25 — CHRISTMAS_OBSERVED`
5. `2025-01-01 — NEW_YEARS_OBSERVED`
6. `2025-04-18 — GOOD_FRIDAY`
7. `2025-12-25 — CHRISTMAS_OBSERVED`
8. `2026-01-01 — NEW_YEARS_OBSERVED`
9. `2026-04-03 — GOOD_FRIDAY`

Their current eligibility reason is the already-qualified material V2 capability change.

### Remaining Class B — 3 unresolved/ineligible

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Current reason:

`RETRY_MATERIAL_CHANGE_NOT_PROVEN:BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED`

The V2 overlap capability does not address `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`; these three must remain separate from Class A.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-TRADING-BREAKS-BATCH15-V2-CLOSED.md`
4. `reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`
5. `reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-15.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
9. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
10. `tools/trading_breaks_recovery_progression.py`
11. relevant Batch 15 V2 policy/freeze/adjudication/integration files and reports
12. relevant overlap-semantics/source-binding qualification files
13. compare active branch HEAD against the commit containing this checkpoint before any mutation.

## Exactly one next governed action

**Re-evaluate the pre-backtest critical path from the current `9 Class A eligible + 3 Class B ineligible` state before deciding whether the next action is another bounded V2 integration batch, a Class-B negative-evidence/completeness workstream, or another upstream gate.**

Do not freeze Batch 16 merely because Batch 15 succeeded.  
Do not launch a browser capture merely because three Class-B dates remain.  
Do not acquire `.bi5`.  
Do not run a real backtest.

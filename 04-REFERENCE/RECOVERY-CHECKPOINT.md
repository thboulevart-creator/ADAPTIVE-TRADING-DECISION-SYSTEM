# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — BATCH 14 FULLY CLOSED / OVERLAP SEMANTIC QUALIFICATION NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests and qualified workflow evidence are authoritative. Do not reconstruct state from conversation memory.

## Batch 14 — FULLY CLOSED

Terminal membership:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Execution/adjudication:

- run/job: `35023845609` / `104565948108`
- probe commit: `4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b`
- artifact: `10418961548`
- artifact SHA-256: `00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910`
- adjudication: `2 PASS / 1 BLOCKED / 0 FAIL`
- `2026-06-19` PASS record `101094`
- `2026-07-02` BLOCKED `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`
- `2026-07-03` PASS record `101959`

Atomic integration commit:

`075b33b79c8de3b2f4f6201a7541c6555585a5e4`

Independent persisted-HEAD re-break:

- trigger: `ceec67b5951c52564c3ce610c8347d0f46a721e4`
- run/job: `35063579495` / `104688908778`
- permissions: `contents: read`
- regression: `461 passed in 2.01s`
- exact calendar/ledger/progression/provenance: PASS
- progression regeneration byte-stable: PASS
- final worktree clean: PASS
- verdict: **PASS — `BATCH14_PERSISTED_HEAD_REBREAK_CONFIRMS_TERMINAL_INTEGRATION`**
- report: `reports/data-qualification/historical_trading_breaks_recovery_batch14_persisted_head_rebreak.md`

The verifier workflow is archived to `workflow_dispatch` only.

## Deterministic post-Batch14 state

- global calendar: `111 / 74 resolved / 37 unresolved / 0 FAIL`
- execution-window candidate `2021-08-14 → 2026-08-14`: `68 / 51 resolved / 17 unresolved / 0 FAIL`
- raw recovery queue: `17`
- attempt ledger: `68`
- same-capability BLOCKED/ineligible: `17`
- execution-eligible unresolved under `TRADING_BREAKS_PRIMARY_WIDGET_V1`: `0`
- material capability changes: `0`
- execution window frozen: NO
- `.bi5`: FORBIDDEN
- real backtest: NOT AUTHORIZED

The current capability is exhausted. **Batch 15 under the same capability is forbidden.**

## Critical-path classification

Decision record:

`reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-15.md`

### Class A — 14 semantic-admissibility cases

These have an already captured positive primary broker record overlapping the target day but were BLOCKED solely by the exact-start-date rule:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
6. `2023-12-25 — CHRISTMAS_OBSERVED`
7. `2024-01-01 — NEW_YEARS_OBSERVED`
8. `2024-03-29 — GOOD_FRIDAY`
9. `2024-12-25 — CHRISTMAS_OBSERVED`
10. `2025-01-01 — NEW_YEARS_OBSERVED`
11. `2025-04-18 — GOOD_FRIDAY`
12. `2025-12-25 — CHRISTMAS_OBSERVED`
13. `2026-01-01 — NEW_YEARS_OBSERVED`
14. `2026-04-03 — GOOD_FRIDAY`

Blocking reason: `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`.

### Class B — 3 no-positive-record cases

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Blocking reason: `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`.

These need a separate completeness/negative-evidence decision and must not be conflated with Class A.

## Material-change rule

Historical attempts `1..68` are immutable.

A later Class-A retry/re-adjudication may only become eligible after a separately qualified material capability change that:

- changes an executable capability dimension, not proof metadata alone;
- adds the governed proof capability `QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION`;
- explicitly addresses `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- is tied to a qualification contract and qualification commit;
- preserves all existing proof capabilities.

Do not register or activate such a capability before the semantic contract itself passes adversarial qualification.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-TRADING-BREAKS-BATCH14-CLOSED-SEMANTIC-PIVOT.md`
4. `reports/data-qualification/historical_trading_breaks_recovery_batch14_persisted_head_rebreak.md`
5. `reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-15.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
9. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
10. `tools/trading_breaks_recovery_progression.py`
11. `tests/test_trading_breaks_recovery_progression.py`
12. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
13. `tools/trading_breaks_recovery_protocol.py`
14. relevant persisted historical runtimes/adjudications containing Class-A evidence
15. compare active branch HEAD against the commit containing this checkpoint before any write.

## Exactly one next governed action

**Qualify offline and adversarially a target-day-overlap attribution contract using only already captured Class-A broker-native evidence.**

The contract must prove that a cross-date broker-native interval may support only those whole UTC hours of the target day that it actually covers, while rejecting at minimum:

- adjacent but non-overlapping records;
- wrong target date;
- wrong instrument;
- malformed/reversed intervals;
- missing raw broker payload/provenance;
- multiple/ambiguous matching records;
- DOM/network contradiction when DOM exists;
- fabricated reopen timestamps;
- partial-hour rounding;
- unrelated record/year borrowing;
- `CAPTURED → PASS` without independent semantic validation.

This qualification is offline only. No browser, no `probe_candidate`, no new capture, no `.bi5`, no real backtest.

If and only if this semantic contract passes, the next action is to register/activate the corresponding material capability change and re-adjudicate the 14 Class-A dates from persisted evidence without rewriting historical attempts.

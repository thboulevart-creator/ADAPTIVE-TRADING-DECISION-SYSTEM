# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — BATCH 15 V2 FULLY CLOSED / CLASS-B COMPLETENESS NEXT

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

Authoritative reports:

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

Independent persisted-HEAD re-break:

- first verifier: `3befa42956f9d4013fced5623f283996f75a227e`
- first run/job: `35085516084 / 104759279481`
- first result: FAIL because a pre-integration adjudicator requiring 68 attempts was incorrectly replayed against the legitimate 73-attempt post-integration state;
- corrected verifier: `4bb7712bcab8b8930c4054e1500302621f881f4f`
- authoritative run/job: `35085635675 / 104759660665`
- permissions: `contents: read`
- post-state-safe regression: `65 passed in 0.25s`
- integration ancestry and three-file atomic mutation: PASS
- historical attempts `1..68` immutable: PASS
- retry attempts `69..73`: PASS
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

## Current deterministic state

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
- execution-eligible unresolved Class A: `9`
- unresolved/ineligible Class B: `3`
- execution window frozen: **NO**
- `.bi5`: **FORBIDDEN**
- real backtest: **NOT AUTHORIZED**

## Critical-path reevaluation — 9 Class A + 3 Class B

Decision record:

`reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-16.md`

Verdict:

**PASS — `CLASS_B_COMPLETENESS_IS_THE_ONLY_INFORMATIONAL_BLOCKER_WORTH_ATTACKING_NEXT`**

### Remaining Class A — 9 proven PASS but not yet integrated

1. `2023-12-25 — CHRISTMAS_OBSERVED`
2. `2024-01-01 — NEW_YEARS_OBSERVED`
3. `2024-03-29 — GOOD_FRIDAY`
4. `2024-12-25 — CHRISTMAS_OBSERVED`
5. `2025-01-01 — NEW_YEARS_OBSERVED`
6. `2025-04-18 — GOOD_FRIDAY`
7. `2025-12-25 — CHRISTMAS_OBSERVED`
8. `2026-01-01 — NEW_YEARS_OBSERVED`
9. `2026-04-03 — GOOD_FRIDAY`

These nine already belong to the authoritative `14 PASS / 0 BLOCKED / 0 FAIL` offline V2 readjudication.

Their immediate integration is **DEFERRED**, not rejected. Integrating all nine now would only move the execution-window state to `65 resolved / 3 unresolved`; the freeze would remain BLOCKED. No new information would be learned.

**Do not create Batch 16 / Batch 17 merely to re-process already-qualified outcomes.**

### Class B — 3 actual uncertain blockers

1. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
2. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Blocking reason:

`NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

Persisted captures for all three already establish:

- exact historical date honored;
- HTTP `200` navigation/document path;
- exact target instrument `USATECH.IDX/USD` / `9016`;
- raw payload present;
- runtime errors empty;
- `matching_records=[]`;
- no DOM witness line.

`2021-12-31` also has two independent historical attempts with the same no-positive-record result.

But existing route/protocol qualification explicitly forbids promoting empty/no-record responses into `NO_SPECIAL_CHANGE_EVIDENCE` without a separately qualified negative-evidence/completeness contract.

Therefore Class B — not Class A integration — is the current information bottleneck.

## Selected path

Before building a new browser or alternate broker route, first determine whether the **already persisted broker-native responses** can be qualified as complete negative evidence.

Candidate contract name:

`TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`

It must be offline/read-only and end in PASS / FAIL / BLOCKED.

It must never implement `matching_records=[] → PASS` directly.

At minimum it must reject:

1. HTTP `200` with missing raw payload;
2. date fallback / date not honored;
3. wrong or missing instrument identity;
4. parser/filter behavior that hides a raw target-instrument record;
5. raw payload containing a target-day overlapping record while normalized matches are empty;
6. incomplete/truncated/paginated response whose completeness is not proven;
7. route response scope that cannot prove the target day was fully represented;
8. adjacent-date or other-year absence borrowing;
9. runtime/network/selector errors presented as negative evidence;
10. provenance mismatch between runtime/artifact/digest/job/probe commit;
11. inconsistent repeated observations;
12. empty normalized result promoted without an independently proven completeness property.

If this contract PASSes and independently validates all three persisted Class-B captures, the later closure integration may combine:

- the nine already-qualified Class-A positive PASS dates;
- the three newly qualified Class-B negative-evidence PASS dates;

with the target state `68 / 68 resolved / 0 unresolved / 0 FAIL`, followed by an independent persisted-HEAD re-break.

If the Class-B completeness contract is BLOCKED, do **not** repeat the current browser capability. The next materially justified work becomes a capability explicitly addressing `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`, such as:

- `ALTERNATE_BROKER_NATIVE_RECORD_ROUTE`, or
- `BROKER_ARCHIVE_BACKFILL_ACCESS`.

Only the three Class-B dates need that route.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-PRE-BACKTEST-CRITICAL-PATH-9A-3B.md`
4. `reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-16.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`
6. `reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch01_runtime.json`
10. `reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`
11. `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`
12. `reports/data-qualification/historical_trading_breaks_recovery_batch14_runtime.json`
13. `04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`
14. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
15. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
16. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
17. compare active branch HEAD against the commit containing this checkpoint before any mutation.

## Exactly one next governed action

**Formalize and adversarially qualify an offline `TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1` candidate against the three already persisted Class-B captures, without browser access, without new capture, without calendar/ledger mutation, and without changing the current capability registry.**

Only after PASS / FAIL / BLOCKED may the system decide whether existing Class-B evidence is sufficient or a materially different broker-native route is required.

No Batch 16 freeze.  
No new browser capture.  
No `.bi5`.  
No real backtest.

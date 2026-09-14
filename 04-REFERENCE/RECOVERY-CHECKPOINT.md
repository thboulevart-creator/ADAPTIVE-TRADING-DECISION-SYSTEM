# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — ATTEMPT-AWARE TRADING BREAKS PROGRESSION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Global calendar:** `111 candidates / 30 resolved / 81 unresolved / 0 FAIL`
- **Candidate window:** `68 candidates / 7 resolved / 61 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Attempt-aware recovery progression:** PASS
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Historical attempt ledger entries:** `10`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `3`
- **Execution-eligible unresolved:** `58`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest executable calendar-evidence integration commit remains:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

Latest corrected progression-runtime commit:

`b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Latest progression qualification:

- run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- conclusion: **SUCCESS**
- adversarial/regression suite: **72 passed in 0.51s**

Session backup immediately preceding this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-PROGRESSION-PASS.md`

Backup commit:

`d55885702539823c6e127c608bf50fa837ec3c06`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-PROGRESSION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
10. `tools/trading_breaks_recovery_progression.py`
11. `tests/test_trading_breaks_recovery_progression.py`
12. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH02-POLICY.md`
13. `reports/data-qualification/historical_trading_breaks_recovery_batch02_qualification.md`
14. `reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`
15. `tools/trading_breaks_recovery_batch02.py`
16. `tests/test_trading_breaks_recovery_batch02.py`
17. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
18. `tools/trading_breaks_recovery_protocol.py`
19. `tests/test_trading_breaks_recovery_protocol.py`
20. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. CALENDAR EVIDENCE STATE — UNCHANGED BY PROGRESSION

The execution-window candidate remains exactly:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **7**
- unresolved/BLOCKED: **61**
- FAIL: **0**

Resolved in-window dates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted, shortened, or extended because unresolved dates remain.

`BLOCKED` still means unresolved. It does not populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 4. ATTEMPT-AWARE PROGRESSION — PASS

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Final verdict:

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

The progression layer now separates:

1. calendar evidence state;
2. immutable attempt history;
3. execution eligibility.

Authoritative attempt ledger:

`reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`

Authoritative material-change registry:

`reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

Current state:

- unresolved calendar dates: `61`
- historical attempts: `10`
- registered material capability changes: `0`
- already-attempted BLOCKED / execution-ineligible: `3`
- execution-eligible unresolved: `58`

The three already-attempted BLOCKED dates remain in calendar unresolved accounting but are not retry-eligible under the unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

Each is classified:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

Later never-attempted unresolved candidates remain eligible, so this prefix no longer causes starvation.

## 5. WHY THE FIRST NOMINAL PASS WAS NOT ACCEPTED

First adversarial run:

- run: `34890138036`
- job: `104130467209`
- suite: `67 passed`

A second adversarial review found two genuine bypasses after that nominal PASS:

1. a blocker-relevant `proof_capability` token could be added without a real route/protocol/capture change and masquerade as material capability change;
2. caller-provided attempts/current capability/change objects could inject unversioned retry authorization.

The workflow was paused, both boundaries were corrected minimally, and the corrected version was re-broken.

## 6. FINAL RE-BREAK

Final authoritative run:

- run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- conclusion: SUCCESS
- suite: `72 passed in 0.51s`
- runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

The final boundary rejects:

- identical-capability retries;
- provenance-only changes masquerading as semantic changes;
- version-label-only changes;
- proof-token-only changes;
- blocker-irrelevant capabilities;
- wrong fingerprints;
- false changed dimensions;
- proof-capability regression;
- missing/invalid material-change qualification provenance;
- caller-injected retry/scheduling state;
- hidden omission of unresolved dates;
- starvation;
- PASS/unresolved contradictions;
- silent retry after FAIL.

The progression qualification workflow is archived to `workflow_dispatch` only.

## 7. MATERIAL RETRY RULE — FROZEN

A previously BLOCKED date may become retry-eligible only through a versioned material-capability change that proves all required predicates, including:

- exact old/new capability fingerprints;
- a real change to route/protocol/capture implementation;
- a newly added blocker-relevant proof capability;
- no regression of existing proof capabilities;
- exact changed dimensions;
- explicit blocker coverage;
- qualification contract and exact qualification commit.

A new run/job/artifact/probe commit under the same semantic capability is not enough.

A proof-capability label by itself is not enough.

## 8. CURRENT BOUNDARY MATRIX

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 9. WHAT MUST NOT BE REPEATED

- do not convert BLOCKED attempts into resolved calendar state;
- do not remove BLOCKED dates from `recovery_queue()` merely because they were attempted;
- do not use raw `recovery_queue()[:5]` for the next batch;
- do not retry already-BLOCKED dates under unchanged semantic capability;
- do not treat new run/artifact/probe-commit provenance as material capability change;
- do not allow caller-injected retry authorization;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 03 with `BATCH_SIZE = 5` as exactly the first five entries of the governed `eligible_recovery_queue()`, BEFORE any Batch 03 historical observation.**

Batch 03 membership MUST be derived mechanically from `eligible_recovery_queue()` and locked before browser execution.

No candidate may be inserted, skipped, substituted, or reordered based on expected outcome, holiday type, apparent ease/difficulty, manual preference, or convenience.

This checkpoint does **not** itself define or freeze Batch 03 membership.

No `.bi5`. No real backtest.

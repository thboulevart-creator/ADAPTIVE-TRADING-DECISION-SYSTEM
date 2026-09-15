# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 08 INTEGRATION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 53 resolved / 58 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 30 resolved / 38 unresolved / 0 FAIL`
- **Historical Trading Breaks broker-evidence route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Attempt-aware recovery progression:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated
- **Recovery Batch 04:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 05:** PASS (`5 PASS / 0 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 06:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 07:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 08:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and **atomically integrated + persisted-HEAD re-break PASS**
- **Historical attempt ledger entries:** `40`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `10`
- **Execution-eligible unresolved:** `28`
- **First current eligible unresolved:** `2024-09-02 — LABOR_DAY`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Batch 09 membership:** NOT FROZEN
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-INTEGRATION-PASS.md`

Backup commit:

`48d34c744b2db4bf6b72f93ea47496fed4ea9df4`

Current boundary report commit:

`cef4e6c4410baae0b029e0a60ac974e5da58c1c1`

## 2. MANDATORY RECOVERY ORDER

Before the next substantive write:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch08_integration_qualification.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch08_adjudication.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch08_runtime.json`
8. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH08-POLICY.md`
9. `tools/trading_breaks_recovery_batch08.py`
10. `tools/trading_breaks_recovery_batch08_adjudication.py`
11. `tools/integrate_trading_breaks_recovery_batch08.py`
12. `tests/test_trading_breaks_recovery_batch08.py`
13. `tests/test_trading_breaks_recovery_batch08_adjudication.py`
14. `tests/test_trading_breaks_recovery_batch08_integration_contract.py`
15. `tests/test_trading_breaks_recovery_batch08_integration.py`
16. `tests/test_dukascopy_usatech_calendar_2024_batch08.py`
17. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
18. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
19. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
20. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
21. `tools/trading_breaks_recovery_progression.py`
22. `tests/test_trading_breaks_recovery_progression.py`
23. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
24. `tools/trading_breaks_recovery_protocol.py`
25. `tests/test_trading_breaks_recovery_protocol.py`
26. `tools/dukascopy_usatech_calendar.py`
27. `tools/dukascopy_usatech_calendar_coverage.py`
28. `tests/test_dukascopy_usatech_calendar_coverage.py`
29. `tests/test_coverage_execution_window_boundary.py`
30. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is source of truth. Do not reconstruct state from conversation memory.

## 3. BATCH 08 HISTORICAL FROZEN MEMBERSHIP

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

Freeze rule at freeze time:

`batch08_targets() == eligible_recovery_queue()[:5]`

This historical identity remains immutable. Do not compare it to the current eligible prefix as if it were supposed to remain live.

## 4. BATCH 08 EXECUTION / ADJUDICATION

Authoritative execution:

- run `34984538763`
- job `104433139005`
- probe commit `5cc4834af2c75de99f6e3427f31ab07b38b42611`
- runtime persistence commit `6136243c2fbe906a242546d3014a6ee78d30beeb`
- artifact `10402433119`
- artifact SHA-256 `644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd`
- pre-Chromium regression `307 passed in 1.47s`
- exact frozen identity gate PASS
- no-live-membership-recalculation gate PASS

Independent adjudication successful rerun:

- run `34985341285`
- job `104435886156`
- trigger `cb5d281b2097c751066dc08dd591e7384dc14376`
- evidence commit `c2c0ae35e61b5054c23ebbdba8f27d56c6c8380c`
- `117 passed in 0.40s`
- final `4 PASS / 1 BLOCKED / 0 FAIL`

Date-level adjudication:

- `2024-03-29` BLOCKED — no exact-target-date positive record; overlap record `66555` begins `2024-03-28T20:14:59Z`, never promoted.
- `2024-05-27` PASS — record `68242`, whole closed UTC hours `17..21`.
- `2024-06-19` PASS — record `69037`, whole closed UTC hours `17..21`.
- `2024-07-03` PASS — record `69819`, start `17:14:59Z`; only whole UTC hours `18..21` encoded closed.
- `2024-07-04` PASS — record `69820`, whole closed UTC hours `17..21`.

Adjudication harness note: first persistence run `34985087276` passed all substantive gates but failed on Markdown EOF whitespace only. Minimal correction, complete rerun PASS. No governed state mutation in the failed run.

## 5. BATCH 08 ATOMIC INTEGRATION — PASS

Authoritative integrated commit:

`aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74`

Successful integration:

- run `34987791998`
- job `104444271495`
- trigger `8aef1091193ae117d404f58573370ea9092b6c8c`
- pre-mutation integration contract `79 passed in 0.33s`
- post-mutation regression `335 passed in 1.62s`
- exact post-state assertion PASS
- integration executable AST no-browser/no-capture/no-live-membership path PASS

Atomic persisted mutations:

- added only PASS dates `2024-05-27`, `2024-06-19`, `2024-07-03`, `2024-07-04` to executable calendar evidence;
- appended all five factual Batch08 attempts as sequences `36..40`;
- attempt outcomes `[BLOCKED, PASS, PASS, PASS, PASS]` in frozen order;
- `2024-03-29` remains unresolved and absent from positive/negative executable evidence;
- `2024-03-29` now has progression reason `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- progression regenerated deterministically;
- capability registry unchanged.

Integration qualification:

`reports/data-qualification/historical_trading_breaks_recovery_batch08_integration_qualification.md`

Integration harness note: initial run `34987503866` / job `104443288047` stopped before mutation at `78 PASS / 1 FAIL` because a source-text scanner detected `playwright` inside a string literal for a future test. The guard was minimally converted to executable AST inspection. No governed state mutation occurred in that failed run.

## 6. BATCH 08 INDEPENDENT PERSISTED-HEAD RE-BREAK — PASS

Final verifier trigger commit:

`d996d1e3573bfc36437710cc95510ca73b519650`

Final verifier:

- run `34988096558`
- job `104445314023`
- token permissions `contents: read`, `metadata: read`
- exact detached persisted HEAD checkout PASS
- integration commit ancestry PASS
- governed-state immutability since `aa85a2a...` PASS
- full regression `335 passed in 1.47s`
- exact persisted accounting PASS
- deterministic progression regeneration and tracked `git diff --exit-code` PASS
- clean worktree assertion PASS

Verifier harness note: initial verifier `34987958976` / job `104444833841` passed all substantive proofs but failed final cleanliness because Python created untracked `tests/__pycache__/` and `tools/__pycache__/`. Tracked diff was already clean. `PYTHONDONTWRITEBYTECODE=1` was added and the complete verifier rerun passed. No governed state changed.

## 7. FINAL POST-BATCH08 STATE

- global `111 / 53 resolved / 58 unresolved / 0 FAIL`
- execution window `68 / 30 resolved / 38 unresolved / 0 FAIL`
- ledger `40`
- capability changes `0`
- same-capability attempted BLOCKED/ineligible `10`
- eligible unresolved `28`
- first current eligible unresolved `2024-09-02 — LABOR_DAY`

Ten same-capability attempted BLOCKED dates remain unresolved/ineligible. The new tenth member is `2024-03-29 — GOOD_FRIDAY`.

## 8. WORKFLOW CLOSURE

Completed Batch08 workflows are manual-only.

- integration archive commit: `f4e86e45546e2fc32ff1dae8124115250bf59247`
- persisted-HEAD verifier archive commit: `550420e66a1d687a37ce645764ff0edb0c7c1b64`

Membership, execution and adjudication workflows were already archived.

## 9. CURRENT DOWNSTREAM BOUNDARY

PASS now includes:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_PERSISTED_HEAD_REBREAK`

Still BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 09 from the persisted post-Batch08 `eligible_recovery_queue()`, then adversarially break its membership before any browser/Chromium observation.**

Rules:

- do NOT manually choose Batch09 members;
- recompute the governed `eligible_recovery_queue()` from the persisted current GitHub state;
- apply the governed fixed-size prefix rule and verify the current protocol/policy pattern before freezing;
- freeze/version membership before observation;
- no skip, reorder, substitution, expansion, shortening or outcome-based selection;
- the currently proven first eligible entry is `2024-09-02 — LABOR_DAY`, but derive all remaining members from GitHub rather than conversation memory;
- same branch; no auxiliary branch proliferation;
- no `.bi5`;
- no real backtest.

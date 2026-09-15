# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 08 EXECUTION + ADJUDICATION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 49 resolved / 62 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 26 resolved / 42 unresolved / 0 FAIL`
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
- **Recovery Batch 08 membership:** PASS — immutable and frozen before observation
- **Recovery Batch 08 execution/adjudication:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) — **NOT YET INTEGRATED**
- **Historical attempt ledger entries:** `35` — pre-Batch08-integration persisted state
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `9` — pre-Batch08-integration persisted state
- **Persisted execution-eligible unresolved:** `33` — **STALE FOR BATCH 09 SCHEDULING**
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Batch 09 membership:** NOT FROZEN
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-ADJUDICATION-PASS.md`

Backup commit:

`9aa05d5dc982421f6308aae9a22302661ef20e3f`

Current boundary report commit:

`35cfe8655603d79e0807d1386a81e6a769a456e4`

## 2. MANDATORY RECOVERY ORDER

Before the next substantive write:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-ADJUDICATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH08-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch08_policy_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch08_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch08_adjudication.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch08_qualification.md`
10. `tools/trading_breaks_recovery_batch08.py`
11. `tools/trading_breaks_recovery_batch08_execute.py`
12. `tools/trading_breaks_recovery_batch08_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch08.py`
14. `tests/test_trading_breaks_recovery_batch08_adjudication.py`
15. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
16. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
17. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
18. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
19. `tools/trading_breaks_recovery_progression.py`
20. `tests/test_trading_breaks_recovery_progression.py`
21. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
22. `tools/trading_breaks_recovery_protocol.py`
23. `tests/test_trading_breaks_recovery_protocol.py`
24. `tools/dukascopy_usatech_calendar.py`
25. `tools/dukascopy_usatech_calendar_coverage.py`
26. `tests/test_dukascopy_usatech_calendar_coverage.py`
27. `tests/test_coverage_execution_window_boundary.py`
28. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is source of truth. Do not reconstruct state from conversation memory.

## 3. BATCH 08 FROZEN MEMBERSHIP

Freeze baseline checkpoint:

`2e9e51cea8342c701eec14d8d86aca215c5b7b62`

Membership qualification:

- run `34967834638`
- job `104376461078`
- trigger commit `7e0fc3268d6ec202267ecf71efe69b0e593be4ea`
- `307 passed in 1.46s`

Frozen exact membership:

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

Selection rule at freeze:

`batch08_targets() == eligible_recovery_queue()[:5]`

Execution/adjudication MUST continue to consume the immutable frozen tuple, never a live queue.

## 4. BATCH 08 AUTHORITATIVE BROWSER EXECUTION — PASS

Execution workflow:

- run `34984538763`
- job `104433139005`
- trigger/probe commit `5cc4834af2c75de99f6e3427f31ab07b38b42611`
- runtime persistence commit `6136243c2fbe906a242546d3014a6ee78d30beeb`
- artifact `10402433119`
- artifact SHA-256 `644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd`
- pre-browser governed regression `307 passed in 1.47s`
- exact frozen identity gate PASS
- no-live-membership-recalculation gate PASS
- Chromium installed only after all pre-browser gates passed

Runtime:

`reports/data-qualification/historical_trading_breaks_recovery_batch08_runtime.json`

## 5. BATCH 08 INDEPENDENT ADJUDICATION — PASS

Authoritative successful rerun:

- run `34985341285`
- job `104435886156`
- trigger commit `cb5d281b2097c751066dc08dd591e7384dc14376`
- adversarial/parent suite `117 passed in 0.40s`
- final adjudication persistence commit `c2c0ae35e61b5054c23ebbdba8f27d56c6c8380c`
- final result `4 PASS / 1 BLOCKED / 0 FAIL`
- no browser/probe/live-queue path PASS

Final date outcomes:

- `2024-03-29 — GOOD_FRIDAY` — BLOCKED `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`; overlap record `66555` begins `2024-03-28T20:14:59Z` and MUST NOT be promoted to exact-target PASS.
- `2024-05-27 — MEMORIAL_DAY` — PASS — record `68242`.
- `2024-06-19 — JUNETEENTH_OBSERVED` — PASS — record `69037`.
- `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION` — PASS — record `69819`; start `17:14:59Z`, so only `[18,19,20,21]` are fully closed.
- `2024-07-04 — INDEPENDENCE_DAY_OBSERVED` — PASS — record `69820`.

Reports:

- `reports/data-qualification/historical_trading_breaks_recovery_batch08_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch08_qualification.md`

## 6. SAFE PERSISTENCE CORRECTION

The first independent adjudication run:

- run `34985087276`
- job `104435014275`
- adversarial suite `117 passed in 0.36s`
- substantive adjudication `4 PASS / 1 BLOCKED / 0 FAIL` PASS

It failed only at final report persistence because `git diff --cached --check` detected a blank line at EOF in the generated Markdown.

No governed calendar, attempt ledger, capability registry or progression state was mutated by that failure.

A minimal persistence-only EOF normalization was committed at:

`cb5d281b2097c751066dc08dd591e7384dc14376`

The entire independent adjudication chain was then rerun and passed, including report persistence.

## 7. STATE MUTATION BOUNDARY — BATCH 08 NOT INTEGRATED

The Batch 08 observations are now factual evidence, but they have not yet been integrated into the executable calendar or attempt-aware progression.

Persisted state therefore remains:

- global `111 / 49 resolved / 62 unresolved / 0 FAIL`
- execution window `68 / 26 resolved / 42 unresolved / 0 FAIL`
- attempt ledger `35`
- material capability changes `0`
- attempted BLOCKED/ineligible `9`
- eligible unresolved `33`

The value `33` is stale for scheduling because the five Batch 08 factual attempts are not yet in the ledger and the four PASS results are not yet in executable calendar evidence.

**Do not freeze Batch 09 before Batch 08 atomic integration and persisted-HEAD re-break PASS.**

## 8. WORKFLOW CLOSURE

The following Batch 08 workflows are archived to `workflow_dispatch` only:

- `.github/workflows/trading-breaks-recovery-batch08-policy.yml`
- `.github/workflows/trading-breaks-recovery-batch08.yml`
- `.github/workflows/trading-breaks-recovery-batch08-adjudication.yml`

Normal pushes cannot silently re-freeze, re-execute or re-adjudicate Batch 08.

## 9. CURRENT DOWNSTREAM BOUNDARY

PASS now includes:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_EXECUTION_ADJUDICATION`

Still BLOCKED:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ATOMIC_INTEGRATION — NOT YET EXECUTED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Integrate Batch 08 atomically: add only `2024-05-27`, `2024-06-19`, `2024-07-03` and `2024-07-04` to executable calendar evidence; append all five factual Batch 08 attempts to the ledger; leave `2024-03-29` unresolved and make it `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`; regenerate progression; adversarially re-break calendar/coverage/progression; then independently verify the persisted HEAD before any Batch 09 membership freeze.**

Before integration, verify the current ledger and derive the next attempt sequence numbers from persisted GitHub state rather than assuming them.

Do not recalculate Batch 08 membership. No Batch 09 before integration + persisted-HEAD re-break PASS. No `.bi5`. No real backtest.

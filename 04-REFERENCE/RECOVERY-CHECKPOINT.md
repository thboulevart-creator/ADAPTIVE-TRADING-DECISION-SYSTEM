# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS BATCH 03 MEMBERSHIP PASS

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
- **Batch 03 membership policy:** PASS — frozen before observation
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Historical attempt ledger entries:** `10`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `3`
- **Execution-eligible unresolved before Batch 03 execution:** `58`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest executable calendar-evidence integration commit remains:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

Latest corrected progression-runtime commit:

`b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Batch 03 membership qualification:

- run: `34891341634`
- job: `104134524746`
- trigger commit: `4260fd7c91fe855aeb0ff99c70ceb7458d593993`
- conclusion: **SUCCESS**
- suite: **84 passed in 0.39s**
- exact membership assertion: **PASS**
- browser/probe execution-path guard: **PASS**

Session backup immediately preceding this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH03-MEMBERSHIP-PASS.md`

Backup commit:

`ed11c54a185038c58506a31b7daa669eb08e99c2`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH03-MEMBERSHIP-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH03-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch03_policy_qualification.md`
7. `tools/trading_breaks_recovery_batch03.py`
8. `tests/test_trading_breaks_recovery_batch03.py`
9. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
10. `reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`
11. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
12. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
13. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
14. `tools/trading_breaks_recovery_progression.py`
15. `tests/test_trading_breaks_recovery_progression.py`
16. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
17. `tools/trading_breaks_recovery_protocol.py`
18. `tests/test_trading_breaks_recovery_protocol.py`
19. `LOCAL-EVIDENCE/README.md`
20. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
21. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. CALENDAR EVIDENCE STATE — UNCHANGED

The execution-window candidate remains exactly:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **7**
- unresolved/BLOCKED: **61**
- FAIL: **0**

Resolved in-window dates remain:

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

Current state before Batch 03 execution:

- unresolved calendar dates: `61`
- historical attempts: `10`
- registered material capability changes: `0`
- already-attempted BLOCKED / execution-ineligible: `3`
- execution-eligible unresolved: `58`

The three already-attempted BLOCKED dates remain unresolved but are not retry-eligible under the unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

Each is classified:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

## 5. BATCH 03 MEMBERSHIP — FROZEN AND PASS

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Verdict:

**PASS — `BATCH03_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Frozen size:

`BATCH_SIZE = 5`

Selection rule at freeze:

`eligible_recovery_queue()[:5]`

Immutable Batch 03 membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Every member was proven to be `INITIAL_ATTEMPT`, unresolved, eligible, unattempted, chronological and unique at freeze time.

Raw `recovery_queue()[:5]` is not an admissible Batch 03 selection source.

Freeze provenance:

- pre-freeze checkpoint HEAD: `d4dab0a10ba6bc782186159899f7b8225e7aab59`
- source progression runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 6. BATCH 03 QUALIFICATION HISTORY

First run:

- run: `34891254793`
- job: `104134235510`
- trigger commit: `3fa23b7027d722ce474d2a7dc9034a79233e5176`
- suite: `84 passed in 0.59s`
- exact membership assertion: PASS
- final browser guard: false positive

The false positive was caused by a self-referential string search: the guard searched for `playwright install` while that literal appeared inside its own assertion. It did not indicate browser execution or membership failure.

The guard was corrected minimally and the full suite was rerun.

Authoritative corrected re-break:

- run: `34891341634`
- job: `104134524746`
- trigger commit: `4260fd7c91fe855aeb0ff99c70ceb7458d593993`
- conclusion: SUCCESS
- suite: `84 passed in 0.39s`
- exact frozen membership assertion: PASS
- no-browser/probe execution-path guard: PASS

The Batch 03 freeze tool contains membership only and no Playwright, Chromium, `probe_candidate`, or asyncio execution path.

No Batch 03 historical observation has occurred yet.

The Batch 03 policy qualification workflow is archived to `workflow_dispatch` only.

## 7. LOCAL ZIP EVIDENCE — CONFIRMED PASS

The three retained ZIP archives are correctly governed locally.

Versioned manifest:

`LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

`LOCAL-EVIDENCE/README.md` records successful local placement and independent SHA-256 verification of all three archives.

The ZIP binaries themselves remain intentionally ignored by Git. Their names, sizes, roles, artifact IDs, workflow runs and SHA-256 hashes are versioned in the manifest.

No corrective action is required for these three ZIPs.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 9. WHAT MUST NOT BE REPEATED

- do not redefine or recalculate Batch 03 membership after outcomes become known;
- do not use raw `recovery_queue()[:5]` for Batch 03;
- do not reinsert the three identical-capability BLOCKED dates;
- do not convert BLOCKED attempts into resolved calendar state;
- do not treat new run/artifact/probe-commit provenance as material capability change;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Execute the already-frozen Batch 03 membership under the qualified Trading Breaks capture/adjudication chain, with all parent/progression/Batch 03 gates passing before Chromium opens.**

The execution MUST use exactly these five frozen dates and this exact order:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Membership MUST NOT be recalculated, substituted, expanded, shortened, or reordered according to observed or expected outcomes.

After execution, independently adjudicate all five dates under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`, integrate only genuine PASS evidence, preserve BLOCKED as unresolved, append all five factual attempts to the attempt ledger with exact provenance/capability identity, and rerun coverage/progression regressions as required.

No `.bi5`. No real backtest.

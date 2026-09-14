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
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`)
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Historical attempt ledger entries:** `15`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `4`
- **Execution-eligible unresolved:** `53`
- **First currently eligible unresolved:** `2022-11-24 — THANKSGIVING_DAY`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest atomic Batch 03 calendar/attempt integration commit:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Session backup immediately preceding this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH03-PASS.md`

Backup commit:

`05488b9dd25a625d26d4ecd1fe5e41c1663e6e7f`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH03-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH03-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch03_policy_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch03_qualification.md`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch03_adjudication.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`
10. `tools/trading_breaks_recovery_batch03.py`
11. `tools/trading_breaks_recovery_batch03_execute.py`
12. `tools/trading_breaks_recovery_batch03_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch03.py`
14. `tests/test_trading_breaks_recovery_batch03_adjudication.py`
15. `tests/test_trading_breaks_recovery_batch03_integration.py`
16. `tests/test_dukascopy_usatech_calendar_2022_batch03.py`
17. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
18. `reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`
19. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
20. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
21. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
22. `tools/trading_breaks_recovery_progression.py`
23. `tests/test_trading_breaks_recovery_progression.py`
24. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
25. `tools/trading_breaks_recovery_protocol.py`
26. `tests/test_trading_breaks_recovery_protocol.py`
27. `LOCAL-EVIDENCE/README.md`
28. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
29. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. CALENDAR EVIDENCE STATE AFTER BATCH 03

The execution-window candidate remains exactly:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **11**
- unresolved/BLOCKED: **57**
- FAIL: **0**

Resolved in-window dates:

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

The window MUST NOT be shifted, shortened, or extended because unresolved dates remain.

`BLOCKED` still means unresolved. It does not populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 4. BATCH 03 MEMBERSHIP — HISTORICALLY FROZEN

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Frozen membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

The membership was frozen from the governed attempt-aware eligible queue before browser observation. It was not recalculated after outcomes became known.

## 5. BATCH 03 AUTHORITATIVE EXECUTION

Authoritative browser runtime:

- run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- conclusion: SUCCESS

Independent date-level verdicts:

- `2022-05-30` → **PASS** — broker record `37019`, Memorial Day, fully closed hours `17–21 UTC`
- `2022-06-20` → **PASS** — broker record `38945`, Juneteenth Holiday, fully closed hours `17–21 UTC`
- `2022-07-01` → **BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED**
- `2022-07-04` → **PASS** — broker record `41225`, Independence Day, fully closed hours `17–21 UTC`
- `2022-09-05` → **PASS** — broker record `42569`, Labor Day, fully closed hours `17–21 UTC`

Only the four PASS dates entered executable calendar evidence.

## 6. ADVERSARIAL ADJUDICATION HISTORY

First adjudication run:

- run: `34892773715`
- job: `104139273746`
- result: FAIL before final acceptance

It exposed a representation defect: the DOM exposes human name `USATECH.IDX/USD`; the network payload exposes Dukascopy ID `9016`. The initial adapter compared the two representations directly.

Minimal correction:

- validate exact DOM human name first;
- normalize to governed ID `9016` only after that validation;
- attack incorrect DOM instrument names explicitly.

Corrected re-break:

- run: `34893116066`
- job: `104140394051`
- conclusion: SUCCESS
- suite: `62 passed`
- adjudication: `4 PASS / 1 BLOCKED / 0 FAIL`
- persisted adjudication commit: `a46e48ee4e4b1828e28418bfca1a0f84fd795b19`

## 7. ADVERSARIAL INTEGRATION HISTORY

First atomic integration run:

- run: `34893471211`
- job: `104141565466`
- result: FAIL
- integration commit pushed: **NO**

It exposed:

1. a stale historical Batch 02 current-count assertion;
2. historical Batch 03 replay being incorrectly tied to mutable live `recovery_queue()`.

The second issue was corrected by separating:

- live execution validation, which remains tied to the current unresolved queue and cannot re-enable resolved dates;
- historical replay validation, which is bound to the immutable frozen Batch 03 scope and is used only for reproducibility/adjudication.

Frozen replay rejects malformed/empty scope, duplicates, non-chronological scope, absent targets and reason substitutions. It does not change the live queue.

This correction did not change the semantic broker evidence capability, registered no material capability change and required no new browser observation.

Final atomic integration:

- run: `34893854678`
- job: `104142824703`
- conclusion: SUCCESS
- suite: `104 passed`
- integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Calendar evidence and all five attempt facts were persisted atomically.

## 8. INDEPENDENT PERSISTED-HEAD RE-BREAK

After the integration commit was already persisted:

- run: `34893976903`
- job: `104143235284`
- conclusion: SUCCESS
- suite: `104 passed in 0.60s`

Independently confirmed:

- global accounting: `111 / 34 / 77`
- execution-window accounting: `68 / 11 / 57`
- evidence-shape errors: `0`
- orphan evidence: `0`
- contradictory evidence: `0`
- historical attempts: `15`
- registered material capability changes: `0`
- attempted BLOCKED / ineligible: `4`
- execution-eligible unresolved: `53`
- first currently eligible unresolved: `2022-11-24 — THANKSGIVING_DAY`

## 9. ATTEMPT-AWARE PROGRESSION AFTER BATCH 03

The four attempted BLOCKED dates remain unresolved but cannot be replayed under unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Each is governed by:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

They remain in calendar unresolved accounting but are excluded from the current execution projection.

## 10. WORKFLOW AND LOCAL-EVIDENCE CLOSURE

The Batch 03 membership-policy, browser execution, independent adjudication, atomic integration and persisted-HEAD regression workflows are archived to `workflow_dispatch` only.

The three previously retained local ZIP archives remain correctly governed and PASS. Their binaries remain intentionally outside Git while their filenames, roles, artifact/run identities and SHA-256 hashes remain versioned in:

- `LOCAL-EVIDENCE/README.md`
- `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

No corrective ZIP action is required.

## 11. CURRENT BOUNDARY MATRIX

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 04 with `BATCH_SIZE = 5` as exactly the first five entries of the current governed `eligible_recovery_queue()`, BEFORE any Batch 04 historical observation.**

Batch 04 membership MUST be derived mechanically at freeze time and versioned before browser execution. No candidate may be inserted, skipped, substituted or reordered based on expected outcome, holiday type, apparent ease/difficulty, source availability, manual preference or convenience.

This checkpoint does **not** define or freeze Batch 04 membership. The only current progression fact recorded for orientation is that `2022-11-24 — THANKSGIVING_DAY` is the first eligible unresolved candidate.

No `.bi5`. No real backtest.

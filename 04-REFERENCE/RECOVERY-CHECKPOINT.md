# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 02 PASS

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
- **Latest persisted-HEAD calendar/boundary regression:** `70 PASS`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest executable-evidence integration commit:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

Latest independent calendar-regression run:

- run: `34888592937`
- job: `104125313335`
- conclusion: **SUCCESS**
- pytest: **70 passed in 0.57s**

Session backup immediately preceding this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH02-PASS.md`

Backup commit:

`8c511ad20f1e148268457d5b644c51caf42e2cc1`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH02-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH02-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch02_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`
8. `tools/trading_breaks_recovery_batch02.py`
9. `tests/test_trading_breaks_recovery_batch02.py`
10. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH-POLICY.md`
11. `reports/data-qualification/historical_trading_breaks_recovery_batch01_qualification.md`
12. `tools/trading_breaks_recovery_batch01.py`
13. `tests/test_trading_breaks_recovery_batch01.py`
14. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
15. `tools/trading_breaks_recovery_protocol.py`
16. `tests/test_trading_breaks_recovery_protocol.py`
17. `04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`
18. `LOCAL-EVIDENCE/README.md`
19. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
20. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. EXECUTION-WINDOW BOUNDARY — UNCHANGED

Window-selection contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Selected candidate:

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

The window MUST NOT be shifted, shortened, or extended because recovery remains incomplete.

## 4. HISTORICAL BROKER-EVIDENCE ROUTE — PASS

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

Target broker instrument:

- `USATECH.IDX/USD`
- Dukascopy instrument ID `9016`

The route remains qualified for **positive exact historical break records only**.

Empty/no-record evidence remains:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

Neighboring-date/overlapping records do not become exact-target evidence merely because they cover the target date.

Absence MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 5. SYSTEMATIC RECOVERY PROTOCOL — PASS

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

The protocol remains the mandatory date-level adjudication boundary. It rejects queue/date/instrument drift, empty-response promotion, missing raw payload, malformed intervals, neighboring-date substitution, DOM/network contradiction, missing/invalid provenance, incorrect reopen semantics, and partial-hour rounding.

## 6. BATCH 01 — HISTORICAL IMMUTABLE PASS

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Frozen size:

`BATCH_SIZE = 5`

Outcome:

- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Authoritative runtime:

- run: `34885895206`
- job: `104116336235`
- probe commit: `479900e05eebc6e2c29e0f9f3bddfdfc78e78224`
- artifact: `10364872726`
- SHA-256: `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`

Batch 01 workflow is archived to manual-only and membership remains immutable.

## 7. BATCH 02 POLICY — FROZEN BEFORE OUTCOMES

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1`

Frozen size:

`BATCH_SIZE = 5`

Immutable Batch 02 membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

Policy/tool/tests were versioned before any new Batch 02 browser observation. No candidate was skipped or substituted according to expected outcome.

## 8. BATCH 02 AUTHORITATIVE EXECUTION

- workflow run: `34888022168`
- job: `104123381873`
- probe commit: `619a0200a9718827346d3c5458d1c1a290f3e5ce`
- artifact: `10364984459`
- artifact SHA-256: `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- conclusion: **SUCCESS**
- read-only: true
- market data written: false

Independent adjudication:

- `2021-12-24` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**
- `2021-12-31` → **BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED**
- `2022-01-17` → **PASS — EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED**
- `2022-02-21` → **PASS — EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED**
- `2022-04-15` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**

Overall Batch 02:

**PASS — `BATCH02_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

Only the two PASS records were integrated.

Batch 02 execution workflow is archived to manual-only after completion.

## 9. BATCH 02 EXECUTABLE EVIDENCE

### 2022-01-17 — Martin Luther King Day

- record: `32811`
- start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- exact DOM/network witness: concordant

### 2022-02-21 — Presidents Day

- record: `33515`
- start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- broker reason: `Presidents Day and Washington's Birthday`
- exact DOM/network witness: concordant

Persisted executable-evidence commit:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

The three BLOCKED dates remain unresolved and absent from `SPECIAL_SESSION_EVIDENCE`.

## 10. POST-BATCH-02 REGRESSION

Integration validation:

- run: `34888531830`
- job: `104125107659`
- conclusion: **SUCCESS**
- pytest: **98 passed in 0.74s**
- global assertions: `111 / 30 resolved / 81 unresolved`
- execution-window assertions: `68 / 7 resolved / 61 unresolved`

Independent persisted-HEAD calendar regression:

- run: `34888592937`
- job: `104125313335`
- conclusion: **SUCCESS**
- pytest: **70 passed in 0.57s**
- candidate dates: `111`
- resolved: `30`
- unresolved: `81`
- orphan evidence: `0`
- contradictory evidence: `0`
- evidence-shape errors: `0`

The global and execution-window verdicts therefore remain legitimately **BLOCKED because unresolved dates remain**, not because of a regression, contradiction, or FAIL date.

## 11. CURRENT RECOVERY QUEUE AND STARVATION BOUNDARY

Current in-window unresolved queue size:

`61`

First unresolved candidate:

`2021-12-24 — CHRISTMAS_OBSERVED`

Last unresolved candidate:

`2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Important: the unresolved queue intentionally still contains Batch 02 BLOCKED dates, including:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`

This is correct evidence accounting. **BLOCKED is not resolved.**

However, Batch 02 exposes a new scheduling boundary: using raw `recovery_queue()[:5]` for Batch 03 would automatically reselect already-attempted BLOCKED dates under the same unchanged evidence capability, and repeated use could starve later unresolved dates indefinitely.

Therefore the system must now distinguish:

1. **calendar evidence state** — resolved PASS versus unresolved/BLOCKED;
2. **recovery attempt state** — whether a date was attempted, under which route/protocol/runtime capability identity, and with what outcome;
3. **batch execution eligibility** — whether another attempt is justified now.

This separation MUST NOT alter the unresolved accounting.

## 12. RETRY / PROGRESSION RULE THAT MUST BE FORMALIZED NEXT

A previously attempted BLOCKED date may not be silently retried simply because it remains first in the unresolved queue.

A retry must require an explicit deterministic predicate tied to a material change such as a newly qualified evidence route, protocol capability, or runtime evidence capability that can plausibly address the prior blocking reason.

The future progression contract must reject:

- hiding BLOCKED dates from coverage accounting;
- marking them resolved without evidence;
- turning no-record into negative evidence;
- manual/discretionary skipping;
- retrying the same date indefinitely under an unchanged capability;
- selecting later dates based on expected outcome;
- starvation of later unresolved candidates.

## 13. CURRENT BOUNDARY MATRIX

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02 = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 14. WORKSTREAM HYGIENE

An accidental auxiliary branch `__invalid_noop__` created during connector-capability probing in this session was deleted with a narrowly scoped temporary workflow. The temporary cleanup workflow was then removed. This branch is not part of project history and must not be recreated.

Cleanup workflow removal commit:

`56a9349249768684e7dca4c73c0feb7a5f9d95c6`

Do not alter unrelated historical auxiliary branches merely because they exist.

## 15. WHAT MUST NOT BE REPEATED

- do not rerun Batch 01 or Batch 02 merely because BLOCKED dates remain unresolved;
- do not infer normal trading from empty/no-record responses;
- do not use neighboring-date records as exact-target proof;
- do not hide attempted BLOCKED dates from unresolved accounting;
- do not define Batch 03 from raw `recovery_queue()[:5]` until progression eligibility is governed;
- do not move the execution window;
- do not download massive `.bi5` data;
- do not start a real backtest.

## 16. EXACTLY ONE NEXT GOVERNED ACTION

**Formalize and adversarially qualify an attempt-aware recovery progression contract before defining Batch 03.**

The contract must preserve every BLOCKED date as unresolved calendar evidence while creating a separate deterministic execution-eligibility layer based on recovery-attempt history and capability identity. It must prevent identical-route BLOCKED dates from starving later unresolved candidates and allow retry only through an explicit material-capability-change predicate.

Required sequence:

1. formalize attempt identity / attempt ledger / eligibility / retry predicate;
2. adversarially break queue starvation, silent skipping, hidden reclassification, duplicate identical-capability retries, and outcome-based selection paths;
3. correct the smallest boundary necessary;
4. re-break and issue PASS/FAIL/BLOCKED;
5. only after PASS, derive and freeze Batch 03 membership before observing Batch 03 outcomes.

No `.bi5`. No real backtest.

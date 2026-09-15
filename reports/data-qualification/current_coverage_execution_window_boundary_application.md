# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 05 atomic integration + persisted-HEAD re-break PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 42 resolved / 69 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 19 resolved / 49 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware progression: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — atomically integrated + persisted-HEAD re-break PASS**
- Historical attempt ledger entries: **25**
- Registered material capability changes: **0**
- Attempted BLOCKED / execution-ineligible: **6**
- Execution-eligible unresolved: **43**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 05 immutable membership and adjudicated records

Frozen membership:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

Authoritative browser execution:

- workflow run: `34947146056`
- job: `104309150262`
- probe commit: `33ae476c48372bce64421a411066db2ddea6125c`
- artifact: `10386998786`
- artifact SHA-256: `ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c`

Independent adjudication: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL**.

Integrated records:

1. `2023-01-16` → broker record `49338`, whole closed UTC hours `18–22`.
2. `2023-02-20` → broker record `50456`, whole closed UTC hours `18–22`.
3. `2023-04-07` → broker record `52290`, exact start `14:14Z`; only target-day whole closed UTC hours `15–23` are encoded although the broker interval spans the weekend.
4. `2023-05-29` → broker record `54373`, whole closed UTC hours `17–21`.
5. `2023-06-19` → broker record `55281`, whole closed UTC hours `17–21`.

No cross-date evidence was promoted and no partial start hour was rounded to a full closed hour.

## Batch 05 atomic integration qualification

Authoritative integration workflow:

- workflow run: `34949197265`
- job: `104315829990`
- conclusion: **SUCCESS**
- pre-mutation adversarial qualification: **76 passed**
- post-mutation adversarial regression: **166 passed**
- atomic integration commit: `99c2f38842a0c4ea66ba6ff90496380986d02e52`
- qualification report: `reports/data-qualification/historical_trading_breaks_recovery_batch05_integration_qualification.md`

The single atomic integration commit:

- added exactly the five independently adjudicated PASS records to executable calendar evidence;
- appended exactly five factual Batch 05 attempts as immutable sequences `21..25`, all `PASS`;
- regenerated the progression runtime;
- preserved all six historical same-capability BLOCKED dates as unresolved and execution-ineligible;
- registered no material capability change;
- did not populate negative evidence from an empty record or cross-date witness.

## Independent persisted-HEAD re-break

First re-break attempt:

- workflow run: `34949393807`
- job: `104316469582`
- persisted-state adversarial suite: **166 passed in 0.74s**
- exact persisted calendar/ledger/progression assertion: **PASS**
- overall run: **FAIL**, solely because the browser-free self-check searched for forbidden strings that were literally present in its own search list.

This was a self-referential guard false positive, not a calendar, ledger, progression, provenance, or integration failure. The only correction fragmented the self-check search tokens; no executable data or integration semantics were changed.

Corrected authoritative re-break:

- workflow run: `34949499981`
- job: `104316813519`
- verified commit: `70428e536689793a74420d35c84744b8ad0f2f3d`
- conclusion: **SUCCESS**
- adversarial regression: **166 passed in 0.99s**
- exact persisted calendar / ledger / progression assertion: **PASS**
- no-browser/no-capture-path guard: **PASS**
- deterministic progression regeneration + `git diff --exit-code`: **PASS**
- workflow permissions: `contents: read`, `metadata: read`

The integration and persisted-HEAD workflows are archived to `workflow_dispatch` only after completion.

## Persisted progression state after Batch 05

- calendar unresolved in execution window: **49**
- attempt ledger: **25**
- registered material capability changes: **0**
- attempted BLOCKED / execution-ineligible: **6**
- execution-eligible unresolved: **43**
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The six historical same-capability BLOCKED dates remain unresolved and execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each remains:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

The first currently execution-eligible unresolved date is `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`. This is progression state only; **Batch 06 membership has not yet been frozen**.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_PERSISTED_HEAD_REBREAK`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 06 from the persisted post-Batch05 `eligible_recovery_queue()`, then adversarially break its membership before any Chromium/browser observation.**

Batch 06 has **not** been frozen in this action. Its membership must be mechanically derived from the persisted eligible queue under the same governance rules; no manual substitution, skipping, reorder, or outcome-based selection is permitted.

No `.bi5`. No real backtest.

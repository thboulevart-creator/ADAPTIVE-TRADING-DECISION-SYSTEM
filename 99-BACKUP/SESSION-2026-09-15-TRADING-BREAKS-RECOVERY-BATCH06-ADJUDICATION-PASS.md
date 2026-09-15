# SESSION BACKUP — 15 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 06 EXECUTION + ADJUDICATION PASS

## Final session verdict

**PASS — `BATCH06_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Batch 06 was executed only after every parent/progression/frozen-membership gate passed before Chromium installation/opening. The five results were then adjudicated by a separate browser-free replay boundary.

Final accounting:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

No calendar integration was performed in this session.

## Frozen Batch 06 membership

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

This membership remains immutable.

## Browser execution

Execution runner:

`tools/trading_breaks_recovery_batch06_execute.py`

Runner creation commit:

`ae98364bfd5f9f3cbecd3de1137a4fbca4dd792b`

Execution workflow:

`.github/workflows/trading-breaks-recovery-batch06.yml`

Workflow trigger/probe commit:

`e968db2be1fbfd4d2c419f9dad717ca479b52edd`

Authoritative execution:

- run: `34954308324`
- job: `104332522379`
- conclusion: SUCCESS
- pre-browser suite: `170 passed in 0.72s`
- exact frozen Batch 06 identity gate: PASS
- no live membership recalculation gate: PASS
- Playwright/Chromium installation occurred only after those gates passed.

Complete runtime artifact:

- artifact ID: `10390926878`
- SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- files: `31`

Persisted runtime:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_runtime.json`

Runtime persistence commit:

`b50529991d9af6e27170090bd45b42eb751d0958`

## Independent adjudication

Adjudicator:

`tools/trading_breaks_recovery_batch06_adjudication.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_batch06_adjudication.py`

Adjudication workflow:

`.github/workflows/trading-breaks-recovery-batch06-adjudication.yml`

Authoritative independent adjudication:

- run: `34954764562`
- job: `104334032049`
- trigger commit: `44bac8e3ebb8c783d02295f052fe17c86c222049`
- conclusion: SUCCESS
- adversarial/regression suite: `114 passed in 0.36s`
- exact final accounting assertion: PASS
- no-browser/no-probe/no-live-queue guard: PASS

Persisted adjudication commit:

`874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`

Reports:

- `reports/data-qualification/historical_trading_breaks_recovery_batch06_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch06_qualification.md`

## Date-level outcomes

### 2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `56233`
- broker reason: `Independence Day`
- start: `2023-07-03T17:14:00Z`
- final closed minute: `2023-07-04T21:59:00Z`
- calibrated reopen: `2023-07-04T22:00:00Z`
- target-day fully closed UTC hours: `18,19,20,21,22,23`
- partial `17h` is not rounded closed.

### 2023-07-04 — INDEPENDENCE_DAY_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap witness: broker record `56233`
- the record starts `2023-07-03T17:14:00Z`
- it overlaps the target day through `2023-07-04T21:59:00Z`
- it is retained only as an overlap witness and MUST NOT be promoted to exact-target evidence.

### 2023-09-04 — LABOR_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `57462`
- start: `2023-09-04T16:59:00Z`
- final closed minute: `2023-09-04T21:59:00Z`
- reopen: `2023-09-04T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`.

### 2023-11-23 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `59358`
- start: `2023-11-23T16:59:00Z`
- final closed minute: `2023-11-23T22:59:00Z`
- reopen: `2023-11-23T23:00:00Z`
- fully closed UTC hours: `17,18,19,20,21,22`.

### 2023-11-24 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `59359`
- start: `2023-11-24T17:14:00Z`
- final closed minute: `2023-11-26T22:59:00Z`
- reopen: `2023-11-26T23:00:00Z`
- target-day fully closed UTC hours: `18,19,20,21,22,23`
- partial `17h` remains open; weekend continuation is not promoted to another target date.

## State boundary after adjudication

The factual Batch 06 attempts exist in evidence, but they have **not yet been atomically written** to calendar/attempt-ledger/progression state.

Persisted executable state therefore remains pre-integration:

- global: `111 / 42 resolved / 69 unresolved / 0 FAIL`
- execution window: `68 / 19 resolved / 49 unresolved / 0 FAIL`
- attempt ledger: `25`
- material capability changes: `0`
- persisted same-capability BLOCKED/ineligible: `6`
- persisted eligible unresolved: `43` — stale for scheduling until integration.

Consequences:

- do not freeze Batch 07 yet;
- do not rerun Batch 06 merely because integration is pending;
- do not separately integrate the four PASS records without recording all five attempts;
- `2023-07-04` remains unresolved and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Workflow closure

Execution workflow archived to `workflow_dispatch` only:

`224a4f99daf4fce09f7c07759a8fd89f4aa2b77a`

Independent adjudication workflow archived to `workflow_dispatch` only:

`285d94e11a7887d1cc62858390c4c29752ef5588`

No normal push may silently repeat Batch 06 browser execution or adjudication.

Current boundary report update:

`158a3d55841ba2cb5bc8f4cbd00aac0daf6eed83`

## Exactly one next governed action

**Atomically integrate Batch 06: add only the four independently adjudicated PASS records to executable calendar evidence, record all five Batch 06 factual attempts in the immutable attempt ledger, regenerate attempt-aware progression, adversarially rerun calendar/coverage/progression regressions, then perform an independent persisted-HEAD re-break before any Batch 07 freeze.**

Integrate PASS only:

- `2023-07-03`
- `2023-09-04`
- `2023-11-23`
- `2023-11-24`

Do not resolve:

- `2023-07-04`

After factual-attempt integration, `2023-07-04` must remain unresolved and become `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` under the current unchanged capability.

No `.bi5`. No real backtest.

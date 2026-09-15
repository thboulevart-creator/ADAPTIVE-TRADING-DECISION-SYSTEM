# SESSION BACKUP — 2026-09-15 — TRADING BREAKS RECOVERY BATCH 09 EXECUTION PASS

## Authoritative result

**PASS — `BATCH09_EXACT_FROZEN_MEMBERSHIP_EXECUTED_WITH_COMPLETE_CAPTURE_PROVENANCE_PENDING_INDEPENDENT_ADJUDICATION`**

This PASS is an execution/capture PASS only. It is **not** independent date-level adjudication and does not authorize calendar/ledger integration.

## Source state

- repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- branch: `feat/multi-year-dukascopy-acquisition`
- pre-execution recovery checkpoint: `f90a9ee7dfb539536a8e3d6506805a81ae08ada1`
- semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- capture implementation reused: `tools.trading_breaks_recovery_batch01.probe_candidate`

## Immutable Batch 09 membership

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

Execution consumed only `batch09_targets()`.

No live `eligible_recovery_queue()` or `recovery_queue()` call was present in the execution scheduling path. No member was skipped, substituted, reordered, expanded, shortened or duplicated.

## Execution implementation and adversarial pre-browser gates

Added:

- `tools/trading_breaks_recovery_batch09_execute.py`
- `tests/test_trading_breaks_recovery_batch09_execution_contract.py`
- `.github/workflows/trading-breaks-recovery-batch09.yml`

Execution contract attacks include:

- shortened membership rejected before any probe;
- reordered membership rejected before any probe;
- duplicate membership rejected before any probe;
- caller cannot inject target membership;
- a single probe exception becomes a factual capture-layer BLOCKED result but cannot skip remaining frozen members;
- executor has no live queue/progression/freeze-selection call;
- qualified capture probe itself has no membership-selection call.

Authoritative workflow pre-browser proof:

- checkpoint ancestry + governed frozen-state immutability: PASS;
- full governed and execution regression: `359 passed in 1.31s`;
- exact frozen identity: PASS;
- executor no-live-membership AST gate: PASS;
- qualified probe no-membership-selection AST gate: PASS.

Chromium was installed/opened only after all these gates passed.

## Authoritative execution provenance

- workflow trigger/probe commit: `0b5dedf6028add27040af112d0bceef76be25827`
- run: `34993614373`
- job: `104464228483`
- workflow conclusion: `success`
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`
- artifact ID: `10406357435`
- artifact name: `dukascopy-trading-breaks-recovery-batch09`
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`
- artifact size: `3599127` bytes
- artifact file count observed during upload: `31`
- runtime: `reports/data-qualification/historical_trading_breaks_recovery_batch09_runtime.json`
- execution qualification: `reports/data-qualification/historical_trading_breaks_recovery_batch09_execution_qualification.md`

## Raw capture results — pending independent adjudication

All five capture attempts returned:

`CAPTURED — POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION`

with observed instrument ID `9016`, instrument `USATECH.IDX/USD`, target document HTTP `200`, raw payload retained, DOM witness retained and no runtime error.

Observed records:

1. `2024-09-02` → record `70878`, start `2024-09-02T16:59:59Z`, end `2024-09-02T21:59:59Z`, reason `Labor Day`.
2. `2024-11-28` → record `72887`, start `2024-11-28T17:59:59Z`, end `2024-11-28T22:59:59Z`, reason `Thanksgiving Day`.
3. `2024-11-29` → record `72888`, start `2024-11-29T18:14:59Z`, end `2024-12-01T22:59:59Z`, reason `Thanksgiving Day`.
4. `2024-12-24` → record `74339`, start `2024-12-24T18:14:59Z`, end `2024-12-25T22:59:59Z`, reason `Christmas`.
5. `2024-12-25` → capture returned overlapping record `74339`, whose native start is `2024-12-24T18:14:59Z`.

Critical: the fifth capture is **not** a date-level PASS merely because the interval overlaps Dec 25. Independent adjudication must enforce the exact-target-date/cross-date contract. No cross-date promotion is authorized by this backup.

## Workflow closure

Completed Batch 09 execution workflow archived to `workflow_dispatch` only:

`785b29fa0e54848d21f02ce88b9e56a51adf8cd3`

Normal pushes cannot silently rerun Batch 09 execution.

## Persisted state remains unchanged pending adjudication/integration

- global calendar: `111 candidates / 53 resolved / 58 unresolved / 0 FAIL`
- execution window: `68 / 30 resolved / 38 unresolved / 0 FAIL`
- raw recovery queue: `38`
- historical attempt ledger: `40`
- material capability changes: `0`
- same-capability attempted BLOCKED/ineligible: `10`
- execution-eligible unresolved: `28`
- window frozen: NO

No `.bi5`. No real backtest.

## Exactly one next governed action

**Independently adjudicate the persisted Batch 09 runtime against immutable `batch09_targets()` and locked run/job/artifact/hash/probe provenance, with no browser and no live membership recalculation.**

The adjudication must attack frozen-membership tampering/reordering, provenance tampering, wrong instrument/date, DOM/network contradiction, duplicate records, cross-date promotion (especially `2024-12-25` / record `74339`), partial-hour rounding, and capture-layer `CAPTURED` → automatic PASS bypass.

Do not integrate executable calendar evidence and do not append Batch 09 ledger outcomes before independent adjudication PASS.

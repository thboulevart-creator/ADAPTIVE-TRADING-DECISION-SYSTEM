# HISTORICAL TRADING BREAKS RECOVERY — BATCH 09 EXECUTION QUALIFICATION

**PASS — `BATCH09_EXACT_FROZEN_MEMBERSHIP_EXECUTED_WITH_COMPLETE_CAPTURE_PROVENANCE_PENDING_INDEPENDENT_ADJUDICATION`**

## Execution identity

- frozen membership source: `tools.trading_breaks_recovery_batch09.batch09_targets()`
- batch size: `5`
- semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- qualified capture implementation reused unchanged: `tools.trading_breaks_recovery_batch01.probe_candidate`
- workflow trigger/probe commit: `0b5dedf6028add27040af112d0bceef76be25827`
- workflow run: `34993614373`
- job: `104464228483`
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`
- artifact ID: `10406357435`
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`
- artifact files: `31`
- artifact size: `3599127` bytes

## Pre-browser gates

All pre-browser gates passed before Playwright/Chromium installation:

- checkpoint ancestry and governed frozen-state immutability: PASS;
- complete governed regression: `359 passed in 1.31s`;
- exact immutable Batch 09 identity: PASS;
- execution AST has no `eligible_recovery_queue`, `recovery_queue`, progression, freeze-derivation, or caller-injected selection path: PASS;
- qualified `probe_candidate` itself has no membership-selection call: PASS.

Only after these gates passed was Playwright/Chromium installed and the browser opened.

## Exact executed membership

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

No member was skipped, substituted, reordered, duplicated, added, or removed.

## Raw capture outcomes — NOT YET ADJUDICATED

All five executions returned capture-layer `CAPTURED — POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION` with instrument `USATECH.IDX/USD`, observed instrument ID `9016`, HTTP target status `200`, exact requested historical date honored, raw payload retained, DOM witness retained, and no runtime error.

Observed broker records:

- `2024-09-02`: record `70878`, starts `2024-09-02T16:59:59Z`, ends `2024-09-02T21:59:59Z`, broker reason `Labor Day`.
- `2024-11-28`: record `72887`, starts `2024-11-28T17:59:59Z`, ends `2024-11-28T22:59:59Z`, broker reason `Thanksgiving Day`.
- `2024-11-29`: record `72888`, starts `2024-11-29T18:14:59Z`, ends `2024-12-01T22:59:59Z`, broker reason `Thanksgiving Day`.
- `2024-12-24`: record `74339`, starts `2024-12-24T18:14:59Z`, ends `2024-12-25T22:59:59Z`, broker reason `Christmas`.
- `2024-12-25`: the capture route returned the same overlapping record `74339`, whose broker-native start is `2024-12-24T18:14:59Z`, not the target date.

The `2024-12-25` result is intentionally **not promoted** here. Capture-layer `CAPTURED` is not a date-level PASS. The independent adjudicator must enforce exact-target-date/cross-date rules and may classify that target PASS, BLOCKED, or FAIL only under the qualified adjudication contract.

## State mutation boundary

This execution persisted capture evidence only. It did **not** mutate:

- `SPECIAL_SESSION_EVIDENCE`;
- `NO_SPECIAL_CHANGE_EVIDENCE`;
- the historical attempt ledger;
- progression eligibility;
- material capability registry;
- execution-window freeze state.

No `.bi5` acquisition occurred. No real backtest occurred.

## Next governed action

Independently adjudicate the persisted Batch 09 runtime against the immutable `batch09_targets()` identity and locked run/job/artifact/hash/probe provenance. The adjudicator must have no browser path and no live membership recalculation path. It must specifically attack cross-date promotion, DOM/network contradiction, provenance tampering, result reordering, duplicate records, partial-hour rounding, and any attempt to treat capture-layer `CAPTURED` as automatic PASS.

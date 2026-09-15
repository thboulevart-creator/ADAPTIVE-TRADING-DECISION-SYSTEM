# SESSION BACKUP — 2026-09-15 — TRADING BREAKS RECOVERY BATCH 09 ADJUDICATION PASS

## Authoritative outcome

Batch 09 independent adjudication is complete and persisted.

**PASS — `BATCH09_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Accounting:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

No calendar, attempt-ledger, capability-registry or progression mutation has occurred yet.

## Immutable Batch 09 membership

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

Membership source is immutable `batch09_targets()`. Adjudication contains no live queue selection/recalculation.

## Locked execution provenance adjudicated

- browser execution run: `34993614373`
- browser execution job: `104464228483`
- probe commit: `0b5dedf6028add27040af112d0bceef76be25827`
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`
- artifact: `10406357435`
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`
- instrument: `USATECH.IDX/USD` / `9016`

The adjudication workflow independently checked the above run/job/artifact/hash/head SHA through GitHub Actions before using the persisted runtime.

## Adjudication implementation

- `tools/trading_breaks_recovery_batch09_adjudication.py`
- `tests/test_trading_breaks_recovery_batch09_adjudication.py`
- `reports/data-qualification/historical_trading_breaks_recovery_batch09_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch09_qualification.md`

Adjudicator constraints:

- offline only;
- no Playwright/Chromium/Selenium;
- no `probe_candidate`;
- no `eligible_recovery_queue()` / `recovery_queue()` / progression scheduling;
- replay scope only `batch09_targets()`;
- locked execution provenance;
- independently recalculates interval/reopen/fully-closed-hour semantics from native timestamps;
- `CAPTURED` is never treated as automatic PASS.

## Adversarial attacks covered

- frozen membership tampering;
- result reordering;
- provenance tampering: run/job/artifact/hash/probe/artifact URL;
- wrong requested date / epoch / instrument;
- DOM/network contradiction;
- duplicate broker records;
- duplicate DOM witnesses;
- DOM without broker record;
- capture-layer `PASS` injection;
- `CAPTURED → PASS` bypass;
- cross-date promotion;
- stored derived reopen tampering;
- partial-hour rounding tampering;
- caller selection override surface.

## Exact date-level result

### PASS

- `2024-09-02 — LABOR_DAY`: record `70878`, fully closed UTC `[17,18,19,20,21]`.
- `2024-11-28 — THANKSGIVING_DAY`: record `72887`, fully closed UTC `[18,19,20,21,22]`.
- `2024-11-29 — THANKSGIVING_FRIDAY`: record `72888`, native start `18:14:59Z`, fully closed UTC `[19,20,21,22,23]`; hour 18 is not rounded closed.
- `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`: record `74339`, native start `18:14:59Z`, fully closed UTC `[19,20,21,22,23]`; hour 18 is not rounded closed.

### BLOCKED

- `2024-12-25 — CHRISTMAS_OBSERVED`: capture had record `74339`, but that record starts on `2024-12-24T18:14:59Z`. Final adjudication is `BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`. The cross-date overlap is not promoted and no executable closed-hour evidence is emitted for Dec 25.

## Workflow evidence

First run:

- run/job: `34995813928` / `104471627623`
- semantic gates: PASS
- provenance check: PASS
- governed/adversarial regression: `387 passed in 1.68s`
- adjudication: PASS `4/1/0`
- state non-mutation gate: PASS
- final persistence: FAILED only because `git diff --cached --check` rejected an extra blank line at EOF in generated Markdown.

This was a persistence-harness defect only; no governed state mutation occurred.

Minimal correction:

- workflow commit: `a23836aa296dbfb6080b0b710aacc493a42edc20`
- normalized generated Markdown EOF before `git add`.

Corrected authoritative run:

- run/job: `34995973784` / `104472165374`
- conclusion: `success`
- regression: `387 passed in 1.39s`
- provenance check: PASS
- offline/no-live-selection gate: PASS
- exact adjudication assertion: PASS
- executable-state non-mutation: PASS
- persistence: PASS
- adjudication evidence commit: `394753a95259356a205dd98a7675bddfb6b53b2e`

Adjudication workflow archived manual-only:

`4a5b3e048c2c8f1aef460706d91ec632e8d2036c`

Boundary report advanced at:

`bd8b1c034f6b740ce985a430cd8f6a1a1d3e1114`

## Current executable state — intentionally unchanged

- global calendar: `111 / 53 resolved / 58 unresolved / 0 FAIL`
- execution window: `68 / 30 resolved / 38 unresolved / 0 FAIL`
- raw recovery queue: `38`
- attempt ledger: `40`
- material capability changes: `0`
- same-capability attempted BLOCKED/ineligible: `10`
- eligible unresolved: `28`

Expected state only after a separately governed Batch 09 atomic integration PASS:

- global `111 / 57 / 54 / 0 FAIL`
- execution window `68 / 34 / 34 / 0 FAIL`
- ledger `45`
- BLOCKED/ineligible `11`
- eligible unresolved `23`
- `2024-12-25` remains unresolved.

## Exactly one next governed action

Atomically integrate the persisted Batch 09 adjudication into calendar evidence, historical attempt ledger and deterministic progression state. Add only the four PASS dates to executable calendar evidence, append all five factual attempts in frozen order, leave Dec 25 unresolved/BLOCKED, prove the expected post-state, and rerun the complete governed regression.

Persisted-HEAD re-break is a separate action after integration PASS.

No `.bi5`. No real backtest. Same branch only.
# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 EXECUTION QUALIFICATION

**PASS — `BATCH10_FROZEN_MEMBERSHIP_EXECUTED_WITH_PRE_BROWSER_GATES_AND_CAPTURE_ONLY_BOUNDARY`**

## Authoritative execution

- checkpoint baseline: `cfe283ccfc4e8c581830e2b1c8f3f3b49d8a82c2`
- execution trigger / probe commit: `443b3696e4e2740a54354787de231c886f90b26e`
- workflow run: `35004172846`
- job: `104499660140`
- runtime persistence commit: `1134f96517157647d7663ce1ebaf045267e78bcb`
- artifact: `10411022092`
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`
- artifact files: `31`
- artifact ZIP size: `3796617` bytes
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## Pre-browser gates

Before Playwright/Chromium installation, the authoritative run proved:

- checkpoint ancestry and frozen governed-state immutability: PASS;
- complete governed + adversarial regression: `423 passed in 1.88s`;
- exact immutable `batch10_targets()` identity, size `5`, chronological order and capability fingerprint: PASS;
- execution path consumes `batch10_targets()` and has no live `eligible_recovery_queue()` / `recovery_queue()` / progression selection: PASS;
- qualified `probe_candidate` has no membership-selection responsibility: PASS.

Only after those gates passed was Playwright/Chromium installed and opened.

## Exact execution scope

The browser execution consumed exactly this frozen order once each:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

No live queue recalculation, skip, replacement, reorder, shrink or expansion occurred.

## Raw capture facts — not date-level adjudication

1. `2024-12-31` — `CAPTURED`; broker record `75799`, start `2024-12-31T21:14:59Z`, end `2025-01-01T22:59:59Z`, DOM witness retained.
2. `2025-01-01` — `CAPTURED`; broker record `75799`, whose native start is `2024-12-31T21:14:59Z`; DOM witness retained. This is a cross-date fact requiring later independent adjudication and is not promoted here.
3. `2025-01-20` — `CAPTURED`; broker record `76806`, start `2025-01-20T17:59:59Z`, end `2025-01-20T22:59:59Z`, DOM witness retained.
4. `2025-02-17` — `CAPTURED`; broker record `78513`, start `2025-02-17T17:59:59Z`, end `2025-02-17T22:59:59Z`, DOM witness retained.
5. `2025-04-18` — capture outcome `BLOCKED — EXPECTED_DOM_CROSSCHECK_MISSING`; network record `80057` was retained, starts `2025-04-17T20:14:59Z`, and no DOM witness line was captured. This remains a raw execution fact only.

`CAPTURED` is not a date-level PASS. This execution report performs no independent evidence adjudication and authorizes no calendar integration.

## State mutation boundary

The execution action did not modify:

- executable calendar evidence;
- attempt ledger;
- attempt-aware progression;
- capability-change registry.

Persisted governed counts therefore remain:

- global: `111 / 57 resolved / 54 unresolved / 0 FAIL`;
- execution-window candidate: `68 / 34 resolved / 34 unresolved / 0 FAIL`;
- attempt ledger: `45`;
- same-capability BLOCKED/ineligible: `11`;
- execution-eligible unresolved: `23`;
- material capability changes: `0`.

No `.bi5`. No real backtest.

## Next boundary

The next governed action is an independent, offline Batch 10 adjudication over the persisted runtime/artifact provenance. It must not open a browser or recalculate membership, and must explicitly test cross-date promotion, missing-DOM handling, provenance, order, duplicate/contradictory evidence, interval semantics and any `CAPTURED -> PASS` bypass before any integration.

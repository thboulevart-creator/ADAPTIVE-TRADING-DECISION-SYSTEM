# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 10 execution/capture PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 57 resolved / 54 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 34 resolved / 34 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware recovery progression: **PASS**
- Historical attempt ledger entries: **45**
- Registered material capability changes: **0**
- Attempted BLOCKED / same-capability execution-ineligible: **11**
- Execution-eligible unresolved: **23**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 09: **FULLY CLOSED THROUGH PERSISTED-HEAD RE-BREAK PASS**
- Batch 10 membership: **FROZEN + ADVERSARIALLY QUALIFIED + INDEPENDENT PERSISTED-MEMBERSHIP RE-BREAK PASS**
- Batch 10 execution/capture: **PASS — CAPTURE ONLY, NOT ADJUDICATED**
- Batch 10 independent adjudication: **NOT STARTED**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 09 final closed state

- atomic integration commit: `126ff25129728dc9f5c26cfeff701c1e04270843`;
- persisted-HEAD verifier run/job: `34998844423` / `104481875172`;
- final verdict: **PASS — `BATCH09_PERSISTED_HEAD_REBREAK_CONFIRMS_ATOMIC_INTEGRATION`**;
- global state: `111 / 57 / 54 / 0 FAIL`;
- execution window: `68 / 34 / 34 / 0 FAIL`;
- ledger: `45`;
- BLOCKED/ineligible: `11`;
- eligible unresolved: `23`.

## Batch 10 immutable membership

Selection rule: `eligible_recovery_queue()[:5]`, fixed size `5`.

Frozen snapshot commit:

`65b789f310c066f90b39cd9e1ed69d2bd0962b6c`

Exact immutable order:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

Mechanical freeze run/job: `35003111213` / `104496100100`.

Independent persisted-membership re-break run/job: `35003238287` / `104496526561`.

Membership qualification and persisted re-break proved:

- fixed chronological prefix: PASS;
- skip/reorder/substitution/cardinality/duplicate/raw-queue bypass: rejected;
- attempted BLOCKED / resolved-date reinsertion: rejected;
- all five `INITIAL_ATTEMPT`, unresolved and execution-eligible at freeze: PASS;
- no browser/probe/network observation during freeze: PASS;
- governed state mutation during freeze/re-break: NONE;
- complete persisted-membership regression: `415 passed in 2.15s`.

## Batch 10 execution/capture — PASS

Final execution verdict:

**PASS — `BATCH10_FROZEN_MEMBERSHIP_EXECUTED_WITH_PRE_BROWSER_GATES_AND_CAPTURE_ONLY_BOUNDARY`**

Authoritative execution:

- checkpoint baseline: `cfe283ccfc4e8c581830e2b1c8f3f3b49d8a82c2`;
- trigger / probe commit: `443b3696e4e2740a54354787de231c886f90b26e`;
- workflow run/job: `35004172846` / `104499660140`;
- pre-browser governed + adversarial regression: **`423 passed in 1.88s`**;
- runtime persistence commit: `1134f96517157647d7663ce1ebaf045267e78bcb`;
- artifact: `10411022092`;
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`;
- artifact files: `31`;
- browser installation/opening occurred only after protocol/progression/identity/no-live-selection gates PASS;
- execution consumed exactly `batch10_targets()` in frozen order;
- no live membership recalculation occurred;
- no date-level adjudication occurred;
- no calendar/ledger/progression integration occurred.

Raw capture facts, still requiring independent adjudication:

1. `2024-12-31` — `CAPTURED`; record `75799`; native start `2024-12-31T21:14:59Z`; DOM witness retained.
2. `2025-01-01` — `CAPTURED`; record `75799`; native start `2024-12-31T21:14:59Z`; DOM witness retained. This is cross-date and has not been promoted.
3. `2025-01-20` — `CAPTURED`; record `76806`; native start `2025-01-20T17:59:59Z`; DOM witness retained.
4. `2025-02-17` — `CAPTURED`; record `78513`; native start `2025-02-17T17:59:59Z`; DOM witness retained.
5. `2025-04-18` — capture result `BLOCKED — EXPECTED_DOM_CROSSCHECK_MISSING`; network record `80057` retained; native start `2025-04-17T20:14:59Z`; no DOM witness line captured.

`CAPTURED` is not date-level PASS. None of these raw facts changes executable calendar state before independent adjudication.

Execution qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch10_execution_qualification.md`

Completed execution workflow archive commit:

`c1f63d835a5d5b4475225f929deb3d95a0d33211`

The execution workflow is now manual-only with read permissions. Normal pushes cannot silently repeat completed Batch 10 capture.

## Current downstream boundary

PASS now includes:

- all completed Batch 01–09 recovery/integration gates;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_POLICY`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_PERSISTED_MEMBERSHIP_REBREAK`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_EXECUTION_CAPTURE`.

Still pending/BLOCKED:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_INDEPENDENT_ADJUDICATION — NOT STARTED`;
- `DECLARE_GLOBAL_COVERAGE_PASS — GLOBAL_UNRESOLVED_REMAINS_54`;
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_34_UNRESOLVED_DATES`;
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`;
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`.

No `.bi5` acquisition occurred. No real backtest occurred.

## Exactly one next governed action

**Independently adjudicate the persisted Batch 10 runtime offline, without browser and without live membership recalculation.**

The adjudication must consume immutable `batch10_targets()` plus the persisted runtime/provenance and adversarially reject at minimum:

- promotion of the cross-date `2025-01-01 / 75799` capture solely because it overlaps the target date;
- promotion of `2025-04-18 / 80057` despite cross-date start or missing required DOM witness;
- any `CAPTURED -> PASS` shortcut;
- wrong/missing run, job, artifact, artifact digest or probe commit;
- target order/membership mutation;
- duplicate or multiple conflicting records;
- DOM/network contradiction;
- wrong instrument/date;
- timestamp/reopen/fully-closed-hour tampering or silent partial-hour rounding.

No calendar/ledger integration may occur until that independent adjudication is PASS. Same branch only. No `.bi5`. No real backtest.

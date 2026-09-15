# SESSION BACKUP — 15 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 10 INDEPENDENT ADJUDICATION PASS

## Final verdict

**PASS — `BATCH10_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_OR_MISSING_DOM_PROMOTION`**

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

## Authoritative frozen Batch 10

Snapshot commit: `65b789f310c066f90b39cd9e1ed69d2bd0962b6c`.

Exact immutable order:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

## Authoritative execution provenance

- execution run/job: `35004172846` / `104499660140`
- probe commit: `443b3696e4e2740a54354787de231c886f90b26e`
- artifact: `10411022092`
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`
- artifact size: `3796617` bytes
- runtime persistence commit: `1134f96517157647d7663ce1ebaf045267e78bcb`

The independent adjudication workflow re-verified the run conclusion, job conclusion, execution head SHA, artifact ID, digest, size and non-expired status directly from GitHub before adjudication.

## Independent offline adjudication

- adjudicator source preparation: `34c154597990f1200ab6f8522bc880f0d88f9a88`
- adversarial tests: `79de8930587ff373817d064994e1bb18dfe3175f`
- workflow trigger: `44081d66127c9c620c2001b15024cc2092a0155f`
- run/job: `35005525644` / `104504189641`
- full governed + adversarial regression: `459 passed in 2.02s`
- adjudication report persistence commit: `77964da`
- completed adjudication workflow archive commit: `e03fd706d094df20dfcb126863d96b1c1b524a7a`
- adjudication workflow after closure: `workflow_dispatch` only, `contents: read`
- browser/Chromium/Playwright during adjudication: NONE
- `probe_candidate` execution during adjudication: NONE
- live `eligible_recovery_queue()` / `recovery_queue()` membership selection: NONE

## Exact date-level outcomes

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `75799`
   - start `2024-12-31T21:14:59Z`
   - final closed minute `2025-01-01T22:59:59Z`
   - reopen `2025-01-01T23:00:59Z`
   - fully closed target-day UTC hours `[22,23]`
   - DOM witness present.

2. `2025-01-01 — NEW_YEARS_OBSERVED`
   - **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**
   - overlap record `75799`
   - native broker start remains `2024-12-31T21:14:59Z`
   - capture layer was `CAPTURED`, but `CAPTURED -> PASS` was explicitly rejected.

3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `76806`
   - fully closed target-day UTC hours `[18,19,20,21,22]`.

4. `2025-02-17 — PRESIDENTS_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `78513`
   - fully closed target-day UTC hours `[18,19,20,21,22]`.

5. `2025-04-18 — GOOD_FRIDAY`
   - **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**
   - overlap record `80057`
   - native broker start `2025-04-17T20:14:59Z`
   - DOM witness absent
   - capture layer reason `EXPECTED_DOM_CROSSCHECK_MISSING`
   - cross-date + missing DOM cannot be promoted.

Final accounting: **3 PASS / 2 BLOCKED / 0 FAIL**.

## Adversarial boundary actually broken

The adjudication rejected or detected:

- frozen membership tampering;
- result reorder and result-count mutation;
- run/job/artifact/digest/probe/artifact-URL provenance tampering;
- wrong requested date / target epoch / instrument;
- duplicate or conflicting network records;
- duplicate DOM witnesses;
- DOM/network contradiction;
- wrong DOM instrument;
- `CAPTURED -> PASS` shortcut;
- cross-date promotion of `2025-01-01 / 75799`;
- cross-date + missing-DOM promotion of `2025-04-18 / 80057`;
- exact-target promotion with missing DOM;
- forged `capture_verdict=PASS`;
- start/end/reopen timestamp tampering;
- fully-closed-hour tampering and silent partial-hour rounding;
- DOM witness without a network record;
- browser/probe/live-membership-selection paths in the adjudicator.

## State mutation boundary

Independent adjudication did not mutate:

- executable calendar evidence;
- no-special-change evidence;
- attempt ledger;
- progression runtime;
- capability-change registry;
- Batch 10 runtime.

Persisted governed state therefore remains pre-integration:

- global `111 / 57 resolved / 54 unresolved / 0 FAIL`
- execution window `68 / 34 resolved / 34 unresolved / 0 FAIL`
- raw unresolved `34`
- ledger `45`
- same-capability BLOCKED/ineligible `11`
- eligible unresolved `23`
- capability changes `0`.

No `.bi5`. No real backtest.

## Exactly one next governed action

**Integrate Batch 10 atomically from the persisted independent adjudication: add only `2024-12-31`, `2025-01-20` and `2025-02-17` to executable calendar evidence; append all five factual attempts in frozen order; keep `2025-01-01` and `2025-04-18` unresolved/BLOCKED and make them same-capability ineligible; regenerate progression; then adversarially prove the exact post-state before any Batch 11 work.**

Expected deterministic post-integration accounting if no other rule changes:

- global `111 / 60 resolved / 51 unresolved / 0 FAIL`
- execution window `68 / 37 resolved / 31 unresolved / 0 FAIL`
- raw unresolved `31`
- ledger `50`
- same-capability BLOCKED/ineligible `13`
- eligible unresolved `18`
- capability changes `0`.

Do not freeze Batch 11 before Batch 10 integration and its governed verification pass.

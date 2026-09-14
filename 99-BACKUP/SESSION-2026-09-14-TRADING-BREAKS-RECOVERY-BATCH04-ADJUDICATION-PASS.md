# SESSION BACKUP — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 04 ADJUDICATION PASS

## Final verdict for this governed action

**PASS — Batch 04 frozen membership was executed only after all pre-browser gates passed, then independently adjudicated as `3 PASS / 2 BLOCKED / 0 FAIL` without recalculating membership or promoting cross-date overlaps.**

No Batch 04 calendar/attempt integration has yet been applied.

## Frozen Batch 04 membership

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

Membership remained the immutable tuple from `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`. Neither execution nor adjudication read the live eligible queue to choose members.

## Authoritative browser execution

- workflow run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact ID: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- persisted runtime commit: `2fb64b3857dcbe53f08c9dcabe85669f0eb5c81f`
- pre-browser suite: `110 passed in 0.59s`
- exact frozen membership guard: PASS
- no-live-queue runner guard: PASS
- browser execution: SUCCESS

Chromium was installed/opened only after all gates passed.

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_runtime.json`

## Independent adjudication

Adjudication workflow:

- run: `34895985689`
- job: `104149952523`
- trigger commit: `e3c40f3bfcd7300bfbe7383c21e4d70c16df783e`
- adversarial suite: `81 passed in 0.27s`
- final accounting assertion: PASS
- browser-free/no-membership-recalculation guard: PASS

Final verdict:

**PASS — `BATCH04_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Date-level results:

1. `2022-11-24` → PASS — record `45119`, Thanksgiving Day, fully closed UTC hours `18–22`.
2. `2022-11-25` → PASS — record `45120`, Thanksgiving Day, exact target-date start `18:14Z`, fully closed target-day hours `19–23`.
3. `2022-12-23` → PASS — record `46756`, Christmas Day, exact target-date start `21:14Z`, fully closed target-day hours `22–23`.
4. `2022-12-26` → BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`; overlap record `46756` starts `2022-12-23T21:14:00Z`.
5. `2023-01-02` → BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`; overlap record `48045` starts `2022-12-30T21:14:00Z`.

Only the first three are authorized for later executable calendar integration. The two cross-date overlaps remain unresolved and are not negative evidence.

## Adversarial overlap boundary

The Batch 04 adjudication explicitly rejects:

- promotion of a cross-date overlap as exact-target evidence;
- an unrelated neighboring record that does not actually overlap the target day;
- DOM/network contradiction on exact positives or overlap witnesses;
- multiple matching records being silently selected;
- runtime membership tampering or result reordering;
- provenance digest tampering;
- use of the overlap-only path for a record whose start has become exact-target;
- browser/probe execution or live eligible-queue membership recalculation inside adjudication.

## Workflow closure

Both completed Batch 04 workflows are archived to `workflow_dispatch` only:

- `.github/workflows/trading-breaks-recovery-batch04.yml`
- `.github/workflows/trading-breaks-recovery-batch04-adjudication.yml`

No normal push can silently rerun Batch 04 browser capture or adjudication.

## Current executable state — deliberately not yet integrated

Persisted executable calendar remains pre-Batch04-integration:

- global: `111 / 34 resolved / 77 unresolved / 0 FAIL`
- execution-window candidate: `68 / 11 resolved / 57 unresolved / 0 FAIL`
- attempt ledger: `15`

The pre-execution progression projection (`53` eligible unresolved) is now stale for future scheduling because Batch 04 factual attempts have occurred but are not yet atomically written to the attempt ledger. It MUST NOT be used to freeze Batch 05.

## Exactly one next governed action

**Atomically integrate Batch 04: add only the three PASS records to executable calendar evidence, record all five factual attempts in the attempt ledger, regenerate progression state, and adversarially prove the persisted post-integration calendar/coverage/progression state.**

The two BLOCKED dates must remain unresolved and become same-capability execution-ineligible after their factual attempts are recorded.

No `.bi5`. No real backtest.

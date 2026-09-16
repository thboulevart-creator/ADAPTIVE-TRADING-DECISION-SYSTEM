# SESSION BACKUP — 2026-09-16 — TRADING BREAKS BATCH 15 V2 CLOSED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests and qualified workflow evidence are authoritative. This backup is a recovery aid, not a substitute for executable state.

## What changed after Batch 14 closure

The post-Batch14 critical-path review split the 17 unresolved dates into:

- Class A: 14 dates with persisted positive broker-native records spanning the target day but blocked by the old exact-start-date admissibility rule;
- Class B: 3 dates with no positive broker record recovered.

The Class-A semantic problem was then independently qualified rather than solved by new browser capture.

## Qualified overlap capability V2

Semantic contract:

`TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`

Capability:

`TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`

Fingerprint:

`e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

Material capability change:

`TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_CHANGE_V1`

Qualification commit:

`061e97d90eed2c4c3f1d5f2a261e457fd796413f`

Persisted qualification chain proves:

- target-day interval-overlap attribution is adversarially qualified;
- historical Class-A evidence is bound to immutable original V1 attempts;
- V2 activation is atomic and independently re-broken;
- all 14 Class-A dates were readjudicated offline as PASS under the qualified semantic contract;
- no browser/probe/live recapture was used for that readjudication.

## Batch 15 V2

Policy:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH15_OVERLAP_V2_RETRY_POLICY_V1`

Frozen membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Freeze qualification:

- baseline: `d6622e8da58e2d4218947ff3f2953fe8e19a2c96`
- qualification HEAD: `8066e82607db1f8de0b406ec36684a6856e0646d`
- run/job: `35067822465 / 104702050599`
- persisted-membership re-break run/job: `35067904056 / 104702309977`

Offline execution/adjudication:

- execution selector HEAD: `f73d31e645bdc1ad4081a7cf3c104e3f3bd4848b`
- execution run/job: `35068035246 / 104702726720`
- adjudication trigger: `6dc134aa53a0904cda6c08108377dd8be8dd718c`
- adjudication run/job: `35068120024 / 104702999768`
- result: `5 PASS / 0 BLOCKED / 0 FAIL`

Atomic integration:

`4dee7e22af1402626341f76611926b108fd1d8c0`

It changed exactly:

- `tools/dukascopy_usatech_calendar.py`
- `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
- `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`

## Independent persisted-HEAD re-break

Initial verifier attempt:

- commit: `3befa42956f9d4013fced5623f283996f75a227e`
- run/job: `35085516084 / 104759279481`
- outcome: FAIL because the verifier replayed the pre-integration Batch15 adjudicator against a post-integration 73-attempt ledger; the adjudicator correctly rejected that invalid replay scope.

Corrected verifier:

- commit: `4bb7712bcab8b8930c4054e1500302621f881f4f`
- run/job: `35085635675 / 104759660665`
- permissions: `contents: read`
- regression: `65 passed in 0.25s`
- integration ancestry/atomicity: PASS
- attempts `1..68` immutable: PASS
- exact attempts `69..73` and source provenance: PASS
- exact calendar state: PASS
- material capability registry: PASS
- global coverage: `111 / 79 resolved / 32 unresolved`
- execution window: `68 / 56 resolved / 12 unresolved`
- progression: `12 unresolved / 9 eligible / 3 ineligible`
- deterministic progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE
- workflow conclusion: success

Durable report:

`reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_persisted_head_rebreak.md`

Batch 15 V2 verdict: **FULLY CLOSED**.

## Current unresolved state

Remaining Class-A overlap-V2 eligible retries: 9

1. `2023-12-25 — CHRISTMAS_OBSERVED`
2. `2024-01-01 — NEW_YEARS_OBSERVED`
3. `2024-03-29 — GOOD_FRIDAY`
4. `2024-12-25 — CHRISTMAS_OBSERVED`
5. `2025-01-01 — NEW_YEARS_OBSERVED`
6. `2025-04-18 — GOOD_FRIDAY`
7. `2025-12-25 — CHRISTMAS_OBSERVED`
8. `2026-01-01 — NEW_YEARS_OBSERVED`
9. `2026-04-03 — GOOD_FRIDAY`

Remaining Class-B unresolved/ineligible: 3

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Class-B reason:

`RETRY_MATERIAL_CHANGE_NOT_PROVEN:BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED`

## Boundary

Do not infer Batch 16 merely because Batch 15 passed. Re-evaluate the current critical path first using the now-reduced `9 Class A + 3 Class B` state.

No new browser capture.  
No `.bi5`.  
No real backtest.

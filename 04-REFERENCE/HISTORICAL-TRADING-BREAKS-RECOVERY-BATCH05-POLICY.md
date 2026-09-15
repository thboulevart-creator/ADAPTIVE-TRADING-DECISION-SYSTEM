# HISTORICAL TRADING BREAKS RECOVERY — BATCH 05 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Qualification status

**CANDIDATE — adversarial qualification required before any browser observation.**

This policy freezes Batch 05 membership from the persisted post-Batch04 attempt-aware execution state. No Batch 05 historical broker observation is authorized until the membership contract passes its dedicated adversarial qualification.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`601310a55b64233ada9e481d3cb2f11dc20a30d5`

Source post-Batch04 atomic integration / progression-state commit:

`6cafa5337f28c5424cbcc25280c690de702061d9`

Governed progression state at freeze:

- calendar unresolved: `54`
- historical attempts: `20`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `48`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size remains fixed. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 05 membership is exactly:

`eligible_recovery_queue()[:5]`

at the freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

## 4. Frozen Batch 05 membership

The mechanically derived immutable membership is:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

These identities and this order are frozen before any Batch 05 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Eligibility properties required for PASS

The dedicated qualification must prove that each frozen member:

- equals the corresponding entry of persisted post-Batch04 `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is unique and chronologically ordered.

It must also prove that all six same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 05 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Their exclusion is scheduling only. They remain unresolved calendar gaps.

## 6. Forbidden selection inputs

Batch 05 membership MUST remain independent of:

- expected PASS/BLOCKED/FAIL outcome;
- expected positive-record probability;
- holiday category/type;
- source availability;
- apparent difficulty;
- convenience;
- manual priority;
- manual skip/substitution;
- caller-supplied membership.

Only governed chronological execution eligibility plus fixed `BATCH_SIZE = 5` is admissible.

## 7. Browser boundary

The membership-freeze module MUST contain no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

No browser installation or broker observation belongs to this action.

## 8. Downstream boundary

Even after membership qualification PASS, no date is resolved by this policy alone.

Only a later separately governed action may execute exactly the frozen five dates under the qualified Trading Breaks capture chain, with parent/progression/Batch05 gates PASS before Chromium opens, followed by independent adjudication.

No `.bi5` acquisition. No real backtest.

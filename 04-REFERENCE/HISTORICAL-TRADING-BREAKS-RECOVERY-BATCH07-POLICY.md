# HISTORICAL TRADING BREAKS RECOVERY — BATCH 07 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Qualification status

**CANDIDATE — adversarial qualification pending**

Batch 07 membership is frozen here before any Batch 07 historical broker observation. No execution is authorized by this policy candidate until the membership qualification workflow passes.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`16c6288158985bb3ad68360401b6bdae60687e15`

Source post-Batch06 atomic integration / progression-state commit:

`a2a59baefd7986f65efb4d625acd2c47c085ae31`

Independent post-Batch06 persisted-HEAD re-break trigger commit:

`3feb9f937bf74202f68642992ca3fe8b363398d9`

Governed progression state at freeze:

- calendar unresolved: `45`
- historical attempts: `30`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- execution-eligible unresolved: `38`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size is fixed before observation. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 07 membership is exactly:

`eligible_recovery_queue()[:5]`

at the persisted post-Batch06 freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

The production freeze module does not call either queue live. It stores only the already-derived immutable snapshot.

## 4. Frozen Batch 07 membership

The mechanically derived immutable membership is:

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

These identities and this order are frozen before any Batch 07 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Required qualification proof

Qualification must prove that every frozen member:

- equals the corresponding entry of persisted post-Batch06 `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is classified `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is unique and chronologically ordered.

It must also prove that all seven same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 07 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Their exclusion is scheduling only. They remain unresolved calendar gaps.

## 6. Adversarial qualification boundary

The suite must reject:

- raw `recovery_queue()` substitution;
- skipping the first eligible member;
- reordering members;
- substituting a later eligible member;
- shortening or expanding batch cardinality;
- reinserting same-capability attempted BLOCKED dates;
- reintroducing already-resolved Batch 06 PASS dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- caller mutation or caller selection surfaces;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent protocol/progression/calendar/boundary regressions.

## 7. Browser boundary

The Batch 07 freeze module MUST contain no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call;
- browser/network observation path.

No Batch 07 broker observation is permitted during membership freeze or qualification.

## 8. State mutation boundary

This freeze is scheduling/governance only. It MUST NOT:

- resolve any calendar candidate;
- modify executable calendar evidence;
- append any factual attempt;
- register any material capability change;
- alter progression runtime;
- alter global/window coverage counts.

Persisted accounting must remain:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`;
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`;
- attempt ledger: `30`;
- attempted BLOCKED / execution-ineligible: `7`;
- execution-eligible unresolved: `38`.

## 9. Next action after qualification PASS

Only after adversarial membership qualification PASS may a later separately governed action execute exactly `batch07_targets()` through the qualified Trading Breaks capture chain.

No `.bi5` acquisition. No real backtest.

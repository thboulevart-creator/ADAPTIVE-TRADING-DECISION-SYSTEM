# HISTORICAL TRADING BREAKS RECOVERY — BATCH 08 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Qualification status

**CANDIDATE — adversarial membership qualification pending.**

No Batch 08 historical broker observation is authorized until this membership gate reaches PASS.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`2e9e51cea8342c701eec14d8d86aca215c5b7b62`

Source post-Batch07 atomic integration / progression-state commit:

`616643e2bfd0b8a8ae3f21352554dc32fdbb503d`

Independent post-Batch07 persisted-HEAD re-break trigger commit:

`b4a2f3400b0629e7b1d0a715320735f74293b15a`

Governed progression state at freeze:

- calendar unresolved: `42`
- historical attempts: `35`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `9`
- execution-eligible unresolved: `33`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size is fixed. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 08 membership is exactly:

`eligible_recovery_queue()[:5]`

at the persisted post-Batch07 freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

The production freeze module does not call either queue live. It stores only the already-derived immutable snapshot.

## 4. Frozen Batch 08 membership

The mechanically derived immutable membership is:

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

These identities and this order are frozen before any Batch 08 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Required adversarial qualification

The membership gate MUST reject or expose:

- raw `recovery_queue()` substitution;
- skipping the first eligible member;
- reordering members;
- substituting a later eligible member;
- shortening or expanding batch cardinality;
- reinserting same-capability attempted BLOCKED dates;
- reintroducing already-resolved Batch 07 PASS dates;
- chronology or duplicate defects;
- prior-attempt contamination;
- caller mutation or caller selection surfaces;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- semantic capability or progression-state drift;
- parent protocol/progression/calendar/coverage regressions.

The gate MUST also prove the frozen module contains no Playwright, Chromium, `probe_candidate`, asyncio, browser/network observation path, or live queue-selection call.

## 6. State mutation boundary

This freeze is scheduling/governance only. It MUST NOT:

- resolve any calendar candidate;
- modify executable calendar evidence;
- append any factual attempt;
- register any material capability change;
- alter progression runtime;
- alter global/window coverage counts;
- freeze the execution window;
- authorize `.bi5` acquisition;
- authorize any real backtest.

Persisted accounting must remain:

- global: `111 / 49 resolved / 62 unresolved / 0 FAIL`;
- execution window: `68 / 26 resolved / 42 unresolved / 0 FAIL`;
- attempt ledger: `35`;
- attempted BLOCKED / execution-ineligible: `9`;
- execution-eligible unresolved: `33`.

## 7. Browser boundary

No Batch 08 browser observation is authorized by this policy candidate.

Only after adversarial membership qualification reaches PASS may the next governed action be defined as execution of exactly `batch08_targets()` under the already-qualified capture chain.

No `.bi5`. No real backtest.

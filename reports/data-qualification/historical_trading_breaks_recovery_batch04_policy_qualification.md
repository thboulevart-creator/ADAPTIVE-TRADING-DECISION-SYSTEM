# HISTORICAL TRADING BREAKS RECOVERY — BATCH 04 POLICY QUALIFICATION

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

## Final verdict

**PASS — `BATCH04_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Batch 04 was frozen and adversarially qualified before any Batch 04 historical broker observation.

Frozen size:

`BATCH_SIZE = 5`

Frozen membership:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

## Freeze provenance

Pre-freeze checkpoint HEAD:

`4d3c5db74ec31215b74799f27cdfe476d513014b`

Source post-Batch03 atomic integration / progression-state commit:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Semantic capability:

- ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- calendar unresolved at freeze: `57`
- historical attempts at freeze: `15`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `4`
- execution-eligible unresolved: `53`

## Deterministic membership proof

The qualification mechanically asserted:

`batch04_targets() == eligible_recovery_queue()[:5]`

against the current governed repository state and recovered exactly the five frozen members above.

The raw unresolved prefix is not an admissible source. `recovery_queue()[:5]` contains the already-attempted BLOCKED prefix and therefore differs from Batch 04 membership.

Each Batch 04 member was proven to be:

- currently unresolved;
- execution-eligible;
- `ELIGIBLE — INITIAL_ATTEMPT`;
- absent from the historical attempt ledger;
- unique and chronological.

The following four dates remain unresolved but are execution-ineligible under the unchanged capability and were proven absent from Batch 04:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Their exclusion is scheduling only. They remain unresolved and are not promoted to negative evidence.

## Adversarial coverage

The Batch 04 suite rejects or proves against at least:

- batch-size drift;
- membership drift from current `eligible_recovery_queue()[:5]`;
- raw `recovery_queue()[:5]` substitution;
- reinsertion of already-attempted BLOCKED dates;
- prior-attempt contamination;
- non-`INITIAL_ATTEMPT` eligibility;
- duplicate or non-chronological membership;
- mutable-return corruption;
- caller/manual membership inputs;
- expected-outcome, priority, holiday-type, source-availability or manual-skip selection surfaces;
- semantic-capability fingerprint drift;
- unexpected material capability-change registry entries;
- browser/probe execution code inside the membership freeze module.

Parent progression, recovery protocol, Batch 03 adjudication/integration, calendar coverage and execution-window boundary tests were run in the same qualification suite.

## Authoritative adversarial execution

- workflow run: `34894947834`
- job: `104146491103`
- trigger commit: `641b0e0369ed5a47c4adb69370e2b166b8088c06`
- conclusion: **SUCCESS**
- adversarial/regression suite: **104 passed in 0.35s**
- exact `eligible_recovery_queue()[:5]` membership assertion: **PASS**
- no-browser/no-probe execution-path guard: **PASS**

The exact runtime assertion printed the five frozen dates in governed order and confirmed that the Batch 04 freeze equals the first five current execution-eligible entries.

## Browser boundary

The qualified Batch 04 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

No Batch 04 historical broker observation occurred during this qualification.

The qualification workflow was archived to `workflow_dispatch` only after PASS so normal pushes cannot silently replay the completed membership qualification.

## Boundary after PASS

Batch 04 membership is now immutable historical membership. It MUST NOT be recalculated, substituted, expanded, shortened or reordered based on any later observation.

This PASS authorizes only the next governed action: execute these exact five frozen dates under the already-qualified Trading Breaks route, with parent/progression/Batch04 gates passing before Chromium opens, then independently adjudicate all five results.

Calendar evidence accounting is unchanged by membership freeze alone.

No `.bi5` acquisition. No real backtest.

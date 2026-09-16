# Historical Trading Breaks Recovery — Batch 15 V2 persisted-HEAD re-break

## Verdict

**PASS — `BATCH15_V2_PERSISTED_HEAD_REBREAK_CONFIRMS_INTEGRATION`**

## Scope

This is an independent, read-only verification of the persisted Batch 15 V2 integration state.

- integration commit: `4dee7e22af1402626341f76611926b108fd1d8c0`
- pre-integration parent: `bfafa6966c39a5eb759d62d493ebb58ef2bdad80`
- corrected verifier HEAD: `4bb7712bcab8b8930c4054e1500302621f881f4f`
- workflow: `Trading Breaks Recovery Batch 15 V2 Persisted HEAD Re-break`
- authoritative run/job: `35085635675 / 104759660665`
- permissions: `contents: read`
- final workflow conclusion: `success`

## First adversarial attempt

The first verifier execution was intentionally not hidden:

- initial verifier commit: `3befa42956f9d4013fced5623f283996f75a227e`
- run/job: `35085516084 / 104759279481`
- conclusion: `failure`
- observed regression result before failure: `65 passed / 2 failed`

Both failures came from replaying `tests/test_trading_breaks_recovery_batch15_v2_adjudication.py` against the post-integration state. That adjudicator is deliberately frozen to the pre-integration governance state of exactly 68 attempts and therefore correctly rejected the post-integration 73-attempt ledger with `BATCH15_ADJUDICATION_GOVERNANCE_STATE_MISMATCH`.

This was a verifier-scope defect, not an integration-state defect. The correction removed only that invalid post-state replay. No calendar, ledger, capability registry, progression code, recovery protocol, or persisted evidence was modified.

## Corrected persisted-state re-break

The corrected run proved all of the following.

### Integration ancestry and atomicity

- `4dee7e22...` is an ancestor of the verifier HEAD;
- `bfafa696...` is the direct pre-integration ancestry boundary used for comparison;
- Batch 15 integration changed exactly three governed files:
  - `tools/dukascopy_usatech_calendar.py`
  - `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
  - `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
- between integration and verifier HEAD, no governed recovery state changed; only the verifier workflow was added/corrected.

### Durable semantic/boundary regression

The post-state-safe suites passed:

- target-day overlap semantics;
- immutable historical source binding;
- USATECH calendar regression;
- calendar coverage regression;
- execution-window boundary regression.

Observed result:

`65 passed in 0.25s`

### Frozen Batch 15 V2 membership

Membership remains exactly:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

### Historical attempt immutability

- pre-integration attempts: `68`
- post-integration attempts: `73`
- attempts `1..68`: exact semantic equality with the pre-integration ledger
- capability definitions: unchanged by Batch 15 integration
- current capability remains `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current capability fingerprint remains `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

### Retry attempts 69..73

All five V2 retries remain PASS with no blocking reason and with adjudication reason:

`TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED`

Each retry retains exactly the provenance of its immutable historical V1 source attempt, and each executable calendar entry is bound to that same source attempt and provenance.

### Exact persisted coverage/progression

Global calendar:

- candidates: `111`
- resolved: `79`
- unresolved: `32`
- orphan evidence: `0`
- contradictions: `0`
- evidence-shape errors: `0`

Execution-window candidate `2021-08-14 → 2026-08-14`:

- candidates: `68`
- resolved: `56`
- unresolved: `12`
- FAIL: `0`

Attempt ledger:

- attempts: `73`
- material capability changes: `1`

Current deterministic execution eligibility:

- Class-A overlap-V2 eligible retries remaining: `9`
- Class-B ineligible unresolved dates: `3`

The three Class-B dates remain unresolved and absent from executable calendar evidence:

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Their current reason remains:

`RETRY_MATERIAL_CHANGE_NOT_PROVEN:BLOCKING_REASON_NOT_EXPLICITLY_ADDRESSED`

### Determinism and read-only boundary

- progression regeneration: byte-stable;
- final worktree: clean;
- verifier mutation: NONE;
- workflow token permission: `contents: read`.

## Closure

Batch 15 V2 integration is **FULLY CLOSED**.

This PASS does not authorize `.bi5` acquisition or a real backtest.

The next work must be decided from the now-current deterministic state. Batch 16 must not be inferred merely because Batch 15 succeeded; the critical path must be re-evaluated before any new freeze or execution.

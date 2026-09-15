# HISTORICAL TRADING BREAKS RECOVERY — BATCH 14 TERMINAL-REMAINDER POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH14_TERMINAL_POLICY_V1`

Parent protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

## Purpose

Define the only admissible final recovery batch under the **current unchanged capability** when fewer candidates remain execution-eligible than the nominal operational batch size.

This policy is versioned before any Batch 14 target observation.

## Nominal and terminal size rule

Nominal recovery batch size remains:

`NOMINAL_BATCH_SIZE = 5`

A terminal remainder batch is allowed only when the deterministic pre-observation state satisfies:

`0 < len(eligible_recovery_queue()) < NOMINAL_BATCH_SIZE`

When that condition holds:

`terminal_batch = tuple(eligible_recovery_queue())`

Therefore terminal size is not chosen from target outcomes, holiday identity, expected ease, broker evidence, or backtest performance. It is mechanically equal to the **entire remaining eligible queue**.

Padding is forbidden. A same-capability BLOCKED/ineligible date cannot be inserted merely to preserve a five-item visual batch.

If eligible count is `0`, no terminal batch exists. If eligible count is `>= 5`, this terminal policy is inapplicable and MUST fail closed.

## Current pre-observation state

At baseline HEAD `57bdcea7f417d8bf558e6a59498f1b753bace2f2`:

- recovery queue: `19`
- attempt ledger: `65`
- same-capability BLOCKED/ineligible: `16`
- eligible unresolved: `3`
- material capability changes: `0`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The complete eligible queue is:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Batch 14 terminal membership is exactly those three items, in that order.

## Anti-selection invariants

Before any browser observation, executable qualification MUST reject at minimum:

- omission of any one of the three eligible candidates;
- reordering or reversal;
- duplication;
- substitution with any same-capability BLOCKED/ineligible candidate;
- adding/padding any fourth candidate;
- changing the terminal size from the eligible queue length;
- applying this terminal policy when five or more candidates are eligible;
- recomputing membership after target-specific evidence has been observed.

## Evidence boundary

The policy changes neither capability nor historical verdicts.

The existing `16` same-capability BLOCKED/ineligible dates remain unresolved and visible. Batch 14 cannot borrow, reclassify, or silently clear them.

No `.bi5` acquisition, execution-window freeze, or real backtest is authorized by this policy.

## Required continuation

1. mechanically freeze the complete three-item eligible queue;
2. adversarially qualify that freeze read-only;
3. independently re-break the persisted membership read-only;
4. only after both PASS may browser capture begin.

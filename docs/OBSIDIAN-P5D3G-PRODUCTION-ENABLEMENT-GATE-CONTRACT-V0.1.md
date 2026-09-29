# P5-D3G — Production Enablement / Real-Live Publication Gate V0.1

## Purpose

This gate separates production planning authority from production execution authority.

It exists to make it possible to inspect the exact real Obsidian Vault read-only and build one exact publication plan without weakening the already-qualified sacrificial publication runtime.

## Core rule

The current P5-D3G runtime remains sacrificial-only.

The real-Vault guard is not removed.

A later production-planning implementation must use a distinct explicit entrypoint with READ-ONLY authority only.

## Two-stage human authority

### Stage A — plan approval

The system may:

1. inspect the exact real Vault read-only;
2. verify the retained P5-D3F handoff;
3. capture the exact CURRENT / CURRENT.tmp / target-generation prestate;
4. build a deterministic production plan;
5. bind one one-shot human plan approval to the exact plan;
6. prove that the real Vault did not change;
7. persist evidence outside the real Vault;
8. STOP.

Stage-A approval is not publication authority.

### Stage B — execution authorization

Stage B is outside this gate.

It requires a separate later human instruction after Stage-A qualification.

Any future execution authorization must bind both the exact Stage-A plan and the exact Stage-A approval, then revalidate the real Vault immediately before any first mutation.

## Qualification boundary

Contract qualification itself may not touch the real Vault.

The subsequent production-enablement implementation qualification may read the real Vault but may not write it.

Success therefore means:

    PASS_PRODUCTION_ENABLEMENT_READ_ONLY_GATE_QUALIFIED

and simultaneously:

    REAL PUBLICATION EXECUTED = FALSE
    PRODUCTION CURRENT MUTATED = FALSE
    PRODUCTION GENERATION MATERIALIZED = FALSE
    PRODUCTION PROMOTION_CONFIRMED = FALSE
    STAGE-B EXECUTION AUTHORITY ISSUED = FALSE

## Fail-closed requirements

Any production planner must fail closed on:

- wrong or aliased real-Vault identity;
- invalid retained handoff;
- changed CURRENT prestate;
- changed CURRENT.tmp state;
- changed target-generation state;
- plan tampering;
- missing or mismatched Stage-A approval;
- Stage-A approval reuse;
- any mutation observed during planning;
- any reachable production execution surface;
- any premature Stage-B authority.

## Mandatory STOP

After the read-only production-enablement gate qualifies, execution remains closed.

A distinct human authorization is required before any real publication transaction can be opened.

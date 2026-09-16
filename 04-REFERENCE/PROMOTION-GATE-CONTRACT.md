# P1.0 — PROMOTION GATE FAIL-CLOSED + EXECUTABLE TIERING

**Contract ID:** `PROMOTION_GATE_FAIL_CLOSED_V1`  
**Tier:** A  
**Initial mode:** `REJECT_ALL_PROMOTION`

## Purpose

No transition may increase operational permission, reduce a proof/tier requirement, or otherwise relax governance without passing one explicit promotion gate.

P1.0 establishes the mechanism only. It does **not** authorize native `.bi5` acquisition, real-data backtest, live execution, or any governance relaxation.

Normative sources already versioned in this repository:

- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md` — `GOVERNANCE_RELAXATION_COOLING_OFF_V1`, A→B is an assouplissement, Tier-A relaxation requires observable revocation/detection/blast-radius/rollback/monitor conditions;
- `GOVERNANCE/META-GOVERNANCE-AND-SELF-CHALLENGE.md` — learning/validation is separated from controlled authorization and deployment;
- P0.6 checkpoint — the next gate must initially deny promotion by default.

## Canonical decision chain

`REQUESTED TRANSITION → CONSEQUENCES → DERIVED TIER → BOUNDARY TIER INHERITANCE → PERMISSION DELTA → RELAXATION? → RELAXATION READINESS → PROMOTION GATE → PASS / FAIL / BLOCKED`

## Tier order

The safety order is:

`C < B < A`

A boundary inherits the **maximum** tier among the participating tiers and the tier derived from its consequences. A caller may not lower the effective tier by declaring a weaker target tier.

### Tier A consequences

Any of the following derives Tier A:

- `PERMISSION_INCREASE`
- `GOVERNANCE_RELAXATION`
- `EVIDENCE_REQUIREMENT_REDUCTION`
- `TIER_REQUIREMENT_REDUCTION`
- `NATIVE_ACQUISITION_OR_REAL_BACKTEST`
- `LIVE_OR_EXTERNAL_SIDE_EFFECT`
- `CAPITAL_OR_REAL_WORLD_EXPOSURE`
- `TRUST_BOUNDARY_CHANGE`
- any unknown or ambiguous consequence
- an empty consequence set, because consequence completeness is then unproven

### Tier B consequence

`DETERMINISTIC_INTERNAL_ONLY` is Tier B only when it is the strongest declared consequence and cannot increase permission, external effects, persisted authority, evidence requirements, or research conclusions.

### Tier C consequence

`RESEARCH_ONLY_NON_AUTHORIZING` is Tier C only when it is the strongest declared consequence and cannot itself change permissions or operational state.

Mixed consequences inherit the strongest tier.

## Protected permission vocabulary

P1.0 knows the following permissions:

- `NATIVE_BI5_ACQUISITION`
- `REAL_DATA_BACKTEST`
- `LIVE_EXECUTION`
- `GOVERNANCE_RELAXATION`

A target containing an unknown permission is invalid rather than implicitly accepted.

A permission increase is any permission present in the target set but absent from the current set.

A restriction is a target permission set that is a strict subset of the current set.

## Relaxation

A transition is a relaxation if at least one of these is true:

- it adds any protected permission;
- it lowers the requested tier (`A→B`, `A→C`, or `B→C`);
- its consequence set includes `GOVERNANCE_RELAXATION`, `EVIDENCE_REQUIREMENT_REDUCTION`, or `TIER_REQUIREMENT_REDUCTION`.

A stricter tier (`C→B`, `C→A`, `B→A`) is not a relaxation by itself.

## Cooling-off rule

When a proposed relaxation is causally linked to a loss, incident, missed opportunity, or operational constraint related to the rule being relaxed, a minimum 30-day cooling-off applies.

A same-cause event during that period resets the cooling-off. P1.0 may study or harden during the cooling-off but may not promote the relaxation.

## Tier-A relaxation readiness

For an effective Tier-A relaxation, readiness is incomplete unless all are demonstrated:

1. observable revocation condition;
2. sufficiently timely detection;
3. reaction latency compatible with risk;
4. bounded blast radius;
5. executable revocation;
6. rollback or safe state defined;
7. monitor sufficiently independent from the mechanism being monitored;
8. monitor falsifiable by injection of a revocation condition;
9. revocation cost bounded and known.

These conditions establish only **readiness evidence**. They do not authorize a P1.0 promotion.

## P1.0 authorization invariant

P1.0 is deliberately `REJECT_ALL_PROMOTION`:

- no permission increase can return PASS;
- no tier downgrade can return PASS;
- no governance/evidence relaxation can return PASS;
- supplying every Tier-A readiness field still cannot return PASS;
- acquisition/backtest/live permissions remain absent.

The only PASS outcomes allowed in P1.0 are non-promotional outcomes:

- no permission/tier relaxation (`NO_PROMOTION`);
- a strictly more restrictive permission set (`RESTRICTION_ALLOWED`);
- a stricter tier with no permission increase (`TIER_HARDENING_ALLOWED`).

Malformed or unknown permission state returns FAIL. Missing/insufficient proof for a requested relaxation returns BLOCKED. A fully evidenced requested promotion still returns BLOCKED with the reject-all reason.

## Existing acquisition boundary

The existing acquisition evaluator must remain independently fail-closed **and** must not be able to produce an operational acquisition authorization without crossing this promotion gate. P1.0 therefore requires the acquisition authorization path to be promotion-gate-bound.

## Side-effect invariant

The P1.0 evaluator is pure/read-only:

- no network access;
- no file writes;
- no subprocess execution;
- no acquisition;
- no backtest;
- no live action.

## Qualification protocol

`formalisation → pre-correction FAIL → minimal implementation → F0–F20 adversarial break → P0.2–P0.6 re-break → persisted-HEAD verdict`

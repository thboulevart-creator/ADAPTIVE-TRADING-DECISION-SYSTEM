# P1.0 — PROMOTION GATE + EXECUTABLE TIERING CONTRACT

**Contract ID:** `PROMOTION_GATE_TIERING_V1`  
**Tier:** A  
**Initial mode:** `REJECT_ALL`

## Purpose

No transition may increase system permission, reduce required evidence, lower a proof tier, enable acquisition/backtest/live capability, or relax governance without passing one explicit promotion gate.

Normative chain:

`REQUESTED TRANSITION → CONSEQUENCE → TIER → BOUNDARY INHERITANCE → PERMISSION DELTA → RELAXATION? → EVIDENCE/REVOCATION CONDITIONS → GATE → PASS / FAIL / BLOCKED`

## Fail-closed rules

1. Unknown capability, consequence, tier, transition, evidence state or permission state is `BLOCKED`.
2. Absence of an explicit gate is `BLOCKED`.
3. A system may become more restrictive without a permissive promotion.
4. Any increase in effective permission is a promotion and requires an explicit gate.
5. Any reduction in evidence strength, refusal criteria or boundary tier is a governance relaxation.
6. `A → B` is always a relaxation.
7. Boundary tier is the maximum tier implied by the consequences protected by that boundary.
8. Caller-declared tier never overrides consequence-derived tier.
9. P1.0 has no allowlist of permissive transitions: every permission-increasing or relaxation request is denied by default.
10. P1.0 must not authorize native `.bi5` acquisition, real backtest, live execution or any equivalent capability.

## Consequence-derived tiers

The evaluator must derive tier from consequences, not from component labels.

- `A`: a failure could increase external/financial/operational permission, violate a critical trust boundary, corrupt authoritative evidence/provenance, bypass a safety gate, or make an irreversible/high-impact action possible.
- `B`: failure is bounded to deterministic internal computation/research state and cannot itself increase operational permission or corrupt a Tier-A authority.
- `C`: hypothesis/research-only state that cannot become operational authority without a later Tier-A gate.

If multiple consequences apply, the effective tier is the maximum severity: `A > B > C`.

## Relaxation controls

Governance relaxation follows existing `GOVERNANCE_RELAXATION_COOLING_OFF_V1`.

A relaxation causally linked to a loss, incident, missed opportunity or operational constraint is subject to the existing minimum 30-day cooling-off period. Same-cause recurrence resets the period.

For Tier A, permissive relaxation remains `BLOCKED` unless all existing governance conditions are evidenced:

- observable revocation condition;
- timely detection;
- reaction latency compatible with risk;
- bounded blast radius;
- executable revocation;
- rollback/safe state;
- sufficient monitor independence;
- monitor falsifiability by injected revocation condition;
- bounded and known revocation cost.

These conditions are necessary but **not sufficient** in P1.0 because the initial gate is reject-all.

## Initial P1.0 verdict semantics

- Restrictive/no-permission-increase transition: `PASS` only as a non-promotion classification; it grants no new capability.
- Permission increase or governance relaxation: `BLOCKED` with reject-all reason, even if supporting conditions are present.
- Invalid/unknown/incomplete request: `BLOCKED`.
- No path in P1.0 returns an authorization for acquisition, real backtest or live execution.

## Required adversarial attacks

At minimum:

- caller lies about tier;
- mixed consequences where one is Tier A;
- unknown consequence;
- permission increase disguised as neutral transition;
- evidence requirement reduced without permission flag;
- A→B downgrade;
- missing explicit gate;
- direct capability boolean bypass;
- self-declared PASS/evidence boolean;
- cooling-off bypass;
- incomplete Tier-A revocation package;
- monitor non-independence;
- non-falsifiable monitor;
- unbounded blast radius/revocation cost;
- acquisition/backtest/live requests;
- restrictive transition remains possible without granting a higher permission.

## Scope boundary

P1.0 builds and qualifies the reject-all promotion/tiering mechanism only. It does not define the first permissive promotion policy and does not authorize acquisition, real backtest or live execution.

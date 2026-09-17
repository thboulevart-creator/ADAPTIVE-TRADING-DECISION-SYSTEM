# P1.0 — PROMOTION GATE TIERING / ADVERSARIAL COMPANION

**Status:** `NON_NORMATIVE_QUALIFICATION_COMPANION`  
**Canonical authority:** `04-REFERENCE/PROMOTION-GATE-CONTRACT.md`  
**Canonical contract ID:** `PROMOTION_GATE_FAIL_CLOSED_V1`  
**Historical superseded ID:** `PROMOTION_GATE_TIERING_V1`

## Purpose

This file is retained only as a qualification companion for P1.0. It does not define a second promotion contract.

All permission semantics, verdict semantics, tier ordering, consequence classification, relaxation rules, evidence requirements, cooling-off rules and authorization invariants are owned exclusively by `PROMOTION-GATE-CONTRACT.md`.

If this companion is inconsistent with the canonical contract, the inconsistency is a qualification defect; this file never overrides the canonical contract.

## Qualification map derived from the canonical contract

The implementation and tests must demonstrate the canonical chain:

`REQUESTED TRANSITION → CONSEQUENCES → REQUEST VALIDITY → DERIVED TIER → BOUNDARY MAX-TIER → PERMISSION DELTA → RELAXATION ? → EVIDENCE / REVOCATION CONDITIONS → PROMOTION GATE → PASS / FAIL / BLOCKED`

The qualification surface must explicitly exercise at least these adversarial classes:

- caller lies about tier;
- mixed consequences where one is Tier A;
- unknown consequence: conservative Tier-A derivation plus evaluator `BLOCKED`;
- empty consequence set: conservative Tier-A derivation plus evaluator `BLOCKED`;
- permission increase disguised as neutral transition;
- evidence requirement reduced without permission flag;
- A→B downgrade;
- unknown tier or permission state;
- direct capability bypass;
- self-declared PASS/evidence bypass;
- cooling-off bypass;
- incomplete Tier-A revocation package;
- monitor non-independence;
- non-falsifiable monitor;
- unbounded blast radius or revocation cost;
- native acquisition, real-backtest and live requests;
- restrictive/non-promotional transitions remain possible without granting a higher permission;
- forced legacy acquisition `PASS` remains externally `BLOCKED` by the canonical promotion gate.

## Scope boundary

This companion adds no capability and grants no authorization. P1.0 remains `REJECT_ALL_PROMOTION`; native `.bi5` acquisition, real-data backtest and live execution remain unauthorized.

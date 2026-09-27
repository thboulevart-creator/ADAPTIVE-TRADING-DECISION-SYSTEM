# OBSIDIAN P5-D3A — CANDIDATE EVALUATION CONTRACT PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3A defines the finite controlled candidate-evaluation contract only.

No evaluator runtime is implemented or authorized.

## Qualified predecessor

P5-D2 qualification commit:

    6096984eec9f923c31f70508cc7000408290fb56

P5-D2 qualification report blob:

    68cda09d273f19a2a93e1fcd9b0c393e72cd5a35

## Candidate branch

    feat/obsidian-projection-p5d3a-candidate-evaluation-contract-v0.1

## Exact functional candidate

    f145744b5aafbc9837b4cc140df38afd09d3ce39

This exact HEAD is the P5-D3A functional candidate for local re-break.

Later report commits are evidence-only and do not replace it.

## Persisted candidate artifacts

Contract:

    tools/obsidian_projection/candidate_evaluation_contract_v0_1.json
    blob: 52d1aa79d04b99a75f9a00befc0251f2aec9256e

Contract breakers:

    tests/obsidian_projection/test_candidate_evaluation_contract_v0_1.py
    blob: 33ee17a6528f208380cbdcf9604510de9fbd1f9c

Documentation:

    docs/OBSIDIAN-P5D3A-CONTROLLED-CANDIDATE-EVALUATION-CONTRACT-V0.1.md
    blob: 1df5efa9d8725bd557d0bdd84abb3cd917bd48cf

## Static contract inventory

Required breakers:

    84 unique

Python contract-test methods:

    24

These are repository counts only and are not execution evidence.

## Functional delta

Relative to the qualified P5-D2 checkpoint, the functional P5-D3A candidate adds exactly three artifacts:

1. candidate-evaluation contract;
2. contract breaker module;
3. documentation.

No previously qualified source file is modified.

## Critical repository findings captured by the contract

### Current-head semantic bridge is not yet qualified

P5-B2 produces:

    DynamicInventory
    ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1

The existing semantic classifier consumes:

    FrozenInventory
    ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1

The current P2 path still requires exactly:

    74 semantic records

Therefore no direct DynamicInventory → existing classifier/current-head projection path is treated as already qualified.

P5-D3A forbids:

- implicit DynamicInventory → FrozenInventory coercion;
- guessing selection_zone → inventory_class;
- retaining the pilot 74-record hardcode;
- silently dropping unsupported dynamic entries;
- silently upgrading metadata-only content to full text.

### Real candidate-generation packaging is not yet qualified

P5-C2 qualified the immutable-generation atomic-pointer primitive in a sacrificial promotion experiment.

That qualification does not establish that the P5-C2 experimental fixture generator is a real current-head projection packager.

A separate candidate-generation staging contract is therefore required before the finite orchestrator.

## Outcome semantics

P5-D3A distinguishes:

    QUALIFIED
    REJECTED
    BLOCKED

QUALIFIED:

    emits candidate EVALUATION_PASSED

REJECTED:

    emits candidate EVALUATION_FAILED

BLOCKED:

    emits no P5-D2 evaluation-result event

The BLOCKED rule is deliberate because qualified P5-D2 has no EVALUATION_BLOCKED event and infrastructure uncertainty must not be converted into false candidate rejection.

For BLOCKED:

    observer remains EVALUATING
    P5-D2 sequence does not advance

## Last-known-good boundary

Throughout P5-D3 candidate evaluation:

    live_projection_head_after
        ==
    live_projection_head_before

and:

    real_vault_modified = false
    production_promotion_authorized = false

## Required local re-break

Before P5-D3A may qualify:

1. recover exact functional candidate HEAD f145744b5aafbc9837b4cc140df38afd09d3ce39;
2. require a clean control checkout;
3. py_compile the P5-D3A contract breaker;
4. execute the targeted P5-D3A contract breaker;
5. execute the full tests/obsidian_projection suite;
6. require the control checkout to remain source-clean.

No P5-D3B implementation is authorized before this re-break passes.

## Next governed boundary on PASS

    P5-D3B — CURRENT-HEAD SEMANTIC PROJECTION BRIDGE

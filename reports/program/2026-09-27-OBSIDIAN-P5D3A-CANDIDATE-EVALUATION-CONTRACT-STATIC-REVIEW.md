# OBSIDIAN P5-D3A — CANDIDATE EVALUATION CONTRACT STATIC REVIEW

Date: 2026-09-27

## Review status

This is a static review performed by the same assistant that designed the P5-D3A contract.

It is not an independent review.
It is not local runtime evidence.
It does not qualify P5-D3A.
It does not authorize P5-D3B.

## Functional candidate reviewed

    f145744b5aafbc9837b4cc140df38afd09d3ce39

Branch:

    feat/obsidian-projection-p5d3a-candidate-evaluation-contract-v0.1

Evidence-only preflight commit:

    f02b31e64d365ed129afcaf6e056b28dda69fd20

## Exact candidate artifacts

Contract:

    tools/obsidian_projection/candidate_evaluation_contract_v0_1.json
    52d1aa79d04b99a75f9a00befc0251f2aec9256e

Contract breakers:

    tests/obsidian_projection/test_candidate_evaluation_contract_v0_1.py
    33ee17a6528f208380cbdcf9604510de9fbd1f9c

Documentation:

    docs/OBSIDIAN-P5D3A-CONTROLLED-CANDIDATE-EVALUATION-CONTRACT-V0.1.md
    1df5efa9d8725bd557d0bdd84abb3cd917bd48cf

## Delta boundary

Relative to the qualified P5-D2 checkpoint, the functional P5-D3A candidate adds exactly three files:

- one contract;
- one contract-breaker module;
- one documentation file.

No previously qualified source file is modified.

## Static predecessor checks

    exact repository pinned                                  PASS
    exact monitored branch pinned                            PASS
    P5-D1 contract pinned                                    PASS
    P5-D2 contract pinned                                    PASS
    P5-D2 implementation pinned                              PASS
    P5-D2 qualification report pinned                        PASS
    P5-D2 qualification commit pinned                        PASS
    P5-B2 dynamic-inventory implementation pinned            PASS
    P5-B2 qualification report pinned                        PASS
    P5-C2 promotion qualification report pinned              PASS

## Activation checks

P5-D3 activation requires:

    qualified P5-D2 tick result                              PASS
    START_EXACT_HEAD_EVALUATION decision                     PASS
    observer phase EVALUATING                                PASS
    candidate == decision candidate                          PASS
    candidate == pending queue head                          PASS
    automatic promotion authority false                      PASS
    production write authority false                         PASS
    source tick audit binding                                PASS

## Authority checks

    GitHub remote remains canonical                          PASS
    isolated checkout is read-only execution input           PASS
    staged candidate remains unpromoted derived artifact     PASS
    live projection remains last-known-good                  PASS
    observer state changes only through P5-D2 tick           PASS
    evaluator cannot push/commit GitHub                      PASS
    evaluator cannot mutate canonical worktree               PASS
    evaluator cannot mutate real Vault                       PASS
    evaluator cannot promote candidate                       PASS

## Isolation checks

    disposable checkout required                             PASS
    checkout outside canonical worktree                      PASS
    checkout outside Vault                                   PASS
    staging outside real Vault                               PASS
    Git worktree-registry dependency forbidden               PASS
    exact origin required                                    PASS
    exact branch required                                    PASS
    exact commit required                                    PASS
    checkout HEAD == candidate                               PASS
    candidate tree identity recorded                         PASS
    canonical worktree remains unchanged                     PASS

## Ordered pipeline

The contract preregisters an ordered finite pipeline from P5-D2 activation through exact-head isolation, P5-B2 inventory, semantic projection bridge, deterministic double build, preregistered breakers, candidate-generation staging, outcome classification and P5-D2 result transition.

Any failed gate stops later gates.

Partial candidates may never become QUALIFIED.

Live projection and real Vault remain unchanged throughout evaluation.

Static review: PASS.

## Current-head semantic bridge finding

Repository evidence shows:

    P5-B2 output type = DynamicInventory
    P5-B2 schema = ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1

while the existing semantic classifier consumes:

    FrozenInventory
    ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1

and the current P2 build path explicitly expects:

    74 semantic records

The P5-D3A contract therefore correctly marks:

    current_head_semantic_bridge_gap.status
        = OPEN_REQUIRED_SUBFRONTIER

The contract forbids:

    implicit DynamicInventory -> FrozenInventory conversion  PASS
    selection_zone -> inventory_class guessing               PASS
    metadata-only -> full-text silent upgrade                PASS
    frozen pilot substitution                                PASS
    retained 74-record continuous-mode hardcode              PASS
    silent dynamic-entry drop                                PASS
    unsupported artifact silent acceptance                   PASS
    classifier reuse without applicability proof             PASS

This prevents the orchestrator from being built on a fictitious interface.

## Semantic bridge requirements

Every dynamic inventory entry must receive an explicit disposition.

Allowed dispositions are preregistered.

Source path/blob/commit/tree identity must be preserved.

Bridge rules and bridge output must be digest-bound.

Unsupported artifacts fail closed.

Static review: PASS.

## Deterministic double-build checks

    same candidate HEAD required                             PASS
    same candidate tree required                             PASS
    same dynamic inventory digest required                   PASS
    same semantic input digest required                      PASS
    same projection contract required                        PASS
    independent stage roots required                         PASS
    exact file-map equality required                         PASS
    projection-tree digest equality required                 PASS
    semantic-record digest equality required                 PASS
    manifest digest equality required                        PASS
    generated-file count equality required                   PASS
    any mismatch => candidate REJECTED                        PASS

## Breaker boundary checks

    preregistered breaker manifest required                  PASS
    breaker manifest digest required                         PASS
    vague "run all tests" rejected as insufficient           PASS
    candidate breaker failure => REJECTED                    PASS
    breaker infrastructure failure => BLOCKED                PASS
    source/live mutation by breakers forbidden               PASS

## Candidate-generation packaging finding

P5-C2 qualified an immutable-generation atomic-pointer primitive in a sacrificial promotion experiment.

That does not establish that the experimental P5-C2 fixture builder is a real current-head projection packager.

The contract therefore correctly marks:

    candidate_generation_packaging_gap.status
        = OPEN_REQUIRED_SUBFRONTIER

It forbids relabelling experimental fixture generation as real candidate packaging.

A separate candidate-generation staging contract is required before the finite orchestrator.

Static review: PASS.

## Candidate-generation identity checks

The staged generation must bind:

    repository                                               PASS
    branch                                                   PASS
    candidate HEAD                                           PASS
    candidate tree                                           PASS
    dynamic inventory digest                                 PASS
    semantic bridge digest                                   PASS
    semantic record digest                                   PASS
    projection contract version                              PASS
    projection tree digest                                   PASS
    generated file count                                     PASS
    breaker manifest digest                                  PASS

It must be complete before verification and immutable after sealing.

No CURRENT/pointer mutation is permitted during P5-D3.

## Outcome semantics review

Exact outcomes:

    QUALIFIED
    REJECTED
    BLOCKED

QUALIFIED means all candidate-validity gates passed.

REJECTED means deterministic candidate evidence proves violation.

BLOCKED means candidate validity could not be determined because infrastructure/tooling/evidence was insufficient.

The contract explicitly forbids conflating REJECTED and BLOCKED.

Static review: PASS.

## P5-D2 result-event review

    QUALIFIED => EVALUATION_PASSED                           PASS
    REJECTED => EVALUATION_FAILED                            PASS
    BLOCKED => no P5-D2 evaluation-result event              PASS

For BLOCKED:

    observer remains EVALUATING                              PASS
    event sequence does not advance                          PASS

This preserves epistemic meaning because qualified P5-D2 has no EVALUATION_BLOCKED event.

Direct observer-state mutation is forbidden.

Determinate result events must be applied by the qualified P5-D2 one_shot_tick.

## Last-known-good and report review

Evaluation report requires before/after live HEAD fields.

The contract requires:

    live_projection_head_after == live_projection_head_before
    real_vault_modified = false
    production_promotion_authorized = false

Static review: PASS.

## Retry semantics review

BLOCKED may retry the same exact candidate only after all identity gates are revalidated.

Unverified partial candidates may not become qualified through retry.

REJECTED may not be silently reclassified as BLOCKED to obtain retry semantics.

QUALIFIED still does not imply promotion authority.

Static review: PASS.

## Runtime non-authorizations

P5-D3A boundary confirms false for:

    semantic bridge implementation                           PASS
    candidate-generation packager                            PASS
    finite evaluation orchestrator                           PASS
    network fetch execution                                  PASS
    isolated checkout execution                              PASS
    candidate breaker execution                              PASS
    P5-D2 result-event execution                             PASS
    background observer                                      PASS
    polling loop                                             PASS
    production promotion                                     PASS
    continuous Vault write                                   PASS
    Windows startup registration                             PASS
    scheduled task                                           PASS
    Windows service                                          PASS
    Graph/Search CURRENT semantics                           PASS

## Breaker inventory

Required breakers:

    84

Unique required breakers:

    84

Persisted Python contract-test methods:

    24

These are static repository counts only and are not executed evidence.

## Next gates

The repository-visible interface gaps justify the ordered P5-D3 decomposition:

    P5-D3B — CURRENT-HEAD SEMANTIC PROJECTION BRIDGE
    P5-D3C — CANDIDATE GENERATION STAGING CONTRACT
    P5-D3D — FINITE CANDIDATE EVALUATION ORCHESTRATOR
    P5-D3E — SANDBOX CANDIDATE EVALUATION QUALIFICATION

Then:

    P5-D4 — BOUNDED OBSERVER LOOP CANDIDATE
    P5-E  — END-TO-END NEAR-REAL-TIME QUALIFICATION
    P6    — CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

## Limitation

No Python compilation or test execution was performed by this static review.

No network fetch, checkout, inventory build, projection build, staging, candidate breaker or P5-D2 result transition was executed.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK REQUIRED.**

P5-D3A remains unqualified until the exact functional candidate:

    f145744b5aafbc9837b4cc140df38afd09d3ce39

passes the governed local re-break.

# OBSIDIAN P5-D3A — CONTROLLED CANDIDATE EVALUATION CONTRACT V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3A defines the finite qualification pipeline for one exact Git candidate HEAD selected by the qualified P5-D2 observer state machine.

It is a contract-and-breakers phase only.

P5-D3A does not yet implement:

- candidate fetching;
- isolated checkout creation;
- semantic projection of the current HEAD;
- candidate-generation packaging;
- candidate breakers;
- result-event execution;
- promotion;
- any background observer loop.

## 2. Qualified predecessor

P5-D2 qualification commit:

    6096984eec9f923c31f70508cc7000408290fb56

P5-D2 contract:

    5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3

P5-D2 implementation:

    fd212f61ec38332b677110f40265638af55a73e2

P5-D2 qualification report:

    68cda09d273f19a2a93e1fcd9b0c393e72cd5a35

P5-D3A does not reopen P5-D2.

## 3. Activation boundary

The evaluator may only be activated from a qualified P5-D2 tick result whose decision is:

    START_EXACT_HEAD_EVALUATION

The source observer state must already be:

    observer_phase = EVALUATING

The candidate must equal:

    decision.candidate_head
    pending_heads[0]

The source P5-D2 decision must still state:

    automatic_promotion_authorized = false
    production_write_authorized = false

P5-D3A never manufactures its own candidate choice.

## 4. Finite evaluation architecture

Target sequence:

    VALIDATE P5-D2 ACTIVATION
          ↓
    VERIFY REPOSITORY IDENTITY
          ↓
    RESOLVE EXACT CANDIDATE HEAD
          ↓
    CREATE DISPOSABLE ISOLATED CHECKOUT
          ↓
    VERIFY HEAD + TREE
          ↓
    BUILD P5-B2 DYNAMIC INVENTORY
          ↓
    VERIFY INVENTORY IDENTITY
          ↓
    ADAPT CURRENT-HEAD INVENTORY
          ↓
    CLASSIFY CURRENT-HEAD ARTIFACTS
          ↓
    BUILD PROJECTION A
          ↓
    BUILD PROJECTION B
          ↓
    REQUIRE A == B
          ↓
    RUN PREREGISTERED BREAKERS
          ↓
    PACKAGE COMPLETE CANDIDATE GENERATION
          ↓
    VERIFY CANDIDATE GENERATION
          ↓
    CLASSIFY OUTCOME
          ↓
    QUALIFIED / REJECTED / BLOCKED
          ↓
    only if determinate:
    EVALUATION_PASSED or EVALUATION_FAILED
          ↓
    qualified P5-D2 one_shot_tick()

No promotion occurs in this chain.

## 5. Exact-head isolation

The candidate checkout must be:

- disposable;
- outside the canonical user worktree;
- outside the Obsidian Vault;
- independent of the user's Git worktree registry;
- exact-repository verified;
- exact-branch verified;
- exact-commit verified.

The checked-out HEAD must equal the candidate HEAD.

The candidate tree identity must also be recorded.

The canonical user worktree must remain unchanged.

## 6. First discovered interface gap

Static inspection of the qualified repository establishes two different inventory models.

P5-B2 produces:

    DynamicInventory
    schema = ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1

The existing semantic classifier consumes:

    FrozenInventory
    schema = ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1

The current P2 deterministic build path also contains:

    expected 74 semantic records

Therefore there is no already-qualified direct interface:

    DynamicInventory
          ↓
    classify_inventory()
          ↓
    current-head semantic records

P5-D3A explicitly forbids pretending otherwise.

## 7. Consequence: P5-D3B is mandatory

Before the finite evaluator can be implemented, a governed current-head semantic projection bridge must define how every P5-B2 inventory entry is handled.

No implicit mapping is permitted between:

    selection_zone

and:

    inventory_class

No METADATA_ONLY entry may be silently upgraded to full-text semantic content.

No dynamic entry may silently disappear.

Every entry must receive an explicit disposition:

    SEMANTIC_FULL_TEXT
    SEMANTIC_METADATA_ONLY
    EXCLUDED_BY_PREREGISTERED_RULE
    BLOCKED_UNSUPPORTED

The bridge must preserve:

    source_path
    source_blob_sha
    source_commit
    source_tree

and emit its own deterministic digest.

## 8. Existing classifier reuse is conditional

P5-D3A does not reject reuse of the existing classifier.

It requires proof that the classifier's assumptions apply to the new current-head bridge.

Reuse without such proof is forbidden.

The old frozen pilot inventory may not be substituted for P5-B2 current-head inventory.

The old hardcoded 74-record expectation may not survive into continuous candidate evaluation.

## 9. Deterministic double build

The candidate must be projected twice from independent stage roots.

Build A and Build B must share exactly:

    candidate HEAD
    candidate tree
    dynamic inventory digest
    semantic bridge digest / semantic input digest
    semantic record digest
    projection contract version

Qualification requires equality of at least:

    exact generated file map
    projection tree digest
    semantic record digest
    manifest digest
    generated file count

Any deterministic mismatch is a candidate rejection, not an infrastructure block.

## 10. Breaker manifest

"Run the full tests" is not a candidate-breaker contract.

P5-D3 requires a preregistered candidate-breaker manifest with its own digest.

Each candidate evaluation report must bind itself to that exact breaker manifest.

A breaker assertion failure means:

    REJECTED

when it is evidence about the candidate.

A breaker runner infrastructure failure means:

    BLOCKED

unless deterministic candidate evidence proves rejection.

## 11. Second discovered interface gap

P5-C2 qualified the Windows/OneDrive visibility primitive:

    immutable generation
          +
    atomic pointer

That does not prove that the existing P5-C2 experimental fixture generator is a valid packager for a real current-head projection.

The P5-C2 experimental function:

    build_generation(...)

was built for the promotion experiment.

It may not be relabelled as a production/current-head candidate-generation packager without a separate contract.

Therefore P5-D3C is mandatory.

## 12. Candidate-generation requirements

A real candidate generation must be fully assembled outside the live Vault.

Before it can be marked qualified it must bind:

    repository
    branch
    candidate_head
    candidate_tree
    dynamic_inventory_digest
    semantic_bridge_digest
    semantic_record_digest
    projection_contract_version
    projection_tree_digest
    generated_file_count
    breaker_manifest_digest

The generation must be complete before verification and immutable after sealing.

No CURRENT pointer or production pointer may be changed.

## 13. Three terminal evaluation outcomes

P5-D3 distinguishes three outcomes.

### QUALIFIED

All candidate-validity gates passed and the complete staged generation verified.

Result:

    emit candidate EVALUATION_PASSED

### REJECTED

Deterministic evidence establishes that the exact candidate HEAD violates a preregistered candidate-validity rule.

Examples:

- high-confidence secret;
- sensitive tracked path;
- unsupported tracked object;
- unsupported semantic bridge case;
- deterministic A/B mismatch;
- candidate breaker failure;
- invalid candidate generation.

Result:

    emit candidate EVALUATION_FAILED

### BLOCKED

The evaluator cannot determine candidate validity because infrastructure, tooling or evidence is unavailable or inconsistent.

Examples:

- network unavailable before exact fetch;
- wrong configured origin;
- unavailable control workspace;
- contract blob mismatch;
- breaker-runner infrastructure error;
- insufficient evidence to classify a failure.

BLOCKED is not candidate rejection.

## 14. Why BLOCKED emits no P5-D2 event

The qualified P5-D2 vocabulary has:

    EVALUATION_PASSED
    EVALUATION_FAILED

but no:

    EVALUATION_BLOCKED

P5-D3A therefore forbids translating an infrastructure BLOCKED into a false EVALUATION_FAILED.

For BLOCKED:

    no P5-D2 result event is emitted
    P5-D2 event sequence does not advance
    observer state remains EVALUATING

A later governed retry may evaluate the same exact candidate again.

This preserves epistemic meaning without reopening P5-D2.

## 15. Observer-state mutation rule

P5-D3 may never directly edit observer state.

For a determinate result:

    evaluation outcome
          ↓
    normalized P5-D2 event
          ↓
    qualified one_shot_tick()
          ↓
    next observer state

This preserves P5-D2 as the only authority for observer-state transitions.

## 16. Last-known-good boundary

During candidate evaluation:

    live_projection_head_before
        ==
    live_projection_head_after

The real Vault must remain unchanged.

A candidate may be:

    QUALIFIED

without being:

    PROMOTED

Qualification and promotion remain separate authorities.

## 17. Retry semantics

A BLOCKED evaluation may be retried against the same exact candidate HEAD.

The retry must repeat identity gates.

An unverified partial candidate may not be reused as qualified.

A deterministic REJECTED candidate may not be silently reclassified as BLOCKED simply to obtain a retry.

A QUALIFIED staged generation still requires separate promotion authority.

## 18. P5-D3A non-authorizations

P5-D3A authorizes no runtime implementation.

Still forbidden:

    semantic bridge implementation
    candidate-generation packager
    finite orchestrator
    network fetch
    isolated checkout execution
    candidate breaker execution
    P5-D2 result event execution
    background observer
    polling loop
    production promotion
    continuous Vault write
    Windows startup registration
    scheduled task
    Windows service
    Graph/Search CURRENT semantics

## 19. Required sub-frontiers

P5-D3 is now decomposed according to the interfaces actually present in the repository.

If P5-D3A qualifies:

    P5-D3B
    CURRENT-HEAD SEMANTIC PROJECTION BRIDGE

Then:

    P5-D3C
    CANDIDATE GENERATION STAGING CONTRACT

Then:

    P5-D3D
    FINITE CANDIDATE EVALUATION ORCHESTRATOR

Then:

    P5-D3E
    SANDBOX CANDIDATE EVALUATION QUALIFICATION

Only after those may the project approach:

    P5-D4
    BOUNDED OBSERVER LOOP CANDIDATE

The production-oriented end-to-end near-real-time gate remains:

    P5-E

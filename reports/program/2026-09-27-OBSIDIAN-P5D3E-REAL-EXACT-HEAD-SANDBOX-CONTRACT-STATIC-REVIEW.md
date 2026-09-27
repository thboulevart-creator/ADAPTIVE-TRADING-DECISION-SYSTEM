# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX CONTRACT STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static review.

It is not independent.
It is not local runtime evidence.
It does not qualify P5-D3E.
It does not authorize a real candidate evaluation until the local contract re-break passes.

## Functional candidate reviewed

    3d76f3402c7eaba6e911d5f6e3038e9720be2284

Branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-v0.1

Evidence-only preflight commit:

    a20eae470cf2e5613c3e022cbc3feeafe14cd6b3

## Exact contract artifacts

Contract:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Contract breakers:

    f03980d4b650792b49bd13ea8ca5f168e87ef73b

## Delta review

Relative to qualified P5-D3D:

    exactly three P5-D3E contract files added
    no P5-D3D qualified runtime or contract file modified

Static review: PASS.

## P5-D3D predecessor binding

The contract pins:

    P5-D3D qualification commit
    7c244f8ab77d3497a16447b9257c8b204f3e048f

    P5-D3D qualification report blob
    49890581b7c377b26cc4f2379e37b69fc4250c4b

    P5-D3D functional candidate
    6efa84c657bbea4edaa56d643d2b9dc0150bcdb1

    finite evaluator blob
    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

The P5-D3E contract does not reopen or alter P5-D3D semantics.

Static review: PASS.

## Candidate-resolution semantics

The contract permits one network fetch solely to resolve:

    integration/system-v1

through the exact remote-tracking refspec.

The candidate HEAD and TREE are frozen immediately after resolution.

No second network fetch is authorized during evaluation.

Branch movement after capture does not change the candidate under test.

Static review: PASS.

## Design-time HEAD handling

The documentation records the design-time observed real branch identity:

    HEAD
    731380d8f1dd851c52de732c1edaf70f28ecc3c5

    TREE
    1c227d3da4959820797d1d29baab23d9fac4c430

The contract does not hardcode this as the permanent qualification target.

The actual governed run must resolve its own exact candidate immediately before execution.

Static review: PASS.

## Sacrificial clone boundary

The future harness is constrained to:

    OS-temp root
    local clone
    --no-hardlinks
    --no-checkout

The exact candidate object/ref is transferred locally from the control repository.

No network transport is authorized for clone or local candidate transfer.

The clone origin must then be restored to the canonical GitHub origin.

Final candidate checkout must be detached at the exact frozen HEAD.

Static review: PASS.

## Object-store independence

Explicitly forbidden:

    Git alternates
    shared-object-store dependency
    hardlinked object store

Required:

    --no-hardlinks
    no .git/objects/info/alternates

This keeps the sacrificial repository independent from the control repository during evaluator execution.

Static review: PASS.

## Repository identity

Before evaluation the candidate sandbox must satisfy:

    canonical origin
    exact candidate HEAD
    exact candidate TREE
    detached HEAD
    clean worktree

After evaluation the same HEAD/TREE and clean worktree are required.

Static review: PASS.

## Workspace isolation

The evaluation workspace is a fresh sibling of the candidate repository.

It may not be ancestor/descendant of:

    candidate repository
    control repository
    real Vault

Preexisting:

    build-a
    build-b
    candidate-package

are forbidden.

Static review: PASS.

## P5-D2 activation

The contract requires activation through qualified P5-D2 primitives:

    make_initial_state
    REMOTE_HEAD_OBSERVED / INITIAL
    EVALUATION_STARTED

Required activation phase:

    EVALUATING

Required action:

    START_EXACT_HEAD_EVALUATION

The contract explicitly labels this as sandbox control state, not live observer state.

Static review: PASS.

## Real evaluator binding

The runtime evaluator remains exactly the qualified P5-D3D implementation.

No replacement evaluator, alternate builder, or modified breaker runner is authorized by P5-D3E.

Network fetch inside the evaluator remains forbidden.

Static review: PASS.

## Qualification semantics

PASS requires:

    evaluator outcome = QUALIFIED
    failure_code = null
    P5-D2 result event emitted
    package status = PASS_SEALED_UNPROMOTED
    Build A tree digest = Build B tree digest
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    all scientific evidence digests present
    live projection unchanged
    no CURRENT
    no promotion
    no real Vault mutation

This prevents a merely executable but rejected or blocked real candidate from being misreported as P5-D3E PASS.

Static review: PASS.

## REJECTED semantics

Real candidate REJECTED maps to:

    FAIL_REAL_CANDIDATE_REJECTED

It requires:

    P5-D2 result event emitted
    stable non-null failure code

It may not be relabelled BLOCKED or QUALIFIED.

Static review: PASS.

## BLOCKED semantics

Evaluator BLOCKED maps to:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

It requires:

    no P5-D2 result event

It may not be relabelled REJECTED or QUALIFIED.

Static review: PASS.

## Post-package verification

A QUALIFIED real candidate must undergo a second read-only P5-D3C2 package verification.

Required:

    PASS_SEALED_UNPROMOTED

and:

    second candidate-generation digest
        =
    evaluator-reported candidate-generation digest

This creates an explicit post-evaluation integrity confirmation.

Static review: PASS.

## Build evidence

The contract requires both real build manifests to bind the same candidate HEAD/TREE and scientific identities.

Both must show:

    metadata_only_body_read_count = 0

Both must satisfy:

    artifact_record_count = source_record_count

Build A/B projection-tree digests must match.

Static review: PASS.

## Publication boundary

Still false:

    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling loop
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

Static review: PASS.

## Report boundary

The success report is:

    ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_REPORT_V0_1

with status:

    PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

It distinguishes:

    candidate_resolution_network_fetch_performed = true
    evaluation_network_fetch_performed = false

No absolute sandbox path or host identity is permitted.

Static review: PASS.

## Breaker inventory

Required breakers:

    66

Unique required breakers:

    66

Persisted contract-test methods:

    15

These are static repository facts only.

## Non-authorizations before contract qualification

No P5-D3E runtime harness is yet authorized.

No real candidate may yet be evaluated under P5-D3E.

The next action is the local contract re-break only.

## Verdict

**STATIC REVIEW PASS — LOCAL CONTRACT RE-BREAK REQUIRED.**

Exact P5-D3E contract candidate to execute:

    3d76f3402c7eaba6e911d5f6e3038e9720be2284

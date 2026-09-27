# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX CONTRACT V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3E qualifies the real exact-head execution path of the already-qualified P5-D3D finite evaluator.

The target chain is:

    governed fetch of integration/system-v1
        ↓
    freeze exact candidate HEAD + TREE
        ↓
    sacrificial local Git clone
        ↓
    detached exact candidate checkout
        ↓
    sandbox P5-D2 activation
        ↓
    qualified P5-D3D finite evaluator
        ↓
    real DynamicInventory
        ↓
    real P5-D3B semantic bridge
        ↓
    real current-head Build A / Build B
        ↓
    real CHP-B01..B12
        ↓
    real P5-D3C2 sealed candidate package
        ↓
    QUALIFIED
        ↓
    P5-D2 EVALUATION_PASSED

P5-D3E remains non-promoting.

## 2. Qualified predecessor

P5-D3D qualification commit:

    7c244f8ab77d3497a16447b9257c8b204f3e048f

Qualification report blob:

    49890581b7c377b26cc4f2379e37b69fc4250c4b

Qualified P5-D3D functional candidate:

    6efa84c657bbea4edaa56d643d2b9dc0150bcdb1

Qualified finite evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

P5-D3E does not modify that evaluator.

It qualifies the real sandbox path around it.

## 3. Candidate resolution

The candidate is not hardcoded permanently into the P5-D3E contract.

At the beginning of one qualification run:

    integration/system-v1

is fetched once with the exact refspec:

    +refs/heads/integration/system-v1:
    refs/remotes/origin/integration/system-v1

The resulting remote-tracking commit becomes:

    candidate_head

Its exact tree becomes:

    candidate_tree

These two identities are frozen for the rest of the run.

If the remote branch moves afterward, that does not change the candidate being evaluated.

No second network fetch occurs during evaluation.

## 4. Design-time observed HEAD

At contract design time, GitHub reported:

    HEAD
    731380d8f1dd851c52de732c1edaf70f28ecc3c5

    TREE
    1c227d3da4959820797d1d29baab23d9fac4c430

This is contextual evidence only.

It is not the permanent P5-D3E candidate identity.

The local governed run must resolve its own exact HEAD/TREE immediately before qualification.

## 5. Why the candidate repository is locally cloned

P5-D3D requires an already prepared isolated repository.

P5-D3E therefore creates one sacrificial candidate repository under the OS temporary directory.

The process is:

    local git clone
      --no-hardlinks
      --no-checkout

from the control repository.

Then the exact candidate object/ref is transferred from the control repository by a local Git fetch.

This transfer is filesystem-local.

It is not a network fetch.

After transfer:

    origin

inside the sacrificial clone is rewritten to the canonical GitHub origin so that:

    FrozenGitSource.verify_repository()

continues to verify the same repository identity as production.

Finally:

    git checkout --detach <candidate_head>

materializes exactly the frozen candidate.

## 6. Independence safeguards

The sacrificial clone must not use:

    hard-linked object storage
    Git alternates
    shared object-store dependency

Required:

    --no-hardlinks

and:

    .git/objects/info/alternates absent

The candidate repository must remain:

    detached
    exact HEAD
    exact TREE
    worktree clean

before and after evaluation.

## 7. Control repository safeguards

The control repository must be:

    correct origin
    worktree clean before
    worktree clean after

The initial governed fetch may update remote-tracking Git metadata.

It may not modify source files.

P5-D3E does not create commits, pushes, or production refs.

## 8. Evaluation workspace

The evaluation workspace is a fresh sibling of the candidate repository under the same OS-temp sandbox parent.

It must not be:

    candidate repository ancestor
    candidate repository descendant
    canonical control repository descendant
    real Vault descendant

Before P5-D3D starts, these paths must not exist:

    build-a/
    build-b/
    candidate-package/

The qualified finite evaluator creates them itself.

## 9. Sandbox activation

P5-D3E does not pretend to be a live observer loop.

It creates a controlled P5-D2 activation with qualified primitives:

    make_initial_state()

then:

    REMOTE_HEAD_OBSERVED
    transition_class = INITIAL
    sequence = 1
    observed_head = candidate_head

then:

    EVALUATION_STARTED
    sequence = 2
    candidate_head = candidate_head

Required resulting state:

    observer_phase = EVALUATING

Required decision:

    START_EXACT_HEAD_EVALUATION

This activation is sandbox control evidence only.

It is not production observer state.

## 10. Real evaluator execution

P5-D3E calls exactly:

    evaluate_candidate_finitely()

from the qualified P5-D3D implementation.

The evaluator receives:

    exact activation
    exact candidate tree
    sacrificial candidate repository
    fresh evaluation workspace
    forbidden roots

No network fetch occurs inside the evaluator.

## 11. Qualification PASS semantics

P5-D3E PASS requires the real exact candidate outcome:

    QUALIFIED

It also requires:

    failure_code = null
    P5-D2 result event emitted
    package = PASS_SEALED_UNPROMOTED
    Build A tree digest = Build B tree digest
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    all major scientific digests present
    live projection head unchanged
    no CURRENT pointer
    no promotion authority
    no real Vault mutation

A successful evaluator call alone is not enough.

The real candidate itself must pass.

## 12. REJECTED semantics

If the real exact candidate is:

    REJECTED

P5-D3E records:

    FAIL_REAL_CANDIDATE_REJECTED

This is not BLOCKED.

The P5-D2 failure event must exist and a stable failure code must be present.

This outcome is meaningful candidate evidence, but it does not qualify the full real path through a sealed package.

## 13. BLOCKED semantics

If the evaluator returns:

    BLOCKED

P5-D3E records:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

No P5-D2 result event may be emitted.

BLOCKED remains retryable after infrastructure/evidence repair.

It is not converted into candidate rejection.

## 14. Post-evaluation package verification

On QUALIFIED, P5-D3E performs another read-only verification of:

    candidate-package/

using the qualified P5-D3C2 verifier.

Required:

    PASS_SEALED_UNPROMOTED

The candidate-generation digest from this second verification must equal the digest reported by the finite evaluator.

This provides a post-evaluation integrity check independent of the evaluator's earlier package verification step.

## 15. Real build evidence

Build A and Build B manifests must both bind:

    candidate HEAD
    candidate TREE
    DynamicInventory digest
    semantic bridge digest
    semantic-record digest

Both must report:

    metadata_only_body_read_count = 0

Both must satisfy:

    artifact_record_count = source_record_count

Build A and Build B projection-tree digests must match.

## 16. Forbidden package surfaces

The final sealed package may contain no:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views
    .obsidian
    .git

P5-D3E does not create a live projection namespace.

## 17. Cleanup

The candidate repository and evaluation workspace are sacrificial.

After evidence has been computed:

    candidate repository retained = false
    evaluation workspace retained = false

No absolute sandbox path is emitted in the qualification report.

## 18. Report

Success schema:

    ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_REPORT_V0_1

Success status:

    PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

The report binds:

    exact real candidate HEAD/TREE
    real evaluation outcome
    inventory/bridge/semantic identities
    Build A/B identities
    breaker identities
    determinism evidence
    package identity
    P5-D2 result evidence
    mutation/authority invariants

It records separately:

    candidate_resolution_network_fetch_performed = true
    evaluation_network_fetch_performed = false

This distinction is intentional.

## 19. Non-authorizations

P5-D3E still does not authorize:

    production promotion
    CURRENT mutation
    real Vault writes
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

It qualifies only the real exact-head sandbox evaluation path.

## 20. Contract-first boundary

Before a P5-D3E harness may be implemented or executed, this contract and its breakers must pass the governed local contract re-break.

After contract qualification, implementation may add:

    local clone sandbox preparation
    exact-head verification
    controlled activation
    real finite-evaluation wrapper
    post-package verifier
    qualification report

No production publication mechanism becomes authorized.

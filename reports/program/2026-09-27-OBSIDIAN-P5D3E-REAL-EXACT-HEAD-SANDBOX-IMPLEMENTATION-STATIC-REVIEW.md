# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX IMPLEMENTATION STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static review.

It is not independent execution evidence.
It does not qualify P5-D3E implementation.
It does not authorize the real integration/system-v1 run until the local implementation re-break passes.

## Functional candidate reviewed

    d403482b222b8bcfa4b0befa7684eda4b9d662fc

Branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-implementation-v0.1

Evidence-only preflight commit:

    581944d477b879d2112e2e25cdca85d2d079be6e

## Exact functional artifacts

Harness:

    tools/obsidian_projection/p5d3e_verify.py
    blob: 2380cddc3e15caf1b3f4d1b7942f064c179389ee

Harness tests:

    tests/obsidian_projection/test_p5d3e_verify.py
    blob: a1ae77ae7bfe768d1152885a2cfa154695c47bf0

Adversarial tests:

    tests/obsidian_projection/test_p5d3e_adversarial.py
    blob: 6af423b77b4ad78a833f7f4e3dedc53f5f23cead

Implementation documentation:

    docs/OBSIDIAN-P5D3E-REAL-EXACT-HEAD-SANDBOX-IMPLEMENTATION-V0.1.md
    blob: b21440ea7321da10cbafdb28170972570f530461

## Delta review

Relative to qualified P5-D3E contract checkpoint:

    4 files added
    0 qualified predecessor files modified

Static review: PASS.

## Contract binding

The harness pins:

    P5-D3E contract blob
    ae4b1691fae16fcd1616e265a089670b9654db4a

and verifies the runtime contract file by Git blob identity before use.

It also checks that the contract still binds the qualified P5-D3D evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

Static review: PASS.

## Real-context authority

The implementation separates:

    resolve_real_candidate()
    run_pre_resolved_sandbox()
    run_real_exact_head_qualification()

The public pre-resolved function hardcodes:

    real_context = false

The real wrapper is the only implementation path that calls the private sandbox core with:

    real_context = true

Therefore a synthetic/pre-resolved caller cannot supply booleans to self-assert real qualification.

Static review: PASS.

## Governed network boundary

resolve_real_candidate() performs the one authorized network command:

    git fetch --no-tags origin
    +refs/heads/integration/system-v1:
    refs/remotes/origin/integration/system-v1

It then freezes:

    candidate_head
    candidate_tree

The sandbox phase contains no requests/urllib/socket client and does not perform an origin fetch.

The later candidate-object transfer is local Git transport from the control repository path.

Static review: PASS.

## Control repository boundary

Before network resolution and before sandbox evaluation the control repository must be:

    existing
    canonical origin
    clean worktree

After the governed fetch the worktree is checked clean again.

After evaluation the worktree is checked clean again.

Remote-tracking metadata movement is not treated as a source-file mutation.

Static review: PASS.

## OS-temp protection

The system temp root is resolved before sandbox creation.

If OS temp is itself inside:

    control repository
    real Vault
    additional forbidden root

execution fails before TemporaryDirectory creation.

Static review: PASS.

## Sacrificial clone independence

Candidate preparation requires:

    git clone --no-hardlinks --no-checkout

Then:

    local exact candidate-ref transfer
    canonical-origin restoration
    git checkout --detach exact HEAD

The harness rejects:

    HEAD mismatch
    TREE mismatch
    attached branch
    dirty candidate worktree
    .git/objects/info/alternates
    object-store files whose st_nlink != 1

Static review: PASS.

## P5-D2 activation

The harness constructs activation only through:

    make_initial_state()
    one_shot_tick(REMOTE_HEAD_OBSERVED / INITIAL)
    one_shot_tick(EVALUATION_STARTED)

It then verifies:

    START_EXACT_HEAD_EVALUATION
    EVALUATING
    automatic_promotion_authorized = false
    production_write_authorized = false

Static review: PASS.

## Qualified P5-D3D reuse

The harness imports and calls:

    evaluate_candidate_finitely()

No alternate builder, bridge, breaker runner or evaluator implementation is introduced.

Static review: PASS.

## Outcome separation

QUALIFIED requires:

    failure_code null
    P5-D2 result event true
    PASS_SEALED_UNPROMOTED
    A/B projection digest equality
    all required scientific SHA-256 values

REJECTED requires:

    failure_code non-null
    P5-D2 result event true

BLOCKED requires:

    failure_code non-null
    P5-D2 result event false

Unknown outcomes are governance failure.

Static review: PASS.

## Build evidence

On QUALIFIED the harness independently loads both real build manifests.

It verifies:

    exact repository/branch/head/tree
    inventory digest
    semantic bridge digest
    semantic record digest
    projection contract identity
    build_status PASS
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    no pilot identity
    Build A/B count equality

Static review: PASS.

## Post-package verifier

On QUALIFIED the harness independently calls:

    verify_candidate_generation()

after the evaluator has already verified the package.

The second verifier must return:

    PASS_SEALED_UNPROMOTED

and agree with evaluator evidence on:

    candidate HEAD
    candidate TREE
    candidate-generation digest
    semantic bridge digest
    semantic-record digest
    breaker manifest digest
    breaker result digest

Static review: PASS.

## Protected Vault evidence

The real Vault is fingerprinted before and after evaluation.

The fingerprint includes deterministic path/type/content evidence.

Reparse/symlink entries are not followed.

Any fingerprint mismatch is a governance failure.

No absolute Vault path is inserted into the qualification report.

Static review: PASS.

## Package publication boundary

The package is scanned for forbidden surfaces:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views
    .obsidian
    .git

These names are used only as rejection predicates.

No CURRENT writer or promotion primitive exists in the harness.

Static review: PASS.

## Background/network surface

Static inspection of the runtime harness finds no:

    while True
    time.sleep
    requests
    urllib
    socket client
    promotion_experiment
    PROMOTION_CONFIRMED
    _write_pointer

Static review: PASS.

## Synthetic implementation test path

The implementation tests construct a local Git control repository and a protected sentinel Vault.

They exercise:

    remote-tracking candidate binding
    local no-hardlinks clone
    detached exact checkout
    qualified P5-D3D evaluator
    Build A/B
    CHP breakers
    P5-D3C2 package
    post-package verifier
    cleanup

without the real network-resolution path.

Synthetic success is explicitly:

    PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX

and cannot become:

    PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

Static review: PASS.

## Static test inventory

Harness tests:

    5

Adversarial tests:

    15

Total implementation-specific tests:

    20

These are static repository facts only.

## Remaining required evidence

P5-D3E implementation remains unqualified until exact candidate:

    d403482b222b8bcfa4b0befa7684eda4b9d662fc

passes:

1. exact blob guards;
2. py_compile;
3. targeted P5-D3E contract + implementation tests;
4. predecessor P5-D3D implementation tests;
5. full tests/obsidian_projection;
6. local pre-resolved synthetic sandbox exercise;
7. clean source checkout after tests;
8. no real branch fetch/evaluation during this implementation gate.

## Verdict

**STATIC REVIEW PASS — LOCAL IMPLEMENTATION RE-BREAK REQUIRED.**

The real integration/system-v1 candidate run remains unauthorized until that re-break passes.

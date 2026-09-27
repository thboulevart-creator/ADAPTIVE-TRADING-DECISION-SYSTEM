# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX IMPLEMENTATION V0.1

Date: 2026-09-27

## 1. Qualified authority

P5-D3E contract qualification commit:

    f413171075fb002b7c6080a10247cad65954f2be

P5-D3E contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Qualified predecessor evaluator:

    P5-D3D finite candidate evaluator

Blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

The P5-D3E implementation does not modify the P5-D3D evaluator.

## 2. Runtime module

Implementation:

    tools/obsidian_projection/p5d3e_verify.py

The implementation is divided into two explicit phases.

### Phase A — real candidate resolution

    resolve_real_candidate()

This phase:

    verifies the control repository is clean;
    verifies canonical GitHub origin;
    performs exactly one governed network fetch;
    resolves refs/remotes/origin/integration/system-v1;
    resolves candidate HEAD^{tree};
    freezes both identities.

The exact refspec is:

    +refs/heads/integration/system-v1:
    refs/remotes/origin/integration/system-v1

No candidate is evaluated in this function.

### Phase B — pre-resolved sandbox evaluation

    run_pre_resolved_sandbox()

This phase receives already frozen:

    candidate_head
    candidate_tree

It performs no network fetch.

It creates a sacrificial local clone and runs the qualified evaluator.

## 3. Sacrificial clone

The candidate repository is created below OS temp with:

    git clone
    --no-hardlinks
    --no-checkout

from the local control repository.

The candidate remote-tracking ref is then transferred locally from:

    refs/remotes/origin/integration/system-v1

to:

    refs/remotes/p5d3e-source/integration/system-v1

No GitHub fetch is used for this transfer.

The sandbox origin is then rewritten to:

    https://github.com/thboulevart-creator/
    ADAPTIVE-TRADING-DECISION-SYSTEM.git

The candidate is checked out with:

    git checkout --detach <candidate_head>

Required before evaluation:

    exact HEAD
    exact TREE
    detached checkout
    clean worktree
    canonical origin

## 4. Object-store independence

The implementation rejects:

    .git/objects/info/alternates

It also walks the sacrificial Git object store and requires:

    st_nlink == 1

for every object-store file.

Therefore a clone using shared/hard-linked object storage is not accepted.

## 5. Real Vault protection

The real Vault is not merely passed as a forbidden root.

Before evaluation the harness computes a deterministic read-only content fingerprint of the protected Vault.

After evaluation the same fingerprint is recomputed.

Any difference causes a P5-D3E governance failure.

Reparse/symlink entries are not followed.

No Vault path is emitted in the qualification report.

## 6. Sandbox P5-D2 activation

The harness creates a controlled activation through the qualified P5-D2 primitives:

    make_initial_state()
        ↓
    REMOTE_HEAD_OBSERVED / INITIAL
        ↓
    EVALUATION_STARTED

Required activation result:

    action = START_EXACT_HEAD_EVALUATION
    observer_phase = EVALUATING
    automatic_promotion_authorized = false
    production_write_authorized = false

This remains sandbox state only.

## 7. Qualified P5-D3D invocation

The harness calls:

    evaluate_candidate_finitely()

with:

    exact frozen candidate tree
    sacrificial candidate repository
    fresh evaluation workspace
    control repository as forbidden root
    real Vault as forbidden root

The evaluator remains responsible for:

    P5-B2 DynamicInventory
    P5-D3B semantic bridge
    Build A
    Build B
    determinism
    CHP-B01..B12
    P5-D3C2 package staging
    P5-D2 result event

## 8. Real outcome validation

The harness independently validates the P5-D3D report.

QUALIFIED requires:

    exact candidate HEAD/TREE
    repository/branch identity
    failure_code = null
    P5-D2 result event emitted
    PASS_SEALED_UNPROMOTED
    Build A projection digest = Build B projection digest
    all scientific SHA-256 identities present
    live projection unchanged
    no real Vault mutation claim
    no CURRENT creation
    no promotion authority

REJECTED requires:

    non-null stable failure code
    P5-D2 result event emitted

BLOCKED requires:

    non-null failure code
    no P5-D2 result event

## 9. Build-manifest verification

For a QUALIFIED candidate the harness independently reads:

    build-a/generated/manifests/build-manifest.json
    build-b/generated/manifests/build-manifest.json

Both must bind:

    source repository
    source branch
    candidate HEAD
    candidate TREE
    DynamicInventory digest
    semantic bridge digest
    semantic-record digest
    projection contract

Both must report:

    build_status = PASS
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count

Their seven count fields must match exactly.

Pilot identity fields remain forbidden.

## 10. Post-package verification

After P5-D3D reports QUALIFIED, the harness independently calls:

    verify_candidate_generation()

against:

    candidate-package/

Required:

    PASS_SEALED_UNPROMOTED

The second verifier must agree with the evaluator on:

    candidate HEAD
    candidate TREE
    candidate-generation digest
    semantic bridge digest
    semantic-record digest
    breaker manifest digest
    breaker result digest

A mismatch is a P5-D3E governance failure.

## 11. Forbidden package surfaces

The reverified package is scanned for:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views
    .obsidian
    .git

Any such path fails P5-D3E.

These strings are detection surfaces only.

No pointer-writing primitive exists in the harness.

## 12. Post-evaluation repository checks

Before sandbox cleanup the harness rechecks:

    candidate HEAD unchanged
    candidate TREE unchanged
    candidate worktree clean
    control worktree clean
    Vault fingerprint unchanged

The candidate repository and evaluation workspace are then deleted by the OS-temp sandbox lifecycle.

The returned report records:

    candidate_repository_retained = false
    evaluation_workspace_retained = false

## 13. Report semantics

Real PASS:

    PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

Real candidate rejection:

    FAIL_REAL_CANDIDATE_REJECTED

Infrastructure/evidence block:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

A local pre-resolved synthetic fixture can exercise the same sandbox path before the real run, but it receives:

    PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX

and can never be reported as real P5-D3E qualification.

## 14. Network accounting

The real run reports separately:

    candidate_resolution_network_fetch_performed = true
    evaluation_network_fetch_performed = false

The first corresponds only to exact branch resolution.

The second confirms that the P5-D3D evaluation phase itself is network-free.

## 15. Implementation qualification before real run

Before the real branch is evaluated, this harness must pass:

    py_compile
    P5-D3E implementation unit tests
    P5-D3E adversarial tests
    qualified predecessor contract chain
    full tests/obsidian_projection
    local pre-resolved synthetic sandbox fixture
    source-clean verification

Only after that implementation gate passes may the CLI execute:

    run_real_exact_head_qualification()

against the then-current exact integration/system-v1 HEAD.

## 16. Still forbidden

P5-D3E does not authorize:

    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

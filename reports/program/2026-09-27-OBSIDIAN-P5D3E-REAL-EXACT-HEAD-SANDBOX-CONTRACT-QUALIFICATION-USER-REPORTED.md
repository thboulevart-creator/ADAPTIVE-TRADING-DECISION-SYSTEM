# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX CONTRACT QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified contract candidate

Exact P5-D3E contract candidate:

    3d76f3402c7eaba6e911d5f6e3038e9720be2284

Branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-v0.1

Evidence-only commits after this candidate do not replace the tested contract candidate.

## Exact qualified contract artifacts

Real exact-head sandbox contract:

    tools/obsidian_projection/real_exact_head_sandbox_contract_v0_1.json
    blob: ae4b1691fae16fcd1616e265a089670b9654db4a

Contract breakers:

    tests/obsidian_projection/test_real_exact_head_sandbox_contract_v0_1.py
    blob: f03980d4b650792b49bd13ea8ca5f168e87ef73b

Documentation:

    docs/OBSIDIAN-P5D3E-REAL-EXACT-HEAD-SANDBOX-CONTRACT-V0.1.md
    blob: 876adf255e3b5940c3b2638c63e52b5a324a18f8

## Qualified predecessor

P5-D3D qualification commit:

    7c244f8ab77d3497a16447b9257c8b204f3e048f

P5-D3D qualification report blob:

    49890581b7c377b26cc4f2379e37b69fc4250c4b

Qualified finite evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Reported local result

The user reported:

    Ran 1037 tests in 17.181s
    OK
    P5D3E_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3E_CONTRACT_REBREAK_COMPLETED=PASS

This directly supports successful completion of the full tests/obsidian_projection regression and a clean control checkout after execution.

Because the governed wrapper stops on py_compile or targeted-contract failure before the full-suite completion marker, reaching the reported final PASS is consistent with the earlier wrapper gates having passed. Those individual earlier lines were not included in the supplied excerpt and are therefore not separately claimed as direct user-reported evidence.

## Qualified P5-D3E contract authority

This qualification authorizes implementation of the P5-D3E real exact-head sandbox harness under the preregistered contract.

The qualified contract fixes the following semantics:

- one governed initial network fetch may resolve integration/system-v1;
- candidate HEAD and TREE are frozen for the entire run;
- no second network fetch occurs during evaluator execution;
- the sacrificial repository lives under OS temp;
- local clone uses --no-hardlinks and --no-checkout;
- Git alternates/shared object-store dependence is forbidden;
- canonical GitHub origin is restored before P5-D3D evaluation;
- the candidate checkout is detached at the exact frozen HEAD;
- the candidate repository and evaluation workspace remain outside the control repository and real Vault;
- sandbox activation is produced with qualified P5-D2 primitives;
- the already-qualified P5-D3D finite evaluator remains the evaluator authority;
- P5-D3E PASS requires a real evaluator outcome of QUALIFIED;
- REJECTED and BLOCKED remain distinct non-PASS outcomes;
- the final candidate package must verify PASS_SEALED_UNPROMOTED;
- a second read-only package verification is required after evaluation;
- Build A/B identities and zero METADATA_ONLY body reads must be confirmed;
- candidate and control repositories must remain clean after evaluation;
- candidate/workspace sandboxes are sacrificial and removed after evidence capture.

## Contract breaker registry

Required P5-D3E breakers:

    66

Unique:

    66

Persisted P5-D3E contract-test methods:

    15

The reported full regression included the persisted P5-D3E contract tests as part of the repository-wide Obsidian suite.

## PASS semantics now fixed

A future P5-D3E real run qualifies only if:

    candidate outcome = QUALIFIED
    failure_code = null
    package status = PASS_SEALED_UNPROMOTED
    P5-D2 result event emitted
    Build A projection tree = Build B projection tree
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    post-package read-only verification passes
    post-package candidate-generation digest equals evaluator report
    live projection head unchanged
    no CURRENT pointer
    no promotion authority
    no real Vault mutation

## REJECTED semantics

If the exact real candidate is rejected, P5-D3E must report:

    FAIL_REAL_CANDIDATE_REJECTED

This remains valid candidate evidence but does not qualify the full real exact-head path.

## BLOCKED semantics

If infrastructure/tooling/evidence prevents classification, P5-D3E must report:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

BLOCKED must not be relabelled REJECTED or QUALIFIED.

## Implementation scope now authorized

Under the same P5-D3E frontier, implementation may now add:

    governed exact-head resolver input verification
    local no-hardlinks sacrificial clone preparation
    local exact candidate object/ref transfer
    canonical-origin restoration
    detached exact checkout verification
    controlled sandbox P5-D2 activation
    qualified P5-D3D evaluator invocation
    post-package P5-D3C2 verification
    post-evaluation repository/build/package checks
    deterministic P5-D3E qualification report
    sandbox cleanup

## Explicit non-authorizations preserved

This contract qualification does NOT authorize:

- production promotion;
- CURRENT pointer mutation;
- real Vault writes;
- background observer execution;
- polling;
- Windows startup/task/service persistence;
- Graph/Search CURRENT semantics.

It also does not yet establish that any real integration/system-v1 HEAD has passed P5-D3E.

## Verdict

**PASS — P5-D3E REAL EXACT-HEAD SANDBOX CONTRACT QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed action

Remain inside P5-D3E and build the implementation candidate:

    REAL EXACT-HEAD SANDBOX HARNESS

The implementation must preserve the qualified P5-D3D evaluator unchanged and must not execute a real candidate until its own static/test boundary is ready.

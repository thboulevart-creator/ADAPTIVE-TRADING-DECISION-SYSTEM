# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX CONTRACT PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3E is currently contract-only.

No real exact-head sandbox harness, local clone preparer, or real candidate evaluation execution is authorized until this contract gate qualifies.

## Qualified predecessor

P5-D3D qualification commit:

    7c244f8ab77d3497a16447b9257c8b204f3e048f

P5-D3D qualification report blob:

    49890581b7c377b26cc4f2379e37b69fc4250c4b

Qualified P5-D3D functional candidate:

    6efa84c657bbea4edaa56d643d2b9dc0150bcdb1

Qualified finite evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Candidate branch

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-v0.1

## Exact functional candidate

    3d76f3402c7eaba6e911d5f6e3038e9720be2284

Later evidence-only commits must not replace this candidate.

## Exact contract artifacts

Contract:

    tools/obsidian_projection/real_exact_head_sandbox_contract_v0_1.json
    blob: ae4b1691fae16fcd1616e265a089670b9654db4a

Contract breakers:

    tests/obsidian_projection/test_real_exact_head_sandbox_contract_v0_1.py
    blob: f03980d4b650792b49bd13ea8ca5f168e87ef73b

Documentation:

    docs/OBSIDIAN-P5D3E-REAL-EXACT-HEAD-SANDBOX-CONTRACT-V0.1.md

## Functional delta

Relative to qualified P5-D3D:

    exactly 3 files added
    no qualified predecessor file modified

## Static registry

Required breakers:

    66 unique

Persisted contract-test methods:

    15

These are repository facts only, not executed evidence.

## Design-time observed branch identity

At contract design time, GitHub reported:

    integration/system-v1 HEAD:
    731380d8f1dd851c52de732c1edaf70f28ecc3c5

    tree:
    1c227d3da4959820797d1d29baab23d9fac4c430

This identity is contextual only.

The governed P5-D3E run must resolve the real branch again at execution time and freeze that exact HEAD/TREE for the entire run.

## Candidate-resolution model

One initial network fetch is allowed only to resolve:

    refs/remotes/origin/integration/system-v1

Exact refspec:

    +refs/heads/integration/system-v1:
    refs/remotes/origin/integration/system-v1

After capture:

    candidate_head and candidate_tree are immutable run inputs

No second network fetch is authorized during the evaluation itself.

## Sacrificial-repository model

The future harness must prepare a candidate repository under OS temp using:

    git clone --no-hardlinks --no-checkout

from the local control repository.

The exact candidate ref/object is then transferred from the control repository by local Git transport.

After local transfer:

    origin is restored to the canonical GitHub origin

and:

    checkout --detach exact candidate HEAD

is required.

Forbidden:

    Git alternates
    shared object store dependency
    hard-linked object store
    candidate repo retained after run

## Evaluation-workspace model

A fresh OS-temp workspace must be a sibling of the sacrificial candidate repository.

Before evaluation:

    build-a absent
    build-b absent
    candidate-package absent

The workspace must not intersect:

    canonical control repository
    real Vault
    candidate repository

## Activation model

P5-D3E uses qualified P5-D2 primitives to construct a controlled sandbox activation:

    REMOTE_HEAD_OBSERVED / INITIAL
    EVALUATION_STARTED

The activation is not claimed to be live observer state.

## PASS requirement

P5-D3E qualification requires the real candidate itself to reach:

    outcome = QUALIFIED

with:

    candidate_generation_verification_status =
    PASS_SEALED_UNPROMOTED

and:

    P5-D2 result event emitted
    failure_code null
    Build A == Build B
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    live projection unchanged
    no CURRENT
    no promotion
    no real Vault mutation

## REJECTED / BLOCKED distinction

Real candidate REJECTED:

    FAIL_REAL_CANDIDATE_REJECTED

This is candidate evidence, not infrastructure BLOCKED.

Evaluator BLOCKED:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

This is not candidate rejection and does not qualify P5-D3E.

## Post-package verification

On QUALIFIED, the future harness must independently call the qualified P5-D3C2 read-only verifier on:

    candidate-package/

The second verification must return:

    PASS_SEALED_UNPROMOTED

and its candidate-generation digest must exactly equal the evaluator report.

## Publication boundary

Still forbidden:

    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

## Required local contract re-break

Before P5-D3E runtime implementation is authorized:

1. recover exact contract candidate 3d76f3402c7eaba6e911d5f6e3038e9720be2284;
2. verify exact P5-D3E contract blob;
3. py_compile the P5-D3E contract breaker;
4. run targeted predecessor + P5-D3E contract tests;
5. run full tests/obsidian_projection;
6. require clean control checkout.

No real candidate is evaluated during this contract gate.

## Next action on PASS

Remain inside P5-D3E and implement the qualification harness:

    governed exact-head input verification
    local no-hardlinks clone preparation
    canonical-origin restoration
    detached exact checkout
    controlled P5-D2 activation
    qualified P5-D3D evaluation
    post-package verification
    cleanup
    deterministic qualification report

Only then may the real exact-head sandbox run occur.

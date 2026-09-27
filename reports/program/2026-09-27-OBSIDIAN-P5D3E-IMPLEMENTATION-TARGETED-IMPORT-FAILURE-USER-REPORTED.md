# OBSIDIAN P5-D3E — IMPLEMENTATION TARGETED IMPORT FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Tested functional candidate

    d403482b222b8bcfa4b0befa7684eda4b9d662fc

Branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-implementation-v0.1

## Reported execution

The targeted P5-D3E implementation test phase reported:

    Ran 134 tests in 2.672s
    FAILED (errors=2)

Wrapper result:

    BLOCKED: targeted P5-D3E implementation tests failed.

The two import errors were:

    test_p5d3e_verify
    test_p5d3e_adversarial

Both failed while importing:

    tools.obsidian_projection.p5d3e_verify

Exact cause:

    ImportError:
    cannot import name 'git_blob_oid'
    from 'tools.obsidian_projection.git_source'

Therefore:

    P5D3E_TARGETED_IMPLEMENTATION_TESTS=FAIL
    P5D3E_FULL_REBREAK=NOT_EXECUTED
    P5D3E_PRE_RESOLVED_SYNTHETIC_SANDBOX=NOT_EXECUTED
    P5D3E_IMPLEMENTATION_QUALIFICATION=NOT_GRANTED

## Static adjudication

At the tested candidate:

    tools/obsidian_projection/git_source.py

does not define:

    git_blob_oid

The repository already contains the canonical Git blob object-id algorithm in:

    tools/obsidian_projection/dynamic_inventory.py

under the private helper:

    _git_blob_oid(raw)

Algorithm:

    SHA1(
        ASCII("blob " + decimal_byte_length + NUL)
        + raw_bytes
    )

The P5-D3E harness incorrectly imported a non-existent public symbol from git_source.py.

This is an implementation import defect in the harness.

The qualified P5-D3D evaluator is not implicated.

The P5-D3E contract is not implicated.

## Authorized correction scope

Correction is limited to:

    tools/obsidian_projection/p5d3e_verify.py

and a minimal unit breaker in:

    tests/obsidian_projection/test_p5d3e_verify.py

The harness must:

1. remove the invalid git_blob_oid import from git_source.py;
2. define a local deterministic Git-blob OID helper using the canonical Git blob formula;
3. use that helper only for exact P5-D3E contract blob verification;
4. preserve all existing sandbox, authority and publication boundaries.

No P5-D3D evaluator runtime may be modified.

No real integration/system-v1 candidate may be evaluated during correction qualification.

## Verdict

**FAIL — TARGETED IMPLEMENTATION IMPORT ERROR**

P5-D3E implementation remains unqualified.

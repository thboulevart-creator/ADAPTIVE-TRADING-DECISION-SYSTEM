# OBSIDIAN P5-D3C2 — TARGETED RE-BREAK FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Tested functional candidate

    f5304fa9697bd33ea98214598321473087b65e24

Branch:

    feat/obsidian-projection-p5d3c2-staging-implementation-v0.1

## Reported execution

The governed wrapper reached:

    P5D3C2_RUNTIME_HEAD=f5304fa9697bd33ea98214598321473087b65e24
    P5D3C_STAGING_CONTRACT_BLOB=PASS
    P5D3C2_RUNTIME_CONTRACT_BLOB=PASS
    P5D3C2_PY_COMPILE=PASS

The targeted test batch then reported:

    Ran 95 tests in 3.618s
    FAILED (errors=1)

The wrapper stopped before:

- full tests/obsidian_projection regression;
- sacrificial sandbox execution;
- mutation-breaker qualification.

Therefore:

    P5D3C2_FULL_REBREAK=NOT_EXECUTED
    P5D3C2_SANDBOX_QUALIFICATION=NOT_EXECUTED
    P5D3C2_QUALIFICATION=NOT_GRANTED

## Exact failing test

    tests.obsidian_projection.test_candidate_generation_staging_implementation_contract_v0_1
    P5D3C2StagingImplementationContractTests.test_reparse_probe_has_explicit_capability_policy

Reported exception:

    KeyError:
    capability_unavailable_does_not_waive_static_and_synthetic_breakers

## Static adjudication

The exact P5-D3C2 implementation contract contains:

    capability_unavailable_does_not_waive_static_and_unit_reparse_breakers

The exact contract test incorrectly requested:

    capability_unavailable_does_not_waive_static_and_synthetic_breakers

The P5-D3C2 documentation also describes the non-waiver as applying to:

    static/unit reparse breakers

Therefore the runtime contract is not implicated by this failure.

The packager/verifier implementation and sandbox runner are not implicated by this failure.

## Scope of correction

Authorized correction is limited to:

    tests/obsidian_projection/test_candidate_generation_staging_implementation_contract_v0_1.py

The test must assert the exact existing contract key:

    capability_unavailable_does_not_waive_static_and_unit_reparse_breakers

No contract field, implementation behavior, sandbox semantics, authority boundary or qualification condition may be weakened.

## Verdict

**FAIL — TARGETED RE-BREAK NOT QUALIFIED**

Cause:

    CONTRACT TEST KEY TYPO

P5-D3C2 remains unqualified.

A corrected functional candidate must be re-broken from the beginning.

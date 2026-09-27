# OBSIDIAN P5-D3C2 — CONTRACT TEST KEY CORRECTION STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static correction review.

Not independent execution evidence.
Does not qualify P5-D3C2.

## Failed tested candidate

    f5304fa9697bd33ea98214598321473087b65e24

Reported local targeted result:

    P5D3C2_PY_COMPILE=PASS
    Ran 95 tests in 3.618s
    FAILED (errors=1)

Exact failing test:

    P5D3C2StagingImplementationContractTests.test_reparse_probe_has_explicit_capability_policy

## Root cause

The exact implementation contract contains:

    capability_unavailable_does_not_waive_static_and_unit_reparse_breakers

The test incorrectly requested:

    capability_unavailable_does_not_waive_static_and_synthetic_breakers

This was a test-key typo.

The contract, packager/verifier implementation and sandbox runner were not implicated.

## Corrected functional candidate

    41d19df20dc5214e3b64098dd72519a23ea6e010

## Functional correction

Only:

    tests/obsidian_projection/test_candidate_generation_staging_implementation_contract_v0_1.py

was functionally modified.

Corrected test blob:

    93b1599a388d6ed3d6085e4b673b5b9c749da4ec

The test now asserts the exact existing contract key:

    capability_unavailable_does_not_waive_static_and_unit_reparse_breakers

## Unchanged runtime artifacts

P5-D3C2 runtime contract unchanged:

    12f04ad90567c6b0451713a4180f3b10df66de41

Packager/verifier unchanged:

    e2e5867536f4f9c7dec475c6696737249536ff39

Sandbox runner unchanged:

    82f5ad9aab8582c32a4e38069934ed4849b8f08e

No runtime semantic, filesystem boundary, verifier rule, sandbox breaker, authority flag or qualification criterion was weakened.

## Evidence-only commits between candidates

The corrected candidate also includes evidence-only reports for:

- P5-D3C2 preflight;
- original static review;
- user-reported targeted FAIL.

Those reports do not alter runtime behavior.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL GOVERNED RE-BREAK + SANDBOX QUALIFICATION REQUIRED**

P5-D3C2 remains unqualified.

Exact corrected candidate to execute:

    41d19df20dc5214e3b64098dd72519a23ea6e010

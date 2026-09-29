# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT CONTRACT RE-BREAK BLOCKED V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION.

## Verified GitHub state before persistence

Remote HEAD:

    87ece3d1c601e075ea1754b8d26308276bb9655a

Functional contract candidate:

    82e8e1aacc8fcb1129c12a5dc66ce2015c6ae845

Contract blob:

    5de65f5d13a93d1325d53e1b58536ed0860921f2

Tests blob:

    12873436d6354ffa454253cdf754023378d35076

Governed runner blob:

    2ddee8bbd0b949a2a9f187b8d10be11150c05f9b

## User-reported result

Targeted production-enablement contract tests:

    Ran 18 tests in 0.097s
    OK

Full historical Obsidian suite:

    Ran 1165 tests in 142.276s
    OK

Runner marker:

    P5D3G_PRODUCTION_ENABLEMENT_CONTRACT_FULL_REBREAK=PASS

Final cleanliness gate:

    BLOCKED: working tree non propre après production-enablement contract re-break:
    ?? tests/obsidian_projection/__pycache__/test_production_enablement_gate_contract_v0_1.cpython-314.pyc

## Adjudication

The contract tests and complete historical suite passed.

The contract is NOT yet qualified because the governed runner itself violated the clean-control-clone requirement by allowing py_compile to create an untracked bytecode artifact inside the repository.

## Correction boundary

Correct only runner bytecode placement.

Do not modify:

- production-enablement contract semantics;
- contract blob;
- contract-test expectations;
- real-Vault authority boundary.

The corrected runner must direct py_compile cache output outside the repository and must still require a clean control clone at the end.

# OBSIDIAN P5-D3B — MUTATION BREAKER CORRECTION STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static review.

Not independent execution evidence.
Does not qualify P5-D3B.

## Failed predecessor candidate

    1f7005eb4dd2f59d7416c0862a149ab092e7febc

User-reported targeted result:

    Ran 114 tests
    FAILED (failures=1)
    CONTROL_CLONE_CLEAN=PASS

Exact failing breaker:

    P5D3BAdversarialTests.test_input_is_not_mutated_by_assignment

False-positive literal:

    entry.content_mode =

The literal matched the prefix of valid comparisons such as:

    entry.content_mode == "FULL_TEXT"
    entry.content_mode == "METADATA_ONLY"

## Corrected functional candidate

    b45a692bc90953e1cfe06106da596023ed2fb248

## Scope of functional correction

Only:

    tests/obsidian_projection/test_p5d3b_adversarial.py

was functionally modified.

Corrected adversarial-test blob:

    c54d563ef77bc4de4451438c765f451a93ae6a22

The corrected breaker now parses the bridge module AST and detects actual mutation targets through:

    ast.Assign
    ast.AnnAssign
    ast.AugAssign
    setattr(...)

for protected DynamicInventory / DynamicInventoryEntry fields.

Comparison expressions are no longer treated as assignments.

## Unchanged functional artifacts

Contract unchanged:

    7015db1206cd40b703795d12519707a6455b4fc3

Bridge implementation unchanged:

    ff3c2dd232487594a5283a9ab7750780ac098f2d

Real-head verifier unchanged:

    9b283a2198fcc464b9ac75b07286b07713efd666

No bridge behavior, semantic rule, provenance rule, content-mode rule, runtime authority, Vault boundary, promotion boundary, or qualification condition was weakened.

## Evidence-only files added since failed candidate

The branch also contains evidence-only reports documenting:

- P5-D3B preflight;
- original static review;
- user-reported targeted failure.

These do not replace the corrected functional candidate identity.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL GOVERNED RE-BREAK REQUIRED**

Exact corrected candidate to execute:

    b45a692bc90953e1cfe06106da596023ed2fb248

P5-D3B remains unqualified until the corrected candidate passes:

1. targeted P5-D3A + P5-D3B tests;
2. full Obsidian suite;
3. real-head P5-B2 -> P5-D3B bridge harness;
4. final control-clone cleanliness.

# OBSIDIAN P5-D3E — ALTERNATES BREAKER FORMATTING CORRECTION STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static correction review.

Not independent execution evidence.
Does not qualify P5-D3E implementation.

## Previous candidate

    a0478167404a53aed94a3f3404addb4e7cc23e6a

User-reported targeted result:

    Ran 153 tests in 8.252s
    FAILED (failures=1)

The exact local failing-test traceback was not supplied.

## Static defect

The adversarial test required the exact one-line source substring:

    "objects" / "info" / "alternates"

The runtime harness expresses the same path across multiple Python lines:

    git_dir
    / "objects"
    / "info"
    / "alternates"

The runtime behavior explicitly rejects an existing:

    .git/objects/info/alternates

Therefore the adversarial assertion was formatting-dependent.

## Corrected functional candidate

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

## Functional correction

Only:

    tests/obsidian_projection/test_p5d3e_adversarial.py

was functionally modified.

Corrected adversarial-test blob:

    6b159ede31fb26ac366f9c69cd72256ee553753c

The breaker now requires the three semantic path components independently:

    "objects"
    "info"
    "alternates"

This preserves the intended governance assertion without depending on source formatting.

## Unchanged runtime and authorities

P5-D3E contract:

    ae4b1691fae16fcd1616e265a089670b9654db4a

P5-D3E runtime harness:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

P5-D3E harness tests:

    fe47910cf7f10a09021d958d7ae60693d0def4bf

Qualified P5-D3D evaluator:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

No runtime behavior changed.

No real integration/system-v1 candidate is authorized by this correction.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL GOVERNED IMPLEMENTATION RE-BREAK REQUIRED**

Exact corrected candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

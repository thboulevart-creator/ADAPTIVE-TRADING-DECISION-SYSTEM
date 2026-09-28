# OBSIDIAN P5-D3F — WORKTREE BLOB ASSERTION CORRECTION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static correction review.

Not independent execution evidence.
Does not qualify P5-D3F.

## Triggering local evidence

USER-REPORTED LOCAL EXECUTION:

    Ran 24 tests in 0.031s
    FAILED (failures=1)

Exact failing test:

    test_contract_blob_and_schema_are_exact

The governed runner had already reported:

    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS

The unit test then compared a Git blob OID recomputed from Path.read_bytes() against the canonical committed blob and failed on Windows working-tree materialization.

## Root cause

The test coupled canonical Git object identity to raw working-tree bytes.

That is not portable across checkout newline materialization.

A clean Windows checkout may expose working-tree bytes with different line endings while Git still represents the canonical committed object with the expected blob identity.

The repository-level runner correctly used Git to verify the expected contract blob.

Therefore the test was stricter in the wrong dimension.

## Narrow correction

Only:

    tests/obsidian_projection/test_promotion_handoff_contract_v0_1.py

was functionally corrected.

The corrected test now:

1. requires Git to report no logical working-tree diff for the contract path;
2. obtains the committed contract blob with:

       git rev-parse HEAD:tools/obsidian_projection/promotion_handoff_contract_v0_1.json

3. compares that committed object identity to the preregistered expected blob.

This preserves exact Git authority while remaining checkout-normalization safe.

## Runner pin update

The governed Python runner changed only its pinned expected contract-test blob.

Corrected contract-test blob:

    3dc1d7315874d4352eeaf05407f266961c878e70

Corrected runner blob:

    1c574e45a970b290ce78e78a7a0b9967e69e43bd

Runner-test blob remains:

    b309c3efb759ac3c9604b76fc7defa9cbe446482

## Unchanged contract authority

P5-D3F contract blob remains exactly:

    64744325251db350d26c0269090ce62d5fa5f2e8

No P5-D3F contract semantic changed.

No authority bit changed.

No handoff runtime was implemented.

No real Vault write was introduced.

## Corrected functional qualification candidate

    a12bc12d6279b1dfc58b507c282578310d7fd2b0

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL LOCAL CONTRACT RE-BREAK REQUIRED**

Next permitted action:

    rerun the governed Python P5-D3F contract re-break

against:

    a12bc12d6279b1dfc58b507c282578310d7fd2b0

A PASS is still required before any P5-D3F implementation is authorized.

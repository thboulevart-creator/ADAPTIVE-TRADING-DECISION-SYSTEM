# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V5

Date: 2026-09-28

## Exact functional candidate

    401cdf3e8eb8fea40fc61536227441de83c49246

## Exact functional blobs

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Governed Python runner:

    dcc85c9e426565a56ada1c30d029c3a565769752

Runner tests:

    e1d16c07ce3a85c4ef65964346b587dabd4dcf07

.gitattributes:

    e0154899b5640da025a082ef6b02f4bf179d3030

## V5 purpose

V5 preserves V4's repository-level LF policy but no longer relies on Git checkout conversion to repair an already-materialized Windows worktree.

Before historical full regression, the runner restores the exact committed bytes for the bounded byte-pinned compatibility paths directly from Git objects and verifies raw byte identity.

## Required PASS

    P5D3F_CANONICAL_BLOB_MATERIALIZATION=PASS
    P5D3F_BYTE_PIN_COMPATIBILITY=PASS
    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS
    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

No P5-D3F implementation authority is granted before this local PASS is adjudicated and persisted.

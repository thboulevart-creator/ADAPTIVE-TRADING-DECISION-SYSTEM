# OBSIDIAN P5-D3F — CONTRACT TARGETED BLOB FAILURE

Date: 2026-09-28

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The user supplied a governed local run from the new clone:

    C:\Users\Boulevart\ATDS-GIT\ADAPTIVE-TRADING-DECISION-SYSTEM

The assistant did not independently execute the local Windows test run.

## Runtime candidate

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83

## Reported preconditions

    CONTROL_REPO_ROOT=C:\Users\Boulevart\ATDS-GIT\ADAPTIVE-TRADING-DECISION-SYSTEM
    CONTROL_CLONE_CLEAN_BEFORE=PASS
    FETCHED_HEAD=ed7030c398976425642b91b641a8fac28846a2be
    REMOTE_RACE_GUARD=PASS
    P5D3F_RUNTIME_HEAD=f4d8258a59af52c67b3ddb66c5c1bfc502060e83
    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS

## Reported targeted result

    Ran 24 tests in 0.031s
    FAILED (failures=1)
    BLOCKED: P5-D3F targeted contract tests failed

Exact failing test:

    test_contract_blob_and_schema_are_exact

Reported assertion:

    _git_blob_oid(self.raw)
        = 2a92945aaf44635dd3b56a8d225a6292b09fa269

    EXPECTED_CONTRACT_BLOB
        = 64744325251db350d26c0269090ce62d5fa5f2e8

## Interpretation

The governed runner independently passed its Git-level contract blob guard:

    P5D3F_CONTRACT_BLOB=PASS

before the Python unit test failed.

Therefore the failure does not demonstrate that the committed contract blob changed.

The unit test computes a Git blob OID directly from working-tree bytes read with Path.read_bytes().

On Windows, working-tree newline materialization may differ from the canonical committed Git blob representation.

The exact-blob contract assertion is therefore incorrectly coupled to local checkout byte representation.

## Correction scope

Correct only the platform-sensitive contract-test identity assertion.

The corrected test should bind to the committed Git object identity rather than re-deriving that identity from working-tree bytes.

Preserve unchanged:

    P5-D3F contract semantics
    P5-D3F contract blob
    P5-D3F architecture
    P5-D3F authority boundary

Update the governed runner only as required to pin the corrected test blob.

## Qualification state

    P5D3F_CONTRACT_TARGETED=FAIL
    P5D3F_FULL_REBREAK=NOT_EXECUTED
    P5D3F_CONTRACT_REBREAK_COMPLETED=NOT_GRANTED

## Verdict

**BLOCKED — PLATFORM-SENSITIVE WORKING-TREE BLOB ASSERTION**

No P5-D3F contract qualification is granted by this run.

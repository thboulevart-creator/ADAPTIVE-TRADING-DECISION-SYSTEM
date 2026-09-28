# OBSIDIAN P5-D3F — STALE IN-MEMORY RUNNER BLOCK

Date: 2026-09-28

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The local run was supplied by the user and was not independently executed by the assistant.

## Reported sequence

The runner started from:

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83

It then successfully resolved the remote race guard:

    FETCHED_HEAD=fbb6626b5c647efda1adad6da2f199acf51a17fc
    REMOTE_RACE_GUARD=PASS

and switched the worktree to:

    a12bc12d6279b1dfc58b507c282578310d7fd2b0

It then reported:

    P5D3F_RUNTIME_HEAD=a12bc12d6279b1dfc58b507c282578310d7fd2b0

and blocked at:

    BLOCKED: P5-D3F contract-test blob inattendu:
    3dc1d7315874d4352eeaf05407f266961c878e70

## Root cause

The runner process was loaded into Python memory before the worktree checkout changed.

Therefore:

- filesystem source after checkout = a12bc12 candidate;
- in-memory constants/functions = f4d8258 runner.

The a12bc12 worktree contains:

    EXPECTED_TEST_BLOB =
    3dc1d7315874d4352eeaf05407f266961c878e70

but the already-running f4d8258 process retained the earlier expected test blob.

The reported actual test blob was therefore correct, but it was compared by stale in-memory code.

## Governance interpretation

This is a runner-bootstrap defect.

It is not:

- a P5-D3F contract semantic failure;
- a contract-test failure;
- a full regression failure;
- a handoff-runtime failure.

No qualification is granted.

## Required correction

A governed runner that changes its own repository HEAD must not continue qualification with code loaded from the previous HEAD.

After an actual candidate checkout it must:

1. verify the exact new HEAD;
2. verify the runner exists at the new HEAD;
3. re-exec the Python interpreter against the runner file from the new HEAD;
4. only then perform blob checks and qualification tests.

The re-exec must be bounded and loop-safe.

## Verdict

**BLOCKED — STALE IN-MEMORY RUNNER AFTER SELF-CHECKOUT**

P5-D3F contract remains unqualified pending corrected runner re-break.

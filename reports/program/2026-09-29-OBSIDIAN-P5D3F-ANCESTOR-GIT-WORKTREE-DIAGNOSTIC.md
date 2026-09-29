# OBSIDIAN P5-D3F — ANCESTOR GIT WORKTREE DIAGNOSTIC

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL DIAGNOSTIC.

## Observed diagnostic

Sacrificial staging path:

    C:\Users\Boulevart\AppData\Local\Temp\p5d3f-gitcheck-blnuoqvz\promotion-staging

Git probe:

    git -C <staging> rev-parse --show-toplevel

Observed:

    RC=0
    OUT=C:/Users/Boulevart
    GIT_DIR=None
    GIT_WORK_TREE=None

## Interpretation

The staging directory is not itself the Git worktree root.

Instead, Git discovers an ancestor worktree rooted at:

    C:/Users/Boulevart

The current implementation helper treats any directory located inside an ancestor Git worktree as if the directory itself were a Git repository/worktree.

That is broader than the frozen P5-D3F contract field:

    staging_must_not_be_git_repository = true

and causes sacrificial temp staging beneath the user profile to fail before evaluation.

## Correction boundary

The implementation must distinguish:

1. staging itself is a Git repository/worktree root -> reject;
2. staging merely has an ancestor Git worktree -> do not reject on this check alone.

No mutation of C:\Users\Boulevart or any ancestor .git metadata is authorized.

P5-D3F implementation remains unqualified until the corrected candidate passes the governed full suite.

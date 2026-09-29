# OBSIDIAN P5-D3F — ANCESTOR GIT WORKTREE CORRECTION STATIC REVIEW

Date: 2026-09-29

## Evidence status

Same-assistant static review only.

## Exact corrected functional candidate

    6cfcf61e6ad484883f973e4b9518c4d086a6d61f

Implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Tests blob:

    ab05169e298cca06e35f2bcc1775f38b30857aae

## Triggering evidence

USER-REPORTED local diagnostic established:

    staging path = C:\Users\Boulevart\AppData\Local\Temp\...\promotion-staging
    git rev-parse --show-toplevel = C:/Users/Boulevart
    GIT_DIR=None
    GIT_WORK_TREE=None

The prior helper therefore confused a directory inside an ancestor Git worktree with the staging directory itself being a Git repository root.

## Test-first correction

Two breakers were added before implementation correction:

1. ancestor Git worktree does not make staging itself a repository;
2. staging that is itself initialized as a Git repository still fails closed.

## Implementation correction

The helper now rejects only when:

    resolved(git --show-toplevel) == resolved(staging)

A nonzero Git probe remains accepted as "not a Git repository root".

A successful probe resolving to an ancestor no longer rejects staging on this condition.

No ancestor Git metadata is mutated.

## Scope

No P5-D3F contract semantics were changed.
No publication authority was opened.
No real Vault write was added.
No CURRENT/CURRENT.tmp writer was added.
P5-D3G remains closed.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    LOCAL GOVERNED RE-BREAK = REQUIRED
    P5-D3F IMPLEMENTATION = UNQUALIFIED UNTIL LOCAL PASS

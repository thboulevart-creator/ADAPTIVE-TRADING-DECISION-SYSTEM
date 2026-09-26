# OBSIDIAN P5-A — CONTINUOUS PROJECTION ENGINE QUALIFICATION

Date: 2026-09-26

## Scope

This record closes P5-A, the contract-and-breakers phase for the continuous GitHub → Obsidian projection engine.

## Persisted candidate identity

Branch:

    feat/obsidian-projection-p5a-continuous-projection-contract-v0.1

Persisted candidate HEAD before local execution:

    2989f2f046705eceba9c60f3ea0ebb5d37939b3f

Qualified predecessor P4-C closure:

    10355f467ccf8f87070ab18839b96ba6fc547d9d

## User-reported local execution

The user reported:

    Ran 343 tests in 7.404s
    OK

The initial wrapper then emitted:

    BLOCKED: P5-A control clone became dirty.

A read-only `git status --porcelain --untracked-files=all` inspection of the exact control clone reported only:

    ?? tests/obsidian_projection/__pycache__/test_continuous_projection_contract_v0_1.cpython-313.pyc

No tracked-file modification was reported.

## Adjudication of the dirty-clone signal

The sole untracked file is a Python bytecode cache produced by local runtime execution.

It is not repository source, not a governed artifact, not a projection artifact, and not evidence of source mutation.

Therefore:

- the 343-test suite result remains accepted as PASS;
- the control clone is treated as **SOURCE-CLEAN WITH RUNTIME RESIDUE**;
- no test rerun is required;
- the wrapper's generic `git status` cleanliness criterion is adjudicated as overly broad for Python execution.

Future persisted re-break procedures must distinguish:

    TRACKED SOURCE CHANGE
        => BLOCKED

    UNEXPECTED UNTRACKED SOURCE/ARTIFACT
        => BLOCKED

    __pycache__/ or *.pyc runtime residue only
        => IGNORE FOR SOURCE-CLEANLINESS

This adjudication does not permit ignoring arbitrary untracked files.

## Qualified P5-A boundary

P5-A qualifies only the architecture and contract for a continuous projection engine.

Qualified architecture:

- canonical source: GitHub `origin/integration/system-v1`;
- candidate observer: local read-only remote-ref observer;
- delivery semantics: near-real-time bounded latency;
- target maximum detection latency: 60 seconds;
- candidate observation interval: 30 seconds;
- exact-head isolated checkout required;
- same HEAD => NOOP;
- only INITIAL / FAST_FORWARD may auto-promote;
- NON_FAST_FORWARD / UNKNOWN => BLOCKED_REQUIRES_ADJUDICATION;
- dynamic inventory required for each exact HEAD;
- deterministic double build required;
- failed candidate leaves last-known-good projection unchanged;
- direct in-place multi-file promotion forbidden;
- mixed generation visibility forbidden;
- human `views/` protected from automatic overwrite;
- `.obsidian/`, plugins, Sync, and canonical user worktree protected;
- volatile observer state remains outside the Vault;
- single promotion writer required;
- projection states: CURRENT / STALE / BLOCKED / ORPHAN / MISSING.

## Non-authorizations preserved

P5-A still does not authorize:

- starting a background observer;
- starting a polling loop;
- registering a Windows service/startup task;
- creating a scheduled task;
- continuously mutating the Vault;
- replacing the live generated tree;
- overwriting human views;
- modifying `.obsidian/`.

## Evidence status

Runtime execution evidence is USER-REPORTED LOCAL EXECUTION.

GitHub persistence of this record does not convert it into independent execution evidence.

## Verdict

**PASS — P5-A CONTINUOUS PROJECTION ENGINE CONTRACT QUALIFIED**

The next authorized boundary is:

    P5-B — DYNAMIC CURRENT-HEAD INVENTORY
    + SOURCE SELECTION CONTRACT

P5-B must remove the frozen 74-artifact pilot limitation before continuous synchronization implementation can proceed.

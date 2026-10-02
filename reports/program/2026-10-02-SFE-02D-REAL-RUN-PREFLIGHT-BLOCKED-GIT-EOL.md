# SFE-02D — REAL RUN PREFLIGHT BLOCKED — GIT EOL NORMALIZATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## State

```text
HEAD =
8170e9140b60fd5b0b1c7441b281c6380c2d7f5c

TREE =
f4cde4723995674bc4eb23063c151c6ea0b5982a
```

## Attempted operation

The governed SFE-02D runner was invoked in no-peek mode before any result persistence.

It failed closed during protected-artifact verification, before reading the real H1 dataset and before calculating any strategy result.

Observed blocker:

```text
GIT_BLOB_MISMATCH:
GOVERNANCE/SFE-02C-DUAL-EXPERIMENT-SHARED-SURFACE-V0.1.json

EXPECTED GIT BLOB =
0fcf3ce86033b5d8b75caa0a1f18cc6b64fd54a2

RAW WORKTREE HASH =
d73123c92f633ff7cfe12be75753ade20e470c7a
```

## Root cause

Windows Git configuration:

```text
core.autocrlf = true
```

Canonical repository object:

```text
git rev-parse HEAD:GOVERNANCE/SFE-02C-DUAL-EXPERIMENT-SHARED-SURFACE-V0.1.json
=
0fcf3ce86033b5d8b75caa0a1f18cc6b64fd54a2
```

The checkout bytes contain CRLF line endings, so raw working-tree byte hashing does not equal the normalized Git object identity.

## Safety result

```text
REAL H1 READ =
NO

BREAKOUT RESULT CALCULATED =
NO

MEAN REVERSION RESULT CALCULATED =
NO

BREAKOUT ENVELOPE EXISTS =
NO

MEAN REVERSION ENVELOPE EXISTS =
NO

DUAL MANIFEST EXISTS =
NO

WORKTREE =
CLEAN
```

## Correction boundary

Only the Git-provenance verifier may change:

```text
OLD =
raw worktree bytes → synthetic Git blob SHA-1

NEW =
canonical Git object identity from HEAD:path
+
clean-worktree verification
```

No experiment definition, estimator, evidence gate, statistical rule, outcome rule, strategy runtime, dataset identity, or no-peek rule may change.

## Status

```text
SFE_02D_REAL_RUN =
NOT_STARTED

PERFORMANCE_OBSERVATION =
NONE

RUNNER_V0_1_GIT_VERIFIER =
NOT_PORTABLE_TO_CRLF_CHECKOUT

NEXT =
RUNNER V0.2 TARGETED PROVENANCE FIX
→ SYNTHETIC REBREAK
→ REAL NO-PEEK RUN IF PASS
```

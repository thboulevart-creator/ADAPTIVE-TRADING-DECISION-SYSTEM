# CHECKPOINT — 2026-09-28 — P5-D3F CONTRACT QUALIFIED

## Purpose

Simple restart checkpoint for the next session.

## Starting point of the day

P5-D3F was still blocked by Windows/Git worktree byte-representation issues.

The main symptom was:

- Git considered files logically unchanged;
- some historical tests computed Git blob IDs from raw worktree bytes;
- Windows checkout had CRLF bytes for files whose committed Git blobs were LF;
- therefore historical byte-pinned tests failed even while `git status` could be clean.

## What was established today

### 1. V7 — path-scoped Git index reconciliation

A controlled A/B experiment established that:

- whole-index `git update-index --really-refresh` did not clear the representative stat-only dirty classification;
- path-scoped `git update-index --really-refresh -- <path>` did;
- staged mode/OID/stage remained invariant.

V7 therefore replaced whole-index reconciliation with individually path-scoped reconciliation.

### 2. V8 — historical P2/P3 raw-byte dependencies

The first V7 full-suite execution passed all P5-D3F-specific targeted gates but exposed historical byte-pin failures.

A local diagnostic found seven additional historical dependencies with:

    RAW=MISMATCH
    FILTER=PASS
    i/lf
    w/crlf

Affected paths:

    tools/obsidian_projection/materialization_contract_v0_1.json
    tools/obsidian_projection/materialize.py
    tools/obsidian_projection/rendering.py
    tools/obsidian_projection/relations.py
    tools/obsidian_projection/integrity.py
    tools/obsidian_projection/builder.py
    tools/obsidian_projection/p2_verify.py

V8 added exactly those paths to the bounded byte-exact compatibility surface.

### 3. V9 — dynamic inventory tooling contract

After V8, only two failures remained:

    P5-D3D -> TOOLING_CONTRACT_MISMATCH
    P5-D3E -> TOOLING_CONTRACT_MISMATCH

A one-line diagnostic established for:

    tools/obsidian_projection/dynamic_inventory_contract_v0_1.json

that:

    HEAD=80729156f4ac51b760c4347f581f052a175b88b3
    RAW=4e4d4ed8e7135453d54504fc74c9586a55ae9c4a
    FILTER=80729156f4ac51b760c4347f581f052a175b88b3
    i/lf
    w/crlf

Static inspection showed dynamic_inventory.py validates this contract from raw bytes and maps its mismatch into the TOOLING_CONTRACT_MISMATCH family.

V9 therefore added exactly this path to the same bounded byte-exact compatibility surface.

## Final V9 governed local result

USER-REPORTED LOCAL EXECUTION:

    Ran 32 tests in 1.805s
    OK

    Ran 1090 tests in 22.598s
    OK

    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Qualified state

P5-D3F contract qualification report:

    reports/program/2026-09-28-OBSIDIAN-P5D3F-CONTRACT-QUALIFICATION-V9.md

Qualification commit:

    cff4355014639474146aba5b33eac72f0794ebd1

Qualification status:

    P5-D3F CONTRACT QUALIFICATION = PASS

Important scope:

- this qualifies the P5-D3F contract;
- it does NOT mean the promotion handoff runtime is implemented;
- it does NOT authorize production publication;
- it does NOT authorize real Vault writes;
- it does NOT authorize CURRENT or CURRENT.tmp mutation;
- it does NOT open P5-D3G.

## Simple mental model

Example:

Git stores the authoritative file as:

    line 1\n
    line 2\n

Windows had some local copies as:

    line 1\r\n
    line 2\r\n

For ordinary Git status, both can represent the same tracked content after normalization.

But a raw-byte pin sees different bytes and therefore a different blob ID.

The governed runner now canonicalizes only the explicitly identified byte-pinned compatibility files back to the exact committed bytes, verifies raw equality, reconciles Git stat state path-by-path, and proves the staged index did not change.

## Exact next frontier for tomorrow

Per the frozen P5-D3F contract:

    P5-D3F IMPLEMENTATION
    —
    FINITE_PROMOTION_HANDOFF_IMPLEMENTATION
    + SACRIFICIAL_STAGING_QUALIFICATION

The next session must begin with read-only/static reconstruction of the implementation boundary from the qualified contract and existing P5-D3C2 / P5-D3D / P5-D3E authorities before any implementation mutation.

The implementation must remain:

- outside the real Vault;
- finite, not continuous;
- staging-only for qualification;
- READY_UNAUTHORIZED;
- without CURRENT/CURRENT.tmp mutation;
- without live publication;
- without P5-D2 PROMOTION_CONFIRMED;
- without polling/background observer;
- without P5-D3G authority.

## Repository / branch

Repository:

    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

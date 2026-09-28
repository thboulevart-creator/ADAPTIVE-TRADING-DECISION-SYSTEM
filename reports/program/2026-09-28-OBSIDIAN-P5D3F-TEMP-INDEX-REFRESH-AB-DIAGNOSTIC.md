# OBSIDIAN P5-D3F — TEMP INDEX REFRESH A/B DIAGNOSTIC

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

This is not independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    8ded12890e9c7f6bdb9d8454edd184faedffc7ff

## Experiment

Two temporary copies of the real Git index were created through GIT_INDEX_FILE.

A — git update-index --really-refresh

Before refresh, the representative contract path was reported:

    1 .M N... 100644 100644 100644
    64744325251db350d26c0269090ce62d5fa5f2e8
    64744325251db350d26c0269090ce62d5fa5f2e8
    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

The command reported the eight bounded compatibility paths as "needs update" and returned:

    A_REFRESH_EXIT=1

The complete staged representation remained unchanged:

    A_STAGE_UNCHANGED=True

Afterwards, status against the temporary A index was clean.

B — git add --refresh

Before refresh, the same representative path was .M.

The command returned:

    B_REFRESH_EXIT=0
    B_STAGE_UNCHANGED=True

Afterwards, status against the temporary B index still reported .M.

The representative identities remained:

    HEAD=64744325251db350d26c0269090ce62d5fa5f2e8
    INDEX=100644 64744325251db350d26c0269090ce62d5fa5f2e8 0 <path>
    RAW=64744325251db350d26c0269090ce62d5fa5f2e8

The real index SHA-256 remained identical before/after the experiment:

    REAL_INDEX_UNCHANGED=True

## Adjudication

Supported:

- git add --refresh is NOT a viable correction for this failure;
- git update-index --really-refresh CAN reconcile the dirty classification when operating on a temporary index copy;
- staged mode/OID/stage remained invariant in the successful temporary-index case.

Still unresolved:

- why the same update-index --really-refresh operation did not reconcile the real .git/index in the earlier controlled recovery attempt.

Therefore no V7 implementation is authorized yet.

## Next diagnostic

Inspect structural index state without mutation:

- git rev-parse --shared-index-path;
- core.splitIndex;
- index.sparse;
- index version;
- fsmonitor-valid flag for the representative path;
- core.fsmonitor / core.untrackedCache / core.fscache;
- real index file attributes.

This will determine whether the real index has a structural/extension state that changes behavior relative to the temporary copy.

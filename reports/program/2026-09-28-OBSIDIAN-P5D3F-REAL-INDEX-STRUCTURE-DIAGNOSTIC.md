# OBSIDIAN P5-D3F — REAL INDEX STRUCTURE DIAGNOSTIC

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

Not independent execution evidence.

## Branch state before persistence

Verified remote HEAD:

    14c61bd5dbce425158b49fb2b706ad5288773bfe

## Observed Git/index state

Git version:

    2.54.0.windows.1

Index version:

    2

Shared index path:

    NONE

Repository configuration:

    core.splitIndex = UNSET
    index.sparse = UNSET
    core.fsmonitor = UNSET
    core.untrackedCache = UNSET

Representative fsmonitor-valid inspection:

    git ls-files -f -- <path>
    H <path>

The uppercase H does not indicate fsmonitor-valid lower-case state.

System Git configuration:

    core.fscache = true
    origin = C:/Program Files/Git/etc/gitconfig

Real index file:

    path = .git/index
    length = 147923
    attributes = Archive
    creation time UTC = 2026-09-28 18:52:43
    last write time UTC = 2026-09-28 18:52:43

## Adjudication

The following candidate explanations are not supported by this diagnostic:

- split-index;
- sparse index;
- configured fsmonitor;
- fsmonitor-valid flag on the representative path;
- configured untracked cache.

The remaining configuration-specific candidate exposed by this diagnostic is the Git-for-Windows filesystem cache:

    core.fscache=true

This is NOT yet established as the cause.

## Next bounded diagnostic

Before any runner mutation, test the existing dirty representative path with process-local:

    -c core.fscache=false

using status with --no-optional-locks.

Then, if the status remains dirty, compare temporary-index update-index --really-refresh under fscache=true versus fscache=false while preserving stage/OID invariance and leaving the real index untouched.

No V7 implementation is authorized until this diagnostic is adjudicated.

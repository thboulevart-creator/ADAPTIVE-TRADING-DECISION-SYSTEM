# OBSIDIAN P5-D3F — PERSISTENT REAL EXECUTION POST-WINERROR5 RESIDUAL AUDIT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY AUDIT.

No mutation is claimed.

## Exact persistent staging state

Path:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

Observed:

    STAGING_EXISTS=True

Metadata:

    Attributes = ReadOnly, Directory, Archive, ReparsePoint
    Mode = lar--
    CreationTime = 2026-09-29 13:48:16
    LastWriteTime = 2026-09-29 13:52:34

Recursive content listing returned no entries.

Therefore:

    staging content state = EMPTY

## Parent OneDrive / ATDS state

Path:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS

Observed metadata:

    Attributes = ReadOnly, Directory, Archive, ReparsePoint
    Mode = lar--

Observed ACL:

    Everyone = Deny DeleteSubdirectoriesAndFiles
    SYSTEM = Allow FullControl
    Administrators = Allow FullControl
    DESKTOP-49BN9M3\Boulevart = Allow FullControl

## Staging ACL

Observed:

    Everyone = Deny DeleteSubdirectoriesAndFiles
    SYSTEM = Allow FullControl
    Administrators = Allow FullControl
    DESKTOP-49BN9M3\Boulevart = Allow FullControl

## Handoff search

Recursive PROMOTION-HANDOFF.json search under:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS

returned no result.

Therefore:

    persistent handoff residual = NONE OBSERVED

## Adjudication

The failed governed execution created the exact persistent staging directory, but no retained handoff content is present.

The subsequent failure cleanup could not remove the directory. The observed inherited ACL includes a Deny DeleteSubdirectoriesAndFiles entry on Everyone, consistent with the observed WinError 5 at directory removal.

The staging and its parent also expose the ReparsePoint attribute through PowerShell. This is material because the persistent handoff implementation contains fail-closed alias/reparse checks.

However, PowerShell metadata alone does not establish exactly how Python os.stat/lstat and os.path.isjunction classify these OneDrive paths inside the governed implementation.

Therefore:

    PERSISTENT STAGING = PRESENT_EMPTY
    PROMOTION-HANDOFF = ABSENT
    REAL HANDOFF SUCCESS = NOT ESTABLISHED
    ORIGINAL INNER EXECUTION ERROR = STILL UNKNOWN / MAY HAVE BEEN MASKED
    SAME AUTHORIZATION RETRY = NOT AUTHORIZED

## Required next gate

READ-ONLY Python filesystem-semantics probe only.

The probe must inspect the exact parent, staging, and protected real Vault using the same Python primitives used by the implementation:

- Path.resolve(strict=True/False);
- Path.lstat().st_file_attributes;
- stat.FILE_ATTRIBUTE_REPARSE_POINT;
- os.path.isjunction when available;
- is_symlink;
- directory accessibility.

It must not create, delete, rename or write anything.

Only after this probe may the implementation failure path or OneDrive compatibility contract be changed.

The prior one-shot human authorization is treated as spent for governance purposes because the governed execution entrypoint was reached and persistent state changed from ABSENT to PRESENT_EMPTY.

A new one-shot human authorization will be required after any correction and requalification.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.

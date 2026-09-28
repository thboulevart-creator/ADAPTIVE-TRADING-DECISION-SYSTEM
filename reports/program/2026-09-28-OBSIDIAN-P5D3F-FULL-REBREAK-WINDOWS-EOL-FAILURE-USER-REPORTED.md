# OBSIDIAN P5-D3F — FULL RE-BREAK WINDOWS EOL FAILURE

Date: 2026-09-28

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The user supplied the final section of the governed P5-D3F full re-break from:

    C:\Users\Boulevart\ATDS-GIT\ADAPTIVE-TRADING-DECISION-SYSTEM

The assistant did not independently execute the Windows run.

## Reported full-suite result

    Ran 1084 tests in 16.750s
    FAILED (failures=4, errors=8)
    BLOCKED: full Obsidian suite failed

## Primary failure family

Multiple previously-qualified historical guards reported canonical expected Git blob IDs but different working-tree-derived blob IDs.

Examples reported:

P3-C first-open contract:

    expected=5cd11e9512249da26adf4b6f86e79259af725809
    actual=6aeeff6ea066c447a7df2ab2b019f6611a39bc39

P3-C2 first-open contract:

    expected=ddda9eb0abac4ff3fae02f459e16a1fa70bf907d
    actual=720acf12cce20859af7527039dae1bd146be117b

P2-A contract:

    expected=c546b7116c68ee17fd0ff5868748bb4b1bbae1f3
    actual=724093d71ee3005fb8527823904e6df90bf880e7

P5-D3E contract:

    expected canonical contract authority
    runtime raised "P5-D3E contract blob mismatch"

P5-C3R retry contract:

    runtime raised "P5-C3R retry contract blob mismatch"

## Cascading failures

The supplied output also showed downstream synthetic qualification failures in P5-D3D and P5-D3E after predecessor blob verification failed.

These are treated as downstream consequences until a contrary cause is demonstrated.

## Static diagnosis

The new working clone is on Windows and the repository currently has no .gitattributes file.

The failure pattern is consistent with checkout newline materialization changing local text-file bytes while Git still stores and reports the canonical committed blobs expected by the historical qualification surfaces.

The P5-D3F-specific targeted contract stage had already passed before the full historical regression reached these predecessor guards.

## Required correction direction

Do not rewrite or repin historical qualified predecessor blobs.

Do not weaken predecessor tests.

Instead, make the repository checkout representation deterministic and canonical for text files so working-tree byte hashing reproduces the committed LF-form Git objects.

A repository-level .gitattributes rule should be preferred over relying on machine-global core.autocrlf state.

## Qualification status

    P5D3F_CONTRACT_TARGETED = PASS prior to full suite
    P5D3F_FULL_REBREAK = FAIL
    P5D3F_CONTRACT_REBREAK_COMPLETED = NOT_GRANTED

## Verdict

**BLOCKED — WINDOWS WORKTREE TEXT NORMALIZATION INCOMPATIBLE WITH HISTORICAL BYTE-PIN TESTS**

No P5-D3F qualification is granted by this run.

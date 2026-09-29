# OBSIDIAN P5-D3G — IMPLEMENTATION QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed P5-D3G implementation re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    a887e89865eace663b82f18dbec677690450f7bf

Corrected functional candidate:

    f725854a7539d1a3b589ca2e49d45c22f6699d3d

Implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

Implementation tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed runner blob:

    94d2a08cce581244c64945e7a50de76cbe13900b

Frozen P5-D3G contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

## User-reported governed result

Targeted P5-D3G contract + implementation tests:

    Ran 43 tests in 95.052s
    OK

Complete historical Obsidian suite:

    Ran 1147 tests in 148.506s
    OK

Terminal markers:

    P5D3G_IMPLEMENTATION_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3G_IMPLEMENTATION_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed governed run.

## Adjudication

    P5-D3G IMPLEMENTATION QUALIFICATION = PASS
    SACRIFICIAL LIVE-VAULT QUALIFICATION = PASS

This qualifies the corrected finite live-publication transaction implementation only within the sacrificial qualification boundary exercised by the tests.

## Authority boundary after qualification

Still NOT authorized by this qualification alone:

- production real-Vault execution;
- write to C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION;
- production CURRENT.md or CURRENT.tmp mutation;
- production P5-D2 PROMOTION_CONFIRMED;
- automatic publication;
- background observer or polling;
- Windows startup / scheduled-task / service registration;
- P5-D4 observer-loop qualification;
- P6 Graph/Search CURRENT-generation semantics.

## Next-boundary note

The qualified contract requires explicit human authorization after an exact read-only publication plan for any finite live publication transaction.

The sacrificial-only guard in the qualified implementation must not be silently weakened or bypassed.

Any production enablement or real-Vault transaction therefore requires a separately governed boundary and explicit human authorization.

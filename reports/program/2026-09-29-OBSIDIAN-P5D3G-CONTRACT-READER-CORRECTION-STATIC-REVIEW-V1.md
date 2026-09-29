# OBSIDIAN P5-D3G — CONTRACT READER CORRECTION STATIC REVIEW V1

Date: 2026-09-29

## Evidence status

Same-assistant static review only.

## Triggering evidence

USER-REPORTED local isolated test:

    test_planning_is_read_only ... ERROR
    LivePublicationGovernanceError:
    non-canonical JSON:
    live_publication_transaction_contract_v0_1.json

## Exact correction candidate

    f725854a7539d1a3b589ca2e49d45c22f6699d3d

Corrected implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

Implementation tests blob unchanged:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed runner blob:

    94d2a08cce581244c64945e7a50de76cbe13900b

Qualified contract blob unchanged:

    64997ddd9977229961387f66af4de356c045c0ac

## Correction

_operation_sequence_digest() no longer passes the exact qualified human-readable contract through the compact-canonical JSON artifact reader.

It now:

1. reads the exact blob-pinned contract bytes;
2. decodes strict UTF-8;
3. parses JSON;
4. requires an object;
5. extracts operation_order;
6. canonically hashes only the operation_order value.

The exact qualified contract is still protected by _verify_tooling_identity() before publication planning.

## Boundary

No contract semantic changed.
No contract blob changed.
No implementation test expectation changed.
No live-Vault authority changed.
No real Vault write is authorized.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    REPRESENTATIVE LOCAL TEST = REQUIRED
    FULL GOVERNED RE-BREAK = NOT YET AUTHORIZED AS PASS EVIDENCE
    P5-D3G IMPLEMENTATION = UNQUALIFIED

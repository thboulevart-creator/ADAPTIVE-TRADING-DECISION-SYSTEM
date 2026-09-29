# OBSIDIAN P5-D3G — IMPLEMENTATION STATIC REVIEW V1

Date: 2026-09-29

## Evidence status

Same-assistant static review only.

This is not local execution evidence and does not qualify the implementation.

## Exact candidate reviewed

    80a40ee5413644904d6841f2acfd13a29c796b3a

Implementation blob:

    eb0e6607430d32fe51c065ed4bacba05721f42b6

Implementation tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed runner blob:

    624b9752184137a23819dd15f490b5d57518da96

Frozen contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

## Static findings

PASS — the implementation hard-rejects the exact real production Vault path during this qualification phase.

PASS — planning is read-only and materialization cannot begin before exact human-authorization validation and exclusive writer ownership.

PASS — authorization is bound to the exact plan digest, candidate HEAD/TREE, generation ID, publication mode and previous CURRENT state.

PASS — authorization consumption is persisted outside the live Vault and cannot be silently reused by a second normal transaction.

PASS — a rollback basis is durably captured outside the live Vault before live materialization.

PASS — the retained P5-D3F handoff is freshly reverified before mutation and its sealed package is copied byte-for-byte into the immutable live-generation wrapper.

PASS — publication metadata remains outside the sealed package.

PASS — CURRENT.tmp is exclusively created, flushed, fsynced and byte-verified before pointer replacement.

PASS — normal and recovery pointer replacement use bounded retries only for Windows sharing-conflict winerror 5/32.

PASS — CURRENT is read back and the target generation is independently verified after replacement.

PASS — the physical receipt is persisted before P5-D2 PROMOTION_CONFIRMED is attempted.

PASS — logical-confirmation failure remains a distinct physical-success/logical-pending state.

PASS — recovery distinguishes previous CURRENT / new CURRENT / exact target / invalid target / ambiguous state.

PASS — exact new CURRENT + exact target completes forward rather than blindly rolling back.

PASS — replace-mode rollback requires the persisted exact previous CURRENT bytes and reverifies the previous immutable generation before restoring the pointer.

PASS — rollback does not emit PROMOTION_CONFIRMED for the failed candidate.

PASS — the implementation contains no background thread, repeated observer loop, task/service registration or scheduler surface.

## Static surface counts

Implementation tests:

    20

Forbidden-loop scan:

    while True = 0
    threading.Thread = 0
    polling token = 0
    schtasks token = 0
    CreateService token = 0
    schedule. token = 0

Expected bounded atomic replacements:

    os.replace calls = 2

## Remaining uncertainty

No Python compilation has yet been observed for this exact candidate.

No targeted implementation tests have yet been observed.

No full historical suite has yet been observed.

Therefore:

    STATIC IMPLEMENTATION REVIEW = PASS
    P5-D3G IMPLEMENTATION = NOT YET QUALIFIED
    SACRIFICIAL LIVE-VAULT QUALIFICATION = NOT YET ESTABLISHED
    REAL VAULT = CLOSED

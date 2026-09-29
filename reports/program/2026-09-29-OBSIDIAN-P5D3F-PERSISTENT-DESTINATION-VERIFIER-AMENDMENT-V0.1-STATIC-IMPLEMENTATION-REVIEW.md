# OBSIDIAN P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT V0.1 — STATIC IMPLEMENTATION REVIEW

Date: 2026-09-29

## Evidence status

SAME-ASSISTANT STATIC REVIEW of GitHub source state.

No local test execution is claimed by this report.

## Implementation candidate

    48f75479e2a6c3a0c837e9a3476555fcdaa8a36d

## Exact blobs

Candidate-generation verifier:

    65edda8427744c0ed8b8dfa7ae0333d474b8c00d

P5-D3F promotion handoff:

    cb8dd498fbc503acfcccb38799965c8139db82a7

Persistent production wrapper:

    1babcefe4f75173fab5d1f0aeec43c2f7b8aad68

Amendment implementation tests:

    6599b63a8d7595d136938d451b0781b549020bfc

Persistent wrapper historical tests:

    3c463e818909a8330557fcc463e7c4e16d38b9b2

Governed re-break:

    eb976bcfad405668e8da549997bc7e6d2ef784eb

## Static review

### Historical TEMP-only verifier

verify_candidate_generation remains a distinct public entrypoint.

Its existing location policy still passes through _validate_existing_package_root, which retains:

    package root must be below OS temp root

The content-verification body was moved into one shared internal function:

    _verify_candidate_generation_content

The TEMP-only root policy itself was not broadened.

### New persistent verifier

A distinct read-only entrypoint now exists:

    verify_persistent_candidate_generation

It requires an explicit:

    authorized_staging_root

and validates the package under the exact wrapper shape:

    <authorized_staging_root>/packages/<generation_id>/package

before delegating to the same semantic/content verification core used by the historical TEMP-only verifier.

It additionally verifies that the wrapper generation directory name equals the descriptor generation_id.

### Alias and hardlink controls

The persistent path performs lexical ancestor-chain checks before resolving the path and also rechecks the resolved directory chain.

The existing recursive package-tree alias/reparse/symlink and single-link regular-file controls remain reused.

### P5-D3F binding

The source candidate package continues to use:

    verify_candidate_generation

The copied persistent destination uses:

    verify_persistent_candidate_generation

with:

    authorized_staging_root=staging

Source/destination descriptor equality and package byte-tree digest equality remain mandatory.

Post-write P5-D3F handoff reverification receives the explicit promotion staging authority.

### Persistent wrapper closure

The outer persistent_production_handoff wrapper now passes:

    promotion_staging_root=staging

to its post-materialization verify_promotion_handoff call.

Its qualified P5-D3F implementation pin is updated to the amended P5-D3F blob.

This closes the second persistent reverification path that would otherwise have fallen back to the historical TEMP-only verifier.

### Authority boundary

No real execution is performed by these changes.

No real-Vault write, CURRENT/CURRENT.tmp mutation, live publication, PROMOTION_CONFIRMED, Stage A, Stage B, background loop, scheduler, or service authority is added.

## Test surface

Amendment implementation tests:

    20 tests

They cover at minimum:

- exact authorized persistent wrapper acceptance;
- TEMP/persistent descriptor parity;
- read-only verification;
- wrong staging authority;
- wrong wrapper layout;
- arbitrary package outside authority;
- real-Vault intersection;
- alias/reparse chain;
- ancestor alias;
- hardlink;
- tampered payload;
- tampered generation manifest;
- tampered seal;
- generation-id wrapper mismatch;
- one shared verification core;
- P5-D3F destination binding;
- post-write staging-authority reverification;
- persistent wrapper staging-authority reverification;
- no later publication authority.

## Static adjudication

    STATIC IMPLEMENTATION REVIEW = PASS
    LOCAL TARGETED TESTS = PENDING
    FULL OBSIDIAN RE-BREAK = PENDING
    REAL EXECUTION = NOT AUTHORIZED

## Next exact action

Run the governed synthetic re-break from the implementation candidate while the remote branch is pinned to this review commit.

Mandatory STOP after the re-break result.

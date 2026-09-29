# OBSIDIAN P5-D3F — IMPLEMENTATION LOCAL RE-BREAK BLOCKED V2

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION.

Not independent execution evidence.

## Verified GitHub state before persistence

Remote HEAD:

    5a2967dc26e8526c5e5193154a5f954ed47cf2af

Functional implementation candidate:

    4185c20241eaed03d3155e8d9b30d333947c6293

Implementation blob:

    90922f53b5ac74fc4ac7ad643d3b38860d60abbb

Tests blob:

    ec3292b685f8ee107140a2a75f747de6bb1839b0

## User-reported governed local result

Targeted P5-D3F contract controls:

    Ran 32 tests in 1.995s
    OK

Full Obsidian suite:

    Ran 1102 tests in 32.433s
    FAILED (errors=9)
    BLOCKED: full Obsidian suite failed

Nine implementation tests errored:

    test_blocked_candidate_creates_no_handoff
    test_existing_generation_target_blocks
    test_handoff_verifier_is_read_only
    test_handoff_wrapper_name_matches_generation_id
    test_rejected_candidate_creates_no_handoff
    test_staging_overlap_with_live_vault_fails_closed
    test_successful_synthetic_handoff_is_ready_unauthorized
    test_tampered_copied_payload_is_rejected
    test_tampered_handoff_identity_is_rejected

## Current adjudication

Supported:

- the qualified P5-D3F contract still passes its targeted controls;
- the new implementation candidate does not pass the full historical suite;
- the failures concentrate on tests that execute run_finite_promotion_handoff().

Not yet established:

- the exact common exception/root cause;
- whether all nine errors are one pre-evaluation failure or multiple defects.

## Next action

Run one representative successful-handoff test without broad output filtering and inspect only its final traceback.

Do not modify the implementation until the first concrete exception is identified.

P5-D3F implementation remains unqualified.
Sacrificial-staging qualification remains unopened.
P5-D3G remains closed.

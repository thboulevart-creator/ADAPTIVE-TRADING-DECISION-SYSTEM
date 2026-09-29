# OBSIDIAN P5-D3G — IMPLEMENTATION LOCAL RE-BREAK BLOCKED V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION.

## Verified GitHub state

Remote HEAD before persistence:

    0005cc7bc10eea196102fffeeaeb47a98e745d86

Functional candidate under test:

    88e222c0ab95f683b36a9ac08a8b9929a83b5994

## Governed targeted result

Reported:

    Ran 43 tests in 58.952s
    FAILED (errors=17)
    BLOCKED: P5-D3G targeted implementation tests failed

The 43 targeted tests consist of the qualified P5-D3G contract tests plus the implementation tests.

## Isolated representative failure

User-reported isolated execution:

    test_planning_is_read_only ... ERROR
    Ran 1 test in 3.896s
    FAILED (errors=1)

First exception:

    LivePublicationGovernanceError:
    non-canonical JSON:
    live_publication_transaction_contract_v0_1.json

Trace location:

    build_publication_plan
      -> _operation_sequence_digest
      -> _read_json_canonical

## Static diagnosis

The qualified P5-D3G contract blob is:

    64997ddd9977229961387f66af4de356c045c0ac

The committed contract is intentionally stored as human-readable indented JSON.

The implementation already verifies the exact qualified contract Git blob through _verify_tooling_identity() before planning.

_operation_sequence_digest() then redundantly reopens that exact qualified contract through _read_json_canonical(), which additionally requires compact canonical JSON bytes.

That serialization requirement is not an authority boundary of the qualified contract source file. The contract requires canonical JSON for publication plans and governed transaction artifacts, not compact serialization of the human-readable qualified contract document itself.

## Correction boundary

Do not modify or reserialize the qualified contract.

Do not weaken exact contract blob verification.

Correct only the internal contract reader used by _operation_sequence_digest() so that it:

1. reads the exact blob-pinned contract as UTF-8 JSON;
2. requires a JSON object;
3. extracts operation_order;
4. retains canonical hashing of the operation_order value.

P5-D3G implementation remains unqualified until corrected governed execution passes.

# OBSIDIAN P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT V0.1 — FIRST FULL RE-BREAK FAILURE ADJUDICATION

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION plus VERIFIED GITHUB source state plus SAME-ASSISTANT STATIC REVIEW.

## User-reported governed re-break result

Targeted amendment surface:

    Ran 65 tests in 24.637s
    OK
    P5D3F_PERSISTENT_VERIFIER_AMENDMENT_TARGETED=PASS

Full Obsidian suite:

    Ran 1299 tests in 147.225s
    FAILED (failures=2, errors=17)

The governed runner correctly stopped:

    BLOCKED: full Obsidian suite failed

The following preconditions were reported PASS:

    REMOTE_RACE_GUARD=PASS
    P5D3F_PERSISTENT_VERIFIER_AMENDMENT_BLOBS=PASS
    P5D3F_PERSISTENT_VERIFIER_AMENDMENT_SURFACE_SCAN=PASS
    P5D3F_PERSISTENT_VERIFIER_AMENDMENT_PY_COMPILE=PASS

## Direct amendment compatibility failures

Two failures were in historical P5-D3C2 adversarial tests:

    test_descriptor_authority_is_literal_false
    test_no_background_loop_entrypoints

Static review identified both as amendment-induced compatibility regressions in test-observable historical surface, not desired new behavior.

### Descriptor authority surface

The shared-core refactor moved the literal:

    "promotion_authorized": False

out of the public verify_candidate_generation function body.

The historical adversarial test intentionally inspects that public function's source.

Correction:

- shared semantic/content core retained;
- public historical verifier now additionally enforces a local literal false authority guard;
- no promotion authority is added.

### Background-loop surface

The amendment introduced two new alias-chain helpers using unbounded lexical form:

    while True

The historical P5-D3C2 adversarial test permits a while loop only in the already-qualified historical alias-chain helper.

Correction:

- the two new persistent-only alias traversals are now finite bounded for-loops;
- each has an explicit traversal-exceeded fail-closed error;
- the historical helper itself is untouched.

## Downstream P5-D3G errors

All 17 reported errors belong to:

    test_p5d3g_live_publication_transaction.P5D3GLivePublicationImplementationTests

Static dependency review shows the qualified P5-D3G live-publication implementation still pins:

    P5D3F_IMPLEMENTATION_BLOB =
    2108131914cf65bb076b80f5bb63cd63267567fa

and:

    P5D3C2_VERIFIER_BLOB =
    e2e5867536f4f9c7dec475c6696737249536ff39

The current amendment necessarily changes those upstream blobs.

P5-D3G calls _verify_tooling_identity() at its public planning, verification, execution, classification, and recovery entrypoints.

Therefore these 17 downstream errors are structurally consistent with stale P5-D3G dependency pins.

This report does NOT requalify or modify P5-D3G because the current human authorization explicitly does not authorize live publication, Stage A, or Stage B.

A corrected re-break is required to confirm that the two direct historical compatibility failures are closed and to isolate any remaining downstream P5-D3G dependency-pin blocker.

## Corrected implementation state

Candidate-generation verifier blob:

    398bda75604f8172128fbe0ddaf78cab4cee9f92

P5-D3F handoff blob:

    23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60

Persistent wrapper blob:

    375607d88bc926e4fd4c297ddc6fedba5506642a

Governed re-break blob:

    3e72f1884458fcfaaf93d5f4c631c886b33f6ce3

The targeted re-break now explicitly includes:

    test_p5d3c2_adversarial

so the two historical compatibility regressions can no longer hide behind a targeted PASS.

## Governance status

    FIRST TARGETED RUN = PASS
    FIRST FULL RE-BREAK = BLOCKED
    TWO DIRECT COMPATIBILITY REGRESSIONS = CORRECTED STATICALLY
    P5-D3G DOWNSTREAM PIN DRIFT = SUSPECTED / NOT YET LOCALLY CONFIRMED BY TRACEBACK
    REAL EXECUTION = NOT AUTHORIZED
    LIVE PUBLICATION = NOT AUTHORIZED
    MANDATORY STOP = ACTIVE

No P5-D3G source or tests were modified.
No real persistent handoff was executed.
No real Vault access was authorized.

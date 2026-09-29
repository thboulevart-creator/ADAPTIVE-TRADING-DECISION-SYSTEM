# OBSIDIAN P5-D3G — LIVE PUBLICATION TRANSACTION CONTRACT STATIC REVIEW V1

Date: 2026-09-29

## Evidence status

Same-assistant static review.

This is not execution evidence and does not qualify the contract.

## Exact candidate reviewed

Functional candidate:

    195f2689d10edbadf2904f68621fd5df65000498

Contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

Tests blob:

    dbf37f769a407923fbdeb3bb476aa8cd0405b6ef

Runner blob:

    88c1540fa0865558d73e4feb640ca59201e226e3

Documentation blob:

    9fd3d9869289535af2313d990d2c018dde341295

## Static findings

PASS — P5-D3F is the only admissible candidate-input authority and must reverify READY_UNAUTHORIZED before planning and immediately before first mutation.

PASS — publication planning is explicitly read-only and precedes human authorization.

PASS — human authorization is exact-plan-bound, one-shot and cannot be inferred from CLI invocation, configuration or prior approval.

PASS — one finite writer owns the transaction; a second writer blocks and stale ownership cannot be silently stolen.

PASS — P5-C2 authority is preserved exactly: only IMMUTABLE_GENERATION_ATOMIC_POINTER survives. Directory swap and MoveFileEx fallbacks remain forbidden.

PASS — the contract identifies the P5-C3R2 productionization gap. The exact qualified synthetic writer hardcodes GEN_A/GEN_B and is not falsely treated as production-generalized authority.

PASS — P5-C3R2 bounded pointer semantics are preserved: CURRENT.tmp, fsync, byte verification, os.replace, Windows write retries for winerror 5/32, bounded reader retry and read-after-write verification.

PASS — the sealed P5-D3F package remains byte-exact inside a production wrapper; publication metadata remains outside the sealed package.

PASS — target generation verification is ordered before CURRENT.tmp creation.

PASS — existing partial or mismatched targets block rather than being overwritten or recursively deleted.

PASS — replace and bootstrap publication modes are distinct.

PASS — physical publication, physical evidence and logical P5-D2 PROMOTION_CONFIRMED are separate ordered facts.

PASS — crash recovery is state-based and distinguishes old CURRENT, new CURRENT, exact target, partial target and ambiguous states.

PASS — a verified new CURRENT + exact target must complete forward rather than being rolled back merely because later evidence persistence was interrupted.

PASS — rollback is restricted to replace mode and exact captured previous CURRENT / previous verified generation.

PASS — last-known-good generations may not be deleted during recovery.

PASS — P5-D4 remains BOUNDED_OBSERVER_LOOP_CANDIDATE.

PASS — Graph/Search semantics remain deferred to P6.

## Surface inventory

Required adversarial breakers:

    87

Unique adversarial breakers:

    87

Contract test methods:

    23

The governed runner targets the exact P5-D3G contract test and the complete historical Obsidian test discovery.

## Boundary verification

The contract currently keeps all of the following false:

    live_publication_runtime_implementation_authorized
    sacrificial_live_vault_execution_authorized
    production_live_vault_execution_authorized
    real_vault_write_authorized
    current_pointer_creation_authorized
    current_pointer_mutation_authorized
    p5d2_promotion_confirmed_event_authorized
    automatic_publication_authorized
    background_observer_authorized
    polling_loop_authorized
    windows_startup_registration_authorized
    scheduled_task_authorized
    windows_service_authorized
    graph_search_current_semantics_authorized

## Remaining uncertainty

No local Python compilation or unittest execution has yet been observed for this P5-D3G contract candidate.

No P5-D3G runtime exists.

No sacrificial live-Vault transaction has been executed.

No real Vault write has been authorized or performed.

## Verdict

    STATIC CONTRACT REVIEW = PASS
    FUNCTIONAL CONTRACT CANDIDATE = READY FOR GOVERNED LOCAL RE-BREAK
    P5-D3G CONTRACT = UNQUALIFIED
    P5-D3G RUNTIME = CLOSED
    REAL VAULT WRITE = CLOSED

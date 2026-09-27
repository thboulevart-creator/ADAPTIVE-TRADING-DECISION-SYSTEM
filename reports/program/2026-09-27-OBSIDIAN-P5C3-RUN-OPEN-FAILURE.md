# OBSIDIAN P5-C3 — RUN-OPEN FAILURE

Date: 2026-09-27

## Candidate

Branch:

    feat/obsidian-projection-p5c3-obsidian-open-compatibility-v0.1

Executed HEAD:

    29d0787f4ba737077cd61ce65edda80238b21f0c

## User-reported control state

    Ran 543 tests in 10.688s
    OK
    P5C3_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    SNAPSHOT_FALLBACK=ONEDRIVE_CONTROL_COPY
    P5C3_OPEN_DIAGNOSTIC=PASS

All nine read-only precondition gates passed before mutation:

    CONTRACT                              PASS
    SNAPSHOT                              PASS
    SNAPSHOT_BINDING                      PASS
    SANDBOX_BOUNDARY                      PASS
    OBSIDIAN_PROCESS                      PASS
    OBSIDIAN_WORKSPACE_AND_PLUGIN_STATE   PASS
    LIVE_VAULT_DIGESTS                    PASS
    IMMUTABLE_GENERATIONS                 PASS
    CURRENT_POINTER                       PASS

## Instrumented RUN-OPEN result

    schema = ATDS_OBSIDIAN_P5C3_OPEN_METRICS_V0_1
    status = FAIL

    cycles_requested = 250
    cycles_completed = 8

    failure_phase = PROMOTION_LOOP
    failure_cycle = 8
    failure_code = PermissionError

    failure_message =
      [WinError 5] Accès refusé:
      CURRENT.tmp -> CURRENT.md

    pointer_write_error_count = 1

Reader observations:

    samples = 110
    samples_during_promotions = 110
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    partial_generation_count = 1
    parse_error_count = 0

Final logical pointer state:

    generation_id = GEN_A
    generation_tree_digest_sha256 =
      5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a

Postcondition gate:

    postcondition_failure_gate = null

Obsidian remained running and safe before/after:

    sync_enabled = false
    community_plugins_enabled = false
    workspace_references_current = true
    obsidian_subdirectory_count = 0

Reported:

    live_vault_modified = false
    obsidian_open_qualified = false
    p5c3_qualified = false
    production_promotion_authorized = false

Append-only event log:

    C:\Users\Boulevart\AppData\Local\ATDS\obsidian_projection\p5c3\open-events.jsonl

## Adjudication

**FAIL — the un-retried os.replace CURRENT.tmp -> CURRENT.md primitive is not qualified for promotion while CURRENT.md is open in Obsidian in this Windows/OneDrive environment.**

The failure is not attributable to a persistent precondition defect: all read-only gates passed immediately before RUN-OPEN.

Eight promotions succeeded before a Windows access-denied conflict occurred at cycle 8. This supports investigating a bounded sharing-conflict retry strategy, but does not itself establish that the conflict is transient or that retries are safe.

## Important interpretation

P5-C2 remains valid only for the filesystem primitive outside the Obsidian-open condition it tested.

P5-C3 demonstrates that the same primitive, without a retry policy, is insufficient for reliable Obsidian-open operation.

No further identical RUN-OPEN repetition is authorized.

## Next governed boundary

    P5-C3R — BOUNDED WINDOWS SHARING-CONFLICT RETRY CANDIDATE

The new candidate must preregister:

- retry only for PermissionError / WinError 5 from the atomic replace step;
- finite retry deadline;
- bounded backoff;
- exact attempt/conflict telemetry;
- temp-file integrity verification between attempts;
- zero terminal promotion failures;
- unchanged atomic replacement primitive;
- synthetic Windows sharing-lock breaker before the real open-Vault experiment;
- recovery of any stale CURRENT.tmp from the failed P5-C3 run before testing.

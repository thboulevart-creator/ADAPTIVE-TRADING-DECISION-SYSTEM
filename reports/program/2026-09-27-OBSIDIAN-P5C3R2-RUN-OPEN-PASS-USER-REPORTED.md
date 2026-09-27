# OBSIDIAN P5-C3R2 — RUN-OPEN PASS

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following runtime result was supplied from the user's Windows terminal.
It was not independently executed by the assistant.

## Runtime candidate

Exact runtime candidate executed:

    b5f3a8de061772e15bc94b20095d419130c20781

Branch:

    feat/obsidian-projection-p5c3r2-reader-eacces-retry-v0.1

Later commits on the branch are evidence-only and do not replace the tested runtime candidate.

## Automated open experiment

Schema:

    ATDS_OBSIDIAN_P5C3R2_OPEN_METRICS_V0_1

Status:

    PASS_AUTOMATED_OPEN_RETRY_EXPERIMENT

Completion:

    cycles_requested = 250
    cycles_completed = 250
    samples = 5002
    samples_during_promotions = 2239

Write-side telemetry:

    total_replace_attempts = 290
    access_denied_retry_conflict_count = 40
    max_retry_depth = 2
    max_promotion_latency_ms = 35.3073
    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    verification_read_access_denied_retry_count = 0

Reader telemetry:

    reader_access_denied_retry_count = 14
    reader_eacces_without_winerror_retry_count = 14
    reader_max_retry_depth = 1
    reader_terminal_access_error_count = 0

Semantic integrity:

    mixed_generation_count = 0
    missing_entrypoint_count = 0
    semantic_partial_generation_count = 0
    semantic_partial_signature_total_count = 0
    semantic_partial_signatures = {}
    parse_error_count = 0

Failure fields:

    failure_phase = null
    failure_cycle = null
    failure_type = null
    failure_message = null
    postcondition_failure_gate = null

Final state:

    final_generation_id = GEN_A
    final_generation_tree_digest_sha256 = 5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a
    live_vault_modified = false

Manual-gate fields:

    manual_visual_acceptance_required = true
    manual_visual_acceptance_pending = true

Qualification and authority:

    obsidian_open_retry_qualified = false
    p5c3r_qualified = false
    p5c3r2_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

Append-only event log:

    C:\Users\Boulevart\AppData\Local\ATDS\obsidian_projection\p5c3r2\retry-events.jsonl

## Adjudication

**P5-C3R2 AUTOMATED RUN-OPEN GATE: PASS on USER-REPORTED LOCAL EXECUTION evidence.**

The successor reader-only EACCES policy was actually exercised:

    reader_eacces_without_winerror_retry_count = 14

and all such reader access denials were absorbed within the bounded retry policy:

    reader_terminal_access_error_count = 0

The semantic anomaly counters remained zero:

    semantic_partial_generation_count = 0
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    parse_error_count = 0

The final pointer returned to GEN_A and no postcondition failure was reported.

## Scientific interpretation

This run supports the candidate hypothesis that the previously observed:

    PermissionError
    errno = 13
    winerror = None

reader failures can be treated as bounded transient reader access denials on this Windows/Obsidian environment.

It does not retroactively convert the failed P5-C3R runs into PASS.

P5-C3R remains unqualified.

P5-C3R2 is not yet fully qualified because the manual final visual acceptance and dedicated post-close gate remain outstanding.

## Next required gates

1. Keep Obsidian open.
2. Perform final manual visual acceptance of CURRENT.md.
3. Confirm final visible generation GEN_A.
4. Only after that, close Obsidian fully.
5. Execute dedicated P5-C3R2 post-close verification.
6. Adjudicate P5-C3R2 qualification only if post-close passes.

## Preserved non-authorizations

    p5c3r_qualified = false
    p5c3r2_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

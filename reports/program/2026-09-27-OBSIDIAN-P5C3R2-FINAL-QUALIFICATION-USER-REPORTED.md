# OBSIDIAN P5-C3R2 — FINAL QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION + USER-PROVIDED VISUAL EVIDENCE**

The Windows runtime results and visual confirmations were supplied by the user.
The assistant did not independently execute the local Obsidian experiments.

## Runtime candidate

Exact runtime candidate qualified:

    b5f3a8de061772e15bc94b20095d419130c20781

Branch:

    feat/obsidian-projection-p5c3r2-reader-eacces-retry-v0.1

Later branch commits contain evidence-only reports and do not replace the qualified runtime candidate.

## Qualification chain

### 1. Local re-break

Reported:

    Ran 618 tests in 10.822s
    OK
    P5C3R2_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS
    P5C3R2_SYNTHETIC_LOCK_BREAKER=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5C3R2_LOCAL_REBREAK_COMPLETED=PASS

Synthetic Windows lock breaker:

    access_denied_conflicts = 5
    attempts = 6
    final_generation = GEN_B
    stale_temp_present = false

### 2. Pre-run visual confirmation

User-provided screenshot showed:

    CURRENT open in Obsidian
    generation_id = GEN_A
    Active generation: GEN_A
    generation_tree_digest_sha256 =
    5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a

### 3. Governed RUN-OPEN

Reported schema:

    ATDS_OBSIDIAN_P5C3R2_OPEN_METRICS_V0_1

Reported status:

    PASS_AUTOMATED_OPEN_RETRY_EXPERIMENT

Completion:

    cycles_requested = 250
    cycles_completed = 250
    samples = 5002
    samples_during_promotions = 2239

Write side:

    access_denied_retry_conflict_count = 40
    total_replace_attempts = 290
    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    verification_read_access_denied_retry_count = 0

Reader side:

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

Final state:

    final_generation_id = GEN_A
    final_generation_tree_digest_sha256 =
    5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a
    postcondition_failure_gate = null
    live_vault_modified = false

The successor reader-only EACCES path was actually exercised:

    reader_eacces_without_winerror_retry_count = 14

with no terminal reader error and no semantic-partial observation.

### 4. Final manual visual acceptance

User-provided post-run screenshot showed:

    CURRENT open
    generation_id = GEN_A
    Active generation: GEN_A
    same visible generation tree digest
    Open active generation link visible

The screenshot did not expose the internal hyperlink target; no stronger visual claim is made.

### 5. Dedicated P5-C3R2 POST-CLOSE

Reported preconditions:

    RUNTIME_HEAD=b5f3a8de061772e15bc94b20095d419130c20781
    OBSIDIAN_PROCESS=CLOSED
    POST_CLOSE_RUNNER_BLOB=PASS
    CONTROL_CLONE_CLEAN=PASS

Snapshot fallback:

    SNAPSHOT_FALLBACK=ONEDRIVE_CONTROL_COPY

Reported schema:

    ATDS_OBSIDIAN_P5C3R2_POST_CLOSE_REPORT_V0_1

Reported status:

    PASS

Reported final state:

    final_generation_id = GEN_A
    manual_visual_acceptance = true
    live_vault_modified = false
    reader_access_denied_retry_count = 0
    reader_eacces_without_winerror_retry_count = 0

Qualification identity:

    obsidian_open_retry_qualified = true
    p5c3r_qualified = false
    p5c3r2_qualified = true

Authority boundaries:

    production_promotion_authorized = false
    continuous_observer_authorized = false
    graph_current_pointer_semantics_qualified = false

Runner result:

    P5C3R2_POST_CLOSE=PASS
    P5C3R2_POST_CLOSE_EXIT_CODE=0
    P5C3R2_GOVERNED_POST_CLOSE=PASS

## Final adjudication

**P5-C3R2 QUALIFICATION = PASS on USER-REPORTED LOCAL EXECUTION and USER-PROVIDED VISUAL EVIDENCE.**

The qualified result is specifically the bounded reader-only handling of:

    PermissionError
    winerror is None
    errno == EACCES (13)

while preserving the write-side retry boundary:

    PermissionError
    winerror in {5, 32}

The previously failed P5-C3R candidate is not retroactively qualified.

    p5c3r_qualified = false
    p5c3r2_qualified = true

## What is now established

Within the tested sacrificial Windows/OneDrive/Obsidian environment:

- the immutable-generation model remained intact;
- CURRENT.md atomic publication completed across 250 promotions;
- write-side sharing conflicts were absorbed within the bounded policy;
- the observed reader-only EACCES failures were absorbed within the 500 ms reader policy;
- no mixed, missing, semantic-partial, parse, terminal-reader, terminal-write, or retry-deadline anomaly remained in the qualifying run;
- the final visible and post-close generation was GEN_A;
- the real live Vault boundary remained unmodified according to the reported checks.

## What is not authorized

Qualification of P5-C3R2 does NOT authorize:

    production promotion
    continuous observer
    native Obsidian Graph/Search CURRENT-generation semantics

Those remain separate governed phases.

## Next governed frontier

The next candidate frontier is:

    P5-D CONTINUOUS OBSERVER IMPLEMENTATION CANDIDATE

P5-D must start from the qualified P5-C3R2 result without reopening or weakening the completed P5-C3R2 gates.

Graph/Search semantics remain deferred to:

    P6 CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

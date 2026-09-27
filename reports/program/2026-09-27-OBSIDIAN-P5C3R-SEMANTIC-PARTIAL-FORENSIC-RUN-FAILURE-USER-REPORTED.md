# OBSIDIAN P5-C3R — SEMANTIC PARTIAL FORENSIC RUN FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following runtime result was supplied from the user's Windows terminal.
It is not independently executed or independently validated by the assistant.

## Runtime candidate

Exact forensic runtime HEAD:

    2cd17fe24668a276efda490c9102e423d9de70b8

Branch:

    feat/obsidian-projection-p5c3r-semantic-partial-forensics-v0.1

## Precheck

The read-only precheck reported PASS for:

    CONTRACT
    SNAPSHOT
    SNAPSHOT_BINDING
    SANDBOX_BOUNDARY
    OBSIDIAN_PROCESS
    OBSIDIAN_WORKSPACE_AND_PLUGIN_STATE
    LIVE_VAULT_DIGESTS
    IMMUTABLE_GENERATIONS
    CURRENT_POINTER

Starting CURRENT:

    generation_id = GEN_A
    current_sha256 = 2b9cc5f94d5dbb18978f1642e2bbf47121deab6d825cbbb9d617b67d294f2daa
    generation_tree_digest_sha256 = 5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a

## Forensic run result

Schema:

    ATDS_OBSIDIAN_P5C3R_OPEN_METRICS_V0_1

Status:

    FAIL

Completion:

    cycles_requested = 250
    cycles_completed = 250
    samples = 5008
    samples_during_promotions = 2348

Pointer replacement:

    total_replace_attempts = 297
    access_denied_retry_conflict_count = 47
    max_retry_depth = 3
    max_promotion_latency_ms = 77.8831
    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    verification_read_access_denied_retry_count = 0

Reader:

    reader_access_denied_retry_count = 0
    reader_terminal_access_error_count = 0
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    semantic_partial_generation_count = 12
    semantic_partial_signature_total_count = 12
    parse_error_count = 0

Exact semantic-partial attribution:

    message=CURRENT.md unreadable|cause_type=PermissionError|errno=13|winerror=None
    count = 12

Final state:

    final_generation_id = GEN_A
    final_generation_tree_digest_sha256 = 5d250c1c42e6193b3442d4a62fc4a842f12f22982e5ce7f11289b443acd76f3a
    postcondition_failure_gate = null
    live_vault_modified = false

## Adjudication

**FORENSIC RUN = FAIL.**

The pre-registered P5-C3R criterion still requires:

    semantic_partial_generation_count = 0

Observed:

    semantic_partial_generation_count = 12

Therefore this run cannot qualify P5-C3R.

## What the instrumentation established

All 12 semantic-partial observations had the same top-level path:

    CURRENT.md unreadable

All 12 had the same immediate cause class:

    PermissionError

All 12 carried:

    errno = 13
    winerror = None

The run did not observe semantic-partial signatures for malformed frontmatter, wrong schema, wrong digest, unreadable target manifest, or missing target INDEX.

The current reader retry classifier only accepts underlying PermissionError where:

    winerror in {5, 32}

Therefore these 12 PermissionError(errno=13, winerror=None) observations were not retried and were counted as semantic partials.

## Interpretation boundary

This evidence supports the conclusion that the observed failures were read-access failures of CURRENT.md rather than demonstrated semantic content corruption.

It does not by itself authorize treating every errno=13 as retryable.

Any reader-policy change must be separately preregistered and tested.

The write-side os.replace policy remains unchanged and is not implicated by this finding.

## Next governed candidate

A successor reader-only candidate may test a narrowly scoped classification:

    PermissionError
    AND winerror is None
    AND errno == EACCES (13)

as retryable reader access denial.

The write-side retry policy remains exactly:

    winerror in {5, 32}

No generic errno=13 write retry is authorized.

## Non-authorizations

    p5c3r_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

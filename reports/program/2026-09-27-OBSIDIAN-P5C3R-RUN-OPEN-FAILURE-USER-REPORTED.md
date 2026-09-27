# OBSIDIAN P5-C3R — RUN-OPEN FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following result was supplied from the user's Windows terminal.
It is not an independently executed or independently validated runtime result.

## Runtime candidate

Branch used for development:

    feat/obsidian-projection-p5c3r-access-denied-retry-v0.1

Exact runtime candidate executed:

    ae7d1adbb146fffb60c4e302750abb896136d968

Later branch commits contained evidence-only reports and did not replace the runtime candidate for this experiment.

## Reported experiment result

Schema:

    ATDS_OBSIDIAN_P5C3R_OPEN_METRICS_V0_1

Status:

    FAIL

Core completion:

    cycles_requested = 250
    cycles_completed = 250
    samples = 5004
    samples_during_promotions = 2362

Pointer-replacement telemetry:

    total_replace_attempts = 301
    access_denied_retry_conflict_count = 51
    max_retry_depth = 2
    max_promotion_latency_ms = 35.5968
    terminal_pointer_write_error_count = 0
    retry_deadline_exceeded_count = 0
    verification_read_access_denied_retry_count = 0

Reader outcomes:

    reader_access_denied_retry_count = 0
    reader_terminal_access_error_count = 0
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    semantic_partial_generation_count = 19
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

Authorization fields:

    obsidian_open_retry_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

## Adjudication

**P5-C3R RUN-OPEN = FAIL.**

The failure is caused by violation of the pre-registered semantic criterion:

    semantic_partial_generation_count_must_equal = 0

Observed:

    semantic_partial_generation_count = 19

The retry candidate therefore cannot be qualified from this run.

The 51 Windows sharing conflicts were absorbed without terminal pointer-write error or retry-deadline exhaustion. They are not themselves the terminal failing criterion.

## Post-failure read-only state

A subsequent user-reported read-only diagnostic showed:

    HEAD = ae7d1adbb146fffb60c4e302750abb896136d968
    Obsidian process = RUNNING
    git status count = 0
    CURRENT.md exists = true
    CURRENT.tmp exists = false
    CURRENT generation = GEN_A
    all P5-C3 read-only diagnostic gates = PASS
    diagnostic mutation_performed = false

Therefore no recovery mutation is authorized solely from this failure record.

## Unresolved cause

The runtime report counts 19 OpenPointerPartialError observations but does not retain their exact messages or underlying exception causes.

The current validator can produce OpenPointerPartialError for multiple distinct paths, including:

- CURRENT.md read/unicode failure;
- malformed or incomplete CURRENT frontmatter;
- schema/generation/digest problems;
- target MANIFEST read/parse failure;
- missing target INDEX.

Some read failures may themselves wrap transient Windows/OSError conditions.

No specific cause is adjudicated from the existing evidence.

## Next authorized scope

Do not repeat the identical RUN-OPEN.

Authorized next work is a forensic instrumentation candidate that:

- preserves retry policy exactly {WinError 5, WinError 32};
- preserves the atomic publication primitive;
- preserves immutable generations;
- records bounded signatures for every semantic OpenPointerPartialError;
- records top-level message, immediate cause type, errno and winerror where present;
- does not reinterpret or suppress semantic failures;
- is re-broken before any further Obsidian-open run.

## Non-authorizations

    p5c3r_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

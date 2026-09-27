# OBSIDIAN P5-C3R2 — READER-ONLY EACCES RETRY V0.1

Date: 2026-09-27

## Why P5-C3R2 exists

The first P5-C3R RUN-OPEN completed all 250 promotions but failed because:

    semantic_partial_generation_count = 19

A forensic successor then repeated the experiment with causal attribution and observed:

    cycles_completed = 250
    semantic_partial_generation_count = 12
    semantic_partial_signature_total_count = 12

All 12 signatures were identical:

    message=CURRENT.md unreadable
    cause_type=PermissionError
    errno=13
    winerror=None

No semantic-partial signature was observed for malformed CURRENT content, wrong schema, wrong generation, wrong digest, unreadable target manifest, or missing target INDEX.

The observed failure class is therefore a CURRENT.md read-access failure, not demonstrated semantic content corruption.

## Scientific boundary

The forensic run remains FAIL.

P5-C3R is not retroactively qualified.

P5-C3R2 is a new candidate with a separately preregistered reader policy.

## Write policy — unchanged

The atomic publication operation remains:

    os.replace(CURRENT.tmp, CURRENT.md)

Write-side retry remains limited to PermissionError with:

    winerror in {5, 32}

The following is explicitly forbidden on the write side:

    PermissionError
    winerror = None
    errno = EACCES

Write retry bounds remain:

    deadline = 5000 ms
    initial backoff = 10 ms
    multiplier = 2
    maximum backoff = 500 ms

CURRENT.tmp remains write-once before the replace loop.

## Reader policy — narrow successor

Reader retry accepts only PermissionError satisfying either:

    winerror in {5, 32}

or:

    winerror is None
    errno == EACCES
    errno numeric value == 13

The EACCES fallback is reader-only.

It is forbidden for:

- non-PermissionError with errno EACCES;
- PermissionError EACCES with a non-null WinError outside {5,32};
- unrelated PermissionError errno values;
- semantic OpenPointerPartialError without an access-denied cause.

Reader retry bounds remain:

    deadline = 500 ms
    initial backoff = 5 ms
    multiplier = 2
    maximum backoff = 50 ms

A permanent access denial therefore remains terminal after the bounded deadline.

## Qualification criteria — unchanged

The real open-Vault experiment still requires:

    250 promotions
    >= 5000 reader samples
    >= 1 fresh reader sample per promotion
    initial GEN_A
    final GEN_A

Required zero outcomes remain:

    terminal pointer write errors = 0
    retry deadline exceeded = 0
    mixed generation = 0
    missing entrypoint = 0
    semantic partial generation = 0
    parse errors = 0
    terminal reader access errors = 0

A non-zero EACCES retry count is allowed and must be telemetried.

## New telemetry

The report must expose:

    reader_access_denied_retry_count
    reader_eacces_without_winerror_retry_count

The forensic fields remain:

    semantic_partial_signature_total_count
    semantic_partial_signatures

This allows the successor run to demonstrate whether the exact failure observed previously was absorbed by the reader-only policy.

## Runtime evidence separation

P5-C3R2 uses:

    schema:
    ATDS_OBSIDIAN_P5C3R2_OPEN_METRICS_V0_1

    synthetic lock schema:
    ATDS_OBSIDIAN_P5C3R2_SYNTHETIC_LOCK_BREAKER_V0_1

    post-close schema:
    ATDS_OBSIDIAN_P5C3R2_POST_CLOSE_REPORT_V0_1

    event log namespace:
    %LOCALAPPDATA%\ATDS\obsidian_projection\p5c3r2\retry-events.jsonl

Dedicated CLI:

    tools.obsidian_projection.p5c3r2_verify

Dedicated runners:

    tools/obsidian_projection/run_p5c3r2_open.ps1
    tools/obsidian_projection/run_p5c3r2_post_close.ps1

The predecessor P5-C3R runners remain byte-identical.

## Qualification identity

Even if P5-C3R2 eventually passes all gates:

    p5c3r_qualified = false
    p5c3r2_qualified = true

Production promotion remains unauthorized.

Continuous observer remains unauthorized.

Native Obsidian Graph/Search CURRENT-generation semantics remain deferred to P6.

## Required sequence

Before any P5-C3R2 open run:

1. close Obsidian;
2. checkout exact persisted P5-C3R2 candidate;
3. targeted tests including V0.2 contract;
4. full Obsidian suite;
5. clean working tree;
6. synthetic Windows lock breaker;
7. read-only state verification;
8. reopen the same sacrificial Vault;
9. open CURRENT.md and confirm GEN_A;
10. run P5-C3R2 open experiment.

If automated open passes:

11. manual visual final acceptance;
12. fully close Obsidian;
13. run dedicated P5-C3R2 post-close;
14. only then adjudicate P5-C3R2 qualification.

## Non-authorizations

    production_promotion_authorized = false
    continuous_observer_authorized = false
    native_graph_current_pointer_semantics_qualified = false

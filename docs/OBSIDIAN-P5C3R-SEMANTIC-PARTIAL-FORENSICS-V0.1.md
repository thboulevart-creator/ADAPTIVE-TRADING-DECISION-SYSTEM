# OBSIDIAN P5-C3R — SEMANTIC PARTIAL FORENSICS V0.1

Date: 2026-09-27

## Purpose

This forensic subphase exists because the first P5-C3R RUN-OPEN completed all 250 promotions but reported:

    semantic_partial_generation_count = 19

The retry candidate therefore failed its pre-registered criterion.

The cause of those 19 observations was not retained by the original runtime telemetry.

## Scope

This candidate changes telemetry only.

It does NOT change:

- retryable WinErrors;
- retry deadlines;
- retry backoff;
- atomic publication primitive;
- immutable-generation model;
- CURRENT.tmp write-once rule;
- PASS/FAIL criteria;
- sandbox boundary;
- production authorization;
- continuous-observer authorization.

Retryable Windows sharing conflicts remain exactly:

    {5, 32}

Semantic partial observations remain terminal qualification failures.

## Forensic attribution

Each OpenPointerPartialError observed by the reader is assigned a bounded signature containing:

    top-level OpenPointerPartialError message
    immediate cause type
    immediate cause errno
    immediate cause winerror

Example:

    message=CURRENT.md unreadable
    cause_type=FileNotFoundError
    errno=2
    winerror=None

The exact observed environment may produce different errno/winerror values.

No cause is reclassified by this instrumentation.

## Accounting

The report gains:

    semantic_partial_signature_total_count
    semantic_partial_signatures

Required accounting invariant:

    semantic_partial_signature_total_count
    ==
    semantic_partial_generation_count

when every semantic partial was recorded by the reader.

A non-zero semantic partial count still forces FAIL.

## Hypotheses to discriminate

The first failed run does not establish which hypothesis is true.

Candidate hypotheses include:

H1 — genuine semantic corruption of CURRENT.md.

H2 — transient read failure of CURRENT.md wrapped as OpenPointerPartialError.

H3 — transient target-manifest access failure.

H4 — transient path-observation race such as FileNotFoundError during atomic replacement.

H5 — another OSError/Unicode/parse failure not covered by the existing sharing-conflict retry policy.

No hypothesis is accepted before runtime evidence identifies the actual signature(s).

## Required breakers before forensic rerun

The candidate must demonstrate locally that:

- existing WinError 5 retry behavior remains;
- existing WinError 32 retry behavior remains;
- unrelated WinErrors remain non-retryable;
- a synthetic semantic partial remains counted as semantic;
- that synthetic semantic partial produces one forensic signature;
- access-denied retry telemetry is not incremented by that semantic fixture;
- existing P5-C3R adversarial breakers still pass;
- full Obsidian suite still passes;
- working tree remains clean.

## Runtime rule

The next Obsidian-open execution is diagnostic, not a qualification rerun.

Its purpose is to identify the signatures underlying semantic partial observations.

If semantic partial count is again non-zero, the result remains FAIL even if the cause appears operationally transient.

A later policy change, such as adding another retryable Windows error, would require separate evidence, preregistration, breakers, and adjudication.

## Non-authorizations

    p5c3r_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

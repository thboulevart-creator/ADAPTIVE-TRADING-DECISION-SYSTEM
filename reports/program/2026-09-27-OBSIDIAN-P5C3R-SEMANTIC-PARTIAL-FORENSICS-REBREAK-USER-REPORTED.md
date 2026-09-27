# OBSIDIAN P5-C3R — SEMANTIC PARTIAL FORENSICS RE-BREAK

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following results were supplied from the user's Windows terminal.
They are not independently executed or independently validated runtime results.

## Candidate

Branch:

    feat/obsidian-projection-p5c3r-semantic-partial-forensics-v0.1

Exact candidate tested:

    2cd17fe24668a276efda490c9102e423d9de70b8

## Reported full re-break

Terminal result:

    Ran 592 tests in 10.691s
    OK
    FORENSIC_FULL_REBREAK=PASS

The initial clean-tree gate then blocked because py_compile/test execution created only:

    ?? tests/obsidian_projection/__pycache__/
    ?? tools/obsidian_projection/__pycache__/

No tracked-file modification was reported.

## Controlled cleanup

A follow-up cleanup guard checked that the only untracked entries were exactly the two expected __pycache__ directories.

The cleanup then removed those generated cache directories only.

Reported result:

    FORENSIC_HEAD=2cd17fe24668a276efda490c9102e423d9de70b8
    FORENSIC_592_TESTS=USER_REPORTED_PASS
    GENERATED_PYCACHE_REMOVED=PASS
    CONTROL_CLONE_CLEAN=PASS
    FORENSIC_REBREAK_COMPLETED=PASS

## Adjudication

**FORENSIC RE-BREAK GATE: PASS on USER-REPORTED LOCAL EXECUTION evidence.**

The forensic candidate is therefore eligible for the next governed diagnostic Obsidian-open run.

This does not qualify P5-C3R.

The purpose of the next run is causal attribution of semantic partial observations only.

## Preserved boundaries

The candidate still preserves:

    retryable WinErrors = {5, 32}
    semantic_partial_generation_count > 0 => FAIL
    production_promotion_authorized = false
    continuous_observer_authorized = false

The prior P5-C3R RUN-OPEN failure remains authoritative.

No retry expansion has been authorized.

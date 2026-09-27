# OBSIDIAN P5-C3R2 — LOCAL RE-BREAK

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following Windows execution results were supplied by the user.
They were not independently executed by the assistant.

## Candidate

Branch:

    feat/obsidian-projection-p5c3r2-reader-eacces-retry-v0.1

Exact runtime candidate tested:

    b5f3a8de061772e15bc94b20095d419130c20781

## Full re-break

Reported result:

    Ran 618 tests in 10.822s
    OK
    P5C3R2_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

Interpretation:

- the reported full Obsidian suite passed;
- the control checkout remained clean after the suite.

## Synthetic Windows lock breaker

Reported result:

    schema = ATDS_OBSIDIAN_P5C3R2_SYNTHETIC_LOCK_BREAKER_V0_1
    status = PASS
    lock_release_delay_ms = 200
    attempts = 6
    access_denied_conflicts = 5
    elapsed_ms = 328.043099
    max_backoff_ms = 160.0
    verification_read_access_denied_retries = 0
    final_generation = GEN_B
    stale_temp_present = false
    production_promotion_authorized = false

Interpretation:

- the write-side bounded retry still absorbed real Windows sharing conflicts;
- at least one retry conflict was observed;
- the synthetic lock breaker completed successfully;
- no stale CURRENT.tmp remained.

## Final clean-tree gate

Reported result:

    CONTROL_CLONE_CLEAN=PASS
    P5C3R2_LOCAL_REBREAK_COMPLETED=PASS

## Adjudication

**P5-C3R2 LOCAL RE-BREAK GATE: PASS on USER-REPORTED LOCAL EXECUTION evidence.**

This does not qualify P5-C3R2.

Still required:

1. manually reopen the same sacrificial Obsidian Vault;
2. open CURRENT.md and confirm GEN_A;
3. leave Obsidian open;
4. execute the dedicated P5-C3R2 open experiment;
5. adjudicate automated metrics, including reader_eacces_without_winerror_retry_count;
6. if automated PASS, perform manual final visual acceptance;
7. close Obsidian completely;
8. run dedicated P5-C3R2 post-close.

## Preserved non-authorizations

    p5c3r_qualified = false
    p5c3r2_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

# OBSIDIAN P5-C3R — RECOVERY CONTROL

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

These results were supplied from the user's Windows terminal.
They are not independently executed or independently validated by the assistant.

## Candidate

Branch:

    feat/obsidian-projection-p5c3r-access-denied-retry-v0.1

Persisted candidate HEAD executed:

    ae7d1adbb146fffb60c4e302750abb896136d968

Static-review predecessor at execution time:

    ae7d1adbb146fffb60c4e302750abb896136d968

## Full Obsidian re-break

Reported terminal result:

    Ran 588 tests in 11.379s
    OK
    P5C3R_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS

Interpretation:

- the reported full Obsidian test suite passed;
- the reported control checkout remained clean after the suite.

No claim of independent execution is made.

## Synthetic Windows sharing-lock breaker

Reported result:

    schema = ATDS_OBSIDIAN_P5C3R_SYNTHETIC_LOCK_BREAKER_V0_1
    status = PASS
    lock_release_delay_ms = 200
    attempts = 6
    access_denied_conflicts = 5
    elapsed_ms = 328.5795
    max_backoff_ms = 160.0
    verification_read_access_denied_retries = 0
    final_generation = GEN_B
    stale_temp_present = false
    production_promotion_authorized = false

Interpretation:

- at least one real Windows sharing conflict was observed;
- five retryable conflicts were reported;
- the bounded retry eventually completed;
- the final pointer selected GEN_B;
- no stale CURRENT.tmp remained.

This supports the synthetic-breaker gate only.

## Snapshot fallback

The primary LocalAppData snapshot was not used.
The runner reported:

    SNAPSHOT_FALLBACK=ONEDRIVE_CONTROL_COPY

The recovery therefore used the governed OneDrive control copy.

Snapshot token:

    bf2b9a1e817b35abdb550375970f21f84fd65de56590abf925aec329b0468b3b

## Failed P5-C3 state recovery

Reported result:

    schema = ATDS_OBSIDIAN_P5C3R_RECOVERY_REPORT_V0_1
    status = PASS
    current_generation = GEN_A
    stale_temp_action = VERIFIED_AND_REMOVED
    generation_rebuild_performed = false
    reader_access_denied_retry_count = 0
    live_vault_modified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

Sandbox:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX

Append-only event log:

    C:\Users\Boulevart\AppData\Local\ATDS\obsidian_projection\p5c3r\retry-events.jsonl

Interpretation:

- recovery returned the failed P5-C3 sandbox to the required GEN_A starting state;
- the surviving CURRENT.tmp was accepted only after exact expected-byte verification, then removed;
- generations were not rebuilt;
- the real Vault was reported unchanged;
- no production or continuous-observer authority was granted.

## Gate adjudication

**RECOVERY CONTROL GATE: PASS on USER-REPORTED LOCAL EXECUTION evidence.**

This does not qualify P5-C3R.

Still required:

1. manually open the same sacrificial sandbox in Obsidian;
2. open CURRENT.md;
3. confirm visually that CURRENT.md shows GEN_A and the GEN_A link;
4. keep Obsidian open;
5. run the governed P5-C3R open experiment;
6. if automated open experiment passes, perform manual visual acceptance;
7. close Obsidian;
8. run P5-C3R POST-CLOSE.

## Non-authorizations

    p5c3r_qualified = false
    production_promotion_authorized = false
    continuous_observer_authorized = false

The native Obsidian Graph/Search CURRENT-generation indexing problem remains deferred to P6.

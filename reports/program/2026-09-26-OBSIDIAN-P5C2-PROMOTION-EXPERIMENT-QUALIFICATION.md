# OBSIDIAN P5-C2 — PROMOTION EXPERIMENT QUALIFICATION

Date: 2026-09-26

## Scope

This record closes P5-C2, the empirical Windows/OneDrive filesystem-promotion experiment executed only against the sacrificial sandbox.

## Persisted candidate

Branch:

    feat/obsidian-projection-p5c2-promotion-experiment-harness-v0.1

Persisted candidate HEAD:

    6ef02ce03ef6826e3f805ea6a8c2f00460844f66

Qualified predecessor P5-C:

    0a649ec676d0b4ef7331f008a8701beecd14bf5d

## User-reported local execution

The user reported:

    Ran 467 tests in 8.945s
    OK

    P5C2_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5C2_PREFLIGHT=PASS
    P5C2_EXPERIMENT_EXECUTION_PASS

The sandbox experiment produced:

    schema = ATDS_OBSIDIAN_P5C_PROMOTION_METRICS_V0_1
    status = PASS
    adjudication = ONE_CANDIDATE_QUALIFIED

This is USER-REPORTED LOCAL EXECUTION, not independent execution evidence.

## Environment

    Windows-11-10.0.22631-SP0
    NTFS
    Python 3.13.14
    sandbox:
      C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C-PROMOTION-SANDBOX

Observed sandbox reparse state:

    attributes_hex = 0x00000031
    is_reparse_point = false
    is_symlink = false

The qualification is bounded to this tested environment and does not generalize automatically to other Windows, filesystem, OneDrive, or provider conditions.

## Protected live Vault evidence

Live Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

Before/after byte-tree digests were identical.

generated/:

    before =
    46a8959efbf7ead73c8d79b3dd6268df94aa9176d5ca76721d7ad5f484217088

    after =
    46a8959efbf7ead73c8d79b3dd6268df94aa9176d5ca76721d7ad5f484217088

views/:

    before =
    853e08b68f92a86ca4cdc8d91c78448debc87d631467c9b4daefecbea7fbd4bb

    after =
    853e08b68f92a86ca4cdc8d91c78448debc87d631467c9b4daefecbea7fbd4bb

Reported:

    live_vault_modified = false

## Negative control

Candidate:

    DIRECT_IN_PLACE_PER_FILE_REPLACE

Role:

    NEGATIVE_CONTROL
    qualification_allowed = false

Result:

    result = PASS

Meaning:

The control PASS means the breaker succeeded in demonstrating non-atomic visibility.

Observed:

    cycles_completed = 24 / 24
    samples = 4377
    samples_during_promotions = 4376

    mixed_generation_count = 0
    missing_entrypoint_count = 0
    partial_generation_count = 4375
    parse_error_count = 0

This validates that the concurrent reader was capable of detecting non-atomic live state.

It does not qualify direct per-file replacement.

## Candidate 1 — directory two-rename swap

    DIRECTORY_TWO_RENAME_SWAP

Result:

    FAIL

Observed:

    cycles_completed = 0 / 250
    failure_code = PermissionError
    samples = 1

No qualification claim is permitted.

## Candidate 2 — MoveFileEx directory replacement

    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE

Result:

    NOT_SUPPORTED

Observed:

    cycles_completed = 0 / 250
    failure_code = MOVEFILEEX_ERROR_5
    samples = 1

No qualification claim is permitted.

## Candidate 3 — immutable generation + atomic pointer

    IMMUTABLE_GENERATION_ATOMIC_POINTER

Result:

    PASS
    qualifies_primitive = true

Observed:

    cycles_completed = 250 / 250
    samples = 5001
    samples_during_promotions = 250

Reader anomalies:

    mixed_generation_count = 0
    missing_entrypoint_count = 0
    partial_generation_count = 0
    parse_error_count = 0

Final generation:

    GEN_A

Final tree digest:

    9472aac1da28674d28964ead6b51d1a6cda95184adc63239a4eca7065492a701

The candidate therefore satisfied the preregistered filesystem visibility conditions for this environment.

## Crash recovery probe

The selected pointer primitive also passed the bounded recovery probe:

    before_promotion = PASS
    after_first_mutation_step_if_multi_step =
      NOT_APPLICABLE_SINGLE_STEP
    after_promotion_before_state_record = PASS

    last_known_good_identifiable = true
    recovery_deterministic = true

Recovered generation:

    GEN_B

Recovered tree digest:

    42414edd11ceaf657795772c7bbbdf91788ad88607300422419dda45ca06b00f

## Selected filesystem primitive

Exactly one filesystem candidate qualified:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

This is the only selected primitive for subsequent bounded work.

The two directory-replacement approaches are not fallbacks unless separately redesigned and requalified.

## Important architectural interpretation

This result qualifies a **filesystem publication primitive**, not the complete future Obsidian visual architecture.

The selected model is:

    immutable complete generation directories
        +
    one atomically replaced CURRENT pointer

A later machine-managed visual layer must define how Obsidian follows this pointer without exposing stale duplicate generations in Graph/Search or confusing human navigation.

The pointer result therefore does not authorize simply placing multiple complete generations into ordinary searchable note namespaces.

## Non-authorizations preserved

The experiment explicitly reported:

    obsidian_open_qualified = false
    production_promotion_authorized = false

Therefore P5-C2 does NOT authorize:

- promotion while the real Vault is open in Obsidian;
- continuous production synchronization;
- Windows startup/service/task registration;
- live machine-view replacement;
- automatic human-view overwrite.

## Verdict

**PASS — P5-C2 FILESYSTEM PROMOTION PRIMITIVE QUALIFIED**

Selected primitive:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

Rejected / unsupported in the tested environment:

    DIRECTORY_TWO_RENAME_SWAP
      = FAIL / PermissionError

    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE
      = NOT_SUPPORTED / MOVEFILEEX_ERROR_5

## Next governed boundary

The next logical boundary is:

    P5-C3 — OBSIDIAN-OPEN SANDBOX COMPATIBILITY QUALIFICATION

P5-C3 must test the selected immutable-generation atomic-pointer primitive while a sacrificial sandbox Vault is actually open in Obsidian.

It must not use the real user Vault.

Only after that boundary can the continuous observer implementation be considered for production-oriented end-to-end qualification.

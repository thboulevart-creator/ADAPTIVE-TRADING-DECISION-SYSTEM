# OBSIDIAN P5-D3F — PERSISTENT REAL EXECUTION WINERROR-5 INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL REAL-EXECUTION ATTEMPT.

The governed entrypoint was reached.

## Observed output

    P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS
    P5D3F_PERSISTENT_STAGING_PRESTATE=ABSENT
    BLOCKED: PermissionError: [WinError 5] Access denied:
    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING
    EXIT_CODE=2

## Adjudication

Unlike the earlier import-mode failure, this attempt entered the governed real-execution path.

No PASS handoff result was emitted.
No RESULT_JSON was emitted.
No REAL_VAULT_ZERO_MUTATION=PASS marker was emitted.
No completion marker was emitted.

Therefore:

    PERSISTENT HANDOFF REAL EXECUTION = NOT QUALIFIED
    SUCCESS = NOT ESTABLISHED
    AUTHORIZATION MAY NOT BE SILENTLY REUSED
    RETRY = FORBIDDEN PENDING RESIDUAL AUDIT

## Static error-path finding

The real runner wraps execute_persistent_production_handoff in an exception handler and then invokes:

    _cleanup_empty_staging_after_failure(staging, prestate)

For an original prestate of ABSENT, that cleanup may execute:

    staging.rmdir()

The cleanup routine does not wrap OSError/PermissionError at that rmdir call.

Therefore the reported PermissionError on the exact staging path can be a cleanup failure that replaced the original execution exception.

The observed PermissionError alone does NOT prove that staging.mkdir was the failing operation.

The original inner failure may have been masked.

## Required immediate boundary

READ-ONLY audit only.

Determine whether the exact staging path is:

- absent;
- present and empty;
- present with an empty packages directory;
- present with nonempty residual evidence.

Also search for PROMOTION-HANDOFF.json.

Do not delete, create, rename or retry anything.

If staging is nonempty, preserve all evidence.

If staging is absent or empty, the execution runner still requires correction so a future failure preserves the original exception and handles cleanup failures explicitly before any retry can be authorized.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.

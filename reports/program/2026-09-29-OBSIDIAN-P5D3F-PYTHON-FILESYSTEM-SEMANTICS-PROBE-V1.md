# OBSIDIAN P5-D3F — PYTHON FILESYSTEM SEMANTICS PROBE V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY PYTHON PROBE.

No mutation was performed by the probe.

## Exact paths probed

- C:\Users\Boulevart\OneDrive\Bureau\ATDS
- C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING
- C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

## Python observations

For all three paths:

    exists = true
    is_dir = true
    is_symlink = false
    os.path.isjunction = false
    implementation _is_alias = false
    _assert_alias_free_chain = PASS
    resolve(strict=True) = PASS

Observed Python st_file_attributes:

    49

Observed stat.FILE_ATTRIBUTE_REPARSE_POINT:

    1024

Therefore:

    reparse_bit_set = false

for all three paths.

## Governed helper observations

    validate_persistent_paths = PASS

Resolved staging:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

Resolved real Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

    validate_staging_prestate = PRESENT_EMPTY

Probe exit code:

    0

## Adjudication

The PowerShell Mode/Attributes presentation observed earlier must not be treated as evidence that the governed Python implementation sees these paths as reparse aliases.

Using the exact Python primitives used by the implementation:

    alias / reparse guard = PASS
    staging prestate = PRESENT_EMPTY

Therefore the current blocker is NOT the implementation's alias/reparse guard.

The prior WinError 5 remains attributable to the failure-cleanup path unless and until an original inner exception is recovered. The cleanup path is capable of masking the original exception because it performs deletion operations after catching the execution exception.

## Required correction

Before any further real execution attempt:

1. preserve the original execution exception;
2. do not let cleanup deletion replace or hide it;
3. prefer preserving persistent residual evidence over deleting it;
4. expose a deterministic read-only residual snapshot on failure;
5. re-run targeted and complete synthetic qualification;
6. require a new explicit one-shot human authorization.

No previous one-shot authorization remains active.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.

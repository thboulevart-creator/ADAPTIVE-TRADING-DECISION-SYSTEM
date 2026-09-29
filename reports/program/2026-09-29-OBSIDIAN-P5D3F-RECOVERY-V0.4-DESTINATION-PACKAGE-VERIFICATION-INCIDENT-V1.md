# OBSIDIAN P5-D3F — RECOVERY V0.4 DESTINATION PACKAGE VERIFICATION INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL REAL-EXECUTION ATTEMPT plus VERIFIED GITHUB source review and SAME-ASSISTANT STATIC CONTROL-FLOW ANALYSIS.

## Authorized execution identity

V0.4 runner HEAD:

    1d725a35490fbf0c137072152d2876c53d63f183

V0.4 runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Authorized monitored integration/system-v1 HEAD:

    59f1dc26973b0b50efefccf12b26784d1e41f546

## User-reported governed output

    P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS
    P5D3F_EXPECTED_MONITORED_HEAD=59f1dc26973b0b50efefccf12b26784d1e41f546
    P5D3F_MONITORED_HEAD_AUTHORITY=PASS
    P5D3F_PERSISTENT_STAGING_PRESTATE=PRESENT_EMPTY_PACKAGES_RECOVERY
    P5D3F_RECOVERY_PRESTATE_AUTHORIZED=PASS
    P5D3F_PERSISTENT_FAILURE_ORIGINAL=PromotionHandoffGovernanceError: destination package verification failed
    P5D3F_PERSISTENT_FAILURE_TEMP_ROOT=C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5D3F-PERSISTENT-HANDOFF-9m9sk9rr
    P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON={"entries":[{"path":"packages","type":"DIRECTORY"}],"exists":true,...,"state":"PRESENT_NONEMPTY"}
    BLOCKED: PromotionHandoffGovernanceError: destination package verification failed
    EXIT_CODE=2

## Immediate adjudication

    REAL EXECUTION = BLOCKED
    ONE-SHOT AUTHORIZATION = CONSUMED
    READY_UNAUTHORIZED = NOT ESTABLISHED
    SILENT RETRY = FORBIDDEN

The original body exception was preserved and the temporary evidence root survived as designed.

## Exact static root cause

The qualified P5-D3F handoff implementation copies the sealed source package into the persistent promotion staging root and then calls:

    verify_candidate_generation(destination_package, ...)

The qualified candidate-generation verifier begins by calling:

    _validate_existing_package_root(package_root, forbidden_roots)

That validator enforces:

    package_root MUST be below tempfile.gettempdir()

and otherwise raises:

    CandidateGenerationInvalidError("package root must be below OS temp root")

The production contract, however, requires the destination package to live under:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

which is intentionally outside the OS temporary root.

Therefore the production contract and the qualified destination verifier are structurally incompatible:

    TEMP-ONLY VERIFIER
        versus
    PERSISTENT ONEDRIVE DESTINATION

The wrapper catches CandidateGenerationInvalidError and surfaces only:

    PromotionHandoffGovernanceError("destination package verification failed")

which exactly matches the observed real-execution failure.

## Why synthetic qualification did not expose it

The earlier P5-D3F sacrificial/synthetic qualification used temporary roots, so the destination package satisfied the verifier's temp-root policy.

The production staging contract explicitly moved the destination outside temp, but the downstream verifier root-policy assumption was not represented by a dedicated adversarial test.

This is a real coverage gap, not a transient machine failure.

## Contract contradiction

Persistent gate contracts V0.1/V0.2 require:

- exact persistent production staging under OneDrive;
- destination package verification after copy;
- source/destination verifier descriptor equality;
- byte-exact persistent materialization.

The qualified P5-D3F verifier requires the verified package root to remain under OS temp.

Both cannot be true simultaneously without an explicit persistent-verification amendment.

## Governance consequence

Do NOT weaken or bypass verification.
Do NOT copy directly into the real Vault.
Do NOT relabel this as infrastructure failure.
Do NOT retry the same runner.

The next governed frontier must be a narrow persistent-destination verification amendment that:

1. preserves the existing temp-only verifier behavior for historical/synthetic paths;
2. introduces an explicit, separately authorized persistent-package verification path;
3. constrains that path to the exact promotion staging root and keeps the real Vault forbidden;
4. reuses the same content/manifest/seal/file-map/integrity checks;
5. preserves alias/reparse/hardlink rejection;
6. adds an adversarial test proving a non-temp persistent staging destination can be verified only under the explicit persistent policy;
7. requalifies the affected P5-D3F handoff surface before any new real authorization.

No real execution is authorized by this report.

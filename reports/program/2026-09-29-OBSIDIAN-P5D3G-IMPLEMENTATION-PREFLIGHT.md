# OBSIDIAN P5-D3G — IMPLEMENTATION PREFLIGHT

Date: 2026-09-29

## Evidence status

READ-ONLY / STATIC RECONSTRUCTION.

No P5-D3G runtime execution has occurred.
No sacrificial live-Vault transaction has occurred.
No real Vault write is authorized or performed.

## Verified opening state

Remote HEAD:

    4e7be40211e1902015d42540afd7fe9eebb2103e

Qualified P5-D3G contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

Qualified P5-D3F implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Qualified P5-D2 observer tick blob:

    fd212f61ec38332b677110f40265638af55a73e2

## Implementation boundary opened by human instruction

Only the following boundary is opened:

    P5-D3G IMPLEMENTATION
    FINITE LIVE PUBLICATION TRANSACTION IMPLEMENTATION
    + SACRIFICIAL LIVE-VAULT QUALIFICATION

Still closed:

    real Vault execution
    production CURRENT/CURRENT.tmp mutation
    production PROMOTION_CONFIRMED
    automatic publication
    P5-D4 observer loop
    P6 Graph/Search semantics

## Candidate implementation shape

A bounded implementation module may provide:

    build_publication_plan(...)
    publication_plan_digest(...)
    verify_live_publication(...)
    execute_finite_live_publication(...)
    classify_publication_recovery(...)

The implementation must require an explicit authorization object supplied after the read-only plan.

No helper may silently manufacture production authorization.

## Sacrificial-only guard

During this qualification phase the implementation must fail closed if the target live-Vault path resolves to the real production Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

The sacrificial Vault, control/evidence root and retained handoff must be mutually disjoint.

## Required transaction behavior

1. fresh read-only P5-D3F handoff verification;
2. read-only publication plan;
3. exact one-shot authorization validation;
4. exclusive external writer lock;
5. handoff and CURRENT prestate revalidation;
6. immutable generation wrapper materialization;
7. target verification;
8. exclusive CURRENT.tmp creation and fsync;
9. bounded atomic replace/retry;
10. read-after-write verification;
11. durable external physical receipt;
12. P5-D2 PROMOTION_CONFIRMED;
13. durable external logical receipt;
14. writer release.

## Test-first minimum

Tests must freeze at least:

- read-only planning;
- real-Vault path rejection;
- missing/mismatched authorization rejection;
- one-shot authorization reuse rejection;
- writer contention rejection;
- successful bootstrap publication;
- immutable package equality;
- CURRENT.tmp preexistence rejection;
- changed CURRENT after planning rejection;
- target collision rejection;
- read-only publication verification;
- physical-before-logical ordering;
- logical-confirmation failure => physical-success/logical-pending;
- crash/recovery state classification;
- no P5-D4/background/polling surface.

No implementation qualification may be claimed before a governed full-suite PASS.

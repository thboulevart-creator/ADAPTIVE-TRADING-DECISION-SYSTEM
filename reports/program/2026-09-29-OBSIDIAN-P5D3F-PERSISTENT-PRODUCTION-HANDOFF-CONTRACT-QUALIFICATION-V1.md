# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF CONTRACT QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed persistent-production-handoff contract re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    fe727c6ef06ca66cd261119e2522d5aec0f27856

Contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Contract tests blob:

    6cc6af77efe3c6abb1aaf8ae2df5be9e64cb1bb7

Governed contract runner blob:

    beeaed399b1eefc82a0422a21444c6b740460304

## User-reported governed result

Targeted persistent-production-handoff contract tests:

    Ran 12 tests in 0.093s
    OK

Complete historical Obsidian suite:

    Ran 1194 tests in 197.567s
    OK

Terminal markers:

    P5D3F_PERSISTENT_HANDOFF_CONTRACT_TARGETED=PASS
    P5D3F_PERSISTENT_HANDOFF_CONTRACT_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_PERSISTENT_HANDOFF_CONTRACT_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed governed run.

## Adjudication

    P5-D3F PERSISTENT PRODUCTION HANDOFF CONTRACT = QUALIFIED

This qualification opens only the next bounded candidate frontier:

    P5-D3F-PERSISTENT-PRODUCTION-HANDOFF-EXECUTION-HARNESS

## Authority boundary after contract qualification

Still NOT authorized by this qualification:

- creation of the persistent staging root;
- execution of the persistent handoff;
- any real-Vault write;
- CURRENT/CURRENT.tmp mutation;
- real-Vault generation materialization;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage-A authority;
- Stage-B authority;
- automatic publication;
- background observer / polling;
- P5-D4;
- P6.

## Required next gate

The execution harness must be preregistered, statically reviewed and synthetically qualified before any persistent staging creation or real-Vault read occurs.

The harness must:

1. freshly bind origin/integration/system-v1 HEAD and tree;
2. construct a clean temporary detached candidate repository;
3. construct a temporary evaluation workspace;
4. independently fingerprint the real Vault before execution;
5. create only the exact persistent staging root if absent;
6. invoke only the already-qualified P5-D3F runtime once;
7. reverify the retained handoff;
8. independently fingerprint the real Vault afterward;
9. require exact before/after equality;
10. clean temporary candidate/evaluation roots;
11. STOP.

No publication authority is implied.

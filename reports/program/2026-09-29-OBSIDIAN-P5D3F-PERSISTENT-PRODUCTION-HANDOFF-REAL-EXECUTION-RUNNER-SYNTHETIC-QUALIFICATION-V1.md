# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF REAL EXECUTION RUNNER SYNTHETIC QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed synthetic real-execution-runner re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    d661b3463dfe901a5ddabd36c0cdfa70d2b070ea

Exact runner qualification candidate:

    a97dc6c150fb0c7cc7835f169275a7920c49ac45

Real execution runner blob:

    e56501e3710ab23537975e950aff016e4a832742

Runner adversarial tests blob:

    97d7577d46f728aae5bfe1e0eadc389121dd7872

Governed runner re-break blob:

    d18be484bb74398d88ab37d42eb989392fa47deb

Qualified persistent-handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Qualified persistent-handoff implementation tests blob:

    7da1fadeb1b3e9efee54b7ca09f0735277af345c

Qualified persistent-handoff gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## User-reported governed result

Targeted real-execution-runner tests:

    Ran 9 tests in 0.009s
    OK

Complete historical Obsidian suite:

    Ran 1218 tests in 203.596s
    OK

Terminal markers:

    P5D3F_PERSISTENT_REAL_RUNNER_TARGETED=PASS
    P5D3F_PERSISTENT_REAL_RUNNER_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_PERSISTENT_REAL_RUNNER_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed governed run.

## Adjudication

    P5-D3F PERSISTENT PRODUCTION HANDOFF REAL EXECUTION RUNNER — SYNTHETIC QUALIFICATION = PASS

The runner is qualified against its frozen adversarial surface and the complete historical Obsidian suite.

## Next exact gate

    HUMAN ONE-SHOT REAL P5-D3F PERSISTENT HANDOFF AUTHORIZATION

The runner may be executed against the exact persistent staging and real Vault only after a distinct explicit human authorization for one finite READY_UNAUTHORIZED handoff.

Required authorization literal:

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Scope of that authorization

It may authorize only:

- creation of the exact persistent staging root if absent;
- read-only fingerprinting of the real Vault before and after;
- fresh observation of origin/integration/system-v1;
- construction of a clean temporary detached candidate repository;
- one invocation of the qualified P5-D3F handoff runtime;
- persistence of exactly one READY_UNAUTHORIZED handoff under the staging root;
- post-write handoff reverification;
- zero-real-Vault-mutation proof;
- cleanup of temporary candidate/evaluation roots;
- mandatory STOP.

It does NOT authorize:

- any real-Vault write;
- CURRENT or CURRENT.tmp mutation;
- real-Vault generation materialization;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage-A approval;
- Stage-B authority;
- automatic publication;
- background observer or polling;
- P5-D4;
- P6.

## Post-execution requirement

A successful real execution must report:

    P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION=PASS
    REAL_VAULT_ZERO_MUTATION=PASS
    LIVE_PUBLICATION_EXECUTED=FALSE
    MANDATORY_STOP=TRUE
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION_COMPLETED=PASS

and must emit the exact RESULT_JSON for persistence and review.

After that successful handoff:

    STOP

The next eligible frontier returns to:

    P5-D3G — EXACT REAL-VAULT READ-ONLY PLAN QUALIFICATION

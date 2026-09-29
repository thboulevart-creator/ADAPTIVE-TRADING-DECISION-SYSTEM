# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF REAL EXECUTION RUNNER QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Synthetic qualification target only.

No persistent staging creation is performed by this report.
No real Vault access is performed by this report.
No persistent handoff execution is authorized by this report alone.

## Exact qualification candidate

    a97dc6c150fb0c7cc7835f169275a7920c49ac45

Real execution runner:

    tools/obsidian_projection/p5d3f_persistent_production_handoff_real_execution.py

Real execution runner blob:

    e56501e3710ab23537975e950aff016e4a832742

Frozen runner tests:

    tests/obsidian_projection/test_p5d3f_persistent_production_handoff_real_execution_runner.py

Runner tests blob:

    97d7577d46f728aae5bfe1e0eadc389121dd7872

Governed synthetic re-break runner:

    tools/obsidian_projection/p5d3f_persistent_production_handoff_real_execution_runner_rebreak.py

Synthetic re-break runner blob:

    d18be484bb74398d88ab37d42eb989392fa47deb

Qualified persistent handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Qualified persistent handoff implementation tests blob:

    7da1fadeb1b3e9efee54b7ca09f0735277af345c

Qualified persistent handoff gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Frozen targeted surface

    9 targeted tests

The tests cover:

- exact one-shot human authorization literal;
- exact real-execution branch binding;
- exact qualified runtime authority pins;
- repository-origin normalization;
- rollback of a staging root created by a failed run when it remains empty;
- restoration of a preexisting empty staging root;
- refusal to delete nonempty residual evidence after failure;
- explicit governed-runner blob binding;
- absence of live-publication and later-authority calls.

## Real execution runner authority

A future invocation requires all of:

1. exact clean control clone;
2. exact local runner HEAD;
3. exact remote runner-branch HEAD;
4. exact committed and worktree runner blob supplied explicitly by the human;
5. exact qualified implementation/test/contract/runtime blobs;
6. exact explicit authorization literal:

       AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

Only after these checks may the runner invoke the already-synthetically-qualified persistent-handoff implementation once.

## Failure handling

If execution fails after creating only an empty staging root or an empty packages directory, the runner may restore that known-empty prestate.

If any nonempty residual exists, it is preserved and execution blocks for audit rather than deleting evidence.

## Qualification sequence

Synthetic runner qualification requires:

1. exact implementation-branch remote-race guard;
2. manual exact candidate checkout;
3. exact blob pins;
4. static required/forbidden surface scan;
5. Python compilation with bytecode outside the repository;
6. 9 targeted runner tests;
7. complete historical Obsidian suite;
8. final clean-control-clone gate.

Only after this synthetic runner qualification may the user be given the distinct command that performs the real persistent P5-D3F handoff.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.

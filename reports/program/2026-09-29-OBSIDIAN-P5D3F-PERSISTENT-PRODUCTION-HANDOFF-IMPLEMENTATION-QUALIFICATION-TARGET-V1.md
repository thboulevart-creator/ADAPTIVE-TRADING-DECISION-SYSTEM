# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF IMPLEMENTATION QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No persistent staging creation is claimed.
No real Vault access is claimed.
No persistent handoff execution is claimed.

## Exact synthetic qualification candidate

    b6129fd735186fa0a68d0862b3326308f1ba3d25

Implementation:

    tools/obsidian_projection/persistent_production_handoff.py

Implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Frozen adversarial tests:

    tests/obsidian_projection/test_p5d3f_persistent_production_handoff.py

Tests blob:

    7da1fadeb1b3e9efee54b7ca09f0735277af345c

Governed synthetic re-break runner:

    tools/obsidian_projection/p5d3f_persistent_production_handoff_implementation_rebreak.py

Runner blob:

    65016ec10d2ad9b2ddf4ce5c9a359fc035a323ef

Qualified persistent gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Frozen test surface

    15 targeted tests

The synthetic tests use only temporary roots.

They do not create the real persistent staging root and do not access the user's real Vault.

## Candidate behavior

The candidate adds a bounded execution harness that:

1. validates the exact persistent staging and real-Vault sibling identities;
2. rejects unknown preexisting staging contents;
3. fingerprints the protected Vault read-only;
4. freshly observes origin/integration/system-v1;
5. rechecks remote freshness;
6. constructs a temporary clean detached candidate repository;
7. invokes only the already-qualified P5-D3F runtime;
8. reverifies the retained handoff;
9. fingerprints the protected Vault again;
10. requires exact zero mutation;
11. deletes temporary candidate/evaluation roots;
12. returns a STOP-bearing READY_UNAUTHORIZED result.

## Synthetic qualification sequence

1. exact remote-race guard on this implementation branch;
2. exact functional-candidate checkout;
3. exact contract / implementation / tests / qualified-runtime blob pins;
4. static forbidden-surface scan;
5. Python compilation with bytecode outside the repository;
6. 15 targeted synthetic tests;
7. complete historical Obsidian suite;
8. final clean-control-clone gate.

A synthetic PASS is necessary but not sufficient to materialize the persistent handoff.

After synthetic qualification, a distinct governed execution runner must be frozen before the real persistent handoff is executed.

Real Vault WRITE remains closed.
Live publication remains closed.

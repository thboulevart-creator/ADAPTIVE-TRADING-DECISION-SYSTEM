# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT IMPLEMENTATION QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local execution is claimed.
No real Vault access is claimed by this report.

## Exact synthetic qualification candidate

    e268f1ca67cdf3166a2f7dd15972774adc9dd825

Production-enablement implementation:

    tools/obsidian_projection/production_enablement.py

Implementation blob:

    64c1b2279835f57c03c9ec2d6a0eae9e349d55ee

Frozen adversarial tests:

    tests/obsidian_projection/test_p5d3g_production_enablement.py

Tests blob:

    5a05ac5fccaf7032248f35f8fd2933d5943b100c

Governed synthetic re-break runner:

    tools/obsidian_projection/p5d3g_production_enablement_implementation_rebreak.py

Runner blob:

    1c126f27d7a48ec44cbfc6e7eafe056dd5a9cefb

Qualified production-enablement contract blob:

    5de65f5d13a93d1325d53e1b58536ed0860921f2

Qualified predecessor live-publication implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

## Frozen test surface

    17 targeted tests

The tests use sacrificial temporary directories and patch only the production-enable­ment module's exact REAL_VAULT identity to those temporary roots.

The governed synthetic re-break itself must not access the user's real Vault.

## Candidate behavior

The candidate adds only:

- exact production Vault identity validation;
- read-only whole-tree snapshotting;
- deterministic real-live publication-plan construction;
- exact handoff / candidate / generation / CURRENT / CURRENT.tmp / target-state binding;
- Stage-A approval validation;
- one-shot Stage-A consumption evidence outside the Vault;
- before/after zero-mutation proof.

It does not add a Stage-B authorization issuer or any real publication execution entrypoint.

## Qualification sequence

Synthetic qualification requires:

1. exact implementation-branch remote-race guard;
2. exact candidate checkout;
3. exact blob pins;
4. static execution/background-surface scan;
5. Python compilation with bytecode outside the repository;
6. targeted production-enablement implementation tests;
7. complete historical Obsidian suite;
8. final clean-control-clone gate.

A synthetic PASS is necessary but not sufficient for final production-enablement qualification.

After synthetic PASS, the next step is a separately governed exact real-Vault READ-ONLY plan run, followed by human Stage-A approval and zero-mutation validation.

No Stage-B authority is opened.

# OBSIDIAN P5-D3F — PERSISTENT REAL EXECUTION IMPORT FAILURE INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION FAILURE.

GitHub state was independently verified after the failure.

## Attempted governed execution

Authorized runner HEAD:

    a6a0c8e4cd57d4028fc4b44d758f046ec572caff

Authorized runner blob:

    e56501e3710ab23537975e950aff016e4a832742

Authorization literal:

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Observed failure

Python terminated before module import completed:

    ModuleNotFoundError: No module named 'tools'

Exit code:

    1

The failure occurred at the top-level import:

    from tools.obsidian_projection.persistent_production_handoff import ...

when the file was invoked directly by path.

## Adjudication

    GOVERNED P5-D3F HANDOFF RUNTIME ENTERED = NO
    execute_persistent_production_handoff CALLED = NO
    persistent staging creation by runner = NOT REACHED
    real Vault fingerprint = NOT REACHED
    P5-D3F handoff materialization = NOT REACHED

This is an invocation-mode defect, not evidence of an implementation failure.

The runner is written with an absolute package import rooted at tools. Direct path invocation sets Python's initial import path to tools/obsidian_projection, so the repository root is not necessarily available as the package root.

The same immutable runner can instead be invoked as a module from the repository root:

    python -m tools.obsidian_projection.p5d3f_persistent_production_handoff_real_execution

No runner-byte change is required for that invocation correction.

## Authorization consumption

The recorded one-shot authorization is not adjudicated as consumed by this failed attempt because execution did not pass module import and the governed handoff entrypoint was never reached.

However, retry is forbidden until the persistent staging prestate is read-only audited and confirmed compatible with the original authorized prestate.

## Required next step

READ-ONLY audit only:

- inspect exact persistent staging path;
- confirm whether it is absent, empty, or contains residual state;
- do not create/delete/modify anything.

If the staging is absent or empty and no PROMOTION-HANDOFF.json exists, the same explicit authorization may be used in one reviewed retry with corrected module invocation.

If any nonempty residual exists, STOP for audit.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.

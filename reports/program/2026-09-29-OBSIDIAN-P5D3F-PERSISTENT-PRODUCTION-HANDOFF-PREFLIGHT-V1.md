# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF MATERIALIZATION PREFLIGHT V1

Date: 2026-09-29

## Evidence status

STATIC / READ-ONLY PREFLIGHT.

No persistent staging directory is created by this document.
No P5-D3F runtime is executed.
No real Vault write is authorized.

## Confirmed local prerequisite state

User-provided read-only inventory established:

- no persistent PROMOTION-HANDOFF.json exists under C:\Users\Boulevart\OneDrive\Bureau\ATDS;
- C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING does not exist;
- the real Vault C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION exists;
- the ATDS-GIT clone is clean but currently detached on an Obsidian implementation candidate;
- the OneDrive repository clone is not clean and is therefore ineligible as the production handoff candidate repository.

## Qualified P5-D3F authority

P5-D3F contract blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F qualified implementation candidate:

    a41c5b150168c2e4eb06648237022a4974868423

P5-D3F qualified implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

P5-D3F implementation qualification report blob:

    d1aafa4ab8e2dfea2fe8cb5d480e9126bc50f257

P5-D3F sacrificial staging qualification report blob:

    c99d74383c25653dd05e0831eb4eab355afb3b6e

## Exact missing frontier

    P5-D3F — PERSISTENT PRODUCTION HANDOFF MATERIALIZATION

Purpose:

Materialize exactly one durable READY_UNAUTHORIZED P5-D3F handoff in the dedicated production-staging sibling of the real Vault, while proving the real Vault remains byte-for-byte unchanged.

## Source candidate rule

The candidate must not be silently selected from whichever local clone is currently checked out.

At execution time:

1. fetch origin/integration/system-v1;
2. bind the exact freshly observed remote HEAD;
3. bind its exact tree;
4. create a clean temporary detached candidate repository;
5. verify origin identity, HEAD, TREE and clean status;
6. evaluate and hand off only that exact candidate.

Observed during this preflight only, not frozen as execution authority:

    integration/system-v1 HEAD = b2758218d22424555e482e1d6c35029df4333aaa
    TREE = 93bd4ac4d2c43f387f03234bc4d1a9d7a85d53ad

The execution gate must re-check freshness.

## Persistent paths

Exact staging root:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

Exact protected real Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

The staging root may be created only by the governed persistent-handoff execution harness after all preflight guards pass.

The qualified P5-D3F runtime may then create only:

    <staging>\packages\<generation_id>\package\...
    <staging>\packages\<generation_id>\PROMOTION-HANDOFF.json

## Real-Vault boundary

The real Vault may be read only for before/after fingerprinting and P5-D3F verification.

Forbidden:

- CURRENT;
- CURRENT.md;
- CURRENT.tmp;
- generations materialization;
- live publication transaction;
- P5-D2 PROMOTION_CONFIRMED;
- Stage-A or Stage-B authority;
- automatic publication;
- observer/polling/task/service registration.

## Success semantics

Success requires all of:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED
    handoff_status = READY_UNAUTHORIZED
    package_status = PASS_SEALED_UNPROMOTED
    publication_authorized = false
    real_vault_modified = false
    current_pointer_created = false
    production_promotion_authorized = false
    p5d2_promotion_confirmed_emitted = false

plus an independently computed exact before/after real-Vault fingerprint equality.

## STOP

After one persistent handoff is materialized and verified:

    STOP

The next eligible frontier returns to:

    P5-D3G — EXACT REAL-VAULT READ-ONLY PLAN QUALIFICATION

No publication authority is implied.

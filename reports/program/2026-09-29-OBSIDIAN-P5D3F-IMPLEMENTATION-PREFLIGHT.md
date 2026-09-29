# OBSIDIAN P5-D3F — IMPLEMENTATION PREFLIGHT

Date: 2026-09-29

## Evidence status

READ-ONLY / STATIC RECONSTRUCTION.

No P5-D3F handoff runtime has been executed.
No sacrificial staging has been created.
No real Vault write is authorized or performed.

## Verified start state

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD:

    de2251e4143005d15a8bc5c4b1d25d01a9a9f3e9

Qualified P5-D3F contract blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

Qualified P5-D3C2 packager/verifier blob:

    e2e5867536f4f9c7dec475c6696737249536ff39

Qualified P5-D3D finite evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

Qualified P5-D3E harness blob:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

## Reconstructed implementation boundary

P5-D3F must consume an already prepared isolated candidate repository identified by exact lowercase 40-hex HEAD and TREE.

The handoff core must remain network-free.

The exact qualified P5-D3D evaluator performs a fresh finite evaluation and creates:

    <evaluation-workspace>/candidate-package

The package must independently reverify through the exact qualified P5-D3C2 verifier as:

    PASS_SEALED_UNPROMOTED

Only after QUALIFIED evaluation and source-package verification may the handoff touch promotion staging.

The retained wrapper target is:

    packages/<generation_id>/
        package/
            generated/
            _atds_generation/
        PROMOTION-HANDOFF.json

The inner package must remain byte-exact and unchanged.

PROMOTION-HANDOFF.json must be the final wrapper mutation and must retain all publication authority flags as false.

The handoff verifier must be read-only.

## Existing interfaces reused

P5-D3D:

    evaluate_candidate_finitely(...)

P5-D3C2:

    verify_candidate_generation(...)

P5-D2 activation semantics:

    make_initial_state()
    one_shot_tick(...)

Candidate repository identity:

    FrozenGitSource

The P5-D3C2 generation manifest contains the additional scientific identity fields required to cross-check dynamic-inventory and determinism digests that are not all exposed by the verifier descriptor.

## Implementation candidate shape

A new bounded module may provide:

    run_finite_promotion_handoff(...)

and:

    verify_promotion_handoff(...)

The implementation candidate must:

- verify exact tooling/contract identities before use;
- verify exact candidate repository HEAD/TREE/origin/clean state;
- validate staging/live-Vault separation and alias safety;
- perform fresh finite evaluation;
- keep REJECTED and BLOCKED distinct;
- verify source package;
- compute deterministic byte-tree identity;
- copy each path and byte without rename/hard-link aliasing;
- verify destination package;
- require source/destination descriptors and byte-tree digests to match;
- write canonical PROMOTION-HANDOFF.json last;
- reverify the completed handoff read-only;
- return PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED only after all checks pass;
- never create CURRENT or CURRENT.tmp;
- never invoke P5-C2/P5-C3R2 writers;
- never emit P5-D2 PROMOTION_CONFIRMED;
- never touch the real Vault.

## Test-first requirement

Before implementation, tests must freeze at least:

- successful synthetic retained handoff;
- source/destination byte-tree equality;
- exact wrapper layout;
- canonical record and exact field set;
- all publication authority bits false;
- REJECTED cannot produce a handoff;
- BLOCKED cannot produce a handoff;
- overlapping live Vault/staging is rejected;
- pre-existing target blocks;
- hard-link/reparse/symlink surfaces fail closed;
- tampered copied payload is rejected;
- tampered handoff identity is rejected;
- verifier is read-only;
- no CURRENT/CURRENT.tmp surface exists.

## Authority

The qualified contract plus explicit human continuation opens only the P5-D3F IMPLEMENTATION CANDIDATE boundary.

Sacrificial execution remains a later local qualification gate.

Production handoff, real Vault writes, P5-D3G, CURRENT mutation, background execution and automatic publication remain closed.

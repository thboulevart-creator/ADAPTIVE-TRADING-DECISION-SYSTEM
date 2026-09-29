# OBSIDIAN P5-D3G — IMPLEMENTATION GOVERNED PRE-RUN V1

Date: 2026-09-29

## Evidence status

Static pre-run checkpoint only.

No local P5-D3G implementation execution is claimed here.

## Exact functional candidate

    80a40ee5413644904d6841f2acfd13a29c796b3a

Implementation blob:

    eb0e6607430d32fe51c065ed4bacba05721f42b6

Implementation tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed implementation runner blob:

    624b9752184137a23819dd15f490b5d57518da96

Frozen P5-D3G contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

Implementation test count:

    20

## Qualification boundary

The next local run is allowed to execute only:

- Python compilation;
- targeted P5-D3G contract + implementation tests;
- complete historical tests/obsidian_projection discovery;
- sacrificial temporary live-Vault transactions created by the tests;
- clean-control-clone verification.

Still forbidden:

- real production Vault write;
- production CURRENT/CURRENT.tmp mutation;
- production PROMOTION_CONFIRMED;
- automatic publication;
- P5-D4 background observer/polling;
- P6 Graph/Search claim.

## Expected result semantics

A full governed PASS may qualify:

    P5-D3G IMPLEMENTATION
    +
    SACRIFICIAL LIVE-VAULT BEHAVIOR

It may not authorize the real Vault.

Any FAIL, ERROR or BLOCKED result keeps P5-D3G implementation unqualified.

# OBSIDIAN P5-D3G — IMPLEMENTATION QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local P5-D3G implementation execution is claimed here.

## Exact functional candidate

    80a40ee5413644904d6841f2acfd13a29c796b3a

Implementation:

    tools/obsidian_projection/live_publication_transaction.py

Implementation blob:

    eb0e6607430d32fe51c065ed4bacba05721f42b6

Implementation tests:

    tests/obsidian_projection/test_p5d3g_live_publication_transaction.py

Tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Governed runner:

    tools/obsidian_projection/p5d3g_implementation_rebreak.py

Runner blob:

    624b9752184137a23819dd15f490b5d57518da96

Frozen contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

Qualified predecessor P5-D3F implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Qualified predecessor P5-D2 observer blob:

    fd212f61ec38332b677110f40265638af55a73e2

## Candidate scope

The implementation remains sacrificial-only during this qualification gate.

It includes:

- read-only publication planning;
- exact one-shot human authorization validation;
- external exclusive writer ownership;
- fresh P5-D3F handoff reverification;
- durable rollback-basis capture outside the Vault;
- immutable generation wrapper materialization;
- exact sealed-package preservation;
- CURRENT.tmp exclusive write + fsync;
- bounded atomic CURRENT replace/retry;
- read-after-write publication verification;
- append-only physical/logical receipts outside the Vault;
- P5-D2 PROMOTION_CONFIRMED only after physical verification and physical receipt;
- finite recovery classification;
- forward-completion recovery;
- replace-mode rollback to exact previous CURRENT;
- real production Vault path rejection.

## Test surface

The implementation test module contains 20 tests, including:

- read-only planning;
- real-Vault rejection;
- missing/mismatched authorization;
- writer contention;
- bootstrap publication;
- sealed-package byte equality;
- one-shot authorization;
- stale CURRENT.tmp;
- CURRENT race after planning;
- target collision;
- read-only live verification;
- physical-success/logical-pending distinction;
- recovery-state classification;
- replace-mode publication;
- bounded retryable Windows sharing conflicts;
- forward recovery;
- rollback after invalid newly published target;
- absence of background/scheduler surfaces.

## Qualification gate

The governed implementation runner must:

1. verify branch and remote race guard;
2. check out this exact functional candidate;
3. restore bounded canonical byte-pinned worktree representation;
4. verify exact contract / implementation / implementation-test / contract-test blobs;
5. py_compile runner, implementation and both test modules;
6. run targeted P5-D3G implementation + contract tests;
7. run the complete historical tests/obsidian_projection suite;
8. require a clean control clone after execution.

Only a full PASS may qualify the implementation and sacrificial live-Vault behavior.

The real Vault remains closed.

# OBSIDIAN P5-D3G — CONTRACT QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local P5-D3G contract execution is claimed here.

## Exact functional contract candidate

    195f2689d10edbadf2904f68621fd5df65000498

Contract:

    tools/obsidian_projection/live_publication_transaction_contract_v0_1.json

Contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

Contract tests:

    tests/obsidian_projection/test_live_publication_transaction_contract_v0_1.py

Tests blob:

    dbf37f769a407923fbdeb3bb476aa8cd0405b6ef

Documentation:

    docs/OBSIDIAN-P5D3G-LIVE-PUBLICATION-TRANSACTION-CONTRACT-V0.1.md

Documentation blob:

    9fd3d9869289535af2313d990d2c018dde341295

Governed runner:

    tools/obsidian_projection/p5d3g_contract_rebreak.py

Runner blob:

    88c1540fa0865558d73e4feb640ca59201e226e3

## Frozen contract scope

The candidate defines contract-only semantics for:

- read-only publication planning;
- explicit one-shot human authorization;
- exclusive single-writer ownership;
- fresh retained-handoff reverification;
- immutable production generation wrapper;
- target verification before CURRENT.tmp;
- P5-C3R2-equivalent bounded CURRENT replace/retry semantics;
- read-after-write verification;
- physical-publication evidence;
- P5-D2 PROMOTION_CONFIRMED ordering;
- crash recovery and bounded rollback;
- bootstrap versus replace modes;
- preservation of P5-D4 and P6 boundaries.

## Explicit closure

The candidate does not implement or authorize:

    real Vault writes
    CURRENT/CURRENT.tmp mutation
    P5-D2 PROMOTION_CONFIRMED emission
    P5-D3G runtime
    P5-D4 observer loop
    Graph/Search CURRENT semantics

## Qualification gate

The governed runner must pass:

1. exact branch/remote/candidate identity gates;
2. exact contract and test blob gates;
3. Python compilation;
4. P5-D3G targeted contract tests;
5. complete tests/obsidian_projection discovery;
6. clean control clone after execution.

Only then may P5-D3G contract qualification be persisted.

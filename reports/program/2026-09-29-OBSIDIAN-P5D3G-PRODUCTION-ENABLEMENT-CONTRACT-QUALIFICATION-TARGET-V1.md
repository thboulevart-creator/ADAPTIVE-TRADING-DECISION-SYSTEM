# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT CONTRACT QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No production runtime execution is claimed.
No real Vault access is claimed.
No real Vault write is authorized.

## Exact functional candidate

    82e8e1aacc8fcb1129c12a5dc66ce2015c6ae845

Contract:

    tools/obsidian_projection/production_enablement_gate_contract_v0_1.json

Contract blob:

    5de65f5d13a93d1325d53e1b58536ed0860921f2

Contract tests:

    tests/obsidian_projection/test_production_enablement_gate_contract_v0_1.py

Tests blob:

    12873436d6354ffa454253cdf754023378d35076

Governed runner:

    tools/obsidian_projection/p5d3g_production_enablement_contract_rebreak.py

Runner blob:

    2ddee8bbd0b949a2a9f187b8d10be11150c05f9b

Human-readable contract:

    docs/OBSIDIAN-P5D3G-PRODUCTION-ENABLEMENT-GATE-CONTRACT-V0.1.md

Documentation blob:

    dcb7e9ab2e0d5a6a0b763b1239d9383905904dab

Qualified predecessor implementation commit:

    87c189cd3b0fe6ce40845214a943a14407618ece

## Contract surface

Contract tests:

    18

Required adversarial breakers:

    70 unique

## Qualification scope

Only the contract may qualify here.

A PASS may open the next candidate frontier:

    P5-D3G-PRODUCTION-ENABLEMENT-IMPLEMENTATION

whose allowed purpose is only:

    READ_ONLY_REAL_VAULT_PLAN
    +
    STAGE_A_ONE_SHOT_PLAN_APPROVAL_VALIDATION
    +
    ZERO_REAL_VAULT_MUTATION_PROOF

Still closed after contract qualification alone:

- any real-Vault read by runtime;
- any real-Vault write;
- any production CURRENT/CURRENT.tmp mutation;
- any production generation materialization;
- any production P5-D2 PROMOTION_CONFIRMED;
- any Stage-B execution authorization;
- any production publication execution;
- P5-D4;
- P6.

## Governed re-break requirement

The governed runner must:

1. verify exact repository and branch;
2. enforce remote-race guard;
3. check out this exact functional candidate;
4. verify exact contract and test blobs;
5. compile runner and test module;
6. run targeted production-enablement contract tests;
7. run the complete historical Obsidian test suite;
8. require a clean control clone after execution.

Only a complete PASS qualifies this contract.

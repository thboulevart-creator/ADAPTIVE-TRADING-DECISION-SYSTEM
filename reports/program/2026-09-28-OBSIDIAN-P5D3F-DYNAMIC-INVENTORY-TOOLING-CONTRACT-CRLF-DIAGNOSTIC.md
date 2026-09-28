# OBSIDIAN P5-D3F — DYNAMIC INVENTORY TOOLING CONTRACT CRLF DIAGNOSTIC

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION / DIAGNOSTIC.

Not independent execution evidence.

## Verified GitHub state before persistence

Remote HEAD:

    72ab68e4ba694d2ad436ccf8d0a3ff01c72f5c15

V8 functional candidate:

    6b45681bf060d6571782b83593a347ca6acd7a30

## Local diagnostic

Path:

    tools/obsidian_projection/dynamic_inventory_contract_v0_1.json

Observed:

    HEAD=80729156f4ac51b760c4347f581f052a175b88b3
    RAW=4e4d4ed8e7135453d54504fc74c9586a55ae9c4a
    FILTER=80729156f4ac51b760c4347f581f052a175b88b3
    i/lf
    w/crlf
    attr/text=auto eol=lf

## Static code correlation

At the exact V8 candidate, tools/obsidian_projection/dynamic_inventory.py defines:

    CONTRACT_BLOB=80729156f4ac51b760c4347f581f052a175b88b3

Its verify_contract() implementation reads dynamic_inventory_contract_v0_1.json as raw bytes, computes the Git blob OID from those raw bytes, and raises:

    P5-B contract blob mismatch

when the computed OID differs from CONTRACT_BLOB.

finite_candidate_evaluator.py maps the P5-B contract unreadable/blob mismatch/schema family to:

    TOOLING_CONTRACT_MISMATCH

The V8 local targeted diagnostic reported both remaining P5-D3D and P5-D3E failures with exactly:

    FAILURE=TOOLING_CONTRACT_MISMATCH

## Adjudication

The current common V8 synthetic failure is directly explained by the CRLF raw-byte mismatch of dynamic_inventory_contract_v0_1.json.

No historical expected blob is stale:

    committed Git blob == expected CONTRACT_BLOB == 80729156f4ac51b760c4347f581f052a175b88b3

The mismatch exists only in raw local worktree bytes.

## V9 correction boundary

A V9 candidate may add exactly:

    tools/obsidian_projection/dynamic_inventory_contract_v0_1.json

to the existing BYTE_PIN_COMPATIBILITY_PATHS set.

No other tooling-contract path is justified by the present evidence.

No historical repinning is authorized.
No historical test weakening is authorized.

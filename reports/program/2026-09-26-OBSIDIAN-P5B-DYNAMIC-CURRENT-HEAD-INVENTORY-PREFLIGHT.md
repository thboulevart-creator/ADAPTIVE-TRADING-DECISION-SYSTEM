# OBSIDIAN P5-B — DYNAMIC CURRENT-HEAD INVENTORY PREFLIGHT

Date: 2026-09-26

## Scope

P5-B preregisters deterministic source selection for continuous projection.

It removes the frozen 74-artifact pilot as the future runtime source-universe mechanism without modifying that historical pilot.

## Exact predecessor

Qualified P5-A closure:

    343d253074abe603eb61bebab29ba58f0bd9301c

## Candidate branch

    feat/obsidian-projection-p5b-dynamic-current-head-inventory-v0.1

## Monitored canonical source observed for design census

Repository:

    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch:

    integration/system-v1

Observed HEAD:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

Observed tree:

    ac1e61838a72852cad96e003bfb593de567c2b6d

## Persisted candidate artifacts

Contract:

    tools/obsidian_projection/dynamic_inventory_contract_v0_1.json
    blob: 80729156f4ac51b760c4347f581f052a175b88b3

Documentation:

    docs/OBSIDIAN-P5B-DYNAMIC-CURRENT-HEAD-INVENTORY-CONTRACT-V0.1.md
    blob: fcae57d40de517126f73f2d78e0e589c578909a8

Contract breakers:

    tests/obsidian_projection/test_dynamic_inventory_contract_v0_1.py
    blob: a8247a483163177e03fb56865cb88772f7b51cd6

## Current Git-tree census

The exact observed tree contains:

    908 regular tracked blobs
    100,818,496 aggregate blob bytes

Extension census includes:

    .md    457
    .py    183
    .json  154
    .yml    84
    .txt    20
    .bi5     9
    .log     1

No symlink or gitlink was observed.

Under the preregistered P5-B content-mode rules:

    FULL_TEXT      890
    METADATA_ONLY   18

The 18 metadata-only artifacts consist of:

- 9 BI5 blobs;
- 1 log;
- 8 JSON blobs larger than 1 MiB.

The largest observed blob is:

    evidence/bfiq02/interval_inventory_v0_1.json
    22,826,236 bytes

No candidate sensitive path matched the preregistered path policy in the observed tree.

These counts are evidence for this HEAD only and are not runtime constants.

## Selection architecture

Inventory is derived from the exact Git tree, not the working tree.

Default:

    every tracked regular blob is inventoried

unless an explicit safety condition blocks the HEAD.

Unknown future top-level directories become:

    OTHER_TRACKED

instead of being silently omitted.

Selection zones are provenance/navigation labels only. They do not imply semantic role, authority, qualification or scientific state.

## Safety boundaries

HEAD is blocked for:

- symlink;
- gitlink;
- undecodable path;
- tracked Vault-derived/runtime surfaces;
- sensitive path candidate;
- unavailable secret scanner for FULL_TEXT candidates;
- high-confidence secret match;
- exact-head/tree/blob mismatch.

Large/binary artifacts remain visible as METADATA_ONLY and their source bytes are not copied into the projection.

## Determinism

The inventory contains only Git-derived stable fields.

Forbidden deterministic fields include:

- timestamps;
- hostnames;
- usernames;
- absolute local paths.

Entry order is UTF-8 bytewise source-path order.

Inventory digest is SHA-256 over canonical JSON entry dictionaries.

## Relationship to semantic classification

P5-B does not alter P1 semantic rules.

In particular:

    path / selection zone
        ≠ semantic role
        ≠ qualification
        ≠ scientific status
        ≠ authority

METADATA_ONLY body content cannot enter semantic classification without a separately qualified parser.

## Non-authorizations

P5-B does not authorize:

- runtime dynamic inventory implementation;
- continuous observer execution;
- Vault writes;
- projection rebuild;
- semantic-classifier modification;
- mutation of the historical pilot inventory.

## Required persisted local re-break

Before P5-B closes PASS:

1. recover exact persisted P5-B HEAD using LF-preserving checkout;
2. run the targeted P5-B contract breakers with Python bytecode writing disabled;
3. run the complete Obsidian projection test suite with bytecode writing disabled;
4. require no tracked-file changes;
5. require no unexpected untracked artifacts.

No separate `py_compile` step is required: importing and executing the targeted/full unittest suites parses the module while avoiding the P5-A bytecode-residue mistake.

## Next boundary after PASS

    P5-B2 — DYNAMIC INVENTORY IMPLEMENTATION CANDIDATE

P5-B2 will implement and adversarially test the inventory builder against synthetic mutants and the current real Git HEAD.

## Current verdict

**P5-B CONTRACT CANDIDATE PERSISTED — LOCAL RE-BREAK REQUIRED**

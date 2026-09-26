# OBSIDIAN P5-B2 — DYNAMIC INVENTORY IMPLEMENTATION PREFLIGHT

Date: 2026-09-26

## Scope

P5-B2 implements the qualified P5-B dynamic exact-HEAD inventory contract.

This phase remains read-only toward the canonical repository and does not write the Obsidian Vault or projection.

## Qualified predecessor

P5-B qualification:

    7a608a65914d7940bc168fbadb27acb357f0f4ef

## Candidate branch

    feat/obsidian-projection-p5b2-dynamic-inventory-implementation-v0.1

## Persisted implementation artifacts

Implementation:

    tools/obsidian_projection/dynamic_inventory.py
    blob: 5f6ed61f36e889dc27ef14ef09467ada9f9f0f58

CLI:

    tools/obsidian_projection/p5b2_verify.py
    blob: bd8d52fdd5fa42fff710cf5426d1c401e6fdb5bf

Unit tests:

    tests/obsidian_projection/test_dynamic_inventory.py
    blob: 91135860adf9a353617013bf2f38ab118858f598

Adversarial breakers:

    tests/obsidian_projection/test_p5b2_adversarial.py
    blob: 785fbe8bacb120541dc2487d83b5e4a7a1c51a42

## Contract binding

The implementation pins the qualified P5-B contract blob:

    80729156f4ac51b760c4347f581f052a175b88b3

It reuses the previously qualified read-only exact Git-object boundary:

    tools/obsidian_projection/git_source.py

The implementation does not enumerate the working tree.

## Runtime behavior

Given:

- repository root containing the exact Git objects;
- exact source HEAD;
- exact source tree;
- observed remote HEAD;

the builder:

1. verifies repository identity;
2. verifies commit/tree identity;
3. requires source HEAD == observed remote HEAD;
4. enumerates the exact Git tree;
5. blocks symlink/gitlink/unsupported modes;
6. blocks derived/runtime tracked surfaces;
7. blocks sensitive-path candidates without logging the plaintext path;
8. assigns a provenance-only selection zone;
9. assigns FULL_TEXT or METADATA_ONLY;
10. reads FULL_TEXT candidate bytes only;
11. verifies raw FULL_TEXT length;
12. converts invalid UTF-8 or NUL-bearing candidates to METADATA_ONLY;
13. runs pinned high-confidence secret scanning on valid FULL_TEXT;
14. emits deterministic inventory metadata;
15. computes the inventory SHA-256 digest.

## High-confidence secret scan V0.1

Pinned scanner identity:

    ATDS_HIGH_CONFIDENCE_SECRET_SCAN_V0_1

Initial high-confidence signatures:

- private-key PEM/OpenSSH header;
- AWS access-key identifier shape;
- GitHub classic-token shape;
- GitHub fine-grained-token shape.

The scanner reports only rule IDs and SHA-256(path), never matched secret values.

The current canonical repository was searched for these signature families during preflight and no matching code-search result was observed.

This search is supplementary evidence, not a replacement for the runtime exact-blob scanner.

## Non-write design

Neither the implementation nor CLI contains a file-write pathway for:

- Vault;
- generated projection;
- views;
- .obsidian;
- canonical source.

The CLI emits inventory or summary JSON to stdout only.

## Synthetic breaker coverage

The unit/adversarial suite covers at least:

- ordinary text inventory;
- unknown-zone preservation;
- root files;
- executable regular blobs;
- >1 MiB metadata-only behavior without body read;
- non-allowlisted binary metadata-only behavior;
- invalid UTF-8;
- NUL byte;
- raw-length mismatch;
- private-key secret detection and non-disclosure;
- sensitive path and root sensitive directory;
- generated/runtime cache surfaces;
- symlink;
- gitlink;
- wrong repository;
- wrong branch;
- wrong observed HEAD;
- duplicate path;
- backslash path;
- parent traversal;
- deterministic UTF-8 ordering;
- order-independent digest;
- no host volatility;
- summary counts;
- static absence of write primitives;
- static absence of Git mutation commands;
- static absence of Vault mutation surface.

## Real-HEAD qualification requirement

After persisted local synthetic/full-suite re-break PASS, P5-B2 must run once against the then-current remote:

    origin/integration/system-v1

The real run must resolve the remote HEAD at execution time rather than assuming the design-time HEAD is still current.

If the remote HEAD remains:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

then the implementation is expected to reproduce the design census:

    source_blob_count    908
    full_text_count      890
    metadata_only_count   18

If the remote HEAD has advanced, different counts are allowed and must be adjudicated against that exact new tree rather than treated as a failure merely because the historical census changed.

## P5-B2 non-authorizations

P5-B2 does not authorize:

- continuous polling;
- background observer;
- Vault writes;
- projection promotion;
- atomic generation swap;
- semantic classifier changes;
- machine-live visual generation.

## Qualification sequence

Required before P5-B2 PASS:

1. exact persisted P5-B2 HEAD control clone with LF-preserving checkout;
2. targeted P5-B2 unit tests;
3. targeted P5-B2 adversarial breakers;
4. full Obsidian projection suite;
5. source-clean control clone;
6. fetch current `integration/system-v1` into the isolated control clone;
7. resolve exact remote source HEAD and tree;
8. run P5-B2 summary against that exact HEAD;
9. adjudicate summary against the exact source tree.

## Current verdict

**P5-B2 IMPLEMENTATION CANDIDATE PERSISTED — LOCAL + REAL-HEAD QUALIFICATION REQUIRED**

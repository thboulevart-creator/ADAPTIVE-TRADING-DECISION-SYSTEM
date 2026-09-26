# OBSIDIAN P4-B — NATIVE VIEW BUNDLE PREFLIGHT

Date: 2026-09-26

## Purpose

P4-B implements the first native human-facing navigation bundle authorized by qualified P4-A.

P4-B is separate from P2/P3 and may write only the previously empty human-owned `views/` subtree after its own persisted local re-break passes.

## Predecessor

Qualified P4-A closure:

    ea809bc2aa9f2d9d80b0b1e5854b52b48799c872

## Candidate branch

    feat/obsidian-projection-p4b-native-view-bundle-v0.1

## Candidate implementation identity

Native view bundle module:

    tools/obsidian_projection/native_view_bundle.py
    blob: bd5b9ea6a7a5ed216e59b317fa9d105c2745343b

CLI:

    tools/obsidian_projection/p4b_verify.py
    blob: 694b773ef02d90fd2947be6f8464fd91f49d476c

Unit tests:

    tests/obsidian_projection/test_native_view_bundle.py
    blob: 1e626fe7ffc72409da65396ea9595f62fe2dcf51

Adversarial breakers:

    tests/obsidian_projection/test_p4b_adversarial.py
    blob: 7691b24ceca49c872d86fd5e45d4294fbd2c29c3

## Projection binding

P4-B is bound to:

    generated_file_count = 92

    projection_tree_digest_sha256 =
    bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0

P4-B also pins the qualified P4-A contract blob:

    699cbaf60141d8ecbb4f7f1afad214b6dd51f92b

## Exact initial bundle

P4-B may create exactly seven files:

    views/HOME.md
    views/dashboards/PROJECT-SNAPSHOT.md
    views/dashboards/QUALIFICATION-STATUS.md
    views/maps/SYSTEM-ARCHITECTURE.md
    views/maps/GOVERNANCE.md
    views/maps/RESEARCH-LIFECYCLE.md
    views/canvas/ATDS-OVERVIEW.canvas

The Markdown layer is snapshot-bound and explicitly non-authoritative.

The Canvas is native Obsidian JSON and uses unlabeled navigation edges only.

## Pre-write guards

Real Vault seeding requires:

- Windows runtime;
- exact qualified Vault path;
- Obsidian fully closed;
- P4-A contract blob exact;
- `views/` exists and is empty;
- `generated/` exists;
- `.obsidian/` exists after qualified first open;
- no `.git` inside the Vault;
- generated file count exactly 92;
- generated projection digest exact;
- repository state snapshot;
- generated tree snapshot;
- `.obsidian/` tree snapshot.

## Write semantics

The implementation:

- creates only the three required subdirectories under `views/`;
- uses exclusive-create mode `xb` for every view file;
- never overwrites an existing human file;
- does not write `generated/`;
- does not write `.obsidian/`;
- does not launch Obsidian;
- does not enable plugins;
- does not enable Sync;
- does not require Dataview or any external network service.

## Post-write verification

A successful seed requires:

- exact seven-file path set;
- exact byte equality with the in-memory bundle;
- per-file size/SHA-256 manifest;
- native-safe regular-file state for each seeded file;
- generated tree byte equality before/after;
- unchanged projection digest;
- unchanged `.obsidian/` tree digest;
- unchanged repository branch/HEAD/status.

## Failure semantics

An unexpected pre-existing human view blocks the seed.

No automated overwrite or repair is authorized.

If a write fails after partial creation, the evidence is preserved for adjudication; the implementation does not recursively delete or silently retry over existing human files.

## Static remote review

The persisted candidate was statically checked for:

- exact P4-A contract pin;
- exact projection digest pin;
- exact seven view paths;
- exclusive view writes;
- empty-view guard;
- no generated write primitive;
- no Obsidian-config write primitive;
- generated before/after comparison;
- Obsidian-config before/after comparison;
- repository before/after comparison;
- Obsidian-closed requirement;
- OneDrive-native file safety check;
- VIEW/NONE authority frontmatter;
- BOUND freshness;
- unlabeled Canvas navigation edges;
- preview cannot authorize seeding;
- BLOCKED report cannot claim qualification.

Static review result: PASS.

Static review is not runtime qualification.

## Required local re-break

Before any real Vault write:

1. recover the exact persisted P4-B HEAD;
2. run `py_compile` for module, CLI and both P4-B test files;
3. run targeted P4-B unit tests;
4. run targeted P4-B adversarial breakers;
5. run the full `tests/obsidian_projection/test_*.py` suite;
6. preserve the original repository state.

Only after this re-break returns PASS may `--seed-native-views` run.

## Current verdict

**P4-B IMPLEMENTATION CANDIDATE PERSISTED — REAL VAULT WRITE NOT YET AUTHORIZED**

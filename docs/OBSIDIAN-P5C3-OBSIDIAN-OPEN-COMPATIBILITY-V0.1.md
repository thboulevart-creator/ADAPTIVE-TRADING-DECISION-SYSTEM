# OBSIDIAN P5-C3 — OBSIDIAN-OPEN SANDBOX COMPATIBILITY V0.1

Date: 2026-09-27

## 1. Purpose

P5-C3 tests the filesystem publication primitive qualified in P5-C2 while a sacrificial Vault is actually open in Obsidian.

Selected primitive:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

P5-C3 does not use the real ATDS Vault as the experiment target.

## 2. Qualified predecessor

P5-C2 qualification commit:

    33c6184d8404b6cb0f59dbb0ead68949ece27544

Session checkpoint base:

    3bd534c755c65f112d5a64c6e2bbb0fa4913589f

## 3. Protected real Vault

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

P5-C3 may only read this Vault to:

- verify the already-safe Obsidian core-plugin state;
- hash `generated/`;
- hash `views/`.

Any before/after digest change blocks P5-C3.

## 4. Sacrificial Vault

Exact target:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX

The sandbox must:

- be absent before PREPARE;
- share the qualified OneDrive root;
- never overlap the real Vault;
- contain no `.git`;
- remain sacrificial and non-authoritative.

## 5. Prepared structure

PREPARE creates:

    ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX/
    ├── .obsidian/
    │   ├── core-plugins.json
    │   └── community-plugins.json
    ├── CURRENT.md
    └── generations/
        ├── GEN_A/
        │   ├── INDEX.md
        │   ├── MANIFEST.json
        │   └── 128 Markdown notes
        └── GEN_B/
            ├── INDEX.md
            ├── MANIFEST.json
            └── 128 Markdown notes

The two generation directories become immutable after PREPARE.

## 6. Safe Obsidian configuration

PREPARE reads the already-qualified real Vault core-plugin configuration and requires Sync to be disabled.

Only the safe core-plugin state is copied to the sandbox.

The sandbox community-plugin list is explicitly initialized as:

    []

No plugin directory, theme, CSS, Sync or community plugin is authorized.

## 7. CURRENT.md

The only live publication entrypoint is:

    CURRENT.md

It contains:

- schema;
- active generation ID;
- active generation tree digest;
- one Obsidian link to the selected generation `INDEX.md`.

The update mechanism is:

    write CURRENT.tmp
        ↓
    flush + fsync
        ↓
    os.replace(CURRENT.tmp, CURRENT.md)

Direct in-place writes to `CURRENT.md` are forbidden.

## 8. PREPARE phase

Requirements:

    Obsidian closed
    sandbox absent
    real Vault digests readable
    safe Sync/plugin state
    GEN_A + GEN_B complete and validated

Initial state:

    CURRENT.md → GEN_A

PREPARE writes the same bound snapshot in two byte-identical locations outside both Vaults:

    LocalAppData primary:
    %LOCALAPPDATA%\ATDS\obsidian_projection\p5c3\snapshots

    OneDrive control-evidence backup:
    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-CONTROL-EVIDENCE\snapshots

Both copies bind the same payload SHA-256. RUN-OPEN and POST-CLOSE may use either verified copy. If the LocalAppData copy disappears, the persisted runners automatically fall back to the OneDrive control copy. If both copies are missing, execution blocks.

It never launches Obsidian.

## 8A. Guarded reset

If an earlier P5-C3 candidate already created the sacrificial Vault, the persisted reset runner may be used only with Obsidian fully closed.

It can remove only:

    ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX
    ATDS-P5C3-CONTROL-EVIDENCE
    %LOCALAPPDATA%\ATDS\obsidian_projection\p5c3

Before deleting the sandbox it verifies the expected P5-C3 structure. It never deletes the real Vault and requires the real Vault to remain present after reset.

## 9. Manual open proof

After PREPARE the user must manually:

1. open the exact sacrificial Vault in Obsidian;
2. open `CURRENT.md`;
3. make no edits;
4. enable no Sync or plugins;
5. leave Obsidian open.

RUN-OPEN requires:

    Obsidian.exe running
    .obsidian present
    workspace.json present
    workspace.json references CURRENT.md
    Sync disabled
    community plugins empty/absent

This is the strongest local evidence used by P5-C3 that the sacrificial Vault, and specifically `CURRENT.md`, is the active Obsidian workspace.

## 10. Open experiment

While Obsidian remains open:

    250 atomic CURRENT.md promotions
    GEN_A ↔ GEN_B
    final expected generation = GEN_A

Concurrent validation requires:

    >= 5000 reader samples
    >= 1 new reader sample after every promotion
    pointer write errors = 0
    mixed generation = 0
    missing entrypoint = 0
    partial generation = 0
    parse errors = 0

Obsidian process state is checked repeatedly during the experiment and again at the end.

Both immutable generation directory digests and both real-Vault digests must remain unchanged.

## 11. Manual visual acceptance

An automated filesystem/Open-process PASS is not enough.

While Obsidian is still open, the user must provide a screenshot or equivalent direct human observation showing:

    note = CURRENT.md
    active generation = GEN_A
    visible link target = generations/GEN_A/INDEX

No user edit is permitted during this check.

## 12. POST-CLOSE

Only after manual visual acceptance:

1. close Obsidian completely;
2. run post-close verification;
3. require Obsidian process absent;
4. require final CURRENT = GEN_A;
5. require both immutable generations unchanged;
6. require Sync disabled;
7. require community plugins empty/absent;
8. require real-Vault digests unchanged.

Only then can:

    obsidian_open_qualified = true
    p5c3_qualified = true

## 13. What P5-C3 does not qualify

Even a full P5-C3 PASS does not authorize:

- production continuous synchronization;
- Windows task/service registration;
- automatic observer startup;
- writes to human `views/`;
- Obsidian Sync;
- community plugins.

It also does not solve the future graph-indexing issue created by multiple immutable generations physically existing in one Vault.

Specifically P5-C3 does not claim:

    native Obsidian Graph understands CURRENT.md as generation-selection authority

That issue remains explicitly deferred to:

    P6 — CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

## 14. Next boundary

On full P5-C3 PASS:

    P5-D — CONTINUOUS OBSERVER IMPLEMENTATION CANDIDATE

P5-D may then implement the read-only GitHub HEAD observer and queue/state machine using the already-qualified dynamic inventory and publication primitive.

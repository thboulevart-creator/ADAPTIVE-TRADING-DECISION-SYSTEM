# OBSIDIAN P5-C3 — OBSIDIAN-OPEN COMPATIBILITY PREFLIGHT

Date: 2026-09-27

## Scope

P5-C3 tests the P5-C2-selected immutable-generation atomic-pointer publication mechanism while a sacrificial Vault is actually open in Obsidian.

The real user Vault is never the experiment target.

## Qualified predecessor

P5-C2 qualification commit:

    33c6184d8404b6cb0f59dbb0ead68949ece27544

Checkpoint base:

    3bd534c755c65f112d5a64c6e2bbb0fa4913589f

## Candidate branch

    feat/obsidian-projection-p5c3-obsidian-open-compatibility-v0.1

## Persisted candidate artifacts

Contract:

    tools/obsidian_projection/obsidian_open_compatibility_contract_v0_1.json
    blob: 4974302509a989fbd296ee7052ca15f22a0750a6

Harness:

    tools/obsidian_projection/obsidian_open_compatibility.py
    blob: 2255b7ce20377cbf0bead47a7e96aa2975c443f5

CLI:

    tools/obsidian_projection/p5c3_verify.py
    blob: b68440b53c07c05cde7e3aea3d6bb4d41d141b8d

Prepare/control runner:

    tools/obsidian_projection/run_p5c3_prepare_control.ps1
    blob: c5aab6ed2543c1c151c13bca19846c8aecb37c6d

Open-experiment runner:

    tools/obsidian_projection/run_p5c3_open.ps1
    blob: 2b538f4c03c72342cba78fc8a96b7d0972c0f22d

Post-close runner:

    tools/obsidian_projection/run_p5c3_post_close.ps1
    blob: 1d1d457b6fcaa518806ee027d67a02385420bcdf

Reset runner:

    tools/obsidian_projection/run_p5c3_reset.ps1
    blob: ffce2b32c556a0581c5b3caf6fd97b80996556de

Contract breakers:

    tests/obsidian_projection/test_obsidian_open_compatibility_contract_v0_1.py
    blob: 0fd820812922f2c25e42b98c796dc594ae075423

Unit tests:

    tests/obsidian_projection/test_obsidian_open_compatibility.py
    blob: 05154a9fe3be7c61b066a2f12067408b26f16d44

Adversarial breakers:

    tests/obsidian_projection/test_p5c3_adversarial.py
    blob: a3fa766aa09ec6eb6550e165355dedd441e07421

Protocol documentation:

    docs/OBSIDIAN-P5C3-OBSIDIAN-OPEN-COMPATIBILITY-V0.1.md
    blob: ee4264f3011beb39545e08decea23cacbd25804e

Inherited P5-C2 regression test stabilized in P5-C3:

    tests/obsidian_projection/test_promotion_experiment.py
    blob: f2ffaa3d1c975d6fc026607f9946602b207a25b4

The qualified P5-C2 implementation itself remains unchanged:

    tools/obsidian_projection/promotion_experiment.py
    blob: b5ba13a6aa9ddf1690842aafea422973e15cdf2d

The inherited unit test now uses a deterministic reader harness for its synthetic logic check. The real concurrency claim remains grounded in the already persisted P5-C2 empirical experiment (250/250 promotions, 5001 reader samples, zero anomalies).

## Snapshot persistence correction

The first P5-C3 PREPARE execution established a valid historical PREPARE state, but the single LocalAppData snapshot directory was later reported absent before RUN-OPEN.

The current candidate therefore supersedes that single-copy assumption.

PREPARE now writes the same bound snapshot to two byte-identical locations:

    %LOCALAPPDATA%\ATDS\obsidian_projection\p5c3\snapshots

and:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-CONTROL-EVIDENCE\snapshots

Both copies bind the same payload SHA-256.

RUN-OPEN and POST-CLOSE may use either verified copy. The persisted PowerShell runners automatically fall back to the OneDrive control copy when the LocalAppData primary is missing.

Both copies missing => BLOCKED.

Content-addressed snapshot reuse rule:

- existing digest path + byte-identical envelope => REUSE / allowed;
- existing digest path + different bytes => BLOCKED.

This prevents a deterministic rerun of PREPARE from being falsely classified as a collision.

The earlier PREPARE PASS report is retained as historical evidence but explicitly marked superseded for current execution:

    reports/program/2026-09-27-OBSIDIAN-P5C3-PREPARE-PASS.md
    blob: b59317214177de571d795b7e0bb76f5ce5c07136

A fresh guarded reset and PREPARE are required for this revised candidate.

## Protected live Vault

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

P5-C3 only reads:

- `generated/` for a deterministic before/after digest;
- `views/` for a deterministic before/after digest;
- the already-safe `.obsidian/core-plugins.json` as the source of the sandbox core-plugin state.

No live-Vault mutation path is authorized.

## Sacrificial open-Vault target

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX

PREPARE requires:

- Windows;
- Obsidian closed;
- sandbox absent;
- no overlap with the real Vault;
- no `.git`;
- Sync disabled in the safe source configuration;
- community plugin list empty/absent.

PREPARE does not launch Obsidian.

## Prepared fixture

The sandbox contains:

- one atomic `CURRENT.md` entry note;
- immutable `GEN_A`;
- immutable `GEN_B`;
- 128 Markdown notes per generation;
- 8 nested directories per generation;
- one `INDEX.md` per generation;
- one deterministic manifest per generation;
- safe sandbox `.obsidian/` seed.

Initial state:

    CURRENT.md -> GEN_A

## Open proof

Before RUN-OPEN:

- Obsidian.exe must be running;
- the sandbox `.obsidian/workspace.json` must exist;
- workspace state must reference `CURRENT.md`;
- Sync must still be disabled;
- community plugins must remain empty/absent;
- no `.obsidian` subdirectory is accepted.

The harness checks Obsidian process state at the beginning, during the promotion sequence, and again at the end.

## Open experiment

The only mutable semantic entrypoint is:

    CURRENT.md

Publication primitive:

    CURRENT.tmp write
      -> flush
      -> fsync
      -> os.replace(CURRENT.tmp, CURRENT.md)

Required scale:

    250 atomic pointer promotions
    >= 5000 concurrent reader samples
    >= 1 fresh reader sample after every promotion

Required anomalies:

    pointer write errors = 0
    mixed generation = 0
    missing entrypoint = 0
    partial generation = 0
    parse errors = 0

Expected final state:

    GEN_A

The two generation directories must remain byte-identical to their PREPARE snapshot.

The real Vault `generated/` and `views/` digests must also remain unchanged.

## Manual visual gate

An automated PASS does not close P5-C3.

While Obsidian is still open, the user must provide direct visual evidence showing:

    CURRENT.md
    Active generation: GEN_A
    link -> generations/GEN_A/INDEX

Only after this human-visible result is accepted may the user close Obsidian and execute POST-CLOSE with the manual-acceptance flag.

## POST-CLOSE

POST-CLOSE requires:

- Obsidian fully closed;
- explicit manual-visual-acceptance flag;
- final CURRENT = GEN_A;
- immutable generation digests unchanged;
- Sync disabled;
- community plugins empty/absent;
- real Vault digests unchanged.

Only POST-CLOSE PASS may establish:

    obsidian_open_qualified = true
    p5c3_qualified = true

It still leaves:

    production_promotion_authorized = false
    continuous_observer_authorized = false
    graph_current_pointer_semantics_qualified = false

## Graph-indexing limitation remains open

P5-C3 does not solve the fact that native Obsidian Graph/Search may index both immutable generations physically present in a Vault.

No claim is made that native Graph understands `CURRENT.md` as selection authority.

This remains explicitly deferred to P6.

## Required local qualification sequence

1. exact LF-preserving control clone of the persisted P5-C3 HEAD;
2. targeted P5-C3 tests;
3. full Obsidian projection suite;
4. source-clean clone;
5. P5-C3 PREPARE;
6. manual open of the sacrificial Vault and `CURRENT.md`;
7. RUN-OPEN;
8. manual screenshot/visual acceptance;
9. close Obsidian;
10. POST-CLOSE.

## Current verdict

**P5-C3 CANDIDATE PERSISTED — LOCAL RE-BREAK + MANUAL OPEN EXPERIMENT REQUIRED**

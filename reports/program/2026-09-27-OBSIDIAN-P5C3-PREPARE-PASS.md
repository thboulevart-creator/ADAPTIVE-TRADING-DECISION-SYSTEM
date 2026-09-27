# OBSIDIAN P5-C3 — PREPARE PASS

Date: 2026-09-27

## Persisted candidate

Branch:

    feat/obsidian-projection-p5c3-obsidian-open-compatibility-v0.1

Candidate HEAD:

    1c47c377ed55ac38fedc32e71a33303272482c78

## User-reported local execution

The user reported:

    Ran 529 tests in 9.470s
    OK
    P5C3_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS

PREPARE report:

    schema =
      ATDS_OBSIDIAN_P5C3_PREPARE_REPORT_V0_1

    status = PASS

    automatic_obsidian_launch = false

    initial_generation = GEN_A

    live_vault_modified = false

Sacrificial Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX

Snapshot:

    C:\Users\Boulevart\AppData\Local\ATDS\obsidian_projection\p5c3\snapshots\p5c3-open-snapshot-bf2b9a1e817b35abdb550375970f21f84fd65de56590abf925aec329b0468b3b.json

Snapshot token:

    bf2b9a1e817b35abdb550375970f21f84fd65de56590abf925aec329b0468b3b

## Qualification meaning

P5-C3 PREPARE is qualified for the next manual-open boundary.

This does not yet qualify Obsidian-open behavior.

## Next exact action

The user must manually:

1. open the exact sacrificial Vault in Obsidian;
2. open CURRENT.md;
3. make no edits;
4. enable no Sync or plugins;
5. leave Obsidian open.

Only after that may RUN-OPEN execute against the preserved snapshot above.


## Supersession

This PREPARE PASS remains valid as historical evidence for the earlier P5-C3 candidate.

It is **SUPERSEDED FOR CURRENT EXECUTION** because the single-copy snapshot persistence assumption failed after PREPARE: the entire LocalAppData snapshot directory was later reported absent before RUN-OPEN.

The P5-C3 candidate was subsequently revised to require two byte-identical bound snapshot copies:

- LocalAppData primary;
- OneDrive control-evidence backup outside both Vaults.

Therefore this historical PREPARE result must not be reused for the revised candidate. A fresh guarded reset and PREPARE are required.

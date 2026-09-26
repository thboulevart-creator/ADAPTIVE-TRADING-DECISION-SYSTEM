# OBSIDIAN P3-D2 — FIRST-OPEN QUALIFICATION

Date: 2026-09-26

## Scope

This record closes the governed first-open verification for the OneDrive Vault:

`C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION`

Source repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

P3-D2 implementation branch:

`feat/obsidian-projection-p3d2-onedrive-first-open-harness-v0.2`

Persisted P3-D2 harness implementation remained byte-identical during the breaker corrections.

## Pre-open qualification

The user reported a persisted local re-break with:

- 249 tests executed
- result: `OK`
- marker: `P3D2_PERSISTED_LOCAL_REBREAK_PASS`
- control worktree clean

The subsequent P3-D2 prepare report returned:

- schema: `ATDS_OBSIDIAN_P3D2_PREPARE_REPORT_V0_2`
- status: `PASS`
- `first_open_authorized: true`
- generated file count: `92`
- projection tree digest SHA-256:
  `bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0`
- snapshot authorization token:
  `3c02cff164d86be04ee0728c131438f26475ab27c74ecf6ec75b8d6efc680014`
- automatic Obsidian launch: `false`
- Vault modified by prepare: `false`

## First-open observation and remediation

The user manually opened the exact Vault in Obsidian and closed it.

The first post-close verification correctly returned `BLOCKED` because Obsidian had written `"sync": true` into `.obsidian/core-plugins.json`.

A separate adjudication authorized one bounded remediation only: manually disable the core Sync plugin while leaving the deterministic projection and views unchanged.

No relaxation of the P3-C2 contract was authorized.

## Final post-close verification

After the bounded remediation, the user reported:

- `OBSIDIAN_SYNC_DISABLED=PASS`
- schema: `ATDS_OBSIDIAN_P3D2_VERIFY_REPORT_V0_2`
- status: `PASS`
- `first_open_qualified: true`
- `community_plugins_enabled: false`
- `obsidian_sync_enabled: false`
- generated file count: `92`
- `generated_modified_by_harness: false`
- projection tree digest SHA-256:
  `bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0`
- `repository_state_preserved: true`
- snapshot authorization token:
  `3c02cff164d86be04ee0728c131438f26475ab27c74ecf6ec75b8d6efc680014`
- `vault_written_by_harness: false`
- `views_entry_count: 0`
- `views_modified_by_harness: false`

Post-open `.obsidian/` state reported:

- directory present
- four root JSON files only:
  - `app.json`
  - `appearance.json`
  - `core-plugins.json`
  - `workspace.json`
- subdirectory count: `0`
- community plugins disabled
- Obsidian Sync disabled

Generated and `.obsidian/` files were accepted under the qualified OneDrive file policy, with the final verification observing `NO_REPARSE_POINT` for the inspected files and no directory reparse points, offline files, sparse files, symlink/junction files, or unreadable files.

## Disposition

**PASS — P3-D2 FIRST OPEN QUALIFIED**

This PASS is limited to the first-open safety boundary. It establishes that the exact OneDrive Vault was opened manually and subsequently verified without mutation of the deterministic generated projection, without views changes, without repository-state change, without community plugins, and with Obsidian Sync disabled.

It does not authorize:

- treating Obsidian as canonical truth;
- writes to `generated/`;
- Git automation from the Vault;
- Obsidian Sync;
- community plugins;
- semantic authority for `.obsidian/`;
- unreviewed changes to projection architecture.

## Evidence status

Runtime evidence in this record is **USER-REPORTED LOCAL EXECUTION**. GitHub persistence of this record does not convert that runtime evidence into independent execution evidence.

## Closure

P3-D2 first-open safety boundary is closed PASS.

Any next phase must start from a new explicit gate and must preserve the established authority boundary:

GitHub/ATDS canonical → Obsidian projection derived/non-authoritative.

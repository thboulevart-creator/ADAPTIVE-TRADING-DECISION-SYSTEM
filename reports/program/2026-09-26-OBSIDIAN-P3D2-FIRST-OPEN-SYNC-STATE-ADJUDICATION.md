# OBSIDIAN P3-D2 — FIRST-OPEN SYNC STATE ADJUDICATION

Date: 2026-09-26

## Scope

This adjudication concerns only the first-open P3-D2 post-close BLOCKED state observed for the OneDrive Vault:

`C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION`

It does not alter P3-B, P3-C2, the deterministic generated projection, or the P3-D2 harness implementation.

## Observed evidence

User-reported post-close verification returned:

- schema: `ATDS_OBSIDIAN_P3D2_BLOCKED_REPORT_V0_2`
- status: `BLOCKED`
- error: `Obsidian Sync core plugin enabled`
- first_open_qualified: `false`
- vault_written_by_harness: `false`

A read-only listing of `.obsidian/` then reported exactly four root JSON files:

- `app.json`
- `appearance.json`
- `core-plugins.json`
- `workspace.json`

No `community-plugins.json` or plugin subdirectory was reported.

The reported `core-plugins.json` contains the boolean mapping:

`"sync": true`

## Contract interpretation

P3-C2 explicitly states:

- `obsidian_sync_authorized: false`
- `obsidian_sync_enablement_forbidden: true`
- acceptance breaker: `Obsidian Sync enabled`

Therefore the BLOCKED result is correct under the persisted contract.

The contract is not relaxed merely because Obsidian created this state on first open.

## Adjudication

Disposition: **REMEDIATION AUTHORIZED — CONTRACT UNCHANGED**

The observed state is treated as an Obsidian UI-configuration incompatibility with the preregistered first-open policy, not as evidence that generated projection bytes changed.

Exactly one remediation is authorized:

1. Reopen the exact OneDrive Vault manually in Obsidian.
2. Change only the core-plugin setting for **Sync** from enabled to disabled.
3. Do not edit any note or generated artifact.
4. Do not modify `views/`.
5. Do not enable or install community plugins.
6. Do not enable Obsidian Sync or connect a remote vault.
7. Close Obsidian fully.
8. Re-run the existing P3-D2 post-close verifier against the existing pre-open snapshot.

No automated Vault mutation is authorized.

## Snapshot reuse

The existing pre-open snapshot remains the comparison baseline for the deterministic projection because the post-close verifier independently rechecks:

- repository state,
- Vault filesystem identity,
- generated relative path set,
- generated file sizes and SHA-256 values,
- build/integrity manifests,
- projection-tree digest,
- `views/` emptiness,
- fresh P2 reconstruction equality.

The remediation is confined to non-semantic Obsidian UI configuration under `.obsidian/`.

If any deterministic or governed state differs during the retry, verification remains BLOCKED.

## Authority boundary

This adjudication does not qualify the first open.

Qualification remains conditional on a subsequent persisted-harness post-close report with:

- `status: PASS`
- `first_open_qualified: true`

No success claim is authorized before that report.

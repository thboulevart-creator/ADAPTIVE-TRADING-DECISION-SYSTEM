# OBSIDIAN P3-C — FIRST-OPEN SAFETY CONTRACT V0.1

Status: **CANDIDATE PREREGISTRATION ONLY**

Qualified P3-B HEAD: `bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba`

Materialized Vault:

    C:\Users\Boulevart\AppData\Local\ATDS-OBSIDIAN-PROJECTION

## 1. Purpose

P3-C defines the safety boundary for the first time Obsidian is allowed to open the qualified external projection.

P3-C itself does not open Obsidian, create `.obsidian/`, or write to the Vault.

## 2. Authority model

    GitHub / ATDS = canonical truth

    materialized Vault = derived projection

    generated/ = machine-owned / deterministic / immutable during first open

    views/ = human-owned / must remain empty during first-open observation

    .obsidian/ = local Obsidian UI configuration only / no semantic authority

`.obsidian/` must never become an input to ATDS semantic truth.

## 3. Why cryptographic reconstruction is mandatory

The local terminal reached `P3B_LOCAL_MATERIALIZATION_PASS`, but the complete P3-B JSON report and digest values were not captured in the conversation.

Therefore the first-open boundary may not rely on undocumented digest values.

Before first open, the harness must rerun the exact qualified P2 pipeline and prove that the currently materialized `generated/` tree is byte-identical to the fresh qualified P2 BUILD A after BUILD A equals BUILD B.

Any mismatch blocks first open.

## 4. Pre-open state

Required immediately before first open:

- real Vault exists at the exact expected destination;
- `generated/` exists;
- `views/` exists and is empty;
- `.obsidian/` does not exist;
- top level is exactly `generated/` and `views/`;
- integrity manifest reports all covered generated files CLEAN;
- current `generated/` matches a fresh qualified P2 BUILD A exactly;
- Vault filesystem identity is captured;
- ATDS branch, HEAD, and status are captured.

The snapshot is stored outside the Vault under OS TEMP.

## 5. First-open execution model

The first open is deliberately manual and split into three phases:

    PREPARE
      → freeze pre-open snapshot

    HUMAN FIRST OPEN
      → open this exact Vault in Obsidian
      → make no content edits
      → do not edit views/
      → do not alter generated/
      → close Obsidian fully

    VERIFY
      → compare post-close state to pre-open snapshot

The harness must not launch Obsidian automatically.

Post-check while Obsidian is still running is BLOCKED.

## 6. What `.obsidian/` may contain after first open

The first-open policy is intentionally narrow.

Allowed:

- `.obsidian/` directory itself;
- regular root-level JSON configuration/state files created by Obsidian.

Forbidden during the first-open qualification:

- root-level non-JSON files;
- any `.obsidian/` subdirectory;
- `.obsidian/plugins/`;
- `.obsidian/themes/`;
- `.obsidian/snippets/`;
- symlinks, junctions, reparse points, or non-regular files.

`community-plugins.json` is allowed only if absent or a valid empty JSON array.

`core-plugins.json` is allowed only if its structure can be interpreted and the core Sync plugin id `sync` is not enabled.

Any additional path whose filename or directory name case-insensitively indicates Sync is BLOCKED during first-open qualification.

This policy is deliberately conservative. If Obsidian creates a legitimate new configuration shape outside this contract, the result is BLOCKED for review rather than silently accepted.

## 7. `generated/` before/after gate

After Obsidian is fully closed:

- exact relative-path set must match the pre-open snapshot;
- exact file sizes must match;
- exact SHA-256 for every file must match;
- projection-tree digest must match;
- build manifest must be unchanged;
- integrity manifest must verify all entries CLEAN.

Any byte change means first-open qualification fails.

No automatic repair is authorized.

## 8. `views/` before/after gate

`views/` must contain zero entries before and after the first open.

The first opening is observation only; human view authoring begins only after the first-open boundary is qualified.

## 9. Vault structure after first open

Allowed top-level entries after closing Obsidian:

    generated/
    views/
    .obsidian/

`.git/` inside the Vault is forbidden.

Any other top-level entry blocks first-open qualification.

The Vault filesystem identity must remain the same as before opening.

## 10. Repository before/after gate

ATDS must remain unchanged:

- same branch;
- same HEAD;
- same `git status --porcelain` output.

Any change blocks qualification.

## 11. Failure protocol

On any first-open anomaly:

- do not reopen Obsidian;
- do not auto-repair `generated/`;
- do not auto-delete unexpected `.obsidian/` state;
- preserve evidence for adjudication;
- report BLOCKED.

## 12. Qualification

Opening Obsidian is not a PASS.

Creation of `.obsidian/` is not a PASS.

The folder name is not a PASS.

First-open PASS exists only after the external post-close verifier passes every registered gate.

## 13. P3-C prohibition

During this preregistration step:

- no Obsidian launch;
- no `.obsidian/` creation;
- no Vault writes;
- no generated writes;
- no views writes;
- no plugin installation;
- no Sync;
- no Git automation.

## 14. Next gate

After persisted re-break, the only next action is:

    P3D_FIRST_OPEN_SAFETY_HARNESS_IMPLEMENTATION_CANDIDATE

That harness may prepare a pre-open snapshot and perform a post-close verification. It still may not launch Obsidian itself.

## 15. Candidate verdict

**READY FOR PERSISTED FIRST-OPEN CONTRACT RE-BREAK ONLY.**

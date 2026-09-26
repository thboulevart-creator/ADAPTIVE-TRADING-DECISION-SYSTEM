# OBSIDIAN P3-C2 — ONEDRIVE FIRST-OPEN SAFETY CONTRACT V0.2

Status: **CANDIDATE PREREGISTRATION ONLY**

Predecessor P3-C HEAD: `fa1e24e20acbfba60de2c3ebaaa7dc5427778851`

Predecessor P3-D HEAD: `3cafa6e98ec45236aba48ddf60e55957e49bed76`

Qualified P3-B HEAD: `bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba`

Qualified P2-B HEAD: `157b519dafb226e53ae13a281f7dc294d584cc0d`

New materialized Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

## 1. Purpose

P3-C2 supersedes the destination assumptions of P3-C V0.1 for the first-open boundary only.

It does not rewrite P3-C V0.1, P3-D V0.1, P3-B, P2, or any earlier record.

The reason for this successor is a human-directed relocation of both the local ATDS worktree and the derived Obsidian projection under OneDrive.

The canonical truth remains GitHub / ATDS. The Vault remains a derived projection.

## 2. Evidence available before preregistration

The following results are treated as **REPORTED LOCAL EXECUTION EVIDENCE**, not as remote execution performed by GitHub:

- relocated Vault exists at the exact OneDrive path above;
- top level is exactly `generated/` and `views/`;
- `.obsidian/` is absent;
- `views/` contains zero entries;
- generated file count is exactly 92;
- integrity-manifest SHA-256 is
  `a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b`;
- deterministic projection-tree entry count is 91;
- projection-tree digest SHA-256 is
  `bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0`;
- no generated file was reported offline, sparse, unreadable, symlinked, or junctioned;
- native Windows `fsutil reparsepoint query` classified all 92 generated files as reparse points;
- all 92 native queries returned the same tag:
  `0x9000601A`.

Microsoft documents `0x9000601A` as `IO_REPARSE_TAG_CLOUD_6`, used by the Windows Cloud Files filter for files managed by a synchronization engine such as OneDrive.

This semantic classification is an external platform fact. The actual local condition still has to be checked by the future P3-D2 harness at runtime.

## 3. Why generic reparse rejection cannot be retained unchanged

P3-C V0.1 deliberately rejected any reparse point because the original Vault was outside synchronization infrastructure.

That rule was correct for the original threat model.

After relocation under OneDrive, the same generic rule rejects the entire generated tree even though:

- cryptographic file content is unchanged;
- no symlink is present;
- no junction is present;
- no generated file is offline;
- no generated file is sparse;
- every generated file is readable;
- the native reparse tag is uniformly Cloud Files `CLOUD_6`.

P3-C2 therefore narrows the rule rather than removing it.

## 4. Reparse policy V0.2

For **regular files only**, the candidate allowed classes are:

    NO_REPARSE_POINT

or

    IO_REPARSE_TAG_CLOUD_6 = 0x9000601A

This is not a generic permission for OneDrive metadata.

The following remain forbidden:

- every other reparse tag;
- symlinks;
- junctions;
- mount points;
- directory reparse points;
- offline files;
- sparse files;
- unreadable files.

A change between ordinary regular-file state and `CLOUD_6` metadata is not itself a semantic change, but it is acceptable only when every content-integrity and structural gate also passes.

## 5. Host sync versus Obsidian Sync

P3-C2 distinguishes two unrelated mechanisms.

### Host storage environment

The Vault is intentionally located under the user's OneDrive Cloud Files environment.

This bounded host-storage condition is accepted as an execution environment candidate.

### Obsidian Sync

Obsidian Sync remains forbidden.

The future first-open verifier must block:

- core plugin id `sync` when enabled;
- explicit Sync configuration artifacts outside the registered exception;
- any ambiguity about whether Obsidian Sync is enabled.

The presence of OneDrive does not authorize Obsidian Sync.

## 6. Authority model

    GitHub / ATDS = canonical truth

    OneDrive Vault = derived projection

    generated/ = machine-owned deterministic projection

    views/ = human-owned, zero entries during first-open qualification

    .obsidian/ = Obsidian UI configuration only, no semantic authority

Cloud Files metadata never becomes semantic truth and never creates qualification.

## 7. Pre-open cryptographic gate

Before the manual first open, P3-D2 must reconstruct the exact qualified P2 projection.

The following must still hold:

- qualified P2 identity is exact;
- BUILD A and BUILD B are byte-identical;
- current generated relative-path set equals fresh BUILD A;
- every generated file size matches;
- every generated file SHA-256 matches;
- integrity manifest verifies CLEAN;
- build manifest identity matches;
- projection-tree digest equals
  `bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0`;
- generated file count is 92;
- integrity-manifest SHA-256 equals
  `a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b`.

Any mismatch blocks first open.

## 8. Pre-open native filesystem gate

The future P3-D2 harness must inspect native Windows filesystem state.

It must not rely only on Python `Path.is_symlink()`, `st_reparse_tag`, or PowerShell's generic `Attributes` field.

The gate must establish:

- file readability;
- not offline;
- not sparse;
- no symlink;
- no junction;
- no directory reparse point;
- any file reparse tag is either absent or exactly `0x9000601A`.

Unexpected or unclassifiable native reparse state means BLOCKED.

## 9. Pre-open snapshot

The external snapshot remains stored under OS TEMP, outside the Vault.

It must include the previous P3-C fields plus a summary of the generated-file native reparse classification.

The snapshot must not modify deterministic Vault bytes.

## 10. First-open execution model

The execution model remains:

    PREPARE
      -> freeze external snapshot

    HUMAN FIRST OPEN
      -> open the exact OneDrive Vault manually
      -> make no content edits
      -> do not edit generated/
      -> do not edit views/
      -> do not enable plugins or Sync
      -> fully close Obsidian

    VERIFY
      -> compare post-close state to the snapshot

The harness must never launch Obsidian automatically.

## 11. .obsidian policy under OneDrive

Obsidian may create `.obsidian/` during the authorized manual first open.

Only regular root-level JSON files are candidates for acceptance.

A regular JSON file may be either:

- an ordinary non-reparse regular file; or
- a `CLOUD_6` regular file with native tag `0x9000601A`.

Still forbidden:

- subdirectories;
- `.obsidian/plugins/`;
- `.obsidian/themes/`;
- `.obsidian/snippets/`;
- non-JSON root files;
- symlinks;
- junctions;
- directory reparse points;
- any other file reparse tag;
- offline files;
- sparse files;
- unreadable files.

`community-plugins.json` is allowed only if absent or a valid empty JSON array.

`core-plugins.json` is allowed only when interpretable and core plugin id `sync` is not enabled.

## 12. Generated before/after gate

Generated semantic content remains byte-governed.

After Obsidian closes:

- exact generated relative paths must match;
- sizes must match;
- per-file SHA-256 must match;
- projection-tree digest must match;
- build manifest must be unchanged;
- integrity manifest must remain CLEAN;
- native filesystem state must remain inside the P3-C2 allowlist.

A OneDrive metadata transition between no-reparse and `CLOUD_6` is not by itself a content mutation.

Any byte mutation is BLOCKED.

## 13. Repository gate

The local ATDS repository must preserve:

- branch;
- HEAD;
- `git status --porcelain`.

A repository change during first-open qualification is BLOCKED.

The fact that the local worktree is also under OneDrive does not change GitHub's canonical authority.

## 14. Failure protocol

No automatic repair is authorized.

On anomaly:

- do not reopen Obsidian;
- do not auto-restore generated files;
- do not auto-delete `.obsidian/`;
- do not normalize reparse metadata;
- preserve evidence;
- report BLOCKED for adjudication.

## 15. P3-C2 prohibition

During this preregistration:

- no Obsidian launch;
- no `.obsidian/` creation;
- no Vault write;
- no generated write;
- no views write;
- no community plugin installation;
- no Obsidian Sync;
- no Git automation.

## 16. Next gate

Only after persisted P3-C2 re-break may the next candidate be created:

    P3D2_ONEDRIVE_FIRST_OPEN_SAFETY_HARNESS_IMPLEMENTATION_CANDIDATE

P3-D2 may implement:

- native reparse classification;
- fresh P2 reconstruction;
- external pre-open snapshot;
- post-close verification.

It still may not launch Obsidian or edit the Vault.

## 17. Candidate verdict

**READY FOR PERSISTED P3-C2 CONTRACT RE-BREAK ONLY.**

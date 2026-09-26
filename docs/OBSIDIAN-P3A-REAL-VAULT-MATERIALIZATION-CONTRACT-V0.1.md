# OBSIDIAN P3-A — REAL VAULT MATERIALIZATION CONTRACT V0.1

Status: **CANDIDATE PREREGISTRATION ONLY**

Qualified P2-B HEAD: `157b519dafb226e53ae13a281f7dc294d584cc0d`
Frozen ATDS source commit: `7bd8c1312430dfc3def5523eb65397a5d6a5ae05`
Frozen source tree: `66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b`
Pilot artifact count: **74**

## 1. Purpose

P3-A defines how a previously qualified deterministic P2 projection may later be materialized as the first real external Vault.

P3-A itself does not materialize anything. It authorizes documentation and breakers only.

## 2. Exact destination

Candidate destination expression:

    %LOCALAPPDATA%\ATDS-OBSIDIAN-PROJECTION

Observed resolved destination on the qualified workstation:

    C:\Users\Boulevart\AppData\Local\ATDS-OBSIDIAN-PROJECTION

The final destination must still be absent when the materialization attempt starts.

Required destination properties:

- NTFS;
- final Vault outside the ATDS repository;
- ATDS repository outside the Vault;
- no known sync-root containment;
- no reparse, junction or symlink ancestor ambiguity;
- exact normalized destination identity.

Any ambiguity blocks.

## 3. A TEMP path is not authority

An arbitrary folder produced in TEMP is not sufficient evidence that it is a qualified P2 projection.

The future materializer must run a fresh P2 execution using the exact qualified P2 core blobs inherited from P2-B.

The P2 execution must establish:

- status PASS;
- 74 semantic records;
- 74 artifact records;
- BUILD A byte-identical to BUILD B;
- all integrity entries CLEAN;
- no real Vault creation;
- no `.obsidian` creation.

Only BUILD A may then be selected, and only after BUILD A equals BUILD B.

The selected source is frozen by its P2 projection identity:

- semantic record digest;
- artifact-set digest;
- relation-set digest;
- integrity-manifest SHA-256;
- projection-tree digest;
- artifact count;
- relation count;
- generated-file count.

## 4. P2 implementation identity is pinned

The P3 materializer must verify the exact Git blob identities of:

- `rendering.py`;
- `relations.py`;
- `integrity.py`;
- `builder.py`;
- `p2_verify.py`.

P3 may not silently alter those qualified components and then call the new output a P2-qualified build.

## 5. Never copy directly into the final Vault name

The future materialization uses an incoming sibling under `%LOCALAPPDATA%`:

    ATDS-OBSIDIAN-PROJECTION.__INCOMING__.{projection_tree_digest_first16}

The incoming path must not already exist.

The future implementation must capture its filesystem identity immediately after exclusive creation.

If stable filesystem identity cannot be obtained, materialization blocks.

## 6. Incoming structure

The incoming directory contains exactly the copied deterministic P2 `generated/` tree plus an empty `views/` directory.

Required structure:

    generated/
      artifacts/
      relations/
      manifests/
    views/

`views/` must be empty.

`.obsidian/` must not exist.

No plugin, sync metadata or Git automation is created.

## 7. Copy semantics

Source files are copied byte-for-byte from the selected fresh qualified P2 BUILD A.

Required:

- exclusive create;
- no overwrite;
- no hard-link materialization;
- no symlink copy;
- no junction/reparse copy;
- no arbitrary TEMP files;
- no canonical repository files outside the qualified generated tree;
- no extra files.

## 8. Incoming verification before final name

The final Vault name must remain absent until the incoming directory has passed every verification.

Required incoming checks:

- exact generated relative-path set;
- exact generated file count;
- exact size for every file;
- exact SHA-256 for every file;
- regular files only;
- link count exactly 1;
- no reparse/symlink/junction;
- empty `views/`;
- absent `.obsidian/`;
- integrity manifest all CLEAN;
- build manifest matches frozen P2 projection identity;
- projection-tree digest equals qualified P2 source.

Any mismatch blocks before the final Vault name exists.

## 9. Final promotion

Promotion is one directory rename inside the same NTFS volume:

    verified incoming sibling
             ↓
    ATDS-OBSIDIAN-PROJECTION

The final target must be checked absent again immediately before rename.

Forbidden:

- replace/overwrite an existing final path;
- cross-volume promotion;
- direct copy into final;
- exposing the final name before incoming verification passes.

## 10. Post-promotion verification

A successful rename is not sufficient qualification.

After rename, the implementation must verify again:

- exact resolved destination;
- same filesystem object identity as the verified incoming directory;
- exact path set/count;
- exact sizes and hashes;
- link count 1;
- no reparse/symlink/junction;
- empty `views/`;
- absent `.obsidian/`;
- integrity manifest all CLEAN;
- build-manifest identity match;
- projection-tree digest match;
- repository branch unchanged;
- repository HEAD unchanged;
- repository working tree unchanged.

Only all checks together may produce a materialization PASS.

## 11. Failure before final rename

Before final rename, the real final destination must remain absent.

An incoming directory may be automatically cleaned only if:

- it is still under the exact expected parent;
- its filesystem identity still equals the identity captured by the current attempt;
- it is not a reparse/symlink/junction.

If identity differs, the implementation must not recursively delete it.

Cleanup uncertainty means BLOCKED, not best-effort deletion.

## 12. Failure after final rename

The final directory remains **unqualified** until post-promotion verification succeeds.

If post-promotion verification fails:

- do not open Obsidian;
- do not claim success;
- do not recursively delete automatically;
- prefer a same-volume quarantine rename to:

    ATDS-OBSIDIAN-PROJECTION.__FAILED__.{projection_tree_digest_first16}

The quarantine target must itself be absent and the final directory identity must still match the object created by this attempt.

If quarantine fails, leave the directory in place, report BLOCKED and explicitly prohibit opening it as a qualified Vault.

## 13. Crash / power-loss semantics

Folder names never prove qualification.

Interpretation after interruption:

- final absent → no qualified Vault;
- incoming present → unqualified/incomplete or unadjudicated;
- final present without external successful P3 execution record → unqualified until reverified.

## 14. Qualification is external to deterministic Vault bytes

Materialization must not mutate the deterministic `generated/` projection to insert a P3 success flag.

The build manifest proves deterministic build identity, not successful materialization.

The integrity manifest proves byte integrity, not successful materialization.

The final materialization qualification is carried by the P3 execution report and a later Git governance record.

## 15. P3-A explicit prohibitions

P3-A itself may not:

- create the final Vault;
- create the incoming sibling;
- write under `%LOCALAPPDATA%`;
- implement materialization code;
- create `.obsidian/`;
- launch Obsidian;
- install plugins;
- enable sync;
- enable Git automation;
- alter P2 core code;
- delete any filesystem path.

## 16. Next gate

After this contract is persisted and re-broken, the only allowed next action is:

    P3B_MATERIALIZATION_IMPLEMENTATION_CANDIDATE

P3-B may implement the preflight and one real materialization attempt only.

Even P3-B may not create `.obsidian`, launch Obsidian, install plugins, enable sync or modify the P2 core.

## 17. Candidate verdict

**READY FOR PERSISTED CONTRACT RE-BREAK ONLY.**

No AppData write and no real Vault creation is authorized by P3-A.

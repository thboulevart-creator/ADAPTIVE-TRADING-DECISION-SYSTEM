# OBSIDIAN P3-B MATERIALIZATION ADJUDICATION

Date: 2026-09-26

## 1. Scope

This adjudication records only what is supported by the executed P3-B boundary and the evidence available in the working conversation.

It does not invent missing relation counts, digests, or the full P3-B JSON execution report.

## 2. Persisted implementation identity

Qualified P3-B implementation candidate HEAD:

    bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba

The remote branch was reverified after local execution and remained exactly on that HEAD.

## 3. Local execution evidence

The local terminal reached:

    P3B_LOCAL_MATERIALIZATION_PASS

This is treated as a **reported local terminal execution result** produced after the bounded P3-B script completed its own preflight, fresh P2 rebuild, incoming verification, final rename, post-promotion verification, independent filesystem checks, and repository-state checks.

## 4. What may be concluded

Within the bounded P3-B procedure, the following are accepted:

- the external Vault materialization completed;
- the real destination exists at `C:\Users\Boulevart\AppData\Local\ATDS-OBSIDIAN-PROJECTION`;
- the materialized projection remains DERIVED relative to canonical GitHub/ATDS truth;
- `generated/` is the machine-owned deterministic projection;
- `views/` exists and was required empty by the terminal script;
- `.obsidian/` was required absent by the terminal script;
- Obsidian was not launched;
- community plugins were not enabled;
- Sync was not enabled;
- Git automation was not enabled;
- the ATDS branch, HEAD, and working tree were required preserved by the terminal script.

## 5. What may not be concluded from the evidence captured here

The conversation does not contain the full P3-B JSON report.

Therefore this adjudication does **not** persist or infer:

- the exact relation record count;
- the semantic-record digest;
- the artifact-set digest;
- the relation-set digest;
- the integrity-manifest SHA-256;
- the projection-tree digest;
- the final filesystem identity values.

Those values must be reconstructed before first open from the materialized Vault and a fresh qualified P2 build.

## 6. Authority boundary

    GitHub / ATDS
        = CANONICAL

    external Obsidian projection
        = DERIVED

    generated/
        = machine-owned deterministic projection

    views/
        = human-owned, currently expected empty

    .obsidian/
        = absent before first open

The materialized folder name, build manifest, or integrity manifest alone do not create canonical authority.

## 7. First-open gate

Because the full P3-B digest set was not captured in this conversation, **first open is not authorized directly by this adjudication**.

Before Obsidian is opened, a first-open safety harness must:

1. run a fresh P2 build using the exact qualified P2 identity;
2. verify BUILD A equals BUILD B;
3. compare the current Vault `generated/` tree byte-for-byte to BUILD A;
4. verify the integrity manifest and build-manifest identity;
5. snapshot `generated/`, `views/`, `.obsidian` absence, Vault filesystem identity, and repository state outside the Vault;
6. only then authorize a manual first open.

## 8. Bounded verdict

**PASS — BOUNDED MATERIALIZATION, WITH CRYPTOGRAPHIC RECONSTRUCTION REQUIRED BEFORE FIRST OPEN.**

This is not yet a first-open PASS.

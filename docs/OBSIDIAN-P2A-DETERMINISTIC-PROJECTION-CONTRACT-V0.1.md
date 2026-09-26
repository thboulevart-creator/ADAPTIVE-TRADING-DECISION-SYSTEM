# OBSIDIAN P2-A — DETERMINISTIC PROJECTION CONTRACT V0.1

Status: **CANDIDATE PREREGISTRATION ONLY**

Parent qualified P1-B HEAD: `26e541c0aedc85440bb069cdc767b2075b56317c`
Frozen ATDS source commit: `7bd8c1312430dfc3def5523eb65397a5d6a5ae05`
Frozen source tree: `66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b`
Pilot: **74 semantic artifact records**

## 1. Purpose

P2-A freezes the deterministic physical projection contract before any renderer, typed relation generator or integrity-manifest implementation exists.

Future bounded pipeline:

    74 SemanticRecord
    → deterministic artifact IDs
    → flat frontmatter
    → deterministic Markdown bytes
    → preregistered typed relations
    → deterministic relation records
    → integrity/build manifests
    → two independent builds
    → byte + semantic determinism comparison

P2-A itself creates no projection output.

## 2. Authority separation

A generated note is DERIVED even when the represented source artifact is CANONICAL.

Required separate fields:

    source_authority_role
    projection_authority_role

For the frozen pilot, `source_authority_role=CANONICAL` and `projection_authority_role=DERIVED`.

## 3. Deterministic artifact identity

Artifact ID:

    A- + first16hex(SHA256(UTF8(source_repository) + NUL + UTF8(source_path)))

Collision blocks the build. UUID/random identifiers are forbidden.

Output path is exactly `generated/artifacts/{projection_record_id}.md`. Source paths are never reused as output paths.

## 4. Flat frontmatter schema

The exact artifact frontmatter field order is machine-frozen in `deterministic_projection_contract_v0_1.json`.

Fixed projection values:

    projection_authority_role = DERIVED
    source_freshness = UNKNOWN
    projection_integrity = CLEAN

`source_freshness=UNKNOWN` is intentional: branch-relative freshness is dynamic and must not contaminate deterministic bytes.

## 5. Markdown byte contract

Required: UTF-8, no BOM, LF only, final newline, exact registered field order, deterministic JSON-compatible quoting, deterministic arrays, and no unknown fields.

Artifact body V0.1 is minimal and deterministic:

    # {projection_record_id}

    Source artifact: `{source_path}`

Canonical source text is not copied into notes in V0.1. Wikilinks are not generated.

## 6. Typed relations

Allowed relation types: REFERENCES, USES_INPUT, PRODUCES, GOVERNS, TESTED_BY, CHALLENGED_BY, ADJUDICATED_BY, SUCCESSOR_OF.

Allowed authoritative bases: EXPLICIT_STRUCTURED, EXPLICIT_TEXT, DERIVED_BY_RULE.

`INFERRED` is forbidden from authoritative generated relations.

Every relation requires source record, target record, relation type, basis, evidence source path and evidence source blob SHA.

Missing provenance means no relation.

## 7. Relation identity

Relation IDs are deterministic hashes over source record ID, relation type, target record ID, basis and exact evidence identity. Collision blocks the build.

P2 V0.1 may target only the 74 projected artifact records. Unresolved targets are skipped, never guessed.

## 8. No graph inflation

Wikilinks, backlinks, filename similarity, same date, adjacent version numbers, directory proximity and chronology alone are not semantic relations.

No LLM free-text relation inference is authorized.

## 9. Ownership

`generated/` is machine-owned, disposable and reproducible. It may contain no unique human knowledge and may not be edited in place.

`views/` is human-owned. The builder may neither write it nor consume it as semantic input.

## 10. Temporary staging only

P2 implementation must build only in a new empty OS temporary directory using exclusive file creation.

Pre-existing targets, writes outside staging, writes to `views/` or `.obsidian/`, alias escapes, unexpected hard links, or unavailable hard-link verification all block.

Promotion to the real AppData Vault remains forbidden.

## 11. Integrity manifest

`generated/manifests/integrity-manifest.json` lists deterministic artifact/relation files by sorted relative path with size and SHA-256.

The integrity manifest excludes itself.

A record's own `projection_integrity=CLEAN` is not proof. Verification authority is the manifest comparison. Manual edits must be reported as MODIFIED and missing files as MISSING.

## 12. Build manifest

`generated/manifests/build-manifest.json` is deterministic. Timestamps, host/user names, absolute repository paths and absolute staging paths are forbidden.

Optional volatile run metadata may exist only outside the deterministic `generated/` tree and may not influence any digest.

## 13. Ordering

Artifact files sort by projection record ID. Relation files sort by relation ID. Manifest entries sort by relative UTF-8 path. Filesystem enumeration order has no semantic meaning.

## 14. Double-build gate

Two independent fresh staging directories must be built from identical frozen inputs.

They must have identical relative-path sets, bytes, SHA-256s, semantic-record digest, artifact-set digest, relation-set digest, integrity-manifest SHA-256 and projection-tree digest.

Any difference blocks qualification.

## 15. Adversarial surface

The machine contract preregisters breakers for field-order drift, CRLF/BOM, volatile data, absolute paths, random IDs, ID collisions, graph inflation, missing provenance, out-of-pilot targets, overwrite, forbidden writes, hard-link/reparse escapes, false CLEAN integrity, recursive manifest inclusion, byte nondeterminism, source-path output reuse, source-text copying and silent extra fields.

## 16. Boundary

After persisted re-break, the only next action is `P2_IMPLEMENTATION_CANDIDATE_IN_TEMP_STAGING_ONLY`.

Still forbidden: real Vault creation, `.obsidian`, opening Obsidian on the projection, community plugins, sync, or promotion into the AppData Vault path.

## 17. Candidate verdict

**READY FOR PERSISTED CONTRACT RE-BREAK ONLY.**

No renderer, relation generator, manifest implementation or Vault is created by this preregistration.

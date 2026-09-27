# OBSIDIAN P5-D3B — CURRENT-HEAD SEMANTIC PROJECTION BRIDGE V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3B closes the first concrete interface gap identified by qualified P5-D3A:

    P5-B2 DynamicInventory
            ↓
    explicit governed bridge
            ↓
    current-head semantic projection input

The bridge does not coerce DynamicInventory into the historical FrozenInventory model.

It produces one conservative semantic projection record for every dynamic inventory entry.

## 2. Qualified predecessor

P5-D3A qualification commit:

    d1198a5b7e32607d2a2ef46084f6d11bca36b3e2

P5-D3A qualification report blob:

    bf8c5e917b08a6a1b1de7fdd7c0098a5969bfb87

Qualified P5-B2 implementation:

    5f6ed61f36e889dc27ef14ef09467ada9f9f0f58

P5-D3B does not reopen P5-D3A or P5-B2.

## 3. Why the old classifier is not reused as the bridge

The historical classifier is bound to:

    FrozenInventory
    ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1

Its rules are also bound to:

    exact frozen source_commit
    exact frozen source_tree
    pilot_source_count = 74

and artifact-family logic depends on:

    inventory_class

P5-B2 instead produces:

    DynamicInventory
    ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1

with:

    selection_zone
    content_mode

P5-B explicitly states that selection_zone is not artifact_family and is not semantic authority.

Therefore P5-D3B does not call:

    classify_inventory()
    classify_record()

and does not load:

    semantic_classification_rules_v0_1.json

## 4. Output model

Every P5-B2 inventory entry produces exactly one bridge entry and exactly one semantic projection record.

No silent drop is allowed.

Bridge result schema:

    ATDS_OBSIDIAN_CURRENT_HEAD_SEMANTIC_BRIDGE_RESULT_V0_1

Entry schema:

    ATDS_OBSIDIAN_CURRENT_HEAD_SEMANTIC_BRIDGE_ENTRY_V0_1

Semantic record schema remains:

    ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1

The bridge preserves:

    source_repository
    source_branch
    source_commit
    source_tree
    source_path
    source_blob_sha
    source_blob_size
    git_mode
    selection_zone
    content_mode

## 5. Dispositions

FULL_TEXT:

    disposition = SEMANTIC_FULL_TEXT

METADATA_ONLY:

    disposition = SEMANTIC_METADATA_ONLY

P5-D3B V0.1 does not exclude valid P5-B2 inventory members by default.

Unsupported bridge conditions fail closed.

## 6. No body reads in the bridge

P5-D3B V0.1 deliberately performs no source-body semantic read.

This applies even to FULL_TEXT entries.

The bridge is a structural/provenance bridge, not a new semantic inference engine.

For every entry:

    semantic_body_read = false

For FULL_TEXT:

    downstream_body_read_allowed = true

For METADATA_ONLY:

    downstream_body_read_allowed = false

This preserves the P5-B2 rule that metadata-only source bodies must not become semantic input without a separately qualified parser.

## 7. Conservative semantic policy

Because P5-D3B does not read the body, semantic axes remain conservative.

For every V0.1 semantic record:

    semantic_role = UNKNOWN
    procedure_role = NONE
    qualification_status = UNKNOWN
    qualification_scope = null
    scientific_status = UNKNOWN
    epistemic_role = UNKNOWN
    temporal_role = UNKNOWN
    limitations = []
    non_claims = []

Source authority remains:

    authority_role = CANONICAL

because the record is bound to an exact tracked Git-tree blob.

Persistence remains:

    TRACKED_IN_GIT_TREE

No path token, selection zone or filename token may promote qualification/scientific/epistemic state.

## 8. Artifact family

Artifact family is treated as physical classification only.

It is not derived from selection_zone.

METADATA_ONLY always becomes:

    METADATA_ONLY

FULL_TEXT uses an explicit extension registry.

Examples:

    .md     → DOCUMENT
    .py     → CODE
    .json   → STRUCTURED_DATA
    .yaml   → STRUCTURED_DATA
    .txt    → TEXT
    .html   → WEB_ASSET

An unregistered FULL_TEXT extension fails closed.

## 9. Selection zone remains provenance only

selection_zone is preserved in the bridge binding.

Changing selection_zone for the same exact source path/blob may change:

    bridge_entry_digest_sha256

because the provenance binding changed.

It must not change:

    artifact_family
    semantic_role
    qualification_status
    semantic_record_digest_sha256

when every other semantic-record input remains identical.

## 10. Digests

P5-D3B binds two distinct deterministic digests.

Semantic record digest:

    semantic_record_digest_sha256

It follows the existing semantic-record canonical digest function.

Bridge binding digest:

    bridge_entry_digest_sha256

It additionally binds:

    git_mode
    selection_zone
    content_mode
    disposition
    artifact_family
    semantic_body_read
    downstream_body_read_allowed
    semantic_record

The bridge also records the exact:

    dynamic_inventory_digest_sha256
    bridge_contract_version

## 11. No fixed corpus size

P5-D3B contains no normative:

    74
    908

or any other exact source count.

The bridge accepts the exact dynamic inventory size produced for the evaluated HEAD.

Output count must equal input count.

## 12. Legacy relation extractor remains unsafe for metadata-only records

Static repository inspection established that the historical:

    extract_relations()

calls:

    source.read_blob(...)

and UTF-8 decodes every SemanticRecord.

Therefore bridge output must not be passed blindly to the old relation extractor.

In particular:

    METADATA_ONLY

records may not be body-read.

A future current-head builder/relation adaptation must be content-mode aware.

This is deferred to the governed projection-builder/orchestrator boundary.

## 13. Legacy builder is not silently promoted to current-head qualification

The historical deterministic projection contract still contains:

    pilot_source_count = 74

and the build manifest still contains the historical field:

    pilot_inventory_digest_sha256

The old relation path also remains metadata-only unsafe.

Therefore P5-D3B does not call:

    build_projection_from_records()

and does not claim the old P2 builder is already current-head qualified.

The bridge only produces the governed semantic projection input needed for the later current-head builder adaptation.

## 14. Real-head qualification harness

P5-D3B includes a bounded qualification harness:

    p5d3b_verify.py

The harness may reuse qualified P5-B2:

    build_from_repository()

against one exact monitored HEAD/tree.

Then it applies the pure bridge.

The report is summary-only.

It does not serialize bridge entries or source bodies.

The harness verifies:

    source HEAD identity
    source tree identity
    dynamic inventory digest binding
    source blob count equality
    FULL_TEXT count equality
    METADATA_ONLY count equality
    semantic record count equality
    semantic_body_read = false for every entry
    downstream_body_read_allowed = false for every METADATA_ONLY entry

It reports:

    real_vault_modified = false
    projection_modified = false
    canonical_worktree_write_required = false

No fixed expected real-head count is used.

## 15. Failure model

Invalid input fails closed.

Examples:

    wrong repository
    wrong branch
    malformed commit/tree
    unsorted inventory
    duplicate path
    malformed blob SHA
    unsupported git mode
    unknown content mode
    unsupported FULL_TEXT extension

No partial bridge result is returned.

## 16. P5-D3B non-authorizations

P5-D3B still does not authorize:

    body semantic enrichment
    network fetch by bridge
    FrozenInventory conversion
    legacy classifier execution
    legacy relation extractor execution
    projection builder execution
    candidate generation staging
    evaluation orchestrator
    real Vault writes
    production promotion
    background observer
    polling loop
    Graph/Search CURRENT semantics

## 17. Next governed boundary

If P5-D3B qualifies, the next already-preregistered boundary remains:

    P5-D3C — CANDIDATE GENERATION STAGING CONTRACT

The later finite evaluator must also include a governed current-head builder/relation adaptation before using P5-D3B output for deterministic A/B projection builds.

That adaptation must preserve the METADATA_ONLY no-body-read boundary.

The finite orchestrator remains:

    P5-D3D

Sandbox end-to-end candidate evaluation remains:

    P5-D3E

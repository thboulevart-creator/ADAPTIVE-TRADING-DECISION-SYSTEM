# OBSIDIAN P5-D3D — FINITE CANDIDATE EVALUATOR CONTRACT V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3D closes the last structural gap between the qualified current-head semantic bridge and a complete finite candidate evaluation.

The target chain is:

    P5-D2 EVALUATION_STARTED
        ↓
    exact isolated candidate repository
        ↓
    P5-B2 DynamicInventory
        ↓
    P5-D3B current-head semantic bridge
        ↓
    current-head projection builder A
        +
    current-head projection builder B
        ↓
    exact deterministic equality
        ↓
    preregistered projection breakers
        ↓
    P5-D3C2 SEALED_UNPROMOTED package
        ↓
    QUALIFIED / REJECTED / BLOCKED
        ↓
    P5-D2 result event only when determinate

P5-D3D is finite.

It is not an observer loop.

It does not promote.

## 2. Qualified predecessors

P5-D2 one-shot observer tick:

    contract blob:
    5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3

    implementation blob:
    fd212f61ec38332b677110f40265638af55a73e2

P5-B2 dynamic inventory:

    contract blob:
    80729156f4ac51b760c4347f581f052a175b88b3

    implementation blob:
    5f6ed61f36e889dc27ef14ef09467ada9f9f0f58

P5-D3B current-head semantic bridge:

    contract blob:
    7015db1206cd40b703795d12519707a6455b4fc3

    implementation blob:
    ff3c2dd232487594a5283a9ab7750780ac098f2d

P5-D3C2 staging qualification:

    qualification commit:
    205d09e22430e60324b76f2713024e36527e5dba

    qualification report blob:
    d1ffea5fefc8845831c11a153a0e17492401ef60

    packager/verifier blob:
    e2e5867536f4f9c7dec475c6696737249536ff39

## 3. Why the legacy builder cannot be reused directly

The legacy deterministic projection stack remains pilot-bound in two ways.

First:

    build_projection_from_records()

accepts and persists:

    pilot_inventory_digest_sha256

Second:

    extract_relations()

reads:

    source.read_blob(record.source_blob_sha)

for every SemanticRecord.

That means METADATA_ONLY bridge entries would be body-read.

This directly violates the qualified P5-D3B boundary.

The legacy deterministic contract also contains:

    74 frozen source paths
    pilot target policies
    pilot semantic digest wording

Therefore P5-D3D does not rename or wrap the legacy builder and call it current-head qualified.

## 4. What may be reused

The following legacy mechanics remain reusable because they are generic and do not impose the frozen-inventory authority model:

    render_artifact()
    render_relation()

    deterministic artifact/relation IDs

    exclusive_write()
    file_digest()
    digest_entries()
    make_integrity_manifest()
    verify_integrity_manifest()
    projection_tree_digest()
    all_generated_files()

Reuse does not make the legacy P2 contract authoritative.

The new current-head contract is the authority.

## 5. Current-head projection authority

Exact contract:

    tools/obsidian_projection/current_head_projection_contract_v0_1.json

Blob:

    12e9904faf9b157cd6991455883ef35e628ee672

Schema:

    ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_CONTRACT_V0_1

It contains no fixed source-count authority.

It contains no pilot_inventory_digest field in its current-head build manifest.

## 6. One artifact per bridge entry

Every P5-D3B bridge entry receives one artifact record.

Therefore:

    artifact_record_count
        =
    source_record_count
        =
    bridge entry count

METADATA_ONLY is not exclusion.

It means:

    metadata projection allowed
    source body read forbidden

## 7. Body-read authority

Default:

    DENY

Artifact rendering:

    NEVER reads source body

Relation extraction may read a source blob only when all are true:

    content_mode == FULL_TEXT
    downstream_body_read_allowed == true
    suffix == .md OR .json

Therefore:

    METADATA_ONLY
        → no body read

    FULL_TEXT .py
        → no relation body read

    FULL_TEXT .md
        → body read allowed for explicit relation extraction

    FULL_TEXT .json
        → body read allowed for explicit relation extraction

Every permitted body read is audited.

The audit binds:

    source_path
    source_blob_sha
    content_mode
    purpose

Required:

    metadata_only_body_read_count = 0

## 8. Relation policy

Only:

    REFERENCES

is authorized in current-head V0.1.

Only two bases are authorized:

    EXPLICIT_STRUCTURED
    EXPLICIT_TEXT

The two current-head rules are:

    CH-REL-V0-EXACT-STRUCTURED-PATH
    CH-REL-V0-EXPLICIT-LABELED-TEXT-PATH

No:

    inferred relation
    filename similarity
    chronological adjacency
    backlink
    wikilink
    guessed target

may create an authoritative relation.

## 9. Metadata-only relation targets

A METADATA_ONLY artifact may be a relation target.

Example:

    FULL_TEXT docs/foo.md
        explicitly names exact repository path:
        assets/binary.dat

If:

    assets/binary.dat

is a projected METADATA_ONLY bridge entry, a REFERENCES edge may target it.

No target body read is required.

Therefore:

    metadata-only source relation = forbidden

but:

    metadata-only target relation = allowed

when the exact source path was explicitly cited by an eligible FULL_TEXT source.

## 10. Current-head build manifest

Schema:

    ATDS_OBSIDIAN_CURRENT_HEAD_BUILD_MANIFEST_V0_1

It binds:

    source_repository
    source_branch
    source_commit
    source_tree

    dynamic_inventory_digest_sha256
    semantic_bridge_digest_sha256
    semantic_record_digest_sha256

    projection_contract_version
    renderer_version
    relation_rule_registry_version

    source_record_count
    full_text_count
    metadata_only_count

    artifact_record_count
    relation_record_count

    relation_source_body_read_count
    metadata_only_body_read_count
    body_read_audit_digest_sha256

    artifact_set_digest_sha256
    relation_set_digest_sha256
    integrity_manifest_sha256
    build_status

Forbidden:

    pilot_inventory_digest_sha256
    pilot_source_count
    timestamp
    host
    absolute staging path

## 11. Deterministic double-build

Every candidate is built twice.

Build A and Build B must use:

    same candidate HEAD
    same candidate tree
    same DynamicInventory digest
    same semantic bridge digest
    same semantic record digest
    same projection contract blob

They must use:

    distinct fresh OS-temp roots

Required equality includes:

    exact relative path set
    every generated byte
    every generated SHA-256
    body-read audit digest
    body-read count
    semantic-record digest
    artifact-set digest
    relation-set digest
    integrity-manifest digest
    projection-tree digest
    generated-file count

Any deterministic mismatch is:

    REJECTED

with:

    DETERMINISTIC_DOUBLE_BUILD_MISMATCH

It is not infrastructure BLOCKED.

## 12. Projection breaker manifest

P5-D3D preregisters exactly twelve candidate breakers:

    CHP-B01
      artifact count equals source/bridge count

    CHP-B02
      metadata-only body-read count is zero

    CHP-B03
      every body-read row is eligible FULL_TEXT .md/.json

    CHP-B04
      every relation evidence source exists in body-read audit

    CHP-B05
      every relation target resolves to a bridge artifact

    CHP-B06
      no CURRENT/views/.obsidian/.git generated surface

    CHP-B07
      integrity manifest is CLEAN

    CHP-B08
      build manifest identity matches candidate/inventory/bridge

    CHP-B09
      no pilot inventory field or fixed pilot count

    CHP-B10
      A/B file maps and bytes are identical

    CHP-B11
      A/B body-read audits are identical

    CHP-B12
      A/B stage roots are distinct

The breaker manifest and result each receive deterministic SHA-256 identity.

## 13. Packaging

Only after:

    double-build PASS
    +
    all CHP breakers PASS

may P5-D3D construct:

    VerifiedProjectionCandidate

for P5-D3C2.

It binds:

    exact candidate HEAD/tree
    DynamicInventory digest
    semantic bridge digest
    semantic-record digest
    current-head projection contract blob
    projection-tree digest
    generated-file count
    breaker PASS
    determinism PASS
    breaker manifest/result digests
    double-build evidence digest

P5-D3C2 must return:

    PASS_SEALED_UNPROMOTED

before QUALIFIED is possible.

## 14. Activation boundary

P5-D3D begins only from a qualified P5-D2 tick result whose decision is:

    START_EXACT_HEAD_EVALUATION

Required:

    next observer phase = EVALUATING

and:

    candidate HEAD
        =
    decision candidate HEAD
        =
    pending_heads[0]

The activation tick must also retain:

    automatic_promotion_authorized = false
    production_write_authorized = false

Its deterministic result digest is recorded in P5-D3D evidence.

## 15. Prepared isolated candidate repository

P5-D3D itself does not perform:

    network fetch
    git checkout creation

It consumes an already prepared isolated candidate repository root.

That root must be:

    outside canonical user worktree
    outside real Vault
    outside live projection
    exact repository
    exact candidate commit available
    exact candidate tree available

P5-D3D may read from it.

It may not mutate it.

The surrounding exact-checkout workflow is reserved for P5-D3E sandbox qualification.

## 16. Outcome model

Three outcomes exist:

    QUALIFIED
    REJECTED
    BLOCKED

QUALIFIED means every candidate-validity gate passed and the sealed package verified.

REJECTED means deterministic evidence proves the candidate violated a preregistered validity rule.

BLOCKED means infrastructure/tooling/evidence prevented a validity conclusion.

These meanings are not interchangeable.

## 17. P5-D2 result mapping

QUALIFIED:

    EVALUATION_PASSED
    failure_code = null

REJECTED:

    EVALUATION_FAILED
    failure_code = stable candidate failure code

BLOCKED:

    no P5-D2 result event

For determinate outcomes:

    sequence =
    activation.next_state.last_event_sequence + 1

The event is applied only through:

    one_shot_tick()

P5-D3D may not mutate observer state directly.

## 18. Live projection invariants

During P5-D3D evaluation:

    live_projection_head_after
        =
    live_projection_head_before

for:

    QUALIFIED
    REJECTED
    BLOCKED

QUALIFIED means:

    candidate qualified pending promotion

not:

    candidate promoted

No CURRENT mutation occurs.

## 19. Finite evaluation report

Schema:

    ATDS_OBSIDIAN_P5D3D_FINITE_EVALUATION_REPORT_V0_1

The report binds:

    activation digest
    candidate HEAD/tree
    inventory digest
    bridge digest
    semantic-record digest
    projection contract blob
    both projection-tree digests
    breaker manifest/result digests
    double-build evidence digest
    candidate-generation digest
    final outcome/failure code
    P5-D2 result-tick digest when determinate
    live head before/after

Required:

    real_vault_modified = false
    current_pointer_created = false
    production_promotion_authorized = false

No absolute host path belongs in the report.

## 20. Retry semantics

BLOCKED may retry the same exact candidate.

But retry must start over with:

    activation revalidation
    identity revalidation
    fresh Build A root
    fresh Build B root
    fresh package root

A partial failed build/package is never reused as qualified evidence.

## 21. Contract-only boundary

This P5-D3D phase is contract-only.

Not yet authorized:

    current-head builder implementation
    current-head relation adapter implementation
    breaker runner implementation
    finite evaluator implementation
    orchestrator execution

Also still forbidden:

    network fetch
    checkout creation
    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Graph/Search CURRENT semantics

## 22. Next action after contract qualification

If this P5-D3D contract gate passes, implementation becomes authorized under the same P5-D3D frontier.

Only synthetic fixture execution is initially allowed for the implementation candidate.

A real exact-head sandbox evaluation remains reserved for:

    P5-D3E

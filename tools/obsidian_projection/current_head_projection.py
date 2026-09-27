from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .current_head_relations import (
    BodyReadAuditRow,
    CurrentHeadRelationError,
    CurrentHeadRelationInfrastructureError,
    CurrentHeadRelationRecord,
    RELATION_RULE_REGISTRY_VERSION,
    extract_current_head_relations,
)
from .current_head_semantic_bridge import (
    CurrentHeadSemanticBridgeResult,
)
from .integrity import (
    FileDigest,
    IntegrityError,
    all_generated_files,
    canonical_json_file_bytes,
    create_stage_directories,
    digest_entries,
    exclusive_write,
    file_digest,
    make_integrity_manifest,
    projection_tree_digest,
    verify_integrity_manifest,
)
from .rendering import (
    RenderedFile,
    RenderingError,
    render_artifact,
    render_relation,
)


class CurrentHeadProjectionError(RuntimeError):
    pass


class CurrentHeadProjectionInvalidError(
    CurrentHeadProjectionError
):
    pass


class CurrentHeadProjectionInfrastructureError(
    CurrentHeadProjectionError
):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
PROJECTION_CONTRACT_BLOB = (
    "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2"
)
P5D3D_CONTRACT_QUALIFICATION_COMMIT = (
    "c2d0323df53c40c8818d7f8d9805210e1961116e"
)
RENDERER_VERSION = "ATDS_OBSIDIAN_RENDERER_V0_1"

_BUILD_MANIFEST_PATH = (
    "generated/manifests/build-manifest.json"
)
_INTEGRITY_MANIFEST_PATH = (
    "generated/manifests/integrity-manifest.json"
)


@dataclass(frozen=True)
class CurrentHeadBuildResult:
    stage_root: str
    source_commit: str
    source_tree: str
    dynamic_inventory_digest_sha256: str
    semantic_bridge_digest_sha256: str
    semantic_record_digest_sha256: str
    projection_contract_version: str
    source_record_count: int
    full_text_count: int
    metadata_only_count: int
    artifact_record_count: int
    relation_record_count: int
    relation_source_body_read_count: int
    metadata_only_body_read_count: int
    body_read_audit_digest_sha256: str
    artifact_set_digest_sha256: str
    relation_set_digest_sha256: str
    integrity_manifest_sha256: str
    projection_tree_digest_sha256: str
    generated_file_count: int
    body_read_audit_rows: tuple[
        BodyReadAuditRow, ...
    ]
    relation_records: tuple[
        CurrentHeadRelationRecord, ...
    ]


def load_current_head_projection_contract() -> dict[str, Any]:
    path = Path(__file__).with_name(
        "current_head_projection_contract_v0_1.json"
    )
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise CurrentHeadProjectionInfrastructureError(
            "current-head projection contract unavailable"
        ) from exc

    if not isinstance(value, dict):
        raise CurrentHeadProjectionInvalidError(
            "projection contract must be object"
        )
    if value.get("schema") != (
        "ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_CONTRACT_V0_1"
    ):
        raise CurrentHeadProjectionInvalidError(
            "projection contract schema mismatch"
        )
    return value


def _classify_integrity_error(
    exc: IntegrityError,
) -> CurrentHeadProjectionError:
    message = str(exc)
    infrastructure_markers = (
        "cannot lstat",
        "cannot stat",
        "junction check failed",
        "hard-link count unavailable",
    )
    if any(
        marker in message
        for marker in infrastructure_markers
    ):
        return CurrentHeadProjectionInfrastructureError(
            message
        )
    return CurrentHeadProjectionInvalidError(
        message
    )


def _validate_bridge(
    bridge: CurrentHeadSemanticBridgeResult,
    contract: Mapping[str, Any],
) -> None:
    if not isinstance(
        bridge,
        CurrentHeadSemanticBridgeResult,
    ):
        raise CurrentHeadProjectionInvalidError(
            "bridge result type mismatch"
        )
    if bridge.source_repository != EXPECTED_REPOSITORY:
        raise CurrentHeadProjectionInvalidError(
            "bridge repository mismatch"
        )
    if bridge.source_branch != EXPECTED_BRANCH:
        raise CurrentHeadProjectionInvalidError(
            "bridge branch mismatch"
        )
    if not bridge.entries:
        raise CurrentHeadProjectionInvalidError(
            "empty bridge forbidden"
        )

    entries = tuple(bridge.entries)
    if entries != tuple(
        sorted(
            entries,
            key=lambda item:
                item.source_path.encode("utf-8"),
        )
    ):
        raise CurrentHeadProjectionInvalidError(
            "bridge entries are not bytewise sorted"
        )

    paths = [
        entry.source_path
        for entry in entries
    ]
    if len(paths) != len(set(paths)):
        raise CurrentHeadProjectionInvalidError(
            "duplicate bridge source_path"
        )

    if len(bridge.semantic_records) != len(entries):
        raise CurrentHeadProjectionInvalidError(
            "semantic record count mismatch"
        )

    input_contract = contract.get(
        "input_contract"
    )
    if not isinstance(input_contract, dict):
        raise CurrentHeadProjectionInvalidError(
            "input contract missing"
        )

    for entry in entries:
        if entry.semantic_body_read:
            raise CurrentHeadProjectionInvalidError(
                "bridge semantic body read must be false"
            )
        if (
            entry.content_mode == "METADATA_ONLY"
            and entry.downstream_body_read_allowed
        ):
            raise CurrentHeadProjectionInvalidError(
                "METADATA_ONLY downstream read authority"
            )

        record = entry.semantic_record
        if record.record_schema != (
            "ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1"
        ):
            raise CurrentHeadProjectionInvalidError(
                "semantic record schema mismatch"
            )
        if record.source_repository != bridge.source_repository:
            raise CurrentHeadProjectionInvalidError(
                "semantic record repository mismatch"
            )
        if record.source_branch != bridge.source_branch:
            raise CurrentHeadProjectionInvalidError(
                "semantic record branch mismatch"
            )
        if record.source_commit != bridge.source_commit:
            raise CurrentHeadProjectionInvalidError(
                "semantic record commit mismatch"
            )
        if record.source_tree != bridge.source_tree:
            raise CurrentHeadProjectionInvalidError(
                "semantic record tree mismatch"
            )
        if record.source_path != entry.source_path:
            raise CurrentHeadProjectionInvalidError(
                "semantic record path mismatch"
            )
        if record.source_blob_sha != entry.source_blob_sha:
            raise CurrentHeadProjectionInvalidError(
                "semantic record blob mismatch"
            )
        if record.source_blob_size != entry.source_blob_size:
            raise CurrentHeadProjectionInvalidError(
                "semantic record size mismatch"
            )
        if record.artifact_family != entry.artifact_family:
            raise CurrentHeadProjectionInvalidError(
                "semantic record artifact-family mismatch"
            )


def _render_artifacts(
    bridge: CurrentHeadSemanticBridgeResult,
    contract: Mapping[str, Any],
) -> tuple[RenderedFile, ...]:
    rendered: list[RenderedFile] = []
    seen_paths: set[str] = set()

    for record in bridge.semantic_records:
        item = render_artifact(
            record,
            contract,
        )
        if item.relative_path in seen_paths:
            raise CurrentHeadProjectionInvalidError(
                "artifact projection ID collision"
            )
        seen_paths.add(item.relative_path)
        rendered.append(item)

    rendered.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(rendered)


def _render_relations(
    relations: Sequence[
        CurrentHeadRelationRecord
    ],
    contract: Mapping[str, Any],
) -> tuple[RenderedFile, ...]:
    rendered: list[RenderedFile] = []
    seen_paths: set[str] = set()

    for relation in relations:
        item = render_relation(
            relation,
            contract,
        )
        if item.relative_path in seen_paths:
            raise CurrentHeadProjectionInvalidError(
                "relation projection ID collision"
            )
        seen_paths.add(item.relative_path)
        rendered.append(item)

    rendered.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(rendered)


def _write_rendered_set(
    stage_root: Path,
    files: Sequence[RenderedFile],
) -> tuple[FileDigest, ...]:
    digests: list[FileDigest] = []
    for rendered in files:
        path = exclusive_write(
            stage_root,
            rendered,
        )
        digests.append(
            file_digest(
                stage_root,
                path,
            )
        )
    return tuple(digests)


def _build_manifest_bytes(
    *,
    bridge: CurrentHeadSemanticBridgeResult,
    body_read_audit_digest_sha256: str,
    relation_source_body_read_count: int,
    metadata_only_body_read_count: int,
    artifact_record_count: int,
    relation_record_count: int,
    artifact_set_digest_sha256: str,
    relation_set_digest_sha256: str,
    integrity_manifest_sha256: str,
    contract: Mapping[str, Any],
) -> bytes:
    values = {
        "schema":
            contract["build_manifest"]["schema"],
        "source_repository":
            bridge.source_repository,
        "source_branch":
            bridge.source_branch,
        "source_commit":
            bridge.source_commit,
        "source_tree":
            bridge.source_tree,
        "dynamic_inventory_digest_sha256":
            bridge.dynamic_inventory_digest_sha256,
        "semantic_bridge_digest_sha256":
            bridge.bridge_entry_digest_sha256,
        "semantic_record_digest_sha256":
            bridge.semantic_record_digest_sha256,
        "projection_contract_version":
            PROJECTION_CONTRACT_BLOB,
        "renderer_version":
            RENDERER_VERSION,
        "relation_rule_registry_version":
            RELATION_RULE_REGISTRY_VERSION,
        "source_record_count":
            len(bridge.entries),
        "full_text_count":
            bridge.full_text_count,
        "metadata_only_count":
            bridge.metadata_only_count,
        "artifact_record_count":
            artifact_record_count,
        "relation_record_count":
            relation_record_count,
        "relation_source_body_read_count":
            relation_source_body_read_count,
        "metadata_only_body_read_count":
            metadata_only_body_read_count,
        "body_read_audit_digest_sha256":
            body_read_audit_digest_sha256,
        "artifact_set_digest_sha256":
            artifact_set_digest_sha256,
        "relation_set_digest_sha256":
            relation_set_digest_sha256,
        "integrity_manifest_sha256":
            integrity_manifest_sha256,
        "build_status":
            "PASS",
    }

    expected = contract[
        "build_manifest"
    ]["field_order"]
    if list(values.keys()) != expected:
        raise CurrentHeadProjectionInvalidError(
            "current-head build-manifest field order drift"
        )

    forbidden = set(
        contract["build_manifest"][
            "forbidden_fields"
        ]
    )
    if forbidden & set(values):
        raise CurrentHeadProjectionInvalidError(
            "forbidden pilot/volatile build-manifest field"
        )

    return canonical_json_file_bytes(
        values
    )


def build_current_head_projection(
    *,
    source: Any,
    bridge: CurrentHeadSemanticBridgeResult,
    stage_root: Path,
    contract: Mapping[str, Any] | None = None,
) -> CurrentHeadBuildResult:
    active_contract = (
        load_current_head_projection_contract()
        if contract is None
        else dict(contract)
    )

    _validate_bridge(
        bridge,
        active_contract,
    )

    try:
        create_stage_directories(
            stage_root
        )

        artifact_files = _render_artifacts(
            bridge,
            active_contract,
        )

        relation_result = (
            extract_current_head_relations(
                source=source,
                bridge=bridge,
                contract=active_contract,
            )
        )

        if (
            relation_result.metadata_only_body_read_count
            != 0
        ):
            raise CurrentHeadProjectionInvalidError(
                "METADATA_ONLY body-read count nonzero"
            )

        relation_files = _render_relations(
            relation_result.relations,
            active_contract,
        )

        artifact_digests = _write_rendered_set(
            stage_root,
            artifact_files,
        )
        relation_digests = _write_rendered_set(
            stage_root,
            relation_files,
        )

        if len(artifact_digests) != len(
            bridge.entries
        ):
            raise CurrentHeadProjectionInvalidError(
                "artifact count differs from bridge entry count"
            )

        artifact_set_digest = digest_entries(
            artifact_digests
        )
        relation_set_digest = digest_entries(
            relation_digests
        )

        manifest_bytes, _aggregate = (
            make_integrity_manifest(
                (
                    *artifact_digests,
                    *relation_digests,
                )
            )
        )

        manifest_path = exclusive_write(
            stage_root,
            RenderedFile(
                relative_path=_INTEGRITY_MANIFEST_PATH,
                content=manifest_bytes,
            ),
        )
        manifest_digest = file_digest(
            stage_root,
            manifest_path,
        )

        statuses = verify_integrity_manifest(
            stage_root
        )
        not_clean = {
            relative: status
            for relative, status
            in statuses.items()
            if status != "CLEAN"
        }
        if not_clean:
            raise CurrentHeadProjectionInvalidError(
                "integrity verification failed"
            )

        tree_digest = projection_tree_digest(
            stage_root
        )

        build_manifest = _build_manifest_bytes(
            bridge=bridge,
            body_read_audit_digest_sha256=(
                relation_result
                .body_read_audit_digest_sha256
            ),
            relation_source_body_read_count=(
                relation_result
                .relation_source_body_read_count
            ),
            metadata_only_body_read_count=(
                relation_result
                .metadata_only_body_read_count
            ),
            artifact_record_count=len(
                artifact_files
            ),
            relation_record_count=len(
                relation_files
            ),
            artifact_set_digest_sha256=(
                artifact_set_digest
            ),
            relation_set_digest_sha256=(
                relation_set_digest
            ),
            integrity_manifest_sha256=(
                manifest_digest.sha256
            ),
            contract=active_contract,
        )

        exclusive_write(
            stage_root,
            RenderedFile(
                relative_path=_BUILD_MANIFEST_PATH,
                content=build_manifest,
            ),
        )

        generated_files = all_generated_files(
            stage_root
        )

    except CurrentHeadRelationInfrastructureError as exc:
        raise CurrentHeadProjectionInfrastructureError(
            str(exc)
        ) from exc
    except CurrentHeadRelationError as exc:
        raise CurrentHeadProjectionInvalidError(
            str(exc)
        ) from exc
    except RenderingError as exc:
        raise CurrentHeadProjectionInvalidError(
            str(exc)
        ) from exc
    except IntegrityError as exc:
        raise _classify_integrity_error(
            exc
        ) from exc

    return CurrentHeadBuildResult(
        stage_root=str(stage_root),
        source_commit=bridge.source_commit,
        source_tree=bridge.source_tree,
        dynamic_inventory_digest_sha256=(
            bridge.dynamic_inventory_digest_sha256
        ),
        semantic_bridge_digest_sha256=(
            bridge.bridge_entry_digest_sha256
        ),
        semantic_record_digest_sha256=(
            bridge.semantic_record_digest_sha256
        ),
        projection_contract_version=(
            PROJECTION_CONTRACT_BLOB
        ),
        source_record_count=len(
            bridge.entries
        ),
        full_text_count=bridge.full_text_count,
        metadata_only_count=(
            bridge.metadata_only_count
        ),
        artifact_record_count=len(
            artifact_files
        ),
        relation_record_count=len(
            relation_files
        ),
        relation_source_body_read_count=(
            relation_result
            .relation_source_body_read_count
        ),
        metadata_only_body_read_count=(
            relation_result
            .metadata_only_body_read_count
        ),
        body_read_audit_digest_sha256=(
            relation_result
            .body_read_audit_digest_sha256
        ),
        artifact_set_digest_sha256=(
            artifact_set_digest
        ),
        relation_set_digest_sha256=(
            relation_set_digest
        ),
        integrity_manifest_sha256=(
            manifest_digest.sha256
        ),
        projection_tree_digest_sha256=(
            tree_digest
        ),
        generated_file_count=len(
            generated_files
        ),
        body_read_audit_rows=(
            relation_result.body_read_audit_rows
        ),
        relation_records=(
            relation_result.relations
        ),
    )

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .classification import (
    SemanticRecord,
    records_digest_sha256,
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
from .relations import (
    RelationRecord,
    extract_relations,
)
from .rendering import (
    RenderedFile,
    RenderingError,
    render_artifact,
    render_relation,
)


class BuilderError(RuntimeError):
    """Raised when deterministic P2 build cannot fail closed."""


RENDERER_VERSION = "ATDS_OBSIDIAN_RENDERER_V0_1"
RELATION_RULE_REGISTRY_VERSION = (
    "ATDS_OBSIDIAN_RELATION_RULES_V0_1"
)


@dataclass(frozen=True)
class BuildResult:
    stage_root: str
    artifact_record_count: int
    relation_record_count: int
    semantic_record_digest_sha256: str
    artifact_set_digest_sha256: str
    relation_set_digest_sha256: str
    integrity_manifest_sha256: str
    projection_tree_digest_sha256: str
    deterministic_file_count: int
    generated_file_count: int


def _assert_contract_boundary(
    contract: Mapping[str, Any],
) -> None:
    boundary = contract[
        "execution_boundary"
    ]
    gate = contract["next_action_gate"]

    if not boundary.get("staging_only"):
        raise BuilderError(
            "contract does not require staging-only"
        )
    if boundary.get(
        "real_vault_creation_authorized"
    ):
        raise BuilderError(
            "real Vault creation unexpectedly authorized"
        )
    if gate.get(
        "real_vault_creation_allowed"
    ):
        raise BuilderError(
            "next-action gate unexpectedly allows Vault"
        )
    if gate.get("obsidian_open_allowed"):
        raise BuilderError(
            "Obsidian opening unexpectedly authorized"
        )


def _render_artifacts(
    records: Sequence[SemanticRecord],
    contract: Mapping[str, Any],
) -> tuple[RenderedFile, ...]:
    rendered: list[RenderedFile] = []
    seen_paths: set[str] = set()

    for record in records:
        item = render_artifact(
            record,
            contract,
        )
        if item.relative_path in seen_paths:
            raise BuilderError(
                "artifact projection ID collision: "
                f"{item.relative_path}"
            )
        seen_paths.add(item.relative_path)
        rendered.append(item)

    rendered.sort(
        key=lambda item: item.relative_path
    )
    return tuple(rendered)


def _render_relations(
    relations: Sequence[RelationRecord],
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
            raise BuilderError(
                "relation projection ID collision: "
                f"{item.relative_path}"
            )
        seen_paths.add(item.relative_path)
        rendered.append(item)

    rendered.sort(
        key=lambda item: item.relative_path
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

    digests.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(digests)


def _build_manifest_bytes(
    *,
    source_repository: str,
    source_commit: str,
    source_tree: str,
    pilot_inventory_digest_sha256: str,
    semantic_record_digest_sha256: str,
    projection_contract_version: str,
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
            source_repository,
        "source_commit":
            source_commit,
        "source_tree":
            source_tree,
        "pilot_inventory_digest_sha256":
            pilot_inventory_digest_sha256,
        "semantic_record_digest_sha256":
            semantic_record_digest_sha256,
        "projection_contract_version":
            projection_contract_version,
        "renderer_version":
            RENDERER_VERSION,
        "relation_rule_registry_version":
            RELATION_RULE_REGISTRY_VERSION,
        "artifact_record_count":
            artifact_record_count,
        "relation_record_count":
            relation_record_count,
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
        raise BuilderError(
            "build-manifest field order drift"
        )

    return canonical_json_file_bytes(
        values
    )


def build_projection_from_records(
    *,
    source: Any,
    records: Sequence[SemanticRecord],
    pilot_inventory_digest_sha256: str,
    semantic_record_digest_sha256: str,
    contract: Mapping[str, Any],
    stage_root: Path,
) -> BuildResult:
    _assert_contract_boundary(
        contract
    )

    if not records:
        raise BuilderError(
            "semantic record set is empty"
        )

    source_repository = records[0].source_repository
    source_commit = records[0].source_commit
    source_tree = records[0].source_tree

    for record in records:
        if record.source_repository != source_repository:
            raise BuilderError(
                "mixed source_repository in semantic records"
            )
        if record.source_commit != source_commit:
            raise BuilderError(
                "mixed source_commit in semantic records"
            )
        if record.source_tree != source_tree:
            raise BuilderError(
                "mixed source_tree in semantic records"
            )

    actual_semantic_digest = records_digest_sha256(
        tuple(records)
    )
    if (
        actual_semantic_digest
        != semantic_record_digest_sha256
    ):
        raise BuilderError(
            "semantic-record digest mismatch"
        )

    create_stage_directories(
        stage_root
    )

    try:
        artifact_files = _render_artifacts(
            records,
            contract,
        )

        relations = extract_relations(
            source,
            records,
            contract,
        )
        relation_files = _render_relations(
            relations,
            contract,
        )

        artifact_digests = _write_rendered_set(
            stage_root,
            artifact_files,
        )
        relation_digests = _write_rendered_set(
            stage_root,
            relation_files,
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

        manifest_rendered = RenderedFile(
            relative_path=(
                "generated/manifests/"
                "integrity-manifest.json"
            ),
            content=manifest_bytes,
        )
        manifest_path = exclusive_write(
            stage_root,
            manifest_rendered,
        )
        manifest_digest = file_digest(
            stage_root,
            manifest_path,
        )

        statuses = verify_integrity_manifest(
            stage_root
        )
        not_clean = {
            path: status
            for path, status in statuses.items()
            if status != "CLEAN"
        }
        if not_clean:
            raise BuilderError(
                f"integrity verification failed: "
                f"{not_clean}"
            )

        tree_digest = projection_tree_digest(
            stage_root
        )

        build_manifest_bytes = _build_manifest_bytes(
            source_repository=source_repository,
            source_commit=source_commit,
            source_tree=source_tree,
            pilot_inventory_digest_sha256=(
                pilot_inventory_digest_sha256
            ),
            semantic_record_digest_sha256=(
                semantic_record_digest_sha256
            ),
            projection_contract_version=(
                contract["schema"]
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
            contract=contract,
        )

        exclusive_write(
            stage_root,
            RenderedFile(
                relative_path=(
                    "generated/manifests/"
                    "build-manifest.json"
                ),
                content=build_manifest_bytes,
            ),
        )

        generated_files = all_generated_files(
            stage_root
        )

    except (
        IntegrityError,
        RenderingError,
    ) as exc:
        raise BuilderError(str(exc)) from exc

    return BuildResult(
        stage_root=str(stage_root),
        artifact_record_count=len(
            artifact_files
        ),
        relation_record_count=len(
            relation_files
        ),
        semantic_record_digest_sha256=(
            semantic_record_digest_sha256
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
        deterministic_file_count=(
            len(artifact_files)
            + len(relation_files)
            + 1
        ),
        generated_file_count=len(
            generated_files
        ),
    )

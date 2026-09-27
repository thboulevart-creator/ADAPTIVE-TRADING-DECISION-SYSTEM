from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .current_head_projection import (
    CurrentHeadBuildResult,
)
from .current_head_semantic_bridge import (
    CurrentHeadSemanticBridgeResult,
)
from .integrity import (
    IntegrityError,
    all_generated_files,
    verify_integrity_manifest,
)
from .rendering import artifact_record_id


class CurrentHeadBreakerError(RuntimeError):
    pass


class CurrentHeadBreakerInfrastructureError(
    CurrentHeadBreakerError
):
    pass


EVALUATOR_CONTRACT_BLOB = (
    "b6c17167875874db30a575be95e8e6aa33d630dd"
)
PROJECTION_CONTRACT_BLOB = (
    "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2"
)
MANIFEST_SCHEMA = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_BREAKER_MANIFEST_V0_1"
)
RESULT_SCHEMA = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_BREAKER_RESULT_V0_1"
)


@dataclass(frozen=True)
class CurrentHeadBreakerResult:
    manifest_digest_sha256: str
    result_digest_sha256: str
    status: str
    breaker_statuses: tuple[
        tuple[str, str], ...
    ]

    @property
    def all_pass(self) -> bool:
        return self.status == "PASS"


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CurrentHeadBreakerError(
            "value is not canonical JSON"
        ) from exc


def _sha256(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _load_evaluator_contract() -> dict[str, Any]:
    path = Path(__file__).with_name(
        "finite_candidate_evaluator_contract_v0_1.json"
    )
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise CurrentHeadBreakerInfrastructureError(
            "finite evaluator contract unavailable"
        ) from exc
    if not isinstance(value, dict):
        raise CurrentHeadBreakerError(
            "finite evaluator contract must be object"
        )
    return value


def _generated_bytes(
    stage_root: Path,
) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    try:
        entries = all_generated_files(
            stage_root
        )
        for entry in entries:
            path = stage_root.joinpath(
                *entry.relative_path.split("/")
            )
            result[entry.relative_path] = (
                path.read_bytes()
            )
    except OSError as exc:
        raise CurrentHeadBreakerInfrastructureError(
            "generated file read unavailable"
        ) from exc
    except IntegrityError as exc:
        message = str(exc)
        if any(
            marker in message
            for marker in (
                "cannot lstat",
                "cannot stat",
                "hard-link count unavailable",
                "junction check failed",
            )
        ):
            raise CurrentHeadBreakerInfrastructureError(
                message
            ) from exc
        raise CurrentHeadBreakerError(
            message
        ) from exc
    return result


def _load_build_manifest(
    stage_root: Path,
) -> dict[str, Any]:
    path = (
        stage_root
        / "generated"
        / "manifests"
        / "build-manifest.json"
    )
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except OSError as exc:
        raise CurrentHeadBreakerInfrastructureError(
            "build manifest read unavailable"
        ) from exc
    except json.JSONDecodeError as exc:
        raise CurrentHeadBreakerError(
            "build manifest is invalid JSON"
        ) from exc

    if not isinstance(value, dict):
        raise CurrentHeadBreakerError(
            "build manifest must be object"
        )
    return value


def _manifest_and_digest(
    contract: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    spec = contract[
        "projection_breaker_manifest"
    ]
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "breakers": spec["breakers"],
    }
    return manifest, _sha256(manifest)


def _forbidden_generated_surface(
    relative_path: str,
) -> bool:
    parts = relative_path.split("/")
    if any(
        part in {".git", ".obsidian", "views"}
        for part in parts
    ):
        return True
    return any(
        part in {
            "CURRENT",
            "CURRENT.md",
            "CURRENT.json",
            "CURRENT.tmp",
        }
        for part in parts
    )


def run_current_head_projection_breakers(
    *,
    bridge: CurrentHeadSemanticBridgeResult,
    build_a: CurrentHeadBuildResult,
    build_b: CurrentHeadBuildResult,
    evaluator_contract: Mapping[str, Any] | None = None,
) -> CurrentHeadBreakerResult:
    contract = (
        _load_evaluator_contract()
        if evaluator_contract is None
        else dict(evaluator_contract)
    )

    if contract.get("schema") != (
        "ATDS_OBSIDIAN_P5D3D_FINITE_CANDIDATE_EVALUATOR_CONTRACT_V0_1"
    ):
        raise CurrentHeadBreakerError(
            "finite evaluator contract schema mismatch"
        )

    manifest, manifest_digest = (
        _manifest_and_digest(
            contract
        )
    )
    breaker_ids = [
        item["id"]
        for item in manifest["breakers"]
    ]
    if breaker_ids != [
        f"CHP-B{index:02d}"
        for index in range(1, 13)
    ]:
        raise CurrentHeadBreakerError(
            "projection breaker registry drift"
        )

    stage_a = Path(build_a.stage_root)
    stage_b = Path(build_b.stage_root)

    files_a = _generated_bytes(stage_a)
    files_b = _generated_bytes(stage_b)
    build_manifest_a = _load_build_manifest(
        stage_a
    )
    build_manifest_b = _load_build_manifest(
        stage_b
    )

    try:
        integrity_a = verify_integrity_manifest(
            stage_a
        )
        integrity_b = verify_integrity_manifest(
            stage_b
        )
    except IntegrityError as exc:
        message = str(exc)
        if any(
            marker in message
            for marker in (
                "cannot lstat",
                "cannot stat",
                "hard-link count unavailable",
                "junction check failed",
            )
        ):
            raise CurrentHeadBreakerInfrastructureError(
                message
            ) from exc
        integrity_a = {"__breaker__": "INVALID"}
        integrity_b = {"__breaker__": "INVALID"}

    artifact_ids = {
        artifact_record_id(
            bridge.source_repository,
            entry.source_path,
        )
        for entry in bridge.entries
    }
    bridge_by_path = {
        entry.source_path: entry
        for entry in bridge.entries
    }

    audit_a = {
        row.source_path: row
        for row in build_a.body_read_audit_rows
    }
    audit_b = {
        row.source_path: row
        for row in build_b.body_read_audit_rows
    }

    b01 = (
        build_a.artifact_record_count
        == build_a.source_record_count
        == len(bridge.entries)
        and build_b.artifact_record_count
        == build_b.source_record_count
        == len(bridge.entries)
    )

    b02 = (
        build_a.metadata_only_body_read_count == 0
        and build_b.metadata_only_body_read_count == 0
        and all(
            row.content_mode != "METADATA_ONLY"
            for row in (
                *build_a.body_read_audit_rows,
                *build_b.body_read_audit_rows,
            )
        )
    )

    def audit_rows_eligible(
        build: CurrentHeadBuildResult,
    ) -> bool:
        for row in build.body_read_audit_rows:
            entry = bridge_by_path.get(
                row.source_path
            )
            if entry is None:
                return False
            suffix = (
                "." + row.source_path.rsplit(
                    ".", 1
                )[-1].lower()
                if "." in row.source_path.rsplit(
                    "/", 1
                )[-1]
                else ""
            )
            if (
                row.content_mode != "FULL_TEXT"
                or entry.content_mode != "FULL_TEXT"
                or not entry.downstream_body_read_allowed
                or row.source_blob_sha
                != entry.source_blob_sha
                or suffix not in {".md", ".json"}
            ):
                return False
        return True

    b03 = (
        audit_rows_eligible(build_a)
        and audit_rows_eligible(build_b)
    )

    b04 = all(
        relation.evidence_source_path in audit_a
        for relation in build_a.relation_records
    ) and all(
        relation.evidence_source_path in audit_b
        for relation in build_b.relation_records
    )

    b05 = all(
        relation.target_record_id in artifact_ids
        for relation in (
            *build_a.relation_records,
            *build_b.relation_records,
        )
    )

    b06 = not any(
        _forbidden_generated_surface(path)
        for path in (
            *files_a.keys(),
            *files_b.keys(),
        )
    )

    b07 = (
        bool(integrity_a)
        and bool(integrity_b)
        and all(
            value == "CLEAN"
            for value in integrity_a.values()
        )
        and all(
            value == "CLEAN"
            for value in integrity_b.values()
        )
    )

    expected_manifest_identity = {
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
    }

    b08 = all(
        manifest_value.get(key) == value
        for manifest_value in (
            build_manifest_a,
            build_manifest_b,
        )
        for key, value
        in expected_manifest_identity.items()
    )

    pilot_fields = {
        "pilot_inventory_digest_sha256",
        "pilot_source_count",
    }
    b09 = all(
        not (
            pilot_fields
            & set(manifest_value.keys())
        )
        for manifest_value in (
            build_manifest_a,
            build_manifest_b,
        )
    )

    b10 = (
        set(files_a) == set(files_b)
        and all(
            files_a[path] == files_b[path]
            for path in files_a
        )
    )

    b11 = (
        build_a.body_read_audit_digest_sha256
        == build_b.body_read_audit_digest_sha256
        and build_a.relation_source_body_read_count
        == build_b.relation_source_body_read_count
        and build_a.metadata_only_body_read_count
        == build_b.metadata_only_body_read_count
        and build_a.body_read_audit_rows
        == build_b.body_read_audit_rows
    )

    try:
        distinct_roots = (
            stage_a.resolve()
            != stage_b.resolve()
        )
    except OSError as exc:
        raise CurrentHeadBreakerInfrastructureError(
            "stage-root resolution unavailable"
        ) from exc

    b12 = distinct_roots

    booleans = (
        b01,
        b02,
        b03,
        b04,
        b05,
        b06,
        b07,
        b08,
        b09,
        b10,
        b11,
        b12,
    )

    statuses = tuple(
        (
            breaker_id,
            "PASS" if passed else "FAIL",
        )
        for breaker_id, passed
        in zip(breaker_ids, booleans)
    )
    overall = (
        "PASS"
        if all(booleans)
        else "FAIL"
    )

    result_payload = {
        "schema": RESULT_SCHEMA,
        "manifest_digest_sha256":
            manifest_digest,
        "candidate_head":
            bridge.source_commit,
        "candidate_tree":
            bridge.source_tree,
        "projection_contract_blob":
            PROJECTION_CONTRACT_BLOB,
        "breaker_statuses": [
            {
                "id": breaker_id,
                "status": status,
            }
            for breaker_id, status
            in statuses
        ],
        "status": overall,
    }

    return CurrentHeadBreakerResult(
        manifest_digest_sha256=(
            manifest_digest
        ),
        result_digest_sha256=(
            _sha256(result_payload)
        ),
        status=overall,
        breaker_statuses=statuses,
    )

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Protocol

from .classification import git_blob_oid
from .current_head_semantic_bridge import (
    CurrentHeadBridgeEntry,
    CurrentHeadSemanticBridgeResult,
)
from .git_source import GitSourceError
from .rendering import (
    artifact_record_id,
    relation_record_id,
)


class CurrentHeadRelationError(RuntimeError):
    pass


class CurrentHeadRelationInfrastructureError(
    CurrentHeadRelationError
):
    pass


class BlobReader(Protocol):
    def read_blob(self, oid: str) -> bytes: ...


PROJECTION_CONTRACT_BLOB = (
    "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2"
)
RELATION_RULE_REGISTRY_VERSION = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_RELATION_RULES_V0_1"
)
_BODY_READ_PURPOSE = "RELATION_EXPLICIT_PATH_EXTRACTION"

_LABELED_BACKTICK_PATH = re.compile(
    r"^\s*(?:[-*]\s*)?"
    r"[^:\n]{1,120}:\s*"
    r"\x60([^\x60\r\n]+)\x60"
    r"(?:\s*[.;,]?\s*)$"
)


@dataclass(frozen=True)
class BodyReadAuditRow:
    source_path: str
    source_blob_sha: str
    content_mode: str
    purpose: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class CurrentHeadRelationRecord:
    projection_relation_id: str
    source_record_id: str
    relation_type: str
    target_record_id: str
    basis: str
    evidence_source_path: str
    evidence_source_blob_sha: str
    source_commit: str


@dataclass(frozen=True)
class CurrentHeadRelationResult:
    relations: tuple[CurrentHeadRelationRecord, ...]
    body_read_audit_rows: tuple[BodyReadAuditRow, ...]
    body_read_audit_digest_sha256: str
    relation_source_body_read_count: int
    metadata_only_body_read_count: int


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise CurrentHeadRelationError(
            "value is not canonical JSON"
        ) from exc
    return encoded.encode("utf-8")


def _audit_digest(
    rows: tuple[BodyReadAuditRow, ...],
) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(
            [row.as_dict() for row in rows]
        )
    ).hexdigest()


def _suffix(source_path: str) -> str:
    name = source_path.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return "." + name.rsplit(".", 1)[-1].lower()


def _walk_json_strings(
    value: Any,
) -> Iterable[str]:
    if isinstance(value, dict):
        for child in value.values():
            if isinstance(child, str):
                yield child
            else:
                yield from _walk_json_strings(child)
        return

    if isinstance(value, list):
        for child in value:
            if isinstance(child, str):
                yield child
            else:
                yield from _walk_json_strings(child)


def _structured_targets(
    text: str,
    exact_paths: set[str],
) -> set[str]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return set()

    return {
        value.strip()
        for value in _walk_json_strings(parsed)
        if value.strip() in exact_paths
    }


def _labeled_text_targets(
    text: str,
    exact_paths: set[str],
) -> set[str]:
    targets: set[str] = set()
    for line in text.splitlines():
        match = _LABELED_BACKTICK_PATH.match(line)
        if match is None:
            continue
        candidate = match.group(1).strip()
        if candidate in exact_paths:
            targets.add(candidate)
    return targets


def _validate_contract(
    contract: Mapping[str, Any],
) -> None:
    if contract.get("schema") != (
        "ATDS_OBSIDIAN_CURRENT_HEAD_PROJECTION_CONTRACT_V0_1"
    ):
        raise CurrentHeadRelationError(
            "current-head projection contract schema mismatch"
        )

    relation = contract.get("relation_record")
    if not isinstance(relation, dict):
        raise CurrentHeadRelationError(
            "relation_record contract missing"
        )

    if relation.get(
        "legacy_extract_relations_direct_reuse_allowed"
    ) is not False:
        raise CurrentHeadRelationError(
            "legacy relation extractor unexpectedly authorized"
        )

    if relation.get("allowed_relation_types") != [
        "REFERENCES"
    ]:
        raise CurrentHeadRelationError(
            "unexpected relation type authority"
        )

    if relation.get("allowed_basis") != [
        "EXPLICIT_STRUCTURED",
        "EXPLICIT_TEXT",
    ]:
        raise CurrentHeadRelationError(
            "unexpected relation basis authority"
        )

    body = contract.get("body_read_authority")
    if not isinstance(body, dict):
        raise CurrentHeadRelationError(
            "body-read authority missing"
        )
    if body.get("metadata_only_body_read_allowed") is not False:
        raise CurrentHeadRelationError(
            "METADATA_ONLY body read unexpectedly authorized"
        )
    if body.get(
        "full_text_non_relation_suffix_body_read_allowed"
    ) is not False:
        raise CurrentHeadRelationError(
            "nonrelation FULL_TEXT body read unexpectedly authorized"
        )


def _validate_bridge_entry(
    entry: CurrentHeadBridgeEntry,
) -> None:
    if entry.semantic_body_read:
        raise CurrentHeadRelationError(
            "bridge semantic_body_read must remain false"
        )

    if entry.content_mode == "METADATA_ONLY":
        if entry.downstream_body_read_allowed:
            raise CurrentHeadRelationError(
                "METADATA_ONLY downstream body read unexpectedly allowed"
            )
        return

    if entry.content_mode != "FULL_TEXT":
        raise CurrentHeadRelationError(
            "unknown bridge content_mode"
        )

    if not entry.downstream_body_read_allowed:
        raise CurrentHeadRelationError(
            "FULL_TEXT bridge entry unexpectedly denies downstream read"
        )


def _read_eligible_blob(
    source: BlobReader,
    entry: CurrentHeadBridgeEntry,
) -> bytes:
    try:
        raw = source.read_blob(
            entry.source_blob_sha
        )
    except (GitSourceError, OSError) as exc:
        raise CurrentHeadRelationInfrastructureError(
            "source blob read unavailable"
        ) from exc

    if git_blob_oid(raw) != entry.source_blob_sha:
        raise CurrentHeadRelationError(
            "body-read blob SHA differs from bridge entry"
        )
    if len(raw) != entry.source_blob_size:
        raise CurrentHeadRelationError(
            "body-read blob size differs from bridge entry"
        )
    return raw


def extract_current_head_relations(
    *,
    source: BlobReader,
    bridge: CurrentHeadSemanticBridgeResult,
    contract: Mapping[str, Any],
) -> CurrentHeadRelationResult:
    _validate_contract(contract)

    if not isinstance(
        bridge,
        CurrentHeadSemanticBridgeResult,
    ):
        raise CurrentHeadRelationError(
            "bridge result type mismatch"
        )

    entries = tuple(bridge.entries)
    if not entries:
        raise CurrentHeadRelationError(
            "empty bridge is forbidden"
        )

    expected_order = tuple(
        sorted(
            entries,
            key=lambda item:
                item.source_path.encode("utf-8"),
        )
    )
    if entries != expected_order:
        raise CurrentHeadRelationError(
            "bridge entries are not bytewise source-path sorted"
        )

    exact_paths: set[str] = set()
    record_ids: dict[str, str] = {}

    for entry in entries:
        _validate_bridge_entry(entry)
        if entry.source_path in exact_paths:
            raise CurrentHeadRelationError(
                "duplicate bridge source_path"
            )
        exact_paths.add(entry.source_path)
        record_ids[entry.source_path] = (
            artifact_record_id(
                bridge.source_repository,
                entry.source_path,
            )
        )

    relations: list[CurrentHeadRelationRecord] = []
    audit_rows: list[BodyReadAuditRow] = []
    seen_relation_ids: set[str] = set()

    for entry in entries:
        suffix = _suffix(entry.source_path)

        if entry.content_mode == "METADATA_ONLY":
            continue

        if suffix not in {".md", ".json"}:
            continue

        if not entry.downstream_body_read_allowed:
            raise CurrentHeadRelationError(
                "eligible FULL_TEXT entry lacks body-read authority"
            )

        raw = _read_eligible_blob(
            source,
            entry,
        )
        audit_rows.append(
            BodyReadAuditRow(
                source_path=entry.source_path,
                source_blob_sha=entry.source_blob_sha,
                content_mode=entry.content_mode,
                purpose=_BODY_READ_PURPOSE,
            )
        )

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CurrentHeadRelationError(
                "eligible relation source is not UTF-8"
            ) from exc

        if suffix == ".json":
            targets = _structured_targets(
                text,
                exact_paths,
            )
            basis = "EXPLICIT_STRUCTURED"
        else:
            targets = _labeled_text_targets(
                text,
                exact_paths,
            )
            basis = "EXPLICIT_TEXT"

        source_record_id = record_ids[
            entry.source_path
        ]

        for target_path in sorted(
            targets,
            key=lambda item: item.encode("utf-8"),
        ):
            if target_path == entry.source_path:
                continue

            target_record_id = record_ids.get(
                target_path
            )
            if target_record_id is None:
                continue

            relation_id = relation_record_id(
                source_record_id,
                "REFERENCES",
                target_record_id,
                basis,
                entry.source_path,
                entry.source_blob_sha,
            )
            if relation_id in seen_relation_ids:
                raise CurrentHeadRelationError(
                    "relation projection ID collision"
                )
            seen_relation_ids.add(relation_id)

            relations.append(
                CurrentHeadRelationRecord(
                    projection_relation_id=relation_id,
                    source_record_id=source_record_id,
                    relation_type="REFERENCES",
                    target_record_id=target_record_id,
                    basis=basis,
                    evidence_source_path=(
                        entry.source_path
                    ),
                    evidence_source_blob_sha=(
                        entry.source_blob_sha
                    ),
                    source_commit=(
                        bridge.source_commit
                    ),
                )
            )

    audit_rows.sort(
        key=lambda row:
            row.source_path.encode("utf-8")
    )
    relations.sort(
        key=lambda relation:
            relation.projection_relation_id.encode(
                "ascii"
            )
    )

    audit_tuple = tuple(audit_rows)
    relation_tuple = tuple(relations)

    if any(
        row.content_mode == "METADATA_ONLY"
        for row in audit_tuple
    ):
        raise CurrentHeadRelationError(
            "METADATA_ONLY appeared in body-read audit"
        )

    return CurrentHeadRelationResult(
        relations=relation_tuple,
        body_read_audit_rows=audit_tuple,
        body_read_audit_digest_sha256=(
            _audit_digest(audit_tuple)
        ),
        relation_source_body_read_count=(
            len(audit_tuple)
        ),
        metadata_only_body_read_count=0,
    )

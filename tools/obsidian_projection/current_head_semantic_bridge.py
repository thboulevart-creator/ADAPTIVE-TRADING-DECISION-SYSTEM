from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

from .classification import (
    SemanticRecord,
    records_digest_sha256,
)
from .dynamic_inventory import (
    DynamicInventory,
    DynamicInventoryEntry,
)


class CurrentHeadSemanticBridgeError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CONTRACT_BLOB = "d1018443ce4dbbac614f0a65185ffd51ca7ffd69"

RESULT_SCHEMA = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_SEMANTIC_BRIDGE_RESULT_V0_1"
)
ENTRY_SCHEMA = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_SEMANTIC_BRIDGE_ENTRY_V0_1"
)
SEMANTIC_RECORD_SCHEMA = "ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1"

_ALLOWED_CONTENT_MODES = frozenset(
    {
        "FULL_TEXT",
        "METADATA_ONLY",
    }
)
_ALLOWED_GIT_MODES = frozenset(
    {
        "100644",
        "100755",
    }
)
_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")

_FULL_TEXT_FAMILY_BY_EXTENSION = {
    ".md": "DOCUMENT",
    ".py": "CODE",
    ".js": "CODE",
    ".jsx": "CODE",
    ".ts": "CODE",
    ".tsx": "CODE",
    ".sql": "CODE",
    ".sh": "CODE",
    ".ps1": "CODE",
    ".bat": "CODE",
    ".cmd": "CODE",
    ".json": "STRUCTURED_DATA",
    ".yml": "STRUCTURED_DATA",
    ".yaml": "STRUCTURED_DATA",
    ".toml": "STRUCTURED_DATA",
    ".ini": "STRUCTURED_DATA",
    ".cfg": "STRUCTURED_DATA",
    ".csv": "STRUCTURED_DATA",
    ".tsv": "STRUCTURED_DATA",
    ".xml": "STRUCTURED_DATA",
    ".html": "WEB_ASSET",
    ".css": "WEB_ASSET",
    ".txt": "TEXT",
}


def _canonical_json_bytes(
    value: Any,
    *,
    terminal_lf: bool,
) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise CurrentHeadSemanticBridgeError(
            "value is not canonical JSON"
        ) from exc

    if terminal_lf:
        encoded += "\n"
    return encoded.encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(
            value,
            terminal_lf=False,
        )
    ).hexdigest()


def _extension(source_path: str) -> str:
    name = source_path.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return "." + name.rsplit(".", 1)[-1].lower()


def _validate_source_path(source_path: Any) -> str:
    if not isinstance(source_path, str) or not source_path:
        raise CurrentHeadSemanticBridgeError(
            "invalid source_path"
        )
    if source_path.startswith(("/", "\\")):
        raise CurrentHeadSemanticBridgeError(
            "absolute source_path forbidden"
        )
    if "\\" in source_path:
        raise CurrentHeadSemanticBridgeError(
            "backslash source_path forbidden"
        )
    if ".." in source_path.split("/"):
        raise CurrentHeadSemanticBridgeError(
            "parent traversal forbidden"
        )
    return source_path


def _validate_head(value: Any, field: str) -> str:
    if (
        not isinstance(value, str)
        or _HEAD_RE.fullmatch(value) is None
    ):
        raise CurrentHeadSemanticBridgeError(
            f"{field} must be lowercase 40-hex SHA-1"
        )
    return value


def _validate_entry(
    entry: DynamicInventoryEntry,
) -> None:
    if not isinstance(entry, DynamicInventoryEntry):
        raise CurrentHeadSemanticBridgeError(
            "inventory entry type mismatch"
        )

    _validate_source_path(entry.source_path)
    _validate_head(
        entry.source_blob_sha,
        "source_blob_sha",
    )

    if (
        isinstance(entry.source_blob_size, bool)
        or not isinstance(entry.source_blob_size, int)
        or entry.source_blob_size < 0
    ):
        raise CurrentHeadSemanticBridgeError(
            "invalid source_blob_size"
        )

    if entry.git_mode not in _ALLOWED_GIT_MODES:
        raise CurrentHeadSemanticBridgeError(
            "unsupported git_mode"
        )

    if (
        not isinstance(entry.selection_zone, str)
        or not entry.selection_zone
    ):
        raise CurrentHeadSemanticBridgeError(
            "invalid selection_zone"
        )

    if entry.content_mode not in _ALLOWED_CONTENT_MODES:
        raise CurrentHeadSemanticBridgeError(
            "unsupported content_mode"
        )


def _artifact_family(
    entry: DynamicInventoryEntry,
) -> str:
    if entry.content_mode == "METADATA_ONLY":
        return "METADATA_ONLY"

    extension = _extension(entry.source_path)
    family = _FULL_TEXT_FAMILY_BY_EXTENSION.get(
        extension
    )
    if family is None:
        raise CurrentHeadSemanticBridgeError(
            "unsupported FULL_TEXT extension"
        )
    return family


def _semantic_record(
    inventory: DynamicInventory,
    entry: DynamicInventoryEntry,
    artifact_family: str,
) -> SemanticRecord:
    return SemanticRecord(
        record_schema=SEMANTIC_RECORD_SCHEMA,
        record_type="ARTIFACT",
        source_repository=inventory.source_repository,
        source_branch=inventory.source_branch,
        source_commit=inventory.source_commit,
        source_tree=inventory.source_tree,
        source_path=entry.source_path,
        source_blob_sha=entry.source_blob_sha,
        source_blob_size=entry.source_blob_size,
        artifact_family=artifact_family,
        semantic_role="UNKNOWN",
        procedure_role="NONE",
        authority_role="CANONICAL",
        qualification_status="UNKNOWN",
        qualification_scope=None,
        scientific_status="UNKNOWN",
        epistemic_role="UNKNOWN",
        temporal_role="UNKNOWN",
        persistence_state="TRACKED_IN_GIT_TREE",
        limitations=(),
        non_claims=(),
    )


@dataclass(frozen=True)
class CurrentHeadBridgeEntry:
    source_path: str
    source_blob_sha: str
    source_blob_size: int
    git_mode: str
    selection_zone: str
    content_mode: str
    disposition: str
    artifact_family: str
    semantic_body_read: bool
    downstream_body_read_allowed: bool
    semantic_record: SemanticRecord

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": ENTRY_SCHEMA,
            "source_path": self.source_path,
            "source_blob_sha": self.source_blob_sha,
            "source_blob_size": self.source_blob_size,
            "git_mode": self.git_mode,
            "selection_zone": self.selection_zone,
            "content_mode": self.content_mode,
            "disposition": self.disposition,
            "artifact_family": self.artifact_family,
            "semantic_body_read": self.semantic_body_read,
            "downstream_body_read_allowed":
                self.downstream_body_read_allowed,
            "semantic_record":
                self.semantic_record.to_dict(),
        }


@dataclass(frozen=True)
class CurrentHeadSemanticBridgeResult:
    source_repository: str
    source_branch: str
    source_commit: str
    source_tree: str
    dynamic_inventory_digest_sha256: str
    entries: tuple[CurrentHeadBridgeEntry, ...]

    @property
    def semantic_records(
        self,
    ) -> tuple[SemanticRecord, ...]:
        return tuple(
            entry.semantic_record
            for entry in self.entries
        )

    @property
    def full_text_count(self) -> int:
        return sum(
            entry.content_mode == "FULL_TEXT"
            for entry in self.entries
        )

    @property
    def metadata_only_count(self) -> int:
        return sum(
            entry.content_mode == "METADATA_ONLY"
            for entry in self.entries
        )

    @property
    def semantic_record_digest_sha256(self) -> str:
        return records_digest_sha256(
            self.semantic_records
        )

    @property
    def bridge_entry_digest_sha256(self) -> str:
        return _sha256(
            [
                entry.as_dict()
                for entry in self.entries
            ]
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": RESULT_SCHEMA,
            "source_repository": self.source_repository,
            "source_branch": self.source_branch,
            "source_commit": self.source_commit,
            "source_tree": self.source_tree,
            "dynamic_inventory_digest_sha256":
                self.dynamic_inventory_digest_sha256,
            "bridge_contract_version": CONTRACT_BLOB,
            "source_blob_count": len(self.entries),
            "full_text_count": self.full_text_count,
            "metadata_only_count":
                self.metadata_only_count,
            "semantic_record_count":
                len(self.semantic_records),
            "semantic_record_digest_sha256":
                self.semantic_record_digest_sha256,
            "bridge_entry_digest_sha256":
                self.bridge_entry_digest_sha256,
            "entries": [
                entry.as_dict()
                for entry in self.entries
            ],
        }

    def canonical_json_bytes(self) -> bytes:
        return _canonical_json_bytes(
            self.as_dict(),
            terminal_lf=True,
        )


def build_current_head_semantic_bridge(
    inventory: DynamicInventory,
) -> CurrentHeadSemanticBridgeResult:
    if not isinstance(inventory, DynamicInventory):
        raise CurrentHeadSemanticBridgeError(
            "input must be DynamicInventory"
        )

    if inventory.source_repository != EXPECTED_REPOSITORY:
        raise CurrentHeadSemanticBridgeError(
            "source repository mismatch"
        )
    if inventory.source_branch != EXPECTED_BRANCH:
        raise CurrentHeadSemanticBridgeError(
            "source branch mismatch"
        )

    _validate_head(
        inventory.source_commit,
        "source_commit",
    )
    _validate_head(
        inventory.source_tree,
        "source_tree",
    )

    entries = tuple(inventory.entries)
    expected_order = tuple(
        sorted(
            entries,
            key=lambda item:
                item.source_path.encode("utf-8"),
        )
    )
    if entries != expected_order:
        raise CurrentHeadSemanticBridgeError(
            "inventory entries are not bytewise sorted"
        )

    seen_paths: set[str] = set()
    bridge_entries: list[
        CurrentHeadBridgeEntry
    ] = []

    for entry in entries:
        _validate_entry(entry)

        if entry.source_path in seen_paths:
            raise CurrentHeadSemanticBridgeError(
                "duplicate source_path"
            )
        seen_paths.add(entry.source_path)

        family = _artifact_family(entry)
        disposition = (
            "SEMANTIC_FULL_TEXT"
            if entry.content_mode == "FULL_TEXT"
            else "SEMANTIC_METADATA_ONLY"
        )

        record = _semantic_record(
            inventory,
            entry,
            family,
        )

        bridge_entries.append(
            CurrentHeadBridgeEntry(
                source_path=entry.source_path,
                source_blob_sha=entry.source_blob_sha,
                source_blob_size=entry.source_blob_size,
                git_mode=entry.git_mode,
                selection_zone=entry.selection_zone,
                content_mode=entry.content_mode,
                disposition=disposition,
                artifact_family=family,
                semantic_body_read=False,
                downstream_body_read_allowed=(
                    entry.content_mode == "FULL_TEXT"
                ),
                semantic_record=record,
            )
        )

    result = CurrentHeadSemanticBridgeResult(
        source_repository=inventory.source_repository,
        source_branch=inventory.source_branch,
        source_commit=inventory.source_commit,
        source_tree=inventory.source_tree,
        dynamic_inventory_digest_sha256=(
            inventory.digest_sha256
        ),
        entries=tuple(bridge_entries),
    )

    if len(result.entries) != len(entries):
        raise CurrentHeadSemanticBridgeError(
            "bridge output count mismatch"
        )
    if len(result.semantic_records) != len(entries):
        raise CurrentHeadSemanticBridgeError(
            "semantic record count mismatch"
        )

    result.canonical_json_bytes()
    return result

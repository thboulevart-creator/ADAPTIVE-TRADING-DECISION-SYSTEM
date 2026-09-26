from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .git_source import FrozenGitSource, TreeEntry

_ALLOWED_CLASSES = frozenset(
    {
        "GOVERNANCE_ANCHOR",
        "CORE_PROTOCOL",
        "AP_PROGRAM",
        "EVIDENCE",
        "IMPLEMENTATION",
        "TEST",
        "BREAKER",
        "HISTORICAL_LINEAGE",
        "CORE_PROFILE",
    }
)


class InventoryError(RuntimeError):
    """Raised when the pilot inventory is malformed or diverges from Git."""


@dataclass(frozen=True)
class InventoryEntry:
    source_path: str
    source_blob_sha: str
    source_blob_size: int
    inventory_class: str


@dataclass(frozen=True)
class FrozenInventory:
    schema: str
    source_repository: str
    source_branch: str
    source_commit: str
    source_tree: str
    source_artifact_count: int
    entries: tuple[InventoryEntry, ...]

    def canonical_entries_bytes(self) -> bytes:
        payload = [
            {
                "inventory_class": entry.inventory_class,
                "source_blob_sha": entry.source_blob_sha,
                "source_blob_size": entry.source_blob_size,
                "source_path": entry.source_path,
            }
            for entry in sorted(
                self.entries,
                key=lambda item: item.source_path,
            )
        ]
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    @property
    def digest_sha256(self) -> str:
        return hashlib.sha256(
            self.canonical_entries_bytes()
        ).hexdigest()


@dataclass(frozen=True)
class VerifiedInventoryEntry:
    inventory: InventoryEntry
    git_tree_entry: TreeEntry


def _require_oid(value: object, field: str) -> str:
    if not isinstance(value, str) or len(value) != 40:
        raise InventoryError(
            f"{field} must be a full 40-character Git object id"
        )
    try:
        int(value, 16)
    except ValueError as exc:
        raise InventoryError(
            f"{field} must be hexadecimal"
        ) from exc
    return value.lower()


def load_inventory(path: str | Path) -> FrozenInventory:
    try:
        raw = json.loads(
            Path(path).read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise InventoryError(
            f"cannot read inventory: {exc}"
        ) from exc

    required_top_level = {
        "schema",
        "source_repository",
        "source_branch",
        "source_commit",
        "source_tree",
        "source_artifact_count",
        "entries",
    }
    missing = sorted(required_top_level - set(raw))
    if missing:
        raise InventoryError(
            f"inventory missing top-level fields: {missing}"
        )

    if raw["schema"] != "ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1":
        raise InventoryError(
            f"unsupported inventory schema: {raw['schema']!r}"
        )

    if not isinstance(raw["entries"], list):
        raise InventoryError("entries must be a list")

    entries: list[InventoryEntry] = []
    seen_paths: set[str] = set()

    for index, item in enumerate(raw["entries"]):
        if not isinstance(item, dict):
            raise InventoryError(
                f"entry {index} is not an object"
            )

        required = {
            "source_path",
            "source_blob_sha",
            "source_blob_size",
            "inventory_class",
        }
        missing_entry = sorted(required - set(item))
        if missing_entry:
            raise InventoryError(
                f"entry {index} missing fields: {missing_entry}"
            )

        source_path = item["source_path"]
        if (
            not isinstance(source_path, str)
            or not source_path
            or source_path.startswith(("/", "\\"))
        ):
            raise InventoryError(
                f"entry {index} has invalid source_path"
            )

        if ".." in Path(source_path).parts:
            raise InventoryError(
                f"entry {index} escapes repository path"
            )

        if source_path in seen_paths:
            raise InventoryError(
                f"duplicate inventory path: {source_path}"
            )
        seen_paths.add(source_path)

        inventory_class = item["inventory_class"]
        if inventory_class not in _ALLOWED_CLASSES:
            raise InventoryError(
                f"entry {index} has unknown inventory_class: "
                f"{inventory_class!r}"
            )

        source_blob_size = item["source_blob_size"]
        if (
            not isinstance(source_blob_size, int)
            or source_blob_size < 0
        ):
            raise InventoryError(
                f"entry {index} has invalid source_blob_size"
            )

        entries.append(
            InventoryEntry(
                source_path=source_path,
                source_blob_sha=_require_oid(
                    item["source_blob_sha"],
                    "source_blob_sha",
                ),
                source_blob_size=source_blob_size,
                inventory_class=inventory_class,
            )
        )

    declared_count = raw["source_artifact_count"]
    if (
        not isinstance(declared_count, int)
        or declared_count != len(entries)
    ):
        raise InventoryError(
            f"source_artifact_count mismatch: "
            f"declared={declared_count!r} actual={len(entries)}"
        )

    return FrozenInventory(
        schema=raw["schema"],
        source_repository=raw["source_repository"],
        source_branch=raw["source_branch"],
        source_commit=_require_oid(
            raw["source_commit"],
            "source_commit",
        ),
        source_tree=_require_oid(
            raw["source_tree"],
            "source_tree",
        ),
        source_artifact_count=declared_count,
        entries=tuple(entries),
    )


def verify_inventory(
    source: FrozenGitSource,
    inventory: FrozenInventory,
) -> tuple[VerifiedInventoryEntry, ...]:
    if inventory.source_repository != source.expected_repository:
        raise InventoryError(
            f"inventory repository mismatch: "
            f"expected={source.expected_repository} "
            f"inventory={inventory.source_repository}"
        )

    if inventory.source_commit != source.source_commit:
        raise InventoryError(
            f"inventory commit mismatch: "
            f"expected={source.source_commit} "
            f"inventory={inventory.source_commit}"
        )

    if inventory.source_tree != source.expected_tree:
        raise InventoryError(
            f"inventory tree mismatch: "
            f"expected={source.expected_tree} "
            f"inventory={inventory.source_tree}"
        )

    source.verify_repository()
    source.verify_frozen_source()
    tree = source.tree_entry_map()

    verified: list[VerifiedInventoryEntry] = []

    for item in inventory.entries:
        entry = tree.get(item.source_path)

        if entry is None:
            raise InventoryError(
                f"inventory path missing from frozen tree: "
                f"{item.source_path}"
            )

        if entry.object_type != "blob" or entry.mode == "120000":
            raise InventoryError(
                f"inventory path is not an admissible regular blob: "
                f"{item.source_path} "
                f"type={entry.object_type} mode={entry.mode}"
            )

        if entry.oid != item.source_blob_sha:
            raise InventoryError(
                f"blob mismatch for {item.source_path}: "
                f"expected={item.source_blob_sha} actual={entry.oid}"
            )

        if entry.size != item.source_blob_size:
            raise InventoryError(
                f"size mismatch for {item.source_path}: "
                f"expected={item.source_blob_size} actual={entry.size}"
            )

        verified.append(
            VerifiedInventoryEntry(item, entry)
        )

    if len(verified) != inventory.source_artifact_count:
        raise InventoryError(
            "verified inventory count mismatch"
        )

    return tuple(verified)

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol, Sequence

from .git_source import FrozenGitSource, TreeEntry


class DynamicInventoryError(RuntimeError):
    pass


class SensitivePathError(DynamicInventoryError):
    pass


class SecretDetectedError(DynamicInventoryError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CONTRACT_SCHEMA = "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_CONTRACT_V0_1"
CONTRACT_BLOB = "80729156f4ac51b760c4347f581f052a175b88b3"
INVENTORY_SCHEMA = "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1"
SECRET_SCANNER_VERSION = "ATDS_HIGH_CONFIDENCE_SECRET_SCAN_V0_1"
MAX_FULL_TEXT_BYTES = 1_048_576

FULL_TEXT_EXTENSIONS = frozenset(
    {
        ".md",
        ".py",
        ".json",
        ".yml",
        ".yaml",
        ".txt",
        ".toml",
        ".ini",
        ".cfg",
        ".csv",
        ".tsv",
        ".xml",
        ".html",
        ".css",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".sql",
        ".sh",
        ".ps1",
        ".bat",
        ".cmd",
    }
)

KNOWN_ZONES = (
    ("GOVERNANCE/", "GOVERNANCE"),
    ("docs/", "DOCUMENTATION"),
    ("evidence/", "EVIDENCE"),
    ("reports/", "REPORT"),
    ("requirements/", "REQUIREMENT"),
    ("src/", "IMPLEMENTATION"),
    ("tests/", "TEST"),
    ("tools/", "TOOL"),
    ("breakers/", "BREAKER"),
    (".github/", "GITHUB_AUTOMATION_OR_CONFIG"),
    ("04-REFERENCE/", "REFERENCE"),
    ("99-BACKUP/", "HISTORICAL_LINEAGE"),
)

FORBIDDEN_ROOT_PREFIXES = (
    "generated/",
    "views/",
    ".obsidian/",
    ".git/",
)
FORBIDDEN_COMPONENTS = frozenset(
    {
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".venv",
        "venv",
        "node_modules",
    }
)
FORBIDDEN_SUFFIXES = (".pyc", ".pyo")

SENSITIVE_PATH_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa*",
    "*/secrets/*",
    "*/credentials/*",
    "*credential*",
    "*private-key*",
    "*private_key*",
)

_SECRET_PATTERNS = (
    (
        "PRIVATE_KEY_BLOCK",
        re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
        ),
    ),
    (
        "AWS_ACCESS_KEY_ID",
        re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])"),
    ),
    (
        "GITHUB_CLASSIC_TOKEN",
        re.compile(
            r"(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{36,255}"
        ),
    ),
    (
        "GITHUB_FINE_GRAINED_TOKEN",
        re.compile(
            r"(?<![A-Za-z0-9])github_pat_[A-Za-z0-9_]{40,255}"
        ),
    ),
)


class GitInventorySource(Protocol):
    expected_repository: str
    source_commit: str
    expected_tree: str

    def verify_repository(self) -> None: ...

    def verify_frozen_source(self) -> None: ...

    def tree_entries(self) -> tuple[TreeEntry, ...]: ...

    def read_blob(self, oid: str) -> bytes: ...


@dataclass(frozen=True)
class DynamicInventoryEntry:
    source_path: str
    source_blob_sha: str
    source_blob_size: int
    git_mode: str
    selection_zone: str
    content_mode: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "source_blob_sha": self.source_blob_sha,
            "source_blob_size": self.source_blob_size,
            "git_mode": self.git_mode,
            "selection_zone": self.selection_zone,
            "content_mode": self.content_mode,
        }


@dataclass(frozen=True)
class DynamicInventory:
    source_repository: str
    source_branch: str
    source_commit: str
    source_tree: str
    entries: tuple[DynamicInventoryEntry, ...]

    @property
    def full_text_count(self) -> int:
        return sum(
            item.content_mode == "FULL_TEXT"
            for item in self.entries
        )

    @property
    def metadata_only_count(self) -> int:
        return sum(
            item.content_mode == "METADATA_ONLY"
            for item in self.entries
        )

    def canonical_entry_bytes(self) -> bytes:
        payload = [
            item.as_dict()
            for item in sorted(
                self.entries,
                key=lambda item:
                    item.source_path.encode("utf-8"),
            )
        ]
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

    @property
    def digest_sha256(self) -> str:
        return hashlib.sha256(
            self.canonical_entry_bytes()
        ).hexdigest()

    def as_dict(self) -> dict[str, Any]:
        entries = sorted(
            self.entries,
            key=lambda item:
                item.source_path.encode("utf-8"),
        )
        return {
            "schema": INVENTORY_SCHEMA,
            "source_repository": self.source_repository,
            "source_branch": self.source_branch,
            "source_commit": self.source_commit,
            "source_tree": self.source_tree,
            "selection_contract_version": CONTRACT_BLOB,
            "source_blob_count": len(entries),
            "full_text_count": self.full_text_count,
            "metadata_only_count": self.metadata_only_count,
            "entries": [
                item.as_dict()
                for item in entries
            ],
            "inventory_digest_sha256": self.digest_sha256,
        }

    def canonical_json_bytes(self) -> bytes:
        return (
            json.dumps(
                self.as_dict(),
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def verify_contract(package_dir: Path) -> dict[str, Any]:
    path = package_dir / "dynamic_inventory_contract_v0_1.json"
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DynamicInventoryError(
            "P5-B contract unreadable"
        ) from exc

    actual = _git_blob_oid(raw)
    if actual != CONTRACT_BLOB:
        raise DynamicInventoryError(
            "P5-B contract blob mismatch"
        )
    if value.get("schema") != CONTRACT_SCHEMA:
        raise DynamicInventoryError(
            "unexpected P5-B contract schema"
        )
    return value


def _contains_surrogate(value: str) -> bool:
    return any(
        0xD800 <= ord(char) <= 0xDFFF
        for char in value
    )


def _validate_source_path(path: str) -> None:
    if not path:
        raise DynamicInventoryError(
            "empty source path"
        )
    if path.startswith(("/", "\\")):
        raise DynamicInventoryError(
            "absolute source path forbidden"
        )
    if "\\" in path:
        raise DynamicInventoryError(
            "backslash source separator forbidden"
        )
    if _contains_surrogate(path):
        raise DynamicInventoryError(
            "undecodable source path forbidden"
        )

    parts = path.split("/")
    if ".." in parts:
        raise DynamicInventoryError(
            "parent traversal forbidden"
        )


def _forbidden_surface(path: str) -> bool:
    lowered = path.lower()
    if any(
        lowered.startswith(prefix.lower())
        for prefix in FORBIDDEN_ROOT_PREFIXES
    ):
        return True

    components = {
        part.lower()
        for part in path.split("/")
    }
    if components & {
        item.lower()
        for item in FORBIDDEN_COMPONENTS
    }:
        return True

    return lowered.endswith(FORBIDDEN_SUFFIXES)


def _sensitive_path(path: str) -> bool:
    lowered = path.lower()
    base = lowered.rsplit("/", 1)[-1]
    components = lowered.split("/")

    if any(
        part in {"secrets", "credentials"}
        for part in components[:-1]
    ):
        return True

    candidates = {lowered, base}
    for pattern in SENSITIVE_PATH_PATTERNS:
        pattern_lower = pattern.lower()
        if any(
            fnmatch.fnmatchcase(candidate, pattern_lower)
            for candidate in candidates
        ):
            return True
    return False


def _path_hash(path: str) -> str:
    return hashlib.sha256(
        path.encode("utf-8")
    ).hexdigest()


def selection_zone(path: str) -> str:
    for prefix, zone in KNOWN_ZONES:
        if path.startswith(prefix):
            return zone
    if "/" not in path:
        return "ROOT_DOCUMENT"
    return "OTHER_TRACKED"


def _extension(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    if "." not in name:
        return ""
    return "." + name.rsplit(".", 1)[-1].lower()


def _scan_high_confidence_secrets(
    text: str,
) -> tuple[str, ...]:
    hits = tuple(
        rule_id
        for rule_id, pattern in _SECRET_PATTERNS
        if pattern.search(text)
    )
    return hits


def _classify_content_mode(
    entry: TreeEntry,
    read_blob: Callable[[str], bytes],
) -> str:
    if entry.size is None:
        raise DynamicInventoryError(
            "regular blob size missing"
        )

    if (
        entry.size > MAX_FULL_TEXT_BYTES
        or _extension(entry.path)
        not in FULL_TEXT_EXTENSIONS
    ):
        return "METADATA_ONLY"

    raw = read_blob(entry.oid)
    if len(raw) != entry.size:
        raise DynamicInventoryError(
            "full-text raw blob length mismatch"
        )

    if b"\0" in raw:
        return "METADATA_ONLY"

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "METADATA_ONLY"

    hits = _scan_high_confidence_secrets(text)
    if hits:
        raise SecretDetectedError(
            "high-confidence secret detected "
            f"rule_ids={','.join(hits)} "
            f"path_sha256={_path_hash(entry.path)}"
        )

    return "FULL_TEXT"


def build_dynamic_inventory(
    *,
    source: GitInventorySource,
    source_branch: str,
    observed_remote_head: str,
) -> DynamicInventory:
    if source.expected_repository != EXPECTED_REPOSITORY:
        raise DynamicInventoryError(
            "wrong repository identity configured"
        )
    if source_branch != EXPECTED_BRANCH:
        raise DynamicInventoryError(
            "wrong monitored branch"
        )
    if source.source_commit != observed_remote_head:
        raise DynamicInventoryError(
            "source commit differs from observed remote HEAD"
        )

    source.verify_repository()
    source.verify_frozen_source()

    entries = source.tree_entries()
    result: list[DynamicInventoryEntry] = []
    seen_paths: set[str] = set()

    for entry in entries:
        _validate_source_path(entry.path)

        if entry.path in seen_paths:
            raise DynamicInventoryError(
                "duplicate source path"
            )
        seen_paths.add(entry.path)

        if entry.mode == "120000":
            raise DynamicInventoryError(
                "symlink tracked object blocks HEAD"
            )
        if entry.mode == "160000" or entry.object_type == "commit":
            raise DynamicInventoryError(
                "gitlink tracked object blocks HEAD"
            )
        if entry.object_type != "blob":
            raise DynamicInventoryError(
                "non-blob tracked object blocks HEAD"
            )
        if entry.mode not in {"100644", "100755"}:
            raise DynamicInventoryError(
                "unsupported tracked blob mode"
            )
        if entry.size is None or entry.size < 0:
            raise DynamicInventoryError(
                "invalid tracked blob size"
            )

        if _forbidden_surface(entry.path):
            raise DynamicInventoryError(
                "forbidden tracked runtime/derived surface"
            )

        if _sensitive_path(entry.path):
            raise SensitivePathError(
                "sensitive tracked path blocks HEAD "
                f"path_sha256={_path_hash(entry.path)}"
            )

        mode = _classify_content_mode(
            entry,
            source.read_blob,
        )

        result.append(
            DynamicInventoryEntry(
                source_path=entry.path,
                source_blob_sha=entry.oid,
                source_blob_size=entry.size,
                git_mode=entry.mode,
                selection_zone=selection_zone(
                    entry.path
                ),
                content_mode=mode,
            )
        )

    result.sort(
        key=lambda item:
            item.source_path.encode("utf-8")
    )

    return DynamicInventory(
        source_repository=source.expected_repository,
        source_branch=source_branch,
        source_commit=source.source_commit,
        source_tree=source.expected_tree,
        entries=tuple(result),
    )


def build_from_repository(
    *,
    repo_root: Path,
    source_head: str,
    source_tree: str,
    observed_remote_head: str,
) -> DynamicInventory:
    verify_contract(Path(__file__).resolve().parent)

    source = FrozenGitSource(
        repo_root=repo_root,
        expected_repository=EXPECTED_REPOSITORY,
        source_commit=source_head,
        expected_tree=source_tree,
    )

    return build_dynamic_inventory(
        source=source,
        source_branch=EXPECTED_BRANCH,
        observed_remote_head=observed_remote_head,
    )


def inventory_summary(
    inventory: DynamicInventory,
) -> dict[str, Any]:
    zones: dict[str, int] = {}
    for item in inventory.entries:
        zones[item.selection_zone] = (
            zones.get(item.selection_zone, 0) + 1
        )

    return {
        "schema":
            "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_SUMMARY_V0_1",
        "source_repository":
            inventory.source_repository,
        "source_branch":
            inventory.source_branch,
        "source_commit":
            inventory.source_commit,
        "source_tree":
            inventory.source_tree,
        "source_blob_count":
            len(inventory.entries),
        "full_text_count":
            inventory.full_text_count,
        "metadata_only_count":
            inventory.metadata_only_count,
        "inventory_digest_sha256":
            inventory.digest_sha256,
        "selection_zone_counts": {
            key: zones[key]
            for key in sorted(
                zones,
                key=lambda item: item.encode("utf-8"),
            )
        },
        "secret_scanner_version":
            SECRET_SCANNER_VERSION,
        "vault_modified": False,
        "projection_modified": False,
        "canonical_worktree_write_required": False,
    }

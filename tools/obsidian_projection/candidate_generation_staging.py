from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .integrity import (
    IntegrityError,
    projection_tree_digest,
    validate_new_temp_staging_path,
)


class CandidateGenerationError(RuntimeError):
    pass


class CandidateGenerationInvalidError(
    CandidateGenerationError
):
    pass


class CandidateGenerationInfrastructureError(
    CandidateGenerationError
):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
STAGING_CONTRACT_BLOB = (
    "79c6a3380a1dcefc49aa4619259baaa8eeadb535"
)
P5D3C_QUALIFICATION_COMMIT = (
    "437ab790f2a1fa4b490344d28cb7b7a2e8116db3"
)
IMPLEMENTATION_CONTRACT_BLOB = (
    "12f04ad90567c6b0451713a4180f3b10df66de41"
)

PAYLOAD_MANIFEST_SCHEMA = (
    "ATDS_OBSIDIAN_CANDIDATE_PAYLOAD_MANIFEST_V0_1"
)
GENERATION_MANIFEST_SCHEMA = (
    "ATDS_OBSIDIAN_CANDIDATE_GENERATION_MANIFEST_V0_1"
)
SEAL_SCHEMA = (
    "ATDS_OBSIDIAN_CANDIDATE_GENERATION_SEAL_V0_1"
)
DESCRIPTOR_SCHEMA = (
    "ATDS_OBSIDIAN_CANDIDATE_GENERATION_DESCRIPTOR_V0_1"
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

_MACHINE_ROOT = "_atds_generation"
_PAYLOAD_ROOT = "generated"
_PAYLOAD_MANIFEST = (
    "_atds_generation/payload-manifest.json"
)
_GENERATION_MANIFEST = (
    "_atds_generation/generation-manifest.json"
)
_SEAL = "_atds_generation/SEAL.json"

_FORBIDDEN_COMPONENTS = frozenset(
    {
        ".git",
        ".obsidian",
        "views",
    }
)
_FORBIDDEN_NAMES = frozenset(
    {
        "CURRENT",
        "CURRENT.md",
        "CURRENT.json",
        "CURRENT.tmp",
    }
)

_PAYLOAD_MANIFEST_FIELDS = frozenset(
    {
        "schema",
        "file_count",
        "file_map_digest_sha256",
        "files",
    }
)
_PAYLOAD_FILE_FIELDS = frozenset(
    {
        "relative_path",
        "size_bytes",
        "sha256",
    }
)
_GENERATION_MANIFEST_FIELDS = frozenset(
    {
        "schema",
        "generation_id",
        "generation_identity_digest_sha256",
        "repository",
        "branch",
        "candidate_head",
        "candidate_tree",
        "dynamic_inventory_digest_sha256",
        "semantic_bridge_digest_sha256",
        "semantic_record_digest_sha256",
        "projection_contract_version",
        "projection_tree_digest_sha256",
        "generated_file_count",
        "payload_file_map_digest_sha256",
        "payload_manifest_digest_sha256",
        "breaker_status",
        "determinism_status",
        "breaker_manifest_digest_sha256",
        "breaker_result_digest_sha256",
        "determinism_evidence_digest_sha256",
        "staging_contract_blob",
        "package_status",
    }
)
_SEAL_FIELDS = frozenset(
    {
        "schema",
        "generation_id",
        "generation_identity_digest_sha256",
        "payload_manifest_digest_sha256",
        "generation_manifest_digest_sha256",
        "payload_file_map_digest_sha256",
        "projection_tree_digest_sha256",
        "candidate_head",
        "candidate_tree",
        "staging_contract_blob",
        "seal_status",
    }
)


@dataclass(frozen=True)
class VerifiedProjectionCandidate:
    repository: str
    branch: str
    candidate_head: str
    candidate_tree: str
    dynamic_inventory_digest_sha256: str
    semantic_bridge_digest_sha256: str
    semantic_record_digest_sha256: str
    projection_contract_version: str
    projection_tree_digest_sha256: str
    generated_file_count: int
    breaker_status: str
    determinism_status: str
    breaker_manifest_digest_sha256: str
    breaker_result_digest_sha256: str
    determinism_evidence_digest_sha256: str


@dataclass(frozen=True)
class PayloadFile:
    relative_path: str
    size_bytes: int
    sha256: str

    def as_manifest_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
        }

    def as_digest_row(self) -> list[Any]:
        return [
            self.relative_path,
            self.sha256,
            self.size_bytes,
        ]


def _canonical_json_bytes(
    value: Any,
    *,
    terminal_lf: bool,
) -> bytes:
    try:
        raw = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CandidateGenerationInvalidError(
            "value is not canonical JSON"
        ) from exc

    if terminal_lf:
        raw += b"\n"
    return raw


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_head(value: Any, field: str) -> str:
    if (
        not isinstance(value, str)
        or _HEAD_RE.fullmatch(value) is None
    ):
        raise CandidateGenerationInvalidError(
            f"{field} must be lowercase 40-hex SHA-1"
        )
    return value


def _require_sha256(value: Any, field: str) -> str:
    if (
        not isinstance(value, str)
        or _SHA256_RE.fullmatch(value) is None
    ):
        raise CandidateGenerationInvalidError(
            f"{field} must be lowercase 64-hex SHA-256"
        )
    return value


def _validate_candidate(
    candidate: VerifiedProjectionCandidate,
) -> None:
    if not isinstance(
        candidate,
        VerifiedProjectionCandidate,
    ):
        raise CandidateGenerationInvalidError(
            "candidate type mismatch"
        )

    if candidate.repository != EXPECTED_REPOSITORY:
        raise CandidateGenerationInvalidError(
            "repository mismatch"
        )
    if candidate.branch != EXPECTED_BRANCH:
        raise CandidateGenerationInvalidError(
            "branch mismatch"
        )

    _require_head(
        candidate.candidate_head,
        "candidate_head",
    )
    _require_head(
        candidate.candidate_tree,
        "candidate_tree",
    )

    for field in (
        "dynamic_inventory_digest_sha256",
        "semantic_bridge_digest_sha256",
        "semantic_record_digest_sha256",
        "projection_tree_digest_sha256",
        "breaker_manifest_digest_sha256",
        "breaker_result_digest_sha256",
        "determinism_evidence_digest_sha256",
    ):
        _require_sha256(
            getattr(candidate, field),
            field,
        )

    if (
        not isinstance(
            candidate.projection_contract_version,
            str,
        )
        or not candidate.projection_contract_version
    ):
        raise CandidateGenerationInvalidError(
            "projection_contract_version required"
        )

    if (
        isinstance(candidate.generated_file_count, bool)
        or not isinstance(
            candidate.generated_file_count,
            int,
        )
        or candidate.generated_file_count < 0
    ):
        raise CandidateGenerationInvalidError(
            "generated_file_count must be nonnegative int"
        )

    if candidate.breaker_status != "PASS":
        raise CandidateGenerationInvalidError(
            "breaker_status must be PASS"
        )
    if candidate.determinism_status != "PASS":
        raise CandidateGenerationInvalidError(
            "determinism_status must be PASS"
        )


def _is_reparse_or_symlink(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot lstat path: {path}: {exc}"
        ) from exc

    if stat.S_ISLNK(info.st_mode):
        return True

    attributes = getattr(
        info,
        "st_file_attributes",
        None,
    )
    reparse_flag = getattr(
        stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        None,
    )
    return bool(
        attributes is not None
        and reparse_flag is not None
        and attributes & reparse_flag
    )


def _assert_regular_single_link(path: Path) -> None:
    if _is_reparse_or_symlink(path):
        raise CandidateGenerationInvalidError(
            f"reparse/symlink file forbidden: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot stat file: {path}: {exc}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise CandidateGenerationInvalidError(
            f"non-regular file forbidden: {path}"
        )

    link_count = getattr(
        info,
        "st_nlink",
        None,
    )
    if link_count is None:
        raise CandidateGenerationInfrastructureError(
            f"hard-link count unavailable: {path}"
        )
    if int(link_count) != 1:
        raise CandidateGenerationInvalidError(
            f"hard-link alias forbidden: {path}"
        )


def _assert_directory_not_alias(path: Path) -> None:
    if _is_reparse_or_symlink(path):
        raise CandidateGenerationInvalidError(
            f"reparse/symlink directory forbidden: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot stat directory: {path}: {exc}"
        ) from exc

    if not stat.S_ISDIR(info.st_mode):
        raise CandidateGenerationInvalidError(
            f"expected directory: {path}"
        )


def _assert_directory_chain_no_alias(
    path: Path,
    root: Path,
) -> None:
    current = _resolved(path)
    boundary = _resolved(root)

    while True:
        if (
            current != boundary
            and boundary not in current.parents
        ):
            raise CandidateGenerationInvalidError(
                "directory chain escaped package root"
            )

        _assert_directory_not_alias(current)

        if current == boundary:
            return
        current = current.parent


def _assert_tree_has_no_aliases(root: Path) -> None:
    _assert_directory_not_alias(root)

    try:
        with os.scandir(root) as iterator:
            entries = list(iterator)
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot enumerate directory: {root}: {exc}"
        ) from exc

    for entry in entries:
        path = Path(entry.path)
        if entry.is_symlink():
            raise CandidateGenerationInvalidError(
                f"symlink forbidden: {path}"
            )

        if entry.is_dir(follow_symlinks=False):
            _assert_tree_has_no_aliases(path)
        elif entry.is_file(follow_symlinks=False):
            _assert_regular_single_link(path)
        else:
            raise CandidateGenerationInvalidError(
                f"unsupported filesystem object: {path}"
            )


def _safe_payload_relative(
    value: str,
) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise CandidateGenerationInvalidError(
            "empty payload relative path"
        )
    if value.startswith(("/", "\\")):
        raise CandidateGenerationInvalidError(
            "absolute payload path forbidden"
        )
    if "\\" in value:
        raise CandidateGenerationInvalidError(
            "backslash payload path forbidden"
        )

    posix = PurePosixPath(value)
    if posix.is_absolute() or ".." in posix.parts:
        raise CandidateGenerationInvalidError(
            "payload traversal forbidden"
        )
    if not posix.parts or posix.parts[0] != _PAYLOAD_ROOT:
        raise CandidateGenerationInvalidError(
            "payload path must begin generated/"
        )
    if any(
        part in _FORBIDDEN_COMPONENTS
        for part in posix.parts
    ):
        raise CandidateGenerationInvalidError(
            "forbidden payload component"
        )
    if posix.name in _FORBIDDEN_NAMES:
        raise CandidateGenerationInvalidError(
            "CURRENT-like payload path forbidden"
        )
    return posix


def _resolved(path: Path) -> Path:
    try:
        return path.resolve(strict=False)
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot resolve path: {path}: {exc}"
        ) from exc


def _assert_outside_forbidden_roots(
    candidate: Path,
    forbidden_roots: Iterable[Path],
) -> None:
    resolved_candidate = _resolved(candidate)
    for root in forbidden_roots:
        resolved_root = _resolved(Path(root))
        if (
            resolved_candidate == resolved_root
            or resolved_root in resolved_candidate.parents
            or resolved_candidate in resolved_root.parents
        ):
            raise CandidateGenerationInvalidError(
                "staging root intersects forbidden root"
            )


def _validate_new_package_root(
    package_root: Path,
    forbidden_roots: Iterable[Path],
) -> Path:
    try:
        candidate = validate_new_temp_staging_path(
            package_root
        )
    except IntegrityError as exc:
        raise CandidateGenerationInvalidError(
            str(exc)
        ) from exc

    _assert_outside_forbidden_roots(
        candidate,
        forbidden_roots,
    )
    return candidate


def _validate_existing_package_root(
    package_root: Path,
    forbidden_roots: Iterable[Path],
) -> Path:
    root = _resolved(package_root)
    temp_root = _resolved(
        Path(tempfile.gettempdir())
    )

    if (
        root == temp_root
        or temp_root not in root.parents
    ):
        raise CandidateGenerationInvalidError(
            "package root must be below OS temp root"
        )
    _assert_outside_forbidden_roots(
        root,
        forbidden_roots,
    )
    _assert_tree_has_no_aliases(root)

    if (root / ".git").exists():
        raise CandidateGenerationInvalidError(
            "package root may not be Git repository"
        )
    return root


def _read_bytes(path: Path) -> bytes:
    _assert_regular_single_link(path)
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot read file: {path}: {exc}"
        ) from exc


def _write_exclusive(
    package_root: Path,
    relative_path: str,
    data: bytes,
) -> Path:
    posix = PurePosixPath(relative_path)
    if (
        not relative_path
        or relative_path.startswith(("/", "\\"))
        or "\\" in relative_path
        or ".." in posix.parts
        or posix.is_absolute()
    ):
        raise CandidateGenerationInvalidError(
            "unsafe package write path"
        )

    destination = package_root.joinpath(
        *posix.parts
    )
    resolved_destination = _resolved(destination)
    root = _resolved(package_root)
    if (
        resolved_destination == root
        or root not in resolved_destination.parents
    ):
        raise CandidateGenerationInvalidError(
            "package write escapes root"
        )

    _assert_directory_chain_no_alias(
        destination.parent,
        package_root,
    )
    try:
        with destination.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise CandidateGenerationInvalidError(
            f"pre-existing package target: {relative_path}"
        ) from exc
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot write package file: {relative_path}: {exc}"
        ) from exc

    _assert_regular_single_link(destination)
    return destination


def _payload_files_from_projection(
    projection_root: Path,
) -> tuple[PayloadFile, ...]:
    root = _resolved(projection_root)
    generated = root / _PAYLOAD_ROOT

    if not generated.exists():
        raise CandidateGenerationInvalidError(
            "verified projection generated/ missing"
        )
    _assert_tree_has_no_aliases(generated)

    items: list[PayloadFile] = []
    seen: set[str] = set()

    try:
        paths = [
            path
            for path in generated.rglob("*")
            if path.is_file()
        ]
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot enumerate verified projection: {exc}"
        ) from exc

    for path in paths:
        _assert_regular_single_link(path)
        relative = path.relative_to(root).as_posix()
        _safe_payload_relative(relative)

        if relative in seen:
            raise CandidateGenerationInvalidError(
                "duplicate payload path"
            )
        seen.add(relative)

        data = _read_bytes(path)
        items.append(
            PayloadFile(
                relative_path=relative,
                size_bytes=len(data),
                sha256=_sha256_bytes(data),
            )
        )

    items.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(items)


def _payload_file_map_digest(
    files: tuple[PayloadFile, ...],
) -> str:
    rows = [
        item.as_digest_row()
        for item in files
    ]
    return _sha256_bytes(
        _canonical_json_bytes(
            rows,
            terminal_lf=False,
        )
    )


def _payload_manifest(
    files: tuple[PayloadFile, ...],
) -> tuple[dict[str, Any], bytes, str]:
    payload = {
        "schema": PAYLOAD_MANIFEST_SCHEMA,
        "file_count": len(files),
        "file_map_digest_sha256":
            _payload_file_map_digest(files),
        "files": [
            item.as_manifest_dict()
            for item in files
        ],
    }
    raw = _canonical_json_bytes(
        payload,
        terminal_lf=True,
    )
    return payload, raw, _sha256_bytes(raw)


def _identity_basis(
    candidate: VerifiedProjectionCandidate,
    *,
    payload_file_map_digest_sha256: str,
    payload_manifest_digest_sha256: str,
) -> dict[str, Any]:
    return {
        "repository": candidate.repository,
        "branch": candidate.branch,
        "candidate_head": candidate.candidate_head,
        "candidate_tree": candidate.candidate_tree,
        "dynamic_inventory_digest_sha256":
            candidate.dynamic_inventory_digest_sha256,
        "semantic_bridge_digest_sha256":
            candidate.semantic_bridge_digest_sha256,
        "semantic_record_digest_sha256":
            candidate.semantic_record_digest_sha256,
        "projection_contract_version":
            candidate.projection_contract_version,
        "projection_tree_digest_sha256":
            candidate.projection_tree_digest_sha256,
        "generated_file_count":
            candidate.generated_file_count,
        "payload_file_map_digest_sha256":
            payload_file_map_digest_sha256,
        "payload_manifest_digest_sha256":
            payload_manifest_digest_sha256,
        "breaker_status": candidate.breaker_status,
        "determinism_status":
            candidate.determinism_status,
        "breaker_manifest_digest_sha256":
            candidate.breaker_manifest_digest_sha256,
        "breaker_result_digest_sha256":
            candidate.breaker_result_digest_sha256,
        "determinism_evidence_digest_sha256":
            candidate.determinism_evidence_digest_sha256,
        "staging_contract_blob":
            STAGING_CONTRACT_BLOB,
    }


def _generation_identity(
    basis: dict[str, Any],
) -> tuple[str, str]:
    digest = _sha256_bytes(
        _canonical_json_bytes(
            basis,
            terminal_lf=False,
        )
    )
    return digest, f"gen-{digest}"


def _generation_manifest(
    candidate: VerifiedProjectionCandidate,
    *,
    generation_id: str,
    generation_identity_digest_sha256: str,
    payload_file_map_digest_sha256: str,
    payload_manifest_digest_sha256: str,
) -> tuple[dict[str, Any], bytes, str]:
    payload = {
        "schema": GENERATION_MANIFEST_SCHEMA,
        "generation_id": generation_id,
        "generation_identity_digest_sha256":
            generation_identity_digest_sha256,
        "repository": candidate.repository,
        "branch": candidate.branch,
        "candidate_head": candidate.candidate_head,
        "candidate_tree": candidate.candidate_tree,
        "dynamic_inventory_digest_sha256":
            candidate.dynamic_inventory_digest_sha256,
        "semantic_bridge_digest_sha256":
            candidate.semantic_bridge_digest_sha256,
        "semantic_record_digest_sha256":
            candidate.semantic_record_digest_sha256,
        "projection_contract_version":
            candidate.projection_contract_version,
        "projection_tree_digest_sha256":
            candidate.projection_tree_digest_sha256,
        "generated_file_count":
            candidate.generated_file_count,
        "payload_file_map_digest_sha256":
            payload_file_map_digest_sha256,
        "payload_manifest_digest_sha256":
            payload_manifest_digest_sha256,
        "breaker_status": candidate.breaker_status,
        "determinism_status":
            candidate.determinism_status,
        "breaker_manifest_digest_sha256":
            candidate.breaker_manifest_digest_sha256,
        "breaker_result_digest_sha256":
            candidate.breaker_result_digest_sha256,
        "determinism_evidence_digest_sha256":
            candidate.determinism_evidence_digest_sha256,
        "staging_contract_blob":
            STAGING_CONTRACT_BLOB,
        "package_status":
            "COMPLETE_PENDING_SEAL",
    }
    raw = _canonical_json_bytes(
        payload,
        terminal_lf=True,
    )
    return payload, raw, _sha256_bytes(raw)


def _seal_payload(
    *,
    generation_id: str,
    generation_identity_digest_sha256: str,
    payload_manifest_digest_sha256: str,
    generation_manifest_digest_sha256: str,
    payload_file_map_digest_sha256: str,
    candidate: VerifiedProjectionCandidate,
) -> tuple[dict[str, Any], bytes, str]:
    payload = {
        "schema": SEAL_SCHEMA,
        "generation_id": generation_id,
        "generation_identity_digest_sha256":
            generation_identity_digest_sha256,
        "payload_manifest_digest_sha256":
            payload_manifest_digest_sha256,
        "generation_manifest_digest_sha256":
            generation_manifest_digest_sha256,
        "payload_file_map_digest_sha256":
            payload_file_map_digest_sha256,
        "projection_tree_digest_sha256":
            candidate.projection_tree_digest_sha256,
        "candidate_head": candidate.candidate_head,
        "candidate_tree": candidate.candidate_tree,
        "staging_contract_blob":
            STAGING_CONTRACT_BLOB,
        "seal_status": "SEALED_UNPROMOTED",
    }
    raw = _canonical_json_bytes(
        payload,
        terminal_lf=True,
    )
    return payload, raw, _sha256_bytes(raw)


def _parse_canonical_json_file(
    path: Path,
) -> tuple[dict[str, Any], bytes]:
    raw = _read_bytes(path)
    if not raw.endswith(b"\n") or b"\r" in raw:
        raise CandidateGenerationInvalidError(
            f"non-canonical JSON framing: {path.name}"
        )
    try:
        value = json.loads(raw.decode("utf-8"))
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise CandidateGenerationInvalidError(
            f"cannot parse manifest: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise CandidateGenerationInvalidError(
            f"manifest must be object: {path.name}"
        )
    if raw != _canonical_json_bytes(
        value,
        terminal_lf=True,
    ):
        raise CandidateGenerationInvalidError(
            f"manifest bytes not canonical: {path.name}"
        )
    return value, raw


def _require_exact_fields(
    value: dict[str, Any],
    fields: frozenset[str],
    label: str,
) -> None:
    if frozenset(value.keys()) != fields:
        raise CandidateGenerationInvalidError(
            f"{label} field set mismatch"
        )


def _enumerate_actual_files(
    package_root: Path,
) -> tuple[str, ...]:
    _assert_tree_has_no_aliases(package_root)
    files: list[str] = []
    for path in package_root.rglob("*"):
        if not path.is_file():
            continue
        _assert_regular_single_link(path)
        files.append(
            path.relative_to(
                package_root
            ).as_posix()
        )
    files.sort(key=lambda item: item.encode("utf-8"))
    return tuple(files)


def _verify_payload_manifest(
    package_root: Path,
    payload: dict[str, Any],
) -> tuple[tuple[PayloadFile, ...], str]:
    _require_exact_fields(
        payload,
        _PAYLOAD_MANIFEST_FIELDS,
        "payload manifest",
    )
    if payload["schema"] != PAYLOAD_MANIFEST_SCHEMA:
        raise CandidateGenerationInvalidError(
            "payload manifest schema mismatch"
        )

    raw_files = payload["files"]
    if not isinstance(raw_files, list):
        raise CandidateGenerationInvalidError(
            "payload manifest files must be list"
        )
    if (
        isinstance(payload["file_count"], bool)
        or not isinstance(payload["file_count"], int)
        or payload["file_count"] < 0
    ):
        raise CandidateGenerationInvalidError(
            "invalid payload file_count"
        )
    if payload["file_count"] != len(raw_files):
        raise CandidateGenerationInvalidError(
            "payload manifest file_count mismatch"
        )

    files: list[PayloadFile] = []
    seen: set[str] = set()
    previous_key: bytes | None = None

    for item in raw_files:
        if not isinstance(item, dict):
            raise CandidateGenerationInvalidError(
                "payload file entry must be object"
            )
        _require_exact_fields(
            item,
            _PAYLOAD_FILE_FIELDS,
            "payload file entry",
        )

        relative = item["relative_path"]
        _safe_payload_relative(relative)
        if relative in seen:
            raise CandidateGenerationInvalidError(
                "duplicate payload manifest path"
            )
        seen.add(relative)

        key = relative.encode("utf-8")
        if previous_key is not None and key <= previous_key:
            raise CandidateGenerationInvalidError(
                "payload manifest not bytewise sorted"
            )
        previous_key = key

        size = item["size_bytes"]
        if (
            isinstance(size, bool)
            or not isinstance(size, int)
            or size < 0
        ):
            raise CandidateGenerationInvalidError(
                "invalid payload file size"
            )
        digest = _require_sha256(
            item["sha256"],
            "payload file sha256",
        )

        path = package_root.joinpath(
            *PurePosixPath(relative).parts
        )
        if not path.exists():
            raise CandidateGenerationInvalidError(
                f"payload file missing: {relative}"
            )
        data = _read_bytes(path)
        if len(data) != size:
            raise CandidateGenerationInvalidError(
                f"payload size mismatch: {relative}"
            )
        if _sha256_bytes(data) != digest:
            raise CandidateGenerationInvalidError(
                f"payload SHA256 mismatch: {relative}"
            )

        files.append(
            PayloadFile(
                relative_path=relative,
                size_bytes=size,
                sha256=digest,
            )
        )

    result = tuple(files)
    expected_map = _payload_file_map_digest(
        result
    )
    if (
        payload["file_map_digest_sha256"]
        != expected_map
    ):
        raise CandidateGenerationInvalidError(
            "payload file-map digest mismatch"
        )
    return result, expected_map


def _expected_file_set(
    files: tuple[PayloadFile, ...],
) -> frozenset[str]:
    return frozenset(
        {
            *(
                item.relative_path
                for item in files
            ),
            _PAYLOAD_MANIFEST,
            _GENERATION_MANIFEST,
            _SEAL,
        }
    )


def _candidate_from_generation_manifest(
    manifest: dict[str, Any],
) -> VerifiedProjectionCandidate:
    return VerifiedProjectionCandidate(
        repository=manifest["repository"],
        branch=manifest["branch"],
        candidate_head=manifest["candidate_head"],
        candidate_tree=manifest["candidate_tree"],
        dynamic_inventory_digest_sha256=(
            manifest[
                "dynamic_inventory_digest_sha256"
            ]
        ),
        semantic_bridge_digest_sha256=(
            manifest[
                "semantic_bridge_digest_sha256"
            ]
        ),
        semantic_record_digest_sha256=(
            manifest[
                "semantic_record_digest_sha256"
            ]
        ),
        projection_contract_version=(
            manifest["projection_contract_version"]
        ),
        projection_tree_digest_sha256=(
            manifest[
                "projection_tree_digest_sha256"
            ]
        ),
        generated_file_count=(
            manifest["generated_file_count"]
        ),
        breaker_status=manifest["breaker_status"],
        determinism_status=(
            manifest["determinism_status"]
        ),
        breaker_manifest_digest_sha256=(
            manifest[
                "breaker_manifest_digest_sha256"
            ]
        ),
        breaker_result_digest_sha256=(
            manifest[
                "breaker_result_digest_sha256"
            ]
        ),
        determinism_evidence_digest_sha256=(
            manifest[
                "determinism_evidence_digest_sha256"
            ]
        ),
    )


def verify_candidate_generation(
    package_root: Path,
    *,
    expected_candidate: (
        VerifiedProjectionCandidate | None
    ) = None,
    forbidden_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    root = _validate_existing_package_root(
        package_root,
        forbidden_roots,
    )

    top_level = {
        path.name
        for path in root.iterdir()
    }
    if top_level != {
        _PAYLOAD_ROOT,
        _MACHINE_ROOT,
    }:
        raise CandidateGenerationInvalidError(
            "top-level package layout mismatch"
        )

    payload_manifest, payload_raw = (
        _parse_canonical_json_file(
            root / _PAYLOAD_MANIFEST
        )
    )
    generation_manifest, generation_raw = (
        _parse_canonical_json_file(
            root / _GENERATION_MANIFEST
        )
    )
    seal, seal_raw = _parse_canonical_json_file(
        root / _SEAL
    )

    files, file_map_digest = (
        _verify_payload_manifest(
            root,
            payload_manifest,
        )
    )

    actual_files = frozenset(
        _enumerate_actual_files(root)
    )
    if actual_files != _expected_file_set(files):
        raise CandidateGenerationInvalidError(
            "package exact file set mismatch"
        )

    _require_exact_fields(
        generation_manifest,
        _GENERATION_MANIFEST_FIELDS,
        "generation manifest",
    )
    if generation_manifest["schema"] != (
        GENERATION_MANIFEST_SCHEMA
    ):
        raise CandidateGenerationInvalidError(
            "generation manifest schema mismatch"
        )
    if generation_manifest["package_status"] != (
        "COMPLETE_PENDING_SEAL"
    ):
        raise CandidateGenerationInvalidError(
            "generation package status mismatch"
        )
    if generation_manifest["staging_contract_blob"] != (
        STAGING_CONTRACT_BLOB
    ):
        raise CandidateGenerationInvalidError(
            "staging contract blob mismatch"
        )

    candidate = _candidate_from_generation_manifest(
        generation_manifest
    )
    _validate_candidate(candidate)

    if expected_candidate is not None:
        _validate_candidate(expected_candidate)
        if candidate != expected_candidate:
            raise CandidateGenerationInvalidError(
                "generation candidate identity mismatch"
            )

    if len(files) != candidate.generated_file_count:
        raise CandidateGenerationInvalidError(
            "generated file count mismatch"
        )

    if (
        payload_manifest["file_count"]
        != candidate.generated_file_count
    ):
        raise CandidateGenerationInvalidError(
            "payload count/candidate mismatch"
        )

    payload_manifest_digest = _sha256_bytes(
        payload_raw
    )
    if generation_manifest[
        "payload_manifest_digest_sha256"
    ] != payload_manifest_digest:
        raise CandidateGenerationInvalidError(
            "payload manifest digest binding mismatch"
        )
    if generation_manifest[
        "payload_file_map_digest_sha256"
    ] != file_map_digest:
        raise CandidateGenerationInvalidError(
            "payload map digest binding mismatch"
        )

    basis = _identity_basis(
        candidate,
        payload_file_map_digest_sha256=(
            file_map_digest
        ),
        payload_manifest_digest_sha256=(
            payload_manifest_digest
        ),
    )
    identity_digest, generation_id = (
        _generation_identity(basis)
    )

    if generation_manifest[
        "generation_identity_digest_sha256"
    ] != identity_digest:
        raise CandidateGenerationInvalidError(
            "generation identity digest mismatch"
        )
    if generation_manifest["generation_id"] != generation_id:
        raise CandidateGenerationInvalidError(
            "generation ID mismatch"
        )

    generation_manifest_digest = _sha256_bytes(
        generation_raw
    )

    _require_exact_fields(
        seal,
        _SEAL_FIELDS,
        "seal",
    )
    if seal["schema"] != SEAL_SCHEMA:
        raise CandidateGenerationInvalidError(
            "seal schema mismatch"
        )
    if seal["seal_status"] != "SEALED_UNPROMOTED":
        raise CandidateGenerationInvalidError(
            "seal status mismatch"
        )
    if seal["staging_contract_blob"] != (
        STAGING_CONTRACT_BLOB
    ):
        raise CandidateGenerationInvalidError(
            "seal contract binding mismatch"
        )

    expected_seal, expected_seal_raw, _ = (
        _seal_payload(
            generation_id=generation_id,
            generation_identity_digest_sha256=(
                identity_digest
            ),
            payload_manifest_digest_sha256=(
                payload_manifest_digest
            ),
            generation_manifest_digest_sha256=(
                generation_manifest_digest
            ),
            payload_file_map_digest_sha256=(
                file_map_digest
            ),
            candidate=candidate,
        )
    )
    if seal != expected_seal:
        raise CandidateGenerationInvalidError(
            "seal binding mismatch"
        )
    if seal_raw != expected_seal_raw:
        raise CandidateGenerationInvalidError(
            "seal byte binding mismatch"
        )

    candidate_generation_digest = _sha256_bytes(
        seal_raw
    )

    return {
        "schema": DESCRIPTOR_SCHEMA,
        "generation_id": generation_id,
        "candidate_generation_digest_sha256":
            candidate_generation_digest,
        "candidate_head": candidate.candidate_head,
        "candidate_tree": candidate.candidate_tree,
        "projection_tree_digest_sha256":
            candidate.projection_tree_digest_sha256,
        "payload_file_count": len(files),
        "payload_file_map_digest_sha256":
            file_map_digest,
        "semantic_record_digest_sha256":
            candidate.semantic_record_digest_sha256,
        "semantic_bridge_digest_sha256":
            candidate.semantic_bridge_digest_sha256,
        "breaker_manifest_digest_sha256":
            candidate.breaker_manifest_digest_sha256,
        "breaker_result_digest_sha256":
            candidate.breaker_result_digest_sha256,
        "verification_status":
            "PASS_SEALED_UNPROMOTED",
        "promotion_authorized": False,
    }


def stage_candidate_generation(
    candidate: VerifiedProjectionCandidate,
    *,
    verified_projection_root: Path,
    package_root: Path,
    forbidden_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    _validate_candidate(candidate)

    projection_root = _resolved(
        verified_projection_root
    )
    if not projection_root.exists():
        raise CandidateGenerationInvalidError(
            "verified projection root missing"
        )

    source_files = _payload_files_from_projection(
        projection_root
    )

    if len(source_files) != candidate.generated_file_count:
        raise CandidateGenerationInvalidError(
            "verified projection file count mismatch"
        )

    try:
        actual_projection_digest = (
            projection_tree_digest(
                projection_root
            )
        )
    except IntegrityError as exc:
        raise CandidateGenerationInvalidError(
            f"projection tree verification failed: {exc}"
        ) from exc

    if actual_projection_digest != (
        candidate.projection_tree_digest_sha256
    ):
        raise CandidateGenerationInvalidError(
            "projection tree digest mismatch"
        )

    root = _validate_new_package_root(
        package_root,
        (
            *tuple(forbidden_roots),
            projection_root,
        ),
    )

    try:
        root.mkdir()
        (root / _PAYLOAD_ROOT).mkdir()
        (root / _MACHINE_ROOT).mkdir()
    except OSError as exc:
        raise CandidateGenerationInfrastructureError(
            f"cannot create package root: {exc}"
        ) from exc

    staged_files: list[PayloadFile] = []

    for item in source_files:
        source = projection_root.joinpath(
            *PurePosixPath(
                item.relative_path
            ).parts
        )
        data = _read_bytes(source)

        destination = root.joinpath(
            *PurePosixPath(
                item.relative_path
            ).parts
        )
        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as exc:
            raise CandidateGenerationInfrastructureError(
                f"cannot create payload directory: {exc}"
            ) from exc

        _write_exclusive(
            root,
            item.relative_path,
            data,
        )

        copied = PayloadFile(
            relative_path=item.relative_path,
            size_bytes=len(data),
            sha256=_sha256_bytes(data),
        )
        if copied != item:
            raise CandidateGenerationInvalidError(
                "payload copy identity mismatch"
            )
        staged_files.append(copied)

    files = tuple(staged_files)
    payload_manifest, payload_raw, payload_digest = (
        _payload_manifest(files)
    )
    _write_exclusive(
        root,
        _PAYLOAD_MANIFEST,
        payload_raw,
    )

    file_map_digest = payload_manifest[
        "file_map_digest_sha256"
    ]
    basis = _identity_basis(
        candidate,
        payload_file_map_digest_sha256=(
            file_map_digest
        ),
        payload_manifest_digest_sha256=(
            payload_digest
        ),
    )
    identity_digest, generation_id = (
        _generation_identity(basis)
    )

    generation_manifest, generation_raw, generation_digest = (
        _generation_manifest(
            candidate,
            generation_id=generation_id,
            generation_identity_digest_sha256=(
                identity_digest
            ),
            payload_file_map_digest_sha256=(
                file_map_digest
            ),
            payload_manifest_digest_sha256=(
                payload_digest
            ),
        )
    )
    _write_exclusive(
        root,
        _GENERATION_MANIFEST,
        generation_raw,
    )

    actual_preseal = frozenset(
        _enumerate_actual_files(root)
    )
    expected_preseal = frozenset(
        {
            *(
                item.relative_path
                for item in files
            ),
            _PAYLOAD_MANIFEST,
            _GENERATION_MANIFEST,
        }
    )
    if actual_preseal != expected_preseal:
        raise CandidateGenerationInvalidError(
            "pre-seal exact file set mismatch"
        )

    verified_files, verified_map = (
        _verify_payload_manifest(
            root,
            payload_manifest,
        )
    )
    if verified_files != files:
        raise CandidateGenerationInvalidError(
            "pre-seal payload verification mismatch"
        )
    if verified_map != file_map_digest:
        raise CandidateGenerationInvalidError(
            "pre-seal file-map verification mismatch"
        )

    if _sha256_bytes(payload_raw) != payload_digest:
        raise CandidateGenerationInvalidError(
            "pre-seal payload manifest digest mismatch"
        )
    if (
        _sha256_bytes(generation_raw)
        != generation_digest
    ):
        raise CandidateGenerationInvalidError(
            "pre-seal generation manifest digest mismatch"
        )

    _, seal_raw, _ = _seal_payload(
        generation_id=generation_id,
        generation_identity_digest_sha256=(
            identity_digest
        ),
        payload_manifest_digest_sha256=(
            payload_digest
        ),
        generation_manifest_digest_sha256=(
            generation_digest
        ),
        payload_file_map_digest_sha256=(
            file_map_digest
        ),
        candidate=candidate,
    )

    _write_exclusive(
        root,
        _SEAL,
        seal_raw,
    )

    return verify_candidate_generation(
        root,
        expected_candidate=candidate,
        forbidden_roots=forbidden_roots,
    )

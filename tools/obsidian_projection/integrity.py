from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .rendering import RenderedFile


class IntegrityError(RuntimeError):
    """Raised when projection filesystem or integrity checks fail closed."""


@dataclass(frozen=True)
class FileDigest:
    relative_path: str
    size_bytes: int
    sha256: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=False,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_json_file_bytes(value: object) -> bytes:
    raw = canonical_json_bytes(value) + b"\n"
    if b"\r" in raw:
        raise IntegrityError(
            "canonical JSON unexpectedly contains CR"
        )
    return raw


def _relative_posix(
    path: Path,
    root: Path,
) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise IntegrityError(
            f"path escapes staging root: {path}"
        ) from exc
    return relative.as_posix()


def _is_reparse_or_link(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as exc:
        raise IntegrityError(
            f"cannot lstat path: {path}: {exc}"
        ) from exc

    if stat.S_ISLNK(info.st_mode):
        return True

    file_attributes = getattr(
        info,
        "st_file_attributes",
        None,
    )
    reparse_flag = getattr(
        stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        None,
    )
    if (
        file_attributes is not None
        and reparse_flag is not None
        and file_attributes & reparse_flag
    ):
        return True

    isjunction = getattr(
        os.path,
        "isjunction",
        None,
    )
    if isjunction is not None:
        try:
            if isjunction(path):
                return True
        except OSError as exc:
            raise IntegrityError(
                f"junction check failed: {path}: {exc}"
            ) from exc

    return False


def _assert_no_alias_chain(
    path: Path,
    stop_at: Path,
) -> None:
    current = path

    while True:
        if current.exists():
            if _is_reparse_or_link(current):
                raise IntegrityError(
                    f"reparse/symlink/junction path forbidden: "
                    f"{current}"
                )

        if current == stop_at:
            return

        if stop_at not in current.parents:
            raise IntegrityError(
                f"alias-chain path escaped stop root: {current}"
            )

        current = current.parent


def validate_new_temp_staging_path(
    stage_root: Path,
) -> Path:
    if stage_root.exists():
        raise IntegrityError(
            f"staging root already exists: {stage_root}"
        )

    temp_root = Path(
        tempfile.gettempdir()
    ).resolve()
    candidate = stage_root.resolve(
        strict=False
    )

    if (
        candidate == temp_root
        or temp_root not in candidate.parents
    ):
        raise IntegrityError(
            "staging root must be below OS temp root"
        )

    parent = candidate.parent
    if not parent.exists():
        raise IntegrityError(
            "staging parent must already exist"
        )

    _assert_no_alias_chain(
        parent,
        temp_root,
    )

    return candidate


def _assert_regular_single_link(
    path: Path,
) -> None:
    if _is_reparse_or_link(path):
        raise IntegrityError(
            f"generated path is reparse/link: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise IntegrityError(
            f"cannot stat generated file: {path}: {exc}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise IntegrityError(
            f"generated path is not regular file: {path}"
        )

    link_count = getattr(
        info,
        "st_nlink",
        None,
    )
    if link_count is None:
        raise IntegrityError(
            f"hard-link count unavailable: {path}"
        )

    if int(link_count) != 1:
        raise IntegrityError(
            f"unexpected hard-link count "
            f"{link_count}: {path}"
        )


def create_stage_directories(
    stage_root: Path,
) -> None:
    candidate = validate_new_temp_staging_path(
        stage_root
    )
    candidate.mkdir()

    for relative in (
        "generated",
        "generated/artifacts",
        "generated/relations",
        "generated/manifests",
    ):
        path = candidate / relative
        path.mkdir()

    _assert_no_alias_chain(
        candidate / "generated" / "manifests",
        candidate,
    )


def exclusive_write(
    stage_root: Path,
    rendered: RenderedFile,
) -> Path:
    if rendered.content.startswith(b"\xef\xbb\xbf"):
        raise IntegrityError(
            "UTF-8 BOM forbidden in deterministic output"
        )
    if b"\r" in rendered.content:
        raise IntegrityError(
            "CR/CRLF forbidden in deterministic output"
        )
    if not rendered.content.endswith(b"\n"):
        raise IntegrityError(
            "deterministic output must end with LF"
        )

    candidate = stage_root.resolve()
    destination = (
        candidate
        / Path(rendered.relative_path)
    )

    relative = _relative_posix(
        destination,
        candidate,
    )

    if not (
        relative.startswith(
            "generated/artifacts/"
        )
        or relative.startswith(
            "generated/relations/"
        )
        or relative.startswith(
            "generated/manifests/"
        )
    ):
        raise IntegrityError(
            f"write outside allowed generated roots: "
            f"{relative}"
        )

    if (
        relative.startswith("views/")
        or relative.startswith(".obsidian/")
    ):
        raise IntegrityError(
            f"forbidden builder write root: {relative}"
        )

    _assert_no_alias_chain(
        destination.parent,
        candidate,
    )

    try:
        with destination.open("xb") as handle:
            handle.write(rendered.content)
    except FileExistsError as exc:
        raise IntegrityError(
            f"pre-existing output target: {relative}"
        ) from exc

    _assert_regular_single_link(
        destination
    )
    return destination


def file_digest(
    stage_root: Path,
    path: Path,
) -> FileDigest:
    _assert_regular_single_link(path)
    data = path.read_bytes()
    return FileDigest(
        relative_path=_relative_posix(
            path.resolve(),
            stage_root.resolve(),
        ),
        size_bytes=len(data),
        sha256=sha256_bytes(data),
    )


def digest_entries(
    entries: Sequence[FileDigest],
) -> str:
    payload = [
        [
            item.relative_path,
            item.sha256,
            item.size_bytes,
        ]
        for item in sorted(
            entries,
            key=lambda item: item.relative_path.encode(
                "utf-8"
            ),
        )
    ]
    return sha256_bytes(
        canonical_json_bytes(payload)
    )


def make_integrity_manifest(
    entries: Sequence[FileDigest],
) -> tuple[bytes, str]:
    ordered = sorted(
        entries,
        key=lambda item: item.relative_path.encode(
            "utf-8"
        ),
    )

    file_entries = [
        {
            "relative_path":
                item.relative_path,
            "size_bytes":
                item.size_bytes,
            "sha256":
                item.sha256,
        }
        for item in ordered
    ]

    aggregate = sha256_bytes(
        canonical_json_bytes(file_entries)
    )

    payload = {
        "schema":
            "ATDS_OBSIDIAN_INTEGRITY_MANIFEST_V0_1",
        "files":
            file_entries,
        "aggregate_digest_sha256":
            aggregate,
    }

    raw = canonical_json_file_bytes(
        payload
    )
    return raw, aggregate


def verify_integrity_manifest(
    stage_root: Path,
) -> dict[str, str]:
    manifest_path = (
        stage_root
        / "generated"
        / "manifests"
        / "integrity-manifest.json"
    )

    _assert_regular_single_link(
        manifest_path
    )

    try:
        payload = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(
            f"cannot parse integrity manifest: {exc}"
        ) from exc

    if payload.get("schema") != (
        "ATDS_OBSIDIAN_INTEGRITY_MANIFEST_V0_1"
    ):
        raise IntegrityError(
            "unexpected integrity manifest schema"
        )

    files = payload.get("files")
    if not isinstance(files, list):
        raise IntegrityError(
            "integrity manifest files must be list"
        )

    expected_aggregate = sha256_bytes(
        canonical_json_bytes(files)
    )
    if payload.get(
        "aggregate_digest_sha256"
    ) != expected_aggregate:
        raise IntegrityError(
            "integrity manifest aggregate mismatch"
        )

    statuses: dict[str, str] = {}

    for item in files:
        relative = item["relative_path"]
        if relative == (
            "generated/manifests/"
            "integrity-manifest.json"
        ):
            raise IntegrityError(
                "integrity manifest includes itself"
            )

        path = stage_root / relative

        if not path.exists():
            statuses[relative] = "MISSING"
            continue

        _assert_regular_single_link(path)
        data = path.read_bytes()

        if (
            len(data) == item["size_bytes"]
            and sha256_bytes(data)
            == item["sha256"]
        ):
            statuses[relative] = "CLEAN"
        else:
            statuses[relative] = "MODIFIED"

    return statuses


def deterministic_tree_files(
    stage_root: Path,
) -> tuple[FileDigest, ...]:
    generated = stage_root / "generated"
    if not generated.exists():
        raise IntegrityError(
            "generated directory missing"
        )

    entries: list[FileDigest] = []
    for path in generated.rglob("*"):
        if not path.is_file():
            continue

        relative = _relative_posix(
            path.resolve(),
            stage_root.resolve(),
        )

        if relative == (
            "generated/manifests/"
            "build-manifest.json"
        ):
            continue

        entries.append(
            file_digest(
                stage_root,
                path,
            )
        )

    entries.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(entries)


def projection_tree_digest(
    stage_root: Path,
) -> str:
    return digest_entries(
        deterministic_tree_files(
            stage_root
        )
    )


def all_generated_files(
    stage_root: Path,
) -> tuple[FileDigest, ...]:
    generated = stage_root / "generated"
    entries: list[FileDigest] = []

    for path in generated.rglob("*"):
        if path.is_file():
            entries.append(
                file_digest(
                    stage_root,
                    path,
                )
            )

    entries.sort(
        key=lambda item:
            item.relative_path.encode("utf-8")
    )
    return tuple(entries)

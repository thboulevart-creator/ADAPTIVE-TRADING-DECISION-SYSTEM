from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable


class ObsidianOpenCompatibilityError(RuntimeError):
    pass


class OpenPointerMissingError(ObsidianOpenCompatibilityError):
    pass


class OpenPointerMixedError(ObsidianOpenCompatibilityError):
    pass


class OpenPointerPartialError(ObsidianOpenCompatibilityError):
    pass


CONTRACT_SCHEMA = "ATDS_OBSIDIAN_OPEN_COMPATIBILITY_CONTRACT_V0_1"
CONTRACT_BLOB = "4974302509a989fbd296ee7052ca15f22a0750a6"

LIVE_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)
SANDBOX_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX"
)
CONTROL_EVIDENCE_ROOT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-P5C3-CONTROL-EVIDENCE"
)

GENERATION_IDS = ("GEN_A", "GEN_B")
NOTES_PER_GENERATION = 128
NESTED_DIRECTORIES = 8
PROMOTION_CYCLES = 250
MIN_READER_SAMPLES = 5000
READER_INTERVAL_SECONDS = 0.001

CURRENT_SCHEMA = "ATDS_OBSIDIAN_P5C3_CURRENT_V0_1"
SNAPSHOT_SCHEMA = "ATDS_OBSIDIAN_P5C3_PREPARE_SNAPSHOT_V0_1"
OPEN_METRICS_SCHEMA = "ATDS_OBSIDIAN_P5C3_OPEN_METRICS_V0_1"
POST_CLOSE_SCHEMA = "ATDS_OBSIDIAN_P5C3_POST_CLOSE_REPORT_V0_1"


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def verify_contract(package_dir: Path) -> dict[str, Any]:
    path = (
        package_dir
        / "obsidian_open_compatibility_contract_v0_1.json"
    )
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise ObsidianOpenCompatibilityError(
            "P5-C3 contract unreadable"
        ) from exc

    if _git_blob_oid(raw) != CONTRACT_BLOB:
        raise ObsidianOpenCompatibilityError(
            "P5-C3 contract blob mismatch"
        )
    if value.get("schema") != CONTRACT_SCHEMA:
        raise ObsidianOpenCompatibilityError(
            "unexpected P5-C3 contract schema"
        )
    return value


def _norm(path: Path) -> str:
    return os.path.normcase(
        os.path.abspath(str(path))
    )


def assert_sandbox_boundary(
    sandbox: Path = SANDBOX_VAULT,
    live_vault: Path = LIVE_VAULT,
) -> None:
    if _norm(sandbox) == _norm(live_vault):
        raise ObsidianOpenCompatibilityError(
            "sandbox overlaps real Vault"
        )
    if _norm(sandbox).startswith(
        _norm(live_vault) + os.sep
    ):
        raise ObsidianOpenCompatibilityError(
            "sandbox is inside real Vault"
        )
    if _norm(live_vault).startswith(
        _norm(sandbox) + os.sep
    ):
        raise ObsidianOpenCompatibilityError(
            "sandbox contains real Vault"
        )

    expected_parent = Path(
        r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    )
    if _norm(sandbox.parent) != _norm(expected_parent):
        raise ObsidianOpenCompatibilityError(
            "sandbox outside qualified OneDrive root"
        )

    if (sandbox / ".git").exists():
        raise ObsidianOpenCompatibilityError(
            "sandbox contains .git"
        )


def obsidian_running() -> bool:
    if os.name != "nt":
        raise ObsidianOpenCompatibilityError(
            "P5-C3 requires Windows"
        )

    completed = subprocess.run(
        [
            "tasklist",
            "/FI",
            "IMAGENAME eq Obsidian.exe",
            "/FO",
            "CSV",
            "/NH",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise ObsidianOpenCompatibilityError(
            "cannot inspect Obsidian process state"
        )

    reader = csv.reader(
        io.StringIO(
            completed.stdout.decode(
                "utf-8",
                errors="replace",
            )
        )
    )
    return any(
        row
        and row[0].strip().strip('"').casefold()
        == "obsidian.exe"
        for row in reader
    )


def _tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ObsidianOpenCompatibilityError(
            f"directory missing: {root}"
        )

    records: list[list[Any]] = []
    for current, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        directories.sort(
            key=lambda item: item.encode("utf-8")
        )
        files.sort(
            key=lambda item: item.encode("utf-8")
        )
        current_path = Path(current)

        for name in files:
            path = current_path / name
            if path.is_symlink():
                raise ObsidianOpenCompatibilityError(
                    "symlink forbidden in protected tree"
                )
            raw = path.read_bytes()
            records.append(
                [
                    path.relative_to(root).as_posix(),
                    _sha256(raw),
                    len(raw),
                ]
            )

    return _sha256(
        _canonical_json_bytes(records)
    )


def _generation_content_digest(
    records: list[list[Any]],
) -> str:
    ordered = sorted(
        records,
        key=lambda row:
            str(row[0]).encode("utf-8"),
    )
    return _sha256(
        _canonical_json_bytes(ordered)
    )


def _note_bytes(
    generation_id: str,
    index: int,
) -> bytes:
    payload = (
        f"---\n"
        f"p5c3_generation: {generation_id}\n"
        f"p5c3_index: {index}\n"
        f"---\n\n"
        f"# Artifact {index:04d}\n\n"
        f"Generation: **{generation_id}**\n\n"
        f"This note exists only inside the sacrificial "
        f"P5-C3 Obsidian-open compatibility Vault.\n"
    )
    return payload.encode("utf-8")


def _index_bytes(
    generation_id: str,
) -> bytes:
    lines = [
        "---",
        f"p5c3_generation: {generation_id}",
        "p5c3_role: GENERATION_INDEX",
        "---",
        "",
        f"# {generation_id} — Generation Index",
        "",
        f"Immutable P5-C3 generation: **{generation_id}**.",
        "",
        "## Notes",
        "",
    ]

    for index in range(NOTES_PER_GENERATION):
        directory = f"d{index % NESTED_DIRECTORIES:02d}"
        lines.append(
            f"- [[{directory}/artifact-{index:04d}"
            f"|Artifact {index:04d}]]"
        )

    return ("\n".join(lines) + "\n").encode("utf-8")


def build_markdown_generation(
    root: Path,
    generation_id: str,
) -> dict[str, Any]:
    if root.exists():
        raise ObsidianOpenCompatibilityError(
            "generation root already exists"
        )
    if generation_id not in GENERATION_IDS:
        raise ObsidianOpenCompatibilityError(
            "unexpected generation ID"
        )

    root.mkdir(parents=True)
    records: list[list[Any]] = []
    file_rows: list[dict[str, Any]] = []

    index_raw = _index_bytes(generation_id)
    index_path = root / "INDEX.md"
    index_path.write_bytes(index_raw)
    records.append(
        ["INDEX.md", _sha256(index_raw), len(index_raw)]
    )
    file_rows.append(
        {
            "path": "INDEX.md",
            "sha256": _sha256(index_raw),
            "size_bytes": len(index_raw),
        }
    )

    for index in range(NOTES_PER_GENERATION):
        directory = root / (
            f"d{index % NESTED_DIRECTORIES:02d}"
        )
        directory.mkdir(exist_ok=True)
        relative = (
            Path(directory.name)
            / f"artifact-{index:04d}.md"
        )
        raw = _note_bytes(
            generation_id,
            index,
        )
        (root / relative).write_bytes(raw)
        row = [
            relative.as_posix(),
            _sha256(raw),
            len(raw),
        ]
        records.append(row)
        file_rows.append(
            {
                "path": row[0],
                "sha256": row[1],
                "size_bytes": row[2],
            }
        )

    content_digest = _generation_content_digest(
        records
    )
    manifest = {
        "schema":
            "ATDS_OBSIDIAN_P5C3_GENERATION_MANIFEST_V0_1",
        "generation_id": generation_id,
        "file_count": len(file_rows),
        "generation_tree_digest_sha256":
            content_digest,
        "files": sorted(
            file_rows,
            key=lambda row:
                row["path"].encode("utf-8"),
        ),
    }
    (root / "MANIFEST.json").write_bytes(
        _canonical_json_bytes(manifest)
    )

    return manifest


def validate_markdown_generation(
    root: Path,
) -> dict[str, Any]:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        raise OpenPointerPartialError(
            "generation manifest missing"
        )

    try:
        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise OpenPointerPartialError(
            "generation manifest unreadable"
        ) from exc

    generation_id = manifest.get(
        "generation_id"
    )
    files = manifest.get("files")
    expected_count = manifest.get(
        "file_count"
    )
    expected_digest = manifest.get(
        "generation_tree_digest_sha256"
    )

    if generation_id not in GENERATION_IDS:
        raise OpenPointerPartialError(
            "generation ID invalid"
        )
    if not isinstance(files, list):
        raise OpenPointerPartialError(
            "generation file list invalid"
        )
    if expected_count != len(files):
        raise OpenPointerPartialError(
            "generation file count mismatch"
        )

    records: list[list[Any]] = []

    for row in files:
        if not isinstance(row, dict):
            raise OpenPointerPartialError(
                "generation row invalid"
            )
        relative = row.get("path")
        expected_sha = row.get("sha256")
        expected_size = row.get("size_bytes")

        if (
            not isinstance(relative, str)
            or "\\" in relative
            or relative.startswith("/")
            or ".." in relative.split("/")
        ):
            raise OpenPointerPartialError(
                "generation relative path invalid"
            )

        target = root / Path(relative)
        try:
            raw = target.read_bytes()
        except FileNotFoundError as exc:
            raise OpenPointerPartialError(
                "generation file missing"
            ) from exc

        if len(raw) != expected_size:
            raise OpenPointerPartialError(
                "generation file size mismatch"
            )
        actual_sha = _sha256(raw)
        if actual_sha != expected_sha:
            raise OpenPointerPartialError(
                "generation file digest mismatch"
            )

        if relative.endswith(".md"):
            text = raw.decode(
                "utf-8",
                errors="strict",
            )
            if generation_id not in text:
                raise OpenPointerMixedError(
                    "generation note identity mismatch"
                )

        records.append(
            [
                relative,
                actual_sha,
                len(raw),
            ]
        )

    actual_digest = _generation_content_digest(
        records
    )
    if actual_digest != expected_digest:
        raise OpenPointerPartialError(
            "generation tree digest mismatch"
        )

    return {
        "generation_id": generation_id,
        "file_count": len(files),
        "generation_tree_digest_sha256":
            actual_digest,
        "directory_tree_digest_sha256":
            _tree_digest(root),
    }


def _current_note_bytes(
    generation_id: str,
    generation_digest: str,
) -> bytes:
    target = (
        f"generations/{generation_id}/INDEX"
    )
    return (
        "---\n"
        f"schema: {CURRENT_SCHEMA}\n"
        f"generation_id: {generation_id}\n"
        f"generation_tree_digest_sha256: "
        f"{generation_digest}\n"
        "---\n\n"
        "# P5-C3 — Current Generation\n\n"
        f"Active generation: **{generation_id}**\n\n"
        f"[[{target}|Open active generation]]\n"
    ).encode("utf-8")


def write_current_atomic(
    sandbox: Path,
    generation_id: str,
    generation_digest: str,
) -> None:
    pointer = sandbox / "CURRENT.md"
    temporary = sandbox / "CURRENT.tmp"

    raw = _current_note_bytes(
        generation_id,
        generation_digest,
    )

    with temporary.open("wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

    os.replace(
        temporary,
        pointer,
    )


def _parse_simple_frontmatter(
    text: str,
) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise OpenPointerPartialError(
            "CURRENT frontmatter missing"
        )

    result: dict[str, str] = {}
    closed = False
    for line in lines[1:]:
        if line == "---":
            closed = True
            break
        if ":" not in line:
            raise OpenPointerPartialError(
                "CURRENT frontmatter invalid"
            )
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()

    if not closed:
        raise OpenPointerPartialError(
            "CURRENT frontmatter not closed"
        )
    return result


def validate_current_pointer(
    sandbox: Path,
) -> dict[str, Any]:
    pointer = sandbox / "CURRENT.md"
    if not pointer.is_file():
        raise OpenPointerMissingError(
            "CURRENT.md missing"
        )

    try:
        raw = pointer.read_bytes()
        text = raw.decode(
            "utf-8",
            errors="strict",
        )
    except (
        OSError,
        UnicodeDecodeError,
    ) as exc:
        raise OpenPointerPartialError(
            "CURRENT.md unreadable"
        ) from exc

    frontmatter = _parse_simple_frontmatter(
        text
    )
    if frontmatter.get("schema") != CURRENT_SCHEMA:
        raise OpenPointerPartialError(
            "CURRENT schema mismatch"
        )

    generation_id = frontmatter.get(
        "generation_id"
    )
    if generation_id not in GENERATION_IDS:
        raise OpenPointerPartialError(
            "CURRENT generation invalid"
        )

    expected_digest = frontmatter.get(
        "generation_tree_digest_sha256"
    )
    if not isinstance(expected_digest, str):
        raise OpenPointerPartialError(
            "CURRENT digest missing"
        )

    expected_link = (
        f"[[generations/{generation_id}/INDEX"
        f"|Open active generation]]"
    )
    if expected_link not in text:
        raise OpenPointerMixedError(
            "CURRENT link target mismatch"
        )

    manifest_path = (
        sandbox
        / "generations"
        / generation_id
        / "MANIFEST.json"
    )
    try:
        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise OpenPointerPartialError(
            "CURRENT target manifest unreadable"
        ) from exc

    if manifest.get("generation_id") != generation_id:
        raise OpenPointerMixedError(
            "CURRENT target generation mismatch"
        )

    target_digest = manifest.get(
        "generation_tree_digest_sha256"
    )
    if target_digest != expected_digest:
        raise OpenPointerMixedError(
            "CURRENT target digest mismatch"
        )

    if not (
        sandbox
        / "generations"
        / generation_id
        / "INDEX.md"
    ).is_file():
        raise OpenPointerPartialError(
            "CURRENT target INDEX missing"
        )

    return {
        "generation_id": generation_id,
        "generation_tree_digest_sha256":
            expected_digest,
        "current_sha256": _sha256(raw),
    }


def _core_plugins_sync_disabled(
    path: Path,
) -> bool:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise ObsidianOpenCompatibilityError(
            "core-plugins.json unreadable"
        ) from exc

    if isinstance(value, dict):
        if not all(
            isinstance(key, str)
            and isinstance(enabled, bool)
            for key, enabled in value.items()
        ):
            raise ObsidianOpenCompatibilityError(
                "core-plugins.json object invalid"
            )
        return not any(
            key.casefold() == "sync"
            and enabled
            for key, enabled in value.items()
        )

    if isinstance(value, list):
        if not all(
            isinstance(item, str)
            for item in value
        ):
            raise ObsidianOpenCompatibilityError(
                "core-plugins.json list invalid"
            )
        return not any(
            item.casefold() == "sync"
            for item in value
        )

    raise ObsidianOpenCompatibilityError(
        "core-plugins.json unsupported shape"
    )


def _safe_obsidian_state(
    vault: Path,
    *,
    require_workspace_current: bool,
) -> dict[str, Any]:
    obsidian = vault / ".obsidian"
    if not obsidian.is_dir():
        raise ObsidianOpenCompatibilityError(
            ".obsidian directory missing"
        )

    forbidden_dirs = []
    for entry in obsidian.iterdir():
        if entry.is_dir():
            forbidden_dirs.append(entry.name)

    if forbidden_dirs:
        raise ObsidianOpenCompatibilityError(
            ".obsidian subdirectory forbidden: "
            + ",".join(sorted(forbidden_dirs))
        )

    core = obsidian / "core-plugins.json"
    if not core.is_file():
        raise ObsidianOpenCompatibilityError(
            "core-plugins.json missing"
        )
    if not _core_plugins_sync_disabled(core):
        raise ObsidianOpenCompatibilityError(
            "Obsidian Sync core plugin enabled"
        )

    community = (
        obsidian
        / "community-plugins.json"
    )
    if community.exists():
        try:
            value = json.loads(
                community.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise ObsidianOpenCompatibilityError(
                "community-plugins.json unreadable"
            ) from exc
        if not isinstance(value, list) or value:
            raise ObsidianOpenCompatibilityError(
                "community plugins enabled"
            )

    workspace = obsidian / "workspace.json"
    workspace_references_current = False

    if require_workspace_current:
        if not workspace.is_file():
            raise ObsidianOpenCompatibilityError(
                "workspace.json missing"
            )
        try:
            workspace_value = json.loads(
                workspace.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise ObsidianOpenCompatibilityError(
                "workspace.json unreadable"
            ) from exc

        def visit(value: Any) -> bool:
            if isinstance(value, str):
                normalized = value.replace(
                    "\\",
                    "/",
                ).casefold()
                return (
                    normalized == "current.md"
                    or normalized.endswith(
                        "/current.md"
                    )
                )
            if isinstance(value, list):
                return any(
                    visit(item)
                    for item in value
                )
            if isinstance(value, dict):
                return any(
                    visit(item)
                    for item in value.values()
                )
            return False

        workspace_references_current = visit(
            workspace_value
        )
        if not workspace_references_current:
            raise ObsidianOpenCompatibilityError(
                "workspace does not reference CURRENT.md"
            )

    return {
        "sync_enabled": False,
        "community_plugins_enabled": False,
        "workspace_references_current":
            workspace_references_current,
        "obsidian_root_files": sorted(
            entry.name
            for entry in obsidian.iterdir()
            if entry.is_file()
        ),
        "obsidian_subdirectory_count": 0,
    }


def _seed_safe_obsidian_config(
    sandbox: Path,
) -> dict[str, Any]:
    live_obsidian = LIVE_VAULT / ".obsidian"
    live_core = (
        live_obsidian
        / "core-plugins.json"
    )
    if not live_core.is_file():
        raise ObsidianOpenCompatibilityError(
            "live core-plugins.json missing"
        )
    if not _core_plugins_sync_disabled(
        live_core
    ):
        raise ObsidianOpenCompatibilityError(
            "live Vault Sync state is unsafe"
        )

    live_community = (
        live_obsidian
        / "community-plugins.json"
    )
    if live_community.exists():
        value = json.loads(
            live_community.read_text(
                encoding="utf-8"
            )
        )
        if not isinstance(value, list) or value:
            raise ObsidianOpenCompatibilityError(
                "live Vault community plugins unsafe"
            )

    obsidian = sandbox / ".obsidian"
    obsidian.mkdir()
    shutil.copyfile(
        live_core,
        obsidian / "core-plugins.json",
    )
    (
        obsidian
        / "community-plugins.json"
    ).write_bytes(b"[]\n")

    return _safe_obsidian_state(
        sandbox,
        require_workspace_current=False,
    )


def _snapshot_directories() -> tuple[Path, Path]:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise ObsidianOpenCompatibilityError(
            "LOCALAPPDATA unavailable"
        )
    primary = (
        Path(local)
        / "ATDS"
        / "obsidian_projection"
        / "p5c3"
        / "snapshots"
    )

    control = CONTROL_EVIDENCE_ROOT / "snapshots"

    for protected in (LIVE_VAULT, SANDBOX_VAULT):
        if _norm(control).startswith(
            _norm(protected) + os.sep
        ) or _norm(control) == _norm(protected):
            raise ObsidianOpenCompatibilityError(
                "control snapshot path overlaps protected Vault"
            )

    return primary, control


def _metrics_log_path() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise ObsidianOpenCompatibilityError(
            "LOCALAPPDATA unavailable"
        )
    return (
        Path(local)
        / "ATDS"
        / "obsidian_projection"
        / "p5c3"
        / "open-events.jsonl"
    )


def _write_snapshot(
    payload: dict[str, Any],
) -> tuple[Path, Path, str]:
    digest = _sha256(
        _canonical_json_bytes(payload)
    )
    envelope = _canonical_json_bytes(
        {
            "payload": payload,
            "payload_sha256": digest,
        }
    )

    primary_dir, backup_dir = (
        _snapshot_directories()
    )
    paths: list[Path] = []

    for directory in (
        primary_dir,
        backup_dir,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        path = (
            directory
            / f"p5c3-open-snapshot-{digest}.json"
        )
        if path.exists():
            existing = path.read_bytes()
            if existing != envelope:
                raise ObsidianOpenCompatibilityError(
                    "snapshot digest-path collision with different bytes"
                )
        else:
            path.write_bytes(envelope)
        paths.append(path)

    if (
        paths[0].read_bytes()
        != paths[1].read_bytes()
    ):
        raise ObsidianOpenCompatibilityError(
            "snapshot copies differ after write"
        )

    return paths[0], paths[1], digest


def _load_snapshot(
    path: Path,
) -> tuple[dict[str, Any], str]:
    try:
        envelope = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise ObsidianOpenCompatibilityError(
            "P5-C3 snapshot unreadable"
        ) from exc

    payload = envelope.get("payload")
    digest = envelope.get("payload_sha256")
    if not isinstance(payload, dict):
        raise ObsidianOpenCompatibilityError(
            "snapshot payload invalid"
        )
    if not isinstance(digest, str):
        raise ObsidianOpenCompatibilityError(
            "snapshot digest invalid"
        )
    actual = _sha256(
        _canonical_json_bytes(payload)
    )
    if actual != digest:
        raise ObsidianOpenCompatibilityError(
            "snapshot digest mismatch"
        )
    expected_name = (
        f"p5c3-open-snapshot-{digest}.json"
    )
    if path.name != expected_name:
        raise ObsidianOpenCompatibilityError(
            "snapshot filename mismatch"
        )

    primary_dir, backup_dir = (
        _snapshot_directories()
    )
    primary = primary_dir / expected_name
    backup = backup_dir / expected_name

    existing = [
        candidate
        for candidate in (primary, backup)
        if candidate.exists()
    ]
    if not existing:
        raise ObsidianOpenCompatibilityError(
            "both snapshot copies are missing"
        )

    reference = existing[0].read_bytes()
    if any(
        candidate.read_bytes() != reference
        for candidate in existing[1:]
    ):
        raise ObsidianOpenCompatibilityError(
            "snapshot copies differ"
        )

    if path not in existing:
        raise ObsidianOpenCompatibilityError(
            "snapshot path is not a verified persisted copy"
        )

    return payload, digest


def _append_event(
    report: dict[str, Any],
) -> Path:
    path = _metrics_log_path()
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with path.open("ab") as handle:
        handle.write(
            _canonical_json_bytes(report)
        )
        handle.flush()
        os.fsync(handle.fileno())
    return path


def prepare_open_experiment() -> dict[str, Any]:
    verify_contract(
        Path(__file__).resolve().parent
    )
    assert_sandbox_boundary()

    if obsidian_running():
        raise ObsidianOpenCompatibilityError(
            "Obsidian must be closed during P5-C3 prepare"
        )
    if SANDBOX_VAULT.exists():
        raise ObsidianOpenCompatibilityError(
            "P5-C3 sandbox already exists"
        )

    live_generated_digest = _tree_digest(
        LIVE_VAULT / "generated"
    )
    live_views_digest = _tree_digest(
        LIVE_VAULT / "views"
    )

    SANDBOX_VAULT.mkdir()
    safe_config = _seed_safe_obsidian_config(
        SANDBOX_VAULT
    )

    generations = (
        SANDBOX_VAULT
        / "generations"
    )
    generations.mkdir()

    manifests: dict[str, dict[str, Any]] = {}
    directory_digests: dict[str, str] = {}

    for generation_id in GENERATION_IDS:
        root = generations / generation_id
        build_markdown_generation(
            root,
            generation_id,
        )
        validated = validate_markdown_generation(
            root
        )
        manifests[generation_id] = validated
        directory_digests[generation_id] = (
            validated[
                "directory_tree_digest_sha256"
            ]
        )

    write_current_atomic(
        SANDBOX_VAULT,
        "GEN_A",
        manifests["GEN_A"][
            "generation_tree_digest_sha256"
        ],
    )
    current = validate_current_pointer(
        SANDBOX_VAULT
    )

    if sorted(
        entry.name
        for entry in SANDBOX_VAULT.iterdir()
    ) != [
        ".obsidian",
        "CURRENT.md",
        "generations",
    ]:
        raise ObsidianOpenCompatibilityError(
            "prepared sandbox top-level entries invalid"
        )

    payload = {
        "schema": SNAPSHOT_SCHEMA,
        "sandbox_path":
            str(SANDBOX_VAULT),
        "live_vault_path":
            str(LIVE_VAULT),
        "live_generated_digest_sha256":
            live_generated_digest,
        "live_views_digest_sha256":
            live_views_digest,
        "generation_directory_digests":
            directory_digests,
        "generation_content_digests": {
            key:
                manifests[key][
                    "generation_tree_digest_sha256"
                ]
            for key in GENERATION_IDS
        },
        "initial_current":
            current,
        "safe_obsidian_seed":
            safe_config,
        "promotion_cycles":
            PROMOTION_CYCLES,
        "minimum_reader_samples":
            MIN_READER_SAMPLES,
        "expected_final_generation":
            "GEN_A",
    }
    (
        snapshot_path,
        snapshot_backup_path,
        token,
    ) = _write_snapshot(
        payload
    )

    return {
        "schema":
            "ATDS_OBSIDIAN_P5C3_PREPARE_REPORT_V0_1",
        "status": "PASS",
        "snapshot_path":
            str(snapshot_path),
        "snapshot_backup_path":
            str(snapshot_backup_path),
        "snapshot_token": token,
        "sandbox_path":
            str(SANDBOX_VAULT),
        "initial_generation": "GEN_A",
        "automatic_obsidian_launch": False,
        "live_vault_modified": False,
        "instruction": (
            "Manually open this exact sacrificial Vault "
            "in Obsidian, open CURRENT.md, make no edits, "
            "enable no Sync/plugins, and leave Obsidian open."
        ),
    }


@dataclass
class OpenReaderMetrics:
    samples: int = 0
    mixed_generation_count: int = 0
    missing_entrypoint_count: int = 0
    partial_generation_count: int = 0
    parse_error_count: int = 0


class OpenReaderProbe:
    def __init__(
        self,
        validator: Callable[[], dict[str, Any]],
    ) -> None:
        self._validator = validator
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.metrics = OpenReaderMetrics()

    def start(self) -> None:
        if self._thread is not None:
            raise ObsidianOpenCompatibilityError(
                "reader already started"
            )
        self._thread = threading.Thread(
            target=self._run,
            name="P5C3OpenReader",
            daemon=True,
        )
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            started = time.perf_counter()
            try:
                self._validator()
            except OpenPointerMissingError:
                self.metrics.missing_entrypoint_count += 1
            except OpenPointerMixedError:
                self.metrics.mixed_generation_count += 1
            except OpenPointerPartialError:
                self.metrics.partial_generation_count += 1
            except Exception:
                self.metrics.parse_error_count += 1
            finally:
                self.metrics.samples += 1

            elapsed = time.perf_counter() - started
            delay = (
                READER_INTERVAL_SECONDS
                - elapsed
            )
            if delay > 0:
                time.sleep(delay)

    def wait_for_progress(
        self,
        baseline: int,
        *,
        timeout_seconds: float = 10.0,
    ) -> None:
        deadline = (
            time.monotonic()
            + timeout_seconds
        )
        while self.metrics.samples <= baseline:
            if time.monotonic() >= deadline:
                raise ObsidianOpenCompatibilityError(
                    "reader did not progress during promotion"
                )
            time.sleep(0.0005)

    def wait_for_samples(
        self,
        minimum: int,
        *,
        timeout_seconds: float = 300.0,
    ) -> None:
        deadline = (
            time.monotonic()
            + timeout_seconds
        )
        while self.metrics.samples < minimum:
            if time.monotonic() >= deadline:
                raise ObsidianOpenCompatibilityError(
                    "reader sample target timeout"
                )
            time.sleep(0.01)

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            if self._thread.is_alive():
                raise ObsidianOpenCompatibilityError(
                    "reader did not stop"
                )


def _require_snapshot_live_digests(
    payload: dict[str, Any],
) -> None:
    if (
        _tree_digest(
            LIVE_VAULT / "generated"
        )
        != payload.get(
            "live_generated_digest_sha256"
        )
    ):
        raise ObsidianOpenCompatibilityError(
            "real live generated digest changed"
        )
    if (
        _tree_digest(
            LIVE_VAULT / "views"
        )
        != payload.get(
            "live_views_digest_sha256"
        )
    ):
        raise ObsidianOpenCompatibilityError(
            "real live views digest changed"
        )


def _require_generation_immutability(
    payload: dict[str, Any],
) -> None:
    expected = payload.get(
        "generation_directory_digests"
    )
    if not isinstance(expected, dict):
        raise ObsidianOpenCompatibilityError(
            "snapshot generation digests missing"
        )

    for generation_id in GENERATION_IDS:
        actual = _tree_digest(
            SANDBOX_VAULT
            / "generations"
            / generation_id
        )
        if actual != expected.get(
            generation_id
        ):
            raise ObsidianOpenCompatibilityError(
                f"immutable generation changed: "
                f"{generation_id}"
            )


def diagnose_open_preconditions(
    snapshot_path: Path,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(
        name: str,
        operation: Callable[[], Any],
    ) -> Any:
        try:
            value = operation()
        except Exception as exc:
            checks.append(
                {
                    "check": name,
                    "status": "FAIL",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            raise
        checks.append(
            {
                "check": name,
                "status": "PASS",
            }
        )
        return value

    try:
        record(
            "CONTRACT",
            lambda: verify_contract(
                Path(__file__).resolve().parent
            ),
        )

        payload, token = record(
            "SNAPSHOT",
            lambda: _load_snapshot(
                snapshot_path
            ),
        )

        def require_snapshot_binding() -> None:
            if payload.get("schema") != SNAPSHOT_SCHEMA:
                raise ObsidianOpenCompatibilityError(
                    "snapshot schema mismatch"
                )
            if payload.get("sandbox_path") != str(
                SANDBOX_VAULT
            ):
                raise ObsidianOpenCompatibilityError(
                    "snapshot sandbox mismatch"
                )

        record(
            "SNAPSHOT_BINDING",
            require_snapshot_binding,
        )

        record(
            "SANDBOX_BOUNDARY",
            assert_sandbox_boundary,
        )

        def require_obsidian_running() -> None:
            if not obsidian_running():
                raise ObsidianOpenCompatibilityError(
                    "Obsidian must be running during P5-C3 open experiment"
                )

        record(
            "OBSIDIAN_PROCESS",
            require_obsidian_running,
        )

        obsidian_state = record(
            "OBSIDIAN_WORKSPACE_AND_PLUGIN_STATE",
            lambda: _safe_obsidian_state(
                SANDBOX_VAULT,
                require_workspace_current=True,
            ),
        )

        record(
            "LIVE_VAULT_DIGESTS",
            lambda: _require_snapshot_live_digests(
                payload
            ),
        )

        record(
            "IMMUTABLE_GENERATIONS",
            lambda: _require_generation_immutability(
                payload
            ),
        )

        current = record(
            "CURRENT_POINTER",
            lambda: validate_current_pointer(
                SANDBOX_VAULT
            ),
        )

        return {
            "schema":
                "ATDS_OBSIDIAN_P5C3_OPEN_DIAGNOSTIC_V0_1",
            "status": "PASS",
            "snapshot_token": token,
            "checks": checks,
            "obsidian_state": obsidian_state,
            "current": current,
            "mutation_performed": False,
            "production_promotion_authorized": False,
            "continuous_observer_authorized": False,
        }

    except Exception as exc:
        return {
            "schema":
                "ATDS_OBSIDIAN_P5C3_OPEN_DIAGNOSTIC_V0_1",
            "status": "FAIL",
            "checks": checks,
            "failure_type": type(exc).__name__,
            "failure": str(exc),
            "mutation_performed": False,
            "production_promotion_authorized": False,
            "continuous_observer_authorized": False,
        }


def run_while_obsidian_open(
    snapshot_path: Path,
) -> dict[str, Any]:
    verify_contract(
        Path(__file__).resolve().parent
    )
    payload, token = _load_snapshot(
        snapshot_path
    )

    if payload.get("schema") != SNAPSHOT_SCHEMA:
        raise ObsidianOpenCompatibilityError(
            "snapshot schema mismatch"
        )
    if payload.get("sandbox_path") != str(
        SANDBOX_VAULT
    ):
        raise ObsidianOpenCompatibilityError(
            "snapshot sandbox mismatch"
        )

    assert_sandbox_boundary()
    if not obsidian_running():
        raise ObsidianOpenCompatibilityError(
            "Obsidian must be running during P5-C3 open experiment"
        )

    obsidian_state = _safe_obsidian_state(
        SANDBOX_VAULT,
        require_workspace_current=True,
    )
    _require_snapshot_live_digests(
        payload
    )
    _require_generation_immutability(
        payload
    )

    reader = OpenReaderProbe(
        lambda: validate_current_pointer(
            SANDBOX_VAULT
        )
    )
    reader.start()

    pointer_write_errors = 0
    samples_at_start = reader.metrics.samples
    completed = 0
    failure_code: str | None = None
    failure_message: str | None = None
    failure_phase: str | None = None
    failure_cycle: int | None = None
    reader_stop_error: str | None = None

    try:
        for cycle in range(PROMOTION_CYCLES):
            if (
                cycle % 25 == 0
                and not obsidian_running()
            ):
                raise ObsidianOpenCompatibilityError(
                    "Obsidian stopped during P5-C3 open experiment"
                )

            target_id = (
                "GEN_B"
                if cycle % 2 == 0
                else "GEN_A"
            )
            before_samples = (
                reader.metrics.samples
            )
            digest = payload[
                "generation_content_digests"
            ][target_id]

            try:
                write_current_atomic(
                    SANDBOX_VAULT,
                    target_id,
                    digest,
                )
            except Exception:
                pointer_write_errors += 1
                raise

            completed += 1
            reader.wait_for_progress(
                before_samples
            )

        samples_after_promotions = (
            reader.metrics.samples
        )
        reader.wait_for_samples(
            MIN_READER_SAMPLES
        )
    except Exception as exc:
        failure_code = type(exc).__name__
        failure_message = str(exc)
        failure_phase = "PROMOTION_LOOP"
        failure_cycle = completed
    finally:
        try:
            reader.stop()
        except Exception as exc:
            reader_stop_error = (
                f"{type(exc).__name__}: {exc}"
            )
            if failure_code is None:
                failure_code = type(exc).__name__
                failure_message = str(exc)
                failure_phase = "READER_STOP"
                failure_cycle = completed

    obsidian_state_after: dict[str, Any] | None = None
    current: dict[str, Any] | None = None
    postcondition_failure_gate: str | None = None

    def final_check(
        gate: str,
        operation: Callable[[], Any],
    ) -> Any:
        nonlocal failure_code
        nonlocal failure_message
        nonlocal failure_phase
        nonlocal failure_cycle
        nonlocal postcondition_failure_gate

        if postcondition_failure_gate is not None:
            return None

        try:
            return operation()
        except Exception as exc:
            postcondition_failure_gate = gate
            if failure_code is None:
                failure_code = type(exc).__name__
                failure_message = str(exc)
                failure_phase = "POSTCONDITION"
                failure_cycle = completed
            return None

    def require_obsidian_at_end() -> None:
        if not obsidian_running():
            raise ObsidianOpenCompatibilityError(
                "Obsidian is not running at end of P5-C3 open experiment"
            )

    final_check(
        "OBSIDIAN_PROCESS_END",
        require_obsidian_at_end,
    )

    if postcondition_failure_gate is None:
        obsidian_state_after = final_check(
            "OBSIDIAN_WORKSPACE_AND_PLUGIN_STATE_END",
            lambda: _safe_obsidian_state(
                SANDBOX_VAULT,
                require_workspace_current=True,
            ),
        )

    if postcondition_failure_gate is None:
        current = final_check(
            "CURRENT_POINTER_END",
            lambda: validate_current_pointer(
                SANDBOX_VAULT
            ),
        )

    if postcondition_failure_gate is None:
        final_check(
            "IMMUTABLE_GENERATIONS_END",
            lambda: _require_generation_immutability(
                payload
            ),
        )

    if postcondition_failure_gate is None:
        final_check(
            "LIVE_VAULT_DIGESTS_END",
            lambda: _require_snapshot_live_digests(
                payload
            ),
        )

    if current is None:
        try:
            current = validate_current_pointer(
                SANDBOX_VAULT
            )
        except Exception:
            current = None

    metrics = reader.metrics
    samples_during_promotions = (
        samples_after_promotions
        - samples_at_start
        if "samples_after_promotions" in locals()
        else metrics.samples
        - samples_at_start
    )

    zero_anomalies = (
        metrics.mixed_generation_count == 0
        and metrics.missing_entrypoint_count == 0
        and metrics.partial_generation_count == 0
        and metrics.parse_error_count == 0
    )

    automated_pass = (
        failure_code is None
        and pointer_write_errors == 0
        and completed == PROMOTION_CYCLES
        and metrics.samples
        >= MIN_READER_SAMPLES
        and samples_during_promotions
        >= PROMOTION_CYCLES
        and zero_anomalies
        and postcondition_failure_gate is None
        and current is not None
        and current["generation_id"]
        == "GEN_A"
    )

    report = {
        "schema": OPEN_METRICS_SCHEMA,
        "status":
            "PASS_AUTOMATED_OPEN_EXPERIMENT"
            if automated_pass
            else "FAIL",
        "snapshot_token": token,
        "sandbox_path":
            str(SANDBOX_VAULT),
        "obsidian_process_running":
            True,
        "obsidian_state_before":
            obsidian_state,
        "obsidian_state_after":
            obsidian_state_after,
        "cycles_requested":
            PROMOTION_CYCLES,
        "cycles_completed":
            completed,
        "samples":
            metrics.samples,
        "samples_during_promotions":
            samples_during_promotions,
        "pointer_write_error_count":
            pointer_write_errors,
        "mixed_generation_count":
            metrics.mixed_generation_count,
        "missing_entrypoint_count":
            metrics.missing_entrypoint_count,
        "partial_generation_count":
            metrics.partial_generation_count,
        "parse_error_count":
            metrics.parse_error_count,
        "failure_code":
            failure_code,
        "failure_message":
            failure_message,
        "failure_phase":
            failure_phase,
        "failure_cycle":
            failure_cycle,
        "reader_stop_error":
            reader_stop_error,
        "postcondition_failure_gate":
            postcondition_failure_gate,
        "final_generation_id": (
            None
            if current is None
            else current["generation_id"]
        ),
        "final_generation_tree_digest_sha256": (
            None
            if current is None
            else current[
                "generation_tree_digest_sha256"
            ]
        ),
        "manual_visual_acceptance_required":
            True,
        "manual_visual_acceptance_pending":
            automated_pass,
        "expected_visible_note":
            "CURRENT.md",
        "expected_visible_generation":
            "GEN_A",
        "expected_visible_link":
            "generations/GEN_A/INDEX",
        "live_vault_modified": False,
        "obsidian_open_qualified": False,
        "production_promotion_authorized":
            False,
        "p5c3_qualified": False,
    }

    event_log = _append_event(report)
    report["append_only_event_log"] = str(
        event_log
    )
    return report


def post_close_verify(
    snapshot_path: Path,
    *,
    manual_visual_accepted: bool,
) -> dict[str, Any]:
    verify_contract(
        Path(__file__).resolve().parent
    )
    payload, token = _load_snapshot(
        snapshot_path
    )

    if not manual_visual_accepted:
        raise ObsidianOpenCompatibilityError(
            "manual visual acceptance not supplied"
        )

    if obsidian_running():
        raise ObsidianOpenCompatibilityError(
            "Obsidian must be fully closed before P5-C3 post-close verify"
        )

    obsidian_state = _safe_obsidian_state(
        SANDBOX_VAULT,
        require_workspace_current=True,
    )
    _require_generation_immutability(
        payload
    )
    _require_snapshot_live_digests(
        payload
    )

    current = validate_current_pointer(
        SANDBOX_VAULT
    )
    if current["generation_id"] != "GEN_A":
        raise ObsidianOpenCompatibilityError(
            "post-close final generation is not GEN_A"
        )

    report = {
        "schema": POST_CLOSE_SCHEMA,
        "status": "PASS",
        "snapshot_token": token,
        "sandbox_path":
            str(SANDBOX_VAULT),
        "manual_visual_acceptance":
            True,
        "final_generation_id":
            current["generation_id"],
        "obsidian_state":
            obsidian_state,
        "live_vault_modified":
            False,
        "obsidian_open_qualified":
            True,
        "production_promotion_authorized":
            False,
        "continuous_observer_authorized":
            False,
        "p5c3_qualified":
            True,
        "graph_current_pointer_semantics_qualified":
            False,
    }
    event_log = _append_event(report)
    report["append_only_event_log"] = str(
        event_log
    )
    return report

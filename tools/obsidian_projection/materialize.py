from __future__ import annotations

import ctypes
import json
import os
import stat
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from .classification import git_blob_oid
from .integrity import (
    _is_reparse_or_link,
    all_generated_files,
    projection_tree_digest,
    sha256_bytes,
    verify_integrity_manifest,
)
from .p2_verify import build_report as build_p2_report


EXPECTED_REPOSITORY = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_FINAL_NAME = "ATDS-OBSIDIAN-PROJECTION"
FROZEN_SOURCE_COMMIT = (
    "7bd8c1312430dfc3def5523eb65397a5d6a5ae05"
)
FROZEN_SOURCE_TREE = (
    "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b"
)


class MaterializationError(RuntimeError):
    """Raised when P3-B must fail closed."""


@dataclass(frozen=True)
class FilesystemIdentity:
    volume_serial: int
    file_identity: int
    filesystem: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RepositoryState:
    branch: str
    head: str
    status_porcelain: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise MaterializationError(
            f"cannot read JSON contract/manifest: {path}: {exc}"
        ) from exc


def _run_git(
    repo_root: Path,
    *args: str,
) -> str:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode(
            "utf-8",
            errors="replace",
        ).strip()
        raise MaterializationError(
            f"git {' '.join(args)} failed: {stderr}"
        )
    return completed.stdout.decode(
        "utf-8",
        errors="strict",
    ).rstrip("\r\n")


def repository_state(
    repo_root: Path,
) -> RepositoryState:
    return RepositoryState(
        branch=_run_git(
            repo_root,
            "branch",
            "--show-current",
        ),
        head=_run_git(
            repo_root,
            "rev-parse",
            "HEAD",
        ),
        status_porcelain=_run_git(
            repo_root,
            "status",
            "--porcelain",
        ),
    )


def _norm(path: Path) -> str:
    return os.path.normcase(
        os.path.abspath(str(path))
    )


def _is_within(
    child: Path,
    parent: Path,
) -> bool:
    child_norm = _norm(child)
    parent_norm = _norm(parent)

    try:
        return (
            os.path.commonpath(
                [child_norm, parent_norm]
            )
            == parent_norm
        )
    except ValueError:
        return False


def _assert_no_reparse_ancestors(
    path: Path,
) -> None:
    current = path

    while True:
        if current.exists() and _is_reparse_or_link(
            current
        ):
            raise MaterializationError(
                "reparse/symlink/junction ancestor "
                f"forbidden: {current}"
            )

        parent = current.parent
        if parent == current:
            break
        current = parent


def _windows_volume_information(
    path: Path,
) -> tuple[int, str]:
    if os.name != "nt":
        raise MaterializationError(
            "P3-B real materialization requires Windows"
        )

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )

    get_volume_path = (
        kernel32.GetVolumePathNameW
    )
    get_volume_path.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
    ]
    get_volume_path.restype = ctypes.c_int

    get_volume_info = (
        kernel32.GetVolumeInformationW
    )
    get_volume_info.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.c_wchar_p,
        ctypes.c_uint32,
    ]
    get_volume_info.restype = ctypes.c_int

    volume_path = ctypes.create_unicode_buffer(
        260
    )
    if not get_volume_path(
        str(path),
        volume_path,
        len(volume_path),
    ):
        raise MaterializationError(
            "GetVolumePathNameW failed: "
            f"{ctypes.get_last_error()}"
        )

    serial = ctypes.c_uint32()
    max_component = ctypes.c_uint32()
    flags = ctypes.c_uint32()
    fs_name = ctypes.create_unicode_buffer(
        64
    )

    if not get_volume_info(
        volume_path.value,
        None,
        0,
        ctypes.byref(serial),
        ctypes.byref(max_component),
        ctypes.byref(flags),
        fs_name,
        len(fs_name),
    ):
        raise MaterializationError(
            "GetVolumeInformationW failed: "
            f"{ctypes.get_last_error()}"
        )

    return int(serial.value), fs_name.value


def filesystem_identity(
    path: Path,
) -> FilesystemIdentity:
    try:
        info = path.stat()
    except OSError as exc:
        raise MaterializationError(
            f"cannot stat filesystem object: {path}: {exc}"
        ) from exc

    file_identity = getattr(
        info,
        "st_ino",
        None,
    )
    if (
        file_identity is None
        or int(file_identity) == 0
    ):
        raise MaterializationError(
            f"stable file/directory identity unavailable: "
            f"{path}"
        )

    volume_serial, fs_name = (
        _windows_volume_information(path)
    )

    return FilesystemIdentity(
        volume_serial=volume_serial,
        file_identity=int(file_identity),
        filesystem=fs_name,
    )


def _known_sync_roots() -> tuple[Path, ...]:
    names = (
        "OneDrive",
        "OneDriveConsumer",
        "OneDriveCommercial",
        "Dropbox",
        "BOX",
        "Box",
        "iCloudDrive",
        "ICLOUDDRIVE",
    )
    found: list[Path] = []

    for name in names:
        value = os.environ.get(name)
        if not value:
            continue
        candidate = Path(value)
        if candidate.exists():
            resolved = candidate.resolve()
            if resolved not in found:
                found.append(resolved)

    return tuple(found)


def verify_p2_core_blobs(
    package_dir: Path,
    contract: Mapping[str, Any],
) -> None:
    expected = contract[
        "qualified_p2_core_blobs"
    ]

    projection_contract_path = (
        package_dir
        / "deterministic_projection_contract_v0_1.json"
    )
    try:
        projection_contract_raw = (
            projection_contract_path.read_bytes()
        )
    except OSError as exc:
        raise MaterializationError(
            "cannot read pinned P2-A projection contract"
        ) from exc

    actual_contract_oid = git_blob_oid(
        projection_contract_raw
    )
    expected_contract_oid = contract[
        "p2a_contract_blob_sha"
    ]
    if actual_contract_oid != expected_contract_oid:
        raise MaterializationError(
            "P2-A contract blob mismatch: "
            f"expected={expected_contract_oid} "
            f"actual={actual_contract_oid}"
        )

    for relative, expected_oid in expected.items():
        prefix = "tools/obsidian_projection/"
        if not relative.startswith(prefix):
            raise MaterializationError(
                "unexpected P2 core pin path"
            )

        local_name = relative[len(prefix):]
        path = package_dir / local_name
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise MaterializationError(
                f"cannot read pinned P2 core: {path}: {exc}"
            ) from exc

        actual_oid = git_blob_oid(raw)
        if actual_oid != expected_oid:
            raise MaterializationError(
                f"P2 core blob mismatch: {relative}: "
                f"expected={expected_oid} actual={actual_oid}"
            )


def validate_destination(
    repo_root: Path,
    contract: Mapping[str, Any],
) -> tuple[Path, Path]:
    if os.name != "nt":
        raise MaterializationError(
            "real Vault materialization requires Windows"
        )

    local_appdata = os.environ.get(
        "LOCALAPPDATA"
    )
    if not local_appdata:
        raise MaterializationError(
            "LOCALAPPDATA unavailable"
        )

    parent = Path(
        local_appdata
    ).resolve()
    final_path = (
        parent / EXPECTED_FINAL_NAME
    ).resolve(strict=False)

    expected = Path(
        contract["destination"][
            "observed_resolved_path"
        ]
    )

    if _norm(final_path) != _norm(expected):
        raise MaterializationError(
            "resolved final destination mismatch: "
            f"expected={expected} actual={final_path}"
        )

    if not parent.exists() or not parent.is_dir():
        raise MaterializationError(
            f"LOCALAPPDATA parent unavailable: {parent}"
        )

    if final_path.exists():
        raise MaterializationError(
            f"final Vault already exists: {final_path}"
        )

    repo_resolved = repo_root.resolve()
    if (
        _is_within(final_path, repo_resolved)
        or _is_within(repo_resolved, final_path)
    ):
        raise MaterializationError(
            "repository/Vault containment forbidden"
        )

    for sync_root in _known_sync_roots():
        if _is_within(final_path, sync_root):
            raise MaterializationError(
                "destination lies inside known sync root: "
                f"{sync_root}"
            )

    _assert_no_reparse_ancestors(parent)

    volume_serial, filesystem = (
        _windows_volume_information(parent)
    )
    if filesystem.upper() != (
        contract["destination"][
            "expected_filesystem"
        ].upper()
    ):
        raise MaterializationError(
            f"unexpected destination filesystem: "
            f"{filesystem}"
        )

    if volume_serial <= 0:
        raise MaterializationError(
            "destination volume identity unavailable"
        )

    return parent, final_path


def _assert_regular_single_link(
    path: Path,
) -> None:
    if _is_reparse_or_link(path):
        raise MaterializationError(
            f"reparse/symlink/junction forbidden: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise MaterializationError(
            f"cannot stat file: {path}: {exc}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise MaterializationError(
            f"non-regular file forbidden: {path}"
        )

    link_count = getattr(
        info,
        "st_nlink",
        None,
    )
    if link_count is None:
        raise MaterializationError(
            f"hard-link count unavailable: {path}"
        )
    if int(link_count) != 1:
        raise MaterializationError(
            f"unexpected hard-link count "
            f"{link_count}: {path}"
        )


def _assert_tree_no_aliases(
    root: Path,
) -> None:
    if _is_reparse_or_link(root):
        raise MaterializationError(
            f"tree root is reparse/link: {root}"
        )

    for current, directories, files in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current)

        for name in tuple(directories):
            child = current_path / name
            if _is_reparse_or_link(child):
                raise MaterializationError(
                    f"directory alias forbidden: {child}"
                )

        for name in files:
            _assert_regular_single_link(
                current_path / name
            )


def _digest_map(
    root: Path,
) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}

    for item in all_generated_files(root):
        result[item.relative_path] = (
            item.size_bytes,
            item.sha256,
        )

    return result


def _parse_build_manifest(
    root: Path,
) -> dict[str, Any]:
    return _load_json(
        root
        / "generated"
        / "manifests"
        / "build-manifest.json"
    )


def _assert_build_manifest_identity(
    root: Path,
    p2_report: Mapping[str, Any],
) -> None:
    manifest = _parse_build_manifest(root)

    expected = {
        "source_repository":
            p2_report["repository"],
        "source_commit":
            p2_report["source_commit"],
        "source_tree":
            p2_report["source_tree"],
        "semantic_record_digest_sha256":
            p2_report[
                "semantic_record_digest_sha256"
            ],
        "artifact_record_count":
            p2_report["artifact_record_count"],
        "relation_record_count":
            p2_report["relation_record_count"],
        "artifact_set_digest_sha256":
            p2_report[
                "artifact_set_digest_sha256"
            ],
        "relation_set_digest_sha256":
            p2_report[
                "relation_set_digest_sha256"
            ],
        "integrity_manifest_sha256":
            p2_report[
                "integrity_manifest_sha256"
            ],
        "build_status":
            "PASS",
    }

    mismatches = {
        field: {
            "expected": value,
            "actual": manifest.get(field),
        }
        for field, value in expected.items()
        if manifest.get(field) != value
    }

    if mismatches:
        raise MaterializationError(
            "build-manifest identity mismatch: "
            + json.dumps(
                mismatches,
                sort_keys=True,
            )
        )


def validate_fresh_p2_report(
    report: Mapping[str, Any],
) -> Path:
    if report.get("repository") != EXPECTED_REPOSITORY:
        raise MaterializationError(
            "fresh P2 repository identity mismatch"
        )
    if report.get(
        "source_commit"
    ) != FROZEN_SOURCE_COMMIT:
        raise MaterializationError(
            "fresh P2 source commit mismatch"
        )
    if report.get(
        "source_tree"
    ) != FROZEN_SOURCE_TREE:
        raise MaterializationError(
            "fresh P2 source tree mismatch"
        )

    if report.get("status") != "PASS":
        raise MaterializationError(
            "fresh P2 report is not PASS"
        )
    if report.get(
        "semantic_record_count"
    ) != 74:
        raise MaterializationError(
            "fresh P2 semantic record count != 74"
        )
    if report.get(
        "artifact_record_count"
    ) != 74:
        raise MaterializationError(
            "fresh P2 artifact record count != 74"
        )
    if report.get(
        "real_vault_created"
    ) is not False:
        raise MaterializationError(
            "fresh P2 unexpectedly reports Vault creation"
        )
    if report.get(
        "obsidian_config_created"
    ) is not False:
        raise MaterializationError(
            "fresh P2 unexpectedly reports .obsidian creation"
        )

    double = report.get("double_build")
    if not isinstance(double, dict):
        raise MaterializationError(
            "fresh P2 double-build proof missing"
        )
    if double.get("mismatched_files") != []:
        raise MaterializationError(
            "fresh P2 double-build mismatch"
        )
    if (
        double.get("byte_identical_file_count")
        != double.get("relative_path_count")
    ):
        raise MaterializationError(
            "fresh P2 byte identity count mismatch"
        )

    expected_clean = (
        int(report["artifact_record_count"])
        + int(report["relation_record_count"])
    )
    if report.get(
        "build_a_integrity_clean_count"
    ) != expected_clean:
        raise MaterializationError(
            "fresh P2 build A integrity not all CLEAN"
        )
    if report.get(
        "build_b_integrity_clean_count"
    ) != expected_clean:
        raise MaterializationError(
            "fresh P2 build B integrity not all CLEAN"
        )

    expected_generated = (
        int(report["artifact_record_count"])
        + int(report["relation_record_count"])
        + 2
    )
    if report.get(
        "generated_file_count"
    ) != expected_generated:
        raise MaterializationError(
            "fresh P2 generated file count mismatch"
        )

    build_a = Path(
        str(report["build_a"])
    )
    build_b = Path(
        str(report["build_b"])
    )

    if not build_a.exists() or not build_b.exists():
        raise MaterializationError(
            "fresh P2 build path missing"
        )

    map_a = _digest_map(build_a)
    map_b = _digest_map(build_b)
    if map_a != map_b:
        raise MaterializationError(
            "fresh P2 builds differ on re-verification"
        )

    _assert_tree_no_aliases(build_a)
    _assert_tree_no_aliases(build_b)

    statuses_a = verify_integrity_manifest(
        build_a
    )
    statuses_b = verify_integrity_manifest(
        build_b
    )
    if any(
        status != "CLEAN"
        for status in statuses_a.values()
    ):
        raise MaterializationError(
            "fresh P2 build A integrity recheck failed"
        )
    if any(
        status != "CLEAN"
        for status in statuses_b.values()
    ):
        raise MaterializationError(
            "fresh P2 build B integrity recheck failed"
        )

    if projection_tree_digest(
        build_a
    ) != report[
        "projection_tree_digest_sha256"
    ]:
        raise MaterializationError(
            "fresh P2 projection-tree digest mismatch"
        )

    _assert_build_manifest_identity(
        build_a,
        report,
    )

    return build_a


def _create_incoming_structure(
    incoming: Path,
) -> FilesystemIdentity:
    try:
        incoming.mkdir(exist_ok=False)
    except FileExistsError as exc:
        raise MaterializationError(
            f"incoming path already exists: {incoming}"
        ) from exc

    identity = filesystem_identity(
        incoming
    )

    for relative in (
        "generated",
        "generated/artifacts",
        "generated/relations",
        "generated/manifests",
        "views",
    ):
        (incoming / relative).mkdir()

    return identity


def _copy_qualified_generated_tree(
    source_build: Path,
    incoming: Path,
) -> None:
    source_map = _digest_map(
        source_build
    )

    for relative in sorted(
        source_map,
        key=lambda value: value.encode("utf-8"),
    ):
        source_file = source_build / relative
        destination = incoming / relative

        _assert_regular_single_link(
            source_file
        )

        data = source_file.read_bytes()

        try:
            with destination.open("xb") as handle:
                handle.write(data)
        except FileExistsError as exc:
            raise MaterializationError(
                f"copy target already exists: {relative}"
            ) from exc

        _assert_regular_single_link(
            destination
        )

        expected_size, expected_sha = (
            source_map[relative]
        )
        if (
            len(data) != expected_size
            or sha256_bytes(data) != expected_sha
        ):
            raise MaterializationError(
                f"source digest changed during copy: "
                f"{relative}"
            )

        copied = destination.read_bytes()
        if (
            len(copied) != expected_size
            or sha256_bytes(copied)
            != expected_sha
        ):
            raise MaterializationError(
                f"copied digest mismatch: {relative}"
            )


def _assert_exact_projection_layout(
    root: Path,
) -> None:
    expected_directories = {
        "generated",
        "generated/artifacts",
        "generated/relations",
        "generated/manifests",
        "views",
    }

    actual_directories = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_dir()
    }

    if actual_directories != expected_directories:
        raise MaterializationError(
            "unexpected projection directory set: "
            f"{sorted(actual_directories)}"
        )

    allowed_top = {
        "generated",
        "views",
    }
    actual_top = {
        path.name
        for path in root.iterdir()
    }
    if actual_top != allowed_top:
        raise MaterializationError(
            f"unexpected top-level projection entries: "
            f"{sorted(actual_top)}"
        )

    views = root / "views"
    if any(views.iterdir()):
        raise MaterializationError(
            "views must be empty"
        )

    if (root / ".obsidian").exists():
        raise MaterializationError(
            ".obsidian must be absent"
        )


def verify_materialized_projection(
    *,
    root: Path,
    source_build: Path,
    p2_report: Mapping[str, Any],
    expected_identity: FilesystemIdentity | None,
) -> FilesystemIdentity:
    if not root.exists() or not root.is_dir():
        raise MaterializationError(
            f"projection root missing: {root}"
        )

    _assert_tree_no_aliases(root)
    _assert_exact_projection_layout(root)

    identity = filesystem_identity(root)
    if (
        expected_identity is not None
        and identity != expected_identity
    ):
        raise MaterializationError(
            "filesystem identity changed across rename"
        )

    source_map = _digest_map(
        source_build
    )
    copied_map = _digest_map(root)

    if copied_map != source_map:
        raise MaterializationError(
            "materialized generated tree differs "
            "from qualified P2 source"
        )

    if len(copied_map) != int(
        p2_report["generated_file_count"]
    ):
        raise MaterializationError(
            "materialized generated file count mismatch"
        )

    statuses = verify_integrity_manifest(
        root
    )
    if any(
        status != "CLEAN"
        for status in statuses.values()
    ):
        raise MaterializationError(
            "materialized integrity manifest not all CLEAN"
        )

    _assert_build_manifest_identity(
        root,
        p2_report,
    )

    if projection_tree_digest(root) != (
        p2_report[
            "projection_tree_digest_sha256"
        ]
    ):
        raise MaterializationError(
            "materialized projection-tree digest mismatch"
        )

    return identity


def _quarantine_after_failed_post_verify(
    *,
    final_path: Path,
    expected_identity: FilesystemIdentity,
    quarantine_path: Path,
) -> str:
    if not final_path.exists():
        return "FINAL_MISSING_NO_QUARANTINE"

    try:
        current_identity = filesystem_identity(
            final_path
        )
    except MaterializationError:
        return "IDENTITY_UNAVAILABLE_LEFT_IN_PLACE"

    if current_identity != expected_identity:
        return "IDENTITY_MISMATCH_LEFT_IN_PLACE"

    if quarantine_path.exists():
        return "QUARANTINE_TARGET_EXISTS_LEFT_IN_PLACE"

    try:
        final_path.rename(
            quarantine_path
        )
    except OSError:
        return "QUARANTINE_RENAME_FAILED_LEFT_IN_PLACE"

    return "QUARANTINED"


def materialize_once(
    repo_root: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    contract = _load_json(
        package_dir
        / "materialization_contract_v0_1.json"
    )

    if contract.get(
        "qualified_p2b_head"
    ) != "157b519dafb226e53ae13a281f7dc294d584cc0d":
        raise MaterializationError(
            "P3 contract P2-B HEAD binding mismatch"
        )

    verify_p2_core_blobs(
        package_dir,
        contract,
    )

    repo_root = repo_root.resolve()
    repo_before = repository_state(
        repo_root
    )

    parent, final_path = validate_destination(
        repo_root,
        contract,
    )

    p2_report = build_p2_report(
        repo_root
    )
    source_build = validate_fresh_p2_report(
        p2_report
    )

    digest = str(
        p2_report[
            "projection_tree_digest_sha256"
        ]
    )
    if (
        len(digest) != 64
        or any(
            char not in "0123456789abcdef"
            for char in digest.lower()
        )
    ):
        raise MaterializationError(
            "invalid P2 projection-tree digest"
        )

    suffix = digest[:16]
    incoming = parent / (
        "ATDS-OBSIDIAN-PROJECTION."
        f"__INCOMING__.{suffix}"
    )
    quarantine = parent / (
        "ATDS-OBSIDIAN-PROJECTION."
        f"__FAILED__.{suffix}"
    )

    if final_path.exists():
        raise MaterializationError(
            "final path appeared before incoming creation"
        )
    if incoming.exists():
        raise MaterializationError(
            f"incoming path already exists: {incoming}"
        )

    incoming_identity = (
        _create_incoming_structure(
            incoming
        )
    )

    final_renamed = False
    quarantine_status = None

    try:
        _copy_qualified_generated_tree(
            source_build,
            incoming,
        )

        verify_materialized_projection(
            root=incoming,
            source_build=source_build,
            p2_report=p2_report,
            expected_identity=incoming_identity,
        )

        repo_mid = repository_state(
            repo_root
        )
        if repo_mid != repo_before:
            raise MaterializationError(
                "repository changed before final promotion"
            )

        if final_path.exists():
            raise MaterializationError(
                "final destination appeared before rename"
            )

        incoming_volume = filesystem_identity(
            incoming
        )
        parent_volume = filesystem_identity(
            parent
        )
        if (
            incoming_volume.volume_serial
            != parent_volume.volume_serial
        ):
            raise MaterializationError(
                "cross-volume final promotion forbidden"
            )

        incoming.rename(
            final_path
        )
        final_renamed = True

        final_identity = (
            verify_materialized_projection(
                root=final_path,
                source_build=source_build,
                p2_report=p2_report,
                expected_identity=incoming_identity,
            )
        )

        if _norm(final_path) != _norm(
            Path(
                contract["destination"][
                    "observed_resolved_path"
                ]
            )
        ):
            raise MaterializationError(
                "post-promotion final destination mismatch"
            )

        repo_after = repository_state(
            repo_root
        )
        if repo_after != repo_before:
            raise MaterializationError(
                "repository changed during materialization"
            )

        return {
            "schema":
                "ATDS_OBSIDIAN_P3B_EXECUTION_REPORT_V0_1",
            "repository":
                EXPECTED_REPOSITORY,
            "qualified_p2b_head":
                contract["qualified_p2b_head"],
            "source_commit":
                p2_report["source_commit"],
            "source_tree":
                p2_report["source_tree"],
            "semantic_record_digest_sha256":
                p2_report[
                    "semantic_record_digest_sha256"
                ],
            "artifact_set_digest_sha256":
                p2_report[
                    "artifact_set_digest_sha256"
                ],
            "relation_set_digest_sha256":
                p2_report[
                    "relation_set_digest_sha256"
                ],
            "integrity_manifest_sha256":
                p2_report[
                    "integrity_manifest_sha256"
                ],
            "projection_tree_digest_sha256":
                digest,
            "artifact_record_count":
                p2_report["artifact_record_count"],
            "relation_record_count":
                p2_report["relation_record_count"],
            "generated_file_count":
                p2_report["generated_file_count"],
            "p2_double_build_byte_match":
                True,
            "final_destination":
                str(final_path),
            "final_filesystem_identity":
                final_identity.to_dict(),
            "views_empty":
                True,
            "obsidian_config_created":
                False,
            "obsidian_launched":
                False,
            "plugins_enabled":
                False,
            "sync_enabled":
                False,
            "git_automation_enabled":
                False,
            "repository_state_preserved":
                True,
            "materialization_qualified":
                True,
            "status":
                "PASS",
        }

    except Exception:
        if final_renamed:
            quarantine_status = (
                _quarantine_after_failed_post_verify(
                    final_path=final_path,
                    expected_identity=incoming_identity,
                    quarantine_path=quarantine,
                )
            )

        message = (
            "P3-B materialization failed"
        )
        if quarantine_status is not None:
            message += (
                f"; quarantine_status="
                f"{quarantine_status}"
            )
        raise MaterializationError(
            message
        )

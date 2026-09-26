from __future__ import annotations

import csv
import ctypes
import hashlib
import io
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .classification import git_blob_oid
from .materialize import (
    FilesystemIdentity,
    MaterializationError,
    _digest_map as qualified_temp_digest_map,
    filesystem_identity,
    repository_state,
    validate_fresh_p2_report,
    verify_p2_core_blobs,
)
from .p2_verify import build_report as build_p2_report


QUALIFIED_P3B_HEAD = (
    "bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba"
)
QUALIFIED_P2B_HEAD = (
    "157b519dafb226e53ae13a281f7dc294d584cc0d"
)
PREDECESSOR_P3D_HEAD = (
    "3cafa6e98ec45236aba48ddf60e55957e49bed76"
)
FIRST_OPEN_CONTRACT_V02_BLOB = (
    "ddda9eb0abac4ff3fae02f459e16a1fa70bf907d"
)
MATERIALIZATION_CONTRACT_BLOB = (
    "b11120c9f6d3ee68b253928b125747159536bbf0"
)
QUALIFIED_MATERIALIZE_HELPER_BLOB = (
    "9c4c925f59200c11054d08f16dfca38820d6f9ac"
)

EXPECTED_VAULT = (
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)
EXPECTED_GENERATED_COUNT = 92
EXPECTED_TREE_DIGEST = (
    "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0"
)
EXPECTED_INTEGRITY_MANIFEST_SHA256 = (
    "a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b"
)

CLOUD_6_TAG = 0x9000601A
SYMLINK_TAG = 0xA000000C
MOUNT_POINT_TAG = 0xA0000003

FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
FILE_ATTRIBUTE_SPARSE_FILE = 0x00000200
FILE_ATTRIBUTE_OFFLINE = 0x00001000
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FSCTL_GET_REPARSE_POINT = 0x000900A8
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

SNAPSHOT_SCHEMA = (
    "ATDS_OBSIDIAN_FIRST_OPEN_ONEDRIVE_SNAPSHOT_V0_2"
)
PREPARE_REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P3D2_PREPARE_REPORT_V0_2"
)
VERIFY_REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P3D2_VERIFY_REPORT_V0_2"
)


class FirstOpenOneDriveError(RuntimeError):
    """Raised whenever P3-D2 must fail closed."""


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise FirstOpenOneDriveError(
            f"cannot load JSON: {path}: {exc}"
        ) from exc
    if not isinstance(value, dict):
        raise FirstOpenOneDriveError(
            f"JSON object required: {path}"
        )
    return value


def _verify_blob(
    path: Path,
    expected_oid: str,
    label: str,
) -> None:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"cannot read pinned {label}: {path}: {exc}"
        ) from exc

    actual = git_blob_oid(raw)
    if actual != expected_oid:
        raise FirstOpenOneDriveError(
            f"{label} blob mismatch: "
            f"expected={expected_oid} actual={actual}"
        )


def verify_harness_dependencies(
    package_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    contract_path = (
        package_dir
        / "first_open_safety_contract_v0_2.json"
    )
    materialization_contract_path = (
        package_dir
        / "materialization_contract_v0_1.json"
    )
    materialize_helper_path = (
        package_dir / "materialize.py"
    )

    _verify_blob(
        contract_path,
        FIRST_OPEN_CONTRACT_V02_BLOB,
        "P3-C2 first-open contract",
    )
    _verify_blob(
        materialization_contract_path,
        MATERIALIZATION_CONTRACT_BLOB,
        "P3-A materialization contract",
    )
    _verify_blob(
        materialize_helper_path,
        QUALIFIED_MATERIALIZE_HELPER_BLOB,
        "P3-B materialization helper",
    )

    contract = _load_json(contract_path)
    materialization_contract = _load_json(
        materialization_contract_path
    )

    if contract.get("schema") != (
        "ATDS_OBSIDIAN_FIRST_OPEN_SAFETY_CONTRACT_V0_2"
    ):
        raise FirstOpenOneDriveError(
            "unexpected P3-C2 contract schema"
        )
    if contract.get(
        "predecessor_p3d_head"
    ) != PREDECESSOR_P3D_HEAD:
        raise FirstOpenOneDriveError(
            "P3-C2 predecessor P3-D binding mismatch"
        )
    if contract.get(
        "qualified_p3b_head"
    ) != QUALIFIED_P3B_HEAD:
        raise FirstOpenOneDriveError(
            "P3-C2 P3-B binding mismatch"
        )
    if contract.get(
        "qualified_p2b_head"
    ) != QUALIFIED_P2B_HEAD:
        raise FirstOpenOneDriveError(
            "P3-C2 P2-B binding mismatch"
        )

    vault = contract.get("materialized_vault")
    if not isinstance(vault, dict) or vault.get(
        "observed_resolved_path"
    ) != EXPECTED_VAULT:
        raise FirstOpenOneDriveError(
            "P3-C2 exact OneDrive Vault path mismatch"
        )

    try:
        verify_p2_core_blobs(
            package_dir,
            materialization_contract,
        )
    except MaterializationError as exc:
        raise FirstOpenOneDriveError(
            str(exc)
        ) from exc

    return contract, materialization_contract


def _obsidian_running() -> bool:
    if os.name != "nt":
        raise FirstOpenOneDriveError(
            "P3-D2 requires Windows"
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
        raise FirstOpenOneDriveError(
            "cannot inspect Obsidian process state: "
            + completed.stderr.decode(
                "utf-8",
                errors="replace",
            ).strip()
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


def _repository_payload(
    repo_root: Path,
) -> dict[str, str]:
    state = repository_state(repo_root)
    return {
        "branch": state.branch,
        "head": state.head,
        "status_porcelain": state.status_porcelain,
    }


def _top_level_names(root: Path) -> list[str]:
    try:
        return sorted(
            path.name
            for path in root.iterdir()
        )
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"cannot list Vault root: {exc}"
        ) from exc


def _get_file_attributes(path: Path) -> int:
    if os.name != "nt":
        raise FirstOpenOneDriveError(
            "native filesystem gate requires Windows"
        )

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )
    get_attrs = kernel32.GetFileAttributesW
    get_attrs.argtypes = [ctypes.c_wchar_p]
    get_attrs.restype = ctypes.c_uint32

    attrs = int(get_attrs(str(path)))
    if attrs == INVALID_FILE_ATTRIBUTES:
        error = ctypes.get_last_error()
        raise FirstOpenOneDriveError(
            f"GetFileAttributesW failed for {path}: "
            f"winerror={error}"
        )
    return attrs


def _native_reparse_tag(path: Path) -> int | None:
    attrs = _get_file_attributes(path)
    if not (attrs & FILE_ATTRIBUTE_REPARSE_POINT):
        return None

    kernel32 = ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )

    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        ctypes.c_wchar_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    create_file.restype = ctypes.c_void_p

    handle = create_file(
        str(path),
        0,
        (
            FILE_SHARE_READ
            | FILE_SHARE_WRITE
            | FILE_SHARE_DELETE
        ),
        None,
        OPEN_EXISTING,
        (
            FILE_FLAG_OPEN_REPARSE_POINT
            | FILE_FLAG_BACKUP_SEMANTICS
        ),
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        raise FirstOpenOneDriveError(
            f"CreateFileW reparse open failed for {path}: "
            f"winerror={error}"
        )

    try:
        device_io = kernel32.DeviceIoControl
        device_io.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.c_void_p,
        ]
        device_io.restype = ctypes.c_int

        buffer = ctypes.create_string_buffer(
            16 * 1024
        )
        returned = ctypes.c_uint32(0)

        ok = device_io(
            handle,
            FSCTL_GET_REPARSE_POINT,
            None,
            0,
            buffer,
            len(buffer),
            ctypes.byref(returned),
            None,
        )
        if not ok:
            error = ctypes.get_last_error()
            raise FirstOpenOneDriveError(
                f"FSCTL_GET_REPARSE_POINT failed "
                f"for {path}: winerror={error}"
            )
        if returned.value < 8:
            raise FirstOpenOneDriveError(
                f"reparse payload too short for {path}"
            )

        return int.from_bytes(
            buffer.raw[:4],
            "little",
            signed=False,
        )
    finally:
        kernel32.CloseHandle(
            ctypes.c_void_p(handle)
        )


def _assert_safe_directory(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        raise FirstOpenOneDriveError(
            f"directory missing: {path}"
        )

    attrs = _get_file_attributes(path)
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
        tag = _native_reparse_tag(path)
        raise FirstOpenOneDriveError(
            f"directory reparse point forbidden: "
            f"{path} tag=0x{int(tag or 0):08X}"
        )


def _file_native_state(
    path: Path,
) -> dict[str, Any]:
    attrs = _get_file_attributes(path)

    if attrs & FILE_ATTRIBUTE_OFFLINE:
        raise FirstOpenOneDriveError(
            f"offline file forbidden: {path}"
        )
    if attrs & FILE_ATTRIBUTE_SPARSE_FILE:
        raise FirstOpenOneDriveError(
            f"sparse file forbidden: {path}"
        )

    tag = _native_reparse_tag(path)
    if tag in (SYMLINK_TAG, MOUNT_POINT_TAG):
        raise FirstOpenOneDriveError(
            f"link/mount reparse tag forbidden: {path}"
        )
    if tag not in (None, CLOUD_6_TAG):
        raise FirstOpenOneDriveError(
            f"unexpected reparse tag for {path}: "
            f"0x{tag:08X}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"cannot stat file: {path}: {exc}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise FirstOpenOneDriveError(
            f"non-regular file forbidden: {path}"
        )

    link_count = getattr(info, "st_nlink", None)
    if link_count is None or int(link_count) != 1:
        raise FirstOpenOneDriveError(
            f"unexpected hard-link count for {path}: "
            f"{link_count}"
        )

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"unreadable file: {path}: {exc}"
        ) from exc

    return {
        "class":
            (
                "NO_REPARSE_POINT"
                if tag is None
                else "IO_REPARSE_TAG_CLOUD_6"
            ),
        "tag_hex":
            (
                None
                if tag is None
                else f"0x{tag:08X}"
            ),
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def _assert_directory_tree_safe(vault: Path) -> None:
    _assert_safe_directory(vault)

    for current, directories, _files in os.walk(
        vault,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current)
        _assert_safe_directory(current_path)

        for name in list(directories):
            _assert_safe_directory(
                current_path / name
            )


def _views_entry_count(vault: Path) -> int:
    views = vault / "views"
    _assert_safe_directory(views)
    try:
        return sum(1 for _ in views.iterdir())
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"cannot inspect views: {exc}"
        ) from exc


def _generated_state(
    vault: Path,
) -> tuple[
    dict[str, tuple[int, str]],
    dict[str, Any],
]:
    generated = vault / "generated"
    _assert_safe_directory(generated)

    result: dict[str, tuple[int, str]] = {}
    classes = {
        "NO_REPARSE_POINT": 0,
        "IO_REPARSE_TAG_CLOUD_6": 0,
    }

    for current, directories, files in os.walk(
        generated,
        topdown=True,
        followlinks=False,
    ):
        current_path = Path(current)
        _assert_safe_directory(current_path)

        for name in list(directories):
            _assert_safe_directory(
                current_path / name
            )

        for name in files:
            path = current_path / name
            state = _file_native_state(path)
            relative = path.relative_to(
                vault
            ).as_posix()
            result[relative] = (
                int(state["size_bytes"]),
                str(state["sha256"]),
            )
            classes[
                str(state["class"])
            ] += 1

    ordered = dict(
        sorted(
            result.items(),
            key=lambda item:
                item[0].encode("utf-8"),
        )
    )

    summary = {
        "generated_file_count": len(ordered),
        "no_reparse_point_count":
            classes["NO_REPARSE_POINT"],
        "cloud_6_count":
            classes[
                "IO_REPARSE_TAG_CLOUD_6"
            ],
        "allowed_classes": [
            "NO_REPARSE_POINT",
            "IO_REPARSE_TAG_CLOUD_6:0x9000601A",
        ],
        "offline_files": 0,
        "sparse_files": 0,
        "unreadable_files": 0,
        "directory_reparse_points": 0,
        "symlink_or_junction_files": 0,
    }

    return ordered, summary


def _projection_tree_digest_from_map(
    digest_map: Mapping[
        str,
        tuple[int, str],
    ],
) -> str:
    entries = [
        [
            relative,
            sha256,
            size_bytes,
        ]
        for relative, (
            size_bytes,
            sha256,
        ) in sorted(
            digest_map.items(),
            key=lambda item:
                item[0].encode("utf-8"),
        )
        if relative != (
            "generated/manifests/"
            "build-manifest.json"
        )
    ]

    return hashlib.sha256(
        _canonical_json_bytes(entries)
    ).hexdigest()


def _manifest_sha256_from_map(
    digest_map: Mapping[
        str,
        tuple[int, str],
    ],
) -> str:
    key = (
        "generated/manifests/"
        "integrity-manifest.json"
    )
    if key not in digest_map:
        raise FirstOpenOneDriveError(
            "integrity manifest missing"
        )
    return digest_map[key][1]


def _build_manifest_sha256_from_map(
    digest_map: Mapping[
        str,
        tuple[int, str],
    ],
) -> str:
    key = (
        "generated/manifests/"
        "build-manifest.json"
    )
    if key not in digest_map:
        raise FirstOpenOneDriveError(
            "build manifest missing"
        )
    return digest_map[key][1]


def _fresh_p2_and_compare(
    repo_root: Path,
    vault: Path,
) -> tuple[
    dict[str, Any],
    Path,
    dict[str, tuple[int, str]],
    dict[str, Any],
]:
    try:
        report = build_p2_report(
            repo_root
        )
        build_a = validate_fresh_p2_report(
            report
        )
    except Exception as exc:
        raise FirstOpenOneDriveError(
            f"fresh qualified P2 reconstruction "
            f"failed: {exc}"
        ) from exc

    fresh_map = qualified_temp_digest_map(
        build_a
    )
    vault_map, summary = (
        _generated_state(vault)
    )

    if fresh_map != vault_map:
        raise FirstOpenOneDriveError(
            "current OneDrive Vault generated "
            "tree differs from fresh qualified "
            "P2 BUILD A"
        )

    if len(vault_map) != EXPECTED_GENERATED_COUNT:
        raise FirstOpenOneDriveError(
            "generated file count != 92"
        )

    tree_digest = (
        _projection_tree_digest_from_map(
            vault_map
        )
    )
    if tree_digest != EXPECTED_TREE_DIGEST:
        raise FirstOpenOneDriveError(
            "qualified projection-tree digest mismatch"
        )
    if tree_digest != report.get(
        "projection_tree_digest_sha256"
    ):
        raise FirstOpenOneDriveError(
            "current projection-tree digest "
            "differs from fresh P2"
        )

    if (
        _manifest_sha256_from_map(
            vault_map
        )
        != EXPECTED_INTEGRITY_MANIFEST_SHA256
    ):
        raise FirstOpenOneDriveError(
            "qualified integrity-manifest "
            "SHA-256 mismatch"
        )

    return (
        report,
        build_a,
        vault_map,
        summary,
    )


def _assert_pre_open_vault(
    vault: Path,
) -> FilesystemIdentity:
    if not vault.exists() or not vault.is_dir():
        raise FirstOpenOneDriveError(
            f"materialized Vault missing: {vault}"
        )

    _assert_directory_tree_safe(vault)

    if _top_level_names(vault) != [
        "generated",
        "views",
    ]:
        raise FirstOpenOneDriveError(
            "pre-open Vault top-level entries "
            "must be exactly generated and views"
        )
    if (vault / ".obsidian").exists():
        raise FirstOpenOneDriveError(
            ".obsidian already exists before first open"
        )
    if (vault / ".git").exists():
        raise FirstOpenOneDriveError(
            ".git is forbidden inside the Vault"
        )
    if _views_entry_count(vault) != 0:
        raise FirstOpenOneDriveError(
            "views must be empty before first open"
        )

    return filesystem_identity(vault)


def _generated_snapshot_fields(
    digest_map: Mapping[
        str,
        tuple[int, str],
    ],
) -> tuple[
    list[str],
    dict[str, int],
    dict[str, str],
]:
    paths = list(digest_map.keys())
    sizes = {
        path: digest_map[path][0]
        for path in paths
    }
    hashes = {
        path: digest_map[path][1]
        for path in paths
    }
    return paths, sizes, hashes


def _generated_map_from_snapshot(
    payload: Mapping[str, Any],
) -> dict[str, tuple[int, str]]:
    paths = payload.get(
        "generated_relative_path_set"
    )
    sizes = payload.get(
        "generated_file_sizes"
    )
    hashes = payload.get(
        "generated_file_sha256"
    )

    if (
        not isinstance(paths, list)
        or not all(
            isinstance(path, str)
            for path in paths
        )
        or len(paths) != len(set(paths))
        or paths != sorted(
            paths,
            key=lambda value:
                value.encode("utf-8"),
        )
    ):
        raise FirstOpenOneDriveError(
            "snapshot generated path set invalid"
        )
    if not isinstance(sizes, dict):
        raise FirstOpenOneDriveError(
            "snapshot generated sizes invalid"
        )
    if not isinstance(hashes, dict):
        raise FirstOpenOneDriveError(
            "snapshot generated hashes invalid"
        )
    if (
        set(paths) != set(sizes)
        or set(paths) != set(hashes)
    ):
        raise FirstOpenOneDriveError(
            "snapshot generated metadata key mismatch"
        )

    result: dict[str, tuple[int, str]] = {}
    for path in paths:
        size = sizes[path]
        digest = hashes[path]
        if (
            not isinstance(size, int)
            or size < 0
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(
                char
                not in "0123456789abcdef"
                for char in digest.lower()
            )
        ):
            raise FirstOpenOneDriveError(
                "snapshot generated metadata invalid"
            )
        result[path] = (
            size,
            digest.lower(),
        )
    return result


def _snapshot_envelope(
    payload: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    digest = hashlib.sha256(
        _canonical_json_bytes(payload)
    ).hexdigest()
    return (
        {
            "schema": SNAPSHOT_SCHEMA,
            "payload_sha256": digest,
            "payload": dict(payload),
        },
        digest,
    )


def _write_snapshot(
    envelope: Mapping[str, Any],
    digest: str,
) -> Path:
    root = Path(
        tempfile.mkdtemp(
            prefix=(
                "ATDS-OBSIDIAN-FIRST-OPEN-"
                "ONEDRIVE-"
            )
        )
    )
    path = root / (
        "first-open-onedrive-snapshot-"
        f"{digest}.json"
    )

    raw = (
        json.dumps(
            envelope,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")

    try:
        with path.open("xb") as handle:
            handle.write(raw)
    except OSError as exc:
        raise FirstOpenOneDriveError(
            f"cannot persist external snapshot: {exc}"
        ) from exc

    return path


def _load_snapshot(
    snapshot_path: Path,
) -> tuple[dict[str, Any], str]:
    temp_root = Path(
        tempfile.gettempdir()
    ).absolute()
    snapshot = snapshot_path.absolute()

    try:
        inside_temp = (
            os.path.commonpath(
                [
                    os.path.normcase(
                        os.path.abspath(
                            str(snapshot)
                        )
                    ),
                    os.path.normcase(
                        os.path.abspath(
                            str(temp_root)
                        )
                    ),
                ]
            )
            == os.path.normcase(
                os.path.abspath(
                    str(temp_root)
                )
            )
        )
    except ValueError:
        inside_temp = False

    if not inside_temp:
        raise FirstOpenOneDriveError(
            "snapshot must be stored under OS TEMP"
        )
    if not snapshot.exists() or not snapshot.is_file():
        raise FirstOpenOneDriveError(
            "snapshot file missing"
        )
    if (
        _get_file_attributes(snapshot)
        & FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise FirstOpenOneDriveError(
            "snapshot reparse point forbidden"
        )

    envelope = _load_json(snapshot)
    if envelope.get("schema") != SNAPSHOT_SCHEMA:
        raise FirstOpenOneDriveError(
            "unexpected snapshot schema"
        )

    payload = envelope.get("payload")
    digest = envelope.get("payload_sha256")
    if not isinstance(payload, dict):
        raise FirstOpenOneDriveError(
            "snapshot payload missing"
        )
    if not isinstance(digest, str):
        raise FirstOpenOneDriveError(
            "snapshot digest missing"
        )

    actual = hashlib.sha256(
        _canonical_json_bytes(payload)
    ).hexdigest()
    if digest != actual:
        raise FirstOpenOneDriveError(
            "snapshot payload digest mismatch"
        )

    expected_name = (
        "first-open-onedrive-snapshot-"
        f"{digest}.json"
    )
    if snapshot.name != expected_name:
        raise FirstOpenOneDriveError(
            "snapshot filename/digest binding mismatch"
        )

    return payload, digest


def _identity_from_payload(
    value: object,
) -> FilesystemIdentity:
    if not isinstance(value, dict):
        raise FirstOpenOneDriveError(
            "snapshot Vault identity missing"
        )

    try:
        return FilesystemIdentity(
            volume_serial=int(
                value["volume_serial"]
            ),
            file_identity=int(
                value["file_identity"]
            ),
            filesystem=str(
                value["filesystem"]
            ),
        )
    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise FirstOpenOneDriveError(
            "snapshot Vault identity invalid"
        ) from exc


def _validate_obsidian_json_file(
    path: Path,
) -> object:
    state = _file_native_state(path)

    if path.suffix.casefold() != ".json":
        raise FirstOpenOneDriveError(
            f"non-JSON .obsidian root file "
            f"forbidden: {path.name}"
        )

    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise FirstOpenOneDriveError(
            f"invalid .obsidian JSON file: "
            f"{path.name}: {exc}"
        ) from exc

    if state["class"] not in (
        "NO_REPARSE_POINT",
        "IO_REPARSE_TAG_CLOUD_6",
    ):
        raise FirstOpenOneDriveError(
            "unexpected .obsidian file class"
        )

    return value


def _verify_obsidian_directory(
    vault: Path,
) -> dict[str, Any]:
    obsidian = vault / ".obsidian"
    _assert_safe_directory(obsidian)

    files: list[str] = []
    class_counts = {
        "NO_REPARSE_POINT": 0,
        "IO_REPARSE_TAG_CLOUD_6": 0,
    }

    for entry in obsidian.iterdir():
        if entry.is_dir():
            raise FirstOpenOneDriveError(
                f".obsidian subdirectory forbidden: "
                f"{entry.name}"
            )
        if not entry.is_file():
            raise FirstOpenOneDriveError(
                f".obsidian non-regular entry "
                f"forbidden: {entry.name}"
            )

        state = _file_native_state(entry)
        class_counts[
            str(state["class"])
        ] += 1

        name_casefold = entry.name.casefold()

        if (
            "sync" in name_casefold
            and name_casefold
            != "core-plugins.json"
        ):
            raise FirstOpenOneDriveError(
                f"explicit Obsidian Sync artifact "
                f"forbidden: {entry.name}"
            )

        parsed = _validate_obsidian_json_file(
            entry
        )
        files.append(entry.name)

        if name_casefold == (
            "community-plugins.json"
        ):
            if (
                not isinstance(parsed, list)
                or parsed
            ):
                raise FirstOpenOneDriveError(
                    "community-plugins.json must be []"
                )

        if name_casefold == "core-plugins.json":
            if isinstance(parsed, list):
                if not all(
                    isinstance(item, str)
                    for item in parsed
                ):
                    raise FirstOpenOneDriveError(
                        "core-plugins.json list "
                        "shape invalid"
                    )
                if any(
                    item.casefold() == "sync"
                    for item in parsed
                ):
                    raise FirstOpenOneDriveError(
                        "Obsidian Sync core plugin enabled"
                    )
            elif isinstance(parsed, dict):
                if not all(
                    isinstance(key, str)
                    and isinstance(enabled, bool)
                    for key, enabled
                    in parsed.items()
                ):
                    raise FirstOpenOneDriveError(
                        "core-plugins.json object "
                        "shape invalid"
                    )
                if any(
                    key.casefold() == "sync"
                    and enabled
                    for key, enabled
                    in parsed.items()
                ):
                    raise FirstOpenOneDriveError(
                        "Obsidian Sync core plugin enabled"
                    )
            else:
                raise FirstOpenOneDriveError(
                    "core-plugins.json shape "
                    "cannot be interpreted"
                )

    return {
        "directory_present": True,
        "root_json_files": sorted(files),
        "community_plugins_enabled": False,
        "obsidian_sync_enabled": False,
        "subdirectory_count": 0,
        "file_reparse_class_counts":
            class_counts,
    }


def prepare_first_open(
    repo_root: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    contract, _ = verify_harness_dependencies(
        package_dir
    )

    if _obsidian_running():
        raise FirstOpenOneDriveError(
            "Obsidian must be closed before prepare"
        )

    repo_root = repo_root.resolve()
    repo_before = _repository_payload(
        repo_root
    )

    vault = Path(
        str(
            contract["materialized_vault"][
                "observed_resolved_path"
            ]
        )
    )
    if str(vault) != EXPECTED_VAULT:
        raise FirstOpenOneDriveError(
            "runtime Vault path mismatch"
        )

    vault_identity = _assert_pre_open_vault(
        vault
    )

    (
        p2_report,
        _build_a,
        vault_map,
        reparse_summary,
    ) = _fresh_p2_and_compare(
        repo_root,
        vault,
    )

    if _repository_payload(
        repo_root
    ) != repo_before:
        raise FirstOpenOneDriveError(
            "ATDS repository changed during "
            "pre-open reconstruction"
        )

    paths, sizes, hashes = (
        _generated_snapshot_fields(
            vault_map
        )
    )

    payload = {
        "contract_schema":
            contract["schema"],
        "qualified_p3b_head":
            QUALIFIED_P3B_HEAD,
        "qualified_p2b_head":
            QUALIFIED_P2B_HEAD,
        "vault_resolved_path":
            str(vault),
        "vault_filesystem_identity":
            vault_identity.to_dict(),
        "generated_relative_path_set":
            paths,
        "generated_file_sizes":
            sizes,
        "generated_file_sha256":
            hashes,
        "generated_tree_digest_sha256":
            _projection_tree_digest_from_map(
                vault_map
            ),
        "integrity_manifest_sha256":
            _manifest_sha256_from_map(
                vault_map
            ),
        "build_manifest_sha256":
            _build_manifest_sha256_from_map(
                vault_map
            ),
        "generated_reparse_policy_summary":
            reparse_summary,
        "views_entry_count":
            _views_entry_count(vault),
        "obsidian_directory_present":
            (vault / ".obsidian").exists(),
        "vault_top_level_entries":
            _top_level_names(vault),
        "repository_branch":
            repo_before["branch"],
        "repository_head":
            repo_before["head"],
        "repository_status_porcelain":
            repo_before["status_porcelain"],
        "fresh_p2_identity": {
            "repository":
                p2_report["repository"],
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
                p2_report[
                    "projection_tree_digest_sha256"
                ],
            "artifact_record_count":
                p2_report[
                    "artifact_record_count"
                ],
            "relation_record_count":
                p2_report[
                    "relation_record_count"
                ],
            "generated_file_count":
                p2_report[
                    "generated_file_count"
                ],
        },
        "phase":
            "PREPARED_FOR_MANUAL_FIRST_OPEN_ONEDRIVE",
    }

    envelope, digest = _snapshot_envelope(
        payload
    )
    snapshot_path = _write_snapshot(
        envelope,
        digest,
    )

    return {
        "schema": PREPARE_REPORT_SCHEMA,
        "status": "PASS",
        "first_open_authorized": True,
        "automatic_obsidian_launch": False,
        "vault_modified": False,
        "obsidian_config_created": False,
        "obsidian_sync_enabled": False,
        "snapshot_path": str(snapshot_path),
        "authorization_token": digest,
        "vault_resolved_path": str(vault),
        "generated_file_count":
            len(vault_map),
        "generated_reparse_policy_summary":
            reparse_summary,
        "projection_tree_digest_sha256":
            payload[
                "generated_tree_digest_sha256"
            ],
        "instruction":
            (
                "Manually open this exact OneDrive Vault "
                "in Obsidian, make no edits, enable no "
                "plugins or Sync, then fully close "
                "Obsidian before verify-first-open."
            ),
    }


def verify_first_open(
    repo_root: Path,
    snapshot_path: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    contract, _ = verify_harness_dependencies(
        package_dir
    )

    if _obsidian_running():
        raise FirstOpenOneDriveError(
            "Obsidian is still running; close it fully "
            "before post-check"
        )

    payload, token = _load_snapshot(
        snapshot_path
    )

    if payload.get(
        "contract_schema"
    ) != contract.get("schema"):
        raise FirstOpenOneDriveError(
            "snapshot contract schema mismatch"
        )
    if payload.get(
        "qualified_p3b_head"
    ) != QUALIFIED_P3B_HEAD:
        raise FirstOpenOneDriveError(
            "snapshot P3-B identity mismatch"
        )
    if payload.get(
        "qualified_p2b_head"
    ) != QUALIFIED_P2B_HEAD:
        raise FirstOpenOneDriveError(
            "snapshot P2-B identity mismatch"
        )

    repo_root = repo_root.resolve()
    current_repo = _repository_payload(
        repo_root
    )

    snapshot_repo = {
        "branch":
            payload.get(
                "repository_branch"
            ),
        "head":
            payload.get(
                "repository_head"
            ),
        "status_porcelain":
            payload.get(
                "repository_status_porcelain"
            ),
    }
    if current_repo != snapshot_repo:
        raise FirstOpenOneDriveError(
            "ATDS repository state changed "
            "since prepare"
        )

    vault = Path(
        str(
            contract["materialized_vault"][
                "observed_resolved_path"
            ]
        )
    )
    if str(vault) != payload.get(
        "vault_resolved_path"
    ):
        raise FirstOpenOneDriveError(
            "snapshot Vault path mismatch"
        )
    if not vault.exists() or not vault.is_dir():
        raise FirstOpenOneDriveError(
            "Vault missing during post-check"
        )

    current_identity = filesystem_identity(
        vault
    )
    if current_identity != _identity_from_payload(
        payload.get(
            "vault_filesystem_identity"
        )
    ):
        raise FirstOpenOneDriveError(
            "Vault filesystem identity changed"
        )

    _assert_directory_tree_safe(vault)

    if _top_level_names(vault) != [
        ".obsidian",
        "generated",
        "views",
    ]:
        raise FirstOpenOneDriveError(
            "post-open Vault top-level entries invalid"
        )
    if (vault / ".git").exists():
        raise FirstOpenOneDriveError(
            ".git is forbidden inside the Vault"
        )
    if _views_entry_count(vault) != 0:
        raise FirstOpenOneDriveError(
            "views changed during first open"
        )

    snapshot_generated = (
        _generated_map_from_snapshot(
            payload
        )
    )
    current_generated, reparse_summary = (
        _generated_state(vault)
    )

    if current_generated != snapshot_generated:
        raise FirstOpenOneDriveError(
            "generated bytes changed since prepare"
        )
    if (
        _manifest_sha256_from_map(
            current_generated
        )
        != payload.get(
            "integrity_manifest_sha256"
        )
    ):
        raise FirstOpenOneDriveError(
            "integrity-manifest bytes changed"
        )
    if (
        _build_manifest_sha256_from_map(
            current_generated
        )
        != payload.get(
            "build_manifest_sha256"
        )
    ):
        raise FirstOpenOneDriveError(
            "build-manifest bytes changed"
        )

    current_tree_digest = (
        _projection_tree_digest_from_map(
            current_generated
        )
    )
    if current_tree_digest != payload.get(
        "generated_tree_digest_sha256"
    ):
        raise FirstOpenOneDriveError(
            "generated projection-tree "
            "digest changed"
        )

    (
        p2_report,
        fresh_build_a,
        fresh_current_map,
        _fresh_reparse_summary,
    ) = _fresh_p2_and_compare(
        repo_root,
        vault,
    )

    if fresh_current_map != snapshot_generated:
        raise FirstOpenOneDriveError(
            "snapshot/generated state no longer "
            "equals fresh qualified P2 BUILD A"
        )
    if (
        qualified_temp_digest_map(
            fresh_build_a
        )
        != snapshot_generated
    ):
        raise FirstOpenOneDriveError(
            "fresh P2 BUILD A no longer "
            "equals snapshot"
        )

    fresh_identity = payload.get(
        "fresh_p2_identity"
    )
    if not isinstance(
        fresh_identity,
        dict,
    ):
        raise FirstOpenOneDriveError(
            "snapshot fresh P2 identity missing"
        )

    identity_fields = (
        "repository",
        "source_commit",
        "source_tree",
        "semantic_record_digest_sha256",
        "artifact_set_digest_sha256",
        "relation_set_digest_sha256",
        "integrity_manifest_sha256",
        "projection_tree_digest_sha256",
        "artifact_record_count",
        "relation_record_count",
        "generated_file_count",
    )
    for field in identity_fields:
        if p2_report.get(
            field
        ) != fresh_identity.get(field):
            raise FirstOpenOneDriveError(
                f"fresh P2 identity changed: {field}"
            )

    obsidian_state = (
        _verify_obsidian_directory(
            vault
        )
    )

    if _repository_payload(
        repo_root
    ) != snapshot_repo:
        raise FirstOpenOneDriveError(
            "ATDS repository changed "
            "during post-check"
        )

    return {
        "schema": VERIFY_REPORT_SCHEMA,
        "status": "PASS",
        "first_open_qualified": True,
        "vault_resolved_path":
            str(vault),
        "snapshot_authorization_token":
            token,
        "generated_file_count":
            len(current_generated),
        "projection_tree_digest_sha256":
            current_tree_digest,
        "generated_reparse_policy_summary":
            reparse_summary,
        "views_entry_count": 0,
        "obsidian_state":
            obsidian_state,
        "automatic_obsidian_launch":
            False,
        "vault_written_by_harness":
            False,
        "generated_modified_by_harness":
            False,
        "views_modified_by_harness":
            False,
        "obsidian_sync_enabled":
            False,
        "community_plugins_enabled":
            False,
        "repository_state_preserved":
            True,
    }

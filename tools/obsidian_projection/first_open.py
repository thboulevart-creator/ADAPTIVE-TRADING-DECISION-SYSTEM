from __future__ import annotations

import csv
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
from .integrity import (
    _is_reparse_or_link,
    projection_tree_digest,
    sha256_bytes,
    verify_integrity_manifest,
)
from .materialize import (
    EXPECTED_FINAL_NAME,
    EXPECTED_REPOSITORY,
    FilesystemIdentity,
    MaterializationError,
    _assert_build_manifest_identity,
    _assert_regular_single_link,
    _assert_tree_no_aliases,
    _digest_map,
    _norm,
    filesystem_identity,
    repository_state,
    validate_fresh_p2_report,
    verify_p2_core_blobs,
)
from .p2_verify import build_report as build_p2_report


QUALIFIED_P3B_HEAD = (
    "bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba"
)
FIRST_OPEN_CONTRACT_BLOB = (
    "5cd11e9512249da26adf4b6f86e79259af725809"
)
MATERIALIZATION_CONTRACT_BLOB = (
    "b11120c9f6d3ee68b253928b125747159536bbf0"
)
QUALIFIED_MATERIALIZE_HELPER_BLOB = (
    "9c4c925f59200c11054d08f16dfca38820d6f9ac"
)
SNAPSHOT_SCHEMA = (
    "ATDS_OBSIDIAN_FIRST_OPEN_SNAPSHOT_V0_1"
)
PREPARE_REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P3D_PREPARE_REPORT_V0_1"
)
VERIFY_REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P3D_VERIFY_REPORT_V0_1"
)


class FirstOpenError(RuntimeError):
    """Raised when first-open safety must fail closed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise FirstOpenError(
            f"cannot load JSON: {path}: {exc}"
        ) from exc

    if not isinstance(value, dict):
        raise FirstOpenError(
            f"JSON object required: {path}"
        )
    return value


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _verify_blob(
    path: Path,
    expected_oid: str,
    label: str,
) -> None:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FirstOpenError(
            f"cannot read pinned {label}: {path}: {exc}"
        ) from exc

    actual_oid = git_blob_oid(raw)
    if actual_oid != expected_oid:
        raise FirstOpenError(
            f"{label} blob mismatch: "
            f"expected={expected_oid} actual={actual_oid}"
        )


def verify_harness_dependencies(
    package_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    first_open_contract_path = (
        package_dir
        / "first_open_safety_contract_v0_1.json"
    )
    materialization_contract_path = (
        package_dir
        / "materialization_contract_v0_1.json"
    )
    materialize_helper_path = (
        package_dir / "materialize.py"
    )

    _verify_blob(
        first_open_contract_path,
        FIRST_OPEN_CONTRACT_BLOB,
        "P3-C first-open contract",
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

    first_open_contract = _load_json(
        first_open_contract_path
    )
    materialization_contract = _load_json(
        materialization_contract_path
    )

    if first_open_contract.get(
        "qualified_p3b_head"
    ) != QUALIFIED_P3B_HEAD:
        raise FirstOpenError(
            "P3-C contract P3-B binding mismatch"
        )

    try:
        verify_p2_core_blobs(
            package_dir,
            materialization_contract,
        )
    except MaterializationError as exc:
        raise FirstOpenError(
            str(exc)
        ) from exc

    return (
        first_open_contract,
        materialization_contract,
    )


def _obsidian_running() -> bool:
    if os.name != "nt":
        raise FirstOpenError(
            "first-open harness requires Windows"
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
        stderr = completed.stderr.decode(
            "utf-8",
            errors="replace",
        ).strip()
        raise FirstOpenError(
            f"cannot inspect Obsidian process state: {stderr}"
        )

    text = completed.stdout.decode(
        "utf-8",
        errors="replace",
    )
    reader = csv.reader(io.StringIO(text))

    for row in reader:
        if not row:
            continue
        image = row[0].strip().strip('"')
        if image.casefold() == "obsidian.exe":
            return True

    return False


def _expected_vault_path(
    contract: Mapping[str, Any],
) -> Path:
    if os.name != "nt":
        raise FirstOpenError(
            "first-open harness requires Windows"
        )

    expected_raw = contract[
        "materialized_vault"
    ].get("observed_resolved_path")

    if not isinstance(
        expected_raw,
        str,
    ) or not expected_raw:
        raise FirstOpenError(
            "contractual Vault path missing"
        )

    expected = Path(
        expected_raw
    )

    if not expected.is_absolute():
        raise FirstOpenError(
            "contractual Vault path must be absolute"
        )

    if expected.name != EXPECTED_FINAL_NAME:
        raise FirstOpenError(
            "contractual Vault final name mismatch"
        )

    # The P3-C contract blob is pinned before this function
    # is used.  Therefore its exact observed_resolved_path is
    # the authority for first-open verification.  Do not derive
    # the path from LOCALAPPDATA here: Microsoft Store / MSIX
    # Python may expose a virtualized LOCALAPPDATA pointing into
    # Packages/.../LocalCache/Local even when the qualified P3-B
    # Vault exists at the host path recorded by the contract.
    return expected.resolve(strict=False)


def _top_level_names(root: Path) -> list[str]:
    try:
        return sorted(
            path.name
            for path in root.iterdir()
        )
    except OSError as exc:
        raise FirstOpenError(
            f"cannot list Vault root: {exc}"
        ) from exc


def _views_entry_count(vault: Path) -> int:
    views = vault / "views"
    if not views.exists() or not views.is_dir():
        raise FirstOpenError(
            "views directory missing"
        )
    if _is_reparse_or_link(views):
        raise FirstOpenError(
            "views may not be reparse/symlink/junction"
        )
    try:
        return sum(1 for _ in views.iterdir())
    except OSError as exc:
        raise FirstOpenError(
            f"cannot inspect views: {exc}"
        ) from exc


def _generated_entries(
    root: Path,
) -> list[dict[str, object]]:
    digests = _digest_map(root)
    return [
        {
            "relative_path": relative,
            "size_bytes": size_sha[0],
            "sha256": size_sha[1],
        }
        for relative, size_sha in sorted(
            digests.items(),
            key=lambda item: item[0].encode("utf-8"),
        )
    ]


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
            key=lambda value: value.encode("utf-8"),
        )
    ):
        raise FirstOpenError(
            "snapshot generated_relative_path_set invalid"
        )

    if not isinstance(sizes, dict):
        raise FirstOpenError(
            "snapshot generated_file_sizes invalid"
        )
    if not isinstance(hashes, dict):
        raise FirstOpenError(
            "snapshot generated_file_sha256 invalid"
        )

    if set(paths) != set(sizes) or set(paths) != set(hashes):
        raise FirstOpenError(
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
                char not in "0123456789abcdef"
                for char in digest.lower()
            )
        ):
            raise FirstOpenError(
                "snapshot generated file metadata invalid"
            )
        result[path] = (size, digest)

    return result


def _manifest_sha256(vault: Path) -> str:
    path = (
        vault
        / "generated"
        / "manifests"
        / "integrity-manifest.json"
    )
    _assert_regular_single_link(path)
    return sha256_bytes(path.read_bytes())


def _build_manifest_sha256(vault: Path) -> str:
    path = (
        vault
        / "generated"
        / "manifests"
        / "build-manifest.json"
    )
    _assert_regular_single_link(path)
    return sha256_bytes(path.read_bytes())


def _fresh_p2_and_compare(
    repo_root: Path,
    vault: Path,
) -> tuple[dict[str, Any], Path]:
    try:
        report = build_p2_report(
            repo_root
        )
        build_a = validate_fresh_p2_report(
            report
        )
    except Exception as exc:
        raise FirstOpenError(
            f"fresh qualified P2 reconstruction failed: {exc}"
        ) from exc

    fresh_map = _digest_map(build_a)
    vault_map = _digest_map(vault)

    if fresh_map != vault_map:
        raise FirstOpenError(
            "current Vault generated tree differs "
            "from fresh qualified P2 BUILD A"
        )

    statuses = verify_integrity_manifest(
        vault
    )
    if any(
        status != "CLEAN"
        for status in statuses.values()
    ):
        raise FirstOpenError(
            "current Vault integrity manifest is not all CLEAN"
        )

    try:
        _assert_build_manifest_identity(
            vault,
            report,
        )
    except MaterializationError as exc:
        raise FirstOpenError(
            str(exc)
        ) from exc

    tree_digest = projection_tree_digest(
        vault
    )
    if tree_digest != report[
        "projection_tree_digest_sha256"
    ]:
        raise FirstOpenError(
            "current Vault projection-tree digest "
            "differs from fresh P2"
        )

    return report, build_a


def _assert_pre_open_vault(
    vault: Path,
) -> FilesystemIdentity:
    if not vault.exists() or not vault.is_dir():
        raise FirstOpenError(
            f"materialized Vault missing: {vault}"
        )

    try:
        _assert_tree_no_aliases(vault)
    except MaterializationError as exc:
        raise FirstOpenError(
            str(exc)
        ) from exc

    if _top_level_names(vault) != [
        "generated",
        "views",
    ]:
        raise FirstOpenError(
            "pre-open Vault top-level entries must be "
            "exactly generated and views"
        )

    if (vault / ".obsidian").exists():
        raise FirstOpenError(
            ".obsidian already exists before first open"
        )

    if (vault / ".git").exists():
        raise FirstOpenError(
            ".git is forbidden inside the Vault"
        )

    if _views_entry_count(vault) != 0:
        raise FirstOpenError(
            "views must be empty before first open"
        )

    return filesystem_identity(vault)


def _repository_payload(
    repo_root: Path,
) -> dict[str, str]:
    state = repository_state(repo_root)
    return {
        "branch": state.branch,
        "head": state.head,
        "status_porcelain": state.status_porcelain,
    }


def _snapshot_envelope(
    payload: Mapping[str, Any],
) -> tuple[dict[str, Any], str]:
    payload_bytes = _canonical_json_bytes(
        payload
    )
    digest = hashlib.sha256(
        payload_bytes
    ).hexdigest()

    envelope = {
        "schema": SNAPSHOT_SCHEMA,
        "payload_sha256": digest,
        "payload": dict(payload),
    }
    return envelope, digest


def _write_snapshot(
    envelope: Mapping[str, Any],
    digest: str,
) -> Path:
    root = Path(
        tempfile.mkdtemp(
            prefix="ATDS-OBSIDIAN-FIRST-OPEN-"
        )
    )
    path = root / (
        f"first-open-snapshot-{digest}.json"
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
        raise FirstOpenError(
            f"cannot persist external snapshot: {exc}"
        ) from exc

    return path


def prepare_first_open(
    repo_root: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    first_open_contract, _ = (
        verify_harness_dependencies(
            package_dir
        )
    )

    if _obsidian_running():
        raise FirstOpenError(
            "Obsidian must be closed before prepare"
        )

    repo_root = repo_root.resolve()
    repo_before = _repository_payload(
        repo_root
    )

    vault = _expected_vault_path(
        first_open_contract
    )
    vault_identity = _assert_pre_open_vault(
        vault
    )

    p2_report, _build_a = (
        _fresh_p2_and_compare(
            repo_root,
            vault,
        )
    )

    repo_after_reconstruction = (
        _repository_payload(repo_root)
    )
    if repo_after_reconstruction != repo_before:
        raise FirstOpenError(
            "ATDS repository changed during pre-open reconstruction"
        )

    generated_entries = _generated_entries(
        vault
    )
    generated_paths = [
        str(item["relative_path"])
        for item in generated_entries
    ]
    generated_sizes = {
        str(item["relative_path"]):
            int(item["size_bytes"])
        for item in generated_entries
    }
    generated_hashes = {
        str(item["relative_path"]):
            str(item["sha256"])
        for item in generated_entries
    }

    payload = {
        "qualified_p3b_head":
            QUALIFIED_P3B_HEAD,
        "vault_resolved_path":
            str(vault),
        "vault_filesystem_identity":
            vault_identity.to_dict(),
        "generated_relative_path_set":
            generated_paths,
        "generated_file_sizes":
            generated_sizes,
        "generated_file_sha256":
            generated_hashes,
        "generated_tree_digest_sha256":
            projection_tree_digest(vault),
        "integrity_manifest_sha256":
            _manifest_sha256(vault),
        "build_manifest_sha256":
            _build_manifest_sha256(vault),
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
                p2_report["artifact_record_count"],
            "relation_record_count":
                p2_report["relation_record_count"],
            "generated_file_count":
                p2_report["generated_file_count"],
        },
        "phase": "PREPARED_FOR_MANUAL_FIRST_OPEN",
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
        "snapshot_path": str(snapshot_path),
        "authorization_token": digest,
        "vault_resolved_path": str(vault),
        "generated_file_count":
            len(
                payload[
                    "generated_relative_path_set"
                ]
            ),
        "projection_tree_digest_sha256":
            payload[
                "generated_tree_digest_sha256"
            ],
        "instruction":
            (
                "Manually open this exact Vault in Obsidian, "
                "make no edits, then fully close Obsidian "
                "before running verify-first-open."
            ),
    }


def _load_snapshot(
    snapshot_path: Path,
) -> tuple[dict[str, Any], str]:
    temp_root = Path(
        tempfile.gettempdir()
    ).resolve()
    resolved = snapshot_path.resolve()

    try:
        inside_temp = (
            os.path.commonpath(
                [
                    _norm(resolved),
                    _norm(temp_root),
                ]
            )
            == _norm(temp_root)
        )
    except ValueError:
        inside_temp = False

    if not inside_temp:
        raise FirstOpenError(
            "snapshot must be stored under OS TEMP"
        )

    if _is_reparse_or_link(resolved):
        raise FirstOpenError(
            "snapshot may not be reparse/symlink/junction"
        )

    _assert_regular_single_link(resolved)

    envelope = _load_json(resolved)

    if envelope.get("schema") != SNAPSHOT_SCHEMA:
        raise FirstOpenError(
            "unexpected snapshot schema"
        )

    payload = envelope.get("payload")
    digest = envelope.get("payload_sha256")

    if not isinstance(payload, dict):
        raise FirstOpenError(
            "snapshot payload missing"
        )
    if not isinstance(digest, str):
        raise FirstOpenError(
            "snapshot digest missing"
        )

    actual = hashlib.sha256(
        _canonical_json_bytes(payload)
    ).hexdigest()

    if digest != actual:
        raise FirstOpenError(
            "snapshot payload digest mismatch"
        )

    expected_name = (
        f"first-open-snapshot-{digest}.json"
    )
    if resolved.name != expected_name:
        raise FirstOpenError(
            "snapshot filename/digest binding mismatch"
        )

    return payload, digest


def _identity_from_payload(
    value: object,
) -> FilesystemIdentity:
    if not isinstance(value, dict):
        raise FirstOpenError(
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
        raise FirstOpenError(
            "snapshot Vault identity invalid"
        ) from exc


def _validate_json_file(path: Path) -> object:
    _assert_regular_single_link(path)
    if path.suffix.casefold() != ".json":
        raise FirstOpenError(
            f"non-JSON .obsidian root file forbidden: "
            f"{path.name}"
        )

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise FirstOpenError(
            f"invalid .obsidian JSON file: "
            f"{path.name}: {exc}"
        ) from exc


def _verify_obsidian_directory(
    vault: Path,
) -> dict[str, Any]:
    obsidian = vault / ".obsidian"

    if not obsidian.exists() or not obsidian.is_dir():
        raise FirstOpenError(
            ".obsidian was not created by the manual first open"
        )

    if _is_reparse_or_link(obsidian):
        raise FirstOpenError(
            ".obsidian may not be reparse/symlink/junction"
        )

    files: list[str] = []

    for entry in obsidian.iterdir():
        if _is_reparse_or_link(entry):
            raise FirstOpenError(
                f".obsidian alias forbidden: {entry.name}"
            )

        if entry.is_dir():
            raise FirstOpenError(
                f".obsidian subdirectory forbidden: "
                f"{entry.name}"
            )

        if not entry.is_file():
            raise FirstOpenError(
                f".obsidian non-regular entry forbidden: "
                f"{entry.name}"
            )

        name_casefold = entry.name.casefold()

        if (
            "sync" in name_casefold
            and name_casefold
            != "core-plugins.json"
        ):
            raise FirstOpenError(
                f"explicit Sync artifact forbidden: "
                f"{entry.name}"
            )

        parsed = _validate_json_file(entry)
        files.append(entry.name)

        if name_casefold == (
            "community-plugins.json"
        ):
            if not isinstance(parsed, list) or parsed:
                raise FirstOpenError(
                    "community-plugins.json must be []"
                )

        if name_casefold == "core-plugins.json":
            if isinstance(parsed, list):
                if not all(
                    isinstance(item, str)
                    for item in parsed
                ):
                    raise FirstOpenError(
                        "core-plugins.json list shape invalid"
                    )
                if any(
                    item.casefold() == "sync"
                    for item in parsed
                ):
                    raise FirstOpenError(
                        "Obsidian Sync core plugin enabled"
                    )
            elif isinstance(parsed, dict):
                if not all(
                    isinstance(key, str)
                    and isinstance(enabled, bool)
                    for key, enabled in parsed.items()
                ):
                    raise FirstOpenError(
                        "core-plugins.json object shape invalid"
                    )
                if any(
                    key.casefold() == "sync"
                    and enabled
                    for key, enabled in parsed.items()
                ):
                    raise FirstOpenError(
                        "Obsidian Sync core plugin enabled"
                    )
            else:
                raise FirstOpenError(
                    "core-plugins.json shape cannot be interpreted"
                )

    return {
        "directory_present": True,
        "root_json_files": sorted(files),
        "community_plugins_enabled": False,
        "sync_enabled": False,
        "subdirectory_count": 0,
    }


def verify_first_open(
    repo_root: Path,
    snapshot_path: Path,
) -> dict[str, Any]:
    package_dir = Path(__file__).resolve().parent
    first_open_contract, _ = (
        verify_harness_dependencies(
            package_dir
        )
    )

    if _obsidian_running():
        raise FirstOpenError(
            "Obsidian is still running; close it fully "
            "before post-check"
        )

    payload, token = _load_snapshot(
        snapshot_path
    )

    if payload.get(
        "qualified_p3b_head"
    ) != QUALIFIED_P3B_HEAD:
        raise FirstOpenError(
            "snapshot P3-B identity mismatch"
        )

    repo_root = repo_root.resolve()
    current_repo = _repository_payload(
        repo_root
    )

    snapshot_repo = {
        "branch":
            payload.get("repository_branch"),
        "head":
            payload.get("repository_head"),
        "status_porcelain":
            payload.get(
                "repository_status_porcelain"
            ),
    }
    if current_repo != snapshot_repo:
        raise FirstOpenError(
            "ATDS repository state changed since prepare"
        )

    vault = _expected_vault_path(
        first_open_contract
    )
    if _norm(vault) != _norm(
        Path(str(payload.get(
            "vault_resolved_path",
            "",
        )))
    ):
        raise FirstOpenError(
            "snapshot Vault path mismatch"
        )

    if not vault.exists() or not vault.is_dir():
        raise FirstOpenError(
            "Vault missing during post-check"
        )

    snapshot_identity = _identity_from_payload(
        payload.get(
            "vault_filesystem_identity"
        )
    )
    current_identity = filesystem_identity(
        vault
    )
    if current_identity != snapshot_identity:
        raise FirstOpenError(
            "Vault filesystem identity changed"
        )

    try:
        _assert_tree_no_aliases(vault)
    except MaterializationError as exc:
        raise FirstOpenError(
            str(exc)
        ) from exc

    top_level = _top_level_names(vault)
    if top_level != [
        ".obsidian",
        "generated",
        "views",
    ]:
        raise FirstOpenError(
            "post-open Vault top-level entries invalid"
        )

    if (vault / ".git").exists():
        raise FirstOpenError(
            ".git is forbidden inside the Vault"
        )

    if _views_entry_count(vault) != 0:
        raise FirstOpenError(
            "views changed during first open"
        )

    snapshot_generated = (
        _generated_map_from_snapshot(payload)
    )
    current_generated = _digest_map(vault)

    if current_generated != snapshot_generated:
        raise FirstOpenError(
            "generated bytes changed since prepare"
        )

    if _manifest_sha256(vault) != payload.get(
        "integrity_manifest_sha256"
    ):
        raise FirstOpenError(
            "integrity-manifest bytes changed"
        )

    if _build_manifest_sha256(vault) != payload.get(
        "build_manifest_sha256"
    ):
        raise FirstOpenError(
            "build-manifest bytes changed"
        )

    current_tree_digest = projection_tree_digest(
        vault
    )
    if current_tree_digest != payload.get(
        "generated_tree_digest_sha256"
    ):
        raise FirstOpenError(
            "generated projection-tree digest changed"
        )

    statuses = verify_integrity_manifest(
        vault
    )
    if any(
        status != "CLEAN"
        for status in statuses.values()
    ):
        raise FirstOpenError(
            "generated integrity not all CLEAN after open"
        )

    p2_report, fresh_build_a = (
        _fresh_p2_and_compare(
            repo_root,
            vault,
        )
    )

    if _digest_map(
        fresh_build_a
    ) != snapshot_generated:
        raise FirstOpenError(
            "snapshot/generated state no longer equals "
            "fresh qualified P2 BUILD A"
        )

    fresh_identity = payload.get(
        "fresh_p2_identity"
    )
    if not isinstance(
        fresh_identity,
        dict,
    ):
        raise FirstOpenError(
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
        if p2_report.get(field) != (
            fresh_identity.get(field)
        ):
            raise FirstOpenError(
                f"fresh P2 identity changed: {field}"
            )

    obsidian_state = (
        _verify_obsidian_directory(vault)
    )

    repo_after = _repository_payload(
        repo_root
    )
    if repo_after != current_repo:
        raise FirstOpenError(
            "ATDS repository changed during post-check"
        )

    return {
        "schema": VERIFY_REPORT_SCHEMA,
        "status": "PASS",
        "first_open_qualified": True,
        "authorization_token": token,
        "vault_resolved_path": str(vault),
        "vault_filesystem_identity":
            current_identity.to_dict(),
        "generated_file_count":
            len(current_generated),
        "projection_tree_digest_sha256":
            current_tree_digest,
        "views_entry_count": 0,
        "obsidian_state":
            obsidian_state,
        "generated_unchanged": True,
        "fresh_p2_match": True,
        "repository_unchanged": True,
        "automatic_obsidian_launch": False,
        "vault_written_by_harness": False,
    }

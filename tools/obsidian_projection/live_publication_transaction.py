from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import stat
import subprocess
import time
from pathlib import Path
from typing import Any

from .candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
    CandidateGenerationInvalidError,
    verify_candidate_generation,
)
from .observer_tick import (
    INPUT_SCHEMA,
    ObserverTickError,
    one_shot_tick,
)
from .p5d3f_promotion_handoff import (
    PromotionHandoffBlockedError,
    PromotionHandoffGovernanceError,
    _copy_package_exact,
    _package_byte_tree_digest,
    verify_promotion_handoff,
)


class LivePublicationError(RuntimeError):
    pass


class LivePublicationBlockedError(
    LivePublicationError
):
    pass


class LivePublicationGovernanceError(
    LivePublicationError
):
    pass


class LivePublicationRecoveryRequiredError(
    LivePublicationError
):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"

CONTRACT_BLOB = (
    "64997ddd9977229961387f66af4de356c045c0ac"
)
P5D3F_IMPLEMENTATION_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
)
P5D3C2_VERIFIER_BLOB = (
    "e2e5867536f4f9c7dec475c6696737249536ff39"
)
P5D2_OBSERVER_BLOB = (
    "fd212f61ec38332b677110f40265638af55a73e2"
)

REAL_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)

PLAN_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_PUBLICATION_PLAN_V0_1"
)
AUTH_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_HUMAN_AUTHORIZATION_V0_1"
)
PUBLICATION_MANIFEST_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_PUBLICATION_MANIFEST_V0_1"
)
INDEX_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_GENERATION_INDEX_V0_1"
)
CURRENT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_CURRENT_V0_1"
)
PHYSICAL_RECEIPT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_PHYSICAL_PUBLICATION_RECEIPT_V0_1"
)
LOGICAL_RECEIPT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_LOGICAL_CONFIRMATION_RECEIPT_V0_1"
)
ROLLBACK_BASIS_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_ROLLBACK_BASIS_V0_1"
)
ROLLBACK_RECEIPT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_ROLLBACK_RECEIPT_V0_1"
)

SUCCESS_PHYSICAL = (
    "PASS_PHYSICAL_LIVE_PUBLICATION_VERIFIED"
)
SUCCESS_LOGICAL_PENDING = (
    "PASS_PHYSICAL_PUBLICATION_LOGICAL_CONFIRMATION_PENDING"
)
SUCCESS_FINAL = (
    "PASS_LIVE_PUBLICATION_CONFIRMED"
)
ROLLBACK_COMPLETED = (
    "ROLLBACK_COMPLETED_FAILED_CANDIDATE"
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GENERATION_RE = re.compile(r"^gen-[0-9a-f]{64}$")
_NONCE_RE = re.compile(r"^[0-9A-Za-z._-]{16,256}$")

_PLAN_FIELDS = frozenset(
    {
        "schema",
        "source_repository",
        "source_branch",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "candidate_generation_digest_sha256",
        "handoff_package_byte_tree_digest_sha256",
        "handoff_record_sha256",
        "publication_mode",
        "target_generation_relative_path",
        "target_wrapper_schema",
        "expected_previous_current_state",
        "expected_previous_current_sha256",
        "expected_previous_generation_id",
        "expected_previous_generation_digest_sha256",
        "planned_current_sha256",
        "planned_publication_generation_digest_sha256",
        "operation_sequence_digest_sha256",
        "rollback_basis_digest_sha256",
    }
)

_AUTH_FIELDS = frozenset(
    {
        "schema",
        "authorized_action",
        "plan_digest_sha256",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "publication_mode",
        "expected_previous_current_state",
        "one_shot_nonce",
    }
)

_PUBLICATION_MANIFEST_FIELDS = frozenset(
    {
        "schema",
        "source_repository",
        "source_branch",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "candidate_generation_digest_sha256",
        "projection_tree_digest_sha256",
        "package_byte_tree_digest_sha256",
        "payload_file_map_digest_sha256",
        "handoff_contract_blob",
        "p5d3g_contract_blob",
        "materialization_status",
    }
)

_TOOLING = {
    (
        "tools/obsidian_projection/"
        "live_publication_transaction_contract_v0_1.json"
    ): CONTRACT_BLOB,
    (
        "tools/obsidian_projection/"
        "p5d3f_promotion_handoff.py"
    ): P5D3F_IMPLEMENTATION_BLOB,
    (
        "tools/obsidian_projection/"
        "candidate_generation_staging.py"
    ): P5D3C2_VERIFIER_BLOB,
    (
        "tools/obsidian_projection/"
        "observer_tick.py"
    ): P5D2_OBSERVER_BLOB,
}

WRITE_RETRY_DEADLINE_SECONDS = 5.0
WRITE_INITIAL_BACKOFF_SECONDS = 0.010
WRITE_MAX_BACKOFF_SECONDS = 0.500

READ_RETRY_DEADLINE_SECONDS = 0.500
READ_INITIAL_BACKOFF_SECONDS = 0.005
READ_MAX_BACKOFF_SECONDS = 0.050

_WRITER_LOCK_NAME = "P5D3G-WRITER.lock"
_EVENT_LOG_NAME = "P5D3G-publication-events.jsonl"


def _canonical_json_bytes(
    value: Any,
    *,
    terminal_lf: bool = True,
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
        raise LivePublicationGovernanceError(
            "value is not canonical JSON"
        ) from exc

    if terminal_lf:
        raw += b"\n"
    if b"\r" in raw:
        raise LivePublicationGovernanceError(
            "canonical JSON unexpectedly contains CR"
        )
    return raw


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_value(value: Any) -> str:
    return _sha256_bytes(
        _canonical_json_bytes(
            value,
            terminal_lf=False,
        )
    )


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run_git(
    repo: Path,
    *args: str,
) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            env={
                **os.environ,
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "Git unavailable"
        ) from exc

    if completed.returncode != 0:
        raise LivePublicationBlockedError(
            "Git command unavailable"
        )
    return completed.stdout.strip()


def _filtered_blob(
    repo: Path,
    relative: str,
) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "hash-object",
                f"--path={relative}",
                relative,
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            env={
                **os.environ,
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "tooling worktree hash unavailable"
        ) from exc

    if completed.returncode != 0:
        raise LivePublicationBlockedError(
            "tooling worktree identity unavailable"
        )
    return completed.stdout.strip()


def _verify_tooling_identity() -> None:
    repo = _repo_root()

    for relative, expected in _TOOLING.items():
        committed = _run_git(
            repo,
            "rev-parse",
            f"HEAD:{relative}",
        )
        filtered = _filtered_blob(
            repo,
            relative,
        )

        if committed != expected:
            raise LivePublicationGovernanceError(
                f"qualified tooling commit mismatch: {relative}"
            )
        if filtered != expected:
            raise LivePublicationGovernanceError(
                f"qualified tooling worktree mismatch: {relative}"
            )


def _resolve(path: Path) -> Path:
    try:
        return path.resolve(strict=False)
    except OSError as exc:
        raise LivePublicationBlockedError(
            "path resolution unavailable"
        ) from exc


def _intersects(
    first: Path,
    second: Path,
) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )


def _is_reparse_or_link(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as exc:
        raise LivePublicationBlockedError(
            f"cannot lstat path: {path}"
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
    if (
        attributes is not None
        and reparse_flag is not None
        and attributes & reparse_flag
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
            raise LivePublicationBlockedError(
                "junction check unavailable"
            ) from exc

    return False


def _assert_alias_free_chain(path: Path) -> None:
    current = (
        path
        if path.exists()
        else path.parent
    )

    for _ in range(256):
        if current.exists() and _is_reparse_or_link(
            current
        ):
            raise LivePublicationGovernanceError(
                f"reparse/symlink/junction forbidden: {current}"
            )

        parent = current.parent
        if parent == current:
            return
        current = parent

    raise LivePublicationGovernanceError(
        "alias-chain traversal exceeded finite bound"
    )


def _assert_regular_single_link(
    path: Path,
) -> None:
    if _is_reparse_or_link(path):
        raise LivePublicationGovernanceError(
            f"link/reparse file forbidden: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise LivePublicationBlockedError(
            f"cannot stat file: {path}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise LivePublicationGovernanceError(
            f"non-regular file forbidden: {path}"
        )

    links = getattr(
        info,
        "st_nlink",
        None,
    )
    if links is None:
        raise LivePublicationBlockedError(
            "hard-link count unavailable"
        )
    if int(links) != 1:
        raise LivePublicationGovernanceError(
            f"hard-link alias forbidden: {path}"
        )


def _validate_sacrificial_live_vault(
    live_vault_root: Path,
) -> Path:
    live = _resolve(live_vault_root)
    real = _resolve(REAL_VAULT)

    if live == real:
        raise LivePublicationGovernanceError(
            "real production Vault is closed during P5-D3G qualification"
        )

    if not live.exists() or not live.is_dir():
        raise LivePublicationBlockedError(
            "sacrificial live-Vault root must already exist"
        )

    _assert_alias_free_chain(live)

    if (live / ".git").exists():
        raise LivePublicationGovernanceError(
            "sacrificial live Vault may not contain .git"
        )

    return live


def _validate_control_root(
    control_root: Path,
    *,
    live: Path,
    handoff: Path,
) -> Path:
    control = _resolve(control_root)

    if not control.exists() or not control.is_dir():
        raise LivePublicationBlockedError(
            "control root must already exist"
        )

    _assert_alias_free_chain(control)

    if _intersects(control, live):
        raise LivePublicationGovernanceError(
            "control/evidence root overlaps live Vault"
        )
    if _intersects(control, handoff):
        raise LivePublicationGovernanceError(
            "control/evidence root overlaps retained handoff"
        )

    return control


def _require_head(
    value: Any,
    field: str,
) -> str:
    if (
        not isinstance(value, str)
        or _HEAD_RE.fullmatch(value) is None
    ):
        raise LivePublicationGovernanceError(
            f"{field} must be lowercase 40-hex"
        )
    return value


def _require_sha256(
    value: Any,
    field: str,
) -> str:
    if (
        not isinstance(value, str)
        or _SHA256_RE.fullmatch(value) is None
    ):
        raise LivePublicationGovernanceError(
            f"{field} must be lowercase SHA-256"
        )
    return value


def _require_generation_id(
    value: Any,
) -> str:
    if (
        not isinstance(value, str)
        or _GENERATION_RE.fullmatch(value) is None
    ):
        raise LivePublicationGovernanceError(
            "generation_id must be gen- plus lowercase SHA-256"
        )
    return value


def _read_json_canonical(
    path: Path,
) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(
            raw.decode("utf-8")
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise LivePublicationGovernanceError(
            f"canonical JSON unavailable: {path.name}"
        ) from exc

    if not isinstance(value, dict):
        raise LivePublicationGovernanceError(
            f"JSON object required: {path.name}"
        )

    if raw != _canonical_json_bytes(value):
        raise LivePublicationGovernanceError(
            f"non-canonical JSON: {path.name}"
        )

    return value, raw


def _verified_handoff(
    handoff_root: Path,
    live: Path,
) -> tuple[
    Path,
    dict[str, Any],
    dict[str, Any],
    bytes,
]:
    handoff = _resolve(handoff_root)

    if _intersects(handoff, live):
        raise LivePublicationGovernanceError(
            "retained handoff overlaps live Vault"
        )

    try:
        verified = verify_promotion_handoff(
            handoff,
            live_vault_root=live,
        )
    except PromotionHandoffBlockedError as exc:
        raise LivePublicationBlockedError(
            "P5-D3F retained handoff verification unavailable"
        ) from exc
    except PromotionHandoffGovernanceError as exc:
        raise LivePublicationGovernanceError(
            "P5-D3F retained handoff invalid"
        ) from exc

    if (
        verified.get("status")
        != "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED"
        or verified.get("handoff_status")
        != "READY_UNAUTHORIZED"
        or verified.get("package_status")
        != "PASS_SEALED_UNPROMOTED"
        or verified.get("publication_authorized")
        is not False
        or verified.get(
            "production_promotion_authorized"
        )
        is not False
        or verified.get(
            "p5d2_promotion_confirmed_emitted"
        )
        is not False
    ):
        raise LivePublicationGovernanceError(
            "retained handoff authority boundary invalid"
        )

    record, raw = _read_json_canonical(
        handoff / "PROMOTION-HANDOFF.json"
    )

    for field in (
        "publication_authorized",
        "current_pointer_mutation_authorized",
        "real_vault_write_authorized",
        "promotion_confirmed_event_authorized",
    ):
        if record.get(field) is not False:
            raise LivePublicationGovernanceError(
                f"retained handoff authority true: {field}"
            )

    if record.get("handoff_status") != (
        "READY_UNAUTHORIZED"
    ):
        raise LivePublicationGovernanceError(
            "retained handoff status mismatch"
        )

    return handoff, verified, record, raw


def _publication_manifest(
    record: dict[str, Any],
) -> dict[str, Any]:
    manifest = {
        "schema":
            PUBLICATION_MANIFEST_SCHEMA,
        "source_repository":
            record["source_repository"],
        "source_branch":
            record["source_branch"],
        "candidate_head":
            record["candidate_head"],
        "candidate_tree":
            record["candidate_tree"],
        "generation_id":
            record["generation_id"],
        "candidate_generation_digest_sha256":
            record[
                "candidate_generation_digest_sha256"
            ],
        "projection_tree_digest_sha256":
            record[
                "projection_tree_digest_sha256"
            ],
        "package_byte_tree_digest_sha256":
            record[
                "package_byte_tree_digest_sha256"
            ],
        "payload_file_map_digest_sha256":
            record[
                "payload_file_map_digest_sha256"
            ],
        "handoff_contract_blob":
            record["handoff_contract_blob"],
        "p5d3g_contract_blob":
            CONTRACT_BLOB,
        "materialization_status":
            "COMPLETE_IMMUTABLE",
    }

    if frozenset(manifest) != (
        _PUBLICATION_MANIFEST_FIELDS
    ):
        raise LivePublicationGovernanceError(
            "publication manifest field set mismatch"
        )

    return manifest


def _index_bytes(
    *,
    generation_id: str,
    candidate_head: str,
    candidate_tree: str,
) -> bytes:
    text = (
        "---\n"
        f"schema: {INDEX_SCHEMA}\n"
        f"generation_id: {generation_id}\n"
        f"candidate_head: {candidate_head}\n"
        f"candidate_tree: {candidate_tree}\n"
        "---\n\n"
        "# ATDS Published Generation\n\n"
        f"Generation: **{generation_id}**\n\n"
        "[[package/generated/manifests/build-manifest.json|"
        "Build manifest]]\n"
    )
    return text.encode("utf-8")


def _current_bytes(
    *,
    generation_id: str,
    publication_generation_digest_sha256: str,
    candidate_head: str,
    candidate_tree: str,
) -> bytes:
    text = (
        "---\n"
        f"schema: {CURRENT_SCHEMA}\n"
        f"generation_id: {generation_id}\n"
        "publication_generation_digest_sha256: "
        f"{publication_generation_digest_sha256}\n"
        f"candidate_head: {candidate_head}\n"
        f"candidate_tree: {candidate_tree}\n"
        "---\n\n"
        "# ATDS Current Projection\n\n"
        f"Active generation: **{generation_id}**\n\n"
        f"[[generations/{generation_id}/INDEX|"
        "Open active generation]]\n"
    )
    return text.encode("utf-8")


def _virtual_target_digest(
    *,
    source_package: Path,
    publication_manifest_raw: bytes,
    index_raw: bytes,
) -> str:
    root = _resolve(source_package)

    _package_byte_tree_digest(root)

    rows: list[list[Any]] = [
        [
            "F",
            "INDEX.md",
            len(index_raw),
            _sha256_bytes(index_raw),
        ],
        [
            "F",
            "PUBLICATION-MANIFEST.json",
            len(publication_manifest_raw),
            _sha256_bytes(
                publication_manifest_raw
            ),
        ],
        ["D", "package"],
    ]

    try:
        paths = sorted(
            root.rglob("*"),
            key=lambda p: p.relative_to(
                root
            ).as_posix(),
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "source package enumeration unavailable"
        ) from exc

    for path in paths:
        relative = (
            "package/"
            + path.relative_to(
                root
            ).as_posix()
        )

        if _is_reparse_or_link(path):
            raise LivePublicationGovernanceError(
                "source package alias forbidden"
            )

        info = path.stat()
        if stat.S_ISDIR(info.st_mode):
            rows.append(
                ["D", relative]
            )
            continue

        _assert_regular_single_link(path)
        raw = path.read_bytes()
        rows.append(
            [
                "F",
                relative,
                len(raw),
                _sha256_bytes(raw),
            ]
        )

    rows.sort(
        key=lambda row: row[1]
    )

    return _sha256_bytes(
        _canonical_json_bytes(
            rows,
            terminal_lf=False,
        )
    )


def _parse_frontmatter(
    raw: bytes,
) -> dict[str, str]:
    try:
        text = raw.decode(
            "utf-8",
            errors="strict",
        )
    except UnicodeDecodeError as exc:
        raise LivePublicationGovernanceError(
            "CURRENT is not UTF-8"
        ) from exc

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise LivePublicationGovernanceError(
            "CURRENT frontmatter missing"
        )

    result: dict[str, str] = {}
    closed = False

    for line in lines[1:]:
        if line == "---":
            closed = True
            break
        if ":" not in line:
            raise LivePublicationGovernanceError(
                "CURRENT frontmatter invalid"
            )
        key, value = line.split(":", 1)
        key = key.strip()
        if key in result:
            raise LivePublicationGovernanceError(
                "CURRENT duplicate frontmatter field"
            )
        result[key] = value.strip()

    if not closed:
        raise LivePublicationGovernanceError(
            "CURRENT frontmatter not closed"
        )

    return result


def _is_retryable_reader_access(
    exc: BaseException,
) -> bool:
    current: BaseException | None = exc
    seen: set[int] = set()

    for _ in range(32):
        if (
            current is None
            or id(current) in seen
        ):
            return False

        seen.add(id(current))

        if isinstance(current, PermissionError):
            winerror = getattr(
                current,
                "winerror",
                None,
            )
            if winerror in {5, 32}:
                return True
            if (
                winerror is None
                and getattr(
                    current,
                    "errno",
                    None,
                )
                == errno.EACCES
            ):
                return True

        current = current.__cause__

    return False


def _read_bytes_with_retry(
    path: Path,
) -> bytes:
    started = time.monotonic()
    delay = READ_INITIAL_BACKOFF_SECONDS

    for _ in range(64):
        try:
            return path.read_bytes()
        except PermissionError as exc:
            if not _is_retryable_reader_access(
                exc
            ):
                raise

            elapsed = (
                time.monotonic()
                - started
            )
            remaining = (
                READ_RETRY_DEADLINE_SECONDS
                - elapsed
            )
            if remaining <= 0:
                raise LivePublicationBlockedError(
                    "reader access retry deadline exceeded"
                ) from exc

            time.sleep(
                min(
                    delay,
                    remaining,
                )
            )
            delay = min(
                delay * 2,
                READ_MAX_BACKOFF_SECONDS,
            )

    raise LivePublicationBlockedError(
        "reader access retry attempt bound exceeded"
    )


def _validate_target(
    target: Path,
) -> dict[str, Any]:
    target = _resolve(target)

    if (
        not target.exists()
        or not target.is_dir()
    ):
        raise LivePublicationBlockedError(
            "published generation target unavailable"
        )

    _assert_alias_free_chain(target)

    try:
        top = {
            child.name
            for child in target.iterdir()
        }
    except OSError as exc:
        raise LivePublicationBlockedError(
            "published generation layout unavailable"
        ) from exc

    if top != {
        "package",
        "PUBLICATION-MANIFEST.json",
        "INDEX.md",
    }:
        raise LivePublicationGovernanceError(
            "published generation wrapper layout mismatch"
        )

    package = target / "package"

    try:
        descriptor = verify_candidate_generation(
            package
        )
    except CandidateGenerationInfrastructureError as exc:
        raise LivePublicationBlockedError(
            "published package verification unavailable"
        ) from exc
    except CandidateGenerationInvalidError as exc:
        raise LivePublicationGovernanceError(
            "published package invalid"
        ) from exc

    manifest, manifest_raw = (
        _read_json_canonical(
            target
            / "PUBLICATION-MANIFEST.json"
        )
    )

    if frozenset(manifest) != (
        _PUBLICATION_MANIFEST_FIELDS
    ):
        raise LivePublicationGovernanceError(
            "publication manifest exact field set mismatch"
        )

    if (
        manifest.get("schema")
        != PUBLICATION_MANIFEST_SCHEMA
        or manifest.get(
            "materialization_status"
        )
        != "COMPLETE_IMMUTABLE"
        or manifest.get(
            "p5d3g_contract_blob"
        )
        != CONTRACT_BLOB
    ):
        raise LivePublicationGovernanceError(
            "publication manifest authority mismatch"
        )

    expected = {
        "source_repository":
            EXPECTED_REPOSITORY,
        "source_branch":
            EXPECTED_BRANCH,
        "candidate_head":
            descriptor["candidate_head"],
        "candidate_tree":
            descriptor["candidate_tree"],
        "generation_id":
            descriptor["generation_id"],
        "candidate_generation_digest_sha256":
            descriptor[
                "candidate_generation_digest_sha256"
            ],
        "projection_tree_digest_sha256":
            descriptor[
                "projection_tree_digest_sha256"
            ],
        "package_byte_tree_digest_sha256":
            _package_byte_tree_digest(
                package
            ),
        "payload_file_map_digest_sha256":
            descriptor[
                "payload_file_map_digest_sha256"
            ],
        "handoff_contract_blob":
            "64744325251db350d26c0269090ce62d5fa5f2e8",
    }

    for field, value in expected.items():
        if manifest.get(field) != value:
            raise LivePublicationGovernanceError(
                f"publication manifest mismatch: {field}"
            )

    generation_id = _require_generation_id(
        manifest["generation_id"]
    )

    if target.name != generation_id:
        raise LivePublicationGovernanceError(
            "target directory generation ID mismatch"
        )

    index_path = target / "INDEX.md"
    _assert_regular_single_link(index_path)
    try:
        index_raw = index_path.read_bytes()
    except OSError as exc:
        raise LivePublicationBlockedError(
            "generation INDEX unavailable"
        ) from exc

    expected_index = _index_bytes(
        generation_id=generation_id,
        candidate_head=(
            descriptor["candidate_head"]
        ),
        candidate_tree=(
            descriptor["candidate_tree"]
        ),
    )
    if index_raw != expected_index:
        raise LivePublicationGovernanceError(
            "generation INDEX identity mismatch"
        )

    wrapper_digest = (
        _package_byte_tree_digest(
            target
        )
    )

    return {
        "generation_id": generation_id,
        "candidate_head":
            descriptor["candidate_head"],
        "candidate_tree":
            descriptor["candidate_tree"],
        "candidate_generation_digest_sha256":
            descriptor[
                "candidate_generation_digest_sha256"
            ],
        "projection_tree_digest_sha256":
            descriptor[
                "projection_tree_digest_sha256"
            ],
        "payload_file_map_digest_sha256":
            descriptor[
                "payload_file_map_digest_sha256"
            ],
        "package_byte_tree_digest_sha256":
            expected[
                "package_byte_tree_digest_sha256"
            ],
        "publication_generation_digest_sha256":
            wrapper_digest,
        "publication_manifest_sha256":
            _sha256_bytes(
                manifest_raw
            ),
    }


def _validate_current_pointer(
    live: Path,
) -> dict[str, Any]:
    pointer = live / "CURRENT.md"

    if not pointer.is_file():
        raise LivePublicationBlockedError(
            "CURRENT.md missing"
        )

    _assert_regular_single_link(pointer)

    try:
        raw = _read_bytes_with_retry(
            pointer
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT.md read unavailable"
        ) from exc

    frontmatter = _parse_frontmatter(
        raw
    )

    required = {
        "schema",
        "generation_id",
        "publication_generation_digest_sha256",
        "candidate_head",
        "candidate_tree",
    }
    if set(frontmatter) != required:
        raise LivePublicationGovernanceError(
            "CURRENT frontmatter field set mismatch"
        )

    if frontmatter["schema"] != (
        CURRENT_SCHEMA
    ):
        raise LivePublicationGovernanceError(
            "CURRENT schema mismatch"
        )

    generation_id = _require_generation_id(
        frontmatter["generation_id"]
    )
    digest = _require_sha256(
        frontmatter[
            "publication_generation_digest_sha256"
        ],
        "publication_generation_digest_sha256",
    )
    head = _require_head(
        frontmatter["candidate_head"],
        "candidate_head",
    )
    tree = _require_head(
        frontmatter["candidate_tree"],
        "candidate_tree",
    )

    expected_raw = _current_bytes(
        generation_id=generation_id,
        publication_generation_digest_sha256=(
            digest
        ),
        candidate_head=head,
        candidate_tree=tree,
    )
    if raw != expected_raw:
        raise LivePublicationGovernanceError(
            "CURRENT bytes are not canonical"
        )

    target = (
        live
        / "generations"
        / generation_id
    )
    verified = _validate_target(
        target
    )

    if (
        verified[
            "publication_generation_digest_sha256"
        ]
        != digest
        or verified["candidate_head"]
        != head
        or verified["candidate_tree"]
        != tree
    ):
        raise LivePublicationGovernanceError(
            "CURRENT target identity mismatch"
        )

    return {
        **verified,
        "current_sha256":
            _sha256_bytes(raw),
        "current_raw": raw,
    }


def verify_live_publication(
    *,
    live_vault_root: Path,
    expected_generation_id: str | None = None,
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_sacrificial_live_vault(
        live_vault_root
    )

    current = _validate_current_pointer(
        live
    )

    if (
        expected_generation_id is not None
        and current["generation_id"]
        != expected_generation_id
    ):
        raise LivePublicationGovernanceError(
            "CURRENT generation differs from expected"
        )

    if (live / "CURRENT.tmp").exists():
        raise LivePublicationGovernanceError(
            "CURRENT.tmp remains beside verified CURRENT"
        )

    return {
        "status":
            SUCCESS_PHYSICAL,
        "generation_id":
            current["generation_id"],
        "candidate_head":
            current["candidate_head"],
        "candidate_tree":
            current["candidate_tree"],
        "publication_generation_digest_sha256":
            current[
                "publication_generation_digest_sha256"
            ],
        "current_sha256":
            current["current_sha256"],
        "current_pointer_verified": True,
        "target_generation_verified": True,
        "real_vault_modified": False,
    }


def _operation_sequence_digest() -> str:
    contract_path = (
        _repo_root()
        / "tools"
        / "obsidian_projection"
        / "live_publication_transaction_contract_v0_1.json"
    )
    contract, _ = _read_json_canonical(
        contract_path
    )
    sequence = contract.get(
        "operation_order"
    )
    if not isinstance(sequence, list):
        raise LivePublicationGovernanceError(
            "contract operation_order unavailable"
        )
    return _sha256_value(sequence)


def build_publication_plan(
    *,
    handoff_root: Path,
    live_vault_root: Path,
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_sacrificial_live_vault(
        live_vault_root
    )

    if (live / "CURRENT.tmp").exists():
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_TMP_PREEXISTS"
        )

    (
        handoff,
        verified,
        record,
        handoff_raw,
    ) = _verified_handoff(
        handoff_root,
        live,
    )

    generation_id = _require_generation_id(
        verified["generation_id"]
    )
    target = (
        live
        / "generations"
        / generation_id
    )

    if target.exists():
        raise LivePublicationBlockedError(
            "BLOCKED_TARGET_GENERATION_COLLISION"
        )

    manifest = _publication_manifest(
        record
    )
    manifest_raw = _canonical_json_bytes(
        manifest
    )
    index_raw = _index_bytes(
        generation_id=generation_id,
        candidate_head=(
            verified["candidate_head"]
        ),
        candidate_tree=(
            verified["candidate_tree"]
        ),
    )

    wrapper_digest = _virtual_target_digest(
        source_package=(
            handoff / "package"
        ),
        publication_manifest_raw=(
            manifest_raw
        ),
        index_raw=index_raw,
    )

    pointer = live / "CURRENT.md"

    if pointer.exists():
        previous = _validate_current_pointer(
            live
        )
        publication_mode = (
            "REPLACE_EXISTING_CURRENT"
        )
        previous_state = "PRESENT_VALID"
        previous_sha = (
            previous["current_sha256"]
        )
        previous_generation_id = (
            previous["generation_id"]
        )
        previous_generation_digest = (
            previous[
                "publication_generation_digest_sha256"
            ]
        )
    else:
        publication_mode = (
            "BOOTSTRAP_NO_CURRENT"
        )
        previous_state = "ABSENT"
        previous_sha = None
        previous_generation_id = None
        previous_generation_digest = None

    current_raw = _current_bytes(
        generation_id=generation_id,
        publication_generation_digest_sha256=(
            wrapper_digest
        ),
        candidate_head=(
            verified["candidate_head"]
        ),
        candidate_tree=(
            verified["candidate_tree"]
        ),
    )

    rollback_basis = {
        "expected_previous_current_state":
            previous_state,
        "expected_previous_current_sha256":
            previous_sha,
        "expected_previous_generation_id":
            previous_generation_id,
        "expected_previous_generation_digest_sha256":
            previous_generation_digest,
        "target_state": "ABSENT",
    }

    plan = {
        "schema": PLAN_SCHEMA,
        "source_repository":
            record["source_repository"],
        "source_branch":
            record["source_branch"],
        "candidate_head":
            verified["candidate_head"],
        "candidate_tree":
            verified["candidate_tree"],
        "generation_id":
            generation_id,
        "candidate_generation_digest_sha256":
            verified[
                "candidate_generation_digest_sha256"
            ],
        "handoff_package_byte_tree_digest_sha256":
            verified[
                "package_byte_tree_digest_sha256"
            ],
        "handoff_record_sha256":
            _sha256_bytes(
                handoff_raw
            ),
        "publication_mode":
            publication_mode,
        "target_generation_relative_path":
            (
                "generations/"
                + generation_id
            ),
        "target_wrapper_schema":
            PUBLICATION_MANIFEST_SCHEMA,
        "expected_previous_current_state":
            previous_state,
        "expected_previous_current_sha256":
            previous_sha,
        "expected_previous_generation_id":
            previous_generation_id,
        "expected_previous_generation_digest_sha256":
            previous_generation_digest,
        "planned_current_sha256":
            _sha256_bytes(
                current_raw
            ),
        "planned_publication_generation_digest_sha256":
            wrapper_digest,
        "operation_sequence_digest_sha256":
            _operation_sequence_digest(),
        "rollback_basis_digest_sha256":
            _sha256_value(
                rollback_basis
            ),
    }

    publication_plan_digest(plan)
    return plan


def publication_plan_digest(
    plan: dict[str, Any],
) -> str:
    if not isinstance(plan, dict):
        raise LivePublicationGovernanceError(
            "publication plan must be object"
        )
    if frozenset(plan) != _PLAN_FIELDS:
        raise LivePublicationGovernanceError(
            "publication plan exact field set mismatch"
        )
    if plan.get("schema") != PLAN_SCHEMA:
        raise LivePublicationGovernanceError(
            "publication plan schema mismatch"
        )
    if plan.get("source_repository") != (
        EXPECTED_REPOSITORY
    ):
        raise LivePublicationGovernanceError(
            "publication plan repository mismatch"
        )
    if plan.get("source_branch") != (
        EXPECTED_BRANCH
    ):
        raise LivePublicationGovernanceError(
            "publication plan branch mismatch"
        )

    _require_head(
        plan.get("candidate_head"),
        "candidate_head",
    )
    _require_head(
        plan.get("candidate_tree"),
        "candidate_tree",
    )
    _require_generation_id(
        plan.get("generation_id")
    )

    for field in (
        "candidate_generation_digest_sha256",
        "handoff_package_byte_tree_digest_sha256",
        "handoff_record_sha256",
        "planned_current_sha256",
        "planned_publication_generation_digest_sha256",
        "operation_sequence_digest_sha256",
        "rollback_basis_digest_sha256",
    ):
        _require_sha256(
            plan.get(field),
            field,
        )

    if plan.get("publication_mode") not in {
        "REPLACE_EXISTING_CURRENT",
        "BOOTSTRAP_NO_CURRENT",
    }:
        raise LivePublicationGovernanceError(
            "publication mode invalid"
        )

    expected_target = (
        "generations/"
        + plan["generation_id"]
    )
    if plan.get(
        "target_generation_relative_path"
    ) != expected_target:
        raise LivePublicationGovernanceError(
            "target generation relative path mismatch"
        )

    if plan.get("target_wrapper_schema") != (
        PUBLICATION_MANIFEST_SCHEMA
    ):
        raise LivePublicationGovernanceError(
            "target wrapper schema mismatch"
        )

    previous_state = plan.get(
        "expected_previous_current_state"
    )

    if plan["publication_mode"] == (
        "BOOTSTRAP_NO_CURRENT"
    ):
        if (
            previous_state != "ABSENT"
            or plan[
                "expected_previous_current_sha256"
            ]
            is not None
            or plan[
                "expected_previous_generation_id"
            ]
            is not None
            or plan[
                "expected_previous_generation_digest_sha256"
            ]
            is not None
        ):
            raise LivePublicationGovernanceError(
                "bootstrap publication prestate invalid"
            )
    else:
        if previous_state != "PRESENT_VALID":
            raise LivePublicationGovernanceError(
                "replace publication prestate invalid"
            )
        _require_sha256(
            plan[
                "expected_previous_current_sha256"
            ],
            "expected_previous_current_sha256",
        )
        _require_generation_id(
            plan[
                "expected_previous_generation_id"
            ]
        )
        _require_sha256(
            plan[
                "expected_previous_generation_digest_sha256"
            ],
            "expected_previous_generation_digest_sha256",
        )

    return _sha256_value(plan)


def _validate_authorization(
    authorization: dict[str, Any] | None,
    plan: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    if authorization is None:
        raise LivePublicationBlockedError(
            "BLOCKED_HUMAN_AUTHORIZATION"
        )
    if not isinstance(authorization, dict):
        raise LivePublicationGovernanceError(
            "authorization must be object"
        )
    if frozenset(authorization) != (
        _AUTH_FIELDS
    ):
        raise LivePublicationGovernanceError(
            "authorization exact field set mismatch"
        )
    if authorization.get("schema") != (
        AUTH_SCHEMA
    ):
        raise LivePublicationGovernanceError(
            "authorization schema mismatch"
        )
    if authorization.get(
        "authorized_action"
    ) != (
        "EXECUTE_ONE_FINITE_LIVE_PUBLICATION_TRANSACTION"
    ):
        raise LivePublicationGovernanceError(
            "authorization action mismatch"
        )

    plan_digest = publication_plan_digest(
        plan
    )

    expected = {
        "plan_digest_sha256":
            plan_digest,
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "generation_id":
            plan["generation_id"],
        "publication_mode":
            plan["publication_mode"],
        "expected_previous_current_state":
            plan[
                "expected_previous_current_state"
            ],
    }

    for field, value in expected.items():
        if authorization.get(field) != value:
            raise LivePublicationGovernanceError(
                f"authorization binding mismatch: {field}"
            )

    nonce = authorization.get(
        "one_shot_nonce"
    )
    if (
        not isinstance(nonce, str)
        or _NONCE_RE.fullmatch(nonce)
        is None
    ):
        raise LivePublicationGovernanceError(
            "authorization one-shot nonce invalid"
        )

    return authorization, _sha256_value(
        authorization
    )


def _assert_current_matches_plan_prestate(
    live: Path,
    plan: dict[str, Any],
) -> None:
    pointer = live / "CURRENT.md"

    if plan[
        "expected_previous_current_state"
    ] == "ABSENT":
        if pointer.exists():
            raise LivePublicationBlockedError(
                "BLOCKED_CURRENT_PRECONDITION_CHANGED"
            )
        return

    if not pointer.is_file():
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_PRECONDITION_CHANGED"
        )

    try:
        raw = _read_bytes_with_retry(
            pointer
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT prestate read unavailable"
        ) from exc

    if _sha256_bytes(raw) != plan[
        "expected_previous_current_sha256"
    ]:
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_PRECONDITION_CHANGED"
        )

    current = _validate_current_pointer(
        live
    )
    if (
        current["generation_id"]
        != plan[
            "expected_previous_generation_id"
        ]
        or current[
            "publication_generation_digest_sha256"
        ]
        != plan[
            "expected_previous_generation_digest_sha256"
        ]
    ):
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_PRECONDITION_CHANGED"
        )


def _acquire_writer_lock(
    control: Path,
    *,
    plan_digest: str,
    authorization_digest: str,
) -> Path:
    lock = control / _WRITER_LOCK_NAME
    payload = {
        "schema":
            "ATDS_OBSIDIAN_P5D3G_WRITER_OWNERSHIP_V0_1",
        "plan_digest_sha256":
            plan_digest,
        "authorization_digest_sha256":
            authorization_digest,
    }

    try:
        with lock.open("xb") as handle:
            handle.write(
                _canonical_json_bytes(
                    payload
                )
            )
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LivePublicationBlockedError(
            "BLOCKED_SINGLE_WRITER"
        ) from exc
    except OSError as exc:
        raise LivePublicationBlockedError(
            "writer ownership unavailable"
        ) from exc

    _assert_regular_single_link(lock)
    return lock


def _consume_authorization(
    control: Path,
    authorization: dict[str, Any],
    *,
    authorization_digest: str,
) -> Path:
    nonce = authorization[
        "one_shot_nonce"
    ]

    directory = (
        control
        / "consumed-authorizations"
    )
    try:
        directory.mkdir(
            exist_ok=True
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "authorization ledger unavailable"
        ) from exc

    marker = directory / (
        nonce + ".json"
    )
    payload = {
        "schema":
            "ATDS_OBSIDIAN_P5D3G_CONSUMED_AUTHORIZATION_V0_1",
        "one_shot_nonce":
            nonce,
        "plan_digest_sha256":
            authorization[
                "plan_digest_sha256"
            ],
        "authorization_digest_sha256":
            authorization_digest,
    }

    try:
        with marker.open("xb") as handle:
            handle.write(
                _canonical_json_bytes(
                    payload
                )
            )
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LivePublicationBlockedError(
            "authorization already consumed"
        ) from exc
    except OSError as exc:
        raise LivePublicationBlockedError(
            "authorization consumption unavailable"
        ) from exc

    return marker


def _consumed_authorization_path(
    control: Path,
    authorization: dict[str, Any],
) -> Path:
    return (
        control
        / "consumed-authorizations"
        / (
            authorization[
                "one_shot_nonce"
            ]
            + ".json"
        )
    )


def _verify_consumed_authorization(
    control: Path,
    authorization: dict[str, Any],
    *,
    authorization_digest: str,
) -> None:
    marker = _consumed_authorization_path(
        control,
        authorization,
    )

    if not marker.is_file():
        raise LivePublicationBlockedError(
            "consumed authorization evidence missing"
        )

    value, _ = _read_json_canonical(
        marker
    )

    expected = {
        "schema":
            "ATDS_OBSIDIAN_P5D3G_CONSUMED_AUTHORIZATION_V0_1",
        "one_shot_nonce":
            authorization[
                "one_shot_nonce"
            ],
        "plan_digest_sha256":
            authorization[
                "plan_digest_sha256"
            ],
        "authorization_digest_sha256":
            authorization_digest,
    }

    if value != expected:
        raise LivePublicationGovernanceError(
            "consumed authorization evidence mismatch"
        )


def _rollback_basis_payload(
    *,
    live: Path,
    plan: dict[str, Any],
    plan_digest: str,
) -> dict[str, Any]:
    _assert_current_matches_plan_prestate(
        live,
        plan,
    )

    if plan[
        "publication_mode"
    ] == "BOOTSTRAP_NO_CURRENT":
        previous_raw_hex = None
    else:
        try:
            previous_raw = (
                _read_bytes_with_retry(
                    live / "CURRENT.md"
                )
            )
        except OSError as exc:
            raise LivePublicationBlockedError(
                "previous CURRENT capture unavailable"
            ) from exc

        if _sha256_bytes(
            previous_raw
        ) != plan[
            "expected_previous_current_sha256"
        ]:
            raise LivePublicationBlockedError(
                "previous CURRENT changed before rollback capture"
            )

        previous_raw_hex = (
            previous_raw.hex()
        )

    rollback_basis = {
        "expected_previous_current_state":
            plan[
                "expected_previous_current_state"
            ],
        "expected_previous_current_sha256":
            plan[
                "expected_previous_current_sha256"
            ],
        "expected_previous_generation_id":
            plan[
                "expected_previous_generation_id"
            ],
        "expected_previous_generation_digest_sha256":
            plan[
                "expected_previous_generation_digest_sha256"
            ],
        "target_state": "ABSENT",
    }

    if _sha256_value(
        rollback_basis
    ) != plan[
        "rollback_basis_digest_sha256"
    ]:
        raise LivePublicationGovernanceError(
            "rollback basis digest mismatch"
        )

    return {
        "schema":
            ROLLBACK_BASIS_SCHEMA,
        "publication_plan_digest_sha256":
            plan_digest,
        "publication_mode":
            plan["publication_mode"],
        "rollback_basis_digest_sha256":
            plan[
                "rollback_basis_digest_sha256"
            ],
        "previous_current_sha256":
            plan[
                "expected_previous_current_sha256"
            ],
        "previous_current_raw_hex":
            previous_raw_hex,
        "previous_generation_id":
            plan[
                "expected_previous_generation_id"
            ],
        "previous_generation_digest_sha256":
            plan[
                "expected_previous_generation_digest_sha256"
            ],
    }


def _persist_rollback_basis(
    control: Path,
    *,
    live: Path,
    plan: dict[str, Any],
    plan_digest: str,
) -> Path:
    directory = (
        control / "rollback-basis"
    )

    try:
        directory.mkdir(
            exist_ok=True
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "rollback-basis directory unavailable"
        ) from exc

    path = directory / (
        plan_digest + ".json"
    )
    payload = _rollback_basis_payload(
        live=live,
        plan=plan,
        plan_digest=plan_digest,
    )

    try:
        with path.open("xb") as handle:
            handle.write(
                _canonical_json_bytes(
                    payload
                )
            )
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LivePublicationBlockedError(
            "rollback basis already exists"
        ) from exc
    except OSError as exc:
        raise LivePublicationBlockedError(
            "rollback basis persistence unavailable"
        ) from exc

    return path


def _load_rollback_basis(
    control: Path,
    *,
    plan: dict[str, Any],
    plan_digest: str,
) -> dict[str, Any]:
    path = (
        control
        / "rollback-basis"
        / (
            plan_digest + ".json"
        )
    )

    if not path.is_file():
        raise LivePublicationBlockedError(
            "rollback basis evidence missing"
        )

    value, _ = _read_json_canonical(
        path
    )

    if (
        value.get("schema")
        != ROLLBACK_BASIS_SCHEMA
        or value.get(
            "publication_plan_digest_sha256"
        )
        != plan_digest
        or value.get(
            "publication_mode"
        )
        != plan["publication_mode"]
        or value.get(
            "rollback_basis_digest_sha256"
        )
        != plan[
            "rollback_basis_digest_sha256"
        ]
        or value.get(
            "previous_current_sha256"
        )
        != plan[
            "expected_previous_current_sha256"
        ]
        or value.get(
            "previous_generation_id"
        )
        != plan[
            "expected_previous_generation_id"
        ]
        or value.get(
            "previous_generation_digest_sha256"
        )
        != plan[
            "expected_previous_generation_digest_sha256"
        ]
    ):
        raise LivePublicationGovernanceError(
            "rollback basis evidence mismatch"
        )

    raw_hex = value.get(
        "previous_current_raw_hex"
    )

    if plan[
        "publication_mode"
    ] == "BOOTSTRAP_NO_CURRENT":
        if raw_hex is not None:
            raise LivePublicationGovernanceError(
                "bootstrap rollback basis unexpectedly contains CURRENT bytes"
            )
    else:
        if not isinstance(raw_hex, str):
            raise LivePublicationGovernanceError(
                "replace rollback basis CURRENT bytes missing"
            )
        try:
            raw = bytes.fromhex(
                raw_hex
            )
        except ValueError as exc:
            raise LivePublicationGovernanceError(
                "rollback basis CURRENT bytes invalid"
            ) from exc

        if _sha256_bytes(
            raw
        ) != plan[
            "expected_previous_current_sha256"
        ]:
            raise LivePublicationGovernanceError(
                "rollback basis CURRENT digest mismatch"
            )

    return value


def _materialize_target(
    *,
    handoff: Path,
    record: dict[str, Any],
    live: Path,
    plan: dict[str, Any],
) -> dict[str, Any]:
    generations = (
        live / "generations"
    )

    try:
        generations.mkdir(
            exist_ok=True
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "live generations namespace unavailable"
        ) from exc

    if not generations.is_dir():
        raise LivePublicationGovernanceError(
            "live generations namespace is not directory"
        )

    _assert_alias_free_chain(
        generations
    )

    target = (
        generations
        / plan["generation_id"]
    )

    if target.exists():
        raise LivePublicationBlockedError(
            "BLOCKED_TARGET_GENERATION_COLLISION"
        )

    try:
        target.mkdir()
    except OSError as exc:
        raise LivePublicationBlockedError(
            "target generation creation unavailable"
        ) from exc

    destination_package = (
        target / "package"
    )

    _copy_package_exact(
        handoff / "package",
        destination_package,
    )

    source_package_digest = (
        _package_byte_tree_digest(
            handoff / "package"
        )
    )
    destination_package_digest = (
        _package_byte_tree_digest(
            destination_package
        )
    )

    if (
        source_package_digest
        != destination_package_digest
        or source_package_digest
        != plan[
            "handoff_package_byte_tree_digest_sha256"
        ]
    ):
        raise LivePublicationGovernanceError(
            "materialized package byte-tree mismatch"
        )

    manifest = _publication_manifest(
        record
    )
    manifest_raw = _canonical_json_bytes(
        manifest
    )
    index_raw = _index_bytes(
        generation_id=(
            plan["generation_id"]
        ),
        candidate_head=(
            plan["candidate_head"]
        ),
        candidate_tree=(
            plan["candidate_tree"]
        ),
    )

    try:
        with (
            target
            / "PUBLICATION-MANIFEST.json"
        ).open("xb") as handle:
            handle.write(manifest_raw)

        with (
            target / "INDEX.md"
        ).open("xb") as handle:
            handle.write(index_raw)
    except OSError as exc:
        raise LivePublicationBlockedError(
            "publication wrapper write unavailable"
        ) from exc

    verified = _validate_target(
        target
    )

    if (
        verified[
            "publication_generation_digest_sha256"
        ]
        != plan[
            "planned_publication_generation_digest_sha256"
        ]
    ):
        raise LivePublicationGovernanceError(
            "materialized target differs from planned digest"
        )

    return verified


def _planned_current_raw(
    plan: dict[str, Any],
) -> bytes:
    raw = _current_bytes(
        generation_id=(
            plan["generation_id"]
        ),
        publication_generation_digest_sha256=(
            plan[
                "planned_publication_generation_digest_sha256"
            ]
        ),
        candidate_head=(
            plan["candidate_head"]
        ),
        candidate_tree=(
            plan["candidate_tree"]
        ),
    )

    if _sha256_bytes(raw) != plan[
        "planned_current_sha256"
    ]:
        raise LivePublicationGovernanceError(
            "planned CURRENT bytes digest mismatch"
        )

    return raw


def _create_current_tmp(
    live: Path,
    plan: dict[str, Any],
) -> bytes:
    temporary = live / "CURRENT.tmp"

    if temporary.exists():
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_TMP_PREEXISTS"
        )

    raw = _planned_current_raw(
        plan
    )

    try:
        with temporary.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_TMP_PREEXISTS"
        ) from exc
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT.tmp write unavailable"
        ) from exc

    _assert_regular_single_link(
        temporary
    )

    try:
        observed = temporary.read_bytes()
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT.tmp verification unavailable"
        ) from exc

    if observed != raw:
        raise LivePublicationGovernanceError(
            "CURRENT.tmp bytes differ from plan"
        )

    return raw


def _replace_current_with_retry(
    live: Path,
    plan: dict[str, Any],
    expected_raw: bytes,
) -> None:
    pointer = live / "CURRENT.md"
    temporary = live / "CURRENT.tmp"

    started = time.monotonic()
    delay = WRITE_INITIAL_BACKOFF_SECONDS

    for _ in range(64):
        try:
            os.replace(
                temporary,
                pointer,
            )
            break
        except PermissionError as exc:
            if getattr(
                exc,
                "winerror",
                None,
            ) not in {5, 32}:
                raise

            if not temporary.is_file():
                raise LivePublicationGovernanceError(
                    "CURRENT.tmp disappeared after retryable replace failure"
                ) from exc

            try:
                temp_raw = temporary.read_bytes()
            except OSError as read_exc:
                raise LivePublicationBlockedError(
                    "CURRENT.tmp retry verification unavailable"
                ) from read_exc

            if temp_raw != expected_raw:
                raise LivePublicationGovernanceError(
                    "CURRENT.tmp changed after retryable replace failure"
                ) from exc

            _assert_current_matches_plan_prestate(
                live,
                plan,
            )

            remaining = (
                WRITE_RETRY_DEADLINE_SECONDS
                - (
                    time.monotonic()
                    - started
                )
            )
            if remaining <= 0:
                raise LivePublicationBlockedError(
                    "BLOCKED_CURRENT_REPLACE_DEADLINE"
                ) from exc

            time.sleep(
                min(
                    delay,
                    remaining,
                )
            )
            delay = min(
                delay * 2,
                WRITE_MAX_BACKOFF_SECONDS,
            )
    else:
        raise LivePublicationBlockedError(
            "CURRENT replace attempt bound exceeded"
        )

    if temporary.exists():
        raise LivePublicationGovernanceError(
            "CURRENT.tmp remains after successful replace"
        )

    try:
        observed = _read_bytes_with_retry(
            pointer
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT read-after-write unavailable"
        ) from exc

    if observed != expected_raw:
        raise LivePublicationGovernanceError(
            "CURRENT read-after-write bytes differ from plan"
        )


def _append_receipt(
    control: Path,
    receipt: dict[str, Any],
) -> str:
    raw = _canonical_json_bytes(
        receipt
    )
    path = control / _EVENT_LOG_NAME

    try:
        with path.open("ab") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise LivePublicationRecoveryRequiredError(
            "publication evidence persistence requires recovery"
        ) from exc

    return _sha256_bytes(raw)


def _physical_receipt(
    *,
    plan: dict[str, Any],
    plan_digest: str,
    authorization_digest: str,
    verified: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema":
            PHYSICAL_RECEIPT_SCHEMA,
        "receipt_type":
            "PHYSICAL_PUBLICATION",
        "status":
            SUCCESS_PHYSICAL,
        "publication_plan_digest_sha256":
            plan_digest,
        "human_authorization_digest_sha256":
            authorization_digest,
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "generation_id":
            plan["generation_id"],
        "publication_generation_digest_sha256":
            verified[
                "publication_generation_digest_sha256"
            ],
        "previous_current_sha256":
            plan[
                "expected_previous_current_sha256"
            ],
        "new_current_sha256":
            verified["current_sha256"],
    }


def _logical_receipt(
    *,
    plan: dict[str, Any],
    plan_digest: str,
    authorization_digest: str,
    verified: dict[str, Any],
    tick_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema":
            LOGICAL_RECEIPT_SCHEMA,
        "receipt_type":
            "LOGICAL_CONFIRMATION",
        "status":
            SUCCESS_FINAL,
        "publication_plan_digest_sha256":
            plan_digest,
        "human_authorization_digest_sha256":
            authorization_digest,
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "generation_id":
            plan["generation_id"],
        "publication_generation_digest_sha256":
            verified[
                "publication_generation_digest_sha256"
            ],
        "previous_current_sha256":
            plan[
                "expected_previous_current_sha256"
            ],
        "new_current_sha256":
            verified["current_sha256"],
        "p5d2_tick_result_digest_sha256":
            _sha256_value(
                tick_result
            ),
    }


def _emit_p5d2_confirmation(
    observer_state: dict[str, Any],
    candidate_head: str,
) -> dict[str, Any]:
    if not isinstance(
        observer_state,
        dict,
    ):
        raise LivePublicationGovernanceError(
            "observer state must be object"
        )

    sequence = observer_state.get(
        "last_event_sequence"
    )
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
    ):
        raise LivePublicationGovernanceError(
            "observer sequence unavailable"
        )

    return one_shot_tick(
        observer_state,
        {
            "schema": INPUT_SCHEMA,
            "event_type":
                "PROMOTION_CONFIRMED",
            "sequence": sequence + 1,
            "observed_head": None,
            "transition_class": None,
            "candidate_head":
                candidate_head,
            "failure_code": None,
        },
    )


def execute_finite_live_publication(
    *,
    handoff_root: Path,
    live_vault_root: Path,
    control_root: Path,
    plan: dict[str, Any],
    authorization: dict[str, Any] | None,
    observer_state: dict[str, Any],
) -> dict[str, Any]:
    _verify_tooling_identity()

    live = _validate_sacrificial_live_vault(
        live_vault_root
    )
    handoff = _resolve(
        handoff_root
    )
    control = _validate_control_root(
        control_root,
        live=live,
        handoff=handoff,
    )

    plan_digest = publication_plan_digest(
        plan
    )
    (
        authorization_value,
        authorization_digest,
    ) = _validate_authorization(
        authorization,
        plan,
    )

    lock = _acquire_writer_lock(
        control,
        plan_digest=plan_digest,
        authorization_digest=(
            authorization_digest
        ),
    )

    terminal_state_reached = False

    try:
        consumed = (
            control
            / "consumed-authorizations"
            / (
                authorization_value[
                    "one_shot_nonce"
                ]
                + ".json"
            )
        )
        if consumed.exists():
            raise LivePublicationBlockedError(
                "authorization already consumed"
            )

        (
            verified_handoff_root,
            verified_handoff,
            handoff_record,
            _handoff_raw,
        ) = _verified_handoff(
            handoff,
            live,
        )

        if (
            verified_handoff[
                "candidate_head"
            ]
            != plan["candidate_head"]
            or verified_handoff[
                "candidate_tree"
            ]
            != plan["candidate_tree"]
            or verified_handoff[
                "generation_id"
            ]
            != plan["generation_id"]
            or verified_handoff[
                "candidate_generation_digest_sha256"
            ]
            != plan[
                "candidate_generation_digest_sha256"
            ]
        ):
            raise LivePublicationGovernanceError(
                "fresh handoff identity differs from plan"
            )

        try:
            fresh_plan = build_publication_plan(
                handoff_root=(
                    verified_handoff_root
                ),
                live_vault_root=live,
            )
        except LivePublicationGovernanceError as exc:
            raise LivePublicationBlockedError(
                "BLOCKED_CURRENT_PRECONDITION_CHANGED"
            ) from exc

        if publication_plan_digest(
            fresh_plan
        ) != plan_digest:
            raise LivePublicationBlockedError(
                "BLOCKED_CURRENT_PRECONDITION_CHANGED"
            )

        _assert_current_matches_plan_prestate(
            live,
            plan,
        )

        if (live / "CURRENT.tmp").exists():
            raise LivePublicationBlockedError(
                "BLOCKED_CURRENT_TMP_PREEXISTS"
            )

        _consume_authorization(
            control,
            authorization_value,
            authorization_digest=(
                authorization_digest
            ),
        )

        _persist_rollback_basis(
            control,
            live=live,
            plan=plan,
            plan_digest=plan_digest,
        )

        target_verified = _materialize_target(
            handoff=verified_handoff_root,
            record=handoff_record,
            live=live,
            plan=plan,
        )

        if (
            target_verified[
                "publication_generation_digest_sha256"
            ]
            != plan[
                "planned_publication_generation_digest_sha256"
            ]
        ):
            raise LivePublicationGovernanceError(
                "target verification differs from plan"
            )

        current_raw = _create_current_tmp(
            live,
            plan,
        )

        _replace_current_with_retry(
            live,
            plan,
            current_raw,
        )

        physical = verify_live_publication(
            live_vault_root=live,
            expected_generation_id=(
                plan["generation_id"]
            ),
        )

        physical_receipt = (
            _physical_receipt(
                plan=plan,
                plan_digest=plan_digest,
                authorization_digest=(
                    authorization_digest
                ),
                verified=physical,
            )
        )
        physical_receipt_digest = (
            _append_receipt(
                control,
                physical_receipt,
            )
        )

        try:
            tick_result = (
                _emit_p5d2_confirmation(
                    observer_state,
                    plan["candidate_head"],
                )
            )
        except ObserverTickError:
            terminal_state_reached = True
            return {
                **physical,
                "status":
                    SUCCESS_LOGICAL_PENDING,
                "physical_receipt_digest_sha256":
                    physical_receipt_digest,
                "logical_receipt_digest_sha256":
                    None,
                "p5d2_promotion_confirmed_emitted":
                    False,
            }

        if (
            tick_result["decision"][
                "action"
            ]
            != "CONFIRM_LIVE_PROJECTION"
            or tick_result["next_state"][
                "live_projection_head"
            ]
            != plan["candidate_head"]
        ):
            raise LivePublicationGovernanceError(
                "P5-D2 logical confirmation result invalid"
            )

        logical_receipt = _logical_receipt(
            plan=plan,
            plan_digest=plan_digest,
            authorization_digest=(
                authorization_digest
            ),
            verified=physical,
            tick_result=tick_result,
        )
        logical_receipt_digest = (
            _append_receipt(
                control,
                logical_receipt,
            )
        )

        terminal_state_reached = True

        return {
            **physical,
            "status":
                SUCCESS_FINAL,
            "physical_receipt_digest_sha256":
                physical_receipt_digest,
            "logical_receipt_digest_sha256":
                logical_receipt_digest,
            "p5d2_promotion_confirmed_emitted":
                True,
            "p5d2_tick_result":
                tick_result,
        }

    finally:
        if lock.exists():
            try:
                lock.unlink()
            except OSError as exc:
                if terminal_state_reached:
                    raise LivePublicationRecoveryRequiredError(
                        "writer ownership release requires adjudication"
                    ) from exc
                raise LivePublicationBlockedError(
                    "writer ownership release unavailable"
                ) from exc


def classify_publication_recovery(
    *,
    live_vault_root: Path,
    plan: dict[str, Any],
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_sacrificial_live_vault(
        live_vault_root
    )
    publication_plan_digest(plan)

    target = (
        live
        / "generations"
        / plan["generation_id"]
    )

    if not target.exists():
        target_state = "ABSENT"
    else:
        try:
            verified_target = (
                _validate_target(
                    target
                )
            )
            if (
                verified_target[
                    "publication_generation_digest_sha256"
                ]
                == plan[
                    "planned_publication_generation_digest_sha256"
                ]
            ):
                target_state = "EXACT"
            else:
                target_state = "INVALID"
        except (
            LivePublicationBlockedError,
            LivePublicationGovernanceError,
        ):
            target_state = "INVALID"

    pointer = live / "CURRENT.md"

    if not pointer.exists():
        if plan[
            "expected_previous_current_state"
        ] == "ABSENT":
            current_state = "PREVIOUS"
        else:
            current_state = "OTHER"
    else:
        try:
            raw = _read_bytes_with_retry(
                pointer
            )
        except OSError:
            raw = b""

        digest = _sha256_bytes(raw)

        if (
            plan[
                "expected_previous_current_sha256"
            ]
            is not None
            and digest
            == plan[
                "expected_previous_current_sha256"
            ]
        ):
            current_state = "PREVIOUS"
        elif digest == plan[
            "planned_current_sha256"
        ]:
            current_state = "NEW"
        else:
            current_state = "OTHER"

    temporary = live / "CURRENT.tmp"
    if not temporary.exists():
        temporary_state = "ABSENT"
    else:
        try:
            temp_raw = temporary.read_bytes()
        except OSError:
            temp_raw = b""

        if _sha256_bytes(
            temp_raw
        ) == plan[
            "planned_current_sha256"
        ]:
            temporary_state = "PLANNED"
        else:
            temporary_state = "OTHER"

    if (
        current_state == "PREVIOUS"
        and target_state == "ABSENT"
    ):
        classification = (
            "PREVIOUS_CURRENT_TARGET_ABSENT"
        )
    elif (
        current_state == "PREVIOUS"
        and target_state == "EXACT"
    ):
        classification = (
            "PREVIOUS_CURRENT_TARGET_EXACT_RESUMABLE"
        )
    elif (
        current_state == "NEW"
        and target_state == "EXACT"
    ):
        classification = (
            "NEW_CURRENT_TARGET_EXACT_FORWARD_COMPLETE"
        )
    elif (
        current_state == "NEW"
        and target_state == "INVALID"
        and plan["publication_mode"]
        == "REPLACE_EXISTING_CURRENT"
    ):
        classification = (
            "NEW_CURRENT_TARGET_INVALID_ROLLBACK_ELIGIBLE"
        )
    elif (
        current_state == "NEW"
        and target_state == "INVALID"
    ):
        classification = (
            "NEW_CURRENT_TARGET_INVALID_BOOTSTRAP_ADJUDICATION"
        )
    else:
        classification = (
            "AMBIGUOUS_PUBLICATION_STATE"
        )

    return {
        "classification":
            classification,
        "current_state":
            current_state,
        "target_state":
            target_state,
        "temporary_state":
            temporary_state,
        "generation_id":
            plan["generation_id"],
    }


def _event_records(
    control: Path,
) -> list[dict[str, Any]]:
    path = control / _EVENT_LOG_NAME

    if not path.exists():
        return []

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise LivePublicationBlockedError(
            "publication event log unavailable"
        ) from exc

    records: list[dict[str, Any]] = []

    for line in raw.splitlines(
        keepends=True
    ):
        if not line:
            continue
        if not line.endswith(b"\n"):
            raise LivePublicationGovernanceError(
                "publication event log has unterminated record"
            )
        try:
            value = json.loads(
                line[:-1].decode(
                    "utf-8"
                )
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise LivePublicationGovernanceError(
                "publication event log record invalid"
            ) from exc

        if (
            not isinstance(value, dict)
            or line
            != _canonical_json_bytes(
                value
            )
        ):
            raise LivePublicationGovernanceError(
                "publication event log record non-canonical"
            )

        records.append(value)

    return records


def _receipt_for_plan(
    records: list[dict[str, Any]],
    *,
    plan_digest: str,
    receipt_type: str,
) -> dict[str, Any] | None:
    matches = [
        row
        for row in records
        if row.get(
            "publication_plan_digest_sha256"
        )
        == plan_digest
        and row.get(
            "receipt_type"
        )
        == receipt_type
    ]

    if len(matches) > 1:
        raise LivePublicationGovernanceError(
            "duplicate publication receipt"
        )

    return (
        matches[0]
        if matches
        else None
    )


def _observer_already_confirms(
    observer_state: dict[str, Any],
    candidate_head: str,
) -> bool:
    return (
        isinstance(
            observer_state,
            dict,
        )
        and observer_state.get(
            "observer_phase"
        )
        == "IDLE"
        and observer_state.get(
            "live_projection_head"
        )
        == candidate_head
    )


def _write_current_tmp_raw(
    live: Path,
    raw: bytes,
) -> None:
    temporary = live / "CURRENT.tmp"

    if temporary.exists():
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_TMP_PREEXISTS"
        )

    try:
        with temporary.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LivePublicationBlockedError(
            "BLOCKED_CURRENT_TMP_PREEXISTS"
        ) from exc
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT.tmp recovery write unavailable"
        ) from exc

    _assert_regular_single_link(
        temporary
    )

    if temporary.read_bytes() != raw:
        raise LivePublicationGovernanceError(
            "CURRENT.tmp recovery bytes mismatch"
        )


def _assert_pointer_raw(
    live: Path,
    expected_raw: bytes | None,
) -> None:
    pointer = live / "CURRENT.md"

    if expected_raw is None:
        if pointer.exists():
            raise LivePublicationBlockedError(
                "CURRENT changed during recovery replace"
            )
        return

    if not pointer.is_file():
        raise LivePublicationBlockedError(
            "CURRENT missing during recovery replace"
        )

    try:
        raw = _read_bytes_with_retry(
            pointer
        )
    except OSError as exc:
        raise LivePublicationBlockedError(
            "CURRENT recovery read unavailable"
        ) from exc

    if raw != expected_raw:
        raise LivePublicationBlockedError(
            "CURRENT changed during recovery replace"
        )


def _replace_current_exact_retry(
    live: Path,
    *,
    expected_old_raw: bytes | None,
    new_raw: bytes,
) -> None:
    pointer = live / "CURRENT.md"
    temporary = live / "CURRENT.tmp"

    if not temporary.is_file():
        raise LivePublicationBlockedError(
            "CURRENT.tmp recovery candidate missing"
        )

    started = time.monotonic()
    delay = WRITE_INITIAL_BACKOFF_SECONDS

    for _ in range(64):
        try:
            os.replace(
                temporary,
                pointer,
            )
            break
        except PermissionError as exc:
            if getattr(
                exc,
                "winerror",
                None,
            ) not in {5, 32}:
                raise

            if not temporary.is_file():
                raise LivePublicationGovernanceError(
                    "CURRENT.tmp disappeared during recovery replace"
                ) from exc

            try:
                temp_raw = temporary.read_bytes()
            except OSError as read_exc:
                raise LivePublicationBlockedError(
                    "CURRENT.tmp recovery verification unavailable"
                ) from read_exc

            if temp_raw != new_raw:
                raise LivePublicationGovernanceError(
                    "CURRENT.tmp changed during recovery replace"
                ) from exc

            _assert_pointer_raw(
                live,
                expected_old_raw,
            )

            remaining = (
                WRITE_RETRY_DEADLINE_SECONDS
                - (
                    time.monotonic()
                    - started
                )
            )
            if remaining <= 0:
                raise LivePublicationBlockedError(
                    "BLOCKED_CURRENT_REPLACE_DEADLINE"
                ) from exc

            time.sleep(
                min(
                    delay,
                    remaining,
                )
            )
            delay = min(
                delay * 2,
                WRITE_MAX_BACKOFF_SECONDS,
            )
    else:
        raise LivePublicationBlockedError(
            "CURRENT recovery replace attempt bound exceeded"
        )

    if temporary.exists():
        raise LivePublicationGovernanceError(
            "CURRENT.tmp remains after recovery replace"
        )

    _assert_pointer_raw(
        live,
        new_raw,
    )


def _finalize_forward_recovery(
    *,
    live: Path,
    control: Path,
    plan: dict[str, Any],
    plan_digest: str,
    authorization_digest: str,
    observer_state: dict[str, Any],
) -> dict[str, Any]:
    physical = verify_live_publication(
        live_vault_root=live,
        expected_generation_id=(
            plan["generation_id"]
        ),
    )

    records = _event_records(
        control
    )
    physical_existing = _receipt_for_plan(
        records,
        plan_digest=plan_digest,
        receipt_type="PHYSICAL_PUBLICATION",
    )

    if physical_existing is None:
        physical_receipt_digest = (
            _append_receipt(
                control,
                _physical_receipt(
                    plan=plan,
                    plan_digest=plan_digest,
                    authorization_digest=(
                        authorization_digest
                    ),
                    verified=physical,
                ),
            )
        )
    else:
        physical_receipt_digest = (
            _sha256_bytes(
                _canonical_json_bytes(
                    physical_existing
                )
            )
        )

    records = _event_records(
        control
    )
    logical_existing = _receipt_for_plan(
        records,
        plan_digest=plan_digest,
        receipt_type="LOGICAL_CONFIRMATION",
    )

    if logical_existing is not None:
        return {
            **physical,
            "status":
                SUCCESS_FINAL,
            "physical_receipt_digest_sha256":
                physical_receipt_digest,
            "logical_receipt_digest_sha256":
                _sha256_bytes(
                    _canonical_json_bytes(
                        logical_existing
                    )
                ),
            "p5d2_promotion_confirmed_emitted":
                True,
            "recovery_completed":
                True,
        }

    if _observer_already_confirms(
        observer_state,
        plan["candidate_head"],
    ):
        raise LivePublicationRecoveryRequiredError(
            "observer already reflects confirmation but logical receipt is missing"
        )

    try:
        tick_result = (
            _emit_p5d2_confirmation(
                observer_state,
                plan["candidate_head"],
            )
        )
    except ObserverTickError:
        return {
            **physical,
            "status":
                SUCCESS_LOGICAL_PENDING,
            "physical_receipt_digest_sha256":
                physical_receipt_digest,
            "logical_receipt_digest_sha256":
                None,
            "p5d2_promotion_confirmed_emitted":
                False,
            "recovery_completed":
                False,
        }

    if (
        tick_result["decision"][
            "action"
        ]
        != "CONFIRM_LIVE_PROJECTION"
        or tick_result["next_state"][
            "live_projection_head"
        ]
        != plan["candidate_head"]
    ):
        raise LivePublicationGovernanceError(
            "recovery P5-D2 confirmation invalid"
        )

    logical_receipt_digest = (
        _append_receipt(
            control,
            _logical_receipt(
                plan=plan,
                plan_digest=plan_digest,
                authorization_digest=(
                    authorization_digest
                ),
                verified=physical,
                tick_result=tick_result,
            ),
        )
    )

    return {
        **physical,
        "status":
            SUCCESS_FINAL,
        "physical_receipt_digest_sha256":
            physical_receipt_digest,
        "logical_receipt_digest_sha256":
            logical_receipt_digest,
        "p5d2_promotion_confirmed_emitted":
            True,
        "p5d2_tick_result":
            tick_result,
        "recovery_completed":
            True,
    }


def _rollback_failed_candidate(
    *,
    live: Path,
    control: Path,
    plan: dict[str, Any],
    plan_digest: str,
    authorization_digest: str,
    rollback_basis: dict[str, Any],
) -> dict[str, Any]:
    if plan[
        "publication_mode"
    ] != "REPLACE_EXISTING_CURRENT":
        raise LivePublicationBlockedError(
            "bootstrap rollback requires human adjudication"
        )

    previous_generation_id = (
        plan[
            "expected_previous_generation_id"
        ]
    )
    assert isinstance(
        previous_generation_id,
        str,
    )

    previous_target = (
        live
        / "generations"
        / previous_generation_id
    )
    previous_verified = _validate_target(
        previous_target
    )

    if (
        previous_verified[
            "publication_generation_digest_sha256"
        ]
        != plan[
            "expected_previous_generation_digest_sha256"
        ]
    ):
        raise LivePublicationBlockedError(
            "previous generation no longer verifies"
        )

    raw_hex = rollback_basis[
        "previous_current_raw_hex"
    ]
    assert isinstance(raw_hex, str)
    previous_raw = bytes.fromhex(
        raw_hex
    )

    expected_previous_raw = _current_bytes(
        generation_id=(
            previous_generation_id
        ),
        publication_generation_digest_sha256=(
            previous_verified[
                "publication_generation_digest_sha256"
            ]
        ),
        candidate_head=(
            previous_verified[
                "candidate_head"
            ]
        ),
        candidate_tree=(
            previous_verified[
                "candidate_tree"
            ]
        ),
    )

    if (
        previous_raw
        != expected_previous_raw
        or _sha256_bytes(
            previous_raw
        )
        != plan[
            "expected_previous_current_sha256"
        ]
    ):
        raise LivePublicationGovernanceError(
            "captured previous CURRENT cannot be reconstructed exactly"
        )

    temporary = live / "CURRENT.tmp"
    if temporary.exists():
        try:
            temp_raw = temporary.read_bytes()
        except OSError as exc:
            raise LivePublicationBlockedError(
                "CURRENT.tmp rollback inspection unavailable"
            ) from exc

        if temp_raw != _planned_current_raw(
            plan
        ):
            raise LivePublicationBlockedError(
                "foreign CURRENT.tmp blocks rollback"
            )
        temporary.unlink()

    new_raw = _planned_current_raw(
        plan
    )
    _assert_pointer_raw(
        live,
        new_raw,
    )

    _write_current_tmp_raw(
        live,
        previous_raw,
    )
    _replace_current_exact_retry(
        live,
        expected_old_raw=new_raw,
        new_raw=previous_raw,
    )

    restored = verify_live_publication(
        live_vault_root=live,
        expected_generation_id=(
            previous_generation_id
        ),
    )

    receipt = {
        "schema":
            ROLLBACK_RECEIPT_SCHEMA,
        "receipt_type":
            "ROLLBACK",
        "status":
            ROLLBACK_COMPLETED,
        "publication_plan_digest_sha256":
            plan_digest,
        "human_authorization_digest_sha256":
            authorization_digest,
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "failed_generation_id":
            plan["generation_id"],
        "restored_generation_id":
            previous_generation_id,
        "restored_current_sha256":
            restored["current_sha256"],
        "p5d2_promotion_confirmed_emitted":
            False,
    }
    rollback_receipt_digest = (
        _append_receipt(
            control,
            receipt,
        )
    )

    return {
        "status":
            ROLLBACK_COMPLETED,
        "failed_generation_id":
            plan["generation_id"],
        "restored_generation_id":
            previous_generation_id,
        "restored_current_sha256":
            restored["current_sha256"],
        "rollback_receipt_digest_sha256":
            rollback_receipt_digest,
        "p5d2_promotion_confirmed_emitted":
            False,
        "real_vault_modified":
            False,
    }


def recover_finite_live_publication(
    *,
    handoff_root: Path,
    live_vault_root: Path,
    control_root: Path,
    plan: dict[str, Any],
    authorization: dict[str, Any] | None,
    observer_state: dict[str, Any],
) -> dict[str, Any]:
    _verify_tooling_identity()

    live = _validate_sacrificial_live_vault(
        live_vault_root
    )
    handoff = _resolve(
        handoff_root
    )
    control = _validate_control_root(
        control_root,
        live=live,
        handoff=handoff,
    )

    plan_digest = publication_plan_digest(
        plan
    )
    (
        authorization_value,
        authorization_digest,
    ) = _validate_authorization(
        authorization,
        plan,
    )

    _verify_consumed_authorization(
        control,
        authorization_value,
        authorization_digest=(
            authorization_digest
        ),
    )
    rollback_basis = _load_rollback_basis(
        control,
        plan=plan,
        plan_digest=plan_digest,
    )

    lock = _acquire_writer_lock(
        control,
        plan_digest=plan_digest,
        authorization_digest=(
            authorization_digest
        ),
    )

    terminal_state_reached = False

    try:
        (
            verified_handoff_root,
            verified_handoff,
            handoff_record,
            _handoff_raw,
        ) = _verified_handoff(
            handoff,
            live,
        )

        if (
            verified_handoff[
                "candidate_head"
            ]
            != plan["candidate_head"]
            or verified_handoff[
                "candidate_tree"
            ]
            != plan["candidate_tree"]
            or verified_handoff[
                "generation_id"
            ]
            != plan["generation_id"]
        ):
            raise LivePublicationGovernanceError(
                "recovery handoff identity differs from plan"
            )

        state = classify_publication_recovery(
            live_vault_root=live,
            plan=plan,
        )
        classification = state[
            "classification"
        ]

        if classification == (
            "NEW_CURRENT_TARGET_INVALID_ROLLBACK_ELIGIBLE"
        ):
            result = _rollback_failed_candidate(
                live=live,
                control=control,
                plan=plan,
                plan_digest=plan_digest,
                authorization_digest=(
                    authorization_digest
                ),
                rollback_basis=(
                    rollback_basis
                ),
            )
            terminal_state_reached = True
            return result

        if classification == (
            "NEW_CURRENT_TARGET_INVALID_BOOTSTRAP_ADJUDICATION"
        ):
            raise LivePublicationBlockedError(
                "BLOCKED_PUBLICATION_RECOVERY_ADJUDICATION"
            )

        if classification == (
            "AMBIGUOUS_PUBLICATION_STATE"
        ):
            raise LivePublicationBlockedError(
                "BLOCKED_PUBLICATION_RECOVERY_ADJUDICATION"
            )

        temporary = live / "CURRENT.tmp"

        if state[
            "temporary_state"
        ] == "OTHER":
            raise LivePublicationBlockedError(
                "BLOCKED_PUBLICATION_RECOVERY_ADJUDICATION"
            )

        if classification == (
            "PREVIOUS_CURRENT_TARGET_ABSENT"
        ):
            if state[
                "temporary_state"
            ] != "ABSENT":
                raise LivePublicationBlockedError(
                    "BLOCKED_PUBLICATION_RECOVERY_ADJUDICATION"
                )

            _materialize_target(
                handoff=(
                    verified_handoff_root
                ),
                record=handoff_record,
                live=live,
                plan=plan,
            )

            current_raw = (
                _create_current_tmp(
                    live,
                    plan,
                )
            )
            _replace_current_with_retry(
                live,
                plan,
                current_raw,
            )

        elif classification == (
            "PREVIOUS_CURRENT_TARGET_EXACT_RESUMABLE"
        ):
            current_raw = (
                _planned_current_raw(
                    plan
                )
            )

            if state[
                "temporary_state"
            ] == "ABSENT":
                _create_current_tmp(
                    live,
                    plan,
                )
            else:
                if temporary.read_bytes() != (
                    current_raw
                ):
                    raise LivePublicationBlockedError(
                        "recovery CURRENT.tmp differs from plan"
                    )

            _replace_current_with_retry(
                live,
                plan,
                current_raw,
            )

        elif classification == (
            "NEW_CURRENT_TARGET_EXACT_FORWARD_COMPLETE"
        ):
            if state[
                "temporary_state"
            ] == "PLANNED":
                if temporary.read_bytes() != (
                    _planned_current_raw(
                        plan
                    )
                ):
                    raise LivePublicationBlockedError(
                        "recovery CURRENT.tmp differs from plan"
                    )
                temporary.unlink()

        else:
            raise LivePublicationBlockedError(
                "BLOCKED_PUBLICATION_RECOVERY_ADJUDICATION"
            )

        result = _finalize_forward_recovery(
            live=live,
            control=control,
            plan=plan,
            plan_digest=plan_digest,
            authorization_digest=(
                authorization_digest
            ),
            observer_state=observer_state,
        )
        terminal_state_reached = (
            result["status"]
            in {
                SUCCESS_FINAL,
                SUCCESS_LOGICAL_PENDING,
            }
        )
        return result

    finally:
        if lock.exists():
            try:
                lock.unlink()
            except OSError as exc:
                if terminal_state_reached:
                    raise LivePublicationRecoveryRequiredError(
                        "recovery writer ownership release requires adjudication"
                    ) from exc
                raise LivePublicationBlockedError(
                    "recovery writer ownership release unavailable"
                ) from exc

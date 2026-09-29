from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .p5d3f_promotion_handoff import (
    run_finite_promotion_handoff,
    verify_promotion_handoff,
)


class PersistentHandoffError(RuntimeError):
    pass


class PersistentHandoffBlockedError(
    PersistentHandoffError
):
    pass


class PersistentHandoffGovernanceError(
    PersistentHandoffError
):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
MONITORED_BRANCH = "integration/system-v1"

PERSISTENT_GATE_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
QUALIFIED_P5D3F_IMPLEMENTATION_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
)

PERSISTENT_STAGING = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING"
)
REAL_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION"
)

_GATE_CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "persistent_production_handoff_gate_contract_v0_1.json"
)
_P5D3F_IMPLEMENTATION_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3f_promotion_handoff.py"
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise PersistentHandoffGovernanceError(
            "value cannot be canonicalized"
        ) from exc


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    args: list[str],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=str(cwd),
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
        raise PersistentHandoffBlockedError(
            "subprocess unavailable"
        ) from exc


def _git(
    repo: Path,
    *args: str,
) -> str:
    completed = _run(
        ["git", *args],
        cwd=repo,
    )
    if completed.returncode != 0:
        details = (
            completed.stderr.strip()
            or completed.stdout.strip()
        )
        raise PersistentHandoffBlockedError(
            "git command failed"
            + (f": {details}" if details else "")
        )
    return completed.stdout.strip()


def _normalize_origin(origin: str) -> str:
    value = origin.strip()
    for prefix in (
        "git@github.com:",
        "https://github.com/",
        "ssh://git@github.com/",
    ):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    else:
        raise PersistentHandoffGovernanceError(
            "unsupported origin form"
        )

    if value.endswith(".git"):
        value = value[:-4]

    value = value.strip("/")
    if value != EXPECTED_REPOSITORY:
        raise PersistentHandoffGovernanceError(
            "repository origin mismatch"
        )
    return value


def _worktree_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "hash-object",
        "--no-filters",
        relative,
    )


def _committed_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "rev-parse",
        f"HEAD:{relative}",
    )


def _verify_tooling_identity(
    control_repo: Path,
) -> None:
    expected = {
        _GATE_CONTRACT_RELATIVE:
            PERSISTENT_GATE_CONTRACT_BLOB,
        _P5D3F_IMPLEMENTATION_RELATIVE:
            QUALIFIED_P5D3F_IMPLEMENTATION_BLOB,
    }

    for relative, blob in expected.items():
        if _committed_blob(
            control_repo,
            relative,
        ) != blob:
            raise PersistentHandoffGovernanceError(
                f"qualified committed blob mismatch: {relative}"
            )
        if _worktree_blob(
            control_repo,
            relative,
        ) != blob:
            raise PersistentHandoffGovernanceError(
                f"qualified worktree blob mismatch: {relative}"
            )


def _is_alias(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            f"cannot lstat path: {path}"
        ) from exc

    if stat.S_ISLNK(info.st_mode):
        return True

    attrs = getattr(
        info,
        "st_file_attributes",
        None,
    )
    reparse = getattr(
        stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        None,
    )
    if (
        attrs is not None
        and reparse is not None
        and attrs & reparse
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
            raise PersistentHandoffBlockedError(
                "junction check unavailable"
            ) from exc

    return False


def _assert_alias_free_chain(
    path: Path,
) -> None:
    current = (
        path
        if path.exists()
        else path.parent
    )

    for _ in range(256):
        if current.exists() and _is_alias(current):
            raise PersistentHandoffGovernanceError(
                f"alias/reparse path forbidden: {current}"
            )

        parent = current.parent
        if parent == current:
            return
        current = parent

    raise PersistentHandoffGovernanceError(
        "alias traversal exceeded finite bound"
    )


def _intersects(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )


def validate_persistent_paths(
    *,
    staging_root: Path | None = None,
    real_vault_root: Path | None = None,
) -> tuple[Path, Path]:
    staging_input = (
        PERSISTENT_STAGING
        if staging_root is None
        else Path(staging_root)
    )
    vault_input = (
        REAL_VAULT
        if real_vault_root is None
        else Path(real_vault_root)
    )

    if os.path.normcase(
        os.path.abspath(str(staging_input))
    ) != os.path.normcase(
        os.path.abspath(str(PERSISTENT_STAGING))
    ):
        raise PersistentHandoffGovernanceError(
            "persistent staging lexical identity mismatch"
        )

    if os.path.normcase(
        os.path.abspath(str(vault_input))
    ) != os.path.normcase(
        os.path.abspath(str(REAL_VAULT))
    ):
        raise PersistentHandoffGovernanceError(
            "real Vault lexical identity mismatch"
        )

    try:
        vault = vault_input.resolve(strict=True)
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            "real Vault unavailable"
        ) from exc

    if not vault.is_dir():
        raise PersistentHandoffBlockedError(
            "real Vault must be a directory"
        )

    parent = staging_input.parent
    try:
        parent_resolved = parent.resolve(strict=True)
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            "persistent staging parent unavailable"
        ) from exc

    if not parent_resolved.is_dir():
        raise PersistentHandoffBlockedError(
            "persistent staging parent must be directory"
        )

    staging = (
        staging_input.resolve(strict=True)
        if staging_input.exists()
        else parent_resolved / staging_input.name
    )

    _assert_alias_free_chain(vault)
    _assert_alias_free_chain(staging)

    if staging.parent != vault.parent:
        raise PersistentHandoffGovernanceError(
            "persistent staging and real Vault must be siblings"
        )

    if _intersects(staging, vault):
        raise PersistentHandoffGovernanceError(
            "persistent staging intersects real Vault"
        )

    return staging, vault


def validate_staging_prestate(
    staging: Path,
) -> str:
    if not staging.exists():
        return "ABSENT"

    if not staging.is_dir():
        raise PersistentHandoffGovernanceError(
            "persistent staging exists but is not directory"
        )

    _assert_alias_free_chain(staging)

    try:
        entries = list(staging.iterdir())
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            "persistent staging enumeration unavailable"
        ) from exc

    if entries:
        raise PersistentHandoffBlockedError(
            "BLOCKED_PERSISTENT_STAGING_CONFLICT"
        )

    return "PRESENT_EMPTY"


def fingerprint_tree(
    root: Path,
) -> dict[str, Any]:
    try:
        resolved = Path(root).resolve(strict=True)
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            "fingerprint root unavailable"
        ) from exc

    if not resolved.is_dir():
        raise PersistentHandoffBlockedError(
            "fingerprint root must be directory"
        )

    _assert_alias_free_chain(resolved)

    rows: list[list[Any]] = []
    files = 0
    directories = 0

    try:
        paths = sorted(
            resolved.rglob("*"),
            key=lambda p: p.relative_to(
                resolved
            ).as_posix(),
        )
    except OSError as exc:
        raise PersistentHandoffBlockedError(
            "fingerprint enumeration unavailable"
        ) from exc

    for path in paths:
        relative = path.relative_to(
            resolved
        ).as_posix()

        if _is_alias(path):
            raise PersistentHandoffGovernanceError(
                f"alias/reparse entry forbidden: {relative}"
            )

        try:
            info = path.stat()
        except OSError as exc:
            raise PersistentHandoffBlockedError(
                f"fingerprint stat unavailable: {relative}"
            ) from exc

        if stat.S_ISDIR(info.st_mode):
            directories += 1
            rows.append(["D", relative])
            continue

        if not stat.S_ISREG(info.st_mode):
            raise PersistentHandoffGovernanceError(
                f"non-regular entry forbidden: {relative}"
            )

        links = getattr(
            info,
            "st_nlink",
            None,
        )
        if links is None:
            raise PersistentHandoffBlockedError(
                f"hard-link count unavailable: {relative}"
            )
        if int(links) != 1:
            raise PersistentHandoffGovernanceError(
                f"hard-link alias forbidden: {relative}"
            )

        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise PersistentHandoffBlockedError(
                f"fingerprint read unavailable: {relative}"
            ) from exc

        files += 1
        rows.append(
            [
                "F",
                relative,
                len(raw),
                _sha256(raw),
            ]
        )

    current = resolved / "CURRENT.md"
    current_tmp = resolved / (
        "CURRENT" + ".tmp"
    )

    if current.exists():
        if _is_alias(current):
            raise PersistentHandoffGovernanceError(
                "current pointer alias forbidden"
            )
        try:
            current_raw = current.read_bytes()
        except OSError as exc:
            raise PersistentHandoffBlockedError(
                "current pointer read unavailable"
            ) from exc
        current_state = "PRESENT"
        current_sha = _sha256(current_raw)
    else:
        current_state = "ABSENT"
        current_sha = None

    return {
        "resolved_root": str(resolved),
        "tree_digest_sha256":
            _sha256(
                _canonical_json_bytes(rows)
            ),
        "file_count": files,
        "directory_count": directories,
        "current_state": current_state,
        "current_sha256": current_sha,
        "current_tmp_state":
            (
                "PRESENT"
                if current_tmp.exists()
                else "ABSENT"
            ),
    }


def assert_zero_real_vault_mutation(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    if before != after:
        raise PersistentHandoffGovernanceError(
            "FAIL_REAL_VAULT_MUTATED"
        )

    return {
        "status":
            "PASS_REAL_VAULT_ZERO_MUTATION",
        "tree_digest_sha256":
            before["tree_digest_sha256"],
        "current_state":
            before["current_state"],
        "current_sha256":
            before["current_sha256"],
        "current_tmp_state":
            before["current_tmp_state"],
        "unchanged": True,
    }


def _fresh_remote_identity(
    control_repo: Path,
) -> dict[str, str]:
    origin_url = _git(
        control_repo,
        "remote",
        "get-url",
        "origin",
    )
    _normalize_origin(origin_url)

    ref = (
        "refs/heads/"
        + MONITORED_BRANCH
    )

    first = _git(
        control_repo,
        "ls-remote",
        "--heads",
        "origin",
        ref,
    )
    parts = first.split()
    if (
        len(parts) != 2
        or parts[1] != ref
        or _HEAD_RE.fullmatch(parts[0]) is None
    ):
        raise PersistentHandoffBlockedError(
            "fresh remote branch identity unavailable"
        )

    head = parts[0]

    _git(
        control_repo,
        "fetch",
        "--no-tags",
        "origin",
        ref,
    )

    fetched = _git(
        control_repo,
        "rev-parse",
        "FETCH_HEAD",
    )
    if fetched != head:
        raise PersistentHandoffBlockedError(
            "BLOCKED_REMOTE_HEAD_RACE"
        )

    tree = _git(
        control_repo,
        "rev-parse",
        "FETCH_HEAD^{tree}",
    )
    if _HEAD_RE.fullmatch(tree) is None:
        raise PersistentHandoffBlockedError(
            "fresh remote tree identity unavailable"
        )

    second = _git(
        control_repo,
        "ls-remote",
        "--heads",
        "origin",
        ref,
    ).split()

    if (
        len(second) != 2
        or second[0] != head
        or second[1] != ref
    ):
        raise PersistentHandoffBlockedError(
            "BLOCKED_REMOTE_HEAD_RACE"
        )

    return {
        "origin_url": origin_url,
        "candidate_head": head,
        "candidate_tree": tree,
    }


def _prepare_candidate_repository(
    *,
    candidate_root: Path,
    origin_url: str,
    candidate_head: str,
    candidate_tree: str,
) -> None:
    candidate_root.mkdir()

    _git(
        candidate_root,
        "init",
    )
    _git(
        candidate_root,
        "remote",
        "add",
        "origin",
        origin_url,
    )
    _git(
        candidate_root,
        "fetch",
        "--no-tags",
        "origin",
        "refs/heads/"
        + MONITORED_BRANCH,
    )

    fetched = _git(
        candidate_root,
        "rev-parse",
        "FETCH_HEAD",
    )
    if fetched != candidate_head:
        raise PersistentHandoffBlockedError(
            "BLOCKED_REMOTE_HEAD_RACE"
        )

    fetched_tree = _git(
        candidate_root,
        "rev-parse",
        "FETCH_HEAD^{tree}",
    )
    if fetched_tree != candidate_tree:
        raise PersistentHandoffGovernanceError(
            "candidate tree mismatch"
        )

    _git(
        candidate_root,
        "switch",
        "--detach",
        candidate_head,
    )

    if _git(
        candidate_root,
        "rev-parse",
        "HEAD",
    ) != candidate_head:
        raise PersistentHandoffGovernanceError(
            "candidate HEAD mismatch"
        )

    if _git(
        candidate_root,
        "rev-parse",
        "HEAD^{tree}",
    ) != candidate_tree:
        raise PersistentHandoffGovernanceError(
            "candidate TREE mismatch"
        )

    if _normalize_origin(
        _git(
            candidate_root,
            "remote",
            "get-url",
            "origin",
        )
    ) != EXPECTED_REPOSITORY:
        raise PersistentHandoffGovernanceError(
            "candidate repository origin mismatch"
        )

    if _git(
        candidate_root,
        "status",
        "--porcelain",
        "--untracked-files=all",
    ):
        raise PersistentHandoffGovernanceError(
            "candidate repository must be clean"
        )


def _ensure_remote_still_exact(
    control_repo: Path,
    expected_head: str,
) -> None:
    ref = (
        "refs/heads/"
        + MONITORED_BRANCH
    )
    result = _git(
        control_repo,
        "ls-remote",
        "--heads",
        "origin",
        ref,
    ).split()

    if (
        len(result) != 2
        or result[0] != expected_head
        or result[1] != ref
    ):
        raise PersistentHandoffBlockedError(
            "BLOCKED_REMOTE_HEAD_RACE"
        )


def _validate_success(
    report: dict[str, Any],
    *,
    candidate_head: str,
    candidate_tree: str,
) -> None:
    expected = {
        "status":
            "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
        "candidate_head":
            candidate_head,
        "candidate_tree":
            candidate_tree,
        "evaluator_outcome":
            "QUALIFIED",
        "package_status":
            "PASS_SEALED_UNPROMOTED",
        "copied_package_status":
            "PASS_SEALED_UNPROMOTED",
        "handoff_status":
            "READY_UNAUTHORIZED",
        "publication_authorized":
            False,
        "current_pointer_created":
            False,
        "real_vault_modified":
            False,
        "production_promotion_authorized":
            False,
        "p5d2_promotion_confirmed_emitted":
            False,
    }

    for field, value in expected.items():
        if report.get(field) != value:
            raise PersistentHandoffGovernanceError(
                f"persistent handoff success mismatch: {field}"
            )

    generation_id = report.get(
        "generation_id"
    )
    if (
        not isinstance(generation_id, str)
        or not generation_id.startswith("gen-")
    ):
        raise PersistentHandoffGovernanceError(
            "generation identity unavailable"
        )


def execute_persistent_production_handoff(
    *,
    control_repo: Path | None = None,
) -> dict[str, Any]:
    repo = (
        _repo_root()
        if control_repo is None
        else Path(control_repo).resolve(strict=True)
    )

    _verify_tooling_identity(repo)

    staging, vault = (
        validate_persistent_paths()
    )
    staging_prestate = (
        validate_staging_prestate(staging)
    )

    remote = _fresh_remote_identity(repo)
    head = remote["candidate_head"]
    tree = remote["candidate_tree"]

    before = fingerprint_tree(vault)

    temp_root = Path(
        tempfile.mkdtemp(
            prefix="ATDS-P5D3F-PERSISTENT-HANDOFF-"
        )
    )
    candidate = temp_root / "candidate"
    evaluation = temp_root / "evaluation"

    if (
        _intersects(temp_root, staging)
        or _intersects(temp_root, vault)
    ):
        shutil.rmtree(
            temp_root,
            ignore_errors=True,
        )
        raise PersistentHandoffGovernanceError(
            "temporary roots intersect protected paths"
        )

    completed = False
    result: dict[str, Any] | None = None

    try:
        evaluation.mkdir()

        _prepare_candidate_repository(
            candidate_root=candidate,
            origin_url=remote[
                "origin_url"
            ],
            candidate_head=head,
            candidate_tree=tree,
        )

        _ensure_remote_still_exact(
            repo,
            head,
        )

        if not staging.exists():
            try:
                staging.mkdir()
            except OSError as exc:
                raise PersistentHandoffBlockedError(
                    "persistent staging creation unavailable"
                ) from exc

        if not staging.is_dir():
            raise PersistentHandoffGovernanceError(
                "persistent staging is not directory"
            )

        _assert_alias_free_chain(staging)

        report = run_finite_promotion_handoff(
            candidate_head=head,
            candidate_tree=tree,
            candidate_repo_root=candidate,
            evaluation_workspace_root=evaluation,
            promotion_staging_root=staging,
            live_vault_root=vault,
        )

        _validate_success(
            report,
            candidate_head=head,
            candidate_tree=tree,
        )

        handoff_root = (
            staging
            / "packages"
            / report["generation_id"]
        )

        verified = verify_promotion_handoff(
            handoff_root,
            live_vault_root=vault,
        )

        _validate_success(
            {
                **verified,
                "evaluator_outcome":
                    report["evaluator_outcome"],
                "copied_package_status":
                    report[
                        "copied_package_status"
                    ],
            },
            candidate_head=head,
            candidate_tree=tree,
        )

        record_path = (
            handoff_root
            / "PROMOTION-HANDOFF.json"
        )
        try:
            record_raw = record_path.read_bytes()
        except OSError as exc:
            raise PersistentHandoffBlockedError(
                "persistent handoff record read unavailable"
            ) from exc

        after = fingerprint_tree(vault)
        zero = assert_zero_real_vault_mutation(
            before,
            after,
        )

        result = {
            "status":
                "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
            "candidate_head": head,
            "candidate_tree": tree,
            "generation_id":
                report["generation_id"],
            "handoff_root":
                str(handoff_root),
            "handoff_record_sha256":
                _sha256(record_raw),
            "package_byte_tree_digest_sha256":
                report[
                    "package_byte_tree_digest_sha256"
                ],
            "staging_prestate":
                staging_prestate,
            "persistent_staging_root":
                str(staging),
            "real_vault_root":
                str(vault),
            "zero_mutation_proof":
                zero,
            "publication_authorized":
                False,
            "live_publication_executed":
                False,
            "mandatory_stop":
                True,
        }

        completed = True
        return result

    finally:
        try:
            shutil.rmtree(temp_root)
        except OSError as exc:
            raise PersistentHandoffBlockedError(
                "BLOCKED_TEMPORARY_CLEANUP"
            ) from exc

        if temp_root.exists():
            raise PersistentHandoffBlockedError(
                "BLOCKED_TEMPORARY_CLEANUP"
            )

        if completed and result is None:
            raise PersistentHandoffGovernanceError(
                "completed result missing"
            )

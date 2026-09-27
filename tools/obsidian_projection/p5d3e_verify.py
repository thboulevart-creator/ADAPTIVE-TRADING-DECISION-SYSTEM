from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable

from .candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
    CandidateGenerationInvalidError,
    verify_candidate_generation,
)
from .finite_candidate_evaluator import (
    FiniteCandidateEvaluatorError,
    evaluate_candidate_finitely,
)
from .git_source import (
    RepositoryIdentityError,
    git_blob_oid,
    normalize_origin,
)
from .observer_tick import (
    INPUT_SCHEMA,
    make_initial_state,
    one_shot_tick,
)


class RealExactHeadSandboxError(RuntimeError):
    pass


class RealExactHeadSandboxBlockedError(
    RealExactHeadSandboxError
):
    pass


class RealExactHeadSandboxGovernanceError(
    RealExactHeadSandboxError
):
    pass


class _GitCommandError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CANONICAL_ORIGIN = (
    "https://github.com/thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM.git"
)
REMOTE_TRACKING_REF = (
    "refs/remotes/origin/integration/system-v1"
)
RESOLUTION_REFSPEC = (
    "+refs/heads/integration/system-v1:"
    "refs/remotes/origin/integration/system-v1"
)
SANDBOX_TRACKING_REF = (
    "refs/remotes/p5d3e-source/integration/system-v1"
)
LOCAL_TRANSFER_REFSPEC = (
    "+"
    + REMOTE_TRACKING_REF
    + ":"
    + SANDBOX_TRACKING_REF
)

P5D3E_CONTRACT_BLOB = (
    "ae4b1691fae16fcd1616e265a089670b9654db4a"
)
P5D3D_EVALUATOR_BLOB = (
    "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562"
)

REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_REPORT_V0_1"
)
BLOCKED_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_BLOCKED_V0_1"
)
FAIL_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_FAIL_V0_1"
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

_FORBIDDEN_PACKAGE_NAMES = frozenset(
    {
        "CURRENT",
        "CURRENT.md",
        "CURRENT.json",
        "CURRENT.tmp",
        "views",
        ".obsidian",
        ".git",
    }
)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _resolve(path: Path) -> Path:
    try:
        return path.resolve(strict=False)
    except OSError as exc:
        raise RealExactHeadSandboxBlockedError(
            "path resolution unavailable"
        ) from exc


def _run(
    argv: list[str],
    *,
    cwd: Path | None = None,
) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=None if cwd is None else str(cwd),
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
        raise _GitCommandError(
            "Git process unavailable"
        ) from exc

    if completed.returncode != 0:
        raise _GitCommandError(
            "Git command failed"
        )
    return completed.stdout.strip()


def _git(repo: Path, *args: str) -> str:
    return _run(
        ["git", "-C", str(repo), *args]
    )


def _require_hex40(
    value: str,
    field: str,
) -> str:
    lowered = value.strip().lower()
    if _HEX40.fullmatch(lowered) is None:
        raise RealExactHeadSandboxGovernanceError(
            f"{field} is not a full lowercase Git object id"
        )
    return lowered


def _require_sha256(
    value: Any,
    field: str,
) -> str:
    if (
        not isinstance(value, str)
        or _HEX64.fullmatch(value) is None
    ):
        raise RealExactHeadSandboxGovernanceError(
            f"{field} is not a lowercase SHA-256"
        )
    return value


def _require_clean(
    repo: Path,
    context: str,
) -> None:
    try:
        status = _git(
            repo,
            "status",
            "--porcelain",
            "--untracked-files=all",
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            f"{context} status unavailable"
        ) from exc
    if status:
        raise RealExactHeadSandboxGovernanceError(
            f"{context} working tree is not clean"
        )


def _require_canonical_origin(
    repo: Path,
    context: str,
) -> None:
    try:
        origin = _git(
            repo,
            "remote",
            "get-url",
            "origin",
        )
        normalized = normalize_origin(origin)
    except (
        _GitCommandError,
        RepositoryIdentityError,
    ) as exc:
        raise RealExactHeadSandboxGovernanceError(
            f"{context} origin is not canonical"
        ) from exc

    if normalized != EXPECTED_REPOSITORY:
        raise RealExactHeadSandboxGovernanceError(
            f"{context} repository identity mismatch"
        )


def _load_contract() -> dict[str, Any]:
    path = Path(__file__).with_name(
        "real_exact_head_sandbox_contract_v0_1.json"
    )
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise RealExactHeadSandboxBlockedError(
            "P5-D3E contract unavailable"
        ) from exc

    if git_blob_oid(raw) != P5D3E_CONTRACT_BLOB:
        raise RealExactHeadSandboxGovernanceError(
            "P5-D3E contract blob mismatch"
        )
    if not isinstance(value, dict):
        raise RealExactHeadSandboxGovernanceError(
            "P5-D3E contract must be an object"
        )
    if value.get("schema") != (
        "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_SANDBOX_CONTRACT_V0_1"
    ):
        raise RealExactHeadSandboxGovernanceError(
            "P5-D3E contract schema mismatch"
        )
    if value.get("qualified_predecessor", {}).get(
        "finite_candidate_evaluator_blob"
    ) != P5D3D_EVALUATOR_BLOB:
        raise RealExactHeadSandboxGovernanceError(
            "P5-D3D evaluator binding mismatch"
        )
    return value


def resolve_real_candidate(
    control_repo_root: Path,
) -> tuple[str, str]:
    _load_contract()

    control = _resolve(control_repo_root)
    if not control.exists() or not control.is_dir():
        raise RealExactHeadSandboxBlockedError(
            "control repository unavailable"
        )

    _require_clean(
        control,
        "control repository before candidate resolution",
    )
    _require_canonical_origin(
        control,
        "control repository",
    )

    try:
        _git(
            control,
            "fetch",
            "--no-tags",
            "origin",
            RESOLUTION_REFSPEC,
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "initial candidate-resolution fetch unavailable"
        ) from exc

    _require_clean(
        control,
        "control repository after candidate resolution",
    )

    try:
        candidate_head = _require_hex40(
            _git(
                control,
                "rev-parse",
                REMOTE_TRACKING_REF,
            ),
            "candidate_head",
        )
        candidate_tree = _require_hex40(
            _git(
                control,
                "rev-parse",
                f"{candidate_head}^{{tree}}",
            ),
            "candidate_tree",
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "candidate HEAD/TREE resolution unavailable"
        ) from exc

    return candidate_head, candidate_tree


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
    except OSError as exc:
        raise RealExactHeadSandboxBlockedError(
            "filesystem fingerprint read unavailable"
        ) from exc
    return digest.hexdigest()


def _tree_fingerprint(root: Path) -> str:
    base = _resolve(root)
    if not base.exists() or not base.is_dir():
        raise RealExactHeadSandboxBlockedError(
            "protected root unavailable"
        )

    rows: list[list[Any]] = []
    reparse_flag = getattr(
        stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        0x400,
    )

    def walk(directory: Path) -> None:
        try:
            entries = sorted(
                os.scandir(directory),
                key=lambda item:
                    item.name.encode("utf-8"),
            )
        except OSError as exc:
            raise RealExactHeadSandboxBlockedError(
                "protected root enumeration unavailable"
            ) from exc

        for entry in entries:
            path = Path(entry.path)
            try:
                relative = (
                    path.relative_to(base)
                    .as_posix()
                )
                info = entry.stat(
                    follow_symlinks=False
                )
            except OSError as exc:
                raise RealExactHeadSandboxBlockedError(
                    "protected root stat unavailable"
                ) from exc

            is_reparse = bool(
                getattr(
                    info,
                    "st_file_attributes",
                    0,
                )
                & reparse_flag
            )

            if entry.is_symlink() or is_reparse:
                rows.append(
                    [
                        relative,
                        "REPARSE",
                        int(info.st_size),
                    ]
                )
                continue

            if stat.S_ISDIR(info.st_mode):
                rows.append(
                    [relative, "DIR"]
                )
                walk(path)
                continue

            if stat.S_ISREG(info.st_mode):
                rows.append(
                    [
                        relative,
                        "FILE",
                        int(info.st_size),
                        _file_sha256(path),
                    ]
                )
                continue

            rows.append(
                [
                    relative,
                    "OTHER",
                    int(info.st_mode),
                    int(info.st_size),
                ]
            )

    walk(base)
    rows.sort(
        key=lambda row:
            str(row[0]).encode("utf-8")
    )
    return _sha256(rows)


def _verify_object_store_independence(
    candidate_repo: Path,
) -> None:
    git_dir = candidate_repo / ".git"
    alternates = (
        git_dir
        / "objects"
        / "info"
        / "alternates"
    )
    if alternates.exists():
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository uses Git alternates"
        )

    objects = git_dir / "objects"
    if not objects.exists() or not objects.is_dir():
        raise RealExactHeadSandboxGovernanceError(
            "candidate object store missing"
        )

    try:
        files = [
            path
            for path in objects.rglob("*")
            if path.is_file()
        ]
    except OSError as exc:
        raise RealExactHeadSandboxBlockedError(
            "candidate object-store enumeration unavailable"
        ) from exc

    if not files:
        raise RealExactHeadSandboxGovernanceError(
            "candidate object store is empty"
        )

    for path in files:
        try:
            links = path.stat().st_nlink
        except OSError as exc:
            raise RealExactHeadSandboxBlockedError(
                "candidate hard-link count unavailable"
            ) from exc
        if links != 1:
            raise RealExactHeadSandboxGovernanceError(
                "candidate object store contains hard links"
            )


def _prepare_candidate_repository(
    *,
    control_repo: Path,
    candidate_repo: Path,
    candidate_head: str,
    candidate_tree: str,
) -> None:
    if candidate_repo.exists():
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository root is not fresh"
        )

    try:
        _run(
            [
                "git",
                "clone",
                "--no-hardlinks",
                "--no-checkout",
                str(control_repo),
                str(candidate_repo),
            ]
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "local no-hardlinks clone unavailable"
        ) from exc

    try:
        _git(
            candidate_repo,
            "fetch",
            "--no-tags",
            control_repo.as_posix(),
            LOCAL_TRANSFER_REFSPEC,
        )
        transferred = _require_hex40(
            _git(
                candidate_repo,
                "rev-parse",
                SANDBOX_TRACKING_REF,
            ),
            "sandbox transferred candidate_head",
        )
        if transferred != candidate_head:
            raise RealExactHeadSandboxGovernanceError(
                "local candidate transfer HEAD mismatch"
            )

        _git(
            candidate_repo,
            "remote",
            "set-url",
            "origin",
            CANONICAL_ORIGIN,
        )
        _git(
            candidate_repo,
            "checkout",
            "--detach",
            candidate_head,
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "candidate repository preparation unavailable"
        ) from exc

    _require_canonical_origin(
        candidate_repo,
        "candidate repository",
    )

    try:
        actual_head = _require_hex40(
            _git(
                candidate_repo,
                "rev-parse",
                "HEAD",
            ),
            "candidate repository HEAD",
        )
        actual_tree = _require_hex40(
            _git(
                candidate_repo,
                "rev-parse",
                "HEAD^{tree}",
            ),
            "candidate repository TREE",
        )
        branch_name = _git(
            candidate_repo,
            "rev-parse",
            "--abbrev-ref",
            "HEAD",
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "candidate repository identity unavailable"
        ) from exc

    if actual_head != candidate_head:
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository HEAD mismatch"
        )
    if actual_tree != candidate_tree:
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository TREE mismatch"
        )
    if branch_name != "HEAD":
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository is not detached"
        )

    _require_clean(
        candidate_repo,
        "candidate repository before evaluation",
    )
    _verify_object_store_independence(
        candidate_repo
    )


def _activation(
    candidate_head: str,
) -> dict[str, Any]:
    state = make_initial_state()

    observed = one_shot_tick(
        state,
        {
            "schema": INPUT_SCHEMA,
            "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1,
            "observed_head": candidate_head,
            "transition_class": "INITIAL",
            "candidate_head": None,
            "failure_code": None,
        },
    )

    activation = one_shot_tick(
        observed["next_state"],
        {
            "schema": INPUT_SCHEMA,
            "event_type": "EVALUATION_STARTED",
            "sequence": 2,
            "observed_head": None,
            "transition_class": None,
            "candidate_head": candidate_head,
            "failure_code": None,
        },
    )

    if (
        activation["decision"]["action"]
        != "START_EXACT_HEAD_EVALUATION"
        or activation["next_state"][
            "observer_phase"
        ] != "EVALUATING"
        or activation["decision"][
            "automatic_promotion_authorized"
        ] is not False
        or activation["decision"][
            "production_write_authorized"
        ] is not False
    ):
        raise RealExactHeadSandboxGovernanceError(
            "sandbox P5-D2 activation invalid"
        )

    return activation


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise RealExactHeadSandboxBlockedError(
            "sandbox JSON evidence unavailable"
        ) from exc
    if not isinstance(value, dict):
        raise RealExactHeadSandboxGovernanceError(
            "sandbox JSON evidence must be an object"
        )
    return value


def _build_manifest_summary(
    workspace: Path,
    evaluator_report: dict[str, Any],
    candidate_head: str,
    candidate_tree: str,
) -> dict[str, int]:
    manifests = []
    for name in ("build-a", "build-b"):
        manifest = _load_json(
            workspace
            / name
            / "generated"
            / "manifests"
            / "build-manifest.json"
        )
        manifests.append(manifest)

    expected_identity = {
        "source_repository": EXPECTED_REPOSITORY,
        "source_branch": EXPECTED_BRANCH,
        "source_commit": candidate_head,
        "source_tree": candidate_tree,
        "dynamic_inventory_digest_sha256":
            evaluator_report[
                "dynamic_inventory_digest_sha256"
            ],
        "semantic_bridge_digest_sha256":
            evaluator_report[
                "semantic_bridge_digest_sha256"
            ],
        "semantic_record_digest_sha256":
            evaluator_report[
                "semantic_record_digest_sha256"
            ],
        "projection_contract_version":
            evaluator_report[
                "projection_contract_blob"
            ],
    }

    for manifest in manifests:
        for key, value in expected_identity.items():
            if manifest.get(key) != value:
                raise RealExactHeadSandboxGovernanceError(
                    "real build-manifest identity mismatch"
                )
        if manifest.get("build_status") != "PASS":
            raise RealExactHeadSandboxGovernanceError(
                "real build status is not PASS"
            )
        if (
            manifest.get(
                "metadata_only_body_read_count"
            )
            != 0
        ):
            raise RealExactHeadSandboxGovernanceError(
                "real build read METADATA_ONLY body"
            )
        if (
            manifest.get("artifact_record_count")
            != manifest.get("source_record_count")
        ):
            raise RealExactHeadSandboxGovernanceError(
                "real build artifact/source count mismatch"
            )
        if (
            "pilot_inventory_digest_sha256"
            in manifest
            or "pilot_source_count" in manifest
        ):
            raise RealExactHeadSandboxGovernanceError(
                "pilot identity leaked into real current-head build"
            )

    count_fields = (
        "source_record_count",
        "full_text_count",
        "metadata_only_count",
        "artifact_record_count",
        "relation_record_count",
        "relation_source_body_read_count",
        "metadata_only_body_read_count",
    )

    for field in count_fields:
        if manifests[0].get(field) != manifests[1].get(field):
            raise RealExactHeadSandboxGovernanceError(
                "Build A/B count mismatch"
            )

    return {
        field: int(manifests[0][field])
        for field in count_fields
    }


def _validate_evaluator_report(
    report: dict[str, Any],
    candidate_head: str,
    candidate_tree: str,
) -> str:
    if report.get("candidate_head") != candidate_head:
        raise RealExactHeadSandboxGovernanceError(
            "evaluator candidate HEAD mismatch"
        )
    if report.get("candidate_tree") != candidate_tree:
        raise RealExactHeadSandboxGovernanceError(
            "evaluator candidate TREE mismatch"
        )
    if report.get("repository") != EXPECTED_REPOSITORY:
        raise RealExactHeadSandboxGovernanceError(
            "evaluator repository mismatch"
        )
    if report.get("branch") != EXPECTED_BRANCH:
        raise RealExactHeadSandboxGovernanceError(
            "evaluator branch mismatch"
        )
    if (
        report.get("real_vault_modified") is not False
        or report.get("current_pointer_created") is not False
        or report.get(
            "production_promotion_authorized"
        ) is not False
    ):
        raise RealExactHeadSandboxGovernanceError(
            "evaluator crossed publication boundary"
        )
    if (
        report.get("live_projection_head_before")
        != report.get("live_projection_head_after")
    ):
        raise RealExactHeadSandboxGovernanceError(
            "evaluator changed live projection head"
        )

    outcome = report.get("outcome")
    if outcome == "QUALIFIED":
        if report.get("failure_code") is not None:
            raise RealExactHeadSandboxGovernanceError(
                "QUALIFIED carries failure code"
            )
        if report.get(
            "p5d2_result_event_emitted"
        ) is not True:
            raise RealExactHeadSandboxGovernanceError(
                "QUALIFIED omitted P5-D2 result event"
            )
        if report.get(
            "candidate_generation_verification_status"
        ) != "PASS_SEALED_UNPROMOTED":
            raise RealExactHeadSandboxGovernanceError(
                "QUALIFIED package status mismatch"
            )
        if (
            report.get(
                "projection_a_tree_digest_sha256"
            )
            != report.get(
                "projection_b_tree_digest_sha256"
            )
        ):
            raise RealExactHeadSandboxGovernanceError(
                "QUALIFIED Build A/B digest mismatch"
            )
        for field in (
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "projection_a_tree_digest_sha256",
            "projection_b_tree_digest_sha256",
            "projection_breaker_manifest_digest_sha256",
            "projection_breaker_result_digest_sha256",
            "determinism_evidence_digest_sha256",
            "candidate_generation_digest_sha256",
            "p5d2_result_tick_digest_sha256",
        ):
            _require_sha256(
                report.get(field),
                field,
            )
        return outcome

    if outcome == "REJECTED":
        if (
            not isinstance(
                report.get("failure_code"),
                str,
            )
            or not report["failure_code"]
        ):
            raise RealExactHeadSandboxGovernanceError(
                "REJECTED failure code missing"
            )
        if report.get(
            "p5d2_result_event_emitted"
        ) is not True:
            raise RealExactHeadSandboxGovernanceError(
                "REJECTED omitted P5-D2 result event"
            )
        return outcome

    if outcome == "BLOCKED":
        if (
            not isinstance(
                report.get("failure_code"),
                str,
            )
            or not report["failure_code"]
        ):
            raise RealExactHeadSandboxGovernanceError(
                "BLOCKED failure code missing"
            )
        if report.get(
            "p5d2_result_event_emitted"
        ) is not False:
            raise RealExactHeadSandboxGovernanceError(
                "BLOCKED emitted P5-D2 result event"
            )
        return outcome

    raise RealExactHeadSandboxGovernanceError(
        "unknown evaluator outcome"
    )


def _verify_package_surfaces(
    package_root: Path,
) -> None:
    try:
        for path in package_root.rglob("*"):
            relative = path.relative_to(
                package_root
            )
            if any(
                part in _FORBIDDEN_PACKAGE_NAMES
                for part in relative.parts
            ):
                raise RealExactHeadSandboxGovernanceError(
                    "forbidden package surface exists"
                )
    except OSError as exc:
        raise RealExactHeadSandboxBlockedError(
            "package surface enumeration unavailable"
        ) from exc


def _candidate_repo_identity(
    candidate_repo: Path,
) -> tuple[str, str, bool]:
    try:
        head = _require_hex40(
            _git(
                candidate_repo,
                "rev-parse",
                "HEAD",
            ),
            "post-evaluation candidate HEAD",
        )
        tree = _require_hex40(
            _git(
                candidate_repo,
                "rev-parse",
                "HEAD^{tree}",
            ),
            "post-evaluation candidate TREE",
        )
        clean = (
            _git(
                candidate_repo,
                "status",
                "--porcelain",
                "--untracked-files=all",
            )
            == ""
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "post-evaluation candidate identity unavailable"
        ) from exc
    return head, tree, clean


def _base_report(
    *,
    status: str,
    candidate_head: str,
    candidate_tree: str,
    evaluator_report: dict[str, Any],
    counts: dict[str, int] | None,
    package_reverification_status: str | None,
    package_reverification_digest_matches: bool | None,
    candidate_resolution_network_fetch_performed: bool,
    real_candidate_evaluated: bool,
    candidate_repository_clean_after: bool,
    control_repository_clean_after: bool,
    real_vault_modified: bool,
) -> dict[str, Any]:
    values = counts or {}
    return {
        "schema": REPORT_SCHEMA,
        "status": status,
        "candidate_head": candidate_head,
        "candidate_tree": candidate_tree,
        "candidate_outcome":
            evaluator_report.get("outcome"),
        "failure_code":
            evaluator_report.get("failure_code"),
        "source_record_count":
            values.get("source_record_count"),
        "full_text_count":
            values.get("full_text_count"),
        "metadata_only_count":
            values.get("metadata_only_count"),
        "artifact_record_count":
            values.get("artifact_record_count"),
        "relation_record_count":
            values.get("relation_record_count"),
        "relation_source_body_read_count":
            values.get(
                "relation_source_body_read_count"
            ),
        "metadata_only_body_read_count":
            values.get(
                "metadata_only_body_read_count"
            ),
        "dynamic_inventory_digest_sha256":
            evaluator_report.get(
                "dynamic_inventory_digest_sha256"
            ),
        "semantic_bridge_digest_sha256":
            evaluator_report.get(
                "semantic_bridge_digest_sha256"
            ),
        "semantic_record_digest_sha256":
            evaluator_report.get(
                "semantic_record_digest_sha256"
            ),
        "projection_a_tree_digest_sha256":
            evaluator_report.get(
                "projection_a_tree_digest_sha256"
            ),
        "projection_b_tree_digest_sha256":
            evaluator_report.get(
                "projection_b_tree_digest_sha256"
            ),
        "projection_breaker_manifest_digest_sha256":
            evaluator_report.get(
                "projection_breaker_manifest_digest_sha256"
            ),
        "projection_breaker_result_digest_sha256":
            evaluator_report.get(
                "projection_breaker_result_digest_sha256"
            ),
        "determinism_evidence_digest_sha256":
            evaluator_report.get(
                "determinism_evidence_digest_sha256"
            ),
        "candidate_generation_digest_sha256":
            evaluator_report.get(
                "candidate_generation_digest_sha256"
            ),
        "candidate_generation_verification_status":
            evaluator_report.get(
                "candidate_generation_verification_status"
            ),
        "package_reverification_status":
            package_reverification_status,
        "package_reverification_digest_matches":
            package_reverification_digest_matches,
        "p5d2_result_event_emitted":
            evaluator_report.get(
                "p5d2_result_event_emitted"
            ),
        "live_projection_head_unchanged": (
            evaluator_report.get(
                "live_projection_head_before"
            )
            == evaluator_report.get(
                "live_projection_head_after"
            )
        ),
        "real_candidate_evaluated":
            real_candidate_evaluated,
        "candidate_resolution_network_fetch_performed":
            candidate_resolution_network_fetch_performed,
        "evaluation_network_fetch_performed":
            False,
        "candidate_repository_clean_after":
            candidate_repository_clean_after,
        "control_repository_clean_after":
            control_repository_clean_after,
        "real_vault_modified":
            real_vault_modified,
        "current_pointer_created":
            evaluator_report.get(
                "current_pointer_created"
            ),
        "production_promotion_authorized":
            evaluator_report.get(
                "production_promotion_authorized"
            ),
        "candidate_repository_retained":
            False,
        "evaluation_workspace_retained":
            False,
    }


def run_pre_resolved_sandbox(
    *,
    control_repo_root: Path,
    candidate_head: str,
    candidate_tree: str,
    real_vault_root: Path,
    candidate_resolution_network_fetch_performed: bool,
    real_candidate_evaluated: bool,
    additional_forbidden_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    _load_contract()

    candidate_head = _require_hex40(
        candidate_head,
        "candidate_head",
    )
    candidate_tree = _require_hex40(
        candidate_tree,
        "candidate_tree",
    )

    control = _resolve(control_repo_root)
    vault = _resolve(real_vault_root)

    if not control.exists() or not control.is_dir():
        raise RealExactHeadSandboxBlockedError(
            "control repository unavailable"
        )
    if not vault.exists() or not vault.is_dir():
        raise RealExactHeadSandboxBlockedError(
            "real Vault root unavailable"
        )

    _require_clean(
        control,
        "control repository before sandbox",
    )
    _require_canonical_origin(
        control,
        "control repository",
    )

    try:
        tracked = _require_hex40(
            _git(
                control,
                "rev-parse",
                REMOTE_TRACKING_REF,
            ),
            "control remote-tracking HEAD",
        )
        tracked_tree = _require_hex40(
            _git(
                control,
                "rev-parse",
                f"{tracked}^{{tree}}",
            ),
            "control remote-tracking TREE",
        )
    except _GitCommandError as exc:
        raise RealExactHeadSandboxBlockedError(
            "control candidate ref unavailable"
        ) from exc

    if tracked != candidate_head:
        raise RealExactHeadSandboxGovernanceError(
            "candidate HEAD differs from governed remote-tracking ref"
        )
    if tracked_tree != candidate_tree:
        raise RealExactHeadSandboxGovernanceError(
            "candidate TREE differs from governed remote-tracking ref"
        )

    vault_before = _tree_fingerprint(vault)

    extra_forbidden = tuple(
        _resolve(Path(root))
        for root in additional_forbidden_roots
    )

    final_report: dict[str, Any] | None = None
    candidate_path: Path | None = None
    workspace_path: Path | None = None

    with tempfile.TemporaryDirectory(
        prefix="atds-p5d3e-real-"
    ) as temp:
        sandbox_root = Path(temp)
        candidate_repo = (
            sandbox_root / "candidate-repo"
        )
        workspace = (
            sandbox_root / "evaluation-workspace"
        )
        candidate_path = candidate_repo
        workspace_path = workspace

        _prepare_candidate_repository(
            control_repo=control,
            candidate_repo=candidate_repo,
            candidate_head=candidate_head,
            candidate_tree=candidate_tree,
        )

        try:
            workspace.mkdir()
        except OSError as exc:
            raise RealExactHeadSandboxBlockedError(
                "evaluation workspace creation unavailable"
            ) from exc

        for name in (
            "build-a",
            "build-b",
            "candidate-package",
        ):
            if (workspace / name).exists():
                raise RealExactHeadSandboxGovernanceError(
                    "evaluation child root is not fresh"
                )

        activation = _activation(
            candidate_head
        )

        forbidden = (
            control,
            vault,
            *extra_forbidden,
        )

        try:
            evaluator_report = (
                evaluate_candidate_finitely(
                    activation_tick_result=activation,
                    candidate_tree=candidate_tree,
                    candidate_repo_root=candidate_repo,
                    evaluation_workspace_root=workspace,
                    forbidden_roots=forbidden,
                )
            )
        except FiniteCandidateEvaluatorError as exc:
            raise RealExactHeadSandboxGovernanceError(
                "qualified P5-D3D evaluator raised unexpectedly"
            ) from exc

        outcome = _validate_evaluator_report(
            evaluator_report,
            candidate_head,
            candidate_tree,
        )

        counts: dict[str, int] | None = None
        package_status: str | None = None
        package_digest_matches: bool | None = None

        if outcome == "QUALIFIED":
            counts = _build_manifest_summary(
                workspace,
                evaluator_report,
                candidate_head,
                candidate_tree,
            )

            package_root = (
                workspace / "candidate-package"
            )
            try:
                descriptor = (
                    verify_candidate_generation(
                        package_root,
                        forbidden_roots=(
                            control,
                            vault,
                            candidate_repo,
                            *extra_forbidden,
                        ),
                    )
                )
            except CandidateGenerationInfrastructureError as exc:
                raise RealExactHeadSandboxBlockedError(
                    "post-evaluation package verification unavailable"
                ) from exc
            except CandidateGenerationInvalidError as exc:
                raise RealExactHeadSandboxGovernanceError(
                    "post-evaluation package verification failed"
                ) from exc

            package_status = descriptor.get(
                "verification_status"
            )
            if package_status != (
                "PASS_SEALED_UNPROMOTED"
            ):
                raise RealExactHeadSandboxGovernanceError(
                    "post-evaluation package status mismatch"
                )

            if descriptor.get(
                "candidate_head"
            ) != candidate_head:
                raise RealExactHeadSandboxGovernanceError(
                    "reverified package HEAD mismatch"
                )
            if descriptor.get(
                "candidate_tree"
            ) != candidate_tree:
                raise RealExactHeadSandboxGovernanceError(
                    "reverified package TREE mismatch"
                )

            package_digest_matches = (
                descriptor.get(
                    "candidate_generation_digest_sha256"
                )
                == evaluator_report.get(
                    "candidate_generation_digest_sha256"
                )
            )
            if not package_digest_matches:
                raise RealExactHeadSandboxGovernanceError(
                    "package reverification digest mismatch"
                )

            for field in (
                "semantic_bridge_digest_sha256",
                "semantic_record_digest_sha256",
                "breaker_manifest_digest_sha256",
                "breaker_result_digest_sha256",
            ):
                report_field = (
                    "projection_" + field
                    if field.startswith("breaker_")
                    else field
                )
                if descriptor.get(field) != (
                    evaluator_report.get(report_field)
                ):
                    raise RealExactHeadSandboxGovernanceError(
                        "package scientific identity mismatch"
                    )

            _verify_package_surfaces(
                package_root
            )

        post_head, post_tree, candidate_clean = (
            _candidate_repo_identity(
                candidate_repo
            )
        )
        if post_head != candidate_head:
            raise RealExactHeadSandboxGovernanceError(
                "candidate repository HEAD changed"
            )
        if post_tree != candidate_tree:
            raise RealExactHeadSandboxGovernanceError(
                "candidate repository TREE changed"
            )
        if not candidate_clean:
            raise RealExactHeadSandboxGovernanceError(
                "candidate repository became dirty"
            )

        try:
            control_clean = (
                _git(
                    control,
                    "status",
                    "--porcelain",
                    "--untracked-files=all",
                )
                == ""
            )
        except _GitCommandError as exc:
            raise RealExactHeadSandboxBlockedError(
                "control post-evaluation status unavailable"
            ) from exc
        if not control_clean:
            raise RealExactHeadSandboxGovernanceError(
                "control repository became dirty"
            )

        vault_after = _tree_fingerprint(vault)
        vault_modified = (
            vault_after != vault_before
        )
        if vault_modified:
            raise RealExactHeadSandboxGovernanceError(
                "real Vault changed during sandbox evaluation"
            )

        if outcome == "QUALIFIED":
            if (
                candidate_resolution_network_fetch_performed
                and real_candidate_evaluated
            ):
                status = (
                    "PASS_REAL_EXACT_HEAD_FINITE_EVALUATION"
                )
            else:
                status = (
                    "PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX"
                )
        elif outcome == "REJECTED":
            status = (
                "FAIL_REAL_CANDIDATE_REJECTED"
            )
        else:
            status = (
                "BLOCKED_REAL_EXACT_HEAD_EVALUATION"
            )

        final_report = _base_report(
            status=status,
            candidate_head=candidate_head,
            candidate_tree=candidate_tree,
            evaluator_report=evaluator_report,
            counts=counts,
            package_reverification_status=(
                package_status
            ),
            package_reverification_digest_matches=(
                package_digest_matches
            ),
            candidate_resolution_network_fetch_performed=(
                candidate_resolution_network_fetch_performed
            ),
            real_candidate_evaluated=(
                real_candidate_evaluated
            ),
            candidate_repository_clean_after=(
                candidate_clean
            ),
            control_repository_clean_after=(
                control_clean
            ),
            real_vault_modified=False,
        )

    if final_report is None:
        raise RealExactHeadSandboxGovernanceError(
            "qualification report was not produced"
        )
    if (
        candidate_path is None
        or workspace_path is None
    ):
        raise RealExactHeadSandboxGovernanceError(
            "sandbox lifecycle evidence missing"
        )
    if candidate_path.exists():
        raise RealExactHeadSandboxGovernanceError(
            "candidate repository retained after run"
        )
    if workspace_path.exists():
        raise RealExactHeadSandboxGovernanceError(
            "evaluation workspace retained after run"
        )

    return final_report


def run_real_exact_head_qualification(
    *,
    control_repo_root: Path,
    real_vault_root: Path,
    additional_forbidden_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    candidate_head, candidate_tree = (
        resolve_real_candidate(
            control_repo_root
        )
    )

    return run_pre_resolved_sandbox(
        control_repo_root=control_repo_root,
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
        real_vault_root=real_vault_root,
        candidate_resolution_network_fetch_performed=True,
        real_candidate_evaluated=True,
        additional_forbidden_roots=(
            additional_forbidden_roots
        ),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "P5-D3E real exact-head sandbox "
            "candidate evaluation qualification."
        )
    )
    parser.add_argument(
        "--control-repo-root",
        default=".",
    )
    parser.add_argument(
        "--real-vault-root",
        required=True,
    )
    parser.add_argument(
        "--forbidden-root",
        action="append",
        default=[],
    )
    return parser


def main() -> int:
    args = _parser().parse_args()

    try:
        report = run_real_exact_head_qualification(
            control_repo_root=Path(
                args.control_repo_root
            ),
            real_vault_root=Path(
                args.real_vault_root
            ),
            additional_forbidden_roots=tuple(
                Path(item)
                for item in args.forbidden_root
            ),
        )
    except RealExactHeadSandboxBlockedError as exc:
        print(
            json.dumps(
                {
                    "schema": BLOCKED_SCHEMA,
                    "status":
                        "BLOCKED_REAL_EXACT_HEAD_EVALUATION",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    except RealExactHeadSandboxGovernanceError as exc:
        print(
            json.dumps(
                {
                    "schema": FAIL_SCHEMA,
                    "status":
                        "FAIL_P5D3E_GOVERNANCE_VIOLATION",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    if (
        report["status"]
        == "PASS_REAL_EXACT_HEAD_FINITE_EVALUATION"
    ):
        return 0
    if (
        report["status"]
        == "BLOCKED_REAL_EXACT_HEAD_EVALUATION"
    ):
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
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
from .git_source import FrozenGitSource, GitSourceError
from .observer_tick import (
    INPUT_SCHEMA,
    make_initial_state,
    one_shot_tick,
)


class PromotionHandoffError(RuntimeError):
    pass


class PromotionHandoffBlockedError(
    PromotionHandoffError
):
    pass


class PromotionHandoffGovernanceError(
    PromotionHandoffError
):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"

HANDOFF_CONTRACT_BLOB = (
    "64744325251db350d26c0269090ce62d5fa5f2e8"
)
P5D3C2_VERIFIER_BLOB = (
    "e2e5867536f4f9c7dec475c6696737249536ff39"
)
P5D3D_EVALUATOR_BLOB = (
    "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562"
)

HANDOFF_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3F_PROMOTION_HANDOFF_V0_1"
)
REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3F_HANDOFF_QUALIFICATION_REPORT_V0_1"
)
SUCCESS_STATUS = (
    "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED"
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

_HANDOFF_FIELDS = frozenset(
    {
        "schema",
        "source_repository",
        "source_branch",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "candidate_generation_digest_sha256",
        "dynamic_inventory_digest_sha256",
        "semantic_bridge_digest_sha256",
        "semantic_record_digest_sha256",
        "projection_tree_digest_sha256",
        "breaker_manifest_digest_sha256",
        "breaker_result_digest_sha256",
        "determinism_evidence_digest_sha256",
        "payload_file_map_digest_sha256",
        "package_byte_tree_digest_sha256",
        "p5d3c2_package_verification_status",
        "handoff_contract_blob",
        "publication_authorized",
        "current_pointer_mutation_authorized",
        "real_vault_write_authorized",
        "promotion_confirmed_event_authorized",
        "handoff_status",
    }
)

_TOOLING = {
    (
        "tools/obsidian_projection/"
        "promotion_handoff_contract_v0_1.json"
    ): HANDOFF_CONTRACT_BLOB,
    (
        "tools/obsidian_projection/"
        "candidate_generation_staging.py"
    ): P5D3C2_VERIFIER_BLOB,
    (
        "tools/obsidian_projection/"
        "finite_candidate_evaluator.py"
    ): P5D3D_EVALUATOR_BLOB,
}


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
        raise PromotionHandoffGovernanceError(
            "handoff value is not canonical JSON"
        ) from exc

    if terminal_lf:
        raw += b"\n"
    if b"\r" in raw:
        raise PromotionHandoffGovernanceError(
            "canonical handoff JSON contains CR"
        )
    return raw


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require_head(
    value: Any,
    field: str,
) -> str:
    if (
        not isinstance(value, str)
        or value != value.lower()
        or _HEX40.fullmatch(value) is None
    ):
        raise PromotionHandoffGovernanceError(
            f"{field} must be lowercase 40-hex"
        )
    return value


def _require_sha256(
    value: Any,
    field: str,
) -> str:
    if (
        not isinstance(value, str)
        or _HEX64.fullmatch(value) is None
    ):
        raise PromotionHandoffGovernanceError(
            f"{field} must be lowercase SHA-256"
        )
    return value


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
        raise PromotionHandoffBlockedError(
            "local Git unavailable"
        ) from exc

    if completed.returncode != 0:
        raise PromotionHandoffBlockedError(
            "local Git command unavailable"
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
        raise PromotionHandoffBlockedError(
            "tooling hash unavailable"
        ) from exc

    if completed.returncode != 0:
        raise PromotionHandoffBlockedError(
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
            raise PromotionHandoffGovernanceError(
                f"qualified tooling commit mismatch: {relative}"
            )
        if filtered != expected:
            raise PromotionHandoffGovernanceError(
                f"qualified tooling worktree mismatch: {relative}"
            )


def _resolve(path: Path) -> Path:
    try:
        return path.resolve(strict=False)
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            "path resolution unavailable"
        ) from exc


def _is_reparse_or_link(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError as exc:
        raise PromotionHandoffBlockedError(
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
            raise PromotionHandoffBlockedError(
                f"junction check unavailable: {path}"
            ) from exc

    return False


def _assert_alias_free_chain(path: Path) -> None:
    current = path if path.exists() else path.parent

    while True:
        if current.exists() and _is_reparse_or_link(
            current
        ):
            raise PromotionHandoffGovernanceError(
                f"reparse/symlink/junction path forbidden: {current}"
            )

        parent = current.parent
        if parent == current:
            return
        current = parent


def _assert_regular_single_link(
    path: Path,
) -> None:
    if _is_reparse_or_link(path):
        raise PromotionHandoffGovernanceError(
            f"reparse/link entry forbidden: {path}"
        )

    try:
        info = path.stat()
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            f"cannot stat file: {path}"
        ) from exc

    if not stat.S_ISREG(info.st_mode):
        raise PromotionHandoffGovernanceError(
            f"non-regular file forbidden: {path}"
        )

    links = getattr(
        info,
        "st_nlink",
        None,
    )
    if links is None:
        raise PromotionHandoffBlockedError(
            f"hard-link count unavailable: {path}"
        )
    if int(links) != 1:
        raise PromotionHandoffGovernanceError(
            f"hard link forbidden: {path}"
        )


def _intersects(
    first: Path,
    second: Path,
) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )


def _is_git_worktree(path: Path) -> bool:
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(path),
                "rev-parse",
                "--show-toplevel",
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
        raise PromotionHandoffBlockedError(
            "Git repository check unavailable"
        ) from exc

    return completed.returncode == 0


def _validate_environment(
    *,
    candidate_repo_root: Path,
    evaluation_workspace_root: Path,
    promotion_staging_root: Path,
    live_vault_root: Path,
) -> tuple[Path, Path, Path, Path]:
    repo = _resolve(candidate_repo_root)
    workspace = _resolve(
        evaluation_workspace_root
    )
    staging = _resolve(
        promotion_staging_root
    )
    vault = _resolve(
        live_vault_root
    )

    for path, label in (
        (repo, "candidate repository"),
        (workspace, "evaluation workspace"),
        (staging, "promotion staging"),
        (vault, "live Vault"),
    ):
        if not path.exists() or not path.is_dir():
            raise PromotionHandoffBlockedError(
                f"{label} must already exist"
            )

    _assert_alias_free_chain(staging)
    _assert_alias_free_chain(vault)

    if _intersects(staging, vault):
        raise PromotionHandoffGovernanceError(
            "promotion staging overlaps live Vault"
        )

    for protected in (
        staging,
        vault,
    ):
        if _intersects(repo, protected):
            raise PromotionHandoffGovernanceError(
                "candidate repository intersects protected root"
            )
        if _intersects(workspace, protected):
            raise PromotionHandoffGovernanceError(
                "evaluation workspace intersects protected root"
            )

    if _intersects(repo, workspace):
        raise PromotionHandoffGovernanceError(
            "candidate repository intersects evaluation workspace"
        )

    if _is_git_worktree(staging):
        raise PromotionHandoffGovernanceError(
            "promotion staging must not be a Git worktree"
        )

    return repo, workspace, staging, vault


def _validate_candidate_repository(
    repo: Path,
    candidate_head: str,
    candidate_tree: str,
) -> None:
    try:
        source = FrozenGitSource(
            repo_root=repo,
            expected_repository=EXPECTED_REPOSITORY,
            source_commit=candidate_head,
            expected_tree=candidate_tree,
        )
        source.verify_repository()
        source.verify_frozen_source()
    except (
        GitSourceError,
        OSError,
        ValueError,
    ) as exc:
        raise PromotionHandoffGovernanceError(
            "candidate repository identity invalid"
        ) from exc

    actual_head = _run_git(
        repo,
        "rev-parse",
        "HEAD",
    )
    actual_tree = _run_git(
        repo,
        "rev-parse",
        "HEAD^{tree}",
    )
    status = _run_git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )

    if actual_head != candidate_head:
        raise PromotionHandoffGovernanceError(
            "candidate repository HEAD mismatch"
        )
    if actual_tree != candidate_tree:
        raise PromotionHandoffGovernanceError(
            "candidate repository TREE mismatch"
        )
    if status:
        raise PromotionHandoffGovernanceError(
            "candidate repository must be clean"
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
        or activation["decision"][
            "automatic_promotion_authorized"
        ] is not False
        or activation["decision"][
            "production_write_authorized"
        ] is not False
    ):
        raise PromotionHandoffGovernanceError(
            "P5-D2 activation crossed publication boundary"
        )

    return activation


def _validate_evaluator_report(
    report: dict[str, Any],
    *,
    candidate_head: str,
    candidate_tree: str,
) -> str:
    if not isinstance(report, dict):
        raise PromotionHandoffGovernanceError(
            "evaluator report must be object"
        )

    required_identity = {
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "candidate_head": candidate_head,
        "candidate_tree": candidate_tree,
    }
    for key, expected in required_identity.items():
        if report.get(key) != expected:
            raise PromotionHandoffGovernanceError(
                f"evaluator identity mismatch: {key}"
            )

    if (
        report.get("real_vault_modified") is not False
        or report.get("current_pointer_created") is not False
        or report.get(
            "production_promotion_authorized"
        ) is not False
    ):
        raise PromotionHandoffGovernanceError(
            "evaluator crossed publication boundary"
        )

    if (
        report.get("live_projection_head_before")
        != report.get("live_projection_head_after")
    ):
        raise PromotionHandoffGovernanceError(
            "evaluator changed live projection head"
        )

    outcome = report.get("outcome")

    if outcome == "REJECTED":
        if (
            not isinstance(
                report.get("failure_code"),
                str,
            )
            or not report["failure_code"]
            or report.get(
                "p5d2_result_event_emitted"
            ) is not True
        ):
            raise PromotionHandoffGovernanceError(
                "invalid REJECTED evaluator report"
            )
        return outcome

    if outcome == "BLOCKED":
        if (
            not isinstance(
                report.get("failure_code"),
                str,
            )
            or not report["failure_code"]
            or report.get(
                "p5d2_result_event_emitted"
            ) is not False
        ):
            raise PromotionHandoffGovernanceError(
                "invalid BLOCKED evaluator report"
            )
        return outcome

    if outcome != "QUALIFIED":
        raise PromotionHandoffGovernanceError(
            "unknown evaluator outcome"
        )

    if (
        report.get("failure_code") is not None
        or report.get(
            "p5d2_result_event_emitted"
        ) is not True
        or report.get(
            "candidate_generation_verification_status"
        ) != "PASS_SEALED_UNPROMOTED"
        or report.get(
            "projection_a_tree_digest_sha256"
        )
        != report.get(
            "projection_b_tree_digest_sha256"
        )
    ):
        raise PromotionHandoffGovernanceError(
            "QUALIFIED evaluator report invalid"
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
    ):
        _require_sha256(
            report.get(field),
            field,
        )

    return outcome


def _load_json(path: Path) -> dict[str, Any]:
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
        raise PromotionHandoffBlockedError(
            f"JSON evidence unavailable: {path.name}"
        ) from exc

    if not isinstance(value, dict):
        raise PromotionHandoffGovernanceError(
            f"JSON object required: {path.name}"
        )
    return value


def _validate_build_counts(
    workspace: Path,
) -> None:
    manifests = []
    for name in ("build-a", "build-b"):
        manifests.append(
            _load_json(
                workspace
                / name
                / "generated"
                / "manifests"
                / "build-manifest.json"
            )
        )

    for manifest in manifests:
        if (
            manifest.get(
                "metadata_only_body_read_count"
            )
            != 0
        ):
            raise PromotionHandoffGovernanceError(
                "METADATA_ONLY body read detected"
            )
        if (
            manifest.get("artifact_record_count")
            != manifest.get("source_record_count")
        ):
            raise PromotionHandoffGovernanceError(
                "artifact/source count mismatch"
            )

    fields = (
        "source_record_count",
        "artifact_record_count",
        "metadata_only_body_read_count",
    )
    for field in fields:
        if manifests[0].get(field) != (
            manifests[1].get(field)
        ):
            raise PromotionHandoffGovernanceError(
                f"Build A/B count mismatch: {field}"
            )


def _package_byte_tree_digest(
    package_root: Path,
) -> str:
    root = _resolve(package_root)
    if not root.exists() or not root.is_dir():
        raise PromotionHandoffBlockedError(
            "package root unavailable"
        )

    if _is_reparse_or_link(root):
        raise PromotionHandoffGovernanceError(
            "package root alias forbidden"
        )

    rows: list[list[Any]] = []

    try:
        paths = sorted(
            root.rglob("*"),
            key=lambda p: p.relative_to(
                root
            ).as_posix(),
        )
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            "package enumeration unavailable"
        ) from exc

    for path in paths:
        relative = path.relative_to(
            root
        ).as_posix()

        if _is_reparse_or_link(path):
            raise PromotionHandoffGovernanceError(
                f"package alias forbidden: {relative}"
            )

        try:
            info = path.stat()
        except OSError as exc:
            raise PromotionHandoffBlockedError(
                f"package stat unavailable: {relative}"
            ) from exc

        if stat.S_ISDIR(info.st_mode):
            rows.append(
                ["D", relative]
            )
            continue

        if not stat.S_ISREG(info.st_mode):
            raise PromotionHandoffGovernanceError(
                f"package entry is not regular: {relative}"
            )

        _assert_regular_single_link(path)

        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise PromotionHandoffBlockedError(
                f"package read unavailable: {relative}"
            ) from exc

        rows.append(
            [
                "F",
                relative,
                len(raw),
                _sha256_bytes(raw),
            ]
        )

    return _sha256_bytes(
        _canonical_json_bytes(
            rows,
            terminal_lf=False,
        )
    )


def _tree_fingerprint(
    root: Path,
) -> str:
    return _package_byte_tree_digest(root)


def _copy_package_exact(
    source_root: Path,
    destination_root: Path,
) -> None:
    source = _resolve(source_root)
    destination = _resolve(
        destination_root
    )

    if destination.exists():
        raise PromotionHandoffBlockedError(
            "destination package already exists"
        )

    if _is_reparse_or_link(source):
        raise PromotionHandoffGovernanceError(
            "source package alias forbidden"
        )

    try:
        destination.mkdir()
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            "destination package creation unavailable"
        ) from exc

    paths = sorted(
        source.rglob("*"),
        key=lambda p: p.relative_to(
            source
        ).as_posix(),
    )

    for path in paths:
        relative = path.relative_to(source)
        target = destination / relative

        if _is_reparse_or_link(path):
            raise PromotionHandoffGovernanceError(
                "source package alias forbidden"
            )

        try:
            info = path.stat()
        except OSError as exc:
            raise PromotionHandoffBlockedError(
                "source package stat unavailable"
            ) from exc

        if stat.S_ISDIR(info.st_mode):
            try:
                target.mkdir()
            except OSError as exc:
                raise PromotionHandoffBlockedError(
                    "destination directory creation unavailable"
                ) from exc
            continue

        _assert_regular_single_link(path)

        try:
            raw = path.read_bytes()
            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            with target.open("xb") as handle:
                handle.write(raw)
        except OSError as exc:
            raise PromotionHandoffBlockedError(
                "byte-exact package copy unavailable"
            ) from exc

        _assert_regular_single_link(target)


def _generation_manifest(
    package_root: Path,
) -> dict[str, Any]:
    path = (
        package_root
        / "_atds_generation"
        / "generation-manifest.json"
    )
    return _load_json(path)


def _cross_check_package_identity(
    *,
    evaluator_report: dict[str, Any],
    descriptor: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    expected_pairs = (
        (
            descriptor.get("candidate_head"),
            evaluator_report.get("candidate_head"),
            "candidate_head",
        ),
        (
            descriptor.get("candidate_tree"),
            evaluator_report.get("candidate_tree"),
            "candidate_tree",
        ),
        (
            descriptor.get(
                "candidate_generation_digest_sha256"
            ),
            evaluator_report.get(
                "candidate_generation_digest_sha256"
            ),
            "candidate_generation_digest_sha256",
        ),
        (
            descriptor.get(
                "projection_tree_digest_sha256"
            ),
            evaluator_report.get(
                "projection_a_tree_digest_sha256"
            ),
            "projection_tree_digest_sha256",
        ),
        (
            descriptor.get(
                "semantic_bridge_digest_sha256"
            ),
            evaluator_report.get(
                "semantic_bridge_digest_sha256"
            ),
            "semantic_bridge_digest_sha256",
        ),
        (
            descriptor.get(
                "semantic_record_digest_sha256"
            ),
            evaluator_report.get(
                "semantic_record_digest_sha256"
            ),
            "semantic_record_digest_sha256",
        ),
        (
            descriptor.get(
                "breaker_manifest_digest_sha256"
            ),
            evaluator_report.get(
                "projection_breaker_manifest_digest_sha256"
            ),
            "breaker_manifest_digest_sha256",
        ),
        (
            descriptor.get(
                "breaker_result_digest_sha256"
            ),
            evaluator_report.get(
                "projection_breaker_result_digest_sha256"
            ),
            "breaker_result_digest_sha256",
        ),
    )

    for actual, expected, field in expected_pairs:
        if actual != expected:
            raise PromotionHandoffGovernanceError(
                f"package/evaluator identity mismatch: {field}"
            )

    manifest_pairs = (
        (
            manifest.get(
                "dynamic_inventory_digest_sha256"
            ),
            evaluator_report.get(
                "dynamic_inventory_digest_sha256"
            ),
            "dynamic_inventory_digest_sha256",
        ),
        (
            manifest.get(
                "determinism_evidence_digest_sha256"
            ),
            evaluator_report.get(
                "determinism_evidence_digest_sha256"
            ),
            "determinism_evidence_digest_sha256",
        ),
        (
            manifest.get("repository"),
            EXPECTED_REPOSITORY,
            "repository",
        ),
        (
            manifest.get("branch"),
            EXPECTED_BRANCH,
            "branch",
        ),
    )

    for actual, expected, field in manifest_pairs:
        if actual != expected:
            raise PromotionHandoffGovernanceError(
                f"generation/evaluator identity mismatch: {field}"
            )


def _record_from(
    *,
    evaluator_report: dict[str, Any],
    descriptor: dict[str, Any],
    manifest: dict[str, Any],
    package_byte_tree_digest_sha256: str,
) -> dict[str, Any]:
    record = {
        "schema": HANDOFF_SCHEMA,
        "source_repository": EXPECTED_REPOSITORY,
        "source_branch": EXPECTED_BRANCH,
        "candidate_head":
            evaluator_report["candidate_head"],
        "candidate_tree":
            evaluator_report["candidate_tree"],
        "generation_id":
            descriptor["generation_id"],
        "candidate_generation_digest_sha256":
            descriptor[
                "candidate_generation_digest_sha256"
            ],
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
        "projection_tree_digest_sha256":
            evaluator_report[
                "projection_a_tree_digest_sha256"
            ],
        "breaker_manifest_digest_sha256":
            evaluator_report[
                "projection_breaker_manifest_digest_sha256"
            ],
        "breaker_result_digest_sha256":
            evaluator_report[
                "projection_breaker_result_digest_sha256"
            ],
        "determinism_evidence_digest_sha256":
            evaluator_report[
                "determinism_evidence_digest_sha256"
            ],
        "payload_file_map_digest_sha256":
            descriptor[
                "payload_file_map_digest_sha256"
            ],
        "package_byte_tree_digest_sha256":
            package_byte_tree_digest_sha256,
        "p5d3c2_package_verification_status":
            descriptor["verification_status"],
        "handoff_contract_blob":
            HANDOFF_CONTRACT_BLOB,
        "publication_authorized": False,
        "current_pointer_mutation_authorized": False,
        "real_vault_write_authorized": False,
        "promotion_confirmed_event_authorized": False,
        "handoff_status": "READY_UNAUTHORIZED",
    }

    if frozenset(record) != _HANDOFF_FIELDS:
        raise PromotionHandoffGovernanceError(
            "handoff record field set mismatch"
        )

    return record


def _write_exclusive(
    path: Path,
    raw: bytes,
) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(raw)
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            f"exclusive write unavailable: {path.name}"
        ) from exc

    _assert_regular_single_link(path)


def _verify_record_against_package(
    *,
    record: dict[str, Any],
    descriptor: dict[str, Any],
    manifest: dict[str, Any],
    package_byte_tree_digest_sha256: str,
) -> None:
    if frozenset(record) != _HANDOFF_FIELDS:
        raise PromotionHandoffGovernanceError(
            "handoff record exact field set mismatch"
        )

    if record.get("schema") != HANDOFF_SCHEMA:
        raise PromotionHandoffGovernanceError(
            "handoff schema mismatch"
        )

    authority = (
        "publication_authorized",
        "current_pointer_mutation_authorized",
        "real_vault_write_authorized",
        "promotion_confirmed_event_authorized",
    )
    if any(
        record.get(field) is not False
        for field in authority
    ):
        raise PromotionHandoffGovernanceError(
            "handoff publication authority must remain false"
        )

    if record.get("handoff_status") != (
        "READY_UNAUTHORIZED"
    ):
        raise PromotionHandoffGovernanceError(
            "handoff status mismatch"
        )

    expected = {
        "source_repository":
            manifest.get("repository"),
        "source_branch":
            manifest.get("branch"),
        "candidate_head":
            descriptor.get("candidate_head"),
        "candidate_tree":
            descriptor.get("candidate_tree"),
        "generation_id":
            descriptor.get("generation_id"),
        "candidate_generation_digest_sha256":
            descriptor.get(
                "candidate_generation_digest_sha256"
            ),
        "dynamic_inventory_digest_sha256":
            manifest.get(
                "dynamic_inventory_digest_sha256"
            ),
        "semantic_bridge_digest_sha256":
            descriptor.get(
                "semantic_bridge_digest_sha256"
            ),
        "semantic_record_digest_sha256":
            descriptor.get(
                "semantic_record_digest_sha256"
            ),
        "projection_tree_digest_sha256":
            descriptor.get(
                "projection_tree_digest_sha256"
            ),
        "breaker_manifest_digest_sha256":
            descriptor.get(
                "breaker_manifest_digest_sha256"
            ),
        "breaker_result_digest_sha256":
            descriptor.get(
                "breaker_result_digest_sha256"
            ),
        "determinism_evidence_digest_sha256":
            manifest.get(
                "determinism_evidence_digest_sha256"
            ),
        "payload_file_map_digest_sha256":
            descriptor.get(
                "payload_file_map_digest_sha256"
            ),
        "package_byte_tree_digest_sha256":
            package_byte_tree_digest_sha256,
        "p5d3c2_package_verification_status":
            descriptor.get(
                "verification_status"
            ),
        "handoff_contract_blob":
            HANDOFF_CONTRACT_BLOB,
    }

    for field, value in expected.items():
        if record.get(field) != value:
            raise PromotionHandoffGovernanceError(
                f"handoff/package identity mismatch: {field}"
            )

    if record.get("source_repository") != (
        EXPECTED_REPOSITORY
    ):
        raise PromotionHandoffGovernanceError(
            "handoff repository mismatch"
        )
    if record.get("source_branch") != EXPECTED_BRANCH:
        raise PromotionHandoffGovernanceError(
            "handoff branch mismatch"
        )


def verify_promotion_handoff(
    handoff_root: Path,
    *,
    live_vault_root: Path,
) -> dict[str, Any]:
    _verify_tooling_identity()

    root = _resolve(handoff_root)
    vault = _resolve(live_vault_root)

    if not root.exists() or not root.is_dir():
        raise PromotionHandoffBlockedError(
            "handoff root unavailable"
        )
    if not vault.exists() or not vault.is_dir():
        raise PromotionHandoffBlockedError(
            "live Vault root unavailable"
        )

    _assert_alias_free_chain(root)
    _assert_alias_free_chain(vault)

    if _intersects(root, vault):
        raise PromotionHandoffGovernanceError(
            "handoff overlaps live Vault"
        )

    try:
        top_level = {
            path.name
            for path in root.iterdir()
        }
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            "handoff layout unavailable"
        ) from exc

    if top_level != {
        "package",
        "PROMOTION-HANDOFF.json",
    }:
        raise PromotionHandoffGovernanceError(
            "handoff exact wrapper layout mismatch"
        )

    handoff_path = (
        root / "PROMOTION-HANDOFF.json"
    )
    _assert_regular_single_link(
        handoff_path
    )

    try:
        raw = handoff_path.read_bytes()
        record = json.loads(
            raw.decode("utf-8")
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise PromotionHandoffGovernanceError(
            "handoff record unreadable"
        ) from exc

    if not isinstance(record, dict):
        raise PromotionHandoffGovernanceError(
            "handoff record must be object"
        )

    if raw != _canonical_json_bytes(record):
        raise PromotionHandoffGovernanceError(
            "handoff record is not canonical JSON"
        )

    package = root / "package"

    try:
        descriptor = verify_candidate_generation(
            package,
            forbidden_roots=(vault,),
        )
    except CandidateGenerationInfrastructureError as exc:
        raise PromotionHandoffBlockedError(
            "copied package reverification unavailable"
        ) from exc
    except CandidateGenerationInvalidError as exc:
        raise PromotionHandoffGovernanceError(
            "copied package reverification failed"
        ) from exc

    package_digest = (
        _package_byte_tree_digest(
            package
        )
    )
    manifest = _generation_manifest(
        package
    )

    _verify_record_against_package(
        record=record,
        descriptor=descriptor,
        manifest=manifest,
        package_byte_tree_digest_sha256=(
            package_digest
        ),
    )

    return {
        "schema": REPORT_SCHEMA,
        "status": SUCCESS_STATUS,
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
        "package_byte_tree_digest_sha256":
            package_digest,
        "package_status":
            descriptor["verification_status"],
        "handoff_status":
            record["handoff_status"],
        "publication_authorized": False,
        "current_pointer_created": False,
        "real_vault_modified": False,
        "production_promotion_authorized": False,
        "p5d2_promotion_confirmed_emitted": False,
    }


def run_finite_promotion_handoff(
    *,
    candidate_head: str,
    candidate_tree: str,
    candidate_repo_root: Path,
    evaluation_workspace_root: Path,
    promotion_staging_root: Path,
    live_vault_root: Path,
) -> dict[str, Any]:
    _verify_tooling_identity()

    head = _require_head(
        candidate_head,
        "candidate_head",
    )
    tree = _require_head(
        candidate_tree,
        "candidate_tree",
    )

    (
        repo,
        workspace,
        staging,
        vault,
    ) = _validate_environment(
        candidate_repo_root=candidate_repo_root,
        evaluation_workspace_root=(
            evaluation_workspace_root
        ),
        promotion_staging_root=(
            promotion_staging_root
        ),
        live_vault_root=live_vault_root,
    )

    _validate_candidate_repository(
        repo,
        head,
        tree,
    )

    vault_before = _tree_fingerprint(
        vault
    )

    activation = _activation(
        head
    )

    try:
        evaluator_report = (
            evaluate_candidate_finitely(
                activation_tick_result=activation,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                forbidden_roots=(
                    staging,
                    vault,
                ),
            )
        )
    except FiniteCandidateEvaluatorError as exc:
        raise PromotionHandoffGovernanceError(
            "qualified finite evaluator raised"
        ) from exc

    outcome = _validate_evaluator_report(
        evaluator_report,
        candidate_head=head,
        candidate_tree=tree,
    )

    if outcome == "REJECTED":
        return {
            "schema": REPORT_SCHEMA,
            "status": "FAIL_CANDIDATE_REJECTED",
            "candidate_head": head,
            "candidate_tree": tree,
            "failure_code":
                evaluator_report["failure_code"],
            "evaluator_outcome": "REJECTED",
            "real_vault_modified": False,
            "current_pointer_created": False,
            "production_promotion_authorized": False,
            "p5d2_promotion_confirmed_emitted": False,
        }

    if outcome == "BLOCKED":
        return {
            "schema": REPORT_SCHEMA,
            "status": "BLOCKED_CANDIDATE_EVALUATION",
            "candidate_head": head,
            "candidate_tree": tree,
            "failure_code":
                evaluator_report["failure_code"],
            "evaluator_outcome": "BLOCKED",
            "real_vault_modified": False,
            "current_pointer_created": False,
            "production_promotion_authorized": False,
            "p5d2_promotion_confirmed_emitted": False,
        }

    _validate_build_counts(
        workspace
    )

    source_package = (
        workspace
        / "candidate-package"
    )

    try:
        source_descriptor = (
            verify_candidate_generation(
                source_package,
                forbidden_roots=(
                    repo,
                    staging,
                    vault,
                ),
            )
        )
    except CandidateGenerationInfrastructureError as exc:
        raise PromotionHandoffBlockedError(
            "source package verification unavailable"
        ) from exc
    except CandidateGenerationInvalidError as exc:
        raise PromotionHandoffGovernanceError(
            "source package verification failed"
        ) from exc

    if source_descriptor.get(
        "verification_status"
    ) != "PASS_SEALED_UNPROMOTED":
        raise PromotionHandoffGovernanceError(
            "source package is not SEALED_UNPROMOTED"
        )

    source_manifest = _generation_manifest(
        source_package
    )

    _cross_check_package_identity(
        evaluator_report=evaluator_report,
        descriptor=source_descriptor,
        manifest=source_manifest,
    )

    source_digest = (
        _package_byte_tree_digest(
            source_package
        )
    )

    generation_id = (
        source_descriptor["generation_id"]
    )

    packages_root = staging / "packages"
    target = (
        packages_root
        / generation_id
    )

    if target.exists():
        raise PromotionHandoffBlockedError(
            "BLOCKED_HANDOFF_TARGET_EXISTS"
        )

    try:
        packages_root.mkdir(
            exist_ok=True,
        )
    except OSError as exc:
        raise PromotionHandoffBlockedError(
            "promotion packages root unavailable"
        ) from exc

    if not packages_root.is_dir():
        raise PromotionHandoffGovernanceError(
            "promotion packages root is not directory"
        )

    _assert_alias_free_chain(
        packages_root
    )

    completed = False

    try:
        target.mkdir()
        destination_package = (
            target / "package"
        )

        _copy_package_exact(
            source_package,
            destination_package,
        )

        try:
            destination_descriptor = (
                verify_candidate_generation(
                    destination_package,
                    forbidden_roots=(
                        repo,
                        workspace,
                        vault,
                    ),
                )
            )
        except CandidateGenerationInfrastructureError as exc:
            raise PromotionHandoffBlockedError(
                "destination package verification unavailable"
            ) from exc
        except CandidateGenerationInvalidError as exc:
            raise PromotionHandoffGovernanceError(
                "destination package verification failed"
            ) from exc

        if destination_descriptor != (
            source_descriptor
        ):
            raise PromotionHandoffGovernanceError(
                "source/destination verifier descriptors differ"
            )

        destination_digest = (
            _package_byte_tree_digest(
                destination_package
            )
        )
        if destination_digest != source_digest:
            raise PromotionHandoffGovernanceError(
                "source/destination package byte-tree digest differs"
            )

        destination_manifest = (
            _generation_manifest(
                destination_package
            )
        )
        _cross_check_package_identity(
            evaluator_report=evaluator_report,
            descriptor=destination_descriptor,
            manifest=destination_manifest,
        )

        record = _record_from(
            evaluator_report=evaluator_report,
            descriptor=destination_descriptor,
            manifest=destination_manifest,
            package_byte_tree_digest_sha256=(
                destination_digest
            ),
        )

        _write_exclusive(
            target / "PROMOTION-HANDOFF.json",
            _canonical_json_bytes(
                record
            ),
        )

        verified = verify_promotion_handoff(
            target,
            live_vault_root=vault,
        )

        if verified["generation_id"] != generation_id:
            raise PromotionHandoffGovernanceError(
                "post-write handoff generation mismatch"
            )

        vault_after = _tree_fingerprint(
            vault
        )
        if vault_after != vault_before:
            raise PromotionHandoffGovernanceError(
                "real Vault changed during handoff"
            )

        completed = True

        return {
            **verified,
            "evaluator_outcome": "QUALIFIED",
            "package_status":
                source_descriptor[
                    "verification_status"
                ],
            "copied_package_status":
                destination_descriptor[
                    "verification_status"
                ],
        }

    finally:
        if not completed and target.exists():
            try:
                shutil.rmtree(target)
            except OSError as exc:
                raise PromotionHandoffBlockedError(
                    "partial handoff cleanup unavailable"
                ) from exc

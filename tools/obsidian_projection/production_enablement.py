from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path
from typing import Any

from .live_publication_transaction import (
    EXPECTED_BRANCH,
    EXPECTED_REPOSITORY,
    PUBLICATION_MANIFEST_SCHEMA,
    REAL_VAULT,
    _assert_alias_free_chain,
    _assert_regular_single_link,
    _current_bytes,
    _index_bytes,
    _intersects,
    _is_reparse_or_link,
    _operation_sequence_digest,
    _publication_manifest,
    _sha256_bytes,
    _sha256_value,
    _validate_current_pointer,
    _verified_handoff,
    _virtual_target_digest,
)
from .persistent_production_handoff import (
    PERSISTENT_STAGING,
)


class ProductionEnablementError(RuntimeError):
    pass


class ProductionEnablementBlockedError(
    ProductionEnablementError
):
    pass


class ProductionEnablementGovernanceError(
    ProductionEnablementError
):
    pass


CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)
QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (
    "b8875f8973ddf1076ff20d8e725ce04abbb814a8"
)
PRODUCTION_ENABLEMENT_PIN_REQUALIFICATION_CONTRACT_BLOB = (
    "6f938414059b2bde425ea17febfbb77635fd91e5"
)
EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (
    "2fb34e1c04b4dd32d19b85b488d89f8a702204d0"
)
STAGEA_PERSISTENT_HANDOFF_BINDING_AMENDMENT_CONTRACT_BLOB = (
    "f2625a98ac53c737c884f5d276bb41f51ce5f498"
)
STAGEA_EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (
    "4a056c3a27796043b833c803a18a17c621b79ab0"
)
PERSISTENT_HANDOFF_IMPLEMENTATION_BLOB = (
    "375607d88bc926e4fd4c297ddc6fedba5506642a"
)

PLAN_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_REAL_LIVE_PUBLICATION_PLAN_V0_1"
)
APPROVAL_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_PRODUCTION_PLAN_APPROVAL_V0_1"
)
APPROVAL_ACTION = (
    "APPROVE_ONE_EXACT_REAL_LIVE_PUBLICATION_PLAN_"
    "FOR_FUTURE_EXECUTION_REVIEW"
)
SNAPSHOT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_REAL_VAULT_SNAPSHOT_V0_1"
)
APPROVAL_RECEIPT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_STAGE_A_APPROVAL_CONSUMPTION_V0_1"
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
        "real_vault_resolved_path",
        "qualified_production_enablement_contract_blob",
        "qualified_live_publication_implementation_blob",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "candidate_generation_digest_sha256",
        "handoff_package_byte_tree_digest_sha256",
        "handoff_record_sha256",
        "publication_mode",
        "expected_current_state",
        "expected_current_sha256",
        "expected_current_generation_id",
        "expected_current_generation_digest_sha256",
        "expected_current_tmp_state",
        "expected_target_state",
        "target_generation_relative_path",
        "planned_current_sha256",
        "planned_publication_generation_digest_sha256",
        "operation_sequence_digest_sha256",
        "real_vault_before_tree_digest_sha256",
    }
)

_APPROVAL_FIELDS = frozenset(
    {
        "schema",
        "authorized_action",
        "plan_digest_sha256",
        "candidate_head",
        "candidate_tree",
        "generation_id",
        "publication_mode",
        "expected_current_state",
        "expected_current_sha256",
        "expected_current_tmp_state",
        "expected_target_state",
        "one_shot_nonce",
    }
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _git_blob(relative: str) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "rev-parse",
                f"HEAD:{relative}",
            ],
            cwd=str(_repo_root()),
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
        raise ProductionEnablementBlockedError(
            "qualified tooling identity unavailable"
        ) from exc

    if completed.returncode != 0:
        raise ProductionEnablementBlockedError(
            "qualified tooling commit unavailable"
        )
    return completed.stdout.strip()


def _worktree_blob(relative: str) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "hash-object",
                "--no-filters",
                relative,
            ],
            cwd=str(_repo_root()),
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
        raise ProductionEnablementBlockedError(
            "qualified tooling worktree identity unavailable"
        ) from exc

    if completed.returncode != 0:
        raise ProductionEnablementBlockedError(
            "qualified tooling worktree unavailable"
        )
    return completed.stdout.strip()


_TOOLING = {
    (
        "tools/obsidian_projection/"
        "production_enablement_gate_contract_v0_1.json"
    ): CONTRACT_BLOB,
    (
        "tools/obsidian_projection/"
        "production_enablement_dependency_pin_requalification_contract_v0_1.json"
    ): PRODUCTION_ENABLEMENT_PIN_REQUALIFICATION_CONTRACT_BLOB,
    (
        "tools/obsidian_projection/"
        "live_publication_transaction.py"
    ): EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
}

_STAGEA_TOOLING = {
    **_TOOLING,
    (
        "tools/obsidian_projection/"
        "p5d3g_stagea_persistent_handoff_verifier_binding_amendment_contract_v0_1.json"
    ): STAGEA_PERSISTENT_HANDOFF_BINDING_AMENDMENT_CONTRACT_BLOB,
    (
        "tools/obsidian_projection/"
        "persistent_production_handoff.py"
    ): PERSISTENT_HANDOFF_IMPLEMENTATION_BLOB,
    (
        "tools/obsidian_projection/"
        "live_publication_transaction.py"
    ): STAGEA_EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
}


def _verify_tooling_identity() -> None:
    for relative, blob in _STAGEA_TOOLING.items():
        if _git_blob(relative) != blob:
            raise ProductionEnablementGovernanceError(
                f"qualified tooling commit mismatch: {relative}"
            )
        if _worktree_blob(relative) != blob:
            raise ProductionEnablementGovernanceError(
                f"qualified tooling worktree mismatch: {relative}"
            )


def _resolve(path: Path) -> Path:
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise ProductionEnablementBlockedError(
            "path resolution unavailable"
        ) from exc


def _validate_promotion_staging_root(
    promotion_staging_root: Path | None,
) -> Path | None:
    if promotion_staging_root is None:
        return None

    supplied = Path(promotion_staging_root)
    expected = Path(PERSISTENT_STAGING)
    if str(supplied) != str(expected):
        raise ProductionEnablementGovernanceError(
            "persistent staging lexical identity mismatch"
        )

    staging = _resolve(supplied)
    exact = _resolve(expected)
    if staging != exact:
        raise ProductionEnablementGovernanceError(
            "persistent staging resolved identity mismatch"
        )
    return staging


def _validate_real_vault(
    real_vault_root: Path,
) -> Path:
    supplied = Path(real_vault_root)
    expected = Path(REAL_VAULT)

    if str(supplied) != str(expected):
        raise ProductionEnablementGovernanceError(
            "real Vault lexical identity mismatch"
        )

    live = _resolve(supplied)
    exact = _resolve(expected)

    if live != exact:
        raise ProductionEnablementGovernanceError(
            "real Vault resolved identity mismatch"
        )
    if not live.is_dir():
        raise ProductionEnablementBlockedError(
            "real Vault root unavailable"
        )

    try:
        _assert_alias_free_chain(live)
    except Exception as exc:
        raise ProductionEnablementGovernanceError(
            "real Vault alias/reparse identity forbidden"
        ) from exc

    if (live / ".git").exists():
        raise ProductionEnablementGovernanceError(
            "real Vault may not be a Git repository root"
        )

    return live


def _tree_digest(
    live: Path,
) -> tuple[str, int, int]:
    rows: list[list[Any]] = []
    file_count = 0
    directory_count = 0

    try:
        paths = sorted(
            live.rglob("*"),
            key=lambda p: p.relative_to(
                live
            ).as_posix(),
        )
    except OSError as exc:
        raise ProductionEnablementBlockedError(
            "real Vault enumeration unavailable"
        ) from exc

    for path in paths:
        relative = path.relative_to(
            live
        ).as_posix()

        try:
            if _is_reparse_or_link(path):
                raise ProductionEnablementGovernanceError(
                    f"real Vault alias/reparse forbidden: {relative}"
                )
            info = path.stat()
        except ProductionEnablementError:
            raise
        except Exception as exc:
            raise ProductionEnablementBlockedError(
                f"real Vault stat unavailable: {relative}"
            ) from exc

        if stat.S_ISDIR(info.st_mode):
            directory_count += 1
            rows.append(["D", relative])
            continue

        if not stat.S_ISREG(info.st_mode):
            raise ProductionEnablementGovernanceError(
                f"real Vault non-regular path forbidden: {relative}"
            )

        links = getattr(info, "st_nlink", None)
        if links is None:
            raise ProductionEnablementBlockedError(
                f"real Vault hard-link count unavailable: {relative}"
            )
        if int(links) != 1:
            raise ProductionEnablementGovernanceError(
                f"real Vault hard-link alias forbidden: {relative}"
            )

        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise ProductionEnablementBlockedError(
                f"real Vault file read unavailable: {relative}"
            ) from exc

        file_count += 1
        rows.append(
            [
                "F",
                relative,
                len(raw),
                hashlib.sha256(raw).hexdigest(),
            ]
        )

    digest = _sha256_value(rows)
    return digest, file_count, directory_count


def snapshot_real_vault(
    real_vault_root: Path,
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_real_vault(
        real_vault_root
    )

    tree_digest, files, directories = (
        _tree_digest(live)
    )

    pointer = live / "CURRENT.md"
    if pointer.exists():
        _assert_regular_single_link(pointer)
        try:
            current_raw = pointer.read_bytes()
        except OSError as exc:
            raise ProductionEnablementBlockedError(
                "CURRENT.md snapshot unavailable"
            ) from exc
        current_state = "PRESENT"
        current_sha = _sha256_bytes(
            current_raw
        )
    else:
        current_state = "ABSENT"
        current_sha = None

    current_tmp_state = (
        "PRESENT"
        if (live / "CURRENT.tmp").exists()
        else "ABSENT"
    )

    return {
        "schema": SNAPSHOT_SCHEMA,
        "real_vault_resolved_path":
            str(live),
        "content_tree_digest_sha256":
            tree_digest,
        "file_count": files,
        "directory_count": directories,
        "current_state": current_state,
        "current_sha256": current_sha,
        "current_tmp_state":
            current_tmp_state,
    }


def prove_zero_real_vault_mutation(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(before, dict) or not isinstance(
        after,
        dict,
    ):
        raise ProductionEnablementGovernanceError(
            "zero-mutation snapshots must be objects"
        )
    if before.get("schema") != SNAPSHOT_SCHEMA:
        raise ProductionEnablementGovernanceError(
            "before snapshot schema mismatch"
        )
    if after.get("schema") != SNAPSHOT_SCHEMA:
        raise ProductionEnablementGovernanceError(
            "after snapshot schema mismatch"
        )
    if before != after:
        raise ProductionEnablementGovernanceError(
            "FAIL_ZERO_REAL_VAULT_MUTATION_PROOF"
        )

    return {
        "status":
            "PASS_ZERO_REAL_VAULT_MUTATION_VERIFIED",
        "real_vault_resolved_path":
            before["real_vault_resolved_path"],
        "before_tree_digest_sha256":
            before[
                "content_tree_digest_sha256"
            ],
        "after_tree_digest_sha256":
            after[
                "content_tree_digest_sha256"
            ],
        "current_state":
            before["current_state"],
        "current_sha256":
            before["current_sha256"],
        "current_tmp_state":
            before["current_tmp_state"],
        "unchanged": True,
    }


def _require_head(value: Any, field: str) -> str:
    if (
        not isinstance(value, str)
        or _HEAD_RE.fullmatch(value) is None
    ):
        raise ProductionEnablementGovernanceError(
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
        raise ProductionEnablementGovernanceError(
            f"{field} must be lowercase SHA-256"
        )
    return value


def _require_generation_id(value: Any) -> str:
    if (
        not isinstance(value, str)
        or _GENERATION_RE.fullmatch(value) is None
    ):
        raise ProductionEnablementGovernanceError(
            "generation_id invalid"
        )
    return value


def production_plan_digest(
    plan: dict[str, Any],
) -> str:
    if not isinstance(plan, dict):
        raise ProductionEnablementGovernanceError(
            "production plan must be object"
        )
    if frozenset(plan) != _PLAN_FIELDS:
        raise ProductionEnablementGovernanceError(
            "production plan exact field set mismatch"
        )
    if plan.get("schema") != PLAN_SCHEMA:
        raise ProductionEnablementGovernanceError(
            "production plan schema mismatch"
        )
    if plan.get("source_repository") != (
        EXPECTED_REPOSITORY
    ):
        raise ProductionEnablementGovernanceError(
            "production plan repository mismatch"
        )
    if plan.get("source_branch") != (
        EXPECTED_BRANCH
    ):
        raise ProductionEnablementGovernanceError(
            "production plan branch mismatch"
        )

    real_path = plan.get(
        "real_vault_resolved_path"
    )
    if not isinstance(real_path, str) or not real_path:
        raise ProductionEnablementGovernanceError(
            "production plan real Vault identity unavailable"
        )

    if plan.get(
        "qualified_production_enablement_contract_blob"
    ) != CONTRACT_BLOB:
        raise ProductionEnablementGovernanceError(
            "production plan contract blob mismatch"
        )
    if plan.get(
        "qualified_live_publication_implementation_blob"
    ) != EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB:
        raise ProductionEnablementGovernanceError(
            "production plan implementation blob mismatch"
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
        "real_vault_before_tree_digest_sha256",
    ):
        _require_sha256(
            plan.get(field),
            field,
        )

    if plan.get("publication_mode") not in {
        "BOOTSTRAP_NO_CURRENT",
        "REPLACE_EXISTING_CURRENT",
    }:
        raise ProductionEnablementGovernanceError(
            "production plan publication mode invalid"
        )

    current_state = plan.get(
        "expected_current_state"
    )
    if current_state not in {
        "ABSENT",
        "PRESENT_VALID",
    }:
        raise ProductionEnablementGovernanceError(
            "production plan current state invalid"
        )

    if current_state == "ABSENT":
        if any(
            plan.get(field) is not None
            for field in (
                "expected_current_sha256",
                "expected_current_generation_id",
                "expected_current_generation_digest_sha256",
            )
        ):
            raise ProductionEnablementGovernanceError(
                "absent CURRENT carries identity"
            )
    else:
        _require_sha256(
            plan.get("expected_current_sha256"),
            "expected_current_sha256",
        )
        _require_generation_id(
            plan.get(
                "expected_current_generation_id"
            )
        )
        _require_sha256(
            plan.get(
                "expected_current_generation_digest_sha256"
            ),
            "expected_current_generation_digest_sha256",
        )

    if plan.get(
        "expected_current_tmp_state"
    ) not in {"ABSENT", "PRESENT"}:
        raise ProductionEnablementGovernanceError(
            "CURRENT.tmp state invalid"
        )

    if plan.get("expected_target_state") != (
        "ABSENT"
    ):
        raise ProductionEnablementGovernanceError(
            "production target must be absent"
        )

    expected_relative = (
        "generations/"
        + plan["generation_id"]
    )
    if plan.get(
        "target_generation_relative_path"
    ) != expected_relative:
        raise ProductionEnablementGovernanceError(
            "target generation path mismatch"
        )

    return _sha256_value(plan)


def build_real_live_publication_plan(
    *,
    handoff_root: Path,
    real_vault_root: Path,
    promotion_staging_root: Path | None = None,
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_real_vault(
        real_vault_root
    )
    staging = _validate_promotion_staging_root(
        promotion_staging_root
    )
    before = snapshot_real_vault(live)

    try:
        (
            handoff,
            verified,
            record,
            handoff_raw,
        ) = _verified_handoff(
            handoff_root,
            live,
            promotion_staging_root=staging,
        )
    except Exception as exc:
        if isinstance(
            exc,
            ProductionEnablementError,
        ):
            raise
        raise ProductionEnablementGovernanceError(
            "FAIL_INVALID_P5D3F_HANDOFF"
        ) from exc

    generation_id = _require_generation_id(
        verified["generation_id"]
    )
    target = (
        live
        / "generations"
        / generation_id
    )
    if target.exists():
        raise ProductionEnablementBlockedError(
            "BLOCKED_TARGET_GENERATION_COLLISION"
        )

    manifest = _publication_manifest(record)
    manifest_raw = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
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
        try:
            current = _validate_current_pointer(
                live
            )
        except Exception as exc:
            raise ProductionEnablementGovernanceError(
                "production CURRENT invalid"
            ) from exc

        publication_mode = (
            "REPLACE_EXISTING_CURRENT"
        )
        current_state = "PRESENT_VALID"
        current_sha = current[
            "current_sha256"
        ]
        current_generation_id = current[
            "generation_id"
        ]
        current_generation_digest = current[
            "publication_generation_digest_sha256"
        ]
    else:
        publication_mode = (
            "BOOTSTRAP_NO_CURRENT"
        )
        current_state = "ABSENT"
        current_sha = None
        current_generation_id = None
        current_generation_digest = None

    current_tmp_state = (
        "PRESENT"
        if (live / "CURRENT.tmp").exists()
        else "ABSENT"
    )

    planned_current_raw = _current_bytes(
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

    plan = {
        "schema": PLAN_SCHEMA,
        "source_repository":
            record["source_repository"],
        "source_branch":
            record["source_branch"],
        "real_vault_resolved_path":
            str(live),
        "qualified_production_enablement_contract_blob":
            CONTRACT_BLOB,
        "qualified_live_publication_implementation_blob":
            EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
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
            _sha256_bytes(handoff_raw),
        "publication_mode":
            publication_mode,
        "expected_current_state":
            current_state,
        "expected_current_sha256":
            current_sha,
        "expected_current_generation_id":
            current_generation_id,
        "expected_current_generation_digest_sha256":
            current_generation_digest,
        "expected_current_tmp_state":
            current_tmp_state,
        "expected_target_state":
            "ABSENT",
        "target_generation_relative_path":
            (
                "generations/"
                + generation_id
            ),
        "planned_current_sha256":
            _sha256_bytes(
                planned_current_raw
            ),
        "planned_publication_generation_digest_sha256":
            wrapper_digest,
        "operation_sequence_digest_sha256":
            _operation_sequence_digest(),
        "real_vault_before_tree_digest_sha256":
            before[
                "content_tree_digest_sha256"
            ],
    }

    production_plan_digest(plan)

    after = snapshot_real_vault(live)
    proof = prove_zero_real_vault_mutation(
        before,
        after,
    )

    if (
        proof[
            "before_tree_digest_sha256"
        ]
        != plan[
            "real_vault_before_tree_digest_sha256"
        ]
    ):
        raise ProductionEnablementGovernanceError(
            "real Vault proof/plan digest mismatch"
        )

    return {
        "status":
            "PASS_REAL_LIVE_PUBLICATION_PLAN_READ_ONLY",
        "plan": plan,
        "plan_digest_sha256":
            production_plan_digest(plan),
        "zero_mutation_proof":
            proof,
        "stage_b_execution_authority":
            False,
    }


def _validate_control_root(
    control_root: Path,
    *,
    live: Path,
    handoff: Path,
) -> Path:
    try:
        control = control_root.resolve(
            strict=True
        )
    except OSError as exc:
        raise ProductionEnablementBlockedError(
            "control root unavailable"
        ) from exc

    if not control.is_dir():
        raise ProductionEnablementBlockedError(
            "control root must be directory"
        )

    try:
        _assert_alias_free_chain(control)
    except Exception as exc:
        raise ProductionEnablementGovernanceError(
            "control root alias/reparse forbidden"
        ) from exc

    if _intersects(control, live):
        raise ProductionEnablementGovernanceError(
            "control root overlaps real Vault"
        )
    if _intersects(control, handoff):
        raise ProductionEnablementGovernanceError(
            "control root overlaps retained handoff"
        )

    return control


def _validate_stage_a_approval(
    plan: dict[str, Any],
    approval: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    plan_digest = production_plan_digest(
        plan
    )

    if approval is None:
        raise ProductionEnablementBlockedError(
            "BLOCKED_STAGE_A_PLAN_APPROVAL"
        )
    if not isinstance(approval, dict):
        raise ProductionEnablementGovernanceError(
            "stage-A approval must be object"
        )
    if frozenset(approval) != (
        _APPROVAL_FIELDS
    ):
        raise ProductionEnablementGovernanceError(
            "stage-A approval exact field set mismatch"
        )
    if approval.get("schema") != (
        APPROVAL_SCHEMA
    ):
        raise ProductionEnablementGovernanceError(
            "stage-A approval schema mismatch"
        )
    if approval.get(
        "authorized_action"
    ) != APPROVAL_ACTION:
        raise ProductionEnablementGovernanceError(
            "stage-A approval action mismatch"
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
        "expected_current_state":
            plan["expected_current_state"],
        "expected_current_sha256":
            plan["expected_current_sha256"],
        "expected_current_tmp_state":
            plan["expected_current_tmp_state"],
        "expected_target_state":
            plan["expected_target_state"],
    }

    for field, value in expected.items():
        if approval.get(field) != value:
            raise ProductionEnablementGovernanceError(
                "FAIL_STAGE_A_PLAN_APPROVAL_MISMATCH"
            )

    nonce = approval.get(
        "one_shot_nonce"
    )
    if (
        not isinstance(nonce, str)
        or _NONCE_RE.fullmatch(nonce) is None
    ):
        raise ProductionEnablementGovernanceError(
            "stage-A approval nonce invalid"
        )

    digest = _sha256_value(
        approval
    )
    return approval, digest


def _assert_plan_prestate(
    live: Path,
    plan: dict[str, Any],
) -> None:
    snapshot = snapshot_real_vault(
        live
    )

    if (
        snapshot[
            "content_tree_digest_sha256"
        ]
        != plan[
            "real_vault_before_tree_digest_sha256"
        ]
    ):
        raise ProductionEnablementBlockedError(
            "BLOCKED_CURRENT_PRECONDITION_CHANGED"
        )

    if plan[
        "expected_current_state"
    ] == "ABSENT":
        if snapshot[
            "current_state"
        ] != "ABSENT":
            raise ProductionEnablementBlockedError(
                "BLOCKED_CURRENT_PRECONDITION_CHANGED"
            )
    else:
        if (
            snapshot[
                "current_state"
            ] != "PRESENT"
            or snapshot[
                "current_sha256"
            ]
            != plan[
                "expected_current_sha256"
            ]
        ):
            raise ProductionEnablementBlockedError(
                "BLOCKED_CURRENT_PRECONDITION_CHANGED"
            )

    if snapshot[
        "current_tmp_state"
    ] != plan[
        "expected_current_tmp_state"
    ]:
        raise ProductionEnablementBlockedError(
            "BLOCKED_CURRENT_PRECONDITION_CHANGED"
        )

    target = (
        live
        / plan[
            "target_generation_relative_path"
        ]
    )
    if target.exists():
        raise ProductionEnablementBlockedError(
            "BLOCKED_TARGET_PRECONDITION_CHANGED"
        )


def consume_stage_a_plan_approval(
    *,
    handoff_root: Path,
    real_vault_root: Path,
    control_root: Path,
    plan: dict[str, Any],
    approval: dict[str, Any] | None,
    promotion_staging_root: Path | None = None,
) -> dict[str, Any]:
    _verify_tooling_identity()
    live = _validate_real_vault(
        real_vault_root
    )
    staging = _validate_promotion_staging_root(
        promotion_staging_root
    )
    handoff = _resolve(
        handoff_root
    )
    control = _validate_control_root(
        control_root,
        live=live,
        handoff=handoff,
    )

    plan_digest = production_plan_digest(
        plan
    )
    if plan[
        "real_vault_resolved_path"
    ] != str(live):
        raise ProductionEnablementGovernanceError(
            "plan real Vault identity mismatch"
        )

    try:
        (
            _verified_root,
            verified,
            _record,
            handoff_raw,
        ) = _verified_handoff(
            handoff,
            live,
            promotion_staging_root=staging,
        )
    except Exception as exc:
        raise ProductionEnablementGovernanceError(
            "FAIL_INVALID_P5D3F_HANDOFF"
        ) from exc

    if (
        verified["candidate_head"]
        != plan["candidate_head"]
        or verified["candidate_tree"]
        != plan["candidate_tree"]
        or verified["generation_id"]
        != plan["generation_id"]
        or _sha256_bytes(handoff_raw)
        != plan["handoff_record_sha256"]
    ):
        raise ProductionEnablementGovernanceError(
            "retained handoff differs from approved plan"
        )

    before = snapshot_real_vault(live)
    _assert_plan_prestate(
        live,
        plan,
    )

    approval_value, approval_digest = (
        _validate_stage_a_approval(
            plan,
            approval,
        )
    )

    directory = (
        control
        / "stage-a-approvals"
    )
    try:
        directory.mkdir(
            exist_ok=True
        )
    except OSError as exc:
        raise ProductionEnablementBlockedError(
            "stage-A approval ledger unavailable"
        ) from exc

    marker = directory / (
        approval_value[
            "one_shot_nonce"
        ]
        + ".json"
    )
    payload = {
        "schema":
            APPROVAL_RECEIPT_SCHEMA,
        "plan_digest_sha256":
            plan_digest,
        "approval_digest_sha256":
            approval_digest,
        "one_shot_nonce":
            approval_value[
                "one_shot_nonce"
            ],
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "generation_id":
            plan["generation_id"],
        "stage_b_execution_authority":
            False,
    }

    raw = (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )

    try:
        with marker.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise ProductionEnablementBlockedError(
            "BLOCKED_STAGE_A_PLAN_APPROVAL_REUSE"
        ) from exc
    except OSError as exc:
        raise ProductionEnablementBlockedError(
            "stage-A approval consumption unavailable"
        ) from exc

    after = snapshot_real_vault(live)
    proof = prove_zero_real_vault_mutation(
        before,
        after,
    )

    return {
        "status":
            "PASS_STAGE_A_PLAN_APPROVAL_VALIDATED_ZERO_REAL_VAULT_MUTATION",
        "plan_digest_sha256":
            plan_digest,
        "approval_digest_sha256":
            approval_digest,
        "approval_receipt_path":
            str(marker),
        "zero_mutation_proof":
            proof,
        "unchanged": True,
        "stage_b_execution_authority":
            False,
    }

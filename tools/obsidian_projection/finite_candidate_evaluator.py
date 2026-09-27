from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable

from .candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
    CandidateGenerationInvalidError,
    VerifiedProjectionCandidate,
    stage_candidate_generation,
    verify_candidate_generation,
)
from .current_head_breakers import (
    CurrentHeadBreakerInfrastructureError,
    run_current_head_projection_breakers,
)
from .current_head_projection import (
    PROJECTION_CONTRACT_BLOB,
    CurrentHeadProjectionInfrastructureError,
    CurrentHeadProjectionInvalidError,
    build_current_head_projection,
)
from .current_head_semantic_bridge import (
    CurrentHeadSemanticBridgeError,
    build_current_head_semantic_bridge,
)
from .dynamic_inventory import (
    DynamicInventoryError,
    SecretDetectedError,
    SensitivePathError,
    build_from_repository,
)
from .git_source import (
    FrozenGitSource,
    GitSourceError,
)
from .integrity import (
    IntegrityError,
    all_generated_files,
)
from .observer_tick import (
    DECISION_SCHEMA,
    INPUT_SCHEMA,
    RESULT_SCHEMA,
    STATE_SCHEMA,
    canonical_result_bytes,
    one_shot_tick,
)


class FiniteCandidateEvaluatorError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
EVALUATOR_CONTRACT_BLOB = (
    "b6c17167875874db30a575be95e8e6aa33d630dd"
)
P5D3D_CONTRACT_QUALIFICATION_COMMIT = (
    "c2d0323df53c40c8818d7f8d9805210e1961116e"
)
REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3D_FINITE_EVALUATION_REPORT_V0_1"
)
DETERMINISM_SCHEMA = (
    "ATDS_OBSIDIAN_CURRENT_HEAD_DOUBLE_BUILD_EVIDENCE_V0_1"
)


def _canonical_json_bytes(
    value: Any,
    *,
    terminal_lf: bool = False,
) -> bytes:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    if terminal_lf:
        encoded += b"\n"
    return encoded


def _sha256(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _validate_activation(
    activation: dict[str, Any],
) -> tuple[str, str | None, str]:
    if not isinstance(activation, dict):
        raise FiniteCandidateEvaluatorError(
            "activation tick result must be object"
        )
    if activation.get("schema") != RESULT_SCHEMA:
        raise FiniteCandidateEvaluatorError(
            "activation tick result schema mismatch"
        )

    decision = activation.get("decision")
    state = activation.get("next_state")
    audit = activation.get("audit")

    if (
        not isinstance(decision, dict)
        or decision.get("schema") != DECISION_SCHEMA
    ):
        raise FiniteCandidateEvaluatorError(
            "activation decision schema mismatch"
        )
    if (
        not isinstance(state, dict)
        or state.get("schema") != STATE_SCHEMA
    ):
        raise FiniteCandidateEvaluatorError(
            "activation state schema mismatch"
        )
    if not isinstance(audit, dict):
        raise FiniteCandidateEvaluatorError(
            "activation audit missing"
        )

    if decision.get("action") != (
        "START_EXACT_HEAD_EVALUATION"
    ):
        raise FiniteCandidateEvaluatorError(
            "activation action mismatch"
        )
    if decision.get("reason_code") != (
        "EVALUATION_STARTED"
    ):
        raise FiniteCandidateEvaluatorError(
            "activation reason mismatch"
        )
    if state.get("observer_phase") != "EVALUATING":
        raise FiniteCandidateEvaluatorError(
            "activation state is not EVALUATING"
        )

    candidate = decision.get("candidate_head")
    pending = state.get("pending_heads")
    if (
        not isinstance(candidate, str)
        or len(candidate) != 40
        or not isinstance(pending, list)
        or not pending
        or pending[0] != candidate
    ):
        raise FiniteCandidateEvaluatorError(
            "activation candidate/queue mismatch"
        )

    if decision.get(
        "automatic_promotion_authorized"
    ) is not False:
        raise FiniteCandidateEvaluatorError(
            "activation unexpectedly authorizes promotion"
        )
    if decision.get(
        "production_write_authorized"
    ) is not False:
        raise FiniteCandidateEvaluatorError(
            "activation unexpectedly authorizes production write"
        )

    if state.get("repository") != EXPECTED_REPOSITORY:
        raise FiniteCandidateEvaluatorError(
            "activation repository mismatch"
        )
    if state.get("branch") != EXPECTED_BRANCH:
        raise FiniteCandidateEvaluatorError(
            "activation branch mismatch"
        )

    activation_digest = _sha256_bytes(
        canonical_result_bytes(
            activation
        )
    )
    return (
        candidate,
        state.get("live_projection_head"),
        activation_digest,
    )


def _resolved(path: Path) -> Path:
    try:
        return path.resolve(strict=False)
    except OSError as exc:
        raise FiniteCandidateEvaluatorError(
            "path resolution unavailable"
        ) from exc


def _validate_workspace(
    workspace_root: Path,
    candidate_repo_root: Path,
    forbidden_roots: Iterable[Path],
) -> tuple[Path, tuple[Path, ...]]:
    workspace = _resolved(workspace_root)
    repo = _resolved(candidate_repo_root)
    temp_root = _resolved(
        Path(tempfile.gettempdir())
    )

    if (
        workspace == temp_root
        or temp_root not in workspace.parents
    ):
        raise FiniteCandidateEvaluatorError(
            "evaluation workspace must be below OS temp root"
        )
    if not workspace.exists() or not workspace.is_dir():
        raise FiniteCandidateEvaluatorError(
            "evaluation workspace must already exist"
        )

    forbidden = tuple(
        _resolved(Path(root))
        for root in forbidden_roots
    )

    for root in forbidden:
        if (
            repo == root
            or root in repo.parents
            or repo in root.parents
        ):
            raise FiniteCandidateEvaluatorError(
                "candidate repository intersects forbidden root"
            )
        if (
            workspace == root
            or root in workspace.parents
            or workspace in root.parents
        ):
            raise FiniteCandidateEvaluatorError(
                "evaluation workspace intersects forbidden root"
            )

    if (
        workspace == repo
        or workspace in repo.parents
        or repo in workspace.parents
    ):
        raise FiniteCandidateEvaluatorError(
            "evaluation workspace intersects candidate repository"
        )

    for name in (
        "build-a",
        "build-b",
        "candidate-package",
    ):
        if (workspace / name).exists():
            raise FiniteCandidateEvaluatorError(
                "evaluation child root must be fresh"
            )

    return workspace, forbidden


def _generated_file_map_digest(
    stage_root: Path,
) -> str:
    try:
        entries = all_generated_files(
            stage_root
        )
    except IntegrityError as exc:
        raise CurrentHeadProjectionInvalidError(
            str(exc)
        ) from exc

    rows = [
        [
            entry.relative_path,
            entry.sha256,
            entry.size_bytes,
        ]
        for entry in entries
    ]
    return _sha256(rows)


def _generated_bytes(
    stage_root: Path,
) -> dict[str, bytes]:
    try:
        entries = all_generated_files(
            stage_root
        )
        return {
            entry.relative_path:
                stage_root.joinpath(
                    *entry.relative_path.split("/")
                ).read_bytes()
            for entry in entries
        }
    except OSError as exc:
        raise CurrentHeadProjectionInfrastructureError(
            "generated bytes unavailable"
        ) from exc
    except IntegrityError as exc:
        raise CurrentHeadProjectionInvalidError(
            str(exc)
        ) from exc


def _double_build_evidence(
    *,
    candidate_head: str,
    candidate_tree: str,
    inventory_digest: str,
    bridge_digest: str,
    semantic_digest: str,
    build_a: Any,
    build_b: Any,
) -> tuple[dict[str, Any], str]:
    bytes_a = _generated_bytes(
        Path(build_a.stage_root)
    )
    bytes_b = _generated_bytes(
        Path(build_b.stage_root)
    )

    result_fields = (
        "source_record_count",
        "full_text_count",
        "metadata_only_count",
        "artifact_record_count",
        "relation_record_count",
        "relation_source_body_read_count",
        "metadata_only_body_read_count",
        "body_read_audit_digest_sha256",
        "artifact_set_digest_sha256",
        "relation_set_digest_sha256",
        "integrity_manifest_sha256",
        "projection_tree_digest_sha256",
        "generated_file_count",
    )

    deterministic = (
        all(
            getattr(build_a, field)
            == getattr(build_b, field)
            for field in result_fields
        )
        and set(bytes_a) == set(bytes_b)
        and all(
            bytes_a[path] == bytes_b[path]
            for path in bytes_a
        )
        and build_a.source_commit
            == build_b.source_commit
            == candidate_head
        and build_a.source_tree
            == build_b.source_tree
            == candidate_tree
        and build_a.dynamic_inventory_digest_sha256
            == build_b.dynamic_inventory_digest_sha256
            == inventory_digest
        and build_a.semantic_bridge_digest_sha256
            == build_b.semantic_bridge_digest_sha256
            == bridge_digest
        and build_a.semantic_record_digest_sha256
            == build_b.semantic_record_digest_sha256
            == semantic_digest
        and build_a.projection_contract_version
            == build_b.projection_contract_version
            == PROJECTION_CONTRACT_BLOB
    )

    payload = {
        "schema": DETERMINISM_SCHEMA,
        "candidate_head": candidate_head,
        "candidate_tree": candidate_tree,
        "dynamic_inventory_digest_sha256":
            inventory_digest,
        "semantic_bridge_digest_sha256":
            bridge_digest,
        "semantic_record_digest_sha256":
            semantic_digest,
        "projection_contract_blob":
            PROJECTION_CONTRACT_BLOB,
        "build_a_projection_tree_digest_sha256":
            build_a.projection_tree_digest_sha256,
        "build_b_projection_tree_digest_sha256":
            build_b.projection_tree_digest_sha256,
        "build_a_generated_file_map_digest_sha256":
            _generated_file_map_digest(
                Path(build_a.stage_root)
            ),
        "build_b_generated_file_map_digest_sha256":
            _generated_file_map_digest(
                Path(build_b.stage_root)
            ),
        "build_a_body_read_audit_digest_sha256":
            build_a.body_read_audit_digest_sha256,
        "build_b_body_read_audit_digest_sha256":
            build_b.body_read_audit_digest_sha256,
        "status": (
            "PASS"
            if deterministic
            else "FAIL"
        ),
    }
    return payload, _sha256(payload)


def _result_event(
    *,
    activation: dict[str, Any],
    candidate_head: str,
    outcome: str,
    failure_code: str | None,
) -> tuple[dict[str, Any], str]:
    state = activation["next_state"]
    event_type = (
        "EVALUATION_PASSED"
        if outcome == "QUALIFIED"
        else "EVALUATION_FAILED"
    )

    event = {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence":
            state["last_event_sequence"] + 1,
        "observed_head": None,
        "transition_class": None,
        "candidate_head": candidate_head,
        "failure_code": (
            None
            if outcome == "QUALIFIED"
            else failure_code
        ),
    }

    result = one_shot_tick(
        state,
        event,
    )
    return (
        result,
        _sha256_bytes(
            canonical_result_bytes(result)
        ),
    )


def _report(
    *,
    candidate_head: str,
    candidate_tree: str,
    activation_digest: str,
    live_before: str | None,
    live_after: str | None,
    inventory_digest: str | None,
    bridge_digest: str | None,
    semantic_digest: str | None,
    projection_a_digest: str | None,
    projection_b_digest: str | None,
    breaker_manifest_digest: str | None,
    breaker_result_digest: str | None,
    determinism_digest: str | None,
    candidate_generation_digest: str | None,
    candidate_generation_status: str | None,
    outcome: str,
    failure_code: str | None,
    p5d2_event_emitted: bool,
    p5d2_result_tick_digest: str | None,
) -> dict[str, Any]:
    return {
        "schema": REPORT_SCHEMA,
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "candidate_head": candidate_head,
        "candidate_tree": candidate_tree,
        "source_tick_result_digest_sha256":
            activation_digest,
        "dynamic_inventory_digest_sha256":
            inventory_digest,
        "semantic_bridge_digest_sha256":
            bridge_digest,
        "semantic_record_digest_sha256":
            semantic_digest,
        "projection_contract_blob":
            PROJECTION_CONTRACT_BLOB,
        "projection_a_tree_digest_sha256":
            projection_a_digest,
        "projection_b_tree_digest_sha256":
            projection_b_digest,
        "projection_breaker_manifest_digest_sha256":
            breaker_manifest_digest,
        "projection_breaker_result_digest_sha256":
            breaker_result_digest,
        "determinism_evidence_digest_sha256":
            determinism_digest,
        "candidate_generation_digest_sha256":
            candidate_generation_digest,
        "candidate_generation_verification_status":
            candidate_generation_status,
        "outcome": outcome,
        "failure_code": failure_code,
        "p5d2_result_event_emitted":
            p5d2_event_emitted,
        "p5d2_result_tick_digest_sha256":
            p5d2_result_tick_digest,
        "live_projection_head_before":
            live_before,
        "live_projection_head_after":
            live_after,
        "real_vault_modified": False,
        "current_pointer_created": False,
        "production_promotion_authorized":
            False,
    }


def evaluate_candidate_finitely(
    *,
    activation_tick_result: dict[str, Any],
    candidate_tree: str,
    candidate_repo_root: Path,
    evaluation_workspace_root: Path,
    forbidden_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    (
        candidate_head,
        live_before,
        activation_digest,
    ) = _validate_activation(
        activation_tick_result
    )

    workspace, forbidden = _validate_workspace(
        evaluation_workspace_root,
        candidate_repo_root,
        forbidden_roots,
    )

    inventory_digest: str | None = None
    bridge_digest: str | None = None
    semantic_digest: str | None = None
    projection_a_digest: str | None = None
    projection_b_digest: str | None = None
    breaker_manifest_digest: str | None = None
    breaker_result_digest: str | None = None
    determinism_digest: str | None = None
    generation_digest: str | None = None
    generation_status: str | None = None

    def blocked(
        code: str,
    ) -> dict[str, Any]:
        return _report(
            candidate_head=candidate_head,
            candidate_tree=candidate_tree,
            activation_digest=activation_digest,
            live_before=live_before,
            live_after=live_before,
            inventory_digest=inventory_digest,
            bridge_digest=bridge_digest,
            semantic_digest=semantic_digest,
            projection_a_digest=projection_a_digest,
            projection_b_digest=projection_b_digest,
            breaker_manifest_digest=(
                breaker_manifest_digest
            ),
            breaker_result_digest=(
                breaker_result_digest
            ),
            determinism_digest=determinism_digest,
            candidate_generation_digest=(
                generation_digest
            ),
            candidate_generation_status=(
                generation_status
            ),
            outcome="BLOCKED",
            failure_code=code,
            p5d2_event_emitted=False,
            p5d2_result_tick_digest=None,
        )

    def rejected(
        code: str,
    ) -> dict[str, Any]:
        result_tick, tick_digest = _result_event(
            activation=activation_tick_result,
            candidate_head=candidate_head,
            outcome="REJECTED",
            failure_code=code,
        )
        live_after = result_tick[
            "next_state"
        ]["live_projection_head"]
        if live_after != live_before:
            raise FiniteCandidateEvaluatorError(
                "REJECTED result changed live projection"
            )
        return _report(
            candidate_head=candidate_head,
            candidate_tree=candidate_tree,
            activation_digest=activation_digest,
            live_before=live_before,
            live_after=live_after,
            inventory_digest=inventory_digest,
            bridge_digest=bridge_digest,
            semantic_digest=semantic_digest,
            projection_a_digest=projection_a_digest,
            projection_b_digest=projection_b_digest,
            breaker_manifest_digest=(
                breaker_manifest_digest
            ),
            breaker_result_digest=(
                breaker_result_digest
            ),
            determinism_digest=determinism_digest,
            candidate_generation_digest=(
                generation_digest
            ),
            candidate_generation_status=(
                generation_status
            ),
            outcome="REJECTED",
            failure_code=code,
            p5d2_event_emitted=True,
            p5d2_result_tick_digest=tick_digest,
        )

    repo_root = _resolved(
        candidate_repo_root
    )

    try:
        source = FrozenGitSource(
            repo_root=repo_root,
            expected_repository=(
                EXPECTED_REPOSITORY
            ),
            source_commit=candidate_head,
            expected_tree=candidate_tree,
        )
        source.verify_repository()
        source.verify_frozen_source()
    except (GitSourceError, OSError, ValueError):
        return blocked(
            "ISOLATED_CANDIDATE_REPOSITORY_UNAVAILABLE"
        )

    try:
        inventory = build_from_repository(
            repo_root=repo_root,
            source_head=candidate_head,
            source_tree=candidate_tree,
            observed_remote_head=candidate_head,
        )
        inventory_digest = (
            inventory.digest_sha256
        )
    except (
        SecretDetectedError,
        SensitivePathError,
        DynamicInventoryError,
    ):
        return rejected(
            "DYNAMIC_INVENTORY_INVALID"
        )
    except (GitSourceError, OSError):
        return blocked(
            "SOURCE_BLOB_READ_UNAVAILABLE"
        )

    if (
        inventory.source_commit != candidate_head
        or inventory.source_tree != candidate_tree
    ):
        return rejected(
            "DYNAMIC_INVENTORY_INVALID"
        )

    try:
        bridge = (
            build_current_head_semantic_bridge(
                inventory
            )
        )
    except CurrentHeadSemanticBridgeError:
        return rejected(
            "SEMANTIC_BRIDGE_INVALID"
        )

    bridge_digest = (
        bridge.bridge_entry_digest_sha256
    )
    semantic_digest = (
        bridge.semantic_record_digest_sha256
    )

    if (
        bridge.source_commit != candidate_head
        or bridge.source_tree != candidate_tree
        or bridge.dynamic_inventory_digest_sha256
        != inventory_digest
        or any(
            entry.semantic_body_read
            for entry in bridge.entries
        )
        or any(
            entry.content_mode
            == "METADATA_ONLY"
            and entry.downstream_body_read_allowed
            for entry in bridge.entries
        )
    ):
        return rejected(
            "SEMANTIC_BRIDGE_INVALID"
        )

    build_a_root = workspace / "build-a"
    build_b_root = workspace / "build-b"

    try:
        build_a = build_current_head_projection(
            source=source,
            bridge=bridge,
            stage_root=build_a_root,
        )
        build_b = build_current_head_projection(
            source=source,
            bridge=bridge,
            stage_root=build_b_root,
        )
    except CurrentHeadProjectionInfrastructureError:
        return blocked(
            "STAGING_INFRASTRUCTURE_UNAVAILABLE"
        )
    except CurrentHeadProjectionInvalidError as exc:
        if "METADATA_ONLY" in str(exc):
            return rejected(
                "METADATA_ONLY_BODY_READ_ATTEMPT"
            )
        return rejected(
            "CURRENT_HEAD_PROJECTION_INVALID"
        )

    projection_a_digest = (
        build_a.projection_tree_digest_sha256
    )
    projection_b_digest = (
        build_b.projection_tree_digest_sha256
    )

    try:
        determinism, determinism_digest = (
            _double_build_evidence(
                candidate_head=candidate_head,
                candidate_tree=candidate_tree,
                inventory_digest=inventory_digest,
                bridge_digest=bridge_digest,
                semantic_digest=semantic_digest,
                build_a=build_a,
                build_b=build_b,
            )
        )
    except CurrentHeadProjectionInfrastructureError:
        return blocked(
            "STAGING_INFRASTRUCTURE_UNAVAILABLE"
        )
    except CurrentHeadProjectionInvalidError:
        return rejected(
            "DETERMINISTIC_DOUBLE_BUILD_MISMATCH"
        )

    if determinism["status"] != "PASS":
        return rejected(
            "DETERMINISTIC_DOUBLE_BUILD_MISMATCH"
        )

    try:
        breaker_result = (
            run_current_head_projection_breakers(
                bridge=bridge,
                build_a=build_a,
                build_b=build_b,
            )
        )
    except CurrentHeadBreakerInfrastructureError:
        return blocked(
            "BREAKER_INFRASTRUCTURE_UNAVAILABLE"
        )

    breaker_manifest_digest = (
        breaker_result.manifest_digest_sha256
    )
    breaker_result_digest = (
        breaker_result.result_digest_sha256
    )

    if not breaker_result.all_pass:
        return rejected(
            "PROJECTION_BREAKER_FAILED"
        )

    verified_candidate = VerifiedProjectionCandidate(
        repository=EXPECTED_REPOSITORY,
        branch=EXPECTED_BRANCH,
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
        dynamic_inventory_digest_sha256=(
            inventory_digest
        ),
        semantic_bridge_digest_sha256=(
            bridge_digest
        ),
        semantic_record_digest_sha256=(
            semantic_digest
        ),
        projection_contract_version=(
            PROJECTION_CONTRACT_BLOB
        ),
        projection_tree_digest_sha256=(
            build_a.projection_tree_digest_sha256
        ),
        generated_file_count=(
            build_a.generated_file_count
        ),
        breaker_status="PASS",
        determinism_status="PASS",
        breaker_manifest_digest_sha256=(
            breaker_manifest_digest
        ),
        breaker_result_digest_sha256=(
            breaker_result_digest
        ),
        determinism_evidence_digest_sha256=(
            determinism_digest
        ),
    )

    package_root = (
        workspace / "candidate-package"
    )
    package_forbidden = (
        *forbidden,
        repo_root,
    )

    try:
        descriptor = stage_candidate_generation(
            verified_candidate,
            verified_projection_root=build_a_root,
            package_root=package_root,
            forbidden_roots=package_forbidden,
        )
        verified = verify_candidate_generation(
            package_root,
            expected_candidate=verified_candidate,
            forbidden_roots=package_forbidden,
        )
    except CandidateGenerationInfrastructureError:
        return blocked(
            "PACKAGING_INFRASTRUCTURE_UNAVAILABLE"
        )
    except CandidateGenerationInvalidError:
        return rejected(
            "CANDIDATE_GENERATION_INVALID"
        )

    if descriptor != verified:
        return rejected(
            "CANDIDATE_GENERATION_INVALID"
        )

    generation_status = verified[
        "verification_status"
    ]
    generation_digest = verified[
        "candidate_generation_digest_sha256"
    ]

    if (
        generation_status
        != "PASS_SEALED_UNPROMOTED"
        or verified.get(
            "promotion_authorized"
        ) is not False
    ):
        return rejected(
            "CANDIDATE_GENERATION_INVALID"
        )

    result_tick, result_tick_digest = (
        _result_event(
            activation=activation_tick_result,
            candidate_head=candidate_head,
            outcome="QUALIFIED",
            failure_code=None,
        )
    )
    live_after = result_tick[
        "next_state"
    ]["live_projection_head"]
    if live_after != live_before:
        raise FiniteCandidateEvaluatorError(
            "QUALIFIED result changed live projection"
        )

    return _report(
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
        activation_digest=activation_digest,
        live_before=live_before,
        live_after=live_after,
        inventory_digest=inventory_digest,
        bridge_digest=bridge_digest,
        semantic_digest=semantic_digest,
        projection_a_digest=projection_a_digest,
        projection_b_digest=projection_b_digest,
        breaker_manifest_digest=(
            breaker_manifest_digest
        ),
        breaker_result_digest=(
            breaker_result_digest
        ),
        determinism_digest=determinism_digest,
        candidate_generation_digest=(
            generation_digest
        ),
        candidate_generation_status=(
            generation_status
        ),
        outcome="QUALIFIED",
        failure_code=None,
        p5d2_event_emitted=True,
        p5d2_result_tick_digest=(
            result_tick_digest
        ),
    )

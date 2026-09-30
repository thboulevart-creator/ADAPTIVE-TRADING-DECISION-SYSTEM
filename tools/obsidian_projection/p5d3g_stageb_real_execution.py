import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from . import live_publication_transaction as lp
from . import production_enablement as pe
from .observer_tick import INPUT_SCHEMA, make_initial_state, one_shot_tick
from .persistent_production_handoff import PERSISTENT_STAGING


class StageBExecutionError(RuntimeError):
    pass


class StageBExecutionBlockedError(StageBExecutionError):
    pass


class StageBExecutionGovernanceError(StageBExecutionError):
    pass


CONTRACT_BLOB = "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead"
LIVE_PUBLICATION_BLOB = "956ccb7274cea366b1a414df5a9239cbf580e3bf"
PRODUCTION_ENABLEMENT_BLOB = "07a04ba2e23dea8512d786cafbf8fa7118572170"
PERSISTENT_HANDOFF_BLOB = "375607d88bc926e4fd4c297ddc6fedba5506642a"
OBSERVER_TICK_BLOB = "fd212f61ec38332b677110f40265638af55a73e2"

REAL_VAULT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-OBSIDIAN-PROJECTION"
)
CONTROL_ROOT = Path(
    r"C:\Users\Boulevart\OneDrive\Bureau\ATDS"
    r"\ATDS-P5D3G-CONTROL-EVIDENCE"
)
STAGE_A_RECEIPT_NONCE = (
    "stagea-7a5df19b2e0e90b89f7319dff57b7ac5-human-approval-01"
)
STAGE_A_RECEIPT_PATH = (
    CONTROL_ROOT / "stage-a-approvals" / (STAGE_A_RECEIPT_NONCE + ".json")
)

EXPECTED_STAGE_A_PLAN_DIGEST = (
    "7a5df19b2e0e90b89f7319dff57b7ac521d5adc24bf408dbc76e221a616bac79"
)
EXPECTED_STAGE_A_APPROVAL_DIGEST = (
    "6c1a5e16df5a6b7a72606d4f50990809cf567a9b92ef48242905f6f3e40a7e3d"
)
EXPECTED_STAGE_A_RECEIPT_SHA256 = (
    "2a2242ff906c33886d6b9860de90c47b1fb195f749d5932812d68630717909f3"
)
EXPECTED_CANDIDATE_HEAD = "59f1dc26973b0b50efefccf12b26784d1e41f546"
EXPECTED_CANDIDATE_TREE = "beb85ddb99e8a87afc4e8a6ed9b989ed0f83e1ea"
EXPECTED_GENERATION_ID = (
    "gen-69e845e1b6f60f213dd2e8e90ed493fd6a2a541084be9cfa9df3b2e035877ea0"
)

STAGE_B_AUTH_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3G_REAL_LIVE_EXECUTION_AUTHORIZATION_V0_1"
)
STAGE_B_AUTH_ACTION = (
    "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION"
)

_NONCE_RE = re.compile(r"^[0-9A-Za-z._-]{16,256}$")
_AUTH_FIELDS = frozenset(
    {
        "schema",
        "authorized_action",
        "stage_a_plan_digest_sha256",
        "stage_a_approval_digest_sha256",
        "stage_a_approval_receipt_sha256",
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

_TOOLING = {
    "tools/obsidian_projection/p5d3g_stageb_real_execution_gate_contract_v0_1.json": CONTRACT_BLOB,
    "tools/obsidian_projection/live_publication_transaction.py": LIVE_PUBLICATION_BLOB,
    "tools/obsidian_projection/production_enablement.py": PRODUCTION_ENABLEMENT_BLOB,
    "tools/obsidian_projection/persistent_production_handoff.py": PERSISTENT_HANDOFF_BLOB,
    "tools/obsidian_projection/observer_tick.py": OBSERVER_TICK_BLOB,
}
def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _git_blob(relative: str) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(_repo_root()),
        check=False,
        text=True,
        capture_output=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        raise StageBExecutionBlockedError("qualified tooling commit unavailable")
    return completed.stdout.strip()


def _worktree_blob(relative: str) -> str:
    completed = subprocess.run(
        ["git", "hash-object", f"--path={relative}", relative],
        cwd=str(_repo_root()),
        check=False,
        text=True,
        capture_output=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        raise StageBExecutionBlockedError("qualified tooling worktree unavailable")
    return completed.stdout.strip()


def _verify_tooling_identity() -> None:
    for relative, blob in _TOOLING.items():
        if _git_blob(relative) != blob or _worktree_blob(relative) != blob:
            raise StageBExecutionGovernanceError(
                f"qualified tooling identity mismatch: {relative}"
            )
def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_value(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return _sha256_bytes(raw)


def _read_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StageBExecutionBlockedError("canonical evidence unavailable") from exc
    expected = (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )
    if raw != expected or not isinstance(value, dict):
        raise StageBExecutionGovernanceError("evidence is not canonical JSON")
    return value, raw


def _exact_path(supplied: Path, expected: Path, label: str) -> Path:
    if str(Path(supplied)) != str(Path(expected)):
        raise StageBExecutionGovernanceError(f"{label} lexical identity mismatch")
    try:
        resolved = Path(supplied).resolve(strict=True)
        expected_resolved = Path(expected).resolve(strict=True)
    except OSError as exc:
        raise StageBExecutionBlockedError(f"{label} unavailable") from exc
    if resolved != expected_resolved:
        raise StageBExecutionGovernanceError(f"{label} resolved identity mismatch")
    return resolved
def _validate_stage_a_receipt(control: Path) -> dict[str, Any]:
    expected_path = control / "stage-a-approvals" / (
        STAGE_A_RECEIPT_NONCE + ".json"
    )
    if expected_path != STAGE_A_RECEIPT_PATH:
        raise StageBExecutionGovernanceError("stage-A receipt path mismatch")

    value, raw = _read_canonical_json(expected_path)
    if _sha256_bytes(raw) != EXPECTED_STAGE_A_RECEIPT_SHA256:
        raise StageBExecutionGovernanceError("stage-A receipt SHA-256 mismatch")

    expected = {
        "schema": "ATDS_OBSIDIAN_P5D3G_STAGE_A_APPROVAL_CONSUMPTION_V0_1",
        "plan_digest_sha256": EXPECTED_STAGE_A_PLAN_DIGEST,
        "approval_digest_sha256": EXPECTED_STAGE_A_APPROVAL_DIGEST,
        "one_shot_nonce": STAGE_A_RECEIPT_NONCE,
        "candidate_head": EXPECTED_CANDIDATE_HEAD,
        "candidate_tree": EXPECTED_CANDIDATE_TREE,
        "generation_id": EXPECTED_GENERATION_ID,
        "stage_b_execution_authority": False,
    }
    if value != expected:
        raise StageBExecutionGovernanceError("stage-A receipt content mismatch")
    return value


def _plan_parity(stage_a: dict[str, Any], tx: dict[str, Any]) -> None:
    pairs = {
        "candidate_head": "candidate_head",
        "candidate_tree": "candidate_tree",
        "generation_id": "generation_id",
        "candidate_generation_digest_sha256": "candidate_generation_digest_sha256",
        "handoff_package_byte_tree_digest_sha256": "handoff_package_byte_tree_digest_sha256",
        "handoff_record_sha256": "handoff_record_sha256",
        "publication_mode": "publication_mode",
        "target_generation_relative_path": "target_generation_relative_path",
        "planned_current_sha256": "planned_current_sha256",
        "planned_publication_generation_digest_sha256": "planned_publication_generation_digest_sha256",
        "operation_sequence_digest_sha256": "operation_sequence_digest_sha256",
    }
    for stage_field, tx_field in pairs.items():
        if stage_a.get(stage_field) != tx.get(tx_field):
            raise StageBExecutionGovernanceError(
                f"Stage-A/transaction plan parity mismatch: {stage_field}"
            )

    prestate_pairs = {
        "expected_current_state": "expected_previous_current_state",
        "expected_current_sha256": "expected_previous_current_sha256",
        "expected_current_generation_id": "expected_previous_generation_id",
        "expected_current_generation_digest_sha256": "expected_previous_generation_digest_sha256",
    }
    for stage_field, tx_field in prestate_pairs.items():
        if stage_a.get(stage_field) != tx.get(tx_field):
            raise StageBExecutionGovernanceError(
                f"Stage-A/transaction prestate mismatch: {stage_field}"
            )

    if stage_a.get("expected_current_tmp_state") != "ABSENT":
        raise StageBExecutionGovernanceError("Stage-A CURRENT.tmp prestate mismatch")
    if stage_a.get("expected_target_state") != "ABSENT":
        raise StageBExecutionGovernanceError("Stage-A target prestate mismatch")


def _candidate_pending_observer_state(candidate_head: str) -> dict[str, Any]:
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
    started = one_shot_tick(
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
    passed = one_shot_tick(
        started["next_state"],
        {
            "schema": INPUT_SCHEMA,
            "event_type": "EVALUATION_PASSED",
            "sequence": 3,
            "observed_head": None,
            "transition_class": None,
            "candidate_head": candidate_head,
            "failure_code": None,
        },
    )
    return passed["next_state"]


def build_stage_b_read_only_candidate(
    *,
    handoff_root: Path,
    promotion_staging_root: Path,
    real_vault_root: Path,
    control_root: Path,
) -> dict[str, Any]:
    _verify_tooling_identity()
    staging = _exact_path(
        promotion_staging_root, PERSISTENT_STAGING, "persistent staging"
    )
    live = _exact_path(real_vault_root, REAL_VAULT, "real Vault")
    control = _exact_path(control_root, CONTROL_ROOT, "control root")

    receipt = _validate_stage_a_receipt(control)
    before = pe.snapshot_real_vault(live)

    stage_a_result = pe.build_real_live_publication_plan(
        handoff_root=handoff_root,
        real_vault_root=live,
        promotion_staging_root=staging,
    )
    if stage_a_result["plan_digest_sha256"] != EXPECTED_STAGE_A_PLAN_DIGEST:
        raise StageBExecutionGovernanceError("fresh Stage-A plan digest mismatch")
    if stage_a_result["stage_b_execution_authority"] is not False:
        raise StageBExecutionGovernanceError("Stage-A leaked Stage-B authority")

    tx_plan = lp.build_publication_plan(
        handoff_root=handoff_root,
        live_vault_root=live,
        promotion_staging_root=staging,
        _production_capability=lp._REAL_PRODUCTION_EXECUTION_CAPABILITY,
    )
    _plan_parity(stage_a_result["plan"], tx_plan)

    after = pe.snapshot_real_vault(live)
    proof = pe.prove_zero_real_vault_mutation(before, after)
    tx_digest = lp.publication_plan_digest(tx_plan)

    return {
        "status": "PASS_STAGE_B_REAL_EXECUTION_PREFLIGHT_READ_ONLY",
        "stage_a_plan_digest_sha256": EXPECTED_STAGE_A_PLAN_DIGEST,
        "stage_a_approval_digest_sha256": EXPECTED_STAGE_A_APPROVAL_DIGEST,
        "stage_a_approval_receipt_sha256": EXPECTED_STAGE_A_RECEIPT_SHA256,
        "stage_a_receipt": receipt,
        "transaction_plan": tx_plan,
        "transaction_plan_digest_sha256": tx_digest,
        "zero_mutation_proof": proof,
        "stage_b_execution_authority": False,
    }


def _validate_stage_b_authorization(
    candidate: dict[str, Any],
    authorization: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    if authorization is None:
        raise StageBExecutionBlockedError("BLOCKED_STAGE_B_HUMAN_AUTHORIZATION")
    if not isinstance(authorization, dict):
        raise StageBExecutionGovernanceError("Stage-B authorization must be object")
    if frozenset(authorization) != _AUTH_FIELDS:
        raise StageBExecutionGovernanceError(
            "Stage-B authorization exact field set mismatch"
        )
    if authorization.get("schema") != STAGE_B_AUTH_SCHEMA:
        raise StageBExecutionGovernanceError("Stage-B authorization schema mismatch")
    if authorization.get("authorized_action") != STAGE_B_AUTH_ACTION:
        raise StageBExecutionGovernanceError("Stage-B authorization action mismatch")
    plan = candidate["transaction_plan"]
    expected = {
        "stage_a_plan_digest_sha256": EXPECTED_STAGE_A_PLAN_DIGEST,
        "stage_a_approval_digest_sha256": EXPECTED_STAGE_A_APPROVAL_DIGEST,
        "stage_a_approval_receipt_sha256": EXPECTED_STAGE_A_RECEIPT_SHA256,
        "candidate_head": plan["candidate_head"],
        "candidate_tree": plan["candidate_tree"],
        "generation_id": plan["generation_id"],
        "publication_mode": plan["publication_mode"],
        "expected_current_state": plan["expected_previous_current_state"],
        "expected_current_sha256": plan["expected_previous_current_sha256"],
        "expected_current_tmp_state": "ABSENT",
        "expected_target_state": "ABSENT",
    }
    for field, value in expected.items():
        if authorization.get(field) != value:
            raise StageBExecutionGovernanceError(
                f"Stage-B authorization binding mismatch: {field}"
            )

    nonce = authorization.get("one_shot_nonce")
    if not isinstance(nonce, str) or _NONCE_RE.fullmatch(nonce) is None:
        raise StageBExecutionGovernanceError("Stage-B one-shot nonce invalid")

    return authorization, _sha256_value(authorization)


def _consume_stage_b_authorization(
    control: Path,
    authorization: dict[str, Any],
    authorization_digest: str,
    transaction_plan_digest: str,
) -> Path:
    directory = control / "stage-b-authorizations"
    directory.mkdir(exist_ok=True)
    marker = directory / (authorization["one_shot_nonce"] + ".json")
    payload = {
        "schema": "ATDS_OBSIDIAN_P5D3G_STAGE_B_AUTHORIZATION_CONSUMPTION_V0_1",
        "one_shot_nonce": authorization["one_shot_nonce"],
        "stage_a_plan_digest_sha256": EXPECTED_STAGE_A_PLAN_DIGEST,
        "stage_a_approval_digest_sha256": EXPECTED_STAGE_A_APPROVAL_DIGEST,
        "stage_a_approval_receipt_sha256": EXPECTED_STAGE_A_RECEIPT_SHA256,
        "transaction_plan_digest_sha256": transaction_plan_digest,
        "authorization_digest_sha256": authorization_digest,
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
        raise StageBExecutionBlockedError(
            "BLOCKED_STAGE_B_AUTHORIZATION_ALREADY_CONSUMED"
        ) from exc
    except OSError as exc:
        raise StageBExecutionBlockedError(
            "Stage-B authorization consumption unavailable"
        ) from exc
    return marker


def execute_one_real_live_publication(
    *,
    handoff_root: Path,
    promotion_staging_root: Path,
    real_vault_root: Path,
    control_root: Path,
    authorization: dict[str, Any] | None,
) -> dict[str, Any]:
    candidate = build_stage_b_read_only_candidate(
        handoff_root=handoff_root,
        promotion_staging_root=promotion_staging_root,
        real_vault_root=real_vault_root,
        control_root=control_root,
    )
    control = _exact_path(control_root, CONTROL_ROOT, "control root")
    auth, auth_digest = _validate_stage_b_authorization(
        candidate,
        authorization,
    )
    tx_plan = candidate["transaction_plan"]
    tx_digest = candidate["transaction_plan_digest_sha256"]

    marker = _consume_stage_b_authorization(
        control,
        auth,
        auth_digest,
        tx_digest,
    )
    internal_authorization = {
        "schema": lp.AUTH_SCHEMA,
        "authorized_action": "EXECUTE_ONE_FINITE_LIVE_PUBLICATION_TRANSACTION",
        "plan_digest_sha256": tx_digest,
        "candidate_head": tx_plan["candidate_head"],
        "candidate_tree": tx_plan["candidate_tree"],
        "generation_id": tx_plan["generation_id"],
        "publication_mode": tx_plan["publication_mode"],
        "expected_previous_current_state": tx_plan[
            "expected_previous_current_state"
        ],
        "one_shot_nonce": auth["one_shot_nonce"],
    }
    observer_state = _candidate_pending_observer_state(
        tx_plan["candidate_head"]
    )

    result = lp.execute_finite_live_publication(
        handoff_root=handoff_root,
        live_vault_root=real_vault_root,
        control_root=control_root,
        plan=tx_plan,
        authorization=internal_authorization,
        observer_state=observer_state,
        promotion_staging_root=promotion_staging_root,
        _production_capability=lp._REAL_PRODUCTION_EXECUTION_CAPABILITY,
    )
    return {
        **result,
        "stage_b_authorization_digest_sha256": auth_digest,
        "stage_b_authorization_receipt_path": str(marker),
        "stage_a_plan_digest_sha256": EXPECTED_STAGE_A_PLAN_DIGEST,
        "stage_a_approval_digest_sha256": EXPECTED_STAGE_A_APPROVAL_DIGEST,
        "mandatory_stop": True,
    }

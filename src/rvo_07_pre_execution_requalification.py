from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping

CONTRACT = "ATDS_RVO_07_PRE_EXECUTION_REQUALIFICATION_V0_1"
REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
CANONICAL_BRANCH = "integration/system-v1"
WORKSPACE_SCHEMA = "ATDS_G05_01_WORKSPACE_QUALIFICATION_RECEIPT_V0_1"
WORKSPACE_STATUS = "G05_01_WORKSPACE_DRY_READY"

DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
PARQUET_FILE_COUNT = 61

INVOCATION_PROFILE_ID = "P1_12C_AP1_CLAIM_SCOPED_V1"
INVOCATION_PROFILE_DIGEST = "3a8689dcfa79515fae9f38b7e4903722ebdcd601ca16e7d84ef9139eb62b4de4"
RUNTIME_LOCK_SCHEMA = "P1_12C_REAL_PRODUCER_RUNTIME_LOCK_V1"
RUNTIME_LOCK_DIGEST = "5b77e0c094812f3e7e9d25efdb87bd3da92748bc6f8a436ffe52cefe6d38f6c4"
SMF_ACTIVATION_DIGEST = "sha256:d6a47dae26cc333200cf47ac98a1ed06378a368664c3fa9d31d88b76573fef36"
SMF_DRY_PLAN_DIGEST = "sha256:b2670b0fe4502b0a8027b5b7304e8886cfb033160f254250f00c8ca98f39d750"

EXPECTED_RUNTIME = {
    "python_version": "3.13.14",
    "python_binary_sha256": "ad169f4cb4bfb78c7a5c030a4529c19d6643276778e33994c93e145b6191c3ec",
    "numpy_version": "2.5.3",
    "numpy_metadata_sha256": "451a9b8028000588e66b0b415587b6aef0bbc51a96d8e8a0cba0dc23acf64f99",
    "numpy_record_sha256": "5135e045b7bc7d8f2ef83e2bd9c618840f46ebd09d8590c819bbcdeb32cfe41e",
    "pyarrow_version": "25.0.1",
    "pyarrow_metadata_sha256": "12ed8d0988a6f7153fec923ee47b7fc1d6134463a86b1b89fa36f24c250163ff",
    "pyarrow_record_sha256": "a6cc5dcd5681d231959f61ccc1b57cb13dc1690f0819ed7bfd66ebd575e0db24",
    "tzdata_version": "2026.3",
    "tzdata_metadata_sha256": "511c019df477939fe7f4c38e32ad74a570c4ebb05b13fd2fffd0f0f2dbe6f7b1",
    "tzdata_record_sha256": "8f9f4ae062c3c9af93f22cff46986c4735d15d1306a413df291d5b67301db0eb",
    "timezone_name": "America/New_York",
    "timeout_seconds": 3600,
    "material_environment_json": '{"PYTHONDONTWRITEBYTECODE":"1","PYTHONHASHSEED":"0"}',
}
EXPECTED_OWNER_BLOBS = {
    "reports/program/2026-10-05-P1-21-QUALIFICATION-RECEIPT-V0.1.json": "49142e1928cf32ec10ed9a4809388a782559ad42",
    "src/p1_12c_qualified_producer_execution.py": "9d304202d44c8917cf640fd0b4114169968e511e",
    "tools/p1_12c_sandbox_runner.py": "b16fa57409a67049eedfbb6c6ec7b2e9ae3e3108",
    "reports/program/2026-10-05-SMF-AP1-M03-01-QUALIFICATION-RECEIPT-V0.1.json": "b7bf4f20d24aebafb9ff6c6e9029330afb9c0921",
    "src/smf_ap1_m03_binding.py": "f4c0295625f8b360effbd27a8d616d9644ea2a5e",
    "tools/smf_ap1_m03_companion.py": "7ec9ef71c8682abc4c8f9561518f84268c00ed11",
    "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json": "ccfccda676abfe7e02082a331557ffed14e1f32b",
    "tools/ap1_intraday_spread_census.py": "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a",
    "GOVERNANCE/RVO-06-PRE-EXECUTION-OWNER-GAP-MATRIX-V0.1.json": "464fe8b03166c687c3618c18e7c3509fbc62f08b",
    "reports/program/2026-10-05-RVO-06-QUALIFICATION-RECEIPT-V0.1.json": "11453a26a181eeca050a518d4ece01c68ddf5716",
    "GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json": "e4e275e8590e3bead9123969c068b036c6c4e1d8",
    "GOVERNANCE/G05-01-FIRST-REAL-CC02-EXECUTION-WORKSPACE-CONTRACT-V0.1.json": "dc7e4e2375855034a796b06fdb52ae43cc1bec41",
    "reports/program/2026-10-05-G05-01-QUALIFICATION-RECEIPT-V0.1.json": "60a17b59aa03a41d517ee887c565d314a3d92ce5",
}
WORKSPACE_PROTECTED_BLOBS = {
    k: EXPECTED_OWNER_BLOBS[k] for k in (
        "GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json",
        "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json",
        "reports/program/2026-10-05-P1-21-QUALIFICATION-RECEIPT-V0.1.json",
        "reports/program/2026-10-05-SMF-AP1-M03-01-QUALIFICATION-RECEIPT-V0.1.json",
        "src/p1_12c_qualified_producer_execution.py",
        "src/smf_ap1_m03_binding.py",
        "tools/ap1_intraday_spread_census.py",
        "tools/p1_12c_sandbox_runner.py",
        "tools/smf_ap1_m03_companion.py",
    )
}
AUTHORITY_NONE = {
    "execution": False,
    "scientific": False,
    "operational": False,
    "trading": False,
    "capital": False,
}
CLOSED = "PRE_EXECUTION_REQUALIFIED_CLOSED"
OPEN = "OPEN"

def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _get(obj: Mapping[str, Any], *path: str, default: Any = None) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, Mapping) or key not in cur:
            return default
        cur = cur[key]
    return cur

def synthetic_valid_workspace_receipt(*, head: str, tree: str, workspace_clean: bool, workspace_detached: bool) -> dict[str, Any]:
    return {
        "schema": WORKSPACE_SCHEMA,
        "status": WORKSPACE_STATUS,
        "identity": {
            "repository": REPOSITORY,
            "canonical_branch": CANONICAL_BRANCH,
            "head": head,
            "tree": tree,
            "dataset_identity": DATASET_IDENTITY,
            "manifest_sha256": AP0_MANIFEST_SHA256,
            "parquet_file_count": PARQUET_FILE_COUNT,
            "protected_blobs": dict(WORKSPACE_PROTECTED_BLOBS),
            "p1_runtime_lock_digest": RUNTIME_LOCK_DIGEST,
            "p1_invocation_profile_digest": INVOCATION_PROFILE_DIGEST,
            "smf_activation_digest": SMF_ACTIVATION_DIGEST,
            "smf_dry_plan_digest": SMF_DRY_PLAN_DIGEST,
        },
        "ap0": {
            "dataset_identity": DATASET_IDENTITY,
            "manifest_sha256": AP0_MANIFEST_SHA256,
            "manifest_declared_files": PARQUET_FILE_COUNT,
            "parquet_file_count": PARQUET_FILE_COUNT,
            "parquet_content_opened": False,
        },
        "runtime_lock": {
            "schema": RUNTIME_LOCK_SCHEMA,
            "runtime_lock_id": "RPRL-" + RUNTIME_LOCK_DIGEST[:32],
            "runtime_lock_digest": RUNTIME_LOCK_DIGEST,
            "invocation_profile_digest": INVOCATION_PROFILE_DIGEST,
            **EXPECTED_RUNTIME,
            "execution_authority": False,
            "result_exposed": False,
        },
        "p1": {
            "data_binding_id": "P1DE-SYNTHETIC-VALID",
            "invocation_profile_id": INVOCATION_PROFILE_ID,
            "dry_plan_id": "QRPP-SYNTHETIC-VALID",
            "qualified_input_scope": "SYNTHETIC_NON_EMPIRICAL_SHAPE_PROOF_ONLY",
            "exact_real_cc02_input_minted": False,
            "result_minted": False,
            "execution_authority": False,
        },
        "smf": {
            "activation_digest": SMF_ACTIVATION_DIGEST,
            "dry_plan_digest": SMF_DRY_PLAN_DIGEST,
            "method_executed": False,
            "result_minted": False,
        },
        "output_probe": {"write_probe": "PASS", "probe_removed": True},
        "authority": dict(AUTHORITY_NONE),
        "forbidden_observations": {
            "ap1_executed": False,
            "m03_executed": False,
            "new_empirical_result": False,
            "oos_consumed": False,
            "parquet_statistical_open": False,
        },
        "workspace_observation": {"clean": workspace_clean, "detached": workspace_detached},
        "workspace_id": "G05WS-SYNTHETIC-VALID",
        "workspace_digest": "f"*64,
        "g05_effect": "WORKSPACE_MATERIALIZED_DRY_QUALIFIED_PENDING_RVO_REAL_REQUALIFICATION",
    }

def evaluate_pre_execution_readiness(
    workspace_receipt: Mapping[str, Any],
    *,
    current_head: str,
    current_tree: str,
    workspace_clean: bool,
    workspace_detached: bool,
    observed_owner_blobs: Mapping[str, str],
    main_checkout_clean: bool = True,
    workspace_receipt_sha256: str | None = None,
) -> dict[str, Any]:
    failures: list[str] = []
    gap_reasons: dict[str, list[str]] = {f"G0{i}": [] for i in range(1, 6)}

    def require(cond: bool, code: str, gap: str | None = None) -> bool:
        if not cond:
            failures.append(code)
            if gap is not None:
                gap_reasons[gap].append(code)
            return False
        return True

    require(_get(workspace_receipt, "schema") == WORKSPACE_SCHEMA, "WORKSPACE_SCHEMA_MISMATCH", "G05")
    require(_get(workspace_receipt, "status") == WORKSPACE_STATUS, "WORKSPACE_NOT_DRY_READY", "G05")
    require(_get(workspace_receipt, "identity", "repository") == REPOSITORY, "REPOSITORY_IDENTITY_MISMATCH", "G05")
    require(_get(workspace_receipt, "identity", "canonical_branch") == CANONICAL_BRANCH, "BRANCH_IDENTITY_MISMATCH", "G05")
    require(_get(workspace_receipt, "identity", "head") == current_head, "WORKSPACE_HEAD_MISMATCH", "G05")
    require(_get(workspace_receipt, "identity", "tree") == current_tree, "WORKSPACE_TREE_MISMATCH", "G05")
    require(workspace_clean, "WORKSPACE_DIRTY", "G05")
    require(workspace_detached, "WORKSPACE_NOT_DETACHED", "G05")
    require(main_checkout_clean, "MAIN_CHECKOUT_DIRTY", "G05")

    observed_map = dict(observed_owner_blobs)
    require(observed_map == EXPECTED_OWNER_BLOBS, "OWNER_BLOB_MAP_MISMATCH")
    require(_get(workspace_receipt, "identity", "protected_blobs") == WORKSPACE_PROTECTED_BLOBS, "WORKSPACE_PROTECTED_BLOB_MAP_MISMATCH", "G05")

    require(_get(workspace_receipt, "ap0", "dataset_identity") == DATASET_IDENTITY, "AP0_DATASET_IDENTITY_MISMATCH", "G05")
    require(_get(workspace_receipt, "ap0", "manifest_sha256") == AP0_MANIFEST_SHA256, "AP0_MANIFEST_SHA256_MISMATCH", "G05")
    require(_get(workspace_receipt, "ap0", "manifest_declared_files") == PARQUET_FILE_COUNT, "AP0_MANIFEST_FILE_COUNT_MISMATCH", "G05")
    require(_get(workspace_receipt, "ap0", "parquet_file_count") == PARQUET_FILE_COUNT, "AP0_PARQUET_FILE_COUNT_MISMATCH", "G05")
    require(_get(workspace_receipt, "ap0", "parquet_content_opened") is False, "PARQUET_STATISTICAL_OPEN_OBSERVED", "G05")
    require(_get(workspace_receipt, "output_probe", "write_probe") == "PASS", "OUTPUT_PROBE_NOT_PASS", "G05")
    require(_get(workspace_receipt, "output_probe", "probe_removed") is True, "OUTPUT_PROBE_NOT_REMOVED", "G05")

    g01 = [
        require(isinstance(_get(workspace_receipt, "p1", "data_binding_id"), str) and bool(_get(workspace_receipt, "p1", "data_binding_id")), "G01_DATA_BINDING_MISSING", "G01"),
        require(observed_map.get("reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json") == EXPECTED_OWNER_BLOBS["reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"], "G01_DATA02_IDENTITY_MISMATCH", "G01"),
        require(observed_map.get("src/p1_12c_qualified_producer_execution.py") == EXPECTED_OWNER_BLOBS["src/p1_12c_qualified_producer_execution.py"], "G01_P112C_IDENTITY_MISMATCH", "G01"),
    ]
    g02 = [
        require(_get(workspace_receipt, "p1", "invocation_profile_id") == INVOCATION_PROFILE_ID, "G02_INVOCATION_PROFILE_ID_MISMATCH", "G02"),
        require(_get(workspace_receipt, "runtime_lock", "invocation_profile_digest") == INVOCATION_PROFILE_DIGEST, "G02_INVOCATION_PROFILE_DIGEST_MISMATCH", "G02"),
        require(observed_map.get("tools/ap1_intraday_spread_census.py") == EXPECTED_OWNER_BLOBS["tools/ap1_intraday_spread_census.py"], "G02_AP1_PRODUCER_IDENTITY_MISMATCH", "G02"),
    ]

    runtime = _get(workspace_receipt, "runtime_lock", default={})
    g03 = [
        require(_get(workspace_receipt, "runtime_lock", "schema") == RUNTIME_LOCK_SCHEMA, "G03_RUNTIME_SCHEMA_MISMATCH", "G03"),
        require(_get(workspace_receipt, "runtime_lock", "runtime_lock_digest") == RUNTIME_LOCK_DIGEST, "G03_RUNTIME_DIGEST_MISMATCH", "G03"),
        require(_get(workspace_receipt, "runtime_lock", "execution_authority") is False, "G03_RUNTIME_EXECUTION_AUTHORITY_PRESENT", "G03"),
        require(_get(workspace_receipt, "runtime_lock", "result_exposed") is False, "G03_RUNTIME_RESULT_EXPOSED", "G03"),
    ]
    for key, expected in EXPECTED_RUNTIME.items():
        g03.append(require(_get(workspace_receipt, "runtime_lock", key) == expected, "G03_RUNTIME_FIELD_MISMATCH:" + key, "G03"))

    g04 = [
        require(_get(workspace_receipt, "smf", "activation_digest") == SMF_ACTIVATION_DIGEST, "G04_SMF_ACTIVATION_DIGEST_MISMATCH", "G04"),
        require(_get(workspace_receipt, "smf", "dry_plan_digest") == SMF_DRY_PLAN_DIGEST, "G04_SMF_DRY_PLAN_DIGEST_MISMATCH", "G04"),
        require(_get(workspace_receipt, "smf", "method_executed") is False, "G04_M03_WAS_EXECUTED", "G04"),
        require(_get(workspace_receipt, "smf", "result_minted") is False, "G04_M03_RESULT_MINTED", "G04"),
        require(observed_map.get("src/smf_ap1_m03_binding.py") == EXPECTED_OWNER_BLOBS["src/smf_ap1_m03_binding.py"], "G04_SMF_BINDING_IDENTITY_MISMATCH", "G04"),
        require(observed_map.get("tools/smf_ap1_m03_companion.py") == EXPECTED_OWNER_BLOBS["tools/smf_ap1_m03_companion.py"], "G04_SMF_COMPANION_IDENTITY_MISMATCH", "G04"),
    ]

    authority = _get(workspace_receipt, "authority", default={})
    for key, expected in AUTHORITY_NONE.items():
        require(authority.get(key) is expected, "AUTHORITY_PRESENT:" + key)
    forbidden = _get(workspace_receipt, "forbidden_observations", default={})
    for key in ("ap1_executed", "m03_executed", "new_empirical_result", "oos_consumed", "parquet_statistical_open"):
        require(forbidden.get(key) is False, "FORBIDDEN_OBSERVATION:" + key)
    require(_get(workspace_receipt, "p1", "exact_real_cc02_input_minted") is False, "EXACT_REAL_CC02_INPUT_ALREADY_MINTED")
    require(_get(workspace_receipt, "p1", "result_minted") is False, "P1_RESULT_ALREADY_MINTED")
    require(_get(workspace_receipt, "p1", "execution_authority") is False, "P1_EXECUTION_AUTHORITY_PRESENT")

    g05 = [
        not gap_reasons["G05"],
        require(_get(workspace_receipt, "g05_effect") == "WORKSPACE_MATERIALIZED_DRY_QUALIFIED_PENDING_RVO_REAL_REQUALIFICATION", "G05_EFFECT_MISMATCH", "G05"),
    ]

    gap_pass = {
        "G01": all(g01) and not gap_reasons["G01"],
        "G02": all(g02) and not gap_reasons["G02"],
        "G03": all(g03) and not gap_reasons["G03"],
        "G04": all(g04) and not gap_reasons["G04"],
        "G05": all(g05) and not gap_reasons["G05"],
    }
    gaps = {
        gap: {"status": CLOSED if ok else OPEN, "reasons": list(gap_reasons[gap])}
        for gap, ok in gap_pass.items()
    }

    freeze_body = {
        "schema": "ATDS_RVO_07_PRE_RESULT_FREEZE_V0_1",
        "repository": REPOSITORY,
        "branch": CANONICAL_BRANCH,
        "head": current_head,
        "tree": current_tree,
        "owner_blobs": dict(sorted(observed_map.items())),
        "workspace": {
            "workspace_id": _get(workspace_receipt, "workspace_id"),
            "workspace_digest": _get(workspace_receipt, "workspace_digest"),
            "workspace_receipt_sha256": workspace_receipt_sha256,
            "clean": workspace_clean,
            "detached": workspace_detached,
            "main_checkout_clean": main_checkout_clean,
        },
        "ap0": {
            "dataset_identity": _get(workspace_receipt, "ap0", "dataset_identity"),
            "manifest_sha256": _get(workspace_receipt, "ap0", "manifest_sha256"),
            "parquet_file_count": _get(workspace_receipt, "ap0", "parquet_file_count"),
            "parquet_statistical_open": _get(workspace_receipt, "ap0", "parquet_content_opened"),
        },
        "p1": {
            "data_binding_id": _get(workspace_receipt, "p1", "data_binding_id"),
            "invocation_profile_id": _get(workspace_receipt, "p1", "invocation_profile_id"),
            "invocation_profile_digest": _get(workspace_receipt, "runtime_lock", "invocation_profile_digest"),
            "dry_plan_id": _get(workspace_receipt, "p1", "dry_plan_id"),
            "dry_plan_digest": _get(workspace_receipt, "identity", "p1_dry_plan_digest"),
            "exact_real_cc02_input_minted": _get(workspace_receipt, "p1", "exact_real_cc02_input_minted"),
            "result_minted": _get(workspace_receipt, "p1", "result_minted"),
        },
        "runtime_lock": {
            "id": _get(workspace_receipt, "runtime_lock", "runtime_lock_id"),
            "digest": _get(workspace_receipt, "runtime_lock", "runtime_lock_digest"),
            "timeout_seconds": _get(workspace_receipt, "runtime_lock", "timeout_seconds"),
            "execution_authority": _get(workspace_receipt, "runtime_lock", "execution_authority"),
        },
        "smf": {
            "activation_digest": _get(workspace_receipt, "smf", "activation_digest"),
            "dry_plan_digest": _get(workspace_receipt, "smf", "dry_plan_digest"),
            "method_executed": _get(workspace_receipt, "smf", "method_executed"),
            "result_minted": _get(workspace_receipt, "smf", "result_minted"),
        },
        "gaps": gaps,
        "authority": dict(AUTHORITY_NONE),
        "real_ap1_executed": False,
        "real_m03_executed": False,
        "new_empirical_result": False,
    }
    freeze = {**freeze_body, "freeze_digest": digest(freeze_body)}
    verdict = "GO" if all(gap_pass.values()) and not failures else "NO_GO"

    return {
        "schema": CONTRACT,
        "status": "RVO_07_REQUALIFICATION_COMPLETE",
        "verdict": verdict,
        "readiness": "PRE_EXECUTION_READINESS_GO" if verdict == "GO" else "PRE_EXECUTION_READINESS_NO_GO",
        "gaps": gaps,
        "failures": failures,
        "pre_result_freeze": freeze,
        "authority": dict(AUTHORITY_NONE),
        "execution_authorized": False,
        "scientific_finding": False,
        "strategy_validated": False,
        "trading_authorized": False,
        "capital_authorized": False,
    }

def _git(root: Path, *args: str) -> str:
    cp = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
    if cp.returncode != 0:
        raise RuntimeError("GIT_COMMAND_FAILED:" + " ".join(args) + ":" + cp.stderr.strip())
    return cp.stdout.strip()

def observe_owner_blobs(repo_root: Path) -> dict[str, str]:
    return {path: _git(repo_root, "rev-parse", "HEAD:" + path) for path in EXPECTED_OWNER_BLOBS}

def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--main-checkout-root", required=True)
    ap.add_argument("--workspace-receipt", required=True)
    ap.add_argument("--expected-head", required=True)
    ap.add_argument("--expected-tree", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root)
    main_root = Path(args.main_checkout_root)
    receipt_path = Path(args.workspace_receipt)
    output_path = Path(args.output)

    if _is_under(output_path, repo_root):
        raise SystemExit("BLOCKED_RVO07_OUTPUT_INSIDE_GOVERNED_WORKSPACE")
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes.decode("utf-8"))

    head = _git(repo_root, "rev-parse", "HEAD")
    tree = _git(repo_root, "rev-parse", "HEAD^{tree}")
    if head != args.expected_head:
        raise SystemExit("BLOCKED_RVO07_WORKSPACE_HEAD_MISMATCH")
    if tree != args.expected_tree:
        raise SystemExit("BLOCKED_RVO07_WORKSPACE_TREE_MISMATCH")

    workspace_clean = not bool(_git(repo_root, "status", "--porcelain", "--untracked-files=all"))
    workspace_detached = not bool(_git(repo_root, "branch", "--show-current"))
    main_checkout_clean = not bool(_git(main_root, "status", "--porcelain", "--untracked-files=all"))
    observed_owner_blobs = observe_owner_blobs(repo_root)

    result = evaluate_pre_execution_readiness(
        receipt,
        current_head=head,
        current_tree=tree,
        workspace_clean=workspace_clean,
        workspace_detached=workspace_detached,
        observed_owner_blobs=observed_owner_blobs,
        main_checkout_clean=main_checkout_clean,
        workspace_receipt_sha256=hashlib.sha256(receipt_bytes).hexdigest(),
    )
    result["observed"] = {
        "workspace_clean": workspace_clean,
        "workspace_detached": workspace_detached,
        "main_checkout_clean": main_checkout_clean,
        "workspace_receipt_path_transport": str(receipt_path),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("RVO_07_REQUALIFICATION_COMPLETE")
    print("VERDICT=" + result["verdict"])
    print("READINESS=" + result["readiness"])
    print("FREEZE_DIGEST=" + result["pre_result_freeze"]["freeze_digest"])
    for gap in ("G01", "G02", "G03", "G04", "G05"):
        print(gap + "=" + result["gaps"][gap]["status"])
    print("OUTPUT=" + str(output_path))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

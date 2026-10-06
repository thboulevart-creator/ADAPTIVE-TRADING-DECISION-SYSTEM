from __future__ import annotations

import json
from pathlib import Path

from src import rvo_09_pre_retry_requalification as r


def test_rvo09_contract_is_pre_retry_only():
    assert r.CONTRACT == "ATDS_RVO_09_PRE_RETRY_REQUALIFICATION_V0_1"
    assert r.PROFILE_ID == "P1_12C_AP1_CLAIM_SCOPED_V1"
    assert r.PROFILE_DIGEST == "7487a1ffc0adab8c60bd36caf196130402908367c676bb03ca9abe36b56c6d9c"
    assert r.RUNTIME_LOCK_DIGEST == "25a96a47d1a1e1677374974e9fe7c8dbd8e3abb37a0f3a1e0566ebd1d88fb306"


def test_protected_owner_map_binds_repaired_p1_and_unchanged_ap1():
    assert r.PROTECTED_BLOBS["src/p1_12c_qualified_producer_execution.py"] == "87d2ef49c0b70b956ada19443f5ba693cfb5b242"
    assert r.PROTECTED_BLOBS["tools/p1_12c_sandbox_runner.py"] == "78aa1615a093c241774fdea1018b69f47728ecb6"
    assert r.PROTECTED_BLOBS["tools/ap1_intraday_spread_census.py"] == "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"


def _bindings():
    return {
        "data_binding": {
            "native_data_status": "PASS_REAL_DATA_ADMISSION",
            "p1_binding_status": "P1_DATA_EVIDENCE_ACCEPTED_FOR_PLAN_BINDING",
            "dataset_identity": r.DATASET_IDENTITY,
            "ap0_manifest_sha256": r.AP0_MANIFEST_SHA256,
        },
        "invocation_profile": {
            "invocation_profile_id": r.PROFILE_ID,
            "invocation_profile_digest": r.PROFILE_DIGEST,
            "child_argv_schema_json": json.dumps({"python_flags": ["-E", "-P"]}),
            "shell": False,
        },
        "runtime_lock": {
            "runtime_lock_id": r.RUNTIME_LOCK_ID,
            "runtime_lock_digest": r.RUNTIME_LOCK_DIGEST,
            "invocation_profile_digest": r.PROFILE_DIGEST,
            "timeout_seconds": r.TIMEOUT_SECONDS,
            "execution_authority": False,
        },
        "smf_activation": {"activation_state": "ACTIVATED"},
        "smf_dry_plan": {
            "status": "M03_BINDING_PLAN_READY",
            "result_minted": False,
            "authority": {"execution": False},
        },
    }


def test_all_five_gaps_close_only_with_repaired_runtime(tmp_path: Path):
    retry_output = tmp_path / "retry.json"
    gaps = r.gap_state(
        _bindings(),
        {"clean": True, "detached": True, "main_checkout_clean": True},
        {
            "dataset_identity": r.DATASET_IDENTITY,
            "manifest_sha256": r.AP0_MANIFEST_SHA256,
            "parquet_file_count": 61,
            "parquet_content_opened": False,
        },
        {
            "dependencies": {"returncode": 0},
            "subprocess": {"returncode": 1},
            "network": {"returncode": 1},
            "dll": {"returncode": 1},
        },
        {"invocation_count": 1, "old_output_exists": False},
        retry_output,
    )
    assert gaps == {f"G0{i}": "PRE_RETRY_REQUALIFIED_CLOSED" for i in range(1, 6)}


def test_g03_reopens_if_old_runtime_digest_is_used(tmp_path: Path):
    bindings = _bindings()
    bindings["runtime_lock"]["runtime_lock_digest"] = "5b77e0c094812f3e7e9d25efdb87bd3da92748bc6f8a436ffe52cefe6d38f6c4"
    gaps = r.gap_state(
        bindings,
        {"clean": True, "detached": True, "main_checkout_clean": True},
        {
            "dataset_identity": r.DATASET_IDENTITY,
            "manifest_sha256": r.AP0_MANIFEST_SHA256,
            "parquet_file_count": 61,
            "parquet_content_opened": False,
        },
        {
            "dependencies": {"returncode": 0},
            "subprocess": {"returncode": 1},
            "network": {"returncode": 1},
            "dll": {"returncode": 1},
        },
        {"invocation_count": 1, "old_output_exists": False},
        tmp_path / "retry.json",
    )
    assert gaps["G03"] == "PRE_RETRY_REQUALIFICATION_OPEN"


def test_g05_reopens_if_history_is_not_exactly_one(tmp_path: Path):
    gaps = r.gap_state(
        _bindings(),
        {"clean": True, "detached": True, "main_checkout_clean": True},
        {
            "dataset_identity": r.DATASET_IDENTITY,
            "manifest_sha256": r.AP0_MANIFEST_SHA256,
            "parquet_file_count": 61,
            "parquet_content_opened": False,
        },
        {
            "dependencies": {"returncode": 0},
            "subprocess": {"returncode": 1},
            "network": {"returncode": 1},
            "dll": {"returncode": 1},
        },
        {"invocation_count": 0, "old_output_exists": False},
        tmp_path / "retry.json",
    )
    assert gaps["G05"] == "PRE_RETRY_REQUALIFICATION_OPEN"


def test_retry_output_preexistence_reopens_g05(tmp_path: Path):
    retry_output = tmp_path / "retry.json"
    retry_output.write_text("preexisting", encoding="utf-8")
    gaps = r.gap_state(
        _bindings(),
        {"clean": True, "detached": True, "main_checkout_clean": True},
        {
            "dataset_identity": r.DATASET_IDENTITY,
            "manifest_sha256": r.AP0_MANIFEST_SHA256,
            "parquet_file_count": 61,
            "parquet_content_opened": False,
        },
        {
            "dependencies": {"returncode": 0},
            "subprocess": {"returncode": 1},
            "network": {"returncode": 1},
            "dll": {"returncode": 1},
        },
        {"invocation_count": 1, "old_output_exists": False},
        retry_output,
    )
    assert gaps["G05"] == "PRE_RETRY_REQUALIFICATION_OPEN"


def test_authority_none_is_all_false():
    assert all(value is False for value in r.AUTHORITY_NONE.values())

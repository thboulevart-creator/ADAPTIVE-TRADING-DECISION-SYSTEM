"""P1-21 real-producer capability qualification tests.

All tests are synthetic or documentary/non-empirical. AP1 is never invoked on
the real AP0 corpus and no market result is produced.
"""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from src import p1_12c_qualified_producer_execution as p12c
from src import p1_12d_qualified_execution_evidence as p12d
from tests.p1_20_fixture import build_common_chain
from tests.p1_21_fixture import (
    AP1,
    DATA_RECEIPT,
    RUNNER,
    RUNTIME_EVIDENCE,
    build_real_capability_case,
)

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "tests" / "p1_21_ap1_profile_probe.py"


def test_p121_01_real_data_binding_preserves_native_owner_status(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    binding = case["data_binding"]
    assert p12c.is_factory_attested_real_data_owner_evidence_binding(binding)
    assert binding.native_data_status == "PASS_REAL_DATA_ADMISSION"
    assert binding.p1_binding_status == "P1_DATA_EVIDENCE_ACCEPTED_FOR_PLAN_BINDING"
    assert binding.native_data_status != "READY_FOR_EXACT_CLAIM"
    assert binding.data_owner_evidence_digest == p12c.DATA02_REAL_EVIDENCE_DIGEST
    assert binding.data_owner_receipt_blob == p12c.DATA02_REAL_RECEIPT_BLOB
    assert binding.scientific_authority is False
    assert binding.trading_authority is False


def test_p121_02_data_binding_uses_exact_dataset_manifest_fileset_schema(tmp_path: Path):
    binding = build_real_capability_case(tmp_path)["data_binding"]
    assert binding.dataset_identity == "USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert binding.ap0_manifest_sha256 == p12c.DATA02_REAL_MANIFEST_SHA256
    assert binding.dataset_file_set_digest == p12c.DATA02_REAL_FILE_SET_DIGEST
    assert binding.schema_identity == p12c.DATA02_REAL_SCHEMA_IDENTITY
    assert binding.file_count == 61
    assert binding.temporal_status == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"


def test_p121_03_stale_receipt_copy_is_rejected_before_any_data_open(tmp_path: Path):
    stale = tmp_path / "receipt.json"
    stale.write_bytes(DATA_RECEIPT.read_bytes() + b"\n")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_STALE_DATA02_RECEIPT"):
        p12c.bind_real_data_owner_evidence(stale)


def test_p121_04_ap1_invocation_profile_binds_exact_producer_and_runner(tmp_path: Path):
    profile = build_real_capability_case(tmp_path)["invocation_profile"]
    assert p12c.is_factory_attested_real_producer_invocation_profile(profile)
    assert profile.producer_id == p12c.AP1_PRODUCER_ID
    assert profile.producer_code_blob == p12c.AP1_PRODUCER_BLOB
    assert profile.invocation_profile_id == p12c.AP1_INVOCATION_PROFILE_ID
    assert profile.sandbox_runner_blob == p12c.git_blob_sha1(RUNNER)
    assert profile.shell is False
    assert profile.output_transport_identity_authority is False


def test_p121_05_ap1_child_argv_is_exact_and_contains_no_legacy_synthetic_flags(tmp_path: Path):
    profile = build_real_capability_case(tmp_path)["invocation_profile"]
    argv = p12c.build_ap1_child_argv(
        profile,
        producer_path="AP1.py",
        ap0_root_transport="AP0_ROOT",
        ap0_manifest_transport="AP0_MANIFEST.json",
        output_transport="AP1_OUTPUT.json",
    )
    assert argv == (
        "AP1.py",
        "--ap0-root", "AP0_ROOT",
        "--ap0-manifest", "AP0_MANIFEST.json",
        "--output", "AP1_OUTPUT.json",
    )
    assert "--source-root" not in argv
    assert "--parameters" not in argv
    assert "--producer-id" not in argv


def test_p121_06_sandbox_runner_forwards_ap1_profile_to_synthetic_probe_only(tmp_path: Path):
    out = tmp_path / "probe-output.json"
    cmd = [
        sys.executable,
        "-E",
        "-P",
        str(RUNNER),
        "--producer", str(PROBE),
        "--invocation-profile", p12c.AP1_INVOCATION_PROFILE_ID,
        "--ap0-root", "SYNTHETIC_AP0_ROOT_NOT_OPENED",
        "--ap0-manifest", "SYNTHETIC_AP0_MANIFEST_NOT_OPENED",
        "--output", str(out),
    ]
    completed = subprocess.run(
        cmd,
        shell=False,
        cwd=str(ROOT),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        timeout=20,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["ap0_root"] == "SYNTHETIC_AP0_ROOT_NOT_OPENED"
    assert payload["ap0_manifest"] == "SYNTHETIC_AP0_MANIFEST_NOT_OPENED"
    assert payload["real_market_data_opened"] is False
    assert payload["ap1_logic_executed"] is False


def test_p121_07_real_runtime_lock_binds_exact_material_dependencies(tmp_path: Path):
    lock = build_real_capability_case(tmp_path)["runtime_lock"]
    assert p12c.is_factory_attested_real_producer_runtime_lock(lock)
    assert lock.schema == p12c.REAL_RUNTIME_LOCK_SCHEMA
    assert lock.python_binary_sha256 == "ad169f4cb4bfb78c7a5c030a4529c19d6643276778e33994c93e145b6191c3ec"
    assert lock.numpy_version == "2.5.3"
    assert lock.pyarrow_version == "25.0.1"
    assert lock.tzdata_version == "2026.3"
    assert lock.timezone_name == "America/New_York"
    assert lock.timeout_seconds == 3600
    assert lock.execution_authority is False


def test_p121_08_runtime_lock_rejects_missing_numpy_identity(tmp_path: Path):
    legacy = build_real_capability_case(tmp_path)
    evidence = copy.deepcopy(legacy["runtime_evidence"])
    evidence["dependencies"].pop("numpy")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_NUMPY_IDENTITY_REQUIRED"):
        p12c.qualify_real_producer_runtime_lock(
            evidence,
            legacy["invocation_profile"],
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=3600,
            material_environment={"PYTHONHASHSEED": "0"},
        )


def test_p121_09_runtime_lock_rejects_version_only_dependency_identity(tmp_path: Path):
    legacy = build_real_capability_case(tmp_path)
    evidence = copy.deepcopy(legacy["runtime_evidence"])
    evidence["dependencies"]["numpy"].pop("record_sha256")
    with pytest.raises(p12c.P112CBlocked, match="REJECT_VERSION_ONLY_DEPENDENCY_IDENTITY"):
        p12c.qualify_real_producer_runtime_lock(
            evidence,
            legacy["invocation_profile"],
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=3600,
            material_environment={"PYTHONHASHSEED": "0"},
        )


def test_p121_10_runtime_lock_requires_explicit_finite_timeout(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_EXPLICIT_TIMEOUT_REQUIRED"):
        p12c.qualify_real_producer_runtime_lock(
            case["runtime_evidence"],
            case["invocation_profile"],
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=3.5,
            material_environment={},
        )
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_FINITE_TIMEOUT_REQUIRED"):
        p12c.qualify_real_producer_runtime_lock(
            case["runtime_evidence"],
            case["invocation_profile"],
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=0,
            material_environment={},
        )


def test_p121_11_real_producer_plan_is_factory_attested_and_non_authorizing(tmp_path: Path):
    plan = build_real_capability_case(tmp_path)["plan"]
    assert p12c.is_factory_attested_qualified_real_producer_execution_plan(plan)
    assert plan.native_data_status == "PASS_REAL_DATA_ADMISSION"
    assert plan.producer_id == p12c.AP1_PRODUCER_ID
    assert plan.producer_code_blob == p12c.AP1_PRODUCER_BLOB
    assert plan.expected_output_schema == p12c.AP1_OUTPUT_SCHEMA
    assert plan.expected_output_status == p12c.AP1_OUTPUT_STATUS
    assert plan.execution_authority is False
    assert plan.scientific_authority is False
    assert plan.operational_authority is False
    assert plan.trading_authority is False
    assert plan.capital_authority is False


def test_p121_12_transport_paths_do_not_change_real_plan_identity(tmp_path: Path):
    case = build_real_capability_case(tmp_path, suffix="A")
    plan_a = case["plan"]
    plan_b = p12c.qualify_real_producer_execution_plan(
        case["qualified_input"],
        case["data_binding"],
        case["invocation_profile"],
        case["runtime_lock"],
        producer_path=AP1,
        ap0_root_transport="DIFFERENT_ROOT",
        ap0_manifest_transport="DIFFERENT_MANIFEST",
        output_transport="DIFFERENT_OUTPUT",
        expected_output_schema=p12c.AP1_OUTPUT_SCHEMA,
        expected_output_status=p12c.AP1_OUTPUT_STATUS,
        expected_output_contract="ATDS_AP1_CANONICAL_JSON_OUTPUT_V1",
        maximum_output_bytes=32 * 1024 * 1024,
    )
    assert plan_a.real_producer_execution_plan_id == plan_b.real_producer_execution_plan_id
    assert plan_a.real_producer_execution_plan_digest == plan_b.real_producer_execution_plan_digest
    assert plan_a.output_transport != plan_b.output_transport


def test_p121_13_runner_command_is_structured_and_profile_bound(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    cmd = p12c.build_ap1_runner_command(
        case["plan"],
        case["invocation_profile"],
        python_executable="BOUND_PYTHON_BINARY",
        runner_path=RUNNER,
        producer_path=AP1,
    )
    assert cmd[0] == "BOUND_PYTHON_BINARY"
    assert cmd[1:3] == ("-E", "-P")
    assert "-I" not in cmd[:4]
    assert "--invocation-profile" in cmd
    assert p12c.AP1_INVOCATION_PROFILE_ID in cmd
    assert "--ap0-manifest" in cmd
    assert "--parameters" not in cmd


def test_p121_14_post_result_selection_is_fail_closed(tmp_path: Path):
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_POST_RESULT_DATA_EVIDENCE_SELECTION"):
        p12c.bind_real_data_owner_evidence(DATA_RECEIPT, result_exposed=True)
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_POST_RESULT_INVOCATION_PROFILE_SELECTION"):
        p12c.qualify_ap1_invocation_profile(AP1, result_exposed=True)


def test_p121_15_legacy_p112c_execution_and_p112d_normalization_still_work(tmp_path: Path):
    chain = build_common_chain(tmp_path, owner="P1.12C")
    assert chain["envelope"].execution_owner_id == "P1.12C"
    assert p12d.is_factory_attested_qualified_execution_evidence(chain["envelope"])
    assert chain["envelope"].measurement_input_identity == chain["native_result"].output_sha256
    assert chain["finding"].finding_status == "SUPPORTED"


def test_p121_16_real_capability_never_mints_execution_result(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    assert type(case["plan"]) is p12c.QualifiedRealProducerExecutionPlan
    assert not hasattr(case["plan"], "producer_execution_result_id")
    assert case["plan"].execution_authority is False


def test_p121_17_runtime_evidence_source_is_exactly_bound(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    assert case["runtime_lock"].runtime_evidence_source_ref == p12c.RVO06_RUNTIME_EVIDENCE_BLOB
    assert case["runtime_lock"].invocation_profile_digest == case["invocation_profile"].invocation_profile_digest


def test_p121_18_ap1_code_is_not_modified_or_duplicated_by_capability(tmp_path: Path):
    case = build_real_capability_case(tmp_path)
    assert p12c.git_blob_sha1(AP1) == p12c.AP1_PRODUCER_BLOB
    assert case["plan"].semantic_parameters_json
    parameters = json.loads(case["plan"].semantic_parameters_json)
    assert parameters["producer_configuration"] == "CODE_FROZEN_BY_EXACT_GIT_BLOB"
    assert parameters["oos_consumption"] is False

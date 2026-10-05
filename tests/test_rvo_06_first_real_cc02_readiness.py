"""RVO-06 static/non-empirical readiness qualification tests.

These tests prove the current real-AP1 route remains fail-closed. They never
invoke AP1, open the real AP0 corpus, calculate market statistics, or mint P1
real results.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: str):
    return json.loads(_text(path))


def test_rvo06_01_target_and_real_data_identity_are_exact():
    freeze = _json("GOVERNANCE/RVO-06-FIRST-REAL-CC02-PRE-RESULT-FREEZE-CANDIDATE-V0.1.json")
    assert freeze["claim"]["class"] == "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
    assert freeze["claim"]["semantic_limit"] == "RETROSPECTIVE_DESCRIPTIVE_ONLY"
    assert freeze["data"]["dataset_identity"] == "USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert freeze["data"]["manifest_sha256"] == "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert freeze["data"]["file_count"] == 61


def test_rvo06_02_real_data_admission_shape_is_not_laundered_into_p112c():
    data = _text("src/data/claim_scoped_admission.py")
    p12c = _text("src/p1_12c_qualified_producer_execution.py")
    assert '"PASS_REAL_DATA_ADMISSION"' in data
    assert '"READY_FOR_EXACT_CLAIM"' in p12c
    assert 'data_admission.get("status") != "READY_FOR_EXACT_CLAIM"' in p12c
    assert 'data_admission.get("binding_basis")' in p12c
    assert 'data_admission.get("admission_digest")' in p12c
    gaps = _json("GOVERNANCE/RVO-06-PRE-EXECUTION-OWNER-GAP-MATRIX-V0.1.json")
    assert gaps["gaps"][0]["reason"] == "BLOCKED_DATA02_REAL_ADMISSION_TO_P112C_CONTRACT_MISMATCH"


def test_rvo06_03_p112c_invocation_protocol_does_not_match_ap1_cli():
    runner = _text("tools/p1_12c_sandbox_runner.py")
    ap1 = _text("tools/ap1_intraday_spread_census.py")
    for flag in ("--source-root", "--parameters", "--producer-id"):
        assert flag in runner
        assert f'add_argument("{flag}"' not in ap1
    assert 'add_argument("--ap0-root"' in ap1
    assert 'add_argument("--ap0-manifest"' in ap1
    gaps = _json("GOVERNANCE/RVO-06-PRE-EXECUTION-OWNER-GAP-MATRIX-V0.1.json")
    assert gaps["gaps"][1]["reason"] == "BLOCKED_P1_12C_AP1_INVOCATION_CONTRACT_MISMATCH"


def test_rvo06_04_current_p112c_runtime_lock_is_synthetic_not_ap1_capable():
    p12c = _text("src/p1_12c_qualified_producer_execution.py")
    ap1 = _text("tools/ap1_intraday_spread_census.py")
    assert '"P1_12C_SYNTHETIC_RUNTIME_LOCK_V1"' in p12c
    assert '"timezone_database_identity": "NOT_USED_BY_SYNTHETIC_PRODUCER"' in p12c
    assert '"material_third_party_dependencies": []' in p12c
    assert '"timeout_seconds": 10' in p12c
    assert "import numpy as np" in ap1
    assert "import pyarrow as pa" in ap1
    assert "ZoneInfo(" in ap1
    gaps = _json("GOVERNANCE/RVO-06-PRE-EXECUTION-OWNER-GAP-MATRIX-V0.1.json")
    assert gaps["gaps"][2]["reason"] == "BLOCKED_P1_12C_RUNTIME_LOCK_NOT_AP1_CAPABLE"


def test_rvo06_05_ap1_linear_quantiles_are_not_exact_smf_procedure_identity():
    ap1 = _text("tools/ap1_intraday_spread_census.py")
    rvo05 = _text("src/rvo_05_cc02_bindings.py")
    analysis = _json("GOVERNANCE/RVO-06-AP1-SMF-M03-BINDING-ANALYSIS-V0.1.json")
    assert 'np.percentile' in ap1
    assert 'method="linear"' in ap1
    assert "smf.ecdf_quantiles" in rvo05
    assert "gitblob:{SMF_CORE_BLOB}#ecdf_quantiles" in rvo05
    assert analysis["synthetic_numeric_parity_observation"]["result"] == "PASS"
    assert analysis["option_m_a"]["verdict"] == "REJECTED"
    assert analysis["final"] == "BLOCKED_SMF_AP1_METHOD_BINDING"


def test_rvo06_06_no_real_p1_chain_or_manifest_is_minted_after_blocker():
    freeze = _json("GOVERNANCE/RVO-06-FIRST-REAL-CC02-PRE-RESULT-FREEZE-CANDIDATE-V0.1.json")
    assert freeze["status"] == "BLOCKED_NOT_EXECUTION_READY"
    assert freeze["p1"]["experiment_spec_id"] == "NOT_MINTED_FAIL_CLOSED"
    assert freeze["p1"]["p1_12c_plan_id"] == "NOT_MINTED_FAIL_CLOSED"
    assert freeze["smf"]["activation_digests"] == "NOT_MINTED_AFTER_BLOCKER"
    assert freeze["rvo_pre_result_manifest_digest"] == "NOT_MINTED_FAIL_CLOSED"
    assert freeze["result_exposed"] is False


def test_rvo06_07_runtime_observation_is_evidence_not_p112c_lock():
    runtime = _json("GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json")
    assert runtime["status"] == "OBSERVED_RUNTIME_EVIDENCE_NOT_P1_12C_RUNTIME_LOCK"
    assert runtime["device"]["python_version"] == "3.13.14"
    assert runtime["dependencies"]["numpy"]["version"] == "2.5.3"
    assert runtime["dependencies"]["pyarrow"]["version"] == "25.0.1"
    assert runtime["dependencies"]["tzdata"]["version"] == "2026.3"
    assert runtime["data_resources"]["parquet_file_count"] == 61
    assert runtime["output_destination_probe"]["market_result_written"] is False


def test_rvo06_08_single_run_package_is_explicit_no_go_and_non_authorizing():
    package = _json("GOVERNANCE/RVO-06-SINGLE-RUN-EXECUTION-AUTHORIZATION-PACKAGE-V0.1.json")
    assert package["status"] == "BLOCKED_NOT_AUTHORIZING"
    assert package["go_no_go"] == "NO_GO"
    assert package["may_authorize_execution"] is False
    assert package["real_ap1_invocation"] is False
    assert package["real_result_exposed"] is False


def test_rvo06_09_frozen_readiness_breaker_contract_is_complete_and_pre_execution():
    contract = _json("GOVERNANCE/RVO-06-FROZEN-READINESS-BREAKER-CONTRACT-V0.1.json")
    assert contract["status"] == "FROZEN_PRE_EXECUTION"
    assert [x["id"] for x in contract["cases"]] == [f"RVO06-B{i:02d}" for i in range(1, 24)]
    assert contract["executable_breaker_present"] is False
    assert contract["real_ap1_execution"] is False


def test_rvo06_10_temporal_scope_is_not_escalated():
    freeze = _json("GOVERNANCE/RVO-06-FIRST-REAL-CC02-PRE-RESULT-FREEZE-CANDIDATE-V0.1.json")
    assert freeze["claim"]["temporal"] == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
    assert freeze["claim"]["predictive"] is False
    assert freeze["claim"]["historical_tradability"] is False
    assert freeze["claim"]["oos"] is False
    assert freeze["claim"]["profitability"] is False


def test_rvo06_11_ap1_output_contract_is_frozen_without_invocation():
    freeze = _json("GOVERNANCE/RVO-06-FIRST-REAL-CC02-PRE-RESULT-FREEZE-CANDIDATE-V0.1.json")
    assert freeze["producer"]["code_blob"] == "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
    assert freeze["producer"]["expected_output_schema"] == "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    assert freeze["producer"]["expected_output_status"] == "AP1_COMPLETE"
    assert freeze["producer"]["max_output_bytes"] == 32 * 1024 * 1024


def test_rvo06_12_final_readiness_is_no_go_without_authority_expansion():
    gaps = _json("GOVERNANCE/RVO-06-PRE-EXECUTION-OWNER-GAP-MATRIX-V0.1.json")
    freeze = _json("GOVERNANCE/RVO-06-FIRST-REAL-CC02-PRE-RESULT-FREEZE-CANDIDATE-V0.1.json")
    assert gaps["final_verdict"] == "BLOCKED_MULTIPLE_PRE_EXECUTION_OWNER_GAPS"
    assert freeze["execution_authorization"] is False
    assert freeze["authority"] == {
        "rvo": "NONE",
        "scientific": False,
        "operational": False,
        "trading": False,
        "capital": False,
    }

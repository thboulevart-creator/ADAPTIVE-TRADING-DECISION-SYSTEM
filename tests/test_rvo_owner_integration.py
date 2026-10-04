"""RVO-03 synthetic integration with canonical owner interfaces."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import rvo_orchestrator as rvo
from src import rvo_owner_adapters as owners
from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case

P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
P1_AUTHORITY_ID = "RVO_03_SYNTHETIC_P1_CAPTURE_AUTHORITY_V1"
MATRIX_BLOB_EXPECTED = "5f2406189af8e118ca8f20f5a7f92f3a2ce91c13"


def _p1_synthetic_spec(tmp_path: Path):
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="RVO03_SYNTHETIC")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)

    capture = persist_witnessed_memory_episode(
        tmp_path / "p1-memory",
        episode,
        authority_id=P1_AUTHORITY_ID,
    )
    historical = reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=P1_AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )
    scope = create_audit_scope(
        question="What synthetic experiment should RVO-03 bind?",
        expected_registration_ids=(historical.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (historical,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Specify an RVO-03 synthetic canonical-owner integration experiment.",
    )
    request = produce_follow_up_request(revision)
    return specify_experiment(
        request,
        hypothesis_statement="Canonical owner interfaces remain semantically separate under RVO.",
        prediction="RVO binds qualified owners without acquiring their authority.",
        falsification_rule="Any owner semantic rewrite or authority expansion falsifies the integration.",
        protocol="Synthetic canonical owner-interface calls only.",
        measurement_plan="Record exact native owner outputs and capability states.",
    )


def _pcp_expected_observed():
    expected = {
        "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        "origin": "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM.git",
        "branch": "integration/system-v1",
        "head": "1" * 40,
        "tree": "2" * 40,
        "protected_artifacts": {
            "GOVERNANCE/RVO-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json": "3" * 40,
        },
    }
    observed = {
        **expected,
        "detached_head": False,
        "working_tree_state": "CLEAN",
        "untracked_files": False,
        "tracked_modifications": False,
        "protected_artifacts": {
            "GOVERNANCE/RVO-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json": {
                "path": "GOVERNANCE/RVO-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json",
                "exists": True,
                "observed_blob": "3" * 40,
            }
        },
    }
    return expected, observed


def _pcp_evidence():
    return {
        "operation_id": "RVO-03-SYNTHETIC-PCP",
        "operation_class": "TEST_OR_PROBE",
        "command_or_check": "synthetic owner-interface compatibility",
        "start_head": "1" * 40,
        "start_tree": "2" * 40,
        "end_head": "1" * 40,
        "end_tree": "2" * 40,
        "exit_code": 0,
        "stdout": "synthetic only",
        "stderr": "",
        "files_changed": [],
        "test_results": [{"name": "RVO03_SYNTHETIC", "status": "PASS"}],
        "probe_results": [{"name": "RVO_AUTHORITY", "status": "PASS", "details": "NONE"}],
        "artifact_hashes": {},
        "started_at_utc": "2026-10-04T00:00:00Z",
        "finished_at_utc": "2026-10-04T00:00:01Z",
        "authority_reference": "RVO-03-SYNTHETIC-NON-AUTHORITATIVE",
        "final_status": "PASS",
    }


def test_capability_matrix_is_exact_and_does_not_launder_gaps():
    matrix = owners.load_capability_matrix()
    rows = {row["capability_id"]: row for row in matrix["capabilities"]}
    assert matrix["authority"]["rvo_authority"] == "NONE"
    assert rows["P1_EXPERIMENT_SPECIFICATION"]["state"] == "QUALIFIED"
    assert rows["SMF_CORE_ACTIVATION_M01_M11"]["state"] == "QUALIFIED"
    assert rows["SMF_CONDITIONAL_C01_C12"]["state"] == "BLOCKED"
    assert rows["MCEPR_MINIMAL_REGISTRY"]["state"] == "QUALIFIED"
    assert rows["PCP_P22_01_STATE_PROJECTOR"]["state"] == "QUALIFIED"
    assert rows["PCP_P22_02_IDENTITY_VERIFIER"]["state"] == "QUALIFIED"
    assert rows["PCP_P22_03_EVIDENCE_ENVELOPE"]["state"] == "QUALIFIED"
    assert rows["DATASET_ADMISSIBILITY_TICK_CSV"]["state"] == "AVAILABLE"
    assert rows["TEMPORAL_GENERIC_POINT_IN_TIME"]["state"] == "UNAVAILABLE"
    assert rows["EXECUTION_GENERIC"]["state"] == "UNAVAILABLE"
    assert rows["EXECUTION_E1_SPECIFIC"]["state"] == "QUALIFIED"
    assert rows["EXECUTION_E1_SPECIFIC"]["generic_for_rvo"] is False


def test_owner_contract_identities_are_exact():
    assert owners.owner_interface_identities() == owners.EXPECTED_OWNER_CONTRACTS


def test_real_p1_experiment_specification_interface_binds_synthetically(tmp_path: Path):
    spec = _p1_synthetic_spec(tmp_path)
    binding = owners.bind_p1_experiment_specification(spec)
    assert binding["capability_state"] == "QUALIFIED"
    assert binding["experiment_spec_id"] == spec.experiment_spec_id
    assert binding["source_verdict"] == spec.source_verdict
    assert binding["source_completeness_status"] == spec.source_completeness_status
    assert binding["source_independence_status"] == spec.source_independence_status
    assert binding["rvo_authority"] == "NONE"


def test_real_smf_core_activation_interface_is_used_before_result():
    bound = owners.create_smf_activation(
        claim_definition_ref="claim:rvo03:synthetic",
        failure_mode_ref="DEPENDENCE_AWARE_INFERENCE",
        method_family_ref="M05",
        validity_scope_ref="scope:rvo03:synthetic",
        assumption_set_ref="assumptions:rvo03:synthetic",
        activation_reason="synthetic canonical-owner integration",
        activation_rule="activate M05 before synthetic result exposure",
        parameter_selection_policy={"scheme": "predeclared-synthetic"},
        dependency_refs=["P1_EXPERIMENT_SPECIFICATION"],
        activation_state="ACTIVATED",
        result_exposed=False,
    )
    payload = bound["owner_payload"]
    assert bound["capability_state"] == "QUALIFIED"
    assert payload["activation_state"] == "ACTIVATED"
    assert payload["method_family_ref"] == "M05"
    assert payload["activation_digest"].startswith("sha256:")


def test_real_mcepr_interface_builds_and_validates_synthetic_segment():
    bound = owners.create_mcepr_synthetic_segment(
        source_blob="d83685b23938b4b7baa9ab098416aa1e1178ab67"
    )
    assert bound["capability_state"] == "QUALIFIED"
    assert bound["event"]["event_id"].startswith("EVT-")
    assert bound["segment"]["registry_id"].startswith("RGS-")
    assert bound["validation"]["status"] == "PASS"
    assert bound["rvo_authority"] == "NONE"


def test_real_pcp_interfaces_preserve_non_authority():
    projected = owners.project_pcp_state(
        {
            "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
            "branch": "integration/system-v1",
            "head": "1" * 40,
            "tree": "2" * 40,
            "working_tree_state": "CLEAN",
        }
    )
    assert projected["owner_payload"]["projection_authority"] is False
    assert projected["owner_payload"]["cache_authority"] is False

    expected, observed = _pcp_expected_observed()
    verified = owners.verify_pcp_identity(observed, expected)
    assert verified["owner_payload"]["final_status"] == "PASS"

    evidence = owners.build_pcp_evidence(_pcp_evidence())
    assert evidence["validation"]["status"] == "PASS"
    assert evidence["owner_payload"]["envelope_authority"] is False
    assert evidence["owner_payload"]["operation_authorized_by_envelope"] is False


def test_real_data_interface_is_available_but_not_promoted_to_qualified(tmp_path: Path):
    dataset = tmp_path / "synthetic_ticks.csv"
    dataset.write_text(
        "timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
        "2026-01-01T00:00:00Z,100.2,100.0,5,4\n"
        "2026-01-01T00:00:01Z,100.3,100.1,6,5\n",
        encoding="utf-8",
    )
    bound = owners.assess_tick_dataset(
        dataset,
        dataset_id="RVO03-SYNTHETIC",
        dataset_version="v1",
        instrument="SYNTHETIC",
        granularity="tick",
        timezone_storage="UTC",
    )
    assert bound["capability_state"] == "AVAILABLE"
    assert bound["owner_payload"]["verdict"] == "PASS"
    assert bound["rvo_authority"] == "NONE"


def test_missing_generic_temporal_and_execution_capabilities_fail_closed():
    with pytest.raises(owners.RVOOwnerBlocked, match="TEMPORAL_GENERIC_POINT_IN_TIME:UNAVAILABLE"):
        owners.require_temporal_generic()
    with pytest.raises(owners.RVOOwnerBlocked, match="EXECUTION_GENERIC:UNAVAILABLE"):
        owners.require_execution_generic()


def test_e1_execution_owner_is_qualified_but_stays_scope_specific():
    bound = owners.execute_e1_specific_synthetic(
        current_position=0,
        target_position=1,
        signal_h1_end_ms=1000,
        raw_ticks=[
            {"timestamp_ms": 999, "bid": 99.0, "ask": 100.0, "continuity_status": "CONTINUOUS"},
            {"timestamp_ms": 1000, "bid": 100.0, "ask": 101.0, "continuity_status": "CONTINUOUS"},
        ],
    )
    assert bound["capability_state"] == "QUALIFIED"
    assert bound["generic_for_rvo"] is False
    assert bound["owner_payload"]["status"] == "EXECUTED"
    assert bound["cost_scope"]["commission"] == {"included": False, "assumed_zero": False}
    assert bound["cost_scope"]["slippage"] == {"included": False, "assumed_zero": False}
    assert bound["cost_scope"]["financing"] == {"included": False, "assumed_zero": False}
    assert "ALL_IN_COST_PROFITABILITY" in bound["forbidden_claims"]


def test_end_to_end_structural_synthetic_integration_preserves_capability_semantics(tmp_path: Path):
    spec = _p1_synthetic_spec(tmp_path)
    p1 = owners.bind_p1_experiment_specification(spec)
    smf = owners.create_smf_activation(
        claim_definition_ref="claim:rvo03:structural",
        failure_mode_ref="DEPENDENCE_AWARE_INFERENCE",
        method_family_ref="M05",
        validity_scope_ref="scope:rvo03:structural",
        assumption_set_ref="assumptions:rvo03:structural",
        activation_reason="structural synthetic integration",
        activation_rule="pre-result",
        parameter_selection_policy={"scheme": "synthetic"},
        dependency_refs=["P1-SPEC"],
        activation_state="ACTIVATED",
        result_exposed=False,
    )
    mcepr = owners.create_mcepr_synthetic_segment(
        source_blob="d83685b23938b4b7baa9ab098416aa1e1178ab67"
    )
    expected, observed = _pcp_expected_observed()
    pcp = owners.verify_pcp_identity(observed, expected)

    dataset = tmp_path / "integration_ticks.csv"
    dataset.write_text(
        "timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
        "2026-01-01T00:00:00Z,100.2,100.0,5,4\n",
        encoding="utf-8",
    )
    data = owners.assess_tick_dataset(
        dataset,
        dataset_id="RVO03-INTEGRATION",
        dataset_version="v1",
        instrument="SYNTHETIC",
        granularity="tick",
        timezone_storage="UTC",
    )

    catalog = rvo.build_control_catalog(
        [
            {
                "control_id": "P1-SPEC", "owner_id": "P1",
                "owner_contract_ref": p1["owner_contract"],
                "failure_mode_refs": ["EXPERIMENT_SPECIFICATION_IDENTITY"],
                "applicability_rule_ref": "rule:rvo03:p1",
                "input_contract_ref": "p1:request",
                "output_contract_ref": "p1:experiment-spec",
                "dependency_control_ids": [],
                "native_status_schema_ref": "p1:source-verdict",
                "blocking_rule_ref": "p1:native-boundary",
                "reconstructibility_contract_ref": "rvo03:p1-replay",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "SMF-ACT", "owner_id": "SMF",
                "owner_contract_ref": smf["owner_contract"],
                "failure_mode_refs": ["DEPENDENCE_AWARE_INFERENCE"],
                "applicability_rule_ref": "rule:rvo03:smf",
                "input_contract_ref": "smf:activation-input",
                "output_contract_ref": "smf:activation-record",
                "dependency_control_ids": ["P1-SPEC"],
                "native_status_schema_ref": "smf:activation-state",
                "blocking_rule_ref": "smf:native-boundary",
                "reconstructibility_contract_ref": "rvo03:smf-replay",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "MCEPR", "owner_id": "MCEPR",
                "owner_contract_ref": mcepr["owner_contract"],
                "failure_mode_refs": ["SEARCH_PROVENANCE"],
                "applicability_rule_ref": "rule:rvo03:mcepr",
                "input_contract_ref": "mcepr:event",
                "output_contract_ref": "mcepr:registry-validation",
                "dependency_control_ids": [],
                "native_status_schema_ref": "mcepr:validation-status",
                "blocking_rule_ref": "mcepr:native-boundary",
                "reconstructibility_contract_ref": "rvo03:mcepr-replay",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "PCP", "owner_id": "PCP",
                "owner_contract_ref": pcp["owner_contract"],
                "failure_mode_refs": ["IDENTITY_STATE_DRIFT"],
                "applicability_rule_ref": "rule:rvo03:pcp",
                "input_contract_ref": "pcp:identity-input",
                "output_contract_ref": "pcp:identity-verification",
                "dependency_control_ids": [],
                "native_status_schema_ref": "pcp:final-status",
                "blocking_rule_ref": "pcp:native-boundary",
                "reconstructibility_contract_ref": "rvo03:pcp-replay",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "DATA", "owner_id": "DATA",
                "owner_contract_ref": "src/data/dataset_admissibility.py",
                "failure_mode_refs": ["DATA_IDENTITY_OR_ADMISSIBILITY"],
                "applicability_rule_ref": "rule:rvo03:data",
                "input_contract_ref": "data:tick-csv",
                "output_contract_ref": "data:admissibility-report",
                "dependency_control_ids": [],
                "native_status_schema_ref": "data:verdict",
                "blocking_rule_ref": "data:native-boundary",
                "reconstructibility_contract_ref": "rvo03:data-replay",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "TEMPORAL-GENERIC", "owner_id": "TEMPORAL",
                "owner_contract_ref": "docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md",
                "failure_mode_refs": ["HISTORICAL_POINT_IN_TIME"],
                "applicability_rule_ref": "rule:rvo03:temporal",
                "input_contract_ref": "temporal:generic",
                "output_contract_ref": "temporal:generic",
                "dependency_control_ids": ["DATA"],
                "native_status_schema_ref": "temporal:native",
                "blocking_rule_ref": "temporal:missing-capability",
                "reconstructibility_contract_ref": "rvo03:temporal",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
            {
                "control_id": "EXECUTION-GENERIC", "owner_id": "EXECUTION",
                "owner_contract_ref": "UNAVAILABLE_GENERIC_EXECUTION_OWNER",
                "failure_mode_refs": ["GENERIC_EXECUTION_REALISM"],
                "applicability_rule_ref": "rule:rvo03:execution",
                "input_contract_ref": "execution:generic",
                "output_contract_ref": "execution:generic",
                "dependency_control_ids": ["DATA"],
                "native_status_schema_ref": "execution:native",
                "blocking_rule_ref": "execution:missing-capability",
                "reconstructibility_contract_ref": "rvo03:execution",
                "validity_scope": "RVO03_STRUCTURAL_SYNTHETIC",
            },
        ],
        catalog_version="RVO03-CANONICAL-OWNER-INTEGRATION-V1",
    )

    pre = rvo.build_pre_snapshot(
        repository="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        branch="integration/system-v1",
        head="1" * 40,
        tree="2" * 40,
        dataset_refs=[data["owner_payload"]["dataset"]["content_hash"]],
        temporal_ref="TEMPORAL_GENERIC_UNAVAILABLE",
        execution_ref="EXECUTION_GENERIC_UNAVAILABLE",
        smf_activation_refs=[smf["owner_payload"]["activation_digest"]],
        mcepr_pre_ref=mcepr["segment"]["registry_id"],
        oos_pre_state="NOT_CONSUMED_SYNTHETIC",
        environment_identity="rvo03:synthetic:environment",
        owner_contract_refs={
            "P1": p1["owner_contract"], "SMF": smf["owner_contract"],
            "MCEPR": mcepr["owner_contract"], "PCP": pcp["owner_contract"],
            "DATA": "src/data/dataset_admissibility.py",
            "TEMPORAL": "UNAVAILABLE_GENERIC",
            "EXECUTION": "UNAVAILABLE_GENERIC",
        },
    )

    applicability = [
        {"control_id": "P1-SPEC", "applicability_state": "APPLICABLE", "applicability_basis": "structural claim starts from exact P1 spec", "material": True},
        {"control_id": "SMF-ACT", "applicability_state": "APPLICABLE", "applicability_basis": "synthetic method activation is under test", "material": True},
        {"control_id": "MCEPR", "applicability_state": "APPLICABLE", "applicability_basis": "cross-experiment provenance interface is under test", "material": True},
        {"control_id": "PCP", "applicability_state": "APPLICABLE", "applicability_basis": "identity-state interface is under test", "material": True},
        {"control_id": "DATA", "applicability_state": "APPLICABLE", "applicability_basis": "available tick-data interface compatibility is under test", "material": True},
        {"control_id": "TEMPORAL-GENERIC", "applicability_state": "NOT_APPLICABLE", "applicability_basis": "structural synthetic claim makes no historical point-in-time assertion", "material": True},
        {"control_id": "EXECUTION-GENERIC", "applicability_state": "NOT_APPLICABLE", "applicability_basis": "structural synthetic claim makes no execution/profitability assertion", "material": True},
    ]
    manifest = rvo.build_pre_result_manifest(
        catalog=catalog,
        experiment_spec_id=p1["experiment_spec_id"],
        claim_ref="claim:rvo03:structural",
        estimand_ref="estimand:rvo03:interface-compatibility",
        validity_scope_ref="scope:rvo03:structural",
        pre_snapshot=pre,
        applicability_records=applicability,
        method_bindings={
            "SMF-ACT": {
                "p1_method_ref": "SMF:M05",
                "activation_digest": smf["owner_payload"]["activation_digest"],
                "qualified_method_ref": "blob:b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb",
                "claim_ref": "claim:rvo03:structural",
                "failure_mode_ref": "DEPENDENCE_AWARE_INFERENCE",
                "assumption_set_ref": "assumptions:rvo03:structural",
                "parameter_policy_ref": "params:rvo03:synthetic",
                "dependency_refs": ["P1-SPEC"],
            }
        },
        result_exposed=False,
    )

    native = {
        "P1-SPEC": p1["source_verdict"],
        "SMF-ACT": smf["owner_payload"]["activation_state"],
        "MCEPR": mcepr["validation"]["status"],
        "PCP": pcp["owner_payload"]["final_status"],
        "DATA": data["owner_payload"]["verdict"],
    }
    assert set(manifest["routing_plan"]) == set(native)
    results = [
        rvo.bind_owner_result(
            control_id=cid,
            owner_id=next(x["owner_id"] for x in catalog["controls"] if x["control_id"] == cid),
            native_status_schema_ref=next(x["native_status_schema_ref"] for x in catalog["controls"] if x["control_id"] == cid),
            native_status=status,
            asserted_native_status=status,
            orchestration_state="READY",
            blocking_rule_ref=None,
            snapshot_digest=pre["pre_snapshot_digest"],
        )
        for cid, status in sorted(native.items())
    ]
    assert rvo.aggregate_procedural_state(results) == "PACKAGE_COMPLETE"
    assert data["capability_state"] == "AVAILABLE"
    assert rvo.RVO_AUTHORITY == "NONE"


def test_applicable_generic_historical_profitability_claim_is_blocked_not_passed():
    with pytest.raises(owners.RVOOwnerBlocked):
        owners.require_temporal_generic()
    with pytest.raises(owners.RVOOwnerBlocked):
        owners.require_execution_generic()
    assert "TEMPORAL_GENERIC_POINT_IN_TIME is UNAVAILABLE." in owners.unresolved_capability_gaps()
    assert any("EXECUTION_GENERIC is UNAVAILABLE" in item for item in owners.unresolved_capability_gaps())

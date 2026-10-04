"""RVO-05 claim-scoped binding adapters for the first CC02 route.

RVO owns only orchestration/binding. This module does not alter P1, SMF, Data,
Temporal, MCEPR, PCP or Execution semantics and grants no authority.
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from src import rvo_orchestrator as rvo
from src import rvo_owner_adapters as owner_adapters
from src.data import claim_scoped_admission as data02
from src import experiment_specification as p1_spec
from src import experiment_execution_binding as p1_binding
from src import qualified_experiment_execution_input as p1_qei
from src import linked_experiment_execution as p1_exec
from src import experiment_evaluation_submission as p1_eval
from src import experiment_measurement_provenance as p1_prov
from src import experiment_evaluator_authority as p1_auth
from src import qualified_experimental_finding as p1_find
from tools import smf03_core_foundation as smf
from src.research import input_binding as research_input_binding

CONTRACT = "ATDS_RVO_05_CC02_BINDING_V0_1"
BUNDLE_SCHEMA = "ATDS_RVO_05_SMF_METHOD_BUNDLE_V0_1"
SMF_RESULT_SCHEMA = "ATDS_RVO_05_SMF_RESULT_BINDING_V0_1"
RVO_AUTHORITY = "NONE"

CLAIM_CLASS = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
SEMANTIC_LIMIT = "RETROSPECTIVE_DESCRIPTIVE_ONLY"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
CONSUMER_ID = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
CLAIM_SCOPE_ID = f"{CLAIM_CLASS}:{SEMANTIC_LIMIT}:{CONSUMER_ID}"
SMF_CORE_BLOB = "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
P1_LINKED_EXECUTION_BLOB = "f2fa07178134e04963d42d1fbdda1a8f7bad179d"
P1_ENGINE = "BI5ResearchEngine"
TARGET_DATA_FAMILY = "AP0_PARQUET"

class RVO05Error(RuntimeError):
    pass

def _decision(status: str, reason: str, **extra: object) -> dict[str, Any]:
    out: dict[str, Any] = {
        "contract": CONTRACT,
        "status": status,
        "reason": reason,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
        "rvo_authority": RVO_AUTHORITY,
    }
    out.update(extra)
    return out

def _activation_payload(value: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    payload = value.get("owner_payload")
    if isinstance(payload, Mapping):
        return payload
    return value

def validate_data_admission(admission, *, expected_digest: str) -> dict[str, Any]:
    if not isinstance(admission, Mapping):
        return _decision("BLOCKED", "BLOCKED_DATA02_ADMISSION_REQUIRED")
    if admission.get("contract") != data02.CONTRACT or admission.get("status") != "READY_FOR_EXACT_CLAIM":
        return _decision("BLOCKED", "BLOCKED_DATA02_ADMISSION_REQUIRED")
    if admission.get("admission_digest") != expected_digest:
        return _decision("BLOCKED", "BLOCKED_DATA02_ADMISSION_DIGEST_MISMATCH")
    basis = admission.get("binding_basis")
    if not isinstance(basis, Mapping) or basis.get("dataset_identity") != DATASET_IDENTITY:
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    if basis.get("claim_scope_id") != CLAIM_SCOPE_ID:
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    for key in ("scientific_authority","operational_authority","trading_authority","capital_authority"):
        if admission.get(key) is True:
            return _decision("BLOCKED", "REJECT_DATA_TO_SCIENCE_LAUNDERING")
    if admission.get("rvo_authority") not in (None, "NONE"):
        return _decision("BLOCKED", "REJECT_DATA_TO_SCIENCE_LAUNDERING")
    return _decision(
        "READY",
        "DATA02_ADMISSION_BOUND",
        admission_digest=str(admission["admission_digest"]),
        dataset_identity=DATASET_IDENTITY,
        binding_basis=dict(basis),
    )

def validate_authority_claims(claims, *, source: str) -> dict[str, Any]:
    if not isinstance(claims, Mapping):
        return _decision("BLOCKED", "REJECT_RVO_AUTHORITY_EXPANSION")
    if any(value is True for value in claims.values()):
        reason = "REJECT_DATA_TO_SCIENCE_LAUNDERING" if source == "DATA" else "REJECT_RVO_AUTHORITY_EXPANSION"
        return _decision("BLOCKED", reason)
    return _decision("READY", "NO_AUTHORITY_EXPANSION")

def activate_required_smf(
    *,
    result_exposed: bool = False,
    claim_ref: str = "claim:rvo05:cc02",
    validity_scope_ref: str = "scope:rvo05:cc02",
) -> dict[str, Any]:
    if result_exposed:
        try:
            owner_adapters.create_smf_activation(
                claim_definition_ref=claim_ref,
                failure_mode_ref="ESTIMAND_DRIFT",
                method_family_ref="M01",
                validity_scope_ref=validity_scope_ref,
                assumption_set_ref="assumptions:rvo05:descriptive",
                activation_reason="freeze claim/estimand before result",
                activation_rule="pre-result",
                parameter_selection_policy={"policy":"frozen-before-result"},
                dependency_refs=["P1-SPEC"],
                activation_state="ACTIVATED",
                result_exposed=True,
            )
        except ValueError as exc:
            if "METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE" in str(exc):
                return _decision("BLOCKED", "BLOCKED_POST_RESULT_METHOD_ACTIVATION")
            raise
        return _decision("BLOCKED", "BLOCKED_POST_RESULT_METHOD_ACTIVATION")

    m01 = owner_adapters.create_smf_activation(
        claim_definition_ref=claim_ref,
        failure_mode_ref="ESTIMAND_DRIFT",
        method_family_ref="M01",
        validity_scope_ref=validity_scope_ref,
        assumption_set_ref="assumptions:rvo05:descriptive",
        activation_reason="preregister exact CC02 claim and estimand before result exposure",
        activation_rule="M01 required before descriptive measurement",
        parameter_selection_policy={"policy":"claim-and-estimand-frozen"},
        dependency_refs=["P1-SPEC"],
        activation_state="ACTIVATED",
        result_exposed=False,
    )
    m03 = owner_adapters.create_smf_activation(
        claim_definition_ref=claim_ref,
        failure_mode_ref="EMPIRICAL_DISTRIBUTION_QUANTILE_SUMMARY",
        method_family_ref="M03",
        validity_scope_ref=validity_scope_ref,
        assumption_set_ref="assumptions:empirical-distribution-no-inference",
        activation_reason="AP1 declares empirical percentile summaries",
        activation_rule="M03 required when empirical distribution/quantiles are claimed",
        parameter_selection_policy={"probabilities":[0.5,0.9,0.95,0.99],"quantile_method":"linear"},
        dependency_refs=["P1-SPEC","DATA-02","SMF-M01"],
        activation_state="ACTIVATED",
        result_exposed=False,
    )
    return {"M01":m01,"M03":m03}

def build_method_bundle(activations: Mapping[str, Any]) -> dict[str, Any]:
    m01 = _activation_payload(activations.get("M01"))
    m03 = _activation_payload(activations.get("M03"))
    if not isinstance(m01, Mapping) or not isinstance(m03, Mapping):
        raise RVO05Error("ACTIVATION_BUNDLE_INCOMPLETE")
    seed = {
        "claim_ref": m01.get("claim_definition_ref"),
        "m01_activation_digest": m01.get("activation_digest"),
        "m03_activation_digest": m03.get("activation_digest"),
        "qualified_implementation_blob": SMF_CORE_BLOB,
    }
    p1_method_ref = "RVO05:SMF:M01+M03:" + rvo.canonical_sha256(seed)[:32]
    body = {
        "schema": BUNDLE_SCHEMA,
        "claim_ref": m01.get("claim_definition_ref"),
        "m01_activation": dict(m01),
        "m03_activation": dict(m03),
        "qualified_implementation_blob": SMF_CORE_BLOB,
        "p1_method_ref": p1_method_ref,
    }
    return {**body,"bundle_digest":rvo.canonical_sha256(body)}

def validate_method_bundle(bundle) -> dict[str, Any]:
    required={"schema","claim_ref","m01_activation","m03_activation","qualified_implementation_blob","p1_method_ref","bundle_digest"}
    if not isinstance(bundle, Mapping) or not required.issubset(bundle):
        return _decision("BLOCKED", "BLOCKED_LABEL_ONLY_P1_METHOD_REF")
    if not str(bundle.get("p1_method_ref","")).startswith("RVO05:SMF:"):
        return _decision("BLOCKED", "BLOCKED_LABEL_ONLY_P1_METHOD_REF")
    m01=_activation_payload(bundle.get("m01_activation"))
    m03=_activation_payload(bundle.get("m03_activation"))
    if not isinstance(m01,Mapping):
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M01_OMITTED")
    if not isinstance(m03,Mapping):
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M03_OMITTED")
    if m01.get("method_family_ref")!="M01" or m01.get("activation_state")!="ACTIVATED":
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M01_OMITTED")
    if m03.get("method_family_ref")!="M03":
        return _decision("BLOCKED", "BLOCKED_WRONG_SMF_METHOD_FAMILY")
    if m03.get("activation_state")!="ACTIVATED":
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M03_OMITTED")
    if bundle.get("qualified_implementation_blob")!=SMF_CORE_BLOB:
        return _decision("BLOCKED", "BLOCKED_SMF_IMPLEMENTATION_IDENTITY")
    return _decision("READY", "EXACT_SMF_METHOD_BUNDLE_BOUND",p1_method_ref=bundle["p1_method_ref"])

def validate_p1_chain_identity(record) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    if record.get("evaluation_submission_id") != record.get("finding_evaluation_submission_id"):
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    return _decision("READY", "P1_CHAIN_IDENTITY_MATCH")

def preserve_native_status(native_status: str, asserted_status: str, *, owner: str) -> dict[str, Any]:
    if native_status == asserted_status:
        return _decision("READY", "NATIVE_STATUS_PRESERVED",native_status=native_status)
    if owner=="P1":
        return _decision("BLOCKED", "REJECT_P1_STATUS_REWRITE")
    if owner=="SMF":
        return _decision("BLOCKED", "REJECT_SMF_STATUS_REWRITE")
    return _decision("BLOCKED", "REJECT_STATUS_LAUNDERING")

def validate_smf_route(metric_contract, *, activated_families: Sequence[str]) -> dict[str, Any]:
    metrics = metric_contract if isinstance(metric_contract, Mapping) else {}
    percentiles = metrics.get("percentiles") or []
    activated = list(activated_families)
    if "M01" not in activated:
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M01_OMITTED")
    if percentiles and "M03" not in activated:
        return _decision("BLOCKED", "BLOCKED_REQUIRED_M03_OMITTED")
    allowed={"M01","M03"}
    if any(item not in allowed for item in activated):
        return _decision("BLOCKED", "BLOCKED_UNJUSTIFIED_SMF_ACTIVATION")
    return _decision("READY", "SMF_ROUTE_EXACT_M01_M03",required=["M01","M03"])

def validate_temporal_scope(claim_flags, temporal_state: str) -> dict[str, Any]:
    flags = claim_flags if isinstance(claim_flags,Mapping) else {}
    expanded=any(flags.get(k) is True for k in ("predictive","historical","historical_tradability","oos","profitability"))
    if expanded and temporal_state=="NOT_APPLICABLE_WITH_EXPLICIT_BASIS":
        return _decision("BLOCKED", "BLOCKED_TEMPORAL_OWNER_REQUIRED")
    return _decision("READY", "TEMPORAL_SCOPE_PRESERVED")

def validate_reconstruction_claim(*, runtime_attestation: bool, durable_inputs: bool) -> dict[str, Any]:
    if runtime_attestation and not durable_inputs:
        return _decision("BLOCKED", "BLOCKED_RUNTIME_ATTESTATION_NOT_DURABLE")
    return _decision("READY", "RECONSTRUCTION_CLASS_NOT_ESCALATED")

def validate_pre_post_use(*, pre_digest: str, post_used_as_pre: bool) -> dict[str, Any]:
    if post_used_as_pre:
        return _decision("BLOCKED", "REJECT_POST_TO_PRE_REWRITE")
    return _decision("READY", "PRE_POST_SEPARATION_PRESERVED",pre_digest=pre_digest)

def validate_global_claim(claim: str) -> dict[str, Any]:
    if claim in {"SCIENTIFIC_PASS","VALIDATED_STRATEGY","TRADING_READY","PROMOTED"}:
        return _decision("BLOCKED", "REJECT_GLOBAL_SCIENTIFIC_PASS")
    return _decision("READY", "GLOBAL_CLAIM_NOT_ESCALATED")

def validate_target_execution_surface(*, data_family: str, p1_engine: str) -> dict[str, Any]:
    if data_family=="AP0_PARQUET" and p1_engine=="BI5ResearchEngine":
        return _decision(
            "BLOCKED",
            "BLOCKED_P1_TARGET_EXECUTION_SURFACE_UNSUPPORTED",
            data_family=data_family,
            p1_engine=p1_engine,
            owner_gap="P1_LINKED_EXECUTION_CURRENTLY_REQUIRES_BI5",
        )
    return _decision("READY", "TARGET_EXECUTION_SURFACE_COMPATIBLE")

def validate_p1_smf_procedure_binding(*,p1_method_ref:str,procedure_ref:str,smf_bundle,smf_result_binding) -> dict[str, Any]:
    valid=validate_method_bundle(smf_bundle)
    if valid["status"]!="READY":
        return valid
    if p1_method_ref!=smf_bundle.get("p1_method_ref"):
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    if not isinstance(smf_result_binding,Mapping):
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    if procedure_ref!=smf_result_binding.get("procedure_ref"):
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    if smf_result_binding.get("activation_digest")!=_activation_payload(smf_bundle["m03_activation"]).get("activation_digest"):
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    if smf_result_binding.get("qualified_implementation_blob")!=SMF_CORE_BLOB:
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    return _decision("READY", "P1_SMF_PROCEDURE_BINDING_EXACT")

def bind_data02_to_p1_preexecution(*, admission, p1_execution_binding, data_root: str | Path) -> dict[str, Any]:
    """Bind exact Data admission to the exact P1 resource binding, then assess owner capability."""
    data_check = validate_data_admission(admission, expected_digest=str(admission.get("admission_digest","")) if isinstance(admission, Mapping) else "")
    if data_check["status"] != "READY":
        return data_check
    if type(p1_execution_binding) is not p1_binding.ExperimentExecutionBinding:
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    if not p1_binding.is_factory_attested_experiment_execution_binding(p1_execution_binding):
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    root = Path(data_root).resolve(strict=False)
    if Path(p1_execution_binding.corpus_root).resolve(strict=False) != root:
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    try:
        observed_hash = research_input_binding.corpus_inventory_hash(root)
    except Exception:
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    if observed_hash != p1_execution_binding.expected_corpus_hash:
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    compatibility = validate_target_execution_surface(data_family=TARGET_DATA_FAMILY, p1_engine=P1_ENGINE)
    if compatibility["status"] != "READY":
        return _decision(
            "BLOCKED_OWNER_GAP",
            compatibility["reason"],
            identity_binding_status="PASS",
            dataset_identity=DATASET_IDENTITY,
            p1_execution_binding_id=p1_execution_binding.execution_binding_id,
            p1_engine=P1_ENGINE,
            owner_gap=compatibility.get("owner_gap"),
        )
    return _decision(
        "READY",
        "DATA02_P1_PREEXECUTION_BOUND",
        identity_binding_status="PASS",
        p1_execution_binding_id=p1_execution_binding.execution_binding_id,
    )

def validate_surface_generalization(*,qualified_surface:str,target_surface:str) -> dict[str, Any]:
    if qualified_surface!=target_surface:
        return _decision("BLOCKED", "REJECT_SYNTHETIC_SURFACE_GENERALIZATION")
    return _decision("READY", "SURFACE_SCOPE_EXACT")

def execute_m03(smf_bundle: Mapping[str, Any], values: Sequence[float], *, probabilities: Sequence[float]) -> dict[str, Any]:
    valid=validate_method_bundle(smf_bundle)
    if valid["status"]!="READY":
        raise RVO05Error(valid["reason"])
    m03=_activation_payload(smf_bundle["m03_activation"])
    result=smf.ecdf_quantiles(values,probabilities=probabilities)
    source=Path(__file__).resolve().parents[1] / "tools" / "smf03_core_foundation.py"
    procedure_sha256=hashlib.sha256(source.read_bytes()).hexdigest()
    procedure_ref=f"gitblob:{SMF_CORE_BLOB}#ecdf_quantiles"
    body={
        "schema":SMF_RESULT_SCHEMA,
        "method_family":"M03",
        "activation_digest":m03["activation_digest"],
        "qualified_implementation_blob":SMF_CORE_BLOB,
        "procedure_ref":procedure_ref,
        "procedure_sha256":procedure_sha256,
        "owner_result":result,
    }
    return {**body,"result_digest":rvo.canonical_sha256(body)}

def bind_p1_chain(
    *,
    specification,
    execution_binding,
    qualified_input,
    execution_result,
    evaluation_submission,
    measurement_provenance,
    evaluation_authority,
    finding,
    smf_bundle,
    smf_result_binding,
) -> dict[str, Any]:
    checks=(
        (type(specification) is p1_spec.ExperimentSpecification and p1_spec.is_factory_attested_experiment_specification(specification)),
        (type(execution_binding) is p1_binding.ExperimentExecutionBinding and p1_binding.is_factory_attested_experiment_execution_binding(execution_binding)),
        (type(qualified_input) is p1_qei.QualifiedExperimentExecutionInput and p1_qei.is_factory_attested_qualified_experiment_execution_input(qualified_input)),
        (type(execution_result) is p1_exec.LinkedExperimentExecutionResult and p1_exec.is_factory_attested_linked_experiment_execution_result(execution_result)),
        (type(evaluation_submission) is p1_eval.ExperimentEvaluationSubmission and p1_eval.is_factory_attested_experiment_evaluation_submission(evaluation_submission)),
        (type(measurement_provenance) is p1_prov.WitnessedMeasurementProvenance and p1_prov.is_factory_attested_witnessed_measurement_provenance(measurement_provenance)),
        (type(evaluation_authority) is p1_auth.QualifiedExperimentEvaluationAuthority and p1_auth.is_factory_attested_qualified_experiment_evaluation_authority(evaluation_authority)),
        (type(finding) is p1_find.QualifiedExperimentalFinding and p1_find.is_factory_attested_qualified_experimental_finding(finding)),
    )
    if not all(checks):
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    ids=(
        specification.experiment_spec_id,
        execution_binding.experiment_spec_id,
        qualified_input.experiment_spec_id,
        execution_result.experiment_spec_id,
        evaluation_submission.experiment_spec_id,
        measurement_provenance.experiment_spec_id,
        evaluation_authority.experiment_spec_id,
        finding.experiment_spec_id,
    )
    if len(set(ids))!=1:
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    if finding.evaluation_submission_id!=evaluation_submission.evaluation_submission_id:
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    if finding.evaluation_authority_qualification_id!=evaluation_authority.qualification_id:
        return _decision("BLOCKED", "BLOCKED_P1_CHAIN_MISMATCH")
    if evaluation_submission.method_ref!=smf_bundle.get("p1_method_ref") or finding.method_ref!=evaluation_submission.method_ref:
        return _decision("BLOCKED", "BLOCKED_LABEL_ONLY_P1_METHOD_REF")
    if len(measurement_provenance.derivations)!=1:
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    derivation=measurement_provenance.derivations[0]
    procedure=validate_p1_smf_procedure_binding(
        p1_method_ref=evaluation_submission.method_ref,
        procedure_ref=derivation.procedure_ref,
        smf_bundle=smf_bundle,
        smf_result_binding=smf_result_binding,
    )
    if procedure["status"]!="READY" or derivation.procedure_sha256!=smf_result_binding.get("procedure_sha256"):
        return _decision("BLOCKED", "BLOCKED_P1_SMF_PROCEDURE_BINDING")
    return _decision(
        "READY",
        "P1_DOWNSTREAM_CHAIN_BOUND",
        experiment_spec_id=specification.experiment_spec_id,
        execution_result_id=execution_result.experiment_execution_result_id,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        provenance_qualification_id=measurement_provenance.provenance_qualification_id,
        evaluation_authority_id=evaluation_authority.qualification_id,
        finding_id=finding.finding_id,
        p1_native_finding_status=finding.finding_status,
        smf_result_digest=smf_result_binding["result_digest"],
        p1_method_ref=evaluation_submission.method_ref,
    )

def readiness_verdict(*,data02_real_status:str,p1_smf_binding_status:str,target_execution_status:str) -> dict[str,Any]:
    if data02_real_status!="PASS_REAL_DATA_ADMISSION":
        return _decision("BLOCKED", "BLOCKED_REAL_DATA_ADMISSION")
    if p1_smf_binding_status!="QUALIFIED_SYNTHETIC_BI5_ONLY":
        return _decision("BLOCKED", "BLOCKED_P1_SMF_BINDING")
    if target_execution_status!="READY":
        return _decision(
            "BLOCKED_OWNER_GAP",
            "BLOCKED_P1_TARGET_EXECUTION_SURFACE_UNSUPPORTED",
            next_owner="P1/RESEARCH_EXECUTION",
            real_cc02_authorized=False,
        )
    return _decision("READY_FOR_SEPARATE_HUMAN_AUTHORIZATION","FIRST_REAL_CC02_PRE_EXECUTION_READY",real_cc02_authorized=False)


def build_synthetic_rvo_validation_package(
    *,
    repository: str,
    branch: str,
    head: str,
    tree: str,
    data_admission: Mapping[str, Any],
    specification,
    p1_chain_binding: Mapping[str, Any],
    smf_bundle: Mapping[str, Any],
    smf_result_binding: Mapping[str, Any],
    environment_identity: str,
) -> dict[str, Any]:
    """Assemble a synthetic RVO package from exact owner-native evidence.

    PACKAGE_COMPLETE remains procedural only. The package preserves the P1
    finding status and exact SMF activation/result references without
    interpreting either as strategy validation or authority.
    """
    data_check = validate_data_admission(
        data_admission,
        expected_digest=str(data_admission.get("admission_digest", "")),
    )
    if data_check["status"] != "READY":
        raise RVO05Error(data_check["reason"])
    method_check = validate_method_bundle(smf_bundle)
    if method_check["status"] != "READY":
        raise RVO05Error(method_check["reason"])
    if p1_chain_binding.get("status") != "READY":
        raise RVO05Error("P1_CHAIN_NOT_READY")
    if not p1_spec.is_factory_attested_experiment_specification(specification):
        raise RVO05Error("P1_SPEC_NOT_ATTESTED")

    m01 = _activation_payload(smf_bundle["m01_activation"])
    m03 = _activation_payload(smf_bundle["m03_activation"])
    if not isinstance(m01, Mapping) or not isinstance(m03, Mapping):
        raise RVO05Error("SMF_ACTIVATION_BINDING_INCOMPLETE")
    if smf_result_binding.get("result_digest") != p1_chain_binding.get("smf_result_digest"):
        raise RVO05Error("P1_SMF_RESULT_BINDING_MISMATCH")

    controls = [
        {
            "control_id": "P1-SPEC",
            "owner_id": "P1",
            "owner_contract_ref": p1_spec.CONTRACT,
            "failure_mode_refs": ["UNFROZEN_EXPERIMENT_SPECIFICATION"],
            "applicability_rule_ref": "rvo05:cc02:p1-spec-required",
            "input_contract_ref": "P1.8:FollowUpRequest",
            "output_contract_ref": p1_spec.CONTRACT,
            "dependency_control_ids": [],
            "native_status_schema_ref": "P1:FACTORY_ATTESTATION",
            "blocking_rule_ref": "rvo05:p1-spec-attestation",
            "reconstructibility_contract_ref": "rvo05:p1-spec-content-identity",
            "validity_scope": "RVO05_CC02_SYNTHETIC_BI5",
        },
        {
            "control_id": "DATA-02",
            "owner_id": "DATA",
            "owner_contract_ref": data02.CONTRACT,
            "failure_mode_refs": ["DATA_IDENTITY_OR_ADMISSIBILITY"],
            "applicability_rule_ref": "rvo05:cc02:data-required",
            "input_contract_ref": "DATA02:AP0_CLAIM_SCOPED_INPUT",
            "output_contract_ref": data02.CONTRACT,
            "dependency_control_ids": ["P1-SPEC"],
            "native_status_schema_ref": "DATA02:ADMISSION_STATUS",
            "blocking_rule_ref": "rvo05:data02-native-status",
            "reconstructibility_contract_ref": "rvo05:data02-admission-digest",
            "validity_scope": "RVO05_CC02_SYNTHETIC_BI5",
        },
        {
            "control_id": "SMF-M01",
            "owner_id": "SMF",
            "owner_contract_ref": smf.CONTRACT,
            "failure_mode_refs": ["ESTIMAND_DRIFT"],
            "applicability_rule_ref": "rvo05:cc02:m01-required",
            "input_contract_ref": "SMF02:ACTIVATION_INPUT",
            "output_contract_ref": smf.CONTRACT,
            "dependency_control_ids": ["P1-SPEC"],
            "native_status_schema_ref": "SMF:ACTIVATION_STATE",
            "blocking_rule_ref": "rvo05:smf-m01-native",
            "reconstructibility_contract_ref": "rvo05:smf-activation-digest",
            "validity_scope": "RVO05_CC02_SYNTHETIC_BI5",
        },
        {
            "control_id": "SMF-M03",
            "owner_id": "SMF",
            "owner_contract_ref": smf.CONTRACT,
            "failure_mode_refs": ["EMPIRICAL_DISTRIBUTION_QUANTILE_SUMMARY"],
            "applicability_rule_ref": "rvo05:cc02:m03-required",
            "input_contract_ref": "SMF02:ACTIVATION_INPUT",
            "output_contract_ref": smf.CONTRACT,
            "dependency_control_ids": ["DATA-02", "P1-SPEC", "SMF-M01"],
            "native_status_schema_ref": "SMF:ACTIVATION_STATE",
            "blocking_rule_ref": "rvo05:smf-m03-native",
            "reconstructibility_contract_ref": "rvo05:smf-activation-and-result-digest",
            "validity_scope": "RVO05_CC02_SYNTHETIC_BI5",
        },
        {
            "control_id": "P1-DOWNSTREAM",
            "owner_id": "P1",
            "owner_contract_ref": p1_find.CONTRACT,
            "failure_mode_refs": ["UNQUALIFIED_EXPERIMENT_FINDING_CHAIN"],
            "applicability_rule_ref": "rvo05:cc02:p1-downstream-required",
            "input_contract_ref": p1_exec.CONTRACT,
            "output_contract_ref": p1_find.CONTRACT,
            "dependency_control_ids": ["DATA-02", "P1-SPEC", "SMF-M03"],
            "native_status_schema_ref": "P1:FINDING_STATUS",
            "blocking_rule_ref": "rvo05:p1-native-finding",
            "reconstructibility_contract_ref": "rvo05:p1-chain-identities",
            "validity_scope": "RVO05_CC02_SYNTHETIC_BI5",
        },
    ]
    catalog = rvo.build_control_catalog(
        controls,
        catalog_version="RVO05_CC02_SYNTHETIC_OWNER_CHAIN_V0_1",
    )
    pre = rvo.build_pre_snapshot(
        repository=repository,
        branch=branch,
        head=head,
        tree=tree,
        dataset_refs=[
            str(data_admission["admission_digest"]),
            str(data_admission["binding_basis"]["dataset_identity"]),
        ],
        temporal_ref="NOT_APPLICABLE_WITH_EXPLICIT_BASIS:RETROSPECTIVE_DESCRIPTIVE_ONLY",
        execution_ref="P1_EXECUTION:SYNTHETIC_BI5_ONLY",
        smf_activation_refs=[
            str(m01["activation_digest"]),
            str(m03["activation_digest"]),
        ],
        mcepr_pre_ref="NOT_APPLICABLE_WITH_BASIS:NO_MATERIAL_SEARCH_EXPOSURE",
        oos_pre_state="NOT_CONSUMED_SYNTHETIC",
        environment_identity=environment_identity,
        owner_contract_refs={
            "RVO": rvo.CONTRACT,
            "DATA": data02.CONTRACT,
            "P1_SPEC": p1_spec.CONTRACT,
            "P1_EXECUTION": p1_exec.CONTRACT,
            "P1_FINDING": p1_find.CONTRACT,
            "SMF": smf.CONTRACT,
        },
    )

    method_bindings = {
        "SMF-M01": {
            "p1_method_ref": smf_bundle["p1_method_ref"],
            "activation_digest": m01["activation_digest"],
            "qualified_method_ref": "gitblob:" + SMF_CORE_BLOB,
            "claim_ref": m01["claim_definition_ref"],
            "failure_mode_ref": m01["failure_mode_ref"],
            "assumption_set_ref": m01["assumption_set_ref"],
            "parameter_policy_ref": rvo.canonical_sha256(m01["parameter_selection_policy"]),
            "dependency_refs": list(m01["dependency_refs"]),
        },
        "SMF-M03": {
            "p1_method_ref": smf_bundle["p1_method_ref"],
            "activation_digest": m03["activation_digest"],
            "qualified_method_ref": "gitblob:" + SMF_CORE_BLOB,
            "claim_ref": m03["claim_definition_ref"],
            "failure_mode_ref": m03["failure_mode_ref"],
            "assumption_set_ref": m03["assumption_set_ref"],
            "parameter_policy_ref": rvo.canonical_sha256(m03["parameter_selection_policy"]),
            "dependency_refs": list(m03["dependency_refs"]),
        },
    }
    applicability = [
        {"control_id":"P1-SPEC","applicability_state":"APPLICABLE","applicability_basis":"Exact empirical experiment specification is required.","material":True},
        {"control_id":"DATA-02","applicability_state":"APPLICABLE","applicability_basis":"Exact claim-scoped data admission is required before empirical execution.","material":True},
        {"control_id":"SMF-M01","applicability_state":"APPLICABLE","applicability_basis":"Claim and estimand must be frozen before result exposure.","material":True},
        {"control_id":"SMF-M03","applicability_state":"APPLICABLE","applicability_basis":"Declared empirical percentile summaries require M03.","material":True},
        {"control_id":"P1-DOWNSTREAM","applicability_state":"APPLICABLE","applicability_basis":"Empirical claim requires the qualified P1 downstream finding chain.","material":True},
    ]
    manifest = rvo.build_pre_result_manifest(
        catalog=catalog,
        experiment_spec_id=specification.experiment_spec_id,
        claim_ref=m01["claim_definition_ref"],
        estimand_ref="estimand:rvo05:synthetic-spread-empirical-quantiles",
        validity_scope_ref=m01["validity_scope_ref"],
        pre_snapshot=pre,
        applicability_records=applicability,
        method_bindings=method_bindings,
        result_exposed=False,
    )

    snapshot = pre["pre_snapshot_digest"]
    owner_results = [
        rvo.bind_owner_result(
            control_id="P1-SPEC", owner_id="P1",
            native_status_schema_ref="P1:FACTORY_ATTESTATION",
            native_status="ATTESTED", asserted_native_status="ATTESTED",
            orchestration_state="READY", blocking_rule_ref=None, snapshot_digest=snapshot,
        ),
        rvo.bind_owner_result(
            control_id="DATA-02", owner_id="DATA",
            native_status_schema_ref="DATA02:ADMISSION_STATUS",
            native_status=str(data_admission["status"]), asserted_native_status=str(data_admission["status"]),
            orchestration_state="READY", blocking_rule_ref=None, snapshot_digest=snapshot,
        ),
        rvo.bind_owner_result(
            control_id="SMF-M01", owner_id="SMF",
            native_status_schema_ref="SMF:ACTIVATION_STATE",
            native_status=str(m01["activation_state"]), asserted_native_status=str(m01["activation_state"]),
            orchestration_state="READY", blocking_rule_ref=None, snapshot_digest=snapshot,
        ),
        rvo.bind_owner_result(
            control_id="SMF-M03", owner_id="SMF",
            native_status_schema_ref="SMF:ACTIVATION_STATE",
            native_status=str(m03["activation_state"]), asserted_native_status=str(m03["activation_state"]),
            orchestration_state="READY", blocking_rule_ref=None, snapshot_digest=snapshot,
        ),
        rvo.bind_owner_result(
            control_id="P1-DOWNSTREAM", owner_id="P1",
            native_status_schema_ref="P1:FINDING_STATUS",
            native_status=str(p1_chain_binding["p1_native_finding_status"]),
            asserted_native_status=str(p1_chain_binding["p1_native_finding_status"]),
            orchestration_state="READY", blocking_rule_ref=None, snapshot_digest=snapshot,
        ),
    ]
    post = rvo.build_post_snapshot(
        pre_manifest_digest=manifest["manifest_digest"],
        actual_input_refs=[
            str(data_admission["admission_digest"]),
            str(p1_chain_binding["execution_result_id"]),
        ],
        owner_output_refs=[
            str(m01["activation_digest"]),
            str(m03["activation_digest"]),
            str(smf_result_binding["result_digest"]),
            str(p1_chain_binding["finding_id"]),
        ],
        p1_finding_refs=[str(p1_chain_binding["finding_id"])],
        pcp_post_ref="SYNTHETIC_PCP_POST:UNCHANGED",
        mcepr_post_ref="NOT_APPLICABLE_WITH_BASIS:NO_MATERIAL_SEARCH_EXPOSURE",
        oos_post_state="NOT_CONSUMED_SYNTHETIC",
        environment_identity=environment_identity,
        material_dependency_refs=[
            "gitblob:" + SMF_CORE_BLOB,
            "gitblob:" + P1_LINKED_EXECUTION_BLOB,
            "gitblob:6ce06e1583e61be9e8618136d1bc8fdda608ffd7",
        ],
    )
    reconstruction = rvo.validate_reconstruction_descriptor(
        reconstruction_class="EVIDENCE_REPLAY",
        material_inputs={
            "data_admission_digest": data_admission["admission_digest"],
            "experiment_spec_id": specification.experiment_spec_id,
            "execution_result_id": p1_chain_binding["execution_result_id"],
            "smf_result_digest": smf_result_binding["result_digest"],
            "finding_id": p1_chain_binding["finding_id"],
        },
        environment_identity=environment_identity,
        dependency_refs=[
            "gitblob:" + SMF_CORE_BLOB,
            "gitblob:" + P1_LINKED_EXECUTION_BLOB,
            "gitblob:6ce06e1583e61be9e8618136d1bc8fdda608ffd7",
        ],
        schema_refs=[data02.CONTRACT, p1_find.CONTRACT, SMF_RESULT_SCHEMA],
        parameters={"probabilities":[0.5,0.9,0.95,0.99],"quantile_method":"linear"},
        seeds={},
        owner_contract_refs={
            "DATA":data02.CONTRACT,
            "P1":p1_find.CONTRACT,
            "SMF":smf.CONTRACT,
            "RVO":rvo.CONTRACT,
        },
        routing_order=manifest["routing_plan"],
        pre_manifest_digest=manifest["manifest_digest"],
        runtime_attestation=p1_chain_binding["finding_id"],
    )
    package = rvo.build_validation_package(
        manifest=manifest,
        pre_snapshot=pre,
        post_snapshot=post,
        owner_results=owner_results,
        reconstruction_descriptor=reconstruction,
    )
    return {
        "catalog":catalog,
        "pre_snapshot":pre,
        "manifest":manifest,
        "post_snapshot":post,
        "reconstruction":reconstruction,
        "owner_results":owner_results,
        "package":package,
    }

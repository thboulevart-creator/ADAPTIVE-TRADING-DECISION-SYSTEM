"""Synthetic owner fixtures for RVO-05 qualification only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src import rvo_05_cc02_bindings as rvo05
from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_evaluation_submission import ExperimentMeasurementClaim, submit_experiment_evaluation
from src.experiment_evaluator_authority import reattest_experiment_evaluator_authority
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_measurement_provenance import reattest_measurement_provenance
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.linked_experiment_execution import run_linked_experiment
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.qualified_experimental_finding import interpret_qualified_experimental_finding
from src.research.bi5_reader import iter_ticks
from src.research.input_binding import bind_execution_input, corpus_inventory_hash, sha256_file
from src.revision import produce_revision_decision
from src.data import claim_scoped_admission as data02
from tests.data_02_fixture import make_package as make_data02_package
from tests.research_runtime_fixture import synthetic_runtime_case

P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
MEMORY_AUTHORITY = "RVO_05_SYNTHETIC_P1_CAPTURE_AUTHORITY_V1"
DERIVATION_AUTHORITY = "measurement-authority:rvo05"
EVALUATION_AUTHORITY = "evaluation-authority:rvo05"
DERIVATION_NONCE = "ab" * 32
EVALUATION_NONCE = "cd" * 32

def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"

def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def make_p1_spec(tmp_path: Path, *, tag: str = "CC02"):
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome=f"RVO05_{tag}_SYNTHETIC")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)

    authority_id = f"{MEMORY_AUTHORITY}:{tag}"
    capture = persist_witnessed_memory_episode(tmp_path / "memory", episode, authority_id=authority_id)
    historical = reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=authority_id,
        expected_receipt_sha256=capture.receipt_sha256,
    )
    scope = create_audit_scope(
        question=f"What exact RVO-05 synthetic descriptive experiment is required for {tag}?",
        expected_registration_ids=(historical.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (historical,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Specify a synthetic retrospective descriptive quantile experiment for RVO-05.",
    )
    request = produce_follow_up_request(revision)
    return specify_experiment(
        request,
        hypothesis_statement="The synthetic BI5 fixture has a predeclared empirical spread distribution.",
        prediction="The M03 empirical median spread equals the value computed from the exact synthetic stream.",
        falsification_rule="A mismatched M03 procedure/result or nonmatching P1 chain falsifies this synthetic integration.",
        protocol="Synthetic owner interfaces only; no real AP1, performance, OOS, trading or capital.",
        measurement_plan="Decode the exact synthetic BI5 stream, compute spread values, activate M01/M03 before result, and bind M03 empirical quantiles into P1 provenance.",
    )

def _p114_id(execution_result, submission, record_sha256: str) -> str:
    payload = {
        "contract_id": "P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1",
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha256,
    }
    return "WMP-" + _sha256(_canonical(payload))[:32]

def _p114_files(tmp_path: Path, execution_result, submission, smf_result):
    claim = submission.measurements[0]
    record = {
        "schema": "P1_14B_MEASUREMENT_DERIVATION_RECORD_V1",
        "contract_id": "P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1",
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "experiment_spec_id": execution_result.experiment_spec_id,
        "stream_sha256": execution_result.stream_sha256,
        "method_ref": submission.method_ref,
        "derivations": [{
            "measurement_id": claim.measurement_id,
            "metric": claim.metric,
            "observed_value": claim.observed_value,
            "unit": claim.unit,
            "sample_size": claim.sample_size,
            "scope": claim.scope,
            "rationale": claim.rationale,
            "procedure_ref": smf_result["procedure_ref"],
            "procedure_sha256": smf_result["procedure_sha256"],
            "input_stream_sha256": execution_result.stream_sha256,
        }],
    }
    record_bytes = _canonical(record)
    record_sha = _sha256(record_bytes)
    receipt = {
        "schema": "P1_14B_MEASUREMENT_DERIVATION_RECEIPT_V1",
        "contract_id": "P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1",
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha,
        "provenance_qualification_id": _p114_id(execution_result, submission, record_sha),
    }
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "measurement.record.json"
    receipt_path = tmp_path / "measurement.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)

def _p115_id(submission, provenance, record_sha256: str) -> str:
    payload = {
        "contract_id": "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1",
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
    }
    return "QEA-" + _sha256(_canonical(payload))[:32]

def _p115_files(tmp_path: Path, submission, provenance):
    procedure_bindings = [
        {
            "measurement_id": item.measurement_id,
            "procedure_ref": item.procedure_ref,
            "procedure_sha256": item.procedure_sha256,
        }
        for item in provenance.derivations
    ]
    record = {
        "schema": "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECORD_V1",
        "contract_id": "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1",
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "experiment_execution_result_id": submission.experiment_execution_result_id,
        "experiment_spec_id": submission.experiment_spec_id,
        "request_id": submission.request_id,
        "evaluator_id": submission.evaluator_id,
        "method_ref": submission.method_ref,
        "prediction_status": submission.prediction_status,
        "falsification_status": submission.falsification_status,
        "evaluation_rationale": submission.evaluation_rationale,
        "measurement_ids": [item.measurement_id for item in submission.measurements],
        "procedure_bindings": procedure_bindings,
    }
    record_bytes = _canonical(record)
    record_sha = _sha256(record_bytes)
    receipt = {
        "schema": "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECEIPT_V1",
        "contract_id": "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1",
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha,
        "qualification_id": _p115_id(submission, provenance, record_sha),
    }
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "authority.record.json"
    receipt_path = tmp_path / "authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)

def build_positive_p1_smf_chain(tmp_path: Path):
    specification = make_p1_spec(tmp_path / "spec")
    activations = rvo05.activate_required_smf(
        result_exposed=False,
        claim_ref="claim:rvo05:cc02:synthetic-bi5",
        validity_scope_ref="scope:rvo05:cc02:synthetic-bi5",
    )
    bundle = rvo05.build_method_bundle(activations)

    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.corpus_root,
            case.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        execution_binding = bind_experiment_execution(specification, bound)
        qualified_input = qualify_experiment_execution_input(execution_binding)
        execution_result = run_linked_experiment(qualified_input)

        contract = json.loads(case.contract_path.read_text(encoding="utf-8"))
        spreads = []
        for path in sorted(case.corpus_root.glob("*.bi5")):
            spreads.extend(float(tick.ask - tick.bid) for tick in iter_ticks(path, contract))

        smf_result = rvo05.execute_m03(bundle, spreads, probabilities=(0.5, 0.9, 0.95, 0.99))
        p50 = smf_result["owner_result"]["quantiles"]["0.5"]
        measurement = ExperimentMeasurementClaim(
            measurement_id="RVO05-M03-P50",
            metric="synthetic_tick_spread_p50",
            observed_value=repr(p50),
            unit="price",
            sample_size=len(spreads),
            scope="synthetic-bi5-only",
            rationale="Exact M03 result over spreads decoded from the same synthetic P1 execution corpus.",
        )
        submission = submit_experiment_evaluation(
            execution_result,
            evaluator_id="evaluator:rvo05:synthetic",
            method_ref=bundle["p1_method_ref"],
            measurements=(measurement,),
            prediction_status="SUPPORTED",
            falsification_status="NOT_FALSIFIED",
            evaluation_rationale="Synthetic P1↔SMF binding qualification only.",
        )

        p114_record, p114_receipt, p114_pin = _p114_files(
            tmp_path / "p114", execution_result, submission, smf_result
        )
        provenance = reattest_measurement_provenance(
            execution_result,
            submission,
            p114_record,
            p114_receipt,
            expected_authority_id=DERIVATION_AUTHORITY,
            expected_receipt_sha256=p114_pin,
        )
        p115_record, p115_receipt, p115_pin = _p115_files(
            tmp_path / "p115", submission, provenance
        )
        authority = reattest_experiment_evaluator_authority(
            submission,
            provenance,
            p115_record,
            p115_receipt,
            expected_authority_id=EVALUATION_AUTHORITY,
            expected_receipt_sha256=p115_pin,
        )
        finding = interpret_qualified_experimental_finding(submission, authority)

        bound_chain = rvo05.bind_p1_chain(
            specification=specification,
            execution_binding=execution_binding,
            qualified_input=qualified_input,
            execution_result=execution_result,
            evaluation_submission=submission,
            measurement_provenance=provenance,
            evaluation_authority=authority,
            finding=finding,
            smf_bundle=bundle,
            smf_result_binding=smf_result,
        )
        return {
            "specification": specification,
            "execution_binding": execution_binding,
            "qualified_input": qualified_input,
            "execution_result": execution_result,
            "submission": submission,
            "provenance": provenance,
            "authority": authority,
            "finding": finding,
            "activations": activations,
            "bundle": bundle,
            "smf_result": smf_result,
            "bound_chain": bound_chain,
            "spreads": tuple(spreads),
        }

def build_target_ap0_preexecution_probe(tmp_path: Path):
    package = make_data02_package(tmp_path / "data02")
    admission = data02.evaluate_synthetic(package)
    specification = make_p1_spec(tmp_path / "target-spec", tag="TARGET")
    contract_path = tmp_path / "target-ap0-resource-contract.json"
    contract_path.write_text(json.dumps({"format":"AP0_PARQUET"}, sort_keys=True, separators=(",",":")), encoding="utf-8")
    corpus_root = Path(package["root"])
    bound = bind_execution_input(
        corpus_root,
        contract_path,
        corpus_inventory_hash(corpus_root),
        sha256_file(contract_path),
    )
    execution_binding = bind_experiment_execution(specification, bound)
    qualified_input = qualify_experiment_execution_input(execution_binding)
    compatibility = rvo05.bind_data02_to_p1_preexecution(
        admission=admission,
        p1_execution_binding=execution_binding,
        data_root=corpus_root,
    )
    return {
        "package": package,
        "admission": admission,
        "specification": specification,
        "execution_binding": execution_binding,
        "qualified_input": qualified_input,
        "compatibility": compatibility,
    }

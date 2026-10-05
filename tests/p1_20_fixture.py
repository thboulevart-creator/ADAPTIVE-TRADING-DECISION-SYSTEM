"""Synthetic dual-owner fixtures for P1-20 common downstream qualification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.experiment_execution_binding import bind_experiment_execution
from src.linked_experiment_execution import run_linked_experiment
from src.p1_12c_qualified_producer_execution import run_qualified_producer
from src.p1_12d_qualified_execution_evidence import normalize_qualified_execution
from src.p1_13c_common_evaluation import (
    CommonExperimentMeasurementClaim,
    submit_common_experiment_evaluation,
)
from src.p1_14c_common_measurement_provenance import (
    CONTRACT as P114C_CONTRACT,
    RECORD_SCHEMA as P114C_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P114C_RECEIPT_SCHEMA,
    reattest_common_measurement_provenance,
)
from src.p1_15c_common_evaluator_authority import (
    CONTRACT as P115C_CONTRACT,
    RECORD_SCHEMA as P115C_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P115C_RECEIPT_SCHEMA,
    reattest_common_evaluator_authority,
)
from src.p1_16c_common_qualified_finding import interpret_common_qualified_finding
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.research.input_binding import bind_execution_input
from tests.p1_18_fixture import build_case as build_p112c_case
from tests.research_runtime_fixture import synthetic_runtime_case
from tests.rvo_05_fixture import make_p1_spec

DERIVATION_AUTHORITY = "p1-20:common-measurement-authority"
EVALUATION_AUTHORITY = "p1-20:common-evaluator-authority"
DERIVATION_NONCE = "ab" * 32
EVALUATION_NONCE = "cd" * 32


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build_p112b_native(tmp_path: Path):
    specification = make_p1_spec(tmp_path / "spec", tag="P120B")
    with synthetic_runtime_case() as case:
        bound = bind_execution_input(
            case.corpus_root,
            case.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        execution_binding = bind_experiment_execution(specification, bound)
        qualified_input = qualify_experiment_execution_input(execution_binding)
        native_result = run_linked_experiment(qualified_input)
        envelope = normalize_qualified_execution(native_result, qualified_input)
    return {
        "specification": specification,
        "execution_binding": execution_binding,
        "qualified_input": qualified_input,
        "native_result": native_result,
        "envelope": envelope,
    }


def build_p112c_native(tmp_path: Path):
    case = build_p112c_case(tmp_path / "p112c")
    native_result = run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    envelope = normalize_qualified_execution(native_result, case["qualified_input"])
    return {
        **case,
        "native_result": native_result,
        "envelope": envelope,
    }


def _p114c_id(envelope, evaluation, record_sha256: str) -> str:
    payload = {
        "contract_id": P114C_CONTRACT,
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "execution_evidence_envelope_id": envelope.execution_evidence_envelope_id,
        "native_result_id": envelope.native_result_id,
        "measurement_input_identity": envelope.measurement_input_identity,
        "record_sha256": record_sha256,
    }
    return "CWMP-" + _sha256(_canonical(payload))[:32]


def _p114c_files(tmp_path: Path, envelope, evaluation):
    claim = evaluation.measurements[0]
    procedure_ref = "procedure:p1-20:identity-observation:v1"
    procedure_sha256 = _sha256(procedure_ref.encode("utf-8"))
    record = {
        "schema": P114C_RECORD_SCHEMA,
        "contract_id": P114C_CONTRACT,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "execution_evidence_envelope_id": envelope.execution_evidence_envelope_id,
        "native_result_id": envelope.native_result_id,
        "experiment_spec_id": envelope.experiment_spec_id,
        "measurement_input_identity": envelope.measurement_input_identity,
        "method_ref": evaluation.method_ref,
        "derivations": [{
            "measurement_id": claim.measurement_id,
            "metric": claim.metric,
            "observed_value": claim.observed_value,
            "unit": claim.unit,
            "sample_size": claim.sample_size,
            "scope": claim.scope,
            "rationale": claim.rationale,
            "execution_evidence_envelope_id": envelope.execution_evidence_envelope_id,
            "native_result_id": envelope.native_result_id,
            "measurement_input_identity": envelope.measurement_input_identity,
            "procedure_ref": procedure_ref,
            "procedure_sha256": procedure_sha256,
        }],
    }
    record_bytes = _canonical(record)
    record_sha = _sha256(record_bytes)
    receipt = {
        "schema": P114C_RECEIPT_SCHEMA,
        "contract_id": P114C_CONTRACT,
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "execution_evidence_envelope_id": envelope.execution_evidence_envelope_id,
        "native_result_id": envelope.native_result_id,
        "measurement_input_identity": envelope.measurement_input_identity,
        "record_sha256": record_sha,
        "provenance_qualification_id": _p114c_id(envelope, evaluation, record_sha),
    }
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "common-measurement.record.json"
    receipt_path = tmp_path / "common-measurement.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes), record, receipt


def _p115c_id(evaluation, provenance, record_sha256: str) -> str:
    payload = {
        "contract_id": P115C_CONTRACT,
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
    }
    return "CQEA-" + _sha256(_canonical(payload))[:32]


def _p115c_files(tmp_path: Path, evaluation, provenance):
    procedure_bindings = [
        {
            "measurement_id": item.measurement_id,
            "procedure_ref": item.procedure_ref,
            "procedure_sha256": item.procedure_sha256,
        }
        for item in provenance.derivations
    ]
    record = {
        "schema": P115C_RECORD_SCHEMA,
        "contract_id": P115C_CONTRACT,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "execution_evidence_envelope_id": evaluation.execution_evidence_envelope_id,
        "native_result_id": evaluation.native_result_id,
        "experiment_spec_id": evaluation.experiment_spec_id,
        "request_id": evaluation.request_id,
        "evaluator_id": evaluation.evaluator_id,
        "method_ref": evaluation.method_ref,
        "prediction_status": evaluation.prediction_status,
        "falsification_status": evaluation.falsification_status,
        "evaluation_rationale": evaluation.evaluation_rationale,
        "measurement_ids": [item.measurement_id for item in evaluation.measurements],
        "procedure_bindings": procedure_bindings,
    }
    record_bytes = _canonical(record)
    record_sha = _sha256(record_bytes)
    receipt = {
        "schema": P115C_RECEIPT_SCHEMA,
        "contract_id": P115C_CONTRACT,
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": evaluation.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha,
        "qualification_id": _p115c_id(evaluation, provenance, record_sha),
    }
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "common-authority.record.json"
    receipt_path = tmp_path / "common-authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes), record, receipt


def build_common_chain(tmp_path: Path, *, owner: str):
    if owner == "P1.12B":
        native = build_p112b_native(tmp_path / "native-b")
    elif owner == "P1.12C":
        native = build_p112c_native(tmp_path / "native-c")
    else:
        raise ValueError("unknown synthetic owner")

    envelope = native["envelope"]
    qualified_input = native["qualified_input"]
    measurement = CommonExperimentMeasurementClaim(
        measurement_id=f"P120-{owner}-M1",
        metric="synthetic_measurement_input_identity_length",
        observed_value=str(len(envelope.measurement_input_identity)),
        unit="hex_chars",
        sample_size=1,
        scope=f"synthetic-common-downstream:{owner}",
        rationale="Synthetic lineage-only qualification; no market-behavior conclusion.",
    )
    evaluation = submit_common_experiment_evaluation(
        envelope,
        qualified_input,
        evaluator_id=f"evaluator:p1-20:{owner}",
        method_ref=f"method:p1-20:{owner}",
        measurements=(measurement,),
        prediction_status="SUPPORTED",
        falsification_status="NOT_FALSIFIED",
        evaluation_rationale="Synthetic common-downstream integration qualification only.",
    )

    p114_record, p114_receipt, p114_pin, _, _ = _p114c_files(
        tmp_path / "p114c", envelope, evaluation
    )
    provenance = reattest_common_measurement_provenance(
        envelope,
        evaluation,
        p114_record,
        p114_receipt,
        expected_authority_id=DERIVATION_AUTHORITY,
        expected_receipt_sha256=p114_pin,
    )

    p115_record, p115_receipt, p115_pin, _, _ = _p115c_files(
        tmp_path / "p115c", evaluation, provenance
    )
    authority = reattest_common_evaluator_authority(
        evaluation,
        provenance,
        p115_record,
        p115_receipt,
        expected_authority_id=EVALUATION_AUTHORITY,
        expected_receipt_sha256=p115_pin,
    )
    finding = interpret_common_qualified_finding(evaluation, authority)
    return {
        **native,
        "evaluation": evaluation,
        "provenance": provenance,
        "authority": authority,
        "finding": finding,
    }

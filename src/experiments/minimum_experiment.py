"""Minimum executable trading experiment boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.data.dataset_admissibility import DatasetIdentity, assess
from src.data.tick_reader import load
from src.experiments.execution import DeterministicExecutor, ExecutionTrace
from src.experiments.failure_boundary import FailureRecord
from src.experiments.results import ExperimentResult
from src.experiments.run_record import ExperimentRunRecord, RunStatus
from src.experiments.temporal_admissibility import TemporalAdmissibilityReport, TemporalContext, assess as assess_temporal
from src.experiments.validation import ValidationCheck, ValidationReport


@dataclass(frozen=True)
class MinimumExperimentOutput:
    run_record: ExperimentRunRecord
    temporal: TemporalAdmissibilityReport
    execution: ExecutionTrace | None
    result: ExperimentResult | None
    validation: ValidationReport
    failure: FailureRecord | None


def run(
    path: str | Path,
    *,
    identity: DatasetIdentity,
    run_id: str,
    experiment_id: str,
    code_version: str,
    configuration_version: str,
    environment_version: str,
    temporal_context: TemporalContext,
    decision_at: datetime,
    started_at: datetime,
    ended_at: datetime,
) -> MinimumExperimentOutput:
    """Execute the frozen minimum boundary without repair or silent fallback."""

    temporal = assess_temporal(temporal_context, decision_at=decision_at)
    admissibility = assess(path, identity=identity)

    if temporal.verdict == "BLOCKED" or admissibility.verdict == "BLOCKED":
        status: RunStatus = "BLOCKED"
        validation_status = "BLOCKED"
        validation_reason = "mandatory experiment input evidence is unavailable"
    elif temporal.verdict == "FAIL" or admissibility.verdict == "FAIL":
        status = "INVALIDATED"
        validation_status = "FAIL"
        validation_reason = "mandatory experiment admissibility check failed"
    else:
        status = "COMPLETED"
        validation_status = "PASS"
        validation_reason = "dataset and temporal admissibility passed"

    execution: ExecutionTrace | None = None
    result: ExperimentResult | None = None
    failure: FailureRecord | None = None

    if status == "COMPLETED":
        try:
            execution = DeterministicExecutor().run(load(path))
            result = ExperimentResult(
                run_id=run_id,
                tick_count=execution.tick_count,
                first_timestamp=execution.first_timestamp,
                last_timestamp=execution.last_timestamp,
                bid_sum=execution.bid_sum,
                ask_sum=execution.ask_sum,
            )
        except Exception as exc:
            status = "FAILED"
            validation_status = "FAIL"
            validation_reason = "execution failed; no silent retry or repair was attempted"
            failure = FailureRecord(
                failure_id=f"{run_id}:failure",
                detected_at=ended_at,
                detected_by="minimum-experiment-boundary",
                subject_id=run_id,
                component="tick-execution",
                failure_class="EXECUTION_ERROR",
                severity="HIGH",
                observed_condition=f"{type(exc).__name__}: {exc}",
                expected_condition="deterministic execution completes without exception",
                evidence_refs=(),
                diagnosis_status="IDENTIFIED",
                diagnosis_explanation=f"execution raised {type(exc).__name__}",
                containment_status="SAFE_HOLD",
                containment_reason="execution failure stops the experiment",
                resolution_action="NONE",
                resolution_actor="governance",
                revalidation_required=True,
                revalidation_report_id=None,
                closure_status="OPEN",
            )
    else:
        observed = validation_reason
        failure = FailureRecord(
            failure_id=f"{run_id}:failure",
            detected_at=ended_at,
            detected_by="minimum-experiment-boundary",
            subject_id=run_id,
            component="dataset-or-temporal-admissibility",
            failure_class="INPUT_ADMISSIBILITY",
            severity="HIGH",
            observed_condition=observed,
            expected_condition="all mandatory admissibility predicates pass",
            evidence_refs=(),
            diagnosis_status="IDENTIFIED" if status == "INVALIDATED" else "UNKNOWN",
            diagnosis_explanation=observed,
            containment_status="SAFE_HOLD",
            containment_reason="experiment execution is not permitted",
            resolution_action="NONE",
            resolution_actor="governance",
            revalidation_required=True,
            revalidation_report_id=None,
            closure_status="BLOCKED" if status == "BLOCKED" else "OPEN",
        )

    record = ExperimentRunRecord(
        run_id=run_id,
        experiment_id=experiment_id,
        code_version=code_version,
        configuration_version=configuration_version,
        dataset_id=identity.dataset_id,
        dataset_version=identity.dataset_version,
        dataset_hash=identity.content_hash,
        environment_version=environment_version,
        started_at=started_at,
        ended_at=ended_at,
        status=status,
    )
    validation = ValidationReport(
        report_id=f"{run_id}:validation",
        subject_id=run_id,
        subject_type="experiment",
        validator_id="minimum-experiment-validator",
        validator_version="v1",
        context_id=experiment_id,
        contract_reference="minimum-executable-trading-boundary",
        contract_version="v1",
        checks=(
            ValidationCheck("dataset_admissibility", admissibility.verdict, "dataset admissibility result"),
            ValidationCheck("temporal_admissibility", temporal.verdict, "point-in-time admissibility result"),
        ),
        evidence_refs=(identity.content_hash,),
        failure_refs=(failure.failure_id,) if failure else (),
        limitations=(),
        verdict_status=validation_status,
        verdict_reason=validation_reason,
        input_identity=identity.content_hash,
        code_version=code_version,
        configuration_version=configuration_version,
        created_at=ended_at,
    )
    return MinimumExperimentOutput(record, temporal, execution, result, validation, failure)

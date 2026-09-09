"""Minimum executable trading experiment boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.data.dataset_admissibility import DatasetIdentity, assess
from src.data.tick_reader import load
from src.experiments.execution import DeterministicExecutor, ExecutionTrace
from src.experiments.results import ExperimentResult
from src.experiments.run_record import ExperimentRunRecord, RunStatus
from src.experiments.temporal_admissibility import TemporalAdmissibilityReport, TemporalContext, assess as assess_temporal


@dataclass(frozen=True)
class MinimumExperimentOutput:
    run_record: ExperimentRunRecord
    temporal: TemporalAdmissibilityReport
    execution: ExecutionTrace | None
    result: ExperimentResult | None


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
    elif temporal.verdict == "FAIL" or admissibility.verdict == "FAIL":
        status = "INVALIDATED"
    else:
        status = "COMPLETED"

    execution: ExecutionTrace | None = None
    result: ExperimentResult | None = None
    if status == "COMPLETED":
        execution = DeterministicExecutor().run(load(path))
        result = ExperimentResult(
            run_id=run_id,
            tick_count=execution.tick_count,
            first_timestamp=execution.first_timestamp,
            last_timestamp=execution.last_timestamp,
            bid_sum=execution.bid_sum,
            ask_sum=execution.ask_sum,
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
    return MinimumExperimentOutput(record, temporal, execution, result)

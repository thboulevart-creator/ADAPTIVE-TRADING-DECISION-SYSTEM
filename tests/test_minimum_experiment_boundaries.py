from datetime import datetime, timezone
from decimal import Decimal

import pytest

from src.data.tick_reader import Tick
from src.experiments.execution import DeterministicExecutor
from src.experiments.failure_boundary import FailureRecord
from src.experiments.results import ExperimentResult
from src.experiments.temporal_admissibility import TemporalContext, assess
from src.experiments.validation import ValidationCheck, ValidationReport


T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _context(**overrides):
    values = dict(
        valid_from=T0,
        valid_to=None,
        known_from=T0,
        known_to=None,
        usable_from=T0,
        usable_to=None,
        pipeline_safe_from=T0,
        pipeline_safe_to=None,
    )
    values.update(overrides)
    return TemporalContext(**values)


def test_temporal_admissibility_passes_only_when_all_predicates_pass():
    report = assess(_context(), decision_at=T0)
    assert report.verdict == "PASS"
    assert {report.valid_at, report.known_at, report.usable_at, report.pipeline_safe_at} == {"PASS"}


def test_temporal_missing_bound_is_blocked_not_pass():
    report = assess(_context(known_from=None), decision_at=T0)
    assert report.verdict == "BLOCKED"
    assert report.known_at == "BLOCKED"


def test_temporal_bad_interval_fails():
    report = assess(_context(valid_from=T0.replace(day=2), valid_to=T0), decision_at=T0)
    assert report.verdict == "FAIL"


def test_executor_is_deterministic_and_preserves_source_order():
    ticks = [
        Tick("2026-01-01T00:00:00+00:00", Decimal("101"), Decimal("100"), Decimal("1"), Decimal("1"), 0),
        Tick("2026-01-01T00:00:01+00:00", Decimal("102"), Decimal("101"), Decimal("2"), Decimal("2"), 1),
    ]
    executor = DeterministicExecutor()
    assert executor.run(ticks) == executor.run(ticks)
    assert executor.run(ticks).first_read_index == 0
    assert executor.run(ticks).last_read_index == 1


def test_result_rejects_inconsistent_empty_shape():
    with pytest.raises(ValueError):
        ExperimentResult("run-1", 0, "timestamp", None, Decimal("0"), Decimal("0"))


def test_validation_report_keeps_blocked_verdict():
    report = ValidationReport(
        report_id="vr-1", subject_id="run-1", subject_type="experiment",
        validator_id="validator-v1", validator_version="1",
        context_id="ctx-1", contract_reference="minimum-experiment", contract_version="1",
        checks=(ValidationCheck("dataset", "BLOCKED", "dataset evidence unavailable"),),
        evidence_refs=(), failure_refs=(), limitations=("no dataset",),
        verdict_status="BLOCKED", verdict_reason="dataset evidence unavailable",
        input_identity="identity-1", code_version="code-1", configuration_version="cfg-1", created_at=T0,
    )
    assert report.verdict_status == "BLOCKED"


def test_failure_record_requires_revalidation_id_only_when_required():
    with pytest.raises(ValueError):
        FailureRecord(
            failure_id="f-1", detected_at=T0, detected_by="executor", subject_id="run-1",
            component="reader", failure_class="INPUT", severity="HIGH",
            observed_condition="bad", expected_condition="good", evidence_refs=(),
            diagnosis_status="UNKNOWN", diagnosis_explanation="unknown",
            containment_status="SAFE_HOLD", containment_reason="stop",
            resolution_action="NONE", resolution_actor="governance",
            revalidation_required=False, revalidation_report_id="vr-1", closure_status="OPEN",
        )

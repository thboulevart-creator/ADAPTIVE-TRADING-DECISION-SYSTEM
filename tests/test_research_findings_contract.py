from dataclasses import replace

import pytest

from src.research_findings import (
    ResearchFinding,
    ResearchFindings,
    ResearchHypothesis,
    ResearchMeasurement,
)
from tests.test_research_to_decision_boundary import coherent_inputs


def minimal_payload():
    evidence, _ = coherent_inputs()
    hypothesis = ResearchHypothesis(
        hypothesis_id="H1",
        statement="TENDANCE may favor MOMENTUM",
        prediction="Momentum metric exceeds comparator under protocol",
        falsification_rule="Comparator is not exceeded under the frozen rule",
    )
    measurement = ResearchMeasurement(
        measurement_id="M1",
        regime="TENDANCE",
        expert="MOMENTUM",
        metric="performance",
        value=1.5,
        sample_size=100,
        scope="2020-01-01/2025-01-01",
    )
    finding = ResearchFinding(
        finding_id="F1",
        hypothesis_id="H1",
        statement="Observed result is consistent with the tested hypothesis",
        supporting_measurement_ids=("M1",),
        status="SUPPORTED",
        rule_reference="H1.falsification_rule",
        reason="Protocol rule satisfied",
    )
    return evidence, hypothesis, measurement, finding


def make_findings(**overrides):
    evidence, hypothesis, measurement, finding = minimal_payload()
    values = {
        "evidence": evidence,
        "hypotheses": (hypothesis,),
        "measurements": (measurement,),
        "findings": (finding,),
        "evidence_refs": ("research/report.json",),
    }
    values.update(overrides)
    return ResearchFindings.from_research_run_evidence(**values)


def test_c0_coherent_research_run_produces_findings() -> None:
    result = make_findings()
    assert result.findings_id.startswith("FIND-")
    assert result.research_run_id
    assert result.context_id
    assert result.findings[0].status == "SUPPORTED"


def test_c1_missing_research_evidence_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    with pytest.raises(TypeError, match="ResearchRunEvidence"):
        ResearchFindings.from_research_run_evidence(
            None,
            hypotheses=(hypothesis,),
            measurements=(measurement,),
            findings=(finding,),
        )


def test_c2_wrong_upstream_object_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    with pytest.raises(TypeError, match="ResearchRunEvidence"):
        ResearchFindings.from_research_run_evidence(
            hypothesis,
            hypotheses=(hypothesis,),
            measurements=(measurement,),
            findings=(finding,),
        )


def test_c3_foreign_context_identity_in_upstream_evidence_is_propagated_not_reconstructed() -> None:
    evidence, hypothesis, measurement, finding = minimal_payload()
    forged = replace(evidence, context_id="CTX-foreign")
    result = ResearchFindings.from_research_run_evidence(
        forged,
        hypotheses=(hypothesis,),
        measurements=(measurement,),
        findings=(finding,),
    )
    assert result.context_id == "CTX-foreign"


def test_c4_duplicate_hypothesis_id_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    with pytest.raises(ValueError, match="duplicate hypothesis_id"):
        make_findings(hypotheses=(hypothesis, hypothesis))


def test_c5_unknown_hypothesis_reference_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(finding, hypothesis_id="H-UNKNOWN")
    with pytest.raises(ValueError, match="unknown hypothesis"):
        make_findings(findings=(bad,))


def test_c6_unknown_measurement_reference_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(finding, supporting_measurement_ids=("M-UNKNOWN",))
    with pytest.raises(ValueError, match="unknown measurement"):
        make_findings(findings=(bad,))


def test_c7_invalid_status_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(finding, status="BUY")
    with pytest.raises(ValueError, match="invalid finding status"):
        make_findings(findings=(bad,))


def test_c8_non_positive_sample_size_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(measurement, sample_size=0)
    with pytest.raises(ValueError, match="sample_size"):
        make_findings(measurements=(bad,))


def test_c9_duplicate_measurement_id_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    with pytest.raises(ValueError, match="duplicate measurement_id"):
        make_findings(measurements=(measurement, measurement))


def test_c10_measurement_without_scope_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(measurement, scope="")
    with pytest.raises(ValueError, match="measurement identity/scope"):
        make_findings(measurements=(bad,))


def test_c11_finding_without_supporting_measurement_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(finding, supporting_measurement_ids=())
    with pytest.raises(ValueError, match="supporting measurements"):
        make_findings(findings=(bad,))


def test_c12_not_interpretable_is_distinct_status() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    bad = replace(finding, status="NOT_INTERPRETABLE")
    result = make_findings(findings=(bad,))
    assert result.findings[0].status == "NOT_INTERPRETABLE"
    assert result.findings[0].status != "REFUTED"


def test_c13_finding_id_is_deterministic_for_same_content() -> None:
    first = make_findings()
    second = make_findings()
    assert first == second
    assert first.findings_id == second.findings_id


def test_c14_findings_id_changes_when_finding_content_changes() -> None:
    first = make_findings()
    _, hypothesis, measurement, finding = minimal_payload()
    changed = replace(finding, statement="Different evidence-bound conclusion")
    second = make_findings(findings=(changed,))
    assert first.findings_id != second.findings_id


def test_c15_trading_decision_is_not_a_findings_field() -> None:
    result = make_findings()
    assert not hasattr(result, "decision")
    assert not hasattr(result, "action_id")


def test_c16_duplicate_finding_id_is_rejected() -> None:
    _, hypothesis, measurement, finding = minimal_payload()
    with pytest.raises(ValueError, match="duplicate finding_id"):
        make_findings(findings=(finding, finding))

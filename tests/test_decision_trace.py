from dataclasses import replace

import pytest

from src.decision_trace import DecisionTrace


@pytest.fixture
def complete_trace() -> DecisionTrace:
    return DecisionTrace(
        decision_id="DEC-001",
        provenance_id="PROV-001",
        research_run_id="RUN-001",
        code_version="CODE-001",
        configuration_version="CFG-001",
        dataset_id="DATA-001",
        dataset_version="v1",
        context_id="CTX-001",
        decision="ENTER_LONG",
        action_id="ACT-001",
        result_id="RES-001",
    )


def test_complete_decision_can_be_reconstructed(complete_trace: DecisionTrace) -> None:
    status, missing = complete_trace.validate()

    assert status == "PASS"
    assert missing == ()
    assert complete_trace.reconstruction_chain() == (
        "PROV-001",
        "RUN-001",
        "CODE-001",
        "CFG-001",
        "DATA-001",
        "v1",
        "CTX-001",
        "DEC-001",
        "ACT-001",
        "RES-001",
    )


@pytest.mark.parametrize(
    "field",
    [
        "provenance_id",
        "research_run_id",
        "code_version",
        "configuration_version",
        "dataset_id",
        "dataset_version",
        "context_id",
        "decision",
        "action_id",
        "result_id",
    ],
)
def test_missing_reconstruction_link_is_not_a_pass(
    complete_trace: DecisionTrace, field: str
) -> None:
    broken = replace(complete_trace, **{field: ""})

    status, missing = broken.validate()

    assert status == "FAIL"
    assert missing == (field,)
    with pytest.raises(ValueError):
        broken.reconstruction_chain()

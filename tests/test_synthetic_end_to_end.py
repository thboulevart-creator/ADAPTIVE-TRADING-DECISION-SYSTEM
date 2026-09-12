import pytest
from dataclasses import replace

from src.decision_trace import DecisionTrace
from src.synthetic_end_to_end import build_synthetic_chain, validate_synthetic_chain


def test_synthetic_chain_is_complete_and_reconstructible():
    data, context, experience, decision, action, result, trace = build_synthetic_chain()

    assert validate_synthetic_chain(data, context, experience, decision, action, result, trace) == ("PASS", ())
    assert trace.validate() == ("PASS", ())
    assert len(trace.reconstruction_chain()) == 10


@pytest.mark.parametrize(
    "field",
    [
        "context_id",
        "decision",
        "action_id",
        "result_id",
        "dataset_id",
        "research_run_id",
    ],
)
def test_synthetic_trace_refuses_missing_links(field):
    _, _, _, _, _, _, trace = build_synthetic_chain()
    broken = DecisionTrace(**{**trace.__dict__, field: ""})

    status, missing = broken.validate()
    assert status == "FAIL"
    assert field in missing
    with pytest.raises(ValueError):
        broken.reconstruction_chain()


def test_synthetic_chain_rejects_wrong_action_linkage():
    data, context, experience, decision, action, result, trace = build_synthetic_chain()
    broken = replace(trace, action_id="action-unrelated")

    status, errors = validate_synthetic_chain(
        data, context, experience, decision, action, result, broken
    )
    assert status == "FAIL"
    assert "trace.action_id" in errors
    assert broken.validate() == ("PASS", ())

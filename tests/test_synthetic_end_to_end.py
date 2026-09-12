import pytest

from src.decision_trace import DecisionTrace
from src.synthetic_end_to_end import build_synthetic_chain


def test_synthetic_chain_is_complete_and_reconstructible():
    data, context, experience, decision, action, result, trace = build_synthetic_chain()

    assert data.data_id == context.data_id
    assert context.context_id == experience.context_id
    assert experience.research_run_id == decision.experience_id
    assert decision.decision_id == action.decision_id
    assert action.action_id == result.action_id
    assert trace.decision_id == decision.decision_id
    assert trace.action_id == action.action_id
    assert trace.result_id == result.result_id
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


def test_synthetic_chain_does_not_hide_wrong_linkage():
    _, _, _, decision, action, result, trace = build_synthetic_chain()
    broken = DecisionTrace(
        **{**trace.__dict__, "action_id": "action-unrelated"}
    )

    # Structural completeness alone must not silently claim linkage integrity.
    assert broken.validate() == ("PASS", ())
    assert broken.action_id != action.action_id
    assert result.action_id == action.action_id
    assert decision.decision_id == action.decision_id

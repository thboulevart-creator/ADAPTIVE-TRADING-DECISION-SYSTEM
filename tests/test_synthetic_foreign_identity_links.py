import pytest
from dataclasses import replace

from src.synthetic_end_to_end import build_synthetic_chain, validate_synthetic_chain


@pytest.mark.parametrize(
    "field,foreign_value,expected_error",
    [
        ("context.data_id", "data-synthetic-FOREIGN", "context.data_id"),
        ("experience.context_id", "context-foreign", "experience.context_id"),
        ("decision.experience_id", "run-foreign", "decision.experience_id"),
        ("action.decision_id", "decision-foreign", "action.decision_id"),
        ("result.action_id", "action-foreign", "result.action_id"),
        ("trace.result_id", "result-foreign", "trace.result_id"),
    ],
)
def test_synthetic_chain_rejects_foreign_identity_links(field, foreign_value, expected_error):
    data, context, experience, decision, action, result, trace = build_synthetic_chain()

    if field == "context.data_id":
        context = replace(context, data_id=foreign_value)
    elif field == "experience.context_id":
        experience = replace(experience, context_id=foreign_value)
    elif field == "decision.experience_id":
        decision = replace(decision, experience_id=foreign_value)
    elif field == "action.decision_id":
        action = replace(action, decision_id=foreign_value)
    elif field == "result.action_id":
        result = replace(result, action_id=foreign_value)
    elif field == "trace.result_id":
        trace = replace(trace, result_id=foreign_value)

    status, errors = validate_synthetic_chain(
        data, context, experience, decision, action, result, trace
    )
    assert status == "FAIL"
    assert expected_error in errors

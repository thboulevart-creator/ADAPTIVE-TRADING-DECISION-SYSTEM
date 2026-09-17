import copy
import gc
import pickle

import pytest

from src.action_result_evidence import (
    QualificationActionEvidence,
    QualificationResultObservation,
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_chain,
)
from src.decision import Decision, is_factory_attested_decision, produce_decision
from src.decision_trace import DecisionTrace
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_decision(payload: str = "HOLD") -> Decision:
    evidence, context = coherent_runtime_inputs()
    return produce_decision(evidence, context=context, decision=payload)


def coherent_chain(
    *,
    payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
):
    decision = coherent_decision(payload)
    action = engage_qualification_action(decision, behavior=behavior)
    result = observe_qualification_result(action, outcome=outcome)
    return decision, action, result


def trace_for(decision: Decision, action_id: str, result_id: str) -> DecisionTrace:
    return DecisionTrace(
        decision_id=decision.decision_id,
        provenance_id="PROV-exact-provenance",
        research_run_id=decision.research_run_id,
        code_version="CODE-exact-provenance",
        configuration_version="CFG-exact-provenance",
        dataset_id="DATA-exact-provenance",
        dataset_version="DV-exact-provenance",
        context_id=decision.context_id,
        decision=decision.decision,
        action_id=action_id,
        result_id=result_id,
    )


# G — Second breaker: exact provenance bypasses


def test_g0_action_cannot_produce_result_after_origin_decision_loses_attestation() -> None:
    """Invalidating the exact upstream Decision must fail closed downstream.

    P1.2 C5 forbids producing/accepting a Result when its Action is no longer
    admissible. An Action whose exact origin Decision has lost factory
    attestation no longer has verifiable exact provenance.
    """
    decision = coherent_decision("HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    assert is_factory_attested_decision(decision)

    object.__setattr__(decision, "decision", "MUTATED")
    assert not is_factory_attested_decision(decision)

    with pytest.raises(ValueError):
        observe_qualification_result(action, outcome="OBSERVED_AFTER_INVALID_ORIGIN")


def test_g1_garbage_collected_origin_cannot_be_replaced_by_same_id_decision() -> None:
    decision_a, action_a, result_a = coherent_chain()
    decision_id = decision_a.decision_id

    del decision_a
    gc.collect()

    decision_b = coherent_decision("HOLD")
    assert decision_b.decision_id == decision_id
    assert not verify_qualification_chain(decision_b, action_a, result_a)


def test_g2_orphaned_action_cannot_mint_new_result_when_exact_origin_is_gone() -> None:
    decision = coherent_decision("HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")

    del decision
    gc.collect()

    with pytest.raises(ValueError):
        observe_qualification_result(action, outcome="ORPHANED_ACTION_OBSERVATION")


def test_g3_repeated_identical_actions_have_distinct_ids_and_cannot_cross_bind_results() -> None:
    decision = coherent_decision("HOLD")
    action_a = engage_qualification_action(decision, behavior="NO_ACTION")
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    assert action_a is not action_b
    assert action_a.action_id != action_b.action_id

    result_a = observe_qualification_result(action_a, outcome="OBSERVED")
    assert verify_qualification_chain(decision, action_a, result_a)
    assert not verify_qualification_chain(decision, action_b, result_a)


def test_g4_repeated_identical_results_have_distinct_ids_without_losing_exact_action_link() -> None:
    decision = coherent_decision("HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result_a = observe_qualification_result(action, outcome="OBSERVED")
    result_b = observe_qualification_result(action, outcome="OBSERVED")

    assert result_a is not result_b
    assert result_a.result_id != result_b.result_id
    assert verify_qualification_chain(decision, action, result_a)
    assert verify_qualification_chain(decision, action, result_b)


def test_g5_pickle_roundtrip_is_silent_reconstruction_not_authentic_provenance() -> None:
    decision, action, result = coherent_chain()
    restored_action = pickle.loads(pickle.dumps(action))
    restored_result = pickle.loads(pickle.dumps(result))

    assert restored_action == action
    assert restored_action is not action
    assert restored_result == result
    assert restored_result is not result
    assert not verify_qualification_chain(decision, restored_action, result)
    assert not verify_qualification_chain(decision, action, restored_result)
    with pytest.raises(ValueError):
        observe_qualification_result(restored_action, outcome="OBSERVED")


def test_g6_private_origin_is_not_a_caller_supplied_public_field() -> None:
    public_fields = set(QualificationActionEvidence.__dataclass_fields__)
    assert public_fields == {"action_id", "decision_id", "behavior"}

    decision = coherent_decision("HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    for name in ("origin_decision", "origin_decision_id", "decision_ref", "_origin_decision"):
        assert not hasattr(action, name)
        with pytest.raises(AttributeError):
            object.__setattr__(action, name, decision)


def test_g7_copy_of_exact_decision_cannot_rebind_authentic_action() -> None:
    decision, action, result = coherent_chain()
    copied_decision = copy.deepcopy(decision)
    assert copied_decision == decision
    assert copied_decision is not decision
    assert not is_factory_attested_decision(copied_decision)
    assert not verify_qualification_chain(copied_decision, action, result)


def test_g8_decision_trace_with_genuine_ids_cannot_recreate_action_or_result_evidence() -> None:
    decision, action, result = coherent_chain()
    trace = trace_for(decision, action.action_id, result.result_id)
    assert trace.validate()[0] == "PASS"

    replayed_action = QualificationActionEvidence(
        action_id=trace.action_id,
        decision_id=trace.decision_id,
        behavior=action.behavior,
    )
    replayed_result = QualificationResultObservation(
        result_id=trace.result_id,
        action_id=trace.action_id,
        outcome=result.outcome,
    )

    assert not verify_qualification_chain(decision, replayed_action, replayed_result)
    assert not verify_qualification_chain(decision, replayed_action, result)
    assert not verify_qualification_chain(decision, action, replayed_result)
    with pytest.raises(ValueError):
        observe_qualification_result(replayed_action, outcome="TRACE_REPLAY")


def test_g9_trace_itself_is_never_action_or_result_provenance() -> None:
    decision, action, result = coherent_chain()
    trace = trace_for(decision, action.action_id, result.result_id)

    assert not verify_qualification_chain(decision, trace, result)
    assert not verify_qualification_chain(decision, action, trace)
    with pytest.raises(ValueError):
        observe_qualification_result(trace, outcome="TRACE_AS_ACTION")  # type: ignore[arg-type]

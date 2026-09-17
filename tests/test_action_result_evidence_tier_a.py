import copy
import inspect
from dataclasses import replace

import pytest

import src.action_result_evidence as evidence_module
from src.action_result_evidence import (
    QualificationActionEvidence,
    QualificationResultObservation,
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_chain,
)
from src.decision import Decision, produce_decision
from src.decision_trace import DecisionTrace
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_decision(payload: str = "HOLD") -> Decision:
    evidence, context = coherent_runtime_inputs()
    return produce_decision(evidence, context=context, decision=payload)


def coherent_chain(
    *,
    decision_payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
):
    decision = coherent_decision(decision_payload)
    action = engage_qualification_action(decision, behavior=behavior)
    result = observe_qualification_result(action, outcome=outcome)
    return decision, action, result


def reconstruct_action(source: QualificationActionEvidence, **changes) -> QualificationActionEvidence:
    values = {
        "action_id": source.action_id,
        "decision_id": source.decision_id,
        "behavior": source.behavior,
    }
    values.update(changes)
    return QualificationActionEvidence(**values)


def reconstruct_result(
    source: QualificationResultObservation,
    **changes,
) -> QualificationResultObservation:
    values = {
        "result_id": source.result_id,
        "action_id": source.action_id,
        "outcome": source.outcome,
    }
    values.update(changes)
    return QualificationResultObservation(**values)


def trace_for(decision: Decision, action_id: str, result_id: str) -> DecisionTrace:
    return DecisionTrace(
        decision_id=decision.decision_id,
        provenance_id="PROV-test",
        research_run_id=decision.research_run_id,
        code_version="CODE-test",
        configuration_version="CFG-test",
        dataset_id="DATA-test",
        dataset_version="DV-test",
        context_id=decision.context_id,
        decision=decision.decision,
        action_id=action_id,
        result_id=result_id,
    )


# A — Existence and origin of Action

def test_a0_authentic_action_and_result_form_a_valid_qualification_chain() -> None:
    decision, action, result = coherent_chain()
    assert verify_qualification_chain(decision, action, result)


def test_a1_absent_decision_cannot_engage_action() -> None:
    with pytest.raises(ValueError):
        engage_qualification_action(None, behavior="NO_ACTION")


def test_a2_wrong_decision_type_cannot_engage_action() -> None:
    with pytest.raises(ValueError):
        engage_qualification_action(object(), behavior="NO_ACTION")  # type: ignore[arg-type]


def test_a3_decision_id_alone_cannot_engage_action() -> None:
    decision = coherent_decision()
    with pytest.raises(ValueError):
        engage_qualification_action(decision.decision_id, behavior="NO_ACTION")  # type: ignore[arg-type]


def test_a4_serialized_decision_fields_cannot_engage_action() -> None:
    decision = coherent_decision()
    serialized = {
        "decision_id": decision.decision_id,
        "research_run_id": decision.research_run_id,
        "context_id": decision.context_id,
        "decision": decision.decision,
    }
    with pytest.raises(ValueError):
        engage_qualification_action(serialized, behavior="NO_ACTION")  # type: ignore[arg-type]


def test_a5_exact_manual_action_reconstruction_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    forged = reconstruct_action(action)
    assert forged == action
    assert forged is not action
    assert not verify_qualification_chain(decision, forged, result)
    with pytest.raises(ValueError):
        observe_qualification_result(forged, outcome="OBSERVED")


def test_a6_authentic_foreign_decision_with_same_id_cannot_claim_action() -> None:
    # Two authentic producer-created Decisions can be distinct objects while
    # carrying the same deterministic decision_id. P1.2 requires binding to the
    # exact Decision object, not merely equality of decision_id values.
    decision_a = coherent_decision("HOLD")
    decision_b = coherent_decision("HOLD")
    assert decision_a is not decision_b
    assert decision_a.decision_id == decision_b.decision_id

    action_a = engage_qualification_action(decision_a, behavior="NO_ACTION")
    result_a = observe_qualification_result(action_a, outcome="OBSERVED")

    assert not verify_qualification_chain(decision_b, action_a, result_a)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a7_action_copy_or_deepcopy_is_not_admissible(copier) -> None:
    decision, action, result = coherent_chain()
    copied = copier(action)
    assert copied == action
    assert copied is not action
    assert not verify_qualification_chain(decision, copied, result)


def test_a7_action_replace_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    copied = replace(action, behavior=action.behavior)
    assert copied == action
    assert copied is not action
    assert not verify_qualification_chain(decision, copied, result)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("action_id", "QACT-mutated"),
        ("decision_id", "DEC-mutated"),
        ("behavior", "BUY"),
    ],
)
def test_a8_post_production_action_mutation_invalidates_chain(field: str, value: str) -> None:
    decision, action, result = coherent_chain()
    object.__setattr__(action, field, value)
    assert not verify_qualification_chain(decision, action, result)


def test_a9_declared_but_unproduced_action_is_not_admissible() -> None:
    decision = coherent_decision()
    declared = QualificationActionEvidence(
        action_id="QACT-declared",
        decision_id=decision.decision_id,
        behavior="BUY",
    )
    declared_result = QualificationResultObservation(
        result_id="QRES-declared",
        action_id=declared.action_id,
        outcome="SUCCESS",
    )
    assert not verify_qualification_chain(decision, declared, declared_result)


def test_a10_decision_trace_action_id_is_not_action_evidence() -> None:
    decision, action, result = coherent_chain()
    trace = trace_for(decision, action.action_id, result.result_id)
    assert trace.validate()[0] == "PASS"
    with pytest.raises(ValueError):
        observe_qualification_result(trace.action_id, outcome="OBSERVED")  # type: ignore[arg-type]


def test_a11_controlled_no_action_is_a_valid_qualification_action() -> None:
    decision = coherent_decision()
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome="NO_ACTION_OBSERVED")
    assert action.behavior == "NO_ACTION"
    assert verify_qualification_chain(decision, action, result)


# B — Existence and origin of Result

def test_b0_authentic_result_for_exact_action_is_admissible() -> None:
    decision, action, result = coherent_chain(outcome="SUCCESS")
    assert verify_qualification_chain(decision, action, result)


def test_b1_absent_result_is_not_admissible() -> None:
    decision = coherent_decision()
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    assert not verify_qualification_chain(decision, action, None)


def test_b2_wrong_result_type_is_not_admissible() -> None:
    decision = coherent_decision()
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    assert not verify_qualification_chain(decision, action, object())


def test_b3_result_id_alone_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    assert not verify_qualification_chain(decision, action, result.result_id)


def test_b4_serialized_result_fields_are_not_admissible() -> None:
    decision, action, result = coherent_chain()
    serialized = {
        "result_id": result.result_id,
        "action_id": result.action_id,
        "outcome": result.outcome,
    }
    assert not verify_qualification_chain(decision, action, serialized)


def test_b5_exact_manual_result_reconstruction_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    forged = reconstruct_result(result)
    assert forged == result
    assert forged is not result
    assert not verify_qualification_chain(decision, action, forged)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_b6_result_copy_or_deepcopy_is_not_admissible(copier) -> None:
    decision, action, result = coherent_chain()
    copied = copier(result)
    assert copied == result
    assert copied is not result
    assert not verify_qualification_chain(decision, action, copied)


def test_b6_result_replace_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    copied = replace(result, outcome=result.outcome)
    assert copied == result
    assert copied is not result
    assert not verify_qualification_chain(decision, action, copied)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("result_id", "QRES-mutated"),
        ("action_id", "QACT-mutated"),
        ("outcome", "MUTATED"),
    ],
)
def test_b7_post_observation_result_mutation_invalidates_chain(field: str, value: str) -> None:
    decision, action, result = coherent_chain()
    object.__setattr__(result, field, value)
    assert not verify_qualification_chain(decision, action, result)


def test_b8_declared_success_without_qualified_observation_is_not_admissible() -> None:
    decision = coherent_decision()
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    declared = QualificationResultObservation(
        result_id="QRES-declared-success",
        action_id=action.action_id,
        outcome="SUCCESS",
    )
    assert not verify_qualification_chain(decision, action, declared)


def test_b9_decision_trace_result_id_is_not_result_observation() -> None:
    decision, action, result = coherent_chain()
    trace = trace_for(decision, action.action_id, result.result_id)
    assert trace.validate()[0] == "PASS"
    assert not verify_qualification_chain(decision, action, trace.result_id)


def test_b10_candidate_does_not_claim_temporal_validation_without_temporal_fields() -> None:
    action_fields = set(QualificationActionEvidence.__dataclass_fields__)
    result_fields = set(QualificationResultObservation.__dataclass_fields__)
    forbidden = {"timestamp", "engaged_at", "observed_at", "valid_from", "valid_until"}
    assert action_fields.isdisjoint(forbidden)
    assert result_fields.isdisjoint(forbidden)


# C — Action -> Result exact binding

def test_c0_result_from_action_b_cannot_be_presented_as_result_of_action_a() -> None:
    decision = coherent_decision()
    action_a = engage_qualification_action(decision, behavior="NO_ACTION")
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")
    assert action_a.action_id != action_b.action_id
    assert not verify_qualification_chain(decision, action_a, result_b)


def test_c1_reconstructed_result_cannot_be_rebound_to_another_action() -> None:
    decision = coherent_decision()
    action_a = engage_qualification_action(decision, behavior="NO_ACTION")
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_a = observe_qualification_result(action_a, outcome="OBSERVED")
    rebound = reconstruct_result(result_a, action_id=action_b.action_id)
    assert not verify_qualification_chain(decision, action_b, rebound)


def test_c2_same_result_id_with_different_outcome_is_not_admissible() -> None:
    decision, action, result = coherent_chain(outcome="SUCCESS")
    forged = reconstruct_result(result, outcome="FAIL")
    assert forged.result_id == result.result_id
    assert not verify_qualification_chain(decision, action, forged)


def test_c3_action_result_pair_from_foreign_decision_chain_is_not_admissible() -> None:
    decision_a, action_a, result_a = coherent_chain(decision_payload="BUY")
    decision_b = coherent_decision("SELL")
    assert decision_a.decision_id != decision_b.decision_id
    assert not verify_qualification_chain(decision_b, action_a, result_a)


def test_c4_candidate_does_not_invent_staleness_semantics_without_validity_domain() -> None:
    decision, action, result = coherent_chain()
    assert verify_qualification_chain(decision, action, result)
    assert "valid_until" not in QualificationResultObservation.__dataclass_fields__
    assert "valid_from" not in QualificationResultObservation.__dataclass_fields__


def test_c5_result_cannot_be_observed_from_unattested_action() -> None:
    decision = coherent_decision()
    forged = QualificationActionEvidence(
        action_id="QACT-forged",
        decision_id=decision.decision_id,
        behavior="NO_ACTION",
    )
    with pytest.raises(ValueError):
        observe_qualification_result(forged, outcome="OBSERVED")


def test_c6_missing_or_ambiguous_action_link_is_not_admissible() -> None:
    decision, action, result = coherent_chain()
    missing = reconstruct_result(result, action_id="")
    foreign = reconstruct_result(result, action_id="QACT-foreign")
    assert not verify_qualification_chain(decision, action, missing)
    assert not verify_qualification_chain(decision, action, foreign)


# D — Forbidden semantic shortcuts

def test_d0_decision_cannot_skip_action_and_directly_produce_result() -> None:
    decision = coherent_decision()
    with pytest.raises(ValueError):
        observe_qualification_result(decision, outcome="SUCCESS")  # type: ignore[arg-type]


def test_d1_favorable_result_has_no_causality_claim() -> None:
    _, _, result = coherent_chain(outcome="SUCCESS")
    assert not hasattr(result, "caused_by_action")
    assert not hasattr(result, "causal")
    assert not hasattr(result, "causality")


def test_d2_favorable_result_does_not_validate_decision_or_knowledge() -> None:
    _, _, result = coherent_chain(outcome="SUCCESS")
    assert not hasattr(result, "decision_valid")
    assert not hasattr(result, "knowledge_valid")
    assert not hasattr(result, "authorized")


def test_d3_absent_result_is_not_implicitly_success_failure_or_neutral() -> None:
    decision = coherent_decision()
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    assert not verify_qualification_chain(decision, action, None)


def test_d4_decision_trace_remains_downstream_and_cannot_mint_evidence() -> None:
    source = inspect.getsource(evidence_module)
    assert "from src.decision_trace" not in source
    assert "import src.decision_trace" not in source
    assert not hasattr(evidence_module, "DecisionTrace")


def test_d5_no_action_is_not_rejected_for_lack_of_broker_order() -> None:
    decision, action, result = coherent_chain(
        behavior="NO_ACTION",
        outcome="NO_ACTION_OBSERVED",
    )
    assert verify_qualification_chain(decision, action, result)


# E — Operational bypass surface must remain absent

def test_e0_candidate_exposes_no_order_or_broker_request_constructor() -> None:
    forbidden = {
        "Action",
        "Order",
        "BrokerRequest",
        "create_order",
        "order_send",
        "execute_action",
        "submit_order",
    }
    assert forbidden.isdisjoint(set(vars(evidence_module)))


def test_e1_candidate_has_no_network_acquisition_broker_or_exchange_dependency() -> None:
    source = inspect.getsource(evidence_module)
    forbidden_imports = (
        "import requests",
        "import socket",
        "import MetaTrader5",
        "from MetaTrader5",
        "urllib.request",
        "dukascopy",
        ".bi5",
    )
    assert all(token not in source for token in forbidden_imports)


def test_e2_candidate_exposes_no_quantitative_risk_or_sizing_surface() -> None:
    forbidden = {
        "lot_size",
        "position_size",
        "leverage",
        "stop_loss",
        "take_profit",
        "risk_budget",
    }
    action_fields = set(QualificationActionEvidence.__dataclass_fields__)
    result_fields = set(QualificationResultObservation.__dataclass_fields__)
    assert action_fields.isdisjoint(forbidden)
    assert result_fields.isdisjoint(forbidden)
    assert forbidden.isdisjoint(set(vars(evidence_module)))


def test_e3_candidate_exposes_no_backtest_or_live_activation_surface() -> None:
    forbidden = {
        "run_backtest",
        "real_backtest",
        "activate_live",
        "live_activation",
        "massive_acquisition",
    }
    assert forbidden.isdisjoint(set(vars(evidence_module)))


def test_e4_rejected_action_cannot_continue_to_result() -> None:
    decision = coherent_decision()
    rejected = QualificationActionEvidence(
        action_id="QACT-rejected",
        decision_id=decision.decision_id,
        behavior="BUY",
    )
    with pytest.raises(ValueError):
        observe_qualification_result(rejected, outcome="SUCCESS")


def test_e5_qualification_evidence_is_not_an_operational_permission() -> None:
    decision, action, result = coherent_chain()
    assert verify_qualification_chain(decision, action, result)
    assert not hasattr(action, "authorized")
    assert not hasattr(result, "authorized")
    assert not hasattr(evidence_module, "AUTHORIZED")
    assert not hasattr(evidence_module, "execute")

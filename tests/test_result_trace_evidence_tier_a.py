import copy
import inspect
from dataclasses import asdict, replace

import pytest

import src.decision_trace as trace_module
from src.action_result_evidence import (
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_chain,
)
from src.decision import Decision, produce_decision
from src.decision_trace import (
    DecisionTrace,
    is_factory_attested_decision_trace,
    produce_decision_trace,
)
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested
from tests.research_runtime_fixture import coherent_runtime_inputs, synthetic_runtime_case


def coherent_inputs(*, decision_payload: str = "HOLD", outcome: str = "OBSERVED"):
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision=decision_payload)
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome=outcome)
    return evidence, context, decision, action, result


def coherent_trace(*, decision_payload: str = "HOLD", outcome: str = "OBSERVED"):
    evidence, context, decision, action, result = coherent_inputs(
        decision_payload=decision_payload,
        outcome=outcome,
    )
    trace = produce_decision_trace(evidence, decision, action, result)
    return evidence, context, decision, action, result, trace


def manual_trace_from(source: DecisionTrace, **changes) -> DecisionTrace:
    values = asdict(source)
    values.update(changes)
    return DecisionTrace(**values)


# A — A coherent list of identifiers is not evidence of a real history.


def test_a0_exact_qualified_chain_produces_attested_trace() -> None:
    _, _, decision, action, result, trace = coherent_trace()
    assert verify_qualification_chain(decision, action, result)
    assert trace.validate() == ("PASS", ())
    assert is_factory_attested_decision_trace(trace)
    assert trace.decision_id == decision.decision_id
    assert trace.action_id == action.action_id
    assert trace.result_id == result.result_id


def test_a1_ids_alone_cannot_produce_trace() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    with pytest.raises(ValueError):
        produce_decision_trace(
            evidence.research_run_id,
            decision.decision_id,
            action.action_id,
            result.result_id,
        )


def test_a2_manual_structurally_complete_trace_is_not_attested() -> None:
    *_, authentic = coherent_trace()
    forged = manual_trace_from(authentic)
    assert forged == authentic
    assert forged is not authentic
    assert forged.validate() == ("PASS", ())
    assert not is_factory_attested_decision_trace(forged)


def test_a3_serialized_trace_fields_are_not_trace_evidence() -> None:
    *_, authentic = coherent_trace()
    serialized = asdict(authentic)
    assert not is_factory_attested_decision_trace(serialized)


def test_a4_structural_pass_does_not_imply_p13_attestation() -> None:
    *_, authentic = coherent_trace()
    forged = manual_trace_from(authentic)
    assert forged.validate()[0] == "PASS"
    assert not is_factory_attested_decision_trace(forged)


def test_a5_reconstruction_chain_is_not_proof_of_event_existence() -> None:
    *_, authentic = coherent_trace()
    forged = manual_trace_from(authentic)
    assert forged.reconstruction_chain() == authentic.reconstruction_chain()
    assert not is_factory_attested_decision_trace(forged)


# B — Exact downstream objects must not be substitutable by foreign or rebuilt ones.


def test_b0_foreign_decision_is_rejected() -> None:
    evidence, context, decision_a, action_a, result_a = coherent_inputs(decision_payload="BUY")
    decision_b = produce_decision(evidence, context=context, decision="SELL")
    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision_b, action_a, result_a)


def test_b1_foreign_action_is_rejected() -> None:
    evidence, _, decision, action_a, result_a = coherent_inputs()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    assert action_b is not action_a
    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision, action_b, result_a)


def test_b2_foreign_result_is_rejected() -> None:
    evidence, _, decision, action_a, _ = coherent_inputs()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")
    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision, action_a, result_b)


def test_b3_foreign_action_result_pair_from_another_decision_is_rejected() -> None:
    evidence_a, _, decision_a, _, _ = coherent_inputs(decision_payload="BUY")
    _, _, _, action_b, result_b = coherent_inputs(decision_payload="SELL")
    with pytest.raises(ValueError):
        produce_decision_trace(evidence_a, decision_a, action_b, result_b)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_b4_trace_copy_or_deepcopy_does_not_reproduce_attestation(copier) -> None:
    *_, trace = coherent_trace()
    copied = copier(trace)
    assert copied == trace
    assert copied is not trace
    assert not is_factory_attested_decision_trace(copied)


def test_b4_trace_replace_does_not_reproduce_attestation() -> None:
    *_, trace = coherent_trace()
    copied = replace(trace, result_id=trace.result_id)
    assert copied == trace
    assert copied is not trace
    assert not is_factory_attested_decision_trace(copied)


def test_b5_post_production_trace_mutation_invalidates_attestation() -> None:
    *_, trace = coherent_trace()
    object.__setattr__(trace, "result_id", "QRES-mutated")
    assert not is_factory_attested_decision_trace(trace)


def test_b5_mutated_result_cannot_produce_trace() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    object.__setattr__(result, "outcome", "MUTATED")
    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision, action, result)


# C — Research/provenance metadata must be evidence-bound, never caller-declared.


def test_c0_missing_research_evidence_is_rejected() -> None:
    _, _, decision, action, result = coherent_inputs()
    with pytest.raises(ValueError):
        produce_decision_trace(None, decision, action, result)


def test_c1_wrong_research_evidence_type_is_rejected() -> None:
    _, _, decision, action, result = coherent_inputs()
    with pytest.raises(ValueError):
        produce_decision_trace(object(), decision, action, result)


def test_c2_serialized_research_fields_are_rejected() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    with pytest.raises(ValueError):
        produce_decision_trace(asdict(evidence), decision, action, result)


def test_c3_manual_research_evidence_reconstruction_is_rejected() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    forged = ResearchRunEvidence(**asdict(evidence))
    assert forged == evidence
    assert forged is not evidence
    assert not is_factory_attested(forged)
    with pytest.raises(ValueError):
        produce_decision_trace(forged, decision, action, result)


def test_c4_authentic_foreign_research_run_id_is_rejected() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    with synthetic_runtime_case(code_version="f" * 40) as foreign_case:
        foreign = foreign_case.evidence
        assert is_factory_attested(foreign)
        assert foreign.research_run_id != evidence.research_run_id
        with pytest.raises(ValueError):
            produce_decision_trace(foreign, decision, action, result)


def test_c5_mutated_context_identity_invalidates_research_evidence() -> None:
    evidence, _, decision, action, result = coherent_inputs()
    object.__setattr__(evidence, "context_id", "CTX-mutated")
    assert not is_factory_attested(evidence)
    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision, action, result)


def test_c6_trace_metadata_cannot_be_overridden_by_caller() -> None:
    signature = inspect.signature(produce_decision_trace)
    assert set(signature.parameters) == {"evidence", "decision", "action", "result"}
    evidence, _, decision, action, result = coherent_inputs()
    with pytest.raises(TypeError):
        produce_decision_trace(  # type: ignore[call-arg]
            evidence,
            decision,
            action,
            result,
            provenance_id="PROV-forged",
        )


def test_c7_authentic_foreign_same_identity_evidence_cannot_claim_decision_origin() -> None:
    evidence_a, context_a = coherent_runtime_inputs()
    evidence_b, _ = coherent_runtime_inputs()
    assert evidence_a is not evidence_b
    assert evidence_a == evidence_b
    assert is_factory_attested(evidence_a)
    assert is_factory_attested(evidence_b)

    decision = produce_decision(evidence_a, context=context_a, decision="HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome="OBSERVED")

    # P1.3 requires the actual upstream provenance of this Decision, not an
    # independently produced same-valued ResearchRunEvidence object.
    with pytest.raises(ValueError):
        produce_decision_trace(evidence_b, decision, action, result)


# D — TRACE is downstream only and cannot mint or repair prior events.


def test_d0_trace_cannot_be_used_as_decision() -> None:
    *_, trace = coherent_trace()
    with pytest.raises(ValueError):
        engage_qualification_action(trace, behavior="NO_ACTION")  # type: ignore[arg-type]


def test_d1_trace_action_id_cannot_mint_result() -> None:
    *_, trace = coherent_trace()
    with pytest.raises(ValueError):
        observe_qualification_result(trace.action_id, outcome="OBSERVED")  # type: ignore[arg-type]


def test_d2_trace_result_id_is_not_result_observation() -> None:
    _, _, decision, action, _, trace = coherent_trace()
    assert not verify_qualification_chain(decision, action, trace.result_id)


def test_d3_mutating_trace_does_not_rewrite_upstream_objects() -> None:
    _, _, decision, action, result, trace = coherent_trace()
    original = (decision.decision_id, action.action_id, result.result_id)
    object.__setattr__(trace, "action_id", "QACT-rewritten")
    assert (decision.decision_id, action.action_id, result.result_id) == original
    assert not is_factory_attested_decision_trace(trace)


def test_d4_favorable_result_does_not_create_causality_or_validation_fields() -> None:
    *_, trace = coherent_trace(outcome="SUCCESS")
    for name in ("causal", "caused_by_action", "decision_valid", "knowledge_valid", "authorized"):
        assert not hasattr(trace, name)


def test_d5_missing_metadata_is_not_silently_repaired() -> None:
    *_, authentic = coherent_trace()
    incomplete = manual_trace_from(authentic, provenance_id="")
    assert incomplete.validate()[0] == "FAIL"
    assert not is_factory_attested_decision_trace(incomplete)


# E — P1.3 must remain a local evidence boundary, not an execution surface.


def test_e0_trace_module_has_no_broker_or_exchange_surface() -> None:
    source = inspect.getsource(trace_module)
    forbidden = ("MetaTrader5", "order_send", "submit_order", "create_order", "broker", "exchange")
    assert all(token not in source for token in forbidden)


def test_e1_trace_module_has_no_sizing_or_quantitative_risk_surface() -> None:
    source = inspect.getsource(trace_module)
    forbidden = ("lot_size", "position_size", "leverage", "stop_loss", "take_profit", "risk_budget")
    assert all(token not in source for token in forbidden)


def test_e2_trace_module_has_no_network_or_acquisition_surface() -> None:
    source = inspect.getsource(trace_module)
    forbidden = ("requests", "urllib.request", "socket", ".bi5", "dukascopy")
    assert all(token not in source for token in forbidden)


def test_e3_trace_module_has_no_real_backtest_surface() -> None:
    assert not hasattr(trace_module, "run_backtest")
    assert not hasattr(trace_module, "real_backtest")


def test_e4_trace_module_has_no_live_activation_surface() -> None:
    assert not hasattr(trace_module, "activate_live")
    assert not hasattr(trace_module, "live_activation")


def test_e5_attested_trace_is_not_operational_permission() -> None:
    *_, trace = coherent_trace()
    assert is_factory_attested_decision_trace(trace)
    assert not hasattr(trace, "authorized")
    assert not hasattr(trace_module, "AUTHORIZED")
    assert not hasattr(trace_module, "execute")

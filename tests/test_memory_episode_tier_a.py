import copy
import gc
import inspect
import weakref
from dataclasses import asdict, replace

import pytest

import src.memory_episode as memory_module
from src.action_result_evidence import (
    QualificationActionEvidence,
    QualificationResultObservation,
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_observation_pair,
)
from src.decision import produce_decision
from src.decision_trace import DecisionTrace, produce_decision_trace
from src.memory_episode import (
    ObservationalMemoryEpisode,
    is_factory_attested_memory_episode,
    produce_observational_memory_episode,
)
from src.research_findings import ResearchFindings
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_episode(
    *,
    decision_payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
):
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision=decision_payload)
    action = engage_qualification_action(decision, behavior=behavior)
    result = observe_qualification_result(action, outcome=outcome)
    trace = produce_decision_trace(evidence, decision, action, result)
    episode = produce_observational_memory_episode(trace, action, result)
    return evidence, context, decision, action, result, trace, episode


def manual_trace_from(source: DecisionTrace, **changes) -> DecisionTrace:
    values = asdict(source)
    values.update(changes)
    return DecisionTrace(**values)


def manual_episode_from(
    source: ObservationalMemoryEpisode, **changes
) -> ObservationalMemoryEpisode:
    values = asdict(source)
    values.update(changes)
    return ObservationalMemoryEpisode(**values)


# A — Only the exact P1.3-attested Trace may seed an observational episode.


def test_a0_exact_trace_action_result_produce_attested_episode() -> None:
    _, _, decision, action, result, trace, episode = coherent_episode()
    assert verify_qualification_observation_pair(action, result)
    assert is_factory_attested_memory_episode(episode)
    assert episode.decision_id == decision.decision_id == trace.decision_id
    assert episode.action_id == action.action_id == trace.action_id
    assert episode.result_id == result.result_id == trace.result_id
    assert episode.behavior == action.behavior
    assert episode.outcome == result.outcome


def test_a1_manual_same_valued_trace_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    forged = manual_trace_from(trace)
    assert forged == trace and forged is not trace
    with pytest.raises(ValueError):
        produce_observational_memory_episode(forged, action, result)


def test_a2_structural_pass_without_p13_attestation_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    forged = manual_trace_from(trace)
    assert forged.validate()[0] == "PASS"
    with pytest.raises(ValueError):
        produce_observational_memory_episode(forged, action, result)


def test_a3_serialized_trace_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    with pytest.raises(ValueError):
        produce_observational_memory_episode(asdict(trace), action, result)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a4_trace_copy_or_deepcopy_is_rejected(copier) -> None:
    *_, action, result, trace, _ = coherent_episode()
    copied = copier(trace)
    assert copied == trace and copied is not trace
    with pytest.raises(ValueError):
        produce_observational_memory_episode(copied, action, result)


def test_a4_trace_replace_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    copied = replace(trace, result_id=trace.result_id)
    assert copied == trace and copied is not trace
    with pytest.raises(ValueError):
        produce_observational_memory_episode(copied, action, result)


def test_a5_mutated_attested_trace_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    object.__setattr__(trace, "decision", "MUTATED")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action, result)


# B — Action/Result must remain exact and currently admissible.


def test_b0_exact_action_result_pair_is_accepted() -> None:
    *_, action, result, trace, episode = coherent_episode()
    assert verify_qualification_observation_pair(action, result)
    assert is_factory_attested_memory_episode(episode)
    assert produce_observational_memory_episode(trace, action, result).episode_id == episode.episode_id


def test_b1_rebuilt_same_valued_action_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    rebuilt = QualificationActionEvidence(**asdict(action))
    assert rebuilt == action and rebuilt is not action
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, rebuilt, result)


def test_b2_rebuilt_same_valued_result_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    rebuilt = QualificationResultObservation(**asdict(result))
    assert rebuilt == result and rebuilt is not result
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action, rebuilt)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_b3_action_copy_or_deepcopy_is_rejected(copier) -> None:
    *_, action, result, trace, _ = coherent_episode()
    copied = copier(action)
    assert copied == action and copied is not action
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, copied, result)


def test_b3_result_replace_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    copied = replace(result, outcome=result.outcome)
    assert copied == result and copied is not result
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action, copied)


def test_b4_mutated_action_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    object.__setattr__(action, "behavior", "MUTATED")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action, result)


def test_b4_mutated_result_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    object.__setattr__(result, "outcome", "MUTATED")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action, result)


def test_b5_foreign_authentic_action_is_rejected() -> None:
    _, _, decision, action_a, result_a, trace, _ = coherent_episode()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    assert action_b.action_id != action_a.action_id
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action_b, result_a)


def test_b6_foreign_authentic_result_is_rejected() -> None:
    _, _, decision, action_a, _, trace, _ = coherent_episode()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action_a, result_b)


def test_b7_authentic_pair_from_another_chain_is_rejected() -> None:
    *_, trace_a, _ = coherent_episode(decision_payload="BUY")
    _, _, _, action_b, result_b, _, _ = coherent_episode(decision_payload="SELL")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace_a, action_b, result_b)


def test_b8_collected_inputs_cannot_be_rebuilt_from_trace() -> None:
    _, _, decision, action, result, trace, _ = coherent_episode()
    action_values = asdict(action)
    result_values = asdict(result)
    action_ref = weakref.ref(action)
    result_ref = weakref.ref(result)
    del action
    del result
    gc.collect()
    assert action_ref() is None
    assert result_ref() is None
    rebuilt_action = QualificationActionEvidence(**action_values)
    rebuilt_result = QualificationResultObservation(**result_values)
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, rebuilt_action, rebuilt_result)
    assert decision.decision_id == trace.decision_id


# C — IDs must agree, but equal IDs cannot replace object admissibility.


def test_c0_trace_action_id_mismatch_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    foreign_trace = manual_trace_from(trace, action_id="QACT-foreign")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(foreign_trace, action, result)


def test_c1_trace_result_id_mismatch_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    foreign_trace = manual_trace_from(trace, result_id="QRES-foreign")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(foreign_trace, action, result)


def test_c2_trace_decision_id_mismatch_is_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    foreign_trace = manual_trace_from(trace, decision_id="DEC-foreign")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(foreign_trace, action, result)


def test_c3_result_action_mismatch_is_rejected() -> None:
    _, _, decision, action_a, _, trace, _ = coherent_episode()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, action_a, result_b)


def test_c4_coherent_ids_on_unattested_objects_are_rejected() -> None:
    *_, action, result, trace, _ = coherent_episode()
    rebuilt_action = QualificationActionEvidence(**asdict(action))
    rebuilt_result = QualificationResultObservation(**asdict(result))
    assert rebuilt_action.action_id == trace.action_id
    assert rebuilt_result.result_id == trace.result_id
    with pytest.raises(ValueError):
        produce_observational_memory_episode(trace, rebuilt_action, rebuilt_result)


def test_c5_observation_content_cannot_be_overridden_by_caller() -> None:
    signature = inspect.signature(produce_observational_memory_episode)
    assert set(signature.parameters) == {"trace", "action", "result"}
    *_, action, result, trace, _ = coherent_episode()
    with pytest.raises(TypeError):
        produce_observational_memory_episode(  # type: ignore[call-arg]
            trace,
            action,
            result,
            behavior="INTERPRETED",
        )


# D — Observation must not silently become interpretation.


def test_d0_action_followed_by_result_does_not_create_causality() -> None:
    *_, episode = coherent_episode(outcome="SUCCESS")
    for name in ("causal", "caused_by_action", "causal_effect", "cause"):
        assert not hasattr(episode, name)


def test_d1_favorable_result_does_not_mark_decision_correct() -> None:
    *_, episode = coherent_episode(outcome="SUCCESS")
    for name in ("decision_correct", "decision_valid", "correct"):
        assert not hasattr(episode, name)


def test_d2_unfavorable_result_does_not_mark_decision_incorrect() -> None:
    *_, episode = coherent_episode(outcome="FAIL")
    for name in ("decision_incorrect", "decision_invalid", "incorrect"):
        assert not hasattr(episode, name)


def test_d3_hypothesis_or_explanation_cannot_be_caller_supplied() -> None:
    *_, action, result, trace, episode = coherent_episode()
    assert not hasattr(episode, "hypothesis")
    assert not hasattr(episode, "explanation")
    with pytest.raises(TypeError):
        produce_observational_memory_episode(  # type: ignore[call-arg]
            trace,
            action,
            result,
            hypothesis="post-hoc",
        )


def test_d4_confidence_is_not_episode_truth() -> None:
    *_, episode = coherent_episode()
    for name in ("confidence", "confidence_score", "evidence_level"):
        assert not hasattr(episode, name)


def test_d5_rewriting_observation_invalidates_episode_attestation() -> None:
    *_, episode = coherent_episode()
    object.__setattr__(episode, "outcome", "CLASSIFIED_AFTERWARD")
    assert not is_factory_attested_memory_episode(episode)


# E — An observational episode is not knowledge or experimental interpretation.


def test_e0_favorable_outcome_does_not_create_supported_status() -> None:
    *_, episode = coherent_episode(outcome="SUCCESS")
    assert not hasattr(episode, "status")
    assert "SUPPORTED" not in asdict(episode).values()


def test_e1_episode_is_not_validated_knowledge() -> None:
    *_, episode = coherent_episode()
    for name in ("knowledge", "knowledge_valid", "validated_knowledge"):
        assert not hasattr(episode, name)


def test_e2_repeated_episode_does_not_create_truth_or_rule() -> None:
    *prefix, action, result, trace, first = coherent_episode()
    second = produce_observational_memory_episode(trace, action, result)
    assert first is not second
    assert first.episode_id == second.episode_id
    assert is_factory_attested_memory_episode(first)
    assert is_factory_attested_memory_episode(second)
    for value in (first, second):
        assert not hasattr(value, "truth")
        assert not hasattr(value, "rule")
        assert not hasattr(value, "independent_evidence")


def test_e3_absence_of_findings_is_not_not_interpretable() -> None:
    *_, episode = coherent_episode()
    assert not hasattr(episode, "finding_status")
    assert not hasattr(episode, "status")
    assert "NOT_INTERPRETABLE" not in asdict(episode).values()


def test_e4_episode_does_not_prove_hypothesis_preexistence() -> None:
    *_, episode = coherent_episode()
    for name in ("hypothesis_id", "hypothesis", "known_from", "available_before_decision"):
        assert not hasattr(episode, name)


def test_e5_episode_cannot_seed_research_findings_as_research_evidence() -> None:
    *_, episode = coherent_episode()
    with pytest.raises(TypeError):
        ResearchFindings.from_research_run_evidence(
            episode,  # type: ignore[arg-type]
            hypotheses=(),
            measurements=(),
            findings=(),
        )


# F — MEMORY remains downstream and cannot authorize or recreate upstream objects.


def test_f0_episode_cannot_mint_or_repair_trace() -> None:
    _, _, decision, action, result, _, episode = coherent_episode()
    with pytest.raises(ValueError):
        produce_decision_trace(episode, decision, action, result)


def test_f1_episode_cannot_mint_action_or_result() -> None:
    *_, episode = coherent_episode()
    with pytest.raises(ValueError):
        engage_qualification_action(episode, behavior="NO_ACTION")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        observe_qualification_result(episode, outcome="OBSERVED")  # type: ignore[arg-type]


def test_f2_episode_cannot_be_research_evidence_for_decision() -> None:
    _, context, _, _, _, _, episode = coherent_episode()
    with pytest.raises(ValueError):
        produce_decision(episode, context=context, decision="HOLD")  # type: ignore[arg-type]


def test_f3_episode_is_not_authorized_action_permission() -> None:
    *_, episode = coherent_episode()
    assert not hasattr(episode, "authorized")
    assert not hasattr(episode, "authorization")
    with pytest.raises(ValueError):
        engage_qualification_action(episode, behavior="NO_ACTION")  # type: ignore[arg-type]


def test_f4_memory_module_has_no_operational_execution_surface() -> None:
    source = inspect.getsource(memory_module)
    forbidden = (
        "MetaTrader5",
        "order_send",
        "create_order",
        "submit_order",
        "lot_size",
        "position_size",
        "stop_loss",
        "take_profit",
        "run_backtest",
        "activate_live",
        "requests.",
        "urllib.request",
        ".bi5",
    )
    assert all(token not in source for token in forbidden)


def test_f5_p14_attestation_is_not_operational_permission() -> None:
    *_, episode = coherent_episode()
    assert is_factory_attested_memory_episode(episode)
    assert not hasattr(memory_module, "AUTHORIZED")
    assert not hasattr(memory_module, "execute")


# G — Serialization/durability/completeness stay outside this local qualification.


def test_g0_serialized_episode_fields_are_not_authority() -> None:
    *_, episode = coherent_episode()
    assert not is_factory_attested_memory_episode(asdict(episode))


def test_g1_reconstructed_same_valued_episode_is_not_reattested() -> None:
    *_, episode = coherent_episode()
    rebuilt = manual_episode_from(episode)
    assert rebuilt == episode and rebuilt is not episode
    assert not is_factory_attested_memory_episode(rebuilt)


def test_g2_duplicate_same_episode_has_same_identity_not_independence_claim() -> None:
    *prefix, action, result, trace, first = coherent_episode()
    second = produce_observational_memory_episode(trace, action, result)
    assert first.episode_id == second.episode_id
    assert not hasattr(first, "independent")
    assert not hasattr(second, "independent")


def test_g3_episode_cannot_claim_memory_exhaustive_or_unbiased() -> None:
    *_, action, result, trace, episode = coherent_episode(outcome="SUCCESS")
    for name in ("exhaustive", "unbiased", "survivorship_safe"):
        assert not hasattr(episode, name)
    with pytest.raises(TypeError):
        produce_observational_memory_episode(  # type: ignore[call-arg]
            trace,
            action,
            result,
            exhaustive=True,
        )


def test_g4_later_rewrite_of_original_observation_invalidates_attestation() -> None:
    *_, episode = coherent_episode()
    object.__setattr__(episode, "behavior", "REINTERPRETED_AFTERWARD")
    assert not is_factory_attested_memory_episode(episode)

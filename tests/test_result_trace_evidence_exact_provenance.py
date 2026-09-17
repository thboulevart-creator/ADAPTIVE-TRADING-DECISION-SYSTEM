import gc
import weakref

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import (
    is_decision_bound_to_exact_research_evidence,
    is_factory_attested_decision,
    produce_decision,
)
from src.decision_trace import is_factory_attested_decision_trace, produce_decision_trace
from src.research_run_evidence import is_factory_attested
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_chain():
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision="HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome="OBSERVED")
    return evidence, context, decision, action, result


def test_g0_invalidated_exact_research_origin_cannot_produce_trace() -> None:
    evidence, _, decision, action, result = coherent_chain()
    assert is_decision_bound_to_exact_research_evidence(decision, evidence)

    object.__setattr__(evidence, "code_version", "mutated-after-decision")
    assert not is_factory_attested(evidence)
    assert is_factory_attested_decision(decision)
    assert not is_decision_bound_to_exact_research_evidence(decision, evidence)

    with pytest.raises(ValueError):
        produce_decision_trace(evidence, decision, action, result)


def test_g1_same_valued_replacement_cannot_replace_collected_exact_origin() -> None:
    evidence, _, decision, action, result = coherent_chain()
    original_values = (
        evidence.research_run_id,
        evidence.context_id,
        evidence.provenance_id,
        evidence.code_version,
        evidence.configuration_version,
        evidence.dataset_id,
        evidence.dataset_version,
    )
    evidence_ref = weakref.ref(evidence)

    del evidence
    gc.collect()
    assert evidence_ref() is None
    assert is_factory_attested_decision(decision)

    replacement, _ = coherent_runtime_inputs()
    replacement_values = (
        replacement.research_run_id,
        replacement.context_id,
        replacement.provenance_id,
        replacement.code_version,
        replacement.configuration_version,
        replacement.dataset_id,
        replacement.dataset_version,
    )
    assert replacement_values == original_values
    assert is_factory_attested(replacement)
    assert not is_decision_bound_to_exact_research_evidence(decision, replacement)

    with pytest.raises(ValueError):
        produce_decision_trace(replacement, decision, action, result)


def test_g2_exact_origin_helper_distinguishes_same_valued_authentic_evidence() -> None:
    evidence_a, context = coherent_runtime_inputs()
    evidence_b, _ = coherent_runtime_inputs()
    assert evidence_a is not evidence_b
    assert evidence_a == evidence_b
    assert is_factory_attested(evidence_a)
    assert is_factory_attested(evidence_b)

    decision = produce_decision(evidence_a, context=context, decision="HOLD")
    assert is_decision_bound_to_exact_research_evidence(decision, evidence_a)
    assert not is_decision_bound_to_exact_research_evidence(decision, evidence_b)


def _produce_trace_then_release_upstream():
    evidence, context, decision, action, result = coherent_chain()
    trace = produce_decision_trace(evidence, decision, action, result)
    references = (
        weakref.ref(evidence),
        weakref.ref(context),
        weakref.ref(decision),
        weakref.ref(action),
        weakref.ref(result),
    )
    return trace, references


def test_g3_attested_trace_remains_downstream_snapshot_after_upstream_collection() -> None:
    trace, references = _produce_trace_then_release_upstream()
    gc.collect()

    assert all(reference() is None for reference in references)
    assert trace.validate() == ("PASS", ())
    assert is_factory_attested_decision_trace(trace)


def test_g4_upstream_mutation_after_trace_does_not_rewrite_trace_snapshot() -> None:
    evidence, _, decision, action, result = coherent_chain()
    trace = produce_decision_trace(evidence, decision, action, result)
    snapshot = trace.reconstruction_chain()

    object.__setattr__(evidence, "code_version", "post-trace-mutation")
    object.__setattr__(decision, "decision", "POST_TRACE_MUTATION")
    object.__setattr__(action, "behavior", "POST_TRACE_MUTATION")
    object.__setattr__(result, "outcome", "POST_TRACE_MUTATION")

    assert trace.reconstruction_chain() == snapshot
    assert is_factory_attested_decision_trace(trace)


def test_g5_decision_can_remain_attested_while_exact_research_origin_is_unavailable() -> None:
    evidence, _, decision, action, result = coherent_chain()
    evidence_ref = weakref.ref(evidence)
    del evidence
    gc.collect()

    assert evidence_ref() is None
    assert is_factory_attested_decision(decision)
    replacement, _ = coherent_runtime_inputs()
    assert replacement.research_run_id == decision.research_run_id
    assert replacement.context_id == decision.context_id
    assert not is_decision_bound_to_exact_research_evidence(decision, replacement)
    with pytest.raises(ValueError):
        produce_decision_trace(replacement, decision, action, result)

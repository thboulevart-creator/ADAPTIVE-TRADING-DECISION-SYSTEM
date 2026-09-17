import gc
import subprocess
import sys
import weakref

import pytest

from src.action_result_evidence import (
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_observation_pair,
)
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.memory_episode import (
    is_factory_attested_memory_episode,
    produce_observational_memory_episode,
)
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_objects(*, decision_payload="HOLD", behavior="NO_ACTION", outcome="OBSERVED"):
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision=decision_payload)
    action = engage_qualification_action(decision, behavior=behavior)
    result = observe_qualification_result(action, outcome=outcome)
    trace = produce_decision_trace(evidence, decision, action, result)
    episode = produce_observational_memory_episode(trace, action, result)
    return evidence, context, decision, action, result, trace, episode


# H — exact provenance, lifetime, duplication, and verifier abuse second breaker.


def test_h0_duplicate_exact_trace_snapshots_share_episode_identity_without_independence_claim() -> None:
    evidence, _, decision, action, result, trace_a, episode_a = coherent_objects()
    trace_b = produce_decision_trace(evidence, decision, action, result)
    assert trace_b is not trace_a
    assert trace_b == trace_a

    episode_b = produce_observational_memory_episode(trace_b, action, result)
    assert episode_b is not episode_a
    assert episode_b == episode_a
    assert episode_b.episode_id == episode_a.episode_id
    assert is_factory_attested_memory_episode(episode_a)
    assert is_factory_attested_memory_episode(episode_b)
    assert not hasattr(episode_a, "independent_evidence")
    assert not hasattr(episode_b, "independent_evidence")


def test_h1_completed_episode_remains_attested_after_all_upstream_objects_are_collected() -> None:
    evidence, context, decision, action, result, trace, episode = coherent_objects()
    expected = (episode.behavior, episode.outcome, episode.action_id, episode.result_id)
    refs = [weakref.ref(value) for value in (decision, action, result, trace)]

    del evidence, context, decision, action, result, trace
    gc.collect()

    assert all(reference() is None for reference in refs)
    assert is_factory_attested_memory_episode(episode)
    assert (episode.behavior, episode.outcome, episode.action_id, episode.result_id) == expected


def test_h2_mutating_upstream_after_episode_creation_cannot_rewrite_or_invalidate_snapshot() -> None:
    _, _, _, action, result, trace, episode = coherent_objects()
    expected = (
        episode.decision_id,
        episode.action_id,
        episode.behavior,
        episode.result_id,
        episode.outcome,
    )

    object.__setattr__(trace, "decision", "REWRITTEN-UPSTREAM")
    object.__setattr__(action, "behavior", "REWRITTEN-UPSTREAM")
    object.__setattr__(result, "outcome", "REWRITTEN-UPSTREAM")

    assert is_factory_attested_memory_episode(episode)
    assert (
        episode.decision_id,
        episode.action_id,
        episode.behavior,
        episode.result_id,
        episode.outcome,
    ) == expected


def test_h3_new_pair_verifier_is_read_only_and_rejects_non_evidence_surfaces() -> None:
    _, _, _, action, result, trace, episode = coherent_objects()
    assert verify_qualification_observation_pair(action, result)
    assert not verify_qualification_observation_pair(trace, result)
    assert not verify_qualification_observation_pair(action, trace)
    assert not verify_qualification_observation_pair(episode, result)
    assert not verify_qualification_observation_pair(action, episode)
    assert not verify_qualification_observation_pair(action.action_id, result.result_id)


def test_h4_pair_verifier_rejects_cross_action_authentic_result() -> None:
    _, _, decision, action_a, result_a, _, _ = coherent_objects()
    action_b = engage_qualification_action(decision, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")

    assert verify_qualification_observation_pair(action_a, result_a)
    assert verify_qualification_observation_pair(action_b, result_b)
    assert not verify_qualification_observation_pair(action_a, result_b)
    assert not verify_qualification_observation_pair(action_b, result_a)


def test_h5_pair_verifier_fails_if_action_origin_decision_is_collected() -> None:
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision="HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome="OBSERVED")
    decision_ref = weakref.ref(decision)

    del decision
    gc.collect()

    assert decision_ref() is None
    assert not verify_qualification_observation_pair(action, result)


def test_h6_pair_verifier_fails_if_action_origin_decision_is_mutated() -> None:
    evidence, context = coherent_runtime_inputs()
    decision = produce_decision(evidence, context=context, decision="HOLD")
    action = engage_qualification_action(decision, behavior="NO_ACTION")
    result = observe_qualification_result(action, outcome="OBSERVED")
    assert verify_qualification_observation_pair(action, result)

    object.__setattr__(decision, "decision", "MUTATED")
    assert not verify_qualification_observation_pair(action, result)


def test_h7_same_valued_authentic_decisions_do_not_make_their_actions_cross_admissible() -> None:
    evidence, context = coherent_runtime_inputs()
    decision_a = produce_decision(evidence, context=context, decision="HOLD")
    decision_b = produce_decision(evidence, context=context, decision="HOLD")
    assert decision_a is not decision_b
    assert decision_a == decision_b

    action_a = engage_qualification_action(decision_a, behavior="NO_ACTION")
    result_a = observe_qualification_result(action_a, outcome="OBSERVED")
    action_b = engage_qualification_action(decision_b, behavior="NO_ACTION")
    result_b = observe_qualification_result(action_b, outcome="OBSERVED")

    assert action_a.action_id != action_b.action_id
    assert result_a.result_id != result_b.result_id
    assert not verify_qualification_observation_pair(action_a, result_b)
    assert not verify_qualification_observation_pair(action_b, result_a)


def test_h8_reinitialized_p12_registry_cannot_rebind_old_trace_to_new_authentic_same_id_pair() -> None:
    # Module reloads deliberately model a fresh P1.2 producer lifecycle. They
    # must run outside this pytest interpreter or they replace module class
    # identities/registries already imported by other collected test modules.
    script = r'''
import importlib

import src.action_result_evidence as action_result_module
import src.memory_episode as memory_module
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from tests.research_runtime_fixture import coherent_runtime_inputs

ar_first = importlib.reload(action_result_module)
importlib.reload(memory_module)

evidence, context = coherent_runtime_inputs()
decision = produce_decision(evidence, context=context, decision="HOLD")
action_a = ar_first.engage_qualification_action(decision, behavior="NO_ACTION")
result_a = ar_first.observe_qualification_result(action_a, outcome="OBSERVED")
trace_a = produce_decision_trace(evidence, decision, action_a, result_a)

ar_second = importlib.reload(action_result_module)
mem_second = importlib.reload(memory_module)
action_b = ar_second.engage_qualification_action(decision, behavior="NO_ACTION")
result_b = ar_second.observe_qualification_result(action_b, outcome="OBSERVED")

assert action_b is not action_a
assert result_b is not result_a
assert action_b.action_id == action_a.action_id == trace_a.action_id
assert result_b.result_id == result_a.result_id == trace_a.result_id
assert ar_second.verify_qualification_observation_pair(action_b, result_b)

try:
    mem_second.produce_observational_memory_episode(trace_a, action_b, result_b)
except ValueError:
    pass
else:
    raise AssertionError("old Trace rebound to new authentic same-ID pair")
'''
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

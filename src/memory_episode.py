"""P1.4 qualification-only TRACE -> observational MEMORY episode boundary.

The episode is a local immutable snapshot of already-qualified observation
facts. It does not attach ResearchFindings, infer causality, promote knowledge,
persist authority, or authorize operational behavior.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass

from src.action_result_evidence import (
    QualificationActionEvidence,
    QualificationResultObservation,
    verify_qualification_observation_pair,
)
from src.decision_trace import (
    DecisionTrace,
    is_factory_attested_decision_trace,
    is_trace_bound_to_exact_observation_pair,
)


CONTRACT = "P1_4_TRACE_MEMORY_EPISODE_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ObservationalMemoryEpisode:
    episode_id: str
    decision_id: str
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    context_id: str
    decision: str
    action_id: str
    behavior: str
    result_id: str
    outcome: str


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _episode_content(value: ObservationalMemoryEpisode) -> dict[str, str]:
    return {
        "decision_id": value.decision_id,
        "provenance_id": value.provenance_id,
        "research_run_id": value.research_run_id,
        "code_version": value.code_version,
        "configuration_version": value.configuration_version,
        "dataset_id": value.dataset_id,
        "dataset_version": value.dataset_version,
        "context_id": value.context_id,
        "decision": value.decision,
        "action_id": value.action_id,
        "behavior": value.behavior,
        "result_id": value.result_id,
        "outcome": value.outcome,
    }


def _episode_id_from_content(content: dict[str, str]) -> str:
    return "MEP-" + _stable_hash({"contract": CONTRACT, "content": content})[:32]


def _episode_fingerprint(value: ObservationalMemoryEpisode) -> str:
    return _stable_hash(
        {
            "episode_id": value.episode_id,
            "contract": CONTRACT,
            "content": _episode_content(value),
        }
    )


def _build_memory_episode_api():
    registry: dict[int, tuple[weakref.ReferenceType[ObservationalMemoryEpisode], str]] = {}

    def produce(
        trace: object,
        action: object,
        result: object,
    ) -> ObservationalMemoryEpisode:
        """Produce one local observational episode from exact qualified inputs."""
        if not isinstance(trace, DecisionTrace):
            raise ValueError("P1.4 MemoryEpisode requires full DecisionTrace")
        if not is_factory_attested_decision_trace(trace):
            raise ValueError("P1.4 MemoryEpisode requires factory-attested DecisionTrace")
        if not isinstance(action, QualificationActionEvidence):
            raise ValueError("P1.4 MemoryEpisode requires full QualificationActionEvidence")
        if not isinstance(result, QualificationResultObservation):
            raise ValueError("P1.4 MemoryEpisode requires full QualificationResultObservation")
        if not verify_qualification_observation_pair(action, result):
            raise ValueError("P1.4 MemoryEpisode requires exact admissible Action -> Result pair")
        if not is_trace_bound_to_exact_observation_pair(trace, action, result):
            raise ValueError("P1.4 MemoryEpisode requires exact Trace -> Action/Result provenance")
        if trace.decision_id != action.decision_id:
            raise ValueError("P1.4 MemoryEpisode decision mismatch")
        if trace.action_id != action.action_id:
            raise ValueError("P1.4 MemoryEpisode action mismatch")
        if trace.result_id != result.result_id:
            raise ValueError("P1.4 MemoryEpisode result mismatch")
        if result.action_id != action.action_id:
            raise ValueError("P1.4 MemoryEpisode Action -> Result mismatch")

        content = {
            "decision_id": trace.decision_id,
            "provenance_id": trace.provenance_id,
            "research_run_id": trace.research_run_id,
            "code_version": trace.code_version,
            "configuration_version": trace.configuration_version,
            "dataset_id": trace.dataset_id,
            "dataset_version": trace.dataset_version,
            "context_id": trace.context_id,
            "decision": trace.decision,
            "action_id": action.action_id,
            "behavior": action.behavior,
            "result_id": result.result_id,
            "outcome": result.outcome,
        }
        produced = ObservationalMemoryEpisode(
            episode_id=_episode_id_from_content(content),
            **content,
        )
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _episode_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, ObservationalMemoryEpisode):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            return False
        if _episode_fingerprint(value) != expected_fingerprint:
            return False
        return value.episode_id == _episode_id_from_content(_episode_content(value))

    return produce, verify


produce_observational_memory_episode, is_factory_attested_memory_episode = _build_memory_episode_api()
del _build_memory_episode_api

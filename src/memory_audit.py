"""P1.6 qualification-only historical MEMORY collection audit.

This module audits collection integrity and contestability for exact P1.5
HistoricalMemoryEpisode objects. It does not validate hypotheses, infer
causality, promote knowledge, recommend rules, revise behavior, or authorize
operations.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass

from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    is_factory_attested_historical_memory,
)


CONTRACT = "P1_6_MEMORY_COLLECTION_AUDIT_BOUNDARY_V1"

_ALLOWED_CONTEXT_FIELDS = frozenset(
    {
        "provenance_id",
        "research_run_id",
        "code_version",
        "configuration_version",
        "dataset_id",
        "dataset_version",
        "context_id",
        "decision",
        "behavior",
    }
)


@dataclass(frozen=True, slots=True)
class AuditScope:
    scope_id: str
    question: str
    expected_registration_ids: tuple[str, ...] | None
    context_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class MemoryCollectionAuditAssessment:
    audit_id: str
    scope_id: str
    verdict: str
    completeness_status: str
    independence_status: str
    examined_registration_ids: tuple[str, ...]
    missing_registration_ids: tuple[str, ...]
    unexpected_registration_ids: tuple[str, ...]
    duplicate_registration_ids: tuple[str, ...]
    unique_episode_ids: tuple[str, ...]
    content_groups: tuple[tuple[str, tuple[str, ...]], ...]
    context_groups: tuple[
        tuple[tuple[tuple[str, str], ...], tuple[str, ...]],
        ...,
    ]
    contradiction_groups: tuple[tuple[str, ...], ...]
    anomalies: tuple[str, ...]


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _scope_content(
    *,
    question: str,
    expected_registration_ids: tuple[str, ...] | None,
    context_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "contract": CONTRACT,
        "question": question,
        "expected_registration_ids": expected_registration_ids,
        "context_fields": context_fields,
    }


def _scope_id(
    *,
    question: str,
    expected_registration_ids: tuple[str, ...] | None,
    context_fields: tuple[str, ...],
) -> str:
    return "MAS-" + _stable_hash(
        _scope_content(
            question=question,
            expected_registration_ids=expected_registration_ids,
            context_fields=context_fields,
        )
    )[:32]


def _validate_registration_ids(value: object) -> tuple[str, ...] | None:
    if value is None:
        return None
    if not isinstance(value, tuple):
        raise TypeError("P1.6 expected_registration_ids must be tuple[str, ...] or None")
    if not value:
        raise ValueError("P1.6 bounded expected_registration_ids must not be empty")
    if any(not isinstance(item, str) or not item for item in value):
        raise ValueError("P1.6 expected registration IDs must be non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError("P1.6 expected registration IDs must be unique")
    return tuple(sorted(value))


def _validate_context_fields(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise TypeError("P1.6 context_fields must be tuple[str, ...]")
    if not value:
        raise ValueError("P1.6 context_fields must not be empty")
    if any(not isinstance(field, str) or not field for field in value):
        raise ValueError("P1.6 context fields must be non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError("P1.6 context fields must be unique")
    forbidden = tuple(field for field in value if field not in _ALLOWED_CONTEXT_FIELDS)
    if forbidden:
        raise ValueError(f"P1.6 forbidden or unknown context fields: {forbidden}")
    return value


def create_audit_scope(
    *,
    question: object,
    expected_registration_ids: object,
    context_fields: object,
) -> AuditScope:
    """Create an immutable external audit declaration; never infer it from memories."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("P1.6 audit question must be non-empty")
    expected = _validate_registration_ids(expected_registration_ids)
    fields = _validate_context_fields(context_fields)
    return AuditScope(
        scope_id=_scope_id(
            question=question,
            expected_registration_ids=expected,
            context_fields=fields,
        ),
        question=question,
        expected_registration_ids=expected,
        context_fields=fields,
    )


def _validate_scope(scope: object) -> AuditScope:
    if not isinstance(scope, AuditScope):
        raise TypeError("P1.6 requires AuditScope separately from collection")
    if not isinstance(scope.question, str) or not scope.question.strip():
        raise ValueError("P1.6 audit question must be non-empty")
    expected = _validate_registration_ids(scope.expected_registration_ids)
    fields = _validate_context_fields(scope.context_fields)
    expected_id = _scope_id(
        question=scope.question,
        expected_registration_ids=expected,
        context_fields=fields,
    )
    if scope.scope_id != expected_id:
        raise ValueError("P1.6 AuditScope identity mismatch")
    if scope.expected_registration_ids != expected:
        raise ValueError("P1.6 AuditScope expected registration order is not canonical")
    if scope.context_fields != fields:
        raise ValueError("P1.6 AuditScope context fields mismatch")
    return scope


def _context_key(memory: HistoricalMemoryEpisode, fields: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    episode = memory.episode
    return tuple((field, getattr(episode, field)) for field in fields)


def _assessment_content(
    *,
    scope_id: str,
    verdict: str,
    completeness_status: str,
    independence_status: str,
    examined_registration_ids: tuple[str, ...],
    missing_registration_ids: tuple[str, ...],
    unexpected_registration_ids: tuple[str, ...],
    duplicate_registration_ids: tuple[str, ...],
    unique_episode_ids: tuple[str, ...],
    content_groups: tuple[tuple[str, tuple[str, ...]], ...],
    context_groups: tuple[tuple[tuple[tuple[str, str], ...], tuple[str, ...]], ...],
    contradiction_groups: tuple[tuple[str, ...], ...],
    anomalies: tuple[str, ...],
) -> dict[str, object]:
    return {
        "scope_id": scope_id,
        "verdict": verdict,
        "completeness_status": completeness_status,
        "independence_status": independence_status,
        "examined_registration_ids": examined_registration_ids,
        "missing_registration_ids": missing_registration_ids,
        "unexpected_registration_ids": unexpected_registration_ids,
        "duplicate_registration_ids": duplicate_registration_ids,
        "unique_episode_ids": unique_episode_ids,
        "content_groups": content_groups,
        "context_groups": context_groups,
        "contradiction_groups": contradiction_groups,
        "anomalies": anomalies,
    }


def _audit_id(**content: object) -> str:
    return "MAU-" + _stable_hash({"contract": CONTRACT, "assessment": content})[:32]


def _assessment_fingerprint(value: MemoryCollectionAuditAssessment) -> str:
    return _stable_hash(
        {
            "contract": CONTRACT,
            "assessment": asdict(value),
        }
    )


def _build_assessment_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[MemoryCollectionAuditAssessment], str],
    ] = {}

    def attest(**values: object) -> MemoryCollectionAuditAssessment:
        produced = MemoryCollectionAuditAssessment(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _assessment_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, MemoryCollectionAuditAssessment):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        return reference() is value and _assessment_fingerprint(value) == expected_fingerprint

    return attest, verify


_attest_assessment, is_factory_attested_memory_collection_audit = _build_assessment_attestation_api()
del _build_assessment_attestation_api


def audit_memory_collection(scope: object, memories: object) -> MemoryCollectionAuditAssessment:
    """Audit P1.5 collection membership/grouping without epistemic promotion."""
    validated_scope = _validate_scope(scope)
    if not isinstance(memories, tuple):
        raise TypeError("P1.6 memories must be tuple[HistoricalMemoryEpisode, ...]")
    if not memories:
        raise ValueError("P1.6 requires at least one historical memory")

    for memory in memories:
        if not isinstance(memory, HistoricalMemoryEpisode):
            raise TypeError("P1.6 collection requires full HistoricalMemoryEpisode members")
        if not is_factory_attested_historical_memory(memory):
            raise ValueError("P1.6 collection requires exact currently-attested P1.5 members")

    counts = Counter(memory.registration_id for memory in memories)
    duplicate_registration_ids = tuple(sorted(reg for reg, count in counts.items() if count > 1))

    unique_by_registration: dict[str, HistoricalMemoryEpisode] = {}
    for memory in memories:
        unique_by_registration.setdefault(memory.registration_id, memory)

    examined_registration_ids = tuple(sorted(unique_by_registration))
    unique_memories = tuple(unique_by_registration[reg] for reg in examined_registration_ids)

    content_map: dict[str, list[str]] = defaultdict(list)
    context_map: dict[tuple[tuple[str, str], ...], list[str]] = defaultdict(list)
    for memory in unique_memories:
        content_map[memory.episode.episode_id].append(memory.registration_id)
        context_map[_context_key(memory, validated_scope.context_fields)].append(memory.registration_id)

    content_groups = tuple(
        (episode_id, tuple(sorted(registrations)))
        for episode_id, registrations in sorted(content_map.items())
    )
    unique_episode_ids = tuple(episode_id for episode_id, _ in content_groups)

    context_groups = tuple(
        (key, tuple(sorted(registrations)))
        for key, registrations in sorted(context_map.items(), key=lambda item: item[0])
    )

    contradiction_groups_list: list[tuple[str, ...]] = []
    for _context, registrations in context_groups:
        subgroup: dict[tuple[str, str], list[HistoricalMemoryEpisode]] = defaultdict(list)
        for registration_id in registrations:
            memory = unique_by_registration[registration_id]
            subgroup[(memory.episode.decision, memory.episode.behavior)].append(memory)
        for members in subgroup.values():
            outcomes = {member.episode.outcome for member in members}
            if len(outcomes) > 1:
                contradiction_groups_list.append(
                    tuple(sorted(member.registration_id for member in members))
                )
    contradiction_groups = tuple(sorted(set(contradiction_groups_list)))

    if validated_scope.expected_registration_ids is None:
        missing_registration_ids: tuple[str, ...] = ()
        unexpected_registration_ids: tuple[str, ...] = ()
        completeness_status = "BLOCKED"
    else:
        expected = set(validated_scope.expected_registration_ids)
        examined = set(examined_registration_ids)
        missing_registration_ids = tuple(sorted(expected - examined))
        unexpected_registration_ids = tuple(sorted(examined - expected))
        completeness_status = (
            "FAIL"
            if missing_registration_ids or unexpected_registration_ids
            else "PASS"
        )

    independence_status = "BLOCKED"

    anomalies_list: list[str] = []
    anomalies_list.extend(f"DUPLICATE_REGISTRATION:{reg}" for reg in duplicate_registration_ids)
    anomalies_list.extend(f"MISSING_REGISTRATION:{reg}" for reg in missing_registration_ids)
    anomalies_list.extend(f"UNEXPECTED_REGISTRATION:{reg}" for reg in unexpected_registration_ids)
    anomalies_list.extend(
        "CONTRADICTION:" + ",".join(group)
        for group in contradiction_groups
    )
    if completeness_status == "BLOCKED":
        anomalies_list.append("COMPLETENESS_BLOCKED")
    anomalies_list.append("INDEPENDENCE_BLOCKED")
    anomalies = tuple(sorted(anomalies_list))

    if duplicate_registration_ids or completeness_status == "FAIL":
        verdict = "FAIL"
    elif completeness_status == "BLOCKED":
        verdict = "BLOCKED"
    else:
        verdict = "PASS"

    content = _assessment_content(
        scope_id=validated_scope.scope_id,
        verdict=verdict,
        completeness_status=completeness_status,
        independence_status=independence_status,
        examined_registration_ids=examined_registration_ids,
        missing_registration_ids=missing_registration_ids,
        unexpected_registration_ids=unexpected_registration_ids,
        duplicate_registration_ids=duplicate_registration_ids,
        unique_episode_ids=unique_episode_ids,
        content_groups=content_groups,
        context_groups=context_groups,
        contradiction_groups=contradiction_groups,
        anomalies=anomalies,
    )
    return _attest_assessment(
        audit_id=_audit_id(**content),
        **content,
    )

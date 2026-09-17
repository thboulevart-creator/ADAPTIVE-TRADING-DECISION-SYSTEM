"""Minimal producer contract for DECISION.

A Decision is produced only from the actual RESEARCH output and the actual
CONTEXT that was used to obtain it. This module deliberately does not invent
trading logic: the decision payload must come from the future decision policy.

P1.1 additionally makes a producer-created Decision downstream-authenticatable
without exposing a raw attestation/minter capability. ACTION/RESULT/TRACE remain
downstream and are intentionally absent.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass

from src.context import Context
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested


@dataclass(frozen=True, slots=True, weakref_slot=True)
class Decision:
    """A decision anchored to one concrete research run and context."""

    decision_id: str
    research_run_id: str
    context_id: str
    decision: str


def _decision_id(research_run_id: str, context_id: str, decision: str) -> str:
    payload = json.dumps(
        {
            "research_run_id": research_run_id,
            "context_id": context_id,
            "decision": decision,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "DEC-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _decision_identity_fingerprint(value: Decision) -> str:
    payload = json.dumps(
        {
            "decision_id": value.decision_id,
            "research_run_id": value.research_run_id,
            "context_id": value.context_id,
            "decision": value.decision,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_decision_api():
    registry: dict[int, tuple[weakref.ReferenceType[Decision], str]] = {}

    def produce(
        evidence: ResearchRunEvidence | None,
        *,
        context: Context | None,
        decision: str,
    ) -> Decision:
        """Produce a decision only from coherent upstream RESEARCH evidence."""
        if evidence is None:
            raise ValueError("RESEARCH -> DECISION requires ResearchRunEvidence")
        if not isinstance(evidence, ResearchRunEvidence):
            raise ValueError("RESEARCH -> DECISION requires the full ResearchRunEvidence object")
        if context is None:
            raise ValueError("RESEARCH -> DECISION requires a Context")
        if not isinstance(context, Context):
            raise ValueError("RESEARCH -> DECISION requires the full Context object")
        if not is_factory_attested(evidence):
            raise ValueError(
                "RESEARCH -> DECISION requires factory-attested, identity-bound ResearchRunEvidence"
            )
        if evidence.context_id != context.context_id:
            raise ValueError("RESEARCH -> DECISION context mismatch")
        if evidence.configuration_version != context.configuration_version:
            raise ValueError("RESEARCH -> DECISION configuration mismatch")
        if evidence.dataset_id != context.dataset_id:
            raise ValueError("RESEARCH -> DECISION dataset mismatch")
        if evidence.dataset_version != context.dataset_version:
            raise ValueError("RESEARCH -> DECISION dataset version mismatch")
        if not evidence.provenance_id.strip():
            raise ValueError("RESEARCH -> DECISION requires provenance_id")
        if not evidence.research_run_id.strip():
            raise ValueError("RESEARCH -> DECISION requires research_run_id")
        if not evidence.code_version.strip():
            raise ValueError("RESEARCH -> DECISION requires code_version")
        if not decision.strip():
            raise ValueError("RESEARCH -> DECISION requires a non-empty decision")

        produced = Decision(
            decision_id=_decision_id(evidence.research_run_id, context.context_id, decision),
            research_run_id=evidence.research_run_id,
            context_id=context.context_id,
            decision=decision,
        )
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _decision_identity_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, Decision):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            return False
        if _decision_identity_fingerprint(value) != expected_fingerprint:
            return False
        return value.decision_id == _decision_id(
            value.research_run_id,
            value.context_id,
            value.decision,
        )

    return produce, verify


produce_decision, is_factory_attested_decision = _build_decision_api()
del _build_decision_api

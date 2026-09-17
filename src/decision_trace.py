"""Minimal, evidence-oriented reconstruction of a completed decision.

This module does not create a decision engine or a provenance registry. It only
makes the minimum reconstruction chain explicit and executable:

provenance -> research run -> code -> configuration -> dataset -> context
-> decision -> action -> result

A missing link is a FAIL, never an implicit PASS.

P1.3 adds a qualification-only producer for DecisionTrace. Structural
``DecisionTrace.validate()`` remains a legacy completeness check and is not an
authenticity or provenance authority.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass
from typing import Literal


Status = Literal["PASS", "FAIL", "BLOCKED"]
CONTRACT = "P1_3_RESULT_TRACE_EVIDENCE_BOUNDARY_V1"


@dataclass(frozen=True)
class DecisionTrace:
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
    result_id: str

    def missing_links(self) -> tuple[str, ...]:
        """Return required reconstruction links that are absent."""
        fields = (
            "provenance_id",
            "research_run_id",
            "code_version",
            "configuration_version",
            "dataset_id",
            "dataset_version",
            "context_id",
            "decision",
            "action_id",
            "result_id",
        )
        return tuple(field for field in fields if not getattr(self, field).strip())

    def validate(self) -> tuple[Status, tuple[str, ...]]:
        """Validate only structural completeness of the reconstruction chain."""
        missing = self.missing_links()
        if missing:
            return "FAIL", missing
        return "PASS", ()

    def reconstruction_chain(self) -> tuple[str, ...]:
        """Return the ordered identifiers needed to reconstruct the decision."""
        status, missing = self.validate()
        if status != "PASS":
            raise ValueError(f"decision trace is incomplete: {', '.join(missing)}")
        return (
            self.provenance_id,
            self.research_run_id,
            self.code_version,
            self.configuration_version,
            self.dataset_id,
            self.dataset_version,
            self.context_id,
            self.decision_id,
            self.action_id,
            self.result_id,
        )


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _trace_fingerprint(value: DecisionTrace) -> str:
    return _stable_hash(
        {
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
            "result_id": value.result_id,
        }
    )


def _build_trace_api():
    registry: dict[
        int,
        tuple[
            weakref.ReferenceType[DecisionTrace],
            str,
            weakref.ReferenceType[object],
            weakref.ReferenceType[object],
        ],
    ] = {}

    def produce(
        evidence: object,
        decision: object,
        action: object,
        result: object,
    ) -> DecisionTrace:
        """Produce one qualification-only Trace from already qualified evidence."""
        # Local imports avoid a module cycle because research_run_evidence keeps
        # a legacy adapter that imports DecisionTrace.
        from src.action_result_evidence import (
            QualificationActionEvidence,
            QualificationResultObservation,
            verify_qualification_chain,
        )
        from src.decision import (
            Decision,
            is_decision_bound_to_exact_research_evidence,
            is_factory_attested_decision,
        )
        from src.research_run_evidence import ResearchRunEvidence, is_factory_attested

        if not isinstance(evidence, ResearchRunEvidence):
            raise ValueError("P1.3 Trace requires full ResearchRunEvidence")
        if not is_factory_attested(evidence):
            raise ValueError("P1.3 Trace requires factory-attested ResearchRunEvidence")
        if not isinstance(decision, Decision):
            raise ValueError("P1.3 Trace requires full Decision")
        if not is_factory_attested_decision(decision):
            raise ValueError("P1.3 Trace requires factory-attested Decision")
        if not is_decision_bound_to_exact_research_evidence(decision, evidence):
            raise ValueError("P1.3 Trace requires exact ResearchRunEvidence -> Decision provenance")
        if not isinstance(action, QualificationActionEvidence):
            raise ValueError("P1.3 Trace requires full QualificationActionEvidence")
        if not isinstance(result, QualificationResultObservation):
            raise ValueError("P1.3 Trace requires full QualificationResultObservation")
        if not verify_qualification_chain(decision, action, result):
            raise ValueError("P1.3 Trace requires exact qualified Decision -> Action -> Result chain")
        if evidence.research_run_id != decision.research_run_id:
            raise ValueError("P1.3 Trace research_run mismatch")
        if evidence.context_id != decision.context_id:
            raise ValueError("P1.3 Trace context mismatch")

        produced = DecisionTrace(
            decision_id=decision.decision_id,
            provenance_id=evidence.provenance_id,
            research_run_id=evidence.research_run_id,
            code_version=evidence.code_version,
            configuration_version=evidence.configuration_version,
            dataset_id=evidence.dataset_id,
            dataset_version=evidence.dataset_version,
            context_id=evidence.context_id,
            decision=decision.decision,
            action_id=action.action_id,
            result_id=result.result_id,
        )
        status, missing = produced.validate()
        if status != "PASS":
            raise ValueError(f"P1.3 produced incomplete Trace: {', '.join(missing)}")

        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (
            reference,
            _trace_fingerprint(produced),
            weakref.ref(action),
            weakref.ref(result),
        )
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, DecisionTrace):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint, _, _ = entry
        if reference() is not value:
            return False
        if _trace_fingerprint(value) != expected_fingerprint:
            return False
        return value.validate()[0] == "PASS"

    def verify_exact_observation_pair(trace: object, action: object, result: object) -> bool:
        """Verify that this Trace was produced from these exact Action/Result objects."""
        if not verify(trace):
            return False
        assert isinstance(trace, DecisionTrace)
        entry = registry.get(id(trace))
        if entry is None:
            return False
        reference, _, origin_action_reference, origin_result_reference = entry
        if reference() is not trace:
            return False
        return origin_action_reference() is action and origin_result_reference() is result

    return produce, verify, verify_exact_observation_pair


(
    produce_decision_trace,
    is_factory_attested_decision_trace,
    is_trace_bound_to_exact_observation_pair,
) = _build_trace_api()
del _build_trace_api

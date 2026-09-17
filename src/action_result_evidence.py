"""P1.2 qualification-only ACTION -> RESULT evidence boundary.

This module deliberately does not create operational ACTION. It provides only a
local, synthetic, side-effect-free qualification surface that can demonstrate
identity-bound ActionEvidence and ResultObservation objects downstream of an
already qualified Decision.

It does not import DecisionTrace and does not open broker, order, sizing,
acquisition, backtest or live capabilities.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import weakref
from dataclasses import dataclass

from src.decision import Decision, is_factory_attested_decision


CONTRACT = "P1_2_ACTION_RESULT_EVIDENCE_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualificationActionEvidence:
    """Qualification-only evidence that one synthetic behavior was engaged."""

    action_id: str
    decision_id: str
    behavior: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualificationResultObservation:
    """Qualification-only observation bound to one exact ActionEvidence."""

    result_id: str
    action_id: str
    outcome: str


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _action_fingerprint(value: QualificationActionEvidence) -> str:
    return _stable_hash(
        {
            "action_id": value.action_id,
            "decision_id": value.decision_id,
            "behavior": value.behavior,
        }
    )


def _result_fingerprint(value: QualificationResultObservation) -> str:
    return _stable_hash(
        {
            "result_id": value.result_id,
            "action_id": value.action_id,
            "outcome": value.outcome,
        }
    )


def _build_qualification_evidence_api():
    action_registry: dict[
        int,
        tuple[weakref.ReferenceType[QualificationActionEvidence], str],
    ] = {}
    result_registry: dict[
        int,
        tuple[weakref.ReferenceType[QualificationResultObservation], str],
    ] = {}
    action_sequence = itertools.count(1)
    result_sequence = itertools.count(1)

    def _new_action_id(decision: Decision, behavior: str) -> str:
        sequence = next(action_sequence)
        return "QACT-" + _stable_hash(
            {
                "sequence": sequence,
                "decision_id": decision.decision_id,
                "behavior": behavior,
                "contract": CONTRACT,
            }
        )[:32]

    def _new_result_id(action: QualificationActionEvidence, outcome: str) -> str:
        sequence = next(result_sequence)
        return "QRES-" + _stable_hash(
            {
                "sequence": sequence,
                "action_id": action.action_id,
                "outcome": outcome,
                "contract": CONTRACT,
            }
        )[:32]

    def _attest_action(produced: QualificationActionEvidence) -> None:
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = action_registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                action_registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        action_registry[object_id] = (reference, _action_fingerprint(produced))

    def _attest_result(produced: QualificationResultObservation) -> None:
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = result_registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                result_registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        result_registry[object_id] = (reference, _result_fingerprint(produced))

    def _is_attested_action(value: object) -> bool:
        if not isinstance(value, QualificationActionEvidence):
            return False
        entry = action_registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            return False
        return _action_fingerprint(value) == expected_fingerprint

    def _is_attested_result(value: object) -> bool:
        if not isinstance(value, QualificationResultObservation):
            return False
        entry = result_registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            return False
        return _result_fingerprint(value) == expected_fingerprint

    def engage_qualification_action(
        decision: Decision | None,
        *,
        behavior: str,
    ) -> QualificationActionEvidence:
        """Engage one qualification-only synthetic behavior for an exact Decision."""
        if decision is None or not isinstance(decision, Decision):
            raise ValueError("P1.2 qualification Action requires full Decision")
        if not is_factory_attested_decision(decision):
            raise ValueError("P1.2 qualification Action requires factory-attested Decision")
        if not isinstance(behavior, str) or not behavior.strip():
            raise ValueError("P1.2 qualification Action requires non-empty behavior")

        produced = QualificationActionEvidence(
            action_id=_new_action_id(decision, behavior),
            decision_id=decision.decision_id,
            behavior=behavior,
        )
        _attest_action(produced)
        return produced

    def observe_qualification_result(
        action: QualificationActionEvidence | None,
        *,
        outcome: str,
    ) -> QualificationResultObservation:
        """Record one qualification-only synthetic observation for an exact Action."""
        if action is None or not isinstance(action, QualificationActionEvidence):
            raise ValueError("P1.2 qualification Result requires full ActionEvidence")
        if not _is_attested_action(action):
            raise ValueError("P1.2 qualification Result requires factory-attested ActionEvidence")
        if not isinstance(outcome, str) or not outcome.strip():
            raise ValueError("P1.2 qualification Result requires non-empty outcome")

        produced = QualificationResultObservation(
            result_id=_new_result_id(action, outcome),
            action_id=action.action_id,
            outcome=outcome,
        )
        _attest_result(produced)
        return produced

    def verify_qualification_chain(
        decision: object,
        action: object,
        result: object,
    ) -> bool:
        """Verify only exact qualification identity and Decision -> Action -> Result binding."""
        if not isinstance(decision, Decision):
            return False
        if not is_factory_attested_decision(decision):
            return False
        if not _is_attested_action(action):
            return False
        if not _is_attested_result(result):
            return False
        assert isinstance(action, QualificationActionEvidence)
        assert isinstance(result, QualificationResultObservation)
        if action.decision_id != decision.decision_id:
            return False
        if result.action_id != action.action_id:
            return False
        return True

    return (
        engage_qualification_action,
        observe_qualification_result,
        verify_qualification_chain,
    )


(
    engage_qualification_action,
    observe_qualification_result,
    verify_qualification_chain,
) = _build_qualification_evidence_api()
del _build_qualification_evidence_api

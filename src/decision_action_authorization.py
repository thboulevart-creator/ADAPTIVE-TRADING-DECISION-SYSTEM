"""P1.1 pre-ACTION authorization boundary.

This module deliberately does not create ACTION. It authenticates qualified
Decision objects, binds an explicit authorization-constraint envelope, and
fails closed until a separately governed positive authorization policy exists.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass
from typing import Literal

from src.decision import Decision, is_factory_attested_decision


CONTRACT = "P1_1_DECISION_ACTION_AUTHORIZATION_BOUNDARY_V1"
CONSTRAINT_POLICY = "P1_1_BLOCK_ONLY_CONSTRAINTS_V1"
BLOCKED = "BLOCKED"
AUTHORIZED = "AUTHORIZED"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class AuthorizationConstraints:
    """Identity-bound, non-authorizing pre-ACTION constraints envelope."""

    constraint_id: str
    decision_id: str
    research_run_id: str
    context_id: str
    policy_version: str


@dataclass(frozen=True, slots=True)
class AuthorizationVerdict:
    verdict: Literal["BLOCKED"]
    reason: str
    decision_id: str
    constraint_id: str | None
    contract: str = CONTRACT


def _stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _constraint_id(decision: Decision, policy_version: str) -> str:
    return "AUTHC-" + _stable_hash(
        {
            "decision_id": decision.decision_id,
            "research_run_id": decision.research_run_id,
            "context_id": decision.context_id,
            "policy_version": policy_version,
        }
    )[:16]


def _constraint_fingerprint(constraints: AuthorizationConstraints) -> str:
    return _stable_hash(
        {
            "constraint_id": constraints.constraint_id,
            "decision_id": constraints.decision_id,
            "research_run_id": constraints.research_run_id,
            "context_id": constraints.context_id,
            "policy_version": constraints.policy_version,
        }
    )


def _build_constraint_api():
    registry: dict[int, tuple[weakref.ReferenceType[AuthorizationConstraints], str]] = {}

    def bind(decision: Decision | None) -> AuthorizationConstraints:
        if decision is None or not isinstance(decision, Decision):
            raise ValueError("P1.1 constraints require full Decision")
        if not is_factory_attested_decision(decision):
            raise ValueError("P1.1 constraints require factory-attested Decision")
        constraints = AuthorizationConstraints(
            constraint_id=_constraint_id(decision, CONSTRAINT_POLICY),
            decision_id=decision.decision_id,
            research_run_id=decision.research_run_id,
            context_id=decision.context_id,
            policy_version=CONSTRAINT_POLICY,
        )
        object_id = id(constraints)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(constraints, cleanup)
        registry[object_id] = (reference, _constraint_fingerprint(constraints))
        return constraints

    def verify(value: object) -> bool:
        if not isinstance(value, AuthorizationConstraints):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            return False
        if _constraint_fingerprint(value) != expected_fingerprint:
            return False
        if value.policy_version != CONSTRAINT_POLICY:
            return False
        return value.constraint_id == _constraint_id(
            Decision(
                decision_id=value.decision_id,
                research_run_id=value.research_run_id,
                context_id=value.context_id,
                decision="__binding_only__",
            ),
            value.policy_version,
        ) or value.constraint_id == "AUTHC-" + _stable_hash(
            {
                "decision_id": value.decision_id,
                "research_run_id": value.research_run_id,
                "context_id": value.context_id,
                "policy_version": value.policy_version,
            }
        )[:16]

    return bind, verify


bind_authorization_constraints, is_factory_attested_constraints = _build_constraint_api()
del _build_constraint_api


def _blocked(reason: str, decision: object, constraints: object) -> AuthorizationVerdict:
    decision_id = decision.decision_id if isinstance(decision, Decision) else ""
    constraint_id = (
        constraints.constraint_id if isinstance(constraints, AuthorizationConstraints) else None
    )
    return AuthorizationVerdict(
        verdict=BLOCKED,
        reason=reason,
        decision_id=decision_id,
        constraint_id=constraint_id,
    )


def evaluate_pre_action_authorization(
    decision: object,
    constraints: object,
) -> AuthorizationVerdict:
    """Evaluate the current P1.1 boundary without creating ACTION.

    The candidate is intentionally block-only. Authenticity and binding can be
    proven now; a positive authorization policy must be introduced and qualified
    separately before AUTHORIZED can ever be emitted.
    """
    if not isinstance(decision, Decision):
        return _blocked("DECISION_REQUIRED", decision, constraints)
    if not is_factory_attested_decision(decision):
        return _blocked("DECISION_NOT_FACTORY_ATTESTED", decision, constraints)
    if not isinstance(constraints, AuthorizationConstraints):
        return _blocked("CONSTRAINTS_REQUIRED", decision, constraints)
    if not is_factory_attested_constraints(constraints):
        return _blocked("CONSTRAINTS_NOT_FACTORY_ATTESTED", decision, constraints)
    if constraints.decision_id != decision.decision_id:
        return _blocked("CONSTRAINT_DECISION_MISMATCH", decision, constraints)
    if constraints.research_run_id != decision.research_run_id:
        return _blocked("CONSTRAINT_RESEARCH_RUN_MISMATCH", decision, constraints)
    if constraints.context_id != decision.context_id:
        return _blocked("CONSTRAINT_CONTEXT_MISMATCH", decision, constraints)
    if constraints.policy_version != CONSTRAINT_POLICY:
        return _blocked("UNKNOWN_OR_STALE_CONSTRAINT_POLICY", decision, constraints)

    return _blocked("NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY", decision, constraints)

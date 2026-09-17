import weakref

import pytest

import src.decision as decision_module
import src.decision_action_authorization as authorization_module
from src.decision import Decision, produce_decision
from src.decision_action_authorization import bind_authorization_constraints
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_decision(payload: str = "HOLD") -> Decision:
    evidence, context = coherent_runtime_inputs()
    return produce_decision(evidence, context=context, decision=payload)


def reconstruct(source: Decision) -> Decision:
    return Decision(
        decision_id=source.decision_id,
        research_run_id=source.research_run_id,
        context_id=source.context_id,
        decision=source.decision,
    )


def test_g0_monkeypatch_blocked_constant_cannot_emit_authorized(monkeypatch) -> None:
    """The evaluator must not emit an AUTHORIZED-looking verdict by rebinding BLOCKED."""
    decision = coherent_decision("BUY")
    constraints = bind_authorization_constraints(decision)

    monkeypatch.setattr(
        authorization_module,
        "BLOCKED",
        authorization_module.AUTHORIZED,
    )

    verdict = authorization_module.evaluate_pre_action_authorization(
        decision,
        constraints,
    )

    assert verdict.verdict == "BLOCKED"


def test_g1_manual_verdict_cannot_claim_authorized() -> None:
    """A caller must not be able to mint a positive-looking authorization verdict directly."""
    with pytest.raises((TypeError, ValueError)):
        authorization_module.AuthorizationVerdict(
            verdict=authorization_module.AUTHORIZED,
            reason="FORGED",
            decision_id="DEC-forged",
            constraint_id="AUTHC-forged",
        )


def test_g2_monkeypatched_decision_verifier_still_ends_hard_block(monkeypatch) -> None:
    """Verifier substitution must not bypass the current block-only final state."""
    authentic = coherent_decision("BUY")
    constraints = bind_authorization_constraints(authentic)
    forged = reconstruct(authentic)

    monkeypatch.setattr(
        authorization_module,
        "is_factory_attested_decision",
        lambda value: True,
    )

    verdict = authorization_module.evaluate_pre_action_authorization(
        forged,
        constraints,
    )

    assert verdict.verdict == "BLOCKED"
    assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"


def test_g3_decision_registry_closure_injection_cannot_authorize() -> None:
    """CPython closure introspection can forge attestation; final boundary must still block."""
    authentic = coherent_decision("BUY")
    constraints = bind_authorization_constraints(authentic)
    forged = reconstruct(authentic)

    closure = decision_module.is_factory_attested_decision.__closure__ or ()
    registries = [cell.cell_contents for cell in closure if isinstance(cell.cell_contents, dict)]
    assert len(registries) == 1
    registry = registries[0]

    registry[id(forged)] = (
        weakref.ref(forged),
        decision_module._decision_identity_fingerprint(forged),
    )
    try:
        assert decision_module.is_factory_attested_decision(forged)
        verdict = authorization_module.evaluate_pre_action_authorization(
            forged,
            constraints,
        )
        assert verdict.verdict == "BLOCKED"
        assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"
    finally:
        registry.pop(id(forged), None)


def test_g4_constraint_registry_closure_injection_cannot_authorize() -> None:
    """Constraint registry introspection may forge attestation but must not yield AUTHORIZED."""
    decision = coherent_decision("BUY")
    authentic = bind_authorization_constraints(decision)
    forged = authorization_module.AuthorizationConstraints(
        constraint_id=authentic.constraint_id,
        decision_id=authentic.decision_id,
        research_run_id=authentic.research_run_id,
        context_id=authentic.context_id,
        policy_version=authentic.policy_version,
    )

    closure = authorization_module.is_factory_attested_constraints.__closure__ or ()
    registries = [cell.cell_contents for cell in closure if isinstance(cell.cell_contents, dict)]
    assert len(registries) == 1
    registry = registries[0]

    registry[id(forged)] = (
        weakref.ref(forged),
        authorization_module._constraint_fingerprint(forged),
    )
    try:
        assert authorization_module.is_factory_attested_constraints(forged)
        verdict = authorization_module.evaluate_pre_action_authorization(
            decision,
            forged,
        )
        assert verdict.verdict == "BLOCKED"
        assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"
    finally:
        registry.pop(id(forged), None)

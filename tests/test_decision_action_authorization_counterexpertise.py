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


def _closure_registry(function) -> dict:
    closure = function.__closure__ or ()
    registries = [cell.cell_contents for cell in closure if isinstance(cell.cell_contents, dict)]
    assert len(registries) == 1
    return registries[0]


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


def test_g3_closure_injection_cannot_mint_decision_attestation() -> None:
    """Injecting the verifier closure registry must not attest a reconstructed Decision."""
    authentic = coherent_decision("BUY")
    forged = reconstruct(authentic)
    registry = _closure_registry(decision_module.is_factory_attested_decision)

    registry[id(forged)] = (
        weakref.ref(forged),
        decision_module._decision_identity_fingerprint(forged),
    )
    try:
        assert decision_module.is_factory_attested_decision(forged) is False
    finally:
        registry.pop(id(forged), None)


def test_g4_closure_injection_cannot_mint_constraint_attestation() -> None:
    """Injecting the verifier closure registry must not attest reconstructed constraints."""
    decision = coherent_decision("BUY")
    authentic = bind_authorization_constraints(decision)
    forged = authorization_module.AuthorizationConstraints(
        constraint_id=authentic.constraint_id,
        decision_id=authentic.decision_id,
        research_run_id=authentic.research_run_id,
        context_id=authentic.context_id,
        policy_version=authentic.policy_version,
    )
    registry = _closure_registry(authorization_module.is_factory_attested_constraints)

    registry[id(forged)] = (
        weakref.ref(forged),
        authorization_module._constraint_fingerprint(forged),
    )
    try:
        assert authorization_module.is_factory_attested_constraints(forged) is False
    finally:
        registry.pop(id(forged), None)


def test_g5_fully_forged_reflective_chain_still_hits_block_only_terminal() -> None:
    """A process-compromised forged chain proves why AUTHORIZED must remain unopened."""
    authentic = coherent_decision("BUY")
    authentic_constraints = bind_authorization_constraints(authentic)
    forged_decision = reconstruct(authentic)
    forged_constraints = authorization_module.AuthorizationConstraints(
        constraint_id=authentic_constraints.constraint_id,
        decision_id=authentic_constraints.decision_id,
        research_run_id=authentic_constraints.research_run_id,
        context_id=authentic_constraints.context_id,
        policy_version=authentic_constraints.policy_version,
    )

    decision_registry = _closure_registry(decision_module.is_factory_attested_decision)
    constraint_registry = _closure_registry(authorization_module.is_factory_attested_constraints)
    decision_registry[id(forged_decision)] = (
        weakref.ref(forged_decision),
        decision_module._decision_identity_fingerprint(forged_decision),
    )
    constraint_registry[id(forged_constraints)] = (
        weakref.ref(forged_constraints),
        authorization_module._constraint_fingerprint(forged_constraints),
    )
    try:
        assert decision_module.is_factory_attested_decision(forged_decision)
        assert authorization_module.is_factory_attested_constraints(forged_constraints)
        verdict = authorization_module.evaluate_pre_action_authorization(
            forged_decision,
            forged_constraints,
        )
        assert verdict.verdict == "BLOCKED"
        assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"
    finally:
        decision_registry.pop(id(forged_decision), None)
        constraint_registry.pop(id(forged_constraints), None)

import copy
from dataclasses import replace

import pytest

import src.decision as decision_module
import src.decision_action_authorization as authorization_module
from src.decision import Decision, is_factory_attested_decision, produce_decision
from src.decision_action_authorization import (
    AuthorizationConstraints,
    BLOCKED,
    CONSTRAINT_POLICY,
    bind_authorization_constraints,
    evaluate_pre_action_authorization,
    is_factory_attested_constraints,
)
from src.decision_trace import DecisionTrace
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_decision(payload: str = "HOLD") -> Decision:
    evidence, context = coherent_runtime_inputs()
    return produce_decision(evidence, context=context, decision=payload)


def reconstruct(decision: Decision, **changes) -> Decision:
    values = {
        "decision_id": decision.decision_id,
        "research_run_id": decision.research_run_id,
        "context_id": decision.context_id,
        "decision": decision.decision,
    }
    values.update(changes)
    return Decision(**values)


def coherent_boundary(payload: str = "HOLD"):
    decision = coherent_decision(payload)
    constraints = bind_authorization_constraints(decision)
    return decision, constraints


# A — Decision existence and type

def test_a0_authentic_decision_reaches_boundary_without_side_effects() -> None:
    decision, constraints = coherent_boundary()
    assert is_factory_attested_decision(decision)
    assert is_factory_attested_constraints(constraints)

    verdict = evaluate_pre_action_authorization(decision, constraints)

    assert verdict.verdict == BLOCKED
    assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"
    assert verdict.decision_id == decision.decision_id
    assert verdict.constraint_id == constraints.constraint_id
    assert not hasattr(verdict, "action")


def test_a1_absent_decision_is_blocked() -> None:
    _, constraints = coherent_boundary()
    verdict = evaluate_pre_action_authorization(None, constraints)
    assert (verdict.verdict, verdict.reason) == (BLOCKED, "DECISION_REQUIRED")


def test_a2_wrong_decision_type_is_blocked() -> None:
    _, constraints = coherent_boundary()
    verdict = evaluate_pre_action_authorization(object(), constraints)
    assert (verdict.verdict, verdict.reason) == (BLOCKED, "DECISION_REQUIRED")


def test_a3_decision_id_alone_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    verdict = evaluate_pre_action_authorization(decision.decision_id, constraints)
    assert (verdict.verdict, verdict.reason) == (BLOCKED, "DECISION_REQUIRED")


def test_a4_serialized_decision_fields_are_blocked() -> None:
    decision, constraints = coherent_boundary()
    serialized = {
        "decision_id": decision.decision_id,
        "research_run_id": decision.research_run_id,
        "context_id": decision.context_id,
        "decision": decision.decision,
    }
    verdict = evaluate_pre_action_authorization(serialized, constraints)
    assert (verdict.verdict, verdict.reason) == (BLOCKED, "DECISION_REQUIRED")


# B — Reconstruction and forgery

def test_b0_exact_manual_decision_reconstruction_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    forged = reconstruct(decision)
    assert forged == decision
    assert forged is not decision
    assert not is_factory_attested_decision(forged)
    verdict = evaluate_pre_action_authorization(forged, constraints)
    assert verdict.reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_b1_forged_decision_id_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    forged = reconstruct(decision, decision_id="DEC-forged")
    assert not is_factory_attested_decision(forged)
    assert evaluate_pre_action_authorization(forged, constraints).verdict == BLOCKED


def test_b2_foreign_research_run_id_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    forged = reconstruct(decision, research_run_id="RUN-foreign")
    assert evaluate_pre_action_authorization(forged, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_b3_foreign_context_id_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    forged = reconstruct(decision, context_id="CTX-foreign")
    assert evaluate_pre_action_authorization(forged, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_b4_dataclass_replace_reconstruction_is_blocked() -> None:
    decision, constraints = coherent_boundary()
    forged = replace(decision, decision=decision.decision)
    assert forged == decision
    assert forged is not decision
    assert evaluate_pre_action_authorization(forged, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_b5_b6_silent_copy_reconstruction_is_blocked(copier) -> None:
    decision, constraints = coherent_boundary()
    forged = copier(decision)
    assert forged == decision
    assert forged is not decision
    assert evaluate_pre_action_authorization(forged, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_b7_self_declared_factory_marker_cannot_be_added() -> None:
    decision, _ = coherent_boundary()
    forged = reconstruct(decision)
    with pytest.raises(AttributeError):
        object.__setattr__(forged, "_factory_validated", True)
    assert not is_factory_attested_decision(forged)


def test_b8_no_raw_decision_attestation_or_minter_capability_is_exposed() -> None:
    forbidden = (
        "_build_decision_api",
        "_attest_factory_decision",
        "attest_decision",
        "mint_decision",
    )
    assert all(not hasattr(decision_module, name) for name in forbidden)
    assert callable(decision_module.produce_decision)
    assert callable(decision_module.is_factory_attested_decision)


# C — Post-production mutation

@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("decision_id", "DEC-mutated"),
        ("decision", "SELL"),
        ("research_run_id", "RUN-mutated"),
        ("context_id", "CTX-mutated"),
    ],
)
def test_c0_c3_post_production_identity_or_payload_mutation_invalidates_attestation(
    field: str, value: str
) -> None:
    decision, constraints = coherent_boundary()
    assert is_factory_attested_decision(decision)
    object.__setattr__(decision, field, value)
    assert not is_factory_attested_decision(decision)
    assert evaluate_pre_action_authorization(decision, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_c4_multi_field_mutation_invalidates_attestation() -> None:
    decision, constraints = coherent_boundary()
    object.__setattr__(decision, "research_run_id", "RUN-mutated")
    object.__setattr__(decision, "context_id", "CTX-mutated")
    object.__setattr__(decision, "decision", "BUY")
    assert not is_factory_attested_decision(decision)
    assert evaluate_pre_action_authorization(decision, constraints).verdict == BLOCKED


def test_c5_no_embedded_private_attestation_marker_exists_to_mutate() -> None:
    decision, _ = coherent_boundary()
    assert not hasattr(decision, "_factory_validated")
    with pytest.raises(AttributeError):
        object.__setattr__(decision, "_factory_validated", False)
    assert is_factory_attested_decision(decision)


# D — Identity/content substitution

def test_d0_same_payload_foreign_research_run_is_blocked() -> None:
    decision, constraints = coherent_boundary("BUY")
    forged = reconstruct(decision, research_run_id="RUN-foreign")
    assert evaluate_pre_action_authorization(forged, constraints).verdict == BLOCKED


def test_d1_same_payload_foreign_context_is_blocked() -> None:
    decision, constraints = coherent_boundary("BUY")
    forged = reconstruct(decision, context_id="CTX-foreign")
    assert evaluate_pre_action_authorization(forged, constraints).verdict == BLOCKED


def test_d2_same_identifiers_altered_payload_is_blocked() -> None:
    decision, constraints = coherent_boundary("BUY")
    forged = reconstruct(decision, decision="SELL")
    assert evaluate_pre_action_authorization(forged, constraints).verdict == BLOCKED


def test_d3_same_decision_id_reused_for_different_content_is_blocked() -> None:
    decision, constraints = coherent_boundary("BUY")
    forged = reconstruct(decision, decision="SELL", decision_id=decision.decision_id)
    assert evaluate_pre_action_authorization(forged, constraints).reason == "DECISION_NOT_FACTORY_ATTESTED"


def test_d4_valid_decision_cannot_be_rebound_to_foreign_constraints() -> None:
    first = coherent_decision("BUY")
    second = coherent_decision("SELL")
    foreign_constraints = bind_authorization_constraints(second)
    assert is_factory_attested_decision(first)
    assert is_factory_attested_constraints(foreign_constraints)
    verdict = evaluate_pre_action_authorization(first, foreign_constraints)
    assert verdict.reason == "CONSTRAINT_DECISION_MISMATCH"


def test_d5_replay_cannot_be_authorized_without_declared_admissibility_envelope() -> None:
    decision, constraints = coherent_boundary("BUY")
    verdict = evaluate_pre_action_authorization(decision, constraints)
    assert verdict.verdict == BLOCKED
    assert verdict.reason == "NO_GOVERNED_POSITIVE_AUTHORIZATION_POLICY"


# E — Authorization-constraint failures

def test_e0_absent_constraints_are_blocked() -> None:
    decision = coherent_decision()
    verdict = evaluate_pre_action_authorization(decision, None)
    assert verdict.reason == "CONSTRAINTS_REQUIRED"


def test_e1_wrong_constraint_type_is_blocked() -> None:
    decision = coherent_decision()
    verdict = evaluate_pre_action_authorization(decision, {"policy_version": CONSTRAINT_POLICY})
    assert verdict.reason == "CONSTRAINTS_REQUIRED"


def test_e2_reconstructed_or_incomplete_constraints_are_blocked() -> None:
    decision, constraints = coherent_boundary()
    reconstructed = AuthorizationConstraints(
        constraint_id=constraints.constraint_id,
        decision_id=constraints.decision_id,
        research_run_id=constraints.research_run_id,
        context_id=constraints.context_id,
        policy_version=constraints.policy_version,
    )
    assert reconstructed == constraints
    assert reconstructed is not constraints
    assert not is_factory_attested_constraints(reconstructed)
    assert evaluate_pre_action_authorization(decision, reconstructed).reason == "CONSTRAINTS_NOT_FACTORY_ATTESTED"


def test_e3_unknown_constraint_policy_has_no_permissive_fallback() -> None:
    decision, constraints = coherent_boundary()
    unknown = replace(constraints, policy_version="UNKNOWN_POLICY")
    assert not is_factory_attested_constraints(unknown)
    assert evaluate_pre_action_authorization(decision, unknown).verdict == BLOCKED


def test_e4_failed_constraints_cannot_be_downgraded_or_ignored_by_caller() -> None:
    decision, constraints = coherent_boundary()
    with pytest.raises(TypeError):
        evaluate_pre_action_authorization(decision, constraints, ignore_failed_constraints=True)


def test_e5_precomputed_authorized_flag_is_not_an_input() -> None:
    decision, constraints = coherent_boundary()
    with pytest.raises(TypeError):
        evaluate_pre_action_authorization(decision, constraints, authorized=True)


def test_e6_conflicting_or_undefined_constraint_representation_is_blocked() -> None:
    decision = coherent_decision()

    class ConflictingConstraints:
        policy_version = CONSTRAINT_POLICY
        fallback_policy_version = "OTHER"

    verdict = evaluate_pre_action_authorization(decision, ConflictingConstraints())
    assert verdict.reason == "CONSTRAINTS_REQUIRED"


def test_e7_foreign_constraints_rebound_to_valid_decision_are_blocked() -> None:
    decision = coherent_decision("BUY")
    foreign = coherent_decision("SELL")
    foreign_constraints = bind_authorization_constraints(foreign)
    verdict = evaluate_pre_action_authorization(decision, foreign_constraints)
    assert verdict.reason == "CONSTRAINT_DECISION_MISMATCH"


def test_constraint_post_factory_mutation_invalidates_attestation() -> None:
    decision, constraints = coherent_boundary()
    object.__setattr__(constraints, "context_id", "CTX-mutated")
    assert not is_factory_attested_constraints(constraints)
    assert evaluate_pre_action_authorization(decision, constraints).reason == "CONSTRAINTS_NOT_FACTORY_ATTESTED"


# F — Downstream bypass

def test_f0_boundary_exposes_no_action_constructor_or_action_payload() -> None:
    decision, constraints = coherent_boundary()
    verdict = evaluate_pre_action_authorization(decision, constraints)
    assert not hasattr(authorization_module, "Action")
    assert not hasattr(authorization_module, "create_action")
    assert not hasattr(verdict, "action")


def test_f1_blocked_is_not_a_soft_warning_or_authorization() -> None:
    decision, constraints = coherent_boundary()
    verdict = evaluate_pre_action_authorization(decision, constraints)
    assert verdict.verdict == BLOCKED
    assert verdict.verdict != authorization_module.AUTHORIZED


def test_f2_decision_trace_is_not_authorization_proof() -> None:
    decision = coherent_decision()
    trace = DecisionTrace(
        decision_id=decision.decision_id,
        provenance_id="PROV-x",
        research_run_id=decision.research_run_id,
        code_version="a" * 40,
        configuration_version="CFG-x",
        dataset_id="DATA-x",
        dataset_version="v1",
        context_id=decision.context_id,
        decision=decision.decision,
        action_id="ACTION-x",
        result_id="RESULT-x",
    )
    verdict = evaluate_pre_action_authorization(decision, trace)
    assert verdict.reason == "CONSTRAINTS_REQUIRED"


def test_f3_p1_0_pass_cannot_be_supplied_as_authorization() -> None:
    decision, constraints = coherent_boundary()
    with pytest.raises(TypeError):
        evaluate_pre_action_authorization(decision, constraints, promotion_pass=True)


def test_f4_acquisition_backtest_or_live_permission_cannot_be_supplied() -> None:
    decision, constraints = coherent_boundary()
    with pytest.raises(TypeError):
        evaluate_pre_action_authorization(
            decision,
            constraints,
            acquisition_authorized=True,
            real_backtest_authorized=True,
            live_authorized=True,
        )


def test_f5_rejected_path_cannot_construct_downstream_action_in_harness() -> None:
    decision, constraints = coherent_boundary()
    forged = reconstruct(decision)
    verdict = evaluate_pre_action_authorization(forged, constraints)
    assert verdict.verdict == BLOCKED
    assert not hasattr(authorization_module, "Action")
    assert not hasattr(authorization_module, "create_action")

from __future__ import annotations

from pathlib import Path

from src.promotion_gate import (
    BLOCKED,
    FAIL,
    PASS,
    CAPITAL_OR_REAL_WORLD_EXPOSURE,
    DETERMINISTIC_INTERNAL_ONLY,
    EVIDENCE_REQUIREMENT_REDUCTION,
    GOVERNANCE_RELAXATION,
    GOVERNANCE_RELAXATION_PERMISSION,
    LIVE_EXECUTION,
    LIVE_OR_EXTERNAL_SIDE_EFFECT,
    NATIVE_ACQUISITION_OR_REAL_BACKTEST,
    NATIVE_BI5_ACQUISITION,
    PERMISSION_INCREASE,
    REAL_DATA_BACKTEST,
    RESEARCH_ONLY_NON_AUTHORIZING,
    TIER_A,
    TIER_B,
    TIER_C,
    TIER_REQUIREMENT_REDUCTION,
    TRUST_BOUNDARY_CHANGE,
    PromotionRequest,
    RelaxationEvidence,
    derive_consequence_tier,
    evaluate_promotion,
)
from tools.coverage_execution_window_boundary import BLOCKED as BOUNDARY_BLOCKED
from tools.frozen_execution_window import evaluate_acquisition_after_persisted_freeze


def request(
    *,
    current_tier: str = TIER_A,
    target_tier: str = TIER_A,
    consequences: tuple[str, ...] = (RESEARCH_ONLY_NON_AUTHORIZING,),
    current_permissions: frozenset[str] = frozenset(),
    target_permissions: frozenset[str] = frozenset(),
    boundary_tiers: tuple[str, ...] = (),
    evidence: RelaxationEvidence | None = None,
) -> PromotionRequest:
    return PromotionRequest(
        current_tier=current_tier,
        target_tier=target_tier,
        consequences=consequences,
        current_permissions=current_permissions,
        target_permissions=target_permissions,
        boundary_tiers=boundary_tiers,
        relaxation_evidence=evidence,
    )


def complete_tier_a_evidence(**overrides) -> RelaxationEvidence:
    values = dict(
        causally_linked_trigger=False,
        days_since_trigger=None,
        same_cause_event_days_ago=None,
        observable_revocation_condition=True,
        timely_detection=True,
        reaction_latency_compatible=True,
        bounded_blast_radius=True,
        executable_revocation=True,
        rollback_or_safe_state=True,
        monitor_independent=True,
        monitor_falsifiable_by_injection=True,
        bounded_known_revocation_cost=True,
    )
    values.update(overrides)
    return RelaxationEvidence(**values)


def test_f0_no_promotion_passes_without_permission_change() -> None:
    decision = evaluate_promotion(
        request(current_tier=TIER_C, target_tier=TIER_C)
    )
    assert decision.verdict == PASS
    assert decision.reason == "NO_PROMOTION"
    assert decision.effective_tier == TIER_C
    assert decision.relaxation is False


def test_f1_permission_restriction_is_allowed() -> None:
    decision = evaluate_promotion(
        request(
            current_permissions=frozenset({LIVE_EXECUTION}),
            target_permissions=frozenset(),
        )
    )
    assert decision.verdict == PASS
    assert decision.reason == "RESTRICTION_ALLOWED"
    assert decision.removed_permissions == frozenset({LIVE_EXECUTION})


def test_f2_research_only_consequence_derives_tier_c() -> None:
    assert derive_consequence_tier((RESEARCH_ONLY_NON_AUTHORIZING,)) == TIER_C


def test_f3_deterministic_internal_consequence_derives_tier_b() -> None:
    assert derive_consequence_tier((DETERMINISTIC_INTERNAL_ONLY,)) == TIER_B


def test_f4_permission_increase_consequence_derives_tier_a() -> None:
    assert derive_consequence_tier((PERMISSION_INCREASE,)) == TIER_A


def test_f5_unknown_consequence_fails_closed_to_tier_a_and_blocks_evaluation() -> None:
    consequences = ("UNRECOGNIZED_CONSEQUENCE",)
    assert derive_consequence_tier(consequences) == TIER_A
    decision = evaluate_promotion(request(consequences=consequences))
    assert decision.verdict == BLOCKED
    assert decision.reason == "UNKNOWN_CONSEQUENCE:UNRECOGNIZED_CONSEQUENCE"
    assert decision.consequence_tier == TIER_A
    assert decision.effective_tier == TIER_A


def test_f6_empty_consequence_set_fails_closed_to_tier_a_and_blocks_evaluation() -> None:
    assert derive_consequence_tier(()) == TIER_A
    decision = evaluate_promotion(request(consequences=()))
    assert decision.verdict == BLOCKED
    assert decision.reason == "CONSEQUENCES_INCOMPLETE"
    assert decision.consequence_tier == TIER_A
    assert decision.effective_tier == TIER_A


def test_f7_mixed_consequences_inherit_strongest_tier() -> None:
    assert (
        derive_consequence_tier(
            (RESEARCH_ONLY_NON_AUTHORIZING, DETERMINISTIC_INTERNAL_ONLY, TRUST_BOUNDARY_CHANGE)
        )
        == TIER_A
    )


def test_f8_boundary_inherits_maximum_participating_tier() -> None:
    decision = evaluate_promotion(
        request(
            current_tier=TIER_C,
            target_tier=TIER_C,
            boundary_tiers=(TIER_B,),
        )
    )
    assert decision.verdict == PASS
    assert decision.effective_tier == TIER_B


def test_f9_caller_cannot_lower_an_existing_tier_a_boundary() -> None:
    decision = evaluate_promotion(
        request(
            current_tier=TIER_A,
            target_tier=TIER_B,
            consequences=(DETERMINISTIC_INTERNAL_ONLY,),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.effective_tier == TIER_A
    assert decision.relaxation is True


def test_f10_tier_a_to_b_downgrade_is_a_blocked_relaxation() -> None:
    decision = evaluate_promotion(
        request(
            current_tier=TIER_A,
            target_tier=TIER_B,
            consequences=(TIER_REQUIREMENT_REDUCTION,),
            evidence=complete_tier_a_evidence(),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "P1_0_REJECT_ALL_PROMOTION"
    assert decision.effective_tier == TIER_A


def test_f11_native_bi5_acquisition_permission_cannot_be_promoted() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(PERMISSION_INCREASE, NATIVE_ACQUISITION_OR_REAL_BACKTEST),
            target_permissions=frozenset({NATIVE_BI5_ACQUISITION}),
            evidence=complete_tier_a_evidence(),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "P1_0_REJECT_ALL_PROMOTION"


def test_f12_real_data_backtest_permission_cannot_be_promoted() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(PERMISSION_INCREASE, NATIVE_ACQUISITION_OR_REAL_BACKTEST),
            target_permissions=frozenset({REAL_DATA_BACKTEST}),
            evidence=complete_tier_a_evidence(),
        )
    )
    assert decision.verdict == BLOCKED


def test_f13_live_execution_permission_cannot_be_promoted() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(PERMISSION_INCREASE, LIVE_OR_EXTERNAL_SIDE_EFFECT, CAPITAL_OR_REAL_WORLD_EXPOSURE),
            target_permissions=frozenset({LIVE_EXECUTION}),
            evidence=complete_tier_a_evidence(),
        )
    )
    assert decision.verdict == BLOCKED


def test_f14_governance_relaxation_permission_cannot_be_promoted() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(GOVERNANCE_RELAXATION, EVIDENCE_REQUIREMENT_REDUCTION),
            target_permissions=frozenset({GOVERNANCE_RELAXATION_PERMISSION}),
            evidence=complete_tier_a_evidence(),
        )
    )
    assert decision.verdict == BLOCKED


def test_f15_all_nine_tier_a_readiness_conditions_still_do_not_authorize_promotion() -> None:
    evidence = complete_tier_a_evidence()
    assert evidence.tier_a_readiness_complete() is True
    decision = evaluate_promotion(
        request(
            consequences=(PERMISSION_INCREASE,),
            target_permissions=frozenset({LIVE_EXECUTION}),
            evidence=evidence,
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "P1_0_REJECT_ALL_PROMOTION"


def test_f16_missing_tier_a_readiness_blocks_before_reject_all() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(PERMISSION_INCREASE,),
            target_permissions=frozenset({LIVE_EXECUTION}),
            evidence=RelaxationEvidence(observable_revocation_condition=True),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "TIER_A_RELAXATION_READINESS_INCOMPLETE"


def test_f17_causally_linked_29_day_cooling_off_blocks_relaxation() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(GOVERNANCE_RELAXATION,),
            evidence=complete_tier_a_evidence(
                causally_linked_trigger=True,
                days_since_trigger=29,
            ),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "GOVERNANCE_RELAXATION_COOLING_OFF_ACTIVE"


def test_f18_same_cause_event_resets_cooling_off() -> None:
    decision = evaluate_promotion(
        request(
            consequences=(GOVERNANCE_RELAXATION,),
            evidence=complete_tier_a_evidence(
                causally_linked_trigger=True,
                days_since_trigger=45,
                same_cause_event_days_ago=3,
            ),
        )
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "GOVERNANCE_RELAXATION_COOLING_OFF_RESET_BY_SAME_CAUSE_EVENT"


def test_f19_tier_hardening_b_to_a_is_allowed_without_permission_increase() -> None:
    decision = evaluate_promotion(
        request(
            current_tier=TIER_B,
            target_tier=TIER_A,
            consequences=(DETERMINISTIC_INTERNAL_ONLY,),
        )
    )
    assert decision.verdict == PASS
    assert decision.reason == "TIER_HARDENING_ALLOWED"
    assert decision.effective_tier == TIER_A


def test_f20_unknown_permission_is_fail_not_implicit_authorization() -> None:
    decision = evaluate_promotion(
        request(target_permissions=frozenset({"UNKNOWN_PERMISSION"}))
    )
    assert decision.verdict == FAIL
    assert decision.reason.startswith("UNKNOWN_PERMISSION:")


def test_existing_acquisition_boundary_remains_blocked() -> None:
    decision = evaluate_acquisition_after_persisted_freeze()
    assert decision.verdict == BOUNDARY_BLOCKED


def test_acquisition_pass_path_is_explicitly_bound_to_promotion_gate() -> None:
    source = Path("tools/frozen_execution_window.py").read_text(encoding="utf-8")
    assert "evaluate_promotion" in source
    assert "NATIVE_BI5_ACQUISITION" in source
    assert "PROMOTION_GATE:" in source


def test_promotion_gate_is_pure_and_has_no_side_effect_surfaces() -> None:
    source = Path("src/promotion_gate.py").read_text(encoding="utf-8")
    forbidden = (
        "requests",
        "urllib",
        "subprocess",
        "open(",
        "write_text",
        "write_bytes",
        "socket",
    )
    assert all(token not in source for token in forbidden)

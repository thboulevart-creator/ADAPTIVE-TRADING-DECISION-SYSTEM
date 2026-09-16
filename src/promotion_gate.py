from __future__ import annotations

from dataclasses import dataclass


PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"

CONTRACT = "PROMOTION_GATE_FAIL_CLOSED_V1"
MODE = "REJECT_ALL_PROMOTION"

TIER_C = "C"
TIER_B = "B"
TIER_A = "A"
TIERS = (TIER_C, TIER_B, TIER_A)
TIER_RANK = {TIER_C: 0, TIER_B: 1, TIER_A: 2}

RESEARCH_ONLY_NON_AUTHORIZING = "RESEARCH_ONLY_NON_AUTHORIZING"
DETERMINISTIC_INTERNAL_ONLY = "DETERMINISTIC_INTERNAL_ONLY"
PERMISSION_INCREASE = "PERMISSION_INCREASE"
GOVERNANCE_RELAXATION = "GOVERNANCE_RELAXATION"
EVIDENCE_REQUIREMENT_REDUCTION = "EVIDENCE_REQUIREMENT_REDUCTION"
TIER_REQUIREMENT_REDUCTION = "TIER_REQUIREMENT_REDUCTION"
NATIVE_ACQUISITION_OR_REAL_BACKTEST = "NATIVE_ACQUISITION_OR_REAL_BACKTEST"
LIVE_OR_EXTERNAL_SIDE_EFFECT = "LIVE_OR_EXTERNAL_SIDE_EFFECT"
CAPITAL_OR_REAL_WORLD_EXPOSURE = "CAPITAL_OR_REAL_WORLD_EXPOSURE"
TRUST_BOUNDARY_CHANGE = "TRUST_BOUNDARY_CHANGE"

TIER_A_CONSEQUENCES = frozenset(
    {
        PERMISSION_INCREASE,
        GOVERNANCE_RELAXATION,
        EVIDENCE_REQUIREMENT_REDUCTION,
        TIER_REQUIREMENT_REDUCTION,
        NATIVE_ACQUISITION_OR_REAL_BACKTEST,
        LIVE_OR_EXTERNAL_SIDE_EFFECT,
        CAPITAL_OR_REAL_WORLD_EXPOSURE,
        TRUST_BOUNDARY_CHANGE,
    }
)
KNOWN_CONSEQUENCES = frozenset(
    set(TIER_A_CONSEQUENCES)
    | {DETERMINISTIC_INTERNAL_ONLY, RESEARCH_ONLY_NON_AUTHORIZING}
)
RELAXATION_CONSEQUENCES = frozenset(
    {GOVERNANCE_RELAXATION, EVIDENCE_REQUIREMENT_REDUCTION, TIER_REQUIREMENT_REDUCTION}
)

NATIVE_BI5_ACQUISITION = "NATIVE_BI5_ACQUISITION"
REAL_DATA_BACKTEST = "REAL_DATA_BACKTEST"
LIVE_EXECUTION = "LIVE_EXECUTION"
GOVERNANCE_RELAXATION_PERMISSION = "GOVERNANCE_RELAXATION"
PROTECTED_PERMISSIONS = frozenset(
    {
        NATIVE_BI5_ACQUISITION,
        REAL_DATA_BACKTEST,
        LIVE_EXECUTION,
        GOVERNANCE_RELAXATION_PERMISSION,
    }
)


@dataclass(frozen=True)
class RelaxationEvidence:
    causally_linked_trigger: bool = False
    days_since_trigger: int | None = None
    same_cause_event_days_ago: int | None = None
    observable_revocation_condition: bool = False
    timely_detection: bool = False
    reaction_latency_compatible: bool = False
    bounded_blast_radius: bool = False
    executable_revocation: bool = False
    rollback_or_safe_state: bool = False
    monitor_independent: bool = False
    monitor_falsifiable_by_injection: bool = False
    bounded_known_revocation_cost: bool = False

    def tier_a_readiness_complete(self) -> bool:
        return all(
            (
                self.observable_revocation_condition,
                self.timely_detection,
                self.reaction_latency_compatible,
                self.bounded_blast_radius,
                self.executable_revocation,
                self.rollback_or_safe_state,
                self.monitor_independent,
                self.monitor_falsifiable_by_injection,
                self.bounded_known_revocation_cost,
            )
        )


@dataclass(frozen=True)
class PromotionRequest:
    current_tier: str
    target_tier: str
    consequences: tuple[str, ...]
    current_permissions: frozenset[str] = frozenset()
    target_permissions: frozenset[str] = frozenset()
    boundary_tiers: tuple[str, ...] = ()
    relaxation_evidence: RelaxationEvidence | None = None


@dataclass(frozen=True)
class PromotionDecision:
    verdict: str
    reason: str
    effective_tier: str | None
    consequence_tier: str | None
    relaxation: bool
    added_permissions: frozenset[str]
    removed_permissions: frozenset[str]
    contract: str = CONTRACT
    mode: str = MODE


def _decision(
    verdict: str,
    reason: str,
    *,
    effective_tier: str | None = None,
    consequence_tier: str | None = None,
    relaxation: bool = False,
    added_permissions: frozenset[str] = frozenset(),
    removed_permissions: frozenset[str] = frozenset(),
) -> PromotionDecision:
    return PromotionDecision(
        verdict=verdict,
        reason=reason,
        effective_tier=effective_tier,
        consequence_tier=consequence_tier,
        relaxation=relaxation,
        added_permissions=added_permissions,
        removed_permissions=removed_permissions,
    )


def derive_consequence_tier(consequences: tuple[str, ...]) -> str:
    # Empty or unknown consequence sets are conservatively Tier A because
    # consequence completeness cannot be established from the request.
    if not consequences:
        return TIER_A
    if any(item not in KNOWN_CONSEQUENCES for item in consequences):
        return TIER_A
    if any(item in TIER_A_CONSEQUENCES for item in consequences):
        return TIER_A
    if DETERMINISTIC_INTERNAL_ONLY in consequences:
        return TIER_B
    return TIER_C


def inherit_boundary_tier(*tiers: str) -> str:
    if not tiers:
        return TIER_A
    if any(tier not in TIER_RANK for tier in tiers):
        raise ValueError("UNKNOWN_TIER")
    return max(tiers, key=TIER_RANK.__getitem__)


def _validate_permissions(current: frozenset[str], target: frozenset[str]) -> str | None:
    unknown = (current | target) - PROTECTED_PERMISSIONS
    if unknown:
        return "UNKNOWN_PERMISSION:" + ",".join(sorted(unknown))
    return None


def _cooling_off_block(evidence: RelaxationEvidence | None) -> str | None:
    if evidence is None:
        return None
    if evidence.days_since_trigger is not None and evidence.days_since_trigger < 0:
        return "INVALID_COOLING_OFF_DAYS"
    if evidence.same_cause_event_days_ago is not None and evidence.same_cause_event_days_ago < 0:
        return "INVALID_SAME_CAUSE_EVENT_DAYS"
    if evidence.causally_linked_trigger:
        if evidence.days_since_trigger is None:
            return "COOLING_OFF_AGE_UNKNOWN"
        if evidence.days_since_trigger < 30:
            return "GOVERNANCE_RELAXATION_COOLING_OFF_ACTIVE"
    if (
        evidence.same_cause_event_days_ago is not None
        and evidence.same_cause_event_days_ago < 30
    ):
        return "GOVERNANCE_RELAXATION_COOLING_OFF_RESET_BY_SAME_CAUSE_EVENT"
    return None


def evaluate_promotion(request: PromotionRequest) -> PromotionDecision:
    declared_tiers = (request.current_tier, request.target_tier, *request.boundary_tiers)
    if any(tier not in TIER_RANK for tier in declared_tiers):
        return _decision(FAIL, "UNKNOWN_TIER")

    permission_error = _validate_permissions(
        request.current_permissions, request.target_permissions
    )
    if permission_error is not None:
        return _decision(FAIL, permission_error)

    consequence_tier = derive_consequence_tier(request.consequences)
    effective_tier = inherit_boundary_tier(*declared_tiers, consequence_tier)

    added = request.target_permissions - request.current_permissions
    removed = request.current_permissions - request.target_permissions
    tier_downgrade = TIER_RANK[request.target_tier] < TIER_RANK[request.current_tier]
    explicit_relaxation = any(
        consequence in RELAXATION_CONSEQUENCES
        for consequence in request.consequences
    )
    relaxation = bool(added or tier_downgrade or explicit_relaxation)

    if not relaxation:
        if removed:
            return _decision(
                PASS,
                "RESTRICTION_ALLOWED",
                effective_tier=effective_tier,
                consequence_tier=consequence_tier,
                removed_permissions=removed,
            )
        if TIER_RANK[request.target_tier] > TIER_RANK[request.current_tier]:
            return _decision(
                PASS,
                "TIER_HARDENING_ALLOWED",
                effective_tier=effective_tier,
                consequence_tier=consequence_tier,
            )
        return _decision(
            PASS,
            "NO_PROMOTION",
            effective_tier=effective_tier,
            consequence_tier=consequence_tier,
        )

    cooling_block = _cooling_off_block(request.relaxation_evidence)
    if cooling_block is not None:
        verdict = FAIL if cooling_block.startswith("INVALID_") else BLOCKED
        return _decision(
            verdict,
            cooling_block,
            effective_tier=effective_tier,
            consequence_tier=consequence_tier,
            relaxation=True,
            added_permissions=added,
            removed_permissions=removed,
        )

    if effective_tier == TIER_A:
        evidence = request.relaxation_evidence
        if evidence is None or not evidence.tier_a_readiness_complete():
            return _decision(
                BLOCKED,
                "TIER_A_RELAXATION_READINESS_INCOMPLETE",
                effective_tier=effective_tier,
                consequence_tier=consequence_tier,
                relaxation=True,
                added_permissions=added,
                removed_permissions=removed,
            )

    # P1.0 never promotes. Readiness evidence can only prove that a later,
    # separately governed promotion could be considered; it cannot authorize it.
    return _decision(
        BLOCKED,
        "P1_0_REJECT_ALL_PROMOTION",
        effective_tier=effective_tier,
        consequence_tier=consequence_tier,
        relaxation=True,
        added_permissions=added,
        removed_permissions=removed,
    )

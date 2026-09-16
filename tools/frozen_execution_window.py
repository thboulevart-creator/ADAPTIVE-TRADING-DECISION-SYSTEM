from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path

from src.promotion_gate import (
    NATIVE_ACQUISITION_OR_REAL_BACKTEST,
    NATIVE_BI5_ACQUISITION,
    PERMISSION_INCREASE,
    TIER_A,
    PromotionRequest,
    evaluate_promotion,
)
from tools.coverage_execution_window_boundary import (
    AUTHORIZE_MASSIVE_ACQUISITION,
    BLOCKED,
    FAIL,
    FREEZE_EXECUTION_WINDOW,
    PASS,
    BoundaryDecision,
    BoundaryState,
    evaluate_boundary,
)
from tools.current_execution_window_boundary_state import (
    BoundaryEvidence,
    evaluate_current_freeze,
)

ROOT = Path(__file__).resolve().parents[1]
FREEZE_PATH = ROOT / "04-REFERENCE" / "EXECUTION-WINDOW-FREEZE.json"
FREEZE_CONTRACT = "EXECUTION_WINDOW_FREEZE_V1"
P0_1_QUALIFIED_HEAD = "bdee1cde6bc261c34f8584b2a3ec0ec460c7f898"
P0_1_FULL_SUITE_RUN = 35126075513
P0_1_PERSISTED_REBREAK_RUN = 35126075438


class PersistedFreezeError(ValueError):
    def __init__(self, verdict: str, reason: str):
        super().__init__(reason)
        self.verdict = verdict
        self.reason = reason


@dataclass(frozen=True)
class PersistedFreezeEvidence:
    record: dict
    boundary_evidence: BoundaryEvidence
    frozen_state: BoundaryState


@dataclass(frozen=True)
class PersistedFreezeEvaluation:
    evidence: PersistedFreezeEvidence | None
    decision: BoundaryDecision


def _fail(reason: str) -> None:
    raise PersistedFreezeError(FAIL, reason)


def _block(reason: str) -> None:
    raise PersistedFreezeError(BLOCKED, reason)


def _read_freeze_record() -> dict:
    try:
        value = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    except OSError:
        _block("PERSISTED_EXECUTION_WINDOW_FREEZE_MISSING")
    except json.JSONDecodeError:
        _fail("PERSISTED_EXECUTION_WINDOW_FREEZE_MALFORMED_JSON")
    if not isinstance(value, dict):
        _fail("PERSISTED_EXECUTION_WINDOW_FREEZE_NOT_OBJECT")
    return value


def _assert_exact(record: dict, key: str, expected) -> None:
    if record.get(key) != expected:
        _fail(f"PERSISTED_FREEZE_MISMATCH:{key}")


def derive_persisted_frozen_boundary() -> PersistedFreezeEvidence:
    current = evaluate_current_freeze()
    if current.evidence is None:
        _block(f"CURRENT_BOUNDARY_EVIDENCE_UNAVAILABLE:{current.decision.reason}")
    if current.decision.verdict != PASS:
        if current.decision.verdict == FAIL:
            _fail(f"CURRENT_FREEZE_ELIGIBILITY_NOT_PASS:{current.decision.reason}")
        _block(f"CURRENT_FREEZE_ELIGIBILITY_NOT_PASS:{current.decision.reason}")

    evidence = current.evidence
    state = evidence.state
    record = _read_freeze_record()

    _assert_exact(record, "schema", FREEZE_CONTRACT)
    _assert_exact(record, "status", "FROZEN")
    _assert_exact(record, "instrument", "USATECHIDXUSD")
    _assert_exact(record, "window_start", state.window_start.isoformat())
    _assert_exact(record, "window_end", state.window_end.isoformat())
    _assert_exact(record, "source_boundary_derivation_contract", evidence.derivation_contract)
    _assert_exact(record, "source_boundary_contract", evidence.boundary_rule_contract)
    _assert_exact(record, "source_selection_rule_contract", evidence.selection_rule_contract)
    _assert_exact(record, "source_qualified_head", P0_1_QUALIFIED_HEAD)
    _assert_exact(record, "source_full_suite_run", P0_1_FULL_SUITE_RUN)
    _assert_exact(record, "source_persisted_head_rebreak_run", P0_1_PERSISTED_REBREAK_RUN)
    _assert_exact(record, "source_freeze_eligibility_verdict", PASS)
    _assert_exact(
        record,
        "source_freeze_eligibility_reason",
        "EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED",
    )
    _assert_exact(record, "global_candidate_count", evidence.global_candidate_count)
    _assert_exact(record, "global_resolved_count", evidence.global_resolved_count)
    _assert_exact(record, "global_unresolved_count", state.global_unresolved_count)
    _assert_exact(record, "window_candidate_count", evidence.window_candidate_count)
    _assert_exact(record, "window_resolved_count", evidence.window_resolved_count)
    _assert_exact(record, "window_unresolved_count", state.window_unresolved_count)
    _assert_exact(record, "window_fail_count", state.window_fail_count)
    _assert_exact(record, "first_included_open_slot_utc", evidence.first_included_open_slot_utc.isoformat())
    _assert_exact(record, "last_included_open_slot_utc", evidence.last_included_open_slot_utc.isoformat())
    _assert_exact(record, "warmup_h1_bars", evidence.warmup_h1_bars)
    _assert_exact(record, "holdout_policy", evidence.holdout_policy)
    _assert_exact(record, "global_coverage_pass", False)
    _assert_exact(record, "massive_acquisition_authorized", False)
    _assert_exact(record, "real_backtest_authorized", False)

    if state.global_unresolved_count <= 0:
        _fail("OUTSIDE_GLOBAL_GAPS_NOT_PRESERVED_BY_FREEZE")
    if state.window_unresolved_count != 0 or state.window_fail_count != 0:
        _fail("PERSISTED_FREEZE_WINDOW_NO_LONGER_ADMISSIBLE")

    frozen_state = replace(
        state,
        execution_window_frozen=True,
        mandatory_window_gates_pass=False,
        acquisition_protocol_ready=False,
        explicit_acquisition_authorization=False,
    )
    return PersistedFreezeEvidence(record=record, boundary_evidence=evidence, frozen_state=frozen_state)


def evaluate_persisted_execution_window_freeze() -> PersistedFreezeEvaluation:
    try:
        evidence = derive_persisted_frozen_boundary()
    except PersistedFreezeError as exc:
        return PersistedFreezeEvaluation(
            evidence=None,
            decision=BoundaryDecision(
                FREEZE_EXECUTION_WINDOW,
                exc.verdict,
                f"PERSISTED_FREEZE:{exc.reason}",
            ),
        )

    eligibility = evaluate_boundary(FREEZE_EXECUTION_WINDOW, evidence.frozen_state)
    if eligibility.verdict != PASS:
        return PersistedFreezeEvaluation(evidence=evidence, decision=eligibility)

    return PersistedFreezeEvaluation(
        evidence=evidence,
        decision=BoundaryDecision(
            FREEZE_EXECUTION_WINDOW,
            PASS,
            "EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE",
        ),
    )


def evaluate_acquisition_after_persisted_freeze() -> BoundaryDecision:
    frozen = evaluate_persisted_execution_window_freeze()
    if frozen.evidence is None or frozen.decision.verdict != PASS:
        return BoundaryDecision(
            AUTHORIZE_MASSIVE_ACQUISITION,
            frozen.decision.verdict,
            f"PERSISTED_FREEZE_NOT_PASS:{frozen.decision.reason}",
        )

    # Preserve all pre-existing acquisition requirements first. P1.0 does not
    # replace or weaken them; it adds a final central permission boundary.
    acquisition = evaluate_boundary(
        AUTHORIZE_MASSIVE_ACQUISITION,
        frozen.evidence.frozen_state,
    )
    if acquisition.verdict != PASS:
        return acquisition

    promotion = evaluate_promotion(
        PromotionRequest(
            current_tier=TIER_A,
            target_tier=TIER_A,
            consequences=(
                PERMISSION_INCREASE,
                NATIVE_ACQUISITION_OR_REAL_BACKTEST,
            ),
            current_permissions=frozenset(),
            target_permissions=frozenset({NATIVE_BI5_ACQUISITION}),
        )
    )
    return BoundaryDecision(
        AUTHORIZE_MASSIVE_ACQUISITION,
        promotion.verdict,
        f"PROMOTION_GATE:{promotion.reason}",
    )

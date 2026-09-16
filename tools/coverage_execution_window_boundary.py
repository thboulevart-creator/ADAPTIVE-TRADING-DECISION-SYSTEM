from __future__ import annotations

from dataclasses import dataclass
from datetime import date


PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"

CONTINUE_LATER_QUALIFICATION = "CONTINUE_LATER_QUALIFICATION"
DECLARE_GLOBAL_COVERAGE_PASS = "DECLARE_GLOBAL_COVERAGE_PASS"
FREEZE_EXECUTION_WINDOW = "FREEZE_EXECUTION_WINDOW"
AUTHORIZE_MASSIVE_ACQUISITION = "AUTHORIZE_MASSIVE_ACQUISITION"

BOUNDARY_CONTRACT = "COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1"


@dataclass(frozen=True)
class BoundaryState:
    global_unresolved_count: int
    global_fail_count: int = 0

    # Prior gaps must remain visible and unchanged while later research proceeds.
    prior_gaps_preserved: bool = True
    hidden_or_reclassified_prior_gap: bool = False

    # Proposed execution-window state.
    window_start: date | None = None
    window_end: date | None = None
    window_contiguous: bool = True
    manual_date_exclusion_inside_window: bool = False
    window_selection_rationale_versioned: bool = False
    window_selection_independent_of_known_gaps: bool = False
    window_shifted_to_avoid_known_gap: bool = False
    window_candidates_enumerated: bool = False
    window_unresolved_count: int | None = None
    window_fail_count: int | None = None

    # Acquisition is deliberately a separate gate.
    execution_window_frozen: bool = False
    mandatory_window_gates_pass: bool = False
    acquisition_protocol_ready: bool = False
    explicit_acquisition_authorization: bool = False


@dataclass(frozen=True)
class BoundaryDecision:
    action: str
    verdict: str
    reason: str
    contract: str = BOUNDARY_CONTRACT


def _add_years(day: date, years: int) -> date:
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        # 29 February -> 28 February when target year is not leap.
        return day.replace(month=2, day=28, year=day.year + years)


def _common_integrity_failure(state: BoundaryState) -> BoundaryDecision | None:
    counts = [state.global_unresolved_count, state.global_fail_count]
    if state.window_unresolved_count is not None:
        counts.append(state.window_unresolved_count)
    if state.window_fail_count is not None:
        counts.append(state.window_fail_count)
    if any(value < 0 for value in counts):
        return BoundaryDecision("STATE", FAIL, "NEGATIVE_EVIDENCE_COUNT")

    if state.hidden_or_reclassified_prior_gap:
        return BoundaryDecision("STATE", FAIL, "PRIOR_GAP_HIDDEN_OR_RECLASSIFIED")

    if state.global_unresolved_count > 0 and not state.prior_gaps_preserved:
        return BoundaryDecision("STATE", FAIL, "GLOBAL_GAPS_NOT_PRESERVED")

    return None


def evaluate_boundary(action: str, state: BoundaryState) -> BoundaryDecision:
    integrity = _common_integrity_failure(state)
    if integrity is not None:
        return BoundaryDecision(action, integrity.verdict, integrity.reason)

    if action == CONTINUE_LATER_QUALIFICATION:
        return BoundaryDecision(
            action,
            PASS,
            "LATER_QUALIFICATION_MAY_CONTINUE_WITH_PRIOR_GAPS_PRESERVED",
        )

    if action == DECLARE_GLOBAL_COVERAGE_PASS:
        if state.global_fail_count > 0:
            return BoundaryDecision(action, FAIL, "GLOBAL_COVERAGE_CONTAINS_FAIL")
        if state.global_unresolved_count > 0:
            return BoundaryDecision(
                action,
                BLOCKED,
                "GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES",
            )
        return BoundaryDecision(action, PASS, "GLOBAL_COVERAGE_COMPLETE")

    if action == FREEZE_EXECUTION_WINDOW:
        if state.window_start is None or state.window_end is None:
            return BoundaryDecision(action, BLOCKED, "EXECUTION_WINDOW_NOT_DEFINED")
        if state.window_end <= state.window_start:
            return BoundaryDecision(action, FAIL, "INVALID_EXECUTION_WINDOW_ORDER")
        if state.window_end < _add_years(state.window_start, 5):
            return BoundaryDecision(action, FAIL, "EXECUTION_WINDOW_SHORTER_THAN_FIVE_YEARS")
        if not state.window_contiguous or state.manual_date_exclusion_inside_window:
            return BoundaryDecision(action, FAIL, "NON_CONTIGUOUS_OR_MANUALLY_EXCLUDED_WINDOW")
        if state.window_shifted_to_avoid_known_gap:
            return BoundaryDecision(action, FAIL, "WINDOW_SHIFTED_TO_AVOID_KNOWN_GAP")
        if not state.window_selection_independent_of_known_gaps:
            return BoundaryDecision(action, FAIL, "WINDOW_SELECTION_NOT_INDEPENDENT_OF_KNOWN_GAPS")
        if not state.window_selection_rationale_versioned:
            return BoundaryDecision(action, BLOCKED, "WINDOW_SELECTION_RATIONALE_NOT_VERSIONED")
        if not state.window_candidates_enumerated:
            return BoundaryDecision(action, BLOCKED, "WINDOW_CALENDAR_CANDIDATES_NOT_ENUMERATED")
        if state.window_unresolved_count is None or state.window_fail_count is None:
            return BoundaryDecision(action, BLOCKED, "WINDOW_EVIDENCE_COUNTS_UNKNOWN")
        if state.window_fail_count > 0:
            return BoundaryDecision(action, FAIL, "EXECUTION_WINDOW_CONTAINS_FAIL")
        if state.window_unresolved_count > 0:
            return BoundaryDecision(action, BLOCKED, "EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES")
        return BoundaryDecision(
            action,
            PASS,
            "EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED",
        )

    if action == AUTHORIZE_MASSIVE_ACQUISITION:
        if not state.execution_window_frozen:
            return BoundaryDecision(action, BLOCKED, "EXECUTION_WINDOW_NOT_FROZEN")

        freeze_decision = evaluate_boundary(FREEZE_EXECUTION_WINDOW, state)
        if freeze_decision.verdict != PASS:
            return BoundaryDecision(
                action,
                freeze_decision.verdict,
                f"WINDOW_FREEZE_NOT_PASS:{freeze_decision.reason}",
            )
        if not state.mandatory_window_gates_pass:
            return BoundaryDecision(action, BLOCKED, "MANDATORY_WINDOW_GATES_NOT_PASS")
        if not state.acquisition_protocol_ready:
            return BoundaryDecision(action, BLOCKED, "ACQUISITION_PROTOCOL_NOT_READY")
        if not state.explicit_acquisition_authorization:
            return BoundaryDecision(action, BLOCKED, "ACQUISITION_NOT_EXPLICITLY_AUTHORIZED")
        return BoundaryDecision(action, PASS, "MASSIVE_ACQUISITION_AUTHORIZED_FOR_FROZEN_WINDOW")

    return BoundaryDecision(action, FAIL, "UNKNOWN_BOUNDARY_ACTION")

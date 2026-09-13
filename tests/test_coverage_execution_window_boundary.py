from datetime import date

from tools.coverage_execution_window_boundary import (
    AUTHORIZE_MASSIVE_ACQUISITION,
    BLOCKED,
    CONTINUE_LATER_QUALIFICATION,
    DECLARE_GLOBAL_COVERAGE_PASS,
    FAIL,
    FREEZE_EXECUTION_WINDOW,
    PASS,
    BoundaryState,
    evaluate_boundary,
)


def _valid_window_state(**overrides) -> BoundaryState:
    values = dict(
        global_unresolved_count=1,
        prior_gaps_preserved=True,
        window_start=date(2020, 1, 1),
        window_end=date(2026, 8, 14),
        window_contiguous=True,
        manual_date_exclusion_inside_window=False,
        window_selection_rationale_versioned=True,
        window_selection_independent_of_known_gaps=True,
        window_shifted_to_avoid_known_gap=False,
        window_candidates_enumerated=True,
        window_unresolved_count=0,
        window_fail_count=0,
    )
    values.update(overrides)
    return BoundaryState(**values)


def test_later_qualification_may_continue_with_prior_gap_preserved() -> None:
    decision = evaluate_boundary(
        CONTINUE_LATER_QUALIFICATION,
        BoundaryState(global_unresolved_count=87, prior_gaps_preserved=True),
    )
    assert decision.verdict == PASS


def test_later_qualification_fails_if_prior_gap_is_hidden_or_reclassified() -> None:
    decision = evaluate_boundary(
        CONTINUE_LATER_QUALIFICATION,
        BoundaryState(
            global_unresolved_count=86,
            prior_gaps_preserved=True,
            hidden_or_reclassified_prior_gap=True,
        ),
    )
    assert decision.verdict == FAIL


def test_global_coverage_cannot_pass_with_unresolved_dates() -> None:
    decision = evaluate_boundary(
        DECLARE_GLOBAL_COVERAGE_PASS,
        BoundaryState(global_unresolved_count=1),
    )
    assert decision.verdict == BLOCKED


def test_global_coverage_fails_if_a_fail_date_remains() -> None:
    decision = evaluate_boundary(
        DECLARE_GLOBAL_COVERAGE_PASS,
        BoundaryState(global_unresolved_count=0, global_fail_count=1),
    )
    assert decision.verdict == FAIL


def test_independent_five_plus_year_window_can_pass_with_outside_global_gap() -> None:
    decision = evaluate_boundary(FREEZE_EXECUTION_WINDOW, _valid_window_state())
    assert decision.verdict == PASS
    assert decision.reason == "EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED"


def test_window_explicitly_shifted_to_avoid_known_gap_fails() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_shifted_to_avoid_known_gap=True),
    )
    assert decision.verdict == FAIL


def test_window_without_independent_selection_rationale_fails() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_selection_independent_of_known_gaps=False),
    )
    assert decision.verdict == FAIL


def test_unversioned_window_rationale_is_blocked() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_selection_rationale_versioned=False),
    )
    assert decision.verdict == BLOCKED


def test_window_with_unresolved_date_inside_remains_blocked() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_unresolved_count=1),
    )
    assert decision.verdict == BLOCKED


def test_window_with_fail_inside_fails() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_fail_count=1),
    )
    assert decision.verdict == FAIL


def test_manual_date_exclusion_inside_window_fails() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(manual_date_exclusion_inside_window=True),
    )
    assert decision.verdict == FAIL


def test_sub_five_year_window_fails_even_with_perfect_evidence() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_end=date(2024, 12, 31)),
    )
    assert decision.verdict == FAIL


def test_window_freeze_blocks_until_candidates_are_enumerated() -> None:
    decision = evaluate_boundary(
        FREEZE_EXECUTION_WINDOW,
        _valid_window_state(window_candidates_enumerated=False),
    )
    assert decision.verdict == BLOCKED


def test_acquisition_is_blocked_before_window_is_frozen() -> None:
    decision = evaluate_boundary(
        AUTHORIZE_MASSIVE_ACQUISITION,
        _valid_window_state(execution_window_frozen=False),
    )
    assert decision.verdict == BLOCKED


def test_continue_qualification_pass_does_not_authorize_acquisition() -> None:
    state = BoundaryState(global_unresolved_count=87, prior_gaps_preserved=True)
    assert evaluate_boundary(CONTINUE_LATER_QUALIFICATION, state).verdict == PASS
    assert evaluate_boundary(AUTHORIZE_MASSIVE_ACQUISITION, state).verdict == BLOCKED


def test_even_frozen_valid_window_needs_separate_acquisition_gates() -> None:
    decision = evaluate_boundary(
        AUTHORIZE_MASSIVE_ACQUISITION,
        _valid_window_state(execution_window_frozen=True),
    )
    assert decision.verdict == BLOCKED
    assert decision.reason == "MANDATORY_WINDOW_GATES_NOT_PASS"


def test_acquisition_can_only_pass_after_all_separate_requirements() -> None:
    decision = evaluate_boundary(
        AUTHORIZE_MASSIVE_ACQUISITION,
        _valid_window_state(
            execution_window_frozen=True,
            mandatory_window_gates_pass=True,
            acquisition_protocol_ready=True,
            explicit_acquisition_authorization=True,
        ),
    )
    assert decision.verdict == PASS


def test_unknown_action_fails_closed() -> None:
    decision = evaluate_boundary("UNKNOWN", BoundaryState(global_unresolved_count=0))
    assert decision.verdict == FAIL

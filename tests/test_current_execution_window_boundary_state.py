from __future__ import annotations

import inspect
from copy import deepcopy
from datetime import date, datetime, timezone

import tools.current_execution_window_boundary_state as current
from tools.coverage_execution_window_boundary import (
    AUTHORIZE_MASSIVE_ACQUISITION,
    BLOCKED,
    FAIL,
    FREEZE_EXECUTION_WINDOW,
    PASS,
    evaluate_boundary,
)


def test_current_boundary_state_is_derived_exactly_from_versioned_truth() -> None:
    evidence = current.derive_current_boundary_evidence()

    assert evidence.state.window_start == date(2021, 8, 14)
    assert evidence.state.window_end == date(2026, 8, 14)
    assert (evidence.global_candidate_count, evidence.global_resolved_count, len(evidence.global_unresolved_dates)) == (111, 91, 20)
    assert (evidence.window_candidate_count, evidence.window_resolved_count, len(evidence.window_unresolved_dates)) == (68, 68, 0)
    assert len(evidence.outside_window_unresolved_dates) == 20
    assert all(day < evidence.state.window_start for day in evidence.outside_window_unresolved_dates)
    assert evidence.state.global_unresolved_count == 20
    assert evidence.state.window_unresolved_count == 0
    assert evidence.state.global_fail_count == 0
    assert evidence.state.window_fail_count == 0
    assert evidence.attempt_count == 73
    assert evidence.capability_change_count == 1
    assert evidence.current_capability_id == current.CURRENT_CAPABILITY_ID
    assert evidence.current_capability_fingerprint == current.CURRENT_CAPABILITY_FINGERPRINT


def test_boundary_effects_are_derived_not_invented() -> None:
    evidence = current.derive_current_boundary_evidence()

    assert evidence.first_included_open_slot_utc == datetime(2021, 8, 15, 22, tzinfo=timezone.utc)
    assert evidence.last_included_open_slot_utc == datetime(2026, 8, 14, 20, tzinfo=timezone.utc)
    assert evidence.warmup_h1_bars == 20
    assert evidence.holdout_policy == "DEFERRED_TO_RUN_BY_VERSIONED_MOMENTUM_V1_PROTOCOL"
    assert evidence.session_calendar_contract == "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"


def test_current_freeze_evaluation_is_pass_without_claiming_global_pass_or_persisted_freeze() -> None:
    result = current.evaluate_current_freeze()

    assert result.evidence is not None
    assert result.decision.action == FREEZE_EXECUTION_WINDOW
    assert result.decision.verdict == PASS
    assert result.decision.reason == "EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED"
    assert result.evidence.state.global_unresolved_count == 20
    assert result.evidence.state.execution_window_frozen is False


def test_acquisition_remains_blocked_after_freeze_eligibility_pass() -> None:
    evidence = current.derive_current_boundary_evidence()
    decision = evaluate_boundary(AUTHORIZE_MASSIVE_ACQUISITION, evidence.state)

    assert decision.verdict == BLOCKED
    assert decision.reason == "EXECUTION_WINDOW_NOT_FROZEN"


def test_public_derivation_has_no_caller_supplied_window_report_or_boolean_surface() -> None:
    assert list(inspect.signature(current.derive_current_boundary_evidence).parameters) == []
    assert list(inspect.signature(current.evaluate_current_freeze).parameters) == []


def test_moved_window_report_without_matching_rule_evidence_fails(monkeypatch) -> None:
    real_audit = current.audit_calendar_coverage
    global_report = real_audit()
    window_report = deepcopy(real_audit(date(2021, 8, 14), date(2026, 8, 14)))
    window_report["coverage_start"] = "2021-08-15"

    def attacked(start=current.COVERAGE_START, end=current.COVERAGE_END):
        if start == current.COVERAGE_START and end == current.COVERAGE_END:
            return deepcopy(global_report)
        return deepcopy(window_report)

    monkeypatch.setattr(current, "audit_calendar_coverage", attacked)
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == FAIL
    assert "COVERAGE_REPORT_BOUNDARY_MISMATCH" in result.decision.reason


def test_omitted_in_window_candidate_fails_closed(monkeypatch) -> None:
    real_audit = current.audit_calendar_coverage
    global_report = real_audit()
    window_report = deepcopy(real_audit(date(2021, 8, 14), date(2026, 8, 14)))
    window_report["candidate_dates"] -= 1
    window_report["resolved_candidate_dates"] -= 1

    def attacked(start=current.COVERAGE_START, end=current.COVERAGE_END):
        if start == current.COVERAGE_START and end == current.COVERAGE_END:
            return deepcopy(global_report)
        return deepcopy(window_report)

    monkeypatch.setattr(current, "audit_calendar_coverage", attacked)
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == FAIL
    assert "CANDIDATE_ENUMERATION_MISMATCH" in result.decision.reason


def test_unresolved_candidate_cannot_be_hidden_by_count_tampering(monkeypatch) -> None:
    real_audit = current.audit_calendar_coverage
    global_report = real_audit()
    window_report = deepcopy(real_audit(date(2021, 8, 14), date(2026, 8, 14)))
    window_report["unresolved"] = [{"date": "2024-01-01", "reason": "ATTACK"}]
    window_report["unresolved_candidate_dates"] = 0

    def attacked(start=current.COVERAGE_START, end=current.COVERAGE_END):
        if start == current.COVERAGE_START and end == current.COVERAGE_END:
            return deepcopy(global_report)
        return deepcopy(window_report)

    monkeypatch.setattr(current, "audit_calendar_coverage", attacked)
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == FAIL
    assert "UNRESOLVED_COUNT_LIST_MISMATCH" in result.decision.reason


def test_outside_global_gaps_remain_visible_in_freeze_pass() -> None:
    result = current.evaluate_current_freeze()
    evidence = result.evidence

    assert evidence is not None
    assert result.decision.verdict == PASS
    assert evidence.state.global_unresolved_count == 20
    assert evidence.state.prior_gaps_preserved is True
    assert len(evidence.outside_window_unresolved_dates) == 20
    assert evidence.window_unresolved_dates == ()


def test_stale_application_report_is_not_a_current_derivation_input() -> None:
    source = inspect.getsource(current)
    assert "current_coverage_execution_window_boundary_application" not in source
    assert "37" not in source
    assert "31" not in source


def test_recovery_progression_mismatch_fails_closed(monkeypatch) -> None:
    capabilities, current_id, attempts = current.load_attempt_ledger()

    monkeypatch.setattr(
        current,
        "load_attempt_ledger",
        lambda: (capabilities, current_id, attempts[:-1]),
    )
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == FAIL
    assert "RECOVERY_ATTEMPT_COUNT_MISMATCH" in result.decision.reason


def test_provenance_identity_mismatch_fails_closed(monkeypatch) -> None:
    attacked = deepcopy(current.NO_SPECIAL_CHANGE_EVIDENCE)
    attacked[date(2022, 7, 1)]["instrument_id"] = "ATTACK"
    monkeypatch.setattr(current, "NO_SPECIAL_CHANGE_EVIDENCE", attacked)

    result = current.evaluate_current_freeze()

    assert result.decision.verdict == FAIL
    assert "NEGATIVE_EVIDENCE_INSTRUMENT_IDENTITY_MISMATCH" in result.decision.reason


def test_missing_gap_independence_contract_blocks_freeze(monkeypatch) -> None:
    original = current._read_required

    def attacked(path):
        text = original(path)
        if path == current.SELECTION_RULE_PATH:
            return text.replace("unresolved calendar dates;", "removed marker;")
        return text

    monkeypatch.setattr(current, "_read_required", attacked)
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == BLOCKED
    assert "SELECTION_RULE_NOT_PROVABLY_GAP_INDEPENDENT" in result.decision.reason


def test_missing_boundary_effect_policy_blocks_freeze(monkeypatch) -> None:
    original = current._read_required

    def attacked(path):
        text = original(path)
        if path == current.MOMENTUM_PROTOCOL_PATH:
            return text.replace("The exact split dates are persisted with the run.", "missing")
        return text

    monkeypatch.setattr(current, "_read_required", attacked)
    result = current.evaluate_current_freeze()

    assert result.decision.verdict == BLOCKED
    assert "MOMENTUM_BOUNDARY_EFFECT_POLICY_INCOMPLETE" in result.decision.reason


def test_derivation_contains_no_network_probe_or_bi5_acquisition_surface() -> None:
    source = inspect.getsource(current).lower()

    assert "requests." not in source
    assert "playwright" not in source
    assert "selenium" not in source
    assert "probe_candidate" not in source
    assert ".bi5" not in source

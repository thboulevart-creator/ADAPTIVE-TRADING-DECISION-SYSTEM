from __future__ import annotations

import inspect
from copy import deepcopy
from datetime import date

import tools.frozen_execution_window as frozen
from tools.coverage_execution_window_boundary import BLOCKED, FAIL, FREEZE_EXECUTION_WINDOW, PASS
from tools.current_execution_window_boundary_state import CurrentFreezeEvaluation


def test_persisted_execution_window_freeze_is_exact_and_durable() -> None:
    result = frozen.evaluate_persisted_execution_window_freeze()

    assert result.evidence is not None
    assert result.decision.action == FREEZE_EXECUTION_WINDOW
    assert result.decision.verdict == PASS
    assert result.decision.reason == "EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE"
    assert result.evidence.frozen_state.window_start == date(2021, 8, 14)
    assert result.evidence.frozen_state.window_end == date(2026, 8, 14)
    assert result.evidence.frozen_state.execution_window_frozen is True
    assert result.evidence.frozen_state.global_unresolved_count == 20
    assert result.evidence.frozen_state.window_unresolved_count == 0
    assert result.evidence.frozen_state.window_fail_count == 0


def test_persisted_freeze_is_bound_to_p0_1_qualification_identity() -> None:
    evidence = frozen.derive_persisted_frozen_boundary()
    record = evidence.record

    assert record["source_qualified_head"] == frozen.P0_1_QUALIFIED_HEAD
    assert record["source_full_suite_run"] == frozen.P0_1_FULL_SUITE_RUN
    assert record["source_persisted_head_rebreak_run"] == frozen.P0_1_PERSISTED_REBREAK_RUN
    assert record["source_boundary_derivation_contract"] == "CURRENT_EXECUTION_WINDOW_BOUNDARY_STATE_DERIVATION_V1"
    assert record["source_freeze_eligibility_verdict"] == PASS


def test_freeze_does_not_promote_global_coverage_or_authorize_acquisition() -> None:
    evidence = frozen.derive_persisted_frozen_boundary()
    acquisition = frozen.evaluate_acquisition_after_persisted_freeze()

    assert evidence.record["global_coverage_pass"] is False
    assert evidence.record["massive_acquisition_authorized"] is False
    assert evidence.record["real_backtest_authorized"] is False
    assert evidence.frozen_state.global_unresolved_count == 20
    assert acquisition.verdict == BLOCKED
    assert acquisition.reason == "MANDATORY_WINDOW_GATES_NOT_PASS"


def test_public_freeze_surface_has_no_caller_supplied_record_or_window() -> None:
    assert list(inspect.signature(frozen.derive_persisted_frozen_boundary).parameters) == []
    assert list(inspect.signature(frozen.evaluate_persisted_execution_window_freeze).parameters) == []


def test_tampered_window_start_fails_closed(monkeypatch) -> None:
    record = deepcopy(frozen._read_freeze_record())
    record["window_start"] = "2021-08-15"
    monkeypatch.setattr(frozen, "_read_freeze_record", lambda: record)

    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == FAIL
    assert "PERSISTED_FREEZE_MISMATCH:window_start" in result.decision.reason


def test_tampered_window_end_fails_closed(monkeypatch) -> None:
    record = deepcopy(frozen._read_freeze_record())
    record["window_end"] = "2026-08-13"
    monkeypatch.setattr(frozen, "_read_freeze_record", lambda: record)

    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == FAIL
    assert "PERSISTED_FREEZE_MISMATCH:window_end" in result.decision.reason


def test_tampered_global_gap_count_fails_closed(monkeypatch) -> None:
    record = deepcopy(frozen._read_freeze_record())
    record["global_unresolved_count"] = 0
    monkeypatch.setattr(frozen, "_read_freeze_record", lambda: record)

    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == FAIL
    assert "PERSISTED_FREEZE_MISMATCH:global_unresolved_count" in result.decision.reason


def test_tampered_source_head_fails_closed(monkeypatch) -> None:
    record = deepcopy(frozen._read_freeze_record())
    record["source_qualified_head"] = "0" * 40
    monkeypatch.setattr(frozen, "_read_freeze_record", lambda: record)

    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == FAIL
    assert "PERSISTED_FREEZE_MISMATCH:source_qualified_head" in result.decision.reason


def test_artifact_cannot_self_authorize_acquisition(monkeypatch) -> None:
    record = deepcopy(frozen._read_freeze_record())
    record["massive_acquisition_authorized"] = True
    monkeypatch.setattr(frozen, "_read_freeze_record", lambda: record)

    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == FAIL
    assert "PERSISTED_FREEZE_MISMATCH:massive_acquisition_authorized" in result.decision.reason


def test_current_boundary_regression_blocks_persisted_freeze(monkeypatch) -> None:
    original = frozen.evaluate_current_freeze()
    attacked = deepcopy(original.evidence)
    assert attacked is not None
    attacked_state = deepcopy(attacked.state)
    object.__setattr__(attacked_state, "window_unresolved_count", 1)
    object.__setattr__(attacked, "state", attacked_state)

    monkeypatch.setattr(
        frozen,
        "evaluate_current_freeze",
        lambda: CurrentFreezeEvaluation(
            evidence=attacked,
            decision=frozen.BoundaryDecision(FREEZE_EXECUTION_WINDOW, BLOCKED, "ATTACK"),
        ),
    )
    result = frozen.evaluate_persisted_execution_window_freeze()
    assert result.decision.verdict == BLOCKED
    assert "CURRENT_FREEZE_ELIGIBILITY_NOT_PASS" in result.decision.reason


def test_freeze_module_contains_no_acquisition_or_backtest_execution_surface() -> None:
    source = inspect.getsource(frozen).lower()

    assert "requests." not in source
    assert "playwright" not in source
    assert "selenium" not in source
    assert "subprocess" not in source
    assert "download" not in source
    assert "strategy tester" not in source

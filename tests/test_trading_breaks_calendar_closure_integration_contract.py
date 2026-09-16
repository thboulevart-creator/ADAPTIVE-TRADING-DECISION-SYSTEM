from __future__ import annotations

import inspect
from datetime import date
from pathlib import Path

import pytest

import tools.integrate_trading_breaks_calendar_closure as closure


def test_exact_membership_is_nine_class_a_plus_three_class_b() -> None:
    assert len(closure.CLASS_A_PENDING) == 9
    assert len(closure.CLASS_B) == 3
    assert len(closure.EXPECTED_QUEUE) == 12
    assert set(closure.CLASS_A_PENDING).isdisjoint(set(closure.CLASS_B))
    assert closure.EXPECTED_QUEUE == (
        closure.CLASS_B[0],
        closure.CLASS_B[1],
        *closure.CLASS_A_PENDING,
        closure.CLASS_B[2],
    )


def test_current_persisted_preintegration_state_matches_exact_contract() -> None:
    closure.guard_preintegration_state()


def test_class_a_sources_are_qualified_and_bound_to_immutable_attempts() -> None:
    items = closure.authoritative_class_a()
    assert [(date.fromisoformat(x["target_date"]), x["candidate_reason"]) for x in items] == list(
        closure.CLASS_A_PENDING
    )
    assert len(items) == 9
    for item in items:
        assert item["verdict"] == "PASS"
        assert item["reason"] == "TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED"
        assert item["source_attempt_id"].startswith("batch")
        assert item["record_id"]
        assert item["broker_reason"]
        assert item["artifact_id"] > 0
        assert len(item["artifact_sha256"]) == 64
        assert len(item["probe_commit"]) == 40


def test_class_b_sources_are_qualified_without_fabricating_new_attempts() -> None:
    items = closure.authoritative_class_b()
    assert [(date.fromisoformat(x["target_date"]), x["candidate_reason"]) for x in items] == list(
        closure.CLASS_B
    )
    assert len(items[0]["source_attempt_ids"]) == 2
    assert len(items[1]["source_attempt_ids"]) == 1
    assert len(items[2]["source_attempt_ids"]) == 1
    assert items[0]["source_attempt_ids"] == (
        "batch01:2021-12-31",
        "batch02:2021-12-31",
    )
    assert items[1]["source_attempt_ids"] == ("batch03:2022-07-01",)
    assert items[2]["source_attempt_ids"] == ("batch14:2026-07-02",)


def test_class_a_rendering_preserves_v2_semantic_binding() -> None:
    rendered = "".join(closure.render_class_a_entry(x) for x in closure.authoritative_class_a())
    assert rendered.count('"target_day_overlap_capability": "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"') == 9
    assert rendered.count(closure.READJUDICATION_REPORT_SOURCE) == 9
    for token in closure.CLASS_A_REASON_TOKENS.values():
        assert token in rendered


def test_class_b_rendering_is_no_change_evidence_not_special_session_fabrication() -> None:
    rendered = "".join(closure.render_class_b_entry(x) for x in closure.authoritative_class_b())
    assert rendered.count(closure.NEGATIVE_CONTRACT) == 3
    assert rendered.count(closure.NEGATIVE_PASS_REASON) == 3
    assert rendered.count(closure.NEGATIVE_REPORT_SOURCE) == 3
    assert "fully_closed_hours_utc" not in rendered
    assert "broker_record_id" not in rendered
    assert closure.NO_CHANGE_REASON in rendered


def test_guard_rejects_manual_queue_omission(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(closure, "recovery_queue", lambda: list(closure.EXPECTED_QUEUE[:-1]))
    with pytest.raises(RuntimeError, match="PRE_CLOSURE_QUEUE_MISMATCH"):
        closure.guard_preintegration_state()


def test_guard_rejects_class_b_manual_retry_eligibility(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        closure,
        "eligible_recovery_queue",
        lambda: [closure.CLASS_B[0], *closure.CLASS_A_PENDING],
    )
    with pytest.raises(RuntimeError, match="PRE_CLOSURE_ELIGIBLE_QUEUE_MISMATCH"):
        closure.guard_preintegration_state()


def test_guard_rejects_preexisting_no_change_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        closure.NO_SPECIAL_CHANGE_EVIDENCE,
        date(2020, 1, 2),
        {"reason": "synthetic"},
    )
    with pytest.raises(RuntimeError, match="PRE_CLOSURE_NO_SPECIAL_CHANGE_EVIDENCE_NOT_EMPTY"):
        closure.guard_preintegration_state()


def test_replace_once_fails_closed_on_missing_or_ambiguous_marker() -> None:
    with pytest.raises(RuntimeError, match="expected exactly one match, found 0"):
        closure.replace_once("abc", "z", "x", "missing")
    with pytest.raises(RuntimeError, match="expected exactly one match, found 2"):
        closure.replace_once("aa", "a", "x", "duplicate")


def test_integration_source_contains_no_live_broker_acquisition_path() -> None:
    source = Path(closure.__file__).read_text(encoding="utf-8").lower()
    for token in ("playwright", "selenium", "requests.", "urllib.request", "probe_candidate"):
        assert token not in source


def test_class_b_contract_does_not_promote_matching_records_empty_directly() -> None:
    class_b_source = (
        inspect.getsource(closure.authoritative_class_b)
        + inspect.getsource(closure.render_class_b_entry)
    )
    assert "matching_records" not in class_b_source
    full_source = Path(closure.__file__).read_text(encoding="utf-8")
    assert "CONTRACT as NEGATIVE_CONTRACT" in full_source
    assert "NEGATIVE_REPORT_SOURCE" in class_b_source
    assert closure.NEGATIVE_CONTRACT == "TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1"

from datetime import date

from tools.dukascopy_usatech_calendar_coverage import (
    NO_SPECIAL_CHANGE_EVIDENCE,
    audit_calendar_coverage,
)
from tools.trading_breaks_recovery_progression import (
    current_capability,
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue

WINDOW_START = date(2021, 8, 14)
WINDOW_END = date(2026, 8, 14)
V2_ID = "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"
V2_FINGERPRINT = "e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31"
CLASS_B_DATES = {
    date(2021, 12, 31),
    date(2022, 7, 1),
    date(2026, 7, 2),
}


def test_post_closure_calendar_current_truth_is_exact() -> None:
    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(WINDOW_START, WINDOW_END)

    assert (
        global_report["candidate_dates"],
        global_report["resolved_candidate_dates"],
        global_report["unresolved_candidate_dates"],
    ) == (111, 91, 20)
    assert global_report["special_session_evidence_dates"] == 88
    assert global_report["no_special_change_evidence_dates"] == 3
    assert global_report["verdict"] == "BLOCKED"
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []
    assert global_report["evidence_shape_errors"] == []
    assert all(
        date.fromisoformat(item["date"]) < WINDOW_START
        for item in global_report["unresolved"]
    )

    assert (
        window_report["candidate_dates"],
        window_report["resolved_candidate_dates"],
        window_report["unresolved_candidate_dates"],
    ) == (68, 68, 0)
    assert window_report["verdict"] == "PASS"
    assert window_report["unresolved"] == []
    assert window_report["orphan_special_evidence"] == []
    assert window_report["contradictory_evidence_dates"] == []
    assert window_report["evidence_shape_errors"] == []


def test_post_closure_recovery_state_is_terminal_without_erasing_history() -> None:
    capabilities, current_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()

    assert current_id == V2_ID
    assert current_id in capabilities
    assert current_capability().fingerprint() == V2_FINGERPRINT
    assert len(attempts) == 73
    assert [item.attempt_sequence for item in attempts] == list(range(1, 74))
    assert len({item.attempt_id for item in attempts}) == 73
    assert len(changes) == 1
    assert recovery_queue() == []
    assert progression_decisions() == []
    assert eligible_recovery_queue() == []


def test_post_closure_negative_evidence_is_exactly_class_b() -> None:
    assert set(NO_SPECIAL_CHANGE_EVIDENCE) == CLASS_B_DATES
    for day in sorted(CLASS_B_DATES):
        record = NO_SPECIAL_CHANGE_EVIDENCE[day]
        assert record["negative_evidence_contract"] == "TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1"
        assert record["negative_evidence_reason"] == "NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY"
        assert record["instrument_name"] == "USATECH.IDX/USD"
        assert record["instrument_id"] == "9016"
        assert record["source_attempt_ids"]
        assert record["source_artifact_ids"]
        assert record["source_artifact_sha256s"]
        assert record["source_probe_commits"]
        assert record["source_workflow_runs"]
        assert record["runtime_evidence_sources"]
        assert record["qualification_report_source"] == "reports/data-qualification/trading_breaks_negative_evidence_completeness_qualification.md"

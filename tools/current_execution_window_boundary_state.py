from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from tools.coverage_execution_window_boundary import (
    BLOCKED,
    FAIL,
    FREEZE_EXECUTION_WINDOW,
    BoundaryDecision,
    BoundaryState,
    evaluate_boundary,
)
from tools.dukascopy_usatech_calendar import (
    CALENDAR_CONTRACT,
    EXPECTED_OPEN,
    classify_slot,
)
from tools.dukascopy_usatech_calendar_coverage import (
    COVERAGE_CONTRACT,
    COVERAGE_END,
    COVERAGE_START,
    NO_SPECIAL_CHANGE_EVIDENCE,
    audit_calendar_coverage,
    candidate_special_dates,
)
from tools.trading_breaks_recovery_progression import (
    current_capability,
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue

ROOT = Path(__file__).resolve().parents[1]
SELECTION_RULE_PATH = ROOT / "04-REFERENCE" / "EXECUTION-WINDOW-SELECTION-RULE.md"
BOUNDARY_RULE_PATH = ROOT / "04-REFERENCE" / "COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md"
MOMENTUM_PROTOCOL_PATH = ROOT / "docs" / "03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md"

SELECTION_RULE_CONTRACT = "EXECUTION_WINDOW_SELECTION_RULE_V1"
BOUNDARY_RULE_CONTRACT = "COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1"
MOMENTUM_PROTOCOL_MARKER = "3.1.2 — MOMENTUM V1 — PREMIER BACKTEST BASELINE PROTOCOL"
DERIVATION_CONTRACT = "CURRENT_EXECUTION_WINDOW_BOUNDARY_STATE_DERIVATION_V1"
HOLDOUT_POLICY = "DEFERRED_TO_RUN_BY_VERSIONED_MOMENTUM_V1_PROTOCOL"
WARMUP_H1_BARS = 20
CURRENT_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"
CURRENT_CAPABILITY_FINGERPRINT = "e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31"
NEGATIVE_EVIDENCE_CONTRACT = "TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1"
CLASS_B_DATES = frozenset((date(2021, 12, 31), date(2022, 7, 1), date(2026, 7, 2)))


class BoundaryDerivationError(ValueError):
    def __init__(self, verdict: str, reason: str):
        super().__init__(reason)
        self.verdict = verdict
        self.reason = reason


@dataclass(frozen=True)
class BoundaryEvidence:
    state: BoundaryState
    coverage_start: date
    coverage_end: date
    first_included_open_slot_utc: datetime
    last_included_open_slot_utc: datetime
    warmup_h1_bars: int
    holdout_policy: str
    global_candidate_count: int
    global_resolved_count: int
    global_unresolved_dates: tuple[date, ...]
    window_candidate_count: int
    window_resolved_count: int
    window_unresolved_dates: tuple[date, ...]
    outside_window_unresolved_dates: tuple[date, ...]
    attempt_count: int
    capability_change_count: int
    current_capability_id: str
    current_capability_fingerprint: str
    selection_rule_contract: str
    boundary_rule_contract: str
    session_calendar_contract: str
    coverage_contract: str
    derivation_contract: str = DERIVATION_CONTRACT


@dataclass(frozen=True)
class CurrentFreezeEvaluation:
    evidence: BoundaryEvidence | None
    decision: BoundaryDecision


def _fail(reason: str) -> None:
    raise BoundaryDerivationError(FAIL, reason)


def _block(reason: str) -> None:
    raise BoundaryDerivationError(BLOCKED, reason)


def _subtract_calendar_years(day: date, years: int) -> date:
    try:
        return day.replace(year=day.year - years)
    except ValueError:
        return day.replace(year=day.year - years, month=2, day=28)


def _read_required(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        _block(f"MISSING_VERSIONED_EVIDENCE:{path.as_posix()}")


def _require_markers(text: str, markers: tuple[str, ...], reason: str) -> None:
    if any(marker not in text for marker in markers):
        _block(reason)


def _report_dates(report: dict) -> tuple[date, ...]:
    unresolved = report.get("unresolved")
    if not isinstance(unresolved, list):
        _fail("MALFORMED_UNRESOLVED_LIST")
    values: list[date] = []
    for item in unresolved:
        if not isinstance(item, dict) or not isinstance(item.get("date"), str):
            _fail("MALFORMED_UNRESOLVED_RECORD")
        try:
            values.append(date.fromisoformat(item["date"]))
        except ValueError:
            _fail("MALFORMED_UNRESOLVED_DATE")
    if len(values) != len(set(values)):
        _fail("DUPLICATE_UNRESOLVED_DATE")
    return tuple(sorted(values))


def _validate_coverage_report(report: dict, expected_start: date, expected_end: date) -> tuple[date, ...]:
    if report.get("schema") != COVERAGE_CONTRACT or report.get("instrument") != "USATECHIDXUSD":
        _fail("COVERAGE_REPORT_IDENTITY_MISMATCH")
    if report.get("coverage_start") != expected_start.isoformat() or report.get("coverage_end") != expected_end.isoformat():
        _fail("COVERAGE_REPORT_BOUNDARY_MISMATCH")

    unresolved = _report_dates(report)
    if report.get("unresolved_candidate_dates") != len(unresolved):
        _fail("UNRESOLVED_COUNT_LIST_MISMATCH")

    candidate_count = report.get("candidate_dates")
    resolved_count = report.get("resolved_candidate_dates")
    expected_candidates = len(candidate_special_dates(expected_start, expected_end))
    if not isinstance(candidate_count, int) or not isinstance(resolved_count, int):
        _fail("MALFORMED_COVERAGE_COUNTS")
    if candidate_count != expected_candidates:
        _fail("CANDIDATE_ENUMERATION_MISMATCH")
    if resolved_count + len(unresolved) != candidate_count:
        _fail("COVERAGE_ACCOUNTING_MISMATCH")

    keys = ("contradictory_evidence_dates", "evidence_shape_errors", "orphan_special_evidence")
    if any(not isinstance(report.get(key), list) for key in keys):
        _fail("MALFORMED_EVIDENCE_INTEGRITY_LIST")
    defects = sum(len(report[key]) for key in keys)
    expected_verdict = FAIL if defects else (BLOCKED if unresolved else "PASS")
    if report.get("verdict") != expected_verdict:
        _fail("COVERAGE_VERDICT_STATE_MISMATCH")
    return unresolved


def _first_open_slot(start: date, end: date) -> datetime:
    day = start
    while day <= end:
        for hour in range(24):
            if classify_slot(day, hour).status == EXPECTED_OPEN:
                return datetime.combine(day, time(hour, tzinfo=timezone.utc))
        day += timedelta(days=1)
    _block("NO_OPEN_SLOT_INSIDE_WINDOW")


def _last_open_slot(start: date, end: date) -> datetime:
    day = end
    while day >= start:
        for hour in range(23, -1, -1):
            if classify_slot(day, hour).status == EXPECTED_OPEN:
                return datetime.combine(day, time(hour, tzinfo=timezone.utc))
        day -= timedelta(days=1)
    _block("NO_OPEN_SLOT_INSIDE_WINDOW")


def _validate_negative_evidence() -> None:
    if set(NO_SPECIAL_CHANGE_EVIDENCE) != set(CLASS_B_DATES):
        _fail("NEGATIVE_EVIDENCE_MEMBERSHIP_MISMATCH")
    required = (
        "source_attempt_ids", "source_artifact_ids", "source_artifact_sha256s",
        "source_probe_commits", "source_workflow_runs", "runtime_evidence_sources",
    )
    for day in sorted(CLASS_B_DATES):
        record = NO_SPECIAL_CHANGE_EVIDENCE[day]
        if record.get("negative_evidence_contract") != NEGATIVE_EVIDENCE_CONTRACT:
            _fail("NEGATIVE_EVIDENCE_CONTRACT_MISMATCH")
        if record.get("negative_evidence_reason") != "NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY":
            _fail("NEGATIVE_EVIDENCE_REASON_MISMATCH")
        if record.get("instrument_name") != "USATECH.IDX/USD" or record.get("instrument_id") != "9016":
            _fail("NEGATIVE_EVIDENCE_INSTRUMENT_IDENTITY_MISMATCH")
        if any(not record.get(key) for key in required):
            _fail("NEGATIVE_EVIDENCE_PROVENANCE_INCOMPLETE")


def _recovery_snapshot() -> tuple[int, int, str, str]:
    capabilities, current_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()
    if current_id != CURRENT_CAPABILITY_ID or current_id not in capabilities:
        _fail("RECOVERY_CURRENT_CAPABILITY_MISMATCH")
    fingerprint = current_capability().fingerprint()
    if fingerprint != CURRENT_CAPABILITY_FINGERPRINT:
        _fail("RECOVERY_CAPABILITY_FINGERPRINT_MISMATCH")
    if len(attempts) != 73:
        _fail("RECOVERY_ATTEMPT_COUNT_MISMATCH")
    if [item.attempt_sequence for item in attempts] != list(range(1, 74)):
        _fail("RECOVERY_ATTEMPT_SEQUENCE_MISMATCH")
    if len({item.attempt_id for item in attempts}) != 73:
        _fail("RECOVERY_ATTEMPT_IDENTITY_MISMATCH")
    if len(changes) != 1:
        _fail("RECOVERY_CAPABILITY_CHANGE_COUNT_MISMATCH")
    if recovery_queue() or progression_decisions() or eligible_recovery_queue():
        _fail("RECOVERY_PROGRESSION_NOT_TERMINAL")
    return len(attempts), len(changes), current_id, fingerprint


def _versioned_policy_evidence() -> None:
    selection = _read_required(SELECTION_RULE_PATH)
    boundary = _read_required(BOUNDARY_RULE_PATH)
    momentum = _read_required(MOMENTUM_PROTOCOL_PATH)
    _require_markers(selection, (
        SELECTION_RULE_CONTRACT,
        "candidate_end = coverage_end",
        "candidate_start = candidate_end shifted backward by exactly 5 calendar years",
        "Inputs forbidden:",
        "unresolved calendar dates;",
        "the interval is contiguous; no date may be manually removed;",
        "It does not choose the OOS split.",
    ), "SELECTION_RULE_NOT_PROVABLY_GAP_INDEPENDENT")
    _require_markers(boundary, (
        BOUNDARY_RULE_CONTRACT,
        "FREEZE_EXECUTION_WINDOW",
        "unresolved candidate count inside the proposed window is zero",
        "FAIL candidate count inside the proposed window is zero",
        "global gaps outside the window remain visible",
    ), "BOUNDARY_RULE_CONTRACT_INCOMPLETE")
    _require_markers(momentum, (
        MOMENTUM_PROTOCOL_MARKER,
        "Horizon: 20 completed H1 bars",
        "The execution window must be fixed before results are observed.",
        "The exact split dates are persisted with the run.",
        "No result may be used to move the split.",
        "No synthetic extension, copied month, interpolation, silent fallback, or substitution is allowed.",
    ), "MOMENTUM_BOUNDARY_EFFECT_POLICY_INCOMPLETE")
    if CALENDAR_CONTRACT != "DUKASCOPY_USATECH_SESSION_CALENDAR_V3":
        _fail("SESSION_CALENDAR_CONTRACT_MISMATCH")


def derive_current_boundary_evidence() -> BoundaryEvidence:
    _versioned_policy_evidence()

    window_end = COVERAGE_END
    window_start = _subtract_calendar_years(window_end, 5)
    if window_start < COVERAGE_START:
        _block("INSUFFICIENT_GOVERNED_HISTORY_FOR_PRIMARY_WINDOW")

    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(window_start, window_end)
    global_unresolved = _validate_coverage_report(global_report, COVERAGE_START, COVERAGE_END)
    window_unresolved = _validate_coverage_report(window_report, window_start, window_end)

    outside = tuple(day for day in global_unresolved if not (window_start <= day <= window_end))
    projected_inside = tuple(day for day in global_unresolved if window_start <= day <= window_end)
    if projected_inside != window_unresolved:
        _fail("GLOBAL_WINDOW_UNRESOLVED_PROJECTION_MISMATCH")
    if len(outside) + len(window_unresolved) != len(global_unresolved):
        _fail("GLOBAL_GAP_VISIBILITY_MISMATCH")

    _validate_negative_evidence()
    attempt_count, change_count, current_id, fingerprint = _recovery_snapshot()

    global_defects = sum(len(global_report[k]) for k in (
        "contradictory_evidence_dates", "evidence_shape_errors", "orphan_special_evidence"))
    window_defects = sum(len(window_report[k]) for k in (
        "contradictory_evidence_dates", "evidence_shape_errors", "orphan_special_evidence"))

    state = BoundaryState(
        global_unresolved_count=len(global_unresolved),
        global_fail_count=global_defects,
        prior_gaps_preserved=True,
        hidden_or_reclassified_prior_gap=False,
        window_start=window_start,
        window_end=window_end,
        window_contiguous=True,
        manual_date_exclusion_inside_window=False,
        window_selection_rationale_versioned=True,
        window_selection_independent_of_known_gaps=True,
        window_shifted_to_avoid_known_gap=False,
        window_candidates_enumerated=True,
        window_unresolved_count=len(window_unresolved),
        window_fail_count=window_defects,
        execution_window_frozen=False,
        mandatory_window_gates_pass=False,
        acquisition_protocol_ready=False,
        explicit_acquisition_authorization=False,
    )
    return BoundaryEvidence(
        state=state,
        coverage_start=COVERAGE_START,
        coverage_end=COVERAGE_END,
        first_included_open_slot_utc=_first_open_slot(window_start, window_end),
        last_included_open_slot_utc=_last_open_slot(window_start, window_end),
        warmup_h1_bars=WARMUP_H1_BARS,
        holdout_policy=HOLDOUT_POLICY,
        global_candidate_count=global_report["candidate_dates"],
        global_resolved_count=global_report["resolved_candidate_dates"],
        global_unresolved_dates=global_unresolved,
        window_candidate_count=window_report["candidate_dates"],
        window_resolved_count=window_report["resolved_candidate_dates"],
        window_unresolved_dates=window_unresolved,
        outside_window_unresolved_dates=outside,
        attempt_count=attempt_count,
        capability_change_count=change_count,
        current_capability_id=current_id,
        current_capability_fingerprint=fingerprint,
        selection_rule_contract=SELECTION_RULE_CONTRACT,
        boundary_rule_contract=BOUNDARY_RULE_CONTRACT,
        session_calendar_contract=CALENDAR_CONTRACT,
        coverage_contract=COVERAGE_CONTRACT,
    )


def evaluate_current_freeze() -> CurrentFreezeEvaluation:
    try:
        evidence = derive_current_boundary_evidence()
    except BoundaryDerivationError as exc:
        return CurrentFreezeEvaluation(
            evidence=None,
            decision=BoundaryDecision(FREEZE_EXECUTION_WINDOW, exc.verdict, f"BOUNDARY_STATE_DERIVATION:{exc.reason}"),
        )
    return CurrentFreezeEvaluation(
        evidence=evidence,
        decision=evaluate_boundary(FREEZE_EXECUTION_WINDOW, evidence.state),
    )

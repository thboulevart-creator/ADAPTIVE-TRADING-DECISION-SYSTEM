from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch06 as batch06_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch06 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH06_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch06_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH06 = [
    (date(2023, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2023, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
    (date(2023, 9, 4), "LABOR_DAY"),
    (date(2023, 11, 23), "THANKSGIVING_DAY"),
    (date(2023, 11, 24), "THANKSGIVING_FRIDAY"),
]
PASS_DAYS = {date(2023, 7, 3), date(2023, 9, 4), date(2023, 11, 23), date(2023, 11, 24)}
BLOCKED_DAY = date(2023, 7, 4)


def test_batch06_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH06_TARGETS, tuple)
    assert batch06_targets() == EXPECTED_BATCH06


def test_batch06_historical_membership_is_not_rederived_post_integration():
    first = batch06_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch06_targets() == EXPECTED_BATCH06
    assert PASS_DAYS.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_batch06_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY in raw_days


def test_batch06_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch06 = [item for item in attempts if item.attempt_id.startswith("batch06:")]
    assert len(attempts) == 35
    assert [item.attempt_sequence for item in batch06] == [26, 27, 28, 29, 30]
    assert [item.target_date for item in batch06] == [day for day, _ in EXPECTED_BATCH06]
    assert [item.outcome for item in batch06] == ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]
    assert batch06[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch06)


def test_batch06_blocked_july4_remains_unresolved_and_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decision = {item.target_date: item for item in progression_decisions()}[BLOCKED_DAY]
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decision.eligible is False
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch06_remains_valid_in_post_batch07_progression_state():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 42
    assert len(attempts) == 35
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 9
    assert len(eligible) == 33
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2024, 2, 19)


def test_batch06_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "289d7f4432efba4ad2bc1e97d5b23f14f587019e"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "99c2f38842a0c4ea66ba6ff90496380986d02e52"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "70428e536689793a74420d35c84744b8ad0f2f3d"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch06_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch06_targets).parameters == {}
    source = inspect.getsource(batch06_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source

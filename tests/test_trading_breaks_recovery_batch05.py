from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch05 as batch05_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch05 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH05_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch05_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH05 = [
    (date(2023, 1, 16), "MARTIN_LUTHER_KING_DAY"),
    (date(2023, 2, 20), "PRESIDENTS_DAY"),
    (date(2023, 4, 7), "GOOD_FRIDAY"),
    (date(2023, 5, 29), "MEMORIAL_DAY"),
    (date(2023, 6, 19), "JUNETEENTH_OBSERVED"),
]
PASS_DAYS = {day for day, _ in EXPECTED_BATCH05}
ATTEMPTED_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),
}


def test_batch05_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH05_TARGETS, tuple)
    assert batch05_targets() == EXPECTED_BATCH05


def test_batch05_historical_membership_is_immutable_and_not_rederived_post_integration():
    first = batch05_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch05_targets() == EXPECTED_BATCH05
    assert PASS_DAYS.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_post_integration_calendar_contains_all_five_batch05_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)


def test_post_integration_attempt_ledger_records_exactly_five_batch05_pass_attempts():
    _, _, attempts = load_attempt_ledger()
    batch05 = [item for item in attempts if item.attempt_id.startswith("batch05:")]
    assert len(attempts) == 25
    assert [item.attempt_sequence for item in batch05] == [21, 22, 23, 24, 25]
    assert [item.target_date for item in batch05] == [day for day, _ in EXPECTED_BATCH05]
    assert [item.outcome for item in batch05] == ["PASS"] * 5
    assert all(item.blocking_reason is None for item in batch05)
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch05)


def test_all_six_historical_blocked_dates_remain_unresolved_but_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ATTEMPTED_BLOCKED <= raw_days
    assert ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    for day in ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch05_postintegration_progression_state_is_exact():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 49
    assert len(attempts) == 25
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 6
    assert len(eligible) == 43
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 6, 19)


def test_batch05_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "601310a55b64233ada9e481d3cb2f11dc20a30d5"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "6cafa5337f28c5424cbcc25280c690de702061d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch05_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch05_targets).parameters == {}
    source = inspect.getsource(batch05_module).lower()
    for forbidden in ("playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source

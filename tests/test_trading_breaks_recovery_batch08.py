from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch08 as batch08_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_batch08 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH08_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch08_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH08 = [
    (date(2024, 3, 29), "GOOD_FRIDAY"),
    (date(2024, 5, 27), "MEMORIAL_DAY"),
    (date(2024, 6, 19), "JUNETEENTH_OBSERVED"),
    (date(2024, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2024, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
]
PASS_DAYS = {date(2024, 5, 27), date(2024, 6, 19), date(2024, 7, 3), date(2024, 7, 4)}
BLOCKED_DAYS = {date(2024, 3, 29)}
ALL_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1),
    date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4), date(2023, 12, 25),
    date(2024, 1, 1), date(2024, 3, 29),
}


def test_batch08_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert isinstance(FROZEN_BATCH08_TARGETS, tuple)
    assert batch08_targets() == EXPECTED_BATCH08


def test_batch08_historical_membership_is_not_rederived_post_integration():
    first = batch08_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch08_targets() == EXPECTED_BATCH08
    current_eligible = {day for day, _ in eligible_recovery_queue()}
    assert {day for day, _ in EXPECTED_BATCH08}.isdisjoint(current_eligible)


def test_batch08_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    assert BLOCKED_DAYS.isdisjoint(set(NO_SPECIAL_CHANGE_EVIDENCE))
    assert BLOCKED_DAYS <= raw_days


def test_batch08_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch08 = [item for item in attempts if item.attempt_id.startswith("batch08:")]
    assert len(attempts) == 40
    assert [item.attempt_sequence for item in batch08] == [36, 37, 38, 39, 40]
    assert [item.target_date for item in batch08] == [day for day, _ in EXPECTED_BATCH08]
    assert [item.outcome for item in batch08] == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]
    assert batch08[0].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch08)


def test_batch08_blocked_good_friday_remains_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ALL_BLOCKED <= raw_days
    assert ALL_BLOCKED.isdisjoint(eligible_days)
    decision = decisions[date(2024, 3, 29)]
    assert decision.eligible is False
    assert decision.latest_attempt_id == "batch08:2024-03-29"
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch08_postintegration_progression_state_is_exact_and_non_starving():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 38
    assert len(attempts) == 40
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 10
    assert len(eligible) == 28
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")


def test_batch08_freeze_provenance_remains_historical_truth_after_integration():
    assert FREEZE_BASELINE_HEAD == "2e9e51cea8342c701eec14d8d86aca215c5b7b62"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "616643e2bfd0b8a8ae3f21352554dc32fdbb503d"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "b4a2f3400b0629e7b1d0a715320735f74293b15a"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch08_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch08_targets).parameters == {}
    source = inspect.getsource(batch08_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "source_availability", "holiday_preference", "manual_skip", "priority="):
        assert forbidden not in source

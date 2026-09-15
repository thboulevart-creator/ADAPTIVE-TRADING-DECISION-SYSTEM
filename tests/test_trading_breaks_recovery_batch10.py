from __future__ import annotations

import inspect

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.freeze_trading_breaks_recovery_batch10 import BATCH_SIZE, validate_freeze_candidate
import tools.trading_breaks_recovery_batch10 as batch10_module
from tools.trading_breaks_recovery_batch10 import batch10_targets
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch10_snapshot_equals_exact_governed_eligible_prefix():
    eligible = eligible_recovery_queue()
    assert batch10_targets() == eligible[:BATCH_SIZE]
    assert validate_freeze_candidate(batch10_targets(), eligible) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch10_members_are_unresolved_initial_attempts_without_history():
    frozen = batch10_targets()
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}
    assert set(frozen) <= set(recovery_queue())
    assert {day for day, _ in frozen}.isdisjoint(attempted_days)
    for day, reason in frozen:
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert decision.contract_verdict == "PASS"


def test_batch10_blocked_and_resolved_dates_are_excluded():
    frozen_days = {day for day, _ in batch10_targets()}
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    resolved_days = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)
    assert frozen_days.isdisjoint(raw_days - eligible_days)
    assert frozen_days.isdisjoint(resolved_days)


def test_batch10_accessor_is_immutable_to_caller():
    original = batch10_targets()
    altered = batch10_targets()
    altered.pop()
    assert batch10_targets() == original


def test_batch10_frozen_module_has_no_live_queue_surface():
    source = inspect.getsource(batch10_module).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source

from __future__ import annotations

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue

BATCH_SIZE = 5
FREEZE_BASELINE_HEAD = 'fa09da05bb80ba0a94cc4a58864f2ba52a6437ec'


def derive():
    raw = recovery_queue()
    eligible = eligible_recovery_queue()
    decisions = progression_decisions()
    _, _, attempts = load_attempt_ledger()

    assert len(raw) == 22
    assert len(eligible) == 8
    assert len(attempts) == 60
    assert sum((not d.eligible) and d.latest_attempt_outcome == 'BLOCKED' for d in decisions) == 14
    assert load_material_capability_changes() == []
    assert eligible == sorted(eligible, key=lambda x: x[0])

    frozen = tuple(eligible[:BATCH_SIZE])
    attempted = {x.target_date for x in attempts}
    resolved = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)
    by_day = {x.target_date: x for x in decisions}

    assert len(frozen) == BATCH_SIZE
    assert len({day for day, _ in frozen}) == BATCH_SIZE

    for day, reason in frozen:
        decision = by_day[day]
        assert day not in attempted
        assert day not in resolved
        assert decision.candidate_reason == reason
        assert decision.eligible
        assert decision.reason == 'INITIAL_ATTEMPT'
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None

    return frozen

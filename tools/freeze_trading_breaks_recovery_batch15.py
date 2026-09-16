from __future__ import annotations

from tools.trading_breaks_recovery_batch15 import (
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
)
from tools.trading_breaks_recovery_progression import (
    current_capability,
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue

NOMINAL_BATCH_SIZE = 5


def derive():
    raw = recovery_queue()
    eligible = eligible_recovery_queue()
    decisions = progression_decisions()
    _, current_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()

    assert FREEZE_BASELINE_HEAD == 'd6622e8da58e2d4218947ff3f2953fe8e19a2c96'
    assert len(raw) == 17
    assert len(eligible) == 14
    assert len(attempts) == 68
    assert len(changes) == 1
    assert current_id == CURRENT_CAPABILITY_ID
    assert current_capability().fingerprint() == CURRENT_CAPABILITY_FINGERPRINT
    assert BATCH_SIZE == NOMINAL_BATCH_SIZE == 5
    assert eligible == sorted(eligible, key=lambda x: x[0])

    frozen = tuple(eligible[:NOMINAL_BATCH_SIZE])
    assert len(frozen) == NOMINAL_BATCH_SIZE
    assert len({day for day, _ in frozen}) == NOMINAL_BATCH_SIZE

    by_day = {item.target_date: item for item in decisions}
    attempts_by_day = {}
    for attempt in attempts:
        attempts_by_day.setdefault(attempt.target_date, []).append(attempt)

    for day, reason in frozen:
        decision = by_day[day]
        history = attempts_by_day[day]
        latest = max(history, key=lambda item: item.attempt_sequence)
        assert decision.candidate_reason == reason
        assert decision.eligible
        assert decision.reason == 'MATERIAL_CAPABILITY_CHANGE_RETRY'
        assert decision.latest_attempt_outcome == 'BLOCKED'
        assert decision.latest_attempt_id == latest.attempt_id
        assert latest.capability_id == 'TRADING_BREAKS_PRIMARY_WIDGET_V1'
        assert latest.blocking_reason == 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'

    return frozen

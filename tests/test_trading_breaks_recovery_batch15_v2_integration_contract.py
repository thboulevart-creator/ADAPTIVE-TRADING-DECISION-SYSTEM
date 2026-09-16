from tools.integrate_trading_breaks_recovery_batch15_v2 import (
    REASON_TOKENS,
    authoritative_adjudication,
    guard_preintegration_state,
    raw_source_by_day,
)
from tools.trading_breaks_recovery_batch15 import CURRENT_CAPABILITY_ID, batch15_targets


def test_batch15_integration_accepts_only_authoritative_five_pass_adjudications():
    guard_preintegration_state()
    report = authoritative_adjudication()
    assert report['verdict'] == 'PASS'
    assert (report['attempted'], report['pass'], report['blocked'], report['fail']) == (5, 5, 0, 0)
    assert [(item['target_date'], item['candidate_reason']) for item in report['adjudications']] == [
        (day.isoformat(), reason) for day, reason in batch15_targets()
    ]
    assert all(item['verdict'] == 'PASS' for item in report['adjudications'])
    assert all(item['adjudication_capability_id'] == CURRENT_CAPABILITY_ID for item in report['adjudications'])


def test_batch15_integration_raw_sources_are_exact_historical_frozen_sources():
    raw = raw_source_by_day()
    assert list(raw) == [day.isoformat() for day, _ in batch15_targets()]
    assert len(raw) == 5
    assert set(raw) == set(REASON_TOKENS)
    assert all(item['broker_reason'] for item in raw.values())
    assert all(isinstance(item['target_epoch_ms'], int) and item['target_epoch_ms'] > 0 for item in raw.values())
    assert [raw[day.isoformat()]['source_batch'] for day, _ in batch15_targets()] == [2, 2, 4, 4, 6]

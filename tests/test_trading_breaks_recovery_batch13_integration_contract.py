import json
from pathlib import Path

from tools.integrate_trading_breaks_recovery_batch13 import (
    BLOCKED_DAYS,
    PASS_RECORDS,
    guard_preintegration_state,
    load_adjudication,
)


def test_batch13_authoritative_adjudication_is_integrable():
    report = load_adjudication()
    assert report['verdict'] == 'PASS'
    assert (report['attempted'], report['pass'], report['blocked'], report['fail']) == (5, 3, 2, 0)
    by_day = {item['target_date']: item for item in report['adjudications']}
    assert set(PASS_RECORDS) == {'2026-01-19', '2026-02-16', '2026-05-25'}
    assert set(BLOCKED_DAYS) == {'2026-01-01', '2026-04-03'}
    assert all(by_day[day]['verdict'] == 'BLOCKED' for day in BLOCKED_DAYS)


def test_batch13_preintegration_state_is_exact_and_unmutated():
    guard_preintegration_state()
    ledger = json.loads(
        Path('reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json').read_text(
            encoding='utf-8'
        )
    )
    assert len(ledger['attempts']) == 60
    assert not any(str(item['attempt_id']).startswith('batch13:') for item in ledger['attempts'])

import json
from pathlib import Path

from tools.integrate_trading_breaks_recovery_batch14 import (
    BLOCKED_DAYS,
    PASS_RECORDS,
    guard_preintegration_state,
    load_adjudication,
)


def test_batch14_authoritative_adjudication_is_integrable():
    report = load_adjudication()
    assert report['verdict'] == 'PASS'
    assert (report['attempted'], report['pass'], report['blocked'], report['fail']) == (3, 2, 1, 0)
    by_day = {item['target_date']: item for item in report['adjudications']}
    assert set(PASS_RECORDS) == {'2026-06-19', '2026-07-03'}
    assert set(BLOCKED_DAYS) == {'2026-07-02'}
    assert by_day['2026-07-02']['verdict'] == 'BLOCKED'
    assert by_day['2026-07-02']['reason'] == 'NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED'


def test_batch14_preintegration_state_is_exact_and_unmutated():
    guard_preintegration_state()
    ledger = json.loads(
        Path('reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json').read_text(
            encoding='utf-8'
        )
    )
    assert len(ledger['attempts']) == 65
    assert not any(str(item['attempt_id']).startswith('batch14:') for item in ledger['attempts'])

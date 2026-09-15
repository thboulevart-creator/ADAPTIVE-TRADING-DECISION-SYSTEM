import json
from pathlib import Path

from tools.integrate_trading_breaks_recovery_batch12 import (
    BLOCKED_DAY,
    BLOCKED_REASON,
    PASS_RECORDS,
    guard_preintegration_state,
    load_adjudication,
)


def test_batch12_authoritative_adjudication_is_integrable():
    report = load_adjudication()
    assert report['verdict'] == 'PASS'
    assert (report['attempted'], report['pass'], report['blocked'], report['fail']) == (5, 4, 1, 0)
    by_day = {item['target_date']: item for item in report['adjudications']}
    assert set(PASS_RECORDS) == {'2025-11-27', '2025-11-28', '2025-12-24', '2025-12-31'}
    assert by_day[BLOCKED_DAY]['verdict'] == 'BLOCKED'
    assert by_day[BLOCKED_DAY]['reason'] == BLOCKED_REASON


def test_batch12_preintegration_state_is_exact_and_unmutated():
    guard_preintegration_state()
    ledger = json.loads(
        Path('reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json').read_text(
            encoding='utf-8'
        )
    )
    assert len(ledger['attempts']) == 55
    assert not any(str(item['attempt_id']).startswith('batch12:') for item in ledger['attempts'])

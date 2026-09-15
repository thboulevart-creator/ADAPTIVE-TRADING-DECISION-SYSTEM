import json
from pathlib import Path

from tools.integrate_trading_breaks_recovery_batch11 import load_adjudication, guard_preintegration_state


def test_batch11_authoritative_adjudication_is_integrable():
    report=load_adjudication()
    assert report['verdict']=='PASS'
    assert (report['attempted'],report['pass'],report['blocked'],report['fail'])==(5,5,0,0)


def test_batch11_preintegration_state_is_exact():
    guard_preintegration_state()
    ledger=json.loads(Path('reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json').read_text(encoding='utf-8'))
    assert len(ledger['attempts'])==50

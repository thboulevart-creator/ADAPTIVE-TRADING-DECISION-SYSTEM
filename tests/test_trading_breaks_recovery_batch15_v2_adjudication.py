from tools.trading_breaks_recovery_batch15 import batch15_targets
from tools.trading_breaks_recovery_batch15_v2_adjudication import adjudicate_batch15


def test_batch15_v2_adjudication_is_exact_five_pass_and_offline():
    report = adjudicate_batch15()
    assert report['verdict'] == 'PASS'
    assert report['reason'] == 'BATCH15_FROZEN_V2_EVIDENCE_INDEPENDENTLY_READJUDICATED_OFFLINE'
    assert (report['attempted'], report['pass'], report['blocked'], report['fail']) == (5, 5, 0, 0)
    assert report['browser_used'] is False
    assert report['probe_used'] is False
    assert report['network_used'] is False
    assert [(item['target_date'], item['candidate_reason']) for item in report['adjudications']] == [
        (day.isoformat(), reason) for day, reason in batch15_targets()
    ]


def test_batch15_v2_adjudication_preserves_retry_and_source_identity():
    report = adjudicate_batch15()
    expected = [
        ('2021-12-24', 'batch02:2021-12-24', 6, '31532'),
        ('2022-04-15', 'batch02:2022-04-15', 10, '34894'),
        ('2022-12-26', 'batch04:2022-12-26', 19, '46756'),
        ('2023-01-02', 'batch04:2023-01-02', 20, '48045'),
        ('2023-07-04', 'batch06:2023-07-04', 27, '56233'),
    ]
    observed = [
        (item['target_date'], item['source_attempt_id'], item['source_attempt_sequence'], item['record_id'])
        for item in report['adjudications']
    ]
    assert observed == expected
    assert all(item['retry_attempt_id'] == f"overlap-v2:{item['target_date']}" for item in report['adjudications'])
    assert all(item['verdict'] == 'PASS' for item in report['adjudications'])

from tools.trading_breaks_recovery_batch15 import batch15_targets
from tools.trading_breaks_recovery_batch15_v2_execution import select_persisted_evidence


def test_batch15_execution_selects_exact_frozen_persisted_rows_without_recapture():
    report = select_persisted_evidence()
    assert report['verdict'] == 'PASS'
    assert report['capture_mode'] == 'PERSISTED_OFFLINE_READJUDICATION_REUSE'
    assert report['browser_used'] is False
    assert report['probe_used'] is False
    assert report['network_used'] is False
    assert (report['selected_count'], report['pass_count'], report['blocked_count'], report['fail_count']) == (5, 5, 0, 0)
    assert [(item['target_date'], item['candidate_reason']) for item in report['results']] == [
        (day.isoformat(), reason) for day, reason in batch15_targets()
    ]
    assert all(item['verdict'] == 'PASS' for item in report['results'])
    assert all(item['cross_date'] is True for item in report['results'])
    assert all(item['proposed_retry_attempt_id'] == f"overlap-v2:{item['target_date']}" for item in report['results'])


def test_batch15_execution_preserves_exact_source_attempts_and_records():
    report = select_persisted_evidence()
    observed = [
        (
            item['target_date'],
            item['source_attempt_id'],
            item['source_attempt_sequence'],
            item['record_id'],
        )
        for item in report['results']
    ]
    assert observed == [
        ('2021-12-24', 'batch02:2021-12-24', 6, '31532'),
        ('2022-04-15', 'batch02:2022-04-15', 10, '34894'),
        ('2022-12-26', 'batch04:2022-12-26', 19, '46756'),
        ('2023-01-02', 'batch04:2023-01-02', 20, '48045'),
        ('2023-07-04', 'batch06:2023-07-04', 27, '56233'),
    ]

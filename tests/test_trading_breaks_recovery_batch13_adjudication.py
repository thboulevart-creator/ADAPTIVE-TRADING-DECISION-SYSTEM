from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.trading_breaks_recovery_batch13_adjudication import RUNTIME_PATH, adjudicate_runtime


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding='utf-8'))


def test_authoritative_batch13_runtime_adjudicates_3_pass_2_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report['verdict'] == 'PASS'
    assert report['attempted'] == 5
    assert report['pass'] == 3
    assert report['blocked'] == 2
    assert report['fail'] == 0
    assert [item['verdict'] for item in report['adjudications']] == [
        'BLOCKED', 'PASS', 'PASS', 'BLOCKED', 'PASS'
    ]


def test_cross_date_records_are_blocked_and_never_promoted():
    report = adjudicate_runtime(_runtime())
    expected = {0: '92491', 3: '98541'}
    for index, record_id in expected.items():
        item = report['adjudications'][index]
        assert item['capture_verdict'] == 'CAPTURED'
        assert item['verdict'] == 'BLOCKED'
        assert item['reason'] == 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'
        assert item['overlap_record_id'] == record_id
        assert item['broker_record_id'] == record_id
        assert 'break_start_utc' not in item
        assert 'fully_closed_hours_utc' not in item


def test_exact_target_positive_records_pass_with_independent_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        1: ('93608', [18, 19, 20, 21, 22]),
        2: ('94467', [18, 19, 20, 21, 22]),
        4: ('100253', [17, 18, 19, 20, 21]),
    }
    for index, (record_id, hours) in expected.items():
        item = report['adjudications'][index]
        assert item['verdict'] == 'PASS'
        assert item['reason'] == 'EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED'
        assert item['broker_record_id'] == record_id
        assert item['fully_closed_hours_utc'] == hours
        assert item['dom_witness_present'] is True


def test_good_friday_candidate_does_not_relabel_cross_date_easter_record():
    item = adjudicate_runtime(_runtime())['adjudications'][3]
    assert item['broker_reason'] == 'Easter'
    assert item['verdict'] == 'BLOCKED'
    assert item['reason'] == 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'


def test_frozen_membership_tampering_is_rejected():
    runtime = _runtime()
    runtime['targets'][0]['target_date'] = '2099-01-01'
    with pytest.raises(ValueError, match='FROZEN_MEMBERSHIP_MISMATCH'):
        adjudicate_runtime(runtime)


def test_runtime_result_reordering_is_rejected():
    runtime = _runtime()
    runtime['results'][0], runtime['results'][1] = runtime['results'][1], runtime['results'][0]
    with pytest.raises(ValueError, match='RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH'):
        adjudicate_runtime(runtime)


@pytest.mark.parametrize(
    ('key', 'value'),
    [
        ('workflow_run', 1),
        ('job_id', 2),
        ('artifact_id', 3),
        ('artifact_sha256', '0' * 64),
        ('probe_commit', '0' * 40),
        ('artifact_url', 'https://example.invalid/tampered'),
    ],
)
def test_provenance_tampering_is_rejected(key: str, value: object):
    runtime = _runtime()
    runtime['provenance'][key] = value
    with pytest.raises(ValueError, match=f'PROVENANCE_MISMATCH:{key}'):
        adjudicate_runtime(runtime)


def test_dom_network_contradiction_fails_closed():
    runtime = _runtime()
    runtime['results'][1]['dom_witness_lines'] = [
        'USATECH.IDX/USD\t19-Jan-26 17:59:59\t19-Jan-26 22:59:59\tTampered Reason'
    ]
    report = adjudicate_runtime(runtime)
    assert report['verdict'] == 'FAIL'
    assert report['adjudications'][1]['reason'] == 'DOM_NETWORK_CONTRADICTION'


def test_multiple_network_records_fail_closed():
    runtime = _runtime()
    runtime['results'][1]['matching_records'].append(
        copy.deepcopy(runtime['results'][1]['matching_records'][0])
    )
    with pytest.raises(ValueError, match='MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION'):
        adjudicate_runtime(runtime)

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.trading_breaks_recovery_batch12_adjudication import RUNTIME_PATH, adjudicate_runtime


def _runtime() -> dict:
    return json.loads(Path(RUNTIME_PATH).read_text(encoding='utf-8'))


def test_authoritative_batch12_runtime_adjudicates_4_pass_1_blocked_0_fail():
    report = adjudicate_runtime(_runtime())
    assert report['verdict'] == 'PASS'
    assert report['attempted'] == 5
    assert report['pass'] == 4
    assert report['blocked'] == 1
    assert report['fail'] == 0
    assert [item['verdict'] for item in report['adjudications']] == [
        'PASS', 'PASS', 'PASS', 'BLOCKED', 'PASS'
    ]


def test_christmas_day_cross_date_record_is_blocked_and_never_promoted():
    item = adjudicate_runtime(_runtime())['adjudications'][3]
    assert item['capture_verdict'] == 'CAPTURED'
    assert item['verdict'] == 'BLOCKED'
    assert item['reason'] == 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'
    assert item['overlap_record_id'] == '91078'
    assert item['broker_record_id'] == '91078'
    assert 'break_start_utc' not in item
    assert 'fully_closed_hours_utc' not in item


def test_exact_target_positive_records_pass_with_independent_hour_projection():
    report = adjudicate_runtime(_runtime())
    expected = {
        0: ('87363', [18, 19, 20, 21, 22]),
        1: ('87364', [19, 20, 21, 22, 23]),
        2: ('91078', [19, 20, 21, 22, 23]),
        4: ('92491', [22, 23]),
    }
    for index, (record_id, hours) in expected.items():
        item = report['adjudications'][index]
        assert item['verdict'] == 'PASS'
        assert item['reason'] == 'EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED'
        assert item['broker_record_id'] == record_id
        assert item['fully_closed_hours_utc'] == hours
        assert item['dom_witness_present'] is True


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
    runtime['results'][0]['dom_witness_lines'] = [
        'USATECH.IDX/USD\t27-Nov-25 18:59:59\t27-Nov-25 22:59:59\tThanksgiving Day'
    ]
    report = adjudicate_runtime(runtime)
    assert report['verdict'] == 'FAIL'
    assert report['adjudications'][0]['reason'] == 'DOM_NETWORK_CONTRADICTION'


def test_multiple_network_records_fail_closed():
    runtime = _runtime()
    runtime['results'][0]['matching_records'].append(
        copy.deepcopy(runtime['results'][0]['matching_records'][0])
    )
    with pytest.raises(ValueError, match='MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION'):
        adjudicate_runtime(runtime)


def test_capture_layer_captured_is_not_automatic_pass_for_cross_date_record():
    runtime = _runtime()
    assert runtime['results'][3]['capture_verdict'] == 'CAPTURED'
    item = adjudicate_runtime(runtime)['adjudications'][3]
    assert item['verdict'] == 'BLOCKED'
    assert item['reason'] == 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'


def test_partial_start_hours_are_not_rounded_closed():
    report = adjudicate_runtime(_runtime())
    thanksgiving_friday = report['adjudications'][1]
    christmas_eve = report['adjudications'][2]
    new_years_eve = report['adjudications'][4]
    assert 18 not in thanksgiving_friday['fully_closed_hours_utc']
    assert 18 not in christmas_eve['fully_closed_hours_utc']
    assert 21 not in new_years_eve['fully_closed_hours_utc']

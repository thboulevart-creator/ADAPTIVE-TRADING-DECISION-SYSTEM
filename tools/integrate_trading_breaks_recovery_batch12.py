from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch12 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch12_targets,
)

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / 'tools' / 'dukascopy_usatech_calendar.py'
LEDGER = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_attempt_ledger.json'
ADJUDICATION = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch12_adjudication.json'

RUN_ID = 35016454761
JOB_ID = 104540999314
PROBE_COMMIT = '2c2fd6e2db2e0ab75a6b978d6cddad679dbda5b8'
ARTIFACT_ID = 10416410006
ARTIFACT_SHA256 = '6649d976bb9d586cce591cd9b9a9e0e71ed8e5496a1e47e2e52bbdaa2de0297d'

PASS_RECORDS = {
    '2025-11-27': {
        'reason_token': 'SPECIAL_THANKSGIVING_DAY_2025',
        'record_id': '87363',
        'broker_reason': 'Thanksgiving Day',
        'request_epoch_ms': 1764201600000,
        'start_utc': '2025-11-27T17:59:59Z',
        'final_closed_minute_utc': '2025-11-27T22:59:59Z',
        'reopen_utc': '2025-11-27T23:00:59Z',
        'closed_hours': (18, 19, 20, 21, 22),
    },
    '2025-11-28': {
        'reason_token': 'SPECIAL_THANKSGIVING_FRIDAY_2025',
        'record_id': '87364',
        'broker_reason': 'Thanksgiving Day',
        'request_epoch_ms': 1764288000000,
        'start_utc': '2025-11-28T18:14:59Z',
        'final_closed_minute_utc': '2025-11-30T22:59:59Z',
        'reopen_utc': '2025-11-30T23:00:59Z',
        'closed_hours': (19, 20, 21, 22, 23),
    },
    '2025-12-24': {
        'reason_token': 'SPECIAL_CHRISTMAS_PRE_HOLIDAY_SESSION_2025',
        'record_id': '91078',
        'broker_reason': 'Christmas Day',
        'request_epoch_ms': 1766534400000,
        'start_utc': '2025-12-24T18:14:59Z',
        'final_closed_minute_utc': '2025-12-25T22:59:59Z',
        'reopen_utc': '2025-12-25T23:00:59Z',
        'closed_hours': (19, 20, 21, 22, 23),
    },
    '2025-12-31': {
        'reason_token': 'SPECIAL_NEW_YEARS_EVE_2025',
        'record_id': '92491',
        'broker_reason': "New Year's Day",
        'request_epoch_ms': 1767139200000,
        'start_utc': '2025-12-31T21:14:59Z',
        'final_closed_minute_utc': '2026-01-01T22:59:59Z',
        'reopen_utc': '2026-01-01T23:00:59Z',
        'closed_hours': (22, 23),
    },
}

BLOCKED_DAY = '2025-12-25'
BLOCKED_REASON = 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


def load_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding='utf-8'))
    if (
        report.get('schema') != 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH12_ADJUDICATION_V1'
        or report.get('verdict') != 'PASS'
    ):
        raise RuntimeError('BATCH12_ADJUDICATION_NOT_AUTHORITATIVE_PASS')
    if (report.get('attempted'), report.get('pass'), report.get('blocked'), report.get('fail')) != (5, 4, 1, 0):
        raise RuntimeError('BATCH12_ADJUDICATION_ACCOUNTING_MISMATCH')

    provenance = report.get('provenance') or {}
    expected_provenance = {
        'workflow_run': RUN_ID,
        'job_id': JOB_ID,
        'probe_commit': PROBE_COMMIT,
        'artifact_id': ARTIFACT_ID,
        'artifact_sha256': ARTIFACT_SHA256,
    }
    for key, value in expected_provenance.items():
        if provenance.get(key) != value:
            raise RuntimeError(f'BATCH12_PROVENANCE_MISMATCH:{key}')

    observed = [
        (item.get('target_date'), item.get('candidate_reason'), item.get('verdict'))
        for item in report.get('adjudications', [])
    ]
    expected = [
        (day.isoformat(), reason, 'BLOCKED' if day.isoformat() == BLOCKED_DAY else 'PASS')
        for day, reason in batch12_targets()
    ]
    if observed != expected:
        raise RuntimeError('BATCH12_FROZEN_ADJUDICATION_IDENTITY_MISMATCH')

    by_day = {item['target_date']: item for item in report['adjudications']}
    for day, record in PASS_RECORDS.items():
        item = by_day[day]
        checks = {
            'reason': 'EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED',
            'broker_record_id': record['record_id'],
            'broker_reason': record['broker_reason'],
            'break_start_utc': record['start_utc'],
            'final_closed_minute_utc': record['final_closed_minute_utc'],
            'reopen_utc': record['reopen_utc'],
            'fully_closed_hours_utc': list(record['closed_hours']),
            'dom_witness_present': True,
        }
        for key, value in checks.items():
            if item.get(key) != value:
                raise RuntimeError(f'BATCH12_PASS_RECORD_MISMATCH:{day}:{key}')

    blocked = by_day[BLOCKED_DAY]
    if blocked.get('reason') != BLOCKED_REASON:
        raise RuntimeError('BATCH12_BLOCKED_REASON_MISMATCH')
    if blocked.get('broker_record_id') != '91078' or blocked.get('overlap_record_id') != '91078':
        raise RuntimeError('BATCH12_BLOCKED_OVERLAP_IDENTITY_MISMATCH')
    if blocked.get('capture_verdict') != 'CAPTURED' or blocked.get('dom_witness_present') is not True:
        raise RuntimeError('BATCH12_BLOCKED_CAPTURE_EVIDENCE_MISMATCH')
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding='utf-8')
    for token in [item['reason_token'] for item in PASS_RECORDS.values()]:
        if token in calendar_text:
            raise RuntimeError('BATCH12_ALREADY_OR_PARTIALLY_INTEGRATED')
    if 'SPECIAL_CHRISTMAS_DAY_2025' in calendar_text or 'SPECIAL_CHRISTMAS_OBSERVED_2025' in calendar_text:
        raise RuntimeError('BATCH12_BLOCKED_DAY_MUST_NOT_BE_IN_CALENDAR')

    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger.get('attempts')
    if not isinstance(attempts, list) or len(attempts) != 55:
        raise RuntimeError('PRE_BATCH12_ATTEMPT_COUNT_MISMATCH')
    if any(str(item.get('attempt_id', '')).startswith('batch12:') for item in attempts):
        raise RuntimeError('BATCH12_ATTEMPTS_ALREADY_PRESENT')


def render_entry(day: str, record: dict) -> str:
    year, month, day_number = map(int, day.split('-'))
    hours = record['closed_hours']
    if hours != tuple(range(hours[0], hours[-1] + 1)):
        raise RuntimeError(f'NONCONTIGUOUS_HOURS:{day}')
    return f'''    date({year}, {month}, {day_number}): {{
        "reason": "{record['reason_token']}",
        "fully_closed_hours_utc": frozenset(range({hours[0]}, {hours[-1] + 1})),
        "broker_record_id": "{record['record_id']}",
        "broker_reason": "{record['broker_reason']}",
        "artifact_id": {ARTIFACT_ID},
        "artifact_sha256": "{ARTIFACT_SHA256}",
        "probe_commit": "{PROBE_COMMIT}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={record['request_epoch_ms']}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/historical_trading_breaks_recovery_batch12_qualification.md"
        ),
    }},
'''


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding='utf-8')
    block = ''.join(render_entry(day, PASS_RECORDS[day]) for day in PASS_RECORDS)
    marker = '}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text = replace_once(text, marker, block + marker, 'Batch12 calendar insertion')
    CALENDAR.write_text(text, encoding='utf-8')


def integrate_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger['attempts']
    provenance = {
        'workflow_run': RUN_ID,
        'job_id': JOB_ID,
        'artifact_id': ARTIFACT_ID,
        'artifact_sha256': ARTIFACT_SHA256,
        'probe_commit': PROBE_COMMIT,
    }
    for sequence, ((day, reason), adjudication) in enumerate(
        zip(batch12_targets(), report['adjudications'], strict=True),
        start=56,
    ):
        outcome = adjudication['verdict']
        if outcome not in {'PASS', 'BLOCKED'}:
            raise RuntimeError(f'BATCH12_UNINTEGRABLE_OUTCOME:{day}:{outcome}')
        if outcome == 'BLOCKED' and day.isoformat() != BLOCKED_DAY:
            raise RuntimeError(f'BATCH12_UNEXPECTED_BLOCKED_DAY:{day}')
        blocking_reason = adjudication['reason'] if outcome == 'BLOCKED' else None
        attempts.append(
            {
                'attempt_sequence': sequence,
                'attempt_id': f'batch12:{day.isoformat()}',
                'batch_contract': BATCH_CONTRACT,
                'target_date': day.isoformat(),
                'candidate_reason': reason,
                'outcome': outcome,
                'adjudication_reason': adjudication['reason'],
                'blocking_reason': blocking_reason,
                'capability_id': CURRENT_CAPABILITY_ID,
                'provenance': dict(provenance),
            }
        )
    if len(attempts) != 60:
        raise RuntimeError('BATCH12_POST_LEDGER_COUNT_MISMATCH')
    LEDGER.write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')


def rewrite_current_state_tests() -> None:
    replacements = {
        'assert len(attempts) == 55': 'assert len(attempts) == 60',
        'list(range(1, 56))': 'list(range(1, 61))',
        'len({item.attempt_id for item in attempts}) == 55': 'len({item.attempt_id for item in attempts}) == 60',
        'assert len(queue) == 26': 'assert len(queue) == 22',
        'assert len(decisions) == len(queue) == 26': 'assert len(decisions) == len(queue) == 22',
        'assert len(recovery_queue()) == len(decisions) == 26': 'assert len(recovery_queue()) == len(decisions) == 22',
        'assert len(eligible) == 13': 'assert len(eligible) == 8',
        '(111, 65, 46)': '(111, 69, 42)',
        '(68, 42, 26)': '(68, 46, 22)',
        'global_report["resolved_candidate_dates"] == 65': 'global_report["resolved_candidate_dates"] == 69',
        'global_report["unresolved_candidate_dates"] == 46': 'global_report["unresolved_candidate_dates"] == 42',
        'window_report["resolved_candidate_dates"] == 42': 'window_report["resolved_candidate_dates"] == 46',
        'window_report["unresolved_candidate_dates"] == 26': 'window_report["unresolved_candidate_dates"] == 22',
        'eligible[0] == (date(2025, 11, 27), "THANKSGIVING_DAY")': 'eligible[0] == (date(2026, 1, 1), "NEW_YEARS_OBSERVED")',
        "eligible[0] == (date(2025, 11, 27), 'THANKSGIVING_DAY')": "eligible[0] == (date(2026, 1, 1), 'NEW_YEARS_OBSERVED')",
        'post_batch11_state': 'post_batch12_state',
        'post_batch11_progression_state': 'post_batch12_progression_state',
    }
    excluded = {
        'test_trading_breaks_recovery_batch12_adjudication.py',
        'test_trading_breaks_recovery_batch12_execution_contract.py',
        'test_trading_breaks_recovery_batch12_integration_contract.py',
    }
    for path in sorted((REPO / 'tests').glob('test_*.py')):
        if path.name.endswith('_integration_contract.py') or path.name in excluded:
            continue
        text = path.read_text(encoding='utf-8')
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding='utf-8')


def main() -> int:
    report = load_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_ledger(report)
    rewrite_current_state_tests()
    print('PASS: prepared Batch 12 atomic worktree integration')
    print('calendar PASS dates:', ', '.join(PASS_RECORDS))
    print('ledger attempts: 56..60')
    print('blocked unresolved date:', BLOCKED_DAY)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

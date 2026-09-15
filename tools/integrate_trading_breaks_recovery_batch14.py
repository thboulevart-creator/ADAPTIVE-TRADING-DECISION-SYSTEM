from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch14 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch14_targets,
)

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / 'tools' / 'dukascopy_usatech_calendar.py'
LEDGER = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_attempt_ledger.json'
ADJUDICATION = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch14_adjudication.json'

RUN_ID = 35023845609
JOB_ID = 104565948108
PROBE_COMMIT = '4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b'
ARTIFACT_ID = 10418961548
ARTIFACT_SHA256 = '00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910'

PASS_RECORDS = {
    '2026-06-19': {
        'reason_token': 'SPECIAL_JUNETEENTH_2026',
        'record_id': '101094',
        'broker_reason': 'Juneteenth Holiday',
        'request_epoch_ms': 1781827200000,
        'start_utc': '2026-06-19T16:59:59Z',
        'final_closed_minute_utc': '2026-06-21T21:59:59Z',
        'reopen_utc': '2026-06-21T22:00:59Z',
        'closed_hours': (17, 18, 19, 20, 21, 22, 23),
    },
    '2026-07-03': {
        'reason_token': 'SPECIAL_INDEPENDENCE_DAY_2026',
        'record_id': '101959',
        'broker_reason': 'Independence Day',
        'request_epoch_ms': 1783036800000,
        'start_utc': '2026-07-03T16:59:59Z',
        'final_closed_minute_utc': '2026-07-05T21:59:59Z',
        'reopen_utc': '2026-07-05T22:00:59Z',
        'closed_hours': (17, 18, 19, 20, 21, 22, 23),
    },
}

BLOCKED_DAYS = {
    '2026-07-02': 'NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED',
}


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


def load_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding='utf-8'))
    if report.get('schema') != 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH14_ADJUDICATION_V1':
        raise RuntimeError('BATCH14_ADJUDICATION_SCHEMA_MISMATCH')
    if report.get('verdict') != 'PASS':
        raise RuntimeError('BATCH14_ADJUDICATION_NOT_AUTHORITATIVE_PASS')
    if (report.get('attempted'), report.get('pass'), report.get('blocked'), report.get('fail')) != (3, 2, 1, 0):
        raise RuntimeError('BATCH14_ADJUDICATION_ACCOUNTING_MISMATCH')

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
            raise RuntimeError(f'BATCH14_PROVENANCE_MISMATCH:{key}')

    observed = [
        (item.get('target_date'), item.get('candidate_reason'), item.get('verdict'))
        for item in report.get('adjudications', [])
    ]
    expected = [
        (day.isoformat(), reason, 'BLOCKED' if day.isoformat() in BLOCKED_DAYS else 'PASS')
        for day, reason in batch14_targets()
    ]
    if observed != expected:
        raise RuntimeError('BATCH14_FROZEN_ADJUDICATION_IDENTITY_MISMATCH')

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
                raise RuntimeError(f'BATCH14_PASS_RECORD_MISMATCH:{day}:{key}')

    for day, reason in BLOCKED_DAYS.items():
        item = by_day[day]
        if item.get('verdict') != 'BLOCKED' or item.get('reason') != reason:
            raise RuntimeError(f'BATCH14_BLOCKED_REASON_MISMATCH:{day}')
        if item.get('broker_record_id') is not None or item.get('capture_verdict') != 'BLOCKED':
            raise RuntimeError(f'BATCH14_BLOCKED_EVIDENCE_MISMATCH:{day}')
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding='utf-8')
    for token in [item['reason_token'] for item in PASS_RECORDS.values()]:
        if token in calendar_text:
            raise RuntimeError('BATCH14_ALREADY_OR_PARTIALLY_INTEGRATED')
    if 'date(2026, 7, 2):' in calendar_text:
        raise RuntimeError('BATCH14_BLOCKED_DAY_MUST_NOT_BE_IN_CALENDAR')

    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger.get('attempts')
    if not isinstance(attempts, list) or len(attempts) != 65:
        raise RuntimeError('PRE_BATCH14_ATTEMPT_COUNT_MISMATCH')
    if any(str(item.get('attempt_id', '')).startswith('batch14:') for item in attempts):
        raise RuntimeError('BATCH14_ATTEMPTS_ALREADY_PRESENT')


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
            "reports/data-qualification/historical_trading_breaks_recovery_batch14_qualification.md"
        ),
    }},
'''


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding='utf-8')
    block = ''.join(render_entry(day, PASS_RECORDS[day]) for day in PASS_RECORDS)
    marker = '}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text = replace_once(text, marker, block + marker, 'Batch14 calendar insertion')
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
        zip(batch14_targets(), report['adjudications'], strict=True), start=66
    ):
        outcome = adjudication['verdict']
        if outcome not in {'PASS', 'BLOCKED'}:
            raise RuntimeError(f'BATCH14_UNINTEGRABLE_OUTCOME:{day}:{outcome}')
        attempts.append(
            {
                'attempt_sequence': sequence,
                'attempt_id': f'batch14:{day.isoformat()}',
                'batch_contract': BATCH_CONTRACT,
                'target_date': day.isoformat(),
                'candidate_reason': reason,
                'outcome': outcome,
                'adjudication_reason': adjudication['reason'],
                'blocking_reason': adjudication['reason'] if outcome == 'BLOCKED' else None,
                'capability_id': CURRENT_CAPABILITY_ID,
                'provenance': dict(provenance),
            }
        )
    if len(attempts) != 68:
        raise RuntimeError('BATCH14_POST_LEDGER_COUNT_MISMATCH')
    LEDGER.write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')


def rewrite_current_state_tests() -> None:
    replacements = {
        'assert len(attempts) == 65': 'assert len(attempts) == 68',
        'list(range(1, 66))': 'list(range(1, 69))',
        'len({item.attempt_id for item in attempts}) == 65': 'len({item.attempt_id for item in attempts}) == 68',
        'assert len(queue) == 19': 'assert len(queue) == 17',
        'assert len(decisions) == len(queue) == 19': 'assert len(decisions) == len(queue) == 17',
        'assert len(recovery_queue()) == len(decisions) == 19': 'assert len(recovery_queue()) == len(decisions) == 17',
        'assert len(eligible) == 3': 'assert len(eligible) == 0',
        'assert eligible[0] == (date(2026, 6, 19), "JUNETEENTH_OBSERVED")': 'assert eligible == []',
        "assert eligible[0] == (date(2026, 6, 19), 'JUNETEENTH_OBSERVED')": 'assert eligible == []',
        'sum((not item.eligible) and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 16': 'sum((not item.eligible) and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 17',
        "sum((not item.eligible) and item.latest_attempt_outcome == 'BLOCKED' for item in decisions) == 16": "sum((not item.eligible) and item.latest_attempt_outcome == 'BLOCKED' for item in decisions) == 17",
        'sum((not d.eligible) and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 16': 'sum((not d.eligible) and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 17',
        "sum((not d.eligible) and d.latest_attempt_outcome == 'BLOCKED' for d in decisions) == 16": "sum((not d.eligible) and d.latest_attempt_outcome == 'BLOCKED' for d in decisions) == 17",
        'sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 16': 'sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 17',
        "sum(not item.eligible and item.latest_attempt_outcome == 'BLOCKED' for item in decisions) == 16": "sum(not item.eligible and item.latest_attempt_outcome == 'BLOCKED' for item in decisions) == 17",
        '(111, 72, 39)': '(111, 74, 37)',
        '(68, 49, 19)': '(68, 51, 17)',
        'global_report["resolved_candidate_dates"] == 72': 'global_report["resolved_candidate_dates"] == 74',
        'global_report["unresolved_candidate_dates"] == 39': 'global_report["unresolved_candidate_dates"] == 37',
        'window_report["resolved_candidate_dates"] == 49': 'window_report["resolved_candidate_dates"] == 51',
        'window_report["unresolved_candidate_dates"] == 19': 'window_report["unresolved_candidate_dates"] == 17',
        'post_batch13_state': 'post_batch14_state',
        'post_batch13_progression_state': 'post_batch14_progression_state',
    }
    excluded = {
        'test_trading_breaks_recovery_batch14.py',
        'test_trading_breaks_recovery_batch14_adjudication.py',
        'test_trading_breaks_recovery_batch14_execution_contract.py',
        'test_trading_breaks_recovery_batch14_integration_contract.py',
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
    print('PASS: prepared terminal Batch 14 atomic worktree integration')
    print('calendar PASS dates:', ', '.join(PASS_RECORDS))
    print('ledger attempts: 66..68')
    print('blocked unresolved date: 2026-07-02')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

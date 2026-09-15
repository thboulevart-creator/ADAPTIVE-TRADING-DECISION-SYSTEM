from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch13 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch13_targets,
)

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / 'tools' / 'dukascopy_usatech_calendar.py'
LEDGER = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_attempt_ledger.json'
ADJUDICATION = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch13_adjudication.json'

RUN_ID = 35020650564
JOB_ID = 104555157264
PROBE_COMMIT = 'a974275d06ff45b0a78ad6558a6480e25cfe0f73'
ARTIFACT_ID = 10416898441
ARTIFACT_SHA256 = '59c93ab69bb1484fa0578bb8704aea76f15d67765e9a27ec0416c615d83faec8'

PASS_RECORDS = {
    '2026-01-19': {
        'reason_token': 'SPECIAL_MLK_DAY_2026',
        'record_id': '93608',
        'broker_reason': 'Martin Luther King Jr. Day',
        'request_epoch_ms': 1768780800000,
        'start_utc': '2026-01-19T17:59:59Z',
        'final_closed_minute_utc': '2026-01-19T22:59:59Z',
        'reopen_utc': '2026-01-19T23:00:59Z',
        'closed_hours': (18, 19, 20, 21, 22),
    },
    '2026-02-16': {
        'reason_token': 'SPECIAL_PRESIDENTS_DAY_2026',
        'record_id': '94467',
        'broker_reason': "President's Day",
        'request_epoch_ms': 1771200000000,
        'start_utc': '2026-02-16T17:59:59Z',
        'final_closed_minute_utc': '2026-02-16T22:59:59Z',
        'reopen_utc': '2026-02-16T23:00:59Z',
        'closed_hours': (18, 19, 20, 21, 22),
    },
    '2026-05-25': {
        'reason_token': 'SPECIAL_MEMORIAL_DAY_2026',
        'record_id': '100253',
        'broker_reason': 'Memorial Day',
        'request_epoch_ms': 1779667200000,
        'start_utc': '2026-05-25T16:59:59Z',
        'final_closed_minute_utc': '2026-05-25T21:59:59Z',
        'reopen_utc': '2026-05-25T22:00:59Z',
        'closed_hours': (17, 18, 19, 20, 21),
    },
}

BLOCKED_DAYS = {
    '2026-01-01': ('92491', 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'),
    '2026-04-03': ('98541', 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE'),
}


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


def load_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding='utf-8'))
    if report.get('schema') != 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH13_ADJUDICATION_V1' or report.get('verdict') != 'PASS':
        raise RuntimeError('BATCH13_ADJUDICATION_NOT_AUTHORITATIVE_PASS')
    if (report.get('attempted'), report.get('pass'), report.get('blocked'), report.get('fail')) != (5, 3, 2, 0):
        raise RuntimeError('BATCH13_ADJUDICATION_ACCOUNTING_MISMATCH')
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
            raise RuntimeError(f'BATCH13_PROVENANCE_MISMATCH:{key}')
    observed = [
        (item.get('target_date'), item.get('candidate_reason'), item.get('verdict'))
        for item in report.get('adjudications', [])
    ]
    expected = [
        (day.isoformat(), reason, 'BLOCKED' if day.isoformat() in BLOCKED_DAYS else 'PASS')
        for day, reason in batch13_targets()
    ]
    if observed != expected:
        raise RuntimeError('BATCH13_FROZEN_ADJUDICATION_IDENTITY_MISMATCH')
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
                raise RuntimeError(f'BATCH13_PASS_RECORD_MISMATCH:{day}:{key}')
    for day, (record_id, reason) in BLOCKED_DAYS.items():
        item = by_day[day]
        if item.get('reason') != reason:
            raise RuntimeError(f'BATCH13_BLOCKED_REASON_MISMATCH:{day}')
        if item.get('broker_record_id') != record_id or item.get('overlap_record_id') != record_id:
            raise RuntimeError(f'BATCH13_BLOCKED_OVERLAP_IDENTITY_MISMATCH:{day}')
        if item.get('capture_verdict') != 'CAPTURED' or item.get('dom_witness_present') is not True:
            raise RuntimeError(f'BATCH13_BLOCKED_CAPTURE_EVIDENCE_MISMATCH:{day}')
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding='utf-8')
    for token in [item['reason_token'] for item in PASS_RECORDS.values()]:
        if token in calendar_text:
            raise RuntimeError('BATCH13_ALREADY_OR_PARTIALLY_INTEGRATED')
    for day in BLOCKED_DAYS:
        y, m, d = map(int, day.split('-'))
        if f'date({y}, {m}, {d}):' in calendar_text:
            raise RuntimeError(f'BATCH13_BLOCKED_DAY_MUST_NOT_BE_IN_CALENDAR:{day}')
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger.get('attempts')
    if not isinstance(attempts, list) or len(attempts) != 60:
        raise RuntimeError('PRE_BATCH13_ATTEMPT_COUNT_MISMATCH')
    if any(str(item.get('attempt_id', '')).startswith('batch13:') for item in attempts):
        raise RuntimeError('BATCH13_ATTEMPTS_ALREADY_PRESENT')


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
            "reports/data-qualification/historical_trading_breaks_recovery_batch13_qualification.md"
        ),
    }},
'''


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding='utf-8')
    block = ''.join(render_entry(day, PASS_RECORDS[day]) for day in PASS_RECORDS)
    marker = '}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text = replace_once(text, marker, block + marker, 'Batch13 calendar insertion')
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
        zip(batch13_targets(), report['adjudications'], strict=True), start=61
    ):
        outcome = adjudication['verdict']
        if outcome not in {'PASS', 'BLOCKED'}:
            raise RuntimeError(f'BATCH13_UNINTEGRABLE_OUTCOME:{day}:{outcome}')
        if outcome == 'BLOCKED' and day.isoformat() not in BLOCKED_DAYS:
            raise RuntimeError(f'BATCH13_UNEXPECTED_BLOCKED_DAY:{day}')
        attempts.append(
            {
                'attempt_sequence': sequence,
                'attempt_id': f'batch13:{day.isoformat()}',
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
    if len(attempts) != 65:
        raise RuntimeError('BATCH13_POST_LEDGER_COUNT_MISMATCH')
    LEDGER.write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')


def rewrite_current_state_tests() -> None:
    replacements = {
        'assert len(attempts) == 60': 'assert len(attempts) == 65',
        'list(range(1, 61))': 'list(range(1, 66))',
        'len({item.attempt_id for item in attempts}) == 60': 'len({item.attempt_id for item in attempts}) == 65',
        'assert len(queue) == 22': 'assert len(queue) == 19',
        'assert len(decisions) == len(queue) == 22': 'assert len(decisions) == len(queue) == 19',
        'assert len(recovery_queue()) == len(decisions) == 22': 'assert len(recovery_queue()) == len(decisions) == 19',
        'assert len(eligible) == 8': 'assert len(eligible) == 3',
        '== 14': '== 16',
        '(111, 69, 42)': '(111, 72, 39)',
        '(68, 46, 22)': '(68, 49, 19)',
        'global_report["resolved_candidate_dates"] == 69': 'global_report["resolved_candidate_dates"] == 72',
        'global_report["unresolved_candidate_dates"] == 42': 'global_report["unresolved_candidate_dates"] == 39',
        'window_report["resolved_candidate_dates"] == 46': 'window_report["resolved_candidate_dates"] == 49',
        'window_report["unresolved_candidate_dates"] == 22': 'window_report["unresolved_candidate_dates"] == 19',
        'eligible[0] == (date(2026, 1, 1), "NEW_YEARS_OBSERVED")': 'eligible[0] == (date(2026, 6, 19), "JUNETEENTH_OBSERVED")',
        "eligible[0] == (date(2026, 1, 1), 'NEW_YEARS_OBSERVED')": "eligible[0] == (date(2026, 6, 19), 'JUNETEENTH_OBSERVED')",
        'post_batch12_state': 'post_batch13_state',
        'post_batch12_progression_state': 'post_batch13_progression_state',
    }
    excluded = {
        'test_trading_breaks_recovery_batch13.py',
        'test_trading_breaks_recovery_batch13_adjudication.py',
        'test_trading_breaks_recovery_batch13_execution_contract.py',
        'test_trading_breaks_recovery_batch13_integration_contract.py',
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
    print('PASS: prepared Batch 13 atomic worktree integration')
    print('calendar PASS dates:', ', '.join(PASS_RECORDS))
    print('ledger attempts: 61..65')
    print('blocked unresolved dates:', ', '.join(BLOCKED_DAYS))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

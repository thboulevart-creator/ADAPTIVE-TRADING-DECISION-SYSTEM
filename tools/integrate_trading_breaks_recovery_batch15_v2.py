from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch15 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch15_targets,
)
from tools.trading_breaks_recovery_batch15_v2_adjudication import adjudicate_batch15
from tools.trading_breaks_target_day_overlap_semantics import load_class_a_evidence

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / 'tools' / 'dukascopy_usatech_calendar.py'
LEDGER = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_attempt_ledger.json'
ADJUDICATION_REPORT = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch15_v2_adjudication.md'

REASON_TOKENS = {
    '2021-12-24': 'SPECIAL_CHRISTMAS_OBSERVED_2021_OVERLAP_V2',
    '2022-04-15': 'SPECIAL_GOOD_FRIDAY_2022_OVERLAP_V2',
    '2022-12-26': 'SPECIAL_CHRISTMAS_OBSERVED_2022_OVERLAP_V2',
    '2023-01-02': 'SPECIAL_NEW_YEARS_OBSERVED_2023_OVERLAP_V2',
    '2023-07-04': 'SPECIAL_INDEPENDENCE_DAY_OBSERVED_2023_OVERLAP_V2',
}


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


def authoritative_adjudication() -> dict:
    report_text = ADJUDICATION_REPORT.read_text(encoding='utf-8')
    required = (
        'PASS — BATCH15_V2_EVIDENCE_INDEPENDENTLY_ADJUDICATED_OFFLINE',
        '35068120024 / 104702999768',
        '6dc134aa53a0904cda6c08108377dd8be8dd718c',
        '5 PASS / 0 BLOCKED / 0 FAIL',
    )
    for token in required:
        if token not in report_text:
            raise RuntimeError(f'BATCH15_PERSISTED_ADJUDICATION_REPORT_MISMATCH:{token}')

    report = adjudicate_batch15()
    if report.get('schema') != 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH15_V2_ADJUDICATION_V1':
        raise RuntimeError('BATCH15_ADJUDICATION_SCHEMA_MISMATCH')
    if report.get('verdict') != 'PASS':
        raise RuntimeError('BATCH15_ADJUDICATION_NOT_PASS')
    if (report.get('attempted'), report.get('pass'), report.get('blocked'), report.get('fail')) != (5, 5, 0, 0):
        raise RuntimeError('BATCH15_ADJUDICATION_ACCOUNTING_MISMATCH')
    expected = [(d.isoformat(), r) for d, r in batch15_targets()]
    observed = [(x.get('target_date'), x.get('candidate_reason')) for x in report.get('adjudications', [])]
    if observed != expected:
        raise RuntimeError('BATCH15_ADJUDICATION_IDENTITY_OR_ORDER_MISMATCH')
    return report


def raw_source_by_day() -> dict[str, dict]:
    result = {}
    frozen = {d for d, _ in batch15_targets()}
    for day, reason, raw, provenance, source_batch in load_class_a_evidence():
        if day not in frozen:
            continue
        records = raw.get('matching_records')
        if not isinstance(records, list) or len(records) != 1:
            raise RuntimeError(f'BATCH15_RAW_RECORD_CARDINALITY:{day}')
        record = records[0]
        broker_reason = str(record.get('reason', '')).strip()
        if not broker_reason:
            raise RuntimeError(f'BATCH15_RAW_BROKER_REASON_MISSING:{day}')
        result[day.isoformat()] = {
            'candidate_reason': reason,
            'broker_reason': broker_reason,
            'target_epoch_ms': raw.get('target_epoch_ms'),
            'source_batch': source_batch,
            'provenance': provenance,
        }
    if list(result) != [d.isoformat() for d, _ in batch15_targets()]:
        raise RuntimeError('BATCH15_RAW_SOURCE_IDENTITY_MISMATCH')
    return result


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding='utf-8')
    for day, _ in batch15_targets():
        if f'date({day.year}, {day.month}, {day.day}):' in calendar_text:
            raise RuntimeError(f'BATCH15_TARGET_ALREADY_IN_CALENDAR:{day}')
    for token in REASON_TOKENS.values():
        if token in calendar_text:
            raise RuntimeError(f'BATCH15_REASON_TOKEN_ALREADY_IN_CALENDAR:{token}')

    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger.get('attempts')
    if not isinstance(attempts, list) or len(attempts) != 68:
        raise RuntimeError('PRE_BATCH15_ATTEMPT_COUNT_MISMATCH')
    if [item.get('attempt_sequence') for item in attempts] != list(range(1, 69)):
        raise RuntimeError('PRE_BATCH15_ATTEMPT_SEQUENCE_MISMATCH')
    if any(str(item.get('attempt_id', '')).startswith('overlap-v2:') for item in attempts):
        raise RuntimeError('BATCH15_V2_RETRY_ATTEMPTS_ALREADY_PRESENT')
    if ledger.get('current_capability_id') != CURRENT_CAPABILITY_ID:
        raise RuntimeError('PRE_BATCH15_CURRENT_CAPABILITY_MISMATCH')


def render_entry(item: dict, raw: dict) -> str:
    day = item['target_date']
    year, month, day_number = map(int, day.split('-'))
    hours = tuple(item['fully_closed_hours_utc'])
    if not hours or hours != tuple(range(hours[0], hours[-1] + 1)):
        raise RuntimeError(f'BATCH15_NONCONTIGUOUS_HOURS:{day}')
    epoch = raw['target_epoch_ms']
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch <= 0:
        raise RuntimeError(f'BATCH15_TARGET_EPOCH_INVALID:{day}')
    return f'''    date({year}, {month}, {day_number}): {{
        "reason": "{REASON_TOKENS[day]}",
        "fully_closed_hours_utc": frozenset(range({hours[0]}, {hours[-1] + 1})),
        "broker_record_id": "{item['record_id']}",
        "broker_reason": {raw['broker_reason']!r},
        "artifact_id": {item['artifact_id']},
        "artifact_sha256": "{item['artifact_sha256']}",
        "probe_commit": "{item['probe_commit']}",
        "target_day_overlap_capability": "{CURRENT_CAPABILITY_ID}",
        "source_attempt_id": "{item['source_attempt_id']}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={epoch}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{item['workflow_run']}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/historical_trading_breaks_recovery_batch15_v2_adjudication.md"
        ),
    }},
'''


def integrate_calendar(report: dict, raw_sources: dict[str, dict]) -> None:
    text = CALENDAR.read_text(encoding='utf-8')
    block = ''.join(render_entry(item, raw_sources[item['target_date']]) for item in report['adjudications'])
    marker = '}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text = replace_once(text, marker, block + marker, 'Batch15 V2 calendar insertion')
    CALENDAR.write_text(text, encoding='utf-8')


def integrate_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    attempts = ledger['attempts']
    before = json.dumps(attempts, sort_keys=True)
    for sequence, ((day, reason), item) in enumerate(
        zip(batch15_targets(), report['adjudications'], strict=True), start=69
    ):
        if item['verdict'] != 'PASS' or item['reason'] != 'TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED':
            raise RuntimeError(f'BATCH15_UNINTEGRABLE_ADJUDICATION:{day}')
        attempts.append(
            {
                'attempt_sequence': sequence,
                'attempt_id': f'overlap-v2:{day.isoformat()}',
                'batch_contract': BATCH_CONTRACT,
                'target_date': day.isoformat(),
                'candidate_reason': reason,
                'outcome': 'PASS',
                'adjudication_reason': item['reason'],
                'blocking_reason': None,
                'capability_id': CURRENT_CAPABILITY_ID,
                'provenance': {
                    'workflow_run': item['workflow_run'],
                    'job_id': item['job_id'],
                    'artifact_id': item['artifact_id'],
                    'artifact_sha256': item['artifact_sha256'],
                    'probe_commit': item['probe_commit'],
                },
            }
        )
    if len(attempts) != 73:
        raise RuntimeError('BATCH15_POST_LEDGER_COUNT_MISMATCH')
    if [x['attempt_sequence'] for x in attempts] != list(range(1, 74)):
        raise RuntimeError('BATCH15_POST_LEDGER_SEQUENCE_MISMATCH')
    if len({x['attempt_id'] for x in attempts}) != 73:
        raise RuntimeError('BATCH15_POST_LEDGER_DUPLICATE_ATTEMPT_ID')
    if json.dumps(attempts[:68], sort_keys=True) != before:
        raise RuntimeError('BATCH15_HISTORICAL_ATTEMPTS_MUTATED')
    LEDGER.write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')


def main() -> int:
    guard_preintegration_state()
    report = authoritative_adjudication()
    raw_sources = raw_source_by_day()
    integrate_calendar(report, raw_sources)
    integrate_ledger(report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

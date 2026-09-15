from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_batch13 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch13_targets,
)
from tools.trading_breaks_recovery_protocol import (
    CONTRACT as RECOVERY_PROTOCOL,
    RecoveryEvidence,
    derive_fully_closed_hours_utc,
    derive_interval,
    validate_positive_recovery_against_frozen_batch,
)

REPO = Path(__file__).resolve().parents[1]
RUNTIME_PATH = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch13_runtime.json'
ADJUDICATION_JSON = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch13_adjudication.json'
QUALIFICATION_MD = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch13_qualification.md'

EXPECTED_RUN = 35020650564
EXPECTED_JOB = 104555157264
EXPECTED_ARTIFACT = 10416898441
EXPECTED_ARTIFACT_SHA256 = '59c93ab69bb1484fa0578bb8704aea76f15d67765e9a27ec0416c615d83faec8'
EXPECTED_PROBE_COMMIT = 'a974275d06ff45b0a78ad6558a6480e25cfe0f73'
EXPECTED_ARTIFACT_URL = (
    'https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/'
    'actions/runs/35020650564/artifacts/10416898441'
)
TARGET_INSTRUMENT_NAME = 'USATECH.IDX/USD'
TARGET_INSTRUMENT_ID = '9016'
ADJUDICATION_SCHEMA = 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH13_ADJUDICATION_V1'


def _epoch_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _iso_z(value: datetime) -> str:
    return value.isoformat().replace('+00:00', 'Z')


def _parse_dom_line(line: str) -> dict[str, Any]:
    parts = [part.strip() for part in line.split('\t')]
    if len(parts) != 4:
        raise ValueError('DOM_WITNESS_SHAPE_INVALID')
    instrument_name, start_raw, end_raw, reason = parts
    if instrument_name != TARGET_INSTRUMENT_NAME:
        raise ValueError('DOM_WITNESS_INSTRUMENT_NAME_MISMATCH')
    start = datetime.strptime(start_raw, '%d-%b-%y %H:%M:%S').replace(tzinfo=timezone.utc)
    end = datetime.strptime(end_raw, '%d-%b-%y %H:%M:%S').replace(tzinfo=timezone.utc)
    return {
        'instrument': TARGET_INSTRUMENT_ID,
        'start': _epoch_ms(start),
        'end': _epoch_ms(end),
        'reason': reason,
    }


def _dom_matches_network(dom: dict[str, Any], network: dict[str, Any]) -> bool:
    try:
        return (
            str(dom['instrument']) == str(network['instrument'])
            and int(dom['start']) == int(network['start'])
            and int(dom['end']) == int(network['end'])
            and str(dom.get('reason', '')).strip() == str(network.get('reason', '')).strip()
        )
    except (KeyError, TypeError, ValueError):
        return False


def _validate_runtime_identity(runtime: dict[str, Any]) -> dict[str, Any]:
    if runtime.get('schema') != BATCH_CONTRACT:
        raise ValueError('RUNTIME_SCHEMA_MISMATCH')
    if runtime.get('parent_protocol') != RECOVERY_PROTOCOL:
        raise ValueError('PARENT_PROTOCOL_MISMATCH')
    if runtime.get('parent_progression_contract') != PARENT_PROGRESSION_CONTRACT:
        raise ValueError('PARENT_PROGRESSION_MISMATCH')
    if runtime.get('batch_number') != 13 or runtime.get('batch_size') != BATCH_SIZE:
        raise ValueError('BATCH_IDENTITY_MISMATCH')
    if runtime.get('selection_rule') != SELECTION_RULE:
        raise ValueError('SELECTION_RULE_MISMATCH')
    if runtime.get('capability_id') != CURRENT_CAPABILITY_ID:
        raise ValueError('CAPABILITY_ID_MISMATCH')
    if runtime.get('capability_fingerprint') != CURRENT_CAPABILITY_FINGERPRINT:
        raise ValueError('CAPABILITY_FINGERPRINT_MISMATCH')

    expected_targets = [
        {'target_date': target_day.isoformat(), 'candidate_reason': reason}
        for target_day, reason in batch13_targets()
    ]
    if runtime.get('targets') != expected_targets:
        raise ValueError('FROZEN_MEMBERSHIP_MISMATCH')
    if runtime.get('read_only') is not True or runtime.get('market_data_written') is not False:
        raise ValueError('RUNTIME_READ_ONLY_BOUNDARY_MISMATCH')
    if runtime.get('workflow_run') != EXPECTED_RUN:
        raise ValueError('RUNTIME_RUN_ID_MISMATCH')
    if runtime.get('probe_commit') != EXPECTED_PROBE_COMMIT:
        raise ValueError('RUNTIME_PROBE_COMMIT_MISMATCH')

    provenance = runtime.get('provenance')
    if not isinstance(provenance, dict):
        raise ValueError('PROVENANCE_MISSING')
    expected = {
        'workflow_run': EXPECTED_RUN,
        'job_id': EXPECTED_JOB,
        'probe_commit': EXPECTED_PROBE_COMMIT,
        'artifact_id': EXPECTED_ARTIFACT,
        'artifact_url': EXPECTED_ARTIFACT_URL,
        'artifact_sha256': EXPECTED_ARTIFACT_SHA256,
    }
    for key, value in expected.items():
        if provenance.get(key) != value:
            raise ValueError(f'PROVENANCE_MISMATCH:{key}')
    return provenance


def _validate_capture_derivatives(
    network_record: dict[str, Any], target_day: date
) -> tuple[datetime, datetime, datetime, list[int]]:
    try:
        start, end, reopen = derive_interval(network_record)
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise ValueError('MALFORMED_NETWORK_INTERVAL') from exc
    expected_hours = sorted(derive_fully_closed_hours_utc(target_day, start, reopen))
    if network_record.get('start_utc') != _iso_z(start):
        raise ValueError('CAPTURE_DERIVED_START_MISMATCH')
    if network_record.get('end_last_closed_minute_utc') != _iso_z(end):
        raise ValueError('CAPTURE_DERIVED_END_MISMATCH')
    if network_record.get('derived_reopen_utc') != _iso_z(reopen):
        raise ValueError('CAPTURE_DERIVED_REOPEN_MISMATCH')
    if network_record.get('fully_closed_hours_utc') != expected_hours:
        raise ValueError('CAPTURE_DERIVED_CLOSED_HOURS_MISMATCH')
    return start, end, reopen, expected_hours


def _validate_result_envelope(
    raw: dict[str, Any], target_day: date, candidate_reason: str
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    if raw.get('target_date') != target_day.isoformat():
        raise ValueError('RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH')
    if raw.get('candidate_reason') != candidate_reason:
        raise ValueError('RESULT_REASON_MISMATCH')
    if raw.get('requested_date') != target_day.isoformat():
        raise ValueError('RESULT_REQUESTED_DATE_MISMATCH')
    midnight = datetime(target_day.year, target_day.month, target_day.day, tzinfo=timezone.utc)
    if raw.get('target_epoch_ms') != _epoch_ms(midnight):
        raise ValueError('RESULT_TARGET_EPOCH_MISMATCH')
    if raw.get('instrument_id_expected') != TARGET_INSTRUMENT_ID:
        raise ValueError('RESULT_EXPECTED_INSTRUMENT_MISMATCH')
    if raw.get('instrument_id_observed') != TARGET_INSTRUMENT_ID:
        raise ValueError('RESULT_OBSERVED_INSTRUMENT_MISMATCH')
    if raw.get('instrument_name') != TARGET_INSTRUMENT_NAME:
        raise ValueError('RESULT_INSTRUMENT_NAME_MISMATCH')
    for key in ('official_page_status', 'current_control_status', 'target_nav_status'):
        status = raw.get(key)
        if not isinstance(status, int) or isinstance(status, bool) or not 200 <= status < 400:
            raise ValueError(f'RESULT_HTTP_STATUS_INVALID:{key}')
    statuses = raw.get('target_document_statuses')
    if not isinstance(statuses, list) or not statuses or any(
        not isinstance(status, int) or isinstance(status, bool) or not 200 <= status < 400
        for status in statuses
    ):
        raise ValueError('RESULT_TARGET_DOCUMENT_STATUS_INVALID')
    if raw.get('date_honored') is not True:
        raise ValueError('RESULT_DATE_NOT_HONORED')
    if raw.get('raw_payload_present') is not True:
        raise ValueError('RESULT_RAW_PAYLOAD_MISSING')
    if raw.get('runtime_errors'):
        raise ValueError('RESULT_RUNTIME_ERRORS_PRESENT')
    if raw.get('capture_verdict') not in {'CAPTURED', 'BLOCKED', 'FAIL'}:
        raise ValueError('CAPTURE_VERDICT_INVALID')
    if not isinstance(raw.get('capture_reason'), str) or not raw['capture_reason'].strip():
        raise ValueError('CAPTURE_REASON_MISSING')
    records = raw.get('matching_records')
    if not isinstance(records, list):
        raise ValueError('MATCHING_RECORDS_NOT_LIST')
    if len(records) > 1:
        raise ValueError('MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION')
    dom_lines = raw.get('dom_witness_lines')
    if not isinstance(dom_lines, list):
        raise ValueError('DOM_WITNESS_LINES_NOT_LIST')
    if len(dom_lines) > 1:
        raise ValueError('MULTIPLE_DOM_WITNESSES_REQUIRE_SEPARATE_ADJUDICATION')
    if not records and dom_lines:
        raise ValueError('DOM_WITNESS_WITHOUT_NETWORK_RECORD')
    return records, _parse_dom_line(dom_lines[0]) if dom_lines else None


def _blocked(
    target_day: date,
    candidate_reason: str,
    provenance: dict[str, Any],
    network_record: dict[str, Any] | None,
    reason: str,
) -> dict[str, Any]:
    return {
        'schema': RECOVERY_PROTOCOL,
        'verdict': 'BLOCKED',
        'reason': reason,
        'target_date': target_day.isoformat(),
        'candidate_reason': candidate_reason,
        'instrument': TARGET_INSTRUMENT_NAME,
        'instrument_id': TARGET_INSTRUMENT_ID,
        'overlap_record_id': str(network_record.get('id')) if network_record else None,
        'workflow_run': provenance['workflow_run'],
        'artifact_id': provenance['artifact_id'],
        'artifact_sha256': provenance['artifact_sha256'],
        'probe_commit': provenance['probe_commit'],
    }


def _adjudicate_one(
    raw: dict[str, Any],
    target_day: date,
    candidate_reason: str,
    provenance: dict[str, Any],
    expected_targets: list[tuple[date, str]],
) -> dict[str, Any]:
    records, dom_record = _validate_result_envelope(raw, target_day, candidate_reason)
    network_record = records[0] if records else None
    if network_record is not None:
        try:
            start, end, reopen, _ = _validate_capture_derivatives(network_record, target_day)
        except ValueError as exc:
            return {'verdict': 'FAIL', 'reason': str(exc)}
        if end < start:
            return {'verdict': 'FAIL', 'reason': 'MALFORMED_NETWORK_INTERVAL'}
        if start.date() != target_day:
            target_start = datetime(target_day.year, target_day.month, target_day.day, tzinfo=timezone.utc)
            target_end = target_start + timedelta(days=1)
            if not (start < target_end and reopen > target_start):
                verdict = {'verdict': 'FAIL', 'reason': 'NON_TARGET_RECORD_DOES_NOT_OVERLAP_TARGET_DAY'}
            elif dom_record is not None and not _dom_matches_network(dom_record, network_record):
                verdict = {'verdict': 'FAIL', 'reason': 'DOM_NETWORK_CONTRADICTION'}
            else:
                verdict = _blocked(
                    target_day,
                    candidate_reason,
                    provenance,
                    network_record,
                    'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE',
                )
        elif dom_record is None:
            verdict = _blocked(
                target_day,
                candidate_reason,
                provenance,
                network_record,
                'EXPECTED_DOM_CROSSCHECK_MISSING',
            )
        elif not _dom_matches_network(dom_record, network_record):
            verdict = {'verdict': 'FAIL', 'reason': 'DOM_NETWORK_CONTRADICTION'}
        elif raw.get('capture_verdict') == 'FAIL':
            verdict = {'verdict': 'FAIL', 'reason': 'CAPTURE_LAYER_FAIL_REQUIRES_REMEDIATION'}
        elif raw.get('capture_verdict') == 'BLOCKED':
            verdict = _blocked(
                target_day,
                candidate_reason,
                provenance,
                network_record,
                str(raw['capture_reason']),
            )
        else:
            evidence = RecoveryEvidence(
                target_date=target_day,
                candidate_reason=candidate_reason,
                requested_date=target_day,
                instrument_id=str(raw['instrument_id_observed']),
                instrument_name=str(raw['instrument_name']),
                network_record=network_record,
                raw_payload_present=True,
                dom_available=True,
                dom_record=dom_record,
                workflow_run=provenance['workflow_run'],
                artifact_id=provenance['artifact_id'],
                artifact_sha256=provenance['artifact_sha256'],
                probe_commit=provenance['probe_commit'],
            )
            verdict = validate_positive_recovery_against_frozen_batch(evidence, expected_targets)
    else:
        if raw.get('capture_verdict') == 'FAIL':
            verdict = {'verdict': 'FAIL', 'reason': 'CAPTURE_LAYER_FAIL_REQUIRES_REMEDIATION'}
        else:
            evidence = RecoveryEvidence(
                target_date=target_day,
                candidate_reason=candidate_reason,
                requested_date=target_day,
                instrument_id=str(raw['instrument_id_observed']),
                instrument_name=str(raw['instrument_name']),
                network_record=None,
                raw_payload_present=True,
                dom_available=False,
                dom_record=None,
                workflow_run=provenance['workflow_run'],
                artifact_id=provenance['artifact_id'],
                artifact_sha256=provenance['artifact_sha256'],
                probe_commit=provenance['probe_commit'],
            )
            verdict = validate_positive_recovery_against_frozen_batch(evidence, expected_targets)
    verdict['capture_verdict'] = raw.get('capture_verdict')
    verdict['capture_reason'] = raw.get('capture_reason')
    verdict['broker_record_id'] = network_record.get('id') if network_record else None
    verdict['broker_reason'] = network_record.get('reason') if network_record else None
    verdict['dom_witness_present'] = dom_record is not None
    return verdict


def adjudicate_runtime(runtime: dict[str, Any]) -> dict[str, Any]:
    provenance = _validate_runtime_identity(runtime)
    results = runtime.get('results')
    if not isinstance(results, list) or len(results) != BATCH_SIZE:
        raise ValueError('RESULT_COUNT_MISMATCH')
    expected_targets = batch13_targets()
    adjudications = [
        _adjudicate_one(raw, day, reason, provenance, expected_targets)
        for raw, (day, reason) in zip(results, expected_targets, strict=True)
    ]
    counts = {
        key: sum(item.get('verdict') == key for item in adjudications)
        for key in ('PASS', 'BLOCKED', 'FAIL')
    }
    overall = 'PASS' if counts['FAIL'] == 0 else 'FAIL'
    return {
        'schema': ADJUDICATION_SCHEMA,
        'batch_contract': BATCH_CONTRACT,
        'parent_protocol': RECOVERY_PROTOCOL,
        'verdict': overall,
        'reason': (
            'BATCH13_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION'
            if overall == 'PASS'
            else 'BATCH13_ADJUDICATION_CONTAINS_FAIL'
        ),
        'attempted': BATCH_SIZE,
        'pass': counts['PASS'],
        'blocked': counts['BLOCKED'],
        'fail': counts['FAIL'],
        'provenance': provenance,
        'adjudications': adjudications,
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        '# HISTORICAL TRADING BREAKS RECOVERY — BATCH 13 INDEPENDENT ADJUDICATION',
        '',
        f"**{report['verdict']} — `{report['reason']}`**",
        '',
        '## Authoritative runtime provenance',
        '',
        f'- workflow run: `{EXPECTED_RUN}`',
        f'- job: `{EXPECTED_JOB}`',
        f'- probe commit: `{EXPECTED_PROBE_COMMIT}`',
        f'- artifact: `{EXPECTED_ARTIFACT}`',
        f'- artifact SHA-256: `{EXPECTED_ARTIFACT_SHA256}`',
        '- browser/network acquisition during adjudication: `NONE`',
        '',
        '## Independent date-level adjudication',
        '',
    ]
    for item, (target_day, reason) in zip(report['adjudications'], batch13_targets(), strict=True):
        lines += [
            f'### {target_day.isoformat()} — {reason}',
            '',
            f"**{item['verdict']} — `{item['reason']}`**",
            '',
        ]
        if item['verdict'] == 'PASS':
            lines += [
                f"- broker record: `{item['broker_record_id']}`",
                f"- broker reason: `{item['broker_reason']}`",
                f"- start: `{item['break_start_utc']}`",
                f"- final closed minute: `{item['final_closed_minute_utc']}`",
                f"- calibrated reopen: `{item['reopen_utc']}`",
                f"- fully closed UTC hours: `{item['fully_closed_hours_utc']}`",
                '',
            ]
        elif item['verdict'] == 'BLOCKED':
            lines += [
                f"- broker/overlap record: `{item.get('broker_record_id')}`",
                '- cross-date overlap is retained as evidence but is not promoted into exact target-date evidence.',
                '',
            ]
    lines += [
        '## Final accounting',
        '',
        f"- attempted: `{report['attempted']}`",
        f"- PASS: `{report['pass']}`",
        f"- BLOCKED: `{report['blocked']}`",
        f"- FAIL: `{report['fail']}`",
        '',
        'Evidence-only adjudication: no calendar, ledger, progression, capability, or execution-window mutation.',
    ]
    return '\n'.join(lines).rstrip() + '\n'


def main() -> int:
    runtime = json.loads(RUNTIME_PATH.read_text(encoding='utf-8'))
    report = adjudicate_runtime(runtime)
    ADJUDICATION_JSON.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    QUALIFICATION_MD.write_text(_render_markdown(report), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0 if report['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

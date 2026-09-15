from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_batch13_adjudication import _adjudicate_one
from tools.trading_breaks_recovery_batch14 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch14_targets,
)
from tools.trading_breaks_recovery_protocol import CONTRACT as RECOVERY_PROTOCOL

REPO = Path(__file__).resolve().parents[1]
RUNTIME_PATH = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch14_runtime.json'
ADJUDICATION_JSON = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch14_adjudication.json'
QUALIFICATION_MD = REPO / 'reports' / 'data-qualification' / 'historical_trading_breaks_recovery_batch14_qualification.md'

EXPECTED_RUN = 35023845609
EXPECTED_JOB = 104565948108
EXPECTED_ARTIFACT = 10418961548
EXPECTED_ARTIFACT_SHA256 = '00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910'
EXPECTED_PROBE_COMMIT = '4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b'
EXPECTED_ARTIFACT_URL = (
    'https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/'
    'actions/runs/35023845609/artifacts/10418961548'
)
ADJUDICATION_SCHEMA = 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH14_ADJUDICATION_V1'


def _validate_runtime_identity(runtime: dict[str, Any]) -> dict[str, Any]:
    if runtime.get('schema') != BATCH_CONTRACT:
        raise ValueError('RUNTIME_SCHEMA_MISMATCH')
    if runtime.get('parent_protocol') != RECOVERY_PROTOCOL:
        raise ValueError('PARENT_PROTOCOL_MISMATCH')
    if runtime.get('parent_progression_contract') != PARENT_PROGRESSION_CONTRACT:
        raise ValueError('PARENT_PROGRESSION_MISMATCH')
    if runtime.get('batch_number') != 14 or runtime.get('batch_size') != BATCH_SIZE:
        raise ValueError('BATCH_IDENTITY_MISMATCH')
    if runtime.get('selection_rule') != SELECTION_RULE:
        raise ValueError('SELECTION_RULE_MISMATCH')
    if runtime.get('capability_id') != CURRENT_CAPABILITY_ID:
        raise ValueError('CAPABILITY_ID_MISMATCH')
    if runtime.get('capability_fingerprint') != CURRENT_CAPABILITY_FINGERPRINT:
        raise ValueError('CAPABILITY_FINGERPRINT_MISMATCH')

    expected_targets = [
        {'target_date': day.isoformat(), 'candidate_reason': reason}
        for day, reason in batch14_targets()
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


def _bind_target_identity(
    item: dict[str, Any], target_day, candidate_reason: str, provenance: dict[str, Any]
) -> dict[str, Any]:
    bound = dict(item)
    bound.setdefault('schema', RECOVERY_PROTOCOL)
    bound.setdefault('target_date', target_day.isoformat())
    bound.setdefault('candidate_reason', candidate_reason)
    bound.setdefault('workflow_run', provenance['workflow_run'])
    bound.setdefault('artifact_id', provenance['artifact_id'])
    bound.setdefault('artifact_sha256', provenance['artifact_sha256'])
    bound.setdefault('probe_commit', provenance['probe_commit'])
    return bound


def adjudicate_runtime(runtime: dict[str, Any]) -> dict[str, Any]:
    provenance = _validate_runtime_identity(runtime)
    results = runtime.get('results')
    if not isinstance(results, list) or len(results) != BATCH_SIZE:
        raise ValueError('RESULT_COUNT_MISMATCH')

    expected_targets = batch14_targets()
    adjudications = []
    for raw, (day, reason) in zip(results, expected_targets, strict=True):
        item = _adjudicate_one(raw, day, reason, provenance, expected_targets)
        adjudications.append(_bind_target_identity(item, day, reason, provenance))

    counts = {
        verdict: sum(item.get('verdict') == verdict for item in adjudications)
        for verdict in ('PASS', 'BLOCKED', 'FAIL')
    }
    overall = 'PASS' if counts['FAIL'] == 0 else 'FAIL'
    return {
        'schema': ADJUDICATION_SCHEMA,
        'batch_contract': BATCH_CONTRACT,
        'parent_protocol': RECOVERY_PROTOCOL,
        'verdict': overall,
        'reason': (
            'BATCH14_TERMINAL_RECORDS_INDEPENDENTLY_ADJUDICATED'
            if overall == 'PASS'
            else 'BATCH14_ADJUDICATION_CONTAINS_FAIL'
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
        '# HISTORICAL TRADING BREAKS RECOVERY — BATCH 14 TERMINAL INDEPENDENT ADJUDICATION',
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
    for item, (target_day, reason) in zip(report['adjudications'], batch14_targets(), strict=True):
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
                f"- capture verdict: `{item.get('capture_verdict')}`",
                f"- broker record: `{item.get('broker_record_id')}`",
                '- unresolved evidence is retained and is not promoted into executable calendar evidence.',
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

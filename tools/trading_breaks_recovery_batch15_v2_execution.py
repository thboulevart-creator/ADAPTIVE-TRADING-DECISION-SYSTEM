from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_batch15 import (
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    batch15_targets,
)

CONTRACT = 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH15_V2_EXECUTION_V1'
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reports' / 'data-qualification' / 'trading_breaks_target_day_overlap_readjudication.json'
SOURCE_CONTRACT = 'TRADING_BREAKS_TARGET_DAY_OVERLAP_READJUDICATION_V1'
SOURCE_REASON = 'ALL_14_CLASS_A_DATES_OFFLINE_READJUDICATED_UNDER_QUALIFIED_V2'


def select_persisted_evidence() -> dict[str, Any]:
    report = json.loads(SOURCE.read_text(encoding='utf-8'))
    if report.get('schema') != SOURCE_CONTRACT or report.get('verdict') != 'PASS':
        raise ValueError('PERSISTED_CLASS_A_READJUDICATION_NOT_AUTHORITATIVE_PASS')
    if report.get('reason') != SOURCE_REASON:
        raise ValueError('PERSISTED_CLASS_A_READJUDICATION_REASON_MISMATCH')
    if report.get('current_capability_id') != CURRENT_CAPABILITY_ID:
        raise ValueError('BATCH15_SOURCE_CAPABILITY_ID_MISMATCH')
    if report.get('current_capability_fingerprint') != CURRENT_CAPABILITY_FINGERPRINT:
        raise ValueError('BATCH15_SOURCE_CAPABILITY_FINGERPRINT_MISMATCH')
    if (report.get('historical_attempt_count'), report.get('material_capability_change_count')) != (68, 1):
        raise ValueError('BATCH15_SOURCE_GOVERNANCE_COUNTS_MISMATCH')
    if (report.get('readjudicated_count'), report.get('pass_count'), report.get('blocked_count'), report.get('fail_count')) != (14, 14, 0, 0):
        raise ValueError('BATCH15_SOURCE_ACCOUNTING_MISMATCH')

    results = report.get('results')
    if not isinstance(results, list) or len(results) != 14:
        raise ValueError('BATCH15_SOURCE_RESULTS_MISMATCH')
    by_key = {(item.get('target_date'), item.get('candidate_reason')): item for item in results}
    if len(by_key) != 14:
        raise ValueError('BATCH15_SOURCE_DUPLICATE_RESULT')

    selected: list[dict[str, Any]] = []
    for day, reason in batch15_targets():
        key = (day.isoformat(), reason)
        item = by_key.get(key)
        if item is None:
            raise ValueError(f'BATCH15_FROZEN_SOURCE_MISSING:{day}')
        if item.get('verdict') != 'PASS':
            raise ValueError(f'BATCH15_FROZEN_SOURCE_NOT_PASS:{day}')
        if item.get('reason') != 'TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED':
            raise ValueError(f'BATCH15_FROZEN_SOURCE_REASON_MISMATCH:{day}')
        if item.get('schema') != 'TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1':
            raise ValueError(f'BATCH15_FROZEN_SOURCE_SCHEMA_MISMATCH:{day}')
        if item.get('source_capability_id') != 'TRADING_BREAKS_PRIMARY_WIDGET_V1':
            raise ValueError(f'BATCH15_SOURCE_ATTEMPT_CAPABILITY_MISMATCH:{day}')
        if item.get('readjudication_capability_id') != CURRENT_CAPABILITY_ID:
            raise ValueError(f'BATCH15_READJUDICATION_CAPABILITY_MISMATCH:{day}')
        if item.get('readjudication_capability_fingerprint') != CURRENT_CAPABILITY_FINGERPRINT:
            raise ValueError(f'BATCH15_READJUDICATION_FINGERPRINT_MISMATCH:{day}')
        if item.get('proposed_retry_attempt_id') != f'overlap-v2:{day.isoformat()}':
            raise ValueError(f'BATCH15_RETRY_ID_MISMATCH:{day}')
        if not item.get('cross_date'):
            raise ValueError(f'BATCH15_EXPECTED_CROSS_DATE_EVIDENCE_MISSING:{day}')
        selected.append(item)

    if [(item['target_date'], item['candidate_reason']) for item in selected] != [
        (day.isoformat(), reason) for day, reason in batch15_targets()
    ]:
        raise ValueError('BATCH15_SELECTED_ORDER_MISMATCH')

    return {
        'schema': CONTRACT,
        'verdict': 'PASS',
        'reason': 'EXACT_FROZEN_BATCH15_PERSISTED_V2_EVIDENCE_SELECTED_WITHOUT_RECAPTURE',
        'capture_mode': 'PERSISTED_OFFLINE_READJUDICATION_REUSE',
        'browser_used': False,
        'probe_used': False,
        'network_used': False,
        'selected_count': 5,
        'pass_count': 5,
        'blocked_count': 0,
        'fail_count': 0,
        'results': selected,
    }


def main() -> int:
    print(json.dumps(select_persisted_evidence(), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

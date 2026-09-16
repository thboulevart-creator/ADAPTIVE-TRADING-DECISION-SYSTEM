from __future__ import annotations

import json
from typing import Any

from tools.trading_breaks_recovery_batch15 import (
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    batch15_targets,
)
from tools.trading_breaks_recovery_batch15_v2_execution import select_persisted_evidence
from tools.trading_breaks_recovery_progression import load_attempt_ledger
from tools.trading_breaks_target_day_overlap_semantics import (
    load_class_a_evidence,
    validate_target_day_overlap_result,
)

CONTRACT = 'HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH15_V2_ADJUDICATION_V1'


def adjudicate_batch15() -> dict[str, Any]:
    execution = select_persisted_evidence()
    if execution.get('verdict') != 'PASS' or execution.get('selected_count') != 5:
        raise ValueError('BATCH15_EXECUTION_NOT_AUTHORITATIVE_PASS')

    _, current_id, attempts = load_attempt_ledger()
    if current_id != CURRENT_CAPABILITY_ID or len(attempts) != 68:
        raise ValueError('BATCH15_ADJUDICATION_GOVERNANCE_STATE_MISMATCH')
    attempts_by_day = {}
    for attempt in attempts:
        attempts_by_day.setdefault(attempt.target_date, []).append(attempt)

    raw_by_key = {
        (day, reason): (raw, provenance, source_batch)
        for day, reason, raw, provenance, source_batch in load_class_a_evidence()
    }
    execution_by_key = {
        (item['target_date'], item['candidate_reason']): item
        for item in execution['results']
    }

    results: list[dict[str, Any]] = []
    for day, reason in batch15_targets():
        raw, provenance, source_batch = raw_by_key[(day, reason)]
        fresh = validate_target_day_overlap_result(raw, day, reason, provenance)
        if fresh.get('verdict') != 'PASS':
            raise ValueError(f'BATCH15_FRESH_ADJUDICATION_FAILED:{day}:{fresh}')
        persisted = execution_by_key[(day.isoformat(), reason)]
        for key in (
            'target_date',
            'candidate_reason',
            'record_id',
            'record_start_utc',
            'record_end_last_closed_minute_utc',
            'reopen_utc',
            'fully_closed_hours_utc',
            'artifact_id',
            'artifact_sha256',
            'probe_commit',
            'workflow_run',
            'job_id',
            'dom_crosscheck',
            'cross_date',
        ):
            if fresh.get(key) != persisted.get(key):
                raise ValueError(f'BATCH15_EXECUTION_FRESH_MISMATCH:{day}:{key}')

        history = attempts_by_day.get(day, [])
        if not history:
            raise ValueError(f'BATCH15_SOURCE_ATTEMPT_MISSING:{day}')
        source_attempt = max(history, key=lambda item: item.attempt_sequence)
        if source_attempt.attempt_id != persisted['source_attempt_id']:
            raise ValueError(f'BATCH15_SOURCE_ATTEMPT_ID_MISMATCH:{day}')
        if source_attempt.attempt_sequence != persisted['source_attempt_sequence']:
            raise ValueError(f'BATCH15_SOURCE_ATTEMPT_SEQUENCE_MISMATCH:{day}')
        if source_attempt.outcome != 'BLOCKED':
            raise ValueError(f'BATCH15_SOURCE_ATTEMPT_NOT_BLOCKED:{day}')
        if source_attempt.blocking_reason != 'NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE':
            raise ValueError(f'BATCH15_SOURCE_BLOCKER_MISMATCH:{day}')

        results.append(
            {
                **fresh,
                'source_batch': source_batch,
                'source_attempt_id': source_attempt.attempt_id,
                'source_attempt_sequence': source_attempt.attempt_sequence,
                'source_capability_id': source_attempt.capability_id,
                'adjudication_capability_id': CURRENT_CAPABILITY_ID,
                'adjudication_capability_fingerprint': CURRENT_CAPABILITY_FINGERPRINT,
                'retry_attempt_id': f'overlap-v2:{day.isoformat()}',
            }
        )

    if [(item['target_date'], item['candidate_reason']) for item in results] != [
        (day.isoformat(), reason) for day, reason in batch15_targets()
    ]:
        raise ValueError('BATCH15_ADJUDICATION_ORDER_MISMATCH')

    return {
        'schema': CONTRACT,
        'verdict': 'PASS',
        'reason': 'BATCH15_FROZEN_V2_EVIDENCE_INDEPENDENTLY_READJUDICATED_OFFLINE',
        'current_capability_id': CURRENT_CAPABILITY_ID,
        'current_capability_fingerprint': CURRENT_CAPABILITY_FINGERPRINT,
        'attempted': 5,
        'pass': 5,
        'blocked': 0,
        'fail': 0,
        'browser_used': False,
        'probe_used': False,
        'network_used': False,
        'adjudications': results,
    }


def main() -> int:
    print(json.dumps(adjudicate_batch15(), indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

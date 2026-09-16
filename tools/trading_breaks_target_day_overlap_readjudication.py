from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.activate_trading_breaks_target_day_overlap_capability import NEW_CAPABILITY_ID, NEW_FINGERPRINT
from tools.trading_breaks_recovery_progression import (
    current_capability,
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
)
from tools.trading_breaks_target_day_overlap_semantics import (
    CLASS_A_SOURCES,
    CONTRACT as SEMANTIC_CONTRACT,
    load_class_a_evidence,
    validate_target_day_overlap_result,
)

CONTRACT = "TRADING_BREAKS_TARGET_DAY_OVERLAP_READJUDICATION_V1"
ROOT = Path(__file__).resolve().parents[1]


def readjudicate_class_a() -> dict[str, Any]:
    capabilities, current_id, attempts = load_attempt_ledger()
    changes = load_material_capability_changes()
    if current_id != NEW_CAPABILITY_ID:
        raise ValueError(f"CURRENT_CAPABILITY_NOT_V2:{current_id}")
    if current_capability().fingerprint() != NEW_FINGERPRINT:
        raise ValueError("CURRENT_V2_FINGERPRINT_MISMATCH")
    if len(attempts) != 68:
        raise ValueError(f"HISTORICAL_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")
    if len(changes) != 1:
        raise ValueError(f"MATERIAL_CHANGE_COUNT_MISMATCH:{len(changes)}")
    if NEW_CAPABILITY_ID not in capabilities:
        raise ValueError("V2_CAPABILITY_MISSING")

    expected_queue = sorted((day, reason) for day, reason, _ in CLASS_A_SOURCES)
    if eligible_recovery_queue() != expected_queue:
        raise ValueError("V2_ELIGIBLE_QUEUE_NOT_EXACT_CLASS_A_SET")

    attempts_by_day: dict[Any, list[Any]] = {}
    for attempt in attempts:
        attempts_by_day.setdefault(attempt.target_date, []).append(attempt)

    results: list[dict[str, Any]] = []
    for target_day, reason, raw, provenance, source_batch in load_class_a_evidence():
        history = attempts_by_day.get(target_day, [])
        if not history:
            raise ValueError(f"SOURCE_ATTEMPT_HISTORY_MISSING:{target_day}")
        source_attempt = max(history, key=lambda item: item.attempt_sequence)
        if source_attempt.outcome != "BLOCKED":
            raise ValueError(f"SOURCE_ATTEMPT_NOT_BLOCKED:{target_day}")
        if source_attempt.blocking_reason != "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE":
            raise ValueError(f"SOURCE_BLOCKER_MISMATCH:{target_day}")
        verdict = validate_target_day_overlap_result(raw, target_day, reason, provenance)
        if verdict.get("verdict") != "PASS":
            raise ValueError(f"READJUDICATION_FAILED:{target_day}:{verdict}")
        results.append(
            {
                **verdict,
                "source_batch": source_batch,
                "source_attempt_id": source_attempt.attempt_id,
                "source_attempt_sequence": source_attempt.attempt_sequence,
                "source_capability_id": source_attempt.capability_id,
                "readjudication_capability_id": NEW_CAPABILITY_ID,
                "readjudication_capability_fingerprint": NEW_FINGERPRINT,
                "proposed_retry_attempt_id": f"overlap-v2:{target_day.isoformat()}",
            }
        )

    if len(results) != 14:
        raise ValueError(f"READJUDICATED_RESULT_COUNT_MISMATCH:{len(results)}")
    if len({item["target_date"] for item in results}) != 14:
        raise ValueError("READJUDICATION_DUPLICATE_TARGET")
    if len({item["proposed_retry_attempt_id"] for item in results}) != 14:
        raise ValueError("READJUDICATION_DUPLICATE_RETRY_ID")

    return {
        "schema": CONTRACT,
        "semantic_contract": SEMANTIC_CONTRACT,
        "verdict": "PASS",
        "reason": "ALL_14_CLASS_A_DATES_OFFLINE_READJUDICATED_UNDER_QUALIFIED_V2",
        "current_capability_id": NEW_CAPABILITY_ID,
        "current_capability_fingerprint": NEW_FINGERPRINT,
        "historical_attempt_count": 68,
        "material_capability_change_count": 1,
        "readjudicated_count": 14,
        "pass_count": 14,
        "blocked_count": 0,
        "fail_count": 0,
        "results": results,
    }


def main() -> int:
    print(json.dumps(readjudicate_class_a(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

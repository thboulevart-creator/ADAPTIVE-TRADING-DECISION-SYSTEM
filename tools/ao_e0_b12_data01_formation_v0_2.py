from __future__ import annotations

EVIDENCE_START_MS = 1791284400000
EVIDENCE_END_EXCLUSIVE_MS = 1822820400000
REFERENCE_PLANNING_N = 58927

def in_evidence_window(decision_time_ms: int) -> bool:
    if isinstance(decision_time_ms, bool) or not isinstance(decision_time_ms, int):
        raise ValueError("INVALID_DECISION_TIME")
    return EVIDENCE_START_MS <= decision_time_ms < EVIDENCE_END_EXCLUSIVE_MS

def collection_state(now_ms: int) -> str:
    if isinstance(now_ms, bool) or not isinstance(now_ms, int):
        raise ValueError("INVALID_NOW")
    if now_ms < EVIDENCE_START_MS:
        return "NOT_STARTED"
    if now_ms < EVIDENCE_END_EXCLUSIVE_MS:
        return "COLLECTING_WAIT_NOT_READY"
    return "FIXED_HORIZON_REACHED"

def identity() -> dict:
    return {
        "evidence_start_ms": EVIDENCE_START_MS,
        "evidence_end_exclusive_ms": EVIDENCE_END_EXCLUSIVE_MS,
        "duration_ms": EVIDENCE_END_EXCLUSIVE_MS - EVIDENCE_START_MS,
        "reference_planning_n": REFERENCE_PLANNING_N,
        "reference_planning_n_is_terminal_authority": False,
        "same_experiment_extension": "FORBIDDEN",
    }

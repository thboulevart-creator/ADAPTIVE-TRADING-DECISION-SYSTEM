from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "EXACT_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": poll_interval_seconds,
        "detection_latency_seconds_max": detection_latency_seconds_max,
        "clock_source": "EXPLICIT_INJECTED_SECONDS_ONLY",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _validate_observations(
    observations: list[dict[str, Any]],
    *,
    interval: int,
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    previous: int | None = None
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != {"at_seconds", "outcome"}:
            raise P5ETimingModelError("observation fields mismatch")
        at_seconds = observation["at_seconds"]
        outcome = observation["outcome"]
        if not _is_nonnegative_int(at_seconds):
            raise P5ETimingModelError("observation time must be nonnegative")
        if at_seconds % interval != 0:
            raise P5ETimingModelError(
                "observation time must lie on the exact 30-second schedule"
            )
        if previous is not None and at_seconds <= previous:
            raise P5ETimingModelError(
                "observation times must be strictly increasing"
            )
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        previous = at_seconds


def _result(
    *,
    status: str,
    detection_latency_seconds: int | None,
    first_detection_at_seconds: int | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_at_seconds": first_detection_at_seconds,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_available_at_seconds: int,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_available_at_seconds):
        raise P5ETimingModelError(
            "source availability time must be a nonnegative integer"
        )
    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    _validate_observations(observations, interval=interval)

    first_detection: int | None = None
    for observation in observations:
        at_seconds = observation["at_seconds"]
        if at_seconds < source_available_at_seconds:
            continue
        if observation["outcome"] == "EXACT_HEAD_OBSERVED":
            first_detection = at_seconds
            break

    if first_detection is not None:
        latency = first_detection - source_available_at_seconds
        if latency <= bound:
            return _result(
                status="PASS_DETECTED_WITHIN_BOUND",
                detection_latency_seconds=latency,
                first_detection_at_seconds=first_detection,
            )
        return _result(
            status="FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
            detection_latency_seconds=latency,
            first_detection_at_seconds=first_detection,
        )

    last_observation = observations[-1]["at_seconds"]
    elapsed_without_detection = (
        last_observation - source_available_at_seconds
    )
    if elapsed_without_detection >= bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            detection_latency_seconds=None,
            first_detection_at_seconds=None,
        )
    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        detection_latency_seconds=None,
        first_detection_at_seconds=None,
    )

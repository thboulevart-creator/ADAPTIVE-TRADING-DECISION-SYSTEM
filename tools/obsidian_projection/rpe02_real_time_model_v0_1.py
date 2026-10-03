"""RPE-02 V0.1: nanosecond-native real-time representation.

Pure timing qualification except capture_monotonic_clock_capability(), which records
host clock capability/evidence. No network, CLI, environment, filesystem config, or
P5-D4/Vault mutation authority exists in this module.
"""

from __future__ import annotations

import platform
import re
import sys
import time
from typing import Any, Mapping, Sequence


NANOSECONDS_PER_SECOND = 1_000_000_000
POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")


class RPE02TimingError(ValueError):
    """Invalid RPE-02 timing evidence or plan."""


def _strict_int(name: str, value: object) -> int:
    if type(value) is not int:
        raise RPE02TimingError(f"{name} must be an integer nanosecond value")
    return value


def _strict_sha40(name: str, value: object) -> str:
    if type(value) is not str or _SHA40_RE.fullmatch(value) is None:
        raise RPE02TimingError(f"{name} must be lowercase 40-hex")
    return value


def make_real_time_plan(*, schedule_origin_ns: int) -> dict[str, Any]:
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    return {
        "schema": "ATDS_RPE02_REAL_TIME_PLAN_V0_1",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "schedule_origin_ns": origin,
        "poll_interval_ns": POLL_INTERVAL_NS,
        "detection_latency_bound_ns": DETECTION_LATENCY_BOUND_NS,
        "synthetic_reference_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE",
    }


def first_fixed_rate_slot_at_or_after_ns(
    timestamp_ns: int,
    poll_interval_ns: int,
    schedule_origin_ns: int,
) -> int:
    timestamp = _strict_int("timestamp_ns", timestamp_ns)
    interval = _strict_int("poll_interval_ns", poll_interval_ns)
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    if interval <= 0:
        raise RPE02TimingError("poll_interval_ns must be positive")
    if timestamp <= origin:
        return origin + interval
    delta = timestamp - origin
    q, r = divmod(delta, interval)
    return origin + (q if r == 0 else q + 1) * interval


def _blocked(code: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": "BLOCKED_REQUIRES_ADJUDICATION",
        "failure_code": code,
        "detection_latency_ns": None,
    }
    out.update(extra)
    return out


def _validate_plan(plan: Mapping[str, Any]) -> tuple[int, int, int]:
    if not isinstance(plan, Mapping):
        raise RPE02TimingError("plan must be a mapping")
    if plan.get("normative_unit") != "INTEGER_MONOTONIC_NANOSECONDS":
        raise RPE02TimingError("plan normative unit mismatch")
    origin = _strict_int("plan.schedule_origin_ns", plan.get("schedule_origin_ns"))
    interval = _strict_int("plan.poll_interval_ns", plan.get("poll_interval_ns"))
    bound = _strict_int(
        "plan.detection_latency_bound_ns",
        plan.get("detection_latency_bound_ns"),
    )
    if interval != POLL_INTERVAL_NS:
        raise RPE02TimingError("poll interval is not the preregistered 30 seconds")
    if bound != DETECTION_LATENCY_BOUND_NS:
        raise RPE02TimingError("latency bound is not the preregistered 60 seconds")
    return origin, interval, bound


def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise RPE02TimingError(f"observations[{index}] must be a mapping")
    required = {
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
        "outcome",
        "observed_head",
    }
    if set(raw) != required:
        raise RPE02TimingError(
            f"observations[{index}] keys mismatch: "
            f"missing={sorted(required - set(raw))}, "
            f"unknown={sorted(set(raw) - required)}"
        )
    out = dict(raw)
    for key in (
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
    ):
        out[key] = _strict_int(f"observations[{index}].{key}", out[key])
    if type(out["outcome"]) is not str or not out["outcome"]:
        raise RPE02TimingError(f"observations[{index}].outcome must be non-empty string")
    if out["observed_head"] is not None:
        out["observed_head"] = _strict_sha40(
            f"observations[{index}].observed_head",
            out["observed_head"],
        )
    return out


def qualify_detection_ns(
    *,
    plan: Mapping[str, Any],
    controlled_source_release_started_at_ns: int,
    target_head: str,
    observations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    origin, interval, bound = _validate_plan(plan)
    release = _strict_int(
        "controlled_source_release_started_at_ns",
        controlled_source_release_started_at_ns,
    )
    target = _strict_sha40("target_head", target_head)
    if release <= origin:
        raise RPE02TimingError(
            "controlled_source_release_started_at_ns must be greater than schedule_origin_ns"
        )
    if not isinstance(observations, Sequence) or isinstance(
        observations, (str, bytes, bytearray)
    ):
        raise RPE02TimingError("observations must be a sequence")

    normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
    normalized.sort(key=lambda item: item["scheduled_at_ns"])

    previous_scheduled: int | None = None
    previous_completion: int | None = None
    seen_slots: set[int] = set()

    for item in normalized:
        scheduled = item["scheduled_at_ns"]
        started = item["attempt_started_at_ns"]
        remote_done = item["remote_observation_completed_at_ns"]
        attempt_done = item["attempt_completed_at_ns"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if scheduled in seen_slots:
            return _blocked("DUPLICATE_FIXED_RATE_SLOT")
        seen_slots.add(scheduled)

        if previous_scheduled is not None and scheduled != previous_scheduled + interval:
            return _blocked("CADENCE_GAP")
        if started < scheduled:
            return _blocked("ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
        if started >= scheduled + interval:
            return _blocked("ACTUAL_START_MISSED_FIXED_RATE_SLOT")
        if remote_done < started:
            return _blocked("REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
        if remote_done > scheduled + interval:
            return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
        if attempt_done < remote_done:
            return _blocked("ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
        if previous_completion is not None and previous_completion > started:
            return _blocked("ATTEMPT_OVERLAP")

        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
            and started < release
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT",
                first_detection_scheduled_at_ns=scheduled,
                first_detection_attempt_started_at_ns=started,
                first_detection_remote_observation_completed_at_ns=remote_done,
                first_detection_attempt_completed_at_ns=attempt_done,
            )

        previous_scheduled = scheduled
        previous_completion = attempt_done

    first_required = first_fixed_rate_slot_at_or_after_ns(release, interval, origin)
    if normalized:
        slots_at_or_after_release = [
            item["scheduled_at_ns"]
            for item in normalized
            if item["scheduled_at_ns"] >= first_required
        ]
        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:
            return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    for item in normalized:
        if item["attempt_started_at_ns"] < release:
            continue
        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
        ):
            latency = item["remote_observation_completed_at_ns"] - release
            status = (
                "PASS_DETECTED_WITHIN_BOUND"
                if latency <= bound
                else "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            )
            return {
                "status": status,
                "failure_code": None,
                "detection_latency_ns": latency,
                "first_detection_scheduled_at_ns": item["scheduled_at_ns"],
                "first_detection_attempt_started_at_ns": item["attempt_started_at_ns"],
                "first_detection_remote_observation_completed_at_ns": item[
                    "remote_observation_completed_at_ns"
                ],
                "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
            }

    window_end = max(
        (item["remote_observation_completed_at_ns"] for item in normalized),
        default=origin,
    )
    if window_end >= release + bound:
        return {
            "status": "FAIL_NO_DETECTION_BY_BOUND",
            "failure_code": None,
            "detection_latency_ns": None,
        }
    return {
        "status": "INCOMPLETE_REAL_TIME_WINDOW",
        "failure_code": None,
        "detection_latency_ns": None,
    }


def capture_monotonic_clock_capability() -> dict[str, Any]:
    info = time.get_clock_info("monotonic")
    sample_1 = time.monotonic_ns()
    sample_2 = time.monotonic_ns()
    if not info.monotonic:
        raise RPE02TimingError("host monotonic clock does not report monotonic capability")
    return {
        "schema": "ATDS_RPE02_MONOTONIC_CLOCK_CAPABILITY_V0_1",
        "api": "time.monotonic_ns",
        "metadata_api": "time.get_clock_info('monotonic')",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "monotonic": bool(info.monotonic),
        "adjustable": bool(info.adjustable),
        "resolution_seconds": info.resolution,
        "implementation": info.implementation,
        "sample_1_ns": sample_1,
        "sample_2_ns": sample_2,
        "same_process_host_domain": True,
        "python_version": sys.version.replace("\n", " "),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }

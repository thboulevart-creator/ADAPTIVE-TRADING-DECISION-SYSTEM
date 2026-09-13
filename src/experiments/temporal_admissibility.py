"""Executable point-in-time admissibility checks for experiment inputs.

This module implements only the already-frozen temporal predicates: valid_at,
known_at, usable_at and pipeline_safe_at. It does not infer missing temporal
metadata and never repairs or shifts timestamps.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


TemporalVerdict = Literal["PASS", "FAIL", "BLOCKED"]


@dataclass(frozen=True)
class TemporalContext:
    """Temporal facts declared for one experiment input."""

    valid_from: datetime | None
    valid_to: datetime | None
    known_from: datetime | None
    known_to: datetime | None
    usable_from: datetime | None
    usable_to: datetime | None
    pipeline_safe_from: datetime | None
    pipeline_safe_to: datetime | None


@dataclass(frozen=True)
class TemporalAdmissibilityReport:
    """Result of explicit point-in-time checks."""

    decision_at: datetime
    valid_at: TemporalVerdict
    known_at: TemporalVerdict
    usable_at: TemporalVerdict
    pipeline_safe_at: TemporalVerdict
    verdict: TemporalVerdict
    reason: str


def _contains(start: datetime | None, end: datetime | None, at: datetime) -> TemporalVerdict:
    if start is None:
        return "BLOCKED"
    if end is not None and end < start:
        return "FAIL"
    return "PASS" if start <= at and (end is None or at <= end) else "FAIL"


def assess(context: TemporalContext, *, decision_at: datetime) -> TemporalAdmissibilityReport:
    """Evaluate all four frozen temporal predicates at one decision time."""

    checks = {
        "valid_at": _contains(context.valid_from, context.valid_to, decision_at),
        "known_at": _contains(context.known_from, context.known_to, decision_at),
        "usable_at": _contains(context.usable_from, context.usable_to, decision_at),
        "pipeline_safe_at": _contains(context.pipeline_safe_from, context.pipeline_safe_to, decision_at),
    }
    statuses = set(checks.values())
    if "FAIL" in statuses:
        verdict: TemporalVerdict = "FAIL"
        reason = "one or more temporal predicates fail at decision_at"
    elif "BLOCKED" in statuses:
        verdict = "BLOCKED"
        reason = "one or more required temporal bounds are not declared"
    else:
        verdict = "PASS"
        reason = "all temporal predicates pass at decision_at"

    return TemporalAdmissibilityReport(
        decision_at=decision_at,
        valid_at=checks["valid_at"],
        known_at=checks["known_at"],
        usable_at=checks["usable_at"],
        pipeline_safe_at=checks["pipeline_safe_at"],
        verdict=verdict,
        reason=reason,
    )

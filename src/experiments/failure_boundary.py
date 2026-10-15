"""Explicit failure/abort boundary for experiment execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


FailureStatus = Literal["OPEN", "RESOLVED", "REJECTED", "BLOCKED"]
ContainmentStatus = Literal["NONE", "SAFE_HOLD", "ISOLATED"]
ResolutionAction = Literal["NONE", "REPAIR", "ESCALATE"]
DiagnosisStatus = Literal["UNKNOWN", "IDENTIFIED", "INCONCLUSIVE"]


@dataclass(frozen=True)
class FailureRecord:
    failure_id: str
    detected_at: datetime
    detected_by: str
    subject_id: str
    component: str
    failure_class: str
    severity: str
    observed_condition: str
    expected_condition: str
    evidence_refs: tuple[str, ...]
    diagnosis_status: DiagnosisStatus
    diagnosis_explanation: str
    containment_status: ContainmentStatus
    containment_reason: str
    resolution_action: ResolutionAction
    resolution_actor: str
    revalidation_required: bool
    revalidation_report_id: str | None
    closure_status: FailureStatus

    def __post_init__(self) -> None:
        required = {
            "failure_id": self.failure_id,
            "detected_by": self.detected_by,
            "subject_id": self.subject_id,
            "component": self.component,
            "failure_class": self.failure_class,
            "severity": self.severity,
            "observed_condition": self.observed_condition,
            "expected_condition": self.expected_condition,
            "diagnosis_explanation": self.diagnosis_explanation,
            "containment_reason": self.containment_reason,
            "resolution_actor": self.resolution_actor,
        }
        for name, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.diagnosis_status not in {"UNKNOWN", "IDENTIFIED", "INCONCLUSIVE"}:
            raise ValueError("invalid diagnosis status")
        if self.containment_status not in {"NONE", "SAFE_HOLD", "ISOLATED"}:
            raise ValueError("invalid containment status")
        if self.resolution_action not in {"NONE", "REPAIR", "ESCALATE"}:
            raise ValueError("invalid resolution action")
        if self.closure_status not in {"OPEN", "RESOLVED", "REJECTED", "BLOCKED"}:
            raise ValueError("invalid closure status")
        if not self.revalidation_required and self.revalidation_report_id is not None:
            raise ValueError("revalidation report requires revalidation_required=True")

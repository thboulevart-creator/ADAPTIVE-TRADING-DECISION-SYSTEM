"""Minimal executable ValidationReport contract.

Validation is descriptive only: it records checks and evidence and does not
make trading or governance decisions beyond the declared verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


ValidationStatus = Literal["PASS", "FAIL", "PARTIAL", "BLOCKED", "UNVERIFIED"]


@dataclass(frozen=True)
class ValidationCheck:
    check_id: str
    status: ValidationStatus
    reason: str


@dataclass(frozen=True)
class ValidationReport:
    report_id: str
    subject_id: str
    subject_type: str
    validator_id: str
    validator_version: str
    context_id: str
    contract_reference: str
    contract_version: str
    checks: tuple[ValidationCheck, ...]
    evidence_refs: tuple[str, ...]
    failure_refs: tuple[str, ...]
    limitations: tuple[str, ...]
    verdict_status: ValidationStatus
    verdict_reason: str
    input_identity: str
    code_version: str
    configuration_version: str
    created_at: datetime

    def __post_init__(self) -> None:
        required = {
            "report_id": self.report_id,
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "validator_id": self.validator_id,
            "validator_version": self.validator_version,
            "context_id": self.context_id,
            "contract_reference": self.contract_reference,
            "contract_version": self.contract_version,
            "verdict_reason": self.verdict_reason,
            "input_identity": self.input_identity,
            "code_version": self.code_version,
            "configuration_version": self.configuration_version,
        }
        for name, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.verdict_status not in {"PASS", "FAIL", "PARTIAL", "BLOCKED", "UNVERIFIED"}:
            raise ValueError(f"invalid validation verdict: {self.verdict_status!r}")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

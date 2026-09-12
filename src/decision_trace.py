"""Minimal, evidence-oriented reconstruction of a completed decision.

This module does not create a decision engine or a provenance registry. It only
makes the minimum reconstruction chain explicit and executable:

provenance -> research run -> code -> configuration -> dataset -> context
-> decision -> action -> result

A missing link is a FAIL, never an implicit PASS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Status = Literal["PASS", "FAIL", "BLOCKED"]


@dataclass(frozen=True)
class DecisionTrace:
    decision_id: str
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    context_id: str
    decision: str
    action_id: str
    result_id: str

    def missing_links(self) -> tuple[str, ...]:
        """Return required reconstruction links that are absent."""
        fields = (
            "provenance_id",
            "research_run_id",
            "code_version",
            "configuration_version",
            "dataset_id",
            "dataset_version",
            "context_id",
            "decision",
            "action_id",
            "result_id",
        )
        return tuple(field for field in fields if not getattr(self, field).strip())

    def validate(self) -> tuple[Status, tuple[str, ...]]:
        """Validate only structural completeness of the reconstruction chain."""
        missing = self.missing_links()
        if missing:
            return "FAIL", missing
        return "PASS", ()

    def reconstruction_chain(self) -> tuple[str, ...]:
        """Return the ordered identifiers needed to reconstruct the decision."""
        status, missing = self.validate()
        if status != "PASS":
            raise ValueError(f"decision trace is incomplete: {', '.join(missing)}")
        return (
            self.provenance_id,
            self.research_run_id,
            self.code_version,
            self.configuration_version,
            self.dataset_id,
            self.dataset_version,
            self.context_id,
            self.decision_id,
            self.action_id,
            self.result_id,
        )

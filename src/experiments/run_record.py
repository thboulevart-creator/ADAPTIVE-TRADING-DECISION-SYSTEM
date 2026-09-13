"""Immutable experiment run identity and terminal lifecycle record."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


RunStatus = Literal[
    "COMPLETED",
    "FAILED",
    "BLOCKED",
    "ABORTED",
    "INVALIDATED",
]

_ALLOWED_STATUSES = frozenset(
    {"COMPLETED", "FAILED", "BLOCKED", "ABORTED", "INVALIDATED"}
)


@dataclass(frozen=True)
class ExperimentRunRecord:
    """Immutable, terminal record identifying one experiment execution.

    The record is intentionally terminal-only: the frozen contract defines no
    RUNNING status. Execution orchestration may create the record at closure,
    preserving the complete identity and lifecycle outcome without permitting
    silent mutation afterwards.
    """

    run_id: str
    experiment_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    dataset_hash: str
    environment_version: str
    started_at: datetime
    ended_at: datetime
    status: RunStatus

    def __post_init__(self) -> None:
        identifiers = {
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "code_version": self.code_version,
            "configuration_version": self.configuration_version,
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "environment_version": self.environment_version,
        }
        for name, value in identifiers.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.dataset_hash, str) or not self.dataset_hash.strip():
            raise ValueError("dataset_hash must be a non-empty string")
        if len(self.dataset_hash) != 64:
            raise ValueError("dataset_hash must be a 64-character SHA-256 hex digest")
        try:
            int(self.dataset_hash, 16)
        except ValueError as exc:
            raise ValueError("dataset_hash must be hexadecimal") from exc

        if not isinstance(self.started_at, datetime):
            raise TypeError("started_at must be a datetime")
        if not isinstance(self.ended_at, datetime):
            raise TypeError("ended_at must be a datetime")
        if self.ended_at < self.started_at:
            raise ValueError("ended_at must be greater than or equal to started_at")

        if self.status not in _ALLOWED_STATUSES:
            raise ValueError(f"invalid terminal run status: {self.status!r}")

    def to_dict(self) -> dict[str, object]:
        """Return a serialization-ready representation without mutating state."""
        return {
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "code_version": self.code_version,
            "configuration_version": self.configuration_version,
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "dataset_hash": self.dataset_hash,
            "environment_version": self.environment_version,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "status": self.status,
        }

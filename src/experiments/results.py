"""Immutable result contract for the minimum executable experiment."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExperimentResult:
    """Result values derived from one deterministic execution trace."""

    run_id: str
    tick_count: int
    first_timestamp: str | None
    last_timestamp: str | None
    bid_sum: Decimal
    ask_sum: Decimal

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id must be a non-empty string")
        if self.tick_count < 0:
            raise ValueError("tick_count must be non-negative")
        if self.tick_count == 0 and (self.first_timestamp is not None or self.last_timestamp is not None):
            raise ValueError("empty result cannot contain timestamps")
        if self.tick_count > 0 and (self.first_timestamp is None or self.last_timestamp is None):
            raise ValueError("non-empty result requires first and last timestamps")

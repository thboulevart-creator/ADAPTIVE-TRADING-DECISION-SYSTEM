"""Deterministic execution boundary for the minimum trading experiment."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from src.data.tick_reader import Tick


@dataclass(frozen=True)
class ExecutionTrace:
    """Deterministic observation trace produced from source ticks."""

    tick_count: int
    first_read_index: int | None
    last_read_index: int | None
    first_timestamp: str | None
    last_timestamp: str | None
    bid_sum: Decimal
    ask_sum: Decimal


class DeterministicExecutor:
    """Consume ticks exactly in supplied order, without mutation or repair."""

    def run(self, ticks: Iterable[Tick]) -> ExecutionTrace:
        count = 0
        first_index: int | None = None
        last_index: int | None = None
        first_timestamp: str | None = None
        last_timestamp: str | None = None
        bid_sum = Decimal("0")
        ask_sum = Decimal("0")

        for tick in ticks:
            if first_index is None:
                first_index = tick.read_index
                first_timestamp = tick.timestamp
            last_index = tick.read_index
            last_timestamp = tick.timestamp
            bid_sum += tick.bid_price
            ask_sum += tick.ask_price
            count += 1

        return ExecutionTrace(
            tick_count=count,
            first_read_index=first_index,
            last_read_index=last_index,
            first_timestamp=first_timestamp,
            last_timestamp=last_timestamp,
            bid_sum=bid_sum,
            ask_sum=ask_sum,
        )

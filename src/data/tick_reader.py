"""Minimal experimental reader for real-market tick CSV files.

This module intentionally performs no sorting, deduplication, repair, or
market-semantic normalization. It reads the five source fields as provided.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterator


EXPECTED_COLUMNS = ("timestamp", "askPrice", "bidPrice", "askVolume", "bidVolume")


@dataclass(frozen=True)
class Tick:
    """One source tick, preserving source ordering through read_index."""

    timestamp: str
    ask_price: Decimal
    bid_price: Decimal
    ask_volume: Decimal
    bid_volume: Decimal
    read_index: int


def load(path: str | Path) -> Iterator[Tick]:
    """Read ticks from a CSV without sorting, deduplication, or repair."""

    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV header is missing")
        if tuple(reader.fieldnames) != EXPECTED_COLUMNS:
            raise ValueError(
                f"Unexpected columns: {tuple(reader.fieldnames)!r}; "
                f"expected {EXPECTED_COLUMNS!r}"
            )

        for read_index, row in enumerate(reader):
            if any(row[column] is None for column in EXPECTED_COLUMNS):
                raise ValueError(f"Malformed row at read_index={read_index}")

            yield Tick(
                timestamp=row["timestamp"],
                ask_price=Decimal(row["askPrice"]),
                bid_price=Decimal(row["bidPrice"]),
                ask_volume=Decimal(row["askVolume"]),
                bid_volume=Decimal(row["bidVolume"]),
                read_index=read_index,
            )

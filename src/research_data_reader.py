"""Minimal research-data reader extracted from the V4.3 qualification path.

This module deliberately owns only data loading. Qualification, compatibility,
and admissibility decisions remain in the V4.3 probe.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ResearchBar:
    timestamp: pd.Timestamp
    open: float
    high: float
    low: float
    close: float
    volume: float


def read_research_bars(path: str | Path) -> tuple[ResearchBar, ...]:
    """Read an existing CSV OHLCV research fixture without qualification logic."""
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"missing research columns: {sorted(missing)}")
    bars: list[ResearchBar] = []
    for row in frame.itertuples(index=False):
        bars.append(
            ResearchBar(
                timestamp=pd.Timestamp(row.timestamp),
                open=float(row.open),
                high=float(row.high),
                low=float(row.low),
                close=float(row.close),
                volume=float(row.volume),
            )
        )
    if not bars:
        raise ValueError("research dataset is empty")
    return tuple(bars)

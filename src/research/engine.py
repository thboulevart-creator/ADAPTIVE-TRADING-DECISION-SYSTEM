"""Controlled reconstruction of the deterministic BI5 research engine."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

from .bi5_reader import iter_ticks, parse_hour
from .input_binding import BoundResearchInput


class BI5ResearchEngine:
    """Engine admissible only behind the bound-input capability."""

    def __init__(self, bound_input: BoundResearchInput):
        if not isinstance(bound_input, BoundResearchInput):
            raise TypeError("BI5ResearchEngine requires BoundResearchInput")
        self._bound_input = bound_input

    def _files(self) -> list[Path]:
        files = sorted(
            (p for p in self._bound_input.corpus_root.rglob("*.bi5") if p.is_file()),
            key=parse_hour,
        )
        hours = [parse_hour(p) for p in files]
        if len(hours) != len(set(hours)):
            raise ValueError("Duplicate BI5 hour detected")
        return files

    def iter_ticks(self) -> Iterator[object]:
        previous = None
        for path in self._files():
            for tick in iter_ticks(path, self._bound_input.contract):
                if previous is not None and tick.timestamp < previous:
                    raise ValueError("Global BI5 tick stream is not monotonic")
                previous = tick.timestamp
                yield tick

    def run(self):
        """Legacy generic helper retained for compatibility, not qualification."""
        return list(self.iter_ticks())

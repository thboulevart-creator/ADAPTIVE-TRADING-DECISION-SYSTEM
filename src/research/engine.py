"""Deterministic BI5 research engine behind an identity-bound input gate."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

from .bi5_reader import iter_ticks, parse_hour
from .input_binding import BoundResearchInput, is_bound_research_input


class BI5ResearchEngine:
    """Engine admissible only behind a currently valid bound-input capability."""

    def __init__(self, bound_input: BoundResearchInput):
        if not is_bound_research_input(bound_input, revalidate_sources=True):
            raise ValueError("BI5ResearchEngine requires factory-bound, identity-valid research input")
        self._bound_input = bound_input

    def _require_current_binding(self) -> None:
        if not is_bound_research_input(self._bound_input, revalidate_sources=True):
            raise ValueError("Research input identity changed after binding")

    def _files(self) -> list[Path]:
        self._require_current_binding()
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
            self._require_current_binding()
            for tick in iter_ticks(path, self._bound_input.contract):
                if previous is not None and tick.timestamp < previous:
                    raise ValueError("Global BI5 tick stream is not monotonic")
                previous = tick.timestamp
                yield tick

    def run(self):
        """Legacy generic helper retained for compatibility, not qualification."""
        return list(self.iter_ticks())

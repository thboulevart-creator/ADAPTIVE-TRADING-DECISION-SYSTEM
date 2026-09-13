"""Controlled reconstruction of the official qualified execution boundary.

RECONSTRUCTION != RECOVERY.
"""
from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .engine import BI5ResearchEngine
from .input_binding import bind_execution_input


@dataclass(frozen=True)
class QualifiedResearchInput:
    corpus_root: Path
    contract_path: Path
    expected_corpus_hash: str
    expected_contract_hash: str


@dataclass(frozen=True)
class ResearchExecutionResult:
    files_consumed: int
    ticks_consumed: int
    first_timestamp: datetime | None
    last_timestamp: datetime | None
    stream_sha256: str


def _execute_bound_stream(bound_input):
    engine = BI5ResearchEngine(bound_input)
    digest = hashlib.sha256()
    files = engine._files()
    tick_count = 0
    first_timestamp = None
    last_timestamp = None
    for tick in engine.iter_ticks():
        if first_timestamp is None:
            first_timestamp = tick.timestamp
        last_timestamp = tick.timestamp
        digest.update(
            tick.timestamp.isoformat().encode("utf-8")
            + b"\x00"
            + struct.pack(">d", tick.ask)
            + struct.pack(">d", tick.bid)
            + struct.pack(">d", tick.ask_volume)
            + struct.pack(">d", tick.bid_volume)
            + b"\n"
        )
        tick_count += 1
    return ResearchExecutionResult(
        files_consumed=len(files),
        ticks_consumed=tick_count,
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        stream_sha256=digest.hexdigest(),
    )


def run_qualified_research(execution_input: QualifiedResearchInput):
    bound_input = bind_execution_input(
        execution_input.corpus_root,
        execution_input.contract_path,
        execution_input.expected_corpus_hash,
        execution_input.expected_contract_hash,
    )
    return _execute_bound_stream(bound_input)

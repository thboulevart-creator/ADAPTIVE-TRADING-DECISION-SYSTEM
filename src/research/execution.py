"""Qualified research execution boundary for the P0.4 producer junction.

RECONSTRUCTION != RECOVERY. P0.4 binds the deterministic runtime result to the
exact qualified input identities and rejects zero-evidence executions.
"""
from __future__ import annotations

import hashlib
import json
import struct
import weakref
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

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


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _input_fingerprint(execution_input: QualifiedResearchInput) -> str:
    return _stable_hash(
        {
            "corpus_root": str(Path(execution_input.corpus_root).resolve()),
            "contract_path": str(Path(execution_input.contract_path).resolve()),
            "expected_corpus_hash": execution_input.expected_corpus_hash,
            "expected_contract_hash": execution_input.expected_contract_hash,
        }
    )


def _result_fingerprint(result: ResearchExecutionResult) -> str:
    return _stable_hash(
        {
            "files_consumed": result.files_consumed,
            "ticks_consumed": result.ticks_consumed,
            "first_timestamp": result.first_timestamp.isoformat() if result.first_timestamp else None,
            "last_timestamp": result.last_timestamp.isoformat() if result.last_timestamp else None,
            "stream_sha256": result.stream_sha256,
        }
    )


def _execute_bound_stream(bound_input) -> ResearchExecutionResult:
    engine = BI5ResearchEngine(bound_input)
    files = engine._files()
    if not files:
        raise ValueError("Qualified research execution requires at least one BI5 file")

    digest = hashlib.sha256()
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

    if tick_count <= 0 or first_timestamp is None or last_timestamp is None:
        raise ValueError("Qualified research execution requires at least one decoded tick")

    return ResearchExecutionResult(
        files_consumed=len(files),
        ticks_consumed=tick_count,
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        stream_sha256=digest.hexdigest(),
    )


def _build_execution_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[ResearchExecutionResult], str, str],
    ] = {}

    def register(
        result: ResearchExecutionResult,
        execution_input: QualifiedResearchInput,
    ) -> ResearchExecutionResult:
        object_id = id(result)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(result, cleanup)
        registry[object_id] = (
            reference,
            _result_fingerprint(result),
            _input_fingerprint(execution_input),
        )
        return result

    def run(execution_input: QualifiedResearchInput) -> ResearchExecutionResult:
        if not isinstance(execution_input, QualifiedResearchInput):
            raise TypeError("run_qualified_research requires QualifiedResearchInput")
        bound_input = bind_execution_input(
            execution_input.corpus_root,
            execution_input.contract_path,
            execution_input.expected_corpus_hash,
            execution_input.expected_contract_hash,
        )
        result = _execute_bound_stream(bound_input)
        return register(result, execution_input)

    def verify(result: object, execution_input: object) -> bool:
        if not isinstance(result, ResearchExecutionResult):
            return False
        if not isinstance(execution_input, QualifiedResearchInput):
            return False
        entry = registry.get(id(result))
        if entry is None:
            return False
        reference, expected_result_fingerprint, expected_input_fingerprint = entry
        if reference() is not result:
            return False
        if _result_fingerprint(result) != expected_result_fingerprint:
            return False
        if _input_fingerprint(execution_input) != expected_input_fingerprint:
            return False
        try:
            bind_execution_input(
                execution_input.corpus_root,
                execution_input.contract_path,
                execution_input.expected_corpus_hash,
                execution_input.expected_contract_hash,
            )
        except (OSError, TypeError, ValueError):
            return False
        return True

    return run, verify


run_qualified_research, is_qualified_execution_result = _build_execution_api()
del _build_execution_api

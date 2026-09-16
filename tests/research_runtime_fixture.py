from __future__ import annotations

import json
import lzma
import struct
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from src.context import Context, build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.research.execution import (
    QualifiedResearchInput,
    ResearchExecutionResult,
    run_qualified_research,
)
from src.research.input_binding import corpus_inventory_hash, sha256_file
from src.research_run_evidence import (
    ResearchRunEvidence,
    derive_runtime_research_identity,
    from_research_execution,
)


CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"
FIRST_TS = "2026-01-02T00:00:00.001000+00:00"
LAST_TS = "2026-01-02T00:00:00.002000+00:00"


@dataclass(frozen=True)
class RuntimeFixture:
    root: Path
    corpus_root: Path
    contract_path: Path
    execution_input: QualifiedResearchInput
    dataset: DatasetIdentity
    context: Context
    result: ResearchExecutionResult
    evidence: ResearchRunEvidence


def _write_synthetic_bi5(path: Path) -> None:
    records = b"".join(
        (
            struct.pack(">IIIff", 1, 100_200, 100_000, 1.5, 2.0),
            struct.pack(">IIIff", 2, 100_300, 100_100, 1.0, 1.25),
        )
    )
    path.write_bytes(lzma.compress(records, format=lzma.FORMAT_ALONE))


def _build_execution_input(root: Path) -> QualifiedResearchInput:
    corpus_root = root / "corpus"
    corpus_root.mkdir(parents=True)
    _write_synthetic_bi5(corpus_root / "2026010200.bi5")

    contract_path = root / "USATECHIDXUSD-Dukascopy-BI5.json"
    contract = {
        "asset_id": "USATECHIDXUSD",
        "source": "Dukascopy",
        "format": "BI5",
        "record_size": 20,
        "record_struct": ">IIIff",
        "timestamp_unit": "milliseconds",
        "price_scale": 1000,
    }
    contract_path.write_text(
        json.dumps(contract, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    return QualifiedResearchInput(
        corpus_root=corpus_root,
        contract_path=contract_path,
        expected_corpus_hash=corpus_inventory_hash(corpus_root),
        expected_contract_hash=sha256_file(contract_path),
    )


@contextmanager
def synthetic_runtime_case(*, code_version: str = CODE_VERSION) -> Iterator[RuntimeFixture]:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        execution_input = _build_execution_input(root)
        identity = derive_runtime_research_identity(execution_input)
        dataset = DatasetIdentity(
            dataset_id=identity.dataset_id,
            dataset_version=identity.dataset_version,
            content_hash=identity.corpus_sha256,
            format=identity.format,
            schema_version="dukascopy-bi5-v1",
            instrument=identity.instrument,
            granularity="tick",
            timezone_storage="UTC",
        )
        context = build_context(
            dataset,
            configuration_version=identity.configuration_version,
            observation_start=FIRST_TS,
            observation_end=LAST_TS,
        )
        result = run_qualified_research(execution_input)
        evidence = from_research_execution(
            execution_input,
            result,
            code_version=code_version,
            context=context,
            dataset=dataset,
        )
        yield RuntimeFixture(
            root=root,
            corpus_root=execution_input.corpus_root,
            contract_path=execution_input.contract_path,
            execution_input=execution_input,
            dataset=dataset,
            context=context,
            result=result,
            evidence=evidence,
        )


def coherent_runtime_inputs() -> tuple[ResearchRunEvidence, Context]:
    with synthetic_runtime_case() as case:
        return case.evidence, case.context

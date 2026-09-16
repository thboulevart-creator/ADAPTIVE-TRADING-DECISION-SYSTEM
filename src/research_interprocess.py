"""Durable RESEARCH -> DECISION bridge by deterministic replay re-attestation.

A persisted proof is never authority by itself.  A fresh process must validate
its canonical content identity, independently supplied QualifiedResearchInput
and expected code version, replay the deterministic research execution, compare
all claims, then mint a new process-local ResearchRunEvidence through the
already-qualified P0.4 factory.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, fields
from datetime import datetime
from pathlib import Path
from typing import Any

from src.context import Context, build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.research.execution import (
    QualifiedResearchInput,
    ResearchExecutionResult,
    is_qualified_execution_result,
    run_qualified_research,
)
from src.research_run_evidence import (
    ResearchRunEvidence,
    derive_runtime_research_identity,
    from_research_execution,
    is_factory_attested,
)


_SCHEMA = "RESEARCH_INTERPROCESS_PROOF_V1"
_PRODUCER_CONTRACT = "RESEARCH_PRODUCER_JUNCTION_V1"
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_CODE_VERSION_RE = re.compile(r"[0-9a-f]{40}\Z")
_FILENAME_RE = re.compile(r"research-proof-([0-9a-f]{64})\.json\Z")


@dataclass(frozen=True)
class ReattestedResearchBundle:
    proof_sha256: str
    evidence: ResearchRunEvidence
    dataset: DatasetIdentity
    context: Context


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        + b"\n"
    )


def _proof_payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()


def _execution_payload(result: ResearchExecutionResult) -> dict[str, Any]:
    return {
        "files_consumed": result.files_consumed,
        "ticks_consumed": result.ticks_consumed,
        "first_timestamp": result.first_timestamp.isoformat() if result.first_timestamp else None,
        "last_timestamp": result.last_timestamp.isoformat() if result.last_timestamp else None,
        "stream_sha256": result.stream_sha256,
    }


def _derived_dataset_and_context(
    execution_input: QualifiedResearchInput,
    result: ResearchExecutionResult,
) -> tuple[DatasetIdentity, Context]:
    identity = derive_runtime_research_identity(execution_input)
    if result.first_timestamp is None or result.last_timestamp is None:
        raise ValueError("inter-process proof requires execution timestamps")
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
        observation_start=result.first_timestamp.isoformat(),
        observation_end=result.last_timestamp.isoformat(),
    )
    return dataset, context


def _build_payload(
    execution_input: QualifiedResearchInput,
    result: ResearchExecutionResult,
    evidence: ResearchRunEvidence,
    dataset: DatasetIdentity,
    context: Context,
) -> dict[str, Any]:
    return {
        "schema": _SCHEMA,
        "producer_contract": _PRODUCER_CONTRACT,
        "code_version": evidence.code_version,
        "source": {
            "corpus_sha256": execution_input.expected_corpus_hash,
            "contract_sha256": execution_input.expected_contract_hash,
        },
        "execution": _execution_payload(result),
        "dataset": asdict(dataset),
        "context": asdict(context),
        "evidence": asdict(evidence),
    }


def _require_exact_keys(label: str, value: object, expected: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} schema mismatch: missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
        )
    return value


def _require_nonempty_strings(label: str, value: dict[str, Any], names: set[str]) -> None:
    for name in names:
        item = value.get(name)
        if not isinstance(item, str) or not item:
            raise ValueError(f"{label}.{name} must be a non-empty string")


def _validate_timestamp(label: str, value: object) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} is not valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_document_shape(document: dict[str, Any]) -> None:
    top = _require_exact_keys(
        "proof",
        document,
        {
            "schema",
            "producer_contract",
            "code_version",
            "source",
            "execution",
            "dataset",
            "context",
            "evidence",
            "proof_sha256",
        },
    )
    if top["schema"] != _SCHEMA:
        raise ValueError("unsupported inter-process proof schema")
    if top["producer_contract"] != _PRODUCER_CONTRACT:
        raise ValueError("inter-process proof producer contract mismatch")
    if not isinstance(top["code_version"], str) or _CODE_VERSION_RE.fullmatch(top["code_version"]) is None:
        raise ValueError("inter-process proof code_version must be lowercase 40-hex")
    if not isinstance(top["proof_sha256"], str) or _SHA256_RE.fullmatch(top["proof_sha256"]) is None:
        raise ValueError("inter-process proof identity must be SHA-256")

    source = _require_exact_keys("source", top["source"], {"corpus_sha256", "contract_sha256"})
    for name in ("corpus_sha256", "contract_sha256"):
        if not isinstance(source[name], str) or _SHA256_RE.fullmatch(source[name]) is None:
            raise ValueError(f"source.{name} must be SHA-256")

    execution = _require_exact_keys(
        "execution",
        top["execution"],
        {"files_consumed", "ticks_consumed", "first_timestamp", "last_timestamp", "stream_sha256"},
    )
    if type(execution["files_consumed"]) is not int or execution["files_consumed"] <= 0:
        raise ValueError("execution.files_consumed must be a positive integer")
    if type(execution["ticks_consumed"]) is not int or execution["ticks_consumed"] <= 0:
        raise ValueError("execution.ticks_consumed must be a positive integer")
    _validate_timestamp("execution.first_timestamp", execution["first_timestamp"])
    _validate_timestamp("execution.last_timestamp", execution["last_timestamp"])
    if not isinstance(execution["stream_sha256"], str) or _SHA256_RE.fullmatch(execution["stream_sha256"]) is None:
        raise ValueError("execution.stream_sha256 must be SHA-256")

    dataset_fields = {field.name for field in fields(DatasetIdentity)}
    dataset = _require_exact_keys("dataset", top["dataset"], dataset_fields)
    _require_nonempty_strings("dataset", dataset, dataset_fields)

    context_fields = {field.name for field in fields(Context)}
    context = _require_exact_keys("context", top["context"], context_fields)
    _require_nonempty_strings("context", context, context_fields)

    evidence_fields = {field.name for field in fields(ResearchRunEvidence)}
    evidence = _require_exact_keys("evidence", top["evidence"], evidence_fields)
    _require_nonempty_strings("evidence", evidence, evidence_fields)
    if evidence["code_version"] != top["code_version"]:
        raise ValueError("proof code_version and evidence code_version differ")


def _load_canonical_proof(path: str | Path) -> dict[str, Any]:
    proof_path = Path(path)
    raw = proof_path.read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("inter-process proof is not valid UTF-8 canonical JSON") from exc
    if not isinstance(document, dict):
        raise ValueError("inter-process proof root must be a JSON object")
    _validate_document_shape(document)
    if raw != _canonical_json_bytes(document):
        raise ValueError("inter-process proof must use canonical JSON encoding")

    payload = dict(document)
    claimed_hash = payload.pop("proof_sha256")
    actual_hash = _proof_payload_hash(payload)
    if claimed_hash != actual_hash:
        raise ValueError("inter-process proof canonical hash mismatch")
    expected_name = f"research-proof-{actual_hash}.json"
    if proof_path.name != expected_name:
        raise ValueError("inter-process proof filename/content identity mismatch")
    return document


def persist_research_execution_proof(
    output_directory: str | Path,
    execution_input: QualifiedResearchInput,
    result: ResearchExecutionResult,
    evidence: ResearchRunEvidence,
    *,
    dataset: DatasetIdentity,
    context: Context,
) -> Path:
    """Persist a canonical, content-addressed non-authorizing execution proof."""
    if not isinstance(execution_input, QualifiedResearchInput):
        raise ValueError("proof persistence requires QualifiedResearchInput")
    if not isinstance(result, ResearchExecutionResult):
        raise ValueError("proof persistence requires ResearchExecutionResult")
    if not is_qualified_execution_result(result, execution_input):
        raise ValueError("proof persistence requires qualified execution result")
    if not isinstance(evidence, ResearchRunEvidence) or not is_factory_attested(evidence):
        raise ValueError("proof persistence requires factory-attested ResearchRunEvidence")
    if not isinstance(dataset, DatasetIdentity) or not isinstance(context, Context):
        raise ValueError("proof persistence requires DatasetIdentity and Context")

    derived_dataset, derived_context = _derived_dataset_and_context(execution_input, result)
    if dataset != derived_dataset:
        raise ValueError("proof persistence dataset is not derived from execution input")
    if context != derived_context:
        raise ValueError("proof persistence context is not derived from execution result")

    expected_evidence = from_research_execution(
        execution_input,
        result,
        code_version=evidence.code_version,
        context=context,
        dataset=dataset,
    )
    if evidence != expected_evidence:
        raise ValueError("proof persistence evidence does not match qualified execution")

    payload = _build_payload(execution_input, result, evidence, dataset, context)
    proof_sha256 = _proof_payload_hash(payload)
    document = dict(payload)
    document["proof_sha256"] = proof_sha256
    raw = _canonical_json_bytes(document)

    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    if not directory.is_dir():
        raise ValueError("proof output_directory is not a directory")
    path = directory / f"research-proof-{proof_sha256}.json"
    try:
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        if path.read_bytes() != raw:
            raise ValueError("existing content-addressed proof bytes differ")
    return path


def reattest_persisted_research_execution(
    proof_path: str | Path,
    execution_input: QualifiedResearchInput,
    *,
    expected_code_version: str,
) -> ReattestedResearchBundle:
    """Replay a persisted proof and mint fresh process-local downstream authority."""
    if not isinstance(execution_input, QualifiedResearchInput):
        raise ValueError("re-attestation requires independently supplied QualifiedResearchInput")
    if not isinstance(expected_code_version, str) or _CODE_VERSION_RE.fullmatch(expected_code_version) is None:
        raise ValueError("expected_code_version must be lowercase 40-hex")

    document = _load_canonical_proof(proof_path)
    if document["code_version"] != expected_code_version:
        raise ValueError("inter-process proof code_version does not match trusted expected_code_version")

    source = document["source"]
    if execution_input.expected_corpus_hash != source["corpus_sha256"]:
        raise ValueError("inter-process proof corpus identity differs from supplied execution input")
    if execution_input.expected_contract_hash != source["contract_sha256"]:
        raise ValueError("inter-process proof contract identity differs from supplied execution input")

    fresh_result = run_qualified_research(execution_input)
    if _execution_payload(fresh_result) != document["execution"]:
        raise ValueError("inter-process replay result differs from persisted execution claims")

    derived_dataset, derived_context = _derived_dataset_and_context(execution_input, fresh_result)
    if asdict(derived_dataset) != document["dataset"]:
        raise ValueError("inter-process replay dataset differs from persisted claims")
    if asdict(derived_context) != document["context"]:
        raise ValueError("inter-process replay context differs from persisted claims")

    fresh_evidence = from_research_execution(
        execution_input,
        fresh_result,
        code_version=expected_code_version,
        context=derived_context,
        dataset=derived_dataset,
    )
    if asdict(fresh_evidence) != document["evidence"]:
        raise ValueError("inter-process replay evidence differs from persisted claims")
    if not is_factory_attested(fresh_evidence):
        raise AssertionError("fresh replay evidence was not process-locally attested")

    return ReattestedResearchBundle(
        proof_sha256=document["proof_sha256"],
        evidence=fresh_evidence,
        dataset=derived_dataset,
        context=derived_context,
    )

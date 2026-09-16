"""Research execution evidence and the Tier-A runtime producer junction.

P0.4 makes downstream-admissible evidence depend on an actual identity-bound
research execution. The legacy V4.3 report adapter remains available for
historical/context compatibility but does not confer downstream attestation.
"""
from __future__ import annotations

import hashlib
import json
import re
import weakref
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.context import Context, validate_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision_trace import DecisionTrace


_RUNTIME_CONTRACT_ID = "RESEARCH_PRODUCER_JUNCTION_V1"
_CODE_VERSION_RE = re.compile(r"[0-9a-f]{40}\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class ResearchRunEvidence:
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    context_id: str


@dataclass(frozen=True)
class RuntimeResearchIdentity:
    dataset_id: str
    dataset_version: str
    configuration_version: str
    instrument: str
    source: str
    format: str
    corpus_sha256: str
    contract_sha256: str


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _evidence_identity_fingerprint(evidence: ResearchRunEvidence) -> str:
    return _stable_hash(
        {
            "provenance_id": evidence.provenance_id,
            "research_run_id": evidence.research_run_id,
            "code_version": evidence.code_version,
            "configuration_version": evidence.configuration_version,
            "dataset_id": evidence.dataset_id,
            "dataset_version": evidence.dataset_version,
            "context_id": evidence.context_id,
        }
    )


def _load_runtime_contract(execution_input) -> dict[str, Any]:
    from src.research.input_binding import corpus_inventory_hash, sha256_file

    contract_path = Path(execution_input.contract_path)
    corpus_root = Path(execution_input.corpus_root)
    if sha256_file(contract_path) != execution_input.expected_contract_hash:
        raise ValueError("RESEARCH producer contract identity mismatch")
    if corpus_inventory_hash(corpus_root) != execution_input.expected_corpus_hash:
        raise ValueError("RESEARCH producer corpus identity mismatch")
    with contract_path.open("r", encoding="utf-8") as handle:
        contract = json.load(handle)
    if not isinstance(contract, dict):
        raise ValueError("RESEARCH producer contract must be a JSON object")
    required = ("asset_id", "source", "format")
    if any(not isinstance(contract.get(key), str) or not contract[key].strip() for key in required):
        raise ValueError("RESEARCH producer contract lacks asset/source/format identity")
    if contract["format"] != "BI5":
        raise ValueError("RESEARCH producer requires BI5 contract format")
    return contract


def derive_runtime_research_identity(execution_input) -> RuntimeResearchIdentity:
    """Derive DATA/config identities from immutable runtime input identities."""
    from src.research.execution import QualifiedResearchInput

    if not isinstance(execution_input, QualifiedResearchInput):
        raise TypeError("runtime identity requires QualifiedResearchInput")
    if _SHA256_RE.fullmatch(execution_input.expected_corpus_hash) is None:
        raise ValueError("runtime corpus identity must be SHA-256")
    if _SHA256_RE.fullmatch(execution_input.expected_contract_hash) is None:
        raise ValueError("runtime contract identity must be SHA-256")
    contract = _load_runtime_contract(execution_input)
    dataset_id = "DATA-" + _stable_hash(
        {
            "asset_id": contract["asset_id"],
            "source": contract["source"],
            "format": contract["format"],
            "corpus_sha256": execution_input.expected_corpus_hash,
        }
    )[:16]
    dataset_version = _stable_hash(
        {
            "corpus_sha256": execution_input.expected_corpus_hash,
            "contract_sha256": execution_input.expected_contract_hash,
        }
    )[:16]
    configuration_version = "CFG-" + _stable_hash(
        {
            "producer_contract": _RUNTIME_CONTRACT_ID,
            "contract_sha256": execution_input.expected_contract_hash,
        }
    )[:16]
    return RuntimeResearchIdentity(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        configuration_version=configuration_version,
        instrument=contract["asset_id"],
        source=contract["source"],
        format=contract["format"],
        corpus_sha256=execution_input.expected_corpus_hash,
        contract_sha256=execution_input.expected_contract_hash,
    )


def _validate_runtime_dataset_and_context(
    identity: RuntimeResearchIdentity,
    dataset: DatasetIdentity,
    context: Context | None,
    result,
) -> None:
    if not isinstance(dataset, DatasetIdentity):
        raise ValueError("RESEARCH producer requires full DatasetIdentity")
    expected_dataset = {
        "dataset_id": identity.dataset_id,
        "dataset_version": identity.dataset_version,
        "content_hash": identity.corpus_sha256,
        "format": identity.format,
        "schema_version": "dukascopy-bi5-v1",
        "instrument": identity.instrument,
        "granularity": "tick",
        "timezone_storage": "UTC",
    }
    for field_name, expected in expected_dataset.items():
        if getattr(dataset, field_name) != expected:
            raise ValueError(f"RESEARCH producer dataset mismatch: {field_name}")

    if context is None or not isinstance(context, Context):
        raise ValueError("RESEARCH producer requires full Context")
    if not validate_context(context, dataset):
        raise ValueError("RESEARCH producer context identity mismatch")
    if context.configuration_version != identity.configuration_version:
        raise ValueError("RESEARCH producer configuration mismatch")
    if result.first_timestamp is None or result.last_timestamp is None:
        raise ValueError("RESEARCH producer result lacks observation bounds")
    if context.observation_start != result.first_timestamp.isoformat():
        raise ValueError("RESEARCH producer observation_start mismatch")
    if context.observation_end != result.last_timestamp.isoformat():
        raise ValueError("RESEARCH producer observation_end mismatch")


def _build_runtime_evidence_api():
    registry: dict[int, tuple[weakref.ReferenceType[ResearchRunEvidence], str]] = {}

    def create(
        execution_input,
        result,
        *,
        code_version: str,
        context: Context | None,
        dataset: DatasetIdentity,
    ) -> ResearchRunEvidence:
        from src.research.execution import (
            QualifiedResearchInput,
            ResearchExecutionResult,
            is_qualified_execution_result,
        )

        if not isinstance(execution_input, QualifiedResearchInput):
            raise ValueError("RESEARCH producer requires QualifiedResearchInput")
        if not isinstance(result, ResearchExecutionResult):
            raise ValueError("RESEARCH producer requires ResearchExecutionResult")
        if not is_qualified_execution_result(result, execution_input):
            raise ValueError("RESEARCH producer requires identity-bound qualified execution result")
        if _CODE_VERSION_RE.fullmatch(code_version) is None:
            raise ValueError("RESEARCH producer code_version must be a lowercase 40-hex commit")
        if result.files_consumed <= 0 or result.ticks_consumed <= 0:
            raise ValueError("RESEARCH producer requires non-empty execution")
        if result.first_timestamp is None or result.last_timestamp is None:
            raise ValueError("RESEARCH producer requires execution timestamps")
        if result.first_timestamp > result.last_timestamp:
            raise ValueError("RESEARCH producer timestamp bounds are inverted")
        if result.first_timestamp.tzinfo is None or result.last_timestamp.tzinfo is None:
            raise ValueError("RESEARCH producer timestamps must be timezone-aware")
        if _SHA256_RE.fullmatch(result.stream_sha256) is None:
            raise ValueError("RESEARCH producer stream identity must be SHA-256")

        identity = derive_runtime_research_identity(execution_input)
        _validate_runtime_dataset_and_context(identity, dataset, context, result)
        assert context is not None

        provenance_payload = {
            "producer_contract": _RUNTIME_CONTRACT_ID,
            "corpus_sha256": identity.corpus_sha256,
            "contract_sha256": identity.contract_sha256,
            "stream_sha256": result.stream_sha256,
            "files_consumed": result.files_consumed,
            "ticks_consumed": result.ticks_consumed,
            "first_timestamp": result.first_timestamp.isoformat(),
            "last_timestamp": result.last_timestamp.isoformat(),
        }
        provenance_id = "PROV-" + _stable_hash(provenance_payload)[:16]
        research_run_id = "RUN-" + _stable_hash(
            {
                "provenance_id": provenance_id,
                "code_version": code_version,
                "configuration_version": identity.configuration_version,
                "dataset_id": identity.dataset_id,
                "dataset_version": identity.dataset_version,
                "context_id": context.context_id,
            }
        )[:16]
        evidence = ResearchRunEvidence(
            provenance_id=provenance_id,
            research_run_id=research_run_id,
            code_version=code_version,
            configuration_version=identity.configuration_version,
            dataset_id=identity.dataset_id,
            dataset_version=identity.dataset_version,
            context_id=context.context_id,
        )
        object_id = id(evidence)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(evidence, cleanup)
        registry[object_id] = (reference, _evidence_identity_fingerprint(evidence))
        return evidence

    def verify(evidence: object) -> bool:
        if not isinstance(evidence, ResearchRunEvidence):
            return False
        entry = registry.get(id(evidence))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not evidence:
            return False
        return _evidence_identity_fingerprint(evidence) == expected_fingerprint

    return create, verify


from_research_execution, is_factory_attested = _build_runtime_evidence_api()
del _build_runtime_evidence_api


def _validate_context_boundary(
    context: Context | None,
    dataset: DatasetIdentity,
    configuration_version: str,
) -> None:
    if context is None:
        raise ValueError("CONTEXT -> RESEARCH requires a Context")
    if not isinstance(context, Context):
        raise ValueError("CONTEXT -> RESEARCH requires the full Context object")
    if not validate_context(context, dataset):
        raise ValueError("CONTEXT -> RESEARCH identity mismatch")
    if context.configuration_version != configuration_version:
        raise ValueError("CONTEXT -> RESEARCH configuration mismatch")


def from_v43_report(
    report: dict[str, Any],
    *,
    code_version: str,
    context: Context | None,
    dataset: DatasetIdentity,
) -> ResearchRunEvidence:
    """Parse legacy V4.3 evidence without granting runtime producer attestation."""
    if report.get("schema") != "RESEARCH_EXECUTION_COMPATIBILITY_V4_3":
        raise ValueError("unsupported research report schema")
    research_files = report.get("research", {}).get("files", [])
    if not research_files or any(not item.get("sha256") for item in research_files):
        raise ValueError("research report lacks immutable source-file hashes")
    source_hashes = sorted(item["sha256"] for item in research_files)
    provenance_id = "PROV-" + _stable_hash(source_hashes)[:16]
    report_dataset_id = "DATA-" + _stable_hash({"research_files": source_hashes})[:16]
    dataset_version = _stable_hash(report.get("research", {}))[:16]
    research_run_id = "RUN-" + _stable_hash(report)[:16]
    configuration_version = "CFG-" + _stable_hash(report.get("scope", {}))[:16]
    _validate_context_boundary(context, dataset, configuration_version)
    assert context is not None
    if context.dataset_id != report_dataset_id or context.dataset_version != dataset_version:
        raise ValueError("CONTEXT -> RESEARCH report identity mismatch")
    return ResearchRunEvidence(
        provenance_id=provenance_id,
        research_run_id=research_run_id,
        code_version=code_version,
        configuration_version=configuration_version,
        dataset_id=report_dataset_id,
        dataset_version=dataset_version,
        context_id=context.context_id,
    )


def decision_trace_from_v43_report(
    report: dict[str, Any],
    *,
    code_version: str,
    context: Context | None,
    dataset: DatasetIdentity,
) -> DecisionTrace:
    """Build a legacy trace record; it is not downstream producer attestation."""
    evidence = from_v43_report(
        report,
        code_version=code_version,
        context=context,
        dataset=dataset,
    )
    return DecisionTrace(
        decision_id="",
        provenance_id=evidence.provenance_id,
        research_run_id=evidence.research_run_id,
        code_version=evidence.code_version,
        configuration_version=evidence.configuration_version,
        dataset_id=evidence.dataset_id,
        dataset_version=evidence.dataset_version,
        context_id=evidence.context_id,
        decision="",
        action_id="",
        result_id="",
    )

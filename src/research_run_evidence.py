"""Minimal adapter from the existing V4.3 research report to decision traceability.

This does not invent a research registry. It derives stable evidence identifiers
from the existing V4.3 report and its source-file hashes, then consumes the
existing CONTEXT object at the CONTEXT -> RESEARCH boundary.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass
from typing import Any

from src.context import Context, validate_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision_trace import DecisionTrace


@dataclass(frozen=True)
class ResearchRunEvidence:
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    context_id: str


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


def _build_attestation_gate():
    """Create a process-local factory attestation bound to object identity and content.

    The registry is deliberately kept inside this closure rather than on the
    evidence object. A caller cannot make a reconstructed dataclass admissible by
    copying fields or by setting a marker attribute. The stored fingerprint also
    invalidates an originally attested object if its frozen fields are bypassed
    with ``object.__setattr__``.
    """

    registry: dict[int, tuple[weakref.ReferenceType[ResearchRunEvidence], str]] = {}

    def attest(evidence: ResearchRunEvidence) -> ResearchRunEvidence:
        object_id = id(evidence)

        def cleanup(
            reference: weakref.ReferenceType[ResearchRunEvidence],
            *,
            expected_object_id: int = object_id,
        ) -> None:
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

    return attest, verify


_attest_factory_evidence, is_factory_attested = _build_attestation_gate()
del _build_attestation_gate


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
    """Anchor V4.3 evidence only after validating the existing CONTEXT boundary."""
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

    if context.dataset_id != report_dataset_id or context.dataset_version != dataset_version:
        raise ValueError("CONTEXT -> RESEARCH report identity mismatch")

    evidence = ResearchRunEvidence(
        provenance_id=provenance_id,
        research_run_id=research_run_id,
        code_version=code_version,
        configuration_version=configuration_version,
        dataset_id=report_dataset_id,
        dataset_version=dataset_version,
        context_id=context.context_id,
    )
    return _attest_factory_evidence(evidence)


def decision_trace_from_v43_report(
    report: dict[str, Any],
    *,
    code_version: str,
    context: Context | None,
    dataset: DatasetIdentity,
) -> DecisionTrace:
    """Build trace using real V4.3 evidence; downstream fields remain explicit."""
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

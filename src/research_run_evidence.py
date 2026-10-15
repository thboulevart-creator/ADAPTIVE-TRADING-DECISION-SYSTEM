"""Minimal adapter from the existing V4.3 research report to decision traceability.

This does not invent a research registry. It derives stable evidence identifiers
from the existing V4.3 report and its source-file hashes, then exposes the
upstream part of the DecisionTrace chain. Missing downstream decision/action/
result evidence remains a FAIL.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from src.decision_trace import DecisionTrace


@dataclass(frozen=True)
class ResearchRunEvidence:
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def from_v43_report(report: dict[str, Any], *, code_version: str) -> ResearchRunEvidence:
    """Anchor the existing V4.3 report to stable provenance/run/dataset IDs."""
    if report.get("schema") != "RESEARCH_EXECUTION_COMPATIBILITY_V4_3":
        raise ValueError("unsupported research report schema")

    research_files = report.get("research", {}).get("files", [])
    if not research_files or any(not item.get("sha256") for item in research_files):
        raise ValueError("research report lacks immutable source-file hashes")

    source_hashes = sorted(item["sha256"] for item in research_files)
    provenance_id = "PROV-" + _stable_hash(source_hashes)[:16]
    dataset_id = "DATA-" + _stable_hash({"research_files": source_hashes})[:16]
    dataset_version = _stable_hash(report.get("research", {}))[:16]
    research_run_id = "RUN-" + _stable_hash(report)[:16]
    configuration_version = "CFG-" + _stable_hash(report.get("scope", {}))[:16]

    return ResearchRunEvidence(
        provenance_id=provenance_id,
        research_run_id=research_run_id,
        code_version=code_version,
        configuration_version=configuration_version,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
    )


def decision_trace_from_v43_report(
    report: dict[str, Any], *, code_version: str
) -> DecisionTrace:
    """Build the trace using real V4.3 evidence; downstream fields stay explicit."""
    evidence = from_v43_report(report, code_version=code_version)
    return DecisionTrace(
        decision_id="",
        provenance_id=evidence.provenance_id,
        research_run_id=evidence.research_run_id,
        code_version=evidence.code_version,
        configuration_version=evidence.configuration_version,
        dataset_id=evidence.dataset_id,
        dataset_version=evidence.dataset_version,
        context_id="",
        decision="",
        action_id="",
        result_id="",
    )

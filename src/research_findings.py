from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable, Mapping

from research_run_evidence import ResearchRunEvidence


STATUSES = {"SUPPORTED", "REFUTED", "NOT_INTERPRETABLE"}


@dataclass(frozen=True)
class ResearchHypothesis:
    hypothesis_id: str
    statement: str
    prediction: str
    falsification_rule: str


@dataclass(frozen=True)
class ResearchMeasurement:
    measurement_id: str
    regime: str
    expert: str
    metric: str
    value: float
    sample_size: int
    scope: str


@dataclass(frozen=True)
class ResearchFinding:
    finding_id: str
    hypothesis_id: str
    statement: str
    supporting_measurement_ids: tuple[str, ...]
    status: str
    rule_reference: str
    reason: str


@dataclass(frozen=True)
class ResearchFindings:
    findings_id: str
    provenance_id: str
    research_run_id: str
    code_version: str
    configuration_version: str
    dataset_id: str
    dataset_version: str
    context_id: str
    hypotheses: tuple[ResearchHypothesis, ...]
    measurements: tuple[ResearchMeasurement, ...]
    findings: tuple[ResearchFinding, ...]
    evidence_refs: tuple[str, ...]

    @classmethod
    def from_research_run_evidence(
        cls,
        evidence: ResearchRunEvidence,
        *,
        hypotheses: Iterable[ResearchHypothesis],
        measurements: Iterable[ResearchMeasurement],
        findings: Iterable[ResearchFinding],
        evidence_refs: Iterable[str] = (),
    ) -> "ResearchFindings":
        if not isinstance(evidence, ResearchRunEvidence):
            raise TypeError("ResearchFindings requires ResearchRunEvidence")

        hs = tuple(hypotheses)
        ms = tuple(measurements)
        fs = tuple(findings)
        refs = tuple(evidence_refs)

        for name, value in (
            ("provenance_id", evidence.provenance_id),
            ("research_run_id", evidence.research_run_id),
            ("code_version", evidence.code_version),
            ("configuration_version", evidence.configuration_version),
            ("dataset_id", evidence.dataset_id),
            ("dataset_version", evidence.dataset_version),
            ("context_id", evidence.context_id),
        ):
            if not value:
                raise ValueError(f"{name} must be non-empty")

        _require_unique("hypothesis_id", (h.hypothesis_id for h in hs))
        _require_unique("measurement_id", (m.measurement_id for m in ms))
        _require_unique("finding_id", (f.finding_id for f in fs))

        hypothesis_ids = {h.hypothesis_id for h in hs}
        measurement_ids = {m.measurement_id for m in ms}

        for h in hs:
            if not all((h.hypothesis_id, h.statement, h.prediction, h.falsification_rule)):
                raise ValueError("hypothesis fields must be non-empty")

        for m in ms:
            if not all((m.measurement_id, m.regime, m.expert, m.metric, m.scope)):
                raise ValueError("measurement identity/scope fields must be non-empty")
            if m.sample_size <= 0:
                raise ValueError("measurement sample_size must be positive")

        for f in fs:
            if f.status not in STATUSES:
                raise ValueError("invalid finding status")
            if not all((f.finding_id, f.hypothesis_id, f.statement, f.rule_reference, f.reason)):
                raise ValueError("finding fields must be non-empty")
            if f.hypothesis_id not in hypothesis_ids:
                raise ValueError("finding references unknown hypothesis")
            if not f.supporting_measurement_ids:
                raise ValueError("finding requires supporting measurements")
            if any(mid not in measurement_ids for mid in f.supporting_measurement_ids):
                raise ValueError("finding references unknown measurement")

        payload = {
            "research_run_id": evidence.research_run_id,
            "hypotheses": [h.__dict__ for h in hs],
            "measurements": [m.__dict__ for m in ms],
            "findings": [f.__dict__ for f in fs],
            "evidence_refs": refs,
        }
        findings_id = "FIND-" + hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()[:16]

        return cls(
            findings_id=findings_id,
            provenance_id=evidence.provenance_id,
            research_run_id=evidence.research_run_id,
            code_version=evidence.code_version,
            configuration_version=evidence.configuration_version,
            dataset_id=evidence.dataset_id,
            dataset_version=evidence.dataset_version,
            context_id=evidence.context_id,
            hypotheses=hs,
            measurements=ms,
            findings=fs,
            evidence_refs=refs,
        )


def _require_unique(label: str, values: Iterable[str]) -> None:
    values = tuple(values)
    if any(not value for value in values):
        raise ValueError(f"{label} must be non-empty")
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {label}")

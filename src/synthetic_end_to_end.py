"""Minimal synthetic execution chain used to test component wiring.

This module is deliberately not a trading engine. It creates deterministic
synthetic evidence for the chain:
DATA -> CONTEXT -> EXPERIENCE -> DECISION -> ACTION -> RESULT -> TRACE.

Every stage requires the previous stage and emits a stable identifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from src.decision_trace import DecisionTrace


@dataclass(frozen=True)
class SyntheticData:
    data_id: str
    dataset_id: str
    dataset_version: str


@dataclass(frozen=True)
class SyntheticContext:
    context_id: str
    data_id: str


@dataclass(frozen=True)
class SyntheticExperience:
    research_run_id: str
    context_id: str
    hypothesis: str


@dataclass(frozen=True)
class SyntheticDecision:
    decision_id: str
    experience_id: str
    decision: str


@dataclass(frozen=True)
class SyntheticAction:
    action_id: str
    decision_id: str
    action: str


@dataclass(frozen=True)
class SyntheticResult:
    result_id: str
    action_id: str
    outcome: str


def _id(kind: str, *parts: str) -> str:
    payload = "|".join((kind, *parts)).encode("utf-8")
    return f"{kind}-{sha256(payload).hexdigest()[:16]}"


def build_synthetic_chain() -> tuple[SyntheticData, SyntheticContext, SyntheticExperience, SyntheticDecision, SyntheticAction, SyntheticResult, DecisionTrace]:
    data = SyntheticData("data-synthetic-001", "dataset-synthetic", "v1")
    context = SyntheticContext(_id("context", data.data_id), data.data_id)
    experience = SyntheticExperience(
        _id("run", context.context_id),
        context.context_id,
        "synthetic-condition-is-actionable",
    )
    decision = SyntheticDecision(
        _id("decision", experience.research_run_id),
        experience.research_run_id,
        "ACT",
    )
    action = SyntheticAction(
        _id("action", decision.decision_id),
        decision.decision_id,
        "EXECUTE_SYNTHETIC_ACTION",
    )
    result = SyntheticResult(
        _id("result", action.action_id),
        action.action_id,
        "SUCCESS",
    )
    trace = DecisionTrace(
        decision_id=decision.decision_id,
        provenance_id=_id("provenance", data.data_id),
        research_run_id=experience.research_run_id,
        code_version="synthetic-code-v1",
        configuration_version="synthetic-config-v1",
        dataset_id=data.dataset_id,
        dataset_version=data.dataset_version,
        context_id=context.context_id,
        decision=decision.decision,
        action_id=action.action_id,
        result_id=result.result_id,
    )
    return data, context, experience, decision, action, result, trace

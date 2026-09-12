"""Minimal producer contract for DECISION.

A Decision is produced only from the actual RESEARCH output and the actual
CONTEXT that was used to obtain it. This module deliberately does not invent
trading logic: the decision payload must come from the future decision policy.

The producer therefore closes only the executable RESEARCH -> DECISION
contract. ACTION/RESULT/TRACE remain downstream and are intentionally absent.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from src.context import Context
from src.research_run_evidence import ResearchRunEvidence


@dataclass(frozen=True)
class Decision:
    """A decision anchored to one concrete research run and context."""

    decision_id: str
    research_run_id: str
    context_id: str
    decision: str


def _decision_id(research_run_id: str, context_id: str, decision: str) -> str:
    payload = json.dumps(
        {
            "research_run_id": research_run_id,
            "context_id": context_id,
            "decision": decision,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return "DEC-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def produce_decision(
    evidence: ResearchRunEvidence | None,
    *,
    context: Context | None,
    decision: str,
) -> Decision:
    """Produce a decision only from coherent upstream RESEARCH evidence.

    ``decision`` is deliberately an input here rather than invented trading
    logic. It represents the output that a future decision policy will supply.
    """
    if evidence is None:
        raise ValueError("RESEARCH -> DECISION requires ResearchRunEvidence")
    if not isinstance(evidence, ResearchRunEvidence):
        raise ValueError("RESEARCH -> DECISION requires the full ResearchRunEvidence object")
    if context is None:
        raise ValueError("RESEARCH -> DECISION requires a Context")
    if not isinstance(context, Context):
        raise ValueError("RESEARCH -> DECISION requires the full Context object")
    if evidence.context_id != context.context_id:
        raise ValueError("RESEARCH -> DECISION context mismatch")
    if not evidence.research_run_id.strip():
        raise ValueError("RESEARCH -> DECISION requires research_run_id")
    if not decision.strip():
        raise ValueError("RESEARCH -> DECISION requires a non-empty decision")

    return Decision(
        decision_id=_decision_id(evidence.research_run_id, context.context_id, decision),
        research_run_id=evidence.research_run_id,
        context_id=context.context_id,
        decision=decision,
    )

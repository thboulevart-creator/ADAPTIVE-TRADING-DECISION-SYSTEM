from dataclasses import replace

import pytest

from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.research_run_evidence import from_v43_report


CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"


def v43_report() -> dict:
    return {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
        "version": "V4.3",
        "status": "UNVERIFIED",
        "scope": {
            "research_instrument": "Dukascopy USATECHIDXUSD",
            "execution_instrument": "VT Markets NAS100.s",
            "minimum_research_years": 5.0,
        },
        "research": {
            "files": [
                {"path": "research/a.bi5", "sha256": "aaa"},
                {"path": "research/b.bi5", "sha256": "bbb"},
            ],
            "rows": 100,
            "first": "2020-01-01T00:00:00+00:00",
            "last": "2025-01-01T00:00:00+00:00",
        },
    }


def coherent_inputs():
    report = v43_report()
    from src.research_run_evidence import _stable_hash

    source_hashes = ["aaa", "bbb"]
    dataset_id = "DATA-" + _stable_hash({"research_files": source_hashes})[:16]
    dataset_version = _stable_hash(report["research"])[:16]
    configuration_version = "CFG-" + _stable_hash(report["scope"])[:16]
    dataset = DatasetIdentity(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        content_hash="content-hash",
        format="csv",
        schema_version="tick-csv-v1",
        instrument="VT Markets NAS100.s",
        granularity="tick",
        timezone_storage="UTC",
    )
    context = build_context(
        dataset,
        configuration_version=configuration_version,
        observation_start="2020-01-01T00:00:00+00:00",
        observation_end="2025-01-01T00:00:00+00:00",
    )
    evidence = from_v43_report(
        report,
        code_version=CODE_VERSION,
        context=context,
        dataset=dataset,
    )
    return evidence, context


def test_c0_coherent_research_output_produces_decision() -> None:
    evidence, context = coherent_inputs()
    decision = produce_decision(evidence, context=context, decision="HOLD")

    assert decision.decision_id.startswith("DEC-")
    assert decision.research_run_id == evidence.research_run_id
    assert decision.context_id == context.context_id
    assert decision.decision == "HOLD"


@pytest.mark.parametrize(
    "case, mutate",
    [
        ("C1", lambda e: replace(e, context_id="CTX-foreign")),
        ("C2", lambda e: replace(e, research_run_id="RUN-foreign")),
        ("C3", lambda e: replace(e, dataset_id="DATA-foreign")),
        ("C4", lambda e: replace(e, dataset_version="VERSION-foreign")),
        ("C5", lambda e: replace(e, configuration_version="CFG-foreign")),
        ("C6", lambda e: replace(e, provenance_id="PROV-foreign")),
    ],
)
def test_c1_to_c6_mutated_research_evidence_is_rejected(case, mutate) -> None:
    evidence, context = coherent_inputs()
    with pytest.raises(ValueError):
        produce_decision(mutate(evidence), context=context, decision="HOLD")


def test_c7_absent_research_evidence_is_rejected() -> None:
    _, context = coherent_inputs()
    with pytest.raises(ValueError, match="ResearchRunEvidence"):
        produce_decision(None, context=context, decision="HOLD")


def test_c8_context_only_is_rejected_as_research_output() -> None:
    _, context = coherent_inputs()
    with pytest.raises(ValueError, match="ResearchRunEvidence"):
        produce_decision(context, context=context, decision="HOLD")


def test_c9_foreign_context_is_rejected() -> None:
    evidence, context = coherent_inputs()
    foreign_context = replace(context, context_id="CTX-foreign")
    with pytest.raises(ValueError, match="context mismatch"):
        produce_decision(evidence, context=foreign_context, decision="HOLD")


def test_c10_empty_decision_is_rejected() -> None:
    evidence, context = coherent_inputs()
    with pytest.raises(ValueError, match="non-empty decision"):
        produce_decision(evidence, context=context, decision="   ")


def test_decision_id_is_deterministic_for_same_upstream_evidence_and_payload() -> None:
    evidence, context = coherent_inputs()
    first = produce_decision(evidence, context=context, decision="BUY")
    second = produce_decision(evidence, context=context, decision="BUY")

    assert first == second


def test_decision_id_changes_when_decision_payload_changes() -> None:
    evidence, context = coherent_inputs()
    buy = produce_decision(evidence, context=context, decision="BUY")
    sell = produce_decision(evidence, context=context, decision="SELL")

    assert buy.decision_id != sell.decision_id

import pytest

from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence, _stable_hash, from_v43_report

CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"


def coherent_inputs():
    report = {
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


def test_bypass_manual_research_run_evidence_is_rejected():
    legitimate, context = coherent_inputs()
    fabricated = ResearchRunEvidence(
        provenance_id="PROV-fake",
        research_run_id="RUN-fake",
        code_version="attacker-code",
        configuration_version="attacker-config",
        dataset_id="DATA-fake",
        dataset_version="attacker-version",
        context_id=context.context_id,
    )

    with pytest.raises(ValueError):
        produce_decision(fabricated, context=context, decision="BUY")


def test_bypass_tampered_research_identity_is_rejected():
    legitimate, context = coherent_inputs()
    tampered = ResearchRunEvidence(
        provenance_id="PROV-fake",
        research_run_id=legitimate.research_run_id,
        code_version=legitimate.code_version,
        configuration_version="CFG-fake",
        dataset_id="DATA-fake",
        dataset_version="VERSION-fake",
        context_id=context.context_id,
    )

    with pytest.raises(ValueError):
        produce_decision(tampered, context=context, decision="BUY")


def test_bypass_context_id_only_with_valid_shape_is_rejected():
    _, context = coherent_inputs()
    context_only = ResearchRunEvidence(
        provenance_id="",
        research_run_id="RUN-from-context-only",
        code_version="",
        configuration_version="",
        dataset_id="",
        dataset_version="",
        context_id=context.context_id,
    )

    with pytest.raises(ValueError):
        produce_decision(context_only, context=context, decision="BUY")

import pytest

from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence, _stable_hash, from_v43_report, is_factory_attested


CODE_VERSION = "963f02e93db63bef36c25d58c3634096a2247e6a"


def legacy_inputs():
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
    return report, dataset, context


def test_c1_legacy_v43_report_only_path_is_not_downstream_admissible() -> None:
    report, dataset, context = legacy_inputs()
    evidence = from_v43_report(
        report,
        code_version=CODE_VERSION,
        context=context,
        dataset=dataset,
    )

    assert not is_factory_attested(evidence), (
        "legacy V4.3 report-only evidence bypasses the real runtime producer junction"
    )
    with pytest.raises(ValueError, match="factory-attested"):
        produce_decision(evidence, context=context, decision="HOLD")


def test_c2_module_exposes_no_raw_evidence_attestation_minter() -> None:
    import src.research_run_evidence as module

    assert not hasattr(module, "_attest_factory_evidence"), (
        "raw ResearchRunEvidence attestation capability is reachable at module scope"
    )


def test_c3_manual_evidence_cannot_be_promoted_through_module_escape() -> None:
    import src.research_run_evidence as module

    _, _, context = legacy_inputs()
    fabricated = ResearchRunEvidence(
        provenance_id="PROV-manual",
        research_run_id="RUN-manual",
        code_version=CODE_VERSION,
        configuration_version=context.configuration_version,
        dataset_id=context.dataset_id,
        dataset_version=context.dataset_version,
        context_id=context.context_id,
    )

    minter = getattr(module, "_attest_factory_evidence", None)
    assert minter is None, "manual object can reach the raw evidence attestation capability"
    assert not is_factory_attested(fabricated)
    with pytest.raises(ValueError, match="factory-attested"):
        produce_decision(fabricated, context=context, decision="HOLD")

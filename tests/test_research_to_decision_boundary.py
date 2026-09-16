import copy
from dataclasses import replace

import pytest

from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence, from_v43_report, is_factory_attested


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


def reconstruct(evidence: ResearchRunEvidence) -> ResearchRunEvidence:
    return ResearchRunEvidence(
        provenance_id=evidence.provenance_id,
        research_run_id=evidence.research_run_id,
        code_version=evidence.code_version,
        configuration_version=evidence.configuration_version,
        dataset_id=evidence.dataset_id,
        dataset_version=evidence.dataset_version,
        context_id=evidence.context_id,
    )


def test_c0_coherent_research_output_produces_decision() -> None:
    evidence, context = coherent_inputs()
    assert is_factory_attested(evidence)

    decision = produce_decision(evidence, context=context, decision="HOLD")

    assert decision.decision_id.startswith("DEC-")
    assert decision.research_run_id == evidence.research_run_id
    assert decision.context_id == context.context_id
    assert decision.decision == "HOLD"


def test_c1_reconstructed_forged_context_id_is_rejected_before_semantic_use() -> None:
    evidence, context = coherent_inputs()
    forged = replace(evidence, context_id="CTX-foreign")
    assert not is_factory_attested(forged)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(forged, context=context, decision="HOLD")


def test_c2_reconstructed_empty_research_run_id_is_rejected_before_semantic_use() -> None:
    evidence, context = coherent_inputs()
    missing = replace(evidence, research_run_id="")
    assert not is_factory_attested(missing)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(missing, context=context, decision="HOLD")


def test_c3_absent_research_evidence_is_rejected() -> None:
    _, context = coherent_inputs()
    with pytest.raises(ValueError, match="ResearchRunEvidence"):
        produce_decision(None, context=context, decision="HOLD")


def test_c4_context_only_is_rejected_as_research_output() -> None:
    _, context = coherent_inputs()
    with pytest.raises(ValueError, match="ResearchRunEvidence"):
        produce_decision(context, context=context, decision="HOLD")


def test_c5_foreign_context_is_rejected() -> None:
    evidence, context = coherent_inputs()
    foreign_context = replace(context, context_id="CTX-foreign")
    with pytest.raises(ValueError, match="context mismatch"):
        produce_decision(evidence, context=foreign_context, decision="HOLD")


def test_c6_empty_decision_is_rejected() -> None:
    evidence, context = coherent_inputs()
    with pytest.raises(ValueError, match="non-empty decision"):
        produce_decision(evidence, context=context, decision="   ")


def test_c7_research_run_id_is_propagated_without_reconstruction() -> None:
    evidence, context = coherent_inputs()
    decision = produce_decision(evidence, context=context, decision="BUY")

    assert decision.research_run_id == evidence.research_run_id


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


def test_exact_field_reconstruction_is_rejected() -> None:
    evidence, context = coherent_inputs()
    forged = reconstruct(evidence)

    assert forged == evidence
    assert forged is not evidence
    assert not is_factory_attested(forged)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(forged, context=context, decision="HOLD")


def test_legacy_self_declared_factory_marker_cannot_attest_reconstruction() -> None:
    evidence, context = coherent_inputs()
    forged = reconstruct(evidence)
    object.__setattr__(forged, "_factory_validated", True)

    assert getattr(forged, "_factory_validated") is True
    assert not is_factory_attested(forged)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(forged, context=context, decision="HOLD")


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_silent_copy_reconstruction_is_rejected(copier) -> None:
    evidence, context = coherent_inputs()
    reconstructed = copier(evidence)

    assert reconstructed == evidence
    assert reconstructed is not evidence
    assert not is_factory_attested(reconstructed)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(reconstructed, context=context, decision="HOLD")


def test_post_factory_research_identity_mutation_invalidates_attestation() -> None:
    evidence, context = coherent_inputs()
    assert is_factory_attested(evidence)

    object.__setattr__(evidence, "research_run_id", "RUN-forged-after-factory")

    assert not is_factory_attested(evidence)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(evidence, context=context, decision="HOLD")


def test_post_factory_context_identity_mutation_invalidates_attestation() -> None:
    evidence, context = coherent_inputs()
    assert is_factory_attested(evidence)

    object.__setattr__(evidence, "context_id", "CTX-forged-after-factory")

    assert not is_factory_attested(evidence)
    with pytest.raises(ValueError, match="factory-attested, identity-bound"):
        produce_decision(evidence, context=context, decision="HOLD")

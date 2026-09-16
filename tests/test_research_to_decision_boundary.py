import copy
from dataclasses import replace

import pytest

from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_inputs():
    return coherent_runtime_inputs()


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

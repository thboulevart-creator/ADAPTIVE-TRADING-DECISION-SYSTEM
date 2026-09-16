import pytest

from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence
from tests.research_runtime_fixture import coherent_runtime_inputs


def coherent_inputs():
    return coherent_runtime_inputs()


def test_bypass_manual_research_run_evidence_is_rejected():
    _, context = coherent_inputs()
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

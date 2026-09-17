import weakref

import src.research_run_evidence as evidence_module
from src.decision import produce_decision
from src.research_run_evidence import ResearchRunEvidence, is_factory_attested
from tests.research_runtime_fixture import synthetic_runtime_case


def _closure_registry(function) -> dict:
    closure = function.__closure__ or ()
    registries = [cell.cell_contents for cell in closure if isinstance(cell.cell_contents, dict)]
    assert len(registries) == 1
    return registries[0]


def test_p0_4_reflective_registry_mutation_is_explicit_process_compromise() -> None:
    """C2R: reflective mutation can forge process-local authority; it is not a supported API minter."""
    assert getattr(evidence_module, "_attest_factory_evidence", None) is None

    with synthetic_runtime_case() as case:
        source = case.evidence
        forged = ResearchRunEvidence(
            provenance_id=source.provenance_id,
            research_run_id=source.research_run_id,
            code_version=source.code_version,
            configuration_version=source.configuration_version,
            dataset_id=source.dataset_id,
            dataset_version=source.dataset_version,
            context_id=source.context_id,
        )
        assert not is_factory_attested(forged)

        registry = _closure_registry(is_factory_attested)
        registry[id(forged)] = (
            weakref.ref(forged),
            evidence_module._evidence_identity_fingerprint(forged),
        )
        try:
            assert is_factory_attested(forged)
            decision = produce_decision(forged, context=case.context, decision="HOLD")
            assert decision.research_run_id == forged.research_run_id
        finally:
            registry.pop(id(forged), None)

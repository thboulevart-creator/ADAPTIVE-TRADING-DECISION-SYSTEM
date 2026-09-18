from __future__ import annotations

import copy
import gc
import importlib
import inspect
import weakref
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.evidence_assessment_criteria import (
    EvidenceAssessmentCriteria,
    declare_evidence_assessment_criteria,
    is_factory_attested_evidence_assessment_criteria,
)
from src.evidence_material_binding import (
    BoundEvidenceMaterial,
    bind_evidence_material,
    is_factory_attested_bound_evidence_material,
)
from src.evidence_submission import submit_evidence
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P112A_CONTRACT = "P1_12A_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_12A_TEST_CAPTURE_AUTHORITY_V1"


def _historical(tmp_path: Path) -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="OBSERVED")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _evidence_request(tmp_path: Path):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which evidence is required?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EVIDENCE",
        "Evaluate exact evidence against explicit criteria.",
    )
    return produce_follow_up_request(revision)


def _criteria(
    tmp_path: Path,
    *,
    minimum_distinct_materials=1,
    require_nonempty_content=True,
    allowed_media_types=("application/pdf",),
    allowed_source_refs=("urn:test:one", "urn:test:two"),
    semantic_requirements=(),
):
    return declare_evidence_assessment_criteria(
        _evidence_request(tmp_path),
        minimum_distinct_materials=minimum_distinct_materials,
        require_nonempty_content=require_nonempty_content,
        allowed_media_types=allowed_media_types,
        allowed_source_refs=allowed_source_refs,
        semantic_requirements=semantic_requirements,
    )


def _material(request, *, source_ref="urn:test:one", media_type="application/pdf", content=b"evidence"):
    submission = submit_evidence(
        request,
        source_ref=source_ref,
        media_type=media_type,
        content=content,
    )
    return bind_evidence_material(submission, content=content)


def _criteria_and_materials(
    tmp_path: Path,
    *,
    minimum_distinct_materials=1,
    require_nonempty_content=True,
    allowed_media_types=("application/pdf",),
    allowed_source_refs=("urn:test:one", "urn:test:two"),
    semantic_requirements=(),
    material_specs=(("urn:test:one", "application/pdf", b"evidence"),),
):
    request = _evidence_request(tmp_path)
    criteria = declare_evidence_assessment_criteria(
        request,
        minimum_distinct_materials=minimum_distinct_materials,
        require_nonempty_content=require_nonempty_content,
        allowed_media_types=allowed_media_types,
        allowed_source_refs=allowed_source_refs,
        semantic_requirements=semantic_requirements,
    )
    materials = tuple(
        _material(request, source_ref=source, media_type=media, content=content)
        for source, media, content in material_specs
    )
    return criteria, materials


def _p112a():
    try:
        module = importlib.import_module("src.declared_evidence_criteria_assessment")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.12A candidate absent — expected pre-implementation FAIL: "
            "src.declared_evidence_criteria_assessment does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "DeclaredEvidenceCriteriaAssessment",
        "assess_declared_evidence_criteria",
        "is_factory_attested_declared_evidence_criteria_assessment",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.12A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P112A_CONTRACT
    return module


def _assess(criteria, materials):
    return _p112a().assess_declared_evidence_criteria(criteria, materials)


def test_a0_exact_criteria_and_material_positive(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    assert result.criteria_id == criteria.criteria_id
    assert result.material_binding_ids == tuple(m.evidence_binding_id for m in materials)
    assert _p112a().is_factory_attested_declared_evidence_criteria_assessment(result)


def test_a1_non_authoritative_criteria_rejected(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    variants = [
        criteria.criteria_id,
        asdict(criteria),
        EvidenceAssessmentCriteria(**asdict(criteria)),
        copy.copy(criteria),
        copy.deepcopy(criteria),
        replace(criteria, criteria_id=criteria.criteria_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _assess(value, materials)


def test_a2_non_authoritative_material_rejected(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    material = materials[0]
    variants = [
        material.evidence_binding_id,
        asdict(material),
        BoundEvidenceMaterial(**asdict(material)),
        copy.copy(material),
        copy.deepcopy(material),
        replace(material, evidence_binding_id=material.evidence_binding_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _assess(criteria, (value,))


def test_a3_mutated_then_restored_authorities_rejected(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    material = materials[0]
    original_criteria = criteria.specification
    object.__setattr__(criteria, "specification", "MUTATED")
    assert not is_factory_attested_evidence_assessment_criteria(criteria)
    object.__setattr__(criteria, "specification", original_criteria)
    with pytest.raises((TypeError, ValueError)):
        _assess(criteria, materials)

    criteria, materials = _criteria_and_materials(tmp_path / "second")
    material = materials[0]
    original_content = material.content
    object.__setattr__(material, "content", b"MUTATED")
    assert not is_factory_attested_bound_evidence_material(material)
    object.__setattr__(material, "content", original_content)
    with pytest.raises((TypeError, ValueError)):
        _assess(criteria, materials)


@pytest.mark.parametrize("materials", [[], set(), {}, "x", None, ()])
def test_b0_materials_requires_exact_nonempty_tuple(tmp_path: Path, materials) -> None:
    criteria = _criteria(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _assess(criteria, materials)


def test_b1_signature_is_exact() -> None:
    sig = inspect.signature(_p112a().assess_declared_evidence_criteria)
    assert tuple(sig.parameters) == ("criteria", "materials")
    for parameter in sig.parameters.values():
        assert parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert parameter.default is inspect.Parameter.empty


def test_c0_cross_request_material_rejected(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path / "one")
    other_request = _evidence_request(tmp_path / "two")
    foreign = _material(other_request)
    with pytest.raises((TypeError, ValueError)):
        _assess(criteria, materials + (foreign,))


def test_c1_duplicate_binding_id_rejected(tmp_path: Path) -> None:
    request = _evidence_request(tmp_path)
    criteria = declare_evidence_assessment_criteria(
        request,
        minimum_distinct_materials=1,
        require_nonempty_content=True,
        allowed_media_types=("application/pdf",),
        allowed_source_refs=("urn:test:one",),
        semantic_requirements=(),
    )
    first = _material(request)
    second = _material(request)
    assert first.evidence_binding_id == second.evidence_binding_id
    with pytest.raises((TypeError, ValueError)):
        _assess(criteria, (first, second))


def test_d0_all_structural_criteria_pass(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        minimum_distinct_materials=2,
        material_specs=(
            ("urn:test:one", "application/pdf", b"A"),
            ("urn:test:two", "application/pdf", b"B"),
        ),
    )
    result = _assess(criteria, materials)
    assert result.distinct_material_count == 2
    assert result.minimum_distinct_materials_status == "PASS"
    assert result.nonempty_content_status == "PASS"
    assert result.media_type_status == "PASS"
    assert result.source_ref_status == "PASS"
    assert result.semantic_requirements_status == "PASS"
    assert result.declared_criteria_verdict == "PASS"
    assert result.request_fulfillment_status == "BLOCKED"


def test_d1_minimum_materials_failure(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path, minimum_distinct_materials=2)
    result = _assess(criteria, materials)
    assert result.minimum_distinct_materials_status == "FAIL"
    assert result.declared_criteria_verdict == "FAIL"


def test_d2_empty_content_failure_when_required(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        material_specs=(("urn:test:one", "application/pdf", b""),),
    )
    result = _assess(criteria, materials)
    assert result.nonempty_content_status == "FAIL"
    assert result.declared_criteria_verdict == "FAIL"


def test_d3_empty_content_pass_when_not_required(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        require_nonempty_content=False,
        material_specs=(("urn:test:one", "application/pdf", b""),),
    )
    assert _assess(criteria, materials).nonempty_content_status == "PASS"


def test_d4_media_type_failure(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        allowed_media_types=("application/pdf",),
        material_specs=(("urn:test:one", "text/plain", b"A"),),
    )
    result = _assess(criteria, materials)
    assert result.media_type_status == "FAIL"
    assert result.declared_criteria_verdict == "FAIL"


def test_d5_media_type_unrestricted_pass(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        allowed_media_types=None,
        material_specs=(("urn:test:one", "anything/type", b"A"),),
    )
    assert _assess(criteria, materials).media_type_status == "PASS"


def test_d6_source_ref_failure(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        allowed_source_refs=("urn:test:one",),
        material_specs=(("urn:test:foreign", "application/pdf", b"A"),),
    )
    result = _assess(criteria, materials)
    assert result.source_ref_status == "FAIL"
    assert result.declared_criteria_verdict == "FAIL"


def test_d7_source_ref_unrestricted_pass(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        allowed_source_refs=None,
        material_specs=(("urn:test:any", "application/pdf", b"A"),),
    )
    assert _assess(criteria, materials).source_ref_status == "PASS"


def test_e0_semantic_requirements_block_declared_verdict(tmp_path: Path) -> None:
    requirements = ("verify authenticity", "corroborate source")
    criteria, materials = _criteria_and_materials(
        tmp_path,
        semantic_requirements=requirements,
    )
    result = _assess(criteria, materials)
    assert result.semantic_requirements_status == "BLOCKED"
    assert result.unresolved_semantic_requirements == requirements
    assert result.declared_criteria_verdict == "BLOCKED"
    assert result.request_fulfillment_status == "BLOCKED"


def test_e1_structural_fail_precedes_semantic_blocked(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        minimum_distinct_materials=2,
        semantic_requirements=("verify authenticity",),
    )
    result = _assess(criteria, materials)
    assert result.semantic_requirements_status == "BLOCKED"
    assert result.declared_criteria_verdict == "FAIL"
    assert result.request_fulfillment_status == "BLOCKED"


def test_e2_dangerous_text_is_not_executed(tmp_path: Path) -> None:
    dangerous = ("AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER",)
    criteria, materials = _criteria_and_materials(tmp_path, semantic_requirements=dangerous)
    result = _assess(criteria, materials)
    assert result.unresolved_semantic_requirements == dangerous
    assert result.semantic_requirements_status == "BLOCKED"
    assert result.request_fulfillment_status == "BLOCKED"


def test_f0_completeness_and_fulfillment_always_blocked(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    assert criteria.criteria_completeness_status == "BLOCKED"
    assert result.criteria_completeness_status == "BLOCKED"
    assert result.request_fulfillment_status == "BLOCKED"


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p112a().DeclaredEvidenceCriteriaAssessment)) == (
        "assessment_id",
        "criteria_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "material_binding_ids",
        "distinct_material_count",
        "minimum_distinct_materials_status",
        "nonempty_content_status",
        "media_type_status",
        "source_ref_status",
        "semantic_requirements_status",
        "unresolved_semantic_requirements",
        "declared_criteria_verdict",
        "criteria_completeness_status",
        "request_fulfillment_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    first = _assess(criteria, materials)
    second = _assess(criteria, materials)
    assert first == second and first is not second
    assert first.assessment_id == second.assessment_id
    assert _p112a().is_factory_attested_declared_evidence_criteria_assessment(first)
    assert _p112a().is_factory_attested_declared_evidence_criteria_assessment(second)


def test_g2_material_order_is_preserved_and_identity_bound(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(
        tmp_path,
        material_specs=(
            ("urn:test:one", "application/pdf", b"A"),
            ("urn:test:two", "application/pdf", b"B"),
        ),
    )
    first = _assess(criteria, materials)
    second = _assess(criteria, tuple(reversed(materials)))
    assert first.material_binding_ids == tuple(m.evidence_binding_id for m in materials)
    assert first.assessment_id != second.assessment_id


def test_g3_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    manual = _p112a().DeclaredEvidenceCriteriaAssessment(**asdict(result))
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(manual)
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(copy.copy(result))
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(copy.deepcopy(result))
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(
        replace(result, assessment_id=result.assessment_id)
    )


def test_g4_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    original = result.declared_criteria_verdict
    object.__setattr__(result, "declared_criteria_verdict", "MUTATED")
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(result)
    object.__setattr__(result, "declared_criteria_verdict", original)
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(result)


def test_g5_upstream_objects_can_be_collected(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    criteria_ref = weakref.ref(criteria)
    material_ref = weakref.ref(materials[0])
    del criteria
    del materials
    gc.collect()
    assert criteria_ref() is None
    assert material_ref() is None
    assert _p112a().is_factory_attested_declared_evidence_criteria_assessment(result)


def test_h0_no_promotion_parsing_io_or_execution_surface() -> None:
    module = _p112a()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "mark_admissible",
        "mark_fulfilled",
        "promote_evidence",
        "create_research_run_evidence",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "run_qualified_research",
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
        "open(",
        ".decode(",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_assessment_id_alone_is_not_authority(tmp_path: Path) -> None:
    criteria, materials = _criteria_and_materials(tmp_path)
    result = _assess(criteria, materials)
    assert not _p112a().is_factory_attested_declared_evidence_criteria_assessment(result.assessment_id)

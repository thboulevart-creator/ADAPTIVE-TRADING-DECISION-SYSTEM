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
from src.declared_evidence_criteria_assessment import (
    DeclaredEvidenceCriteriaAssessment,
    assess_declared_evidence_criteria,
    is_factory_attested_declared_evidence_criteria_assessment,
)
from src.evidence_assessment_criteria import (
    EvidenceAssessmentCriteria,
    declare_evidence_assessment_criteria,
)
from src.evidence_material_binding import BoundEvidenceMaterial, bind_evidence_material
from src.evidence_submission import submit_evidence
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P113A_CONTRACT = "P1_13A_EVIDENCE_SEMANTIC_COMPLETENESS_REVIEW_SUBMISSION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_13A_TEST_CAPTURE_AUTHORITY_V1"


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


def _request(tmp_path: Path):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which evidence review is required?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EVIDENCE",
        "Evaluate explicit evidence criteria without granting fulfillment.",
    )
    return produce_follow_up_request(revision)


def _material(request, *, source_ref: str, content: bytes):
    submission = submit_evidence(
        request,
        source_ref=source_ref,
        media_type="application/pdf",
        content=content,
    )
    return bind_evidence_material(submission, content=content)


def _case(
    tmp_path: Path,
    *,
    semantic_requirements=("verify authenticity",),
    minimum_distinct_materials=1,
    material_specs=(("urn:test:one", b"A"),),
):
    request = _request(tmp_path)
    criteria = declare_evidence_assessment_criteria(
        request,
        minimum_distinct_materials=minimum_distinct_materials,
        require_nonempty_content=True,
        allowed_media_types=("application/pdf",),
        allowed_source_refs=("urn:test:one", "urn:test:two"),
        semantic_requirements=semantic_requirements,
    )
    materials = tuple(
        _material(request, source_ref=source_ref, content=content)
        for source_ref, content in material_specs
    )
    assessment = assess_declared_evidence_criteria(criteria, materials)
    return criteria, materials, assessment


def _p113a():
    try:
        module = importlib.import_module("src.evidence_semantic_completeness_review")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.13A candidate absent — expected pre-implementation FAIL: "
            "src.evidence_semantic_completeness_review does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "SemanticRequirementReview",
        "EvidenceSemanticCompletenessReview",
        "submit_evidence_semantic_completeness_review",
        "is_factory_attested_evidence_semantic_completeness_review",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.13A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P113A_CONTRACT
    return module


def _semantic_review(requirement, material_ids, *, status="PASS", rationale="Reviewed"):
    return _p113a().SemanticRequirementReview(
        requirement=requirement,
        status=status,
        rationale=rationale,
        material_binding_ids=material_ids,
    )


def _submit(
    assessment,
    criteria,
    materials,
    *,
    semantic_reviews=None,
    reviewer_id="reviewer:test",
    method_ref="method:test",
    completeness="PASS",
    completeness_rationale="Criteria cover the declared request.",
):
    module = _p113a()
    if semantic_reviews is None:
        if (
            type(criteria) is EvidenceAssessmentCriteria
            and type(materials) is tuple
            and all(type(material) is BoundEvidenceMaterial for material in materials)
        ):
            ids = tuple(material.evidence_binding_id for material in materials)
            semantic_reviews = tuple(
                module.SemanticRequirementReview(
                    requirement=requirement,
                    status="PASS",
                    rationale="Reviewed",
                    material_binding_ids=ids,
                )
                for requirement in criteria.semantic_requirements
            )
        else:
            semantic_reviews = ()
    return module.submit_evidence_semantic_completeness_review(
        assessment,
        criteria,
        materials,
        reviewer_id=reviewer_id,
        method_ref=method_ref,
        semantic_reviews=semantic_reviews,
        reviewed_criteria_completeness_status=completeness,
        criteria_completeness_rationale=completeness_rationale,
    )


def test_a0_exact_upstream_positive(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    review = _submit(assessment, criteria, materials)
    assert review.assessment_id == assessment.assessment_id
    assert review.criteria_id == criteria.criteria_id
    assert review.material_binding_ids == assessment.material_binding_ids
    assert _p113a().is_factory_attested_evidence_semantic_completeness_review(review)


def test_a1_non_authoritative_assessment_rejected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    variants = [
        assessment.assessment_id,
        asdict(assessment),
        DeclaredEvidenceCriteriaAssessment(**asdict(assessment)),
        copy.copy(assessment),
        copy.deepcopy(assessment),
        replace(assessment, assessment_id=assessment.assessment_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _submit(value, criteria, materials)


def test_a2_non_authoritative_criteria_rejected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
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
            _submit(assessment, value, materials)


def test_a3_non_authoritative_material_rejected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
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
            _submit(assessment, criteria, (value,))


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p113a().submit_evidence_semantic_completeness_review)
    assert tuple(sig.parameters) == (
        "assessment",
        "criteria",
        "materials",
        "reviewer_id",
        "method_ref",
        "semantic_reviews",
        "reviewed_criteria_completeness_status",
        "criteria_completeness_rationale",
    )
    assert sig.parameters["assessment"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["criteria"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["materials"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in tuple(sig.parameters)[3:]:
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_c0_material_order_must_match_assessment(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(
        tmp_path,
        material_specs=(("urn:test:one", b"A"), ("urn:test:two", b"B")),
    )
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, tuple(reversed(materials)))


def test_c1_cross_case_criteria_or_materials_rejected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path / "one")
    foreign_criteria, foreign_materials, _ = _case(tmp_path / "two")
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, foreign_criteria, materials)
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, foreign_materials)


def test_d0_semantic_coverage_exact_and_ordered(tmp_path: Path) -> None:
    requirements = ("verify authenticity", "corroborate source")
    criteria, materials, assessment = _case(tmp_path, semantic_requirements=requirements)
    ids = tuple(m.evidence_binding_id for m in materials)
    reviews = tuple(_semantic_review(req, ids) for req in requirements)
    result = _submit(assessment, criteria, materials, semantic_reviews=reviews)
    assert tuple(r.requirement for r in result.semantic_reviews) == requirements


@pytest.mark.parametrize("bad_kind", ["missing", "extra", "duplicate", "reordered"])
def test_d1_bad_semantic_coverage_rejected(tmp_path: Path, bad_kind: str) -> None:
    requirements = ("verify authenticity", "corroborate source")
    criteria, materials, assessment = _case(tmp_path, semantic_requirements=requirements)
    ids = tuple(m.evidence_binding_id for m in materials)
    first = _semantic_review(requirements[0], ids)
    second = _semantic_review(requirements[1], ids)
    if bad_kind == "missing":
        reviews = (first,)
    elif bad_kind == "extra":
        reviews = (first, second, _semantic_review("extra", ids))
    elif bad_kind == "duplicate":
        reviews = (first, first)
    else:
        reviews = (second, first)
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, materials, semantic_reviews=reviews)


@pytest.mark.parametrize("status", ["PASS", "FAIL", "BLOCKED"])
def test_d2_semantic_status_domain_positive(tmp_path: Path, status: str) -> None:
    criteria, materials, assessment = _case(tmp_path)
    ids = tuple(m.evidence_binding_id for m in materials)
    review = _semantic_review(criteria.semantic_requirements[0], ids, status=status)
    result = _submit(assessment, criteria, materials, semantic_reviews=(review,))
    assert result.semantic_reviews[0].status == status


def test_d3_invalid_semantic_record_fields_rejected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    ids = tuple(m.evidence_binding_id for m in materials)
    cls = _p113a().SemanticRequirementReview
    bad = (
        cls(criteria.semantic_requirements[0], "MAYBE", "r", ids),
        cls(criteria.semantic_requirements[0], "PASS", "", ids),
        cls(criteria.semantic_requirements[0], "PASS", "r", ()),
        cls(criteria.semantic_requirements[0], "PASS", "r", ("foreign",)),
    )
    for review in bad:
        with pytest.raises((TypeError, ValueError)):
            _submit(assessment, criteria, materials, semantic_reviews=(review,))


def test_d4_no_requirements_requires_empty_reviews(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path, semantic_requirements=())
    result = _submit(assessment, criteria, materials, semantic_reviews=())
    assert result.semantic_reviews == ()
    fake = _semantic_review("extra", tuple(m.evidence_binding_id for m in materials))
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, materials, semantic_reviews=(fake,))


@pytest.mark.parametrize("status", ["PASS", "FAIL", "BLOCKED"])
def test_e0_completeness_status_domain_positive(tmp_path: Path, status: str) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials, completeness=status)
    assert result.reviewed_criteria_completeness_status == status


@pytest.mark.parametrize("bad", ["", " ", "MAYBE", 1, None])
def test_e1_invalid_completeness_status_rejected(tmp_path: Path, bad) -> None:
    criteria, materials, assessment = _case(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, materials, completeness=bad)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reviewer_id", ""),
        ("reviewer_id", " "),
        ("reviewer_id", 1),
        ("method_ref", ""),
        ("method_ref", 1),
        ("completeness_rationale", ""),
        ("completeness_rationale", 1),
    ],
)
def test_e2_exact_nonempty_text_fields(tmp_path: Path, field: str, value) -> None:
    criteria, materials, assessment = _case(tmp_path)
    kwargs = {field: value}
    with pytest.raises((TypeError, ValueError)):
        _submit(assessment, criteria, materials, **kwargs)


def test_f0_review_verdict_pass_but_authority_and_fulfillment_blocked(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials)
    assert result.review_verdict == "PASS"
    assert result.declared_criteria_completeness_status == "BLOCKED"
    assert result.review_authority_status == "BLOCKED"
    assert result.request_fulfillment_status == "BLOCKED"


def test_f1_semantic_fail_precedes_blocked(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    ids = tuple(m.evidence_binding_id for m in materials)
    semantic = _semantic_review(criteria.semantic_requirements[0], ids, status="FAIL")
    result = _submit(
        assessment,
        criteria,
        materials,
        semantic_reviews=(semantic,),
        completeness="BLOCKED",
    )
    assert result.review_verdict == "FAIL"


def test_f2_semantic_or_completeness_block_yields_blocked(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    ids = tuple(m.evidence_binding_id for m in materials)
    semantic = _semantic_review(criteria.semantic_requirements[0], ids, status="BLOCKED")
    assert _submit(
        assessment, criteria, materials, semantic_reviews=(semantic,)
    ).review_verdict == "BLOCKED"
    semantic_pass = _semantic_review(criteria.semantic_requirements[0], ids, status="PASS")
    assert _submit(
        assessment,
        criteria,
        materials,
        semantic_reviews=(semantic_pass,),
        completeness="BLOCKED",
    ).review_verdict == "BLOCKED"


def test_f3_structural_fail_is_preserved(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path, minimum_distinct_materials=2)
    result = _submit(assessment, criteria, materials)
    assert result.minimum_distinct_materials_status == "FAIL"
    assert result.review_verdict == "FAIL"


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p113a().EvidenceSemanticCompletenessReview)) == (
        "review_id",
        "assessment_id",
        "criteria_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "material_binding_ids",
        "minimum_distinct_materials_status",
        "nonempty_content_status",
        "media_type_status",
        "source_ref_status",
        "semantic_reviews",
        "reviewed_criteria_completeness_status",
        "criteria_completeness_rationale",
        "review_verdict",
        "declared_criteria_completeness_status",
        "review_authority_status",
        "request_fulfillment_status",
        "reviewer_id",
        "method_ref",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    first = _submit(assessment, criteria, materials)
    second = _submit(assessment, criteria, materials)
    assert first == second and first is not second
    assert first.review_id == second.review_id
    assert _p113a().is_factory_attested_evidence_semantic_completeness_review(first)
    assert _p113a().is_factory_attested_evidence_semantic_completeness_review(second)


def test_g2_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials)
    cls = _p113a().EvidenceSemanticCompletenessReview
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(cls(**asdict(result)))
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(copy.copy(result))
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(copy.deepcopy(result))
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(
        replace(result, review_id=result.review_id)
    )


def test_g3_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials)
    original = result.review_verdict
    object.__setattr__(result, "review_verdict", "MUTATED")
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(result)
    object.__setattr__(result, "review_verdict", original)
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(result)


def test_g4_upstream_objects_can_be_collected(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials)
    refs = (weakref.ref(criteria), weakref.ref(materials[0]), weakref.ref(assessment))
    del criteria
    del materials
    del assessment
    gc.collect()
    assert all(ref() is None for ref in refs)
    assert _p113a().is_factory_attested_evidence_semantic_completeness_review(result)


def test_h0_no_promotion_parsing_execution_or_authorization_surface() -> None:
    module = _p113a()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "mark_admissible",
        "mark_fulfilled",
        "promote_evidence",
        "create_research_run_evidence",
        "authorize",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "run_qualified_research",
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "open(",
        ".decode(",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_review_id_alone_is_not_authority(tmp_path: Path) -> None:
    criteria, materials, assessment = _case(tmp_path)
    result = _submit(assessment, criteria, materials)
    assert not _p113a().is_factory_attested_evidence_semantic_completeness_review(result.review_id)

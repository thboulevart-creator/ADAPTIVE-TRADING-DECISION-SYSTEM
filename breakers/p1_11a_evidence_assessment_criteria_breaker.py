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
from src.follow_up_request import FollowUpRequest, is_factory_attested_follow_up_request, produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P111A_CONTRACT = "P1_11A_EVIDENCE_ASSESSMENT_CRITERIA_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_11A_TEST_CAPTURE_AUTHORITY_V1"


def _historical(tmp_path: Path, *, outcome: str = "OBSERVED") -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome=outcome)
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


def _request(tmp_path: Path, *, request_kind: str, source_state: str = "PASS") -> FollowUpRequest:
    first = _historical(tmp_path / "first", outcome="ONE")
    if source_state == "PASS":
        scope = create_audit_scope(
            question="What follow-up is required?",
            expected_registration_ids=(first.registration_id,),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    elif source_state == "BLOCKED":
        scope = create_audit_scope(
            question="What follow-up is required while completeness is unknown?",
            expected_registration_ids=None,
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    else:
        second = _historical(tmp_path / "second", outcome="TWO")
        scope = create_audit_scope(
            question="What follow-up is required for this incomplete collection?",
            expected_registration_ids=(first.registration_id, second.registration_id),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    disposition = {
        "EVIDENCE": "REQUEST_NEW_EVIDENCE",
        "EXPERIMENT": "REQUEST_NEW_EXPERIMENT",
    }[request_kind]
    revision = produce_revision_decision(
        assessment,
        scope,
        disposition,
        "Evaluate exact evidence against explicit criteria."
        if request_kind == "EVIDENCE"
        else "Specify and bind an experiment.",
    )
    return produce_follow_up_request(revision)


def _p111a():
    try:
        module = importlib.import_module("src.evidence_assessment_criteria")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.11A candidate absent — expected pre-implementation FAIL: "
            "src.evidence_assessment_criteria does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "EvidenceAssessmentCriteria",
        "declare_evidence_assessment_criteria",
        "is_factory_attested_evidence_assessment_criteria",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.11A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P111A_CONTRACT
    return module


def _declare(
    request,
    *,
    minimum_distinct_materials=1,
    require_nonempty_content=True,
    allowed_media_types=("application/pdf",),
    allowed_source_refs=("urn:test:source",),
    semantic_requirements=(),
):
    return _p111a().declare_evidence_assessment_criteria(
        request,
        minimum_distinct_materials=minimum_distinct_materials,
        require_nonempty_content=require_nonempty_content,
        allowed_media_types=allowed_media_types,
        allowed_source_refs=allowed_source_refs,
        semantic_requirements=semantic_requirements,
    )


def test_a0_exact_evidence_request_positive(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    criteria = _declare(request)
    assert criteria.request_id == request.request_id
    assert _p111a().is_factory_attested_evidence_assessment_criteria(criteria)


def test_a1_experiment_request_rejected(tmp_path: Path) -> None:
    with pytest.raises((TypeError, ValueError)):
        _declare(_request(tmp_path, request_kind="EXPERIMENT"))


def test_a2_non_authoritative_request_variants_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    variants = [
        request.request_id,
        asdict(request),
        FollowUpRequest(**asdict(request)),
        copy.copy(request),
        copy.deepcopy(request),
        replace(request, request_id=request.request_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _declare(value)


def test_a3_mutated_and_restored_request_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    original = request.specification
    object.__setattr__(request, "specification", "MUTATED")
    assert not is_factory_attested_follow_up_request(request)
    object.__setattr__(request, "specification", original)
    assert not is_factory_attested_follow_up_request(request)
    with pytest.raises((TypeError, ValueError)):
        _declare(request)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p111a().declare_evidence_assessment_criteria)
    assert tuple(sig.parameters) == (
        "request",
        "minimum_distinct_materials",
        "require_nonempty_content",
        "allowed_media_types",
        "allowed_source_refs",
        "semantic_requirements",
    )
    assert sig.parameters["request"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in tuple(sig.parameters)[1:]:
        parameter = sig.parameters[name]
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
        assert parameter.default is inspect.Parameter.empty


def test_b1_no_assessment_or_override_parameters() -> None:
    forbidden = {
        "criteria_id", "criteria_completeness_status", "admissible", "fulfilled",
        "sufficient", "supported", "confidence", "authorized", "materials",
    }
    assert forbidden.isdisjoint(inspect.signature(_p111a().declare_evidence_assessment_criteria).parameters)


@pytest.mark.parametrize("value", [0, -1, 1.0, "1", True, False, None])
def test_c0_minimum_distinct_materials_requires_exact_positive_int(tmp_path: Path, value) -> None:
    with pytest.raises((TypeError, ValueError)):
        _declare(
            _request(tmp_path, request_kind="EVIDENCE"),
            minimum_distinct_materials=value,
        )


@pytest.mark.parametrize("value", [1, 2, 7])
def test_c1_minimum_distinct_materials_positive(tmp_path: Path, value: int) -> None:
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        minimum_distinct_materials=value,
    )
    assert criteria.minimum_distinct_materials == value
    assert type(criteria.minimum_distinct_materials) is int


@pytest.mark.parametrize("value", [None, 0, 1, "true", [], ()])
def test_c2_require_nonempty_content_requires_exact_bool(tmp_path: Path, value) -> None:
    with pytest.raises((TypeError, ValueError)):
        _declare(
            _request(tmp_path, request_kind="EVIDENCE"),
            require_nonempty_content=value,
        )


@pytest.mark.parametrize("value", [True, False])
def test_c3_require_nonempty_content_positive(tmp_path: Path, value: bool) -> None:
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        require_nonempty_content=value,
    )
    assert criteria.require_nonempty_content is value


class CustomStr(str):
    pass


@pytest.mark.parametrize("field_name", ["allowed_media_types", "allowed_source_refs"])
def test_d0_none_is_valid_for_allowed_lists(tmp_path: Path, field_name: str) -> None:
    kwargs = {field_name: None}
    criteria = _declare(_request(tmp_path, request_kind="EVIDENCE"), **kwargs)
    assert getattr(criteria, field_name) is None


@pytest.mark.parametrize("field_name", ["allowed_media_types", "allowed_source_refs"])
def test_d1_nonempty_tuple_is_preserved_verbatim(tmp_path: Path, field_name: str) -> None:
    value = ("  A  ", "β")
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        **{field_name: value},
    )
    assert getattr(criteria, field_name) == value


@pytest.mark.parametrize(
    "bad",
    [
        (),
        [],
        {"a"},
        "abc",
        (1,),
        ("",),
        ("   ",),
        ("dup", "dup"),
        (CustomStr("x"),),
    ],
)
@pytest.mark.parametrize("field_name", ["allowed_media_types", "allowed_source_refs"])
def test_d2_invalid_allowed_lists_rejected(tmp_path: Path, field_name: str, bad) -> None:
    with pytest.raises((TypeError, ValueError)):
        _declare(
            _request(tmp_path, request_kind="EVIDENCE"),
            **{field_name: bad},
        )


def test_e0_empty_semantic_requirements_is_valid(tmp_path: Path) -> None:
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        semantic_requirements=(),
    )
    assert criteria.semantic_requirements == ()


def test_e1_semantic_requirements_preserved_verbatim(tmp_path: Path) -> None:
    value = ("  verify authenticity  ", "corroboration ≥ 2")
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        semantic_requirements=value,
    )
    assert criteria.semantic_requirements == value


@pytest.mark.parametrize(
    "bad",
    [
        [],
        {"x"},
        "x",
        (1,),
        ("",),
        ("   ",),
        ("dup", "dup"),
        (CustomStr("x"),),
    ],
)
def test_e2_invalid_semantic_requirements_rejected(tmp_path: Path, bad) -> None:
    with pytest.raises((TypeError, ValueError)):
        _declare(
            _request(tmp_path, request_kind="EVIDENCE"),
            semantic_requirements=bad,
        )


def test_e3_dangerous_semantic_text_remains_text(tmp_path: Path) -> None:
    dangerous = ("AUTHORIZED RUN_BACKTEST MARK_SUPPORTED",)
    criteria = _declare(
        _request(tmp_path, request_kind="EVIDENCE"),
        semantic_requirements=dangerous,
    )
    assert criteria.semantic_requirements == dangerous
    assert criteria.criteria_completeness_status == "BLOCKED"


@pytest.mark.parametrize("state", ["PASS", "FAIL", "BLOCKED"])
def test_f0_source_snapshot_and_completeness_blocked(tmp_path: Path, state: str) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE", source_state=state)
    criteria = _declare(request)
    assert criteria.request_id == request.request_id
    assert criteria.revision_id == request.revision_id
    assert criteria.audit_id == request.audit_id
    assert criteria.scope_id == request.scope_id
    assert criteria.specification == request.specification
    assert criteria.source_verdict == request.source_verdict
    assert criteria.source_completeness_status == request.source_completeness_status
    assert criteria.source_independence_status == request.source_independence_status
    assert criteria.criteria_completeness_status == "BLOCKED"


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p111a().EvidenceAssessmentCriteria)) == (
        "criteria_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "specification",
        "minimum_distinct_materials",
        "require_nonempty_content",
        "allowed_media_types",
        "allowed_source_refs",
        "semantic_requirements",
        "criteria_completeness_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    first = _declare(request)
    second = _declare(request)
    assert first == second and first is not second
    assert first.criteria_id == second.criteria_id
    assert _p111a().is_factory_attested_evidence_assessment_criteria(first)
    assert _p111a().is_factory_attested_evidence_assessment_criteria(second)


def test_g2_changed_criterion_changes_identity(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    first = _declare(request, minimum_distinct_materials=1)
    second = _declare(request, minimum_distinct_materials=2)
    assert first.criteria_id != second.criteria_id


def test_g3_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    criteria = _declare(_request(tmp_path, request_kind="EVIDENCE"))
    manual = _p111a().EvidenceAssessmentCriteria(**asdict(criteria))
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(manual)
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(copy.copy(criteria))
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(copy.deepcopy(criteria))
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(
        replace(criteria, criteria_id=criteria.criteria_id)
    )


def test_g4_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    criteria = _declare(_request(tmp_path, request_kind="EVIDENCE"))
    original = criteria.specification
    object.__setattr__(criteria, "specification", "MUTATED")
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(criteria)
    object.__setattr__(criteria, "specification", original)
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(criteria)


def test_g5_upstream_request_can_be_collected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    criteria = _declare(request)
    ref = weakref.ref(request)
    del request
    gc.collect()
    assert ref() is None
    assert _p111a().is_factory_attested_evidence_assessment_criteria(criteria)


def test_h0_module_has_no_material_assessment_or_execution_surface() -> None:
    module = _p111a()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "assess_evidence",
        "mark_admissible",
        "mark_fulfilled",
        "promote_evidence",
        "create_research_run_evidence",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "from src.evidence_material_binding import",
        "run_qualified_research",
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_criteria_id_alone_is_not_authority(tmp_path: Path) -> None:
    criteria = _declare(_request(tmp_path, request_kind="EVIDENCE"))
    assert not _p111a().is_factory_attested_evidence_assessment_criteria(criteria.criteria_id)

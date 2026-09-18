from __future__ import annotations

import copy
import gc
import hashlib
import importlib
import inspect
import weakref
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.evidence_submission import EvidenceSubmission, is_factory_attested_evidence_submission, submit_evidence
from src.experiment_specification import specify_experiment
from src.follow_up_request import FollowUpRequest, produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.research_findings import ResearchFindings
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P110A_CONTRACT = "P1_10A_EVIDENCE_MATERIAL_BINDING_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_10A_TEST_CAPTURE_AUTHORITY_V1"


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
        "Bind exact external material." if request_kind == "EVIDENCE" else "Specify controlled experiment.",
    )
    return produce_follow_up_request(revision)


def _submission(tmp_path: Path, *, content: bytes = b"abc", source_state: str = "PASS") -> EvidenceSubmission:
    return submit_evidence(
        _request(tmp_path, request_kind="EVIDENCE", source_state=source_state),
        source_ref="urn:test:evidence",
        media_type="application/octet-stream",
        content=content,
    )


def _p110a():
    try:
        module = importlib.import_module("src.evidence_material_binding")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.10A candidate absent — expected pre-implementation FAIL: "
            "src.evidence_material_binding does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "BoundEvidenceMaterial",
        "bind_evidence_material",
        "is_factory_attested_bound_evidence_material",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.10A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P110A_CONTRACT
    return module


def _bind(submission, *, content=b"abc"):
    return _p110a().bind_evidence_material(submission, content=content)


def test_a0_exact_submission_positive(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"abc")
    binding = _bind(submission, content=b"abc")
    assert binding.submission_id == submission.submission_id
    assert _p110a().is_factory_attested_bound_evidence_material(binding)


def test_a1_non_authoritative_submission_variants_rejected(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"abc")
    variants = [
        submission.submission_id,
        asdict(submission),
        EvidenceSubmission(**asdict(submission)),
        copy.copy(submission),
        copy.deepcopy(submission),
        replace(submission, submission_id=submission.submission_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _bind(value, content=b"abc")


def test_a2_mutated_and_restored_submission_rejected(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"abc")
    original = submission.source_ref
    object.__setattr__(submission, "source_ref", "MUTATED")
    assert not is_factory_attested_evidence_submission(submission)
    object.__setattr__(submission, "source_ref", original)
    assert not is_factory_attested_evidence_submission(submission)
    with pytest.raises((TypeError, ValueError)):
        _bind(submission, content=b"abc")


def test_a3_experiment_specification_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    spec = specify_experiment(
        request,
        hypothesis_statement="H",
        prediction="P",
        falsification_rule="F",
        protocol="Protocol",
        measurement_plan="Measure",
    )
    with pytest.raises((TypeError, ValueError)):
        _bind(spec, content=b"abc")


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p110a().bind_evidence_material)
    assert tuple(sig.parameters) == ("submission", "content")
    assert sig.parameters["submission"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["content"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["content"].default is inspect.Parameter.empty


class CustomBytes(bytes):
    pass


@pytest.mark.parametrize("value", [None, "abc", bytearray(b"abc"), memoryview(b"abc"), CustomBytes(b"abc")])
def test_b1_content_requires_exact_bytes(tmp_path: Path, value) -> None:
    with pytest.raises((TypeError, ValueError)):
        _bind(_submission(tmp_path, content=b"abc"), content=value)


def test_b2_no_override_parameters() -> None:
    forbidden = {
        "source_ref", "media_type", "content_sha256", "content_size",
        "fulfilled", "admissible", "sufficient", "supported", "confidence", "authorized",
    }
    assert forbidden.isdisjoint(inspect.signature(_p110a().bind_evidence_material).parameters)


def test_c0_zero_byte_content_rebinds_exactly(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"")
    binding = _bind(submission, content=b"")
    assert binding.content == b""
    assert binding.content_size == 0
    assert binding.content_sha256 == hashlib.sha256(b"").hexdigest()


def test_c1_mismatched_content_is_rejected(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"expected")
    with pytest.raises((TypeError, ValueError)):
        _bind(submission, content=b"different")


def test_c2_exact_content_is_preserved(tmp_path: Path) -> None:
    content = b"\x00exact-evidence\xff"
    binding = _bind(_submission(tmp_path, content=content), content=content)
    assert binding.content == content
    assert type(binding.content) is bytes


@pytest.mark.parametrize("state", ["PASS", "FAIL", "BLOCKED"])
def test_d0_snapshots_are_preserved(tmp_path: Path, state: str) -> None:
    submission = _submission(tmp_path, content=b"abc", source_state=state)
    binding = _bind(submission, content=b"abc")
    for name in (
        "submission_id", "request_id", "revision_id", "audit_id", "scope_id",
        "source_ref", "media_type", "content_sha256", "content_size",
        "source_verdict", "source_completeness_status", "source_independence_status",
    ):
        assert getattr(binding, name) == getattr(submission, name)


def test_d1_blocked_stays_blocked(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path, content=b"x", source_state="BLOCKED"), content=b"x")
    assert binding.source_verdict == "BLOCKED"
    assert binding.source_completeness_status == "BLOCKED"
    assert binding.source_independence_status == "BLOCKED"


def test_e0_no_epistemic_or_fulfillment_fields(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path), content=b"abc")
    forbidden = (
        "admissible", "fulfilled", "sufficient", "supported", "refuted",
        "confidence", "evidence_id", "research_run_id", "authorized",
    )
    assert all(not hasattr(binding, name) for name in forbidden)
    assert not isinstance(binding, ResearchRunEvidence)
    assert not isinstance(binding, ResearchFindings)


def test_f0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p110a().BoundEvidenceMaterial)) == (
        "evidence_binding_id", "submission_id", "request_id", "revision_id", "audit_id", "scope_id",
        "source_ref", "media_type", "content_sha256", "content_size", "content",
        "source_verdict", "source_completeness_status", "source_independence_status",
    )


def test_f1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"same")
    first = _bind(submission, content=b"same")
    second = _bind(submission, content=b"same")
    assert first == second and first is not second
    assert first.evidence_binding_id == second.evidence_binding_id
    assert _p110a().is_factory_attested_bound_evidence_material(first)
    assert _p110a().is_factory_attested_bound_evidence_material(second)


def test_f2_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path), content=b"abc")
    manual = _p110a().BoundEvidenceMaterial(**asdict(binding))
    assert not _p110a().is_factory_attested_bound_evidence_material(manual)
    assert not _p110a().is_factory_attested_bound_evidence_material(copy.copy(binding))
    assert not _p110a().is_factory_attested_bound_evidence_material(copy.deepcopy(binding))
    assert not _p110a().is_factory_attested_bound_evidence_material(
        replace(binding, evidence_binding_id=binding.evidence_binding_id)
    )


def test_f3_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path), content=b"abc")
    original = binding.source_ref
    object.__setattr__(binding, "source_ref", "MUTATED")
    assert not _p110a().is_factory_attested_bound_evidence_material(binding)
    object.__setattr__(binding, "source_ref", original)
    assert not _p110a().is_factory_attested_bound_evidence_material(binding)


def test_g0_submission_can_be_collected_after_binding(tmp_path: Path) -> None:
    submission = _submission(tmp_path, content=b"abc")
    binding = _bind(submission, content=b"abc")
    ref = weakref.ref(submission)
    del submission
    gc.collect()
    assert ref() is None
    assert _p110a().is_factory_attested_bound_evidence_material(binding)


def test_g1_binding_id_alone_is_not_authority(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path), content=b"abc")
    assert not _p110a().is_factory_attested_bound_evidence_material(binding.evidence_binding_id)


def test_h0_runtime_has_no_external_acquisition_or_execution_surface() -> None:
    source = inspect.getsource(_p110a())
    forbidden = (
        "requests.", "socket.", "subprocess.", "run_qualified_research",
        "bind_execution_input", "order_send", "MetaTrader5", "run_backtest(", "activate_live(",
    )
    assert all(token not in source for token in forbidden)


def test_h1_binding_does_not_mutate_submission(tmp_path: Path) -> None:
    submission = _submission(tmp_path)
    snapshot = asdict(submission)
    _bind(submission, content=b"abc")
    assert asdict(submission) == snapshot
    assert is_factory_attested_evidence_submission(submission)


def test_h2_binding_cannot_substitute_for_submission(tmp_path: Path) -> None:
    binding = _bind(_submission(tmp_path), content=b"abc")
    with pytest.raises((TypeError, ValueError)):
        _bind(binding, content=b"abc")

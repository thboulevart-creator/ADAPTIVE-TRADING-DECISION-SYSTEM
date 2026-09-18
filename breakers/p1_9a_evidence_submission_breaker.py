from __future__ import annotations

import copy
import gc
import hashlib
import importlib
import inspect
import unicodedata
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
from src.research.execution import QualifiedResearchInput, ResearchExecutionResult
from src.research_findings import ResearchFindings, ResearchMeasurement
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P19A_CONTRACT = "P1_9A_EVIDENCE_SUBMISSION_BOUNDARY_V1"

P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_9_TEST_CAPTURE_AUTHORITY_V1"


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


def _request(
    tmp_path: Path,
    *,
    request_kind: str,
    source_state: str = "PASS",
    detail: str | None = None,
) -> FollowUpRequest:
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
    elif source_state == "FAIL":
        second = _historical(tmp_path / "second", outcome="TWO")
        scope = create_audit_scope(
            question="What follow-up is required for this incomplete bounded collection?",
            expected_registration_ids=(first.registration_id, second.registration_id),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    else:
        raise AssertionError(source_state)

    disposition = {
        "EVIDENCE": "REQUEST_NEW_EVIDENCE",
        "EXPERIMENT": "REQUEST_NEW_EXPERIMENT",
    }[request_kind]
    if detail is None:
        detail = (
            "Request exact external evidence."
            if request_kind == "EVIDENCE"
            else "Specify a controlled follow-up experiment."
        )
    revision = produce_revision_decision(assessment, scope, disposition, detail)
    request = produce_follow_up_request(revision)
    assert request.request_kind == request_kind
    assert is_factory_attested_follow_up_request(request)
    return request


def _p19a():
    try:
        module = importlib.import_module("src.evidence_submission")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.9A candidate absent — expected pre-implementation FAIL: "
            "src.evidence_submission does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = ("EvidenceSubmission", "submit_evidence", "is_factory_attested_evidence_submission")
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.9A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P19A_CONTRACT
    return module


def _submit(request, *, source_ref="urn:test:evidence", media_type="application/octet-stream", content=b"abc"):
    return _p19a().submit_evidence(
        request,
        source_ref=source_ref,
        media_type=media_type,
        content=content,
    )


# A — exact EVIDENCE request only.


def test_a0_exact_evidence_request_positive(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    submission = _submit(request)
    assert submission.request_id == request.request_id
    assert _p19a().is_factory_attested_evidence_submission(submission)


def test_a1_experiment_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    with pytest.raises((TypeError, ValueError)):
        _submit(request)


def test_a2_request_id_alone_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _submit(request.request_id)


def test_a3_dict_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _submit(asdict(request))


def test_a4_manual_same_valued_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    manual = FollowUpRequest(**asdict(request))
    assert manual == request and manual is not request
    with pytest.raises((TypeError, ValueError)):
        _submit(manual)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a5_copy_or_deepcopy_request_is_rejected(tmp_path: Path, copier) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    copied = copier(request)
    assert copied == request and copied is not request
    with pytest.raises((TypeError, ValueError)):
        _submit(copied)


def test_a6_replace_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    copied = replace(request, request_id=request.request_id)
    with pytest.raises((TypeError, ValueError)):
        _submit(copied)


def test_a7_mutated_and_restored_request_remains_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    original = request.specification
    object.__setattr__(request, "specification", "MUTATED")
    assert not is_factory_attested_follow_up_request(request)
    object.__setattr__(request, "specification", original)
    assert not is_factory_attested_follow_up_request(request)
    with pytest.raises((TypeError, ValueError)):
        _submit(request)


# B — exact signature and input types.


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p19a().submit_evidence)
    assert tuple(sig.parameters) == ("request", "source_ref", "media_type", "content")
    assert sig.parameters["request"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("source_ref", "media_type", "content"):
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


class CustomStr(str):
    pass


class CustomBytes(bytes):
    pass


@pytest.mark.parametrize("value", [None, 1, b"x", CustomStr("ref")])
def test_b1_source_ref_requires_exact_str(tmp_path: Path, value) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _submit(request, source_ref=value)


@pytest.mark.parametrize("value", [None, 1, b"x", CustomStr("application/test")])
def test_b2_media_type_requires_exact_str(tmp_path: Path, value) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _submit(request, media_type=value)


@pytest.mark.parametrize("value", [None, "abc", bytearray(b"abc"), memoryview(b"abc"), CustomBytes(b"abc")])
def test_b3_content_requires_exact_bytes(tmp_path: Path, value) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _submit(request, content=value)


def test_b4_no_hash_size_or_epistemic_override_parameters() -> None:
    sig = inspect.signature(_p19a().submit_evidence)
    forbidden = {
        "submission_id", "content_sha256", "content_size", "fulfilled",
        "admissible", "sufficient", "supported", "confidence", "authorized",
    }
    assert forbidden.isdisjoint(sig.parameters)


# C — empty bytes are valid explicit submission; hash/size are derived.


def test_c0_empty_bytes_are_accepted_and_derived_exactly(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    submission = _submit(request, content=b"")
    assert submission.content_size == 0
    assert submission.content_sha256 == hashlib.sha256(b"").hexdigest()


def test_c1_nonempty_bytes_hash_and_size_are_exact(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    content = b"\x00evidence\xff"
    submission = _submit(request, content=content)
    assert submission.content_size == len(content)
    assert submission.content_sha256 == hashlib.sha256(content).hexdigest()


def test_c2_different_bytes_change_submission_identity(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    first = _submit(request, content=b"A")
    second = _submit(request, content=b"B")
    assert first.content_sha256 != second.content_sha256
    assert first.submission_id != second.submission_id


# D — metadata is nonempty exact text, preserved verbatim.


@pytest.mark.parametrize("name", ["source_ref", "media_type"])
@pytest.mark.parametrize("value", ["", " ", "\t", "\n  "])
def test_d0_empty_or_whitespace_metadata_is_rejected(tmp_path: Path, name: str, value: str) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    kwargs = {"source_ref": "ref", "media_type": "type", "content": b"x"}
    kwargs[name] = value
    with pytest.raises((TypeError, ValueError)):
        _p19a().submit_evidence(request, **kwargs)


def test_d1_metadata_is_preserved_verbatim(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    source_ref = "  urn:Évidence:1  "
    media_type = "  application/X-Test  "
    submission = _submit(request, source_ref=source_ref, media_type=media_type)
    assert submission.source_ref == source_ref
    assert submission.media_type == media_type


def test_d2_unicode_equivalent_metadata_is_not_normalized(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    composed = "café"
    decomposed = unicodedata.normalize("NFD", composed)
    first = _submit(request, source_ref=composed)
    second = _submit(request, source_ref=decomposed)
    assert first.source_ref != second.source_ref
    assert first.submission_id != second.submission_id


# E — upstream IDs/statuses are exact snapshots and BLOCKED remains visible.


@pytest.mark.parametrize("state", ["PASS", "FAIL", "BLOCKED"])
def test_e0_ids_and_source_statuses_are_preserved(tmp_path: Path, state: str) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE", source_state=state)
    submission = _submit(request)
    assert submission.request_id == request.request_id
    assert submission.revision_id == request.revision_id
    assert submission.audit_id == request.audit_id
    assert submission.scope_id == request.scope_id
    assert submission.source_verdict == request.source_verdict
    assert submission.source_completeness_status == request.source_completeness_status
    assert submission.source_independence_status == request.source_independence_status


def test_e1_blocked_stays_blocked(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE", source_state="BLOCKED")
    submission = _submit(request, content=b"new material")
    assert submission.source_verdict == "BLOCKED"
    assert submission.source_completeness_status == "BLOCKED"
    assert submission.source_independence_status == "BLOCKED"


# F — submission is not fulfillment/admissibility/evidence promotion.


def test_f0_output_has_no_epistemic_or_fulfillment_fields(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    forbidden = (
        "fulfilled", "admissible", "sufficient", "supported", "refuted",
        "confidence", "evidence_id", "research_run_id", "authorized",
    )
    assert all(not hasattr(submission, name) for name in forbidden)


def test_f1_submission_is_not_research_evidence_or_findings(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    assert not isinstance(submission, ResearchRunEvidence)
    assert not isinstance(submission, ResearchFindings)


def test_f2_multiple_submissions_do_not_create_collection_fulfillment(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    first = _submit(request, content=b"A")
    second = _submit(request, content=b"B")
    assert not hasattr(first, "fulfilled")
    assert not hasattr(second, "fulfilled")
    assert first.submission_id != second.submission_id


# G — exact output model, deterministic identity and sticky attestation.


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p19a().EvidenceSubmission)) == (
        "submission_id", "request_id", "revision_id", "audit_id", "scope_id",
        "source_ref", "media_type", "content_sha256", "content_size",
        "source_verdict", "source_completeness_status", "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    first = _submit(request, content=b"same")
    second = _submit(request, content=b"same")
    assert first == second
    assert first is not second
    assert first.submission_id == second.submission_id
    assert _p19a().is_factory_attested_evidence_submission(first)
    assert _p19a().is_factory_attested_evidence_submission(second)


def test_g2_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    manual = _p19a().EvidenceSubmission(**asdict(submission))
    assert not _p19a().is_factory_attested_evidence_submission(manual)
    assert not _p19a().is_factory_attested_evidence_submission(copy.copy(submission))
    assert not _p19a().is_factory_attested_evidence_submission(copy.deepcopy(submission))
    assert not _p19a().is_factory_attested_evidence_submission(
        replace(submission, submission_id=submission.submission_id)
    )


def test_g3_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    original = submission.source_ref
    object.__setattr__(submission, "source_ref", "MUTATED")
    assert not _p19a().is_factory_attested_evidence_submission(submission)
    object.__setattr__(submission, "source_ref", original)
    assert not _p19a().is_factory_attested_evidence_submission(submission)


def test_g4_request_can_be_collected_after_submission(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    request_id = request.request_id
    submission = _submit(request)
    ref = weakref.ref(request)
    del request
    gc.collect()
    assert ref() is None
    assert submission.request_id == request_id
    assert _p19a().is_factory_attested_evidence_submission(submission)


def test_g5_submission_id_alone_is_not_authority(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    assert not _p19a().is_factory_attested_evidence_submission(submission.submission_id)


# H — no IO/execution/reverse authority.


def test_h0_runtime_has_no_external_io_or_execution_surface() -> None:
    source = inspect.getsource(_p19a())
    forbidden = (
        "open(", "Path(", "requests.", "socket.", "subprocess.",
        "run_qualified_research", "bind_execution_input", "order_send",
        "MetaTrader5", "run_backtest(", "activate_live(",
    )
    assert all(token not in source for token in forbidden)


def test_h1_submission_does_not_mutate_request(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    snapshot = asdict(request)
    _submit(request)
    assert asdict(request) == snapshot
    assert is_factory_attested_follow_up_request(request)


def test_h2_submission_cannot_substitute_for_request(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    with pytest.raises((TypeError, ValueError)):
        _submit(submission)


def test_h3_submission_is_not_executable_input_or_result(tmp_path: Path) -> None:
    submission = _submit(_request(tmp_path, request_kind="EVIDENCE"))
    assert not isinstance(submission, QualifiedResearchInput)
    assert not isinstance(submission, ResearchExecutionResult)

from __future__ import annotations

import copy
import gc
import importlib
import inspect
import json
import weakref
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.evidence_submission import submit_evidence
from src.experiment_specification import ExperimentSpecification, is_factory_attested_experiment_specification, specify_experiment
from src.follow_up_request import FollowUpRequest, produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.research.execution import QualifiedResearchInput, ResearchExecutionResult
from src.research.input_binding import (
    BoundResearchInput,
    bind_execution_input,
    corpus_inventory_hash,
    is_bound_research_input,
    sha256_file,
)
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P110B_CONTRACT = "P1_10B_EXPERIMENT_EXECUTION_BINDING_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_10B_TEST_CAPTURE_AUTHORITY_V1"


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


def _specification(
    tmp_path: Path,
    *,
    source_state: str = "PASS",
    protocol: str = "Protocol",
) -> ExperimentSpecification:
    return specify_experiment(
        _request(tmp_path, request_kind="EXPERIMENT", source_state=source_state),
        hypothesis_statement="H",
        prediction="P",
        falsification_rule="F",
        protocol=protocol,
        measurement_plan="Measure",
    )


def _bound_input(root: Path, *, payload: bytes = b"synthetic-corpus") -> BoundResearchInput:
    corpus = root / "corpus"
    corpus.mkdir(parents=True)
    (corpus / "sample.bi5").write_bytes(payload)
    contract_path = root / "contract.json"
    contract_path.write_text(
        json.dumps(
            {
                "asset_id": "USATECHIDXUSD",
                "source": "synthetic",
                "format": "BI5",
                "record_size": 20,
                "record_struct": ">IIIff",
                "timestamp_unit": "milliseconds",
                "price_scale": 1000,
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return bind_execution_input(
        corpus,
        contract_path,
        corpus_inventory_hash(corpus),
        sha256_file(contract_path),
    )


def _p110b():
    try:
        module = importlib.import_module("src.experiment_execution_binding")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.10B candidate absent — expected pre-implementation FAIL: "
            "src.experiment_execution_binding does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "ExperimentExecutionBinding",
        "bind_experiment_execution",
        "is_factory_attested_experiment_execution_binding",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.10B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P110B_CONTRACT
    return module


def _bind(specification, bound_input):
    return _p110b().bind_experiment_execution(specification, bound_input)


def test_a0_exact_specification_positive(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    binding = _bind(spec, bound)
    assert binding.experiment_spec_id == spec.experiment_spec_id
    assert _p110b().is_factory_attested_experiment_execution_binding(binding)


def test_a1_non_authoritative_specification_variants_rejected(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    variants = [
        spec.experiment_spec_id,
        asdict(spec),
        ExperimentSpecification(**asdict(spec)),
        copy.copy(spec),
        copy.deepcopy(spec),
        replace(spec, experiment_spec_id=spec.experiment_spec_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _bind(value, bound)


def test_a2_mutated_and_restored_specification_rejected(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    original = spec.protocol
    object.__setattr__(spec, "protocol", "MUTATED")
    assert not is_factory_attested_experiment_specification(spec)
    object.__setattr__(spec, "protocol", original)
    assert not is_factory_attested_experiment_specification(spec)
    with pytest.raises((TypeError, ValueError)):
        _bind(spec, bound)


def test_a3_evidence_submission_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path / "request", request_kind="EVIDENCE")
    submission = submit_evidence(
        request,
        source_ref="urn:test:evidence",
        media_type="application/octet-stream",
        content=b"x",
    )
    with pytest.raises((TypeError, ValueError)):
        _bind(submission, _bound_input(tmp_path / "input"))


def test_b0_exact_factory_bound_input_positive(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    assert is_bound_research_input(bound)
    binding = _bind(_specification(tmp_path / "spec"), bound)
    assert binding.expected_corpus_hash == bound.expected_corpus_hash


def test_b1_qualified_research_input_is_rejected(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    qualified = QualifiedResearchInput(
        corpus_root=bound.corpus_root,
        contract_path=bound.contract_path,
        expected_corpus_hash=bound.expected_corpus_hash,
        expected_contract_hash=bound.expected_contract_hash,
    )
    with pytest.raises((TypeError, ValueError)):
        _bind(_specification(tmp_path / "spec"), qualified)


def test_b2_manual_copy_replace_bound_inputs_are_rejected(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    manual = BoundResearchInput(
        corpus_root=bound.corpus_root,
        contract_path=bound.contract_path,
        contract=dict(bound.contract),
        expected_corpus_hash=bound.expected_corpus_hash,
        expected_contract_hash=bound.expected_contract_hash,
    )
    variants = [
        manual,
        copy.copy(bound),
        copy.deepcopy(bound),
        replace(bound, expected_corpus_hash=bound.expected_corpus_hash),
    ]
    spec = _specification(tmp_path / "spec")
    for value in variants:
        assert not is_bound_research_input(value, revalidate_sources=False)
        with pytest.raises((TypeError, ValueError)):
            _bind(spec, value)


def test_b3_mutated_bound_input_is_rejected(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    object.__setattr__(bound, "expected_corpus_hash", "0" * 64)
    assert not is_bound_research_input(bound, revalidate_sources=False)
    with pytest.raises((TypeError, ValueError)):
        _bind(_specification(tmp_path / "spec"), bound)


def test_b4_changed_sources_after_binding_are_rejected(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    (bound.corpus_root / "sample.bi5").write_bytes(b"changed")
    assert not is_bound_research_input(bound)
    with pytest.raises((TypeError, ValueError)):
        _bind(_specification(tmp_path / "spec"), bound)


def test_c0_signature_is_exact() -> None:
    sig = inspect.signature(_p110b().bind_experiment_execution)
    assert tuple(sig.parameters) == ("specification", "bound_input")
    assert all(
        parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        and parameter.default is inspect.Parameter.empty
        for parameter in sig.parameters.values()
    )


def test_c1_paths_are_resolved_and_hashes_preserved(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    binding = _bind(_specification(tmp_path / "spec"), bound)
    assert binding.corpus_root == str(bound.corpus_root.resolve())
    assert binding.contract_path == str(bound.contract_path.resolve())
    assert binding.expected_corpus_hash == bound.expected_corpus_hash
    assert binding.expected_contract_hash == bound.expected_contract_hash


@pytest.mark.parametrize("state", ["PASS", "FAIL", "BLOCKED"])
def test_d0_specification_snapshot_is_preserved(tmp_path: Path, state: str) -> None:
    spec = _specification(tmp_path / "spec", source_state=state)
    binding = _bind(spec, _bound_input(tmp_path / "input"))
    for name in (
        "experiment_spec_id", "request_id", "revision_id", "audit_id", "scope_id",
        "objective", "hypothesis_statement", "prediction", "falsification_rule",
        "protocol", "measurement_plan", "source_verdict",
        "source_completeness_status", "source_independence_status",
    ):
        assert getattr(binding, name) == getattr(spec, name)


def test_d1_blocked_stays_blocked(tmp_path: Path) -> None:
    binding = _bind(
        _specification(tmp_path / "spec", source_state="BLOCKED"),
        _bound_input(tmp_path / "input"),
    )
    assert binding.source_verdict == "BLOCKED"
    assert binding.source_completeness_status == "BLOCKED"
    assert binding.source_independence_status == "BLOCKED"


def test_e0_binding_is_not_execution_input_result_or_evidence(tmp_path: Path) -> None:
    binding = _bind(_specification(tmp_path / "spec"), _bound_input(tmp_path / "input"))
    assert not isinstance(binding, QualifiedResearchInput)
    assert not isinstance(binding, ResearchExecutionResult)
    assert not isinstance(binding, ResearchRunEvidence)


def test_e1_runtime_has_no_execution_surface() -> None:
    source = inspect.getsource(_p110b())
    forbidden = (
        "run_qualified_research", "QualifiedResearchInput(", "ResearchExecutionResult(",
        "ResearchRunEvidence(", "order_send", "MetaTrader5", "run_backtest(", "activate_live(",
        "requests.", "socket.", "subprocess.",
    )
    assert all(token not in source for token in forbidden)


def test_f0_dangerous_protocol_remains_text_only(tmp_path: Path) -> None:
    protocol = "AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER"
    binding = _bind(
        _specification(tmp_path / "spec", protocol=protocol),
        _bound_input(tmp_path / "input"),
    )
    assert binding.protocol == protocol
    forbidden = ("authorized", "execution_result", "measurement", "finding", "knowledge")
    assert all(not hasattr(binding, name) for name in forbidden)


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p110b().ExperimentExecutionBinding)) == (
        "execution_binding_id", "experiment_spec_id", "request_id", "revision_id", "audit_id", "scope_id",
        "objective", "hypothesis_statement", "prediction", "falsification_rule", "protocol", "measurement_plan",
        "corpus_root", "contract_path", "expected_corpus_hash", "expected_contract_hash",
        "source_verdict", "source_completeness_status", "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    first = _bind(spec, bound)
    second = _bind(spec, bound)
    assert first == second and first is not second
    assert first.execution_binding_id == second.execution_binding_id
    assert _p110b().is_factory_attested_experiment_execution_binding(first)
    assert _p110b().is_factory_attested_experiment_execution_binding(second)


def test_g2_different_specification_changes_identity(tmp_path: Path) -> None:
    first_spec = _specification(tmp_path / "spec-a", protocol="Protocol A")
    second_spec = _specification(tmp_path / "spec-b", protocol="Protocol B")
    bound = _bound_input(tmp_path / "input")
    first = _bind(first_spec, bound)
    second = _bind(second_spec, bound)
    assert first.execution_binding_id != second.execution_binding_id


def test_g3_different_valid_resource_binding_changes_identity(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    first = _bind(spec, _bound_input(tmp_path / "input-a", payload=b"A"))
    second = _bind(spec, _bound_input(tmp_path / "input-b", payload=b"B"))
    assert first.execution_binding_id != second.execution_binding_id


def test_g4_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    binding = _bind(_specification(tmp_path / "spec"), _bound_input(tmp_path / "input"))
    manual = _p110b().ExperimentExecutionBinding(**asdict(binding))
    assert not _p110b().is_factory_attested_experiment_execution_binding(manual)
    assert not _p110b().is_factory_attested_experiment_execution_binding(copy.copy(binding))
    assert not _p110b().is_factory_attested_experiment_execution_binding(copy.deepcopy(binding))
    assert not _p110b().is_factory_attested_experiment_execution_binding(
        replace(binding, execution_binding_id=binding.execution_binding_id)
    )


def test_g5_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    binding = _bind(_specification(tmp_path / "spec"), _bound_input(tmp_path / "input"))
    original = binding.protocol
    object.__setattr__(binding, "protocol", "MUTATED")
    assert not _p110b().is_factory_attested_experiment_execution_binding(binding)
    object.__setattr__(binding, "protocol", original)
    assert not _p110b().is_factory_attested_experiment_execution_binding(binding)


def test_g6_upstream_objects_can_be_collected_after_binding(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    binding = _bind(spec, bound)
    spec_ref = weakref.ref(spec)
    bound_ref = weakref.ref(bound)
    del spec, bound
    gc.collect()
    assert spec_ref() is None
    assert bound_ref() is None
    assert _p110b().is_factory_attested_experiment_execution_binding(binding)


def test_h0_binding_does_not_mutate_upstream_objects(tmp_path: Path) -> None:
    spec = _specification(tmp_path / "spec")
    bound = _bound_input(tmp_path / "input")
    spec_snapshot = asdict(spec)
    bound_snapshot = asdict(bound)
    _bind(spec, bound)
    assert asdict(spec) == spec_snapshot
    assert asdict(bound) == bound_snapshot
    assert is_factory_attested_experiment_specification(spec)
    assert is_bound_research_input(bound)


def test_h1_binding_cannot_substitute_for_specification(tmp_path: Path) -> None:
    bound = _bound_input(tmp_path / "input")
    binding = _bind(_specification(tmp_path / "spec"), bound)
    with pytest.raises((TypeError, ValueError)):
        _bind(binding, bound)


def test_h2_binding_id_alone_is_not_authority(tmp_path: Path) -> None:
    binding = _bind(_specification(tmp_path / "spec"), _bound_input(tmp_path / "input"))
    assert not _p110b().is_factory_attested_experiment_execution_binding(binding.execution_binding_id)

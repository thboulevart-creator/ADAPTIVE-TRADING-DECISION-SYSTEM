from __future__ import annotations

import copy
import gc
import importlib
import inspect
import weakref
from contextlib import contextmanager
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
    qualify_experiment_execution_input,
)
from src.research.execution import ResearchExecutionResult
from src.research.input_binding import bind_execution_input
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P112B_CONTRACT = "P1_12B_LINKED_EXPERIMENT_EXECUTION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_12B_TEST_CAPTURE_AUTHORITY_V1"


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


def _experiment_request(tmp_path: Path):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which experiment should be executed?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Execute the qualified synthetic experiment without promoting findings.",
    )
    return produce_follow_up_request(revision)


@contextmanager
def _qualified_case(tmp_path: Path, *, protocol: str = "Protocol"):
    with synthetic_runtime_case() as case:
        request = _experiment_request(tmp_path)
        specification = specify_experiment(
            request,
            hypothesis_statement="H",
            prediction="P",
            falsification_rule="F",
            protocol=protocol,
            measurement_plan="Measure",
        )
        bound = bind_execution_input(
            case.corpus_root,
            case.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        binding = bind_experiment_execution(specification, bound)
        qualified = qualify_experiment_execution_input(binding)
        yield qualified, case


def _p112b():
    try:
        module = importlib.import_module("src.linked_experiment_execution")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.12B candidate absent — expected pre-implementation FAIL: "
            "src.linked_experiment_execution does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "LinkedExperimentExecutionResult",
        "run_linked_experiment",
        "is_factory_attested_linked_experiment_execution_result",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.12B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P112B_CONTRACT
    return module


def _run(execution_input):
    return _p112b().run_linked_experiment(execution_input)


def test_a0_exact_qei_executes_and_links(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, case):
        result = _run(execution_input)
        assert result.experiment_execution_input_id == execution_input.experiment_execution_input_id
        assert result.execution_binding_id == execution_input.execution_binding_id
        assert result.experiment_spec_id == execution_input.experiment_spec_id
        assert result.stream_sha256 == case.result.stream_sha256
        assert _p112b().is_factory_attested_linked_experiment_execution_result(result)


def test_a1_non_authoritative_qei_variants_rejected(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        variants = [
            execution_input.experiment_execution_input_id,
            asdict(execution_input),
            QualifiedExperimentExecutionInput(**asdict(execution_input)),
            copy.copy(execution_input),
            copy.deepcopy(execution_input),
            replace(
                execution_input,
                experiment_execution_input_id=execution_input.experiment_execution_input_id,
            ),
        ]
        for value in variants:
            with pytest.raises((TypeError, ValueError)):
                _run(value)


def test_a2_mutated_then_restored_qei_rejected(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        original = execution_input.protocol
        object.__setattr__(execution_input, "protocol", "MUTATED")
        assert not is_factory_attested_qualified_experiment_execution_input(execution_input)
        object.__setattr__(execution_input, "protocol", original)
        assert not is_factory_attested_qualified_experiment_execution_input(execution_input)
        with pytest.raises((TypeError, ValueError)):
            _run(execution_input)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p112b().run_linked_experiment)
    assert tuple(sig.parameters) == ("execution_input",)
    parameter = sig.parameters["execution_input"]
    assert parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameter.default is inspect.Parameter.empty


def test_c0_execution_metrics_match_p0_4_result(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, case):
        result = _run(execution_input)
        assert result.files_consumed == case.result.files_consumed
        assert result.ticks_consumed == case.result.ticks_consumed
        assert result.first_timestamp == case.result.first_timestamp
        assert result.last_timestamp == case.result.last_timestamp
        assert result.stream_sha256 == case.result.stream_sha256


def test_c1_result_is_not_raw_p0_4_or_run_evidence(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        assert not isinstance(result, ResearchExecutionResult)
        assert not isinstance(result, ResearchRunEvidence)


def test_d0_snapshot_preserves_full_experiment_and_resources(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        for name in (
            "experiment_execution_input_id",
            "execution_binding_id",
            "experiment_spec_id",
            "request_id",
            "revision_id",
            "audit_id",
            "scope_id",
            "objective",
            "hypothesis_statement",
            "prediction",
            "falsification_rule",
            "protocol",
            "measurement_plan",
            "corpus_root",
            "contract_path",
            "expected_corpus_hash",
            "expected_contract_hash",
            "source_verdict",
            "source_completeness_status",
            "source_independence_status",
        ):
            assert getattr(result, name) == getattr(execution_input, name)


def test_e0_modified_corpus_fails_closed(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, case):
        corpus_file = next(case.corpus_root.glob("*.bi5"))
        corpus_file.write_bytes(corpus_file.read_bytes() + b"changed")
        with pytest.raises((OSError, TypeError, ValueError)):
            _run(execution_input)


def test_e1_modified_contract_fails_closed(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, case):
        case.contract_path.write_text(
            case.contract_path.read_text(encoding="utf-8") + "\n",
            encoding="utf-8",
        )
        with pytest.raises((OSError, TypeError, ValueError)):
            _run(execution_input)


def test_e2_missing_contract_fails_closed(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, case):
        case.contract_path.unlink()
        with pytest.raises((OSError, TypeError, ValueError)):
            _run(execution_input)


def test_f0_dangerous_protocol_is_only_snapshotted_text(tmp_path: Path) -> None:
    protocol = "AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER"
    with _qualified_case(tmp_path, protocol=protocol) as (execution_input, _case):
        result = _run(execution_input)
        assert result.protocol == protocol
        for name in ("authorized", "finding", "hypothesis_verdict", "research_run_evidence"):
            assert not hasattr(result, name)


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p112b().LinkedExperimentExecutionResult)) == (
        "experiment_execution_result_id",
        "experiment_execution_input_id",
        "execution_binding_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "objective",
        "hypothesis_statement",
        "prediction",
        "falsification_rule",
        "protocol",
        "measurement_plan",
        "corpus_root",
        "contract_path",
        "expected_corpus_hash",
        "expected_contract_hash",
        "files_consumed",
        "ticks_consumed",
        "first_timestamp",
        "last_timestamp",
        "stream_sha256",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_g1_same_input_same_id_distinct_attested_results(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        first = _run(execution_input)
        second = _run(execution_input)
        assert first == second and first is not second
        assert first.experiment_execution_result_id == second.experiment_execution_result_id
        assert _p112b().is_factory_attested_linked_experiment_execution_result(first)
        assert _p112b().is_factory_attested_linked_experiment_execution_result(second)


def test_g2_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        manual = _p112b().LinkedExperimentExecutionResult(**asdict(result))
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(manual)
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(copy.copy(result))
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(copy.deepcopy(result))
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(
            replace(
                result,
                experiment_execution_result_id=result.experiment_execution_result_id,
            )
        )


def test_g3_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        original = result.stream_sha256
        object.__setattr__(result, "stream_sha256", "0" * 64)
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(result)
        object.__setattr__(result, "stream_sha256", original)
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(result)


def test_g4_upstream_qei_can_be_collected(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        ref = weakref.ref(execution_input)
        del execution_input
        gc.collect()
        assert ref() is None
        assert _p112b().is_factory_attested_linked_experiment_execution_result(result)


def test_h0_module_has_no_evidence_findings_or_operational_surface() -> None:
    module = _p112b()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "create_research_run_evidence",
        "produce_findings",
        "authorize",
        "run_backtest",
        "activate_live",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "from_research_execution(",
        "order_send",
        "MetaTrader5",
        "activate_live(",
        "requests.",
        "socket.",
        "subprocess.",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_result_id_alone_is_not_authority(tmp_path: Path) -> None:
    with _qualified_case(tmp_path) as (execution_input, _case):
        result = _run(execution_input)
        assert not _p112b().is_factory_attested_linked_experiment_execution_result(
            result.experiment_execution_result_id
        )

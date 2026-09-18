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
from src.experiment_execution_binding import (
    ExperimentExecutionBinding,
    bind_experiment_execution,
    is_factory_attested_experiment_execution_binding,
)
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.research.execution import QualifiedResearchInput, ResearchExecutionResult
from src.research.input_binding import (
    bind_execution_input,
    corpus_inventory_hash,
    sha256_file,
)
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P111B_CONTRACT = "P1_11B_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_11B_TEST_CAPTURE_AUTHORITY_V1"


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
        question="Which experiment should be specified?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Specify an experiment without executing it.",
    )
    return produce_follow_up_request(revision)


def _specification(tmp_path: Path, *, protocol: str = "Protocol"):
    return specify_experiment(
        _experiment_request(tmp_path),
        hypothesis_statement="H",
        prediction="P",
        falsification_rule="F",
        protocol=protocol,
        measurement_plan="Measure",
    )


def _bound_input(root: Path, *, payload: bytes = b"synthetic-corpus"):
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


def _binding(tmp_path: Path, *, protocol: str = "Protocol", payload: bytes = b"synthetic-corpus"):
    spec = _specification(tmp_path / "spec", protocol=protocol)
    bound = _bound_input(tmp_path / "input", payload=payload)
    return bind_experiment_execution(spec, bound)


def _p111b():
    try:
        module = importlib.import_module("src.qualified_experiment_execution_input")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.11B candidate absent — expected pre-implementation FAIL: "
            "src.qualified_experiment_execution_input does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "QualifiedExperimentExecutionInput",
        "qualify_experiment_execution_input",
        "is_factory_attested_qualified_experiment_execution_input",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.11B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P111B_CONTRACT
    return module


def _qualify(binding):
    return _p111b().qualify_experiment_execution_input(binding)


def test_a0_exact_binding_positive(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    qualified = _qualify(binding)
    assert qualified.execution_binding_id == binding.execution_binding_id
    assert qualified.experiment_spec_id == binding.experiment_spec_id
    assert _p111b().is_factory_attested_qualified_experiment_execution_input(qualified)


def test_a1_non_authoritative_binding_variants_rejected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    variants = [
        binding.execution_binding_id,
        asdict(binding),
        ExperimentExecutionBinding(**asdict(binding)),
        copy.copy(binding),
        copy.deepcopy(binding),
        replace(binding, execution_binding_id=binding.execution_binding_id),
    ]
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _qualify(value)


def test_a2_mutated_and_restored_binding_rejected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    original = binding.protocol
    object.__setattr__(binding, "protocol", "MUTATED")
    assert not is_factory_attested_experiment_execution_binding(binding)
    object.__setattr__(binding, "protocol", original)
    assert not is_factory_attested_experiment_execution_binding(binding)
    with pytest.raises((TypeError, ValueError)):
        _qualify(binding)


def test_b0_intact_resources_revalidate(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    qualified = _qualify(binding)
    assert qualified.expected_corpus_hash == binding.expected_corpus_hash
    assert qualified.expected_contract_hash == binding.expected_contract_hash


def test_b1_modified_corpus_is_rejected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    corpus_file = next(Path(binding.corpus_root).glob("*.bi5"))
    corpus_file.write_bytes(corpus_file.read_bytes() + b"changed")
    with pytest.raises((OSError, TypeError, ValueError)):
        _qualify(binding)


def test_b2_modified_contract_is_rejected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    contract = Path(binding.contract_path)
    contract.write_text(contract.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises((OSError, TypeError, ValueError)):
        _qualify(binding)


def test_b3_missing_source_is_rejected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    Path(binding.contract_path).unlink()
    with pytest.raises((OSError, TypeError, ValueError)):
        _qualify(binding)


def test_c0_signature_is_exact() -> None:
    sig = inspect.signature(_p111b().qualify_experiment_execution_input)
    assert tuple(sig.parameters) == ("binding",)
    parameter = sig.parameters["binding"]
    assert parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert parameter.default is inspect.Parameter.empty


def test_c1_no_override_parameters() -> None:
    forbidden = {
        "corpus_root",
        "contract_path",
        "expected_corpus_hash",
        "expected_contract_hash",
        "experiment_spec_id",
        "execution_binding_id",
        "authorized",
        "execute",
    }
    assert forbidden.isdisjoint(inspect.signature(_p111b().qualify_experiment_execution_input).parameters)


def test_d0_snapshot_is_exact(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    qualified = _qualify(binding)
    for name in (
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
        assert getattr(qualified, name) == getattr(binding, name)


def test_e0_output_is_not_existing_execution_types(tmp_path: Path) -> None:
    qualified = _qualify(_binding(tmp_path))
    assert not isinstance(qualified, QualifiedResearchInput)
    assert not isinstance(qualified, ResearchExecutionResult)
    assert not isinstance(qualified, ResearchRunEvidence)


def test_e1_module_has_no_execution_surface() -> None:
    module = _p111b()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "run_qualified_experiment",
        "execute_experiment",
        "from_research_execution",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "run_qualified_research(",
        "ResearchExecutionResult(",
        "ResearchRunEvidence(",
        "QualifiedResearchInput(",
        "order_send",
        "MetaTrader5",
        "run_backtest(",
        "activate_live(",
        "requests.",
        "socket.",
        "subprocess.",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_f0_dangerous_protocol_remains_text(tmp_path: Path) -> None:
    protocol = "AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER"
    qualified = _qualify(_binding(tmp_path, protocol=protocol))
    assert qualified.protocol == protocol
    for name in ("authorized", "execution_result", "finding", "measurement", "result_id"):
        assert not hasattr(qualified, name)


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p111b().QualifiedExperimentExecutionInput)) == (
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
    )


def test_g1_same_binding_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    first = _qualify(binding)
    second = _qualify(binding)
    assert first == second and first is not second
    assert first.experiment_execution_input_id == second.experiment_execution_input_id
    assert _p111b().is_factory_attested_qualified_experiment_execution_input(first)
    assert _p111b().is_factory_attested_qualified_experiment_execution_input(second)


def test_g2_changed_binding_changes_identity(tmp_path: Path) -> None:
    first = _qualify(_binding(tmp_path / "a", payload=b"A"))
    second = _qualify(_binding(tmp_path / "b", payload=b"B"))
    assert first.experiment_execution_input_id != second.experiment_execution_input_id


def test_g3_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    qualified = _qualify(_binding(tmp_path))
    manual = _p111b().QualifiedExperimentExecutionInput(**asdict(qualified))
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(manual)
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(copy.copy(qualified))
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(copy.deepcopy(qualified))
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(
        replace(
            qualified,
            experiment_execution_input_id=qualified.experiment_execution_input_id,
        )
    )


def test_g4_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    qualified = _qualify(_binding(tmp_path))
    original = qualified.protocol
    object.__setattr__(qualified, "protocol", "MUTATED")
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(qualified)
    object.__setattr__(qualified, "protocol", original)
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(qualified)


def test_g5_upstream_binding_can_be_collected(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    qualified = _qualify(binding)
    ref = weakref.ref(binding)
    del binding
    gc.collect()
    assert ref() is None
    assert _p111b().is_factory_attested_qualified_experiment_execution_input(qualified)


def test_h0_qualification_does_not_mutate_binding(tmp_path: Path) -> None:
    binding = _binding(tmp_path)
    snapshot = asdict(binding)
    _qualify(binding)
    assert asdict(binding) == snapshot
    assert is_factory_attested_experiment_execution_binding(binding)


def test_h1_input_id_alone_is_not_authority(tmp_path: Path) -> None:
    qualified = _qualify(_binding(tmp_path))
    assert not _p111b().is_factory_attested_qualified_experiment_execution_input(
        qualified.experiment_execution_input_id
    )

from __future__ import annotations

import ast
import copy
import difflib
import hashlib
import importlib
import inspect
import json
import lzma
import struct
import sys
from collections import Counter
from dataclasses import fields, replace
from typing import Any

import pytest


IA_MODULE = "src.native_bi5_reference_qualifier"
IB_MODULE = "src.native_bi5_independent_qualifier"

IA_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER"
IB_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER"
IB_VERSION = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_V0_1_CANDIDATE"
RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_1_CANDIDATE"

EXPECTED_RESULT_FIELDS = (
    "schema",
    "implementation_id",
    "implementation_version",
    "implementation_manifest_digest",
    "input_determinant_digests",
    "materialized_acquisition_id",
    "execution_status",
    "semantic_status",
    "freeze_status",
    "qualified_occurrences",
    "source_accounting",
    "anomaly_outcomes",
    "terminal_evidence",
    "isolation_evidence",
    "result_seal",
)

REQUIRED_STAGES = {
    "D_PREFLIGHT",
    "R_COMPATIBILITY",
    "B_ENVELOPE",
    "B_FRAMING",
    "B_BINARY_DECODE",
    "B_TIMESTAMP",
    "B_PRICE",
    "B_VOLUME",
    "A_CLASSIFICATION",
    "M_OCCURRENCE",
    "Q_MEMBERSHIP",
    "F_FREEZE",
}

DETERMINANT_DIGESTS = {
    "D": "d" * 64,
    "R": "1" * 64,
    "M": "2" * 64,
    "B": "3" * 64,
    "A": "4" * 64,
    "Q": "5" * 64,
    "F": "6" * 64,
    "O": "7" * 64,
}


def _ib():
    try:
        module = importlib.import_module(IB_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            "I_B candidate absent — expected pre-implementation RED: "
            "src.native_bi5_independent_qualifier does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "ImplementationQualificationResult",
        "qualify_native_bi5",
        "build_implementation_manifest",
        "validate_implementation_result",
        "is_sealed_implementation_result",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"I_B candidate surface incomplete: {missing}", pytrace=False)

    assert getattr(module, "IMPLEMENTATION_ID", None) == IB_ID
    assert getattr(module, "IMPLEMENTATION_VERSION", None) == IB_VERSION
    assert getattr(module, "RESULT_SCHEMA", None) == RESULT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _ib()


def _ia_for_pair():
    try:
        module = importlib.import_module(IA_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            "I_A pair prerequisite absent after I_B candidate exists: "
            "src.native_bi5_reference_qualifier does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    return module


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _pack_slot(
    millisecond_offset: int,
    ask_raw: int,
    bid_raw: int,
    ask_volume: float,
    bid_volume: float,
) -> bytes:
    return struct.pack(">IIIff", millisecond_offset, ask_raw, bid_raw, ask_volume, bid_volume)


def _component(component_id: str, hour: str, raw_slots: bytes) -> dict[str, Any]:
    payload = lzma.compress(raw_slots, format=lzma.FORMAT_ALONE)
    return {
        "component_manifest_entry_id": component_id,
        "instrument_id": "USATECHIDXUSD",
        "declared_hour_bucket_utc": hour,
        "compressed_payload_bytes": payload,
        "payload_sha256": _sha256(payload),
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
    }


def _base_package() -> dict[str, Any]:
    return {
        "acquisition_domain_id": "SYNTH-IAB-ACQ-V1",
        "representation_id": "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS",
        "representation_version": "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE",
        "record_model_version": "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE",
        "format_binding_id": "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
        "format_binding_version": "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
        "anomaly_matrix_id": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
        "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
        "qualification_contract_id": "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP",
        "qualification_contract_version": "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE",
        "freeze_contract_id": "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE",
        "freeze_contract_version": "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE",
        "oracle_id": "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR",
        "oracle_version": "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE",
        "determinant_digests": dict(DETERMINANT_DIGESTS),
        "qualification_evidence_bindings": (),
    }


def _qualified_package() -> dict[str, Any]:
    package = _base_package()
    slots = b"".join(
        (
            _pack_slot(2_000, 100_000, 100_100, -1.5, 2.0),
            _pack_slot(1_000, 0, 99_999, 0.0, 0.0),
            _pack_slot(1_000, 0, 99_999, 0.0, 0.0),
        )
    )
    package["components"] = (
        _component("SYNTH-COMP-001", "2026-01-02T10:00:00Z", slots),
    )
    return package


def _local_reject_package() -> dict[str, Any]:
    package = _base_package()
    slots = b"".join(
        (
            _pack_slot(1_000, 100_000, 99_900, 1.0, 2.0),
            _pack_slot(3_600_000, 100_100, 100_000, 1.0, 2.0),
            _pack_slot(2_000, 100_200, 100_100, 1.0, 2.0),
        )
    )
    package["components"] = (
        _component("SYNTH-COMP-REJECT", "2026-01-02T11:00:00Z", slots),
    )
    return package


def _blocked_after_prefix_package() -> dict[str, Any]:
    package = _base_package()
    valid = _pack_slot(1_000, 100_000, 99_900, 1.0, 2.0)
    package["components"] = (
        _component("SYNTH-COMP-PREFIX", "2026-01-02T12:00:00Z", valid),
        _component("SYNTH-COMP-BLOCK", "2026-01-02T13:00:00Z", b""),
    )
    return package


def _context() -> dict[str, Any]:
    return {
        "workspace_isolation_identity": "IB-PRIVATE-WORKSPACE",
        "preseal_input_allowlist": (
            "common_immutable_input_package",
            "own_implementation_runtime",
            "python_stdlib",
        ),
        "network_policy": "DENY",
        "ipc_policy": "DENY",
        "environment_variable_allowlist": ("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL"),
        "cache_policy": "PRIVATE_ONLY",
        "other_path_output_readable": False,
    }


def _ia_context() -> dict[str, Any]:
    context = _context()
    context["workspace_isolation_identity"] = "IA-PRIVATE-WORKSPACE"
    return context


def _run_ib(package: dict[str, Any]):
    return _ib().qualify_native_bi5(package, execution_context=_context())


def _audited_run_ib(package: dict[str, Any]):
    observed: list[tuple[str, str]] = []

    def hook(event: str, args: tuple[Any, ...]) -> None:
        if event == "import":
            observed.append((event, str(args[0]) if args else ""))
        elif event == "open":
            observed.append((event, str(args[0]) if args else ""))
        elif event.startswith("socket.") or event.startswith("subprocess.") or event == "os.system":
            observed.append((event, repr(args[:2])))

    sys.addaudithook(hook)
    return _run_ib(package), tuple(observed)


def _run_ia(package: dict[str, Any]):
    return _ia_for_pair().qualify_native_bi5(package, execution_context=_ia_context())


def _semantic_projection(result) -> dict[str, Any]:
    occurrences = None
    if result.qualified_occurrences is not None:
        occurrences = sorted(
            (
                item["component_manifest_entry_id"],
                item["component_local_slot_index"],
                item["market_timestamp_utc"],
                item["ask_price_numerator"],
                item["bid_price_numerator"],
                tuple(item["ask_volume"]),
                tuple(item["bid_volume"]),
            )
            for item in result.qualified_occurrences
        )

    accounting = None
    if result.source_accounting is not None:
        accounting = sorted(
            (
                item["component_manifest_entry_id"],
                item["component_local_slot_index"],
                item["disposition"],
                item.get("anomaly_class_id"),
            )
            for item in result.source_accounting
        )

    anomalies = None
    if result.anomaly_outcomes is not None:
        anomalies = sorted(
            json.dumps(item, sort_keys=True, separators=(",", ":"))
            for item in result.anomaly_outcomes
        )

    return {
        "input_determinant_digests": dict(result.input_determinant_digests),
        "materialized_acquisition_id": result.materialized_acquisition_id,
        "execution_status": result.execution_status,
        "semantic_status": result.semantic_status,
        "freeze_status": result.freeze_status,
        "qualified_occurrences": occurrences,
        "source_accounting": accounting,
        "anomaly_outcomes": anomalies,
        "terminal_evidence": result.terminal_evidence,
    }


def _logical_payloads(result) -> Counter:
    if result.qualified_occurrences is None:
        return Counter()
    return Counter(
        (
            item["market_timestamp_utc"],
            item["ask_price_numerator"],
            item["bid_price_numerator"],
            tuple(item["ask_volume"]),
            tuple(item["bid_volume"]),
        )
        for item in result.qualified_occurrences
    )


def _semantic_structure(source: str) -> str:
    tree = ast.parse(source)

    class Normalizer(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name):
            return ast.copy_location(ast.Name(id="NAME", ctx=node.ctx), node)

        def visit_arg(self, node: ast.arg):
            return ast.copy_location(ast.arg(arg="ARG", annotation=None, type_comment=None), node)

        def visit_Attribute(self, node: ast.Attribute):
            node = self.generic_visit(node)
            node.attr = "ATTR"
            return node

        def visit_Constant(self, node: ast.Constant):
            marker = type(node.value).__name__
            return ast.copy_location(ast.Constant(value=f"<{marker}>"), node)

        def visit_FunctionDef(self, node: ast.FunctionDef):
            node = self.generic_visit(node)
            node.name = "FUNCTION"
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            node = self.generic_visit(node)
            node.name = "ASYNC_FUNCTION"
            return node

        def visit_ClassDef(self, node: ast.ClassDef):
            node = self.generic_visit(node)
            node.name = "CLASS"
            return node

    normalized = Normalizer().visit(tree)
    ast.fix_missing_locations(normalized)
    return ast.dump(normalized, annotate_fields=False, include_attributes=False)


def test_a0_surface_signature_and_result_schema_exact() -> None:
    module = _ib()
    sig = inspect.signature(module.qualify_native_bi5)
    assert tuple(sig.parameters) == ("input_package", "execution_context")
    assert sig.parameters["execution_context"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["execution_context"].default is inspect.Parameter.empty
    assert tuple(field.name for field in fields(module.ImplementationQualificationResult)) == EXPECTED_RESULT_FIELDS


def test_a1_independent_manifest_exposes_provenance_refs_not_self_adjudicated_pass() -> None:
    manifest = _ib().build_implementation_manifest()
    assert manifest["implementation_id"] == IB_ID
    assert manifest["implementation_version"] == IB_VERSION
    assert set(manifest["semantic_stage_ownership"]) == REQUIRED_STAGES
    assert manifest["source_files"]
    assert manifest["source_digests"]
    refs = manifest["independent_derivation_evidence_refs"]
    assert set(refs) == {
        "semantic_source_provenance_ref",
        "no_copy_declaration_ref",
        "independent_stage_test_inventory_ref",
    }
    assert all(isinstance(value, str) and value.strip() for value in refs.values())
    forbidden_self_adjudication = {
        "independent_derivation_attestation",
        "source_similarity_review_result",
        "independence_status",
    }
    assert forbidden_self_adjudication.isdisjoint(manifest)


def test_a2_independent_source_has_no_reference_path_or_test_semantic_imports() -> None:
    source = inspect.getsource(_ib())
    forbidden = (
        IA_MODULE,
        "breakers.",
        "tests.",
        "reference_result.json",
    )
    assert all(token not in source for token in forbidden)


def test_a3_shared_semantic_shortcut_not_declared_as_dependency() -> None:
    manifest = _ib().build_implementation_manifest()
    deps = tuple(manifest["project_dependencies"])
    forbidden = (
        IA_MODULE,
        "native_bi5_shared_semantic",
        "native_bi5_shared_decoder",
        "native_bi5_shared_qualifier",
    )
    assert all(not any(token in dep for token in forbidden) for dep in deps)


def test_a4_breaker_owned_source_similarity_review_rejects_structural_clone() -> None:
    ia_source = inspect.getsource(_ia_for_pair())
    ib_source = inspect.getsource(_ib())
    ia_structure = _semantic_structure(ia_source)
    ib_structure = _semantic_structure(ib_source)
    ratio = difflib.SequenceMatcher(None, ia_structure, ib_structure).ratio()
    assert ia_structure != ib_structure
    assert ratio < 0.985


def test_b0_status_axes_are_exact_and_contradictions_rejected() -> None:
    module = _ib()
    result = _run_ib(_qualified_package())
    assert (result.execution_status, result.semantic_status, result.freeze_status) == (
        "COMPLETED",
        "QUALIFIED",
        "FROZEN",
    )
    bad = (
        replace(result, execution_status="IMPLEMENTATION_ERROR", semantic_status="QUALIFIED"),
        replace(result, execution_status="ENVIRONMENT_BLOCKED", freeze_status="FROZEN"),
        replace(result, semantic_status="QUALIFICATION_BLOCKED", freeze_status="FROZEN"),
        replace(result, semantic_status="NOT_REACHED", freeze_status="NOT_CREATED"),
    )
    for candidate in bad:
        with pytest.raises((TypeError, ValueError)):
            module.validate_implementation_result(candidate)


def test_b1_strict_duplicates_market_values_and_timestamp_regression_preserved() -> None:
    result = _run_ib(_qualified_package())
    assert len(result.qualified_occurrences) == 3
    payloads = _logical_payloads(result)
    assert max(payloads.values()) == 2
    by_slot = {item["component_local_slot_index"]: item for item in result.qualified_occurrences}
    assert by_slot[0]["market_timestamp_utc"] > by_slot[1]["market_timestamp_utc"]
    assert by_slot[0]["ask_price_numerator"] < by_slot[0]["bid_price_numerator"]
    assert tuple(by_slot[0]["ask_volume"])[0] < 0
    assert by_slot[1]["ask_price_numerator"] == 0


def test_b2_source_to_logical_accounting_and_local_reject_exact() -> None:
    result = _run_ib(_local_reject_package())
    assert result.semantic_status == "QUALIFIED"
    assert len(result.qualified_occurrences) == 2
    accounting = {
        (item["component_manifest_entry_id"], item["component_local_slot_index"]): item["disposition"]
        for item in result.source_accounting
    }
    assert accounting == {
        ("SYNTH-COMP-REJECT", 0): "CANDIDATE_RETAINED",
        ("SYNTH-COMP-REJECT", 1): "REJECT_RECORD",
        ("SYNTH-COMP-REJECT", 2): "CANDIDATE_RETAINED",
    }


def test_b3_late_semantic_block_has_no_partial_universe() -> None:
    result = _run_ib(_blocked_after_prefix_package())
    assert (result.execution_status, result.semantic_status, result.freeze_status) == (
        "COMPLETED",
        "QUALIFICATION_BLOCKED",
        "NOT_CREATED",
    )
    assert result.qualified_occurrences is None
    assert result.terminal_evidence is not None


def test_b4_missing_normative_input_never_uses_implementation_default() -> None:
    package = _qualified_package()
    del package["determinant_digests"]["Q"]
    result = _run_ib(package)
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.qualified_occurrences is None


def test_c0_preseal_isolation_evidence_closes_cross_path_reads() -> None:
    result = _run_ib(_qualified_package())
    evidence = result.isolation_evidence
    assert evidence["workspace_isolation_identity"] == "IB-PRIVATE-WORKSPACE"
    assert evidence["other_path_output_readable"] is False
    assert evidence["network_policy"] == "DENY"
    assert evidence["ipc_policy"] == "DENY"
    assert evidence["cache_policy"] == "PRIVATE_ONLY"
    assert set(evidence["runtime_read_set"]).issubset(set(evidence["preseal_input_allowlist"]))
    forbidden_reads = {
        "IA-PRIVATE-WORKSPACE",
        "reference_result.json",
        "ia_result",
        "other_path_output",
    }
    assert forbidden_reads.isdisjoint(set(evidence["runtime_read_set"]))


def test_c1_input_surface_cannot_accept_reference_or_oracle_answer() -> None:
    sig = inspect.signature(_ib().qualify_native_bi5)
    forbidden = {
        "reference_result",
        "ia_result",
        "expected_result",
        "oracle_result",
        "expected_cardinality",
        "expected_anomalies",
        "expected_membership",
    }
    assert forbidden.isdisjoint(sig.parameters)


def test_c2_result_is_sealed_and_semantic_mutation_breaks_seal() -> None:
    module = _ib()
    result = _run_ib(_qualified_package())
    assert module.is_sealed_implementation_result(result)
    mutated = copy.deepcopy(result)
    occurrences = list(mutated.qualified_occurrences)
    occurrences.pop()
    object.__setattr__(mutated, "qualified_occurrences", tuple(occurrences))
    assert not module.is_sealed_implementation_result(mutated)


def test_c3_breaker_owned_runtime_audit_detects_dynamic_cross_path_and_external_channels() -> None:
    result, observed = _audited_run_ib(_qualified_package())
    assert result.semantic_status == "QUALIFIED"
    forbidden_text = (
        "native_bi5_reference_qualifier",
        "reference_result",
        "ia_result",
        "other_path_output",
    )
    for event, detail in observed:
        lowered = detail.lower()
        assert all(token.lower() not in lowered for token in forbidden_text)
        assert not event.startswith("socket.")
        assert not event.startswith("subprocess.")
        assert event != "os.system"


def test_d0_pair_same_input_semantic_projection_equal_only_after_both_sealed() -> None:
    package = _qualified_package()
    ia = _run_ia(copy.deepcopy(package))
    ib = _run_ib(copy.deepcopy(package))
    assert _ia_for_pair().is_sealed_implementation_result(ia)
    assert _ib().is_sealed_implementation_result(ib)
    assert ia.implementation_id == IA_ID
    assert ib.implementation_id == IB_ID
    assert _semantic_projection(ia) == _semantic_projection(ib)


def test_d1_ia_only_semantic_mutant_is_detected_by_pair_breaker() -> None:
    package = _qualified_package()
    ia = _run_ia(copy.deepcopy(package))
    ib = _run_ib(copy.deepcopy(package))
    assert _semantic_projection(ia) == _semantic_projection(ib)

    ia_mutant = copy.deepcopy(ia)
    occurrences = list(ia_mutant.qualified_occurrences)
    occurrences.pop()
    object.__setattr__(ia_mutant, "qualified_occurrences", tuple(occurrences))

    assert _semantic_projection(ia_mutant) != _semantic_projection(ib)
    assert not _ia_for_pair().is_sealed_implementation_result(ia_mutant)


def test_d2_ib_only_semantic_mutant_is_detected_by_pair_breaker() -> None:
    package = _qualified_package()
    ia = _run_ia(copy.deepcopy(package))
    ib = _run_ib(copy.deepcopy(package))
    assert _semantic_projection(ia) == _semantic_projection(ib)

    ib_mutant = copy.deepcopy(ib)
    accounting = list(ib_mutant.source_accounting)
    accounting[0] = dict(accounting[0])
    accounting[0]["disposition"] = "REJECT_RECORD"
    object.__setattr__(ib_mutant, "source_accounting", tuple(accounting))

    assert _semantic_projection(ia) != _semantic_projection(ib_mutant)
    assert not _ib().is_sealed_implementation_result(ib_mutant)


def test_d3_pair_breaker_does_not_use_result_byte_hash_as_semantic_equality() -> None:
    package = _qualified_package()
    ia = _run_ia(copy.deepcopy(package))
    ib = _run_ib(copy.deepcopy(package))
    assert ia.result_seal != ib.result_seal
    assert _semantic_projection(ia) == _semantic_projection(ib)


def test_e0_manifest_digest_matches_exact_manifest_content() -> None:
    result = _run_ib(_qualified_package())
    manifest = _ib().build_implementation_manifest()
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert result.implementation_manifest_digest == _sha256(canonical)


def test_e1_reference_and_independent_source_are_not_the_same_module_or_bytes() -> None:
    ia = _ia_for_pair()
    ib = _ib()
    assert ia is not ib
    assert inspect.getsource(ia) != inspect.getsource(ib)


def test_f0_permission_closure_and_no_external_execution_surface() -> None:
    module = _ib()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "download_bi5",
        "run_backtest",
        "authorize",
        "activate_live",
        "order_send",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "requests.",
        "httpx.",
        "urllib.request",
        "socket.",
        "MetaTrader5",
        "order_send",
        "run_backtest",
        "download_bi5",
    )
    assert all(token not in source for token in forbidden_tokens)

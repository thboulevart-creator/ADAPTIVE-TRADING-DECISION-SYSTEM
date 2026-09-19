from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
import lzma
import os
import struct
import sys
from collections import Counter
from dataclasses import fields, replace
from typing import Any

import pytest


IB_MODULE = "src.native_bi5_independent_qualifier"

IA_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER"
IA_VERSION = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_V0_1_CANDIDATE"
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

EXECUTION_STATUSES = {"COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR"}
SEMANTIC_STATUSES = {
    "QUALIFIED",
    "QUALIFICATION_BLOCKED",
    "ACQUISITION_REJECTED",
    "NOT_REACHED",
}
FREEZE_STATUSES = {"FROZEN", "NOT_CREATED", "NOT_REACHED"}

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


def _ia():
    try:
        module = importlib.import_module("src.native_bi5_reference_qualifier")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "I_A candidate absent — expected pre-implementation RED: "
            "src.native_bi5_reference_qualifier does not exist",
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
        pytest.fail(f"I_A candidate surface incomplete: {missing}", pytrace=False)

    assert getattr(module, "IMPLEMENTATION_ID", None) == IA_ID
    assert getattr(module, "IMPLEMENTATION_VERSION", None) == IA_VERSION
    assert getattr(module, "RESULT_SCHEMA", None) == RESULT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _ia()


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
        "workspace_isolation_identity": "IA-PRIVATE-WORKSPACE",
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


def _run(package: dict[str, Any]):
    return _ia().qualify_native_bi5(package, execution_context=_context())


def _audited_run(package: dict[str, Any]):
    observed: list[tuple[str, str]] = []
    opposite = sys.modules.pop(IB_MODULE, None)

    def hook(event: str, args: tuple[Any, ...]) -> None:
        if event == "import":
            observed.append((event, str(args[0]) if args else ""))
        elif event == "open":
            observed.append((event, str(args[0]) if args else ""))
        elif event.startswith("socket.") or event.startswith("subprocess.") or event == "os.system":
            observed.append((event, repr(args[:2])))

    sys.addaudithook(hook)
    try:
        result = _run(package)
    finally:
        if opposite is not None:
            sys.modules[IB_MODULE] = opposite
    return result, tuple(observed)


def _cold_import_audit(module_name: str, forbidden_env_key: str):
    observed: list[tuple[str, str]] = []
    accessed_env: set[str] = set()
    previous = sys.modules.pop(module_name, None)
    original_environ = os.environ

    class TrackingEnviron(dict):
        def __getitem__(self, key):
            accessed_env.add(str(key))
            return super().__getitem__(key)

        def get(self, key, default=None):
            accessed_env.add(str(key))
            return super().get(key, default)

    tracked = TrackingEnviron(dict(original_environ))
    tracked[forbidden_env_key] = "CANARY-DO-NOT-READ"
    os.environ = tracked

    def hook(event: str, args: tuple[Any, ...]) -> None:
        if event == "import":
            observed.append((event, str(args[0]) if args else ""))
        elif event == "open":
            observed.append((event, str(args[0]) if args else ""))
        elif event.startswith("socket.") or event.startswith("subprocess.") or event == "os.system":
            observed.append((event, repr(args[:2])))

    sys.addaudithook(hook)
    try:
        fresh = importlib.import_module(module_name)
    finally:
        os.environ = original_environ
        sys.modules.pop(module_name, None)
        if previous is not None:
            sys.modules[module_name] = previous
    return fresh, tuple(observed), frozenset(accessed_env)


def _value_originates_from(value: object, module_name: str) -> bool:
    candidates = [value]
    if inspect.isfunction(value):
        candidates.extend(value.__defaults__ or ())
        candidates.extend((value.__kwdefaults__ or {}).values())
        if value.__closure__:
            for cell in value.__closure__:
                try:
                    candidates.append(cell.cell_contents)
                except ValueError:
                    pass
    for candidate in candidates:
        if inspect.ismodule(candidate) and getattr(candidate, "__name__", None) == module_name:
            return True
        if getattr(candidate, "__module__", None) == module_name:
            return True
    return False


def _occurrence_witnesses(result) -> list[tuple[str, int]]:
    if result.qualified_occurrences is None:
        return []
    return [
        (item["component_manifest_entry_id"], item["component_local_slot_index"])
        for item in result.qualified_occurrences
    ]


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


def test_a0_surface_and_signature_exact() -> None:
    module = _ia()
    sig = inspect.signature(module.qualify_native_bi5)
    assert tuple(sig.parameters) == ("input_package", "execution_context")
    assert sig.parameters["input_package"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["execution_context"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["execution_context"].default is inspect.Parameter.empty


def test_a1_result_schema_exact() -> None:
    module = _ia()
    assert tuple(field.name for field in fields(module.ImplementationQualificationResult)) == EXPECTED_RESULT_FIELDS


def test_a2_status_domains_are_closed() -> None:
    result = _run(_qualified_package())
    assert result.execution_status in EXECUTION_STATUSES
    assert result.semantic_status in SEMANTIC_STATUSES
    assert result.freeze_status in FREEZE_STATUSES
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFIED"
    assert result.freeze_status == "FROZEN"


def test_a3_result_validator_rejects_axis_contradictions() -> None:
    module = _ia()
    result = _run(_qualified_package())
    bad = (
        replace(result, execution_status="IMPLEMENTATION_ERROR", semantic_status="QUALIFIED"),
        replace(result, execution_status="ENVIRONMENT_BLOCKED", freeze_status="FROZEN"),
        replace(result, semantic_status="QUALIFICATION_BLOCKED", freeze_status="FROZEN"),
        replace(result, semantic_status="NOT_REACHED", freeze_status="NOT_CREATED"),
    )
    for candidate in bad:
        with pytest.raises((TypeError, ValueError)):
            module.validate_implementation_result(candidate)


def test_b0_strict_duplicates_are_preserved() -> None:
    result = _run(_qualified_package())
    assert len(result.qualified_occurrences) == 3
    witnesses = _occurrence_witnesses(result)
    assert len(witnesses) == len(set(witnesses)) == 3
    payloads = _logical_payloads(result)
    assert max(payloads.values()) == 2


def test_b1_no_hidden_timestamp_sorting() -> None:
    result = _run(_qualified_package())
    relation = {
        (item["component_manifest_entry_id"], item["component_local_slot_index"]): item["market_timestamp_utc"]
        for item in result.qualified_occurrences
    }
    assert relation[("SYNTH-COMP-001", 0)] > relation[("SYNTH-COMP-001", 1)]
    assert relation[("SYNTH-COMP-001", 1)] == relation[("SYNTH-COMP-001", 2)]


def test_b2_no_market_value_filter_leakage() -> None:
    result = _run(_qualified_package())
    assert len(result.qualified_occurrences) == 3
    by_slot = {
        item["component_local_slot_index"]: item
        for item in result.qualified_occurrences
    }
    assert by_slot[0]["ask_price_numerator"] < by_slot[0]["bid_price_numerator"]
    assert tuple(by_slot[0]["ask_volume"])[0] < 0
    assert by_slot[1]["ask_price_numerator"] == 0


def test_b3_source_to_logical_relation_exact() -> None:
    result = _run(_qualified_package())
    accounting = {
        (item["component_manifest_entry_id"], item["component_local_slot_index"]): item["disposition"]
        for item in result.source_accounting
    }
    assert accounting == {
        ("SYNTH-COMP-001", 0): "CANDIDATE_RETAINED",
        ("SYNTH-COMP-001", 1): "CANDIDATE_RETAINED",
        ("SYNTH-COMP-001", 2): "CANDIDATE_RETAINED",
    }


def test_b4_local_reject_is_accounted_without_partial_loss() -> None:
    result = _run(_local_reject_package())
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFIED"
    assert result.freeze_status == "FROZEN"
    accounting = {
        (item["component_manifest_entry_id"], item["component_local_slot_index"]): item["disposition"]
        for item in result.source_accounting
    }
    assert accounting[("SYNTH-COMP-REJECT", 1)] == "REJECT_RECORD"
    assert len(result.qualified_occurrences) == 2


def test_c0_late_block_never_emits_partial_universe() -> None:
    result = _run(_blocked_after_prefix_package())
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.qualified_occurrences is None
    assert result.terminal_evidence is not None


def test_c1_missing_determinant_fails_closed_without_default() -> None:
    package = _qualified_package()
    del package["determinant_digests"]["B"]
    result = _run(package)
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.qualified_occurrences is None


def test_c2_missing_hour_provenance_is_not_inferred_from_any_name() -> None:
    package = _qualified_package()
    component = dict(package["components"][0])
    component.pop("declared_hour_bucket_utc")
    component["filename"] = "2026/01/02/10h_ticks.bi5"
    package["components"] = (component,)
    result = _run(package)
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.qualified_occurrences is None


def test_d0_manifest_binds_exact_source_and_semantic_stage_ownership() -> None:
    manifest = _ia().build_implementation_manifest()
    assert manifest["implementation_id"] == IA_ID
    assert manifest["implementation_version"] == IA_VERSION
    required_stages = {
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
    assert set(manifest["semantic_stage_ownership"]) == required_stages
    assert all(manifest["semantic_stage_ownership"][stage] for stage in required_stages)
    assert manifest["source_files"]
    assert manifest["source_digests"]


def test_d1_reference_path_does_not_import_independent_semantic_path() -> None:
    source = inspect.getsource(_ia())
    forbidden = (
        "src.native_bi5_independent_qualifier",
        "breakers.",
        "tests.",
        "os.environ",
        "os.getenv",
        "from os import environ",
        "from os import getenv",
    )
    assert all(token not in source for token in forbidden)


def test_d1b_breaker_owned_cold_import_audit_and_global_origin_check() -> None:
    assert IB_MODULE not in sys.modules
    fresh, observed, accessed_env = _cold_import_audit(
        "src.native_bi5_reference_qualifier",
        "IAB_FORBIDDEN_IB_RESULT",
    )
    assert fresh.IMPLEMENTATION_ID == IA_ID
    assert "IAB_FORBIDDEN_IB_RESULT" not in accessed_env
    for event, detail in observed:
        lowered = detail.lower()
        assert "native_bi5_independent_qualifier" not in lowered
        assert not event.startswith("socket.")
        assert not event.startswith("subprocess.")
        assert event != "os.system"
    assert not any(
        _value_originates_from(value, IB_MODULE)
        for value in vars(fresh).values()
    )


def test_d2_result_seal_is_exact_and_mutation_invalidates() -> None:
    module = _ia()
    result = _run(_qualified_package())
    assert module.is_sealed_implementation_result(result)
    mutated = copy.deepcopy(result)
    object.__setattr__(mutated, "semantic_status", "QUALIFICATION_BLOCKED")
    assert not module.is_sealed_implementation_result(mutated)


def test_d3_manifest_digest_matches_result_binding() -> None:
    result = _run(_qualified_package())
    manifest = _ia().build_implementation_manifest()
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert result.implementation_manifest_digest == _sha256(canonical)


def test_e0_isolation_evidence_is_preseal_closed() -> None:
    result = _run(_qualified_package())
    evidence = result.isolation_evidence
    assert evidence["workspace_isolation_identity"] == "IA-PRIVATE-WORKSPACE"
    assert evidence["other_path_output_readable"] is False
    assert evidence["network_policy"] == "DENY"
    assert evidence["ipc_policy"] == "DENY"
    assert set(evidence["runtime_read_set"]).issubset(set(evidence["preseal_input_allowlist"]))


def test_e1_no_o_or_other_path_result_is_input_surface() -> None:
    sig = inspect.signature(_ia().qualify_native_bi5)
    forbidden = {
        "other_result",
        "ia_result",
        "ib_result",
        "expected_result",
        "oracle_result",
        "expected_cardinality",
        "expected_anomalies",
    }
    assert forbidden.isdisjoint(sig.parameters)


def test_e2_breaker_owned_runtime_audit_detects_forbidden_cross_path_or_external_channels() -> None:
    result, observed = _audited_run(_qualified_package())
    assert result.semantic_status == "QUALIFIED"
    forbidden_text = (
        "native_bi5_independent_qualifier",
        "ib_result",
        "other_path_output",
        "independent_result",
    )
    for event, detail in observed:
        lowered = detail.lower()
        assert all(token.lower() not in lowered for token in forbidden_text)
        assert not event.startswith("socket.")
        assert not event.startswith("subprocess.")
        assert event != "os.system"


def test_e3_breaker_owned_environment_canary_is_not_read(monkeypatch) -> None:
    accessed: set[str] = set()

    class TrackingEnviron(dict):
        def __getitem__(self, key):
            accessed.add(str(key))
            return super().__getitem__(key)

        def get(self, key, default=None):
            accessed.add(str(key))
            return super().get(key, default)

    tracked = TrackingEnviron(dict(os.environ))
    tracked["IAB_FORBIDDEN_IB_RESULT"] = "CANARY-DO-NOT-READ"
    monkeypatch.setattr(os, "environ", tracked)
    result = _run(_qualified_package())
    assert result.semantic_status == "QUALIFIED"
    assert "IAB_FORBIDDEN_IB_RESULT" not in accessed


def test_f0_semantic_result_mutant_is_detected_by_seal() -> None:
    module = _ia()
    result = _run(_qualified_package())
    mutated = copy.deepcopy(result)
    occurrences = list(mutated.qualified_occurrences)
    occurrences.pop()
    object.__setattr__(mutated, "qualified_occurrences", tuple(occurrences))
    assert not module.is_sealed_implementation_result(mutated)


def test_g0_permission_closure_and_no_external_execution_surface() -> None:
    module = _ia()
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

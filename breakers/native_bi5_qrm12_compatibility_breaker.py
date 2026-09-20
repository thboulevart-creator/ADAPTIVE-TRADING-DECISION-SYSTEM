from __future__ import annotations

import copy
import hashlib
import importlib
import importlib.util
import inspect
import json
import lzma
import math
import struct
from dataclasses import fields, replace
from pathlib import Path
from typing import Any, Mapping

import pytest

from src import native_bi5_freeze_persistence as freeze
from src import native_bi5_semantic_universe_comparator as oracle


IA2_MODULE = "src.native_bi5_reference_qualifier_qrm12"
IB2_MODULE = "src.native_bi5_independent_qualifier_qrm12"
HANDOFF_MODULE = "src.native_bi5_qrm12_handoff"

INPUT_SCHEMA = "NATIVE_BI5_QRM12_COMMON_INPUT_PACKAGE_V0_2_CANDIDATE"
RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_2_CANDIDATE"
RECEIPT_SCHEMA = "NATIVE_BI5_QRM12_EXECUTION_RECEIPT_V0_1_CANDIDATE"

IA2_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_QRM12"
IA2_VERSION = (
    "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_QRM12_V0_2_CANDIDATE"
)
IB2_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_QRM12"
IB2_VERSION = (
    "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_QRM12_V0_2_CANDIDATE"
)

HANDOFF_ID = "Q_RM_12_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_POSTSEAL_HANDOFF"
HANDOFF_VERSION = (
    "Q_RM_12_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_POSTSEAL_HANDOFF_V0_1_CANDIDATE"
)
HANDOFF_RESULT_SCHEMA = "NATIVE_BI5_QRM12_HANDOFF_RESULT_V0_1_CANDIDATE"

V1_IA_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER"
V1_IB_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER"

EXPECTED_RESULT_FIELDS = (
    "schema",
    "implementation_id",
    "implementation_version",
    "implementation_manifest_digest",
    "input_determinant_bindings",
    "materialized_acquisition_id",
    "execution_status",
    "semantic_status",
    "freeze_status",
    "bound_f_artifact",
    "terminal_evidence",
    "isolation_evidence",
    "result_seal",
)

EXPECTED_HANDOFF_FIELDS = {
    "schema",
    "handoff_id",
    "handoff_version",
    "handoff_result",
    "oracle_result",
    "comparison_scope",
    "reason",
}

STAGES = ("D", "R", "M", "B", "A", "Q", "F", "O")

_EXECUTION = {"COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR"}
_SEMANTIC = {"QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED", "NOT_REACHED"}
_FREEZE = {"FROZEN", "NOT_CREATED", "NOT_REACHED"}

_SLOT = struct.Struct(">IIIff")


def _validate_impl_surface(module, *, expected_id: str, expected_version: str):
    assert getattr(module, "IMPLEMENTATION_ID", None) == expected_id
    assert getattr(module, "IMPLEMENTATION_VERSION", None) == expected_version
    assert getattr(module, "RESULT_SCHEMA", None) == RESULT_SCHEMA
    assert getattr(module, "INPUT_SCHEMA", None) == INPUT_SCHEMA
    for name in (
        "ImplementationQualificationResultV2",
        "qualify_native_bi5_v2",
        "build_implementation_manifest",
        "validate_implementation_result_v2",
        "is_sealed_implementation_result_v2",
    ):
        assert hasattr(module, name), f"{module.__name__} missing {name}"
    return module


def _ia2():
    if importlib.util.find_spec(IA2_MODULE) is None:
        pytest.fail(
            "Q-RM-12 I_A V0.2 surface absent — expected pre-implementation RED: "
            + IA2_MODULE,
            pytrace=False,
        )
    return _validate_impl_surface(
        importlib.import_module(IA2_MODULE),
        expected_id=IA2_ID,
        expected_version=IA2_VERSION,
    )


def _ib2():
    if importlib.util.find_spec(IB2_MODULE) is None:
        pytest.fail(
            "Q-RM-12 I_B V0.2 surface absent — expected pre-implementation RED: "
            + IB2_MODULE,
            pytrace=False,
        )
    return _validate_impl_surface(
        importlib.import_module(IB2_MODULE),
        expected_id=IB2_ID,
        expected_version=IB2_VERSION,
    )


def _handoff():
    if importlib.util.find_spec(HANDOFF_MODULE) is None:
        pytest.fail(
            "Q-RM-12 handoff surface absent — expected pre-implementation RED: "
            + HANDOFF_MODULE,
            pytrace=False,
        )
    module = importlib.import_module(HANDOFF_MODULE)
    assert getattr(module, "HANDOFF_ID", None) == HANDOFF_ID
    assert getattr(module, "HANDOFF_VERSION", None) == HANDOFF_VERSION
    assert getattr(module, "RESULT_SCHEMA", None) == HANDOFF_RESULT_SCHEMA
    assert hasattr(module, "compare_sealed_results")
    return module


def _surface_modules():
    return _ia2(), _ib2(), _handoff()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _result_payload(result: Any) -> dict[str, Any]:
    return {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }


def _breaker_result_seal(result: Any) -> str:
    return _sha256(_canonical_bytes(_result_payload(result)))


def _reseal_result(result: Any):
    return replace(result, result_seal=_breaker_result_seal(result))


def _reseal_f(artifact: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(dict(artifact))
    unsigned = {k: v for k, v in out.items() if k != "artifact_integrity_digest"}
    out["artifact_integrity_digest"] = _sha256(_canonical_bytes(unsigned))
    freeze.validate_freeze_artifact(out)
    return out


def _source_digest(module) -> str:
    return _sha256(Path(module.__file__).read_bytes())


def _manifest_digest(module) -> str:
    manifest = module.build_implementation_manifest()
    return _sha256(_canonical_bytes(manifest))


def _pin(module) -> dict[str, str]:
    return {
        "implementation_id": module.IMPLEMENTATION_ID,
        "implementation_version": module.IMPLEMENTATION_VERSION,
        "implementation_manifest_digest": _manifest_digest(module),
        "implementation_source_digest": _source_digest(module),
    }


def _receipt(module, result, *, run_id: str, workspace: str) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "run_id": run_id,
        "implementation_id": module.IMPLEMENTATION_ID,
        "implementation_version": module.IMPLEMENTATION_VERSION,
        "implementation_manifest_digest": _manifest_digest(module),
        "implementation_source_digest": _source_digest(module),
        "workspace_isolation_identity": workspace,
        "result_seal": result.result_seal,
    }


def _context(side: str) -> dict[str, Any]:
    return {
        "workspace_isolation_identity": f"QRM12-{side}-PRIVATE",
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


def _binding(
    stage: str,
    normative_id: str,
    normative_version: str,
    ref_suffix: str,
    digest_char: str,
) -> dict[str, str]:
    return {
        "stage": stage,
        "normative_id": normative_id,
        "normative_version": normative_version,
        "immutable_reference": f"synthetic://qrm12/{ref_suffix}",
        "integrity_digest": digest_char * 64,
    }


def _bindings() -> tuple[dict[str, str], ...]:
    return (
        _binding(
            "D",
            "D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1",
            "D_MATERIALIZATION_V0_1_SYNTHETIC",
            "d",
            "d",
        ),
        _binding(
            "R",
            "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS",
            "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE",
            "r",
            "1",
        ),
        _binding(
            "M",
            "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL",
            "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE",
            "m",
            "2",
        ),
        _binding(
            "B",
            "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
            "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "b",
            "3",
        ),
        _binding(
            "A",
            "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
            "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "a",
            "4",
        ),
        _binding(
            "Q",
            "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP",
            "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE",
            "q",
            "5",
        ),
        _binding(
            "F",
            freeze.FREEZE_CONTRACT_ID,
            freeze.FREEZE_CONTRACT_VERSION,
            "f",
            "6",
        ),
        _binding(
            "O",
            oracle.ORACLE_ID,
            oracle.ORACLE_VERSION,
            "o",
            "7",
        ),
    )


def _pack_slot(
    millisecond_offset: int,
    ask_raw: int,
    bid_raw: int,
    ask_volume: float,
    bid_volume: float,
) -> bytes:
    return _SLOT.pack(
        millisecond_offset,
        ask_raw,
        bid_raw,
        ask_volume,
        bid_volume,
    )


def _component(component_id: str, hour: str, raw_slots: bytes) -> dict[str, Any]:
    payload = lzma.compress(raw_slots, format=lzma.FORMAT_ALONE)
    digest = _sha256(payload)
    return {
        "component_manifest_entry_id": component_id,
        "instrument_id": "USATECHIDXUSD",
        "instrument_source_identity": "DUKASCOPY/USATECHIDXUSD",
        "declared_hour_bucket_utc": hour,
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
        "immutable_payload_reference": f"synthetic://qrm12/payload/{component_id}",
        "payload_integrity_reference": digest,
        "compressed_payload_bytes": payload,
        "payload_sha256": digest,
    }


def _package() -> dict[str, Any]:
    raw = b"".join(
        (
            _pack_slot(2_000, 100_000, 100_100, -1.5, 2.0),
            _pack_slot(1_000, 0, 99_999, 0.0, 0.0),
            _pack_slot(1_000, 0, 99_999, 0.0, 0.0),
        )
    )
    return {
        "schema": INPUT_SCHEMA,
        "acquisition_domain_id": "SYNTH-QRM12-ACQ-001",
        "acquisition_declaration_version": "D_MATERIALIZATION_V0_1_SYNTHETIC",
        "determinant_bindings": _bindings(),
        "qualification_parameters": {
            "semantic_profile": "QRM12_SYNTHETIC_PROFILE",
            "strict_duplicates": True,
        },
        "d_completeness_evidence": {
            "immutable_reference": "synthetic://qrm12/d/completeness",
            "integrity_digest": "8" * 64,
        },
        "components": (
            _component("SYNTH-QRM12-COMP-001", "2026-01-02T10:00:00Z", raw),
        ),
        "qualification_evidence_bindings": (),
    }


def _qualify_pair():
    ia = _ia2()
    ib = _ib2()
    left = ia.qualify_native_bi5_v2(
        copy.deepcopy(_package()),
        execution_context=_context("IA"),
    )
    right = ib.qualify_native_bi5_v2(
        copy.deepcopy(_package()),
        execution_context=_context("IB"),
    )
    return ia, ib, left, right


def _assert_v2_result(module, result):
    assert isinstance(result, module.ImplementationQualificationResultV2)
    assert tuple(field.name for field in fields(result)) == EXPECTED_RESULT_FIELDS
    assert result.schema == RESULT_SCHEMA
    assert result.implementation_id == module.IMPLEMENTATION_ID
    assert result.implementation_version == module.IMPLEMENTATION_VERSION
    assert result.execution_status in _EXECUTION
    assert result.semantic_status in _SEMANTIC
    assert result.freeze_status in _FREEZE
    assert result.result_seal == _breaker_result_seal(result)
    assert module.is_sealed_implementation_result_v2(result)
    return result


def _run_handoff(
    left,
    right,
    *,
    left_module=None,
    right_module=None,
    left_receipt=None,
    right_receipt=None,
    left_pin=None,
    right_pin=None,
):
    ia = _ia2()
    ib = _ib2()
    handoff = _handoff()
    left_module = ia if left_module is None else left_module
    right_module = ib if right_module is None else right_module
    left_receipt = (
        _receipt(left_module, left, run_id="QRM12-RUN-A", workspace="QRM12-IA-PRIVATE")
        if left_receipt is None
        else left_receipt
    )
    right_receipt = (
        _receipt(right_module, right, run_id="QRM12-RUN-B", workspace="QRM12-IB-PRIVATE")
        if right_receipt is None
        else right_receipt
    )
    left_pin = _pin(left_module) if left_pin is None else left_pin
    right_pin = _pin(right_module) if right_pin is None else right_pin

    result = handoff.compare_sealed_results(
        left,
        left_receipt,
        right,
        right_receipt,
        expected_left=left_pin,
        expected_right=right_pin,
    )
    assert isinstance(result, Mapping)
    assert set(result) == EXPECTED_HANDOFF_FIELDS
    assert result["schema"] == HANDOFF_RESULT_SCHEMA
    assert result["handoff_id"] == HANDOFF_ID
    assert result["handoff_version"] == HANDOFF_VERSION
    assert result["handoff_result"] in {"SEMANTIC_EQUAL", "SEMANTIC_DIFFERENT", "BLOCKED"}
    assert result["oracle_result"] in {
        "SEMANTIC_EQUAL",
        "SEMANTIC_DIFFERENT",
        "BLOCKED",
        "NOT_INVOKED",
    }
    assert isinstance(result["comparison_scope"], str)
    assert isinstance(result["reason"], str)
    return result


def _assert_pre_o_blocked(result: Mapping[str, Any]) -> None:
    assert result["handoff_result"] == "BLOCKED"
    assert result["oracle_result"] == "NOT_INVOKED"


def _replace_binding(
    result,
    stage: str,
    *,
    normative_version: str | None = None,
    immutable_reference: str | None = None,
    integrity_digest: str | None = None,
):
    bindings = [copy.deepcopy(dict(item)) for item in result.input_determinant_bindings]
    target = next(item for item in bindings if item["stage"] == stage)
    if normative_version is not None:
        target["normative_version"] = normative_version
    if immutable_reference is not None:
        target["immutable_reference"] = immutable_reference
    if integrity_digest is not None:
        target["integrity_digest"] = integrity_digest
    return replace(result, input_determinant_bindings=tuple(bindings))


def _mutate_f_binding(
    artifact: Mapping[str, Any],
    stage: str,
    *,
    normative_version: str | None = None,
    immutable_reference: str | None = None,
    integrity_digest: str | None = None,
) -> dict[str, Any]:
    out = copy.deepcopy(dict(artifact))
    universe = out["qualified_universe"]
    target = next(item for item in universe["reconstruction_tuple"] if item["stage"] == stage)
    if normative_version is not None:
        target["normative_version"] = normative_version
        if stage == "D":
            universe["acquisition_declaration_version"] = normative_version
    if immutable_reference is not None:
        target["immutable_reference"] = immutable_reference
    if integrity_digest is not None:
        target["integrity_digest"] = integrity_digest
    return _reseal_f(out)


def _semantic_mutant(artifact: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(dict(artifact))
    for relation in ("b_candidate_occurrences", "retained_occurrences"):
        out["qualified_universe"][relation][0]["logical_payload"]["ask_price"] = {
            "numerator": 100_001,
            "denominator": 1000,
        }
    return _reseal_f(out)


def _permuted_f(artifact: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(dict(artifact))
    universe = out["qualified_universe"]
    universe["reconstruction_tuple"].reverse()
    universe["source_accounting"].reverse()
    universe["b_candidate_occurrences"].reverse()
    universe["retained_occurrences"].reverse()
    value = _reseal_f(out)
    assert value["artifact_integrity_digest"] != artifact["artifact_integrity_digest"]
    return value


def _different_acquisition_f(artifact: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(dict(artifact))
    out["qualified_universe"]["acquisition_domain_id"] = "SYNTH-QRM12-FOREIGN-ACQ"
    return _reseal_f(out)


def test_a0_future_surface_signatures_are_exact() -> None:
    ia, ib, handoff = _surface_modules()
    for module in (ia, ib):
        sig = inspect.signature(module.qualify_native_bi5_v2)
        assert tuple(sig.parameters) == ("input_package", "execution_context")
        assert sig.parameters["execution_context"].kind is inspect.Parameter.KEYWORD_ONLY
    sig = inspect.signature(handoff.compare_sealed_results)
    assert tuple(sig.parameters) == (
        "left_result",
        "left_receipt",
        "right_result",
        "right_receipt",
        "expected_left",
        "expected_right",
    )
    assert sig.parameters["expected_left"].kind is inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["expected_right"].kind is inspect.Parameter.KEYWORD_ONLY


def test_a1_v1_identity_cannot_be_reused_for_v2_compatibility() -> None:
    ia, ib, _, _ = _qualify_pair()
    assert ia.IMPLEMENTATION_ID != V1_IA_ID
    assert ib.IMPLEMENTATION_ID != V1_IB_ID
    assert "V0_2" in ia.IMPLEMENTATION_VERSION
    assert "V0_2" in ib.IMPLEMENTATION_VERSION


@pytest.mark.parametrize("side", ("IA", "IB"))
def test_a2_qualified_result_shape_and_strict_seal(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    module, result = (ia, left) if side == "IA" else (ib, right)
    _assert_v2_result(module, result)
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFIED"
    assert result.freeze_status == "FROZEN"
    assert result.bound_f_artifact is not None
    assert result.terminal_evidence is None
    freeze.validate_freeze_artifact(result.bound_f_artifact)


@pytest.mark.parametrize("side", ("IA", "IB"))
def test_a3_manifest_and_source_are_externally_pinnable(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    module, result = (ia, left) if side == "IA" else (ib, right)
    manifest = module.build_implementation_manifest()
    assert result.implementation_manifest_digest == _sha256(_canonical_bytes(manifest))
    assert _source_digest(module)
    assert manifest["implementation_id"] == module.IMPLEMENTATION_ID
    assert manifest["implementation_version"] == module.IMPLEMENTATION_VERSION
    assert manifest["source_digests"]


@pytest.mark.parametrize("side", ("IA", "IB"))
@pytest.mark.parametrize("mutation", ("missing", "duplicate", "digest_only"))
def test_b0_complete_unique_full_determinant_bindings_required(side: str, mutation: str) -> None:
    module = _ia2() if side == "IA" else _ib2()
    package = _package()
    bindings = [copy.deepcopy(dict(item)) for item in package["determinant_bindings"]]
    if mutation == "missing":
        bindings = bindings[:-1]
    elif mutation == "duplicate":
        bindings.append(copy.deepcopy(bindings[0]))
    else:
        bindings[0] = {
            "stage": "D",
            "integrity_digest": bindings[0]["integrity_digest"],
        }
    package["determinant_bindings"] = tuple(bindings)
    result = module.qualify_native_bi5_v2(package, execution_context=_context(side))
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None


@pytest.mark.parametrize("side", ("IA", "IB"))
@pytest.mark.parametrize("field", ("complete_slot_count", "terminal_fragment"))
def test_b1_common_package_cannot_supply_precomputed_b_semantics(side: str, field: str) -> None:
    module = _ia2() if side == "IA" else _ib2()
    package = _package()
    component = dict(package["components"][0])
    component[field] = 999 if field == "complete_slot_count" else {
        "terminal_fragment_start_offset": 60,
        "terminal_fragment_length": 3,
    }
    package["components"] = (component,)
    result = module.qualify_native_bi5_v2(package, execution_context=_context(side))
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.bound_f_artifact is None


def test_b2_preseal_semantic_f_builder_and_validator_are_not_shared() -> None:
    ia = _ia2()
    ib = _ib2()
    left_source = inspect.getsource(ia)
    right_source = inspect.getsource(ib)

    forbidden_left = (
        IB2_MODULE,
        HANDOFF_MODULE,
        "src.native_bi5_freeze_persistence",
        "src.native_bi5_semantic_universe_comparator",
        "src.native_bi5_independent_qualifier",
    )
    forbidden_right = (
        IA2_MODULE,
        HANDOFF_MODULE,
        "src.native_bi5_freeze_persistence",
        "src.native_bi5_semantic_universe_comparator",
        "src.native_bi5_reference_qualifier",
    )
    assert all(token not in left_source for token in forbidden_left)
    assert all(token not in right_source for token in forbidden_right)

    left_manifest = ia.build_implementation_manifest()
    right_manifest = ib.build_implementation_manifest()
    for manifest, forbidden in (
        (left_manifest, forbidden_left),
        (right_manifest, forbidden_right),
    ):
        dependencies = tuple(manifest["project_dependency_imports"])
        assert all(
            all(token not in dependency for token in forbidden)
            for dependency in dependencies
        )

    assert left_manifest["semantic_stage_ownership"]["F_FREEZE"]
    assert right_manifest["semantic_stage_ownership"]["F_FREEZE"]
    assert (
        left_manifest["semantic_stage_ownership"]["F_FREEZE"]
        != right_manifest["semantic_stage_ownership"]["F_FREEZE"]
    )


def test_b3_shared_structural_schema_cannot_hide_semantic_builder() -> None:
    ia = _ia2()
    ib = _ib2()
    for module in (ia, ib):
        forbidden_exports = (
            "shared_semantic_builder",
            "shared_f_builder",
            "semantic_defaults",
        )
        assert all(not hasattr(module, name) for name in forbidden_exports)


def test_c0_exact_equal_pair_reaches_o_and_is_equal() -> None:
    ia, ib, left, right = _qualify_pair()
    _assert_v2_result(ia, left)
    _assert_v2_result(ib, right)
    result = _run_handoff(left, right)
    assert result["handoff_result"] == "SEMANTIC_EQUAL"
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


@pytest.mark.parametrize("side", ("left", "right"))
def test_c1_qualified_result_missing_exact_f_is_rejected(side: str) -> None:
    _, _, left, right = _qualify_pair()
    target = left if side == "left" else right
    target = _reseal_result(replace(target, bound_f_artifact=None))
    if side == "left":
        result = _run_handoff(target, right)
    else:
        result = _run_handoff(left, target)
    assert result["handoff_result"] == "BLOCKED"


@pytest.mark.parametrize("side", ("IA", "IB"))
def test_c2_terminal_result_cannot_carry_qualified_f(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    module = ia if side == "IA" else ib
    qualified = left if side == "IA" else right
    package = _package()
    package["determinant_bindings"] = tuple(
        item for item in package["determinant_bindings"] if item["stage"] != "B"
    )
    terminal = module.qualify_native_bi5_v2(package, execution_context=_context(side))
    assert terminal.semantic_status == "QUALIFICATION_BLOCKED"
    assert terminal.bound_f_artifact is None
    forged = _reseal_result(
        replace(
            terminal,
            freeze_status="NOT_CREATED",
            bound_f_artifact=copy.deepcopy(qualified.bound_f_artifact),
        )
    )
    if side == "IA":
        result = _run_handoff(forged, right)
    else:
        result = _run_handoff(left, forged)
    assert result["handoff_result"] == "BLOCKED"


def test_c3_result_seal_is_breaker_reproducible_strict_canonical_json() -> None:
    ia, ib, left, right = _qualify_pair()
    for module, result in ((ia, left), (ib, right)):
        assert result.result_seal == _breaker_result_seal(result)
        assert module.is_sealed_implementation_result_v2(result)
        payload = _result_payload(result)
        with pytest.raises((TypeError, ValueError)):
            _canonical_bytes({**payload, "nonfinite_probe": math.nan})


def test_c4_self_asserted_manifest_cannot_replace_external_pin() -> None:
    ia, ib, left, right = _qualify_pair()
    forged = _reseal_result(
        replace(left, implementation_manifest_digest="f" * 64)
    )
    forged_receipt = _receipt(
        ia,
        forged,
        run_id="QRM12-RUN-A-FORGED",
        workspace="QRM12-IA-PRIVATE",
    )
    forged_receipt["implementation_manifest_digest"] = "f" * 64
    result = _run_handoff(
        forged,
        right,
        left_receipt=forged_receipt,
        left_pin=_pin(ia),
    )
    assert result["handoff_result"] == "BLOCKED"


@pytest.mark.parametrize("side", ("left", "right"))
def test_c5_run_receipt_must_bind_exact_emitted_result_seal(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    if side == "left":
        receipt = _receipt(ia, left, run_id="A", workspace="QRM12-IA-PRIVATE")
        receipt["result_seal"] = "0" * 64
        result = _run_handoff(left, right, left_receipt=receipt)
    else:
        receipt = _receipt(ib, right, run_id="B", workspace="QRM12-IB-PRIVATE")
        receipt["result_seal"] = "0" * 64
        result = _run_handoff(left, right, right_receipt=receipt)
    assert result["handoff_result"] == "BLOCKED"


@pytest.mark.parametrize(
    "field,value",
    (
        ("implementation_id", "FORGED_IMPLEMENTATION"),
        ("implementation_version", "FORGED_VERSION"),
        ("implementation_manifest_digest", "e" * 64),
        ("implementation_source_digest", "e" * 64),
    ),
)
def test_c5b_receipt_producer_fields_must_match_external_pin(field: str, value: str) -> None:
    ia, ib, left, right = _qualify_pair()
    receipt = _receipt(ia, left, run_id="A-PROVENANCE", workspace="QRM12-IA-PRIVATE")
    receipt[field] = value
    result = _run_handoff(left, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


def test_c5c_receipt_schema_is_closed() -> None:
    ia, _, left, right = _qualify_pair()
    receipt = _receipt(ia, left, run_id="A-SCHEMA", workspace="QRM12-IA-PRIVATE")
    receipt["schema"] = "FORGED_RECEIPT_SCHEMA"
    result = _run_handoff(left, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


def test_c5d_receipt_workspace_must_match_sealed_isolation_evidence() -> None:
    ia, _, left, right = _qualify_pair()
    receipt = _receipt(ia, left, run_id="A-WORKSPACE", workspace="QRM12-OTHER-WORKSPACE")
    result = _run_handoff(left, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


def test_c5e_cross_path_readable_isolation_evidence_is_rejected() -> None:
    ia, _, left, right = _qualify_pair()
    evidence = copy.deepcopy(dict(left.isolation_evidence))
    evidence["other_path_output_readable"] = True
    forged = _reseal_result(replace(left, isolation_evidence=evidence))
    receipt = _receipt(ia, forged, run_id="A-ISOLATION", workspace="QRM12-IA-PRIVATE")
    result = _run_handoff(forged, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


@pytest.mark.parametrize(
    "execution_status,semantic_status,freeze_status",
    (
        ("COMPLETED", "QUALIFICATION_BLOCKED", "NOT_CREATED"),
        ("COMPLETED", "ACQUISITION_REJECTED", "NOT_CREATED"),
        ("ENVIRONMENT_BLOCKED", "NOT_REACHED", "NOT_REACHED"),
        ("IMPLEMENTATION_ERROR", "NOT_REACHED", "NOT_REACHED"),
    ),
)
def test_c5f_terminal_or_nonreached_result_cannot_carry_qualified_f(
    execution_status: str,
    semantic_status: str,
    freeze_status: str,
) -> None:
    ia, _, left, right = _qualify_pair()
    forged = _reseal_result(
        replace(
            left,
            execution_status=execution_status,
            semantic_status=semantic_status,
            freeze_status=freeze_status,
            terminal_evidence={"reason": "SYNTHETIC_TERMINAL"},
            bound_f_artifact=copy.deepcopy(left.bound_f_artifact),
        )
    )
    receipt = _receipt(ia, forged, run_id="A-TERMINAL", workspace="QRM12-IA-PRIVATE")
    result = _run_handoff(forged, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


@pytest.mark.parametrize("side", ("IA", "IB"))
def test_c5g_real_environment_blocked_result_has_no_f(side: str) -> None:
    module = _ia2() if side == "IA" else _ib2()
    context = _context(side)
    context["other_path_output_readable"] = True
    result = module.qualify_native_bi5_v2(
        copy.deepcopy(_package()),
        execution_context=context,
    )
    assert result.execution_status == "ENVIRONMENT_BLOCKED"
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.bound_f_artifact is None


@pytest.mark.parametrize("side", ("left", "right"))
def test_c6_stale_f_substitution_is_rejected_by_run_bound_result(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    target = left if side == "left" else right
    stale = _permuted_f(target.bound_f_artifact)
    forged = _reseal_result(replace(target, bound_f_artifact=stale))
    assert forged.result_seal != target.result_seal

    if side == "left":
        original_receipt = _receipt(ia, left, run_id="A", workspace="QRM12-IA-PRIVATE")
        result = _run_handoff(forged, right, left_receipt=original_receipt)
    else:
        original_receipt = _receipt(ib, right, run_id="B", workspace="QRM12-IB-PRIVATE")
        result = _run_handoff(left, forged, right_receipt=original_receipt)
    _assert_pre_o_blocked(result)


def test_c7_f_a_f_b_mix_and_match_is_rejected() -> None:
    ia, ib, left, right = _qualify_pair()
    foreign_f = _different_acquisition_f(right.bound_f_artifact)
    left_mixed = _reseal_result(replace(left, bound_f_artifact=foreign_f))
    receipt = _receipt(ia, left_mixed, run_id="A-MIX", workspace="QRM12-IA-PRIVATE")
    result = _run_handoff(left_mixed, right, left_receipt=receipt)
    _assert_pre_o_blocked(result)


@pytest.mark.parametrize("side", ("left", "right"))
def test_d0_result_f_acquisition_identity_mismatch_is_rejected(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    target = left if side == "left" else right
    forged = _reseal_result(
        replace(target, materialized_acquisition_id="SYNTH-QRM12-OTHER-ACQ")
    )
    module = ia if side == "left" else ib
    receipt = _receipt(
        module,
        forged,
        run_id=f"{side}-acq-mismatch",
        workspace="QRM12-IA-PRIVATE" if side == "left" else "QRM12-IB-PRIVATE",
    )
    result = (
        _run_handoff(forged, right, left_receipt=receipt)
        if side == "left"
        else _run_handoff(left, forged, right_receipt=receipt)
    )
    assert result["handoff_result"] == "BLOCKED"


@pytest.mark.parametrize("side", ("left", "right"))
def test_d1_result_f_reconstruction_binding_mismatch_is_rejected(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    target = left if side == "left" else right
    forged = _replace_binding(target, "R", integrity_digest="a" * 64)
    forged = _reseal_result(forged)
    module = ia if side == "left" else ib
    receipt = _receipt(
        module,
        forged,
        run_id=f"{side}-binding-mismatch",
        workspace="QRM12-IA-PRIVATE" if side == "left" else "QRM12-IB-PRIVATE",
    )
    result = (
        _run_handoff(forged, right, left_receipt=receipt)
        if side == "left"
        else _run_handoff(left, forged, right_receipt=receipt)
    )
    assert result["handoff_result"] == "BLOCKED"


def test_d2_integrity_conflict_has_precedence_over_distinct_version() -> None:
    ia, ib, left, right = _qualify_pair()

    altered_f = _mutate_f_binding(
        right.bound_f_artifact,
        "D",
        normative_version="D_MATERIALIZATION_V0_2_SYNTHETIC",
    )
    altered_f = _mutate_f_binding(
        altered_f,
        "R",
        integrity_digest="b" * 64,
    )
    altered = _replace_binding(
        right,
        "D",
        normative_version="D_MATERIALIZATION_V0_2_SYNTHETIC",
    )
    altered = _replace_binding(altered, "R", integrity_digest="b" * 64)
    altered = replace(altered, bound_f_artifact=altered_f)
    altered = _reseal_result(altered)
    receipt = _receipt(ib, altered, run_id="B-CONFLICT", workspace="QRM12-IB-PRIVATE")

    result = _run_handoff(left, altered, right_receipt=receipt)
    assert result["handoff_result"] == "BLOCKED"
    assert result["reason"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"


def test_d3_o_determinant_mismatch_blocks_before_o() -> None:
    ia, ib, left, right = _qualify_pair()
    altered = _replace_binding(
        right,
        "O",
        normative_version="O_SYNTHETIC_DISTINCT_VERSION",
    )
    altered = _reseal_result(altered)
    receipt = _receipt(ib, altered, run_id="B-O-MISMATCH", workspace="QRM12-IB-PRIVATE")
    result = _run_handoff(left, altered, right_receipt=receipt)
    assert result["handoff_result"] == "BLOCKED"
    assert result["reason"] in {
        "DISTINCT_QUALIFICATION_STATE",
        "O_DETERMINANT_MISMATCH",
    }


def test_d4_handoff_is_validation_extraction_only_no_postseal_builder() -> None:
    handoff = _handoff()
    sig = inspect.signature(handoff.compare_sealed_results)
    assert tuple(sig.parameters) == (
        "left_result",
        "left_receipt",
        "right_result",
        "right_receipt",
        "expected_left",
        "expected_right",
    )
    assert "input_package" not in sig.parameters
    assert "common_input" not in sig.parameters
    assert not hasattr(handoff, "build_freeze_artifact")
    assert not hasattr(handoff, "reconstruct_freeze_artifact")
    assert not hasattr(handoff, "repair_freeze_artifact")


@pytest.mark.parametrize("side", ("IA", "IB"))
def test_e0_one_sided_semantic_mutant_remains_observable(side: str) -> None:
    ia, ib, left, right = _qualify_pair()
    if side == "IA":
        mutated_f = _semantic_mutant(left.bound_f_artifact)
        mutated = _reseal_result(replace(left, bound_f_artifact=mutated_f))
        receipt = _receipt(ia, mutated, run_id="A-MUTANT", workspace="QRM12-IA-PRIVATE")
        result = _run_handoff(mutated, right, left_receipt=receipt)
    else:
        mutated_f = _semantic_mutant(right.bound_f_artifact)
        mutated = _reseal_result(replace(right, bound_f_artifact=mutated_f))
        receipt = _receipt(ib, mutated, run_id="B-MUTANT", workspace="QRM12-IB-PRIVATE")
        result = _run_handoff(left, mutated, right_receipt=receipt)
    assert result["handoff_result"] == "SEMANTIC_DIFFERENT"
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_e1_f_artifact_hash_and_order_are_not_semantic_oracle() -> None:
    ia, ib, left, right = _qualify_pair()
    permuted = _permuted_f(right.bound_f_artifact)
    right2 = _reseal_result(replace(right, bound_f_artifact=permuted))
    receipt = _receipt(ib, right2, run_id="B-PERMUTED", workspace="QRM12-IB-PRIVATE")
    result = _run_handoff(left, right2, right_receipt=receipt)
    assert result["handoff_result"] == "SEMANTIC_EQUAL"
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_e2_source_witness_is_not_promoted_to_new_canonical_identity() -> None:
    ia, ib, left, right = _qualify_pair()
    result = _run_handoff(left, right)
    assert "canonical_occurrence_id" not in json.dumps(result, sort_keys=True)
    assert "temporal_precedence" not in json.dumps(result, sort_keys=True)


def test_e3_preseal_cross_path_information_flow_is_forbidden() -> None:
    ia = _ia2()
    ib = _ib2()
    left_source = inspect.getsource(ia)
    right_source = inspect.getsource(ib)
    forbidden_left = (
        "native_bi5_independent_qualifier_qrm12",
        "other_path_output",
        "ib_result",
        "expected_other_result",
    )
    forbidden_right = (
        "native_bi5_reference_qualifier_qrm12",
        "other_path_output",
        "ia_result",
        "expected_other_result",
    )
    assert all(token not in left_source for token in forbidden_left)
    assert all(token not in right_source for token in forbidden_right)

    left_dependencies = tuple(ia.build_implementation_manifest()["project_dependency_imports"])
    right_dependencies = tuple(ib.build_implementation_manifest()["project_dependency_imports"])
    assert all(IB2_MODULE not in item for item in left_dependencies)
    assert all(IA2_MODULE not in item for item in right_dependencies)
    assert all(HANDOFF_MODULE not in item for item in left_dependencies + right_dependencies)


def test_f0_permission_closure() -> None:
    ia, ib, handoff = _surface_modules()
    for module in (ia, ib, handoff):
        source = inspect.getsource(module)
        forbidden_attrs = (
            "download_bi5",
            "run_backtest",
            "authorize",
            "activate_live",
            "order_send",
        )
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
        assert all(not hasattr(module, name) for name in forbidden_attrs)
        assert all(token not in source for token in forbidden_tokens)


def test_f1_handoff_does_not_mutate_inputs() -> None:
    ia, ib, left, right = _qualify_pair()
    handoff = _handoff()
    left_receipt = _receipt(ia, left, run_id="A", workspace="QRM12-IA-PRIVATE")
    right_receipt = _receipt(ib, right, run_id="B", workspace="QRM12-IB-PRIVATE")
    left_pin = _pin(ia)
    right_pin = _pin(ib)

    before = (
        copy.deepcopy(left),
        copy.deepcopy(left_receipt),
        copy.deepcopy(right),
        copy.deepcopy(right_receipt),
        copy.deepcopy(left_pin),
        copy.deepcopy(right_pin),
    )

    handoff.compare_sealed_results(
        left,
        left_receipt,
        right,
        right_receipt,
        expected_left=left_pin,
        expected_right=right_pin,
    )

    after = (left, left_receipt, right, right_receipt, left_pin, right_pin)
    assert after == before

from __future__ import annotations

import copy
import hashlib
import inspect
import json
import math
from dataclasses import fields, replace
from typing import Any, Mapping

import pytest

from breakers import native_bi5_qrm12_compatibility_breaker as qrm
from src import native_bi5_freeze_persistence as freeze
from src import native_bi5_independent_qualifier_qrm12 as ib
from src import native_bi5_reference_qualifier_qrm12 as ia
from src import native_bi5_semantic_universe_comparator as oracle


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _reseal_f(artifact: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(artifact))
    unsigned = {
        key: child
        for key, child in value.items()
        if key != "artifact_integrity_digest"
    }
    value["artifact_integrity_digest"] = _sha256(_canonical_bytes(unsigned))
    return value


def _reseal_result(result):
    payload = {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }
    return replace(result, result_seal=_sha256(_canonical_bytes(payload)))


def _valid_ib():
    result = ib.qualify_native_bi5_v2(
        copy.deepcopy(qrm._package()),
        execution_context=copy.deepcopy(qrm._context("IB")),
    )
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFIED"
    assert result.freeze_status == "FROZEN"
    assert result.bound_f_artifact is not None
    assert ib.is_sealed_implementation_result_v2(result)
    return result


def test_control_valid_ib_result_is_locally_and_postseal_valid() -> None:
    result = _valid_ib()
    ib.validate_implementation_result_v2(result)
    ib._validate_private_freeze(result.bound_f_artifact)
    freeze.validate_freeze_artifact(result.bound_f_artifact)


def test_a1_result_acquisition_is_cross_bound_to_embedded_f() -> None:
    result = _valid_ib()
    forged = _reseal_result(
        replace(result, materialized_acquisition_id="SYNTH-QRM12-FOREIGN-ACQ")
    )
    assert not ib.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ib.validate_implementation_result_v2(forged)


def test_a2_result_bindings_are_cross_bound_to_embedded_f() -> None:
    result = _valid_ib()
    bindings = [copy.deepcopy(dict(item)) for item in result.input_determinant_bindings]
    next(item for item in bindings if item["stage"] == "R")["integrity_digest"] = "e" * 64
    forged = _reseal_result(replace(result, input_determinant_bindings=tuple(bindings)))
    assert not ib.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ib.validate_implementation_result_v2(forged)


def test_a3_embedded_f_reconstruction_cannot_diverge_from_result() -> None:
    result = _valid_ib()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    target = next(
        item
        for item in artifact["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "R"
    )
    target["integrity_digest"] = "e" * 64
    artifact = _reseal_f(artifact)
    forged = _reseal_result(replace(result, bound_f_artifact=artifact))
    assert not ib.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ib.validate_implementation_result_v2(forged)


def test_a4_private_f_rejects_empty_qualified_component_universe() -> None:
    result = _valid_ib()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    universe = artifact["qualified_universe"]
    universe["components"] = []
    universe["source_accounting"] = []
    universe["anomaly_outcomes"] = []
    universe["retained_occurrences"] = []
    universe["b_candidate_occurrences"] = []
    artifact["qualified_occurrence_count"] = 0
    artifact = _reseal_f(artifact)
    with pytest.raises((TypeError, ValueError)):
        ib._validate_private_freeze(artifact)


def test_b0_malformed_nonjson_binding_fails_closed() -> None:
    package = qrm._package()
    bindings = [copy.deepcopy(dict(item)) for item in package["determinant_bindings"]]
    bindings[0] = {
        "stage": "D",
        "integrity_digest": "d" * 64,
        "opaque": b"not-json",
    }
    package["determinant_bindings"] = tuple(bindings)
    result = ib.qualify_native_bi5_v2(package, execution_context=qrm._context("IB"))
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ib.is_sealed_implementation_result_v2(result)


def test_b1_nonfinite_qualification_parameter_is_input_rejection() -> None:
    package = qrm._package()
    package["qualification_parameters"] = {
        "semantic_profile": "QRM12_SYNTHETIC_PROFILE",
        "strict_duplicates": True,
        "nonfinite": math.nan,
    }
    result = ib.qualify_native_bi5_v2(package, execution_context=qrm._context("IB"))
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ib.is_sealed_implementation_result_v2(result)


def test_b2_nonjson_isolation_context_fails_closed_as_environment_blocked() -> None:
    context = qrm._context("IB")
    context["preseal_input_allowlist"] = (
        "common_immutable_input_package",
        "own_implementation_runtime",
        b"not-json",
    )
    result = ib.qualify_native_bi5_v2(qrm._package(), execution_context=context)
    assert result.execution_status == "ENVIRONMENT_BLOCKED"
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.bound_f_artifact is None
    assert ib.is_sealed_implementation_result_v2(result)


def test_b3_nonjson_d_completeness_is_input_rejection() -> None:
    package = qrm._package()
    package["d_completeness_evidence"] = {
        "immutable_reference": "synthetic://qrm12/d/completeness",
        "integrity_digest": "8" * 64,
        "opaque": b"not-json",
    }
    result = ib.qualify_native_bi5_v2(package, execution_context=qrm._context("IB"))
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ib.is_sealed_implementation_result_v2(result)


def test_b4_resealed_open_isolation_evidence_is_rejected() -> None:
    result = _valid_ib()
    isolation = copy.deepcopy(dict(result.isolation_evidence))
    isolation["network_policy"] = "ALLOW"
    forged = _reseal_result(replace(result, isolation_evidence=isolation))
    assert not ib.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ib.validate_implementation_result_v2(forged)


def test_c0_private_f_rejects_boolean_source_slot_indexes() -> None:
    result = _valid_ib()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    universe = artifact["qualified_universe"]
    universe["source_accounting"][0]["component_local_slot_index"] = False
    universe["retained_occurrences"][0]["source_witness"]["component_local_slot_index"] = False
    universe["b_candidate_occurrences"][0]["source_witness"]["component_local_slot_index"] = False
    artifact = _reseal_f(artifact)
    with pytest.raises((TypeError, ValueError)):
        ib._validate_private_freeze(artifact)


def test_c1_private_f_rejects_noncanonical_fractional_timestamp_width() -> None:
    result = _valid_ib()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    universe = artifact["qualified_universe"]
    for relation in ("retained_occurrences", "b_candidate_occurrences"):
        timestamp = universe[relation][0]["logical_payload"]["market_timestamp_utc"]
        universe[relation][0]["logical_payload"]["market_timestamp_utc"] = (
            timestamp[:-4] + timestamp[-4:-1].rstrip("0") + "Z"
        )
    artifact = _reseal_f(artifact)
    with pytest.raises((TypeError, ValueError)):
        ib._validate_private_freeze(artifact)


def test_d0_independent_source_and_manifest_have_no_forbidden_semantic_dependency() -> None:
    source = inspect.getsource(ib)
    forbidden = (
        "native_bi5_reference_qualifier_qrm12",
        "src.native_bi5_reference_qualifier",
        "src.native_bi5_freeze_persistence",
        "src.native_bi5_semantic_universe_comparator",
        "native_bi5_qrm12_handoff",
    )
    assert all(token not in source for token in forbidden)
    manifest = ib.build_implementation_manifest()
    assert tuple(manifest["project_dependency_imports"]) == ()
    assert manifest["semantic_stage_ownership"]["F_FREEZE"]
    assert (
        manifest["semantic_stage_ownership"]["F_FREEZE"]
        != ia.build_implementation_manifest()["semantic_stage_ownership"]["F_FREEZE"]
    )


def test_d1_postseal_independent_f_universes_are_semantically_equal() -> None:
    package = qrm._package()
    left = ia.qualify_native_bi5_v2(
        copy.deepcopy(package),
        execution_context=qrm._context("IA"),
    )
    right = ib.qualify_native_bi5_v2(
        copy.deepcopy(package),
        execution_context=qrm._context("IB"),
    )
    assert ia.is_sealed_implementation_result_v2(left)
    assert ib.is_sealed_implementation_result_v2(right)
    freeze.validate_freeze_artifact(left.bound_f_artifact)
    freeze.validate_freeze_artifact(right.bound_f_artifact)
    comparison = oracle.compare_freeze_artifacts(
        left.bound_f_artifact,
        right.bound_f_artifact,
    )
    assert comparison["oracle_result"] == "SEMANTIC_EQUAL"
    assert comparison["qualified_universe_comparison"] == "SEMANTIC_EQUAL"


def test_d2_qualification_does_not_mutate_input_or_execution_context() -> None:
    package = qrm._package()
    context = qrm._context("IB")
    before_package = copy.deepcopy(package)
    before_context = copy.deepcopy(context)
    ib.qualify_native_bi5_v2(package, execution_context=context)
    assert package == before_package
    assert context == before_context


def test_d3_permission_closure() -> None:
    source = inspect.getsource(ib)
    forbidden_attrs = ("download_bi5", "run_backtest", "authorize", "activate_live", "order_send")
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
    assert all(not hasattr(ib, name) for name in forbidden_attrs)
    assert all(token not in source for token in forbidden_tokens)

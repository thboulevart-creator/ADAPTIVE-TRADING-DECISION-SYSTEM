from __future__ import annotations

import copy
import hashlib
import json
import math
from dataclasses import fields, replace
from typing import Any, Mapping

import pytest

from breakers import native_bi5_qrm12_compatibility_breaker as qrm
from src import native_bi5_reference_qualifier_qrm12 as ia


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


def _valid_result():
    result = ia.qualify_native_bi5_v2(
        copy.deepcopy(qrm._package()),
        execution_context=qrm._context("IA"),
    )
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFIED"
    assert result.freeze_status == "FROZEN"
    assert result.bound_f_artifact is not None
    assert ia.is_sealed_implementation_result_v2(result)
    return result


def test_control_valid_result_is_locally_sealed_and_f_valid() -> None:
    result = _valid_result()
    ia.validate_implementation_result_v2(result)
    ia._ia_validate_freeze_artifact(result.bound_f_artifact)


def test_a1_result_materialized_acquisition_must_cross_bind_embedded_f() -> None:
    result = _valid_result()
    forged = _reseal_result(
        replace(result, materialized_acquisition_id="SYNTH-QRM12-FOREIGN-ACQ")
    )
    assert not ia.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ia.validate_implementation_result_v2(forged)


def test_a2_result_bindings_must_cross_bind_embedded_f_reconstruction() -> None:
    result = _valid_result()
    bindings = [copy.deepcopy(dict(item)) for item in result.input_determinant_bindings]
    next(item for item in bindings if item["stage"] == "R")["integrity_digest"] = "e" * 64
    forged = _reseal_result(
        replace(result, input_determinant_bindings=tuple(bindings))
    )
    assert not ia.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ia.validate_implementation_result_v2(forged)


def test_a3_embedded_f_reconstruction_cannot_diverge_from_result_bindings() -> None:
    result = _valid_result()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    binding = next(
        item
        for item in artifact["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "R"
    )
    binding["integrity_digest"] = "e" * 64
    artifact = _reseal_f(artifact)
    forged = _reseal_result(replace(result, bound_f_artifact=artifact))
    assert not ia.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ia.validate_implementation_result_v2(forged)


def test_a4_private_f_validator_rejects_empty_qualified_component_universe() -> None:
    result = _valid_result()
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
        ia._ia_validate_freeze_artifact(artifact)


def test_b0_malformed_nonjson_binding_fails_closed_as_qualification_blocked() -> None:
    package = qrm._package()
    bindings = [copy.deepcopy(dict(item)) for item in package["determinant_bindings"]]
    bindings[0] = {
        "stage": "D",
        "integrity_digest": "d" * 64,
        "opaque": b"not-json",
    }
    package["determinant_bindings"] = tuple(bindings)
    result = ia.qualify_native_bi5_v2(
        package,
        execution_context=qrm._context("IA"),
    )
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ia.is_sealed_implementation_result_v2(result)


def test_b1_nonfinite_qualification_parameter_is_common_input_rejection() -> None:
    package = qrm._package()
    package["qualification_parameters"] = {
        "semantic_profile": "QRM12_SYNTHETIC_PROFILE",
        "strict_duplicates": True,
        "nonfinite": math.nan,
    }
    result = ia.qualify_native_bi5_v2(
        package,
        execution_context=qrm._context("IA"),
    )
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ia.is_sealed_implementation_result_v2(result)


def test_c0_nonjson_isolation_context_fails_closed_as_environment_blocked() -> None:
    context = qrm._context("IA")
    context["preseal_input_allowlist"] = (
        "common_immutable_input_package",
        "own_implementation_runtime",
        "python_stdlib",
        b"not-json",
    )
    result = ia.qualify_native_bi5_v2(
        copy.deepcopy(qrm._package()),
        execution_context=context,
    )
    assert result.execution_status == "ENVIRONMENT_BLOCKED"
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.bound_f_artifact is None
    assert ia.is_sealed_implementation_result_v2(result)


def test_c1_nonjson_completeness_evidence_is_common_input_rejection() -> None:
    package = qrm._package()
    package["d_completeness_evidence"] = {
        "immutable_reference": "synthetic://qrm12/d/completeness",
        "integrity_digest": "8" * 64,
        "opaque": b"not-json",
    }
    result = ia.qualify_native_bi5_v2(
        package,
        execution_context=qrm._context("IA"),
    )
    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.bound_f_artifact is None
    assert ia.is_sealed_implementation_result_v2(result)


def test_c2_resealed_open_isolation_evidence_is_not_locally_valid() -> None:
    result = _valid_result()
    evidence = copy.deepcopy(dict(result.isolation_evidence))
    evidence["network_policy"] = "ALLOW"
    forged = _reseal_result(replace(result, isolation_evidence=evidence))
    assert not ia.is_sealed_implementation_result_v2(forged)
    with pytest.raises((TypeError, ValueError)):
        ia.validate_implementation_result_v2(forged)


def test_c3_private_f_validator_rejects_boolean_source_slot() -> None:
    result = _valid_result()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    artifact["qualified_universe"]["source_accounting"][0][
        "component_local_slot_index"
    ] = False
    artifact["qualified_universe"]["retained_occurrences"][0][
        "source_witness"
    ]["component_local_slot_index"] = False
    artifact["qualified_universe"]["b_candidate_occurrences"][0][
        "source_witness"
    ]["component_local_slot_index"] = False
    artifact = _reseal_f(artifact)
    with pytest.raises((TypeError, ValueError)):
        ia._ia_validate_freeze_artifact(artifact)


def test_c4_private_f_validator_rejects_noncanonical_timestamp_width() -> None:
    result = _valid_result()
    artifact = copy.deepcopy(dict(result.bound_f_artifact))
    for relation in ("retained_occurrences", "b_candidate_occurrences"):
        timestamp = artifact["qualified_universe"][relation][0]["logical_payload"][
            "market_timestamp_utc"
        ]
        assert timestamp.endswith(".000Z")
        artifact["qualified_universe"][relation][0]["logical_payload"][
            "market_timestamp_utc"
        ] = timestamp.replace(".000Z", ".0Z")
    artifact = _reseal_f(artifact)
    with pytest.raises((TypeError, ValueError)):
        ia._ia_validate_freeze_artifact(artifact)

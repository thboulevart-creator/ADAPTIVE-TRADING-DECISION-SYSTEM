from __future__ import annotations

import hashlib
import json
import lzma
import struct
from dataclasses import fields, replace
from typing import Any

import pytest

from src import native_bi5_reference_qualifier as ia


DETERMINANTS = {
    "D": "d" * 64,
    "R": "1" * 64,
    "M": "2" * 64,
    "B": "3" * 64,
    "A": "4" * 64,
    "Q": "5" * 64,
    "F": "6" * 64,
    "O": "7" * 64,
}


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _slot(ms: int, ask: int, bid: int, av: float, bv: float) -> bytes:
    return struct.pack(">IIIff", ms, ask, bid, av, bv)


def _component(component_id: str, hour: str, raw: bytes) -> dict[str, Any]:
    payload = lzma.compress(raw, format=lzma.FORMAT_ALONE)
    return {
        "component_manifest_entry_id": component_id,
        "instrument_id": "USATECHIDXUSD",
        "declared_hour_bucket_utc": hour,
        "compressed_payload_bytes": payload,
        "payload_sha256": _sha256(payload),
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
    }


def _base() -> dict[str, Any]:
    return {
        "acquisition_domain_id": "SYNTH-IA-ADVERSARIAL",
        "representation_id": ia.REPRESENTATION_ID,
        "representation_version": ia.REPRESENTATION_VERSION,
        "record_model_version": ia.RECORD_MODEL_VERSION,
        "format_binding_id": ia.FORMAT_BINDING_ID,
        "format_binding_version": ia.FORMAT_BINDING_VERSION,
        "anomaly_matrix_id": ia.ANOMALY_MATRIX_ID,
        "anomaly_matrix_version": ia.ANOMALY_MATRIX_VERSION,
        "qualification_contract_id": ia.QUALIFICATION_CONTRACT_ID,
        "qualification_contract_version": ia.QUALIFICATION_CONTRACT_VERSION,
        "freeze_contract_id": ia.FREEZE_CONTRACT_ID,
        "freeze_contract_version": ia.FREEZE_CONTRACT_VERSION,
        "oracle_id": ia.ORACLE_ID,
        "oracle_version": ia.ORACLE_VERSION,
        "determinant_digests": dict(DETERMINANTS),
        "qualification_evidence_bindings": (),
    }


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


def _qualified_package() -> dict[str, Any]:
    package = _base()
    package["components"] = (
        _component(
            "SYNTH-OK",
            "2026-01-02T10:00:00Z",
            _slot(1_000, 100_000, 99_900, 1.0, 2.0),
        ),
    )
    return package


def _external_reseal(result) -> ia.ImplementationQualificationResult:
    payload = {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }
    seal = _sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    )
    return replace(result, result_seal=seal)


def test_ia_f01_unverified_a08_binding_cannot_promote_terminal_fragment() -> None:
    package = _base()
    raw = _slot(1_000, 100_000, 99_900, 1.0, 2.0) + b"X"
    component = _component("SYNTH-PARTIAL", "2026-01-02T10:00:00Z", raw)
    package["components"] = (component,)
    package["qualification_evidence_bindings"] = (
        {
            "evidence_role": "CONSTRUCTIVE_COMPLETENESS_PROOF",
            "immutable_reference": "fabricated://proof",
            "integrity_digest_or_reference": "fabricated-integrity",
            "exact_anomaly_target_binding": {
                "target_scope": "TERMINAL_FRAGMENT",
                "component_manifest_entry_id": "SYNTH-PARTIAL",
                "terminal_fragment_start_offset": 20,
                "terminal_fragment_length": 1,
            },
        },
    )

    result = ia.qualify_native_bi5(package, execution_context=_context())

    assert result.execution_status == "COMPLETED"
    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.freeze_status == "NOT_CREATED"
    assert result.qualified_occurrences is None
    classes = {item["anomaly_class_id"] for item in result.anomaly_outcomes}
    assert "BI5-A07" in classes
    assert "BI5-A08" not in classes


def test_ia_f02_blocked_prefix_has_no_normative_source_accounting() -> None:
    package = _base()
    package["components"] = (
        _component(
            "SYNTH-PREFIX",
            "2026-01-02T10:00:00Z",
            _slot(1_000, 100_000, 99_900, 1.0, 2.0),
        ),
        _component("SYNTH-BLOCK", "2026-01-02T11:00:00Z", b""),
    )

    result = ia.qualify_native_bi5(package, execution_context=_context())

    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.qualified_occurrences is None
    assert result.source_accounting is None
    diagnostic = result.terminal_evidence["execution_diagnostics"]
    assert diagnostic["non_normative_source_accounting"]


def test_ia_f02_noncompleted_resealed_partial_universe_is_invalid() -> None:
    valid = ia.qualify_native_bi5(_qualified_package(), execution_context=_context())
    contradictory = replace(
        valid,
        execution_status="ENVIRONMENT_BLOCKED",
        semantic_status="NOT_REACHED",
        freeze_status="NOT_REACHED",
        result_seal="",
    )
    contradictory = _external_reseal(contradictory)

    assert not ia.is_sealed_implementation_result(contradictory)
    with pytest.raises(ValueError):
        ia.validate_implementation_result(contradictory)


@pytest.mark.parametrize(
    "mutator",
    (
        lambda ctx: ctx.__setitem__("preseal_input_allowlist", ()),
        lambda ctx: ctx.__setitem__(
            "preseal_input_allowlist",
            (
                "common_immutable_input_package",
                "own_implementation_runtime",
                "python_stdlib",
                "semantic_side_channel",
            ),
        ),
        lambda ctx: ctx.__setitem__("environment_variable_allowlist", ()),
        lambda ctx: ctx.__setitem__(
            "environment_variable_allowlist",
            ("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL", "IAB_FORBIDDEN_IB_RESULT"),
        ),
    ),
)
def test_ia_f03_preseal_allowlists_are_closed(mutator) -> None:
    context = _context()
    mutator(context)

    result = ia.qualify_native_bi5(_qualified_package(), execution_context=context)

    assert result.execution_status == "ENVIRONMENT_BLOCKED"
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.qualified_occurrences is None
    assert result.source_accounting is None
    assert ia.is_sealed_implementation_result(result)


def test_ia_f04_resealed_status_contradiction_is_not_valid_sealed_result() -> None:
    valid = ia.qualify_native_bi5(_qualified_package(), execution_context=_context())
    contradictory = replace(
        valid,
        semantic_status="QUALIFICATION_BLOCKED",
        freeze_status="FROZEN",
        result_seal="",
    )
    contradictory = _external_reseal(contradictory)

    assert not ia.is_sealed_implementation_result(contradictory)
    with pytest.raises(ValueError):
        ia.validate_implementation_result(contradictory)


def _anomaly_projection(result):
    return {
        (
            item["anomaly_class_id"],
            json.dumps(item["target"], sort_keys=True, separators=(",", ":")),
            item["mandatory_outcome"],
        )
        for item in result.anomaly_outcomes
    }


def test_ia_f05_blocked_anomaly_relation_is_traversal_independent() -> None:
    empty = _component("SYNTH-EMPTY", "2026-01-02T10:00:00Z", b"")
    missing_hour = _component(
        "SYNTH-NOHOUR",
        "2026-01-02T11:00:00Z",
        _slot(1_000, 100_000, 99_900, 1.0, 2.0),
    )
    missing_hour.pop("declared_hour_bucket_utc")

    package_a = _base()
    package_a["components"] = (empty, missing_hour)
    package_b = _base()
    package_b["components"] = (missing_hour, empty)

    result_a = ia.qualify_native_bi5(package_a, execution_context=_context())
    result_b = ia.qualify_native_bi5(package_b, execution_context=_context())

    assert result_a.semantic_status == result_b.semantic_status == "QUALIFICATION_BLOCKED"
    assert result_a.qualified_occurrences is result_b.qualified_occurrences is None
    assert _anomaly_projection(result_a) == _anomaly_projection(result_b)
    assert {item["anomaly_class_id"] for item in result_a.anomaly_outcomes} == {
        "BI5-A04",
        "BI5-A06",
    }


def test_ia_f05_duplicate_component_preflight_does_not_choose_delivery_winner() -> None:
    package = _base()
    package["components"] = (
        _component(
            "SYNTH-DUP",
            "2026-01-02T10:00:00Z",
            _slot(1_000, 100_000, 99_900, 1.0, 2.0),
        ),
        _component(
            "SYNTH-DUP",
            "2026-01-02T10:00:00Z",
            _slot(2_000, 101_000, 100_900, 1.0, 2.0),
        ),
    )

    result = ia.qualify_native_bi5(package, execution_context=_context())

    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.qualified_occurrences is None
    assert result.source_accounting is None
    assert {item["anomaly_class_id"] for item in result.anomaly_outcomes} == {"BI5-A03"}
    diagnostic = result.terminal_evidence["execution_diagnostics"]
    assert diagnostic["non_normative_source_accounting"] == ()


@pytest.mark.parametrize("workspace_identity", ("", "   ", 123))
def test_ia_f06_workspace_isolation_identity_must_be_nonempty_string(
    workspace_identity,
) -> None:
    context = _context()
    context["workspace_isolation_identity"] = workspace_identity

    result = ia.qualify_native_bi5(_qualified_package(), execution_context=context)

    assert result.execution_status == "ENVIRONMENT_BLOCKED"
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.qualified_occurrences is None
    assert result.source_accounting is None
    assert ia.is_sealed_implementation_result(result)

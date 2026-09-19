from __future__ import annotations

import hashlib
import json
import lzma
import struct
from dataclasses import fields, replace
from typing import Any

import pytest

from src import native_bi5_independent_qualifier as ib


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


def _package() -> dict[str, Any]:
    return {
        "acquisition_domain_id": "SYNTH-IB-ADV",
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
        "determinant_digests": dict(DETERMINANTS),
        "qualification_evidence_bindings": (),
        "components": (
            _component(
                "SYNTH-IB-ADV-001",
                "2026-01-02T10:00:00Z",
                _slot(1_000, 100_000, 99_900, 1.0, 2.0),
            ),
        ),
    }


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


def _external_reseal(result):
    payload = {
        item.name: getattr(result, item.name)
        for item in fields(result)
        if item.name != "result_seal"
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


def test_ib_f01_resealed_manifest_digest_substitution_is_rejected() -> None:
    valid = ib.qualify_native_bi5(_package(), execution_context=_context())
    forged = replace(valid, implementation_manifest_digest="0" * 64, result_seal="")
    forged = _external_reseal(forged)

    assert not ib.is_sealed_implementation_result(forged)
    with pytest.raises(ValueError):
        ib.validate_implementation_result(forged)


def test_ib_f02_resealed_incomplete_determinant_binding_is_rejected() -> None:
    valid = ib.qualify_native_bi5(_package(), execution_context=_context())
    incomplete = dict(valid.input_determinant_digests)
    incomplete.pop("Q")
    forged = replace(valid, input_determinant_digests=incomplete, result_seal="")
    forged = _external_reseal(forged)

    assert not ib.is_sealed_implementation_result(forged)
    with pytest.raises(ValueError):
        ib.validate_implementation_result(forged)


@pytest.mark.parametrize("context", (None, {}, "not-a-context"))
def test_ib_f03_invalid_execution_context_returns_governed_nonsemantic_status(context) -> None:
    result = ib.qualify_native_bi5(_package(), execution_context=context)

    assert result.execution_status in {"ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR"}
    assert result.semantic_status == "NOT_REACHED"
    assert result.freeze_status == "NOT_REACHED"
    assert result.qualified_occurrences is None
    assert result.source_accounting is None
    assert ib.is_sealed_implementation_result(result)


def test_unverified_constructive_proof_claim_remains_fail_closed_a07() -> None:
    package = _package()
    raw = _slot(1_000, 100_000, 99_900, 1.0, 2.0) + b"X"
    package["components"] = (_component("SYNTH-PARTIAL", "2026-01-02T10:00:00Z", raw),)
    package["qualification_evidence_bindings"] = (
        {
            "evidence_role": "CONSTRUCTIVE_COMPLETENESS_PROOF",
            "immutable_reference": "unqualified://claim",
            "integrity_digest_or_reference": "claim",
            "exact_anomaly_target_binding": {
                "target_scope": "TERMINAL_FRAGMENT",
                "component_manifest_entry_id": "SYNTH-PARTIAL",
                "terminal_fragment_start_offset": 20,
                "terminal_fragment_length": 1,
            },
        },
    )

    result = ib.qualify_native_bi5(package, execution_context=_context())

    assert result.semantic_status == "QUALIFICATION_BLOCKED"
    assert result.qualified_occurrences is None
    assert "BI5-A07" in {item["anomaly_class_id"] for item in result.anomaly_outcomes}
    assert "BI5-A08" not in {item["anomaly_class_id"] for item in result.anomaly_outcomes}

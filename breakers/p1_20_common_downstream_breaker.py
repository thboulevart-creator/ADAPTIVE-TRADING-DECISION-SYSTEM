"""Executable P1-20 breaker derived from frozen P1-19 24-case contract.

Before common-downstream runtime exists, all 24 tests must fail with the same
runtime-absent marker. After implementation, the exact frozen case IDs and
expected fail-closed reasons are replayed unchanged.
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FROZEN_PATH = ROOT / "GOVERNANCE" / "P1-19-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
FROZEN = json.loads(FROZEN_PATH.read_text(encoding="utf-8"))
EXPECTED_IDS = [f"P119-B{i:02d}" for i in range(1, 25)]
assert [row["id"] for row in FROZEN["cases"]] == EXPECTED_IDS
BY_ID = {row["id"]: row for row in FROZEN["cases"]}


def _mods():
    names = (
        "src.p1_12d_qualified_execution_evidence",
        "src.p1_13c_common_evaluation",
        "src.p1_14c_common_measurement_provenance",
        "src.p1_15c_common_evaluator_authority",
        "src.p1_16c_common_qualified_finding",
    )
    modules = []
    try:
        for name in names:
            modules.append(importlib.import_module(name))
    except ModuleNotFoundError:
        pytest.fail("P1_COMMON_DOWNSTREAM_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    return modules


def _expect(out, case_id):
    assert out["status"] in {"BLOCKED", "REJECTED"}, out
    assert out["reason"] == BY_ID[case_id]["expected"], out


@pytest.mark.parametrize("case_id", EXPECTED_IDS)
def test_p1_20_frozen_breakers(case_id):
    p12d, p13c, p14c, p15c, p16c = _mods()

    if case_id == "P119-B01":
        return _expect(p12d.validate_common_boundary_claim("P112C_AS_P112B"), case_id)
    if case_id == "P119-B02":
        return _expect(p12d.validate_envelope_candidate({"execution_binding_id":""}), case_id)
    if case_id == "P119-B03":
        return _expect(p12d.validate_envelope_candidate({"execution_binding_id":"X","experiment_spec_id":""}), case_id)
    if case_id == "P119-B04":
        return _expect(p12d.validate_common_boundary_claim("NATIVE_RESULT_IDENTITY_MISMATCH"), case_id)
    if case_id == "P119-B05":
        return _expect(p12d.validate_common_boundary_claim("ENGINE_SPECIFIC_FIELD_AS_UNIVERSAL"), case_id)
    if case_id == "P119-B06":
        return _expect(p12d.validate_common_boundary_claim("BI5_STREAM_AS_P112C_INPUT"), case_id)
    if case_id == "P119-B07":
        return _expect(p12d.validate_common_boundary_claim("PRODUCER_FIELDS_AS_P112B_COMMON"), case_id)
    if case_id == "P119-B08":
        return _expect(p12d.validate_common_boundary_claim("NATIVE_STATUS_REWRITE"), case_id)
    if case_id == "P119-B09":
        return _expect(p13c.validate_common_evaluation_claim("EXECUTED_TO_SUPPORTED"), case_id)
    if case_id == "P119-B10":
        return _expect(p12d.validate_common_boundary_claim("BLOCKED_TO_FAIL"), case_id)
    if case_id == "P119-B11":
        return _expect(p14c.validate_common_provenance_claim("RESULT_IDENTITY_AS_PROVENANCE"), case_id)
    if case_id == "P119-B12":
        return _expect(p13c.validate_common_evaluation_claim("MISSING_EXECUTION_ENVELOPE"), case_id)
    if case_id == "P119-B13":
        return _expect(p14c.validate_common_provenance_claim("WRONG_NATIVE_RESULT"), case_id)
    if case_id == "P119-B14":
        return _expect(p14c.validate_common_provenance_claim("WRONG_MEASUREMENT_INPUT"), case_id)
    if case_id == "P119-B15":
        return _expect(p15c.validate_common_authority_claim("MISMATCHED_PROVENANCE"), case_id)
    if case_id == "P119-B16":
        return _expect(p16c.validate_common_finding_claim("MISMATCHED_AUTHORITY"), case_id)
    if case_id == "P119-B17":
        return _expect(p12d.validate_common_boundary_claim("SCIENTIFIC_AUTHORITY"), case_id)
    if case_id == "P119-B18":
        return _expect(p12d.validate_common_boundary_claim("TRADING_CAPITAL_AUTHORITY"), case_id)
    if case_id == "P119-B19":
        return _expect(p12d.validate_common_boundary_claim("RUNTIME_ATTESTATION_AS_DURABLE"), case_id)
    if case_id == "P119-B20":
        return _expect(p12d.validate_common_boundary_claim("STRUCTURAL_WITHOUT_NATIVE_ATTESTATION"), case_id)
    if case_id == "P119-B21":
        return _expect(p13c.validate_common_evaluation_claim("OWNER_SPECIFIC_DUPLICATE_CHAIN"), case_id)
    if case_id == "P119-B22":
        return _expect(p12d.validate_common_boundary_claim("UNKNOWN_EXECUTION_OWNER"), case_id)
    if case_id == "P119-B23":
        return _expect(p12d.validate_common_boundary_claim("POST_RESULT_NORMALIZER_SELECTION"), case_id)
    if case_id == "P119-B24":
        return _expect(p12d.validate_common_boundary_claim("NATIVE_SEMANTIC_REWRITE"), case_id)
    raise AssertionError(case_id)

"""Executable DATA-02 breaker derived from the frozen DATA-01 32-case contract.

The breaker is intentionally committed before the DATA-02 runtime exists. Each
case calls the future public admission surface through _runtime(); therefore the
pre-implementation baseline is an observed 32-case RED rather than a synthetic
claim that tests would fail.
"""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest

from tests.data_02_fixture import (
    CLAIM_CLASS,
    CONSUMER_ID,
    DATASET_IDENTITY,
    EXACT_SCHEMA,
    SEMANTIC_LIMIT,
    SOURCE_IDENTITY,
    file_set_digest,
    make_package,
    manifest_file_set,
    rewrite_manifest_for_current_files,
    write_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN_CONTRACT_PATH = ROOT / "GOVERNANCE" / "DATA-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
EXPECTED_FROZEN_CONTRACT_BLOB = "d9cafc53c863341ca827097014411702c26633f2"
EXPECTED_CASE_IDS = [f"DATA01-B{i:02d}" for i in range(1, 33)]

def _git_blob(path: Path) -> str:
    import subprocess
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()

assert _git_blob(FROZEN_CONTRACT_PATH) == EXPECTED_FROZEN_CONTRACT_BLOB
FROZEN = json.loads(FROZEN_CONTRACT_PATH.read_text(encoding="utf-8"))
assert [x["id"] for x in FROZEN["cases"]] == EXPECTED_CASE_IDS
FROZEN_BY_ID = {x["id"]: x for x in FROZEN["cases"]}

def _runtime():
    try:
        module = importlib.import_module("src.data.claim_scoped_admission")
    except ModuleNotFoundError:
        pytest.fail("DATA02_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    assert module.CONTRACT == "ATDS_DATA_02_CLAIM_SCOPED_ADMISSION_V0_1"
    assert module.FROZEN_DATA01_BREAKER_BLOB == EXPECTED_FROZEN_CONTRACT_BLOB
    return module

def _reason(decision: dict, expected: str):
    assert decision["reason"] == expected, decision
    return decision

def _ready(m, package):
    out = m.evaluate_synthetic(package)
    assert out["status"] == "READY_FOR_EXACT_CLAIM", out
    return out

def _valid_binding(decision: dict, *, result_identity: str = "RESULT-SYNTHETIC-001") -> dict:
    basis = decision["binding_basis"]
    return {
        "claim_scope_id": basis["claim_scope_id"],
        "dataset_identity": basis["dataset_identity"],
        "ap0_manifest_sha256": basis["ap0_manifest_sha256"],
        "dataset_file_set_digest": basis["dataset_file_set_digest"],
        "schema_identity": basis["schema_identity"],
        "source_identity": basis["source_identity"],
        "transformer_blob": basis["transformer_blob"],
        "usage_envelope_id": basis["usage_envelope_id"],
        "data_admissibility_evidence_ref": decision["admission_digest"],
        "result_identity": result_identity,
    }

def _exercise(case_id: str, tmp_path: Path):
    m = _runtime()
    p = make_package(tmp_path)

    if case_id == "DATA01-B01":
        first = Path(p["root"]) / manifest_file_set(p)[0]["relative_path"]
        first.write_bytes(b"DIFFERENT-BYTES\n")
        return _reason(m.evaluate_synthetic(p), "BLOCKED_CONTENT_IDENTITY_MISMATCH")

    if case_id == "DATA01-B02":
        first = Path(p["root"]) / manifest_file_set(p)[0]["relative_path"]
        first.write_bytes(b"NEW-CONTENT-SAME-DATASET-ID\n")
        rewrite_manifest_for_current_files(p)
        return _reason(m.evaluate_synthetic(p), "BLOCKED_DATASET_ID_COLLISION")

    if case_id == "DATA01-B03":
        manifest_path = Path(p["manifest_path"])
        doc = json.loads(manifest_path.read_text(encoding="utf-8"))
        doc["commentary"] = "manifest drift"
        write_manifest(manifest_path, doc)
        return _reason(m.evaluate_synthetic(p), "BLOCKED_MANIFEST_IDENTITY_DRIFT")

    if case_id == "DATA01-B04":
        a = _ready(m, p)
        p["mutable_commentary"] = "new commentary only"
        b = _ready(m, p)
        assert a["binding_basis"]["dataset_file_set_digest"] == b["binding_basis"]["dataset_file_set_digest"]
        assert a["binding_basis"]["dataset_identity"] == b["binding_basis"]["dataset_identity"]
        return {"status": "PASS", "reason": "REJECT_METADATA_CONTENT_IDENTITY_COUPLING"}

    if case_id == "DATA01-B05":
        d = _ready(m, p)
        binding = _valid_binding(d)
        binding["dataset_identity"] = "SUBSTITUTED_DATASET"
        return _reason(m.validate_result_binding(d, binding), "BLOCKED_SILENT_DATASET_SUBSTITUTION")

    if case_id == "DATA01-B06":
        d = _ready(m, p)
        return _reason(m.validate_result_binding(d, {"result_identity": "R"}), "BLOCKED_INCOMPLETE_RESULT_DATASET_BINDING")

    if case_id == "DATA01-B07":
        d = _ready(m, p)
        return _reason(
            m.validate_result_binding(d, {"filename": "AP0-MANIFEST.json", "result_identity": "R"}),
            "REJECT_FILENAME_ONLY_BINDING",
        )

    if case_id == "DATA01-B08":
        p["provenance"]["child_checks_present"] = False
        return _reason(m.evaluate_synthetic(p), "REJECT_PARENT_PASS_INHERITANCE")

    if case_id == "DATA01-B09":
        p.pop("provenance")
        return _reason(m.evaluate_synthetic(p), "BLOCKED_MISSING_PROVENANCE")

    if case_id == "DATA01-B10":
        p["provenance"]["parent_dataset_ids"] = []
        p["provenance"]["lineage_status"] = "UNKNOWN"
        out = _reason(m.evaluate_synthetic(p), "BLOCKED_LINEAGE_UNKNOWN")
        assert out["lineage_status"] == "UNKNOWN"
        return out

    if case_id == "DATA01-B11":
        p["provenance"]["source_verification"] = "UNVERIFIED"
        out = _reason(m.evaluate_synthetic(p), "REJECT_SOURCE_VERIFICATION_LAUNDERING")
        assert out["status"] == "UNVERIFIED"
        return out

    if case_id == "DATA01-B12":
        p["transformation"].pop("transformer_blob")
        return _reason(m.evaluate_synthetic(p), "BLOCKED_HIDDEN_TRANSFORMATION")

    if case_id == "DATA01-B13":
        p["observed_schema"][0][1] = "string"
        return _reason(m.evaluate_synthetic(p), "BLOCKED_SCHEMA_DRIFT")

    if case_id == "DATA01-B14":
        p["rows"][0]["tick_count"] = 0
        return _reason(m.evaluate_synthetic(p), "FAIL_DATA_DOMAIN_INTEGRITY")

    if case_id == "DATA01-B15":
        p["rows"][1]["minute_start_ms_utc"] = 0
        return _reason(m.evaluate_synthetic(p), "FAIL_ORDERING_INTEGRITY")

    if case_id == "DATA01-B16":
        p["transformation"]["ambiguity"] = True
        return _reason(m.evaluate_synthetic(p), "BLOCKED_TRANSFORMATION_AMBIGUITY")

    if case_id == "DATA01-B17":
        first = Path(p["root"]) / manifest_file_set(p)[0]["relative_path"]
        first.unlink()
        return _reason(m.evaluate_synthetic(p), "BLOCKED_AP0_FILESET_MISMATCH")

    if case_id == "DATA01-B18":
        p["usage"]["claim_class"] = "CC04_PREDICTIVE"
        p["temporal"]["state"] = "TEMPORAL_OWNER_REQUIRED"
        p["temporal"]["basis"] = "predictive claim requires separate Temporal owner"
        return _reason(m.evaluate_synthetic(p), "BLOCKED_USAGE_ENVELOPE_VIOLATION")

    if case_id == "DATA01-B19":
        return _reason(
            m.validate_surface_selection(
                DATASET_IDENTITY,
                claim_class=CLAIM_CLASS,
                consumer_id=CONSUMER_ID,
                subminute_required=True,
                universal_sufficiency_claim=False,
            ),
            "BLOCKED_CLAIM_SURFACE_MISMATCH",
        )

    if case_id == "DATA01-B20":
        p["usage"]["tick_count_as_traded_volume"] = True
        return _reason(m.evaluate_synthetic(p), "REJECT_SEMANTIC_SCOPE_ESCALATION")

    if case_id == "DATA01-B21":
        p["temporal"]["state"] = "PASS"
        p["temporal"]["assertions"] = ["HISTORICAL_PIT_PASS"]
        return _reason(m.evaluate_synthetic(p), "REJECT_TEMPORAL_AUTHORITY_EXPANSION")

    if case_id == "DATA01-B22":
        p["temporal"]["latest_revision_as_historical"] = True
        p["temporal"]["assertions"] = ["HISTORICALLY_AVAILABLE"]
        return _reason(m.evaluate_synthetic(p), "BLOCKED_LATEST_AS_HISTORICAL")

    if case_id == "DATA01-B23":
        p["temporal"]["dependency_status"] = "UNKNOWN"
        p["temporal"]["assertions"] = ["HISTORICAL_PIT_PASS"]
        return _reason(m.evaluate_synthetic(p), "BLOCKED_TEMPORAL_DEPENDENCY_UNKNOWN")

    if case_id == "DATA01-B24":
        p["usage"]["claim_class"] = "CC04_PREDICTIVE"
        p["temporal"]["state"] = "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
        return _reason(m.evaluate_synthetic(p), "BLOCKED_STALE_TEMPORAL_NOT_APPLICABLE")

    if case_id == "DATA01-B25":
        p["provenance"]["source_verification"] = "UNVERIFIED"
        out = m.evaluate_synthetic(p)
        assert out["status"] == "UNVERIFIED"
        assert out["status"] != "READY_FOR_EXACT_CLAIM"
        return {"status": "PASS", "reason": "REJECT_STATUS_LAUNDERING"}

    if case_id == "DATA01-B26":
        p1 = make_package(tmp_path / "blocked_case")
        (Path(p1["root"]) / manifest_file_set(p1)[0]["relative_path"]).unlink()
        blocked = m.evaluate_synthetic(p1)
        p2 = make_package(tmp_path / "fail_case")
        p2["rows"][0]["tick_count"] = 0
        failed = m.evaluate_synthetic(p2)
        assert blocked["status"] == "BLOCKED"
        assert failed["status"] == "FAIL"
        assert blocked["status"] != failed["status"]
        return {"status": "PASS", "reason": "REJECT_STATUS_LAUNDERING"}

    if case_id == "DATA01-B27":
        p["authority_request"]["scientific"] = True
        out = _reason(m.evaluate_synthetic(p), "REJECT_AUTHORITY_LAUNDERING")
        assert out["scientific_authority"] is False
        assert out["trading_authority"] is False
        return out

    if case_id == "DATA01-B28":
        caps = m.CAPABILITIES
        assert caps["read_only_admission"] is True
        for forbidden in (
            "write_dataset","repair_dataset","transform_real_data","temporal_adjudication",
            "backtest","strategy","performance","oos_consumption","trading","capital",
        ):
            assert caps[forbidden] is False
        return {"status": "PASS", "reason": "REJECT_DATA01_SCOPE_EXPANSION"}

    if case_id == "DATA01-B29":
        return _reason(
            m.validate_surface_selection(
                "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
                claim_class=CLAIM_CLASS,
                consumer_id=CONSUMER_ID,
                subminute_required=False,
                universal_sufficiency_claim=False,
            ),
            "REJECT_NON_MINIMAL_H1_SELECTION",
        )

    if case_id == "DATA01-B30":
        return _reason(
            m.validate_surface_selection(
                "GENERIC_TICK_CSV_RUNTIME",
                claim_class=CLAIM_CLASS,
                consumer_id=CONSUMER_ID,
                subminute_required=False,
                universal_sufficiency_claim=False,
            ),
            "REJECT_AVAILABILITY_AS_SELECTION",
        )

    if case_id == "DATA01-B31":
        return _reason(
            m.validate_surface_selection(
                SOURCE_IDENTITY,
                claim_class=CLAIM_CLASS,
                consumer_id=CONSUMER_ID,
                subminute_required=False,
                universal_sufficiency_claim=False,
            ),
            "REJECT_NON_MINIMAL_RAW_SELECTION",
        )

    if case_id == "DATA01-B32":
        return _reason(
            m.validate_surface_selection(
                DATASET_IDENTITY,
                claim_class=CLAIM_CLASS,
                consumer_id=CONSUMER_ID,
                subminute_required=False,
                universal_sufficiency_claim=True,
            ),
            "REJECT_GLOBAL_SUFFICIENCY_OVERCLAIM",
        )

    raise AssertionError(f"unhandled frozen breaker case: {case_id}")

@pytest.mark.parametrize("case_id", EXPECTED_CASE_IDS)
def test_data02_frozen_data01_breakers(case_id: str, tmp_path: Path):
    result = _exercise(case_id, tmp_path)
    assert result["reason"] == FROZEN_BY_ID[case_id]["expected"]

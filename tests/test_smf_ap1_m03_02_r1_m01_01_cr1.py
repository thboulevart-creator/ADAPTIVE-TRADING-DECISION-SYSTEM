from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = ROOT / "GOVERNANCE"
CONTRACT = G / "SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.2.json"
V01 = G / "SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.1.json"
HUMAN = G / "SMF-AP1-M03-02-R1-M01-01-HUMAN-MATERIALITY-ADJUDICATION-V0.1.json"
RECORD = G / "SMF-AP1-M03-02-R1-M01-01-CR1-CORRECTION-RECORD-V0.1.json"

EXPECTED_V02_CANON_SHA256 = "90e8be1de734a633030c76eafaac0de2a95048e143584ec522a45b868f565010"
EXPECTED_V02_BLOB = "2293c665a2d30c520056c7814aec6a9dc79d68d1"
EXPECTED_V01_BLOB = "b7dc3ea554a74d6044e989b8017d4795ab4d9778"
EXPECTED_V01_CANON_SHA256 = "c60acbcb30222018dd6363da148113b5e6decf2df035168eecfa2c95e3f2ca60"
EXPECTED_V01_CRLF_SHA256 = "a3def5bb5867ca4f0fa28c41cfbbecd99a7d1d4dfbd231e6ba7137429f2e1fa6"
EXPECTED_HUMAN_BLOB = "a9382bc08f354e9142ccd55308f46c86da3f1af3"
EXPECTED_HUMAN_CANON_SHA256 = "91fb37bca8e25d1133e4d3859ba10c9f1e227a34390ee359175f5a72d3933b2f"
EXPECTED_HUMAN_CRLF_SHA256 = "e0cac00398f515424f9f6db902ce242928a30811212540aded12937f058b7ec3"

def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def normalized_lf_bytes(path: pathlib.Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def crlf_projection(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")

def blob_id_from_bytes(data: bytes) -> str:
    return subprocess.check_output(["git", "hash-object", "--stdin"], input=data).decode().strip()

def committed_blob(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{rel}"], text=True).strip()

def walk_strings(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from walk_strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk_strings(v)
    elif isinstance(x, str):
        yield x

def test_b1_to_b7_exact_m01_semantics_and_no_m10():
    c = load(CONTRACT)
    m = c["materiality_boundary"]
    assert m["effect_scale"] == "SYMMETRIC_RELATIVE_CHANGE"
    assert m["formula"] == "R[m,p,a,b] = 2 * abs(q[m,p,b] - q[m,p,a]) / (abs(q[m,p,b]) + abs(q[m,p,a]))"
    assert m["zero_denominator"] == "UNDEFINED_BLOCKED"
    assert m["threshold_scope"] == "COMMON_TO_ALL_11_CLAIM_UNITS"
    assert m["threshold"] == 0.20
    assert m["claim_unit_rule"] == "ANY_ADJACENT_MATERIAL_SHIFT"
    assert m["decision_precedence"] == [
        "IF_ANY_REQUIRED_CONTRAST_UNDEFINED_OR_BLOCKED => BLOCKED",
        "ELSE_IF_ANY_ADJACENT_R_GTE_0_20 => MATERIAL_TEMPORAL_VARIATION",
        "ELSE => NO_MATERIAL_TEMPORAL_VARIATION_DETECTED",
    ]
    assert c["primary_estimands"]["claim_units"] == 11
    assert c["primary_contrasts"]["total_contrasts"] == 33
    assert c["primary_estimands"]["global_pass_forbidden"] is True
    assert m["global_cross_metric_pass_fail"] == "FORBIDDEN"
    assert c["provenance"]["claim_origin"] == "EXPLORATORY_RESULT_DERIVED"
    assert c["population"]["primary_analysis"] == "COMPLETE_YEARS_ONLY"
    assert c["population"]["partial_year_role"] == "SENSITIVITY_DESCRIPTIVE_CONTEXT_ONLY"
    assert c["epistemic_limits"]["same_corpus_m10_maximum_semantics"] == "EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"
    assert c["m10_authorized"] is False
    assert c["m10_executed"] is False
    assert c["authority"]["scientific_method_execution"] is False

def test_b8_human_adjudication_multi_identity_exact():
    raw = normalized_lf_bytes(HUMAN)
    assert committed_blob(HUMAN) == EXPECTED_HUMAN_BLOB
    assert blob_id_from_bytes(raw) == EXPECTED_HUMAN_BLOB
    assert sha256(raw) == EXPECTED_HUMAN_CANON_SHA256
    assert sha256(crlf_projection(raw)) == EXPECTED_HUMAN_CRLF_SHA256
    c = load(CONTRACT)
    assert c["human_materiality_adjudication_sha256"] == EXPECTED_HUMAN_CRLF_SHA256
    q = c["correction_provenance"]["identity_transport_correction"]
    assert q["human_adjudication_git_blob_sha256"] == EXPECTED_HUMAN_CANON_SHA256

def test_b9_b10_encoding_and_normative_transitions_exact():
    c = load(CONTRACT)
    assert c["primary_contrasts"]["definition"] == "D[m,p,a->b] = q[m,p,b] - q[m,p,a]"
    assert c["primary_contrasts"]["transitions"] == ["2022->2023", "2023->2024", "2024->2025"]
    assert [s for s in walk_strings(c) if any(ord(ch) > 127 for ch in s)] == []

def test_b11_corrected_contract_canonical_identity_after_final_serialization():
    raw = normalized_lf_bytes(CONTRACT)
    assert sha256(raw) == EXPECTED_V02_CANON_SHA256
    assert blob_id_from_bytes(raw) == EXPECTED_V02_BLOB

def test_original_canonical_artifact_multi_identity_traceable_and_unchanged():
    raw = normalized_lf_bytes(V01)
    assert committed_blob(V01) == EXPECTED_V01_BLOB
    assert blob_id_from_bytes(raw) == EXPECTED_V01_BLOB
    assert sha256(raw) == EXPECTED_V01_CANON_SHA256
    assert sha256(crlf_projection(raw)) == EXPECTED_V01_CRLF_SHA256
    c = load(CONTRACT)
    p = c["correction_provenance"]
    assert p["original_canonical_artifact"]["git_blob"] == EXPECTED_V01_BLOB
    assert p["original_canonical_artifact"]["git_blob_sha256"] == EXPECTED_V01_CANON_SHA256
    assert p["original_canonical_artifact"]["windows_crlf_projection_sha256"] == EXPECTED_V01_CRLF_SHA256
    assert p["pre_persistence_local_identity"]["windows_local_sha256_before_second_reserialization"] == "37d1b18348982ba8a5981e33a31afd5baf7d76ddc32f47acb7b17b102517a26a"
    assert p["pre_persistence_local_identity"]["canonical_persisted"] is False
    assert p["original_identity_restoration"]["decision"] == "DO_NOT_RESTORE_OR_REWRITE_V0_1"

def test_correction_record_binds_actual_multi_identities():
    r = load(RECORD)
    assert r["corrected_contract"]["git_blob_sha256"] == EXPECTED_V02_CANON_SHA256
    assert r["corrected_contract"]["git_blob_precommit"] == EXPECTED_V02_BLOB
    assert r["original_canonical_contract"]["git_blob"] == EXPECTED_V01_BLOB
    assert r["original_canonical_contract"]["git_blob_sha256"] == EXPECTED_V01_CANON_SHA256
    assert r["original_canonical_contract"]["windows_crlf_projection_sha256"] == EXPECTED_V01_CRLF_SHA256
    assert r["human_materiality_adjudication"]["git_blob"] == EXPECTED_HUMAN_BLOB
    assert r["human_materiality_adjudication"]["git_blob_sha256"] == EXPECTED_HUMAN_CANON_SHA256
    assert r["human_materiality_adjudication"]["declared_windows_crlf_projection_sha256"] == EXPECTED_HUMAN_CRLF_SHA256
    assert r["m10_authorized"] is False
    assert r["m10_executed"] is False


def test_b12_final_receipt_references_actual_persisted_contract_identity():
    receipt = ROOT / "reports" / "program" / "2026-10-06-SMF-AP1-M03-02-R1-M01-01-CR1-FINAL-QUALIFICATION-RECEIPT-V0.1.json"
    r = load(receipt)
    c = r["corrected_m01_contract"]
    assert c["git_blob"] == EXPECTED_V02_BLOB
    assert c["git_blob_sha256"] == EXPECTED_V02_CANON_SHA256
    assert r["human_materiality_adjudication"]["git_blob"] == EXPECTED_HUMAN_BLOB
    assert r["human_materiality_adjudication"]["git_blob_sha256"] == EXPECTED_HUMAN_CANON_SHA256
    assert r["original_m01_contract"]["git_blob"] == EXPECTED_V01_BLOB
    assert r["original_m01_contract"]["git_blob_sha256"] == EXPECTED_V01_CANON_SHA256
    assert r["breakers"]["B12_RECEIPT_REFERENCES_ACTUAL_PERSISTED_CONTRACT_BLOB_AND_SHA256"] == "PASS"
    assert r["m10_authorized"] is False
    assert r["m10_executed"] is False

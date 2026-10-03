from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-TD-03C-SOURCE-CONTINUITY-ASSURANCE-CONTRACT-V0.1.json"
TARGET_PATH = ROOT / "tools/e1_td_03c_source_continuity_assurance.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
RUNTIME_CONTRACT = "ATDS_E1_TD_03C_SOURCE_CONTINUITY_ASSURANCE_V0_1"
LANE_A_ID = "LANE_A_SOURCE_B_TD01"
LANE_B_ID = "LANE_B_DUKASCOPY_PROSPECTIVE_INSURANCE"
SOURCE_B_DATASET_ID = "SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1"
INSURANCE_DATASET_ID = "DUKASCOPY_USATECH_PROSPECTIVE_INSURANCE_20261001_20271001_V0_1"
WINDOW_START = "2026-10-01T00:00:00Z"
WINDOW_END = "2027-10-01T00:00:00Z"

assert CONTRACT_DOC["schema"] == "ATDS_E1_TD_03C_SOURCE_CONTINUITY_ASSURANCE_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT_DOC["test_cases"]] == [f"TD03C-{i:02d}" for i in range(1, 31)]


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("E1_TD_03C_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("e1_td_03c_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("E1_TD_03C_RUNTIME_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _binding():
    return {
        "lane_id": LANE_B_ID,
        "dataset_id": INSURANCE_DATASET_ID,
        "provider": "Dukascopy Bank SA",
        "instrument_id": "USATECH.IDX/USD",
        "window_start_utc": WINDOW_START,
        "window_end_utc": WINDOW_END,
        "source_equivalence_status": "UNRESOLVED",
    }


def _file(rel="raw/2026/10/object-001.bin", raw=b"abc", request="REQ-001"):
    return {
        "lane_id": LANE_B_ID,
        "dataset_id": INSURANCE_DATASET_ID,
        "provider": "Dukascopy Bank SA",
        "instrument_id": "USATECH.IDX/USD",
        "relative_path": rel,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "rows": 2,
        "first_timestamp_ms": 1790812800000,
        "last_timestamp_ms": 1790812860000,
        "schema_signature": "synthetic-v1",
        "source_request_id": request,
    }


def _event(event_type="OBJECT_ACCEPTED", request="REQ-001", raw=b"abc"):
    f = _file(raw=raw, request=request)
    return {
        "event_timestamp_utc": "2026-10-03T08:00:00Z",
        "event_type": event_type,
        "lane_id": LANE_B_ID,
        "dataset_id": INSURANCE_DATASET_ID,
        "provider": "Dukascopy Bank SA",
        "instrument_id": "USATECH.IDX/USD",
        "source_request_id": request,
        "requested_start_utc": "2026-10-01T00:00:00Z",
        "requested_end_utc": "2026-10-01T01:00:00Z",
        "object_relative_path": f["relative_path"],
        "object_sha256": f["sha256"],
        "object_size_bytes": f["size_bytes"],
        "parse_status": "PASS",
        "row_count": f["rows"],
        "first_timestamp_ms": f["first_timestamp_ms"],
        "last_timestamp_ms": f["last_timestamp_ms"],
        "schema_signature": f["schema_signature"],
        "event_status": "ACCEPTED",
    }


def _ledger(m):
    out = []
    out = m.append_ledger_event(out, _event())
    return out


def _manifest(m):
    return m.build_manifest(
        binding=_binding(),
        files=[_file()],
        ledger=_ledger(m),
        runtime_environment={"python": "synthetic"},
        created_at_utc="2027-10-01T00:00:01Z",
    )


def test_td03c_01_runtime_contract_and_surface():
    m = _target()
    assert m.CONTRACT == RUNTIME_CONTRACT
    assert set(CONTRACT_DOC["required_runtime_surface"]).issubset(set(dir(m)))


def test_td03c_02_lane_identities_and_window_exact():
    m = _target()
    assert m.LANE_A_IDENTITY["lane_id"] == LANE_A_ID
    assert m.LANE_A_IDENTITY["dataset_id"] == SOURCE_B_DATASET_ID
    assert m.LANE_B_IDENTITY["lane_id"] == LANE_B_ID
    assert m.INSURANCE_DATASET_ID == INSURANCE_DATASET_ID
    assert m.WINDOW_START == WINDOW_START and m.WINDOW_END == WINDOW_END


def test_td03c_03_lane_a_identity_cannot_be_mutated():
    m = _target()
    b = _binding()
    b["dataset_id"] = SOURCE_B_DATASET_ID
    assert m.validate_lane_b_binding(b)["status"] == "BLOCKED_DATASET_IDENTITY"


def test_td03c_04_exact_lane_b_binding_accepted():
    m = _target()
    assert m.validate_lane_b_binding(_binding())["status"] == "PASS_LANE_B_BINDING"


def test_td03c_05_wrong_provider_blocked():
    m = _target()
    b = _binding(); b["provider"] = "Other Provider"
    assert m.validate_lane_b_binding(b)["status"] == "BLOCKED_PROVIDER_IDENTITY"


def test_td03c_06_wrong_instrument_blocked():
    m = _target()
    b = _binding(); b["instrument_id"] = "USA500.IDX/USD"
    assert m.validate_lane_b_binding(b)["status"] == "BLOCKED_INSTRUMENT_IDENTITY"


def test_td03c_07_source_b_dataset_id_reuse_blocked():
    m = _target()
    b = _binding(); b["dataset_id"] = SOURCE_B_DATASET_ID
    assert m.validate_lane_b_binding(b)["status"] == "BLOCKED_DATASET_IDENTITY"


def test_td03c_08_shared_or_nested_storage_blocked():
    m = _target()
    assert m.validate_storage_separation("C:/lane-a", "C:/lane-b")["status"] == "PASS_STORAGE_SEPARATION"
    assert m.validate_storage_separation("C:/same", "C:/same")["status"] == "BLOCKED_CROSS_LANE_CONTAMINATION"
    assert m.validate_storage_separation("C:/root", "C:/root/lane-b")["status"] == "BLOCKED_CROSS_LANE_CONTAMINATION"


def test_td03c_09_lane_a_file_record_blocked():
    m = _target()
    f = _file(); f["lane_id"] = LANE_A_ID
    assert m.validate_file_record(f)["status"] == "BLOCKED_CROSS_LANE_CONTAMINATION"


def test_td03c_10_lane_a_ledger_event_blocked():
    m = _target()
    e = _event(); e["lane_id"] = LANE_A_ID
    with pytest.raises(Exception):
        m.append_ledger_event([], e)


def test_td03c_11_raw_hash_and_size_pass():
    m = _target()
    raw = b"synthetic-raw"
    out = m.verify_raw_object(raw, expected_sha256=hashlib.sha256(raw).hexdigest(), expected_size=len(raw))
    assert out["status"] == "PASS_RAW_OBJECT_INTEGRITY"


def test_td03c_12_one_byte_mutation_blocks():
    m = _target()
    raw = b"synthetic-raw"
    out = m.verify_raw_object(raw+b"x", expected_sha256=hashlib.sha256(raw).hexdigest(), expected_size=len(raw))
    assert out["status"] == "BLOCKED_RAW_OBJECT_INTEGRITY"


def test_td03c_13_source_revision_detected():
    m = _target()
    assert m.detect_source_revision("a"*64, "a"*64)["status"] != "BLOCKED_SOURCE_REVISION"
    assert m.detect_source_revision("a"*64, "b"*64)["status"] == "BLOCKED_SOURCE_REVISION"


def test_td03c_14_valid_interpreted_ticks_pass():
    m = _target()
    rows = [
        {"timestamp":1790812800000,"bid_price":20000.0,"ask_price":20000.5},
        {"timestamp":1790812800100,"bid_price":20000.1,"ask_price":20000.6},
    ]
    sem = {"timezone":"UTC","timestamp_unit":"ms","bid":"BID","ask":"ASK"}
    assert m.inspect_interpreted_ticks(rows, sem)["status"] == "PASS_INTERPRETED_TICKS"


def test_td03c_15_missing_bid_or_ask_blocks():
    m = _target()
    sem = {"timezone":"UTC","timestamp_unit":"ms","bid":"BID","ask":"ASK"}
    assert m.inspect_interpreted_ticks([{"timestamp":1,"ask_price":2.0}], sem)["status"] == "BLOCKED_BID_ASK_SEMANTICS"
    assert m.inspect_interpreted_ticks([{"timestamp":1,"bid_price":1.0}], sem)["status"] == "BLOCKED_BID_ASK_SEMANTICS"


def test_td03c_16_ask_below_bid_blocks():
    m = _target()
    sem = {"timezone":"UTC","timestamp_unit":"ms","bid":"BID","ask":"ASK"}
    assert m.inspect_interpreted_ticks([{"timestamp":1,"bid_price":2.0,"ask_price":1.0}], sem)["status"] == "BLOCKED_BID_ASK_SEMANTICS"


def test_td03c_17_non_increasing_timestamp_blocks():
    m = _target()
    sem = {"timezone":"UTC","timestamp_unit":"ms","bid":"BID","ask":"ASK"}
    rows=[{"timestamp":2,"bid_price":1.0,"ask_price":2.0},{"timestamp":2,"bid_price":1.1,"ask_price":2.1}]
    assert m.inspect_interpreted_ticks(rows, sem)["status"] == "BLOCKED_TIMESTAMP_INTEGRITY"


def test_td03c_18_unknown_timestamp_semantics_blocks():
    m = _target()
    rows=[{"timestamp":1,"bid_price":1.0,"ask_price":2.0}]
    sem={"timezone":"UNKNOWN","timestamp_unit":"ms","bid":"BID","ask":"ASK"}
    assert m.inspect_interpreted_ticks(rows, sem)["status"] == "BLOCKED_TIMESTAMP_SEMANTICS"


def test_td03c_19_unknown_bi5_scale_raw_only():
    m = _target()
    out=m.assess_bi5_decode_semantics({"raw_price_scale":None,"scale_evidence_status":"UNRESOLVED"})
    assert out["raw_preservation"] == "ALLOWED"
    assert out["decoded_values"] == "BLOCKED_RAW_DECODE_SEMANTICS"


def test_td03c_20_decode_semantics_do_not_imply_equivalence():
    m = _target()
    out=m.assess_bi5_decode_semantics({"raw_price_scale":100,"scale_evidence_status":"QUALIFIED_SYNTHETIC"})
    assert out["source_equivalence"] == "UNRESOLVED"


def test_td03c_21_ledger_deterministic():
    m = _target()
    assert m.append_ledger_event([], _event()) == m.append_ledger_event([], _event())
    assert m.validate_ledger(_ledger(m))["status"] == "PASS_LEDGER"


def test_td03c_22_ledger_tampering_detected():
    m = _target()
    ledger=_ledger(m)
    ledger[0]["event_status"]="TAMPERED"
    assert m.validate_ledger(ledger)["status"] == "BLOCKED_LEDGER"


def test_td03c_23_retry_visible():
    m = _target()
    ledger=[]
    ledger=m.append_ledger_event(ledger,_event("ACQUISITION_FAILURE"))
    ledger=m.append_ledger_event(ledger,_event("ACQUISITION_REQUEST"))
    assert len(ledger) == 2
    assert ledger[0]["event_type"] == "ACQUISITION_FAILURE"
    assert ledger[1]["previous_event_digest"] == ledger[0]["event_digest"]


def test_td03c_24_performance_field_rejected():
    m = _target()
    e=_event(); e["pnl"]=1.0
    with pytest.raises(Exception):
        m.append_ledger_event([],e)


def test_td03c_25_inventory_order_and_duplicate_path():
    m = _target()
    a=_file("raw/b.bin",b"b","REQ-B")
    b=_file("raw/a.bin",b"a","REQ-A")
    assert m.canonical_inventory_digest([a,b]) == m.canonical_inventory_digest([b,a])
    with pytest.raises(Exception):
        m.canonical_inventory_digest([a,dict(a)])


def test_td03c_26_manifest_lane_b_only():
    m = _target()
    man=_manifest(m)
    assert m.validate_manifest(man)["status"] == "PASS_MANIFEST"
    man["dataset_id"]=SOURCE_B_DATASET_ID
    assert m.validate_manifest(man)["status"] == "BLOCKED_MANIFEST"


def test_td03c_27_premature_seal_blocks():
    m = _target()
    with pytest.raises(Exception):
        m.build_seal(manifest=_manifest(m), sealed_at_utc="2027-09-30T23:59:59Z", human_authority_reference="SYNTHETIC")


def test_td03c_28_post_seal_mutation_detected():
    m = _target()
    man=_manifest(m)
    seal=m.build_seal(manifest=man,sealed_at_utc="2027-10-01T00:00:01Z",human_authority_reference="SYNTHETIC")
    changed=dict(man); changed["total_rows"]=man["total_rows"]+1
    assert m.verify_seal(changed,seal)["status"] == "BLOCKED_POST_SEAL_MUTATION"


def test_td03c_29_similarity_cannot_authorize_equivalence_or_promotion():
    m = _target()
    claim={"same_provider_lineage":True,"same_instrument_description":True,"historical_overlap_study":"NOT_RUN"}
    assert m.assess_source_equivalence_claim(claim)["status"] == "BLOCKED_SOURCE_EQUIVALENCE"
    assert m.validate_source_b_promotion({"requested":True})["status"] == "BLOCKED_SOURCE_SUBSTITUTION"


def test_td03c_30_forbidden_surfaces_absent():
    m = _target()
    forbidden=set(CONTRACT_DOC["forbidden_runtime_surface"])
    assert forbidden.isdisjoint(set(dir(m)))

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-TD-03A-SOURCE-B-PROVENANCE-COLLECTOR-QUALIFICATION-CONTRACT-V0.1.json"
TARGET_PATH = ROOT / "tools/e1_td_03a_acquisition_collector.py"

CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
RUNTIME_CONTRACT = "ATDS_E1_TD_03A_ACQUISITION_COLLECTOR_V0_1"
DATASET_ID = "SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1"
WINDOW_START = "2026-10-01T00:00:00Z"
WINDOW_END = "2027-10-01T00:00:00Z"

assert CONTRACT_DOC["schema"] == "ATDS_E1_TD_03A_PROVENANCE_COLLECTOR_QUALIFICATION_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT_DOC["test_cases"]] == [f"TD03A-{i:02d}" for i in range(1, 31)]


def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("E1_TD_03A_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("e1_td_03a_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("E1_TD_03A_TARGET_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _provenance():
    return {
        "publisher_dataset": "CarlosSilva1/ustech-ticks",
        "economic_instrument": "USTECH",
        "instrument_description": "Nasdaq 100 Index CFD",
        "timestamp_semantics": "UTC tick time, millisecond precision",
        "price_fields": ["bid_price", "ask_price"],
        "publisher_declared_provenance": "Dukascopy via Tickstory",
        "license": "CC-BY-4.0",
        "status": "PASS_DOCUMENTARY_PROVENANCE",
        "limitations": [
            "native Dukascopy tick-for-tick equivalence not proven",
            "exact Tickstory transformations not proven",
            "third-party broker feed equivalence not proven",
            "volumes not qualified for this research path",
        ],
    }


def _files():
    return [
        {
            "relative_path": "year=2026/month=10/USTECH-2026-10-part0000.parquet",
            "sha256": hashlib.sha256(b"a").hexdigest(),
            "size_bytes": 1,
            "rows": 2,
            "first_timestamp_ms": 1790812800000,
            "last_timestamp_ms": 1790812860000,
            "schema_signature": "schema-v1",
            "source_request_id": "REQ-001",
        },
        {
            "relative_path": "year=2026/month=11/USTECH-2026-11-part0000.parquet",
            "sha256": hashlib.sha256(b"b").hexdigest(),
            "size_bytes": 1,
            "rows": 2,
            "first_timestamp_ms": 1793491200000,
            "last_timestamp_ms": 1793491260000,
            "schema_signature": "schema-v1",
            "source_request_id": "REQ-002",
        },
    ]


def _ledger(m):
    ledger = []
    ledger = m.append_ledger_event(
        ledger,
        {
            "event_timestamp_utc": "2026-10-01T00:00:01Z",
            "event_type": "ACQUISITION_REQUEST",
            "provider_lineage_id": "CarlosSilva1/ustech-ticks",
            "instrument_id": "USTECH",
            "source_request_id": "REQ-001",
            "requested_start_utc": "2026-10-01T00:00:00Z",
            "requested_end_utc": "2026-11-01T00:00:00Z",
            "object_relative_path": None,
            "object_sha256": None,
            "object_size_bytes": None,
            "parse_status": "NOT_APPLICABLE",
            "row_count": None,
            "first_timestamp_ms": None,
            "last_timestamp_ms": None,
            "schema_signature": None,
            "event_status": "REQUESTED",
        },
    )
    ledger = m.append_ledger_event(
        ledger,
        {
            "event_timestamp_utc": "2026-10-01T00:00:02Z",
            "event_type": "OBJECT_ACCEPTED",
            "provider_lineage_id": "CarlosSilva1/ustech-ticks",
            "instrument_id": "USTECH",
            "source_request_id": "REQ-001",
            "requested_start_utc": "2026-10-01T00:00:00Z",
            "requested_end_utc": "2026-11-01T00:00:00Z",
            "object_relative_path": _files()[0]["relative_path"],
            "object_sha256": _files()[0]["sha256"],
            "object_size_bytes": 1,
            "parse_status": "PASS",
            "row_count": 2,
            "first_timestamp_ms": 1790812800000,
            "last_timestamp_ms": 1790812860000,
            "schema_signature": "schema-v1",
            "event_status": "ACCEPTED",
        },
    )
    return ledger


def _manifest(m):
    return m.build_manifest(
        provenance_record=_provenance(),
        files=_files(),
        ledger=_ledger(m),
        runtime_environment={"python": "3.12.14", "platform": "synthetic"},
        created_at_utc="2027-10-01T00:00:01Z",
    )


def test_td03a_01_runtime_contract_and_surface():
    m = _target()
    assert m.CONTRACT == RUNTIME_CONTRACT
    required = set(CONTRACT_DOC["required_runtime_surface"])
    assert required.issubset(set(dir(m)))


def test_td03a_02_dataset_identity_and_window_exact():
    m = _target()
    assert m.DATASET_ID == DATASET_ID
    assert m.WINDOW_START == WINDOW_START
    assert m.WINDOW_END == WINDOW_END


def test_td03a_03_documented_provenance_accepted():
    m = _target()
    assert m.validate_provenance(_provenance()) == {"status": "PASS_PROVENANCE"}


def test_td03a_04_provider_substitution_blocked():
    m = _target()
    p = _provenance()
    p["publisher_dataset"] = "Other/provider"
    assert m.validate_provenance(p)["status"] == "BLOCKED_SOURCE_PROVENANCE"


def test_td03a_05_native_equivalence_limitation_retained():
    m = _target()
    assert "native Dukascopy tick-for-tick equivalence not proven" in m.PROVENANCE["limitations"]


def test_td03a_06_exact_byte_hash_pass():
    m = _target()
    raw = b"synthetic-source-object"
    expected = hashlib.sha256(raw).hexdigest()
    out = m.verify_raw_object(raw, expected_sha256=expected, expected_size=len(raw))
    assert out == {"status": "PASS_OBJECT_INTEGRITY", "sha256": expected, "size_bytes": len(raw)}


def test_td03a_07_one_byte_mutation_blocks():
    m = _target()
    raw = b"synthetic-source-object"
    expected = hashlib.sha256(raw).hexdigest()
    out = m.verify_raw_object(raw + b"x", expected_sha256=expected, expected_size=len(raw))
    assert out["status"] == "BLOCKED_RAW_OBJECT_HASH"


def test_td03a_08_missing_file_field_blocks():
    m = _target()
    files = _files()
    del files[0]["schema_signature"]
    with pytest.raises(m.TD03AError, match="FILE_RECORD_FIELDS"):
        m.canonical_inventory_digest(files)


def test_td03a_09_duplicate_relative_path_blocks():
    m = _target()
    files = _files()
    files[1]["relative_path"] = files[0]["relative_path"]
    with pytest.raises(m.TD03AError, match="DUPLICATE_RELATIVE_PATH"):
        m.canonical_inventory_digest(files)


def test_td03a_10_non_increasing_timestamp_blocks():
    m = _target()
    rows = [
        {"timestamp": 1000, "bid_price": 10.0, "ask_price": 11.0},
        {"timestamp": 999, "bid_price": 10.0, "ask_price": 11.0},
    ]
    with pytest.raises(m.TD03AError, match="NON_INCREASING_SOURCE_TIMESTAMP"):
        m.inspect_source_rows(rows)


def test_td03a_11_gap_gt_60000_inventoried():
    m = _target()
    rows = [
        {"timestamp": 1000, "bid_price": 10.0, "ask_price": 11.0},
        {"timestamp": 61001, "bid_price": 10.0, "ask_price": 11.0},
    ]
    assert m.inspect_source_rows(rows)["gap_gt_60000ms_count"] == 1


def test_td03a_12_gap_eq_60000_not_forbidden():
    m = _target()
    rows = [
        {"timestamp": 1000, "bid_price": 10.0, "ask_price": 11.0},
        {"timestamp": 61000, "bid_price": 10.0, "ask_price": 11.0},
    ]
    assert m.inspect_source_rows(rows)["gap_gt_60000ms_count"] == 0


def test_td03a_13_ledger_chain_deterministic():
    m = _target()
    a = _ledger(m)
    b = _ledger(m)
    assert a == b
    assert m.validate_ledger(a) == {"status": "PASS_COLLECTION_LEDGER", "events": 2}


def test_td03a_14_ledger_tampering_detected():
    m = _target()
    ledger = _ledger(m)
    ledger[0]["event_status"] = "TAMPERED"
    assert m.validate_ledger(ledger)["status"] == "BLOCKED_LEDGER"


def test_td03a_15_retry_remains_ledger_visible():
    m = _target()
    ledger = []
    base = {
        "provider_lineage_id": "CarlosSilva1/ustech-ticks",
        "instrument_id": "USTECH",
        "source_request_id": "REQ-X",
        "requested_start_utc": WINDOW_START,
        "requested_end_utc": "2026-10-02T00:00:00Z",
        "object_relative_path": None,
        "object_sha256": None,
        "object_size_bytes": None,
        "parse_status": "NOT_APPLICABLE",
        "row_count": None,
        "first_timestamp_ms": None,
        "last_timestamp_ms": None,
        "schema_signature": None,
    }
    ledger = m.append_ledger_event(ledger, dict(base, event_timestamp_utc="2026-10-01T00:00:01Z", event_type="ACQUISITION_FAILURE", event_status="FAILED"))
    ledger = m.append_ledger_event(ledger, dict(base, event_timestamp_utc="2026-10-01T00:00:02Z", event_type="ACQUISITION_REQUEST", event_status="RETRY_REQUESTED"))
    assert [x["event_type"] for x in ledger] == ["ACQUISITION_FAILURE", "ACQUISITION_REQUEST"]


def test_td03a_16_performance_fields_rejected_from_ledger():
    m = _target()
    event = {
        "event_timestamp_utc": "2026-10-01T00:00:01Z",
        "event_type": "ACQUISITION_REQUEST",
        "provider_lineage_id": "CarlosSilva1/ustech-ticks",
        "instrument_id": "USTECH",
        "source_request_id": "REQ-001",
        "requested_start_utc": WINDOW_START,
        "requested_end_utc": "2026-10-02T00:00:00Z",
        "object_relative_path": None,
        "object_sha256": None,
        "object_size_bytes": None,
        "parse_status": "NOT_APPLICABLE",
        "row_count": None,
        "first_timestamp_ms": None,
        "last_timestamp_ms": None,
        "schema_signature": None,
        "event_status": "REQUESTED",
        "pnl": 123.0,
    }
    with pytest.raises(m.TD03AError, match="FORBIDDEN_PERFORMANCE_FIELD"):
        m.append_ledger_event([], event)


def test_td03a_17_inventory_order_independent():
    m = _target()
    files = _files()
    assert m.canonical_inventory_digest(files) == m.canonical_inventory_digest(list(reversed(files)))


def test_td03a_18_file_hash_mutation_changes_inventory():
    m = _target()
    a = _files()
    b = _files()
    b[0]["sha256"] = "0" * 64
    assert m.canonical_inventory_digest(a) != m.canonical_inventory_digest(b)


def test_td03a_19_manifest_deterministic():
    m = _target()
    assert _manifest(m) == _manifest(m)
    assert m.canonical_sha256(_manifest(m)) == m.canonical_sha256(_manifest(m))


def test_td03a_20_unknown_manifest_identity_field_blocks():
    m = _target()
    manifest = _manifest(m)
    manifest["surprise_identity_field"] = "x"
    assert m.validate_manifest(manifest)["status"] == "BLOCKED_MANIFEST"


def test_td03a_21_outside_window_rows_not_evaluation_eligible():
    m = _target()
    start_ms = 1790812800000
    end_ms = 1822348800000
    rows = [
        {"timestamp": start_ms - 1},
        {"timestamp": start_ms},
        {"timestamp": end_ms - 1},
        {"timestamp": end_ms},
    ]
    assert [m.is_evaluation_eligible(x["timestamp"]) for x in rows] == [False, True, True, False]


def test_td03a_22_premature_seal_blocks():
    m = _target()
    manifest = _manifest(m)
    with pytest.raises(m.TD03AError, match="PREMATURE_SEAL"):
        m.build_seal(
            manifest=manifest,
            sealed_at_utc="2027-09-30T23:59:59Z",
            human_authority_reference="SYNTHETIC",
        )


def test_td03a_23_final_seal_binds_manifest_inventory_ledger():
    m = _target()
    manifest = _manifest(m)
    seal = m.build_seal(
        manifest=manifest,
        sealed_at_utc="2027-10-01T00:00:00Z",
        human_authority_reference="SYNTHETIC",
    )
    assert seal["manifest_sha256"] == m.canonical_sha256(manifest)
    assert seal["canonical_inventory_digest"] == manifest["canonical_inventory_digest"]
    assert seal["acquisition_ledger_final_digest"] == manifest["acquisition_ledger_final_digest"]


def test_td03a_24_post_seal_manifest_mutation_detected():
    m = _target()
    manifest = _manifest(m)
    seal = m.build_seal(
        manifest=manifest,
        sealed_at_utc="2027-10-01T00:00:00Z",
        human_authority_reference="SYNTHETIC",
    )
    mutated = dict(manifest)
    mutated["total_rows"] += 1
    assert m.verify_seal(mutated, seal)["status"] == "BLOCKED_POST_SEAL_MUTATION"


def test_td03a_25_no_strategy_performance_surface():
    m = _target()
    for name in CONTRACT_DOC["forbidden_runtime_surface"]:
        assert not hasattr(m, name)


def test_td03a_26_no_network_acquisition_implementation_exposed():
    _target()
    src = TARGET_PATH.read_text(encoding="utf-8")
    forbidden = ("requests", "urllib.request", "httpx", "aiohttp", "socket.")
    assert all(x not in src for x in forbidden)


def test_td03a_27_no_h1_construction_surface():
    m = _target()
    assert not hasattr(m, "derive_h1_dataset")
    assert not hasattr(m, "build_h1")


def test_td03a_28_no_automatic_provider_substitution_surface():
    m = _target()
    assert not hasattr(m, "fallback_provider")
    assert not hasattr(m, "substitute_provider")


def test_td03a_29_canonical_json_forbids_nonfinite():
    m = _target()
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.nan})
    with pytest.raises(ValueError):
        m.canonical_json_bytes({"x": math.inf})


def test_td03a_30_no_performance_authority():
    m = _target()
    assert m.AUTHORITY["actual_data_acquisition"] is False
    assert m.AUTHORITY["new_data_observation"] is False
    assert m.AUTHORITY["dataset_materialization"] is False
    assert m.AUTHORITY["h1_build"] is False
    assert m.AUTHORITY["momentum_execution"] is False
    assert m.AUTHORITY["performance_computation"] is False
    assert m.AUTHORITY["backtest"] is False

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from tools.ao_e0_b12_data01_fc01_jf01 import canonicalize_ticks
from tools.e1_td_03c_jf02_evidence import (
    FROZEN_REQUEST,
    JF02Blocked,
    build_receipt,
    compare_repeat_reads,
    evidence_identity_sha256,
    request_manifest_bytes,
    summarize_payload,
)

START = datetime(2025, 10, 1, 14, 0, 0, tzinfo=timezone.utc)
END = datetime(2025, 10, 1, 15, 0, 0, tzinfo=timezone.utc)
START_MS = int(START.timestamp() * 1000)


def tick(ms, ask=25000.5, bid=25000.0, ask_volume=1.25, bid_volume=1.5):
    return {
        "time_ms": ms,
        "ask": ask,
        "bid": bid,
        "askVolume": ask_volume,
        "bidVolume": bid_volume,
    }


def payload():
    return canonicalize_ticks(
        [
            tick(START_MS + 1),
            tick(START_MS + 1, ask=25000.6, bid=25000.1),
            tick(START_MS + 500),
        ],
        interval_start=START,
        interval_end_exclusive=END,
    )


def test_frozen_request_exact_interval_and_no_retry():
    assert FROZEN_REQUEST["jforex_from_ms"] == 1759327200000
    assert FROZEN_REQUEST["jforex_to_ms_inclusive"] == 1759330799999
    assert FROZEN_REQUEST["automatic_request_retries"] == 0
    assert FROZEN_REQUEST["environment"] == "DEMO"


def test_request_manifest_is_deterministic_json():
    first = request_manifest_bytes()
    second = request_manifest_bytes()
    assert first == second
    parsed = json.loads(first)
    assert parsed["instrument_jforex"] == "USATECH.IDX/USD"


def test_evidence_identity_binds_request_and_payload():
    p = payload()
    assert evidence_identity_sha256(p) == evidence_identity_sha256(p)


def test_summary_preserves_equal_timestamp_provider_order():
    p = payload()
    s = summarize_payload(p)
    assert s.tick_count == 3
    assert s.first_timestamp == "2025-10-01T14:00:00.001Z"
    assert s.last_timestamp == "2025-10-01T14:00:00.500Z"


def test_repeat_identical_reads_pass():
    p = payload()
    result = compare_repeat_reads(p, p)
    assert result["byte_identical"] is True


def test_repeat_mismatch_breaker():
    a = payload()
    b = canonicalize_ticks(
        [tick(START_MS + 1), tick(START_MS + 501)],
        interval_start=START,
        interval_end_exclusive=END,
    )
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_REPEAT_RESPONSE_MISMATCH"):
        compare_repeat_reads(a, b)


def test_empty_response_breaker():
    empty = b"timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_EMPTY_RESPONSE"):
        summarize_payload(empty)


def test_crlf_breaker():
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_LINE_ENDING"):
        summarize_payload(payload().replace(b"\n", b"\r\n"))


def test_bom_breaker():
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_BOM"):
        summarize_payload(b"\xef\xbb\xbf" + payload())


def test_schema_breaker():
    bad = payload().replace(b"askPrice", b"ask")
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_SCHEMA_DRIFT"):
        summarize_payload(bad)


def test_api_version_must_be_bound():
    with pytest.raises(JF02Blocked, match="BLOCKED_JF02_API_VERSION_UNBOUND"):
        build_receipt(
            payload(),
            api_version="",
            run_label="READ_A",
            acquisition_started_utc="2026-10-09T00:00:00Z",
            acquisition_finished_utc="2026-10-09T00:00:01Z",
        )


def test_receipt_never_claims_raw_object_or_source_b_equivalence():
    r = build_receipt(
        payload(),
        api_version="TEST",
        run_label="READ_A",
        acquisition_started_utc="2026-10-09T00:00:00Z",
        acquisition_finished_utc="2026-10-09T00:00:01Z",
    )
    assert r["raw_provider_object_claim"] is False
    assert r["source_b_equivalence_claim"] is False

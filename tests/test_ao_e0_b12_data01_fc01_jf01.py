from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.data.dataset_admissibility import assess, build_identity
from src.data.tick_reader import load
from tools.ao_e0_b12_data01_fc01_jf01 import (
    CSV_HEADER,
    JF01Blocked,
    JFOREX_INSTRUMENT_STRING,
    bind_instrument,
    canonicalize_ticks,
    jforex_interval_ms,
    payload_sha256,
)

START = datetime(2026, 10, 8, 8, 0, 0, tzinfo=timezone.utc)
END = START + timedelta(hours=1)
START_MS = int(START.timestamp() * 1000)
END_MS = int(END.timestamp() * 1000)


def tick(ms, ask=25000.5, bid=25000.0, ask_volume=1.25, bid_volume=1.5):
    return {
        "time_ms": ms,
        "ask": ask,
        "bid": bid,
        "askVolume": ask_volume,
        "bidVolume": bid_volume,
    }


def test_instrument_binding_pass():
    assert bind_instrument(JFOREX_INSTRUMENT_STRING) == JFOREX_INSTRUMENT_STRING


def test_jf_s09_null_instrument_breaker():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_NULL_INSTRUMENT"):
        bind_instrument(None)


def test_instrument_identity_mismatch_breaker():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_IDENTITY_MISMATCH"):
        bind_instrument("EUR/USD")


def test_interval_translation_inclusive_to():
    assert jforex_interval_ms(START, END) == (START_MS, END_MS - 1)


def test_jf_s01_normal_multi_tick_hour():
    payload = canonicalize_ticks(
        [tick(START_MS + 1), tick(START_MS + 500), tick(START_MS + 1000)],
        interval_start=START,
        interval_end_exclusive=END,
    )
    text = payload.decode("utf-8")
    assert text.startswith(CSV_HEADER)
    assert text.count("\n") == 4


def test_jf_s02_tick_exactly_at_start():
    payload = canonicalize_ticks([tick(START_MS)], interval_start=START, interval_end_exclusive=END)
    assert b"2026-10-08T08:00:00.000Z" in payload


def test_jf_s03_tick_at_end_minus_1_ms():
    payload = canonicalize_ticks([tick(END_MS - 1)], interval_start=START, interval_end_exclusive=END)
    assert b"2026-10-08T08:59:59.999Z" in payload


def test_jf_s04_tick_exactly_at_end_breaker():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_INTERVAL_LEAK"):
        canonicalize_ticks([tick(END_MS)], interval_start=START, interval_end_exclusive=END)


def test_jf_s05_same_timestamp_ticks_preserved_in_provider_order():
    first = tick(START_MS + 10, ask=25000.2, bid=25000.1)
    second = tick(START_MS + 10, ask=25000.4, bid=25000.3)
    payload = canonicalize_ticks([first, second], interval_start=START, interval_end_exclusive=END)
    rows = payload.decode("utf-8").splitlines()[1:]
    assert len(rows) == 2
    assert ",25000.2,25000.1," in rows[0]
    assert ",25000.4,25000.3," in rows[1]


def test_jf_s06_decreasing_timestamp_breaker():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_SOURCE_ORDERING"):
        canonicalize_ticks(
            [tick(START_MS + 20), tick(START_MS + 10)],
            interval_start=START,
            interval_end_exclusive=END,
        )


def test_jf_s07_ask_below_bid_fails():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_ASK_BELOW_BID"):
        canonicalize_ticks(
            [tick(START_MS + 1, ask=24999.0, bid=25000.0)],
            interval_start=START,
            interval_end_exclusive=END,
        )


def test_jf_s08_negative_volume_fails():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_NEGATIVE_VOLUME"):
        canonicalize_ticks(
            [tick(START_MS + 1, ask_volume=-0.1)],
            interval_start=START,
            interval_end_exclusive=END,
        )


def test_jf_s10_empty_valid_market_hour():
    payload = canonicalize_ticks([], interval_start=START, interval_end_exclusive=END)
    assert payload == CSV_HEADER.encode("utf-8")


def test_nonfinite_value_breaker():
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_NONFINITE_VALUE"):
        canonicalize_ticks(
            [tick(START_MS + 1, ask=float("nan"))],
            interval_start=START,
            interval_end_exclusive=END,
        )


def test_schema_drift_breaker():
    malformed = tick(START_MS + 1)
    malformed["extra"] = 1
    with pytest.raises(JF01Blocked, match="BLOCKED_JF01_SCHEMA_DRIFT"):
        canonicalize_ticks([malformed], interval_start=START, interval_end_exclusive=END)


def test_deterministic_payload_and_sha256():
    source = [tick(START_MS + 1), tick(START_MS + 2, ask=25001.0, bid=25000.5)]
    first = canonicalize_ticks(source, interval_start=START, interval_end_exclusive=END)
    second = canonicalize_ticks(source, interval_start=START, interval_end_exclusive=END)
    assert first == second
    assert payload_sha256(first) == payload_sha256(second)


def test_downstream_tick_reader_and_dataset_admissibility(tmp_path):
    payload = canonicalize_ticks(
        [tick(START_MS), tick(START_MS + 1234, ask=25001.5, bid=25001.0)],
        interval_start=START,
        interval_end_exclusive=END,
    )
    path = tmp_path / "jf01.csv"
    path.write_bytes(payload)

    rows = list(load(path))
    assert len(rows) == 2
    assert rows[0].timestamp == "2026-10-08T08:00:00.000Z"

    identity = build_identity(
        path,
        dataset_id="JF01-SYNTHETIC",
        dataset_version="V0.1",
        instrument="USATECH.IDX-USD",
        granularity="TICK",
        timezone_storage="UTC",
    )
    report = assess(path, identity=identity)
    assert report.verdict == "PASS"


def test_no_bom_crlf_or_extra_columns():
    payload = canonicalize_ticks([tick(START_MS)], interval_start=START, interval_end_exclusive=END)
    assert not payload.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in payload
    assert payload.splitlines()[0] == b"timestamp,askPrice,bidPrice,askVolume,bidVolume"


def test_source_mapping_key_order_is_not_semantic():
    reordered = {
        "bidVolume": 1.5,
        "askVolume": 1.25,
        "bid": 25000.0,
        "ask": 25000.5,
        "time_ms": START_MS,
    }
    payload = canonicalize_ticks([reordered], interval_start=START, interval_end_exclusive=END)
    assert payload.splitlines()[0] == b"timestamp,askPrice,bidPrice,askVolume,bidVolume"

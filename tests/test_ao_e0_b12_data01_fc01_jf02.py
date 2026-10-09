from pathlib import Path
from tools.ao_e0_b12_data01_fc01_jf02 import FROM_MS, TO_MS_INCLUSIVE, validate_canonical_payload, compare_reads


def sample(ms):
    from datetime import datetime, timezone
    ts = datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:23] + "Z"
    return f"{ts},25000.5,25000.0,1.25,1.5\n"


def test_fixed_interval_constants():
    assert FROM_MS == 1791446400000
    assert TO_MS_INCLUSIVE == 1791449999999


def test_real_payload_validator_and_parity(tmp_path):
    raw = "timestamp,askPrice,bidPrice,askVolume,bidVolume\n" + sample(FROM_MS) + sample(TO_MS_INCLUSIVE)
    a = tmp_path / "a.csv"; b = tmp_path / "b.csv"
    a.write_text(raw, encoding="utf-8", newline="")
    b.write_text(raw, encoding="utf-8", newline="")
    result = compare_reads(a, b)
    assert result["byte_parity"]
    assert result["sha256_parity"]
    assert result["a"]["tick_count"] == 2


def test_out_of_interval_fails(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("timestamp,askPrice,bidPrice,askVolume,bidVolume\n" + sample(TO_MS_INCLUSIVE + 1), encoding="utf-8", newline="")
    try:
        validate_canonical_payload(p)
        assert False
    except ValueError as exc:
        assert str(exc) == "INTERVAL_LEAK"

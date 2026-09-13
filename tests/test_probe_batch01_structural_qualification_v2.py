import importlib.util
import lzma
import struct
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "tools" / "probe_batch01_structural_qualification_v2.py"
spec = importlib.util.spec_from_file_location("batch01_probe", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def write_bi5(path: Path, records):
    raw = b"".join(module.BI5_STRUCT.pack(*record) for record in records)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(lzma.compress(raw, format=lzma.FORMAT_ALONE))


def valid_record(ms=0, ask=2000000, bid=1999990, ask_volume=1.0, bid_volume=2.0):
    return (ms, ask, bid, ask_volume, bid_volume)


def test_valid_file_is_qualified(tmp_path):
    root = tmp_path / "corpus"
    path = root / "2025-08-20_14h" / "ticks.bi5"
    write_bi5(path, [valid_record(0), valid_record(1000)])

    result = module.qualify_file(path, root)

    assert result["status"] == "PASS"
    assert result["record_count"] == 2
    assert result["first_timestamp"].endswith("14:00:00+00:00")
    assert result["last_timestamp"].endswith("14:00:01+00:00")
    assert len(result["sha256"]) == 64


def test_decompressed_size_not_multiple_of_20_fails(tmp_path):
    root = tmp_path / "corpus"
    path = root / "2025-08-20_14h" / "ticks.bi5"
    path.parent.mkdir(parents=True)
    path.write_bytes(lzma.compress(b"x" * 21, format=lzma.FORMAT_ALONE))

    result = module.qualify_file(path, root)

    assert result["status"] == "FAIL"
    assert "DECOMPRESSED_SIZE_NOT_MULTIPLE_OF_20" in result["errors"]


def test_millisecond_offset_out_of_range_fails(tmp_path):
    root = tmp_path / "corpus"
    path = root / "2025-08-20_14h" / "ticks.bi5"
    write_bi5(path, [valid_record(3_600_000)])

    result = module.qualify_file(path, root)

    assert result["status"] == "FAIL"
    assert any("MILLISECOND_OFFSET_OUT_OF_RANGE" in e for e in result["errors"])


def test_internal_timestamp_regression_fails(tmp_path):
    root = tmp_path / "corpus"
    path = root / "2025-08-20_14h" / "ticks.bi5"
    write_bi5(path, [valid_record(2000), valid_record(1000)])

    result = module.qualify_file(path, root)

    assert result["status"] == "FAIL"
    assert any("INTERNAL_TIMESTAMP_ORDER_VIOLATION" in e for e in result["errors"])


def test_invalid_quote_fails(tmp_path):
    root = tmp_path / "corpus"
    path = root / "2025-08-20_14h" / "ticks.bi5"
    write_bi5(path, [valid_record(0, ask=1990000, bid=2000000)])

    result = module.qualify_file(path, root)

    assert result["status"] == "FAIL"
    assert any("INVALID_QUOTE" in e for e in result["errors"])

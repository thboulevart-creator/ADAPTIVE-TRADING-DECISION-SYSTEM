from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

RUNTIME_PATH = Path(
    os.environ.get(
        "E1_03_H1_RUNTIME_PATH",
        str(ROOT / "tools/e1_03_h1_dataset_identity.py"),
    )
)

CONTRACT_PATH = ROOT / "GOVERNANCE/E1-03-H1-DATASET-IDENTITY-CONTRACT-V0.1.json"
EXPECTED_CONTRACT_BLOB = "c2d4323039d65fcd9319d4f5eb02f45ee27c8afc"
RUNTIME_CONTRACT = "ATDS_E1_03_H1_DATASET_IDENTITY_V0_1"
OOS_START_MS = 1748131200000
HOUR_MS = 3_600_000
MINUTE_MS = 60_000


def _git_blob_sha1(raw: bytes) -> str:
    h = hashlib.sha1()
    h.update(f"blob {len(raw)}\0".encode("ascii"))
    h.update(raw)
    return h.hexdigest()


_CONTRACT_RAW = CONTRACT_PATH.read_bytes()
assert _git_blob_sha1(_CONTRACT_RAW) == EXPECTED_CONTRACT_BLOB
_CONTRACT = json.loads(_CONTRACT_RAW.decode("utf-8"))
assert _CONTRACT["schema"] == "ATDS_E1_03_H1_DATASET_IDENTITY_CONTRACT_V0_1"
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"H1-{i:02d}" for i in range(1, 22)]
assert len(_CONTRACT["test_cases"]) == 21


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail(
            "E1_03_H1_TRANSFORMER_ABSENT_EXPECTED_RED",
            pytrace=False,
        )

    spec = importlib.util.spec_from_file_location(
        "e1_03_h1_dataset_identity_under_test",
        RUNTIME_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail(
            "E1_03_H1_TRANSFORMER_UNLOADABLE_EXPECTED_RED",
            pytrace=False,
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    required = (
        "CONTRACT",
        "derive_h1_dataset",
        "canonical_stream_sha256",
        "verify_ap0_binding",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(
            f"E1_03_H1_SURFACE_INCOMPLETE_EXPECTED_RED:{missing}",
            pytrace=False,
        )

    assert module.CONTRACT == RUNTIME_CONTRACT
    return module


def _minute(ts: int, *, segment: int = 0, start: bool = False, close: float = 100.0):
    return {
        "minute_start_ms_utc": ts,
        "first_tick_ms": ts + 1,
        "last_tick_ms": ts + MINUTE_MS - 1,
        "tick_count": 2,
        "segment_id": segment,
        "segment_start": start,
        "gap_before_ms": None,
        "mid_close": float(close),
    }


def _hour(
    start: int,
    *,
    segment: int = 0,
    segment_start: bool = False,
    close_base: float = 100.0,
):
    return [
        _minute(
            start + i * MINUTE_MS,
            segment=segment,
            start=(segment_start and i == 0),
            close=close_base + i / 1000.0,
        )
        for i in range(60)
    ]


def _derive(module, rows, *, raw_start=None, raw_end=None):
    if raw_start is None:
        raw_start = min(r["minute_start_ms_utc"] for r in rows) - HOUR_MS
    if raw_end is None:
        raw_end = max(r["minute_start_ms_utc"] for r in rows) + 2 * HOUR_MS
    return module.derive_h1_dataset(
        copy.deepcopy(rows),
        raw_window_start_ms=int(raw_start),
        raw_window_end_ms=int(raw_end),
    )


def _rows(result):
    assert result["status"] == "PASS"
    return result["rows"]


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def test_h1_01_exact_60_minutes_same_segment_accepts():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    out = _rows(_derive(m, _hour(start)))
    assert len(out) == 1
    assert out[0]["h1_start_ms_utc"] == start


def test_h1_02_59_minutes_rejects_hour():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    out = _rows(_derive(m, _hour(start)[:-1]))
    assert out == []


def test_h1_03_duplicate_minute_blocks():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    rows.append(copy.deepcopy(rows[-1]))
    result = _derive(m, rows)
    assert result["status"] == "BLOCKED"


def test_h1_04_wrong_minute_inside_bucket_rejects_hour():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    rows[30]["minute_start_ms_utc"] += MINUTE_MS
    result = _derive(m, rows)
    if result["status"] == "BLOCKED":
        assert True
    else:
        assert result["rows"] == []


def test_h1_05_segment_change_inside_hour_rejects():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    for i in range(30, 60):
        rows[i]["segment_id"] = 1
    rows[30]["segment_start"] = True
    out = _rows(_derive(m, rows))
    assert out == []


def test_h1_06_segment_start_at_minute_zero_accepts_and_resets():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start, segment=0) + _hour(
        start + HOUR_MS,
        segment=1,
        segment_start=True,
        close_base=200.0,
    )
    out = _rows(_derive(m, rows))
    assert len(out) == 2
    assert out[1]["continuity_block_id"] != out[0]["continuity_block_id"]
    assert out[1]["continuity_ordinal"] == 0


def test_h1_07_segment_start_after_minute_zero_rejects():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    rows[27]["segment_start"] = True
    out = _rows(_derive(m, rows))
    assert out == []


def test_h1_08_first_raw_boundary_hour_rejected():
    m = _runtime()
    start = OOS_START_MS - 72 * HOUR_MS
    rows = _hour(start) + _hour(start + HOUR_MS) + _hour(start + 2 * HOUR_MS)
    result = _derive(
        m,
        rows,
        raw_start=start + 1,
        raw_end=start + 4 * HOUR_MS,
    )
    out = _rows(result)
    assert [r["h1_start_ms_utc"] for r in out] == [start + HOUR_MS, start + 2 * HOUR_MS]


def test_h1_09_last_raw_boundary_hour_rejected():
    m = _runtime()
    start = OOS_START_MS - 72 * HOUR_MS
    rows = _hour(start) + _hour(start + HOUR_MS) + _hour(start + 2 * HOUR_MS)
    result = _derive(
        m,
        rows,
        raw_start=start - HOUR_MS,
        raw_end=start + 3 * HOUR_MS - 1,
    )
    out = _rows(result)
    assert [r["h1_start_ms_utc"] for r in out] == [start, start + HOUR_MS]


def test_h1_10_missing_minute_is_not_forward_filled():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    del rows[17]
    out = _rows(_derive(m, rows))
    assert out == []


def test_h1_11_h1_close_is_exact_minute_59_mid_close():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start)
    rows[-1]["mid_close"] = 321.125
    out = _rows(_derive(m, rows))
    assert len(out) == 1
    assert out[0]["mid_close"] == 321.125


def test_h1_12_continuity_block_change_resets_ordinal():
    m = _runtime()
    start = OOS_START_MS - 72 * HOUR_MS
    rows = _hour(start) + _hour(start + HOUR_MS)
    rows += _hour(start + 3 * HOUR_MS, close_base=300.0)
    out = _rows(_derive(m, rows))
    assert len(out) == 3
    assert out[0]["continuity_ordinal"] == 0
    assert out[1]["continuity_ordinal"] == 1
    assert out[2]["continuity_block_id"] != out[1]["continuity_block_id"]
    assert out[2]["continuity_ordinal"] == 0


def test_h1_13_ordinal_19_is_momentum_ineligible():
    m = _runtime()
    start = OOS_START_MS - 96 * HOUR_MS
    rows = []
    for i in range(20):
        rows += _hour(start + i * HOUR_MS, close_base=100.0 + i)
    result = _derive(m, rows)
    out = _rows(result)
    assert out[-1]["continuity_ordinal"] == 19
    assert result["manifest"]["momentum_eligible_h1_rows"] == 0


def test_h1_14_ordinal_20_is_first_momentum_eligible():
    m = _runtime()
    start = OOS_START_MS - 96 * HOUR_MS
    rows = []
    for i in range(21):
        rows += _hour(start + i * HOUR_MS, close_base=100.0 + i)
    result = _derive(m, rows)
    out = _rows(result)
    assert out[-1]["continuity_ordinal"] == 20
    assert result["manifest"]["momentum_eligible_h1_rows"] == 1


def test_h1_15_t_minus_20_across_block_is_forbidden():
    m = _runtime()
    start = OOS_START_MS - 96 * HOUR_MS
    rows = []
    for i in range(10):
        rows += _hour(start + i * HOUR_MS, segment=0, close_base=100.0 + i)
    for i in range(10, 21):
        rows += _hour(
            start + i * HOUR_MS,
            segment=1,
            segment_start=(i == 10),
            close_base=200.0 + i,
        )
    result = _derive(m, rows)
    out = _rows(result)
    assert out[-1]["continuity_ordinal"] == 10
    assert result["manifest"]["momentum_eligible_h1_rows"] == 0


def test_h1_16_exact_oos_start_classifies_as_oos():
    m = _runtime()
    result = _derive(m, _hour(OOS_START_MS))
    out = _rows(result)
    assert len(out) == 1
    assert result["manifest"]["pre_oos_h1_rows"] == 0
    assert result["manifest"]["oos_h1_rows"] == 1


def test_h1_17_oos_can_use_prior_same_block_warmup():
    m = _runtime()
    start = OOS_START_MS - 20 * HOUR_MS
    rows = []
    for i in range(21):
        rows += _hour(start + i * HOUR_MS, close_base=100.0 + i)
    result = _derive(m, rows)
    out = _rows(result)
    assert out[-1]["h1_start_ms_utc"] == OOS_START_MS
    assert out[-1]["continuity_ordinal"] == 20
    assert result["manifest"]["oos_h1_rows"] == 1
    assert result["manifest"]["momentum_eligible_h1_rows"] == 1


def _write_synthetic_binding(tmp_path: Path):
    root = tmp_path / "ap0"
    root.mkdir()
    files = []
    for i in range(61):
        rel = f"f{i:02d}.parquet"
        raw = f"synthetic-ap0-{i:02d}".encode("ascii")
        (root / rel).write_bytes(raw)
        files.append({
            "path": rel,
            "sha256": _sha256(raw),
            "size_bytes": len(raw),
        })
    manifest = {
        "status": "AP0_COMPLETE",
        "output_identity": "USTECH_PROFILE_MINUTE_CORE_V0_1",
        "files": files,
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_raw = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    manifest_path.write_bytes(manifest_raw)
    return root, manifest_path, _sha256(manifest_raw)


def test_h1_18_ap0_manifest_hash_mutation_blocks(tmp_path):
    m = _runtime()
    root, manifest, expected = _write_synthetic_binding(tmp_path)
    bad = ("0" if expected[0] != "0" else "1") + expected[1:]
    result = m.verify_ap0_binding(
        manifest,
        root,
        expected_manifest_sha256=bad,
    )
    assert result["status"] == "BLOCKED"


def test_h1_19_one_ap0_file_hash_mutation_blocks(tmp_path):
    m = _runtime()
    root, manifest, expected = _write_synthetic_binding(tmp_path)
    (root / "f17.parquet").write_bytes(b"mutated")
    result = m.verify_ap0_binding(
        manifest,
        root,
        expected_manifest_sha256=expected,
    )
    assert result["status"] == "BLOCKED"


def test_h1_20_identical_builds_have_same_canonical_digest():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _hour(start) + _hour(start + HOUR_MS)
    a = _rows(_derive(m, rows))
    b = _rows(_derive(m, rows))
    assert a == b
    assert m.canonical_stream_sha256(a) == m.canonical_stream_sha256(b)


def test_h1_21_one_h1_row_mutation_changes_canonical_digest():
    m = _runtime()
    start = OOS_START_MS - 48 * HOUR_MS
    rows = _rows(_derive(m, _hour(start)))
    baseline = m.canonical_stream_sha256(rows)
    mutant = copy.deepcopy(rows)
    mutant[0]["mid_close"] += 0.125
    changed = m.canonical_stream_sha256(mutant)
    assert baseline != changed

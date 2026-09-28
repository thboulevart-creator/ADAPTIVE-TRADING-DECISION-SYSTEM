from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = Path(
    os.environ.get(
        "E1_03_H1_RUNTIME_PATH",
        str(ROOT / "tools/e1_03_h1_dataset_identity.py"),
    )
)

RUNTIME_CONTRACT = "ATDS_E1_03_H1_DATASET_IDENTITY_V0_1"
REAL_AP0_SCHEMA = "ATDS_AP0_USTECH_PROFILE_MINUTE_CORE_MANIFEST_V0_1"
REAL_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("E1_03_RUNTIME_ABSENT", pytrace=False)
    spec = importlib.util.spec_from_file_location(
        "e1_03_real_ap0_manifest_compatibility_under_test",
        RUNTIME_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail("E1_03_RUNTIME_UNLOADABLE", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.CONTRACT == RUNTIME_CONTRACT
    assert hasattr(module, "verify_ap0_binding")
    return module


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _month_sequence():
    year, month = 2021, 5
    out = []
    for _ in range(61):
        out.append((year, month))
        month += 1
        if month == 13:
            year += 1
            month = 1
    return out


def test_rc01_real_ap0_manifest_relative_path_is_accepted(tmp_path):
    module = _runtime()
    root = tmp_path / "ap0"
    root.mkdir()

    files = []
    for i, (year, month) in enumerate(_month_sequence()):
        rel = (
            f"year={year:04d}/month={month:02d}/"
            f"USTECH-PROFILE-M1-{year:04d}-{month:02d}.parquet"
        )
        raw = f"synthetic-real-schema-ap0-{i:02d}".encode("ascii")
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        files.append(
            {
                "first_minute_ms_utc": i * 60_000,
                "first_segment_id": i,
                "last_minute_ms_utc": i * 60_000,
                "last_segment_id": i,
                "relative_path": rel,
                "rows": 1,
                "sha256": _sha256(raw),
                "size_bytes": len(raw),
                "source_ticks": 1,
            }
        )

    manifest = {
        "schema": REAL_AP0_SCHEMA,
        "status": "AP0_COMPLETE",
        "output_identity": REAL_AP0_IDENTITY,
        "files": files,
    }
    manifest_path = tmp_path / "AP0-MANIFEST.json"
    manifest_raw = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    manifest_path.write_bytes(manifest_raw)

    assert len(files) == 61
    assert all("relative_path" in rec for rec in files)
    assert all("path" not in rec for rec in files)

    result = module.verify_ap0_binding(
        manifest_path,
        root,
        expected_manifest_sha256=_sha256(manifest_raw),
    )

    assert result == {"status": "PASS", "files_rehashed": 61}

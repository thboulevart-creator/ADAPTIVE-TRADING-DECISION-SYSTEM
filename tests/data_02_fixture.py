"""Synthetic fixtures for DATA-02 claim-scoped admission qualification.

The files created here are synthetic byte payloads with .parquet names. They are
never represented as real Parquet and are used only to exercise content/file-set
binding. Schema observations are supplied separately to the synthetic admission
surface. No real market data is read.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
SOURCE_IDENTITY = "SOURCE_B_USTECH_PRICE_CORE_V0_1"
CONSUMER_ID = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
CLAIM_CLASS = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
SEMANTIC_LIMIT = "RETROSPECTIVE_DESCRIPTIVE_ONLY"
TRANSFORMER_BLOB = "42fcb38809a1cc0365cd4027fae5154e1d6d3b4f"

EXACT_SCHEMA = [
    ["minute_start_ms_utc", "int64"],
    ["first_tick_ms", "int64"],
    ["last_tick_ms", "int64"],
    ["tick_count", "int64"],
    ["segment_id", "int64"],
    ["segment_start", "bool"],
    ["gap_before_ms", "int64"],
    ["mid_open", "float64"],
    ["mid_high", "float64"],
    ["mid_low", "float64"],
    ["mid_close", "float64"],
    ["spread_mean", "float64"],
    ["spread_min", "float64"],
    ["spread_max", "float64"],
]

def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def sha256_path(path: str | Path) -> str:
    return sha256_bytes(Path(path).read_bytes())

def file_set_digest(records: list[dict[str, Any]]) -> str:
    material = [
        {
            "relative_path": rec["relative_path"],
            "size_bytes": int(rec["size_bytes"]),
            "sha256": rec["sha256"],
        }
        for rec in records
    ]
    raw = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)

def write_manifest(path: Path, manifest: dict[str, Any]) -> str:
    raw = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return sha256_bytes(raw)

def make_package(tmp_path: Path) -> dict[str, Any]:
    root = tmp_path / "ap0"
    root.mkdir(parents=True)
    files: list[dict[str, Any]] = []
    for i in range(61):
        rel = Path(f"year=synthetic/month={i + 1:02d}/AP0-{i:02d}.parquet")
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = f"DATA02-SYNTHETIC-AP0-{i:02d}\n".encode("ascii")
        path.write_bytes(raw)
        files.append(
            {
                "relative_path": rel.as_posix(),
                "size_bytes": len(raw),
                "sha256": sha256_bytes(raw),
                "rows": 1,
                "source_ticks": 2,
            }
        )

    manifest = {
        "schema": "ATDS_AP0_USTECH_PROFILE_MINUTE_CORE_MANIFEST_V0_1",
        "status": "AP0_COMPLETE",
        "output_identity": DATASET_IDENTITY,
        "source_identity": SOURCE_IDENTITY,
        "coverage": {
            "minute_rows_written": 61,
            "source_ticks_read": 122,
            "segments": 1,
            "segment_start_rows": 1,
        },
        "transformation_contract": {
            "source_columns": ["timestamp", "bid_price", "ask_price"],
            "volume_columns_used": [],
            "minute_definition": "floor(timestamp_ms / 60000)",
            "mid_definition": "(bid_price + ask_price) / 2",
            "mid_is_execution_price": False,
            "spread_definition": "ask_price - bid_price",
            "spread_mean_weighting": "tick_weighted",
            "missing_minutes_synthesized": False,
        },
        "files": files,
    }
    manifest_path = root / "AP0-MANIFEST.json"
    manifest_sha = write_manifest(manifest_path, manifest)

    rows = [
        {
            "minute_start_ms_utc": 0,
            "first_tick_ms": 1,
            "last_tick_ms": 59_999,
            "tick_count": 2,
            "segment_id": 0,
            "segment_start": True,
            "gap_before_ms": 0,
            "mid_open": 100.0,
            "mid_high": 101.0,
            "mid_low": 99.0,
            "mid_close": 100.5,
            "spread_mean": 1.0,
            "spread_min": 0.5,
            "spread_max": 1.5,
        },
        {
            "minute_start_ms_utc": 60_000,
            "first_tick_ms": 60_001,
            "last_tick_ms": 119_999,
            "tick_count": 2,
            "segment_id": 0,
            "segment_start": False,
            "gap_before_ms": 1,
            "mid_open": 100.5,
            "mid_high": 102.0,
            "mid_low": 100.0,
            "mid_close": 101.0,
            "spread_mean": 1.1,
            "spread_min": 0.6,
            "spread_max": 1.6,
        },
        {
            "minute_start_ms_utc": 120_000,
            "first_tick_ms": 120_001,
            "last_tick_ms": 179_999,
            "tick_count": 2,
            "segment_id": 0,
            "segment_start": False,
            "gap_before_ms": 1,
            "mid_open": 101.0,
            "mid_high": 103.0,
            "mid_low": 100.5,
            "mid_close": 102.0,
            "spread_mean": 1.2,
            "spread_min": 0.7,
            "spread_max": 1.7,
        },
    ]

    return {
        "mode": "SYNTHETIC_QUALIFICATION",
        "root": str(root),
        "manifest_path": str(manifest_path),
        "expected_manifest_sha256": manifest_sha,
        "declared_content_identity": file_set_digest(files),
        "dataset_identity": DATASET_IDENTITY,
        "observed_schema": [list(x) for x in EXACT_SCHEMA],
        "metadata": {
            "dataset_identity": DATASET_IDENTITY,
            "source_identity": SOURCE_IDENTITY,
            "time_semantics": "UTC epoch milliseconds",
            "mid_semantics": "descriptive_only_not_execution_price",
            "spread_mean_weighting": "tick_weighted",
            "volumes_used": False,
        },
        "rows": rows,
        "provenance": {
            "source_identity": SOURCE_IDENTITY,
            "source_verification": "PASS",
            "parent_dataset_ids": [SOURCE_IDENTITY],
            "lineage_status": "KNOWN_SINGLE_PARENT",
            "child_checks_present": True,
            "parent_validation_status": "PASS",
        },
        "transformation": {
            "transformer_blob": TRANSFORMER_BLOB,
            "parameters": dict(manifest["transformation_contract"]),
            "ambiguity": False,
        },
        "usage": {
            "claim_class": CLAIM_CLASS,
            "consumer_id": CONSUMER_ID,
            "semantic_limit": SEMANTIC_LIMIT,
            "subminute_required": False,
            "tick_count_as_traded_volume": False,
            "mid_as_execution_price": False,
            "claims_universal_ap0_sufficiency": False,
        },
        "temporal": {
            "state": "NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
            "basis": "retrospective descriptive only; no historical availability/tradability assertion",
            "assertions": [],
            "latest_revision_as_historical": False,
            "dependency_status": "NOT_APPLICABLE",
        },
        "authority_request": {
            "scientific": False,
            "operational": False,
            "trading": False,
            "capital": False,
        },
        "mutable_commentary": "synthetic fixture",
    }

def rewrite_manifest_for_current_files(package: dict[str, Any]) -> None:
    root = Path(package["root"])
    manifest_path = Path(package["manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rec in manifest["files"]:
        path = root / rec["relative_path"]
        raw = path.read_bytes()
        rec["size_bytes"] = len(raw)
        rec["sha256"] = sha256_bytes(raw)
    package["expected_manifest_sha256"] = write_manifest(manifest_path, manifest)

def manifest_file_set(package: dict[str, Any]) -> list[dict[str, Any]]:
    return json.loads(Path(package["manifest_path"]).read_text(encoding="utf-8"))["files"]

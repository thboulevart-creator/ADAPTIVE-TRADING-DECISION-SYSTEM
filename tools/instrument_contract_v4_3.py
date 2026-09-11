#!/usr/bin/env python3
"""V4.3 minimal instrument/source decoding contract loader."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = (
    "asset_id", "source", "format", "record_size",
    "record_struct", "timestamp_unit", "price_scale",
)


@dataclass(frozen=True)
class InstrumentContract:
    asset_id: str
    source: str
    format: str
    record_size: int
    record_struct: str
    timestamp_unit: str
    price_scale: int


def load_contract(path: str | Path) -> InstrumentContract:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CONTRACT_MUST_BE_OBJECT")
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"CONTRACT_MISSING_FIELDS:{','.join(missing)}")
    if not isinstance(data["asset_id"], str) or not data["asset_id"]:
        raise ValueError("INVALID_ASSET_ID")
    if not isinstance(data["source"], str) or not data["source"]:
        raise ValueError("INVALID_SOURCE")
    if not isinstance(data["format"], str) or not data["format"]:
        raise ValueError("INVALID_FORMAT")
    if not isinstance(data["record_size"], int) or data["record_size"] <= 0:
        raise ValueError("INVALID_RECORD_SIZE")
    if not isinstance(data["record_struct"], str) or not data["record_struct"]:
        raise ValueError("INVALID_RECORD_STRUCT")
    if data["timestamp_unit"] not in {"milliseconds", "microseconds", "seconds"}:
        raise ValueError("INVALID_TIMESTAMP_UNIT")
    if not isinstance(data["price_scale"], int) or data["price_scale"] <= 0:
        raise ValueError("INVALID_PRICE_SCALE")
    return InstrumentContract(**{field: data[field] for field in REQUIRED_FIELDS})


def resolve_contract(contracts_root: str | Path, asset_id: str, source: str, format: str) -> InstrumentContract:
    path = Path(contracts_root) / f"{asset_id}-{source}-{format}.json"
    if not path.is_file():
        raise ValueError(f"CONTRACT_NOT_FOUND:{asset_id}:{source}:{format}")
    contract = load_contract(path)
    if (contract.asset_id, contract.source, contract.format) != (asset_id, source, format):
        raise ValueError("CONTRACT_IDENTITY_MISMATCH")
    return contract

"""EA-03-P2-I1 — Mock-only read facade for later controlled Terminal integration.

No MT5 import, network, broker access, external callbacks, disk reads or commands.
This is a constrained *in-process interface*, not a security sandbox for
arbitrary hostile Python code, and not a production account reader.
"""
from __future__ import annotations

import copy
import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any

PROTOCOL_VERSION = "ATDS_EA03_P2_I1_READ_V0_1"
MOCK_SCHEMA_VERSION = "ATDS_EA03_P2_I1_MOCK_FIXTURE_V0_1"
MOCK_AUTHORITY = {
    "trading": False, "capital": False, "real_data": False, "network": False,
}
READ_CAPABILITIES = frozenset({
    "read_ea_registry", "read_run_manifest", "read_orders",
    "read_deals", "read_positions", "read_account_snapshots",
    "read_market_context",
})
_ROUTES = {
    "read_ea_registry": "ea_registry",
    "read_run_manifest": "run_manifest",
    "read_orders": "orders",
    "read_deals": "deals",
    "read_positions": "positions",
    "read_account_snapshots": "account_snapshots",
    "read_market_context": "market_context",
}
_FIELDS = {
    "ea_registry": frozenset({
        "ea_id", "ownership", "binary_sha256", "synthetic",
    }),
    "run_manifest": frozenset({
        "run_id", "ea_id", "account_scope", "position_mode", "mode", "synthetic",
    }),
    "orders": frozenset({
        "record_id", "run_id", "native_order_id", "event_time_utc",
        "state", "synthetic",
    }),
    "deals": frozenset({
        "record_id", "run_id", "native_deal_id", "native_order_id",
        "native_position_id", "volume", "profit", "commission", "synthetic",
    }),
    "positions": frozenset({
        "record_id", "run_id", "native_position_id", "side",
        "volume", "floating_pnl", "synthetic",
    }),
    "account_snapshots": frozenset({
        "record_id", "run_id", "account_scope", "currency",
        "balance", "equity", "margin_used", "synthetic",
    }),
    "market_context": frozenset({
        "record_id", "run_id", "available_at_utc", "decision_at_utc", "synthetic",
    }),
}
_DECIMAL_KEYS = frozenset({
    "volume", "profit", "commission", "floating_pnl",
    "balance", "equity", "margin_used",
})
_SHA256 = re.compile(r"^[a-f0-9]{64}$", re.ASCII)
_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$", re.ASCII)


def _require(condition: object, error: str) -> None:
    if not condition:
        raise ValueError(error)


def _json_tree(value: Any) -> bool:
    """Reject executable Python objects and non-finite/binary numeric payloads."""
    if type(value) in (str, bool, int, type(None)):
        return True
    if type(value) is list:
        return all(_json_tree(item) for item in value)
    if type(value) is dict:
        return all(type(k) is str and _json_tree(item)
                   for k, item in value.items())
    return False


def _decimal_string(value: Any) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        return Decimal(value).is_finite()
    except (InvalidOperation, ValueError):
        return False


def _validate_mock_fixture(dataset: Any) -> dict[str, Any]:
    _require(_json_tree(dataset), "NON_JSON_OR_EXECUTABLE_FIXTURE_VALUE")
    _require(type(dataset) is dict and set(dataset) == {
        "schema_version", "synthetic", "authority", "collections",
    }, "INVALID_MOCK_FIXTURE_ROOT")
    _require(dataset["schema_version"] == MOCK_SCHEMA_VERSION,
             "INVALID_MOCK_FIXTURE_SCHEMA")
    _require(dataset["synthetic"] is True, "REAL_FIXTURE_FORBIDDEN")
    _require(type(dataset["authority"]) is dict
             and dataset["authority"] == MOCK_AUTHORITY,
             "PRIVILEGED_FIXTURE_FORBIDDEN")
    collections = dataset["collections"]
    _require(type(collections) is dict and set(collections) == set(_FIELDS),
             "MOCK_COLLECTION_SET_MISMATCH")
    for collection, entries in collections.items():
        _require(type(entries) is list and all(type(row) is dict for row in entries),
                 "MALFORMED_MOCK_COLLECTION")
        seen: set[str] = set()
        for row in entries:
            _require(set(row) == _FIELDS[collection], "UNKNOWN_OR_MISSING_MOCK_FIELD")
            _require(row["synthetic"] is True, "NON_SYNTHETIC_MOCK_RECORD")
            identifier = row.get("ea_id" if collection == "ea_registry" else
                                 "run_id" if collection == "run_manifest" else
                                 "record_id")
            _require(type(identifier) is str and bool(_ID.fullmatch(identifier)),
                     "INVALID_MOCK_RECORD_ID")
            _require(identifier not in seen, "DUPLICATE_MOCK_RECORD_ID")
            seen.add(identifier)
            for key, value in row.items():
                if key in _DECIMAL_KEYS:
                    _require(value is None or _decimal_string(value),
                             "INVALID_MOCK_DECIMAL")
                elif key != "synthetic":
                    _require(type(value) is str and bool(value), "INVALID_MOCK_VALUE")
            if collection == "ea_registry":
                _require(row["ownership"] == "SYNTHETIC", "NON_SYNTHETIC_EA")
                _require(_SHA256.fullmatch(row["binary_sha256"]),
                         "INVALID_MOCK_BINARY_ID")
            if collection == "run_manifest":
                _require(row["mode"] == "SYNTHETIC", "REAL_RUN_FORBIDDEN")
                _require(row["position_mode"] in ("NETTING", "HEDGING", "UNKNOWN"),
                         "INVALID_MOCK_POSITION_MODE")
            if collection == "positions":
                _require(row["side"] in ("BUY", "SELL"), "INVALID_POSITION_SIDE")
    eas = {e["ea_id"] for e in collections["ea_registry"]}
    runs = {r["run_id"] for r in collections["run_manifest"]}
    _require(len(runs) > 0 and len(eas) > 0, "EMPTY_MOCK_IDENTITY")
    for run in collections["run_manifest"]:
        _require(run["ea_id"] in eas, "UNBOUND_MOCK_EA")
    for col in _FIELDS:
        if col in ("ea_registry", "run_manifest"):
            continue
        for row in collections[col]:
            _require(row["run_id"] in runs, "UNBOUND_MOCK_RUN")
    return copy.deepcopy(dataset)


class MockReadFirewall:
    """Seven read-only capabilities, no dynamic method/connector dispatch.

    Designed for possible later *contract review* with an existing terminal.
    No terminal code or production execution is supplied by this class.
    """

    __slots__ = ("_dataset",)

    def __init__(self, dataset: dict[str, Any]) -> None:
        self._dataset = _validate_mock_fixture(dataset)

    def execute(self, request: object) -> dict[str, Any]:
        result: dict[str, Any] = {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": "",
            "status": "DENIED",
            "source": "SYNTHETIC_MOCK",
            "records": [],
            "errors": ["INVALID_REQUEST"],
            "authority": copy.deepcopy(MOCK_AUTHORITY),
        }
        if type(request) is not dict or set(request) != {
            "protocol_version", "request_id", "capability", "filters",
        }:
            return result
        protocol = request.get("protocol_version")
        if type(protocol) is not str or protocol != PROTOCOL_VERSION:
            return result
        rid, capability, filters = (
            request.get("request_id"), request.get("capability"), request.get("filters")
        )
        if type(rid) is not str or not _ID.fullmatch(rid):
            return result
        result["request_id"] = rid
        if type(capability) is not str or capability not in _ROUTES:
            result["errors"] = ["CAPABILITY_NOT_GRANTED"]
            return result
        if type(filters) is not dict:
            return result
        if capability == "read_ea_registry":
            if filters:
                return result
        else:
            if set(filters) != {"run_id"}:
                return result
            run_id = filters["run_id"]
            if type(run_id) is not str or not _ID.fullmatch(run_id):
                return result
        records = self._dataset["collections"][_ROUTES[capability]]
        if capability != "read_ea_registry":
            records = [r for r in records if r["run_id"] == filters["run_id"]]
        result["status"] = "OK"
        result["records"] = copy.deepcopy(records)
        result["errors"] = []
        return result

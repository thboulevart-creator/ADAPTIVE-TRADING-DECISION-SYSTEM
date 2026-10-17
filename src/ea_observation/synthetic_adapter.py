"""ATDS EA-03-P1: offline synthetic-only MT5-shaped feed adapter.

Never imports, starts or connects to MetaTrader 5. Not an MT5 native importer.
Generated evidence hashes self-contained synthetic source records, not broker bytes.
"""
from __future__ import annotations

import copy
from typing import Any

from .provenance import SOURCE_VALUE_FIELDS, sha256_records
from .validation import validate_batch

INPUT_SCHEMA = "EA03_P1_SYNTHETIC_FEED_V0_1"
FORBIDDEN_AUTHORITY = {"trading": False, "capital": False, "real_data": False}

SUPPORTED_TAGS = {
    "MT5_EA_BINDING": ("EA_BINDING", None),
    "MT5_INSTRUMENT_SPEC": ("INSTRUMENT_SPEC", None),
    "MT5_ORDER": ("ORDER", "trade_events"),
    "MT5_DEAL": ("DEAL", "trade_events"),
    "MT5_CASH_FLOW": ("CASH_FLOW", "trade_events"),
    "MT5_POSITION_SNAPSHOT": ("POSITION_SNAPSHOT", "position_snapshots"),
    "MT5_ACCOUNT_SNAPSHOT": ("ACCOUNT_SNAPSHOT", "account_snapshots"),
    "MT5_CONTEXT": ("CONTEXT", "market_context_refs"),
}
TOP_LEVEL = frozenset({
    "input_schema", "batch_id", "synthetic", "authority", "requested_claim",
    "ea_registry", "run_manifest", "feeds",
})
FEED_FIELDS = frozenset({"source_id", "kind", "synthetic", "completeness", "records"})
RECORD_FIELDS = frozenset({"ref", "kind", "values", "annotation"})

# "annotation" describes observation identity / provenance metadata. Every
# economic value, price and native source timestamp MUST live in "values".
ANNOTATION_FIELDS = {
    "ORDER": frozenset({"event_id", "run_id", "time_precision", "timezone_status",
                        "observation_class", "ea_attribution"}),
    "DEAL": frozenset({"event_id", "run_id", "time_precision", "timezone_status",
                       "observation_class", "ea_attribution"}),
    "CASH_FLOW": frozenset({"event_id", "run_id", "time_precision", "timezone_status",
                            "observation_class", "ea_attribution"}),
    "POSITION_SNAPSHOT": frozenset({"snapshot_id", "run_id", "time_precision",
                                     "timezone_status", "attribution"}),
    "ACCOUNT_SNAPSHOT": frozenset({"snapshot_id", "run_id", "time_precision",
                                    "timezone_status"}),
    "CONTEXT": frozenset({"context_id", "run_id", "market_symbol"}),
}
EVIDENCE_ONLY_FIELDS = {
    "EA_BINDING": frozenset(),
    "INSTRUMENT_SPEC": frozenset({"symbol", "minimum_price"}),
}
OBSERVATION_COLLECTIONS = (
    "trade_events", "position_snapshots", "account_snapshots", "market_context_refs"
)


class AdapterRefusal(ValueError):
    """A strictly synthetic or contract-validation precondition was not met."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _require(condition: object, code: str) -> None:
    if not condition:
        raise AdapterRefusal(code)


def _is_object_list(value: object) -> bool:
    return type(value) is list and all(type(x) is dict for x in value)


def _transform(feed: object) -> dict[str, Any]:
    _require(type(feed) is dict, "INVALID_INPUT")
    _require(feed.get("input_schema") == INPUT_SCHEMA, "INVALID_INPUT_SCHEMA")
    _require(set(feed) == TOP_LEVEL, "INVALID_INPUT_FIELD")
    _require(feed.get("synthetic") is True, "NON_SYNTHETIC_INPUT")
    _require(feed.get("authority") == FORBIDDEN_AUTHORITY
             and type(feed.get("authority")) is dict, "UNAUTHORIZED_INPUT_AUTHORITY")
    _require(type(feed.get("batch_id")) is str and bool(feed["batch_id"]),
             "INVALID_BATCH_ID")
    _require(feed.get("requested_claim") is not None
             and type(feed["requested_claim"]) is str, "INVALID_REQUESTED_CLAIM")
    _require(_is_object_list(feed.get("ea_registry"))
             and _is_object_list(feed.get("run_manifest"))
             and _is_object_list(feed.get("feeds"))
             and len(feed["feeds"]) > 0, "INVALID_INPUT_COLLECTION")

    for ea in feed["ea_registry"]:
        _require(ea.get("ownership") == "SYNTHETIC",
                 "NON_SYNTHETIC_EA_IDENTITY")
    for run in feed["run_manifest"]:
        _require(run.get("mode") == "SYNTHETIC", "REAL_RUN_FORBIDDEN")

    batch: dict[str, Any] = {
        "schema_version": "ATDS_EA_OBSERVATION_V0_1",
        "batch_id": feed["batch_id"],
        "synthetic": True,
        "authority": copy.deepcopy(FORBIDDEN_AUTHORITY),
        "requested_claim": feed["requested_claim"],
        "ea_registry": copy.deepcopy(feed["ea_registry"]),
        "run_manifest": copy.deepcopy(feed["run_manifest"]),
        "source_manifest": [],
        **{key: [] for key in OBSERVATION_COLLECTIONS},
    }

    source_ids: set[str] = set()
    for source in feed["feeds"]:
        _require(set(source) == FEED_FIELDS, "INVALID_SOURCE_FIELD")
        _require(source.get("synthetic") is True and source.get("kind") == "SYNTHETIC",
                 "NON_SYNTHETIC_SOURCE")
        sid = source.get("source_id")
        _require(type(sid) is str and bool(sid) and sid not in source_ids,
                 "INVALID_OR_DUPLICATE_SOURCE_ID")
        source_ids.add(sid)
        _require(_is_object_list(source.get("records")), "INVALID_SOURCE_RECORDS")
        _require(type(source.get("completeness")) is dict, "INVALID_COMPLETENESS")
        refs: set[str] = set()
        records: list[dict] = []
        for item in source["records"]:
            _require(set(item) == RECORD_FIELDS, "INVALID_RAW_RECORD_FIELD")
            ref = item.get("ref")
            _require(type(ref) is str and bool(ref), "INVALID_SOURCE_REFERENCE")
            _require(ref not in refs, "DUPLICATE_SOURCE_REFERENCE")
            refs.add(ref)
            kind = item.get("kind")
            _require(type(kind) is str and kind in SUPPORTED_TAGS,
                     "UNSUPPORTED_SYNTHETIC_TAG")
            tag, collection = SUPPORTED_TAGS[kind]
            values, annotation = item.get("values"), item.get("annotation")
            _require(type(values) is dict and type(annotation) is dict,
                     "INVALID_RAW_STRUCTURE")
            if collection is None:
                _require(annotation == {} and set(values) == EVIDENCE_ONLY_FIELDS[tag],
                         "INVALID_SOURCE_EVIDENCE")
            else:
                required = set(SOURCE_VALUE_FIELDS[tag])
                _require(required.issubset(values), "SOURCE_VALUES_MISSING")
                _require(set(values) == required, "UNKNOWN_SOURCE_VALUE")
                _require(not (set(annotation) & required),
                         "ANNOTATION_SOURCE_FIELD_OVERRIDE")
                _require(set(annotation).issubset(ANNOTATION_FIELDS[tag]),
                         "INVALID_ANNOTATION_FIELD")
                _require(all(type(k) is str for k in annotation),
                         "INVALID_ANNOTATION_FIELD")
                if collection == "trade_events":
                    _require(annotation.get("observation_class") == "OBSERVED_DIRECT",
                             "NON_DIRECT_SYNTHETIC_OBSERVATION")
                row = {
                    **copy.deepcopy(annotation), **copy.deepcopy(values),
                    "source_id": sid, "source_record_ref": ref,
                }
                if collection == "trade_events":
                    row["event_type"] = tag
                batch[collection].append(row)
            raw_record = {"ref": ref, "tag": tag}
            if collection is not None or values:
                raw_record["values"] = copy.deepcopy(values)
            records.append(raw_record)

        batch["source_manifest"].append({
            "source_id": sid,
            "kind": "SYNTHETIC",
            "synthetic": True,
            "sha256": sha256_records(records),
            "record_count": len(records),
            "raw_records": records,
            "completeness": copy.deepcopy(source["completeness"]),
        })
    return batch


def adapt_synthetic_feed(feed: object) -> dict[str, Any]:
    """Transform only explicit synthetic records; D1 controls final admissibility.

    Returns PASS only for valid descriptive synthetic results, never a privileged
    authorization. BLOCKED/FAIL results contain no candidate batch.
    """
    response: dict[str, Any] = {
        "status": "FAIL",
        "batch": None,
        "validation": None,
        "errors": [],
        "authority": copy.deepcopy(FORBIDDEN_AUTHORITY),
    }
    try:
        candidate = _transform(feed)
        checked = validate_batch(candidate)
        response["validation"] = checked
        if checked["errors"] or checked["overall_status"] == "FAIL":
            response["errors"] = checked["errors"] or ["D1_VALIDATION_FAILED"]
            return response
        if checked["overall_status"] == "BLOCKED":
            response["status"] = "BLOCKED"
            response["errors"] = ["D1_CLAIM_NOT_AUTHORIZED"]
            return response
        if checked["overall_status"] not in ("STRUCTURALLY_VALID",
                                              "PARTIAL_DESCRIPTIVE_ONLY"):
            response["errors"] = ["UNRECOGNIZED_D1_VERDICT"]
            return response
        response["status"] = "PASS"
        response["batch"] = candidate
        return response
    except AdapterRefusal as refusal:
        response["errors"] = [refusal.code]
    except (TypeError, ValueError, KeyError, OverflowError, RecursionError):
        response["errors"] = ["INVALID_INPUT"]
    return response

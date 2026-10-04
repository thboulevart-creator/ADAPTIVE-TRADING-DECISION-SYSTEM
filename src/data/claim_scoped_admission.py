"""Minimal DATA-02 claim-scoped admission gate.

Scope is intentionally narrow:
- selected dataset: USTECH_PROFILE_MINUTE_CORE_V0_1
- selected consumer: ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1
- claim class: CC02_DESCRIPTIVE_MARKET_BEHAVIOR
- semantics: RETROSPECTIVE_DESCRIPTIVE_ONLY

This module does not transform data, compute market behavior, backtest, adjudicate
Temporal/PIT, or grant scientific/operational/trading/capital authority.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

CONTRACT = "ATDS_DATA_02_CLAIM_SCOPED_ADMISSION_V0_1"
FROZEN_DATA01_BREAKER_BLOB = "d9cafc53c863341ca827097014411702c26633f2"

DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
SOURCE_IDENTITY = "SOURCE_B_USTECH_PRICE_CORE_V0_1"
CONSUMER_ID = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
CLAIM_CLASS = "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
SEMANTIC_LIMIT = "RETROSPECTIVE_DESCRIPTIVE_ONLY"
CLAIM_SCOPE_ID = f"{CLAIM_CLASS}:{SEMANTIC_LIMIT}:{CONSUMER_ID}"
USAGE_ENVELOPE_ID = "DATA01_CC02_AP1_RETROSPECTIVE_V0_1"
TRANSFORMER_BLOB = "42fcb38809a1cc0365cd4027fae5154e1d6d3b4f"
REAL_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
REAL_EXPECTED_FILES = 61
REAL_EXPECTED_ROWS = 1_709_180
REAL_EXPECTED_SOURCE_TICKS = 376_003_618
REAL_EXPECTED_SEGMENTS = 1_606

EXACT_SCHEMA = (
    ("minute_start_ms_utc", "int64"),
    ("first_tick_ms", "int64"),
    ("last_tick_ms", "int64"),
    ("tick_count", "int64"),
    ("segment_id", "int64"),
    ("segment_start", "bool"),
    ("gap_before_ms", "int64"),
    ("mid_open", "float64"),
    ("mid_high", "float64"),
    ("mid_low", "float64"),
    ("mid_close", "float64"),
    ("spread_mean", "float64"),
    ("spread_min", "float64"),
    ("spread_max", "float64"),
)

CAPABILITIES = {
    "read_only_admission": True,
    "write_dataset": False,
    "repair_dataset": False,
    "transform_real_data": False,
    "temporal_adjudication": False,
    "backtest": False,
    "strategy": False,
    "performance": False,
    "oos_consumption": False,
    "trading": False,
    "capital": False,
}

_REQUIRED_BINDING_FIELDS = (
    "claim_scope_id",
    "dataset_identity",
    "ap0_manifest_sha256",
    "dataset_file_set_digest",
    "schema_identity",
    "source_identity",
    "transformer_blob",
    "usage_envelope_id",
    "data_admissibility_evidence_ref",
    "result_identity",
)

def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def _sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def _canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return _sha256_bytes(raw)

def _normalize_type(type_name: str) -> str:
    text = str(type_name).lower()
    if text in {"double", "float64"}:
        return "float64"
    if text in {"bool", "boolean"}:
        return "bool"
    return text

def _normalize_schema(schema: Sequence[Sequence[object]]) -> tuple[tuple[str, str], ...]:
    return tuple((str(row[0]), _normalize_type(str(row[1]))) for row in schema)

def _schema_identity(schema: Sequence[Sequence[object]]) -> str:
    return _canonical_digest([list(x) for x in _normalize_schema(schema)])

def _file_set_digest(records: Sequence[Mapping[str, object]]) -> str:
    material = [
        {
            "relative_path": str(rec["relative_path"]),
            "size_bytes": int(rec["size_bytes"]),
            "sha256": str(rec["sha256"]),
        }
        for rec in records
    ]
    return _canonical_digest(material)

def _decision(status: str, reason: str, **extra: object) -> dict[str, Any]:
    out: dict[str, Any] = {
        "contract": CONTRACT,
        "status": status,
        "reason": reason,
        "temporal_authority": False,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
        "rvo_authority": "NONE",
    }
    out.update(extra)
    return out

def _safe_child(root: Path, relative_path: str) -> Path | None:
    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    candidate = (root / rel).resolve(strict=False)
    root_resolved = root.resolve(strict=False)
    if candidate == root_resolved or root_resolved not in candidate.parents:
        return None
    return candidate

def validate_surface_selection(
    dataset_identity: str,
    *,
    claim_class: str,
    consumer_id: str,
    subminute_required: bool,
    universal_sufficiency_claim: bool,
) -> dict[str, Any]:
    if universal_sufficiency_claim:
        return _decision("BLOCKED", "REJECT_GLOBAL_SUFFICIENCY_OVERCLAIM")
    if dataset_identity == DATASET_IDENTITY and subminute_required:
        return _decision("BLOCKED", "BLOCKED_CLAIM_SURFACE_MISMATCH")
    if dataset_identity == "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1":
        return _decision("BLOCKED", "REJECT_NON_MINIMAL_H1_SELECTION")
    if dataset_identity == "GENERIC_TICK_CSV_RUNTIME":
        return _decision("BLOCKED", "REJECT_AVAILABILITY_AS_SELECTION")
    if dataset_identity == SOURCE_IDENTITY and not subminute_required:
        return _decision("BLOCKED", "REJECT_NON_MINIMAL_RAW_SELECTION")
    if dataset_identity != DATASET_IDENTITY:
        return _decision("BLOCKED", "BLOCKED_CLAIM_SURFACE_MISMATCH")
    if claim_class != CLAIM_CLASS or consumer_id != CONSUMER_ID:
        return _decision("BLOCKED", "BLOCKED_USAGE_ENVELOPE_VIOLATION")
    return _decision(
        "SELECTED",
        "SELECTED_EXACT_FIRST_USE_SURFACE",
        dataset_identity=DATASET_IDENTITY,
        claim_scope_id=CLAIM_SCOPE_ID,
    )

def _validate_rows(rows: object) -> dict[str, Any] | None:
    if not isinstance(rows, list) or not rows:
        return _decision("UNVERIFIED", "UNVERIFIED_MISSING_CHILD_INTEGRITY_EVIDENCE")
    previous_minute: int | None = None
    previous_segment: int | None = None
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")
        try:
            minute = int(row["minute_start_ms_utc"])
            first_tick = int(row["first_tick_ms"])
            last_tick = int(row["last_tick_ms"])
            tick_count = int(row["tick_count"])
            segment_id = int(row["segment_id"])
            segment_start = bool(row["segment_start"])
            gap_raw = row["gap_before_ms"]
            gap_before_ms = None if gap_raw is None else int(gap_raw)
            mid_open = float(row["mid_open"])
            mid_high = float(row["mid_high"])
            mid_low = float(row["mid_low"])
            mid_close = float(row["mid_close"])
            spread_mean = float(row["spread_mean"])
            spread_min = float(row["spread_min"])
            spread_max = float(row["spread_max"])
        except (KeyError, TypeError, ValueError, OverflowError):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")

        if previous_minute is not None and minute <= previous_minute:
            return _decision("FAIL", "FAIL_ORDERING_INTEGRITY")
        previous_minute = minute

        finite = (mid_open, mid_high, mid_low, mid_close, spread_mean, spread_min, spread_max)
        if tick_count <= 0 or (gap_before_ms is not None and gap_before_ms <= 60_000) or not all(math.isfinite(x) for x in finite):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")
        if not (minute <= first_tick <= last_tick < minute + 60_000):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")
        if not (mid_low <= min(mid_open, mid_close) <= max(mid_open, mid_close) <= mid_high):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")
        if not (0.0 < spread_min <= spread_mean <= spread_max):
            return _decision("FAIL", "FAIL_DATA_DOMAIN_INTEGRITY")

        if index == 0:
            if not segment_start or gap_before_ms is not None:
                return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")
        elif previous_segment is not None:
            if segment_id < previous_segment:
                return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")
            if segment_id == previous_segment and (segment_start or gap_before_ms is not None):
                return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")
            if segment_id != previous_segment and (not segment_start or gap_before_ms is None):
                return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")
        previous_segment = segment_id
    return None

def evaluate_synthetic(package: Mapping[str, object]) -> dict[str, Any]:
    if package.get("mode") != "SYNTHETIC_QUALIFICATION":
        return _decision("BLOCKED", "BLOCKED_UNSUPPORTED_ADMISSION_MODE")

    root = Path(str(package.get("root", "")))
    manifest_path = Path(str(package.get("manifest_path", "")))
    if not root.is_dir() or not manifest_path.is_file():
        return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")

    try:
        manifest_raw = manifest_path.read_bytes()
    except OSError:
        return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
    actual_manifest_sha = _sha256_bytes(manifest_raw)
    if actual_manifest_sha != package.get("expected_manifest_sha256"):
        return _decision("BLOCKED", "BLOCKED_MANIFEST_IDENTITY_DRIFT")
    try:
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _decision("BLOCKED", "BLOCKED_MANIFEST_IDENTITY_DRIFT")

    if (
        manifest.get("status") != "AP0_COMPLETE"
        or manifest.get("output_identity") != DATASET_IDENTITY
        or manifest.get("source_identity") != SOURCE_IDENTITY
        or package.get("dataset_identity") != DATASET_IDENTITY
    ):
        return _decision("BLOCKED", "BLOCKED_CLAIM_SURFACE_MISMATCH")

    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != 61:
        return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
    seen: set[str] = set()
    for rec in files:
        if not isinstance(rec, Mapping):
            return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
        try:
            rel = str(rec["relative_path"])
            expected_size = int(rec["size_bytes"])
            expected_sha = str(rec["sha256"])
        except (KeyError, TypeError, ValueError):
            return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
        if rel in seen:
            return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
        seen.add(rel)
        path = _safe_child(root, rel)
        if path is None or not path.is_file():
            return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
        try:
            actual_size = path.stat().st_size
            actual_sha = _sha256_path(path)
        except OSError:
            return _decision("BLOCKED", "BLOCKED_AP0_FILESET_MISMATCH")
        if actual_size != expected_size or actual_sha != expected_sha:
            return _decision("BLOCKED", "BLOCKED_CONTENT_IDENTITY_MISMATCH")

    current_file_set_digest = _file_set_digest(files)
    if package.get("declared_content_identity") != current_file_set_digest:
        return _decision("BLOCKED", "BLOCKED_DATASET_ID_COLLISION")

    observed_schema = package.get("observed_schema")
    if not isinstance(observed_schema, list) or _normalize_schema(observed_schema) != EXACT_SCHEMA:
        return _decision("BLOCKED", "BLOCKED_SCHEMA_DRIFT")
    schema_identity = _schema_identity(observed_schema)

    metadata = package.get("metadata")
    if not isinstance(metadata, Mapping):
        return _decision("BLOCKED", "BLOCKED_SCHEMA_DRIFT")
    if (
        metadata.get("dataset_identity") != DATASET_IDENTITY
        or metadata.get("source_identity") != SOURCE_IDENTITY
        or metadata.get("mid_semantics") != "descriptive_only_not_execution_price"
        or metadata.get("spread_mean_weighting") != "tick_weighted"
        or metadata.get("volumes_used") is not False
    ):
        return _decision("BLOCKED", "REJECT_SEMANTIC_SCOPE_ESCALATION")

    provenance = package.get("provenance")
    if not isinstance(provenance, Mapping):
        return _decision("BLOCKED", "BLOCKED_MISSING_PROVENANCE")
    if provenance.get("source_verification") == "UNVERIFIED":
        return _decision("UNVERIFIED", "REJECT_SOURCE_VERIFICATION_LAUNDERING")
    if (
        provenance.get("source_identity") != SOURCE_IDENTITY
        or provenance.get("source_verification") != "PASS"
    ):
        return _decision("BLOCKED", "BLOCKED_MISSING_PROVENANCE")
    if provenance.get("lineage_status") != "KNOWN_SINGLE_PARENT" or provenance.get("parent_dataset_ids") != [SOURCE_IDENTITY]:
        return _decision("BLOCKED", "BLOCKED_LINEAGE_UNKNOWN", lineage_status="UNKNOWN")
    if provenance.get("child_checks_present") is not True:
        if provenance.get("parent_validation_status") == "PASS":
            return _decision("BLOCKED", "REJECT_PARENT_PASS_INHERITANCE")
        return _decision("UNVERIFIED", "UNVERIFIED_MISSING_CHILD_INTEGRITY_EVIDENCE")

    transformation = package.get("transformation")
    if not isinstance(transformation, Mapping):
        return _decision("BLOCKED", "BLOCKED_HIDDEN_TRANSFORMATION")
    if not transformation.get("transformer_blob") or not isinstance(transformation.get("parameters"), Mapping):
        return _decision("BLOCKED", "BLOCKED_HIDDEN_TRANSFORMATION")
    if transformation.get("transformer_blob") != TRANSFORMER_BLOB:
        return _decision("BLOCKED", "BLOCKED_HIDDEN_TRANSFORMATION")
    if transformation.get("ambiguity") is True:
        return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")
    manifest_transform = manifest.get("transformation_contract")
    if not isinstance(manifest_transform, Mapping) or dict(transformation["parameters"]) != dict(manifest_transform):
        return _decision("BLOCKED", "BLOCKED_TRANSFORMATION_AMBIGUITY")

    row_problem = _validate_rows(package.get("rows"))
    if row_problem is not None:
        return row_problem

    usage = package.get("usage")
    if not isinstance(usage, Mapping):
        return _decision("BLOCKED", "BLOCKED_USAGE_ENVELOPE_VIOLATION")

    temporal = package.get("temporal")
    if not isinstance(temporal, Mapping):
        return _decision("BLOCKED", "TEMPORAL_OWNER_REQUIRED")

    if (
        usage.get("claim_class") != CLAIM_CLASS
        or usage.get("consumer_id") != CONSUMER_ID
        or usage.get("semantic_limit") != SEMANTIC_LIMIT
    ):
        if (
            usage.get("claim_class") != CLAIM_CLASS
            and temporal.get("state") == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
        ):
            return _decision("BLOCKED", "BLOCKED_STALE_TEMPORAL_NOT_APPLICABLE")
        return _decision("BLOCKED", "BLOCKED_USAGE_ENVELOPE_VIOLATION")

    if usage.get("subminute_required") is True:
        return _decision("BLOCKED", "BLOCKED_CLAIM_SURFACE_MISMATCH")
    if usage.get("tick_count_as_traded_volume") is True or usage.get("mid_as_execution_price") is True:
        return _decision("BLOCKED", "REJECT_SEMANTIC_SCOPE_ESCALATION")
    if usage.get("claims_universal_ap0_sufficiency") is True:
        return _decision("BLOCKED", "REJECT_GLOBAL_SUFFICIENCY_OVERCLAIM")

    assertions = temporal.get("assertions")
    assertions = assertions if isinstance(assertions, list) else []
    if temporal.get("latest_revision_as_historical") is True:
        return _decision("BLOCKED", "BLOCKED_LATEST_AS_HISTORICAL")
    if temporal.get("dependency_status") == "UNKNOWN" and assertions:
        return _decision("BLOCKED", "BLOCKED_TEMPORAL_DEPENDENCY_UNKNOWN")
    if temporal.get("state") == "PASS" or any(
        x in {"HISTORICAL_PIT_PASS", "HISTORICALLY_TRADABLE", "HISTORICALLY_AVAILABLE"} for x in assertions
    ):
        return _decision("BLOCKED", "REJECT_TEMPORAL_AUTHORITY_EXPANSION")
    if temporal.get("state") != "NOT_APPLICABLE_WITH_EXPLICIT_BASIS" or not temporal.get("basis"):
        return _decision("BLOCKED", "TEMPORAL_OWNER_REQUIRED")

    authority = package.get("authority_request")
    if not isinstance(authority, Mapping):
        return _decision("BLOCKED", "REJECT_AUTHORITY_LAUNDERING")
    if any(authority.get(x) is True for x in ("scientific", "operational", "trading", "capital")):
        return _decision("BLOCKED", "REJECT_AUTHORITY_LAUNDERING")

    binding_basis = {
        "claim_scope_id": CLAIM_SCOPE_ID,
        "dataset_identity": DATASET_IDENTITY,
        "ap0_manifest_sha256": actual_manifest_sha,
        "dataset_file_set_digest": current_file_set_digest,
        "schema_identity": schema_identity,
        "source_identity": SOURCE_IDENTITY,
        "transformer_blob": TRANSFORMER_BLOB,
        "usage_envelope_id": USAGE_ENVELOPE_ID,
    }
    admission_material = {
        "contract": CONTRACT,
        "binding_basis": binding_basis,
        "lineage_status": "KNOWN",
        "temporal_status": "NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
        "mode": "SYNTHETIC_QUALIFICATION",
    }
    admission_digest = _canonical_digest(admission_material)
    return _decision(
        "READY_FOR_EXACT_CLAIM",
        "PASS_SYNTHETIC_CLAIM_SCOPED_DATA_ADMISSION",
        binding_basis=binding_basis,
        admission_digest=admission_digest,
        lineage_status="KNOWN",
        temporal_status="NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
        unknown_unknown_coverage="NOT_CLAIMED",
    )

def validate_result_binding(admission: Mapping[str, object], binding: Mapping[str, object]) -> dict[str, Any]:
    if "filename" in binding and not all(field in binding for field in _REQUIRED_BINDING_FIELDS):
        return _decision("BLOCKED", "REJECT_FILENAME_ONLY_BINDING")
    missing = [field for field in _REQUIRED_BINDING_FIELDS if not binding.get(field)]
    if missing:
        return _decision("BLOCKED", "BLOCKED_INCOMPLETE_RESULT_DATASET_BINDING", missing_fields=missing)
    if admission.get("status") != "READY_FOR_EXACT_CLAIM":
        return _decision("BLOCKED", "BLOCKED_INCOMPLETE_RESULT_DATASET_BINDING")

    basis = admission.get("binding_basis")
    if not isinstance(basis, Mapping):
        return _decision("BLOCKED", "BLOCKED_INCOMPLETE_RESULT_DATASET_BINDING")
    for field in (
        "claim_scope_id",
        "dataset_identity",
        "ap0_manifest_sha256",
        "dataset_file_set_digest",
        "schema_identity",
        "source_identity",
        "transformer_blob",
        "usage_envelope_id",
    ):
        if binding.get(field) != basis.get(field):
            return _decision("BLOCKED", "BLOCKED_SILENT_DATASET_SUBSTITUTION")
    if binding.get("data_admissibility_evidence_ref") != admission.get("admission_digest"):
        return _decision("BLOCKED", "BLOCKED_SILENT_DATASET_SUBSTITUTION")

    material = {field: binding[field] for field in _REQUIRED_BINDING_FIELDS}
    return _decision(
        "BOUND_TO_EXACT_DATASET",
        "PASS_EXACT_RESULT_DATASET_BINDING",
        binding_digest=_canonical_digest(material),
        result_identity=binding["result_identity"],
    )

def _real_block(reason: str, **extra: object) -> dict[str, Any]:
    return _decision("BLOCKED_ACCESS", reason, real_ap0_qualification="BLOCKED_ACCESS", **extra)

def admit_real_ap0(root: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    """Read-only DATA-only admission of the exact real AP0 corpus.

    The function intentionally performs identity/integrity checks only. It does
    not compute AP1 behavior, returns, signals, PnL, strategy metrics, or OOS.
    """
    root_path = Path(root)
    manifest = Path(manifest_path)
    if not root_path.is_dir():
        return _real_block("REAL_AP0_ROOT_NOT_ACCESSIBLE")
    if not manifest.is_file():
        return _real_block("REAL_AP0_MANIFEST_NOT_ACCESSIBLE")
    try:
        raw = manifest.read_bytes()
    except OSError as exc:
        return _real_block("REAL_AP0_MANIFEST_NOT_ACCESSIBLE", detail=str(exc))
    manifest_sha = _sha256_bytes(raw)
    if manifest_sha != REAL_AP0_MANIFEST_SHA256:
        return _real_block(
            "REAL_AP0_MANIFEST_IDENTITY_MISMATCH",
            observed_manifest_sha256=manifest_sha,
            expected_manifest_sha256=REAL_AP0_MANIFEST_SHA256,
        )
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _real_block("REAL_AP0_MANIFEST_PARSE_BLOCKED", detail=str(exc))

    if (
        doc.get("status") != "AP0_COMPLETE"
        or doc.get("output_identity") != DATASET_IDENTITY
        or doc.get("source_identity") != SOURCE_IDENTITY
    ):
        return _real_block("REAL_AP0_MANIFEST_CONTRACT_MISMATCH")
    files = doc.get("files")
    if not isinstance(files, list) or len(files) != REAL_EXPECTED_FILES:
        return _real_block("REAL_AP0_FILESET_MISMATCH")

    try:
        import pyarrow.parquet as pq  # type: ignore
    except Exception as exc:
        return _real_block("REAL_AP0_SCHEMA_INSPECTOR_UNAVAILABLE", detail=repr(exc))

    previous_minute: int | None = None
    previous_segment: int | None = None
    rows_total = 0
    source_ticks_total = 0
    segment_starts = 0
    observed_records: list[dict[str, object]] = []

    for rec in files:
        if not isinstance(rec, Mapping):
            return _real_block("REAL_AP0_FILESET_MISMATCH")
        try:
            rel = str(rec["relative_path"])
            expected_size = int(rec["size_bytes"])
            expected_sha = str(rec["sha256"])
        except (KeyError, TypeError, ValueError):
            return _real_block("REAL_AP0_FILESET_MISMATCH")
        path = _safe_child(root_path, rel)
        if path is None or not path.is_file():
            return _real_block("REAL_AP0_FILESET_MISMATCH", relative_path=rel)
        try:
            if path.stat().st_size != expected_size:
                return _real_block("REAL_AP0_FILE_SIZE_MISMATCH", relative_path=rel)
            actual_sha = _sha256_path(path)
        except OSError as exc:
            return _real_block("REAL_AP0_FILE_READ_BLOCKED", relative_path=rel, detail=str(exc))
        if actual_sha != expected_sha:
            return _real_block("REAL_AP0_FILE_HASH_MISMATCH", relative_path=rel)

        try:
            pf = pq.ParquetFile(path)
            schema = [(field.name, _normalize_type(str(field.type))) for field in pf.schema_arrow]
        except Exception as exc:
            return _real_block("REAL_AP0_PARQUET_READ_BLOCKED", relative_path=rel, detail=repr(exc))
        if tuple(schema) != EXACT_SCHEMA:
            return _real_block("REAL_AP0_SCHEMA_MISMATCH", relative_path=rel, observed_schema=schema)
        meta = pf.schema_arrow.metadata or {}
        if (
            meta.get(b"dataset_identity") != DATASET_IDENTITY.encode()
            or meta.get(b"source_identity") != SOURCE_IDENTITY.encode()
            or meta.get(b"mid_semantics") != b"descriptive_only_not_execution_price"
            or meta.get(b"spread_mean_weighting") != b"tick_weighted"
            or meta.get(b"volumes_used") != b"false"
        ):
            return _real_block("REAL_AP0_METADATA_MISMATCH", relative_path=rel)

        file_rows = int(pf.metadata.num_rows)
        if file_rows != int(rec.get("rows", -1)):
            return _real_block("REAL_AP0_ROW_COUNT_MISMATCH", relative_path=rel)

        columns = [name for name, _ in EXACT_SCHEMA]
        try:
            for rg in range(pf.num_row_groups):
                table = pf.read_row_group(rg, columns=columns, use_threads=False)
                data = {name: table[name].combine_chunks().to_pylist() for name in columns}
                n = table.num_rows
                for i in range(n):
                    minute = int(data["minute_start_ms_utc"][i])
                    first_tick = int(data["first_tick_ms"][i])
                    last_tick = int(data["last_tick_ms"][i])
                    tick_count = int(data["tick_count"][i])
                    segment = int(data["segment_id"][i])
                    segment_start = bool(data["segment_start"][i])
                    gap_raw = data["gap_before_ms"][i]
                    gap_before = None if gap_raw is None else int(gap_raw)
                    mid_open = float(data["mid_open"][i])
                    mid_high = float(data["mid_high"][i])
                    mid_low = float(data["mid_low"][i])
                    mid_close = float(data["mid_close"][i])
                    spread_mean = float(data["spread_mean"][i])
                    spread_min = float(data["spread_min"][i])
                    spread_max = float(data["spread_max"][i])

                    if previous_minute is not None and minute <= previous_minute:
                        return _real_block("REAL_AP0_ORDERING_INTEGRITY_FAIL", relative_path=rel)
                    if tick_count <= 0 or (gap_before is not None and gap_before <= 60_000):
                        return _real_block("REAL_AP0_DOMAIN_INTEGRITY_FAIL", relative_path=rel)
                    if not (minute <= first_tick <= last_tick < minute + 60_000):
                        return _real_block("REAL_AP0_DOMAIN_INTEGRITY_FAIL", relative_path=rel)
                    vals = (mid_open, mid_high, mid_low, mid_close, spread_mean, spread_min, spread_max)
                    if not all(math.isfinite(x) for x in vals):
                        return _real_block("REAL_AP0_DOMAIN_INTEGRITY_FAIL", relative_path=rel)
                    if not (mid_low <= min(mid_open, mid_close) <= max(mid_open, mid_close) <= mid_high):
                        return _real_block("REAL_AP0_DOMAIN_INTEGRITY_FAIL", relative_path=rel)
                    if not (0.0 < spread_min <= spread_mean <= spread_max):
                        return _real_block("REAL_AP0_DOMAIN_INTEGRITY_FAIL", relative_path=rel)
                    if previous_segment is None:
                        if not segment_start or gap_before is not None:
                            return _real_block("REAL_AP0_SEGMENT_INTEGRITY_FAIL", relative_path=rel)
                    else:
                        if segment < previous_segment:
                            return _real_block("REAL_AP0_SEGMENT_INTEGRITY_FAIL", relative_path=rel)
                        if segment == previous_segment and (segment_start or gap_before is not None):
                            return _real_block("REAL_AP0_SEGMENT_INTEGRITY_FAIL", relative_path=rel)
                        if segment != previous_segment and (not segment_start or gap_before is None):
                            return _real_block("REAL_AP0_SEGMENT_INTEGRITY_FAIL", relative_path=rel)
                    if segment_start:
                        segment_starts += 1
                    previous_minute = minute
                    previous_segment = segment
                    rows_total += 1
                    source_ticks_total += tick_count
        except Exception as exc:
            return _real_block("REAL_AP0_INTEGRITY_READ_BLOCKED", relative_path=rel, detail=repr(exc))

        observed_records.append(
            {"relative_path": rel, "size_bytes": expected_size, "sha256": actual_sha}
        )

    coverage = doc.get("coverage") or {}
    if rows_total != REAL_EXPECTED_ROWS or int(coverage.get("minute_rows_written", -1)) != REAL_EXPECTED_ROWS:
        return _real_block("REAL_AP0_TOTAL_ROW_COUNT_MISMATCH", observed_rows=rows_total)
    if (
        source_ticks_total != REAL_EXPECTED_SOURCE_TICKS
        or int(coverage.get("source_ticks_read", -1)) != REAL_EXPECTED_SOURCE_TICKS
    ):
        return _real_block("REAL_AP0_SOURCE_TICK_ACCOUNTING_MISMATCH", observed_source_ticks=source_ticks_total)
    if (
        segment_starts != REAL_EXPECTED_SEGMENTS
        or int(coverage.get("segments", -1)) != REAL_EXPECTED_SEGMENTS
        or int(coverage.get("segment_start_rows", -1)) != REAL_EXPECTED_SEGMENTS
    ):
        return _real_block("REAL_AP0_SEGMENT_COUNT_MISMATCH", observed_segment_starts=segment_starts)

    file_set_digest = _file_set_digest(observed_records)
    evidence = {
        "contract": CONTRACT,
        "dataset_identity": DATASET_IDENTITY,
        "manifest_sha256": manifest_sha,
        "file_set_digest": file_set_digest,
        "schema_identity": _schema_identity(EXACT_SCHEMA),
        "source_identity": SOURCE_IDENTITY,
        "transformer_blob": TRANSFORMER_BLOB,
        "rows": rows_total,
        "source_ticks": source_ticks_total,
        "segments": segment_starts,
        "usage_envelope_id": USAGE_ENVELOPE_ID,
        "temporal_status": "NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
    }
    return _decision(
        "PASS_REAL_DATA_ADMISSION",
        "PASS_REAL_AP0_READ_ONLY_DATA_ADMISSION",
        real_ap0_qualification="PASS_REAL_DATA_ADMISSION",
        evidence=evidence,
        evidence_digest=_canonical_digest(evidence),
        unknown_unknown_coverage="NOT_CLAIMED",
    )

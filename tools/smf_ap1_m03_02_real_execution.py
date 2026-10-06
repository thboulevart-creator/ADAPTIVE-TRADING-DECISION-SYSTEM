from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from src.smf_ap1_m03_binding import (
    AUTHORITY_NONE,
    CLAIM_SCOPE_ID,
    METHOD_PROCEDURE_REF,
    METRIC_PROBABILITIES,
    SMF_CORE_BLOB,
    create_m03_activation,
    execute_m03_observations,
)

CONTRACT = "ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
AP1_SCHEMA = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
AP1_SHA256 = "db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b"
AP1_BYTES = 179955
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
PARITY_FACTOR = 8.0
DOUBLE_EPSILON = sys.float_info.epsilon
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
NY = ZoneInfo("America/New_York")

REQUIRED_SCHEMA = [
    ("minute_start_ms_utc", "int64"),
    ("first_tick_ms", "int64"),
    ("last_tick_ms", "int64"),
    ("tick_count", "int64"),
    ("segment_id", "int64"),
    ("segment_start", "bool"),
    ("gap_before_ms", "int64"),
    ("mid_open", "double"),
    ("mid_high", "double"),
    ("mid_low", "double"),
    ("mid_close", "double"),
    ("spread_mean", "double"),
    ("spread_min", "double"),
    ("spread_max", "double"),
]
READ_COLUMNS = [
    "minute_start_ms_utc",
    "tick_count",
    "mid_high",
    "mid_low",
    "spread_mean",
]


class ExecutionBlocked(RuntimeError):
    pass


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(value) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ExecutionBlocked(code)


def write_json(path: Path, payload: dict) -> None:
    data = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    require(len(data) <= MAX_OUTPUT_BYTES, "OUTPUT_TOO_LARGE")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def load_ap1(path: Path) -> dict:
    require(path.is_file(), "AP1_RESULT_MISSING")
    require(path.stat().st_size == AP1_BYTES, "AP1_RESULT_BYTES_MISMATCH")
    require(sha256_path(path) == AP1_SHA256, "AP1_RESULT_SHA256_MISMATCH")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(payload.get("schema") == AP1_SCHEMA, "AP1_SCHEMA_MISMATCH")
    require(payload.get("status") == "AP1_COMPLETE", "AP1_STATUS_MISMATCH")
    require(payload.get("input_identity") == DATASET_IDENTITY, "AP1_INPUT_IDENTITY_MISMATCH")
    require(
        payload.get("binding", {}).get("ap0_manifest_sha256") == AP0_MANIFEST_SHA256,
        "AP1_MANIFEST_BINDING_MISMATCH",
    )
    return payload


def load_ap0_arrays(root: Path, manifest_path: Path):
    import numpy as np
    import pyarrow.parquet as pq

    require(root.is_dir(), "AP0_ROOT_MISSING")
    require(manifest_path.is_file(), "AP0_MANIFEST_MISSING")
    require(sha256_path(manifest_path) == AP0_MANIFEST_SHA256, "AP0_MANIFEST_SHA256_MISMATCH")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("status") == "AP0_COMPLETE", "AP0_STATUS_MISMATCH")
    require(manifest.get("output_identity") == DATASET_IDENTITY, "AP0_IDENTITY_MISMATCH")
    files = manifest.get("files")
    require(isinstance(files, list) and len(files) == EXPECTED_FILES, "AP0_FILE_COUNT_MISMATCH")

    minute_chunks = []
    tick_chunks = []
    range_chunks = []
    spread_chunks = []
    total_rows = 0

    for rec in files:
        rel = rec["relative_path"]
        path = (root / Path(rel)).resolve(strict=False)
        require(path.is_file(), "AP0_FILE_MISSING:" + rel)
        require(int(path.stat().st_size) == int(rec["size_bytes"]), "AP0_FILE_SIZE_MISMATCH:" + rel)
        require(sha256_path(path) == rec["sha256"], "AP0_FILE_SHA256_MISMATCH:" + rel)

        pf = pq.ParquetFile(path)
        require(int(pf.metadata.num_rows) == int(rec["rows"]), "AP0_PARQUET_ROWS_MISMATCH:" + rel)
        observed_schema = [(field.name, str(field.type)) for field in pf.schema_arrow]
        require(observed_schema == REQUIRED_SCHEMA, "AP0_SCHEMA_MISMATCH:" + rel)
        meta = pf.schema_arrow.metadata or {}
        require(meta.get(b"dataset_identity") == DATASET_IDENTITY.encode(), "AP0_METADATA_IDENTITY_MISMATCH:" + rel)

        table = pf.read(columns=READ_COLUMNS, use_threads=False)
        minute = table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
        tick = table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
        high = table["mid_high"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
        low = table["mid_low"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
        spread = table["spread_mean"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

        require(minute.size == int(rec["rows"]), "AP0_DECODED_ROWS_MISMATCH:" + rel)
        require(np.all(tick > 0), "NONPOSITIVE_TICK_COUNT:" + rel)
        require(np.all(np.isfinite(high)) and np.all(np.isfinite(low)), "NONFINITE_MID:" + rel)
        require(np.all(np.isfinite(spread)), "NONFINITE_SPREAD:" + rel)
        require(np.all(high >= low), "MID_HIGH_LOW_VIOLATION:" + rel)

        minute_chunks.append(minute.copy())
        tick_chunks.append(tick.copy())
        range_chunks.append((high - low).copy())
        spread_chunks.append(spread.copy())
        total_rows += int(minute.size)

    require(total_rows == EXPECTED_MINUTES, "AP0_TOTAL_MINUTES_MISMATCH")
    minute = np.concatenate(minute_chunks)
    tick = np.concatenate(tick_chunks)
    minute_range = np.concatenate(range_chunks)
    spread_mean = np.concatenate(spread_chunks)

    require(np.all(np.diff(minute) > 0), "GLOBAL_MINUTE_ORDER_VIOLATION")
    return minute, tick, minute_range, spread_mean


def derive_codes(minute):
    import numpy as np

    utc_hour_code = minute // 3_600_000
    utc_hour = (utc_hour_code % 24).astype(np.int16)
    unique_hours, inverse = np.unique(utc_hour_code, return_inverse=True)

    ny_hour_map = np.empty(unique_hours.size, dtype=np.int16)
    ny_weekday_map = np.empty(unique_hours.size, dtype=np.int16)
    utc_year_map = np.empty(unique_hours.size, dtype=np.int16)

    for i, hour_code in enumerate(unique_hours):
        utc_dt = datetime.fromtimestamp(int(hour_code) * 3600, tz=timezone.utc)
        ny_dt = utc_dt.astimezone(NY)
        ny_hour_map[i] = ny_dt.hour
        ny_weekday_map[i] = ny_dt.weekday()
        utc_year_map[i] = utc_dt.year

    ny_hour = ny_hour_map[inverse]
    ny_weekday = ny_weekday_map[inverse]
    ny_weekday_hour = (ny_weekday * 24 + ny_hour).astype(np.int16)
    utc_year = utc_year_map[inverse]

    return {
        "UTC_HOUR": (utc_hour, list(range(24)), lambda x: f"UTC_HOUR:{x:02d}"),
        "NEW_YORK_HOUR": (ny_hour, list(range(24)), lambda x: f"NEW_YORK_HOUR:{x:02d}"),
        "NEW_YORK_WEEKDAY": (ny_weekday, list(range(7)), lambda x: f"NEW_YORK_WEEKDAY:{x}"),
        "NEW_YORK_WEEKDAY_HOUR": (
            ny_weekday_hour,
            list(range(168)),
            lambda x: f"NEW_YORK_WEEKDAY_HOUR:{x // 24}:{x % 24:02d}",
        ),
        "UTC_YEAR": (utc_year, list(range(2021, 2027)), lambda x: f"UTC_YEAR:{x}"),
    }


def empty_evidence(metric: str, bucket_id: str) -> dict:
    body = {
        "schema": "ATDS_SMF_AP1_M03_02_EMPTY_RESULT_V0_1",
        "claim_scope_id": CLAIM_SCOPE_ID,
        "metric": metric,
        "bucket_id": bucket_id,
        "status": "EMPTY_NO_NUMERICAL_RESULT",
        "n": 0,
        "quantiles": {str(p): None for p in METRIC_PROBABILITIES[metric]},
        "procedure_ref": METHOD_PROCEDURE_REF,
        "smf_core_blob": SMF_CORE_BLOB,
        "authority": dict(AUTHORITY_NONE),
    }
    return {**body, "result_digest": canonical_sha256(body)}


def execute_bucket(values_array, indices, *, metric: str, bucket_id: str, activation: dict) -> dict:
    if indices is None:
        n = int(values_array.size)
        if n == 0:
            return empty_evidence(metric, bucket_id)
        values = values_array.tolist()
    else:
        if int(indices.size) == 0:
            return empty_evidence(metric, bucket_id)
        values = values_array[indices].tolist()

    try:
        return execute_m03_observations(
            values,
            metric=metric,
            bucket_id=bucket_id,
            activation=activation,
        )
    finally:
        del values
        gc.collect()


def build_spans(codes):
    import numpy as np
    order = np.argsort(codes, kind="stable")
    sorted_codes = codes[order]
    unique, starts, counts = np.unique(sorted_codes, return_index=True, return_counts=True)
    spans = {int(code): (int(start), int(count)) for code, start, count in zip(unique, starts, counts)}
    return order, spans


def execute_real_m03(minute, tick, minute_range, spread_mean) -> dict:
    arrays = {
        "tick_count": tick,
        "minute_range": minute_range,
        "spread_mean": spread_mean,
    }
    activation = create_m03_activation(result_exposed=False)
    evidence: dict[str, dict] = {"GLOBAL": {}}

    for metric, arr in arrays.items():
        evidence["GLOBAL"][metric] = execute_bucket(
            arr,
            None,
            metric=metric,
            bucket_id="GLOBAL",
            activation=activation,
        )

    code_sets = derive_codes(minute)
    for family, (codes, expected_codes, label_fn) in code_sets.items():
        order, spans = build_spans(codes)
        for code in expected_codes:
            bucket_id = label_fn(code)
            evidence[bucket_id] = {}
            if int(code) in spans:
                start, count = spans[int(code)]
                idx = order[start:start + count]
            else:
                import numpy as np
                idx = np.empty(0, dtype=np.int64)
            for metric, arr in arrays.items():
                evidence[bucket_id][metric] = execute_bucket(
                    arr,
                    idx,
                    metric=metric,
                    bucket_id=bucket_id,
                    activation=activation,
                )
        del order, spans
        gc.collect()

    return {
        "activation": activation,
        "bucket_evidence": evidence,
    }


def ap1_bucket_map(payload: dict) -> dict[str, dict]:
    out = {"GLOBAL": payload["global"]}
    mappings = (
        ("UTC_HOUR", "utc_hour", lambda code: f"UTC_HOUR:{code:02d}"),
        ("NEW_YORK_HOUR", "new_york_hour", lambda code: f"NEW_YORK_HOUR:{code:02d}"),
        ("NEW_YORK_WEEKDAY", "new_york_weekday", lambda code: f"NEW_YORK_WEEKDAY:{code}"),
        (
            "NEW_YORK_WEEKDAY_HOUR",
            "new_york_weekday_hour",
            lambda code: f"NEW_YORK_WEEKDAY_HOUR:{code // 24}:{code % 24:02d}",
        ),
        ("UTC_YEAR", "utc_year", lambda code: f"UTC_YEAR:{code}"),
    )
    for _family, key, label_fn in mappings:
        for item in payload[key]:
            out[label_fn(int(item["code"]))] = item
    return out


def parity_tolerance(ap1_value: float, m03_value: float) -> float:
    return PARITY_FACTOR * DOUBLE_EPSILON * max(1.0, abs(ap1_value), abs(m03_value))


def ap1_field(metric: str, p: float) -> str:
    pct = int(round(p * 100))
    return f"{metric}_p{pct}"


def parity_check(ap1_payload: dict, bucket_evidence: dict) -> dict:
    source = ap1_bucket_map(ap1_payload)
    checks = []
    pass_count = 0
    fail_count = 0
    not_comparable_count = 0
    max_abs_diff = 0.0

    for bucket_id in sorted(bucket_evidence):
        ap1_bucket = source[bucket_id]
        for metric in ("tick_count", "minute_range", "spread_mean"):
            m03 = bucket_evidence[bucket_id][metric]
            if m03.get("status") == "EMPTY_NO_NUMERICAL_RESULT":
                checks.append({
                    "bucket_id": bucket_id,
                    "metric": metric,
                    "status": "NOT_COMPARABLE",
                    "reason": "EMPTY_NO_NUMERICAL_RESULT",
                })
                not_comparable_count += 1
                continue
            for p in METRIC_PROBABILITIES[metric]:
                field = ap1_field(metric, p)
                ap1_value = ap1_bucket.get(field)
                m03_value = m03["quantiles"][str(p)]
                if ap1_value is None:
                    checks.append({
                        "bucket_id": bucket_id,
                        "metric": metric,
                        "probability": p,
                        "status": "NOT_COMPARABLE",
                        "reason": "AP1_VALUE_ABSENT",
                    })
                    not_comparable_count += 1
                    continue
                a = float(ap1_value)
                m = float(m03_value)
                diff = abs(a - m)
                tol = parity_tolerance(a, m)
                status = "PASS" if diff <= tol else "FAIL"
                checks.append({
                    "bucket_id": bucket_id,
                    "metric": metric,
                    "probability": p,
                    "ap1": a,
                    "m03": m,
                    "abs_diff": diff,
                    "tolerance": tol,
                    "status": status,
                })
                max_abs_diff = max(max_abs_diff, diff)
                if status == "PASS":
                    pass_count += 1
                else:
                    fail_count += 1

    overall = "FAIL" if fail_count else ("PASS" if pass_count else "NOT_COMPARABLE")
    return {
        "schema": "ATDS_SMF_AP1_M03_02_REAL_PARITY_V0_1",
        "comparison_rule": "ABS_DIFF <= 8 * IEEE754_DOUBLE_EPSILON * max(1, abs(AP1), abs(M03))",
        "double_epsilon": DOUBLE_EPSILON,
        "factor": PARITY_FACTOR,
        "overall": overall,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "not_comparable_count": not_comparable_count,
        "max_abs_diff": max_abs_diff,
        "checks": checks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument("--ap1-result", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    output = Path(args.output).expanduser().resolve(strict=False)
    started = datetime.now(timezone.utc)

    try:
        ap1_payload = load_ap1(Path(args.ap1_result).expanduser().resolve(strict=False))
        minute, tick, minute_range, spread_mean = load_ap0_arrays(
            Path(args.ap0_root).expanduser().resolve(strict=False),
            Path(args.ap0_manifest).expanduser().resolve(strict=False),
        )
        real = execute_real_m03(minute, tick, minute_range, spread_mean)
        parity = parity_check(ap1_payload, real["bucket_evidence"])
        ended = datetime.now(timezone.utc)

        payload = {
            "schema": CONTRACT,
            "status": (
                "M03_REAL_EXECUTION_COMPLETE"
                if parity["overall"] == "PASS"
                else "M03_REAL_EXECUTION_PARITY_BLOCKED"
            ),
            "claim_scope_id": CLAIM_SCOPE_ID,
            "semantics": "RETROSPECTIVE_DESCRIPTIVE_ONLY",
            "source_ap1": {
                "schema": AP1_SCHEMA,
                "sha256": AP1_SHA256,
                "bytes": AP1_BYTES,
            },
            "source_data02": {
                "dataset_identity": DATASET_IDENTITY,
                "ap0_manifest_sha256": AP0_MANIFEST_SHA256,
                "expected_files": EXPECTED_FILES,
                "minute_rows": EXPECTED_MINUTES,
            },
            "method": {
                "family": "M03",
                "procedure_ref": METHOD_PROCEDURE_REF,
                "core_blob": SMF_CORE_BLOB,
                "activation_digest": real["activation"]["activation_digest"],
                "metric_probabilities": {
                    key: list(value) for key, value in METRIC_PROBABILITIES.items()
                },
                "empty_bucket_rule": "EMPTY_NO_NUMERICAL_RESULT",
                "tail_extrapolation": "FORBIDDEN",
            },
            "execution": {
                "started_at": started.isoformat().replace("+00:00", "Z"),
                "ended_at": ended.isoformat().replace("+00:00", "Z"),
            },
            "bucket_evidence": real["bucket_evidence"],
            "parity": parity,
            "authority": {
                "scientific": False,
                "operational": False,
                "trading": False,
                "capital": False,
            },
            "result_semantics": "M03_METHOD_EXECUTION_RESULT_ONLY",
        }
        write_json(output, payload)
        print("M03_EXIT_STATUS=" + payload["status"])
        print("PARITY_STATUS=" + parity["overall"])
        print("OUTPUT=" + str(output))
        print("OUTPUT_SHA256=" + sha256_path(output))
        return 0 if parity["overall"] == "PASS" else 3
    except Exception as exc:
        ended = datetime.now(timezone.utc)
        blocked = {
            "schema": CONTRACT,
            "status": "M03_REAL_EXECUTION_BLOCKED",
            "reason": str(exc),
            "execution": {
                "started_at": started.isoformat().replace("+00:00", "Z"),
                "ended_at": ended.isoformat().replace("+00:00", "Z"),
            },
            "authority": {
                "scientific": False,
                "operational": False,
                "trading": False,
                "capital": False,
            },
        }
        try:
            write_json(output, blocked)
        except Exception:
            pass
        print("M03_EXIT_STATUS=M03_REAL_EXECUTION_BLOCKED")
        print("REASON=" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

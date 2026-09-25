#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import os
import stat
import tempfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

EXPECTED_MANIFEST_SHA256 = "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
EXPECTED_F0_SHA256 = "5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b"
EXPECTED_INVENTORY_DIGEST = "5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
EXPECTED_FILES = 212
EXPECTED_TOTAL_PARQUET_BYTES = 3_936_721_231
EXPECTED_ROWS = 376_003_618
EXPECTED_ROW_GROUPS = 488
EXPECTED_TIMESTAMP_FIELD = "timestamp"
EXPECTED_TIMESTAMP_TYPE = "timestamp[ms]"
EXPECTED_SCHEMA_SIGNATURE = "c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d"

MAX_CUMULATIVE_PARQUET_LOGICAL_READ_BYTES = 16 * 1024**3
MANIFEST_HASH_READ_BYTES = EXPECTED_TOTAL_PARQUET_BYTES
F0_LOGICAL_METADATA_READ_BYTES = 450_332
TIMESTAMP_VALUE_WIDTH_BYTES = 8
PLANNED_TIMESTAMP_DECODED_BYTES = EXPECTED_ROWS * TIMESTAMP_VALUE_WIDTH_BYTES
PLANNED_CUMULATIVE_LOGICAL_BYTES = (
    MANIFEST_HASH_READ_BYTES
    + F0_LOGICAL_METADATA_READ_BYTES
    + PLANNED_TIMESTAMP_DECODED_BYTES
)

GAP_THRESHOLDS_MS = {
    "gt_1s": 1_000,
    "gt_10s": 10_000,
    "gt_60s": 60_000,
    "gt_5m": 300_000,
    "gt_1h": 3_600_000,
    "gt_6h": 21_600_000,
    "gt_24h": 86_400_000,
}
RECORD_GAP_THRESHOLD_MS = 60_000
MAX_RECORDED_GAPS = 100_000
MAX_RECORDED_BACKWARDS = 10_000
TOP_LARGEST_GAPS = 2_000


def sha256_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child_s = os.path.normcase(str(child))
        parent_s = os.path.normcase(str(parent))
        return os.path.commonpath([child_s, parent_s]) == parent_s
    except ValueError:
        return False


def is_reparse_or_symlink(path: Path) -> bool:
    try:
        st = path.lstat()
    except OSError:
        return True
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def blocked(output: Path, report: dict[str, Any], status: str, reason: str) -> None:
    report["status"] = status
    report["reason"] = reason
    write_json(output, report)
    print(status)
    print(reason)
    print(f"Report: {output}")
    raise SystemExit(2)


def naive_epoch_ms_iso(value_ms: int | None) -> str | None:
    if value_ms is None:
        return None
    try:
        return (
            datetime(1970, 1, 1) + timedelta(milliseconds=int(value_ms))
        ).isoformat(timespec="milliseconds")
    except Exception:
        return None


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in files:
        digest.update(
            f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n".encode("utf-8")
        )
    return digest.hexdigest()


def validate_manifest(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if sha256_path(path) != EXPECTED_MANIFEST_SHA256:
        raise ValueError("manifest SHA-256 mismatch")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    inv = manifest.get("inventory") or {}
    files = inv.get("files")
    if manifest.get("schema") != "ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1":
        raise ValueError("unexpected manifest schema")
    if manifest.get("status") != "MANIFEST_COMPLETE":
        raise ValueError("manifest is not MANIFEST_COMPLETE")
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        raise ValueError("manifest file count mismatch")
    if inv.get("parquet_files") != EXPECTED_FILES:
        raise ValueError("manifest parquet_files mismatch")
    if inv.get("total_parquet_bytes") != EXPECTED_TOTAL_PARQUET_BYTES:
        raise ValueError("manifest byte total mismatch")
    if inv.get("sha256_complete") is not True:
        raise ValueError("manifest sha256_complete is not true")
    if inv.get("snapshot_stable") is not True:
        raise ValueError("manifest snapshot_stable is not true")
    if inv.get("parquet_magic_checked") is not True:
        raise ValueError("manifest parquet_magic_checked is not true")
    if canonical_inventory_digest(files) != EXPECTED_INVENTORY_DIGEST:
        raise ValueError("manifest canonical inventory digest mismatch")
    return manifest, files


def validate_f0(path: Path) -> dict[str, Any]:
    if sha256_path(path) != EXPECTED_F0_SHA256:
        raise ValueError("F0 SHA-256 mismatch")
    f0 = json.loads(path.read_text(encoding="utf-8"))
    if f0.get("schema") != "ATDS_E0_SOURCE_B_F0_FOOTER_CENSUS_V0_1":
        raise ValueError("unexpected F0 schema")
    if f0.get("status") != "F0_COMPLETE":
        raise ValueError("F0 is not F0_COMPLETE")
    binding = f0.get("binding") or {}
    if binding.get("manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise ValueError("F0 manifest binding mismatch")
    if binding.get("inventory_digest") != EXPECTED_INVENTORY_DIGEST:
        raise ValueError("F0 inventory digest binding mismatch")
    meta = f0.get("metadata_census") or {}
    if meta.get("files_decoded") != EXPECTED_FILES:
        raise ValueError("F0 files_decoded mismatch")
    if meta.get("total_rows") != EXPECTED_ROWS:
        raise ValueError("F0 total_rows mismatch")
    if meta.get("total_row_groups") != EXPECTED_ROW_GROUPS:
        raise ValueError("F0 total_row_groups mismatch")
    if meta.get("unique_schema_signatures") != 1:
        raise ValueError("F0 schema is not unique")
    counts = meta.get("schema_signature_counts") or {}
    if counts != {EXPECTED_SCHEMA_SIGNATURE: EXPECTED_FILES}:
        raise ValueError("F0 schema signature count mismatch")
    if meta.get("temporal_field_candidates") != [EXPECTED_TIMESTAMP_FIELD]:
        raise ValueError("F0 timestamp candidate mismatch")
    stats = (meta.get("temporal_statistics") or {}).get(EXPECTED_TIMESTAMP_FIELD) or {}
    if stats.get("row_groups_with_stats") != EXPECTED_ROW_GROUPS:
        raise ValueError("F0 timestamp stats coverage mismatch")
    if stats.get("row_groups_without_stats") != 0:
        raise ValueError("F0 reports row groups without timestamp stats")
    return f0


def push_largest_gap(
    heap: list[tuple[int, int, dict[str, Any]]],
    serial: int,
    record: dict[str, Any],
) -> None:
    item = (int(record["gap_ms"]), serial, record)
    if len(heap) < TOP_LARGEST_GAPS:
        heapq.heappush(heap, item)
    elif item[0] > heap[0][0]:
        heapq.heapreplace(heap, item)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="E0 Source-B F1: timestamp-only continuity inventory. No price/volume reads."
    )
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--f0-report", required=True)
    parser.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-E0-SOURCE-B-F1-TIMESTAMP-SCAN.json"),
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve(strict=False)
    corpus = (repo_root / "data" / "research_source_b_ustech" / "parquet").resolve(strict=False)
    manifest_path = Path(args.manifest).expanduser().resolve(strict=False)
    f0_path = Path(args.f0_report).expanduser().resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)

    # Zero corpus-write guard must precede any report write.
    if output == corpus or is_within(output, corpus):
        print("BLOCKED_OUTPUT_INSIDE_CORPUS")
        return 2

    report: dict[str, Any] = {
        "schema": "ATDS_E0_SOURCE_B_F1_TIMESTAMP_SCAN_V0_1",
        "binding": {
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "f0_sha256": EXPECTED_F0_SHA256,
            "inventory_digest": EXPECTED_INVENTORY_DIGEST,
            "schema_signature": EXPECTED_SCHEMA_SIGNATURE,
            "timestamp_field": EXPECTED_TIMESTAMP_FIELD,
            "timestamp_type": EXPECTED_TIMESTAMP_TYPE,
        },
        "budget": {
            "max_cumulative_parquet_logical_read_bytes": MAX_CUMULATIVE_PARQUET_LOGICAL_READ_BYTES,
            "manifest_hash_read_bytes": MANIFEST_HASH_READ_BYTES,
            "f0_logical_metadata_read_bytes": F0_LOGICAL_METADATA_READ_BYTES,
            "planned_timestamp_decoded_bytes": PLANNED_TIMESTAMP_DECODED_BYTES,
            "planned_cumulative_logical_bytes": PLANNED_CUMULATIVE_LOGICAL_BYTES,
            "physical_os_read_bytes_measured": False,
        },
        "read_contract": {
            "columns_requested": [EXPECTED_TIMESTAMP_FIELD],
            "price_columns_requested": [],
            "volume_columns_requested": [],
            "corpus_writes": 0,
            "strategy_calculation": False,
            "signal_calculation": False,
            "return_calculation": False,
            "trade_or_pnl_calculation": False,
            "provider_network": False,
            "row_group_streaming": True,
        },
        "interpretation_contract": {
            "timezone_claim": None,
            "session_claim": None,
            "gap_abnormality_claim": None,
            "equal_adjacent_timestamp_is_duplicate_row_claim": False,
        },
        "status": "PRECHECK",
        "reason": None,
        "summary": {},
        "gap_threshold_counts": {name: 0 for name in GAP_THRESHOLDS_MS},
        "files": [],
        "recorded_gaps_gt_60s": [],
        "recorded_backwards": [],
        "largest_gaps": [],
    }

    if PLANNED_CUMULATIVE_LOGICAL_BYTES > MAX_CUMULATIVE_PARQUET_LOGICAL_READ_BYTES:
        blocked(output, report, "BLOCKED_F1_LOGICAL_READ_BUDGET", "Planned cumulative logical bytes exceed 16 GiB.")
    if not manifest_path.is_file():
        blocked(output, report, "BLOCKED_MANIFEST_NOT_FOUND", str(manifest_path))
    if not f0_path.is_file():
        blocked(output, report, "BLOCKED_F0_NOT_FOUND", str(f0_path))
    if not corpus.is_dir():
        blocked(output, report, "BLOCKED_CORPUS_NOT_FOUND", str(corpus))
    if is_reparse_or_symlink(corpus):
        blocked(output, report, "BLOCKED_REPARSE_POINT", "Corpus root is symlink/reparse.")

    try:
        _, manifest_files = validate_manifest(manifest_path)
        f0 = validate_f0(f0_path)
    except Exception as exc:
        blocked(output, report, "BLOCKED_BINDING", str(exc))

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
    except Exception as exc:
        blocked(output, report, "BLOCKED_RUNTIME_DEPENDENCY", str(exc))

    f0_files = {row["relative_path"]: row for row in (f0.get("files") or [])}
    if len(f0_files) != EXPECTED_FILES:
        blocked(output, report, "BLOCKED_F0_FILE_MAP", "F0 file map is incomplete.")

    total_rows_read = 0
    total_nulls = 0
    total_valid = 0
    total_equal_adjacent = 0
    total_backward = 0
    total_positive = 0
    global_min: int | None = None
    global_max: int | None = None
    previous_last_valid: int | None = None
    previous_location: dict[str, Any] | None = None
    boundaries_evaluated = 0
    boundaries_broken_by_null = 0
    gap_records_truncated = False
    backward_records_truncated = False
    largest_heap: list[tuple[int, int, dict[str, Any]]] = []
    serial = 0

    def register_transition(
        prev_ms: int,
        curr_ms: int,
        location: dict[str, Any],
        prev_loc: dict[str, Any],
    ) -> None:
        nonlocal total_equal_adjacent, total_backward, total_positive
        nonlocal gap_records_truncated, backward_records_truncated, serial

        diff = int(curr_ms) - int(prev_ms)
        if diff == 0:
            total_equal_adjacent += 1
            return
        if diff < 0:
            total_backward += 1
            if len(report["recorded_backwards"]) < MAX_RECORDED_BACKWARDS:
                report["recorded_backwards"].append({
                    "previous_ms": int(prev_ms),
                    "current_ms": int(curr_ms),
                    "delta_ms": diff,
                    "previous_naive_iso": naive_epoch_ms_iso(prev_ms),
                    "current_naive_iso": naive_epoch_ms_iso(curr_ms),
                    "previous_location": prev_loc,
                    "current_location": location,
                })
            else:
                backward_records_truncated = True
            return

        total_positive += 1
        for name, threshold in GAP_THRESHOLDS_MS.items():
            if diff > threshold:
                report["gap_threshold_counts"][name] += 1

        if diff > RECORD_GAP_THRESHOLD_MS:
            record = {
                "gap_ms": diff,
                "previous_ms": int(prev_ms),
                "current_ms": int(curr_ms),
                "previous_naive_iso": naive_epoch_ms_iso(prev_ms),
                "current_naive_iso": naive_epoch_ms_iso(curr_ms),
                "previous_location": prev_loc,
                "current_location": location,
            }
            serial += 1
            push_largest_gap(largest_heap, serial, record)
            if len(report["recorded_gaps_gt_60s"]) < MAX_RECORDED_GAPS:
                report["recorded_gaps_gt_60s"].append(record)
            else:
                gap_records_truncated = True

    for file_index, manifest_row in enumerate(manifest_files):
        rel = manifest_row["relative_path"]
        path = (corpus / Path(rel)).resolve(strict=False)
        if not is_within(path, corpus):
            blocked(output, report, "BLOCKED_PATH_ESCAPE", rel)
        if not path.is_file():
            blocked(output, report, "BLOCKED_FILE_MISSING", rel)
        if is_reparse_or_symlink(path):
            blocked(output, report, "BLOCKED_REPARSE_POINT", rel)

        st = path.stat(follow_symlinks=False)
        if int(st.st_size) != int(manifest_row["size_bytes"]) or int(st.st_mtime_ns) != int(manifest_row["mtime_ns"]):
            blocked(output, report, "BLOCKED_FILE_METADATA_CHANGED", rel)

        f0_row = f0_files.get(rel)
        if f0_row is None:
            blocked(output, report, "BLOCKED_F0_FILE_MISSING", rel)
        if f0_row.get("schema_signature") != EXPECTED_SCHEMA_SIGNATURE:
            blocked(output, report, "BLOCKED_SCHEMA_DRIFT", rel)

        try:
            pf = pq.ParquetFile(path)
        except Exception as exc:
            blocked(output, report, "BLOCKED_PARQUET_OPEN", f"{rel}: {exc}")

        if int(pf.metadata.num_rows) != int(f0_row["num_rows"]):
            blocked(output, report, "BLOCKED_ROW_COUNT_DRIFT", rel)
        if int(pf.metadata.num_row_groups) != int(f0_row["num_row_groups"]):
            blocked(output, report, "BLOCKED_ROW_GROUP_DRIFT", rel)

        file_rows_read = 0
        file_nulls = 0
        file_equal = 0
        file_backward = 0
        file_positive = 0
        file_min: int | None = None
        file_max: int | None = None
        file_first: int | None = None
        file_last: int | None = None
        file_gap_counts = {name: 0 for name in GAP_THRESHOLDS_MS}

        for rg_index in range(int(pf.metadata.num_row_groups)):
            try:
                table = pf.read_row_group(
                    rg_index,
                    columns=[EXPECTED_TIMESTAMP_FIELD],
                    use_threads=False,
                )
            except Exception as exc:
                blocked(output, report, "BLOCKED_TIMESTAMP_READ", f"{rel} rg={rg_index}: {exc}")

            if table.num_columns != 1 or table.column_names != [EXPECTED_TIMESTAMP_FIELD]:
                blocked(output, report, "BLOCKED_COLUMN_SCOPE", f"{rel} rg={rg_index}")

            col = table.column(0).combine_chunks()
            rg_rows = len(col)
            file_rows_read += rg_rows
            total_rows_read += rg_rows
            nulls = int(col.null_count)
            file_nulls += nulls
            total_nulls += nulls

            if rg_rows == 0:
                continue

            # Convert only timestamp to int64 milliseconds. Nulls are filled only
            # for transport to NumPy; they are excluded from continuity segments.
            try:
                ints = pc.fill_null(pc.cast(col, pa.int64()), 0).to_numpy(zero_copy_only=False)
                valid = pc.invert(pc.is_null(col)).to_numpy(zero_copy_only=False)
            except Exception as exc:
                blocked(output, report, "BLOCKED_TIMESTAMP_CAST", f"{rel} rg={rg_index}: {exc}")

            valid_idx = np.flatnonzero(valid)
            valid_count = int(valid_idx.size)
            total_valid += valid_count
            if valid_count == 0:
                previous_last_valid = None
                previous_location = None
                boundaries_broken_by_null += 1
                continue

            valid_values = ints[valid_idx].astype(np.int64, copy=False)
            rg_min = int(valid_values.min())
            rg_max = int(valid_values.max())
            global_min = rg_min if global_min is None else min(global_min, rg_min)
            global_max = rg_max if global_max is None else max(global_max, rg_max)
            file_min = rg_min if file_min is None else min(file_min, rg_min)
            file_max = rg_max if file_max is None else max(file_max, rg_max)

            first_idx = int(valid_idx[0])
            last_idx = int(valid_idx[-1])
            first_val = int(valid_values[0])
            last_val = int(valid_values[-1])
            if file_first is None:
                file_first = first_val
            file_last = last_val

            first_location = {
                "file": rel,
                "row_group": rg_index,
                "row_index_in_group": first_idx,
            }

            # Boundary transition is valid only if prior row was valid and
            # this row group starts with a valid row.
            if previous_last_valid is not None and previous_location is not None and first_idx == 0:
                before = dict(report["gap_threshold_counts"])
                eq0, bw0, pos0 = total_equal_adjacent, total_backward, total_positive
                register_transition(previous_last_valid, first_val, first_location, previous_location)
                boundaries_evaluated += 1
                file_equal += total_equal_adjacent - eq0
                file_backward += total_backward - bw0
                file_positive += total_positive - pos0
                for name in GAP_THRESHOLDS_MS:
                    file_gap_counts[name] += report["gap_threshold_counts"][name] - before[name]
            elif previous_last_valid is not None:
                boundaries_broken_by_null += 1

            # Process contiguous valid segments only. Never bridge across nulls.
            segment_starts = [0]
            discontinuities = np.flatnonzero(np.diff(valid_idx) != 1)
            segment_starts.extend((discontinuities + 1).tolist())
            segment_ends = discontinuities.tolist()
            segment_ends.append(valid_count - 1)

            for s, e in zip(segment_starts, segment_ends):
                seg = valid_values[s:e + 1]
                seg_idx = valid_idx[s:e + 1]
                if seg.size < 2:
                    continue
                diffs = np.diff(seg)

                eq_count = int(np.count_nonzero(diffs == 0))
                bw_count = int(np.count_nonzero(diffs < 0))
                pos_count = int(np.count_nonzero(diffs > 0))
                total_equal_adjacent += eq_count
                total_backward += bw_count
                total_positive += pos_count
                file_equal += eq_count
                file_backward += bw_count
                file_positive += pos_count

                for name, threshold in GAP_THRESHOLDS_MS.items():
                    count = int(np.count_nonzero(diffs > threshold))
                    report["gap_threshold_counts"][name] += count
                    file_gap_counts[name] += count

                interesting = np.flatnonzero(diffs > RECORD_GAP_THRESHOLD_MS)
                for j in interesting:
                    j = int(j)
                    prev_v = int(seg[j])
                    curr_v = int(seg[j + 1])
                    prev_loc = {
                        "file": rel,
                        "row_group": rg_index,
                        "row_index_in_group": int(seg_idx[j]),
                    }
                    curr_loc = {
                        "file": rel,
                        "row_group": rg_index,
                        "row_index_in_group": int(seg_idx[j + 1]),
                    }
                    record = {
                        "gap_ms": curr_v - prev_v,
                        "previous_ms": prev_v,
                        "current_ms": curr_v,
                        "previous_naive_iso": naive_epoch_ms_iso(prev_v),
                        "current_naive_iso": naive_epoch_ms_iso(curr_v),
                        "previous_location": prev_loc,
                        "current_location": curr_loc,
                    }
                    serial += 1
                    push_largest_gap(largest_heap, serial, record)
                    if len(report["recorded_gaps_gt_60s"]) < MAX_RECORDED_GAPS:
                        report["recorded_gaps_gt_60s"].append(record)
                    else:
                        gap_records_truncated = True

                backwards = np.flatnonzero(diffs < 0)
                for j in backwards[: max(0, MAX_RECORDED_BACKWARDS - len(report["recorded_backwards"]))]:
                    j = int(j)
                    prev_v = int(seg[j])
                    curr_v = int(seg[j + 1])
                    report["recorded_backwards"].append({
                        "previous_ms": prev_v,
                        "current_ms": curr_v,
                        "delta_ms": curr_v - prev_v,
                        "previous_naive_iso": naive_epoch_ms_iso(prev_v),
                        "current_naive_iso": naive_epoch_ms_iso(curr_v),
                        "previous_location": {
                            "file": rel,
                            "row_group": rg_index,
                            "row_index_in_group": int(seg_idx[j]),
                        },
                        "current_location": {
                            "file": rel,
                            "row_group": rg_index,
                            "row_index_in_group": int(seg_idx[j + 1]),
                        },
                    })
                if len(backwards) > max(0, MAX_RECORDED_BACKWARDS - len(report["recorded_backwards"])):
                    backward_records_truncated = True

            # Preserve only a boundary if the row group's last physical row is valid.
            if last_idx == rg_rows - 1:
                previous_last_valid = last_val
                previous_location = {
                    "file": rel,
                    "row_group": rg_index,
                    "row_index_in_group": last_idx,
                }
            else:
                previous_last_valid = None
                previous_location = None
                boundaries_broken_by_null += 1

            del table, col, ints, valid, valid_idx, valid_values

        if file_rows_read != int(f0_row["num_rows"]):
            blocked(output, report, "BLOCKED_FILE_ROWS_READ_MISMATCH", rel)

        st_after = path.stat(follow_symlinks=False)
        if int(st_after.st_size) != int(manifest_row["size_bytes"]) or int(st_after.st_mtime_ns) != int(manifest_row["mtime_ns"]):
            blocked(output, report, "BLOCKED_FILE_CHANGED_DURING_F1", rel)

        report["files"].append({
            "relative_path": rel,
            "rows_read": file_rows_read,
            "null_timestamps": file_nulls,
            "first_valid_ms": file_first,
            "last_valid_ms": file_last,
            "min_valid_ms": file_min,
            "max_valid_ms": file_max,
            "first_valid_naive_iso": naive_epoch_ms_iso(file_first),
            "last_valid_naive_iso": naive_epoch_ms_iso(file_last),
            "min_valid_naive_iso": naive_epoch_ms_iso(file_min),
            "max_valid_naive_iso": naive_epoch_ms_iso(file_max),
            "equal_adjacent_timestamps": file_equal,
            "backward_transitions": file_backward,
            "positive_transitions": file_positive,
            "gap_threshold_counts": file_gap_counts,
        })

    if total_rows_read != EXPECTED_ROWS:
        blocked(output, report, "BLOCKED_TOTAL_ROWS_READ_MISMATCH", f"{total_rows_read} != {EXPECTED_ROWS}")

    report["largest_gaps"] = [
        item[2] for item in sorted(largest_heap, key=lambda x: (-x[0], x[1]))
    ]
    report["summary"] = {
        "rows_read": total_rows_read,
        "valid_timestamps": total_valid,
        "null_timestamps": total_nulls,
        "global_min_ms": global_min,
        "global_max_ms": global_max,
        "global_min_naive_iso": naive_epoch_ms_iso(global_min),
        "global_max_naive_iso": naive_epoch_ms_iso(global_max),
        "equal_adjacent_timestamps": total_equal_adjacent,
        "backward_transitions": total_backward,
        "positive_transitions": total_positive,
        "boundaries_evaluated": boundaries_evaluated,
        "boundaries_broken_by_null": boundaries_broken_by_null,
        "recorded_gaps_gt_60s": len(report["recorded_gaps_gt_60s"]),
        "gap_records_truncated": gap_records_truncated,
        "recorded_backwards": len(report["recorded_backwards"]),
        "backward_records_truncated": backward_records_truncated,
        "largest_gap_ms": (
            max((x[0] for x in largest_heap), default=None)
        ),
        "timezone_qualified": False,
        "session_calendar_applied": False,
    }

    report["runtime"] = {
        "pyarrow_version": pa.__version__,
        "numpy_version": np.__version__,
    }
    report["status"] = "F1_COMPLETE"
    report["reason"] = (
        "Timestamp-only row-group scan completed. Raw temporal structure inventoried; "
        "timezone/session interpretation remains separate."
    )
    write_json(output, report)

    print("F1_COMPLETE")
    print(f"Rows read: {total_rows_read}")
    print(f"Null timestamps: {total_nulls}")
    print(f"Backward transitions: {total_backward}")
    print(f"Equal adjacent timestamps: {total_equal_adjacent}")
    print(f"Gaps >60s: {report['gap_threshold_counts']['gt_60s']}")
    print(f"Largest gap ms: {report['summary']['largest_gap_ms']}")
    print(f"Report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

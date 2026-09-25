#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_MANIFEST_SHA256 = "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
EXPECTED_F0_SHA256 = "5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b"
EXPECTED_F1_SHA256 = "2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067"
EXPECTED_F2_SHA256 = "6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29"
EXPECTED_INVENTORY_DIGEST = "5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
EXPECTED_SCHEMA_SIGNATURE = "c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d"
EXPECTED_FILES = 212
EXPECTED_ROWS = 376_003_618
EXPECTED_GAPS_GT_60S = 1_605
EXPECTED_SEGMENTS = 1_606
EXPECTED_FIRST_MS = 1_621_900_800_309
EXPECTED_LAST_MS = 1_779_667_199_963
GAP_THRESHOLD_MS = 60_000

MAX_LOGICAL_SOURCE_DECODE_BYTES = 12 * 1024**3
PLANNED_LOGICAL_SOURCE_DECODE_BYTES = EXPECTED_ROWS * 3 * 8
MAX_OUTPUT_BYTES = 4 * 1024**3
MAX_OUTPUT_FILES = 100

SOURCE_COLUMNS = ["timestamp", "bid_price", "ask_price"]
OUTPUT_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    h = hashlib.sha256()
    for row in files:
        h.update(
            f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n".encode("utf-8")
        )
    return h.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        c = os.path.normcase(str(child.resolve(strict=False)))
        p = os.path.normcase(str(parent.resolve(strict=False)))
        return os.path.commonpath([c, p]) == p
    except ValueError:
        return False


def is_reparse_or_symlink(path: Path) -> bool:
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def month_key_from_ms(ms: int) -> tuple[int, int]:
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.year, dt.month


def iso_ms(ms: int | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat(timespec="milliseconds")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="AP0: gap-aware 1-minute descriptive transformation for USTECH price-core."
    )
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--f0-report", required=True)
    ap.add_argument("--f1-report", required=True)
    ap.add_argument("--f2-report", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve(strict=False)
    corpus = (repo_root / "data" / "research_source_b_ustech" / "parquet").resolve(strict=False)
    manifest_path = Path(args.manifest).expanduser().resolve(strict=False)
    f0_path = Path(args.f0_report).expanduser().resolve(strict=False)
    f1_path = Path(args.f1_report).expanduser().resolve(strict=False)
    f2_path = Path(args.f2_report).expanduser().resolve(strict=False)
    output_root = Path(args.output_root).expanduser().resolve(strict=False)

    def block(code: str, reason: str) -> int:
        print(code)
        print(reason)
        print(f"Output root: {output_root}")
        if output_root.exists() and output_root.is_dir():
            try:
                write_json(
                    output_root / "AP0-BLOCKED.json",
                    {
                        "schema": "ATDS_AP0_BLOCKED_V0_1",
                        "status": code,
                        "reason": reason,
                        "output_identity": OUTPUT_IDENTITY,
                    },
                )
            except Exception:
                pass
        return 2

    if PLANNED_LOGICAL_SOURCE_DECODE_BYTES > MAX_LOGICAL_SOURCE_DECODE_BYTES:
        return block("BLOCKED_AP0_READ_BUDGET", "Planned logical source decode exceeds 12 GiB.")
    if output_root.exists():
        return block("BLOCKED_AP0_OUTPUT_EXISTS", "Output root must not already exist.")
    if output_root == corpus or is_within(output_root, corpus):
        return block("BLOCKED_AP0_OUTPUT_INSIDE_SOURCE", "Output root must be outside source corpus.")
    if not corpus.is_dir():
        return block("BLOCKED_AP0_CORPUS_NOT_FOUND", str(corpus))
    if is_reparse_or_symlink(corpus):
        return block("BLOCKED_AP0_REPARSE_POINT", "Source corpus root is symlink/reparse.")

    for p, label in [
        (manifest_path, "manifest"),
        (f0_path, "F0"),
        (f1_path, "F1"),
        (f2_path, "F2"),
    ]:
        if not p.is_file():
            return block("BLOCKED_AP0_INPUT_NOT_FOUND", f"{label}: {p}")

    if sha256_path(manifest_path) != EXPECTED_MANIFEST_SHA256:
        return block("BLOCKED_AP0_BINDING", "manifest SHA-256 mismatch")
    if sha256_path(f0_path) != EXPECTED_F0_SHA256:
        return block("BLOCKED_AP0_BINDING", "F0 SHA-256 mismatch")
    if sha256_path(f1_path) != EXPECTED_F1_SHA256:
        return block("BLOCKED_AP0_BINDING", "F1 SHA-256 mismatch")
    if sha256_path(f2_path) != EXPECTED_F2_SHA256:
        return block("BLOCKED_AP0_BINDING", "F2 SHA-256 mismatch")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        f0 = json.loads(f0_path.read_text(encoding="utf-8"))
        f1 = json.loads(f1_path.read_text(encoding="utf-8"))
        f2 = json.loads(f2_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return block("BLOCKED_AP0_JSON_PARSE", str(exc))

    inventory = manifest.get("inventory") or {}
    source_files = inventory.get("files")
    if manifest.get("status") != "MANIFEST_COMPLETE":
        return block("BLOCKED_AP0_MANIFEST_CONTRACT", "Manifest is not complete.")
    if not isinstance(source_files, list) or len(source_files) != EXPECTED_FILES:
        return block("BLOCKED_AP0_MANIFEST_CONTRACT", "Manifest file count mismatch.")
    if canonical_inventory_digest(source_files) != EXPECTED_INVENTORY_DIGEST:
        return block("BLOCKED_AP0_MANIFEST_CONTRACT", "Inventory digest mismatch.")

    f0_meta = f0.get("metadata_census") or {}
    if f0.get("status") != "F0_COMPLETE":
        return block("BLOCKED_AP0_F0_CONTRACT", "F0 is not complete.")
    if f0_meta.get("total_rows") != EXPECTED_ROWS:
        return block("BLOCKED_AP0_F0_CONTRACT", "F0 row count mismatch.")
    if f0_meta.get("schema_signature_counts") != {EXPECTED_SCHEMA_SIGNATURE: EXPECTED_FILES}:
        return block("BLOCKED_AP0_F0_CONTRACT", "F0 schema signature mismatch.")
    f0_map = {row["relative_path"]: row for row in (f0.get("files") or [])}
    if len(f0_map) != EXPECTED_FILES:
        return block("BLOCKED_AP0_F0_CONTRACT", "F0 file map incomplete.")

    f1_summary = f1.get("summary") or {}
    if f1.get("status") != "F1_COMPLETE":
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 is not complete.")
    if f1_summary.get("rows_read") != EXPECTED_ROWS:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 row count mismatch.")
    if f1_summary.get("null_timestamps") != 0:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 has null timestamps.")
    if f1_summary.get("backward_transitions") != 0 or f1_summary.get("equal_adjacent_timestamps") != 0:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 timestamps are not strictly increasing.")
    if f1_summary.get("recorded_gaps_gt_60s") != EXPECTED_GAPS_GT_60S:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 gap count mismatch.")
    if f1_summary.get("gap_records_truncated") is not False:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 gap register is truncated.")
    if f1_summary.get("global_min_ms") != EXPECTED_FIRST_MS or f1_summary.get("global_max_ms") != EXPECTED_LAST_MS:
        return block("BLOCKED_AP0_F1_CONTRACT", "F1 temporal bounds mismatch.")

    f2_summary = f2.get("summary") or {}
    if f2.get("status") != "F2_COMPLETE" or f2_summary.get("rows_read") != EXPECTED_ROWS:
        return block("BLOCKED_AP0_F2_CONTRACT", "F2 contract mismatch.")
    for key in (
        "bid_null", "ask_null", "bid_nonfinite_nonnull", "ask_nonfinite_nonnull",
        "bid_nonpositive", "ask_nonpositive", "ask_lt_bid", "nonpositive_spread", "zero_spread"
    ):
        if f2_summary.get(key) != 0:
            return block("BLOCKED_AP0_F2_CONTRACT", f"F2 invalid counter non-zero: {key}")

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
    except Exception as exc:
        return block("BLOCKED_AP0_RUNTIME_DEPENDENCY", str(exc))

    output_root.mkdir(parents=True, exist_ok=False)

    output_schema = pa.schema(
        [
            ("minute_start_ms_utc", pa.int64()),
            ("first_tick_ms", pa.int64()),
            ("last_tick_ms", pa.int64()),
            ("tick_count", pa.int64()),
            ("segment_id", pa.int64()),
            ("segment_start", pa.bool_()),
            ("gap_before_ms", pa.int64()),
            ("mid_open", pa.float64()),
            ("mid_high", pa.float64()),
            ("mid_low", pa.float64()),
            ("mid_close", pa.float64()),
            ("spread_mean", pa.float64()),
            ("spread_min", pa.float64()),
            ("spread_max", pa.float64()),
        ],
        metadata={
            b"dataset_identity": OUTPUT_IDENTITY.encode(),
            b"source_identity": b"SOURCE_B_USTECH_PRICE_CORE_V0_1",
            b"time_semantics": b"UTC epoch milliseconds",
            b"mid_semantics": b"descriptive_only_not_execution_price",
            b"spread_mean_weighting": b"tick_weighted",
            b"gap_threshold_ms": str(GAP_THRESHOLD_MS).encode(),
            b"volumes_used": b"false",
        },
    )

    monthly_records: list[dict[str, Any]] = []
    current_month: tuple[int, int] | None = None
    pending: dict[str, Any] | None = None
    prev_tick_ms: int | None = None
    segment_id = 0
    gap_count = 0
    source_rows_read = 0
    minute_rows_written = 0
    output_files: list[dict[str, Any]] = []
    total_output_bytes = 0
    observed_first_ms: int | None = None
    observed_last_ms: int | None = None

    def flush_month(key: tuple[int, int], records: list[dict[str, Any]]) -> None:
        nonlocal minute_rows_written, total_output_bytes
        if not records:
            return
        if len(output_files) >= MAX_OUTPUT_FILES:
            raise RuntimeError("Output file cap exceeded.")

        year, month = key
        rel = Path(f"year={year:04d}") / f"month={month:02d}" / f"USTECH-PROFILE-M1-{year:04d}-{month:02d}.parquet"
        out_path = output_root / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cols = {name: [r[name] for r in records] for name in output_schema.names}
        table = pa.Table.from_pydict(cols, schema=output_schema)
        pq.write_table(
            table,
            out_path,
            compression="snappy",
            use_dictionary=False,
            write_statistics=True,
        )

        rows = int(table.num_rows)
        source_ticks = int(sum(r["tick_count"] for r in records))
        size = int(out_path.stat().st_size)
        total_output_bytes += size
        if total_output_bytes > MAX_OUTPUT_BYTES:
            raise RuntimeError("Output byte cap exceeded.")

        # Self-verify persisted output.
        pf = pq.ParquetFile(out_path)
        if int(pf.metadata.num_rows) != rows:
            raise RuntimeError(f"Output row verification failed: {rel.as_posix()}")
        if pf.schema_arrow != output_schema:
            raise RuntimeError(f"Output schema verification failed: {rel.as_posix()}")

        output_files.append(
            {
                "relative_path": rel.as_posix(),
                "rows": rows,
                "source_ticks": source_ticks,
                "size_bytes": size,
                "sha256": sha256_path(out_path),
                "first_minute_ms_utc": int(records[0]["minute_start_ms_utc"]),
                "last_minute_ms_utc": int(records[-1]["minute_start_ms_utc"]),
                "first_segment_id": int(records[0]["segment_id"]),
                "last_segment_id": int(records[-1]["segment_id"]),
            }
        )
        minute_rows_written += rows

    def emit_finalized(row: dict[str, Any]) -> None:
        nonlocal current_month, monthly_records
        key = month_key_from_ms(int(row["minute_start_ms_utc"]))
        if current_month is None:
            current_month = key
        if key != current_month:
            flush_month(current_month, monthly_records)
            monthly_records = []
            current_month = key
        monthly_records.append(row)

    def finalize_pending() -> None:
        nonlocal pending
        if pending is None:
            return
        count = int(pending.pop("_spread_count"))
        spread_sum = float(pending.pop("_spread_sum"))
        if count != int(pending["tick_count"]) or count <= 0:
            raise RuntimeError("Pending spread count mismatch.")
        pending["spread_mean"] = spread_sum / count
        emit_finalized(pending)
        pending = None

    try:
        for source_index, mrow in enumerate(source_files):
            rel = mrow["relative_path"]
            src = (corpus / Path(rel)).resolve(strict=False)
            if not is_within(src, corpus):
                raise RuntimeError(f"Source path escape: {rel}")
            if not src.is_file() or is_reparse_or_symlink(src):
                raise RuntimeError(f"Invalid source file path: {rel}")

            st = src.stat(follow_symlinks=False)
            if int(st.st_size) != int(mrow["size_bytes"]) or int(st.st_mtime_ns) != int(mrow["mtime_ns"]):
                raise RuntimeError(f"Source metadata changed: {rel}")

            f0row = f0_map.get(rel)
            if f0row is None or f0row.get("schema_signature") != EXPECTED_SCHEMA_SIGNATURE:
                raise RuntimeError(f"F0 binding missing/drift: {rel}")

            pf = pq.ParquetFile(src)
            if int(pf.metadata.num_rows) != int(f0row["num_rows"]):
                raise RuntimeError(f"Source row count drift: {rel}")
            if int(pf.metadata.num_row_groups) != int(f0row["num_row_groups"]):
                raise RuntimeError(f"Source row-group drift: {rel}")

            file_rows = 0
            for rg in range(int(pf.metadata.num_row_groups)):
                table = pf.read_row_group(rg, columns=SOURCE_COLUMNS, use_threads=False)
                if table.column_names != SOURCE_COLUMNS or table.num_columns != 3:
                    raise RuntimeError(f"Column-scope violation: {rel} rg={rg}")

                ts_arr = table.column(0).combine_chunks()
                bid_arr = table.column(1).combine_chunks()
                ask_arr = table.column(2).combine_chunks()
                n = len(ts_arr)
                if len(bid_arr) != n or len(ask_arr) != n:
                    raise RuntimeError(f"Column length mismatch: {rel} rg={rg}")
                if ts_arr.null_count or bid_arr.null_count or ask_arr.null_count:
                    raise RuntimeError(f"Unexpected null in qualified source: {rel} rg={rg}")

                ts = pc.cast(ts_arr, pa.int64()).to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
                bid = bid_arr.to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
                ask = ask_arr.to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

                if n:
                    if not np.all(np.isfinite(bid)) or not np.all(np.isfinite(ask)):
                        raise RuntimeError(f"Nonfinite price in qualified source: {rel} rg={rg}")
                    if np.any(bid <= 0) or np.any(ask <= 0) or np.any(ask <= bid):
                        raise RuntimeError(f"Invalid bid/ask in qualified source: {rel} rg={rg}")

                    diffs = np.diff(ts)
                    if np.any(diffs <= 0):
                        raise RuntimeError(f"Non-increasing timestamp inside row group: {rel} rg={rg}")
                    if prev_tick_ms is not None and int(ts[0]) <= prev_tick_ms:
                        raise RuntimeError(f"Non-increasing timestamp across boundary: {rel} rg={rg}")

                    observed_first_ms = int(ts[0]) if observed_first_ms is None else observed_first_ms
                    observed_last_ms = int(ts[-1])

                    minute_code = ts // 60_000
                    starts = np.concatenate((
                        np.array([0], dtype=np.int64),
                        np.flatnonzero(minute_code[1:] != minute_code[:-1]).astype(np.int64) + 1,
                    ))
                    ends = np.concatenate((starts[1:], np.array([n], dtype=np.int64)))

                    mid = (bid + ask) / 2.0
                    spread = ask - bid
                    run_open = mid[starts]
                    run_close = mid[ends - 1]
                    run_high = np.maximum.reduceat(mid, starts)
                    run_low = np.minimum.reduceat(mid, starts)
                    run_spread_sum = np.add.reduceat(spread, starts)
                    run_spread_min = np.minimum.reduceat(spread, starts)
                    run_spread_max = np.maximum.reduceat(spread, starts)

                    for i in range(len(starts)):
                        s = int(starts[i])
                        e = int(ends[i])
                        first_ms = int(ts[s])
                        last_ms = int(ts[e - 1])
                        minute_start = int(minute_code[s] * 60_000)
                        count = e - s

                        gap_before: int | None = None
                        segment_start = False
                        if prev_tick_ms is None:
                            segment_start = True
                        else:
                            gap = first_ms - prev_tick_ms
                            if gap > GAP_THRESHOLD_MS:
                                if pending is not None and int(pending["minute_start_ms_utc"]) == minute_start:
                                    raise RuntimeError("Gap >60s occurred inside one UTC minute.")
                                segment_id += 1
                                gap_count += 1
                                gap_before = gap
                                segment_start = True

                        run = {
                            "minute_start_ms_utc": minute_start,
                            "first_tick_ms": first_ms,
                            "last_tick_ms": last_ms,
                            "tick_count": count,
                            "segment_id": segment_id,
                            "segment_start": segment_start,
                            "gap_before_ms": gap_before,
                            "mid_open": float(run_open[i]),
                            "mid_high": float(run_high[i]),
                            "mid_low": float(run_low[i]),
                            "mid_close": float(run_close[i]),
                            "spread_min": float(run_spread_min[i]),
                            "spread_max": float(run_spread_max[i]),
                            "_spread_sum": float(run_spread_sum[i]),
                            "_spread_count": count,
                        }

                        if pending is None:
                            pending = run
                        elif int(pending["minute_start_ms_utc"]) == minute_start:
                            if segment_start or int(pending["segment_id"]) != segment_id:
                                raise RuntimeError("Segment boundary cannot merge into same minute.")
                            pending["last_tick_ms"] = last_ms
                            pending["tick_count"] = int(pending["tick_count"]) + count
                            pending["mid_high"] = max(float(pending["mid_high"]), float(run["mid_high"]))
                            pending["mid_low"] = min(float(pending["mid_low"]), float(run["mid_low"]))
                            pending["mid_close"] = float(run["mid_close"])
                            pending["spread_min"] = min(float(pending["spread_min"]), float(run["spread_min"]))
                            pending["spread_max"] = max(float(pending["spread_max"]), float(run["spread_max"]))
                            pending["_spread_sum"] = float(pending["_spread_sum"]) + float(run["_spread_sum"])
                            pending["_spread_count"] = int(pending["_spread_count"]) + count
                        else:
                            finalize_pending()
                            pending = run

                        prev_tick_ms = last_ms

                source_rows_read += n
                file_rows += n
                del table, ts_arr, bid_arr, ask_arr, ts, bid, ask

            if file_rows != int(f0row["num_rows"]):
                raise RuntimeError(f"Per-file rows mismatch after AP0 read: {rel}")

            st2 = src.stat(follow_symlinks=False)
            if int(st2.st_size) != int(mrow["size_bytes"]) or int(st2.st_mtime_ns) != int(mrow["mtime_ns"]):
                raise RuntimeError(f"Source changed during AP0: {rel}")

        finalize_pending()
        if current_month is not None:
            flush_month(current_month, monthly_records)
            monthly_records = []

        if source_rows_read != EXPECTED_ROWS:
            raise RuntimeError(f"Source rows read {source_rows_read} != {EXPECTED_ROWS}")
        if observed_first_ms != EXPECTED_FIRST_MS or observed_last_ms != EXPECTED_LAST_MS:
            raise RuntimeError("Observed source bounds mismatch.")
        if gap_count != EXPECTED_GAPS_GT_60S:
            raise RuntimeError(f"Gap count {gap_count} != {EXPECTED_GAPS_GT_60S}")
        if segment_id + 1 != EXPECTED_SEGMENTS:
            raise RuntimeError(f"Segment count {segment_id + 1} != {EXPECTED_SEGMENTS}")
        if len(output_files) > MAX_OUTPUT_FILES:
            raise RuntimeError("Output file cap exceeded.")
        if not output_files:
            raise RuntimeError("No output files written.")

        output_source_ticks = sum(int(x["source_ticks"]) for x in output_files)
        output_rows_sum = sum(int(x["rows"]) for x in output_files)
        if output_source_ticks != EXPECTED_ROWS:
            raise RuntimeError("Output source-tick accounting mismatch.")
        if output_rows_sum != minute_rows_written:
            raise RuntimeError("Output minute-row accounting mismatch.")

        months = [x["relative_path"].split("/")[0] + "/" + x["relative_path"].split("/")[1] for x in output_files]
        if len(months) != len(set(months)):
            raise RuntimeError("Duplicate output month.")

        manifest_out = {
            "schema": "ATDS_AP0_USTECH_PROFILE_MINUTE_CORE_MANIFEST_V0_1",
            "status": "AP0_COMPLETE",
            "output_identity": OUTPUT_IDENTITY,
            "source_identity": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
            "binding": {
                "manifest_sha256": EXPECTED_MANIFEST_SHA256,
                "f0_sha256": EXPECTED_F0_SHA256,
                "f1_sha256": EXPECTED_F1_SHA256,
                "f2_sha256": EXPECTED_F2_SHA256,
                "inventory_digest": EXPECTED_INVENTORY_DIGEST,
                "schema_signature": EXPECTED_SCHEMA_SIGNATURE,
            },
            "transformation_contract": {
                "source_columns": SOURCE_COLUMNS,
                "volume_columns_used": [],
                "minute_definition": "floor(timestamp_ms / 60000)",
                "forward_fill": False,
                "mid_definition": "(bid_price + ask_price) / 2",
                "mid_is_execution_price": False,
                "spread_definition": "ask_price - bid_price",
                "spread_mean_weighting": "tick_weighted",
                "gap_threshold_ms_strictly_greater_than": GAP_THRESHOLD_MS,
                "segment_rule": "increment after each adjacent timestamp gap > 60000 ms",
                "returns_calculated": False,
                "strategy_calculated": False,
                "pnl_calculated": False,
            },
            "budget": {
                "max_logical_source_decode_bytes": MAX_LOGICAL_SOURCE_DECODE_BYTES,
                "planned_logical_source_decode_bytes": PLANNED_LOGICAL_SOURCE_DECODE_BYTES,
                "max_output_bytes": MAX_OUTPUT_BYTES,
                "max_output_files": MAX_OUTPUT_FILES,
                "physical_os_read_bytes_measured": False,
            },
            "coverage": {
                "source_ticks_read": source_rows_read,
                "minute_rows_written": minute_rows_written,
                "gaps_gt_60s": gap_count,
                "segments": segment_id + 1,
                "first_source_tick_ms": observed_first_ms,
                "last_source_tick_ms": observed_last_ms,
                "first_source_tick_utc": iso_ms(observed_first_ms),
                "last_source_tick_utc": iso_ms(observed_last_ms),
                "output_month_files": len(output_files),
                "output_bytes": total_output_bytes,
            },
            "runtime": {
                "numpy_version": np.__version__,
                "pyarrow_version": pa.__version__,
            },
            "source_bytes_rehashed_during_ap0": False,
            "files": output_files,
        }

        manifest_path_out = output_root / "AP0-MANIFEST.json"
        write_json(manifest_path_out, manifest_out)
        manifest_sha = sha256_path(manifest_path_out)

        # Final self-verification of all declared output hashes.
        for rec in output_files:
            p = output_root / rec["relative_path"]
            if not p.is_file() or p.stat().st_size != rec["size_bytes"]:
                raise RuntimeError(f"Final output verification failed: {rec['relative_path']}")
            if sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"Final output hash mismatch: {rec['relative_path']}")

        print("AP0_COMPLETE")
        print(f"Source ticks: {source_rows_read}")
        print(f"Minute rows: {minute_rows_written}")
        print(f"Gaps >60s: {gap_count}")
        print(f"Segments: {segment_id + 1}")
        print(f"Monthly files: {len(output_files)}")
        print(f"Output bytes: {total_output_bytes}")
        print(f"Manifest SHA256: {manifest_sha}")
        print(f"Manifest: {manifest_path_out}")
        return 0

    except Exception as exc:
        return block("BLOCKED_AP0_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())

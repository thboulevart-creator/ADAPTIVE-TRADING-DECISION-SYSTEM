#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import tempfile
from pathlib import Path
from typing import Any

EXPECTED_MANIFEST_SHA256 = "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
EXPECTED_F0_SHA256 = "5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b"
EXPECTED_F1_SHA256 = "2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067"
EXPECTED_INVENTORY_DIGEST = "5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
EXPECTED_SCHEMA_SIGNATURE = "c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d"
EXPECTED_FILES = 212
EXPECTED_ROWS = 376_003_618
EXPECTED_TOTAL_PARQUET_BYTES = 3_936_721_231

MAX_CUMULATIVE_LOGICAL_BYTES = 16 * 1024**3
PRIOR_LOGICAL_BYTES = 6_945_200_507
BID_ASK_DECODED_BYTES = EXPECTED_ROWS * 2 * 8
PLANNED_CUMULATIVE_LOGICAL_BYTES = PRIOR_LOGICAL_BYTES + BID_ASK_DECODED_BYTES

COLUMNS = ["bid_price", "ask_price"]


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath(
            [os.path.normcase(str(child.resolve(strict=False))),
             os.path.normcase(str(parent.resolve(strict=False)))]
        ) == os.path.normcase(str(parent.resolve(strict=False)))
    except ValueError:
        return False


def is_reparse_or_symlink(path: Path) -> bool:
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    h = hashlib.sha256()
    for row in files:
        h.update(
            f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n".encode("utf-8")
        )
    return h.hexdigest()


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def blocked(output: Path, report: dict[str, Any], status: str, reason: str) -> None:
    report["status"] = status
    report["reason"] = reason
    write_json(output, report)
    print(status)
    print(reason)
    print(f"Report: {output}")
    raise SystemExit(2)


def validate_inputs(manifest_path: Path, f0_path: Path, f1_path: Path):
    if sha256_path(manifest_path) != EXPECTED_MANIFEST_SHA256:
        raise ValueError("manifest SHA mismatch")
    if sha256_path(f0_path) != EXPECTED_F0_SHA256:
        raise ValueError("F0 SHA mismatch")
    if sha256_path(f1_path) != EXPECTED_F1_SHA256:
        raise ValueError("F1 SHA mismatch")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    f0 = json.loads(f0_path.read_text(encoding="utf-8"))
    f1 = json.loads(f1_path.read_text(encoding="utf-8"))

    inv = manifest.get("inventory") or {}
    files = inv.get("files")
    if manifest.get("status") != "MANIFEST_COMPLETE":
        raise ValueError("manifest not complete")
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        raise ValueError("manifest file count mismatch")
    if inv.get("total_parquet_bytes") != EXPECTED_TOTAL_PARQUET_BYTES:
        raise ValueError("manifest bytes mismatch")
    if canonical_inventory_digest(files) != EXPECTED_INVENTORY_DIGEST:
        raise ValueError("inventory digest mismatch")

    m = f0.get("metadata_census") or {}
    if f0.get("status") != "F0_COMPLETE":
        raise ValueError("F0 not complete")
    if m.get("total_rows") != EXPECTED_ROWS:
        raise ValueError("F0 row mismatch")
    if m.get("schema_signature_counts") != {EXPECTED_SCHEMA_SIGNATURE: EXPECTED_FILES}:
        raise ValueError("F0 schema mismatch")

    s = f1.get("summary") or {}
    if f1.get("status") != "F1_COMPLETE" or s.get("rows_read") != EXPECTED_ROWS:
        raise ValueError("F1 contract mismatch")
    if s.get("null_timestamps") != 0 or s.get("backward_transitions") != 0:
        raise ValueError("F1 temporal integrity mismatch")

    return files, f0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="E0 Source-B F2: read-only bid/ask quality scan. No volume, signal, strategy or PnL."
    )
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--f0-report", required=True)
    ap.add_argument("--f1-report", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-E0-SOURCE-B-F2-BID-ASK-QUALITY.json"),
    )
    args = ap.parse_args()

    root = Path(args.repo_root).expanduser().resolve(strict=False)
    corpus = (root / "data" / "research_source_b_ustech" / "parquet").resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)
    manifest_path = Path(args.manifest).expanduser().resolve(strict=False)
    f0_path = Path(args.f0_report).expanduser().resolve(strict=False)
    f1_path = Path(args.f1_report).expanduser().resolve(strict=False)

    if output == corpus or is_within(output, corpus):
        print("BLOCKED_OUTPUT_INSIDE_CORPUS")
        return 2

    report: dict[str, Any] = {
        "schema": "ATDS_E0_SOURCE_B_F2_BID_ASK_QUALITY_V0_1",
        "status": "PRECHECK",
        "reason": None,
        "binding": {
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "f0_sha256": EXPECTED_F0_SHA256,
            "f1_sha256": EXPECTED_F1_SHA256,
            "inventory_digest": EXPECTED_INVENTORY_DIGEST,
            "schema_signature": EXPECTED_SCHEMA_SIGNATURE,
        },
        "budget": {
            "max_cumulative_logical_bytes": MAX_CUMULATIVE_LOGICAL_BYTES,
            "prior_logical_bytes": PRIOR_LOGICAL_BYTES,
            "planned_bid_ask_decoded_bytes": BID_ASK_DECODED_BYTES,
            "planned_cumulative_logical_bytes": PLANNED_CUMULATIVE_LOGICAL_BYTES,
            "physical_os_read_bytes_measured": False,
        },
        "read_contract": {
            "columns_requested": COLUMNS,
            "timestamp_requested": False,
            "volume_columns_requested": [],
            "corpus_writes": 0,
            "strategy_calculation": False,
            "signal_calculation": False,
            "return_calculation": False,
            "trade_or_pnl_calculation": False,
            "row_group_streaming": True,
        },
        "summary": {},
        "files": [],
    }

    if PLANNED_CUMULATIVE_LOGICAL_BYTES > MAX_CUMULATIVE_LOGICAL_BYTES:
        blocked(output, report, "BLOCKED_F2_LOGICAL_READ_BUDGET", "F2 would exceed frozen 16 GiB budget.")

    for p, label in [(manifest_path,"manifest"),(f0_path,"F0"),(f1_path,"F1")]:
        if not p.is_file():
            blocked(output, report, "BLOCKED_INPUT_NOT_FOUND", f"{label}: {p}")
    if not corpus.is_dir():
        blocked(output, report, "BLOCKED_CORPUS_NOT_FOUND", str(corpus))
    if is_reparse_or_symlink(corpus):
        blocked(output, report, "BLOCKED_REPARSE_POINT", "corpus root")

    try:
        manifest_files, f0 = validate_inputs(manifest_path, f0_path, f1_path)
    except Exception as exc:
        blocked(output, report, "BLOCKED_BINDING", str(exc))

    try:
        import numpy as np
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
    except Exception as exc:
        blocked(output, report, "BLOCKED_RUNTIME_DEPENDENCY", str(exc))

    f0_map = {r["relative_path"]: r for r in f0.get("files", [])}
    if len(f0_map) != EXPECTED_FILES:
        blocked(output, report, "BLOCKED_F0_FILE_MAP", "F0 file map incomplete")

    total_rows = 0
    bid_null = ask_null = 0
    bid_nonfinite = ask_nonfinite = 0
    bid_nonpositive = ask_nonpositive = 0
    ask_lt_bid = 0
    nonpositive_spread = 0
    zero_spread = 0
    valid_spread_count = 0
    spread_sum = 0.0
    spread_min = math.inf
    spread_max = -math.inf
    bid_min = math.inf
    bid_max = -math.inf
    ask_min = math.inf
    ask_max = -math.inf

    for mrow in manifest_files:
        rel = mrow["relative_path"]
        path = (corpus / Path(rel)).resolve(strict=False)
        if not is_within(path, corpus):
            blocked(output, report, "BLOCKED_PATH_ESCAPE", rel)
        if not path.is_file() or is_reparse_or_symlink(path):
            blocked(output, report, "BLOCKED_FILE_PATH", rel)
        st = path.stat(follow_symlinks=False)
        if int(st.st_size) != int(mrow["size_bytes"]) or int(st.st_mtime_ns) != int(mrow["mtime_ns"]):
            blocked(output, report, "BLOCKED_FILE_METADATA_CHANGED", rel)

        f0row = f0_map.get(rel)
        if f0row is None or f0row.get("schema_signature") != EXPECTED_SCHEMA_SIGNATURE:
            blocked(output, report, "BLOCKED_SCHEMA_BINDING", rel)

        try:
            pf = pq.ParquetFile(path)
        except Exception as exc:
            blocked(output, report, "BLOCKED_PARQUET_OPEN", f"{rel}: {exc}")

        if int(pf.metadata.num_rows) != int(f0row["num_rows"]):
            blocked(output, report, "BLOCKED_ROW_COUNT_DRIFT", rel)
        if int(pf.metadata.num_row_groups) != int(f0row["num_row_groups"]):
            blocked(output, report, "BLOCKED_ROW_GROUP_DRIFT", rel)

        file_counts = {
            "rows": 0, "bid_null": 0, "ask_null": 0,
            "bid_nonfinite": 0, "ask_nonfinite": 0,
            "bid_nonpositive": 0, "ask_nonpositive": 0,
            "ask_lt_bid": 0, "nonpositive_spread": 0, "zero_spread": 0,
        }

        for rg in range(int(pf.metadata.num_row_groups)):
            try:
                table = pf.read_row_group(rg, columns=COLUMNS, use_threads=False)
            except Exception as exc:
                blocked(output, report, "BLOCKED_BID_ASK_READ", f"{rel} rg={rg}: {exc}")
            if table.column_names != COLUMNS or table.num_columns != 2:
                blocked(output, report, "BLOCKED_COLUMN_SCOPE", f"{rel} rg={rg}")

            bid = table.column(0).combine_chunks()
            ask = table.column(1).combine_chunks()
            n = len(bid)
            if len(ask) != n:
                blocked(output, report, "BLOCKED_COLUMN_LENGTH_MISMATCH", f"{rel} rg={rg}")
            total_rows += n
            file_counts["rows"] += n

            bn = int(bid.null_count)
            an = int(ask.null_count)
            bid_null += bn; ask_null += an
            file_counts["bid_null"] += bn; file_counts["ask_null"] += an

            b = pc.fill_null(bid, float("nan")).to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            a = pc.fill_null(ask, float("nan")).to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

            bfinite = np.isfinite(b)
            afinite = np.isfinite(a)
            bnf = int(np.count_nonzero(~bfinite))
            anf = int(np.count_nonzero(~afinite))
            # Nulls are already included in nonfinite after fill; report non-null nonfinite separately.
            bnf_nonnull = max(0, bnf - bn)
            anf_nonnull = max(0, anf - an)
            bid_nonfinite += bnf_nonnull; ask_nonfinite += anf_nonnull
            file_counts["bid_nonfinite"] += bnf_nonnull
            file_counts["ask_nonfinite"] += anf_nonnull

            valid_pair = bfinite & afinite
            bp = int(np.count_nonzero(bfinite & (b <= 0)))
            ap = int(np.count_nonzero(afinite & (a <= 0)))
            bid_nonpositive += bp; ask_nonpositive += ap
            file_counts["bid_nonpositive"] += bp; file_counts["ask_nonpositive"] += ap

            if np.any(bfinite):
                bid_min = min(bid_min, float(np.min(b[bfinite])))
                bid_max = max(bid_max, float(np.max(b[bfinite])))
            if np.any(afinite):
                ask_min = min(ask_min, float(np.min(a[afinite])))
                ask_max = max(ask_max, float(np.max(a[afinite])))

            if np.any(valid_pair):
                spread = a[valid_pair] - b[valid_pair]
                altb = int(np.count_nonzero(spread < 0))
                nps = int(np.count_nonzero(spread <= 0))
                zs = int(np.count_nonzero(spread == 0))
                ask_lt_bid += altb; nonpositive_spread += nps; zero_spread += zs
                file_counts["ask_lt_bid"] += altb
                file_counts["nonpositive_spread"] += nps
                file_counts["zero_spread"] += zs

                valid_spread_count += int(spread.size)
                spread_sum += float(np.sum(spread, dtype=np.float64))
                spread_min = min(spread_min, float(np.min(spread)))
                spread_max = max(spread_max, float(np.max(spread)))

            del table, bid, ask, b, a

        if file_counts["rows"] != int(f0row["num_rows"]):
            blocked(output, report, "BLOCKED_FILE_ROWS_READ_MISMATCH", rel)

        st2 = path.stat(follow_symlinks=False)
        if int(st2.st_size) != int(mrow["size_bytes"]) or int(st2.st_mtime_ns) != int(mrow["mtime_ns"]):
            blocked(output, report, "BLOCKED_FILE_CHANGED_DURING_F2", rel)

        report["files"].append({"relative_path": rel, **file_counts})

    if total_rows != EXPECTED_ROWS:
        blocked(output, report, "BLOCKED_TOTAL_ROWS_MISMATCH", f"{total_rows} != {EXPECTED_ROWS}")

    report["summary"] = {
        "rows_read": total_rows,
        "bid_null": bid_null,
        "ask_null": ask_null,
        "bid_nonfinite_nonnull": bid_nonfinite,
        "ask_nonfinite_nonnull": ask_nonfinite,
        "bid_nonpositive": bid_nonpositive,
        "ask_nonpositive": ask_nonpositive,
        "ask_lt_bid": ask_lt_bid,
        "zero_spread": zero_spread,
        "nonpositive_spread": nonpositive_spread,
        "valid_spread_count": valid_spread_count,
        "spread_min": None if math.isinf(spread_min) else spread_min,
        "spread_max": None if math.isinf(spread_max) else spread_max,
        "spread_mean": (spread_sum / valid_spread_count) if valid_spread_count else None,
        "bid_min": None if math.isinf(bid_min) else bid_min,
        "bid_max": None if math.isinf(bid_max) else bid_max,
        "ask_min": None if math.isinf(ask_min) else ask_min,
        "ask_max": None if math.isinf(ask_max) else ask_max,
        "volume_fields_qualified": False,
    }
    report["status"] = "F2_COMPLETE"
    report["reason"] = "Bid/ask-only quality scan complete; volume fields deliberately outside qualified scope."
    report["runtime"] = {"numpy_version": np.__version__, "pyarrow_version": pq.__version__ if hasattr(pq, "__version__") else None}

    write_json(output, report)
    print("F2_COMPLETE")
    print(f"Rows read: {total_rows}")
    print(f"Bid null: {bid_null}; Ask null: {ask_null}")
    print(f"Ask < Bid: {ask_lt_bid}")
    print(f"Nonpositive spread: {nonpositive_spread}")
    print(f"Spread min/max/mean: {report['summary']['spread_min']} / {report['summary']['spread_max']} / {report['summary']['spread_mean']}")
    print(f"Report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

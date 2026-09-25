#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any

EXPECTED_MANIFEST_SHA256 = "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
EXPECTED_INVENTORY_DIGEST = "c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54"
EXPECTED_PARQUET_FILES = 212
EXPECTED_TOTAL_PARQUET_BYTES = 3_936_721_231
MAX_FOOTER_METADATA_BYTES = 128 * 1024**2
PARQUET_MAGIC = b"PAR1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in files:
        line = f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n"
        digest.update(line.encode("utf-8"))
    return digest.hexdigest()


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return {"encoding": "base64", "value": base64.b64encode(value).decode("ascii")}
    try:
        return value.item()
    except Exception:
        return repr(value)


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
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def blocked(output: Path, report: dict[str, Any], status: str, reason: str) -> None:
    report["status"] = status
    report["reason"] = reason
    write_json(output, report)
    print(status)
    print(reason)
    print(f"Report: {output}")
    raise SystemExit(2)


def read_tail8(path: Path) -> tuple[int, bytes]:
    size = path.stat(follow_symlinks=False).st_size
    if size < 12:
        raise ValueError("file too small for a valid Parquet envelope")
    with path.open("rb") as handle:
        handle.seek(-8, os.SEEK_END)
        tail = handle.read(8)
    if len(tail) != 8:
        raise ValueError("could not read exact 8-byte Parquet tail")
    footer_len = int.from_bytes(tail[:4], "little", signed=False)
    magic = tail[4:]
    if magic != PARQUET_MAGIC:
        raise ValueError(f"tail magic is {magic!r}, expected b'PAR1'")
    if footer_len <= 0:
        raise ValueError("footer length is zero")
    if footer_len + 8 > size - 4:
        raise ValueError("footer length exceeds physical file bounds")
    return footer_len, magic


def load_and_validate_manifest(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    actual_sha = sha256_path(path)
    if actual_sha != EXPECTED_MANIFEST_SHA256:
        raise ValueError(
            f"manifest SHA-256 mismatch: {actual_sha} != {EXPECTED_MANIFEST_SHA256}"
        )

    manifest = json.loads(path.read_text(encoding="utf-8"))
    inventory = manifest.get("inventory") or {}
    files = inventory.get("files")
    if not isinstance(files, list):
        raise ValueError("manifest inventory.files is not a list")

    if manifest.get("schema") != "ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1":
        raise ValueError("unexpected manifest schema")
    if manifest.get("status") != "MANIFEST_COMPLETE":
        raise ValueError("manifest status is not MANIFEST_COMPLETE")
    if inventory.get("parquet_files") != EXPECTED_PARQUET_FILES:
        raise ValueError("manifest parquet_files mismatch")
    if len(files) != EXPECTED_PARQUET_FILES:
        raise ValueError("manifest file-entry count mismatch")
    if inventory.get("total_parquet_bytes") != EXPECTED_TOTAL_PARQUET_BYTES:
        raise ValueError("manifest total_parquet_bytes mismatch")
    if inventory.get("sha256_complete") is not True:
        raise ValueError("manifest sha256_complete is not true")
    if inventory.get("parquet_magic_checked") is not True:
        raise ValueError("manifest parquet_magic_checked is not true")
    if inventory.get("snapshot_stable") is not True:
        raise ValueError("manifest snapshot_stable is not true")

    rels = [row.get("relative_path") for row in files]
    if any(not isinstance(x, str) or not x for x in rels):
        raise ValueError("invalid relative_path in manifest")
    if len(set(rels)) != len(rels):
        raise ValueError("duplicate relative_path in manifest")

    for row in files:
        if row.get("sha256_status") != "PASS":
            raise ValueError(f"non-PASS SHA status for {row.get('relative_path')}")
        digest = row.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid SHA-256 for {row.get('relative_path')}")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError(f"non-hex SHA-256 for {row.get('relative_path')}") from exc

    inv_digest = canonical_inventory_digest(files)
    if inv_digest != EXPECTED_INVENTORY_DIGEST:
        raise ValueError(
            f"canonical inventory digest mismatch: {inv_digest} != {EXPECTED_INVENTORY_DIGEST}"
        )

    return manifest, files


def arrow_field_record(field: Any) -> dict[str, Any]:
    md = None
    if getattr(field, "metadata", None):
        md = {
            base64.b64encode(k).decode("ascii"): base64.b64encode(v).decode("ascii")
            for k, v in sorted(field.metadata.items(), key=lambda kv: kv[0])
        }
    return {
        "name": field.name,
        "type": str(field.type),
        "nullable": bool(field.nullable),
        "metadata_base64": md,
    }


def parquet_column_record(column: Any) -> dict[str, Any]:
    attrs = {}
    for name in (
        "name",
        "path",
        "physical_type",
        "logical_type",
        "converted_type",
        "max_definition_level",
        "max_repetition_level",
        "length",
        "precision",
        "scale",
    ):
        try:
            attrs[name] = json_safe(getattr(column, name))
        except Exception:
            attrs[name] = None
    return attrs


def is_temporal_candidate(name: str, arrow_type: str, logical_type: str) -> bool:
    n = name.casefold()
    t = arrow_type.casefold()
    l = logical_type.casefold()
    exact = {
        "timestamp", "time", "datetime", "date", "ts", "market_timestamp",
        "event_timestamp", "event_time", "time_msc", "time_ms"
    }
    return (
        n in exact
        or "timestamp" in n
        or t.startswith("timestamp[")
        or t.startswith("date")
        or t.startswith("time")
        or "timestamp" in l
        or "date" in l
        or "time" in l
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="E0 Source-B F0: read-only Parquet footer census under the frozen 128 MiB metadata budget."
    )
    parser.add_argument("--repo-root", required=True, help="Root of the local ATDS clone containing Source-B.")
    parser.add_argument("--manifest", required=True, help="Exact sealed ATDS-E0-SOURCE-B-MANIFEST.json.")
    parser.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-E0-SOURCE-B-F0-FOOTER-CENSUS.json"),
        help="Output JSON path; must be outside the corpus.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve(strict=False)
    manifest_path = Path(args.manifest).expanduser().resolve(strict=True)
    output = Path(args.output).expanduser().resolve(strict=False)
    corpus = (repo_root / "data" / "research_source_b_ustech" / "parquet").resolve(strict=False)

    report: dict[str, Any] = {
        "schema": "ATDS_E0_SOURCE_B_F0_FOOTER_CENSUS_V0_1",
        "generated_at_utc": utc_now(),
        "binding": {
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "inventory_digest": EXPECTED_INVENTORY_DIGEST,
            "expected_files": EXPECTED_PARQUET_FILES,
            "expected_total_parquet_bytes": EXPECTED_TOTAL_PARQUET_BYTES,
        },
        "budget": {
            "max_footer_metadata_bytes": MAX_FOOTER_METADATA_BYTES,
            "initial_tail_probe_bytes": EXPECTED_PARQUET_FILES * 8,
        },
        "read_contract": {
            "corpus_writes": 0,
            "column_data_scan": False,
            "strategy_calculation": False,
            "signal_calculation": False,
            "trade_or_pnl_calculation": False,
            "provider_network": False,
        },
        "status": "PRECHECK",
        "reason": None,
        "footer_probe": {},
        "metadata_census": {},
        "files": [],
    }

    if not corpus.is_dir():
        blocked(output, report, "BLOCKED_CORPUS_NOT_FOUND", f"Corpus directory missing: {corpus}")
    if is_reparse_or_symlink(corpus):
        blocked(output, report, "BLOCKED_REPARSE_POINT", "Corpus root is a symlink/reparse point.")

    try:
        manifest, files = load_and_validate_manifest(manifest_path)
    except Exception as exc:
        blocked(output, report, "BLOCKED_MANIFEST_BINDING", str(exc))

    # Snapshot identity check before reading any footer bytes.
    file_paths: list[Path] = []
    for row in files:
        rel = row["relative_path"]
        path = (corpus / Path(rel)).resolve(strict=False)
        try:
            if os.path.commonpath([str(path), str(corpus)]) != str(corpus):
                blocked(output, report, "BLOCKED_PATH_ESCAPE", f"Manifest path escapes corpus: {rel}")
        except ValueError:
            blocked(output, report, "BLOCKED_PATH_ESCAPE", f"Manifest path is on another volume: {rel}")

        if not path.is_file():
            blocked(output, report, "BLOCKED_FILE_MISSING", f"Missing manifest file: {rel}")
        if is_reparse_or_symlink(path):
            blocked(output, report, "BLOCKED_REPARSE_POINT", f"Symlink/reparse file: {rel}")

        st = path.stat(follow_symlinks=False)
        expected_size = int(row["size_bytes"])
        expected_mtime = int(row["mtime_ns"])
        if int(st.st_size) != expected_size:
            blocked(output, report, "BLOCKED_FILE_SIZE_CHANGED", f"Size changed: {rel}")
        if int(st.st_mtime_ns) != expected_mtime:
            blocked(output, report, "BLOCKED_FILE_MTIME_CHANGED", f"mtime changed: {rel}")
        file_paths.append(path)

    if output == corpus or corpus in output.parents:
        blocked(output, report, "BLOCKED_OUTPUT_INSIDE_CORPUS", "Output path must be outside the corpus.")

    # Phase F0-A: exactly 8 tail bytes per file.
    footer_total = 0
    footer_lengths: list[int] = []
    for row, path in zip(files, file_paths):
        try:
            footer_len, _ = read_tail8(path)
        except Exception as exc:
            blocked(output, report, "BLOCKED_FOOTER_TAIL", f"{row['relative_path']}: {exc}")
        footer_lengths.append(footer_len)
        footer_total += footer_len + 8
        report["files"].append({
            "relative_path": row["relative_path"],
            "size_bytes": int(row["size_bytes"]),
            "mtime_ns": int(row["mtime_ns"]),
            "footer_len_bytes": footer_len,
            "footer_envelope_bytes": footer_len + 8,
        })

    report["footer_probe"] = {
        "files_probed": len(footer_lengths),
        "tail_probe_bytes": len(footer_lengths) * 8,
        "footer_envelope_bytes_total": footer_total,
        "footer_len_min": min(footer_lengths),
        "footer_len_max": max(footer_lengths),
        "footer_len_mean": footer_total / len(footer_lengths) - 8,
        "within_128_mib_budget": footer_total <= MAX_FOOTER_METADATA_BYTES,
    }

    if footer_total > MAX_FOOTER_METADATA_BYTES:
        blocked(
            output,
            report,
            "BLOCKED_FOOTER_METADATA_BUDGET",
            f"Footer envelope total {footer_total} exceeds frozen limit {MAX_FOOTER_METADATA_BYTES}.",
        )

    # Phase F0-B: metadata API only. No column data reads are requested.
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        blocked(
            output,
            report,
            "BLOCKED_PYARROW_NOT_AVAILABLE",
            f"pyarrow is required for footer metadata decoding after budget PASS: {exc}",
        )

    schema_signatures: Counter[str] = Counter()
    schema_examples: dict[str, dict[str, Any]] = {}
    total_rows = 0
    total_row_groups = 0
    temporal_candidates: set[str] = set()
    market_field_candidates: dict[str, set[str]] = {
        "bid": set(),
        "ask": set(),
        "spread": set(),
    }
    temporal_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"row_groups_with_stats": 0, "row_groups_without_stats": 0, "mins": [], "maxs": []}
    )

    for file_index, (row, path, out_row) in enumerate(zip(files, file_paths, report["files"])):
        try:
            pf = pq.ParquetFile(path)
            metadata = pf.metadata
            arrow_schema = pf.schema_arrow
            parquet_schema = pf.schema
        except Exception as exc:
            blocked(output, report, "BLOCKED_PARQUET_METADATA_DECODE", f"{row['relative_path']}: {exc}")

        arrow_fields = [arrow_field_record(field) for field in arrow_schema]
        parquet_columns = [parquet_column_record(parquet_schema.column(i)) for i in range(len(parquet_schema))]
        schema_payload = {
            "arrow_fields": arrow_fields,
            "parquet_columns": parquet_columns,
            "arrow_schema_metadata_base64": (
                {
                    base64.b64encode(k).decode("ascii"): base64.b64encode(v).decode("ascii")
                    for k, v in sorted((arrow_schema.metadata or {}).items(), key=lambda kv: kv[0])
                }
                if arrow_schema.metadata
                else None
            ),
        }
        schema_text = json.dumps(schema_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        schema_sig = hashlib.sha256(schema_text.encode("utf-8")).hexdigest()
        schema_signatures[schema_sig] += 1
        schema_examples.setdefault(schema_sig, schema_payload)

        file_rows = int(metadata.num_rows)
        file_row_groups = int(metadata.num_row_groups)
        total_rows += file_rows
        total_row_groups += file_row_groups

        # Identify candidate field names without deciding semantics.
        for field in arrow_fields:
            name = field["name"]
            arrow_type = field["type"]
            pcol = next((c for c in parquet_columns if c.get("name") == name or c.get("path") == name), None)
            logical = str((pcol or {}).get("logical_type") or "")
            if is_temporal_candidate(name, arrow_type, logical):
                temporal_candidates.add(name)
            lower = name.casefold()
            for key in market_field_candidates:
                if key in lower:
                    market_field_candidates[key].add(name)

        out_row.update({
            "num_rows": file_rows,
            "num_row_groups": file_row_groups,
            "schema_signature": schema_sig,
        })

        # Collect only statistics already stored in row-group metadata for temporal candidates.
        for rg_index in range(file_row_groups):
            rg = metadata.row_group(rg_index)
            for col_index in range(rg.num_columns):
                col = rg.column(col_index)
                path_name = col.path_in_schema
                leaf_name = path_name.split(".")[-1]
                if path_name not in temporal_candidates and leaf_name not in temporal_candidates:
                    continue
                stats = col.statistics
                key = path_name
                if stats is None or not getattr(stats, "has_min_max", False):
                    temporal_stats[key]["row_groups_without_stats"] += 1
                    continue
                temporal_stats[key]["row_groups_with_stats"] += 1
                temporal_stats[key]["mins"].append(json_safe(stats.min))
                temporal_stats[key]["maxs"].append(json_safe(stats.max))

        # Detect metadata-visible changes after reading each file's footer.
        st_after = path.stat(follow_symlinks=False)
        if int(st_after.st_size) != int(row["size_bytes"]) or int(st_after.st_mtime_ns) != int(row["mtime_ns"]):
            blocked(
                output,
                report,
                "BLOCKED_FILE_CHANGED_DURING_F0",
                f"File changed during metadata census: {row['relative_path']}",
            )

    def extrema(values: list[Any], which: str) -> Any:
        if not values:
            return None
        try:
            return json_safe(min(values) if which == "min" else max(values))
        except Exception:
            texts = [json.dumps(json_safe(v), ensure_ascii=False, sort_keys=True) for v in values]
            return min(texts) if which == "min" else max(texts)

    temporal_summary = {}
    for key, data in temporal_stats.items():
        temporal_summary[key] = {
            "row_groups_with_stats": data["row_groups_with_stats"],
            "row_groups_without_stats": data["row_groups_without_stats"],
            "observed_min_from_metadata": extrema(data["mins"], "min"),
            "observed_max_from_metadata": extrema(data["maxs"], "max"),
        }

    report["metadata_census"] = {
        "pyarrow_version": pa.__version__,
        "files_decoded": len(files),
        "total_rows": total_rows,
        "total_row_groups": total_row_groups,
        "unique_schema_signatures": len(schema_signatures),
        "schema_signature_counts": dict(sorted(schema_signatures.items())),
        "schema_examples": schema_examples,
        "temporal_field_candidates": sorted(temporal_candidates),
        "temporal_statistics": temporal_summary,
        "market_field_candidates": {
            key: sorted(values) for key, values in market_field_candidates.items()
        },
    }

    # Full metadata snapshot stability check.
    for row, path in zip(files, file_paths):
        st = path.stat(follow_symlinks=False)
        if int(st.st_size) != int(row["size_bytes"]) or int(st.st_mtime_ns) != int(row["mtime_ns"]):
            blocked(output, report, "BLOCKED_CORPUS_CHANGED_DURING_F0", f"Snapshot changed: {row['relative_path']}")

    report["status"] = "F0_COMPLETE"
    report["reason"] = (
        "All 212 sealed files matched size/mtime; footer budget passed; "
        "Parquet metadata census completed without requesting column-data scans."
    )
    write_json(output, report)
    print("F0_COMPLETE")
    print(f"Files: {len(files)}")
    print(f"Footer envelope bytes: {footer_total}")
    print(f"Rows: {total_rows}")
    print(f"Row groups: {total_row_groups}")
    print(f"Schema signatures: {len(schema_signatures)}")
    print(f"Temporal candidates: {', '.join(sorted(temporal_candidates)) or 'NONE'}")
    print(f"Report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

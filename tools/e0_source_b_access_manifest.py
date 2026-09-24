#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import tempfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_ENTRIES = 1_000
MAX_PARQUET_FILES = 500
MAX_TOTAL_PARQUET_READ_BYTES = 16 * 1024**3
MAX_FOOTER_METADATA_BYTES = 128 * 1024**2
MAX_SINGLE_FILE_FULL_READ_BYTES = 8 * 1024**3
HASH_CHUNK_BYTES = 8 * 1024**2


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_within(child: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath([str(child), str(parent)]) == str(parent)
    except ValueError:
        return False


def make_manifest(repo_root: Path, relative_path: str, corpus: Path) -> dict[str, Any]:
    return {
        "schema": "ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1",
        "generated_at_utc": utc_now(),
        "repository_root": str(repo_root),
        "relative_corpus_path": relative_path,
        "resolved_corpus_path": str(corpus),
        "budget": {
            "max_entries": MAX_ENTRIES,
            "max_parquet_files": MAX_PARQUET_FILES,
            "max_total_parquet_read_bytes": MAX_TOTAL_PARQUET_READ_BYTES,
            "max_footer_metadata_bytes": MAX_FOOTER_METADATA_BYTES,
            "max_single_file_full_read_bytes": MAX_SINGLE_FILE_FULL_READ_BYTES,
            "hash_chunk_bytes": HASH_CHUNK_BYTES,
        },
        "read_only_contract": {
            "corpus_writes": 0,
            "provider_network": False,
            "strategy_calculation": False,
            "pnl_calculation": False,
            "backtest": False,
            "follow_symlinks": False,
        },
        "runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "status": "PRECHECK",
        "reason": None,
        "inventory": {
            "total_entries": 0,
            "parquet_files": 0,
            "total_parquet_bytes": 0,
            "magic_read_bytes": 0,
            "sha256_read_bytes": 0,
            "sha256_complete": False,
            "parquet_magic_checked": False,
            "snapshot_stable": False,
            "files": [],
        },
    }


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def stop(manifest: dict[str, Any], output: Path, status: str, reason: str, code: int = 2):
    manifest["status"] = status
    manifest["reason"] = reason
    write_manifest(output, manifest)
    print(status)
    print(reason)
    print(f"Manifest: {output}")
    raise SystemExit(code)


def bounded_snapshot(
    corpus: Path,
    manifest: dict[str, Any],
    output: Path,
) -> tuple[list[Path], dict[str, tuple[int, int]]]:
    queue: deque[Path] = deque([corpus])
    entry_count = 0
    parquet: list[Path] = []
    signatures: dict[str, tuple[int, int]] = {}

    while queue:
        directory = queue.popleft()
        try:
            entries = sorted(os.scandir(directory), key=lambda e: e.name.casefold())
        except OSError as exc:
            stop(manifest, output, "BLOCKED_DIRECTORY_READ", f"Cannot enumerate {directory}: {exc}")

        for entry in entries:
            entry_count += 1
            manifest["inventory"]["total_entries"] = entry_count
            if entry_count > MAX_ENTRIES:
                stop(
                    manifest,
                    output,
                    "BLOCKED_ENTRY_BUDGET",
                    "Entry count exceeds preregistered 1000-entry budget.",
                )

            path = Path(entry.path)
            if entry.is_symlink():
                manifest["symlink_or_reparse_path"] = str(path)
                stop(
                    manifest,
                    output,
                    "BLOCKED_SYMLINK",
                    "A symlink/reparse-style entry exists inside the corpus.",
                )

            try:
                if entry.is_dir(follow_symlinks=False):
                    queue.append(path)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                stop(manifest, output, "BLOCKED_ENTRY_STAT", f"Cannot stat {path}: {exc}")

            rel = path.relative_to(corpus).as_posix()
            signatures[rel] = (int(stat.st_size), int(stat.st_mtime_ns))

            if path.suffix.casefold() == ".parquet":
                parquet.append(path)
                if len(parquet) > MAX_PARQUET_FILES:
                    manifest["inventory"]["parquet_files"] = len(parquet)
                    stop(
                        manifest,
                        output,
                        "BLOCKED_FILE_COUNT_BUDGET",
                        "Parquet file count exceeds preregistered 500-file budget.",
                    )

    return sorted(parquet, key=lambda p: p.as_posix().casefold()), signatures


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    read_bytes = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(HASH_CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
            read_bytes += len(chunk)
    return digest.hexdigest(), read_bytes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only E0 Source-B Parquet manifest bridge."
    )
    parser.add_argument(
        "--repo-root",
        default=os.getcwd(),
        help="ATDS repository root. Default: current directory.",
    )
    parser.add_argument(
        "--relative-path",
        default="data/research_source_b_ustech/parquet",
        help="Exact corpus path relative to repo root.",
    )
    parser.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-E0-SOURCE-B-MANIFEST.json"),
        help="Manifest JSON path outside the corpus.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve(strict=False)
    corpus = (repo_root / args.relative_path).resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)
    manifest = make_manifest(repo_root, args.relative_path, corpus)

    if not is_within(corpus, repo_root):
        stop(
            manifest,
            output,
            "BLOCKED_PATH_ESCAPE",
            "Resolved corpus path escapes repository root.",
        )

    if is_within(output, corpus):
        print("BLOCKED_OUTPUT_INSIDE_CORPUS", file=sys.stderr)
        print("Manifest output must be outside the corpus.", file=sys.stderr)
        return 2

    if not corpus.is_dir():
        stop(
            manifest,
            output,
            "BLOCKED_CORPUS_NOT_FOUND",
            "Exact corpus directory is not present.",
        )

    if corpus.is_symlink():
        stop(
            manifest,
            output,
            "BLOCKED_SYMLINK",
            "Corpus root is a symlink/reparse-style path.",
        )

    parquet, before = bounded_snapshot(corpus, manifest, output)
    manifest["inventory"]["parquet_files"] = len(parquet)

    if not parquet:
        stop(
            manifest,
            output,
            "BLOCKED_NO_PARQUET",
            "No .parquet files found in exact corpus directory.",
        )

    total_bytes = sum(before[p.relative_to(corpus).as_posix()][0] for p in parquet)
    manifest["inventory"]["total_parquet_bytes"] = total_bytes

    rows: list[dict[str, Any]] = []
    for path in parquet:
        rel = path.relative_to(corpus).as_posix()
        size, mtime_ns = before[rel]
        rows.append(
            {
                "relative_path": rel,
                "size_bytes": size,
                "mtime_ns": mtime_ns,
                "sha256": None,
                "sha256_status": "NOT_RUN",
                "parquet_magic_head": None,
                "parquet_magic_tail": None,
                "parquet_magic_status": "NOT_RUN",
            }
        )
    manifest["inventory"]["files"] = rows

    magic_read_bytes = len(parquet) * 8
    manifest["inventory"]["magic_read_bytes"] = magic_read_bytes
    if magic_read_bytes > MAX_FOOTER_METADATA_BYTES:
        stop(
            manifest,
            output,
            "BLOCKED_METADATA_BUDGET",
            "Magic-byte checks exceed preregistered 128 MiB metadata budget.",
        )

    for row, path in zip(rows, parquet):
        if row["size_bytes"] < 8:
            row["parquet_magic_status"] = "FAIL_TOO_SMALL"
            continue
        try:
            with path.open("rb") as handle:
                head = handle.read(4)
                handle.seek(-4, os.SEEK_END)
                tail = handle.read(4)
        except OSError as exc:
            stop(
                manifest,
                output,
                "BLOCKED_FILE_READ",
                f"Cannot read Parquet magic for {row['relative_path']}: {exc}",
            )
        row["parquet_magic_head"] = head.decode("ascii", errors="replace")
        row["parquet_magic_tail"] = tail.decode("ascii", errors="replace")
        row["parquet_magic_status"] = (
            "PASS" if head == b"PAR1" and tail == b"PAR1" else "FAIL"
        )

    manifest["inventory"]["parquet_magic_checked"] = True
    if any(row["parquet_magic_status"] != "PASS" for row in rows):
        stop(
            manifest,
            output,
            "BLOCKED_PARQUET_MAGIC",
            "One or more files do not have PAR1 head/tail magic.",
        )

    if total_bytes > MAX_TOTAL_PARQUET_READ_BYTES:
        stop(
            manifest,
            output,
            "BLOCKED_TOTAL_READ_BUDGET",
            "Total Parquet bytes exceed preregistered 16 GiB hashing budget.",
        )

    oversized = [
        row
        for row in rows
        if row["size_bytes"] > MAX_SINGLE_FILE_FULL_READ_BYTES
    ]
    if oversized:
        manifest["oversized_files"] = [
            {
                "relative_path": row["relative_path"],
                "size_bytes": row["size_bytes"],
            }
            for row in oversized
        ]
        stop(
            manifest,
            output,
            "BLOCKED_SINGLE_FILE_BUDGET",
            "At least one Parquet file exceeds preregistered 8 GiB full-read budget.",
        )

    total_sha_read = 0
    for row, path in zip(rows, parquet):
        before_size, before_mtime = before[row["relative_path"]]
        digest, read_bytes = sha256_file(path)
        total_sha_read += read_bytes
        try:
            after_stat = path.stat(follow_symlinks=False)
        except OSError as exc:
            stop(
                manifest,
                output,
                "BLOCKED_ENTRY_STAT",
                f"Cannot restat {row['relative_path']}: {exc}",
            )
        if (
            int(after_stat.st_size) != before_size
            or int(after_stat.st_mtime_ns) != before_mtime
        ):
            stop(
                manifest,
                output,
                "BLOCKED_FILE_CHANGED_DURING_READ",
                f"File changed during hashing: {row['relative_path']}",
            )
        row["sha256"] = digest
        row["sha256_status"] = "PASS"

    manifest["inventory"]["sha256_read_bytes"] = total_sha_read
    manifest["inventory"]["sha256_complete"] = True

    parquet_after, after = bounded_snapshot(corpus, manifest, output)
    after_parquet_rel = [p.relative_to(corpus).as_posix() for p in parquet_after]
    before_parquet_rel = [p.relative_to(corpus).as_posix() for p in parquet]
    if before != after or before_parquet_rel != after_parquet_rel:
        stop(
            manifest,
            output,
            "BLOCKED_CORPUS_CHANGED_DURING_INVENTORY",
            "Corpus inventory changed during manifest generation.",
        )

    manifest["inventory"]["snapshot_stable"] = True
    manifest["status"] = "MANIFEST_COMPLETE"
    manifest["reason"] = (
        "Exact bounded file inventory and SHA-256 completed "
        "under the preregistered E0 budget."
    )
    write_manifest(output, manifest)
    print("MANIFEST_COMPLETE")
    print(f"Parquet files: {len(parquet)}")
    print(f"Parquet bytes: {total_bytes}")
    print(f"Manifest: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

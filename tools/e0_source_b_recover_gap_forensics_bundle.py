#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_REPORT_JSONS = 27
EXPECTED_TOOL_SCRIPTS = 25
EXPECTED_TOTAL_FILES = 53
MAX_FILES = 100
MAX_TOTAL_BYTES = 16 * 1024 * 1024
REPORT_DIR = Path("reports/data-qualification/dukascopy_research_a")
PROVENANCE_FILE = Path("reports/data-qualification/provenance_timestamp_search.txt")
TOOLS_DIR = Path("tools")
REPORT_GLOB = "huggingface_ustech_*.json"
TOOL_GLOB = "probe_huggingface_ustech_*.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def is_reparse_or_symlink(path: Path) -> bool:
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def is_within(child: Path, parent: Path) -> bool:
    try:
        c = os.path.normcase(str(child.resolve(strict=False)))
        p = os.path.normcase(str(parent.resolve(strict=False)))
        return os.path.commonpath([c, p]) == p
    except ValueError:
        return False


def die(msg: str) -> int:
    print("BLOCKED_GAP_FORENSICS_BUNDLE")
    print(msg)
    return 2


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create a read-only recovery bundle of historical Source-B gap-forensics artifacts."
    )
    ap.add_argument("--repo-root", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-SOURCE-B-GAP-FORENSICS-HISTORICAL.zip"),
    )
    args = ap.parse_args()

    root = Path(args.repo_root).expanduser().resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)

    if not root.is_dir():
        return die(f"Repo root missing: {root}")
    if output == root or is_within(output, root):
        return die("Output must be outside repository root.")

    report_dir = (root / REPORT_DIR).resolve(strict=False)
    tools_dir = (root / TOOLS_DIR).resolve(strict=False)
    provenance = (root / PROVENANCE_FILE).resolve(strict=False)

    if not report_dir.is_dir() or not tools_dir.is_dir() or not provenance.is_file():
        return die("Expected historical report/tools/provenance paths are missing.")

    report_files = sorted(report_dir.glob(REPORT_GLOB))
    tool_files = sorted(tools_dir.glob(TOOL_GLOB))

    if len(report_files) != EXPECTED_REPORT_JSONS:
        return die(
            f"Expected {EXPECTED_REPORT_JSONS} report JSONs, found {len(report_files)}."
        )
    if len(tool_files) != EXPECTED_TOOL_SCRIPTS:
        return die(
            f"Expected {EXPECTED_TOOL_SCRIPTS} tool scripts, found {len(tool_files)}."
        )

    files = report_files + [provenance] + tool_files
    if len(files) != EXPECTED_TOTAL_FILES or len(files) > MAX_FILES:
        return die(f"Unexpected total file count: {len(files)}.")

    records: list[dict[str, Any]] = []
    total_bytes = 0

    for p in files:
        if not p.is_file():
            return die(f"Missing file: {p}")
        if is_reparse_or_symlink(p):
            return die(f"Symlink/reparse point rejected: {p}")
        if not is_within(p, root):
            return die(f"Path escapes repo: {p}")
        rel = p.relative_to(root).as_posix()
        if rel.startswith("data/") or "/data/" in rel:
            return die(f"Data path unexpectedly selected: {rel}")
        st = p.stat(follow_symlinks=False)
        total_bytes += int(st.st_size)
        if total_bytes > MAX_TOTAL_BYTES:
            return die(
                f"Selected bytes {total_bytes} exceed limit {MAX_TOTAL_BYTES}."
            )
        records.append(
            {
                "relative_path": rel,
                "size_bytes": int(st.st_size),
                "mtime_ns": int(st.st_mtime_ns),
                "sha256": sha256_path(p),
            }
        )

    if output.exists():
        output.unlink()

    manifest = {
        "schema": "ATDS_E0_SOURCE_B_GAP_FORENSICS_RECOVERY_BUNDLE_V0_1",
        "generated_at_utc": utc_now(),
        "repo_root_recorded_as": str(root),
        "selection_contract": {
            "report_glob": str(REPORT_DIR / REPORT_GLOB).replace("\\", "/"),
            "tool_glob": str(TOOLS_DIR / TOOL_GLOB).replace("\\", "/"),
            "provenance_file": PROVENANCE_FILE.as_posix(),
            "expected_report_jsons": EXPECTED_REPORT_JSONS,
            "expected_tool_scripts": EXPECTED_TOOL_SCRIPTS,
            "expected_total_files": EXPECTED_TOTAL_FILES,
            "max_total_bytes": MAX_TOTAL_BYTES,
            "data_paths_allowed": False,
        },
        "total_files": len(records),
        "total_bytes": total_bytes,
        "files": records,
    }
    manifest_bytes = (
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("BUNDLE-MANIFEST.json", manifest_bytes)
        for rec, p in zip(records, files):
            # ZIP names are repository-relative only; no absolute paths.
            zf.write(p, arcname=rec["relative_path"])

    # Verify archive inventory after writing.
    with zipfile.ZipFile(output, "r") as zf:
        names = zf.namelist()
        expected_names = ["BUNDLE-MANIFEST.json"] + [r["relative_path"] for r in records]
        if names != expected_names:
            output.unlink(missing_ok=True)
            return die("ZIP inventory differs from planned inventory.")

    zip_sha = sha256_path(output)
    sidecar = output.with_suffix(output.suffix + ".sha256.txt")
    sidecar.write_text(f"{zip_sha}  {output.name}\n", encoding="utf-8", newline="\n")

    print("GAP_FORENSICS_BUNDLE_COMPLETE")
    print(f"Files: {len(records)}")
    print(f"Source bytes: {total_bytes}")
    print(f"ZIP bytes: {output.stat().st_size}")
    print(f"ZIP SHA256: {zip_sha}")
    print(f"Bundle: {output}")
    print(f"SHA file: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

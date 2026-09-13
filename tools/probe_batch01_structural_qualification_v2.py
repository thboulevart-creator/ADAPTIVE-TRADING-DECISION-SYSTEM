#!/usr/bin/env python3
"""V4.3 Batch01 — structural qualification of a physical Dukascopy BI5 corpus.

This probe is deliberately read-only. It qualifies the files that physically
exist on disk; it does not reconstruct missing hours from manifests, download
anything, repair records, sort data, deduplicate ticks, or synthesize a corpus.

PASS requires an explicit expected inventory. Without that inventory the tool
can still measure the physical corpus, but the verdict is BLOCKED because
absence/presence cannot be proven against the expected payload set.

Controls per physical .bi5 file:
- LZMA decompression succeeds
- decompressed payload is non-empty and divisible by 20 bytes
- every 20-byte BI5 record decodes
- millisecond offset is in [0, 3_599_999]
- timestamp reconstructed from path hour is consistent with that hour
- records are internally chronological
- quotes are finite, positive and ask >= bid
- SHA-256 is recorded

Inventory file format: one relative path per line, or JSON containing either
an array of paths or {"files": [paths...]}. Paths are normalized to '/'.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import re
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path

BI5_RECORD_SIZE = 20
BI5_STRUCT = struct.Struct(">IIIff")
HOUR_PATTERNS = (
    re.compile(r"(?P<y>20\\d{2})[-/](?P<m>\\d{2})[-/](?P<d>\\d{2})[ _](?P<h>\\d{1,2})h", re.I),
    re.compile(r"/(?P<y>20\\d{2})/(?P<m>\\d{2})/(?P<d>\\d{2})/(?P<h>\\d{1,2})h_ticks\\.bi5$", re.I),
)


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True, help="Directory containing the physical BI5 files")
    p.add_argument("--expected", help="Expected physical inventory (.txt or .json)")
    p.add_argument("--expected-count", type=int, default=495)
    p.add_argument("--output", default="reports/data-qualification/batch01_structural_qualification_v2.json")
    return p.parse_args()


def norm_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_hour(path: Path) -> datetime:
    text = str(path).replace("\\", "/")
    for pattern in HOUR_PATTERNS:
        m = pattern.search(text)
        if m:
            hour = int(m["h"])
            if hour > 23:
                break
            return datetime(int(m["y"]), int(m["m"]), int(m["d"]), hour, tzinfo=timezone.utc)
    raise ValueError("PATH_HOUR_UNPARSEABLE")


def load_expected(path: Path, root: Path) -> set[str]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("files")
        if not isinstance(data, list):
            raise ValueError("EXPECTED_JSON_MUST_BE_ARRAY_OR_OBJECT_WITH_FILES")
        values = data
    else:
        values = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    out = set()
    for value in values:
        p = Path(str(value).replace("\\", "/"))
        try:
            rel = p.relative_to(root).as_posix()
        except ValueError:
            rel = p.as_posix().lstrip("./")
        out.add(rel)
    return out


def qualify_file(path: Path, root: Path) -> dict:
    rel = norm_rel(path, root)
    result = {
        "path": rel,
        "sha256": sha256(path),
        "compressed_bytes": path.stat().st_size,
        "status": "PASS",
        "record_count": 0,
        "first_timestamp": None,
        "last_timestamp": None,
        "errors": [],
    }
    try:
        hour = parse_hour(path)
        result["hour"] = hour.isoformat()
        raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_ALONE)
        result["decompressed_bytes"] = len(raw)
        if not raw:
            raise ValueError("ZERO_DECOMPRESSED_BYTES")
        if len(raw) % BI5_RECORD_SIZE:
            raise ValueError("DECOMPRESSED_SIZE_NOT_MULTIPLE_OF_20")

        prev = None
        for offset in range(0, len(raw), BI5_RECORD_SIZE):
            try:
                ms, ask_raw, bid_raw, ask_volume, bid_volume = BI5_STRUCT.unpack(raw[offset:offset + BI5_RECORD_SIZE])
            except struct.error as exc:
                raise ValueError(f"BI5_RECORD_DECODE_ERROR:{exc}") from exc
            if ms >= 3_600_000:
                raise ValueError(f"MILLISECOND_OFFSET_OUT_OF_RANGE:{ms}")
            ask = ask_raw / 1000.0
            bid = bid_raw / 1000.0
            if not all(math.isfinite(x) for x in (ask, bid, ask_volume, bid_volume)):
                raise ValueError(f"NON_FINITE_RECORD_AT_OFFSET:{offset}")
            if ask <= 0 or bid <= 0 or ask < bid or ask_volume < 0 or bid_volume < 0:
                raise ValueError(f"INVALID_QUOTE_AT_OFFSET:{offset}")
            ts = hour + timedelta(milliseconds=ms)
            if prev is not None and ts < prev:
                raise ValueError(f"INTERNAL_TIMESTAMP_ORDER_VIOLATION_AT_OFFSET:{offset}")
            prev = ts
            result["record_count"] += 1
            if result["first_timestamp"] is None:
                result["first_timestamp"] = ts.isoformat()
            result["last_timestamp"] = ts.isoformat()
        if result["record_count"] == 0:
            raise ValueError("ZERO_RECORDS")
    except Exception as exc:
        result["status"] = "FAIL"
        result["errors"].append(str(exc))
    return result


def main() -> int:
    a = args()
    root = Path(a.corpus).expanduser().resolve()
    output = Path(a.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "BATCH01_STRUCTURAL_QUALIFICATION_V2",
        "version": "V4.3",
        "mode": "READ_ONLY_PHYSICAL_CORPUS",
        "corpus": str(root),
        "expected_count": a.expected_count,
    }

    if not root.exists() or not root.is_dir():
        report.update({"verdict": "BLOCKED", "reason": "CORPUS_DIRECTORY_UNAVAILABLE"})
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("VERDICT=BLOCKED")
        return 2

    physical = sorted(p for p in root.rglob("*.bi5") if p.is_file())
    physical_set = {norm_rel(p, root) for p in physical}
    report["physical_files_discovered"] = len(physical)

    if a.expected:
        try:
            expected_set = load_expected(Path(a.expected).expanduser().resolve(), root)
        except Exception as exc:
            report.update({"verdict": "BLOCKED", "reason": f"EXPECTED_INVENTORY_UNREADABLE:{exc}"})
            output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            print("VERDICT=BLOCKED")
            return 2
        missing = sorted(expected_set - physical_set)
        unexpected = sorted(physical_set - expected_set)
        report["expected_files"] = len(expected_set)
        report["missing_files"] = missing
        report["unexpected_files"] = unexpected
        inventory_status = "PASS" if not missing and not unexpected and len(expected_set) == a.expected_count else "FAIL"
    else:
        expected_set = None
        report["inventory_status"] = "UNVERIFIED"
        inventory_status = "BLOCKED"

    results = [qualify_file(p, root) for p in physical]
    pass_files = sum(r["status"] == "PASS" for r in results)
    fail_files = sum(r["status"] == "FAIL" for r in results)
    total_records = sum(r["record_count"] for r in results)
    hours = sorted({r.get("hour") for r in results if r.get("hour")})
    duplicate_hours = sorted({h for h in hours if sum(r.get("hour") == h for r in results) > 1})

    report.update({
        "files": results,
        "qualified_files": pass_files,
        "failed_files": fail_files,
        "total_records": total_records,
        "unique_hours": len(hours),
        "duplicate_hours": duplicate_hours,
        "structural_status": "PASS" if physical and fail_files == 0 and len(physical) == a.expected_count else "FAIL",
    })

    if inventory_status == "BLOCKED":
        verdict = "BLOCKED"
    elif inventory_status == "FAIL" or fail_files:
        verdict = "FAIL"
    elif len(physical) != a.expected_count:
        verdict = "FAIL"
    else:
        verdict = "PASS"
    report["verdict"] = verdict
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"PAYLOADS_DISCOVERED={len(physical)}")
    print(f"EXPECTED_DOWNLOADED={len(physical)}")
    print(f"QUALIFIED_FILES={pass_files}")
    print(f"PASS_FILES={pass_files}")
    print(f"FAIL_FILES={fail_files}")
    print(f"TOTAL_RECORDS={total_records}")
    print(f"UNIQUE_HOURS={len(hours)}")
    print(f"VERDICT={verdict}")
    print(f"REPORT={output}")
    return 0 if verdict == "PASS" else 1 if verdict == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())

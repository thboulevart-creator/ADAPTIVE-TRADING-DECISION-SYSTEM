"""V4.3 — Research ↔ Execution data compatibility probe.

Purpose
-------
Compare transfer-relevant properties of independent research and execution
feeds without pretending they should be tick-for-tick identical.

V4.3 is read-only. It never sorts, repairs, deduplicates, merges, rewrites,
or silently converts source data. Source adapters preserve provenance.

Supported source formats
------------------------
* CSV: frozen project tick schema
    timestamp,askPrice,bidPrice,askVolume,bidVolume
* Dukascopy BI5: native compressed 20-byte tick records
    >IIIff, with millisecond offset inside the hour and prices /1000
* Parquet: timestamp,bid_price,ask_price,bid_volume,ask_volume
    Naive timestamps are BLOCKED unless --naive-timezone is explicitly supplied.

Important methodological guardrails
-----------------------------------
* The V4.2 VT Markets boundary is an observable/synchronized MT5 boundary,
  not a claim about inaccessible broker-side history.
* Research and execution coverage remain separate truths.
* Datasets are never spliced into a synthetic history.
* V4.3 does not invent statistical equivalence thresholds.
* TRANSFER_VALIDATION therefore remains UNVERIFIED until explicit acceptance
  criteria are frozen and adversarially tested.

Verdict precedence: BLOCKED > FAIL > UNVERIFIED > PASS.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import lzma
import math
import re
import statistics
import struct
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

EXPECTED_CSV_COLUMNS = ("timestamp", "askPrice", "bidPrice", "askVolume", "bidVolume")
EXPECTED_PARQUET_COLUMNS = ("timestamp", "bid_price", "ask_price", "bid_volume", "ask_volume")
EXECUTION_BOUNDARY_UTC = "2024-12-17T09:38:28+00:00"
MIN_RESEARCH_YEARS = 5.0
BI5_RECORD_SIZE = 20
BI5_STRUCT = struct.Struct(">IIIff")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--research", required=True)
    p.add_argument("--execution", required=True)
    p.add_argument("--research-instrument", default="Dukascopy USATECHIDXUSD")
    p.add_argument("--execution-instrument", default="VT Markets NAS100.s")
    p.add_argument("--naive-timezone", default=None, help="Required to interpret naive Parquet timestamps; never assumed")
    p.add_argument("--output", default="reports/data-qualification/research_execution_compatibility_v4_3.json")
    return p.parse_args()


def utc_iso(dt: datetime | None) -> str | None:
    return dt.astimezone(timezone.utc).isoformat() if dt else None


def parse_aware_timestamp(value: object) -> datetime:
    text = str(value).replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return dt.astimezone(timezone.utc)


def parse_naive_timestamp(value: object, tz_name: str) -> datetime:
    from zoneinfo import ZoneInfo
    dt = datetime.fromisoformat(str(value).replace("Z", ""))
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc)
    return dt.replace(tzinfo=ZoneInfo(tz_name)).astimezone(timezone.utc)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_sources(path_text: str) -> list[Path]:
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in {".csv", ".bi5", ".parquet"})


def source_format(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".bi5":
        return "DUKASCOPY_BI5"
    if ext == ".parquet":
        return "PARQUET"
    if ext == ".csv":
        return "CSV"
    return "UNSUPPORTED"


def empty_stats() -> dict:
    return {
        "files": 0, "rows": 0, "first": None, "last": None,
        "invalid_rows": 0, "ordering_violations": 0, "quote_violations": 0,
        "spreads": [], "hour_mid": {}, "file_errors": [], "formats": defaultdict(int),
        "timezone_semantics": set(),
    }


def record_tick(stats: dict, ts: datetime, ask: float, bid: float, av: float, bv: float, prev: datetime | None) -> datetime:
    stats["rows"] += 1
    if ask <= 0 or bid <= 0 or av < 0 or bv < 0 or not all(math.isfinite(x) for x in (ask, bid, av, bv)):
        stats["invalid_rows"] += 1
    if ask < bid:
        stats["quote_violations"] += 1
    if prev is not None and ts < prev:
        stats["ordering_violations"] += 1
    mid = (ask + bid) / 2.0
    stats["spreads"].append(ask - bid)
    hour = ts.replace(minute=0, second=0, microsecond=0)
    stats["hour_mid"][hour] = mid
    if stats["first"] is None or ts < stats["first"]:
        stats["first"] = ts
    if stats["last"] is None or ts > stats["last"]:
        stats["last"] = ts
    return ts


def scan_csv(path: Path, stats: dict) -> None:
    stats["formats"]["CSV"] += 1
    prev = None
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != EXPECTED_CSV_COLUMNS:
            raise ValueError(f"unexpected CSV schema: {reader.fieldnames!r}")
        for row in reader:
            try:
                ts = parse_aware_timestamp(row["timestamp"])
                ask, bid = float(Decimal(row["askPrice"])), float(Decimal(row["bidPrice"]))
                av, bv = float(Decimal(row["askVolume"])), float(Decimal(row["bidVolume"]))
            except (KeyError, InvalidOperation, ValueError, TypeError) as exc:
                stats["invalid_rows"] += 1
                if len(stats.setdefault("sample_errors", [])) < 5:
                    stats["sample_errors"].append({"path": str(path), "error": str(exc)})
                continue
            prev = record_tick(stats, ts, ask, bid, av, bv, prev)
    stats["timezone_semantics"].add("explicit_utc_or_offset")


def parse_bi5_hour(path: Path) -> datetime:
    text = str(path).replace("\\", "/")
    patterns = [
        r"(?P<y>20\d{2})[-/](?P<m>\d{2})[-/](?P<d>\d{2})[ _](?P<h>\d{1,2})h",
        r"/(?P<y>20\d{2})/(?P<m>\d{2})/(?P<d>\d{2})/(?P<h>\d{1,2})h_ticks\.bi5$",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return datetime(int(m["y"]), int(m["m"]), int(m["d"]), int(m["h"]), tzinfo=timezone.utc)
    raise ValueError("BI5 filename/path does not expose YYYY-MM-DD-HH hour needed for timestamp reconstruction")


def scan_bi5(path: Path, stats: dict) -> None:
    stats["formats"]["DUKASCOPY_BI5"] += 1
    hour = parse_bi5_hour(path)
    raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_ALONE)
    if not raw:
        raise ValueError("ZERO_DECOMPRESSED_BYTES")
    if len(raw) % BI5_RECORD_SIZE:
        raise ValueError("DECOMPRESSED_SIZE_NOT_MULTIPLE_OF_20")
    prev = None
    for offset in range(0, len(raw), BI5_RECORD_SIZE):
        ms, ask_raw, bid_raw, av, bv = BI5_STRUCT.unpack(raw[offset:offset + BI5_RECORD_SIZE])
        if ms >= 3600000:
            stats["invalid_rows"] += 1
            continue
        ts = hour + timedelta(milliseconds=ms)
        prev = record_tick(stats, ts, ask_raw / 1000.0, bid_raw / 1000.0, av, bv, prev)
    stats["timezone_semantics"].add("dukascopy_hour_utc")


def scan_parquet(path: Path, stats: dict, naive_timezone: str | None) -> None:
    stats["formats"]["PARQUET"] += 1
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise RuntimeError("pyarrow is required to read Parquet without rewriting it") from exc
    table = pq.read_table(path, columns=list(EXPECTED_PARQUET_COLUMNS))
    cols = {name: table[name].to_pylist() for name in EXPECTED_PARQUET_COLUMNS}
    prev = None
    for ts_raw, bid_raw, ask_raw, bv_raw, av_raw in zip(
        cols["timestamp"], cols["bid_price"], cols["ask_price"], cols["bid_volume"], cols["ask_volume"]
    ):
        try:
            ts = parse_naive_timestamp(ts_raw, naive_timezone) if naive_timezone else parse_aware_timestamp(ts_raw)
            ask, bid = float(ask_raw), float(bid_raw)
            av, bv = float(av_raw), float(bv_raw)
        except (ValueError, TypeError) as exc:
            if not naive_timezone and getattr(ts_raw, "tzinfo", None) is None:
                raise ValueError("PARQUET_NAIVE_TIMESTAMP_REQUIRES_EXPLICIT_NAIVE_TIMEZONE") from exc
            stats["invalid_rows"] += 1
            continue
        prev = record_tick(stats, ts, ask, bid, av, bv, prev)
    stats["timezone_semantics"].add("explicit_zone_for_naive" if naive_timezone else "explicit_utc_or_offset")


def scan(paths: list[Path], naive_timezone: str | None) -> tuple[dict, list[dict]]:
    stats = empty_stats()
    evidence = []
    for path in paths:
        rec = {"path": str(path), "sha256": sha256(path), "format": source_format(path)}
        stats["files"] += 1
        try:
            fmt = rec["format"]
            if fmt == "CSV": scan_csv(path, stats)
            elif fmt == "DUKASCOPY_BI5": scan_bi5(path, stats)
            elif fmt == "PARQUET": scan_parquet(path, stats, naive_timezone)
            else: raise ValueError(f"unsupported source format: {path.suffix}")
        except Exception as exc:
            rec["error"] = str(exc)
            stats["file_errors"].append({"path": str(path), "error": str(exc)})
        evidence.append(rec)
    return stats, evidence


def percentile(values: list[float], p: float) -> float | None:
    if not values: return None
    values = sorted(values)
    x = (len(values) - 1) * p
    lo, hi = math.floor(x), math.ceil(x)
    return values[lo] if lo == hi else values[lo] + (values[hi] - values[lo]) * (x - lo)


def spread_summary(values: list[float]) -> dict:
    return {
        "count": len(values),
        "mean": statistics.fmean(values) if values else None,
        "p50": percentile(values, .50), "p95": percentile(values, .95), "p99": percentile(values, .99),
    }


def movement_summary(stats: dict) -> dict:
    keys = sorted(stats["hour_mid"])
    returns = [math.log(stats["hour_mid"][b] / stats["hour_mid"][a]) for a, b in zip(keys, keys[1:]) if stats["hour_mid"][a] > 0 and stats["hour_mid"][b] > 0]
    absolute = [abs(x) for x in returns]
    return {
        "hour_buckets": len(keys), "hourly_return_count": len(returns),
        "hourly_abs_return_mean": statistics.fmean(absolute) if absolute else None,
        "hourly_abs_return_p50": percentile(absolute, .50),
        "hourly_abs_return_p95": percentile(absolute, .95),
        "hourly_return_std": statistics.stdev(returns) if len(returns) > 1 else None,
    }


def years_between(a: datetime | None, b: datetime | None) -> float | None:
    return (b - a).total_seconds() / (365.2425 * 86400) if a and b else None


def ratio(a: float | None, b: float | None) -> float | None:
    return b / a if a not in (None, 0) and b is not None else None


def status(checks: list[dict]) -> str:
    s = {c["status"] for c in checks}
    if "BLOCKED" in s: return "BLOCKED"
    if "FAIL" in s: return "FAIL"
    if "UNVERIFIED" in s: return "UNVERIFIED"
    return "PASS"


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        research_paths = collect_sources(args.research)
        execution_paths = collect_sources(args.execution)
    except Exception as exc:
        report = {"schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3", "version": "V4.3", "status": "BLOCKED", "reason": f"source access failed: {exc}"}
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("VERDICT=BLOCKED"); print("REPORT=", output); return 2
    if not research_paths or not execution_paths:
        report = {"schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3", "version": "V4.3", "status": "BLOCKED", "reason": "one or both source sets contain no supported data files", "research_files": len(research_paths), "execution_files": len(execution_paths)}
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("VERDICT=BLOCKED"); print("REPORT=", output); return 2

    research, research_files = scan(research_paths, args.naive_timezone)
    execution, execution_files = scan(execution_paths, args.naive_timezone)

    r_checks = [
        {"id": "source_access", "status": "FAIL" if research["file_errors"] else "PASS"},
        {"id": "coverage_5y", "status": "PASS" if (years_between(research["first"], research["last"]) or 0) >= MIN_RESEARCH_YEARS else "FAIL"},
        {"id": "data_integrity", "status": "FAIL" if research["invalid_rows"] or research["quote_violations"] else "PASS"},
        {"id": "ordering", "status": "FAIL" if research["ordering_violations"] else "PASS"},
    ]
    e_checks = [
        {"id": "source_access", "status": "FAIL" if execution["file_errors"] else "PASS"},
        {"id": "data_integrity", "status": "FAIL" if execution["invalid_rows"] or execution["quote_violations"] else "PASS"},
        {"id": "ordering", "status": "FAIL" if execution["ordering_violations"] else "PASS"},
        {"id": "execution_boundary", "status": "PASS" if execution["first"] and utc_iso(execution["first"]) >= EXECUTION_BOUNDARY_UTC else "UNVERIFIED"},
    ]
    if any("PARQUET_NAIVE_TIMESTAMP_REQUIRES" in e["error"] for e in execution["file_errors"] + research["file_errors"]):
        tz_check = {"id": "timestamp_semantics", "status": "BLOCKED", "reason": "naive Parquet timestamp semantics are not allowed to be guessed"}
        r_checks.append(tz_check.copy()); e_checks.append(tz_check.copy())

    r_status, e_status = status(r_checks), status(e_checks)
    common_start = max(research["first"], execution["first"]) if research["first"] and execution["first"] else None
    common_end = min(research["last"], execution["last"]) if research["last"] and execution["last"] else None
    common_years = years_between(common_start, common_end)
    r_move, e_move = movement_summary(research), movement_summary(execution)
    r_spread, e_spread = spread_summary(research["spreads"]), spread_summary(execution["spreads"])

    t_checks = [
        {"id": "distinct_feeds", "status": "PASS", "reason": "property-based comparison only"},
        {"id": "common_period", "status": "PASS" if common_years and common_years > 0 else "FAIL"},
        {"id": "transfer_metrics", "status": "PASS" if r_move["hourly_return_count"] and e_move["hourly_return_count"] else "UNVERIFIED"},
        {"id": "equivalence_thresholds", "status": "UNVERIFIED", "reason": "no normative transfer-equivalence thresholds are frozen"},
    ]
    t_status = status(t_checks)
    overall = status([{"status": r_status}, {"status": e_status}, {"status": t_status}])

    report = {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3", "version": "V4.3", "status": overall,
        "verdicts": {"RESEARCH_DATA_VALID": r_status, "EXECUTION_DATA_VALID": e_status, "TRANSFER_VALIDATION": t_status},
        "scope": {
            "research_instrument": args.research_instrument, "execution_instrument": args.execution_instrument,
            "research_files": research_files, "execution_files": execution_files,
            "execution_observable_boundary_v4_2": EXECUTION_BOUNDARY_UTC,
            "minimum_research_years": MIN_RESEARCH_YEARS, "naive_timezone_argument": args.naive_timezone,
        },
        "research": {
            "rows": research["rows"], "first": utc_iso(research["first"]), "last": utc_iso(research["last"]),
            "years": years_between(research["first"], research["last"]), "formats": dict(research["formats"]),
            "timezone_semantics": sorted(research["timezone_semantics"]), "invalid_rows": research["invalid_rows"],
            "quote_violations": research["quote_violations"], "ordering_violations": research["ordering_violations"],
            "spread": r_spread, "movement": r_move, "checks": r_checks, "files": research_files,
        },
        "execution": {
            "rows": execution["rows"], "first": utc_iso(execution["first"]), "last": utc_iso(execution["last"]),
            "years": years_between(execution["first"], execution["last"]), "formats": dict(execution["formats"]),
            "timezone_semantics": sorted(execution["timezone_semantics"]), "invalid_rows": execution["invalid_rows"],
            "quote_violations": execution["quote_violations"], "ordering_violations": execution["ordering_violations"],
            "spread": e_spread, "movement": e_move, "checks": e_checks, "files": execution_files,
        },
        "common_period": {"first": utc_iso(common_start), "last": utc_iso(common_end), "years": common_years},
        "transfer_metrics": {
            "spread_mean_ratio_execution_over_research": ratio(r_spread["mean"], e_spread["mean"]),
            "spread_p50_ratio_execution_over_research": ratio(r_spread["p50"], e_spread["p50"]),
            "spread_p95_ratio_execution_over_research": ratio(r_spread["p95"], e_spread["p95"]),
            "hourly_abs_return_mean_ratio_execution_over_research": ratio(r_move["hourly_abs_return_mean"], e_move["hourly_abs_return_mean"]),
            "hourly_abs_return_p95_ratio_execution_over_research": ratio(r_move["hourly_abs_return_p95"], e_move["hourly_abs_return_p95"]),
            "hourly_return_std_ratio_execution_over_research": ratio(r_move["hourly_return_std"], e_move["hourly_return_std"]),
        },
        "transfer_checks": t_checks,
        "methodological_guardrails": [
            "No tick-for-tick equality is required between independent feeds.",
            "No dataset is merged or spliced.",
            "No timezone is guessed for naive timestamps.",
            "No statistical equivalence threshold is invented.",
            "Research coverage and execution coverage remain separate truths.",
            "UNVERIFIED and BLOCKED are never promoted to PASS.",
        ],
        "conclusion": "V4.3 now reads native BI5/Parquet/CSV evidence without forcing conversion. Transfer compatibility remains UNVERIFIED until explicit acceptance criteria are frozen and adversarially tested.",
    }
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("=== V4.3 — RESEARCH ↔ EXECUTION COMPATIBILITY ===")
    print("RESEARCH_FORMATS=", report["research"]["formats"])
    print("EXECUTION_FORMATS=", report["execution"]["formats"])
    print("RESEARCH_FIRST=", report["research"]["first"])
    print("RESEARCH_LAST=", report["research"]["last"])
    print("EXECUTION_FIRST=", report["execution"]["first"])
    print("EXECUTION_LAST=", report["execution"]["last"])
    print("COMMON_YEARS=", report["common_period"]["years"])
    print("RESEARCH_DATA_VALID=", r_status)
    print("EXECUTION_DATA_VALID=", e_status)
    print("TRANSFER_VALIDATION=", t_status)
    print("VERDICT=", overall)
    print("REPORT=", output)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

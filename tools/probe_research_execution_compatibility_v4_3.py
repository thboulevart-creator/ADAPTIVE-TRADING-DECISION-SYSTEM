"""V4.3 — Research ↔ Execution data compatibility probe.

Purpose
-------
Compare the *properties required for transfer validation* between a long-term
research tick dataset and the broker/execution tick dataset without pretending
that two independent feeds should be tick-for-tick identical.

This probe is deliberately read-only: it never sorts, repairs, deduplicates,
merges, or rewrites source data. A directory is only a container of source CSVs;
its files remain distinct evidence.

Accepted source schema is the project's frozen experimental tick schema:
    timestamp,askPrice,bidPrice,askVolume,bidVolume

Final verdict policy is fail-closed:
    BLOCKED > FAIL > UNVERIFIED > PASS

Important: V4.3 does NOT invent statistical equivalence thresholds. It reports
measured differences and leaves TRANSFER_VALIDATION UNVERIFIED until explicit
acceptance criteria exist. This prevents a convenient tolerance from becoming
an accidental methodological rule.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

EXPECTED_COLUMNS = ("timestamp", "askPrice", "bidPrice", "askVolume", "bidVolume")
EXECUTION_BOUNDARY_UTC = "2024-12-17T09:38:28+00:00"
MIN_RESEARCH_YEARS = 5.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--research", required=True, help="Research CSV file or directory of CSV files")
    parser.add_argument("--execution", required=True, help="Execution CSV file or directory of CSV files")
    parser.add_argument("--research-instrument", default="Dukascopy USATECHIDXUSD")
    parser.add_argument("--execution-instrument", default="VT Markets NAS100.s")
    parser.add_argument("--output", default="reports/data-qualification/research_execution_compatibility_v4_3.json")
    return parser.parse_args()


def utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def parse_timestamp(text: str) -> datetime:
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return value.astimezone(timezone.utc)


def collect_csvs(path_text: str) -> list[Path]:
    path = Path(path_text)
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(p for p in path.rglob("*.csv") if p.is_file())
    raise FileNotFoundError(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def empty_stats() -> dict:
    return {
        "files": 0,
        "rows": 0,
        "first": None,
        "last": None,
        "invalid_rows": 0,
        "ordering_violations": 0,
        "quote_violations": 0,
        "negative_volume": 0,
        "spreads": [],
        "mid_first": None,
        "mid_last": None,
        "hour_mid": {},
        "hour_count": defaultdict(int),
    }


def scan(paths: Iterable[Path]) -> tuple[dict, list[dict]]:
    stats = empty_stats()
    evidence: list[dict] = []
    previous_global: datetime | None = None

    for path in paths:
        file_record = {"path": str(path), "sha256": sha256(path), "rows": 0, "first": None, "last": None}
        stats["files"] += 1
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                header = tuple(reader.fieldnames or ())
                if header != EXPECTED_COLUMNS:
                    raise ValueError(f"unexpected columns: {header!r}; expected {EXPECTED_COLUMNS!r}")
                previous_file: datetime | None = None
                for row_no, row in enumerate(reader, start=2):
                    file_record["rows"] += 1
                    stats["rows"] += 1
                    try:
                        ts = parse_timestamp(row["timestamp"])
                        ask = Decimal(row["askPrice"])
                        bid = Decimal(row["bidPrice"])
                        av = Decimal(row["askVolume"])
                        bv = Decimal(row["bidVolume"])
                        if not all(v.is_finite() for v in (ask, bid, av, bv)):
                            raise ValueError("non-finite numeric value")
                        if ask <= 0 or bid <= 0 or av < 0 or bv < 0:
                            raise ValueError("invalid numeric domain")
                    except (KeyError, InvalidOperation, ValueError) as exc:
                        stats["invalid_rows"] += 1
                        if stats["invalid_rows"] <= 5:
                            file_record.setdefault("errors", []).append({"row": row_no, "error": str(exc)})
                        continue

                    if ask < bid:
                        stats["quote_violations"] += 1
                    if previous_file is not None and ts < previous_file:
                        stats["ordering_violations"] += 1
                    if previous_global is not None and ts < previous_global:
                        stats["ordering_violations"] += 1
                    previous_file = ts
                    previous_global = ts

                    spread = float(ask - bid)
                    mid = float((ask + bid) / Decimal(2))
                    stats["spreads"].append(spread)
                    hour = ts.replace(minute=0, second=0, microsecond=0)
                    stats["hour_count"][hour] += 1
                    stats["hour_mid"][hour] = mid
                    if stats["first"] is None or ts < stats["first"]:
                        stats["first"] = ts
                        stats["mid_first"] = mid
                    if stats["last"] is None or ts > stats["last"]:
                        stats["last"] = ts
                        stats["mid_last"] = mid
                    if file_record["first"] is None:
                        file_record["first"] = utc_iso(ts)
                    file_record["last"] = utc_iso(ts)
        except (OSError, UnicodeError, ValueError) as exc:
            file_record["error"] = str(exc)
            stats.setdefault("file_errors", []).append({"path": str(path), "error": str(exc)})
        evidence.append(file_record)

    return stats, evidence


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    index = (len(values) - 1) * p
    lo = math.floor(index)
    hi = math.ceil(index)
    if lo == hi:
        return values[lo]
    return values[lo] + (values[hi] - values[lo]) * (index - lo)


def spread_summary(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "mean": None, "p50": None, "p95": None, "p99": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "p99": percentile(values, 0.99),
    }


def hourly_returns(hour_mid: dict[datetime, float]) -> list[float]:
    keys = sorted(hour_mid)
    result: list[float] = []
    for a, b in zip(keys, keys[1:]):
        if hour_mid[a] > 0 and hour_mid[b] > 0:
            result.append(math.log(hour_mid[b] / hour_mid[a]))
    return result


def movement_summary(stats: dict) -> dict:
    returns = hourly_returns(stats["hour_mid"])
    abs_returns = [abs(x) for x in returns]
    return {
        "hour_buckets": len(stats["hour_mid"]),
        "hourly_return_count": len(returns),
        "hourly_abs_return_mean": statistics.fmean(abs_returns) if abs_returns else None,
        "hourly_abs_return_p50": percentile(abs_returns, 0.50),
        "hourly_abs_return_p95": percentile(abs_returns, 0.95),
        "hourly_return_std": statistics.stdev(returns) if len(returns) > 1 else None,
    }


def years_between(first: datetime | None, last: datetime | None) -> float | None:
    if first is None or last is None:
        return None
    return (last - first).total_seconds() / (365.2425 * 86400)


def compatibility_ratio(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or a == 0 or b == 0:
        return None
    return b / a


def status_from_checks(checks: list[dict]) -> str:
    statuses = {c["status"] for c in checks}
    if "BLOCKED" in statuses:
        return "BLOCKED"
    if "FAIL" in statuses:
        return "FAIL"
    if "UNVERIFIED" in statuses:
        return "UNVERIFIED"
    return "PASS"


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        research_paths = collect_csvs(args.research)
        execution_paths = collect_csvs(args.execution)
    except (OSError, FileNotFoundError) as exc:
        report = {
            "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
            "status": "BLOCKED",
            "reason": f"source access failed: {exc}",
            "verdicts": {"RESEARCH_DATA_VALID": "BLOCKED", "EXECUTION_DATA_VALID": "BLOCKED", "TRANSFER_VALIDATION": "BLOCKED"},
        }
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("VERDICT=BLOCKED")
        print("REPORT=", output)
        return 2

    if not research_paths or not execution_paths:
        report = {
            "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
            "status": "BLOCKED",
            "reason": "one or both source sets contain no CSV files",
            "research_files": len(research_paths),
            "execution_files": len(execution_paths),
        }
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("VERDICT=BLOCKED")
        print("REPORT=", output)
        return 2

    research, research_files = scan(research_paths)
    execution, execution_files = scan(execution_paths)

    research_checks = [
        {"id": "source_access", "status": "FAIL" if research.get("file_errors") else "PASS", "reason": "all research files readable" if not research.get("file_errors") else "one or more research files failed"},
        {"id": "schema", "status": "FAIL" if research.get("file_errors") else "PASS", "reason": "source schema is checked against the project tick contract"},
        {"id": "coverage_5y", "status": "PASS" if (years_between(research["first"], research["last"]) or 0) >= MIN_RESEARCH_YEARS else "FAIL", "reason": "research coverage is at least five years"},
        {"id": "data_integrity", "status": "FAIL" if research["invalid_rows"] or research["quote_violations"] else "PASS", "reason": "no invalid rows or ask < bid observations"},
    ]
    execution_checks = [
        {"id": "source_access", "status": "FAIL" if execution.get("file_errors") else "PASS", "reason": "all execution files readable" if not execution.get("file_errors") else "one or more execution files failed"},
        {"id": "data_integrity", "status": "FAIL" if execution["invalid_rows"] or execution["quote_violations"] else "PASS", "reason": "no invalid rows or ask < bid observations"},
        {"id": "execution_boundary", "status": "PASS" if execution["first"] is not None and utc_iso(execution["first"]) >= EXECUTION_BOUNDARY_UTC else "UNVERIFIED", "reason": "execution source begins at/after the V4.2 observable MT5 boundary"},
    ]

    research_status = status_from_checks(research_checks)
    execution_status = status_from_checks(execution_checks)

    common_start = max(x for x in (research["first"], execution["first"]) if x is not None) if research["first"] and execution["first"] else None
    common_end = min(x for x in (research["last"], execution["last"]) if x is not None) if research["last"] and execution["last"] else None
    common_years = years_between(common_start, common_end)

    r_move = movement_summary(research)
    e_move = movement_summary(execution)
    r_spread = spread_summary(research["spreads"])
    e_spread = spread_summary(execution["spreads"])

    transfer_checks = [
        {"id": "distinct_feeds", "status": "PASS", "reason": "comparison is property-based, not tick-for-tick equality"},
        {"id": "common_period", "status": "PASS" if common_years and common_years > 0 else "FAIL", "reason": "a non-empty common market period exists"},
        {"id": "research_execution_metrics", "status": "PASS" if r_move["hourly_return_count"] and e_move["hourly_return_count"] else "UNVERIFIED", "reason": "both feeds expose measurable movement and spread distributions"},
        {"id": "equivalence_thresholds", "status": "UNVERIFIED", "reason": "no normative transfer-equivalence thresholds are currently frozen; V4.3 must not invent them"},
    ]
    transfer_status = status_from_checks(transfer_checks)

    statuses = {research_status, execution_status, transfer_status}
    if "BLOCKED" in statuses:
        overall = "BLOCKED"
    elif "FAIL" in statuses:
        overall = "FAIL"
    elif "UNVERIFIED" in statuses:
        overall = "UNVERIFIED"
    else:
        overall = "PASS"

    report = {
        "schema": "RESEARCH_EXECUTION_COMPATIBILITY_V4_3",
        "version": "V4.3",
        "status": overall,
        "verdicts": {
            "RESEARCH_DATA_VALID": research_status,
            "EXECUTION_DATA_VALID": execution_status,
            "TRANSFER_VALIDATION": transfer_status,
        },
        "scope": {
            "research_instrument": args.research_instrument,
            "execution_instrument": args.execution_instrument,
            "research_files": research_files,
            "execution_files": execution_files,
            "execution_observable_boundary_v4_2": EXECUTION_BOUNDARY_UTC,
            "minimum_research_years": MIN_RESEARCH_YEARS,
        },
        "research": {
            "rows": research["rows"],
            "first": utc_iso(research["first"]) if research["first"] else None,
            "last": utc_iso(research["last"]) if research["last"] else None,
            "years": years_between(research["first"], research["last"]),
            "invalid_rows": research["invalid_rows"],
            "quote_violations": research["quote_violations"],
            "ordering_violations": research["ordering_violations"],
            "spread": r_spread,
            "movement": r_move,
            "checks": research_checks,
            "files": research_files,
        },
        "execution": {
            "rows": execution["rows"],
            "first": utc_iso(execution["first"]) if execution["first"] else None,
            "last": utc_iso(execution["last"]) if execution["last"] else None,
            "years": years_between(execution["first"], execution["last"]),
            "invalid_rows": execution["invalid_rows"],
            "quote_violations": execution["quote_violations"],
            "ordering_violations": execution["ordering_violations"],
            "spread": e_spread,
            "movement": e_move,
            "checks": execution_checks,
            "files": execution_files,
        },
        "common_period": {
            "first": utc_iso(common_start) if common_start else None,
            "last": utc_iso(common_end) if common_end else None,
            "years": common_years,
        },
        "transfer_metrics": {
            "spread_mean_ratio_execution_over_research": compatibility_ratio(r_spread["mean"], e_spread["mean"]),
            "spread_p50_ratio_execution_over_research": compatibility_ratio(r_spread["p50"], e_spread["p50"]),
            "spread_p95_ratio_execution_over_research": compatibility_ratio(r_spread["p95"], e_spread["p95"]),
            "hourly_abs_return_mean_ratio_execution_over_research": compatibility_ratio(r_move["hourly_abs_return_mean"], e_move["hourly_abs_return_mean"]),
            "hourly_abs_return_p95_ratio_execution_over_research": compatibility_ratio(r_move["hourly_abs_return_p95"], e_move["hourly_abs_return_p95"]),
            "hourly_return_std_ratio_execution_over_research": compatibility_ratio(r_move["hourly_return_std"], e_move["hourly_return_std"]),
        },
        "transfer_checks": transfer_checks,
        "methodological_guardrails": [
            "No tick-for-tick equality is expected between independent feeds.",
            "No dataset is merged or spliced.",
            "No statistical equivalence threshold is invented by this probe.",
            "Research coverage and execution coverage remain separate truths.",
            "A UNVERIFIED transfer verdict is not a PASS.",
        ],
        "conclusion": "V4.3 measures transfer-relevant differences but cannot declare research/execution equivalence until explicit acceptance thresholds are frozen and adversarially tested.",
    }

    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("=== V4.3 — RESEARCH ↔ EXECUTION COMPATIBILITY ===")
    print("RESEARCH=", args.research)
    print("EXECUTION=", args.execution)
    print("RESEARCH_FIRST=", report["research"]["first"])
    print("RESEARCH_LAST=", report["research"]["last"])
    print("EXECUTION_FIRST=", report["execution"]["first"])
    print("EXECUTION_LAST=", report["execution"]["last"])
    print("COMMON_YEARS=", report["common_period"]["years"])
    print("RESEARCH_DATA_VALID=", research_status)
    print("EXECUTION_DATA_VALID=", execution_status)
    print("TRANSFER_VALIDATION=", transfer_status)
    print("VERDICT=", overall)
    print("REPORT=", output)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

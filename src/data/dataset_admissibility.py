"""Executable dataset identity and admissibility boundary for tick experiments.

This module deliberately does not repair, sort, deduplicate, or normalize source
market data. It identifies the exact source bytes and reports whether those bytes
are admissible for an experiment.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal

from src.data.tick_reader import EXPECTED_COLUMNS


Verdict = Literal["PASS", "FAIL", "BLOCKED", "UNVERIFIED"]


@dataclass(frozen=True)
class DatasetIdentity:
    dataset_id: str
    dataset_version: str
    content_hash: str
    format: str
    schema_version: str
    instrument: str
    granularity: str
    timezone_storage: str


@dataclass(frozen=True)
class AdmissibilityCheck:
    check_id: str
    status: Literal["PASS", "FAIL", "UNVERIFIED"]
    reason: str


@dataclass(frozen=True)
class DatasetAdmissibilityReport:
    dataset: DatasetIdentity
    row_count: int
    first_timestamp: str | None
    last_timestamp: str | None
    checks: tuple[AdmissibilityCheck, ...]
    verdict: Verdict


def build_identity(
    path: str | Path,
    *,
    dataset_id: str,
    dataset_version: str,
    instrument: str,
    granularity: str,
    timezone_storage: str,
    schema_version: str = "tick-csv-v1",
) -> DatasetIdentity:
    """Build a content-addressed identity from the exact source file bytes."""

    source = Path(path)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    return DatasetIdentity(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        content_hash=digest,
        format="csv",
        schema_version=schema_version,
        instrument=instrument,
        granularity=granularity,
        timezone_storage=timezone_storage,
    )


def assess(
    path: str | Path,
    *,
    identity: DatasetIdentity,
) -> DatasetAdmissibilityReport:
    """Assess a tick CSV without changing its contents."""

    source = Path(path)
    checks: list[AdmissibilityCheck] = []
    row_count = 0
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    previous_timestamp: datetime | None = None
    seen_timestamps: set[str] = set()

    actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    checks.append(
        AdmissibilityCheck(
            "content_hash",
            "PASS" if actual_hash == identity.content_hash else "FAIL",
            "source bytes match DatasetIdentity" if actual_hash == identity.content_hash else "source bytes differ from DatasetIdentity",
        )
    )

    try:
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
                checks.append(AdmissibilityCheck("schema", "FAIL", "CSV header does not match the declared tick schema"))
            else:
                checks.append(AdmissibilityCheck("schema", "PASS", "CSV header matches the declared tick schema"))

            if tuple(reader.fieldnames or ()) == EXPECTED_COLUMNS:
                for row_count, row in enumerate(reader, start=1):
                    if any(row[column] is None or row[column] == "" for column in EXPECTED_COLUMNS):
                        checks.append(AdmissibilityCheck("row_shape", "FAIL", f"missing value at row={row_count}"))
                        break

                    timestamp_text = row["timestamp"]
                    try:
                        timestamp = datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))
                        if timestamp.tzinfo is None:
                            raise ValueError("timestamp has no timezone")
                    except ValueError as exc:
                        checks.append(AdmissibilityCheck("timestamp", "FAIL", f"invalid timestamp at row={row_count}: {exc}"))
                        break

                    try:
                        ask = Decimal(row["askPrice"])
                        bid = Decimal(row["bidPrice"])
                        ask_volume = Decimal(row["askVolume"])
                        bid_volume = Decimal(row["bidVolume"])
                        if not all(value.is_finite() for value in (ask, bid, ask_volume, bid_volume)):
                            raise ValueError("non-finite numeric value")
                        if ask <= 0 or bid <= 0 or ask_volume < 0 or bid_volume < 0:
                            raise ValueError("invalid price or volume domain value")
                    except (InvalidOperation, ValueError) as exc:
                        checks.append(AdmissibilityCheck("numeric_domain", "FAIL", f"invalid numeric value at row={row_count}: {exc}"))
                        break

                    if ask < bid:
                        checks.append(AdmissibilityCheck("quote_integrity", "FAIL", f"ask < bid at row={row_count}"))
                        break

                    if timestamp_text in seen_timestamps:
                        checks.append(AdmissibilityCheck("duplicates", "FAIL", f"duplicate timestamp at row={row_count}"))
                        break
                    seen_timestamps.add(timestamp_text)

                    if previous_timestamp is not None and timestamp <= previous_timestamp:
                        checks.append(AdmissibilityCheck("ordering", "FAIL", f"timestamps are not strictly increasing at row={row_count}"))
                        break
                    previous_timestamp = timestamp

                    if first_timestamp is None:
                        first_timestamp = timestamp_text
                    last_timestamp = timestamp_text

        if not any(check.check_id == "row_shape" for check in checks):
            checks.append(AdmissibilityCheck("row_shape", "PASS", "all rows contain the declared fields"))
        if not any(check.check_id == "timestamp" for check in checks):
            checks.append(AdmissibilityCheck("timestamp", "PASS", "all timestamps are timezone-aware ISO-8601 values"))
        if not any(check.check_id == "numeric_domain" for check in checks):
            checks.append(AdmissibilityCheck("numeric_domain", "PASS", "prices and volumes satisfy the declared numeric domain"))
        if not any(check.check_id == "quote_integrity" for check in checks):
            checks.append(AdmissibilityCheck("quote_integrity", "PASS", "ask is greater than or equal to bid for every row"))
        if not any(check.check_id == "duplicates" for check in checks):
            checks.append(AdmissibilityCheck("duplicates", "PASS", "no duplicate timestamps observed"))
        if not any(check.check_id == "ordering" for check in checks):
            checks.append(AdmissibilityCheck("ordering", "PASS", "timestamps are strictly increasing"))

    except OSError as exc:
        checks.append(AdmissibilityCheck("source_access", "BLOCKED", f"cannot access source file: {exc}"))

    verdict: Verdict
    statuses = {check.status for check in checks}
    if "BLOCKED" in statuses:
        verdict = "BLOCKED"
    elif "FAIL" in statuses:
        verdict = "FAIL"
    elif "UNVERIFIED" in statuses:
        verdict = "UNVERIFIED"
    else:
        verdict = "PASS"

    return DatasetAdmissibilityReport(
        dataset=identity,
        row_count=row_count,
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        checks=tuple(checks),
        verdict=verdict,
    )

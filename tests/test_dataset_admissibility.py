from pathlib import Path

import pytest

from src.data.dataset_admissibility import DatasetIdentity, assess, build_identity


COLUMNS = "timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
ROWS = (
    "2026-01-01T09:00:00+00:00,100.1,100.0,1,2\n"
    "2026-01-01T09:00:01+00:00,100.2,100.1,1,2\n"
)


def write_dataset(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "ticks.csv"
    path.write_text(COLUMNS + body, encoding="utf-8")
    return path


def identity_for(path: Path) -> DatasetIdentity:
    return build_identity(
        path,
        dataset_id="TEST-NAS100",
        dataset_version="v1",
        instrument="NAS100",
        granularity="tick",
        timezone_storage="UTC",
    )


def test_valid_dataset_is_admissible(tmp_path: Path):
    path = write_dataset(tmp_path, ROWS)
    report = assess(path, identity=identity_for(path))
    assert report.verdict == "PASS"
    assert report.row_count == 2


def test_hash_mismatch_rejects_changed_source(tmp_path: Path):
    path = write_dataset(tmp_path, ROWS)
    identity = identity_for(path)
    path.write_text(COLUMNS + ROWS + "2026-01-01T09:00:02+00:00,100.3,100.2,1,2\n", encoding="utf-8")
    report = assess(path, identity=identity)
    assert report.verdict == "FAIL"
    assert any(c.check_id == "content_hash" and c.status == "FAIL" for c in report.checks)


def test_wrong_schema_is_rejected(tmp_path: Path):
    path = tmp_path / "ticks.csv"
    path.write_text("timestamp,bidPrice,askPrice,askVolume,bidVolume\n" + ROWS.splitlines()[0] + "\n", encoding="utf-8")
    report = assess(path, identity=identity_for(path))
    assert report.verdict == "FAIL"
    assert any(c.check_id == "schema" and c.status == "FAIL" for c in report.checks)


@pytest.mark.parametrize(
    "body,check_id",
    [
        ("2026-01-01T09:00:01+00:00,100.1,100.0,1,2\n2026-01-01T09:00:00+00:00,100.2,100.1,1,2\n", "ordering"),
        ("2026-01-01T09:00:00+00:00,99.0,100.0,1,2\n", "quote_integrity"),
        ("2026-01-01T09:00:00+00:00,100.1,100.0,1,2\n2026-01-01T09:00:01,100.2,100.1,1,2\n", "timestamp"),
        ("2026-01-01T09:00:00+00:00,-1,100.0,1,2\n", "numeric_domain"),
        ("2026-01-01T09:00:00+00:00,100.1,,1,2\n", "row_shape"),
    ],
)
def test_invalid_dataset_is_explicitly_rejected(tmp_path: Path, body: str, check_id: str):
    path = write_dataset(tmp_path, body)
    report = assess(path, identity=identity_for(path))
    assert report.verdict == "FAIL"
    assert any(c.check_id == check_id and c.status == "FAIL" for c in report.checks)


def test_missing_source_is_blocked(tmp_path: Path):
    path = tmp_path / "missing.csv"
    identity = DatasetIdentity(
        dataset_id="TEST-NAS100",
        dataset_version="v1",
        content_hash="0" * 64,
        format="csv",
        schema_version="tick-csv-v1",
        instrument="NAS100",
        granularity="tick",
        timezone_storage="UTC",
    )
    report = assess(path, identity=identity)
    assert report.verdict == "BLOCKED"

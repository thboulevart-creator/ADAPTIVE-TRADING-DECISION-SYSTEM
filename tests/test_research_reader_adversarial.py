from pathlib import Path

import pytest

from src.data.tick_reader import EXPECTED_COLUMNS, load


VALID_ROWS = (
    "2026-01-02T00:00:00.001Z,100.2,100.0,1.5,2.0\n"
    "2026-01-02T00:00:00.002Z,100.3,100.1,1.0,1.25\n"
)


def write_csv(tmp_path: Path, header: str, rows: str = VALID_ROWS) -> Path:
    path = tmp_path / "ticks.csv"
    path.write_text(header + rows, encoding="utf-8")
    return path


def test_c0_v43_frozen_csv_schema_is_consumed(tmp_path: Path) -> None:
    path = write_csv(tmp_path, ",".join(EXPECTED_COLUMNS) + "\n")
    ticks = list(load(path))
    assert len(ticks) == 2
    assert ticks[0].timestamp.endswith("Z")
    assert ticks[0].ask_price > ticks[0].bid_price


def test_c1_missing_v43_column_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "timestamp,askPrice,bidPrice,askVolume\n")
    with pytest.raises(ValueError, match="Unexpected columns"):
        list(load(path))


def test_c2_extra_column_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "timestamp,askPrice,bidPrice,askVolume,bidVolume,extra\n")
    with pytest.raises(ValueError, match="Unexpected columns"):
        list(load(path))


def test_c3_column_reordering_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "timestamp,bidPrice,askPrice,askVolume,bidVolume\n")
    with pytest.raises(ValueError, match="Unexpected columns"):
        list(load(path))


def test_c4_missing_header_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "ticks.csv"
    path.write_text(VALID_ROWS, encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected columns"):
        list(load(path))


def test_c5_malformed_row_is_rejected(tmp_path: Path) -> None:
    path = write_csv(
        tmp_path,
        ",".join(EXPECTED_COLUMNS) + "\n",
        "2026-01-02T00:00:00.001Z,100.2,100.0,1.5\n",
    )
    with pytest.raises(ValueError, match="Malformed row"):
        list(load(path))


def test_c6_non_numeric_price_is_rejected(tmp_path: Path) -> None:
    path = write_csv(
        tmp_path,
        ",".join(EXPECTED_COLUMNS) + "\n",
        "2026-01-02T00:00:00.001Z,NOT_A_NUMBER,100.0,1.5,2.0\n",
    )
    with pytest.raises(Exception):
        list(load(path))


def test_c7_non_numeric_volume_is_rejected(tmp_path: Path) -> None:
    path = write_csv(
        tmp_path,
        ",".join(EXPECTED_COLUMNS) + "\n",
        "2026-01-02T00:00:00.001Z,100.2,100.0,NOT_A_NUMBER,2.0\n",
    )
    with pytest.raises(Exception):
        list(load(path))


def test_c8_empty_data_is_distinct_from_valid_input(tmp_path: Path) -> None:
    path = write_csv(tmp_path, ",".join(EXPECTED_COLUMNS) + "\n", "")
    assert list(load(path)) == []


def test_c9_reader_does_not_repair_or_sort_v43_order(tmp_path: Path) -> None:
    path = write_csv(
        tmp_path,
        ",".join(EXPECTED_COLUMNS) + "\n",
        "2026-01-02T00:00:00.002Z,100.3,100.1,1.0,1.25\n"
        "2026-01-02T00:00:00.001Z,100.2,100.0,1.5,2.0\n",
    )
    ticks = list(load(path))
    assert [tick.read_index for tick in ticks] == [0, 1]
    assert ticks[0].timestamp.endswith("002Z")
    assert ticks[1].timestamp.endswith("001Z")

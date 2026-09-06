from pathlib import Path

import pytest

from src.data.tick_reader import EXPECTED_COLUMNS, Tick, load


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    path = tmp_path / "ticks.csv"
    path.write_text(
        "timestamp,askPrice,bidPrice,askVolume,bidVolume\n"
        "2026-01-02T00:00:00.001Z,100.2,100.0,1.5,2.0\n"
        "2026-01-02T00:00:00.002Z,100.3,100.1,1.0,1.25\n",
        encoding="utf-8",
    )
    return path


def test_expected_schema(sample_csv: Path) -> None:
    ticks = list(load(sample_csv))
    assert len(ticks) == 2
    assert isinstance(ticks[0], Tick)
    assert ticks[0].timestamp == "2026-01-02T00:00:00.001Z"
    assert ticks[0].read_index == 0
    assert ticks[1].read_index == 1


def test_repeated_reads_are_identical(sample_csv: Path) -> None:
    assert list(load(sample_csv)) == list(load(sample_csv))


def test_header_must_match_exactly(tmp_path: Path) -> None:
    path = tmp_path / "ticks.csv"
    path.write_text("timestamp,askPrice,bidPrice\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected columns"):
        list(load(path))


def test_declared_schema_is_exact() -> None:
    assert EXPECTED_COLUMNS == (
        "timestamp",
        "askPrice",
        "bidPrice",
        "askVolume",
        "bidVolume",
    )

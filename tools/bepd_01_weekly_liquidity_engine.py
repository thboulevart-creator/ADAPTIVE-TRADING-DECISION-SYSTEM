from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

PRICE_SURFACE = "mid"
MID_IS_EXECUTION_PRICE = False
FIVE_YEAR_SCAN_AUTHORIZED = False
TRADING_AUTHORITY = False

_EXPECTED_FIXTURE_SCHEMA = "ATDS_BEPD_01A_WEEKLY_LIQUIDITY_CALIBRATION_FIXTURE_V0_1"
_EXPECTED_TIMEZONE = "Europe/Paris"
_EXPECTED_WEEKS = (
    "2026-01-12",
    "2026-01-19",
    "2026-01-26",
    "2026-02-02",
    "2026-02-09",
    "2026-02-16",
)


def _number(value: Any) -> float:
    return round(float(value), 6)


def _strict_take(side: str, close: float, level: float) -> bool:
    if side == "HIGH":
        return float(close) > float(level)
    if side == "LOW":
        return float(close) < float(level)
    raise ValueError(f"invalid side: {side!r}")


def _strict_reintegration(side: str, close: float, level: float) -> bool:
    if side == "HIGH":
        return float(close) < float(level)
    if side == "LOW":
        return float(close) > float(level)
    raise ValueError(f"invalid side: {side!r}")


def _displacement(side: str, level: float, weekly_close: float) -> float:
    if side == "HIGH":
        return _number(float(level) - float(weekly_close))
    if side == "LOW":
        return _number(float(weekly_close) - float(level))
    raise ValueError(f"invalid side: {side!r}")


def evaluate_level_event(
    side: str,
    level: float,
    h1_bars: list[dict[str, Any]],
    weekly_close: float,
) -> dict[str, Any]:
    if side not in {"HIGH", "LOW"}:
        raise ValueError(f"invalid side: {side!r}")

    take_index: int | None = None
    for index, bar in enumerate(h1_bars):
        if _strict_take(side, float(bar["close"]), float(level)):
            take_index = index
            break

    if take_index is None:
        return {
            "taken": False,
            "take_index": None,
            "reintegration_index": None,
            "same_week_reintegration": False,
            "close_displacement": None,
        }

    reintegration_index: int | None = None
    for index in range(take_index + 1, len(h1_bars)):
        if _strict_reintegration(side, float(h1_bars[index]["close"]), float(level)):
            reintegration_index = index
            break

    return {
        "taken": True,
        "take_index": take_index,
        "reintegration_index": reintegration_index,
        "same_week_reintegration": reintegration_index is not None,
        "close_displacement": _displacement(side, float(level), float(weekly_close)),
    }


def _bar_start_iso(bar: dict[str, Any] | None) -> str | None:
    if bar is None or "start" not in bar:
        return None
    value = bar["start"]
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def _event_record(
    level_state: dict[str, Any],
    result: dict[str, Any],
    h1_bars: list[dict[str, Any]],
    weekly_close: float,
) -> dict[str, Any]:
    take_index = int(result["take_index"])
    reintegration_index = result["reintegration_index"]
    take_bar = h1_bars[take_index]
    reintegration_bar = (
        h1_bars[int(reintegration_index)] if reintegration_index is not None else None
    )

    event = {
        "source_week": level_state["source_week"],
        "side": level_state["side"],
        "level": _number(level_state["level"]),
        "age_weeks": int(level_state["age_weeks"]),
        "take_h1": _bar_start_iso(take_bar),
        "take_h1_close": _number(take_bar["close"]),
        "reintegration_h1": _bar_start_iso(reintegration_bar),
        "reintegration_h1_close": (
            _number(reintegration_bar["close"]) if reintegration_bar is not None else None
        ),
        "same_week_reintegration": bool(result["same_week_reintegration"]),
        "target_week_close": _number(weekly_close),
        "close_displacement": _number(result["close_displacement"]),
        "_take_index": take_index,
    }
    return event


def _active_view(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    view = [
        {
            "source_week": row["source_week"],
            "side": row["side"],
            "level": _number(row["level"]),
            "age_weeks": int(row["age_weeks"]),
        }
        for row in rows
    ]
    return sorted(view, key=lambda x: (x["source_week"], x["side"], float(x["level"])))


def advance_week(
    active_levels: list[dict[str, Any]],
    target_week: str,
    h1_bars: list[dict[str, Any]],
    weekly_close: float,
    completed_week_high: float,
    completed_week_low: float,
) -> dict[str, Any]:
    working = deepcopy(active_levels)
    survivors: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []

    for level_state in working:
        side = level_state.get("side")
        if side not in {"HIGH", "LOW"}:
            raise ValueError(f"invalid side: {side!r}")

        level_state["age_weeks"] = int(level_state.get("age_weeks", 0)) + 1
        result = evaluate_level_event(
            side,
            float(level_state["level"]),
            h1_bars,
            float(weekly_close),
        )

        if result["taken"]:
            events.append(
                _event_record(level_state, result, h1_bars, float(weekly_close))
            )
        else:
            survivors.append(level_state)

    events.sort(
        key=lambda x: (
            int(x["_take_index"]),
            x["side"],
            x["source_week"],
            float(x["level"]),
        )
    )
    for event in events:
        event.pop("_take_index", None)

    survivors.extend(
        [
            {
                "source_week": target_week,
                "side": "HIGH",
                "level": _number(completed_week_high),
                "age_weeks": 0,
            },
            {
                "source_week": target_week,
                "side": "LOW",
                "level": _number(completed_week_low),
                "age_weeks": 0,
            },
        ]
    )

    return {
        "cluster": {
            "target_week": target_week,
            "events": events,
        },
        "active_after": _active_view(survivors),
    }


def _required_month_files(ap0_root: Path, weeks: tuple[str, ...]) -> list[Path]:
    seen: set[tuple[int, int]] = set()
    paths: list[Path] = []
    for week in weeks:
        year, month, _ = (int(x) for x in week.split("-"))
        key = (year, month)
        if key in seen:
            continue
        seen.add(key)
        p = (
            ap0_root
            / f"year={year}"
            / f"month={month:02d}"
            / f"USTECH-PROFILE-M1-{year}-{month:02d}.parquet"
        )
        if not p.is_file():
            raise FileNotFoundError(p)
        paths.append(p)
    return paths


def _load_bounded_ap0(ap0_root: Path, fixture: dict[str, Any]):
    import pandas as pd
    import pyarrow.parquet as pq

    fixture_weeks = tuple(x["week"] for x in fixture["weekly_bars"])
    if fixture_weeks != _EXPECTED_WEEKS:
        raise ValueError("BEPD-01C replay is limited to the adopted six-week fixture")

    columns = [
        "minute_start_ms_utc",
        "mid_open",
        "mid_high",
        "mid_low",
        "mid_close",
    ]
    frames = [
        pq.read_table(path, columns=columns).to_pandas()
        for path in _required_month_files(Path(ap0_root), fixture_weeks)
    ]
    df = pd.concat(frames, ignore_index=True)
    df["ts"] = pd.to_datetime(df["minute_start_ms_utc"], unit="ms", utc=True).dt.tz_convert(
        _EXPECTED_TIMEZONE
    )
    return df.sort_values("ts").reset_index(drop=True)


def _weekly_bars_from_ap0(df, fixture: dict[str, Any]) -> tuple[list[dict[str, Any]], list[Any]]:
    import pandas as pd

    bars: list[dict[str, Any]] = []
    slices: list[Any] = []

    for expected in fixture["weekly_bars"]:
        week = expected["week"]
        start = pd.Timestamp(f"{week} 00:00", tz=_EXPECTED_TIMEZONE)
        end = start + pd.Timedelta(days=5)
        g = df[(df["ts"] >= start) & (df["ts"] < end)].copy().sort_values("ts")
        if g.empty:
            raise ValueError(f"no AP0 observations for calibration week {week}")

        high_idx = g["mid_high"].idxmax()
        low_idx = g["mid_low"].idxmin()
        bars.append(
            {
                "week": week,
                "open": _number(g.iloc[0]["mid_open"]),
                "high": _number(g["mid_high"].max()),
                "high_time": g.loc[high_idx, "ts"].isoformat(),
                "low": _number(g["mid_low"].min()),
                "low_time": g.loc[low_idx, "ts"].isoformat(),
                "close": _number(g.iloc[-1]["mid_close"]),
                "close_time": g.iloc[-1]["ts"].isoformat(),
            }
        )
        slices.append(g)

    return bars, slices


def _h1_bars(week_df) -> list[dict[str, Any]]:
    z = week_df.copy()
    z["h1_start"] = z["ts"].dt.floor("h")
    rows: list[dict[str, Any]] = []
    for start, g in z.groupby("h1_start", sort=True):
        g = g.sort_values("ts")
        rows.append(
            {
                "start": start,
                "open": _number(g.iloc[0]["mid_open"]),
                "high": _number(g["mid_high"].max()),
                "low": _number(g["mid_low"].min()),
                "close": _number(g.iloc[-1]["mid_close"]),
            }
        )
    return rows


def replay_calibration(
    ap0_root: Path | str,
    frozen_fixture: dict[str, Any],
) -> dict[str, Any]:
    if frozen_fixture.get("schema") != _EXPECTED_FIXTURE_SCHEMA:
        raise ValueError("unexpected BEPD-01A fixture schema")
    if frozen_fixture.get("price_surface") != PRICE_SURFACE:
        raise ValueError("unexpected price surface")
    if frozen_fixture.get("calendar_timezone") != _EXPECTED_TIMEZONE:
        raise ValueError("unexpected calibration timezone")
    if len(frozen_fixture.get("weekly_bars", [])) != 6:
        raise ValueError("unexpected calibration week count")
    if len(frozen_fixture.get("expected_clusters", [])) != 5:
        raise ValueError("unexpected calibration cluster count")

    df = _load_bounded_ap0(Path(ap0_root), frozen_fixture)
    weekly_bars, week_slices = _weekly_bars_from_ap0(df, frozen_fixture)

    first = weekly_bars[0]
    active: list[dict[str, Any]] = [
        {
            "source_week": first["week"],
            "side": "HIGH",
            "level": first["high"],
            "age_weeks": 0,
        },
        {
            "source_week": first["week"],
            "side": "LOW",
            "level": first["low"],
            "age_weeks": 0,
        },
    ]

    clusters: list[dict[str, Any]] = []
    for index in range(1, len(weekly_bars)):
        current = weekly_bars[index]
        result = advance_week(
            active,
            current["week"],
            _h1_bars(week_slices[index]),
            current["close"],
            current["high"],
            current["low"],
        )
        clusters.append(
            {
                "target_week": current["week"],
                "events": result["cluster"]["events"],
                "active_after": result["active_after"],
            }
        )
        active = result["active_after"]

    return {
        "weekly_bars": weekly_bars,
        "expected_clusters": clusters,
    }

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import subprocess
import sys
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow.parquet as pq

REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"

AUTH_PATH = Path("GOVERNANCE/BEPD-02-REAL-HISTORICAL-WEEKLY-LIQUIDITY-LEDGER-BUILD-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL_CONTRACT_PATH = Path("GOVERNANCE/BEPD-02-REAL-HISTORICAL-LEDGER-BUILD-IMPLEMENTATION-CONTRACT-V0.1.json")
READINESS_CONTRACT_PATH = Path("GOVERNANCE/BEPD-01D-HISTORICAL-EXTENSION-READINESS-CONTRACT-V0.1.md")
LEDGER_SCHEMA_PATH = Path("GOVERNANCE/BEPD-01D-HISTORICAL-LEDGER-SCHEMA-V0.1.json")
PRE_SCAN_BREAKER_CONTRACT_PATH = Path("GOVERNANCE/BEPD-01D-FROZEN-PRE-SCAN-BREAKER-CONTRACT-V0.1.json")
PRE_SCAN_BREAKER_PATH = Path("breakers/bepd_01d_historical_extension_readiness_breaker_v0_1.py")
BEPD01C_ENGINE_PATH = Path("tools/bepd_01_weekly_liquidity_engine.py")
SELF_PATH = Path("tools/bepd_02_historical_weekly_liquidity_ledger_build_v0_1.py")

EXPECTED_BLOBS = {
    AUTH_PATH: "6b035f6f3a102d148d61a570b925ed3f01f79fa7",
    IMPL_CONTRACT_PATH: "d63821bf71a1473729dc1cb190f542af41ebd2a2",
    READINESS_CONTRACT_PATH: "a508fbaaa7468d3fd7a17991e48b9b207e274245",
    LEDGER_SCHEMA_PATH: "85f5cdda60397fce59efc1e5d36c1128cf9cc185",
    PRE_SCAN_BREAKER_CONTRACT_PATH: "c2bf489b4991931d940d273d45856c308d0c99c9",
    PRE_SCAN_BREAKER_PATH: "e8e0375604511765ce796f93354a2eaf55822b45",
    BEPD01C_ENGINE_PATH: "050c96049f720757231136386719a40dd5653bbe",
}

AP0_DATASET_ID = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
LEDGER_SCHEMA_VERSION = "ATDS_BEPD_01D_HISTORICAL_LEDGER_SCHEMA_V0_1"
OUTPUT_SUBDIR = Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1")

NY = ZoneInfo("America/New_York")
UTC = timezone.utc


class BuildFailure(RuntimeError):
    pass


def fail(code: str) -> None:
    raise BuildFailure(code)


def git_text(root: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if cp.returncode != 0:
        raise BuildFailure(f"GIT_COMMAND_FAILED:{' '.join(args)}:{cp.stderr.strip()}")
    return cp.stdout.strip()


def git_blob(root: Path, rel: Path) -> str:
    return git_text(root, "rev-parse", f"HEAD:{rel.as_posix()}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def iso_utc_from_ms(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=UTC).isoformat()


def iso_utc(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat()


def file_binding_digest(bindings: list[tuple[str, str]]) -> str:
    raw = "\n".join(f"{path}:{sha}" for path, sha in sorted(bindings)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_git_bindings(root: Path) -> dict[str, str]:
    actual = {}
    for rel, expected in EXPECTED_BLOBS.items():
        got = git_blob(root, rel)
        if got != expected:
            fail(f"GIT_BINDING_MISMATCH:{rel.as_posix()}:{got}:{expected}")
        actual[rel.as_posix()] = got
    return actual


def verify_ap0(ap0_root: Path) -> tuple[dict[str, Any], bytes]:
    manifest_path = ap0_root / "AP0-MANIFEST.json"
    if not manifest_path.is_file():
        fail("AP0_MANIFEST_MISSING")
    manifest_bytes = manifest_path.read_bytes()
    got_manifest_sha = sha256_bytes(manifest_bytes)
    if got_manifest_sha != AP0_MANIFEST_SHA256:
        fail(f"AP0_MANIFEST_SHA256_MISMATCH:{got_manifest_sha}")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if manifest.get("output_identity") != AP0_DATASET_ID:
        fail(f"AP0_DATASET_ID_MISMATCH:{manifest.get('output_identity')}")
    files = manifest.get("files", [])
    if len(files) != 61:
        fail(f"AP0_FILE_COUNT_MISMATCH:{len(files)}")
    for item in files:
        p = ap0_root / item["relative_path"]
        if not p.is_file():
            fail(f"AP0_FILE_MISSING:{item['relative_path']}")
        got = sha256_file(p)
        if got != item["sha256"]:
            fail(f"AP0_FILE_SHA256_MISMATCH:{item['relative_path']}:{got}:{item['sha256']}")
    return manifest, manifest_bytes


def load_event_evaluator(root: Path):
    target = root / BEPD01C_ENGINE_PATH
    spec = importlib.util.spec_from_file_location("bepd_01c_engine", target)
    if spec is None or spec.loader is None:
        fail("BEPD01C_ENGINE_IMPORT_SPEC_FAILURE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "evaluate_level_event"):
        fail("BEPD01C_EVALUATOR_MISSING")
    if getattr(module, "MID_IS_EXECUTION_PRICE", None) is not False:
        fail("BEPD01C_EXECUTION_PRICE_AUTHORITY_DRIFT")
    if getattr(module, "FIVE_YEAR_SCAN_AUTHORIZED", None) is not False:
        fail("BEPD01C_FIVE_YEAR_AUTHORITY_DRIFT")
    return module.evaluate_level_event


def timezone_runtime_identity() -> dict[str, Any]:
    try:
        tzdata_version = importlib.metadata.version("tzdata")
    except importlib.metadata.PackageNotFoundError:
        tzdata_version = None
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "zoneinfo_key": "America/New_York",
        "tzdata_package_version": tzdata_version,
    }


def generate_complete_weeks(first_tick_utc: datetime, last_tick_utc: datetime) -> list[dict[str, Any]]:
    local_first = first_tick_utc.astimezone(NY)
    days_to_sunday = (6 - local_first.weekday()) % 7
    candidate_date = local_first.date() + timedelta(days=days_to_sunday)
    candidate = datetime.combine(candidate_date, time(18, 0), tzinfo=NY)
    if candidate.astimezone(UTC) < first_tick_utc:
        candidate += timedelta(days=7)

    weeks = []
    start = candidate
    while True:
        end = start + timedelta(days=7)
        if end.astimezone(UTC) > last_tick_utc:
            break
        week_id = (start.date() + timedelta(days=1)).isoformat()
        weeks.append(
            {
                "week_id": week_id,
                "start_ny": start.isoformat(),
                "end_ny": end.isoformat(),
                "start_utc": start.astimezone(UTC),
                "end_utc": end.astimezone(UTC),
                "ny_utc_offset_at_start": start.strftime("%z"),
            }
        )
        start = end
    if not weeks:
        fail("NO_COMPLETE_WEEKS")
    return weeks


def load_ap0_frame(ap0_root: Path, manifest: dict[str, Any]) -> tuple[pd.DataFrame, dict[int, tuple[str, str]]]:
    columns = ["minute_start_ms_utc", "mid_high", "mid_low", "mid_close"]
    frames = []
    file_map: dict[int, tuple[str, str]] = {}
    for idx, item in enumerate(manifest["files"]):
        p = ap0_root / item["relative_path"]
        frame = pq.read_table(p, columns=columns).to_pandas()
        frame["source_file_idx"] = idx
        frames.append(frame)
        file_map[idx] = (item["relative_path"], item["sha256"])
    df = pd.concat(frames, ignore_index=True)
    if df.empty:
        fail("AP0_EMPTY")
    if df["minute_start_ms_utc"].duplicated().any():
        dup = int(df.loc[df["minute_start_ms_utc"].duplicated(), "minute_start_ms_utc"].iloc[0])
        fail(f"DUPLICATE_AP0_MINUTE:{dup}")
    if df[["mid_high", "mid_low", "mid_close"]].isna().any().any():
        fail("AP0_NAN_PRICE")
    df = df.sort_values("minute_start_ms_utc").reset_index(drop=True)
    if not df["minute_start_ms_utc"].is_monotonic_increasing:
        fail("AP0_TIME_NOT_MONOTONIC")
    return df, file_map


def gap_stats(ms_values: pd.Series) -> tuple[int, int | None]:
    values = ms_values.astype("int64").to_numpy()
    if len(values) < 2:
        return 0, None
    diffs = values[1:] - values[:-1]
    gap_count = int((diffs > 60_000).sum())
    return gap_count, int(diffs.max())


def week_file_bindings(g: pd.DataFrame, file_map: dict[int, tuple[str, str]]) -> list[tuple[str, str]]:
    ids = sorted(int(x) for x in g["source_file_idx"].unique())
    return [file_map[i] for i in ids]


def build_week_surface(g: pd.DataFrame, week: dict[str, Any], file_map: dict[int, tuple[str, str]]) -> dict[str, Any]:
    if g.empty:
        fail(f"COMPLETE_WEEK_HAS_NO_OBSERVATIONS:{week['week_id']}")

    high = float(g["mid_high"].max())
    low = float(g["mid_low"].min())
    high_rows = g[g["mid_high"] == high]
    low_rows = g[g["mid_low"] == low]

    if len(high_rows) != 1:
        fail(f"FAIL_CLOSED_EXTREME_TIME_TIE:HIGH:{week['week_id']}:{len(high_rows)}:{high}")
    if len(low_rows) != 1:
        fail(f"FAIL_CLOSED_EXTREME_TIME_TIE:LOW:{week['week_id']}:{len(low_rows)}:{low}")

    gap_count, max_gap_ms = gap_stats(g["minute_start_ms_utc"])
    bindings = week_file_bindings(g, file_map)
    return {
        "week_id": week["week_id"],
        "start_utc": iso_utc(week["start_utc"]),
        "end_utc": iso_utc(week["end_utc"]),
        "start_ny": week["start_ny"],
        "end_ny": week["end_ny"],
        "ny_utc_offset_at_start": week["ny_utc_offset_at_start"],
        "high": high,
        "high_time_utc": iso_utc_from_ms(int(high_rows.iloc[0]["minute_start_ms_utc"])),
        "low": low,
        "low_time_utc": iso_utc_from_ms(int(low_rows.iloc[0]["minute_start_ms_utc"])),
        "close": float(g.iloc[-1]["mid_close"]),
        "gap_count_gt60s": gap_count,
        "max_gap_ms": max_gap_ms,
        "file_binding_digest": file_binding_digest(bindings),
        "file_bindings": bindings,
        "rows": int(len(g)),
    }


def qualified_h1_bars(g: pd.DataFrame) -> list[dict[str, Any]]:
    z = g[["minute_start_ms_utc", "mid_close"]].copy()
    z["bucket_ms"] = (z["minute_start_ms_utc"].astype("int64") // 3_600_000) * 3_600_000
    out: list[dict[str, Any]] = []
    for bucket_ms, x in z.groupby("bucket_ms", sort=True):
        x = x.sort_values("minute_start_ms_utc")
        terminal_ms = int(bucket_ms) + 59 * 60_000
        terminal = x[x["minute_start_ms_utc"] == terminal_ms]
        if len(terminal) > 1:
            fail(f"DUPLICATE_H1_TERMINAL_MINUTE:{terminal_ms}")
        if len(terminal) == 0:
            continue
        gap_count, _ = gap_stats(x["minute_start_ms_utc"])
        out.append(
            {
                "start": iso_utc_from_ms(int(bucket_ms)),
                "terminal_time": iso_utc_from_ms(terminal_ms),
                "close": float(terminal.iloc[0]["mid_close"]),
                "internal_gap_count": gap_count,
            }
        )
    return out


def build_file_fields(schema: dict[str, Any], ledger: str) -> list[str]:
    return [x["name"] for x in schema["primary_ledgers"][ledger]["fields"]]


def serialize_row(row: dict[str, Any], fields: list[str]) -> str:
    if set(row) != set(fields):
        missing = sorted(set(fields) - set(row))
        extra = sorted(set(row) - set(fields))
        fail(f"SCHEMA_FIELD_MISMATCH:missing={missing}:extra={extra}")
    ordered = {name: row[name] for name in fields}
    return json.dumps(ordered, ensure_ascii=False, separators=(",", ":"))


def write_jsonl(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(serialize_row(row, fields) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--ap0-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    ap0_root = args.ap0_root.resolve()
    output_dir = (args.output_dir or (root / OUTPUT_SUBDIR)).resolve()

    try:
        verify_git_bindings(root)
        self_blob = git_blob(root, SELF_PATH)
        head = git_text(root, "rev-parse", "HEAD")
        tree = git_text(root, "rev-parse", "HEAD^{tree}")

        manifest, _ = verify_ap0(ap0_root)
        schema = json.loads((root / LEDGER_SCHEMA_PATH).read_text(encoding="utf-8"))
        impl_contract = json.loads((root / IMPL_CONTRACT_PATH).read_text(encoding="utf-8"))

        if output_dir.exists():
            if any(output_dir.iterdir()):
                fail(f"OUTPUT_DIR_NOT_EMPTY:{output_dir}")
        else:
            output_dir.mkdir(parents=True, exist_ok=False)

        evaluator = load_event_evaluator(root)

        coverage = manifest["coverage"]
        first_tick_utc = datetime.fromisoformat(coverage["first_source_tick_utc"])
        last_tick_utc = datetime.fromisoformat(coverage["last_source_tick_utc"])
        weeks = generate_complete_weeks(first_tick_utc, last_tick_utc)

        df, file_map = load_ap0_frame(ap0_root, manifest)

        week_surfaces: list[dict[str, Any]] = []
        week_frames: list[pd.DataFrame] = []
        for week in weeks:
            start_ms = int(week["start_utc"].timestamp() * 1000)
            end_ms = int(week["end_utc"].timestamp() * 1000)
            g = df[
                (df["minute_start_ms_utc"] >= start_ms)
                & (df["minute_start_ms_utc"] < end_ms)
            ].copy()
            surface = build_week_surface(g, week, file_map)
            week_surfaces.append(surface)
            week_frames.append(g)

        run_payload = {
            "repository": REPOSITORY,
            "branch": BRANCH,
            "executed_head": head,
            "executed_tree": tree,
            "dataset_id": AP0_DATASET_ID,
            "ap0_manifest_sha256": AP0_MANIFEST_SHA256,
            "bepd01c_engine_blob": EXPECTED_BLOBS[BEPD01C_ENGINE_PATH],
            "bepd01d_readiness_contract_blob": EXPECTED_BLOBS[READINESS_CONTRACT_PATH],
            "bepd01d_ledger_schema_blob": EXPECTED_BLOBS[LEDGER_SCHEMA_PATH],
            "bepd01d_breaker_contract_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_CONTRACT_PATH],
            "bepd01d_breaker_executable_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_PATH],
            "bepd02_build_implementation_blob": self_blob,
        }
        run_id = canonical_hash(run_payload)

        level_fields = build_file_fields(schema, "LEVEL_LEDGER")
        event_fields = build_file_fields(schema, "EVENT_LEDGER")

        level_rows: list[dict[str, Any]] = []
        level_by_id: dict[str, dict[str, Any]] = {}
        level_meta: dict[str, dict[str, Any]] = {}
        event_rows: list[dict[str, Any]] = []
        opportunity_rows: list[dict[str, Any]] = []
        active_ids: list[str] = []

        def make_level(surface: dict[str, Any], side: str, source_index: int) -> str:
            level_id = canonical_hash(
                {
                    "dataset_id": AP0_DATASET_ID,
                    "ledger_schema_blob": EXPECTED_BLOBS[LEDGER_SCHEMA_PATH],
                    "source_week_id": surface["week_id"],
                    "side": side,
                }
            )
            if level_id in level_by_id:
                fail(f"DUPLICATE_LEVEL_ID:{level_id}")
            price = surface["high"] if side == "HIGH" else surface["low"]
            observed_at = surface["high_time_utc"] if side == "HIGH" else surface["low_time_utc"]
            row = {
                "schema_version": LEDGER_SCHEMA_VERSION,
                "run_id": run_id,
                "dataset_id": AP0_DATASET_ID,
                "dataset_manifest_sha256": AP0_MANIFEST_SHA256,
                "level_id": level_id,
                "source_week_id": surface["week_id"],
                "source_week_start_utc": surface["start_utc"],
                "source_week_end_utc": surface["end_utc"],
                "side": side,
                "level_price_mid": price,
                "level_observed_at_utc": observed_at,
                "causal_available_from_utc": surface["end_utc"],
                "source_week_file_binding_digest": surface["file_binding_digest"],
                "source_week_gap_count_gt60s": surface["gap_count_gt60s"],
                "source_week_max_gap_ms": surface["max_gap_ms"],
                "source_week_quality_state": "COMPLETE_CORPUS_WEEK_OBSERVED_SURFACE",
                "universe": "CORPUS_BORN_WEEKLY_LEVEL",
                "terminal_state": "ACTIVE_RIGHT_CENSORED",
                "consumed_event_id": None,
                "consumed_target_week_id": None,
                "consumed_at_h1_close_utc": None,
                "age_weeks_at_consumption": None,
                "right_censored_at_utc": None,
                "engine_blob": EXPECTED_BLOBS[BEPD01C_ENGINE_PATH],
                "contract_blob": EXPECTED_BLOBS[READINESS_CONTRACT_PATH],
                "breaker_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_PATH],
            }
            level_rows.append(row)
            level_by_id[level_id] = row
            level_meta[level_id] = {"source_index": source_index}
            return level_id

        for index, surface in enumerate(week_surfaces):
            if index > 0:
                active_at_start = list(active_ids)
                active_count = len(active_at_start)
                h1 = qualified_h1_bars(week_frames[index])
                taken: dict[str, dict[str, Any]] = {}

                for level_id in active_at_start:
                    level = level_by_id[level_id]
                    result = evaluator(
                        level["side"],
                        float(level["level_price_mid"]),
                        h1,
                        float(surface["close"]),
                    )
                    if not result["taken"]:
                        continue

                    take_index = int(result["take_index"])
                    take_bar = h1[take_index]
                    reintegration_index = result["reintegration_index"]
                    reintegration_bar = (
                        h1[int(reintegration_index)]
                        if reintegration_index is not None
                        else None
                    )
                    event_id = canonical_hash(
                        {
                            "level_id": level_id,
                            "take_h1_close_utc": take_bar["terminal_time"],
                        }
                    )
                    if any(x["event_id"] == event_id for x in event_rows):
                        fail(f"DUPLICATE_EVENT_ID:{event_id}")

                    taken[level_id] = {
                        "event_id": event_id,
                        "take_bar": take_bar,
                        "reintegration_bar": reintegration_bar,
                        "result": result,
                    }

                cluster_id = (
                    canonical_hash(
                        {
                            "dataset_id": AP0_DATASET_ID,
                            "ledger_schema_blob": EXPECTED_BLOBS[LEDGER_SCHEMA_PATH],
                            "target_week_id": surface["week_id"],
                        }
                    )
                    if taken
                    else None
                )
                cluster_count = len(taken)

                for level_id in active_at_start:
                    info = taken.get(level_id)
                    opportunity_rows.append(
                        {
                            "run_id": run_id,
                            "level_id": level_id,
                            "target_week_id": surface["week_id"],
                            "dependence_key": surface["week_id"],
                            "side": level_by_id[level_id]["side"],
                            "level_age_weeks": index - level_meta[level_id]["source_index"],
                            "swept_this_week": info is not None,
                            "event_id": info["event_id"] if info is not None else None,
                            "active_level_count_at_target_week_start": active_count,
                        }
                    )

                for level_id, info in taken.items():
                    level = level_by_id[level_id]
                    take_bar = info["take_bar"]
                    reintegration_bar = info["reintegration_bar"]
                    result = info["result"]
                    age = index - level_meta[level_id]["source_index"]

                    event = {
                        "schema_version": LEDGER_SCHEMA_VERSION,
                        "run_id": run_id,
                        "dataset_id": AP0_DATASET_ID,
                        "dataset_manifest_sha256": AP0_MANIFEST_SHA256,
                        "event_id": info["event_id"],
                        "sweep_cluster_id": cluster_id,
                        "level_id": level_id,
                        "source_week_id": level["source_week_id"],
                        "target_week_id": surface["week_id"],
                        "side": level["side"],
                        "level_price_mid": level["level_price_mid"],
                        "level_age_weeks": age,
                        "active_level_count_at_target_week_start": active_count,
                        "cluster_consumed_level_count": cluster_count,
                        "take_h1_bucket_start_utc": take_bar["start"],
                        "take_h1_close_utc": take_bar["terminal_time"],
                        "take_h1_close_mid": take_bar["close"],
                        "take_h1_terminal_minute_present": True,
                        "take_h1_internal_gap_count": take_bar["internal_gap_count"],
                        "reintegration_h1_bucket_start_utc": (
                            reintegration_bar["start"] if reintegration_bar is not None else None
                        ),
                        "reintegration_h1_close_utc": (
                            reintegration_bar["terminal_time"] if reintegration_bar is not None else None
                        ),
                        "reintegration_h1_close_mid": (
                            reintegration_bar["close"] if reintegration_bar is not None else None
                        ),
                        "reintegration_h1_internal_gap_count": (
                            reintegration_bar["internal_gap_count"] if reintegration_bar is not None else None
                        ),
                        "same_week_reintegration": reintegration_bar is not None,
                        "target_week_close_mid": surface["close"],
                        "close_displacement": float(result["close_displacement"]),
                        "target_week_file_binding_digest": surface["file_binding_digest"],
                        "target_week_gap_count_gt60s": surface["gap_count_gt60s"],
                        "target_week_max_gap_ms": surface["max_gap_ms"],
                        "holiday_tag": None,
                        "gap_cause": "UNKNOWN",
                        "engine_blob": EXPECTED_BLOBS[BEPD01C_ENGINE_PATH],
                        "contract_blob": EXPECTED_BLOBS[READINESS_CONTRACT_PATH],
                        "breaker_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_PATH],
                    }
                    event_rows.append(event)

                    level["terminal_state"] = "CONSUMED"
                    level["consumed_event_id"] = info["event_id"]
                    level["consumed_target_week_id"] = surface["week_id"]
                    level["consumed_at_h1_close_utc"] = take_bar["terminal_time"]
                    level["age_weeks_at_consumption"] = age
                    level["right_censored_at_utc"] = None

                active_ids = [x for x in active_ids if x not in taken]

            high_id = make_level(surface, "HIGH", index)
            low_id = make_level(surface, "LOW", index)
            active_ids.extend([high_id, low_id])

        horizon_utc = week_surfaces[-1]["end_utc"]
        for level_id in active_ids:
            level_by_id[level_id]["terminal_state"] = "ACTIVE_RIGHT_CENSORED"
            level_by_id[level_id]["right_censored_at_utc"] = horizon_utc

        level_rows.sort(key=lambda x: (x["source_week_id"], x["side"]))
        event_rows.sort(
            key=lambda x: (
                x["target_week_id"],
                x["take_h1_close_utc"],
                x["side"],
                x["source_week_id"],
                x["level_id"],
            )
        )
        opportunity_rows.sort(key=lambda x: (x["target_week_id"], x["level_id"]))

        if len({x["level_id"] for x in level_rows}) != len(level_rows):
            fail("LEVEL_ID_NOT_UNIQUE")
        if len({x["event_id"] for x in event_rows}) != len(event_rows):
            fail("EVENT_ID_NOT_UNIQUE")
        if len({(x["level_id"], x["target_week_id"]) for x in opportunity_rows}) != len(opportunity_rows):
            fail("OPPORTUNITY_KEY_NOT_UNIQUE")

        event_by_level = {x["level_id"]: x for x in event_rows}
        for level in level_rows:
            if level["terminal_state"] == "CONSUMED":
                ev = event_by_level.get(level["level_id"])
                if ev is None or ev["event_id"] != level["consumed_event_id"]:
                    fail(f"CONSUMED_LEVEL_EVENT_FK_FAILURE:{level['level_id']}")
            else:
                if level["level_id"] in event_by_level:
                    fail(f"RIGHT_CENSORED_LEVEL_HAS_EVENT:{level['level_id']}")

        for opp in opportunity_rows:
            level = level_by_id[opp["level_id"]]
            if opp["target_week_id"] <= level["source_week_id"]:
                fail(f"SELF_OR_PRE_BIRTH_OPPORTUNITY:{opp['level_id']}:{opp['target_week_id']}")
            if opp["swept_this_week"] != (opp["event_id"] is not None):
                fail(f"OPPORTUNITY_EVENT_FLAG_MISMATCH:{opp['level_id']}:{opp['target_week_id']}")
            if opp["event_id"] is not None:
                ev = event_by_level[opp["level_id"]]
                if ev["event_id"] != opp["event_id"] or ev["target_week_id"] != opp["target_week_id"]:
                    fail(f"OPPORTUNITY_EVENT_FK_FAILURE:{opp['level_id']}:{opp['target_week_id']}")

        level_path = output_dir / "LEVEL_LEDGER.jsonl"
        event_path = output_dir / "EVENT_LEDGER.jsonl"
        opp_path = output_dir / "LEVEL_WEEK_OPPORTUNITY.jsonl"

        write_jsonl(level_path, level_rows, level_fields)
        write_jsonl(event_path, event_rows, event_fields)

        opp_fields = [
            "run_id",
            "level_id",
            "target_week_id",
            "dependence_key",
            "side",
            "level_age_weeks",
            "swept_this_week",
            "event_id",
            "active_level_count_at_target_week_start",
        ]
        write_jsonl(opp_path, opportunity_rows, opp_fields)

        selected_files = [
            {
                "relative_path": x["relative_path"],
                "sha256": x["sha256"],
                "rows": x["rows"],
                "size_bytes": x["size_bytes"],
            }
            for x in manifest["files"]
        ]

        output_files = []
        for p, rows in (
            (level_path, level_rows),
            (event_path, event_rows),
            (opp_path, opportunity_rows),
        ):
            output_files.append(
                {
                    "relative_path": p.relative_to(root).as_posix(),
                    "sha256": sha256_file(p),
                    "rows": len(rows),
                    "size_bytes": p.stat().st_size,
                }
            )

        run_manifest = {
            "schema": "ATDS_BEPD_02_REAL_HISTORICAL_LEDGER_RUN_MANIFEST_V0_1",
            "run_id": run_id,
            "repository": REPOSITORY,
            "branch": BRANCH,
            "head": head,
            "tree": tree,
            "dataset_id": AP0_DATASET_ID,
            "dataset_manifest_sha256": AP0_MANIFEST_SHA256,
            "selected_ap0_files": selected_files,
            "timezone_database_runtime_identity": timezone_runtime_identity(),
            "weekly_boundary_timezone": "America/New_York",
            "weekly_boundary_local_time": "Sunday 18:00:00",
            "h1_bucket_timezone": "UTC",
            "h1_terminal_minute_rule": "HH:59:00 UTC minute must be observed",
            "engine_blob": EXPECTED_BLOBS[BEPD01C_ENGINE_PATH],
            "build_implementation_blob": self_blob,
            "human_authorization_blob": EXPECTED_BLOBS[AUTH_PATH],
            "implementation_contract_blob": EXPECTED_BLOBS[IMPL_CONTRACT_PATH],
            "contract_blob": EXPECTED_BLOBS[READINESS_CONTRACT_PATH],
            "ledger_schema_blob": EXPECTED_BLOBS[LEDGER_SCHEMA_PATH],
            "breaker_contract_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_CONTRACT_PATH],
            "breaker_executable_blob": EXPECTED_BLOBS[PRE_SCAN_BREAKER_PATH],
            "command_or_entrypoint": SELF_PATH.as_posix(),
            "complete_week_count": len(week_surfaces),
            "first_complete_week_id": week_surfaces[0]["week_id"],
            "last_complete_week_id": week_surfaces[-1]["week_id"],
            "right_censor_horizon_utc": horizon_utc,
            "output_files": output_files,
            "forbidden_analytics_executed": False,
        }

        manifest_out = output_dir / "RUN_MANIFEST.json"
        manifest_out.write_text(
            json.dumps(run_manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

        print(
            json.dumps(
                {
                    "status": "BEPD02_RAW_LEDGER_BUILD_COMPLETE",
                    "run_id": run_id,
                    "complete_weeks": len(week_surfaces),
                    "level_rows": len(level_rows),
                    "event_rows": len(event_rows),
                    "opportunity_rows": len(opportunity_rows),
                    "active_right_censored": len(active_ids),
                    "output_dir": str(output_dir),
                    "run_manifest_sha256": sha256_file(manifest_out),
                },
                sort_keys=True,
            )
        )
        return 0

    except BuildFailure as exc:
        print(f"BEPD02_BUILD_FAIL:{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow.parquet as pq

AP0_DATASET_ID = "USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_BUILD_HEAD = "79fc7b248118d0b87cb96f51b544f5745738b9e3"
EXPECTED_BUILD_TREE = "007c553e2ff073f3bdd1d06f65f024764f46d4ec"
EXPECTED_BUILDER_BLOB = "99279c2bf252105744a18eb721f2fefe9ef883e8"
EXPECTED_ENGINE_BLOB = "050c96049f720757231136386719a40dd5653bbe"
EXPECTED_READINESS_CONTRACT_BLOB = "a508fbaaa7468d3fd7a17991e48b9b207e274245"
EXPECTED_LEDGER_SCHEMA_BLOB = "85f5cdda60397fce59efc1e5d36c1128cf9cc185"
EXPECTED_PRE_SCAN_BREAKER_CONTRACT_BLOB = "c2bf489b4991931d940d273d45856c308d0c99c9"
EXPECTED_PRE_SCAN_BREAKER_BLOB = "e8e0375604511765ce796f93354a2eaf55822b45"
EXPECTED_AUTH_BLOB = "6b035f6f3a102d148d61a570b925ed3f01f79fa7"
EXPECTED_IMPL_CONTRACT_BLOB = "d63821bf71a1473729dc1cb190f542af41ebd2a2"

NY = ZoneInfo("America/New_York")
UTC = timezone.utc


class BreakerFailure(AssertionError):
    pass


def fail(code: str) -> None:
    raise BreakerFailure(code)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_binding_digest(bindings: list[tuple[str, str]]) -> str:
    raw = "\n".join(f"{p}:{s}" for p, s in sorted(bindings)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.endswith("\n"):
                fail(f"JSONL_LINE_NOT_LF_TERMINATED:{path.name}:{number}")
            rows.append(json.loads(line))
    return rows


def exact_fields(rows: list[dict[str, Any]], expected: list[str], label: str) -> None:
    e = set(expected)
    for i, row in enumerate(rows):
        if set(row) != e:
            fail(f"{label}_FIELD_SET_MISMATCH:{i}")


def parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        fail(f"NAIVE_TIMESTAMP:{value}")
    return dt.astimezone(UTC)


def gap_stats(ms_values: pd.Series) -> tuple[int, int | None]:
    values = ms_values.astype("int64").to_numpy()
    if len(values) < 2:
        return 0, None
    diffs = values[1:] - values[:-1]
    return int((diffs > 60_000).sum()), int(diffs.max())


def load_ap0(ap0_root: Path) -> tuple[dict[str, Any], pd.DataFrame, dict[int, tuple[str, str]]]:
    mp = ap0_root / "AP0-MANIFEST.json"
    if not mp.is_file() or sha256_file(mp) != AP0_MANIFEST_SHA256:
        fail("AP0_MANIFEST_IDENTITY")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    if manifest.get("output_identity") != AP0_DATASET_ID:
        fail("AP0_DATASET_ID")
    if len(manifest.get("files", [])) != 61:
        fail("AP0_FILE_COUNT")

    frames = []
    fmap: dict[int, tuple[str, str]] = {}
    cols = ["minute_start_ms_utc", "mid_high", "mid_low", "mid_close"]
    for idx, item in enumerate(manifest["files"]):
        p = ap0_root / item["relative_path"]
        if not p.is_file():
            fail(f"AP0_FILE_MISSING:{item['relative_path']}")
        if sha256_file(p) != item["sha256"]:
            fail(f"AP0_FILE_DIGEST:{item['relative_path']}")
        frame = pq.read_table(p, columns=cols).to_pandas()
        frame["source_file_idx"] = idx
        frames.append(frame)
        fmap[idx] = (item["relative_path"], item["sha256"])

    df = pd.concat(frames, ignore_index=True).sort_values("minute_start_ms_utc").reset_index(drop=True)
    if df["minute_start_ms_utc"].duplicated().any():
        fail("AP0_DUPLICATE_MINUTE")
    return manifest, df, fmap


def independent_week_surface(
    df: pd.DataFrame,
    fmap: dict[int, tuple[str, str]],
    start_utc: datetime,
    end_utc: datetime,
) -> tuple[dict[str, Any], pd.DataFrame]:
    sm = int(start_utc.timestamp() * 1000)
    em = int(end_utc.timestamp() * 1000)
    g = df[(df["minute_start_ms_utc"] >= sm) & (df["minute_start_ms_utc"] < em)].copy()
    if g.empty:
        fail(f"EMPTY_WEEK:{start_utc.isoformat()}")
    high = float(g["mid_high"].max())
    low = float(g["mid_low"].min())
    hi = g[g["mid_high"] == high]
    lo = g[g["mid_low"] == low]
    if len(hi) != 1 or len(lo) != 1:
        fail(f"EXTREME_TIE_REAPPEARED:{start_utc.isoformat()}:{len(hi)}:{len(lo)}")
    gaps, max_gap = gap_stats(g["minute_start_ms_utc"])
    bindings = [fmap[int(i)] for i in sorted(g["source_file_idx"].unique())]
    return {
        "high": high,
        "low": low,
        "high_time": datetime.fromtimestamp(int(hi.iloc[0]["minute_start_ms_utc"]) / 1000, tz=UTC).isoformat(),
        "low_time": datetime.fromtimestamp(int(lo.iloc[0]["minute_start_ms_utc"]) / 1000, tz=UTC).isoformat(),
        "close": float(g.iloc[-1]["mid_close"]),
        "gaps": gaps,
        "max_gap": max_gap,
        "file_digest": file_binding_digest(bindings),
    }, g


def independent_h1(g: pd.DataFrame) -> list[dict[str, Any]]:
    z = g[["minute_start_ms_utc", "mid_close"]].copy()
    z["bucket_ms"] = (z["minute_start_ms_utc"].astype("int64") // 3_600_000) * 3_600_000
    out = []
    for bucket, x in z.groupby("bucket_ms", sort=True):
        x = x.sort_values("minute_start_ms_utc")
        terminal_ms = int(bucket) + 59 * 60_000
        terminal = x[x["minute_start_ms_utc"] == terminal_ms]
        if len(terminal) > 1:
            fail(f"DUPLICATE_TERMINAL:{terminal_ms}")
        if len(terminal) == 0:
            continue
        gaps, _ = gap_stats(x["minute_start_ms_utc"])
        out.append({
            "start": datetime.fromtimestamp(int(bucket) / 1000, tz=UTC).isoformat(),
            "terminal": datetime.fromtimestamp(terminal_ms / 1000, tz=UTC).isoformat(),
            "close": float(terminal.iloc[0]["mid_close"]),
            "gaps": gaps,
        })
    return out


def first_take(side: str, level: float, bars: list[dict[str, Any]]) -> int | None:
    for i, bar in enumerate(bars):
        c = float(bar["close"])
        if (side == "HIGH" and c > level) or (side == "LOW" and c < level):
            return i
    return None


def first_reintegration(side: str, level: float, bars: list[dict[str, Any]], take: int) -> int | None:
    for i in range(take + 1, len(bars)):
        c = float(bars[i]["close"])
        if (side == "HIGH" and c < level) or (side == "LOW" and c > level):
            return i
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--ap0-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    ap0_root = args.ap0_root.resolve()
    out = args.output_dir.resolve()

    try:
        expected_names = {"LEVEL_LEDGER.jsonl", "EVENT_LEDGER.jsonl", "LEVEL_WEEK_OPPORTUNITY.jsonl", "RUN_MANIFEST.json"}
        if not out.is_dir() or {p.name for p in out.iterdir()} != expected_names:
            fail("OUTPUT_SURFACE_MISMATCH")

        manifest_path = out / "RUN_MANIFEST.json"
        run = json.loads(manifest_path.read_text(encoding="utf-8"))
        if run.get("schema") != "ATDS_BEPD_02_REAL_HISTORICAL_LEDGER_RUN_MANIFEST_V0_1":
            fail("RUN_MANIFEST_SCHEMA")
        checks = {
            "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
            "branch": "integration/system-v1",
            "head": EXPECTED_BUILD_HEAD,
            "tree": EXPECTED_BUILD_TREE,
            "dataset_id": AP0_DATASET_ID,
            "dataset_manifest_sha256": AP0_MANIFEST_SHA256,
            "engine_blob": EXPECTED_ENGINE_BLOB,
            "build_implementation_blob": EXPECTED_BUILDER_BLOB,
            "human_authorization_blob": EXPECTED_AUTH_BLOB,
            "implementation_contract_blob": EXPECTED_IMPL_CONTRACT_BLOB,
            "contract_blob": EXPECTED_READINESS_CONTRACT_BLOB,
            "ledger_schema_blob": EXPECTED_LEDGER_SCHEMA_BLOB,
            "breaker_contract_blob": EXPECTED_PRE_SCAN_BREAKER_CONTRACT_BLOB,
            "breaker_executable_blob": EXPECTED_PRE_SCAN_BREAKER_BLOB,
            "forbidden_analytics_executed": False,
        }
        for key, expected in checks.items():
            if run.get(key) != expected:
                fail(f"RUN_MANIFEST_BINDING:{key}:{run.get(key)}:{expected}")

        run_payload = {
            "repository": run["repository"],
            "branch": run["branch"],
            "executed_head": run["head"],
            "executed_tree": run["tree"],
            "dataset_id": run["dataset_id"],
            "ap0_manifest_sha256": run["dataset_manifest_sha256"],
            "bepd01c_engine_blob": run["engine_blob"],
            "bepd01d_readiness_contract_blob": run["contract_blob"],
            "bepd01d_ledger_schema_blob": run["ledger_schema_blob"],
            "bepd01d_breaker_contract_blob": run["breaker_contract_blob"],
            "bepd01d_breaker_executable_blob": run["breaker_executable_blob"],
            "bepd02_build_implementation_blob": run["build_implementation_blob"],
        }
        if canonical_hash(run_payload) != run["run_id"]:
            fail("RUN_ID_RECOMPUTE_MISMATCH")

        ap0_manifest, df, fmap = load_ap0(ap0_root)
        selected = run.get("selected_ap0_files", [])
        if len(selected) != 61:
            fail("RUN_SELECTED_AP0_COUNT")
        expected_selected = [
            {
                "relative_path": x["relative_path"],
                "sha256": x["sha256"],
                "rows": x["rows"],
                "size_bytes": x["size_bytes"],
            }
            for x in ap0_manifest["files"]
        ]
        if selected != expected_selected:
            fail("RUN_SELECTED_AP0_BINDINGS")

        file_rows = {x["relative_path"]: x for x in run["output_files"]}
        expected_output_paths = {
            "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_LEDGER.jsonl": out / "LEVEL_LEDGER.jsonl",
            "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl": out / "EVENT_LEDGER.jsonl",
            "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl": out / "LEVEL_WEEK_OPPORTUNITY.jsonl",
        }
        if set(file_rows) != set(expected_output_paths):
            fail("RUN_OUTPUT_PATH_SET")
        for rel, path in expected_output_paths.items():
            info = file_rows[rel]
            if sha256_file(path) != info["sha256"] or path.stat().st_size != info["size_bytes"]:
                fail(f"OUTPUT_FILE_IDENTITY:{rel}")

        levels = read_jsonl(out / "LEVEL_LEDGER.jsonl")
        events = read_jsonl(out / "EVENT_LEDGER.jsonl")
        opps = read_jsonl(out / "LEVEL_WEEK_OPPORTUNITY.jsonl")

        for rel, rows in [
            ("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_LEDGER.jsonl", levels),
            ("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl", events),
            ("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl", opps),
        ]:
            if len(rows) != file_rows[rel]["rows"]:
                fail(f"OUTPUT_ROW_COUNT:{rel}")

        schema = json.loads((root / "GOVERNANCE/BEPD-01D-HISTORICAL-LEDGER-SCHEMA-V0.1.json").read_text(encoding="utf-8"))
        level_fields = [x["name"] for x in schema["primary_ledgers"]["LEVEL_LEDGER"]["fields"]]
        event_fields = [x["name"] for x in schema["primary_ledgers"]["EVENT_LEDGER"]["fields"]]
        opp_fields = ["run_id","level_id","target_week_id","dependence_key","side","level_age_weeks","swept_this_week","event_id","active_level_count_at_target_week_start"]
        exact_fields(levels, level_fields, "LEVEL")
        exact_fields(events, event_fields, "EVENT")
        exact_fields(opps, opp_fields, "OPPORTUNITY")

        run_id = run["run_id"]
        if any(x["run_id"] != run_id for x in levels + events + opps):
            fail("RUN_ID_ROW_DRIFT")
        if len({x["level_id"] for x in levels}) != len(levels):
            fail("LEVEL_PK")
        if len({x["event_id"] for x in events}) != len(events):
            fail("EVENT_PK")
        if len({(x["level_id"], x["target_week_id"]) for x in opps}) != len(opps):
            fail("OPPORTUNITY_PK")

        level_by_id = {x["level_id"]: x for x in levels}
        event_by_level = {x["level_id"]: x for x in events}
        opp_by_key = {(x["level_id"], x["target_week_id"]): x for x in opps}

        week_ids = sorted({x["source_week_id"] for x in levels})
        if len(levels) != 2 * len(week_ids):
            fail("TWO_LEVELS_PER_WEEK_COUNT")
        if run["complete_week_count"] != len(week_ids):
            fail("COMPLETE_WEEK_COUNT")
        if run["first_complete_week_id"] != week_ids[0] or run["last_complete_week_id"] != week_ids[-1]:
            fail("COMPLETE_WEEK_ENDPOINTS")
        for a, b in zip(week_ids, week_ids[1:]):
            if (datetime.fromisoformat(b).date() - datetime.fromisoformat(a).date()).days != 7:
                fail(f"WEEK_SEQUENCE_GAP:{a}:{b}")
        week_index = {w: i for i, w in enumerate(week_ids)}

        levels_by_week: dict[str, list[dict[str, Any]]] = {}
        for level in levels:
            levels_by_week.setdefault(level["source_week_id"], []).append(level)
        for week_id, rows in levels_by_week.items():
            if {x["side"] for x in rows} != {"HIGH", "LOW"} or len(rows) != 2:
                fail(f"WEEK_SIDE_SET:{week_id}")

        surface_by_week: dict[str, dict[str, Any]] = {}
        h1_by_week: dict[str, list[dict[str, Any]]] = {}
        for week_id in week_ids:
            level0 = levels_by_week[week_id][0]
            start = parse_utc(level0["source_week_start_utc"])
            end = parse_utc(level0["source_week_end_utc"])
            start_ny = start.astimezone(NY)
            if start_ny.weekday() != 6 or start_ny.hour != 18 or start_ny.minute != 0:
                fail(f"WEEK_BOUNDARY_NY:{week_id}:{start_ny.isoformat()}")
            if (end - start) not in {timedelta(days=7), timedelta(days=7, hours=-1), timedelta(days=7, hours=1)}:
                fail(f"WEEK_DURATION:{week_id}:{end-start}")
            if (start_ny.date() + timedelta(days=1)).isoformat() != week_id:
                fail(f"WEEK_ID_DERIVATION:{week_id}")

            surface, g = independent_week_surface(df, fmap, start, end)
            surface_by_week[week_id] = surface
            h1_by_week[week_id] = independent_h1(g)

            for level in levels_by_week[week_id]:
                if level["causal_available_from_utc"] != level["source_week_end_utc"]:
                    fail(f"CAUSAL_AVAILABILITY:{level['level_id']}")
                if level["source_week_quality_state"] != "COMPLETE_CORPUS_WEEK_OBSERVED_SURFACE":
                    fail(f"SOURCE_WEEK_QUALITY:{level['level_id']}")
                if level["universe"] != "CORPUS_BORN_WEEKLY_LEVEL":
                    fail(f"LEVEL_UNIVERSE:{level['level_id']}")
                if level["engine_blob"] != EXPECTED_ENGINE_BLOB or level["contract_blob"] != EXPECTED_READINESS_CONTRACT_BLOB or level["breaker_blob"] != EXPECTED_PRE_SCAN_BREAKER_BLOB:
                    fail(f"LEVEL_PROVENANCE:{level['level_id']}")
                expected_price = surface["high"] if level["side"] == "HIGH" else surface["low"]
                expected_time = surface["high_time"] if level["side"] == "HIGH" else surface["low_time"]
                if float(level["level_price_mid"]) != float(expected_price) or level["level_observed_at_utc"] != expected_time:
                    fail(f"LEVEL_SURFACE_PARITY:{level['level_id']}")
                if level["source_week_file_binding_digest"] != surface["file_digest"]:
                    fail(f"LEVEL_FILE_DIGEST:{level['level_id']}")
                if level["source_week_gap_count_gt60s"] != surface["gaps"] or level["source_week_max_gap_ms"] != surface["max_gap"]:
                    fail(f"LEVEL_GAP_STATS:{level['level_id']}")

        if len(event_by_level) != len(events):
            fail("MULTIPLE_EVENTS_PER_LEVEL")

        expected_opp_keys = set()
        for level in levels:
            source_i = week_index[level["source_week_id"]]
            if level["terminal_state"] == "CONSUMED":
                if not level["consumed_event_id"] or not level["consumed_target_week_id"] or not level["consumed_at_h1_close_utc"]:
                    fail(f"CONSUMED_NULL_FIELDS:{level['level_id']}")
                if level["right_censored_at_utc"] is not None:
                    fail(f"CONSUMED_RIGHT_CENSOR:{level['level_id']}")
                ev = event_by_level.get(level["level_id"])
                if ev is None or ev["event_id"] != level["consumed_event_id"]:
                    fail(f"CONSUMED_EVENT_FK:{level['level_id']}")
                end_i = week_index[level["consumed_target_week_id"]]
                if level["age_weeks_at_consumption"] != end_i - source_i:
                    fail(f"CONSUMPTION_AGE:{level['level_id']}")
            elif level["terminal_state"] == "ACTIVE_RIGHT_CENSORED":
                if any(level[k] is not None for k in ["consumed_event_id","consumed_target_week_id","consumed_at_h1_close_utc","age_weeks_at_consumption"]):
                    fail(f"RIGHT_CENSOR_CONSUMED_FIELDS:{level['level_id']}")
                if level["right_censored_at_utc"] != run["right_censor_horizon_utc"]:
                    fail(f"RIGHT_CENSOR_HORIZON:{level['level_id']}")
                if level["level_id"] in event_by_level:
                    fail(f"RIGHT_CENSOR_HAS_EVENT:{level['level_id']}")
                end_i = len(week_ids) - 1
            else:
                fail(f"TERMINAL_STATE:{level['level_id']}:{level['terminal_state']}")

            for i in range(source_i + 1, end_i + 1):
                expected_opp_keys.add((level["level_id"], week_ids[i]))

        if set(opp_by_key) != expected_opp_keys:
            missing = list(expected_opp_keys - set(opp_by_key))[:3]
            extra = list(set(opp_by_key) - expected_opp_keys)[:3]
            fail(f"OPPORTUNITY_UNIVERSE:missing={missing}:extra={extra}")

        opps_by_week: dict[str, list[dict[str, Any]]] = {}
        for opp in opps:
            opps_by_week.setdefault(opp["target_week_id"], []).append(opp)
            level = level_by_id.get(opp["level_id"])
            if level is None:
                fail(f"OPPORTUNITY_LEVEL_FK:{opp['level_id']}")
            if opp["dependence_key"] != opp["target_week_id"] or opp["side"] != level["side"]:
                fail(f"OPPORTUNITY_DEPENDENCE_OR_SIDE:{opp['level_id']}:{opp['target_week_id']}")
            expected_age = week_index[opp["target_week_id"]] - week_index[level["source_week_id"]]
            if opp["level_age_weeks"] != expected_age or expected_age <= 0:
                fail(f"OPPORTUNITY_AGE:{opp['level_id']}:{opp['target_week_id']}")

            bars = h1_by_week[opp["target_week_id"]]
            take = first_take(level["side"], float(level["level_price_mid"]), bars)
            should_sweep = take is not None
            if bool(opp["swept_this_week"]) != should_sweep:
                fail(f"OPPORTUNITY_SWEEP_PARITY:{opp['level_id']}:{opp['target_week_id']}")
            if should_sweep:
                ev = event_by_level.get(opp["level_id"])
                if ev is None or ev["target_week_id"] != opp["target_week_id"] or ev["event_id"] != opp["event_id"]:
                    fail(f"OPPORTUNITY_EVENT_PARITY:{opp['level_id']}:{opp['target_week_id']}")
                take_bar = bars[int(take)]
                if ev["take_h1_bucket_start_utc"] != take_bar["start"] or ev["take_h1_close_utc"] != take_bar["terminal"] or float(ev["take_h1_close_mid"]) != float(take_bar["close"]):
                    fail(f"EVENT_FIRST_TAKE_PARITY:{ev['event_id']}")
                if ev["take_h1_internal_gap_count"] != take_bar["gaps"] or ev["take_h1_terminal_minute_present"] is not True:
                    fail(f"EVENT_TAKE_H1_QUALITY:{ev['event_id']}")
                reidx = first_reintegration(level["side"], float(level["level_price_mid"]), bars, int(take))
                if reidx is None:
                    if ev["same_week_reintegration"] is not False or any(ev[k] is not None for k in ["reintegration_h1_bucket_start_utc","reintegration_h1_close_utc","reintegration_h1_close_mid","reintegration_h1_internal_gap_count"]):
                        fail(f"EVENT_NO_REINTEGRATION_PARITY:{ev['event_id']}")
                else:
                    rb = bars[reidx]
                    if ev["same_week_reintegration"] is not True or ev["reintegration_h1_bucket_start_utc"] != rb["start"] or ev["reintegration_h1_close_utc"] != rb["terminal"] or float(ev["reintegration_h1_close_mid"]) != float(rb["close"]) or ev["reintegration_h1_internal_gap_count"] != rb["gaps"]:
                        fail(f"EVENT_REINTEGRATION_PARITY:{ev['event_id']}")

        for week_id, rows in opps_by_week.items():
            count = len(rows)
            if any(x["active_level_count_at_target_week_start"] != count for x in rows):
                fail(f"OPPORTUNITY_ACTIVE_COUNT:{week_id}")

        events_by_week: dict[str, list[dict[str, Any]]] = {}
        for ev in events:
            events_by_week.setdefault(ev["target_week_id"], []).append(ev)
            level = level_by_id.get(ev["level_id"])
            if level is None:
                fail(f"EVENT_LEVEL_FK:{ev['event_id']}")
            if ev["source_week_id"] != level["source_week_id"] or ev["side"] != level["side"] or float(ev["level_price_mid"]) != float(level["level_price_mid"]):
                fail(f"EVENT_LEVEL_PARITY:{ev['event_id']}")
            if ev["dataset_id"] != AP0_DATASET_ID or ev["dataset_manifest_sha256"] != AP0_MANIFEST_SHA256:
                fail(f"EVENT_DATASET_BINDING:{ev['event_id']}")
            if ev["engine_blob"] != EXPECTED_ENGINE_BLOB or ev["contract_blob"] != EXPECTED_READINESS_CONTRACT_BLOB or ev["breaker_blob"] != EXPECTED_PRE_SCAN_BREAKER_BLOB:
                fail(f"EVENT_PROVENANCE:{ev['event_id']}")
            if ev["gap_cause"] != "UNKNOWN":
                fail(f"EVENT_GAP_CAUSE:{ev['event_id']}")
            take_dt = parse_utc(ev["take_h1_close_utc"])
            if take_dt.minute != 59 or take_dt.second != 0:
                fail(f"EVENT_TAKE_TERMINAL:{ev['event_id']}")
            if ev["reintegration_h1_close_utc"] is not None:
                rein = parse_utc(ev["reintegration_h1_close_utc"])
                if rein.minute != 59 or rein.second != 0 or rein <= take_dt:
                    fail(f"EVENT_REINTEGRATION_TERMINAL:{ev['event_id']}")
            surf = surface_by_week[ev["target_week_id"]]
            if float(ev["target_week_close_mid"]) != float(surf["close"]):
                fail(f"EVENT_TARGET_CLOSE:{ev['event_id']}")
            expected_d = (
                float(ev["level_price_mid"]) - float(surf["close"])
                if ev["side"] == "HIGH"
                else float(surf["close"]) - float(ev["level_price_mid"])
            )
            if abs(float(ev["close_displacement"]) - expected_d) > 1e-9:
                fail(f"EVENT_DISPLACEMENT:{ev['event_id']}")
            if ev["target_week_file_binding_digest"] != surf["file_digest"] or ev["target_week_gap_count_gt60s"] != surf["gaps"] or ev["target_week_max_gap_ms"] != surf["max_gap"]:
                fail(f"EVENT_TARGET_PROVENANCE:{ev['event_id']}")
            if ev["active_level_count_at_target_week_start"] != len(opps_by_week[ev["target_week_id"]]):
                fail(f"EVENT_ACTIVE_COUNT:{ev['event_id']}")

        cluster_ids = {}
        for week_id, rows in events_by_week.items():
            ids = {x["sweep_cluster_id"] for x in rows}
            if len(ids) != 1:
                fail(f"CLUSTER_ID_PER_WEEK:{week_id}")
            cid = next(iter(ids))
            if cid in cluster_ids and cluster_ids[cid] != week_id:
                fail(f"CLUSTER_ID_REUSE:{cid}")
            cluster_ids[cid] = week_id
            if any(x["cluster_consumed_level_count"] != len(rows) for x in rows):
                fail(f"CLUSTER_COUNT:{week_id}")

        if run["right_censor_horizon_utc"] != levels_by_week[week_ids[-1]][0]["source_week_end_utc"]:
            fail("RUN_RIGHT_CENSOR_HORIZON")

        print(json.dumps({
            "status":"BEPD02_RAW_LEDGER_QUALIFICATION_PASS",
            "run_id":run_id,
            "level_rows":len(levels),
            "event_rows":len(events),
            "opportunity_rows":len(opps),
            "complete_weeks":len(week_ids),
            "right_censored_levels":sum(1 for x in levels if x["terminal_state"]=="ACTIVE_RIGHT_CENSORED")
        }, sort_keys=True))
        return 0

    except (BreakerFailure, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"BEPD02_RAW_LEDGER_QUALIFICATION_FAIL:{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

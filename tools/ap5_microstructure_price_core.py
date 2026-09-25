#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP4_SHA256 = "c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad"
EXPECTED_AP4_REPO_PATH = Path("reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json")
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
EXPECTED_F2_SPREAD_MIN = 0.000999999996565748
EXPECTED_F2_SPREAD_MAX = 35.66699999999764
EXPECTED_F2_SPREAD_MEAN = 2.1395040593705223
EXPECTED_AP2_MINUTE_RANGE_MEAN_BPS = 4.033115022615127
EXPECTED_AP2_VALID_1M = 1_707_574
EXPECTED_AP2_ABS_RETURN_1M_MEAN_BPS = 2.130371613870453
RECONCILIATION_TOLERANCE = 1e-9
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
NY = ZoneInfo("America/New_York")

REQUIRED_SCHEMA = [
    ("minute_start_ms_utc", "int64"),
    ("first_tick_ms", "int64"),
    ("last_tick_ms", "int64"),
    ("tick_count", "int64"),
    ("segment_id", "int64"),
    ("segment_start", "bool"),
    ("gap_before_ms", "int64"),
    ("mid_open", "double"),
    ("mid_high", "double"),
    ("mid_low", "double"),
    ("mid_close", "double"),
    ("spread_mean", "double"),
    ("spread_min", "double"),
    ("spread_max", "double"),
]
READ_COLUMNS = [
    "minute_start_ms_utc",
    "tick_count",
    "segment_id",
    "segment_start",
    "mid_open",
    "mid_high",
    "mid_low",
    "mid_close",
    "spread_mean",
    "spread_min",
    "spread_max",
]
PCTS_GLOBAL = (10, 25, 50, 75, 90, 95, 99, 99.9)
PCTS_BUCKET = (50, 90, 95, 99)


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        c = os.path.normcase(str(child.resolve(strict=False)))
        p = os.path.normcase(str(parent.resolve(strict=False)))
        return os.path.commonpath([c, p]) == p
    except ValueError:
        return False


def is_reparse_or_symlink(path: Path) -> bool:
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse)


def path_chain_has_reparse_or_symlink(path: Path) -> bool:
    """Reject an existing symlink/reparse at any component before resolve()."""
    absolute = path.absolute()
    parts = absolute.parts
    if not parts:
        return False
    cur = Path(parts[0])
    for part in parts[1:]:
        cur = cur / part
        if os.path.lexists(cur):
            if is_reparse_or_symlink(cur):
                return True
        else:
            break
    return False


def resolve_manifest_member(root: Path, rel: str) -> Path:
    raw = root / Path(rel)
    if path_chain_has_reparse_or_symlink(raw):
        raise RuntimeError(f"AP0 manifest member path contains reparse/symlink: {rel}")
    p = raw.resolve(strict=False)
    if not is_within(p, root) or not p.is_file() or is_reparse_or_symlink(p):
        raise RuntimeError(f"invalid AP0 file path: {rel}")
    return p


def write_json_exclusive(path: Path, payload: dict) -> None:
    raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(raw) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"AP5 JSON exceeds {MAX_OUTPUT_BYTES} bytes")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)


def _pct_key(q: float) -> str:
    return f"p{str(q).replace('.', '_')}"


def distribution(values, percentiles=PCTS_GLOBAL):
    import numpy as np
    x = np.asarray(values, dtype=np.float64)
    x = x[np.isfinite(x)]
    if x.size == 0:
        out = {"count": 0, "mean": None, "min": None, "max": None}
        out.update({_pct_key(q): None for q in percentiles})
        return out
    out = {
        "count": int(x.size),
        "mean": float(np.mean(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }
    for q in percentiles:
        out[_pct_key(q)] = float(np.percentile(x, q, method="linear"))
    return out


def tick_weighted_mean(spread_mean, tick_count) -> float:
    import numpy as np
    spread_mean = np.asarray(spread_mean, dtype=np.float64)
    tick_count = np.asarray(tick_count, dtype=np.int64)
    if spread_mean.size != tick_count.size or spread_mean.size == 0:
        raise ValueError("weighted mean input size mismatch/empty")
    if np.any(~np.isfinite(spread_mean)) or np.any(tick_count <= 0):
        raise ValueError("invalid weighted mean inputs")
    ticks = int(np.sum(tick_count, dtype=np.int64))
    return float(np.sum(spread_mean * tick_count, dtype=np.float64) / ticks)


def compute_minute_range_bps(mid_open, mid_high, mid_low):
    import numpy as np
    op = np.asarray(mid_open, dtype=np.float64)
    hi = np.asarray(mid_high, dtype=np.float64)
    lo = np.asarray(mid_low, dtype=np.float64)
    return (hi - lo) / op * 10000.0


def compute_abs_return_1m_bps(minute, segment, close):
    import numpy as np
    minute = np.asarray(minute, dtype=np.int64)
    segment = np.asarray(segment, dtype=np.int64)
    close = np.asarray(close, dtype=np.float64)
    n = minute.size
    out = np.full(n, np.nan, dtype=np.float64)
    if n <= 1:
        return out
    valid = (segment[1:] == segment[:-1]) & ((minute[1:] - minute[:-1]) == 60_000)
    target = np.flatnonzero(valid) + 1
    out[target] = np.abs(np.log(close[1:][valid] / close[:-1][valid])) * 10000.0
    return out


def pearson_summary(x, y):
    import numpy as np
    a = np.asarray(x, dtype=np.float64)
    b = np.asarray(y, dtype=np.float64)
    if a.size != b.size:
        raise ValueError("correlation input length mismatch")
    mask = np.isfinite(a) & np.isfinite(b)
    a = a[mask]
    b = b[mask]
    if a.size == 0:
        return {"count": 0, "pearson": None}
    ac = a - np.mean(a)
    bc = b - np.mean(b)
    den = math.sqrt(float(np.dot(ac, ac)) * float(np.dot(bc, bc)))
    if den == 0.0:
        return {"count": int(a.size), "pearson": None}
    return {"count": int(a.size), "pearson": float(np.dot(ac, bc) / den)}


def quintile_codes(values, thresholds=None):
    import numpy as np
    x = np.asarray(values, dtype=np.float64)
    if np.any(~np.isfinite(x)):
        raise ValueError("quintile input contains nonfinite")
    if thresholds is None:
        thresholds = np.percentile(x, [20, 40, 60, 80], method="linear")
    thresholds = np.asarray(thresholds, dtype=np.float64)
    if thresholds.shape != (4,) or np.any(np.diff(thresholds) < 0):
        raise ValueError("invalid quintile thresholds")
    return thresholds, np.searchsorted(thresholds, x, side="right").astype(np.int8)


def ny_time_dimensions(minute_ms):
    import numpy as np
    minute_ms = np.asarray(minute_ms, dtype=np.int64)
    hour_code = minute_ms // 3_600_000
    unique, inverse = np.unique(hour_code, return_inverse=True)
    ny_hour_map = np.empty(unique.size, dtype=np.int16)
    ny_weekday_map = np.empty(unique.size, dtype=np.int16)
    utc_year_map = np.empty(unique.size, dtype=np.int16)
    for i, code in enumerate(unique):
        dt = datetime.fromtimestamp(int(code) * 3600, tz=timezone.utc)
        ny = dt.astimezone(NY)
        ny_hour_map[i] = ny.hour
        ny_weekday_map[i] = ny.weekday()
        utc_year_map[i] = dt.year
    ny_hour = ny_hour_map[inverse]
    ny_weekday = ny_weekday_map[inverse]
    minute_of_hour = ((minute_ms // 60_000) % 60).astype(np.int16)
    ny_minute_of_day = (ny_hour * 60 + minute_of_hour).astype(np.int16)
    return ny_hour, ny_weekday, ny_minute_of_day, utc_year_map[inverse]


def cash_clock_proxy_codes(ny_weekday, ny_minute_of_day):
    import numpy as np
    wd = np.asarray(ny_weekday, dtype=np.int16)
    md = np.asarray(ny_minute_of_day, dtype=np.int16)
    if wd.size != md.size:
        raise ValueError("session dimensions length mismatch")
    out = np.full(wd.size, 1, dtype=np.int8)  # weekday outside cash clock
    weekend = wd >= 5
    cash = (wd < 5) & (md >= 9 * 60 + 30) & (md < 16 * 60)
    out[cash] = 0
    out[weekend] = 2
    return out


def validate_arrays(minute, tick, seg, seg_start, op, hi, lo, cl, sm, smin, smax, previous=None):
    import numpy as np
    arrays = [minute, tick, seg, seg_start, op, hi, lo, cl, sm, smin, smax]
    n = len(minute)
    if n == 0 or any(len(x) != n for x in arrays):
        raise ValueError("decoded row mismatch/empty")
    if np.any(np.diff(minute) <= 0):
        raise ValueError("minute order violation")
    if previous is not None:
        pm, ps = previous
        if int(minute[0]) <= int(pm):
            raise ValueError("global minute order violation")
        if int(seg[0]) - int(ps) not in (0, 1):
            raise ValueError("segment boundary violation")
    if np.any(tick <= 0):
        raise ValueError("nonpositive tick_count")
    if np.any(np.diff(seg) < 0) or np.any(np.diff(seg) > 1):
        raise ValueError("segment jump violation")
    if n > 1 and not np.array_equal(seg_start[1:], np.diff(seg) == 1):
        raise ValueError("segment_start mismatch")
    if previous is None:
        if int(seg[0]) != 0 or not bool(seg_start[0]):
            raise ValueError("first row segment invariant")
    else:
        if bool(seg_start[0]) != (int(seg[0]) - int(previous[1]) == 1):
            raise ValueError("boundary segment_start mismatch")
    for x in (op, hi, lo, cl, sm, smin, smax):
        if np.any(~np.isfinite(x)):
            raise ValueError("nonfinite numeric field")
    if np.any(op <= 0) or np.any(hi <= 0) or np.any(lo <= 0) or np.any(cl <= 0):
        raise ValueError("nonpositive OHLC")
    if np.any(lo > op) or np.any(lo > cl) or np.any(hi < op) or np.any(hi < cl):
        raise ValueError("OHLC invariant violation")
    if np.any(smin <= 0) or np.any(smin > sm) or np.any(sm > smax):
        raise ValueError("spread invariant violation")


def bucket_summary(mask, tick_count, spread_mean, spread_max, minute_range=None):
    import numpy as np
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return {
            "minute_count": 0,
            "source_tick_count": 0,
            "tick_count": distribution([], (50, 90, 95, 99)),
            "spread_tick_weighted_mean": None,
            "spread_mean": distribution([], (50, 90, 95, 99)),
            "spread_max_observed": None,
            **({"minute_range_bps": distribution([], (50, 90))} if minute_range is not None else {}),
        }
    tc = tick_count[idx]
    sm = spread_mean[idx]
    sx = spread_max[idx]
    out = {
        "minute_count": int(idx.size),
        "source_tick_count": int(np.sum(tc, dtype=np.int64)),
        "tick_count": distribution(tc, (50, 90, 95, 99)),
        "spread_tick_weighted_mean": tick_weighted_mean(sm, tc),
        "spread_mean": distribution(sm, (50, 90, 95, 99)),
        "spread_max_observed": float(np.max(sx)),
    }
    if minute_range is not None:
        out["minute_range_bps"] = distribution(minute_range[idx], (50, 90))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="AP5 strategy-agnostic minute-core microstructure price profile.")
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument("--output", default=str(Path(tempfile.gettempdir()) / "ATDS-AP5-MICROSTRUCTURE-PRICE-CORE.json"))
    args = ap.parse_args()

    repo_raw = Path(args.repo_root).expanduser()
    root_raw = Path(args.ap0_root).expanduser()
    manifest_raw = Path(args.ap0_manifest).expanduser()
    output_raw = Path(args.output).expanduser()

    if os.path.lexists(output_raw):
        print("BLOCKED_AP5_OUTPUT_EXISTS")
        print(str(output_raw))
        return 2
    for raw, label in ((repo_raw, "repo-root"), (root_raw, "AP0 root"), (manifest_raw, "AP0 manifest"), (output_raw.parent, "output parent")):
        if path_chain_has_reparse_or_symlink(raw):
            print("BLOCKED_AP5_REPARSE")
            print(f"{label}: {raw}")
            return 2

    repo_root = repo_raw.resolve(strict=False)
    root = root_raw.resolve(strict=False)
    manifest_path = manifest_raw.resolve(strict=False)
    output = output_raw.resolve(strict=False)

    def block(code: str, reason: str) -> int:
        payload = {"schema": "ATDS_AP5_BLOCKED_V0_1", "status": code, "reason": reason}
        try:
            if not output.exists():
                write_json_exclusive(output, payload)
        except Exception:
            pass
        print(code)
        print(reason)
        print(f"Report: {output}")
        return 2

    if not repo_root.is_dir() or not root.is_dir() or not manifest_path.is_file():
        return block("BLOCKED_AP5_INPUT_NOT_FOUND", "repo-root, AP0 root or manifest missing")
    if output == root or is_within(output, root):
        return block("BLOCKED_AP5_OUTPUT_INSIDE_INPUT", str(output))
    if sha256_path(manifest_path) != EXPECTED_AP0_MANIFEST_SHA256:
        return block("BLOCKED_AP5_AP0_MANIFEST_SHA", "AP0 manifest SHA mismatch")
    ap4_raw = repo_root / EXPECTED_AP4_REPO_PATH
    if path_chain_has_reparse_or_symlink(ap4_raw):
        return block("BLOCKED_AP5_REPARSE", "AP4 evidence path contains reparse/symlink")
    ap4_path = ap4_raw.resolve(strict=False)
    if not is_within(ap4_path, repo_root) or not ap4_path.is_file() or sha256_path(ap4_path) != EXPECTED_AP4_SHA256:
        return block("BLOCKED_AP5_AP4_BINDING", "AP4 evidence missing, escaped repo-root, or SHA mismatch")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return block("BLOCKED_AP5_MANIFEST_PARSE", str(exc))
    if manifest.get("status") != "AP0_COMPLETE" or manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP5_MANIFEST_CONTRACT", "AP0 identity/status mismatch")
    files = manifest.get("files")
    cov = manifest.get("coverage") or {}
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        return block("BLOCKED_AP5_MANIFEST_CONTRACT", "AP0 file count mismatch")
    if cov.get("minute_rows_written") != EXPECTED_MINUTES or cov.get("source_ticks_read") != EXPECTED_SOURCE_TICKS:
        return block("BLOCKED_AP5_MANIFEST_CONTRACT", "AP0 coverage mismatch")
    if cov.get("segments") != EXPECTED_SEGMENTS or cov.get("segment_start_rows") != EXPECTED_SEGMENTS:
        return block("BLOCKED_AP5_MANIFEST_CONTRACT", "AP0 segment coverage mismatch")

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        return block("BLOCKED_AP5_RUNTIME_DEPENDENCY", str(exc))

    chunks = {k: [] for k in ("minute","tick","seg","seg_start","op","hi","lo","cl","sm","smin","smax")}
    rows = 0
    ticks_total = 0
    segment_starts = 0
    previous = None

    try:
        for rec in files:
            rel = rec["relative_path"]
            p = resolve_manifest_member(root, rel)
            if int(p.stat().st_size) != int(rec["size_bytes"]) or sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"AP0 file identity mismatch: {rel}")
            pf = pq.ParquetFile(p)
            if int(pf.metadata.num_rows) != int(rec["rows"]):
                raise RuntimeError(f"AP0 row mismatch: {rel}")
            if [(f.name, str(f.type)) for f in pf.schema_arrow] != REQUIRED_SCHEMA:
                raise RuntimeError(f"AP0 schema mismatch: {rel}")
            meta = pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity") != EXPECTED_AP0_IDENTITY.encode():
                raise RuntimeError(f"AP0 identity metadata mismatch: {rel}")
            if meta.get(b"volumes_used") != b"false":
                raise RuntimeError(f"AP0 volume metadata violation: {rel}")
            if meta.get(b"mid_semantics") != b"descriptive_only_not_execution_price":
                raise RuntimeError(f"AP0 mid semantics mismatch: {rel}")

            table = pf.read(columns=READ_COLUMNS, use_threads=False)
            if table.column_names != READ_COLUMNS:
                raise RuntimeError(f"AP5 column scope violation: {rel}")
            minute = table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            tick = table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            seg = table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            seg_start = table["segment_start"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.bool_, copy=False)
            op = table["mid_open"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            hi = table["mid_high"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            lo = table["mid_low"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            cl = table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            sm = table["spread_mean"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            smin = table["spread_min"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            smax = table["spread_max"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            if len(minute) != int(rec["rows"]):
                raise RuntimeError(f"decoded row mismatch: {rel}")
            validate_arrays(minute,tick,seg,seg_start,op,hi,lo,cl,sm,smin,smax,previous)
            previous = (int(minute[-1]), int(seg[-1]))
            rows += int(minute.size)
            ticks_total += int(np.sum(tick, dtype=np.int64))
            segment_starts += int(np.count_nonzero(seg_start))
            for k,v in (("minute",minute),("tick",tick),("seg",seg),("seg_start",seg_start),("op",op),("hi",hi),("lo",lo),("cl",cl),("sm",sm),("smin",smin),("smax",smax)):
                chunks[k].append(v.copy())
            if sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"AP0 file changed during AP5: {rel}")

        if rows != EXPECTED_MINUTES or ticks_total != EXPECTED_SOURCE_TICKS or segment_starts != EXPECTED_SEGMENTS:
            raise RuntimeError("AP5 reconstructed coverage mismatch")
        a = {k: np.concatenate(v) for k,v in chunks.items()}
        if int(a["seg"][-1]) != EXPECTED_SEGMENTS - 1:
            raise RuntimeError("AP5 last segment mismatch")

        minute_range = compute_minute_range_bps(a["op"],a["hi"],a["lo"])
        abs1 = compute_abs_return_1m_bps(a["minute"],a["seg"],a["cl"])
        global_weighted = tick_weighted_mean(a["sm"],a["tick"])
        observed_min = float(np.min(a["smin"]))
        observed_max = float(np.max(a["smax"]))
        if abs(global_weighted - EXPECTED_F2_SPREAD_MEAN) > RECONCILIATION_TOLERANCE:
            raise RuntimeError("spread mean does not reconcile F2/AP1")
        if abs(observed_min - EXPECTED_F2_SPREAD_MIN) > RECONCILIATION_TOLERANCE:
            raise RuntimeError("spread min does not reconcile F2")
        if abs(observed_max - EXPECTED_F2_SPREAD_MAX) > RECONCILIATION_TOLERANCE:
            raise RuntimeError("spread max does not reconcile F2")
        if abs(float(np.mean(minute_range)) - EXPECTED_AP2_MINUTE_RANGE_MEAN_BPS) > RECONCILIATION_TOLERANCE:
            raise RuntimeError("minute range mean does not reconcile AP2")
        valid_abs = np.isfinite(abs1)
        if int(np.count_nonzero(valid_abs)) != EXPECTED_AP2_VALID_1M:
            raise RuntimeError("1m return count does not reconcile AP2")
        if abs(float(np.mean(abs1[valid_abs])) - EXPECTED_AP2_ABS_RETURN_1M_MEAN_BPS) > RECONCILIATION_TOLERANCE:
            raise RuntimeError("1m return mean does not reconcile AP2")

        ny_hour, ny_weekday, ny_minute_day, utc_year = ny_time_dimensions(a["minute"])
        session_code = cash_clock_proxy_codes(ny_weekday,ny_minute_day)

        hourly=[]
        for hour in range(24):
            m=ny_hour==hour
            hourly.append({"code":hour,"label":f"{hour:02d}:00 America/New_York",**bucket_summary(m,a["tick"],a["sm"],a["smax"])})
        session_labels=["NY_WEEKDAY_CASH_CLOCK_0930_1600","NY_WEEKDAY_OUTSIDE_CASH_CLOCK","NY_WEEKEND"]
        sessions=[]
        for code,label in enumerate(session_labels):
            m=session_code==code
            sessions.append({"code":code,"label":label,**bucket_summary(m,a["tick"],a["sm"],a["smax"])})
        years=[]
        for year in range(2021,2027):
            m=utc_year==year
            years.append({"code":year,"partial_period":year in (2021,2026),**bucket_summary(m,a["tick"],a["sm"],a["smax"])})

        range_thresholds, range_codes = quintile_codes(minute_range)
        tick_thresholds, tick_codes = quintile_codes(a["tick"].astype(np.float64))
        range_quintiles=[]
        tick_quintiles=[]
        for q in range(5):
            m=range_codes==q
            range_quintiles.append({"code":q+1,**bucket_summary(m,a["tick"],a["sm"],a["smax"],minute_range)})
            m2=tick_codes==q
            tick_quintiles.append({"code":q+1,**bucket_summary(m2,a["tick"],a["sm"],a["smax"],minute_range)})
        if sum(x["minute_count"] for x in hourly)!=EXPECTED_MINUTES or sum(x["minute_count"] for x in sessions)!=EXPECTED_MINUTES or sum(x["minute_count"] for x in years)!=EXPECTED_MINUTES:
            raise RuntimeError("time partition conservation failed")
        if sum(x["minute_count"] for x in range_quintiles)!=EXPECTED_MINUTES or sum(x["minute_count"] for x in tick_quintiles)!=EXPECTED_MINUTES:
            raise RuntimeError("quintile conservation failed")

        payload={
            "schema":"ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1",
            "status":"AP5_COMPLETE",
            "input_identity":EXPECTED_AP0_IDENTITY,
            "binding":{
                "ap0_manifest_sha256":EXPECTED_AP0_MANIFEST_SHA256,
                "ap4_sha256":EXPECTED_AP4_SHA256,
                "ap0_files_rehashed":EXPECTED_FILES,
            },
            "scope":{
                "strategy_agnostic":True,
                "signals_calculated":False,
                "pnl_calculated":False,
                "optimization":False,
                "source_volume_used":False,
                "subminute_microstructure_qualified":False,
                "future_observations_used":False,
                "causal_deployable":False,
            },
            "coverage":{"minute_rows":rows,"source_ticks_accounted":ticks_total,"segments":EXPECTED_SEGMENTS,"segment_start_rows":segment_starts},
            "metric_contract":{
                "spread_basis":"AP0 per-minute spread_mean; tick-weighted mean uses tick_count",
                "tick_density_basis":"AP0 tick_count per observed minute; not traded volume",
                "minute_range_bps":"(mid_high-mid_low)/mid_open*10000",
                "abs_return_1m_bps":"abs(log(close_t/close_t-1))*10000 only exact contiguous minute in same segment",
                "percentile_method":"linear",
                "range_quintile_percentiles":[20,40,60,80],
                "quintile_assignment":"searchsorted thresholds side=right",
                "session_proxy":"NY weekday clock only 09:30<=local<16:00; no exchange-calendar truth",
            },
            "global":{
                "spread_tick_weighted_mean":global_weighted,
                "spread_mean_minute_distribution":distribution(a["sm"]),
                "spread_min_observed":observed_min,
                "spread_max_observed":observed_max,
                "spread_max_minute_distribution":distribution(a["smax"]),
                "tick_density":distribution(a["tick"]),
                "minute_range_bps":distribution(minute_range),
                "abs_return_1m_bps":distribution(abs1),
            },
            "relations":{
                "spread_mean_vs_minute_range_bps":pearson_summary(a["sm"],minute_range),
                "spread_mean_vs_abs_return_1m_bps":pearson_summary(a["sm"],abs1),
                "spread_mean_vs_tick_count":pearson_summary(a["sm"],a["tick"]),
            },
            "new_york_hour":hourly,
            "session_clock_proxy":sessions,
            "range_quintiles":{"thresholds_bps":range_thresholds.tolist(),"buckets":range_quintiles},
            "tick_density_quintiles":{"thresholds_ticks":tick_thresholds.tolist(),"buckets":tick_quintiles},
            "utc_year":years,
            "runtime":{"numpy_version":np.__version__,"pyarrow_version":pa.__version__},
        }
        write_json_exclusive(output,payload)
        print("AP5_COMPLETE")
        print(f"Minute rows: {rows}")
        print(f"Source ticks accounted: {ticks_total}")
        print(f"Spread tick-weighted mean: {global_weighted}")
        print(f"Range/spread Pearson: {payload['relations']['spread_mean_vs_minute_range_bps']['pearson']}")
        print(f"Report: {output}")
        return 0
    except Exception as exc:
        return block("BLOCKED_AP5_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())

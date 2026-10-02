from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import statistics
import struct
import tempfile
from datetime import datetime, timezone


CONTRACT = "ATDS_SFE_02D_DUAL_RESULT_RUN_V0_1"
HOUR_MS = 3_600_000
LOOKBACK = 20
CRITICAL_VALUE = 2.241402727604947
CANONICAL_PREFIX = b"ATDS_E1_H1_CANONICAL_STREAM_V0_1\n"

EXPECTED = {
    "shared_surface": (
        "GOVERNANCE/SFE-02C-DUAL-EXPERIMENT-SHARED-SURFACE-V0.1.json",
        "0fcf3ce86033b5d8b75caa0a1f18cc6b64fd54a2",
    ),
    "breakout_contract": (
        "GOVERNANCE/SFE-02C-A-BREAKOUT-V1-EXPERIMENT-CONTRACT-V0.1.json",
        "55db053489a3c00b015c424297e316e9e5461e38",
    ),
    "mean_reversion_contract": (
        "GOVERNANCE/SFE-02C-B-MEAN-REVERSION-V1-EXPERIMENT-CONTRACT-V0.1.json",
        "672b059b17413c9058cea749992e0ee08e11f2b4",
    ),
    "freeze_record": (
        "reports/program/2026-10-02-SFE-02C-DUAL-EXPERIMENT-PREREGISTRATION-FREEZE.md",
        "72d3bbb05d76a69c3d5f487500908d3a9c40bc3c",
    ),
    "breakout_runtime": (
        "tools/sfe_02a_breakout_v1.py",
        "60f32b2d054390c2b5dbb975b015d7e09a5a1a96",
    ),
    "mean_reversion_runtime": (
        "tools/sfe_02b_mean_reversion_v1.py",
        "273e184093e4cc98f0eb6569cd6f1007366cce40",
    ),
    "run_contract": (
        "GOVERNANCE/SFE-02D-DUAL-RESULT-RUN-CONTRACT-V0.1.json",
        "PENDING_SELF_BINDING",
    ),
}

EXPECTED_H1_FILE_SHA256 = "94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0"
EXPECTED_H1_CANONICAL_SHA256 = "15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"
EXPECTED_H1_ROWS = 27677
EXPECTED_CONTINUITY_BLOCKS = 1436
EXPECTED_FIRST_H1_MS = 1621904400000
EXPECTED_LAST_H1_MS = 1779660000000

BREAKOUT_OUTPUT = "reports/program/2026-10-02-SFE-02D-BREAKOUT-V1-RESULT-ENVELOPE.json"
MEAN_REVERSION_OUTPUT = "reports/program/2026-10-02-SFE-02D-MEAN-REVERSION-V1-RESULT-ENVELOPE.json"
MANIFEST_OUTPUT = "reports/program/2026-10-02-SFE-02D-DUAL-RUN-MANIFEST.json"


class Blocked(RuntimeError):
    pass


def _git_blob_sha1(raw: bytes) -> str:
    h = hashlib.sha1()
    h.update(f"blob {len(raw)}\0".encode("ascii"))
    h.update(raw)
    return h.hexdigest()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Blocked(f"MODULE_UNLOADABLE:{name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _verify_repo_blobs(root: Path, run_contract_blob: str, runner_blob: str) -> dict:
    observed = {}
    for key, (relative, expected) in EXPECTED.items():
        path = root / relative
        if not path.is_file():
            raise Blocked(f"MISSING_PROTECTED_ARTIFACT:{relative}")
        raw = path.read_bytes()
        actual = _git_blob_sha1(raw)
        if key == "run_contract":
            expected = run_contract_blob
        if actual != expected:
            raise Blocked(f"GIT_BLOB_MISMATCH:{relative}:{actual}:{expected}")
        observed[key] = actual

    runner_path = root / "tools/sfe_02d_dual_result_run.py"
    actual_runner = _git_blob_sha1(runner_path.read_bytes())
    if actual_runner != runner_blob:
        raise Blocked(f"RUNNER_BLOB_MISMATCH:{actual_runner}:{runner_blob}")
    observed["runner"] = actual_runner
    return observed


def _read_h1(path: Path):
    raw = path.read_bytes()
    file_sha = _sha256(raw)
    if file_sha != EXPECTED_H1_FILE_SHA256:
        raise Blocked(f"H1_FILE_SHA256_MISMATCH:{file_sha}")

    rows = []
    required = {
        "h1_start_ms_utc",
        "source_segment_id",
        "continuity_block_id",
        "continuity_ordinal",
        "mid_close",
    }

    for line_no, line in enumerate(raw.splitlines(), start=1):
        try:
            row = json.loads(line.decode("utf-8"))
        except Exception as exc:
            raise Blocked(f"H1_JSONL_PARSE_ERROR:{line_no}") from exc
        if not isinstance(row, dict) or set(row.keys()) != required:
            raise Blocked(f"H1_SCHEMA_MISMATCH:{line_no}")

        for name in (
            "h1_start_ms_utc",
            "source_segment_id",
            "continuity_block_id",
            "continuity_ordinal",
        ):
            if isinstance(row[name], bool) or not isinstance(row[name], int):
                raise Blocked(f"H1_INTEGER_FIELD_INVALID:{line_no}:{name}")

        close = row["mid_close"]
        if isinstance(close, bool) or not isinstance(close, (int, float)):
            raise Blocked(f"H1_CLOSE_TYPE_INVALID:{line_no}")
        close_f = float(close)
        if not math.isfinite(close_f) or close_f <= 0.0:
            raise Blocked(f"H1_CLOSE_DOMAIN_INVALID:{line_no}")

        rows.append(
            {
                "h1_start_ms_utc": int(row["h1_start_ms_utc"]),
                "source_segment_id": int(row["source_segment_id"]),
                "continuity_block_id": int(row["continuity_block_id"]),
                "continuity_ordinal": int(row["continuity_ordinal"]),
                "mid_close": close_f,
            }
        )

    if len(rows) != EXPECTED_H1_ROWS:
        raise Blocked(f"H1_ROW_COUNT_MISMATCH:{len(rows)}")
    if rows[0]["h1_start_ms_utc"] != EXPECTED_FIRST_H1_MS:
        raise Blocked("H1_FIRST_TIMESTAMP_MISMATCH")
    if rows[-1]["h1_start_ms_utc"] != EXPECTED_LAST_H1_MS:
        raise Blocked("H1_LAST_TIMESTAMP_MISMATCH")

    block_ids = {row["continuity_block_id"] for row in rows}
    if len(block_ids) != EXPECTED_CONTINUITY_BLOCKS:
        raise Blocked(f"H1_BLOCK_COUNT_MISMATCH:{len(block_ids)}")

    canonical = hashlib.sha256()
    canonical.update(CANONICAL_PREFIX)
    for row in rows:
        canonical.update(
            struct.pack(
                ">qqqqd",
                row["h1_start_ms_utc"],
                row["source_segment_id"],
                row["continuity_block_id"],
                row["continuity_ordinal"],
                row["mid_close"],
            )
        )
    canonical_sha = canonical.hexdigest()
    if canonical_sha != EXPECTED_H1_CANONICAL_SHA256:
        raise Blocked(f"H1_CANONICAL_SHA256_MISMATCH:{canonical_sha}")

    return rows, {
        "file_sha256": file_sha,
        "canonical_stream_sha256": canonical_sha,
        "rows": len(rows),
        "continuity_blocks": len(block_ids),
        "first_h1_ms_utc": rows[0]["h1_start_ms_utc"],
        "last_h1_ms_utc": rows[-1]["h1_start_ms_utc"],
    }


def _strategy_rows(h1_rows):
    return [
        {
            "bar_start_ms_utc": row["h1_start_ms_utc"],
            "continuity_block_id": row["continuity_block_id"],
            "continuity_ordinal": row["continuity_ordinal"],
            "close": row["mid_close"],
        }
        for row in h1_rows
    ]


def _same_next(row, nxt) -> bool:
    return (
        nxt["continuity_block_id"] == row["continuity_block_id"]
        and nxt["continuity_ordinal"] == row["continuity_ordinal"] + 1
        and nxt["h1_start_ms_utc"] == row["h1_start_ms_utc"] + HOUR_MS
        and math.isfinite(nxt["mid_close"])
        and nxt["mid_close"] > 0.0
    )


def _prior_abs_return(h1_rows, index):
    if index <= 0:
        return None
    prev = h1_rows[index - 1]
    row = h1_rows[index]
    if not (
        row["continuity_block_id"] == prev["continuity_block_id"]
        and row["continuity_ordinal"] == prev["continuity_ordinal"] + 1
        and row["h1_start_ms_utc"] == prev["h1_start_ms_utc"] + HOUR_MS
    ):
        return None
    value = abs(row["mid_close"] / prev["mid_close"] - 1.0)
    return value if math.isfinite(value) else None


def _month_key(timestamp_ms: int) -> str:
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)
    return f"{dt.year:04d}-{dt.month:02d}"


def _unconditional_drift(h1_rows):
    values = []
    for i in range(len(h1_rows) - 1):
        row = h1_rows[i]
        nxt = h1_rows[i + 1]
        if _same_next(row, nxt):
            r = nxt["mid_close"] / row["mid_close"] - 1.0
            if not math.isfinite(r):
                raise Blocked("NONFINITE_UNCONDITIONAL_RETURN")
            values.append(r)
    if not values:
        raise Blocked("NO_UNCONDITIONAL_TRANSITIONS")
    return {
        "valid_transitions": len(values),
        "mean_return": math.fsum(values) / len(values),
    }


def _cluster_jackknife(events):
    by_block = {}
    for event in events:
        by_block.setdefault(event["inference_block"], []).append(event["y"])

    block_stats = []
    for key in sorted(by_block, key=lambda item: (str(item[0]), item[1])):
        ys = by_block[key]
        block_stats.append(
            {
                "block": [key[0], key[1]],
                "sum_y": math.fsum(ys),
                "n": len(ys),
            }
        )

    n_total = sum(item["n"] for item in block_stats)
    sum_total = math.fsum(item["sum_y"] for item in block_stats)
    theta = sum_total / n_total if n_total else None
    k = len(block_stats)

    result = {
        "event_bearing_blocks": k,
        "theta": theta,
        "se": None,
        "ci_lower": None,
        "ci_upper": None,
        "degenerate": False,
    }

    if k < 2 or n_total <= 0:
        result["degenerate"] = True
        return result

    leave_one = []
    for item in block_stats:
        denominator = n_total - item["n"]
        if denominator <= 0:
            result["degenerate"] = True
            return result
        value = (sum_total - item["sum_y"]) / denominator
        if not math.isfinite(value):
            result["degenerate"] = True
            return result
        leave_one.append(value)

    jack_mean = math.fsum(leave_one) / k
    variance = ((k - 1) / k) * math.fsum(
        (value - jack_mean) ** 2 for value in leave_one
    )
    if not math.isfinite(variance) or variance < 0.0:
        result["degenerate"] = True
        return result

    se = math.sqrt(variance)
    if not math.isfinite(se) or se == 0.0:
        result["degenerate"] = True
        return result

    result["se"] = se
    result["ci_lower"] = theta - CRITICAL_VALUE * se
    result["ci_upper"] = theta + CRITICAL_VALUE * se
    return result


def _build_family_envelope(
    family_name,
    experiment_id,
    strategy_blob,
    signals,
    h1_rows,
    unconditional,
):
    if signals.get("status") != "PASS":
        raise Blocked(f"{family_name}_SIGNAL_RUNTIME_BLOCKED")
    records = signals.get("records")
    if not isinstance(records, list) or len(records) != len(h1_rows):
        raise Blocked(f"{family_name}_SIGNAL_ROW_COUNT_MISMATCH")

    events = []
    raw_directional = 0
    excluded = []
    n_long_valid = 0
    n_short_valid = 0

    for i, record in enumerate(records):
        if record["bar_start_ms_utc"] != h1_rows[i]["h1_start_ms_utc"]:
            raise Blocked(f"{family_name}_SIGNAL_TIMESTAMP_MISMATCH:{i}")
        signal = record["signal"]
        if signal not in {"LONG", "SHORT"}:
            continue

        raw_directional += 1
        row = h1_rows[i]
        if i + 1 >= len(h1_rows):
            reason = "END_OF_DATASET"
            excluded.append((i, reason))
            continue

        nxt = h1_rows[i + 1]
        if not _same_next(row, nxt):
            if nxt["continuity_block_id"] != row["continuity_block_id"]:
                reason = "END_OF_CONTINUITY_BLOCK"
            else:
                reason = "OTHER_ADMISSIBILITY_FAILURE"
            excluded.append((i, reason))
            continue

        r = nxt["mid_close"] / row["mid_close"] - 1.0
        direction = 1.0 if signal == "LONG" else -1.0
        y = direction * r
        if not math.isfinite(y):
            raise Blocked(f"{family_name}_NONFINITE_Y:{i}")

        block_index = (row["continuity_ordinal"] - LOOKBACK) // LOOKBACK
        if block_index < 0:
            raise Blocked(f"{family_name}_NEGATIVE_INFERENCE_BLOCK:{i}")

        events.append(
            {
                "index": i,
                "signal": signal,
                "y": y,
                "inference_block": (row["continuity_block_id"], int(block_index)),
            }
        )
        if signal == "LONG":
            n_long_valid += 1
        else:
            n_short_valid += 1

    n_valid = len(events)
    inference = _cluster_jackknife(events)

    gates = {
        "valid_directional_events_gte_100": n_valid >= 100,
        "valid_long_events_gte_20": n_long_valid >= 20,
        "valid_short_events_gte_20": n_short_valid >= 20,
        "event_bearing_blocks_gte_30": inference["event_bearing_blocks"] >= 30,
    }
    all_gates = all(gates.values())

    if not all_gates:
        status = "NOT_INTERPRETABLE / INSUFFICIENT_EVIDENCE"
    elif inference["degenerate"]:
        status = "NOT_INTERPRETABLE / DEGENERATE_INFERENCE"
    elif inference["ci_lower"] > 0.0:
        status = "SUPPORTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE"
    elif inference["ci_upper"] <= 0.0:
        status = "REFUTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE"
    else:
        status = "NOT_INTERPRETABLE / NON_DECISIVE_STATISTICAL_EVIDENCE"

    long_ys = [event["y"] for event in events if event["signal"] == "LONG"]
    short_ys = [event["y"] for event in events if event["signal"] == "SHORT"]

    exclusion_reasons = {
        "END_OF_CONTINUITY_BLOCK": 0,
        "END_OF_DATASET": 0,
        "OTHER_ADMISSIBILITY_FAILURE": 0,
    }
    exclusion_months = {}
    included_prior_abs = []
    excluded_prior_abs = []

    excluded_indexes = {index for index, _ in excluded}
    for index, reason in excluded:
        exclusion_reasons[reason] += 1
        month = _month_key(h1_rows[index]["h1_start_ms_utc"])
        exclusion_months[month] = exclusion_months.get(month, 0) + 1
        prior = _prior_abs_return(h1_rows, index)
        if prior is not None:
            excluded_prior_abs.append(prior)

    for event in events:
        prior = _prior_abs_return(h1_rows, event["index"])
        if prior is not None:
            included_prior_abs.append(prior)

    return {
        "schema": "ATDS_SFE_02D_FAMILY_RESULT_ENVELOPE_V0_1",
        "family": family_name,
        "experiment_id": experiment_id,
        "evidence_class":"EXPLORATORY",
        "exposure_status":"E1_EXPOSED",
        "pristine_confirmatory":False,
        "strategy_runtime_blob":strategy_blob,
        "dataset":{
            "identity":"USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
            "canonical_stream_sha256":EXPECTED_H1_CANONICAL_SHA256,
            "rows":EXPECTED_H1_ROWS,
        },
        "primary":{
            "reference":"RAW_ZERO",
            "surface":"ALL_VALID_DIRECTIONAL_EVENTS",
            "theta":inference["theta"],
            "se_cluster_jackknife":inference["se"],
            "critical_value":CRITICAL_VALUE,
            "ci_lower":inference["ci_lower"],
            "ci_upper":inference["ci_upper"],
            "status":status,
        },
        "evidence":{
            "raw_directional_events":raw_directional,
            "valid_directional_events":n_valid,
            "valid_LONG":n_long_valid,
            "valid_SHORT":n_short_valid,
            "event_bearing_inference_blocks":inference["event_bearing_blocks"],
            "gates":gates,
        },
        "diagnostics":{
            "mean_Y_combined":None if not events else math.fsum(e["y"] for e in events)/len(events),
            "mean_Y_LONG":None if not long_ys else math.fsum(long_ys)/len(long_ys),
            "mean_Y_SHORT":None if not short_ys else math.fsum(short_ys)/len(short_ys),
            "unconditional_drift":unconditional,
            "t1_exclusions":{
                "count":len(excluded),
                "fraction_of_raw_directional":0.0 if raw_directional == 0 else len(excluded)/raw_directional,
                "by_reason":exclusion_reasons,
                "by_calendar_month":dict(sorted(exclusion_months.items())),
                "median_prior_abs_h1_return_included":None if not included_prior_abs else statistics.median(included_prior_abs),
                "median_prior_abs_h1_return_excluded":None if not excluded_prior_abs else statistics.median(excluded_prior_abs),
            },
        },
        "non_claims":[
            "PNL","PROFITABILITY","ECONOMIC_EDGE","ROBUSTNESS",
            "SOURCE_INDEPENDENT_CONFIRMATION","COMPARATIVE_SUPERIORITY","PRODUCTION_READY"
        ],
    }


def _cofiring(breakout_records, mean_records):
    counts = {
        "N_BREAKOUT_DIRECTIONAL":0,
        "N_MEAN_REVERSION_DIRECTIONAL":0,
        "N_CO_FIRING":0,
        "N_BREAKOUT_EXCLUSIVE_OTHER_NEUTRAL":0,
        "N_BREAKOUT_EXCLUSIVE_OTHER_UNDEFINED":0,
        "N_MEAN_REVERSION_EXCLUSIVE_OTHER_NEUTRAL":0,
        "N_MEAN_REVERSION_EXCLUSIVE_OTHER_UNDEFINED":0,
    }

    for b, m in zip(breakout_records, mean_records):
        bs = b["signal"]
        ms = m["signal"]
        bd = bs in {"LONG","SHORT"}
        md = ms in {"LONG","SHORT"}

        if bd:
            counts["N_BREAKOUT_DIRECTIONAL"] += 1
        if md:
            counts["N_MEAN_REVERSION_DIRECTIONAL"] += 1
        if bd and md:
            counts["N_CO_FIRING"] += 1
        elif bd and ms == "NEUTRAL":
            counts["N_BREAKOUT_EXCLUSIVE_OTHER_NEUTRAL"] += 1
        elif bd and ms == "UNDEFINED":
            counts["N_BREAKOUT_EXCLUSIVE_OTHER_UNDEFINED"] += 1
        elif md and bs == "NEUTRAL":
            counts["N_MEAN_REVERSION_EXCLUSIVE_OTHER_NEUTRAL"] += 1
        elif md and bs == "UNDEFINED":
            counts["N_MEAN_REVERSION_EXCLUSIVE_OTHER_UNDEFINED"] += 1

    return counts


def _atomic_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return _sha256(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--h1-jsonl", required=True)
    parser.add_argument("--run-contract-blob", required=True)
    parser.add_argument("--runner-blob", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    h1_path = Path(args.h1_jsonl).resolve()
    output_root = Path(args.output_root).resolve()

    protected = _verify_repo_blobs(root, args.run_contract_blob, args.runner_blob)
    h1_rows, h1_validation = _read_h1(h1_path)

    breakout_module = _load_module(root / "tools/sfe_02a_breakout_v1.py", "sfe02d_breakout")
    mean_module = _load_module(root / "tools/sfe_02b_mean_reversion_v1.py", "sfe02d_mean")

    strategy_rows = _strategy_rows(h1_rows)
    breakout_signals = breakout_module.run_breakout_v1(strategy_rows)
    mean_signals = mean_module.run_mean_reversion_v1(strategy_rows)

    if breakout_signals.get("status") != "PASS" or mean_signals.get("status") != "PASS":
        raise Blocked("STRATEGY_RUNTIME_BLOCKED")

    unconditional = _unconditional_drift(h1_rows)

    breakout_envelope = _build_family_envelope(
        "BREAKOUT_V1",
        "BREAKOUT_V1_SOURCE_B_USTECH_H1_E1_EXPOSED_EXPLORATORY_V0_1",
        "60f32b2d054390c2b5dbb975b015d7e09a5a1a96",
        breakout_signals,
        h1_rows,
        unconditional,
    )
    mean_envelope = _build_family_envelope(
        "MEAN_REVERSION_V1",
        "MEAN_REVERSION_V1_SOURCE_B_USTECH_H1_E1_EXPOSED_EXPLORATORY_V0_1",
        "273e184093e4cc98f0eb6569cd6f1007366cce40",
        mean_signals,
        h1_rows,
        unconditional,
    )

    co_firing = _cofiring(breakout_signals["records"], mean_signals["records"])
    breakout_envelope["diagnostics"]["co_firing"] = co_firing
    mean_envelope["diagnostics"]["co_firing"] = co_firing

    breakout_path = output_root / BREAKOUT_OUTPUT
    mean_path = output_root / MEAN_REVERSION_OUTPUT
    manifest_path = output_root / MANIFEST_OUTPUT

    if breakout_path.exists() or mean_path.exists() or manifest_path.exists():
        raise Blocked("OUTPUT_ALREADY_EXISTS")

    breakout_hash = _atomic_json(breakout_path, breakout_envelope)
    mean_hash = _atomic_json(mean_path, mean_envelope)

    manifest = {
        "schema":"ATDS_SFE_02D_DUAL_RUN_MANIFEST_V0_1",
        "status":"DUAL_RESULT_ENVELOPES_PRODUCED_NOT_YET_INTERPRETED",
        "contract":CONTRACT,
        "protected_blobs":protected,
        "dataset_validation":h1_validation,
        "outputs":{
            "breakout":{"path":BREAKOUT_OUTPUT,"sha256":breakout_hash},
            "mean_reversion":{"path":MEAN_REVERSION_OUTPUT,"sha256":mean_hash},
        },
        "atomicity":{
            "single_process":True,
            "both_envelopes_written_before_manifest":True,
            "no_result_values_emitted_to_stdout":True,
        },
    }
    manifest_hash = _atomic_json(manifest_path, manifest)

    print("SFE02D_DATASET_VALIDATION=PASS")
    print("SFE02D_DUAL_ENVELOPES_WRITTEN=TRUE")
    print(f"BREAKOUT_ENVELOPE_SHA256={breakout_hash}")
    print(f"MEAN_REVERSION_ENVELOPE_SHA256={mean_hash}")
    print(f"DUAL_MANIFEST_SHA256={manifest_hash}")


if __name__ == "__main__":
    try:
        main()
    except Blocked as exc:
        print(f"SFE02D_BLOCKED={exc}")
        raise SystemExit(2)

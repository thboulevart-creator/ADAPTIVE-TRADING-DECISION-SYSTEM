from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any, Iterable

ROW_SCHEMA = "ATDS_BEPD_01D_HISTORICAL_LEDGER_SCHEMA_V0_1"
RESULT_SCHEMA = "ATDS_BEPD_04B_SAME_WEEK_REINTEGRATION_RESPONSE_RESULT_V0_1"
INTERPRETATION = "EVENT_CONDITIONAL_HISTORICAL_FIXED_CORPUS_POST_SWEEP_RESPONSE_DESCRIPTION"
SYNTHETIC_SCOPE = "SYNTHETIC_QUALIFICATION"
REAL_SCOPE = "REAL_AUTHORIZED"
SYNTHETIC_LEDGER_BLOB = "SYNTHETIC_BEPD04B_LEDGER_V0_1"
SYNTHETIC_RUN_ID = "SYNTHETIC_BEPD04B_RUN_V0_1"
REAL_LEDGER_BLOB = "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2"
REAL_RUN_ID = "68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
M05_STATE = "BLOCKED"
Q = Decimal("0.000000000000000001")
REQUIRED_FIELDS = (
    "schema_version",
    "run_id",
    "event_id",
    "sweep_cluster_id",
    "target_week_id",
    "level_id",
    "side",
    "take_h1_close_utc",
    "same_week_reintegration",
)
REQUIRED_STRING_FIELDS = (
    "schema_version",
    "run_id",
    "event_id",
    "sweep_cluster_id",
    "target_week_id",
    "level_id",
    "side",
    "take_h1_close_utc",
)
ALLOWED_RESULT_FIELDS = {
    "schema",
    "execution_scope",
    "interpretation",
    "source_ledger_blob",
    "source_run_id",
    "total_event_count",
    "reintegration_true_count",
    "reintegration_false_count",
    "reintegration_fraction",
    "reintegration_share_decimal",
    "dependence_statement",
    "m05_generalization_uncertainty",
    "forbidden_analytics_executed",
}
FORBIDDEN_RESULT_KEYS = {
    "occurrence_rate",
    "opportunity_count",
    "group_by",
    "side_filter",
    "take_day_ny",
    "target_month",
    "target_year",
    "target_month_position",
    "level_age_band",
    "cross_product",
    "close_displacement",
    "time_to_reintegration",
    "reintegration_speed",
    "mfe",
    "mae",
    "p_value",
    "significance",
    "confidence_interval",
    "bootstrap",
    "future_probability",
    "prediction",
    "causation",
    "edge",
    "strategy",
    "backtest",
    "pnl",
    "expectancy",
    "sizing",
    "paper",
    "broker",
    "live",
    "capital",
}


class ResponseFailure(ValueError):
    pass


def fail(code: str, detail: str | None = None) -> None:
    if detail:
        raise ResponseFailure(f"{code}:{detail}")
    raise ResponseFailure(code)


def _validate_context(context: dict[str, Any]) -> tuple[str, str, str]:
    if not isinstance(context, dict):
        fail("UNAUTHORIZED_EXECUTION_SCOPE", "context_not_dict")
    allowed = {"execution_scope", "source_ledger_blob", "source_run_id", "real_execution_authorized"}
    extra = sorted(set(context) - allowed)
    if extra:
        fail("UNAUTHORIZED_OPTION", extra[0])
    scope = context.get("execution_scope")
    blob = context.get("source_ledger_blob")
    run_id = context.get("source_run_id")
    if scope == SYNTHETIC_SCOPE:
        if blob != SYNTHETIC_LEDGER_BLOB:
            fail("SOURCE_LEDGER_BLOB_MISMATCH")
        if run_id != SYNTHETIC_RUN_ID:
            fail("RUN_ID_MISMATCH")
        if context.get("real_execution_authorized") not in (None, False):
            fail("UNAUTHORIZED_EXECUTION_SCOPE", "synthetic_real_flag")
        return scope, blob, run_id
    if scope == REAL_SCOPE:
        if blob != REAL_LEDGER_BLOB:
            fail("SOURCE_LEDGER_BLOB_MISMATCH")
        if run_id != REAL_RUN_ID:
            fail("RUN_ID_MISMATCH")
        if context.get("real_execution_authorized") is not True:
            fail("UNAUTHORIZED_EXECUTION_SCOPE", "real_authority_missing")
        return scope, blob, run_id
    fail("UNAUTHORIZED_EXECUTION_SCOPE", str(scope))


def _validate_options(options: dict[str, Any] | None) -> None:
    if options is None:
        return
    if not isinstance(options, dict):
        fail("UNAUTHORIZED_OPTION", "options_not_dict")
    if options:
        fail("UNAUTHORIZED_OPTION", sorted(options)[0])


def _validate_row(row: Any, row_number: int, expected_run_id: str) -> None:
    if not isinstance(row, dict):
        fail("INVALID_ROW", str(row_number))
    for key in REQUIRED_FIELDS:
        if key not in row:
            fail("MISSING_REQUIRED_FIELD", f"{row_number}:{key}")
    for key in REQUIRED_STRING_FIELDS:
        value = row[key]
        if not isinstance(value, str) or not value:
            fail("INVALID_REQUIRED_STRING", f"{row_number}:{key}")
    if row["schema_version"] != ROW_SCHEMA:
        fail("UNEXPECTED_SCHEMA_VERSION", str(row_number))
    if row["run_id"] != expected_run_id:
        fail("RUN_ID_MISMATCH", str(row_number))
    if row["side"] not in {"HIGH", "LOW"}:
        fail("INVALID_SIDE", str(row_number))
    if type(row["same_week_reintegration"]) is not bool:
        fail("NON_BOOLEAN_RESPONSE", str(row_number))


def validate_result(result: dict[str, Any]) -> None:
    if not isinstance(result, dict):
        fail("FORBIDDEN_RESULT_SURFACE", "not_dict")
    keys = set(result)
    if keys != ALLOWED_RESULT_FIELDS:
        extra = sorted(keys - ALLOWED_RESULT_FIELDS)
        missing = sorted(ALLOWED_RESULT_FIELDS - keys)
        if extra:
            fail("FORBIDDEN_RESULT_SURFACE", extra[0])
        fail("FORBIDDEN_RESULT_SURFACE", f"missing:{missing[0]}")
    if any(str(k).lower() in FORBIDDEN_RESULT_KEYS for k in result):
        fail("FORBIDDEN_RESULT_SURFACE", "forbidden_key")
    if result["schema"] != RESULT_SCHEMA:
        fail("FORBIDDEN_RESULT_SURFACE", "schema")
    if result["execution_scope"] not in {SYNTHETIC_SCOPE, REAL_SCOPE}:
        fail("FORBIDDEN_RESULT_SURFACE", "scope")
    if result["interpretation"] != INTERPRETATION:
        fail("FORBIDDEN_RESULT_SURFACE", "interpretation")
    if result["m05_generalization_uncertainty"] != M05_STATE:
        fail("FORBIDDEN_RESULT_SURFACE", "m05")
    if result["forbidden_analytics_executed"] is not False:
        fail("FORBIDDEN_RESULT_SURFACE", "authority")
    dep = result["dependence_statement"]
    if not isinstance(dep, str) or "EVENT != IID OBSERVATION" not in dep or "sweep_cluster_id" not in dep or "target_week_id" not in dep:
        fail("FORBIDDEN_RESULT_SURFACE", "dependence")
    n = result["total_event_count"]
    t = result["reintegration_true_count"]
    f = result["reintegration_false_count"]
    if any(type(x) is not int or x < 0 for x in (n, t, f)):
        fail("RESULT_RECONCILIATION_FAIL", "count_type")
    if n <= 0 or t + f != n:
        fail("RESULT_RECONCILIATION_FAIL", "counts")
    if result["reintegration_fraction"] != f"{t}/{n}":
        fail("RESULT_RECONCILIATION_FAIL", "fraction")
    expected_share = format((Decimal(t) / Decimal(n)).quantize(Q, rounding=ROUND_HALF_EVEN), "f")
    if result["reintegration_share_decimal"] != expected_share:
        fail("RESULT_RECONCILIATION_FAIL", "share")


def summarize_rows(rows: Iterable[dict[str, Any]], context: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
    _validate_options(options)
    scope, source_blob, source_run_id = _validate_context(context)
    materialized = list(rows)
    if not materialized:
        fail("EMPTY_INPUT")
    seen: set[str] = set()
    true_count = 0
    for number, row in enumerate(materialized, 1):
        _validate_row(row, number, source_run_id)
        event_id = row["event_id"]
        if event_id in seen:
            fail("DUPLICATE_EVENT_ID", event_id)
        seen.add(event_id)
        if row["same_week_reintegration"]:
            true_count += 1
    total = len(materialized)
    false_count = total - true_count
    share = format((Decimal(true_count) / Decimal(total)).quantize(Q, rounding=ROUND_HALF_EVEN), "f")
    result = {
        "schema": RESULT_SCHEMA,
        "execution_scope": scope,
        "interpretation": INTERPRETATION,
        "source_ledger_blob": source_blob,
        "source_run_id": source_run_id,
        "total_event_count": total,
        "reintegration_true_count": true_count,
        "reintegration_false_count": false_count,
        "reintegration_fraction": f"{true_count}/{total}",
        "reintegration_share_decimal": share,
        "dependence_statement": "EVENT != IID OBSERVATION; sweep_cluster_id and target_week_id are preserved dependence/provenance keys; multiple events sharing either structure are not assumed independent",
        "m05_generalization_uncertainty": M05_STATE,
        "forbidden_analytics_executed": False,
    }
    validate_result(result)
    return result


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                fail("INVALID_ROW", f"blank:{line_number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                fail("INVALID_ROW", f"json:{line_number}:{exc.msg}")
            rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--execution-scope", choices=[SYNTHETIC_SCOPE, REAL_SCOPE], required=True)
    parser.add_argument("--source-ledger-blob", required=True)
    parser.add_argument("--source-run-id", required=True)
    parser.add_argument("--real-execution-authorized", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = read_jsonl(args.input)
        result = summarize_rows(
            rows,
            {
                "execution_scope": args.execution_scope,
                "source_ledger_blob": args.source_ledger_blob,
                "source_run_id": args.source_run_id,
                "real_execution_authorized": args.real_execution_authorized,
            },
        )
        if args.output.exists():
            fail("OUTPUT_CONTAMINATION")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "
", encoding="utf-8", newline="
")
        print("BEPD04B_RESPONSE_CALCULATOR_COMPLETE")
        return 0
    except ResponseFailure as exc:
        print(f"BEPD04B_RESPONSE_CALCULATOR_FAIL:{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

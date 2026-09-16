from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, time as dt_time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse
from zipfile import ZipFile


CONTRACT = "TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1"
TARGET_INSTRUMENT_ID = "9016"
TARGET_INSTRUMENT_NAME = "USATECH.IDX/USD"
CAPTURE_BODY_LIMIT_BYTES = 1_000_000
PAGINATION_QUERY_KEYS = {
    "page",
    "pagesize",
    "page_size",
    "offset",
    "limit",
    "cursor",
    "continuation",
    "next",
    "nexttoken",
    "token",
    "size",
}

SOURCE_OBSERVATIONS: tuple[dict[str, Any], ...] = (
    {
        "target_date": "2021-12-31",
        "candidate_reason": "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED",
        "runtime_path": "reports/data-qualification/historical_trading_breaks_recovery_batch01_runtime.json",
        "attempt_id": "batch01:2021-12-31",
    },
    {
        "target_date": "2021-12-31",
        "candidate_reason": "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED",
        "runtime_path": "reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json",
        "attempt_id": "batch02:2021-12-31",
    },
    {
        "target_date": "2022-07-01",
        "candidate_reason": "INDEPENDENCE_PRE_HOLIDAY_SESSION",
        "runtime_path": "reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json",
        "attempt_id": "batch03:2022-07-01",
    },
    {
        "target_date": "2026-07-02",
        "candidate_reason": "INDEPENDENCE_PRE_HOLIDAY_SESSION",
        "runtime_path": "reports/data-qualification/historical_trading_breaks_recovery_batch14_runtime.json",
        "attempt_id": "batch14:2026-07-02",
    },
)

EXPECTED_CLASS_B_DATES = {
    "2021-12-31",
    "2022-07-01",
    "2026-07-02",
}


@dataclass(frozen=True)
class Decision:
    verdict: str
    reason: str


PASS_REASON = "NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY"


def _decision(verdict: str, reason: str) -> Decision:
    if verdict not in {"PASS", "FAIL", "BLOCKED"}:
        raise ValueError(f"invalid verdict: {verdict}")
    return Decision(verdict, reason)


def evaluate_observation(observation: dict[str, Any]) -> Decision:
    """Adjudicate one already-extracted persisted observation.

    The production extractor computes these fields directly from immutable runtime,
    ledger and archived artifact bytes. This function is intentionally strict and
    pure so every bypass can be attacked independently in tests.
    """

    if not observation.get("provenance_match", False):
        return _decision("FAIL", "PROVENANCE_MISMATCH")
    if not observation.get("runtime_artifact_match", False):
        return _decision("FAIL", "RUNTIME_ARTIFACT_CONTRADICTION")
    if observation.get("borrowed_adjacent_or_other_year", False):
        return _decision("FAIL", "BORROWED_NON_TARGET_EVIDENCE")
    if not observation.get("requested_date_exact", False) or not observation.get("date_honored", False):
        return _decision("FAIL", "TARGET_DATE_NOT_EXACTLY_HONORED")
    if not observation.get("instrument_identity_exact", False):
        return _decision("FAIL", "TARGET_INSTRUMENT_IDENTITY_MISMATCH")
    if observation.get("runtime_errors_present", False) or observation.get("artifact_runtime_errors_present", False):
        return _decision("BLOCKED", "RUNTIME_OR_NETWORK_ERRORS_PRESENT")
    if not observation.get("http_success", False):
        return _decision("BLOCKED", "TARGET_BREAKS_RESPONSE_NOT_HTTP_SUCCESS")
    if not observation.get("raw_payload_present", False):
        return _decision("BLOCKED", "RAW_PAYLOAD_MISSING")
    if not observation.get("target_scope_full_day", False):
        return _decision("BLOCKED", "TARGET_DAY_NOT_FULLY_REPRESENTED_BY_RESPONSE_SCOPE")
    if not observation.get("single_target_range_request_response", False):
        return _decision("BLOCKED", "SINGLE_FULL_RANGE_RESPONSE_NOT_PROVEN")
    if observation.get("pagination_present", False):
        return _decision("BLOCKED", "PAGINATION_OR_CONTINUATION_PRESENT")
    if not observation.get("body_capture_complete", False):
        return _decision("BLOCKED", "RAW_BODY_CAPTURE_COMPLETENESS_NOT_PROVEN")
    if not observation.get("jsonp_list_complete", False):
        return _decision("BLOCKED", "RAW_BROKER_LIST_NOT_SYNTACTICALLY_COMPLETE")
    if not observation.get("internal_target_instrument_raw_control", False):
        return _decision("BLOCKED", "RAW_TARGET_INSTRUMENT_SCOPE_CONTROL_MISSING")
    if not observation.get("internal_target_instrument_dom_control", False):
        return _decision("BLOCKED", "DOM_TARGET_INSTRUMENT_SCOPE_CONTROL_MISSING")

    raw_overlap_count = int(observation.get("raw_target_day_overlap_count", -1))
    normalized_count = int(observation.get("normalized_matching_count", -1))
    if raw_overlap_count != normalized_count:
        return _decision("FAIL", "NORMALIZED_FILTER_HIDES_OR_INVENTS_RAW_TARGET_RECORD")
    if raw_overlap_count != 0:
        return _decision("FAIL", "POSITIVE_TARGET_DAY_INTERVAL_EXISTS_NOT_NEGATIVE_EVIDENCE")

    return _decision("PASS", PASS_REASON)


def evaluate_repeated_consistency(observations: list[dict[str, Any]]) -> Decision:
    if len(observations) <= 1:
        return _decision("PASS", "SINGLE_OBSERVATION_NO_REPEAT_CONTRADICTION")

    canonical = {
        (
            json.dumps(item.get("raw_target_instrument_records", []), sort_keys=True, separators=(",", ":")),
            item.get("target_scope_start_ms"),
            item.get("target_scope_end_ms"),
            item.get("raw_target_day_overlap_count"),
        )
        for item in observations
    }
    if len(canonical) != 1:
        return _decision("FAIL", "INCONSISTENT_REPEATED_OBSERVATIONS")
    return _decision("PASS", "REPEATED_OBSERVATIONS_CONSISTENT")


def parse_jsonp(body: str) -> Any | None:
    if not body:
        return None
    match = re.match(r"^[^(]+\((.*)\)\s*;?$", body.strip(), re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_runtime_result(runtime: dict[str, Any], target_date: str) -> dict[str, Any]:
    matches = [item for item in runtime.get("results", []) if item.get("target_date") == target_date]
    if len(matches) != 1:
        raise ValueError(f"runtime result cardinality mismatch for {target_date}: {len(matches)}")
    return matches[0]


def _find_attempt(ledger: dict[str, Any], attempt_id: str) -> dict[str, Any]:
    matches = [item for item in ledger.get("attempts", []) if item.get("attempt_id") == attempt_id]
    if len(matches) != 1:
        raise ValueError(f"attempt cardinality mismatch for {attempt_id}: {len(matches)}")
    return matches[0]


def _core_result_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    fields = (
        "target_date",
        "candidate_reason",
        "requested_date",
        "target_epoch_ms",
        "instrument_name",
        "instrument_id_expected",
        "instrument_id_observed",
        "official_page_status",
        "current_control_status",
        "target_nav_status",
        "target_document_statuses",
        "date_honored",
        "raw_payload_present",
        "matching_records",
        "dom_witness_lines",
        "runtime_errors",
        "capture_verdict",
        "capture_reason",
    )
    return all(left.get(field) == right.get(field) for field in fields)


def _target_bounds(target_date: str) -> tuple[int, int]:
    target = date.fromisoformat(target_date)
    start = datetime.combine(target, dt_time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000) - 1


def _is_breaks_url(url: str) -> bool:
    query = parse_qs(urlparse(url).query)
    return query.get("group") == ["trading"] and query.get("method") == ["breaks"]


def _range_from_url(url: str) -> tuple[int, int] | None:
    query = parse_qs(urlparse(url).query)
    try:
        return int(query["start"][0]), int(query["end"][0])
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def _interval_overlaps_day(item: dict[str, Any], day_start_ms: int, day_end_ms: int) -> bool:
    try:
        start_ms = int(item["start"])
        end_last_closed_minute_ms = int(item["end"])
    except (KeyError, TypeError, ValueError):
        return False
    reopen_ms = end_last_closed_minute_ms + 60_000
    return start_ms <= day_end_ms and reopen_ms > day_start_ms


def extract_observation(
    *,
    repo_root: Path,
    artifact_dir: Path,
    source: dict[str, Any],
    ledger: dict[str, Any],
) -> dict[str, Any]:
    target_date = str(source["target_date"])
    runtime_path = repo_root / str(source["runtime_path"])
    runtime = _load_json(runtime_path)
    runtime_result = _find_runtime_result(runtime, target_date)
    attempt = _find_attempt(ledger, str(source["attempt_id"]))
    provenance = runtime.get("provenance", {})

    artifact_id = int(provenance["artifact_id"])
    artifact_path = artifact_dir / f"{artifact_id}.zip"
    artifact_sha = _sha256(artifact_path)

    expected_provenance = {
        "workflow_run": str(provenance.get("workflow_run")),
        "job_id": str(provenance.get("job_id")),
        "artifact_id": str(provenance.get("artifact_id")),
        "artifact_sha256": str(provenance.get("artifact_sha256")),
        "probe_commit": str(provenance.get("probe_commit")),
    }
    attempt_provenance = attempt.get("provenance", {})
    provenance_match = all(
        str(attempt_provenance.get(key)) == value
        for key, value in expected_provenance.items()
    ) and artifact_sha == expected_provenance["artifact_sha256"]

    day_start_ms, day_end_ms = _target_bounds(target_date)

    with ZipFile(artifact_path) as archive:
        prefix = f"{target_date}/"
        requests = json.loads(archive.read(prefix + "network_requests.json"))
        responses = json.loads(archive.read(prefix + "network_responses.json"))
        page = json.loads(archive.read(prefix + "page.json"))
        artifact_runtime_errors = json.loads(archive.read(prefix + "runtime_errors.json"))
        summary = json.loads(archive.read("batch_summary.json"))

    summary_result = _find_runtime_result(summary, target_date)
    runtime_artifact_match = (
        _core_result_equal(runtime_result, summary_result)
        and str(summary.get("workflow_run")) == str(provenance.get("workflow_run"))
        and str(summary.get("probe_commit")) == str(provenance.get("probe_commit"))
    )

    target_responses: list[dict[str, Any]] = []
    for response in responses:
        url = str(response.get("url", ""))
        if not _is_breaks_url(url):
            continue
        bounds = _range_from_url(url)
        if bounds is None:
            continue
        start_ms, end_ms = bounds
        if start_ms <= day_start_ms and end_ms >= day_end_ms:
            target_responses.append(response)

    target_requests: list[dict[str, Any]] = []
    for request in requests:
        url = str(request.get("url", ""))
        if not _is_breaks_url(url):
            continue
        bounds = _range_from_url(url)
        if bounds is None:
            continue
        start_ms, end_ms = bounds
        if start_ms <= day_start_ms and end_ms >= day_end_ms:
            target_requests.append(request)

    selected_response = target_responses[0] if len(target_responses) == 1 else {}
    selected_request = target_requests[0] if len(target_requests) == 1 else {}
    response_url = str(selected_response.get("url", ""))
    request_url = str(selected_request.get("url", ""))
    response_bounds = _range_from_url(response_url) if response_url else None
    query = parse_qs(urlparse(request_url).query) if request_url else {}
    pagination_present = any(key.lower() in PAGINATION_QUERY_KEYS for key in query)

    body = selected_response.get("body") or ""
    parsed = parse_jsonp(body) if isinstance(body, str) else None
    jsonp_list_complete = isinstance(parsed, list)
    raw_list = parsed if isinstance(parsed, list) else []

    raw_target_instrument_records = [
        dict(item)
        for item in raw_list
        if isinstance(item, dict) and str(item.get("instrument")) == TARGET_INSTRUMENT_ID
    ]
    raw_target_day_overlaps = [
        item
        for item in raw_target_instrument_records
        if _interval_overlaps_day(item, day_start_ms, day_end_ms)
    ]

    page_text = str(page.get("body_text", ""))
    body_bytes = len(body.encode("utf-8")) if isinstance(body, str) else CAPTURE_BODY_LIMIT_BYTES
    target_scope_full_day = bool(
        response_bounds
        and response_bounds[0] <= day_start_ms
        and response_bounds[1] >= day_end_ms
    )

    observation = {
        "contract": CONTRACT,
        "target_date": target_date,
        "candidate_reason": source["candidate_reason"],
        "attempt_id": source["attempt_id"],
        "artifact_id": artifact_id,
        "artifact_sha256": artifact_sha,
        "provenance_match": provenance_match,
        "runtime_artifact_match": runtime_artifact_match,
        "borrowed_adjacent_or_other_year": False,
        "requested_date_exact": runtime_result.get("requested_date") == target_date,
        "date_honored": runtime_result.get("date_honored") is True,
        "instrument_identity_exact": (
            runtime_result.get("instrument_name") == TARGET_INSTRUMENT_NAME
            and str(runtime_result.get("instrument_id_expected")) == TARGET_INSTRUMENT_ID
            and str(runtime_result.get("instrument_id_observed")) == TARGET_INSTRUMENT_ID
        ),
        "runtime_errors_present": bool(runtime_result.get("runtime_errors")),
        "artifact_runtime_errors_present": bool(artifact_runtime_errors),
        "http_success": (
            len(target_responses) == 1
            and 200 <= int(selected_response.get("status", 0)) < 300
        ),
        "raw_payload_present": runtime_result.get("raw_payload_present") is True and bool(body),
        "target_scope_full_day": target_scope_full_day,
        "single_target_range_request_response": (
            len(target_requests) == 1
            and len(target_responses) == 1
            and request_url == response_url
            and query.get("enabled") == ["true"]
        ),
        "pagination_present": pagination_present,
        "body_capture_complete": (
            bool(body)
            and selected_response.get("body_error") in {None, ""}
            and body_bytes < CAPTURE_BODY_LIMIT_BYTES
        ),
        "jsonp_list_complete": jsonp_list_complete,
        "internal_target_instrument_raw_control": bool(raw_target_instrument_records),
        "internal_target_instrument_dom_control": TARGET_INSTRUMENT_NAME in page_text,
        "raw_target_day_overlap_count": len(raw_target_day_overlaps),
        "normalized_matching_count": len(runtime_result.get("matching_records", [])),
        "raw_target_instrument_records": raw_target_instrument_records,
        "raw_target_day_overlap_records": raw_target_day_overlaps,
        "target_scope_start_ms": response_bounds[0] if response_bounds else None,
        "target_scope_end_ms": response_bounds[1] if response_bounds else None,
        "raw_list_count": len(raw_list),
        "raw_body_bytes": body_bytes,
        "page_target_instrument_line_count": sum(
            1 for line in page_text.splitlines() if TARGET_INSTRUMENT_NAME in line
        ),
        "runtime_capture_verdict": runtime_result.get("capture_verdict"),
        "runtime_capture_reason": runtime_result.get("capture_reason"),
    }
    decision = evaluate_observation(observation)
    observation["verdict"] = decision.verdict
    observation["reason"] = decision.reason
    return observation


def qualify(*, repo_root: Path, artifact_dir: Path) -> dict[str, Any]:
    ledger = _load_json(
        repo_root / "reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json"
    )

    observations = [
        extract_observation(
            repo_root=repo_root,
            artifact_dir=artifact_dir,
            source=source,
            ledger=ledger,
        )
        for source in SOURCE_OBSERVATIONS
    ]

    by_date: dict[str, list[dict[str, Any]]] = {}
    for item in observations:
        by_date.setdefault(str(item["target_date"]), []).append(item)

    date_results: list[dict[str, Any]] = []
    for target_date in sorted(EXPECTED_CLASS_B_DATES):
        items = by_date.get(target_date, [])
        if not items:
            date_results.append(
                {
                    "target_date": target_date,
                    "verdict": "BLOCKED",
                    "reason": "PERSISTED_CLASS_B_OBSERVATION_MISSING",
                    "observation_count": 0,
                }
            )
            continue

        non_pass = [item for item in items if item["verdict"] != "PASS"]
        consistency = evaluate_repeated_consistency(items)
        if non_pass:
            verdict = "FAIL" if any(item["verdict"] == "FAIL" for item in non_pass) else "BLOCKED"
            reason = ";".join(sorted({str(item["reason"]) for item in non_pass}))
        elif consistency.verdict != "PASS":
            verdict = consistency.verdict
            reason = consistency.reason
        else:
            verdict = "PASS"
            reason = PASS_REASON

        date_results.append(
            {
                "target_date": target_date,
                "verdict": verdict,
                "reason": reason,
                "observation_count": len(items),
                "consistency_verdict": consistency.verdict,
                "consistency_reason": consistency.reason,
            }
        )

    verdicts = {item["verdict"] for item in date_results}
    if "FAIL" in verdicts:
        overall_verdict = "FAIL"
        overall_reason = "CLASS_B_NEGATIVE_EVIDENCE_CONTRADICTION_OR_INTEGRITY_FAILURE"
    elif "BLOCKED" in verdicts:
        overall_verdict = "BLOCKED"
        overall_reason = "CLASS_B_NEGATIVE_EVIDENCE_COMPLETENESS_NOT_PROVEN"
    else:
        overall_verdict = "PASS"
        overall_reason = "ALL_THREE_CLASS_B_DATES_HAVE_COMPLETE_BROKER_NATIVE_NEGATIVE_EVIDENCE"

    return {
        "schema": CONTRACT,
        "verdict": overall_verdict,
        "reason": overall_reason,
        "read_only": True,
        "browser_used": False,
        "broker_probe_used": False,
        "new_capture_used": False,
        "calendar_mutated": False,
        "attempt_ledger_mutated": False,
        "progression_mutated": False,
        "capability_registry_mutated": False,
        "execution_window_mutated": False,
        "class_b_date_count": len(EXPECTED_CLASS_B_DATES),
        "source_observation_count": len(observations),
        "observations": observations,
        "date_results": date_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    result = qualify(repo_root=Path(args.repo_root), artifact_dir=Path(args.artifact_dir))
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")

    if result["verdict"] == "FAIL":
        return 1
    if result["verdict"] == "BLOCKED":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

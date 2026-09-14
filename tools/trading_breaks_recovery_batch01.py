from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from datetime import date, datetime, time as dt_time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from tools.trading_breaks_recovery_protocol import (
    CONTRACT as RECOVERY_PROTOCOL,
    TARGET_INSTRUMENT_ID,
    TARGET_INSTRUMENT_NAME,
    recovery_queue,
)


BATCH_CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1"
BATCH_SIZE = 5
OFFICIAL_WIDGET_PAGE = "https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks"
FREESERV_BASE = "https://freeserv.dukascopy.com/2.0/"
NORMAL_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
OUT = Path("trading_breaks_batch01_artifacts")


FROZEN_BATCH01_TARGETS: tuple[tuple[date, str], ...] = (
    (date(2021, 11, 25), "THANKSGIVING_DAY"),
    (date(2021, 11, 26), "THANKSGIVING_FRIDAY"),
    (date(2021, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED"),
    (date(2021, 12, 31), "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED"),
)


def batch01_targets() -> list[tuple[date, str]]:
    """Return the immutable membership versioned before Batch 01 execution."""
    return list(FROZEN_BATCH01_TARGETS)


def widget_url(*, current_date: bool, date_ms: int) -> str:
    params = {
        "path": "trading_breaks/index",
        "showHeader": "true",
        "showFooter": "true",
        "headerColor": "#0e0e0e",
        "tableBorderColor": "#D92626",
        "currentDate": "true" if current_date else "false",
        "date": str(date_ms),
        "width": "100%",
        "height": "500",
        "adv": "popup",
        "lang": "en",
    }
    return FREESERV_BASE + "?" + urlencode(params)


def contains_epoch(url: str, epoch_ms: int, body: str = "") -> bool:
    needle = str(epoch_ms)
    if needle in f"{url} {body}":
        return True
    try:
        qs = parse_qs(urlparse(url).query)
    except Exception:
        return False
    return any(needle == v for values in qs.values() for v in values)


def is_trading_breaks_document(url: str) -> bool:
    try:
        qs = parse_qs(urlparse(url).query)
    except Exception:
        return False
    return any(v == "trading_breaks/index" for v in qs.get("path", []))


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


def iso_utc(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat().replace("+00:00", "Z")


def fully_closed_hours(target_day: date, start_ms: int, end_ms: int) -> list[int]:
    start_dt = datetime.fromtimestamp(start_ms / 1000, timezone.utc)
    reopen_dt = datetime.fromtimestamp((end_ms + 60_000) / 1000, timezone.utc)
    closed: list[int] = []
    for hour in range(24):
        bucket_start = datetime.combine(target_day, dt_time(hour=hour), tzinfo=timezone.utc)
        bucket_end = bucket_start + timedelta(hours=1)
        if bucket_start >= start_dt and bucket_end <= reopen_dt:
            closed.append(hour)
    return closed


async def probe_candidate(browser: Any, target_day: date, candidate_reason: str) -> dict[str, Any]:
    day_start = datetime(target_day.year, target_day.month, target_day.day, tzinfo=timezone.utc)
    day_end = day_start + timedelta(days=1)
    epoch_ms = int(day_start.timestamp() * 1000)
    out = OUT / target_day.isoformat()
    out.mkdir(parents=True, exist_ok=True)

    requests: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    console: list[dict[str, str]] = []
    runtime_errors: list[str] = []
    page_record: dict[str, Any] = {}

    official_status: int | None = None
    control_status: int | None = None
    target_status: int | None = None

    context = await browser.new_context(
        viewport={"width": 1440, "height": 1200},
        locale="en-US",
        user_agent=NORMAL_UA,
    )
    page = await context.new_page()
    page.on("console", lambda msg: console.append({"type": msg.type, "text": msg.text}))
    page.on("pageerror", lambda exc: runtime_errors.append(str(exc)))

    def on_request(req: Any) -> None:
        if "dukascopy" in req.url.lower():
            requests.append({
                "url": req.url,
                "method": req.method,
                "resource_type": req.resource_type,
                "post_data": req.post_data,
                "referer": req.headers.get("referer"),
                "origin": req.headers.get("origin"),
                "user_agent": req.headers.get("user-agent"),
            })

    async def on_response(resp: Any) -> None:
        if "dukascopy" not in resp.url.lower():
            return
        item: dict[str, Any] = {
            "url": resp.url,
            "status": resp.status,
            "content_type": resp.headers.get("content-type", ""),
            "body": None,
            "body_error": None,
        }
        ctype = item["content_type"].lower()
        if any(k in ctype for k in ("json", "text", "javascript", "xml", "html")):
            try:
                item["body"] = (await resp.text())[:1_000_000]
            except Exception as exc:
                item["body_error"] = repr(exc)
        responses.append(item)

    page.on("request", on_request)
    page.on("response", on_response)

    try:
        nav = await page.goto(OFFICIAL_WIDGET_PAGE, wait_until="domcontentloaded", timeout=60_000)
        official_status = nav.status if nav else None
        await page.wait_for_timeout(2_000)
    except Exception as exc:
        runtime_errors.append(f"official_page: {exc!r}")

    try:
        nav = await page.goto(
            widget_url(current_date=True, date_ms=int(time.time() * 1000)),
            wait_until="domcontentloaded",
            timeout=60_000,
            referer=OFFICIAL_WIDGET_PAGE,
        )
        control_status = nav.status if nav else None
        await page.wait_for_timeout(3_000)
    except Exception as exc:
        runtime_errors.append(f"current_control: {exc!r}")

    target_url = widget_url(current_date=False, date_ms=epoch_ms)
    try:
        nav = await page.goto(
            target_url,
            wait_until="domcontentloaded",
            timeout=60_000,
            referer=OFFICIAL_WIDGET_PAGE,
        )
        target_status = nav.status if nav else None
        await page.wait_for_timeout(12_000)
        page_record = {
            "url": page.url,
            "status": target_status,
            "body_text": await page.locator("body").inner_text(timeout=5_000),
            "html": (await page.content())[:1_000_000],
        }
        await page.screenshot(path=str(out / "historical_target.png"), full_page=True)
    except Exception as exc:
        runtime_errors.append(f"historical_target: {exc!r}")

    await context.close()

    (out / "network_requests.json").write_text(json.dumps(requests, indent=2), encoding="utf-8")
    (out / "network_responses.json").write_text(json.dumps(responses, indent=2), encoding="utf-8")
    (out / "page.json").write_text(json.dumps(page_record, indent=2), encoding="utf-8")
    (out / "console.json").write_text(json.dumps(console, indent=2), encoding="utf-8")
    (out / "runtime_errors.json").write_text(json.dumps(runtime_errors, indent=2), encoding="utf-8")

    target_responses = [
        r for r in responses
        if is_trading_breaks_document(r.get("url", ""))
        and contains_epoch(r.get("url", ""), epoch_ms, r.get("body") or "")
    ]
    target_statuses = [int(r.get("status", 0)) for r in target_responses]
    target_success = any(200 <= s < 400 for s in target_statuses) or (
        target_status is not None and 200 <= target_status < 400
    )
    date_honored = contains_epoch(page_record.get("url", ""), epoch_ms) or bool(target_responses)

    instrument_id: str | None = None
    for response in responses:
        url = response.get("url", "")
        parsed = parse_jsonp(response.get("body") or "")
        if "group=widgets&method=instruments" not in url or not isinstance(parsed, dict):
            continue
        instruments = parsed.get("instruments", {})
        if not isinstance(instruments, dict):
            continue
        for key, value in instruments.items():
            if isinstance(value, dict) and value.get("name") == TARGET_INSTRUMENT_NAME:
                instrument_id = str(key)
                break
        if instrument_id is not None:
            break

    matching_records: list[dict[str, Any]] = []
    for response in responses:
        url = response.get("url", "")
        if "group=trading&method=breaks" not in url:
            continue
        parsed = parse_jsonp(response.get("body") or "")
        if not isinstance(parsed, list):
            continue
        for item in parsed:
            if not isinstance(item, dict) or str(item.get("instrument")) != TARGET_INSTRUMENT_ID:
                continue
            try:
                start_ms = int(item["start"])
                end_ms = int(item["end"])
            except (KeyError, TypeError, ValueError):
                continue
            start_dt = datetime.fromtimestamp(start_ms / 1000, timezone.utc)
            end_dt = datetime.fromtimestamp(end_ms / 1000, timezone.utc)
            if start_dt < day_end and end_dt >= day_start:
                enriched = dict(item)
                enriched["start_utc"] = iso_utc(start_ms)
                enriched["end_last_closed_minute_utc"] = iso_utc(end_ms)
                enriched["derived_reopen_utc"] = iso_utc(end_ms + 60_000)
                enriched["fully_closed_hours_utc"] = fully_closed_hours(target_day, start_ms, end_ms)
                matching_records.append(enriched)

    target_text = page_record.get("body_text", "")
    dom_label = target_day.strftime("%d-%b-%y")
    dom_witness_lines = [
        line.strip() for line in target_text.splitlines()
        if TARGET_INSTRUMENT_NAME in line and dom_label in line
    ]

    raw_payload_present = any(
        "group=trading&method=breaks" in r.get("url", "") and bool(r.get("body"))
        for r in responses
    )

    if instrument_id is not None and instrument_id != TARGET_INSTRUMENT_ID:
        capture_verdict = "FAIL"
        capture_reason = "INSTRUMENT_IDENTITY_CONTRADICTION"
    elif matching_records and not dom_witness_lines:
        capture_verdict = "BLOCKED"
        capture_reason = "EXPECTED_DOM_CROSSCHECK_MISSING"
    elif matching_records and target_success and date_honored and raw_payload_present:
        capture_verdict = "CAPTURED"
        capture_reason = "POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION"
    elif target_success and date_honored and not matching_records:
        capture_verdict = "BLOCKED"
        capture_reason = "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"
    elif target_status is not None and target_status >= 400:
        capture_verdict = "BLOCKED"
        capture_reason = "TARGET_WIDGET_DOCUMENT_HTTP_BLOCKED"
    else:
        capture_verdict = "BLOCKED"
        capture_reason = "WIDGET_RUNTIME_OR_HISTORICAL_DATE_PROPAGATION_NOT_PROVEN"

    return {
        "target_date": target_day.isoformat(),
        "candidate_reason": candidate_reason,
        "requested_date": target_day.isoformat(),
        "target_epoch_ms": epoch_ms,
        "instrument_name": TARGET_INSTRUMENT_NAME,
        "instrument_id_expected": TARGET_INSTRUMENT_ID,
        "instrument_id_observed": instrument_id,
        "official_page_status": official_status,
        "current_control_status": control_status,
        "target_nav_status": target_status,
        "target_document_statuses": target_statuses,
        "date_honored": date_honored,
        "raw_payload_present": raw_payload_present,
        "matching_records": matching_records,
        "dom_witness_lines": dom_witness_lines,
        "runtime_errors": runtime_errors,
        "capture_verdict": capture_verdict,
        "capture_reason": capture_reason,
    }


async def main() -> int:
    from playwright.async_api import async_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    targets = batch01_targets()
    results: list[dict[str, Any]] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        for target_day, candidate_reason in targets:
            try:
                results.append(await probe_candidate(browser, target_day, candidate_reason))
            except Exception as exc:
                results.append({
                    "target_date": target_day.isoformat(),
                    "candidate_reason": candidate_reason,
                    "requested_date": target_day.isoformat(),
                    "instrument_name": TARGET_INSTRUMENT_NAME,
                    "instrument_id_expected": TARGET_INSTRUMENT_ID,
                    "capture_verdict": "BLOCKED",
                    "capture_reason": "PROBE_EXECUTION_EXCEPTION",
                    "exception": repr(exc),
                })
        await browser.close()

    summary = {
        "schema": BATCH_CONTRACT,
        "parent_protocol": RECOVERY_PROTOCOL,
        "batch_number": 1,
        "batch_size": BATCH_SIZE,
        "selection_rule": "FIRST_N_OF_GOVERNED_RECOVERY_QUEUE",
        "targets": [
            {"date": target_day.isoformat(), "reason": reason}
            for target_day, reason in targets
        ],
        "workflow_run": os.environ.get("GITHUB_RUN_ID"),
        "probe_commit": os.environ.get("GITHUB_SHA"),
        "read_only": True,
        "market_data_written": False,
        "results": results,
    }
    (OUT / "batch_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

    return 1 if any(item.get("capture_verdict") == "FAIL" for item in results) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema": BATCH_CONTRACT,
            "batch_number": 1,
            "batch_size": BATCH_SIZE,
            "verdict": "BLOCKED",
            "reason": "BATCH_EXECUTION_EXCEPTION",
            "exception": repr(exc),
        }
        (OUT / "batch_summary.json").write_text(json.dumps(failure, indent=2), encoding="utf-8")
        print(json.dumps(failure, indent=2), file=sys.stderr)
        raise

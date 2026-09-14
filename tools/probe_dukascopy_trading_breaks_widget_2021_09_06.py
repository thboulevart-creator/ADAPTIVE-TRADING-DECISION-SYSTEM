from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from datetime import datetime, time as dt_time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from playwright.async_api import async_playwright

TARGET_DATE = "2021-09-06"
TARGET_DAY_START = datetime(2021, 9, 6, tzinfo=timezone.utc)
TARGET_DAY_END = TARGET_DAY_START + timedelta(days=1)
TARGET_EPOCH_MS = int(TARGET_DAY_START.timestamp() * 1000)
TARGET_INSTRUMENT = "USATECH.IDX/USD"
EXPECTED_REASON = "Labor Day"
OFFICIAL_WIDGET_PAGE = "https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks"
FREESERV_BASE = "https://freeserv.dukascopy.com/2.0/"
NORMAL_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
OUT = Path("widget_pilot_artifacts")


def iso_utc(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat()


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


TARGET_WIDGET_URL = widget_url(current_date=False, date_ms=TARGET_EPOCH_MS)
CURRENT_CONTROL_URL = widget_url(current_date=True, date_ms=int(time.time() * 1000))


def contains_target_date(url: str, body: str = "") -> bool:
    blob = f"{url} {body}"
    if str(TARGET_EPOCH_MS) in blob:
        return True
    try:
        qs = parse_qs(urlparse(url).query)
    except Exception:
        return False
    return any(str(TARGET_EPOCH_MS) == v for values in qs.values() for v in values)


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


def full_closed_hours(start_ms: int, end_ms: int) -> list[int]:
    start_dt = datetime.fromtimestamp(start_ms / 1000, timezone.utc)
    end_dt = datetime.fromtimestamp(end_ms / 1000, timezone.utc)
    closed: list[int] = []
    for hour in range(24):
        bucket_start = datetime.combine(TARGET_DAY_START.date(), dt_time(hour=hour), tzinfo=timezone.utc)
        bucket_end = bucket_start + timedelta(hours=1) - timedelta(minutes=1)
        if start_dt <= bucket_start and end_dt >= bucket_end:
            closed.append(hour)
    return closed


async def main() -> int:
    OUT.mkdir(exist_ok=True)
    requests: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    console: list[dict[str, str]] = []
    runtime_errors: list[str] = []
    pages: list[dict[str, Any]] = []

    official_page_status: int | None = None
    control_status: int | None = None
    target_nav_status: int | None = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1200},
            locale="en-US",
            user_agent=NORMAL_UA,
        )
        page = await context.new_page()
        page.on("console", lambda msg: console.append({"type": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: runtime_errors.append(str(exc)))

        def on_request(req):
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

        async def on_response(resp):
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
            official_page_status = nav.status if nav else None
            await page.wait_for_timeout(3_000)
        except Exception as exc:
            runtime_errors.append(f"official_page: {exc!r}")

        try:
            nav = await page.goto(
                CURRENT_CONTROL_URL,
                wait_until="domcontentloaded",
                timeout=60_000,
                referer=OFFICIAL_WIDGET_PAGE,
            )
            control_status = nav.status if nav else None
            await page.wait_for_timeout(5_000)
        except Exception as exc:
            runtime_errors.append(f"current_control: {exc!r}")

        try:
            nav = await page.goto(
                TARGET_WIDGET_URL,
                wait_until="domcontentloaded",
                timeout=60_000,
                referer=OFFICIAL_WIDGET_PAGE,
            )
            target_nav_status = nav.status if nav else None
            await page.wait_for_timeout(20_000)
            pages.append({
                "kind": "historical_target",
                "url": page.url,
                "status": target_nav_status,
                "body_text": await page.locator("body").inner_text(timeout=5_000),
                "html": (await page.content())[:1_000_000],
            })
            await page.screenshot(path=str(OUT / "historical_target.png"), full_page=True)
        except Exception as exc:
            runtime_errors.append(f"historical_target: {exc!r}")

        await browser.close()

    (OUT / "network_requests.json").write_text(json.dumps(requests, indent=2), encoding="utf-8")
    (OUT / "network_responses.json").write_text(json.dumps(responses, indent=2), encoding="utf-8")
    (OUT / "pages.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")
    (OUT / "console.json").write_text(json.dumps(console, indent=2), encoding="utf-8")
    (OUT / "runtime_errors.json").write_text(json.dumps(runtime_errors, indent=2), encoding="utf-8")

    target_responses = [
        r for r in responses
        if is_trading_breaks_document(r.get("url", "")) and contains_target_date(r.get("url", ""), r.get("body") or "")
    ]
    target_statuses = [int(r.get("status", 0)) for r in target_responses]
    target_success = any(200 <= s < 400 for s in target_statuses) or (
        target_nav_status is not None and 200 <= target_nav_status < 400
    )
    target_http_blocked = target_nav_status is not None and target_nav_status >= 400

    target_page = next((p for p in pages if p.get("kind") == "historical_target"), {})
    target_text = target_page.get("body_text", "")
    date_honored = contains_target_date(target_page.get("url", "")) or bool(target_responses)

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
            if isinstance(value, dict) and value.get("name") == TARGET_INSTRUMENT:
                instrument_id = str(key)
                break
        if instrument_id is not None:
            break

    matching_records: list[dict[str, Any]] = []
    if instrument_id is not None:
        for response in responses:
            url = response.get("url", "")
            if "group=trading&method=breaks" not in url:
                continue
            parsed = parse_jsonp(response.get("body") or "")
            if not isinstance(parsed, list):
                continue
            for item in parsed:
                if not isinstance(item, dict) or str(item.get("instrument")) != instrument_id:
                    continue
                try:
                    start_ms = int(item["start"])
                    end_ms = int(item["end"])
                except (KeyError, TypeError, ValueError):
                    continue
                start_dt = datetime.fromtimestamp(start_ms / 1000, timezone.utc)
                end_dt = datetime.fromtimestamp(end_ms / 1000, timezone.utc)
                if start_dt < TARGET_DAY_END and end_dt >= TARGET_DAY_START:
                    enriched = dict(item)
                    enriched["start_utc"] = iso_utc(start_ms)
                    enriched["end_last_closed_minute_utc"] = iso_utc(end_ms)
                    enriched["derived_reopen_utc"] = iso_utc(end_ms + 60_000)
                    enriched["fully_closed_hours_utc"] = full_closed_hours(start_ms, end_ms)
                    matching_records.append(enriched)

    dom_witness_lines = [
        line.strip() for line in target_text.splitlines()
        if TARGET_INSTRUMENT in line and "06-Sep-21" in line
    ]

    positive_broker_witness = bool(
        target_success
        and date_honored
        and instrument_id is not None
        and matching_records
        and dom_witness_lines
    )

    reason_match = any(item.get("reason") == EXPECTED_REASON for item in matching_records)

    if positive_broker_witness and reason_match:
        verdict = "PASS"
        reason = "EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED"
    elif target_success and date_honored and not matching_records:
        verdict = "BLOCKED"
        reason = "HISTORICAL_WIDGET_LOADED_BUT_NO_POSITIVE_USATECH_BREAK_RECORD_RECOVERED"
    elif target_success and date_honored:
        verdict = "BLOCKED"
        reason = "HISTORICAL_WIDGET_EVIDENCE_INCOMPLETE_FOR_DATE_LEVEL_PASS"
    elif target_http_blocked:
        verdict = "BLOCKED"
        reason = "TARGET_WIDGET_DOCUMENT_HTTP_BLOCKED"
    else:
        verdict = "BLOCKED"
        reason = "WIDGET_RUNTIME_OR_HISTORICAL_DATE_PROPAGATION_NOT_PROVEN"

    summary = {
        "contract": "HISTORICAL_TRADING_BREAKS_WIDGET_UNRESOLVED_DATE_PILOT_V1",
        "read_only": True,
        "market_data_written": False,
        "selection_rule": "EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE",
        "target_date": TARGET_DATE,
        "candidate_reason": "LABOR_DAY",
        "target_epoch_ms": TARGET_EPOCH_MS,
        "target_instrument": TARGET_INSTRUMENT,
        "official_page_status": official_page_status,
        "current_control_status": control_status,
        "target_nav_status": target_nav_status,
        "target_document_statuses": target_statuses,
        "date_honored": date_honored,
        "instrument_id": instrument_id,
        "matching_records": matching_records,
        "dom_witness_lines": dom_witness_lines,
        "reason_match": reason_match,
        "runtime_errors": runtime_errors,
        "verdict": verdict,
        "reason": reason,
    }
    (OUT / "probe_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== DUKASCOPY TRADING BREAKS SINGLE-DATE PILOT ===")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        summary = {
            "contract": "HISTORICAL_TRADING_BREAKS_WIDGET_UNRESOLVED_DATE_PILOT_V1",
            "target_date": TARGET_DATE,
            "verdict": "BLOCKED",
            "reason": "PROBE_EXECUTION_EXCEPTION",
            "exception": repr(exc),
        }
        (OUT / "probe_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2), file=sys.stderr)
        raise

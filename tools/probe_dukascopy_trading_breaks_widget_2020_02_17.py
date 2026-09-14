from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from playwright.async_api import async_playwright

TARGET_DATE = "2020-02-17"
TARGET_EPOCH_MS = 1581897600000
TARGET_INSTRUMENT = "USATECH.IDX/USD"
EXPECTED_BREAK_START_MS = 1581962400000  # 2020-02-17 18:00:00Z
EXPECTED_BREAK_END_MS = 1581980340000    # 2020-02-17 22:59:00Z, last closed minute
EXPECTED_REOPEN_MS = 1581980400000       # 2020-02-17 23:00:00Z
EXPECTED_REASON = "President's Day"
OFFICIAL_WIDGET_PAGE = "https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks"
FREESERV_BASE = "https://freeserv.dukascopy.com/2.0/"
NORMAL_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
OUT = Path("widget_probe_artifacts")


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
                headers = req.headers
                requests.append({
                    "url": req.url,
                    "method": req.method,
                    "resource_type": req.resource_type,
                    "post_data": req.post_data,
                    "referer": headers.get("referer"),
                    "origin": headers.get("origin"),
                    "user_agent": headers.get("user-agent"),
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
            pages.append({
                "kind": "current_control",
                "url": page.url,
                "status": control_status,
                "body_text": await page.locator("body").inner_text(timeout=5_000),
                "html": (await page.content())[:1_000_000],
            })
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
    target_http_blocked = (
        target_nav_status is not None and target_nav_status >= 400
    ) or (bool(target_statuses) and not target_success and all(s >= 400 for s in target_statuses))

    target_page = next((p for p in pages if p.get("kind") == "historical_target"), {})
    target_text = target_page.get("body_text", "")
    date_honored = contains_target_date(target_page.get("url", "")) or bool(target_responses)

    dom_witness_line = next(
        (line.strip() for line in target_text.splitlines() if TARGET_INSTRUMENT in line),
        None,
    )
    dom_match = bool(
        dom_witness_line
        and "17-Feb-20 18:00:00" in dom_witness_line
        and "17-Feb-20 22:59:00" in dom_witness_line
        and EXPECTED_REASON in dom_witness_line
    )

    instrument_id: str | None = None
    break_record: dict[str, Any] | None = None
    for response in responses:
        url = response.get("url", "")
        body = response.get("body") or ""
        parsed = parse_jsonp(body)
        if parsed is None:
            continue
        if "group=widgets&method=instruments" in url and isinstance(parsed, dict):
            instruments = parsed.get("instruments", {})
            if isinstance(instruments, dict):
                for key, value in instruments.items():
                    if isinstance(value, dict) and value.get("name") == TARGET_INSTRUMENT:
                        instrument_id = str(key)
                        break

    if instrument_id is not None:
        for response in responses:
            url = response.get("url", "")
            body = response.get("body") or ""
            if "group=trading&method=breaks" not in url or "start=1580515200000" not in url:
                continue
            parsed = parse_jsonp(body)
            if not isinstance(parsed, list):
                continue
            for item in parsed:
                if not isinstance(item, dict):
                    continue
                if str(item.get("instrument")) == instrument_id and item.get("reason") == EXPECTED_REASON:
                    break_record = item
                    break
            if break_record is not None:
                break

    structured_match = False
    derived_reopen_ms: int | None = None
    if break_record is not None:
        try:
            break_start_ms = int(break_record["start"])
            break_end_ms = int(break_record["end"])
            derived_reopen_ms = break_end_ms + 60_000
            structured_match = (
                break_start_ms == EXPECTED_BREAK_START_MS
                and break_end_ms == EXPECTED_BREAK_END_MS
                and derived_reopen_ms == EXPECTED_REOPEN_MS
            )
        except (KeyError, TypeError, ValueError):
            structured_match = False

    exact_calibration_match = bool(target_success and date_honored and dom_match and structured_match)

    if exact_calibration_match:
        verdict = "PASS"
        reason = "HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS"
    elif target_success and date_honored:
        verdict = "FAIL"
        reason = "HISTORICAL_WIDGET_DID_NOT_REPRODUCE_LOCKED_2020_02_17_USATECH_WITNESS"
    elif target_http_blocked:
        verdict = "BLOCKED"
        reason = "TARGET_WIDGET_DOCUMENT_HTTP_BLOCKED"
    else:
        verdict = "BLOCKED"
        reason = "WIDGET_RUNTIME_OR_HISTORICAL_DATE_PROPAGATION_NOT_PROVEN"

    structured_witness = None
    if break_record is not None:
        structured_witness = {
            "instrument_id": instrument_id,
            "break_record": break_record,
            "break_start_utc": iso_utc(int(break_record["start"])),
            "break_end_last_closed_minute_utc": iso_utc(int(break_record["end"])),
            "derived_reopen_utc": iso_utc(derived_reopen_ms) if derived_reopen_ms is not None else None,
        }

    summary = {
        "contract": "HISTORICAL_TRADING_BREAKS_WIDGET_CALIBRATION_V1",
        "read_only": True,
        "market_data_written": False,
        "browser_mode": "headed_xvfb",
        "user_agent": NORMAL_UA,
        "official_widget_page": OFFICIAL_WIDGET_PAGE,
        "official_page_status": official_page_status,
        "current_control_status": control_status,
        "target_widget_url": TARGET_WIDGET_URL,
        "target_date": TARGET_DATE,
        "target_epoch_ms": TARGET_EPOCH_MS,
        "target_nav_status": target_nav_status,
        "target_document_statuses": target_statuses,
        "target_document_success": target_success,
        "target_document_http_blocked": target_http_blocked,
        "target_instrument": TARGET_INSTRUMENT,
        "expected_break_start_utc": iso_utc(EXPECTED_BREAK_START_MS),
        "expected_break_end_last_closed_minute_utc": iso_utc(EXPECTED_BREAK_END_MS),
        "expected_reopen_utc": iso_utc(EXPECTED_REOPEN_MS),
        "date_honored": date_honored,
        "dom_witness_line": dom_witness_line,
        "dom_match": dom_match,
        "structured_witness": structured_witness,
        "structured_match": structured_match,
        "exact_calibration_match": exact_calibration_match,
        "dukascopy_request_count": len(requests),
        "dukascopy_response_count": len(responses),
        "runtime_errors": runtime_errors,
        "verdict": verdict,
        "reason": reason,
    }
    (OUT / "probe_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== DUKASCOPY TRADING BREAKS HISTORICAL WIDGET CALIBRATION ===")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as exc:
        OUT.mkdir(exist_ok=True)
        summary = {
            "contract": "HISTORICAL_TRADING_BREAKS_WIDGET_CALIBRATION_V1",
            "target_date": TARGET_DATE,
            "verdict": "BLOCKED",
            "reason": "PROBE_EXECUTION_EXCEPTION",
            "exception": repr(exc),
        }
        (OUT / "probe_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2), file=sys.stderr)
        raise

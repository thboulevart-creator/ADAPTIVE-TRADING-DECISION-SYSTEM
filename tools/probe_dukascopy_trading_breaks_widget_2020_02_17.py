from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from playwright.async_api import async_playwright

TARGET_DATE = "2020-02-17"
TARGET_EPOCH_MS = 1581897600000
TARGET_INSTRUMENT = "USATECH.IDX/USD"
EXPECTED_CLOSE_GMT = "18:00"
EXPECTED_REOPEN_GMT = "23:00"
OFFICIAL_WIDGET_PAGE = "https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks"
OUT = Path("widget_probe_artifacts")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or " ").strip()


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
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    return any(v == "trading_breaks/index" for v in qs.get("path", []))


def calibration_match(text: str) -> bool:
    t = clean_text(text)
    return TARGET_INSTRUMENT in t and EXPECTED_CLOSE_GMT in t and EXPECTED_REOPEN_GMT in t


async def main() -> int:
    OUT.mkdir(exist_ok=True)
    requests: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    console: list[dict[str, str]] = []
    runtime_errors: list[str] = []
    frame_dumps: list[dict[str, str]] = []
    original_iframe_src: str | None = None
    rewritten_iframe_src: str | None = None
    official_page_status: int | None = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1200},
            locale="en-US",
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
            await page.wait_for_selector("iframe[src*='trading_breaks/index']", timeout=30_000)
            original_iframe_src = await page.locator("iframe[src*='trading_breaks/index']").first.get_attribute("src")
            rewritten_iframe_src = await page.locator("iframe[src*='trading_breaks/index']").first.evaluate(
                """(el, ms) => {
                    const u = new URL(el.src, document.baseURI);
                    u.searchParams.set('currentDate', 'false');
                    u.searchParams.set('date', String(ms));
                    el.src = u.toString();
                    return el.src;
                }""",
                TARGET_EPOCH_MS,
            )
            await page.wait_for_timeout(25_000)
        except Exception as exc:
            runtime_errors.append(f"official_page_or_iframe: {exc!r}")

        try:
            await page.screenshot(path=str(OUT / "widget.png"), full_page=True)
        except Exception as exc:
            runtime_errors.append(f"screenshot: {exc!r}")

        for idx, frame in enumerate(page.frames):
            try:
                body_text = await frame.locator("body").inner_text(timeout=5_000)
            except Exception:
                body_text = ""
            try:
                html = await frame.content()
            except Exception:
                html = ""
            frame_dumps.append({
                "index": str(idx),
                "url": frame.url,
                "body_text": body_text,
                "html": html[:1_000_000],
            })

        await browser.close()

    (OUT / "network_requests.json").write_text(json.dumps(requests, indent=2), encoding="utf-8")
    (OUT / "network_responses.json").write_text(json.dumps(responses, indent=2), encoding="utf-8")
    (OUT / "frames.json").write_text(json.dumps(frame_dumps, indent=2), encoding="utf-8")
    (OUT / "console.json").write_text(json.dumps(console, indent=2), encoding="utf-8")
    (OUT / "runtime_errors.json").write_text(json.dumps(runtime_errors, indent=2), encoding="utf-8")

    all_text_parts: list[str] = []
    for frame in frame_dumps:
        all_text_parts.extend([frame.get("body_text", ""), frame.get("html", "")])
    for resp in responses:
        if isinstance(resp.get("body"), str):
            all_text_parts.append(resp["body"])
    all_text = "\n".join(all_text_parts)

    target_requests = [
        r for r in requests
        if is_trading_breaks_document(r.get("url", "")) and contains_target_date(r.get("url", ""), r.get("post_data") or "")
    ]
    target_responses = [
        r for r in responses
        if is_trading_breaks_document(r.get("url", "")) and contains_target_date(r.get("url", ""), r.get("body") or "")
    ]
    target_statuses = [int(r.get("status", 0)) for r in target_responses]
    target_success = any(200 <= s < 400 for s in target_statuses)
    target_http_blocked = bool(target_statuses) and not target_success and all(s >= 400 for s in target_statuses)

    instrument_present = TARGET_INSTRUMENT in all_text
    close_present = EXPECTED_CLOSE_GMT in all_text
    reopen_present = EXPECTED_REOPEN_GMT in all_text
    exact_match = calibration_match(all_text)
    date_honored = bool(target_requests or target_responses)

    if exact_match and target_success and date_honored:
        verdict = "PASS"
        reason = "HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS"
    elif target_http_blocked:
        verdict = "BLOCKED"
        reason = "TARGET_WIDGET_DOCUMENT_HTTP_BLOCKED"
    elif target_success and date_honored:
        verdict = "FAIL"
        reason = "HISTORICAL_WIDGET_DID_NOT_REPRODUCE_LOCKED_2020_02_17_USATECH_WITNESS"
    else:
        verdict = "BLOCKED"
        reason = "WIDGET_RUNTIME_OR_HISTORICAL_DATE_PROPAGATION_NOT_PROVEN"

    summary = {
        "contract": "HISTORICAL_TRADING_BREAKS_WIDGET_CALIBRATION_V1",
        "read_only": True,
        "market_data_written": False,
        "official_widget_page": OFFICIAL_WIDGET_PAGE,
        "official_page_status": official_page_status,
        "target_date": TARGET_DATE,
        "target_epoch_ms": TARGET_EPOCH_MS,
        "target_instrument": TARGET_INSTRUMENT,
        "expected_close_gmt": EXPECTED_CLOSE_GMT,
        "expected_reopen_gmt": EXPECTED_REOPEN_GMT,
        "original_iframe_src": original_iframe_src,
        "rewritten_iframe_src": rewritten_iframe_src,
        "date_honored": date_honored,
        "target_document_statuses": target_statuses,
        "target_document_success": target_success,
        "target_document_http_blocked": target_http_blocked,
        "instrument_present": instrument_present,
        "expected_close_present": close_present,
        "expected_reopen_present": reopen_present,
        "exact_calibration_match": exact_match,
        "dukascopy_request_count": len(requests),
        "dukascopy_response_count": len(responses),
        "target_request_count": len(target_requests),
        "target_response_count": len(target_responses),
        "runtime_errors": runtime_errors,
        "verdict": verdict,
        "reason": reason,
    }
    (OUT / "probe_result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== DUKASCOPY TRADING BREAKS HISTORICAL WIDGET CALIBRATION ===")
    print(json.dumps(summary, indent=2))
    print("=== TARGET DATE REQUESTS ===")
    for req in target_requests:
        print(json.dumps(req, ensure_ascii=False))
    print("=== TARGET DATE RESPONSES ===")
    for resp in target_responses:
        print(json.dumps({k: v for k, v in resp.items() if k != "body"}, ensure_ascii=False))
    print("=== FRAME URLS ===")
    for frame in frame_dumps:
        print(frame["url"])
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

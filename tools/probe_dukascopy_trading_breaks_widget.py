from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


SCHEMA = "DUKASCOPY_TRADING_BREAKS_WIDGET_PROBE_V2"
CORE_JS_URL = "https://freeserv-static.dukascopy.com/2.0/core.js"
INSTRUMENT_TOKENS = ("USATECH", "US.TECH", "USATECH.IDX", "US.TECH.IDX")


@dataclass(frozen=True)
class BrowserRun:
    returncode: int
    stdout: str
    stderr: str


class TableRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_row = False
        self._in_cell = False
        self._cell_parts: list[str] = []
        self._row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._in_row = True
            self._row = []
        elif self._in_row and tag in {"td", "th"}:
            self._in_cell = True
            self._cell_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_row and self._in_cell:
            self._cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._in_row and self._in_cell and tag in {"td", "th"}:
            value = " ".join("".join(self._cell_parts).split())
            self._row.append(value)
            self._cell_parts = []
            self._in_cell = False
        elif self._in_row and tag == "tr":
            if self._row:
                self.rows.append(self._row)
            self._row = []
            self._in_row = False
            self._in_cell = False


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth:
            value = " ".join(data.split())
            if value:
                self.parts.append(value)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def epoch_ms_for_day(day: date) -> int:
    # Noon UTC avoids an accidental previous/next-day shift in local-time code.
    instant = datetime(day.year, day.month, day.day, 12, 0, tzinfo=timezone.utc)
    return int(instant.timestamp() * 1000)


def bootstrap_html(day: date) -> str:
    params = {
        "showHeader": True,
        "showFooter": True,
        "headerColor": "#0e0e0e",
        "tableBorderColor": "#D92626",
        "currentDate": False,
        "date": epoch_ms_for_day(day),
        "width": "100%",
        "height": "900",
        "adv": "popup",
    }
    config = json.dumps({"type": "trading_breaks", "params": params})
    return (
        "<!doctype html><html><head><meta charset='utf-8'></head><body>"
        f"<script>window.DukascopyApplet={config};</script>"
        f"<script src='{CORE_JS_URL}'></script>"
        "</body></html>"
    )


def detect_browser(explicit: str | None = None) -> str | None:
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    for env_name in ("EDGE_BINARY", "CHROME_BINARY", "CHROMIUM_BINARY"):
        value = os.environ.get(env_name)
        if value:
            candidates.append(value)

    program_files = [
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA"),
    ]
    for root in filter(None, program_files):
        candidates.extend(
            [
                str(Path(root) / "Microsoft/Edge/Application/msedge.exe"),
                str(Path(root) / "Google/Chrome/Application/chrome.exe"),
                str(Path(root) / "Chromium/Application/chrome.exe"),
            ]
        )

    for name in ("msedge", "msedge.exe", "chrome", "chrome.exe", "chromium"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append(resolved)

    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        path = Path(candidate)
        if path.exists() and path.is_file():
            return str(path)
    return None


def run_browser(browser: str, target: str, profile: Path, budget_ms: int) -> BrowserRun:
    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--run-all-compositor-stages-before-draw",
        f"--virtual-time-budget={budget_ms}",
        f"--user-data-dir={profile}",
        "--dump-dom",
        target,
    ]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=max(30, budget_ms // 1000 + 20),
        check=False,
    )
    return BrowserRun(completed.returncode, completed.stdout, completed.stderr)


def extract_iframe_urls(dom: str, base_url: str | None = None) -> list[str]:
    urls = re.findall(r"<iframe\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", dom, re.I)
    normalized: list[str] = []
    for value in urls:
        candidate = html.unescape(value).strip()
        if not candidate:
            continue
        if base_url:
            candidate = urljoin(base_url, candidate)
        if candidate not in normalized:
            normalized.append(candidate)
    return normalized


def extract_script_urls(dom: str, base_url: str | None = None) -> list[str]:
    urls = re.findall(r"<script\b[^>]*?\bsrc=[\"']([^\"']+)[\"']", dom, re.I)
    normalized: list[str] = []
    for value in urls:
        candidate = html.unescape(value).strip()
        if not candidate:
            continue
        if base_url:
            candidate = urljoin(base_url, candidate)
        if candidate not in normalized:
            normalized.append(candidate)
    return normalized


def is_allowed_widget_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "https" and (
        host == "dukascopy.com" or host.endswith(".dukascopy.com")
    )


def parse_rows(dom: str) -> list[list[str]]:
    parser = TableRowParser()
    parser.feed(dom)
    return parser.rows


def visible_text(dom: str) -> str:
    parser = VisibleTextParser()
    parser.feed(dom)
    return " | ".join(parser.parts)


def matching_rows(rows: list[list[str]]) -> list[list[str]]:
    matches: list[list[str]] = []
    for row in rows:
        joined = " ".join(row).upper()
        if any(token in joined for token in INSTRUMENT_TOKENS):
            matches.append(row)
    return matches


def text_contexts(text: str, radius: int = 300) -> list[str]:
    upper = text.upper()
    contexts: list[str] = []
    for token in INSTRUMENT_TOKENS:
        start = 0
        while True:
            index = upper.find(token, start)
            if index < 0:
                break
            left = max(0, index - radius)
            right = min(len(text), index + len(token) + radius)
            context = text[left:right]
            if context not in contexts:
                contexts.append(context)
            start = index + len(token)
    return contexts[:20]


def page_summary(url: str, depth: int, run: BrowserRun) -> dict:
    rows = parse_rows(run.stdout)
    text = visible_text(run.stdout)
    nested = [
        item
        for item in extract_iframe_urls(run.stdout, url)
        if is_allowed_widget_url(item)
    ]
    scripts = extract_script_urls(run.stdout, url)
    return {
        "url": url,
        "depth": depth,
        "returncode": run.returncode,
        "dom_sha256": sha256_text(run.stdout),
        "dom_length": len(run.stdout),
        "visible_text_length": len(text),
        "visible_text_sample": text[:1200],
        "table_row_count": len(rows),
        "matching_rows": matching_rows(rows),
        "text_contexts": text_contexts(text),
        "nested_iframe_urls": nested,
        "script_urls": scripts[:40],
        "stderr_tail": run.stderr[-3000:],
    }


def write_bootstrap_artifact(output_dir: Path, dom: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "bootstrap_dom.html").write_text(dom, encoding="utf-8")


def write_page_artifacts(output_dir: Path, index: int, run: BrowserRun) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"widget_{index:02d}_dom.html").write_text(
        run.stdout, encoding="utf-8"
    )
    (output_dir / f"widget_{index:02d}_visible_text.txt").write_text(
        visible_text(run.stdout), encoding="utf-8"
    )
    (output_dir / f"widget_{index:02d}_stderr.txt").write_text(
        run.stderr, encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render Dukascopy's official Trading Breaks widget for one historical "
            "date using installed Edge/Chrome and recursively inspect Dukascopy iframes."
        )
    )
    parser.add_argument("--date", required=True, help="Historical UTC date YYYY-MM-DD")
    parser.add_argument("--browser", default=None, help="Optional Edge/Chrome executable path")
    parser.add_argument("--budget-ms", type=int, default=15000)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        day = date.fromisoformat(args.date)
    except ValueError:
        print(json.dumps({"schema": SCHEMA, "verdict": "FAIL", "reason": "INVALID_DATE"}, indent=2))
        return 1

    if args.budget_ms < 1000:
        print(json.dumps({"schema": SCHEMA, "verdict": "FAIL", "reason": "BUDGET_TOO_SMALL"}, indent=2))
        return 1
    if args.max_depth < 1 or args.max_depth > 6:
        print(json.dumps({"schema": SCHEMA, "verdict": "FAIL", "reason": "INVALID_MAX_DEPTH"}, indent=2))
        return 1

    browser = detect_browser(args.browser)
    if browser is None:
        print(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "date": day.isoformat(),
                    "verdict": "BLOCKED",
                    "reason": "EDGE_OR_CHROME_NOT_FOUND",
                },
                indent=2,
            )
        )
        return 2

    output_dir = Path(args.output_dir) if args.output_dir else None

    with tempfile.TemporaryDirectory(prefix="dukascopy-breaks-probe-") as temp_name:
        temp = Path(temp_name)
        page = temp / "bootstrap.html"
        page.write_text(bootstrap_html(day), encoding="utf-8")

        first = run_browser(browser, page.resolve().as_uri(), temp / "profile-bootstrap", args.budget_ms)
        bootstrap_iframes = [
            url
            for url in extract_iframe_urls(first.stdout)
            if is_allowed_widget_url(url)
        ]

        if output_dir:
            write_bootstrap_artifact(output_dir, first.stdout)

        if not bootstrap_iframes:
            report = {
                "schema": SCHEMA,
                "date": day.isoformat(),
                "browser": browser,
                "bootstrap_returncode": first.returncode,
                "bootstrap_dom_sha256": sha256_text(first.stdout),
                "iframe_urls": extract_iframe_urls(first.stdout),
                "verdict": "BLOCKED",
                "reason": "NO_DUKASCOPY_WIDGET_IFRAME_DISCOVERED",
                "stderr_tail": first.stderr[-3000:],
            }
            print(json.dumps(report, indent=2, sort_keys=True))
            return 2

        queue: list[tuple[str, int]] = [(url, 1) for url in bootstrap_iframes]
        visited: set[str] = set()
        pages: list[dict] = []
        evidence: list[dict] = []
        page_index = 0

        while queue:
            url, depth = queue.pop(0)
            if url in visited or depth > args.max_depth:
                continue
            visited.add(url)
            page_index += 1

            run = run_browser(
                browser,
                url,
                temp / f"profile-widget-{page_index:02d}",
                args.budget_ms,
            )
            summary = page_summary(url, depth, run)
            pages.append(summary)

            if output_dir:
                write_page_artifacts(output_dir, page_index, run)

            if summary["matching_rows"] or summary["text_contexts"]:
                evidence.append(
                    {
                        "url": url,
                        "depth": depth,
                        "matching_rows": summary["matching_rows"],
                        "text_contexts": summary["text_contexts"],
                    }
                )

            if depth < args.max_depth:
                for nested in summary["nested_iframe_urls"]:
                    if nested not in visited:
                        queue.append((nested, depth + 1))

        evidence_found = bool(evidence)
        report = {
            "schema": SCHEMA,
            "date": day.isoformat(),
            "browser": browser,
            "bootstrap_returncode": first.returncode,
            "bootstrap_dom_sha256": sha256_text(first.stdout),
            "bootstrap_iframe_urls": bootstrap_iframes,
            "max_depth": args.max_depth,
            "pages_visited": len(pages),
            "pages": pages,
            "evidence": evidence,
            "artifact_output_dir": args.output_dir,
            "verdict": "PASS" if evidence_found else "BLOCKED",
            "reason": (
                "USATECH_EVIDENCE_RENDERED_BY_OFFICIAL_WIDGET"
                if evidence_found
                else "USATECH_EVIDENCE_NOT_FOUND_AFTER_RECURSIVE_WIDGET_RENDER"
            ),
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if evidence_found else 2


if __name__ == "__main__":
    raise SystemExit(main())

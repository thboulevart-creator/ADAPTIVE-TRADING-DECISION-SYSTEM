from __future__ import annotations

import json
import time
from urllib.parse import parse_qs, urlparse

try:
    import tools.probe_dukascopy_trading_breaks_official_page as base
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    import probe_dukascopy_trading_breaks_official_page as base


CDP_ORIGIN = "http://localhost"
SCHEMA = "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2_2"
PROBE_FRAME_ID = "dukascopy-calendar-probe-frame"
OFFICIAL_WIDGET_URL = (
    "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index"
    "&showHeader=true&showFooter=true&headerColor=%230e0e0e"
    "&tableBorderColor=%23D92626&currentDate=true"
    "&width=100%25&height=900&adv=popup"
)

# Capture V1 callables before monkey-patching. This keeps the wrapper acyclic.
_original_browser_command = base.browser_command
_original_connect = base.WebSocketClient.connect


def browser_command(browser: str, profile, port: int) -> list[str]:
    command = list(_original_browser_command(browser, profile, port))
    allow_arg = f"--remote-allow-origins={CDP_ORIGIN}"
    if allow_arg not in command:
        command.insert(-1, allow_arg)
    return command


@classmethod
def _connect(cls, url: str, timeout: float = 10.0):
    return _original_connect.__func__(cls, url, timeout)


def ensure_widget_iframe_expression() -> str:
    """Create a probe-owned Trading Breaks iframe inside Dukascopy's page.

    Never reuse an arbitrary Trading Breaks iframe already present on the page:
    doing so can couple the probe to a demo/current-date widget and produce a
    false PASS for the requested historical date.
    """
    widget_url = json.dumps(OFFICIAL_WIDGET_URL)
    frame_id = json.dumps(PROBE_FRAME_ID)
    return f"""
(() => {{
  const existing = document.getElementById({frame_id});
  if (existing) existing.remove();

  const frame = document.createElement('iframe');
  frame.id = {frame_id};
  frame.src = {widget_url};
  frame.width = '100%';
  frame.height = '900';
  frame.setAttribute('data-probe-created', 'true');
  (document.body || document.documentElement).appendChild(frame);
  return frame.src || null;
}})()
""".strip()


def wait_for_widget_iframe(cdp, timeout: float) -> str:
    """Create the probe-owned official widget iframe and return its URL."""
    deadline = time.monotonic() + timeout
    expression = ensure_widget_iframe_expression()
    last_value = None
    attempted = False
    while time.monotonic() < deadline:
        # Create only once. Recreating it every polling iteration would prevent
        # the child frame from ever finishing navigation.
        if not attempted:
            last_value = base.eval_js(cdp, expression)
            attempted = True
        else:
            last_value = base.eval_js(
                cdp,
                f"(() => document.getElementById({json.dumps(PROBE_FRAME_ID)})?.src || null)()",
            )
        if isinstance(last_value, str) and "freeserv.dukascopy.com" in last_value:
            return last_value
        time.sleep(0.5)
    raise RuntimeError(
        f"official page could not create probe-owned trading_breaks iframe: {last_value!r}"
    )


def rewrite_widget_expression(epoch_ms: int) -> str:
    """Rewrite only the probe-owned iframe to the requested historical date."""
    frame_id = json.dumps(PROBE_FRAME_ID)
    return f"""
(() => {{
  const frame = document.getElementById({frame_id});
  if (!frame) return null;
  const url = new URL(frame.src);
  if (url.protocol !== 'https:' || url.hostname !== 'freeserv.dukascopy.com') return null;
  url.searchParams.set('path', 'trading_breaks/index');
  url.searchParams.set('currentDate', 'false');
  url.searchParams.set('date', '{epoch_ms}');
  frame.src = url.toString();
  return frame.src;
}})()
""".strip()


def frame_matches_request(frame_url: str, epoch_ms: int) -> bool:
    """Return True only for the exact requested historical Trading Breaks frame."""
    try:
        parsed = urlparse(frame_url)
        query = parse_qs(parsed.query)
    except Exception:
        return False
    return (
        parsed.scheme == "https"
        and (parsed.hostname or "").lower() == "freeserv.dukascopy.com"
        and query.get("path") == ["trading_breaks/index"]
        and query.get("currentDate") == ["false"]
        and query.get("date") == [str(epoch_ms)]
    )


def _walk_frames(node: dict):
    frame = node.get("frame", {})
    if frame:
        yield frame
    for child in node.get("childFrames", []) or []:
        yield from _walk_frames(child)


def strict_find_widget_frame(frame_tree: dict, epoch_ms: int) -> dict | None:
    """Find only the exact requested frame; there is deliberately no fallback."""
    for frame in _walk_frames(frame_tree):
        if frame_matches_request(str(frame.get("url", "")), epoch_ms):
            return frame
    return None


def wait_for_frame(cdp, epoch_ms: int, timeout: float) -> dict:
    """Wait for the exact requested frame and fail closed if it never appears."""
    deadline = time.monotonic() + timeout
    observed_widget_urls: list[str] = []
    while time.monotonic() < deadline:
        tree = cdp.command("Page.getFrameTree").get("frameTree", {})
        frame = strict_find_widget_frame(tree, epoch_ms)
        if frame is not None:
            return frame
        for candidate in _walk_frames(tree):
            url = str(candidate.get("url", ""))
            if "freeserv.dukascopy.com" in url and "trading_breaks" in url:
                if url not in observed_widget_urls:
                    observed_widget_urls.append(url)
        time.sleep(0.5)
    raise RuntimeError(
        "requested historical widget frame never became active; "
        f"expected_date={epoch_ms}; observed={observed_widget_urls[:10]!r}"
    )


base.SCHEMA = SCHEMA
base.browser_command = browser_command
base.WebSocketClient.connect = _connect
base.wait_for_widget_iframe = wait_for_widget_iframe
base.rewrite_widget_expression = rewrite_widget_expression
base.wait_for_frame = wait_for_frame


if __name__ == "__main__":
    raise SystemExit(base.main())

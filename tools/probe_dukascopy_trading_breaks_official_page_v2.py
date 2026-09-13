from __future__ import annotations

import json
import time

try:
    import tools.probe_dukascopy_trading_breaks_official_page as base
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    import probe_dukascopy_trading_breaks_official_page as base


CDP_ORIGIN = "http://localhost"
SCHEMA = "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2_1"
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
    """Return JS that reuses or creates the official Trading Breaks iframe.

    The iframe is created *inside* Dukascopy's official page so the request to
    freeserv carries the Dukascopy page context instead of being a direct
    headless navigation. No non-Dukascopy host is permitted here.
    """
    widget_url = json.dumps(OFFICIAL_WIDGET_URL)
    return f"""
(() => {{
  let frame = Array.from(document.querySelectorAll('iframe'))
    .find(item => (item.src || '').includes('trading_breaks/index'));
  if (frame) return frame.src || null;

  frame = document.createElement('iframe');
  frame.id = 'dukascopy-calendar-probe-frame';
  frame.src = {widget_url};
  frame.width = '100%';
  frame.height = '900';
  frame.setAttribute('data-probe-created', 'true');
  (document.body || document.documentElement).appendChild(frame);
  return frame.src || null;
}})()
""".strip()


def wait_for_widget_iframe(cdp, timeout: float) -> str:
    """Ensure the official widget iframe exists, then return its URL."""
    deadline = time.monotonic() + timeout
    expression = ensure_widget_iframe_expression()
    last_value = None
    while time.monotonic() < deadline:
        last_value = base.eval_js(cdp, expression)
        if isinstance(last_value, str) and "trading_breaks/index" in last_value:
            return last_value
        time.sleep(0.5)
    raise RuntimeError(
        f"official page could not create trading_breaks iframe: {last_value!r}"
    )


base.SCHEMA = SCHEMA
base.browser_command = browser_command
base.WebSocketClient.connect = _connect
base.wait_for_widget_iframe = wait_for_widget_iframe


if __name__ == "__main__":
    raise SystemExit(base.main())

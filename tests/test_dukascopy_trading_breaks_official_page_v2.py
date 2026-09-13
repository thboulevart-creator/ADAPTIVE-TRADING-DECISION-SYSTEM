from pathlib import Path

from tools.probe_dukascopy_trading_breaks_official_page_v2 import (
    CDP_ORIGIN,
    OFFICIAL_WIDGET_URL,
    SCHEMA,
    browser_command,
    ensure_widget_iframe_expression,
)


def test_v2_schema_is_distinct() -> None:
    assert SCHEMA == "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2_1"


def test_browser_allows_exact_websocket_origin_only() -> None:
    command = browser_command("chrome.exe", Path("profile"), 9222)
    assert f"--remote-allow-origins={CDP_ORIGIN}" in command
    assert "--remote-allow-origins=*" not in command
    assert CDP_ORIGIN == "http://localhost"


def test_remote_allow_origin_is_applied_before_target_url() -> None:
    command = browser_command("chrome.exe", Path("profile"), 9222)
    allow_index = command.index("--remote-allow-origins=http://localhost")
    assert allow_index < len(command) - 1
    assert command[-1].startswith("https://www.dukascopy.com/")


def test_injected_widget_is_restricted_to_dukascopy_trading_breaks() -> None:
    assert OFFICIAL_WIDGET_URL.startswith("https://freeserv.dukascopy.com/2.0/")
    assert "path=trading_breaks/index" in OFFICIAL_WIDGET_URL
    assert "http://" not in OFFICIAL_WIDGET_URL


def test_injection_reuses_existing_widget_before_creating_one() -> None:
    expression = ensure_widget_iframe_expression()
    assert "querySelectorAll('iframe')" in expression
    assert "trading_breaks/index" in expression
    assert "document.createElement('iframe')" in expression
    assert "data-probe-created" in expression
    assert expression.index("querySelectorAll('iframe')") < expression.index(
        "document.createElement('iframe')"
    )

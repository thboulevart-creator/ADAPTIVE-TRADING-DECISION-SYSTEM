from pathlib import Path

from tools.probe_dukascopy_trading_breaks_official_page_v2 import (
    CDP_ORIGIN,
    SCHEMA,
    browser_command,
)


def test_v2_schema_is_distinct() -> None:
    assert SCHEMA == "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2"


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

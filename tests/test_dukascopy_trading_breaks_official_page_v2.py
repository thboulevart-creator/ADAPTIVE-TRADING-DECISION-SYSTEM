from pathlib import Path

from tools.probe_dukascopy_trading_breaks_official_page_v2 import (
    CDP_ORIGIN,
    OFFICIAL_WIDGET_URL,
    PROBE_FRAME_ID,
    SCHEMA,
    browser_command,
    ensure_widget_iframe_expression,
    frame_matches_request,
    rewrite_widget_expression,
    strict_find_widget_frame,
)


def test_v2_schema_is_distinct() -> None:
    assert SCHEMA == "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2_2"


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


def test_injected_widget_is_probe_owned_and_not_reused() -> None:
    expression = ensure_widget_iframe_expression()
    assert OFFICIAL_WIDGET_URL.startswith("https://freeserv.dukascopy.com/2.0/")
    assert "path=trading_breaks/index" in OFFICIAL_WIDGET_URL
    assert "document.createElement('iframe')" in expression
    assert PROBE_FRAME_ID in expression
    assert "querySelectorAll('iframe')" not in expression


def test_rewrite_targets_probe_owned_frame_only() -> None:
    expression = rewrite_widget_expression(1736424000000)
    assert PROBE_FRAME_ID in expression
    assert "querySelectorAll('iframe')" not in expression
    assert "currentDate" in expression
    assert "false" in expression
    assert "1736424000000" in expression


def test_frame_match_requires_exact_historical_contract() -> None:
    good = (
        "https://freeserv.dukascopy.com/2.0/?path=trading_breaks%2Findex"
        "&currentDate=false&date=1736424000000"
    )
    assert frame_matches_request(good, 1736424000000)

    assert not frame_matches_request(
        "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index"
        "&currentDate=true&date=1736424000000",
        1736424000000,
    )
    assert not frame_matches_request(
        "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index"
        "&currentDate=false&date=1528909332431",
        1736424000000,
    )


def test_strict_frame_search_has_no_stale_fallback() -> None:
    epoch = 1736424000000
    tree = {
        "frame": {"id": "root", "url": "https://www.dukascopy.com/"},
        "childFrames": [
            {
                "frame": {
                    "id": "stale",
                    "url": (
                        "https://freeserv.dukascopy.com/2.0/"
                        "?path=trading_breaks/index&currentDate=true&date=1528909332431"
                    ),
                }
            }
        ],
    }
    assert strict_find_widget_frame(tree, epoch) is None

    tree["childFrames"].append(
        {
            "frame": {
                "id": "target",
                "url": (
                    "https://freeserv.dukascopy.com/2.0/"
                    "?path=trading_breaks%2Findex&currentDate=false"
                    f"&date={epoch}"
                ),
            }
        }
    )
    assert strict_find_widget_frame(tree, epoch)["id"] == "target"

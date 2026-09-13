from tools.probe_dukascopy_trading_breaks_official_page import (
    find_widget_frame,
    rewrite_widget_expression,
    walk_frames,
    widget_iframe_expression,
)


def test_walk_frames_recurses_nested_children() -> None:
    tree = {
        "frame": {"id": "root", "url": "https://www.dukascopy.com/"},
        "childFrames": [
            {
                "frame": {"id": "child", "url": "https://a.example/"},
                "childFrames": [
                    {"frame": {"id": "grandchild", "url": "https://b.example/"}}
                ],
            }
        ],
    }
    assert [frame["id"] for frame in walk_frames(tree)] == [
        "root",
        "child",
        "grandchild",
    ]


def test_find_widget_frame_prefers_requested_historical_date() -> None:
    epoch_ms = 1736424000000
    tree = {
        "frame": {"id": "root", "url": "https://www.dukascopy.com/"},
        "childFrames": [
            {
                "frame": {
                    "id": "old",
                    "url": "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index&date=1",
                }
            },
            {
                "frame": {
                    "id": "target",
                    "url": (
                        "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index"
                        f"&date={epoch_ms}"
                    ),
                }
            },
        ],
    }
    assert find_widget_frame(tree, epoch_ms)["id"] == "target"


def test_find_widget_frame_falls_back_to_any_trading_breaks_frame() -> None:
    tree = {
        "frame": {"id": "root", "url": "https://www.dukascopy.com/"},
        "childFrames": [
            {
                "frame": {
                    "id": "widget",
                    "url": "https://freeserv.dukascopy.com/2.0/?path=trading_breaks/index",
                }
            }
        ],
    }
    assert find_widget_frame(tree, 1736424000000)["id"] == "widget"


def test_rewrite_expression_changes_only_widget_date_contract() -> None:
    expression = rewrite_widget_expression(1736424000000)
    assert "trading_breaks/index" in expression
    assert "currentDate" in expression
    assert "false" in expression
    assert "1736424000000" in expression


def test_widget_iframe_expression_targets_trading_breaks_only() -> None:
    expression = widget_iframe_expression()
    assert "querySelectorAll('iframe')" in expression
    assert "trading_breaks/index" in expression

from datetime import date

from tools.probe_dukascopy_trading_breaks_widget import (
    BrowserRun,
    epoch_ms_for_day,
    extract_iframe_urls,
    extract_script_urls,
    is_allowed_widget_url,
    matching_rows,
    page_summary,
    parse_rows,
    text_contexts,
)


def test_epoch_ms_uses_requested_utc_day() -> None:
    assert epoch_ms_for_day(date(2025, 1, 9)) == 1736424000000


def test_extract_iframe_urls_decodes_and_deduplicates() -> None:
    dom = """
    <iframe src="https://freeserv.dukascopy.com/widget?a=1&amp;b=2"></iframe>
    <iframe src='https://freeserv.dukascopy.com/widget?a=1&amp;b=2'></iframe>
    """
    assert extract_iframe_urls(dom) == [
        "https://freeserv.dukascopy.com/widget?a=1&b=2"
    ]


def test_extract_iframe_urls_resolves_relative_nested_url() -> None:
    dom = '<iframe src="/2.0/internal/widget?id=7"></iframe>'
    assert extract_iframe_urls(dom, "https://freeserv.dukascopy.com/2.0/root") == [
        "https://freeserv.dukascopy.com/2.0/internal/widget?id=7"
    ]


def test_extract_script_urls_resolves_relative_url() -> None:
    dom = '<script src="assets/app.js"></script>'
    assert extract_script_urls(dom, "https://freeserv.dukascopy.com/2.0/root/") == [
        "https://freeserv.dukascopy.com/2.0/root/assets/app.js"
    ]


def test_widget_url_is_restricted_to_https_dukascopy_hosts() -> None:
    assert is_allowed_widget_url("https://freeserv.dukascopy.com/widget")
    assert is_allowed_widget_url("https://www.dukascopy.com/widget")
    assert not is_allowed_widget_url("http://www.dukascopy.com/widget")
    assert not is_allowed_widget_url("https://dukascopy.com.evil.example/widget")
    assert not is_allowed_widget_url("https://example.com/widget")


def test_table_parser_finds_usatech_row() -> None:
    dom = """
    <table>
      <tr><th>Instrument</th><th>Break</th></tr>
      <tr><td>USA30.IDX/USD</td><td>18:00 - 23:00</td></tr>
      <tr><td>USATECH.IDX/USD</td><td>18:00 - 23:00</td></tr>
    </table>
    """
    rows = parse_rows(dom)
    assert matching_rows(rows) == [["USATECH.IDX/USD", "18:00 - 23:00"]]


def test_text_contexts_finds_non_table_usatech_evidence() -> None:
    text = "Holiday schedule | USATECH.IDX/USD | Trading stops 18:00 | reopens 23:00"
    contexts = text_contexts(text, radius=50)
    assert contexts
    assert "USATECH.IDX/USD" in contexts[0]


def test_page_summary_exposes_nested_iframe_scripts_and_evidence() -> None:
    dom = """
    <html><body>
      <script src="/assets/widget.js"></script>
      <iframe src="/inner"></iframe>
      <div>USATECH.IDX/USD closes 18:00</div>
    </body></html>
    """
    summary = page_summary(
        "https://freeserv.dukascopy.com/root",
        1,
        BrowserRun(0, dom, "diagnostic stderr"),
    )
    assert summary["text_contexts"]
    assert summary["nested_iframe_urls"] == ["https://freeserv.dukascopy.com/inner"]
    assert summary["script_urls"] == ["https://freeserv.dukascopy.com/assets/widget.js"]
    assert summary["stderr_tail"] == "diagnostic stderr"

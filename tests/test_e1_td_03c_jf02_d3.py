from pathlib import Path
import json

JAVA = Path("tools/jforex_jf02/src/main/java/atds/jf02/JF02HistoryRead.java")
CONTRACT = Path("GOVERNANCE/E1-TD-03C-JF02-D3-CACHE-NEUTRAL-CONTROLLED-CAUSAL-TEST-CONTRACT-V0.1.json")
BREAKERS = Path("GOVERNANCE/E1-TD-03C-JF02-D3-BREAKER-MATRIX-V0.1.json")

EXACT_D3_CACHE = r"C:\\Users\\Boulevart\\ATDS-TOOLS\\jf02-d3-cache-v0.1"
BASELINE_CACHE_FRAGMENT = r"AppData\\Local\\JForex\\.cache"

def source() -> str:
    return JAVA.read_text(encoding="utf-8")

def test_d3_contract_frozen_request():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    r = c["frozen_request"]
    assert r["sdk"] == "DDS2-jClient-JForex 3.6.51"
    assert r["api_implementation"] == "2.13.99"
    assert r["account_mode"] == "DEMO"
    assert r["instrument"] == "USATECH.IDX/USD"
    assert r["from_ms"] == 1759327200000
    assert r["to_ms_inclusive"] == 1759330799999
    assert r["automatic_retries"] == 0
    assert r["real_getticks_budget"] == 1

def test_d3_breakers_are_frozen_and_cover_freshness():
    b = json.loads(BREAKERS.read_text(encoding="utf-8"))
    assert b["frozen"] is True
    results = {x["result"] for x in b["breakers"]}
    assert "BLOCKED_D3_CACHE_NOT_FRESH" in results
    assert "BLOCKED_D3_BASELINE_CACHE_FORBIDDEN" in results
    assert "BLOCKED_D3_GETTICKS_BUDGET" in results
    assert "BLOCKED_D3_RETRY_FORBIDDEN" in results

def test_d3_accepts_exact_run_label_only_for_new_lane():
    s = source()
    assert '"D3".equals(runLabel)' in s

def test_d3_exact_isolated_cache_path_is_frozen_in_source():
    s = source()
    assert EXACT_D3_CACHE in s

def test_d3_rejects_preexisting_isolated_cache():
    s = source()
    assert "Files.exists(d3Cache)" in s
    assert "BLOCKED_D3_CACHE_NOT_FRESH" in s

def test_d3_rejects_baseline_cache_selection():
    s = source()
    assert BASELINE_CACHE_FRAGMENT in s
    assert "BLOCKED_D3_BASELINE_CACHE_FORBIDDEN" in s

def test_d3_binds_cache_before_connect():
    s = source()
    bind = s.index("setCacheDirectory")
    connect = s.index("client.connect")
    assert bind < connect

def test_d3_preserves_one_getticks_call_in_collector():
    s = source()
    assert s.count(".getTicks(") == 1

def test_d3_preserves_zero_retry_policy():
    s = source()
    assert "retry" not in s.lower()

def test_d3_preserves_frozen_request():
    s = source()
    assert 'INSTRUMENT_TEXT = "USATECH.IDX/USD"' in s
    assert "FROM_MS = 1759327200000L" in s
    assert "TO_MS = 1759330799999L" in s
    assert 'JNLP_URL = "http://platform.dukascopy.com/demo_3/jforex_3.jnlp"' in s

def test_d3_does_not_add_trading_or_order_paths():
    s = source()
    forbidden = [
        ".submitOrder(", "getEngine().submitOrder", "IEngine.OrderCommand",
        "getOrders(", ".close(", ".mergeOrders("
    ]
    assert all(token not in s for token in forbidden)

def test_d3_does_not_change_canonical_serialization_fields():
    s = source()
    assert 'writer.write("timestamp,askPrice,bidPrice,askVolume,bidVolume\\n")' in s
    assert "BigDecimal.valueOf(ask).toPlainString()" in s
    assert "BigDecimal.valueOf(bid).toPlainString()" in s
    assert "BigDecimal.valueOf(askVol).toPlainString()" in s
    assert "BigDecimal.valueOf(bidVol).toPlainString()" in s

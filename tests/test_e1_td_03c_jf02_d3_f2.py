from pathlib import Path
import json

JAVA = Path("tools/jforex_jf02_f2/src/main/java/atds/jf02/JF02ConnectionProbe.java")
POM = Path("tools/jforex_jf02_f2/pom.xml")
CONTRACT = Path("GOVERNANCE/E1-TD-03C-JF02-D3-F2-CONNECTION-ONLY-STATE-OBSERVABILITY-CONTRACT-V0.1.json")
BREAKERS = Path("GOVERNANCE/E1-TD-03C-JF02-D3-F2-BREAKER-MATRIX-V0.1.json")

def source() -> str:
    return JAVA.read_text(encoding="utf-8") if JAVA.exists() else ""

def test_f2_contract_frozen_values():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["observation"]["post_connect_return_window_ms"] == 120000
    assert c["observation"]["sample_interval_ms"] == 1000
    assert c["observation"]["primary_threshold_ms"] == 30000
    assert c["budgets"]["login"] == 1
    assert c["budgets"]["connect"] == 1
    assert c["budgets"]["reconnect"] == 0
    assert c["budgets"]["retry"] == 0

def test_f2_breakers_frozen():
    b = json.loads(BREAKERS.read_text(encoding="utf-8"))
    assert b["frozen"] is True
    results = {x["result"] for x in b["breakers"]}
    assert "BLOCKED_F2_HISTORY_PATH" in results
    assert "BLOCKED_F2_STRATEGY_PATH" in results
    assert "BLOCKED_F2_RETRY_OR_RECONNECT" in results
    assert "BLOCKED_F2_UNEXPECTED_MARKET_DATA_SIDE_EFFECT" in results

def test_f2_dedicated_source_exists():
    assert JAVA.exists()
    assert POM.exists()

def test_f2_has_exact_frozen_constants():
    s = source()
    assert 'OBSERVATION_WINDOW_MS = 120000L' in s
    assert 'SAMPLE_INTERVAL_MS = 1000L' in s
    assert 'PRIMARY_THRESHOLD_MS = 30000L' in s
    assert 'DISCONNECT_OBSERVATION_MS = 10000L' in s

def test_f2_exact_cache_and_protected_caches_are_frozen():
    s = source()
    assert r'C:\\Users\\Boulevart\\ATDS-TOOLS\\jf02-f2-cache-v0.1' in s
    assert r'C:\\Users\\Boulevart\\AppData\\Local\\JForex\\.cache' in s
    assert r'C:\\Users\\Boulevart\\ATDS-TOOLS\\jf02-d3-cache-v0.1' in s
    assert "BLOCKED_F2_CACHE_NOT_FRESH" in s
    assert "BLOCKED_F2_PROTECTED_CACHE_SELECTED" in s

def test_f2_exactly_one_connect_call_site():
    s = source()
    assert s.count("client.connect(") == 1

def test_f2_observes_system_events_and_state():
    s = source()
    assert "onConnect()" in s
    assert "onDisconnect()" in s
    assert "client.isConnected()" in s
    assert "CONNECT_CALL_START_UTC" in s
    assert "CONNECT_CALL_RETURN_UTC" in s
    assert "CONNECT_CALL_DURATION_MS" in s
    assert "CONNECT_EXCEPTION_CLASS" in s

def test_f2_forbidden_history_strategy_market_and_trading_tokens_absent():
    s = source()
    forbidden = [
        "startStrategy", "IStrategy", "IHistory", "getHistory(", "getTicks(",
        "readTicks(", "setSubscribedInstruments(", "submitOrder(", "getEngine("
    ]
    assert all(token not in s for token in forbidden)

def test_f2_no_retry_or_reconnect_loop():
    s = source().lower()
    assert "reconnect" not in s
    assert "retry" not in s

def test_f2_disconnect_present_once():
    s = source()
    assert s.count("client.disconnect()") == 1

def test_f2_credentials_only_from_environment():
    s = source()
    assert 'System.getenv("JFOREX_USER")' in s
    assert 'System.getenv("JFOREX_PASSWORD")' in s
    assert "password" not in s.split('System.getenv("JFOREX_PASSWORD")',1)[1].lower() or "println" not in s.split('System.getenv("JFOREX_PASSWORD")',1)[1].lower()

def test_f2_pom_pins_sdk():
    p = POM.read_text(encoding="utf-8") if POM.exists() else ""
    assert "<jforex.sdk.version>3.6.51</jforex.sdk.version>" in p
    assert "<mainClass>atds.jf02.JF02ConnectionProbe</mainClass>" in p

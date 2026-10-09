from pathlib import Path

JAVA = Path("tools/jforex_jf02/src/main/java/atds/jf02/JF02HistoryRead.java")


def source() -> str:
    return JAVA.read_text(encoding="utf-8")


def test_cr1_uses_synchronous_getticks_only():
    s = source()
    assert ".getTicks(" in s
    assert ".readTicks(" not in s


def test_cr1_preserves_frozen_instrument_and_interval():
    s = source()
    assert 'INSTRUMENT_TEXT = "USATECH.IDX/USD"' in s
    assert "FROM_MS = 1759327200000L" in s
    assert "TO_MS = 1759330799999L" in s


def test_cr1_classifies_timeout_separately():
    s = source()
    assert "BLOCKED_JF02_HISTORY_NETWORK_TIMEOUT" in s
    assert "SocketTimeoutException" in s
    assert "BLOCKED_JF02_HISTORY_LOAD_FAILURE" in s


def test_cr1_keeps_empty_response_distinct_from_transport_failure():
    s = source()
    assert 'ticks.isEmpty()' in s
    assert 'fail("BLOCKED_JF02_EMPTY_RESPONSE")' in s


def test_cr1_preserves_no_sort_dedup_repair_semantics():
    evidence = Path("GOVERNANCE/E1-TD-03C-JF02-CONTROLLED-JFOREX-HISTORY-EVIDENCE-QUALIFICATION-CONTRACT-V0.1.json").read_text(encoding="utf-8")
    assert '"sorting": false' in evidence
    assert '"deduplication": false' in evidence
    assert '"repair": false' in evidence


def test_cr1_does_not_add_trading_api_calls():
    s = source()
    forbidden = [".submitOrder(", "getEngine().submitOrder", "IEngine.OrderCommand"]
    assert all(token not in s for token in forbidden)

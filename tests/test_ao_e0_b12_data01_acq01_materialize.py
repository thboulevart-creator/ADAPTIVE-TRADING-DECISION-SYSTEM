import pytest
from tools.ao_e0_b12_data01_acq01_materialize import build_ap0_rows,MaterializationError
from tools.e1_03_h1_dataset_identity import derive_h1_dataset

def ticks(minutes=60,start=0):
    out=[]
    for m in range(minutes):
        t=start+m*60000+1000
        out.append({"timestamp":t,"bidPrice":100.0+m/1000,"askPrice":100.2+m/1000})
    return out

def test_01_ap0_exact_minute_semantics():
    r=build_ap0_rows(ticks(2))
    assert len(r)==2 and r[0]["tick_count"]==1 and r[0]["segment_start"] is True and r[1]["segment_start"] is False

def test_02_bid_ask_domain_blocks():
    with pytest.raises(MaterializationError,match="BID_ASK_DOMAIN"):
        build_ap0_rows([{"timestamp":1,"bidPrice":2,"askPrice":1}])

def test_03_order_blocks():
    with pytest.raises(MaterializationError,match="TIMESTAMP_ORDER"):
        build_ap0_rows([{"timestamp":2,"bidPrice":1,"askPrice":2},{"timestamp":1,"bidPrice":1,"askPrice":2}])

def test_04_gap_creates_segment():
    r=build_ap0_rows([{"timestamp":1000,"bidPrice":1,"askPrice":2},{"timestamp":121001,"bidPrice":1,"askPrice":2}])
    assert r[-1]["segment_id"]==1 and r[-1]["segment_start"] is True and r[-1]["gap_before_ms"]==120001

def test_05_no_forward_fill():
    r=build_ap0_rows([{"timestamp":1000,"bidPrice":1,"askPrice":2},{"timestamp":121001,"bidPrice":1,"askPrice":2}])
    assert [x["minute_start_ms_utc"] for x in r]==[0,120000]

def test_06_h1_requires_all_60_minutes():
    a=build_ap0_rows(ticks(59))
    h=derive_h1_dataset(a,raw_window_start_ms=0,raw_window_end_ms=3600000)
    assert h["status"]=="PASS" and h["manifest"]["accepted_h1_rows"]==0

def test_07_h1_exact_60_minutes():
    a=build_ap0_rows(ticks(60))
    h=derive_h1_dataset(a,raw_window_start_ms=0,raw_window_end_ms=3600000)
    assert h["status"]=="PASS" and h["manifest"]["accepted_h1_rows"]==1

def test_08_no_strategy_or_pnl_fields():
    r=build_ap0_rows(ticks(1))[0]
    assert "signal" not in r and "pnl" not in r and "return" not in r

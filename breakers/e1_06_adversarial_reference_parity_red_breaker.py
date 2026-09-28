from __future__ import annotations

import copy
import importlib.util
import inspect
import math
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(os.environ.get("E1_06_TARGET_PATH", ROOT / "tools/e1_06_adversarial_parity.py"))
REFERENCE = ROOT / "tools/e1_06_independent_reference.py"
E105 = ROOT / "tools/e1_05_minimal_momentum_runner.py"
E104 = ROOT / "tools/e1_04_execution_cost_model.py"

HOUR = 3_600_000
OOS = 1_748_131_200_000
BASE = OOS - 30 * HOUR

EXPECTED_CONTRACT = "ATDS_E1_06_ADVERSARIAL_REFERENCE_PARITY_V0_1"
REFERENCE_CONTRACT = "ATDS_E1_06_INDEPENDENT_REFERENCE_V0_1"

EXPECTED_COST_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}

FORBIDDEN_CLAIMS = {
    "STRATEGY_QUALIFIED",
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
}


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _target():
    if not TARGET.is_file():
        pytest.fail("E1_06_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    m = _load(TARGET, "e106_target")
    assert m.CONTRACT == EXPECTED_CONTRACT
    assert m.PNL_SCOPE == EXPECTED_COST_SCOPE
    assert set(m.FORBIDDEN_CLAIMS) == FORBIDDEN_CLAIMS
    assert callable(m.qualify_fixture)
    return m


def _deps():
    r = _load(REFERENCE, "e106_reference")
    e105 = _load(E105, "e105_runtime")
    e104 = _load(E104, "e104_runtime")
    assert r.CONTRACT == REFERENCE_CONTRACT
    return r, e105, e104


def _rows(n=23, *, start=BASE, block=7):
    rows=[]
    for i in range(n):
        close=100.0
        if i==20: close=110.0
        elif i==21: close=90.0
        elif i==22: close=100.0
        rows.append({
            "h1_start_ms_utc":start+i*HOUR,
            "source_segment_id":11,
            "continuity_block_id":block,
            "continuity_ordinal":i,
            "mid_close":close,
        })
    return rows


def _ticks(rows):
    return [
        {"timestamp_ms":rows[20]["h1_start_ms_utc"]+HOUR,"bid":100.0,"ask":101.0,"continuity_status":"OK"},
        {"timestamp_ms":rows[21]["h1_start_ms_utc"]+HOUR,"bid":104.0,"ask":105.0,"continuity_status":"OK"},
        {"timestamp_ms":rows[22]["h1_start_ms_utc"]+HOUR,"bid":99.0,"ask":100.0,"continuity_status":"OK"},
    ]


def _qual(rows=None,ticks=None,reference=None):
    q=_target()
    r,e105,e104=_deps()
    if rows is None: rows=_rows()
    if ticks is None: ticks=_ticks(rows)
    if reference is None: reference=r
    return q.qualify_fixture(
        rows,
        raw_ticks=ticks,
        e1_05_runtime=e105,
        e1_04_runtime=e104,
        reference_runtime=reference,
        initial_position=0,
    )


def test_q6_01_baseline_full_parity():
    out=_qual()
    assert out["status"]=="PASS"
    assert all(out["parity"].values())


def test_q6_02_signal_direction_parity():
    out=_qual()
    actual=[x["signal"] for x in out["runner"]["records"][-3:]]
    assert actual==["LONG","SHORT","NEUTRAL"]
    assert actual==[x["signal"] for x in out["reference"]["records"][-3:]]


def test_q6_03_signal_timestamp_parity():
    out=_qual()
    a=[x["h1_start_ms_utc"] for x in out["runner"]["records"][-3:]]
    b=[x["h1_start_ms_utc"] for x in out["reference"]["records"][-3:]]
    assert a==b


def test_q6_04_execution_timestamp_parity():
    out=_qual()
    a=[e["timestamp_ms"] for r in out["runner"]["records"][-3:] for e in r["execution"]["events"]]
    b=[e["timestamp_ms"] for r in out["reference"]["records"][-3:] for e in r["execution"]["events"]]
    assert a==b


def test_q6_05_bid_ask_side_and_price_parity():
    out=_qual()
    ev=[r["execution"]["events"] for r in out["runner"]["records"][-3:]]
    assert ev[0][0]["price_side"]=="ASK" and ev[0][0]["price"]==101.0
    assert [x["price_side"] for x in ev[1]]==["BID","BID"]
    assert [x["price"] for x in ev[1]]==[104.0,104.0]
    assert ev[2][0]["price_side"]=="ASK" and ev[2][0]["price"]==100.0


def test_q6_06_position_transition_parity_including_reversal():
    out=_qual()
    a=out["runner"]["transitions"][-3:]
    b=out["reference"]["transitions"][-3:]
    assert a==b
    assert [(x["before"],x["after"]) for x in a]==[(0,1),(1,-1),(-1,0)]


def test_q6_07_closed_trade_count_parity():
    out=_qual()
    assert out["runner"]["trade_count"]==2
    assert out["runner"]["trade_count"]==out["reference"]["trade_count"]


def test_q6_08_realized_pnl_components_and_aggregate_parity():
    out=_qual()
    assert out["runner"]["pnl_components"]==[3.0,4.0]
    assert out["runner"]["aggregate_pnl"]==7.0
    assert out["runner"]["pnl_components"]==out["reference"]["pnl_components"]
    assert out["runner"]["aggregate_pnl"]==out["reference"]["aggregate_pnl"]


def test_q6_09_spread_is_intrinsic_in_synthetic_pnl():
    rows=_rows(22)
    rows[20]["mid_close"]=110.0
    rows[21]["mid_close"]=100.0
    ticks=[
        {"timestamp_ms":rows[20]["h1_start_ms_utc"]+HOUR,"bid":100.0,"ask":101.0,"continuity_status":"OK"},
        {"timestamp_ms":rows[21]["h1_start_ms_utc"]+HOUR,"bid":100.0,"ask":101.0,"continuity_status":"OK"},
    ]
    out=_qual(rows,ticks)
    assert out["runner"]["pnl_components"]==[-1.0]
    assert out["runner"]["aggregate_pnl"]==-1.0


def test_q6_10_lookahead_mutation_cannot_change_prior_record():
    rows=_rows()
    out1=_qual(rows,_ticks(rows))
    mutated=copy.deepcopy(rows)
    mutated.append({
        "h1_start_ms_utc":rows[-1]["h1_start_ms_utc"]+HOUR,
        "source_segment_id":11,
        "continuity_block_id":7,
        "continuity_ordinal":23,
        "mid_close":1_000_000.0,
    })
    ticks=_ticks(rows)+[{"timestamp_ms":mutated[-1]["h1_start_ms_utc"]+HOUR,"bid":1.0,"ask":2.0,"continuity_status":"OK"}]
    out2=_qual(mutated,ticks)
    assert out1["runner"]["records"][:23]==out2["runner"]["records"][:23]


def test_q6_11_same_bar_event_cannot_execute():
    rows=_rows(21)
    ticks=[
        {"timestamp_ms":rows[20]["h1_start_ms_utc"]+HOUR-1,"bid":1.0,"ask":2.0,"continuity_status":"OK"},
        {"timestamp_ms":rows[20]["h1_start_ms_utc"]+HOUR,"bid":100.0,"ask":101.0,"continuity_status":"OK"},
    ]
    out=_qual(rows,ticks)
    e=out["runner"]["records"][-1]["execution"]["events"][0]
    assert e["price"]==101.0


def test_q6_12_first_admissible_post_h1_tick_selected():
    rows=_rows(21)
    end=rows[20]["h1_start_ms_utc"]+HOUR
    ticks=[
        {"timestamp_ms":end,"bid":100.0,"ask":None,"continuity_status":"OK"},
        {"timestamp_ms":end+1,"bid":101.0,"ask":102.0,"continuity_status":"OK"},
        {"timestamp_ms":end+2,"bid":103.0,"ask":104.0,"continuity_status":"OK"},
    ]
    out=_qual(rows,ticks)
    e=out["runner"]["records"][-1]["execution"]["events"][0]
    assert e["timestamp_ms"]==end+1 and e["price"]==102.0


def test_q6_13_forbidden_gap_boundary_not_crossed():
    rows=_rows(21)
    end=rows[20]["h1_start_ms_utc"]+HOUR
    ticks=[
        {"timestamp_ms":end,"bid":100.0,"ask":101.0,"continuity_status":"FORBIDDEN_BOUNDARY"},
        {"timestamp_ms":end+1,"bid":102.0,"ask":103.0,"continuity_status":"OK"},
    ]
    out=_qual(rows,ticks)
    assert out["runner"]["records"][-1]["execution"]=={"status":"NOT_EXECUTED","events":[]}


def test_q6_14_warmup_does_not_leak_across_block():
    rows=_rows(20)
    rows.append({
        "h1_start_ms_utc":rows[-1]["h1_start_ms_utc"]+HOUR,
        "source_segment_id":12,
        "continuity_block_id":8,
        "continuity_ordinal":0,
        "mid_close":200.0,
    })
    out=_qual(rows,[])
    assert out["runner"]["records"][-1]["signal"]=="UNDEFINED"


def test_q6_15_oos_boundary_does_not_reset_same_block_warmup():
    start=OOS-20*HOUR
    rows=_rows(21,start=start)
    out=_qual(rows,[])
    assert rows[-1]["h1_start_ms_utc"]==OOS
    assert out["runner"]["records"][-1]["signal"]=="LONG"


def test_q6_16_reversal_close_is_not_double_counted():
    rows=_rows(22)
    ticks=_ticks(_rows())[:2]
    out=_qual(rows,ticks)
    assert len(out["runner"]["records"][-1]["execution"]["events"])==2
    assert out["runner"]["trade_count"]==1
    assert out["runner"]["pnl_components"]==[3.0]


def test_q6_17_missing_price_not_executed_no_fabricated_pnl():
    rows=_rows(21)
    end=rows[20]["h1_start_ms_utc"]+HOUR
    ticks=[{"timestamp_ms":end,"bid":100.0,"ask":None,"continuity_status":"OK"}]
    out=_qual(rows,ticks)
    assert out["runner"]["records"][-1]["execution"]["status"]=="NOT_EXECUTED"
    assert out["runner"]["pnl_components"]==[]


def test_q6_18_deterministic_replay_exact():
    assert _qual()==_qual()


def test_q6_19_cost_scope_exactly_e104_authorized():
    out=_qual()
    assert out["runner"]["pnl_scope"]==EXPECTED_COST_SCOPE
    assert out["reference"]["pnl_scope"]==EXPECTED_COST_SCOPE


def test_q6_20_reference_is_independent():
    r,_,_=_deps()
    src=inspect.getsource(r)
    forbidden=("e1_04","e1_05","execute_transition","run_momentum_runner")
    assert not any(token in src.lower() for token in forbidden)


def test_q6_21_tampered_reference_aggregate_is_detected():
    r,_,_=_deps()
    class Tampered:
        CONTRACT=r.CONTRACT
        PNL_SCOPE=r.PNL_SCOPE
        FORBIDDEN_CLAIMS=r.FORBIDDEN_CLAIMS
        @staticmethod
        def reference_run(*args,**kwargs):
            out=r.reference_run(*args,**kwargs)
            out["aggregate_pnl"]+=1.0
            return out
    out=_qual(reference=Tampered)
    assert out["status"]=="FAIL"
    assert out["parity"]["aggregate_realized_pnl"] is False


def test_q6_22_forbidden_claims_absent():
    q=_target()
    assert set(q.FORBIDDEN_CLAIMS)==FORBIDDEN_CLAIMS
    out=_qual()
    keys=set(out.keys())|set(out["runner"].keys())|set(out["reference"].keys())
    assert not (FORBIDDEN_CLAIMS & keys)

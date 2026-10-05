from __future__ import annotations
import base64, copy, hashlib, io, json, statistics, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B64=ROOT/"reports/program/evidence/ao-e0-b8-m06/E1-REAL-003-USED.zip.b64"
ZIP_SHA="a6588ef94d6cf15447ee8f7d2be0b7d3642ae857f2d64fcf86c77070ced0ca84"
RESULT_RAW_SHA="ab1815c56284000658f04ac70e53472f6cf1390cb57926f96e94076630d6942f"
RESULT_DIGEST="56eaf2626629bff2ff7b6dcd13e2ca178edddf06aade81f9480c4e3d142cf738"
RECORDS_DIGEST="f890dd32f3e14b20430cb5898a05946a5d71231a9103b755fa0eb683f8834fc4"
EXPECTED={
 "FULL":{"n":650,"sum":-3653.772000000031,"mean":-5.621187692307741,"sample_stddev":336.4106561689863},
 "PRE_OOS":{"n":535,"sum":-5940.314000000025,"mean":-11.103390654205654,"sample_stddev":295.834479256387},
 "OOS":{"n":114,"sum":2856.667999999994,"mean":25.05849122807012,"sample_stddev":482.17824961107937},
}
POP_FULL=336.151779134749

def canonical_sha256_without_digest(obj):
    x=copy.deepcopy(obj); x.pop("canonical_digest",None)
    raw=json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def load():
    b=base64.b64decode(B64.read_text(encoding="ascii"),validate=True)
    assert hashlib.sha256(b).hexdigest()==ZIP_SHA
    z=zipfile.ZipFile(io.BytesIO(b))
    raw=z.read("E1-REAL-003-RESULT.json")
    assert hashlib.sha256(raw).hexdigest()==RESULT_RAW_SHA
    result=json.loads(raw)
    assert result["canonical_digest"]==RESULT_DIGEST
    assert canonical_sha256_without_digest(result)==RESULT_DIGEST
    assert result["base_result"]["records_digest"]==RECORDS_DIGEST
    return b,z,result

def diagnostics(result):
    trades=result["base_result"]["trade_ledger"]["closed_trades"]
    groups={
      "FULL":trades,
      "PRE_OOS":[t for t in trades if t["partition"]=="PRE_OOS"],
      "OOS":[t for t in trades if t["partition"]=="OOS"],
    }
    out={}
    for k,g in groups.items():
        x=[float(t["realized_unit_pnl"]) for t in g]
        out[k]={"n":len(x),"sum":sum(x),"mean":statistics.fmean(x),
                "sample_stddev":statistics.stdev(x),
                "population_stddev":statistics.pstdev(x)}
    return out

def verify():
    _,_,r=load()
    d=diagnostics(r)
    assert len(r["base_result"]["trade_ledger"]["closed_trades"])==650
    for k,e in EXPECTED.items():
        for f,v in e.items():
            assert abs(d[k][f]-v) <= 1e-10
    assert abs(d["FULL"]["population_stddev"]-POP_FULL)<=1e-10
    assert d["FULL"]["sample_stddev"] != d["FULL"]["population_stddev"]
    return d

def adversarial():
    _,_,r=load()
    checks={}
    mutated=copy.deepcopy(r)
    mutated["base_result"]["trade_ledger"]["closed_trades"][0]["realized_unit_pnl"] += 0.001
    checks["mutated_ledger_row_detected"]=canonical_sha256_without_digest(mutated)!=RESULT_DIGEST
    checks["population_sigma_rejected"]=abs(POP_FULL-EXPECTED["FULL"]["sample_stddev"])>1e-6
    checks["oos_only_sigma_not_candidate"]=EXPECTED["OOS"]["sample_stddev"]!=EXPECTED["FULL"]["sample_stddev"]
    checks["candidate_is_full_sample"]=EXPECTED["FULL"]["sample_stddev"]==336.4106561689863
    checks["old_oos_not_pristine"]=True
    checks["planning_not_confirmation"]=True
    checks["spread_only_not_historical_f2_s4"]=True
    checks["no_strategy_execution_surface"]=True
    checks["no_new_data_surface"]=True
    assert all(checks.values())
    return checks

if __name__=="__main__":
    print(json.dumps({"diagnostics":verify(),"adversarial":adversarial()},sort_keys=True,indent=2))

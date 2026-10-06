from __future__ import annotations
import hashlib, json, os, tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROVIDER="DUKASCOPY"
TRANSPORT="JETTA_DUKASCOPY_TICKS_API"
INSTRUMENT="USATECH.IDX-USD"
TRANSFORMATION_ID="DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1"
MULTIPLIER="0.001"
RAW_FORWARD_FIRST_HOUR_START_MS=1791280800000
FORWARD_DECISION_START_MS=1791284400000
OLD_E1_OOS_MAX_MS=1779667199963
REQUIRED_CLOSED_TRADES=58927
H1_IDENTITY="USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
AP0_IDENTITY="USTECH_PROFILE_MINUTE_CORE_V0_1"

class ACQ02Blocked(RuntimeError):
    pass

def canonical_bytes(obj:Any)->bytes:
    return (json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)+"\n").encode()

def sha256_bytes(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def parse_iso_hour(s:str)->int:
    dt=datetime.strptime(s,"%Y-%m-%dT%H:00:00Z").replace(tzinfo=timezone.utc)
    return int(dt.timestamp()*1000)

def validate_runtime_policy(p:dict)->None:
    expected={
      "provider":PROVIDER,"instrument":INSTRUMENT,"transport":TRANSPORT,
      "multiplier":MULTIPLIER,"transformation_id":TRANSFORMATION_ID,
      "raw_forward_first_hour_start_ms":RAW_FORWARD_FIRST_HOUR_START_MS,
      "forward_decision_start_ms":FORWARD_DECISION_START_MS,
      "warmup_is_evidence":False,"object_hash_required":True,"interval_identity_required":True,
      "append_only":True,"ledger_chain_required":True,"manifest_deterministic":True,
      "ap0_forward_fill":False,"ap0_volume_used":False,"ap0_returns_calculated":False,
      "ap0_strategy_calculated":False,"ap0_pnl_calculated":False,
      "h1_identity":H1_IDENTITY,"h1_strategy_calculated":False,
      "human_forward_prices_visible":False,"human_performance_visible":False,
      "b12_open":False,"pipe01_first_read_invoked":False,"owner02_real_plan_invoked":False,
      "owner02_real_result_invoked":False,"final_digest_placeholder":False,
      "final_instance_complete_fields_only":True,"terminal_count_from_performance":False,
      "optional_stop_pnl":False,"optional_stop_ci":False,"old_e1_oos_inserted":False,
      "new_external_cost":False,"missing_intervals_allowed":False,
      "duplicate_interval_conflict_allowed":False,"timestamps_strict":True,
      "ask_ge_bid":True,"ap0_h1_bound_to_raw":True,"rolling_is_final":False,
      "data01_ready":False,"strategy_qualified_claim":False,
      "trading_authority":False,"capital_authority":False
    }
    for k,v in expected.items():
        if p.get(k)!=v:
            raise ACQ02Blocked("BLOCKED_"+k.upper())
    if p.get("forward_start_shifted_to_acquisition_time",False):
        raise ACQ02Blocked("BLOCKED_FORWARD_BOUNDARY_SHIFT")
    if p.get("source_semantic_drift",False):
        raise ACQ02Blocked("BLOCKED_SOURCE_SEMANTIC_DRIFT")

def decode_jetta(raw:bytes)->list[dict]:
    try:
        o=json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ACQ02Blocked("BLOCKED_RAW_JSON") from exc
    required=("timestamp","multiplier","times","bid","ask","bids","asks","bidVolumes","askVolumes")
    if any(k not in o for k in required):
        raise ACQ02Blocked("BLOCKED_RAW_SCHEMA")
    if str(o["multiplier"])!=MULTIPLIER:
        raise ACQ02Blocked("BLOCKED_SOURCE_SEMANTIC_DRIFT")
    n=len(o["times"])
    if any(len(o[k])!=n for k in ("bids","asks","bidVolumes","askVolumes")):
        raise ACQ02Blocked("BLOCKED_RAW_ARRAY_LENGTH")
    if n==0:
        return []
    elapsed=0
    bid=int(round(float(o["bid"])*1000))
    ask=int(round(float(o["ask"])*1000))
    out=[]
    last=None
    for i,d in enumerate(o["times"]):
        elapsed+=int(d)
        if i>0:
            bid+=int(o["bids"][i]); ask+=int(o["asks"][i])
        ts=int(o["timestamp"])+elapsed
        if last is not None and ts<=last:
            raise ACQ02Blocked("BLOCKED_TIMESTAMP_DISORDER")
        if ask<bid:
            raise ACQ02Blocked("BLOCKED_ASK_LT_BID")
        out.append({"timestamp_ms":ts,"bid_milli":bid,"ask_milli":ask})
        last=ts
    return out

def _ledger_path(root:Path)->Path:
    return root/"ledger"/"events.jsonl"

def read_ledger(root:Path)->list[dict]:
    p=_ledger_path(root)
    if not p.exists(): return []
    rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    prev="GENESIS"
    seen=set()
    for row in rows:
        body={k:v for k,v in row.items() if k!="event_digest"}
        if row.get("previous_digest")!=prev:
            raise ACQ02Blocked("BLOCKED_LEDGER_CHAIN")
        if sha256_bytes(canonical_bytes(body))!=row.get("event_digest"):
            raise ACQ02Blocked("BLOCKED_MUTABLE_HISTORICAL_LEDGER_EVENT")
        key=(row["interval_start_utc"],row["interval_end_utc"])
        if key in seen: raise ACQ02Blocked("BLOCKED_INTERVAL_DUPLICATED_INCONSISTENTLY")
        seen.add(key); prev=row["event_digest"]
    return rows

def seal_raw_object(root:Path,*,interval_start_utc:str,interval_end_utc:str,raw:bytes,
                    acquisition_time_utc:str,classification:str)->dict:
    root=Path(root)
    if not interval_start_utc or not interval_end_utc:
        raise ACQ02Blocked("BLOCKED_MISSING_INTERVAL_IDENTITY")
    if classification not in ("WARMUP","FORWARD_EVIDENCE"):
        raise ACQ02Blocked("BLOCKED_CLASSIFICATION")
    start_ms=parse_iso_hour(interval_start_utc)
    if classification=="FORWARD_EVIDENCE" and start_ms<RAW_FORWARD_FIRST_HOUR_START_MS:
        raise ACQ02Blocked("BLOCKED_WRONG_FORWARD_START")
    if classification=="WARMUP" and start_ms>=RAW_FORWARD_FIRST_HOUR_START_MS:
        raise ACQ02Blocked("BLOCKED_WARMUP_INCLUDED_AS_EVIDENCE")
    rows=decode_jetta(raw)
    digest=sha256_bytes(raw)
    rel=f"raw/{interval_start_utc[:13].replace(':','')}.json"
    path=root/rel
    path.parent.mkdir(parents=True,exist_ok=True)
    ledger=read_ledger(root)
    existing=[x for x in ledger if x["interval_start_utc"]==interval_start_utc and x["interval_end_utc"]==interval_end_utc]
    if existing:
        if existing[0]["sha256"]==digest:
            if path.exists() and sha256_bytes(path.read_bytes())==digest:
                return {"status":"REPRODUCIBILITY_ONLY","event":existing[0]}
        raise ACQ02Blocked("BLOCKED_SOURCE_OBJECT_MUTATION")
    if path.exists():
        if sha256_bytes(path.read_bytes())!=digest:
            raise ACQ02Blocked("BLOCKED_SOURCE_OBJECT_MUTATION")
        raise ACQ02Blocked("BLOCKED_LEDGER_MISSING_FOR_EXISTING_OBJECT")
    path.write_bytes(raw)
    prev="GENESIS" if not ledger else ledger[-1]["event_digest"]
    event={
      "source_id":PROVIDER,"instrument_id":INSTRUMENT,"transport_id":TRANSPORT,
      "transformation_id":TRANSFORMATION_ID,"classification":classification,
      "interval_start_utc":interval_start_utc,"interval_end_utc":interval_end_utc,
      "acquisition_time_utc":acquisition_time_utc,"size_bytes":len(raw),"sha256":digest,
      "schema_signature":sha256_bytes(canonical_bytes(sorted(json.loads(raw.decode()).keys()))),
      "row_count":len(rows),
      "first_timestamp":None if not rows else rows[0]["timestamp_ms"],
      "last_timestamp":None if not rows else rows[-1]["timestamp_ms"],
      "relative_path":rel,"previous_digest":prev
    }
    event["event_digest"]=sha256_bytes(canonical_bytes(event))
    lp=_ledger_path(root); lp.parent.mkdir(parents=True,exist_ok=True)
    with lp.open("a",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(event,sort_keys=True,separators=(",",":"))+"\n")
    return {"status":"SEALED","event":event}

def rolling_raw_manifest(root:Path)->dict:
    ledger=read_ledger(Path(root))
    rows=sorted(ledger,key=lambda x:(x["interval_start_utc"],x["interval_end_utc"]))
    inventory=[{
      "classification":x["classification"],"interval_start_utc":x["interval_start_utc"],
      "interval_end_utc":x["interval_end_utc"],"relative_path":x["relative_path"],
      "size_bytes":x["size_bytes"],"sha256":x["sha256"],"row_count":x["row_count"]
    } for x in rows]
    inv_digest=sha256_bytes(b"".join(canonical_bytes(x) for x in inventory))
    manifest={
      "schema":"ATDS_ACQ02_RAW_FORWARD_MANIFEST_V0_1","source":PROVIDER,
      "transport":TRANSPORT,"instrument":INSTRUMENT,"transformation_id":TRANSFORMATION_ID,
      "warmup_objects":sum(x["classification"]=="WARMUP" for x in inventory),
      "forward_evidence_objects":sum(x["classification"]=="FORWARD_EVIDENCE" for x in inventory),
      "inventory":inventory,"raw_forward_inventory_digest":inv_digest,
      "b12":"CLOSED","performance_bearing_read":False
    }
    manifest["raw_forward_manifest_sha256"]=sha256_bytes(canonical_bytes(manifest))
    return manifest

def materialize_ap0_from_ledger(root:Path)->dict:
    root=Path(root); ledger=read_ledger(root)
    ticks=[]
    for ev in ledger:
        rows=decode_jetta((root/ev["relative_path"]).read_bytes())
        for r in rows:
            r["classification"]=ev["classification"]
            ticks.append(r)
    ticks.sort(key=lambda r:r["timestamp_ms"])
    if any(ticks[i]["timestamp_ms"]>=ticks[i+1]["timestamp_ms"] for i in range(len(ticks)-1)):
        raise ACQ02Blocked("BLOCKED_TIMESTAMP_DISORDER")
    by={}
    prev_ts=None; segment=0
    for r in ticks:
        ts=r["timestamp_ms"]; minute=(ts//60000)*60000
        if prev_ts is not None and ts-prev_ts>60000: segment+=1
        mid=(r["bid_milli"]+r["ask_milli"])/2000.0
        spread=(r["ask_milli"]-r["bid_milli"])/1000.0
        x=by.setdefault(minute,{"minute_start_ms_utc":minute,"first_tick_ms":ts,"last_tick_ms":ts,"tick_count":0,
             "segment_id":segment,"segment_start":prev_ts is None or (ts-prev_ts>60000 if prev_ts is not None else True),
             "gap_before_ms":None if prev_ts is None else (ts-prev_ts if ts-prev_ts>60000 else None),
             "mid_open":mid,"mid_high":mid,"mid_low":mid,"mid_close":mid,"spread_sum":0.0,"spread_min":spread,"spread_max":spread})
        x["last_tick_ms"]=ts; x["tick_count"]+=1; x["mid_high"]=max(x["mid_high"],mid); x["mid_low"]=min(x["mid_low"],mid); x["mid_close"]=mid
        x["spread_sum"]+=spread; x["spread_min"]=min(x["spread_min"],spread); x["spread_max"]=max(x["spread_max"],spread)
        prev_ts=ts
    rows=[]
    for minute in sorted(by):
        x=by[minute]; x["spread_mean"]=x.pop("spread_sum")/x["tick_count"]; rows.append(x)
    payload={"schema":"ATDS_ACQ02_AP0_STRUCTURAL_V0_1","identity":AP0_IDENTITY,
             "source_raw_manifest_sha256":rolling_raw_manifest(root)["raw_forward_manifest_sha256"],
             "forward_fill":False,"gap_aware":True,"volume_used":False,"returns_calculated":False,
             "strategy_calculated":False,"pnl_calculated":False,"rows":rows}
    payload["ap0_forward_manifest_sha256"]=sha256_bytes(canonical_bytes(payload))
    return payload

def materialize_h1_from_ap0(ap0:dict,raw_window_start_ms:int,raw_window_end_ms:int)->dict:
    from tools.e1_03_h1_dataset_identity import derive_h1_dataset, canonical_stream_sha256
    if ap0.get("identity")!=AP0_IDENTITY or ap0.get("strategy_calculated") or ap0.get("pnl_calculated"):
        raise ACQ02Blocked("BLOCKED_AP0_SEMANTIC_DRIFT")
    result=derive_h1_dataset(ap0["rows"],raw_window_start_ms=raw_window_start_ms,raw_window_end_ms=raw_window_end_ms)
    if result.get("status")!="PASS":
        raise ACQ02Blocked("BLOCKED_H1_SEMANTIC_DRIFT")
    rows=result["rows"]
    return {
      "schema":"ATDS_ACQ02_H1_STRUCTURAL_V0_1","identity":H1_IDENTITY,
      "source_ap0_manifest_sha256":ap0["ap0_forward_manifest_sha256"],
      "strategy_calculated":False,"pnl_calculated":False,
      "h1_row_count":len(rows),"h1_first_boundary":None if not rows else rows[0]["h1_start_ms_utc"],
      "h1_last_boundary":None if not rows else rows[-1]["h1_start_ms_utc"],
      "segment_count":result["manifest"]["continuity_blocks"],
      "h1_forward_stream_sha256":canonical_stream_sha256(rows),"rows":rows
    }

FINAL_FIELDS=("raw_forward_manifest_sha256","raw_forward_inventory_digest","ap0_forward_manifest_sha256",
              "h1_forward_stream_sha256","exact_first_evidence_decision_time","exact_terminal_decision_time",
              "exact_closed_trade_count","non_overlap_attestation")

def rolling_readiness(*,raw_manifest:dict,ap0:dict,h1:dict,terminal_count_info:dict|None=None)->dict:
    base={
      "raw_forward_manifest_sha256":raw_manifest["raw_forward_manifest_sha256"],
      "raw_forward_inventory_digest":raw_manifest["raw_forward_inventory_digest"],
      "ap0_forward_manifest_sha256":ap0["ap0_forward_manifest_sha256"],
      "h1_forward_stream_sha256":h1["h1_forward_stream_sha256"],
      "exact_first_evidence_decision_time":"2026-10-06T11:00:00Z",
      "non_overlap_attestation":{
        "old_e1_oos_max":"2026-05-24T23:59:59.963Z",
        "forward_evidence_start":"2026-10-06T11:00:00Z","temporal_non_overlap":True}
    }
    if terminal_count_info is None:
        return {"state":"WAIT_TERMINAL_COUNT_AUTHORITY","rolling_candidate":True,"exact_forward_instance":"NOT_YET_AVAILABLE",**base}
    if terminal_count_info.get("derived_from_performance"):
        raise ACQ02Blocked("BLOCKED_TERMINAL_COUNT_FROM_PERFORMANCE")
    n=int(terminal_count_info["exact_closed_trade_count"])
    if n<REQUIRED_CLOSED_TRADES:
        return {"state":"WAIT_NOT_READY","rolling_candidate":True,"exact_forward_instance":"NOT_YET_AVAILABLE",**base,
                "exact_closed_trade_count":n,"exact_terminal_decision_time":None}
    base["exact_closed_trade_count"]=n
    base["exact_terminal_decision_time"]=terminal_count_info["exact_terminal_decision_time"]
    if any(base.get(k) is None for k in FINAL_FIELDS):
        raise ACQ02Blocked("BLOCKED_FINAL_INSTANCE_INCOMPLETE")
    digest=sha256_bytes(canonical_bytes({k:base[k] for k in FINAL_FIELDS}))
    return {"state":"QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION","rolling_candidate":False,
            "exact_forward_instance":digest,**base}

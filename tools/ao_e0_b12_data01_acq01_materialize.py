from __future__ import annotations
import hashlib, json, math
from pathlib import Path
from typing import Any
import pyarrow as pa
import pyarrow.parquet as pq
from tools.e1_03_h1_dataset_identity import derive_h1_dataset, canonical_stream_sha256

CONTRACT="ATDS_AO_E0_B12_DATA01_ACQ01_STRUCTURAL_MATERIALIZER_V0_1"
MINUTE_MS=60_000
GAP_MS=60_000
REQUIRED_INPUT_FIELDS={"timestamp","bidPrice","askPrice"}

class MaterializationError(ValueError): pass

def sha256_path(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b=f.read(8*1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

def _validate_ticks(rows:list[dict[str,Any]])->None:
    prev=None
    for r in rows:
        if set(r)!=REQUIRED_INPUT_FIELDS: raise MaterializationError("INPUT_SCHEMA")
        ts=int(r["timestamp"]); bid=float(r["bidPrice"]); ask=float(r["askPrice"])
        if not math.isfinite(bid) or not math.isfinite(ask) or bid<=0 or ask<=0 or ask<bid:
            raise MaterializationError("BID_ASK_DOMAIN")
        if prev is not None and ts<=prev: raise MaterializationError("TIMESTAMP_ORDER")
        prev=ts

def build_ap0_rows(rows:list[dict[str,Any]])->list[dict[str,Any]]:
    _validate_ticks(rows)
    out=[]; pending=None; prev_tick=None; segment=0
    def flush():
        nonlocal pending
        if pending is None:return
        n=pending.pop("_n"); s=pending.pop("_spread_sum")
        pending["spread_mean"]=s/n
        out.append(pending); pending=None
    for r in rows:
        ts=int(r["timestamp"]); bid=float(r["bidPrice"]); ask=float(r["askPrice"])
        mid=(bid+ask)/2.0; spread=ask-bid; m=(ts//MINUTE_MS)*MINUTE_MS
        gap=None; segstart=False
        if prev_tick is None: segstart=True
        elif ts-prev_tick>GAP_MS:
            segment+=1; gap=ts-prev_tick; segstart=True
        if pending is None or pending["minute_start_ms_utc"]!=m:
            flush()
            pending={"minute_start_ms_utc":m,"first_tick_ms":ts,"last_tick_ms":ts,"tick_count":1,
                     "segment_id":segment,"segment_start":segstart,"gap_before_ms":gap,
                     "mid_open":mid,"mid_high":mid,"mid_low":mid,"mid_close":mid,
                     "spread_min":spread,"spread_max":spread,"_spread_sum":spread,"_n":1}
        else:
            if segstart or pending["segment_id"]!=segment:
                raise MaterializationError("SEGMENT_BOUNDARY_INSIDE_MINUTE")
            pending["last_tick_ms"]=ts; pending["tick_count"]+=1
            pending["mid_high"]=max(pending["mid_high"],mid); pending["mid_low"]=min(pending["mid_low"],mid)
            pending["mid_close"]=mid; pending["spread_min"]=min(pending["spread_min"],spread)
            pending["spread_max"]=max(pending["spread_max"],spread); pending["_spread_sum"]+=spread; pending["_n"]+=1
        prev_tick=ts
    flush()
    return out

def ap0_schema()->pa.Schema:
    return pa.schema([
      ("minute_start_ms_utc",pa.int64()),("first_tick_ms",pa.int64()),("last_tick_ms",pa.int64()),
      ("tick_count",pa.int64()),("segment_id",pa.int64()),("segment_start",pa.bool_()),
      ("gap_before_ms",pa.int64()),("mid_open",pa.float64()),("mid_high",pa.float64()),
      ("mid_low",pa.float64()),("mid_close",pa.float64()),("spread_mean",pa.float64()),
      ("spread_min",pa.float64()),("spread_max",pa.float64())
    ],metadata={
      b"dataset_identity":b"AO_E0_DATA01_FORWARD_AP0_V0_1",
      b"source_identity":b"DUKASCOPY_USATECH_FORWARD_CANDIDATE_V0_1",
      b"forward_fill":b"false",b"volumes_used":b"false",b"strategy_calculated":b"false",b"pnl_calculated":b"false"
    })

def materialize(input_json:Path,ap0_path:Path,h1_path:Path,*,raw_window_start_ms:int,raw_window_end_ms:int)->dict[str,Any]:
    data=json.loads(input_json.read_bytes())
    if not isinstance(data,list) or not data: raise MaterializationError("EMPTY_INPUT")
    ap0=build_ap0_rows(data)
    table=pa.Table.from_pylist(ap0,schema=ap0_schema())
    ap0_path.parent.mkdir(parents=True,exist_ok=True)
    if ap0_path.exists() or h1_path.exists(): raise MaterializationError("APPEND_ONLY_TARGET_EXISTS")
    pq.write_table(table,ap0_path,compression="snappy",use_dictionary=False,write_statistics=True)
    h1=derive_h1_dataset(ap0,raw_window_start_ms=raw_window_start_ms,raw_window_end_ms=raw_window_end_ms)
    if h1.get("status")!="PASS": raise MaterializationError("H1_DERIVATION_BLOCKED")
    h1_rows=h1["rows"]
    with h1_path.open("x",encoding="utf-8",newline="\n") as f:
        for row in h1_rows:f.write(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n")
    eligible_forward=sum(1 for r in h1_rows if r["h1_start_ms_utc"]>=1791280800000 and r["continuity_ordinal"]>=20)
    return {
      "schema":"ATDS_AO_E0_B12_DATA01_ACQ01_STRUCTURAL_MATERIALIZATION_RECEIPT_V0_1",
      "input_sha256":sha256_path(input_json),"input_rows":len(data),
      "ap0_sha256":sha256_path(ap0_path),"ap0_rows":len(ap0),
      "ap0_segments":0 if not ap0 else max(r["segment_id"] for r in ap0)+1,
      "ap0_first_minute_ms":ap0[0]["minute_start_ms_utc"] if ap0 else None,
      "ap0_last_minute_ms":ap0[-1]["minute_start_ms_utc"] if ap0 else None,
      "h1_file_sha256":sha256_path(h1_path),"h1_canonical_stream_sha256":canonical_stream_sha256(h1_rows),
      "h1_rows":len(h1_rows),"h1_continuity_blocks":h1["manifest"]["continuity_blocks"],
      "h1_first_ms":h1["manifest"]["first_admissible_h1"],"h1_last_ms":h1["manifest"]["last_admissible_h1"],
      "forward_h1_momentum_structurally_eligible_count":eligible_forward,
      "strategy_calculated":False,"pnl_calculated":False,"performance_observed":False
    }

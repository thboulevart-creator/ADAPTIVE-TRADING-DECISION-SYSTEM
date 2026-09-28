from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

CONTRACT = "ATDS_E1_08A_ONE_SHOT_REAL_E1_V0_1"
REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"
EXPERIMENT_ID = "ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0"
HYPOTHESIS_FAMILY = "MOMENTUM_V1"
SOURCE_DATASET_ID = "SOURCE_B_USTECH_PRICE_CORE_V0_1"
SOURCE_MANIFEST_SHA256 = "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
SOURCE_INVENTORY_DIGEST = "5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
H1_JSONL_SHA256 = "94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0"
H1_CANONICAL_STREAM_SHA256 = "15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"
OOS_START = "2025-05-25T00:00:00Z"
OOS_END = "2026-05-24T23:59:59.963Z"
OOS_START_MS = 1_748_131_200_000

PROTECTED_BLOBS = {
    "e1_01_e1_02_freeze_package_blob": "6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e",
    "e1_03_runtime_blob": "38d481755e00ce3c2ed9c66c4db710500ca0911a",
    "e1_04_runtime_blob": "15e72b8743e7726fc8b8bedd933cf7defe56413b",
    "e1_05_runtime_blob": "baad3bd7c2e810451737c89bf8f9bcabc17c5ba6",
    "e1_06_reference_blob": "25b01e6d31709f02f9c095262bfe78366e83003b",
    "e1_06_qualifier_blob": "0793adc08416563125f57a55c0d272d24bb4b3df",
    "e1_07_runtime_blob": "88ca1f1ae89d1a2cfac1ae35becb3ea6209755f5",
    "phase_21_decision_blob": "eecbfd4a7c214a2d09210f5b0490c06673619c24",
}

FORBIDDEN_CLAIMS = (
    "STRATEGY_QUALIFIED", "EDGE_CONFIRMED", "ROBUST", "CONFIRMATORY_RESULT",
    "BROKER_NET_PNL", "ALL_IN_COST_PROFITABILITY", "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM", "DECISION_AUTHORITY", "ACTION_AUTHORITY",
    "MT5_AUTHORIZED", "PAPER_AUTHORIZED", "BROKER_AUTHORIZED", "LIVE_AUTHORIZED",
    "CAPITAL_AUTHORIZED",
)

FULL_METRIC_KEYS = (
    "aggregate_realized_unit_pnl", "closed_trade_count", "win_count", "loss_count",
    "zero_pnl_count", "win_rate", "average_win", "average_loss",
    "expectancy_per_closed_trade", "realized_closed_trade_max_drawdown",
    "long_trade_count", "long_realized_pnl", "short_trade_count", "short_realized_pnl",
    "executed_transition_count", "not_executed_transition_count",
)
PARTITION_METRIC_KEYS = FULL_METRIC_KEYS[:-2]
COST_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}
EXPOSURE_KEYS = {
    "schema", "experiment_id", "hypothesis_family", "dataset_identity", "oos_start", "oos_end",
    "prior_oos_performance_exposure", "declaration_timestamp_utc", "human_authority_reference",
    "oos_clean", "canonical_digest",
}
AUTHORITY_KEYS = {
    "schema", "experiment_id", "run_id", "repository", "branch", "authorized_base_head",
    "authorized_base_tree", "executor_blob", "protected_bindings", "source_manifest_sha256",
    "h1_jsonl_sha256", "oos_start", "oos_end", "max_runs", "real_e1_run_authorized",
    "authorized_at_utc", "human_decision_reference", "canonical_digest",
}

class E108Error(Exception):
    pass

def canonical_sha256(value):
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def _blocked(reason,**extra):
    out={"status":"BLOCKED","reason":reason}; out.update(extra); return out

def _sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def verify_file_bytes(path,expected_sha256):
    p=Path(path)
    try:
        before=p.stat(); digest=_sha256_file(p); after=p.stat()
    except OSError:
        return _blocked("FILE_UNREADABLE")
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        return _blocked("FILE_CHANGED_DURING_READ")
    if digest!=expected_sha256:
        return _blocked("FILE_SHA256_MISMATCH",observed_sha256=digest)
    return {"status":"PASS","sha256":digest,"size_bytes":before.st_size}

def canonical_inventory_digest(files):
    h=hashlib.sha256()
    for row in files:
        h.update(f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n".encode("utf-8"))
    return h.hexdigest()

def verify_source_manifest(path,expected_manifest_sha256,expected_inventory_digest,expected_files):
    v=verify_file_bytes(path,expected_manifest_sha256)
    if v["status"]!="PASS": return v
    try: payload=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,UnicodeDecodeError,json.JSONDecodeError): return _blocked("SOURCE_MANIFEST_PARSE_ERROR")
    inv=payload.get("inventory") or {}; files=inv.get("files")
    if payload.get("schema")!="ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1" or payload.get("status")!="MANIFEST_COMPLETE":
        return _blocked("SOURCE_MANIFEST_CONTRACT_MISMATCH")
    if not isinstance(files,list) or len(files)!=expected_files or inv.get("parquet_files")!=expected_files:
        return _blocked("SOURCE_MANIFEST_FILE_COUNT_MISMATCH")
    try: observed=canonical_inventory_digest(files)
    except (KeyError,TypeError,ValueError): return _blocked("SOURCE_MANIFEST_FILE_RECORD_INVALID")
    if observed!=expected_inventory_digest: return _blocked("SOURCE_INVENTORY_DIGEST_MISMATCH")
    return {"status":"PASS","files":files,"inventory_digest":observed}

def adapt_tick_rows(rows):
    previous=None
    for row in rows:
        if not isinstance(row,dict) or not {"timestamp","bid_price","ask_price"}.issubset(row):
            raise E108Error("INVALID_SOURCE_TICK")
        try:
            ts=int(row["timestamp"]); bid=float(row["bid_price"]); ask=float(row["ask_price"])
        except (TypeError,ValueError,OverflowError): raise E108Error("INVALID_SOURCE_TICK")
        if not math.isfinite(bid) or not math.isfinite(ask): raise E108Error("INVALID_SOURCE_PRICE")
        if previous is not None and ts<=previous: raise E108Error("NON_INCREASING_SOURCE_TIMESTAMP")
        continuity="OK" if previous is None or ts-previous<=60_000 else "FORBIDDEN_BOUNDARY"
        previous=ts
        yield {"timestamp_ms":ts,"bid":bid,"ask":ask,"continuity_status":continuity}

def load_h1_jsonl(path,expected_file_sha256,expected_stream_sha256,e1_03_runtime):
    v=verify_file_bytes(path,expected_file_sha256)
    if v["status"]!="PASS": return v
    rows=[]
    try:
        with Path(path).open("r",encoding="utf-8") as f:
            for line in f:
                if line.strip(): rows.append(json.loads(line))
    except (OSError,UnicodeDecodeError,json.JSONDecodeError): return _blocked("H1_JSONL_PARSE_ERROR")
    try: stream=e1_03_runtime.canonical_stream_sha256(rows)
    except Exception: return _blocked("H1_STREAM_HASH_ERROR")
    if stream!=expected_stream_sha256: return _blocked("H1_CANONICAL_STREAM_MISMATCH")
    return {"status":"PASS","rows":rows,"file_sha256":expected_file_sha256,"stream_sha256":stream}

def build_exposure_declaration(*,declaration_timestamp_utc,human_authority_reference,prior_oos_performance_exposure="NONE_DECLARED"):
    out={"schema":"E1_OOS_EXPOSURE_DECLARATION_V0","experiment_id":EXPERIMENT_ID,
         "hypothesis_family":HYPOTHESIS_FAMILY,"dataset_identity":SOURCE_DATASET_ID,
         "oos_start":OOS_START,"oos_end":OOS_END,
         "prior_oos_performance_exposure":prior_oos_performance_exposure,
         "declaration_timestamp_utc":declaration_timestamp_utc,
         "human_authority_reference":human_authority_reference,
         "oos_clean":prior_oos_performance_exposure=="NONE_DECLARED"}
    out["canonical_digest"]=canonical_sha256(out); return out

def verify_exposure_declaration(value):
    try:
        if not isinstance(value,dict) or set(value)!=EXPOSURE_KEYS: return _blocked("EXPOSURE_SCHEMA_MISMATCH")
        unsigned={k:v for k,v in value.items() if k!="canonical_digest"}
        if canonical_sha256(unsigned)!=value["canonical_digest"]: return _blocked("EXPOSURE_DIGEST_MISMATCH")
        if value["schema"]!="E1_OOS_EXPOSURE_DECLARATION_V0" or value["experiment_id"]!=EXPERIMENT_ID:
            return _blocked("EXPOSURE_IDENTITY_MISMATCH")
        if value["hypothesis_family"]!=HYPOTHESIS_FAMILY or value["dataset_identity"]!=SOURCE_DATASET_ID:
            return _blocked("EXPOSURE_SCOPE_MISMATCH")
        if value["oos_start"]!=OOS_START or value["oos_end"]!=OOS_END: return _blocked("EXPOSURE_WINDOW_MISMATCH")
        if not isinstance(value["human_authority_reference"],str) or not value["human_authority_reference"]:
            return _blocked("EXPOSURE_AUTHORITY_REFERENCE_MISSING")
        clean=value["prior_oos_performance_exposure"]=="NONE_DECLARED"
        if value["oos_clean"] is not clean: return _blocked("EXPOSURE_CLEAN_STATUS_MISMATCH")
        return {"status":"PASS","canonical_digest":value["canonical_digest"],"oos_clean":value["oos_clean"]}
    except (KeyError,TypeError,ValueError): return _blocked("EXPOSURE_MALFORMED")

def verify_one_shot_authority(value,*,executor_blob):
    try:
        if not isinstance(value,dict) or set(value)!=AUTHORITY_KEYS: return _blocked("AUTHORITY_SCHEMA_MISMATCH")
        unsigned={k:v for k,v in value.items() if k!="canonical_digest"}
        if canonical_sha256(unsigned)!=value["canonical_digest"]: return _blocked("AUTHORITY_DIGEST_MISMATCH")
        if value["schema"]!="E1_ONE_SHOT_RUN_AUTHORITY_V0" or value["experiment_id"]!=EXPERIMENT_ID:
            return _blocked("AUTHORITY_IDENTITY_MISMATCH")
        if value["repository"]!=REPOSITORY or value["branch"]!=BRANCH: return _blocked("AUTHORITY_REPOSITORY_MISMATCH")
        if value["executor_blob"]!=executor_blob: return _blocked("AUTHORITY_EXECUTOR_MISMATCH")
        if value["protected_bindings"]!=PROTECTED_BLOBS: return _blocked("AUTHORITY_PROTECTED_BINDING_MISMATCH")
        if value["source_manifest_sha256"]!=SOURCE_MANIFEST_SHA256 or value["h1_jsonl_sha256"]!=H1_JSONL_SHA256:
            return _blocked("AUTHORITY_DATASET_BINDING_MISMATCH")
        if value["oos_start"]!=OOS_START or value["oos_end"]!=OOS_END: return _blocked("AUTHORITY_WINDOW_MISMATCH")
        if value["max_runs"]!=1 or value["real_e1_run_authorized"] is not True: return _blocked("AUTHORITY_RUN_LIMIT_MISMATCH")
        if not isinstance(value["run_id"],str) or not value["run_id"]: return _blocked("AUTHORITY_RUN_ID_INVALID")
        return {"status":"PASS","canonical_digest":value["canonical_digest"]}
    except (KeyError,TypeError,ValueError): return _blocked("AUTHORITY_MALFORMED")

def consume_authorization_once(marker_path,authority):
    try:
        if not isinstance(authority,dict) or set(authority)!=AUTHORITY_KEYS: return _blocked("AUTHORITY_SCHEMA_MISMATCH")
        unsigned={k:v for k,v in authority.items() if k!="canonical_digest"}
        if canonical_sha256(unsigned)!=authority["canonical_digest"] or authority["max_runs"]!=1 or authority["real_e1_run_authorized"] is not True:
            return _blocked("AUTHORITY_INVALID")
        fd=os.open(str(marker_path),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        try: os.write(fd,authority["canonical_digest"].encode("ascii"))
        finally: os.close(fd)
        return {"status":"PASS","authority_digest":authority["canonical_digest"]}
    except FileExistsError: return _blocked("AUTHORITY_ALREADY_CONSUMED")
    except (KeyError,TypeError,ValueError,OSError): return _blocked("AUTHORITY_CONSUMPTION_FAILED")

def classify_trade(entry_timestamp_ms,exit_timestamp_ms):
    if entry_timestamp_ms<OOS_START_MS and exit_timestamp_ms<OOS_START_MS: return "PRE_OOS"
    if entry_timestamp_ms>=OOS_START_MS: return "OOS"
    return "CROSS_BOUNDARY"

def _calendar_year(timestamp_ms):
    return str(datetime.fromtimestamp(int(timestamp_ms)/1000,tz=timezone.utc).year)

def derive_trade_ledger(records):
    position=0; entry_price=None; entry_ts=None; trades=[]
    for record in records:
        execution=record.get("execution") or {}
        if execution.get("status")!="EXECUTED": continue
        for event in execution.get("events",[]):
            action=event["action"]; price=float(event["price"]); ts=int(event["timestamp_ms"]); role=event.get("role")
            if role=="CLOSE":
                if position==1 and action=="SELL": pnl=price-entry_price; direction="LONG"
                elif position==-1 and action=="BUY": pnl=entry_price-price; direction="SHORT"
                else: raise E108Error("INVALID_CLOSE_EVENT")
                trades.append({"direction":direction,"entry_timestamp_ms":entry_ts,"entry_price":entry_price,
                    "exit_timestamp_ms":ts,"exit_price":price,"realized_unit_pnl":round(pnl,12),
                    "partition":classify_trade(entry_ts,ts),"calendar_period":_calendar_year(ts)})
                position=0; entry_price=None; entry_ts=None; continue
            if role=="OPEN":
                if position!=0: raise E108Error("INVALID_OPEN_EVENT")
                position=1 if action=="BUY" else -1; entry_price=price; entry_ts=ts; continue
            if position==0:
                position=1 if action=="BUY" else -1; entry_price=price; entry_ts=ts
            elif position==1 and action=="SELL":
                pnl=price-entry_price
                trades.append({"direction":"LONG","entry_timestamp_ms":entry_ts,"entry_price":entry_price,
                    "exit_timestamp_ms":ts,"exit_price":price,"realized_unit_pnl":round(pnl,12),
                    "partition":classify_trade(entry_ts,ts),"calendar_period":_calendar_year(ts)})
                position=0; entry_price=None; entry_ts=None
            elif position==-1 and action=="BUY":
                pnl=entry_price-price
                trades.append({"direction":"SHORT","entry_timestamp_ms":entry_ts,"entry_price":entry_price,
                    "exit_timestamp_ms":ts,"exit_price":price,"realized_unit_pnl":round(pnl,12),
                    "partition":classify_trade(entry_ts,ts),"calendar_period":_calendar_year(ts)})
                position=0; entry_price=None; entry_ts=None
    open_position=None
    if position:
        open_position={"status":"OPEN_UNREALIZED","direction":"LONG" if position==1 else "SHORT",
                       "entry_timestamp_ms":entry_ts,"entry_price":entry_price}
    return {"closed_trades":trades,"open_position":open_position}

def _bucket_metrics(trades):
    pnls=[float(t["realized_unit_pnl"]) for t in trades]; wins=[x for x in pnls if x>0]; losses=[x for x in pnls if x<0]
    cumulative=0.0; peak=0.0; max_dd=0.0
    for x in pnls:
        cumulative+=x; peak=max(peak,cumulative); max_dd=max(max_dd,peak-cumulative)
    longs=[t for t in trades if t["direction"]=="LONG"]; shorts=[t for t in trades if t["direction"]=="SHORT"]; n=len(trades)
    return {"aggregate_realized_unit_pnl":round(sum(pnls),12),"closed_trade_count":n,"win_count":len(wins),
        "loss_count":len(losses),"zero_pnl_count":sum(x==0 for x in pnls),"win_rate":None if n==0 else len(wins)/n,
        "average_win":None if not wins else sum(wins)/len(wins),"average_loss":None if not losses else sum(losses)/len(losses),
        "expectancy_per_closed_trade":None if n==0 else sum(pnls)/n,"realized_closed_trade_max_drawdown":round(max_dd,12),
        "long_trade_count":len(longs),"long_realized_pnl":round(sum(float(t["realized_unit_pnl"]) for t in longs),12),
        "short_trade_count":len(shorts),"short_realized_pnl":round(sum(float(t["realized_unit_pnl"]) for t in shorts),12)}

def compute_metrics(trades,records):
    full=_bucket_metrics(trades)
    full["executed_transition_count"]=sum((r.get("execution") or {}).get("status")=="EXECUTED" for r in records)
    full["not_executed_transition_count"]=sum((r.get("execution") or {}).get("status")=="NOT_EXECUTED" for r in records)
    pre=_bucket_metrics([t for t in trades if t["partition"]=="PRE_OOS"]); oos=_bucket_metrics([t for t in trades if t["partition"]=="OOS"])
    cross=[t for t in trades if t["partition"]=="CROSS_BOUNDARY"]; cal={}
    for year in sorted({t["calendar_period"] for t in trades}):
        ys=[t for t in trades if t["calendar_period"]==year]
        cal[year]={"trade_count":len(ys),"aggregate_realized_unit_pnl":round(sum(float(t["realized_unit_pnl"]) for t in ys),12)}
    return {"full_sample":full,"pre_oos":pre,"oos":oos,
        "cross_boundary":{"trade_count":len(cross),"aggregate_realized_unit_pnl":round(sum(float(t["realized_unit_pnl"]) for t in cross),12)},
        "calendar":cal}

def build_result_payload(records,exposure,authority,*,execution_status):
    if verify_exposure_declaration(exposure)["status"]!="PASS": raise E108Error("INVALID_EXPOSURE")
    ledger=derive_trade_ledger(records); metrics=compute_metrics(ledger["closed_trades"],records)
    out={"schema":"E1_REAL_RESULT_V0","experiment_id":EXPERIMENT_ID,"execution_status":execution_status,
         "records_digest":canonical_sha256(records),"exposure_digest":exposure["canonical_digest"],
         "authority_digest":authority["canonical_digest"],"trade_ledger":ledger,"metrics":metrics,
         "cost_scope":COST_SCOPE,"oos_clean":exposure["oos_clean"],"forbidden_claims":list(FORBIDDEN_CLAIMS)}
    out["result_digest"]=canonical_sha256(out); return out

def run_synthetic_qualification(h1_rows,raw_rows,e1_05_runtime,e1_04_runtime,e1_07_runtime,preflight,exposure,authority,marker_path):
    if verify_exposure_declaration(exposure)["status"]!="PASS": return _blocked("EXPOSURE_INVALID")
    if verify_one_shot_authority(authority,executor_blob=authority.get("executor_blob"))["status"]!="PASS":
        return _blocked("AUTHORITY_INVALID")
    used=consume_authorization_once(marker_path,authority)
    if used["status"]!="PASS": return used
    raw_ticks=list(adapt_tick_rows(raw_rows))
    runner=e1_05_runtime.run_momentum_runner(h1_rows,raw_ticks=raw_ticks,e1_03_identity=H1_IDENTITY,
        e1_04_runtime=e1_04_runtime,initial_position=0)
    if runner.get("status")!="PASS": return _blocked("RUNNER_BLOCKED",runner=runner)
    result=build_result_payload(runner["records"],exposure,authority,execution_status="QUALIFICATION_FIXTURE")
    trace=e1_07_runtime.build_result_envelope(preflight,run_id=authority["run_id"],
        timestamp_utc=authority["authorized_at_utc"],execution_status="QUALIFICATION_FIXTURE",
        metrics=result["metrics"],result_payload=result)
    return {"status":"PASS","result":result,"trace":trace}

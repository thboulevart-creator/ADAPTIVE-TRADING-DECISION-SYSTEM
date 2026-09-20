#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import http.client
import json
import lzma
import math
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LOCATOR_PATH = ROOT / "evidence/berd02/locator_manifest_v0_1.json"
PROBE_PATH = ROOT / "evidence/berd02/probe_plan_v0_1.json"
POLICY_PATH = ROOT / "evidence/berd02/gha_transport_policy_v0_1.json"

EXPECTED_LOCATOR_SEAL = "a9fc7115af925fcb5e848e76fb98da7c51053ad136dfb2f6adbd239c004b4db7"
EXPECTED_PROBE_SEAL = "af5b70ffef6125a0ab6b146c3bb917089182a5abb3adc260a9092e8d584b44ce"

def canonical_bytes(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sealed_hash(obj, field):
    x = dict(obj)
    x.pop(field, None)
    return hashlib.sha256(canonical_bytes(x)).hexdigest()

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def verify_seal(obj, field, expected=None):
    actual = sealed_hash(obj, field)
    if actual != obj.get(field):
        raise RuntimeError(f"seal mismatch {field}: {actual} != {obj.get(field)}")
    if expected and actual != expected:
        raise RuntimeError(f"unexpected identity {field}: {actual} != {expected}")

def render_k1(start_iso):
    t = dt.datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    return (
        "https://datafeed.dukascopy.com/datafeed/USATECHIDXUSD/"
        f"{t.year}/{t.month - 1:02d}/{t.day:02d}/{t.hour:02d}h_ticks.bi5"
    )

def raw_https_get(url, policy, body_path):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.query or parts.fragment:
        raise RuntimeError("invalid sealed K1 locator")
    headers = dict(policy["k1"]["request_headers"])
    headers["Host"] = parts.hostname
    cap = {
        "request_method": "GET",
        "requested_locator": url,
        "request_headers": headers,
        "request_started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "response_received_at_utc": None,
        "http_status": None,
        "response_headers": [],
        "raw_response_byte_length": None,
        "raw_response_sha256": None,
        "body_artifact": None,
        "transport_disposition": None,
        "family_disposition": None,
        "error": None,
    }
    conn = http.client.HTTPSConnection(parts.hostname, port=parts.port or 443, timeout=policy["k1"]["connect_timeout_seconds"])
    try:
        conn.connect()
        if conn.sock is not None:
            conn.sock.settimeout(policy["k1"]["read_timeout_seconds"])
        conn.putrequest("GET", parts.path, skip_host=True, skip_accept_encoding=True)
        for k, v in headers.items():
            conn.putheader(k, v)
        conn.endheaders()
        resp = conn.getresponse()
        cap["response_received_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        cap["http_status"] = resp.status
        cap["response_headers"] = [{"name": k, "value": v} for k, v in resp.getheaders()]
        max_bytes = int(policy["k1"]["max_body_bytes"])
        body = resp.read(max_bytes + 1)
        if len(body) > max_bytes:
            cap["transport_disposition"] = "TRANSPORT_AMBIGUOUS"
            cap["family_disposition"] = "BLOCKED"
            cap["error"] = "sealed body cap exceeded"
            return cap
        body_path.parent.mkdir(parents=True, exist_ok=True)
        body_path.write_bytes(body)
        cap["raw_response_byte_length"] = len(body)
        cap["raw_response_sha256"] = sha256_bytes(body)
        cap["body_artifact"] = str(body_path)
        if resp.status == 200:
            cap["transport_disposition"] = "OBJECT_BYTES_OBTAINED"
            cap["family_disposition"] = "FAMILY_OBSERVED" if body else "FAMILY_NOT_OBSERVED"
        elif resp.status == 404:
            cap["transport_disposition"] = "OBJECT_ABSENT_SIGNAL"
            cap["family_disposition"] = "FAMILY_NOT_OBSERVED"
        elif resp.status in (301,302,303,307,308):
            cap["transport_disposition"] = "REDIRECTED_TO_UNKNOWN"
            cap["family_disposition"] = "BLOCKED"
        elif resp.status in (401,403):
            cap["transport_disposition"] = "AUTH_OR_POLICY_BLOCK"
            cap["family_disposition"] = "BLOCKED"
        elif resp.status == 429:
            cap["transport_disposition"] = "RATE_LIMITED"
            cap["family_disposition"] = "BLOCKED"
        elif 500 <= resp.status <= 599:
            cap["transport_disposition"] = "TRANSIENT_SERVER_FAILURE"
            cap["family_disposition"] = "BLOCKED"
        else:
            cap["transport_disposition"] = "TRANSPORT_AMBIGUOUS"
            cap["family_disposition"] = "BLOCKED"
        return cap
    except Exception as exc:
        cap["response_received_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        cap["transport_disposition"] = "TRANSPORT_AMBIGUOUS"
        cap["family_disposition"] = "BLOCKED"
        cap["error"] = f"{type(exc).__name__}: {exc}"
        return cap
    finally:
        try:
            conn.close()
        except Exception:
            pass

def validate_and_fingerprint(raw):
    if len(raw) % 20:
        raise ValueError(f"decompressed length {len(raw)} not divisible by 20")
    h = hashlib.sha256()
    errors = []
    count = len(raw) // 20
    for idx in range(count):
        chunk = raw[idx*20:(idx+1)*20]
        ms = int.from_bytes(chunk[0:4], "big", signed=False)
        ask = int.from_bytes(chunk[4:8], "big", signed=False)
        bid = int.from_bytes(chunk[8:12], "big", signed=False)
        ask_vol = struct.unpack(">f", chunk[12:16])[0]
        bid_vol = struct.unpack(">f", chunk[16:20])[0]
        if not (0 <= ms < 3600000):
            errors.append(f"{idx}:ms={ms}")
        if ask == 0 or bid == 0:
            errors.append(f"{idx}:zero-price")
        if ask < bid:
            errors.append(f"{idx}:ask<bid")
        if not math.isfinite(ask_vol) or not math.isfinite(bid_vol):
            errors.append(f"{idx}:nonfinite-volume")
        h.update(f"{ms},{ask},{bid},{chunk[12:16].hex()},{chunk[16:20].hex()}\n".encode("ascii"))
    return h.hexdigest(), count, errors

def diagnostic_a(body):
    out={"path_id":"A_PYTHON_LZMA_STRUCT","success":False}
    try:
        raw=lzma.decompress(body, format=lzma.FORMAT_ALONE)
        fp,count,errors=validate_and_fingerprint(raw)
        out.update(success=True,decompressed_sha256=sha256_bytes(raw),decompressed_byte_length=len(raw),record_count=count,projection_sha256=fp,plausibility_errors=errors)
    except Exception as exc:
        out["error"]=f"{type(exc).__name__}: {exc}"
    return out

def diagnostic_b(body):
    out={"path_id":"B_XZ_MANUAL_PARSE","success":False}
    try:
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/"input.bi5"
            src.write_bytes(body)
            cp=subprocess.run(["xz","--format=lzma","--decompress","--stdout",str(src)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
            if cp.returncode:
                raise RuntimeError(cp.stderr.decode("utf-8","replace").strip())
            raw=cp.stdout
        fp,count,errors=validate_and_fingerprint(raw)
        out.update(success=True,decompressed_sha256=sha256_bytes(raw),decompressed_byte_length=len(raw),record_count=count,projection_sha256=fp,plausibility_errors=errors)
    except Exception as exc:
        out["error"]=f"{type(exc).__name__}: {exc}"
    return out

def k1_disposition(cap,a,b):
    if cap["family_disposition"]=="FAMILY_NOT_OBSERVED":
        return "NOT_OBSERVED",["OBJECT_NOT_OBSERVED_ZERO_REFUTATION_WEIGHT"]
    if cap["family_disposition"]!="FAMILY_OBSERVED":
        return "BLOCKED",[cap["transport_disposition"]]
    if a is None or b is None:
        return "BLOCKED",["DIAGNOSTICS_NOT_REACHED"]
    if a.get("success") and b.get("success"):
        if a["decompressed_sha256"]!=b["decompressed_sha256"]:
            return "BLOCKED",["INDEPENDENT_DECOMPRESSION_DISAGREEMENT"]
        if a["projection_sha256"]!=b["projection_sha256"]:
            return "BLOCKED",["INDEPENDENT_PARSE_DISAGREEMENT"]
        if a["record_count"]<=0:
            return "BLOCKED",["ZERO_DECODED_RECORDS"]
        if a["plausibility_errors"] or b["plausibility_errors"]:
            return "REFUTED",["CANDIDATE_HOURLY_SEMANTICS_VIOLATED"]
        return "SUPPORTED",["TWO_INDEPENDENT_DIAGNOSTICS_AGREE"]
    if not a.get("success") and not b.get("success"):
        return "REFUTED",["BOTH_INDEPENDENT_PATHS_REJECT_K1_STRUCTURE"]
    return "BLOCKED",["INDEPENDENT_DIAGNOSTIC_DISAGREEMENT"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--execution-id",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    outdir=Path(args.output)
    outdir.mkdir(parents=True,exist_ok=True)

    locator=read_json(LOCATOR_PATH)
    probes=read_json(PROBE_PATH)
    policy=read_json(POLICY_PATH)
    verify_seal(locator,"manifest_seal",EXPECTED_LOCATOR_SEAL)
    verify_seal(probes,"probe_plan_seal",EXPECTED_PROBE_SEAL)
    verify_seal(policy,"policy_seal")

    captures=[]
    diag_a_records=[]
    diag_b_records=[]
    per_probe=[]

    for probe in probes["resolved_probes"]:
        pid=probe["probe_id"]
        url=render_k1(probe["market_interval_start_utc"])
        body_path=outdir/"bodies"/f"{pid}_K1.bi5"
        cap=raw_https_get(url,policy,body_path)
        cap.update(schema="B_ERD_02_GHA_TRANSPORT_CAPTURE_V0_1",execution_id=args.execution_id,probe_id=pid,candidate_id="K1_LEGACY_HOURLY_TICK_BI5",retry_performed=False)
        body=body_path.read_bytes() if body_path.exists() and cap["http_status"]==200 else None
        a=diagnostic_a(body) if body is not None else None
        b=diagnostic_b(body) if body is not None else None
        if a is not None:
            a.update(execution_id=args.execution_id,probe_id=pid,raw_response_sha256=cap["raw_response_sha256"])
            a["diagnostic_seal"]=sealed_hash(a,"diagnostic_seal")
            diag_a_records.append(a)
        if b is not None:
            b.update(execution_id=args.execution_id,probe_id=pid,raw_response_sha256=cap["raw_response_sha256"])
            b["diagnostic_seal"]=sealed_hash(b,"diagnostic_seal")
            diag_b_records.append(b)
        disp,reasons=k1_disposition(cap,a,b)
        cap["capture_seal"]=sealed_hash(cap,"capture_seal")
        captures.append(cap)
        per_probe.append({
            "probe_id":pid,
            "window_start_utc":probe["market_interval_start_utc"],
            "window_end_utc":probe["market_interval_end_utc"],
            "K1":{"disposition":disp,"reason_codes":reasons},
            "K2":{"disposition":"BLOCKED","reason_codes":["SECURITY_CAPTURE_POLICY_BLOCK"],"request_sent":False},
            "cross_family_relation":"COMPARISON_BLOCKED_K2_NOT_EXECUTED"
        })

    ds=[p["K1"]["disposition"] for p in per_probe]
    if "REFUTED" in ds:
        overall="PROBE_REFUTED"
    elif any(x in ("BLOCKED","NOT_OBSERVED") for x in ds):
        overall="BLOCKED"
    elif all(x=="SUPPORTED" for x in ds):
        overall="PROBE_SUPPORTED"
    else:
        overall="BLOCKED"

    result={
        "schema":"B_ERD_02_GHA_EXECUTION_RESULT_V0_1",
        "execution_id":args.execution_id,
        "source_head":os.environ.get("GITHUB_SHA"),
        "locator_manifest_id":locator["locator_manifest_id"],
        "locator_manifest_seal":locator["manifest_seal"],
        "probe_plan_id":probes["probe_plan_id"],
        "probe_plan_seal":probes["probe_plan_seal"],
        "runtime_policy_id":policy["policy_id"],
        "runtime_policy_seal":policy["policy_seal"],
        "per_probe_results":per_probe,
        "K1_supported_count":sum(x=="SUPPORTED" for x in ds),
        "K1_refuted_count":sum(x=="REFUTED" for x in ds),
        "K1_not_observed_count":sum(x=="NOT_OBSERVED" for x in ds),
        "K1_blocked_count":sum(x=="BLOCKED" for x in ds),
        "K2_execution_status":"SECURITY_CAPTURE_POLICY_BLOCK",
        "overall_probe_verdict":overall,
        "anti_extrapolation":"PROBE_SUPPORTED_NE_FULL_INTERVAL_QUALIFIED",
        "full_acquisition_performed":False,
        "backtest_performed":False,
        "created_at_utc":dt.datetime.now(dt.timezone.utc).isoformat()
    }
    result["result_seal"]=sealed_hash(result,"result_seal")
    capture_set={"schema":"B_ERD_02_GHA_CAPTURE_SET_V0_1","execution_id":args.execution_id,"capture_count":len(captures),"captures":captures}
    capture_set["capture_set_seal"]=sealed_hash(capture_set,"capture_set_seal")

    outputs={
        "transport_captures.json":capture_set,
        "diagnostic_a.json":{"records":diag_a_records},
        "diagnostic_b.json":{"records":diag_b_records},
        "execution_result.json":result
    }
    for name,obj in outputs.items():
        (outdir/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    print(json.dumps({
        "execution_id":args.execution_id,
        "overall_probe_verdict":overall,
        "K1_supported_count":result["K1_supported_count"],
        "K1_refuted_count":result["K1_refuted_count"],
        "K1_not_observed_count":result["K1_not_observed_count"],
        "K1_blocked_count":result["K1_blocked_count"],
        "K2_execution_status":result["K2_execution_status"],
        "result_seal":result["result_seal"]
    },sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

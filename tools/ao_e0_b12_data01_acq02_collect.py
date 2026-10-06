from __future__ import annotations
import argparse, hashlib, json, time, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tools.ao_e0_b12_data01_acq02 import (
    seal_raw_object, rolling_raw_manifest, materialize_ap0_from_ledger,
    materialize_h1_from_ap0, rolling_readiness, canonical_bytes, sha256_bytes,
    ACQ02Blocked
)

BASE_URL="https://jetta.dukascopy.com/v1/ticks/USATECH.IDX-USD"
UA="ATDS-ACQ02/0.1"
WARMUP_START=datetime(2026,10,5,14,tzinfo=timezone.utc)
FORWARD_RAW_START=datetime(2026,10,6,10,tzinfo=timezone.utc)

def url_for(dt):
    return f"{BASE_URL}/{dt.year}/{dt.month}/{dt.day}/{dt.hour}"

def cache_name(dt):
    return f"ticks%2FUSATECH.IDX-USD%2F{dt.year}%2F{dt.month}%2F{dt.day}%2F{dt.hour}.json"

def get_raw(cache:Path,dt:datetime)->tuple[bytes,str]:
    cache.mkdir(parents=True,exist_ok=True)
    p=cache/cache_name(dt)
    if p.exists():
        return p.read_bytes(),"CACHE_REUSE"
    last=None
    for delay in (0,2,4,8,16):
        if delay: time.sleep(delay)
        req=urllib.request.Request(url_for(dt),headers={"User-Agent":UA,"Accept":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=30) as r:
                if r.status!=200: raise RuntimeError(f"HTTP_{r.status}")
                raw=r.read()
            # Structural validation occurs in seal_raw_object before promotion.
            p.write_bytes(raw)
            return raw,"NETWORK"
        except Exception as exc:
            last=exc
            if isinstance(exc,urllib.error.HTTPError) and exc.code not in (429,500,502,503,504):
                break
    raise RuntimeError(f"BLOCKED_FORWARD_TRANSPORT_UNAVAILABLE {dt.isoformat()} {last}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--end-hour-utc",required=True,help="exclusive UTC hour, YYYY-MM-DDTHH:00:00Z")
    args=ap.parse_args()
    root=Path(args.root)
    end=datetime.strptime(args.end_hour_utc,"%Y-%m-%dT%H:00:00Z").replace(tzinfo=timezone.utc)
    if end<=FORWARD_RAW_START: raise SystemExit("END_BEFORE_FORWARD_START")
    for name in ("raw","manifests","ledger","ap0","h1","evidence"):
        (root/name).mkdir(parents=True,exist_ok=True)
    cache=root/"raw"/"provider-cache"
    dt=WARMUP_START
    sealed=replayed=network=cache_reuse=0
    while dt<end:
        raw,source=get_raw(cache,dt)
        classification="WARMUP" if dt<FORWARD_RAW_START else "FORWARD_EVIDENCE"
        nxt=dt+timedelta(hours=1)
        now=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
        result=seal_raw_object(
            root,
            interval_start_utc=dt.strftime("%Y-%m-%dT%H:00:00Z"),
            interval_end_utc=nxt.strftime("%Y-%m-%dT%H:00:00Z"),
            raw=raw,acquisition_time_utc=now,classification=classification)
        sealed+=result["status"]=="SEALED"; replayed+=result["status"]=="REPRODUCIBILITY_ONLY"
        network+=source=="NETWORK"; cache_reuse+=source=="CACHE_REUSE"
        dt=nxt

    raw_manifest=rolling_raw_manifest(root)
    (root/"manifests"/"RAW-FORWARD-MANIFEST.json").write_bytes(canonical_bytes(raw_manifest))

    ap0=materialize_ap0_from_ledger(root)
    # Local AP0 payload may contain price values; never print it.
    (root/"ap0"/"AP0-ROLLING.json").write_bytes(canonical_bytes(ap0))
    ap0_meta={
      "identity":ap0["identity"],
      "source_raw_manifest_sha256":ap0["source_raw_manifest_sha256"],
      "ap0_forward_manifest_sha256":ap0["ap0_forward_manifest_sha256"],
      "row_count":len(ap0["rows"]),
      "first_minute_ms":None if not ap0["rows"] else ap0["rows"][0]["minute_start_ms_utc"],
      "last_minute_ms":None if not ap0["rows"] else ap0["rows"][-1]["minute_start_ms_utc"],
      "forward_fill":False,"volume_used":False,"returns_calculated":False,
      "strategy_calculated":False,"pnl_calculated":False
    }
    (root/"manifests"/"AP0-ROLLING-MANIFEST.json").write_bytes(canonical_bytes(ap0_meta))

    h1=materialize_h1_from_ap0(
        ap0,
        raw_window_start_ms=int(WARMUP_START.timestamp()*1000),
        raw_window_end_ms=int(end.timestamp()*1000))
    (root/"h1"/"H1-ROLLING.json").write_bytes(canonical_bytes(h1))
    h1_meta={k:v for k,v in h1.items() if k!="rows"}
    h1_meta["coverage_start_utc"]=WARMUP_START.strftime("%Y-%m-%dT%H:00:00Z")
    h1_meta["coverage_end_exclusive_utc"]=end.strftime("%Y-%m-%dT%H:00:00Z")
    (root/"manifests"/"H1-ROLLING-MANIFEST.json").write_bytes(canonical_bytes(h1_meta))

    readiness=rolling_readiness(raw_manifest=raw_manifest,ap0=ap0,h1=h1,terminal_count_info=None)
    readiness["acq02"]="QUALIFIED_ROLLING_DATA01_CANDIDATE"
    readiness["b12"]="CLOSED"
    readiness["performance_bearing_read"]=False
    readiness["performance_observed"]=False
    readiness["strategy_qualified_claim"]=False
    readiness["coverage_end_exclusive_utc"]=end.strftime("%Y-%m-%dT%H:00:00Z")
    (root/"evidence"/"ROLLING-DATA01-READINESS.json").write_bytes(canonical_bytes(readiness))

    # Human-visible output is metadata only.
    print("ACQ02=QUALIFIED_ROLLING_DATA01_CANDIDATE")
    print("B12=CLOSED")
    print("PERFORMANCE_BEARING_READ=FALSE")
    print("STRATEGY_QUALIFIED=NO_CLAIM")
    print(f"SEALED_NEW_OBJECTS={sealed}")
    print(f"REPLAYED_OBJECTS={replayed}")
    print(f"NETWORK_OBJECTS={network}")
    print(f"CACHE_REUSE_OBJECTS={cache_reuse}")
    print(f"WARMUP_OBJECTS={raw_manifest['warmup_objects']}")
    print(f"FORWARD_EVIDENCE_OBJECTS={raw_manifest['forward_evidence_objects']}")
    print(f"RAW_INVENTORY_DIGEST={raw_manifest['raw_forward_inventory_digest']}")
    print(f"RAW_MANIFEST_SHA256={raw_manifest['raw_forward_manifest_sha256']}")
    print(f"AP0_ROW_COUNT={ap0_meta['row_count']}")
    print(f"AP0_MANIFEST_SHA256={ap0_meta['ap0_forward_manifest_sha256']}")
    print(f"H1_ROW_COUNT={h1_meta['h1_row_count']}")
    print(f"H1_FIRST_BOUNDARY={h1_meta['h1_first_boundary']}")
    print(f"H1_LAST_BOUNDARY={h1_meta['h1_last_boundary']}")
    print(f"H1_STREAM_SHA256={h1_meta['h1_forward_stream_sha256']}")
    print(f"READINESS_STATE={readiness['state']}")
    print(f"EXACT_FORWARD_INSTANCE={readiness['exact_forward_instance']}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

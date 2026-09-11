"""V4.3 — Research ↔ Execution data compatibility probe.

Native source formats are preserved. Instrument-specific BI5 decoding semantics
are resolved from the normative instrument contract layer.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, lzma, math, re, statistics, struct
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from tools.instrument_contract_v4_3 import resolve_contract

EXPECTED_CSV_COLUMNS=("timestamp","askPrice","bidPrice","askVolume","bidVolume")
EXPECTED_PARQUET_COLUMNS=("timestamp","bid_price","ask_price","bid_volume","ask_volume")
EXECUTION_BOUNDARY_UTC="2024-12-17T09:38:28+00:00"
MIN_RESEARCH_YEARS=5.0
BI5_RECORD_SIZE=20
BI5_STRUCT=struct.Struct(">IIIff")

def parse_args():
 p=argparse.ArgumentParser(); p.add_argument("--research",required=True); p.add_argument("--execution",required=True)
 p.add_argument("--research-instrument",default="Dukascopy USATECHIDXUSD"); p.add_argument("--execution-instrument",default="VT Markets NAS100.s")
 p.add_argument("--contracts-root",default="docs/04-REFERENCE/INSTRUMENT-CONTRACTS"); p.add_argument("--naive-timezone",default=None)
 p.add_argument("--output",default="reports/data-qualification/research_execution_compatibility_v4_3.json"); return p.parse_args()

def utc_iso(dt): return dt.astimezone(timezone.utc).isoformat() if dt else None

def parse_aware_timestamp(value):
 dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
 if dt.tzinfo is None: raise ValueError("timestamp has no timezone")
 return dt.astimezone(timezone.utc)

def parse_naive_timestamp(value,tz_name):
 from zoneinfo import ZoneInfo
 dt=datetime.fromisoformat(str(value).replace("Z","")); return (dt.astimezone(timezone.utc) if dt.tzinfo is not None else dt.replace(tzinfo=ZoneInfo(tz_name)).astimezone(timezone.utc))

def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()

def collect_sources(text):
 p=Path(text)
 if not p.exists(): raise FileNotFoundError(p)
 return [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in {".csv",".bi5",".parquet"})

def source_format(path):
 return {".bi5":"DUKASCOPY_BI5",".parquet":"PARQUET",".csv":"CSV"}.get(path.suffix.lower(),"UNSUPPORTED")

def empty_stats(): return {"files":0,"rows":0,"first":None,"last":None,"invalid_rows":0,"ordering_violations":0,"quote_violations":0,"spreads":[],"hour_mid":{},"file_errors":[],"formats":defaultdict(int),"timezone_semantics":set()}

def record_tick(s,ts,ask,bid,av,bv,prev):
 s["rows"]+=1
 if ask<=0 or bid<=0 or av<0 or bv<0 or not all(math.isfinite(x) for x in (ask,bid,av,bv)): s["invalid_rows"]+=1
 if ask<bid: s["quote_violations"]+=1
 if prev is not None and ts<prev: s["ordering_violations"]+=1
 s["spreads"].append(ask-bid); s["hour_mid"][ts.replace(minute=0,second=0,microsecond=0)]=(ask+bid)/2
 if s["first"] is None or ts<s["first"]: s["first"]=ts
 if s["last"] is None or ts>s["last"]: s["last"]=ts
 return ts

def scan_csv(path,s):
 s["formats"]["CSV"]+=1; prev=None
 with path.open("r",encoding="utf-8-sig",newline="") as f:
  r=csv.DictReader(f)
  if tuple(r.fieldnames or ())!=EXPECTED_CSV_COLUMNS: raise ValueError(f"unexpected CSV schema: {r.fieldnames!r}")
  for row in r:
   try: ts=parse_aware_timestamp(row["timestamp"]); ask,bid=float(Decimal(row["askPrice"])),float(Decimal(row["bidPrice"])); av,bv=float(Decimal(row["askVolume"])),float(Decimal(row["bidVolume"]))
   except (KeyError,InvalidOperation,ValueError,TypeError): s["invalid_rows"]+=1; continue
   prev=record_tick(s,ts,ask,bid,av,bv,prev)
 s["timezone_semantics"].add("explicit_utc_or_offset")

def parse_bi5_hour(path):
 text=str(path).replace("\\","/")
 for pat in (r"(?P<y>20\d{2})[-/](?P<m>\d{2})[-/](?P<d>\d{2})[ _](?P<h>\d{1,2})h",r"/(?P<y>20\d{2})/(?P<m>\d{2})/(?P<d>\d{2})/(?P<h>\d{1,2})h_ticks\.bi5$"):
  m=re.search(pat,text)
  if m: return datetime(int(m["y"]),int(m["m"]),int(m["d"]),int(m["h"]),tzinfo=timezone.utc)
 raise ValueError("BI5 filename/path does not expose YYYY-MM-DD-HH hour needed for timestamp reconstruction")

def scan_bi5(path,s,contract):
 s["formats"]["DUKASCOPY_BI5"]+=1
 if (contract.record_size,contract.record_struct,contract.timestamp_unit)!=(20,">IIIff","milliseconds"): raise ValueError("BI5_CONTRACT_INCOMPATIBLE")
 hour=parse_bi5_hour(path); raw=lzma.decompress(path.read_bytes(),format=lzma.FORMAT_ALONE)
 if not raw: raise ValueError("ZERO_DECOMPRESSED_BYTES")
 if len(raw)%contract.record_size: raise ValueError("DECOMPRESSED_SIZE_NOT_MULTIPLE_OF_CONTRACT_RECORD_SIZE")
 prev=None
 for off in range(0,len(raw),contract.record_size):
  ms,ask_raw,bid_raw,av,bv=BI5_STRUCT.unpack(raw[off:off+contract.record_size])
  if ms>=3600000: s["invalid_rows"]+=1; continue
  prev=record_tick(s,hour+timedelta(milliseconds=ms),ask_raw/contract.price_scale,bid_raw/contract.price_scale,av,bv,prev)
 s["timezone_semantics"].add("dukascopy_hour_utc")

def scan_parquet(path,s,tz):
 s["formats"]["PARQUET"]+=1
 import pyarrow.parquet as pq
 table=pq.read_table(path,columns=list(EXPECTED_PARQUET_COLUMNS)); c={n:table[n].to_pylist() for n in EXPECTED_PARQUET_COLUMNS}; prev=None
 for ts0,bid0,ask0,bv0,av0 in zip(c["timestamp"],c["bid_price"],c["ask_price"],c["bid_volume"],c["ask_volume"]):
  try: ts=parse_naive_timestamp(ts0,tz) if tz else parse_aware_timestamp(ts0); ask,bid,av,bv=float(ask0),float(bid0),float(av0),float(bv0)
  except (ValueError,TypeError) as exc:
   if not tz and getattr(ts0,"tzinfo",None) is None: raise ValueError("PARQUET_NAIVE_TIMESTAMP_REQUIRES_EXPLICIT_NAIVE_TIMEZONE") from exc
   s["invalid_rows"]+=1; continue
  prev=record_tick(s,ts,ask,bid,av,bv,prev)
 s["timezone_semantics"].add("explicit_zone_for_naive" if tz else "explicit_utc_or_offset")

def scan(paths,tz,contract=None):
 s=empty_stats(); evidence=[]
 for p in paths:
  rec={"path":str(p),"sha256":sha256(p),"format":source_format(p)}; s["files"]+=1
  try:
   if rec["format"]=="CSV": scan_csv(p,s)
   elif rec["format"]=="DUKASCOPY_BI5":
    if contract is None: raise ValueError("BI5_CONTRACT_REQUIRED")
    scan_bi5(p,s,contract)
   elif rec["format"]=="PARQUET": scan_parquet(p,s,tz)
   else: raise ValueError(f"unsupported source format: {p.suffix}")
  except Exception as exc: rec["error"]=str(exc); s["file_errors"].append({"path":str(p),"error":str(exc)})
  evidence.append(rec)
 return s,evidence

def percentile(v,p):
 if not v:return None
 v=sorted(v); x=(len(v)-1)*p; lo,hi=math.floor(x),math.ceil(x); return v[lo] if lo==hi else v[lo]+(v[hi]-v[lo])*(x-lo)

def spread_summary(v): return {"count":len(v),"mean":statistics.fmean(v) if v else None,"p50":percentile(v,.5),"p95":percentile(v,.95),"p99":percentile(v,.99)}

def movement_summary(s):
 k=sorted(s["hour_mid"]); r=[math.log(s["hour_mid"][b]/s["hour_mid"][a]) for a,b in zip(k,k[1:]) if s["hour_mid"][a]>0 and s["hour_mid"][b]>0]; a=[abs(x) for x in r]
 return {"hour_buckets":len(k),"hourly_return_count":len(r),"hourly_abs_return_mean":statistics.fmean(a) if a else None,"hourly_abs_return_p50":percentile(a,.5),"hourly_abs_return_p95":percentile(a,.95),"hourly_return_std":statistics.stdev(r) if len(r)>1 else None}

def years_between(a,b): return (b-a).total_seconds()/(365.2425*86400) if a and b else None

def ratio(a,b): return b/a if a not in (None,0) and b is not None else None

def status(checks):
 s={c["status"] for c in checks}
 if "BLOCKED" in s:return "BLOCKED"
 if "FAIL" in s:return "FAIL"
 if "UNVERIFIED" in s:return "UNVERIFIED"
 return "PASS"

def main():
 a=parse_args(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 try: rp,ep=collect_sources(a.research),collect_sources(a.execution)
 except Exception as exc: print("VERDICT=BLOCKED"); return 2
 if not rp or not ep: print("VERDICT=BLOCKED"); return 2
 def cf(paths,instrument):
  if not any(p.suffix.lower()==".bi5" for p in paths): return None
  m=re.match(r"\s*([^ ]+)\s+(.+?)\s*$",instrument)
  if not m: raise ValueError("BI5_INSTRUMENT_IDENTITY_UNPARSEABLE")
  return resolve_contract(a.contracts_root,m.group(2),m.group(1),"BI5")
 try: rc,ec=cf(rp,a.research_instrument),cf(ep,a.execution_instrument)
 except Exception as exc: out.write_text(json.dumps({"schema":"RESEARCH_EXECUTION_COMPATIBILITY_V4_3","version":"V4.3","status":"BLOCKED","reason":f"instrument contract resolution failed: {exc}"},indent=2),encoding="utf-8"); print("VERDICT=BLOCKED"); return 2
 r,rf=scan(rp,a.naive_timezone,rc); e,ef=scan(ep,a.naive_timezone,ec)
 rcx=[{"id":"source_access","status":"FAIL" if r["file_errors"] else "PASS"},{"id":"coverage_5y","status":"PASS" if (years_between(r["first"],r["last"]) or 0)>=5 else "FAIL"},{"id":"data_integrity","status":"FAIL" if r["invalid_rows"] or r["quote_violations"] else "PASS"},{"id":"ordering","status":"FAIL" if r["ordering_violations"] else "PASS"}]
 ecx=[{"id":"source_access","status":"FAIL" if e["file_errors"] else "PASS"},{"id":"data_integrity","status":"FAIL" if e["invalid_rows"] or e["quote_violations"] else "PASS"},{"id":"ordering","status":"FAIL" if e["ordering_violations"] else "PASS"}]
 rs,es=status(rcx),status(ecx); cs=status([{"status":rs},{"status":es},{"status":"UNVERIFIED"}]); overall=status([{"status":rs},{"status":es},{"status":cs}])
 report={"schema":"RESEARCH_EXECUTION_COMPATIBILITY_V4_3","version":"V4.3","status":overall,"verdicts":{"RESEARCH_DATA_VALID":rs,"EXECUTION_DATA_VALID":es,"TRANSFER_VALIDATION":cs},"contracts":{"research_price_scale":rc.price_scale if rc else None,"execution_price_scale":ec.price_scale if ec else None},"research":{"files":rf,"rows":r["rows"],"first":utc_iso(r["first"]),"last":utc_iso(r["last"]),"checks":rcx,"spread":spread_summary(r["spreads"]),"movement":movement_summary(r)},"execution":{"files":ef,"rows":e["rows"],"first":utc_iso(e["first"]),"last":utc_iso(e["last"]),"checks":ecx,"spread":spread_summary(e["spreads"]),"movement":movement_summary(e)}}
 out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8"); print("RESEARCH_DATA_VALID=",rs); print("EXECUTION_DATA_VALID=",es); print("TRANSFER_VALIDATION=",cs); print("VERDICT=",overall); print("REPORT=",out); return 0 if overall=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())

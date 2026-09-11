#!/usr/bin/env python3
"""V4.3 Batch01 — structural qualification of a physical Dukascopy BI5 corpus.

The probe is read-only. It qualifies only physically present files and never
reconstructs missing hours. BI5 decoding semantics are resolved from the
normative instrument contract layer.
"""
from __future__ import annotations
import argparse, hashlib, json, lzma, math, re, struct
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tools.instrument_contract_v4_3 import resolve_contract

HOUR_PATTERNS=(re.compile(r"(?P<y>20\d{2})[-/](?P<m>\d{2})[-/](?P<d>\d{2})[ _](?P<h>\d{1,2})h",re.I),re.compile(r"/(?P<y>20\d{2})/(?P<m>\d{2})/(?P<d>\d{2})/(?P<h>\d{1,2})h_ticks\.bi5$",re.I))

def args():
 p=argparse.ArgumentParser(); p.add_argument("--corpus",required=True); p.add_argument("--expected"); p.add_argument("--expected-count",type=int,default=495); p.add_argument("--contracts-root",default="docs/04-REFERENCE/INSTRUMENT-CONTRACTS"); p.add_argument("--instrument",default="USATECHIDXUSD"); p.add_argument("--source",default="Dukascopy"); p.add_argument("--output",default="reports/data-qualification/batch01_structural_qualification_v2.json"); return p.parse_args()

def norm_rel(path,root): return path.relative_to(root).as_posix()

def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()

def parse_hour(path):
 text=str(path).replace("\\","/")
 for pat in HOUR_PATTERNS:
  m=pat.search(text)
  if m:
   hour=int(m["h"])
   if hour>23: break
   return datetime(int(m["y"]),int(m["m"]),int(m["d"]),hour,tzinfo=timezone.utc)
 raise ValueError("PATH_HOUR_UNPARSEABLE")

def load_expected(path,root):
 if path.suffix.lower()==".json":
  data=json.loads(path.read_text(encoding="utf-8")); data=data.get("files") if isinstance(data,dict) else data
  if not isinstance(data,list): raise ValueError("EXPECTED_JSON_MUST_BE_ARRAY_OR_OBJECT_WITH_FILES")
  values=data
 else: values=[x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip() and not x.lstrip().startswith("#")]
 out=set()
 for value in values:
  p=Path(str(value).replace("\\","/"))
  try: out.add(p.relative_to(root).as_posix())
  except ValueError: out.add(p.as_posix().lstrip("./"))
 return out

def qualify_file(path,root,contract):
 result={"path":norm_rel(path,root),"sha256":sha256(path),"compressed_bytes":path.stat().st_size,"status":"PASS","record_count":0,"first_timestamp":None,"last_timestamp":None,"errors":[]}
 try:
  if (contract.record_size,contract.record_struct,contract.timestamp_unit)!=(20,">IIIff","milliseconds"): raise ValueError("BI5_CONTRACT_INCOMPATIBLE")
  hour=parse_hour(path); result["hour"]=hour.isoformat(); raw=lzma.decompress(path.read_bytes(),format=lzma.FORMAT_ALONE); result["decompressed_bytes"]=len(raw)
  if not raw: raise ValueError("ZERO_DECOMPRESSED_BYTES")
  if len(raw)%contract.record_size: raise ValueError("DECOMPRESSED_SIZE_NOT_MULTIPLE_OF_CONTRACT_RECORD_SIZE")
  prev=None
  for off in range(0,len(raw),contract.record_size):
   ms,ask_raw,bid_raw,av,bv=struct.Struct(contract.record_struct).unpack(raw[off:off+contract.record_size])
   if ms>=3600000: raise ValueError(f"MILLISECOND_OFFSET_OUT_OF_RANGE:{ms}")
   ask,bid=ask_raw/contract.price_scale,bid_raw/contract.price_scale
   if not all(math.isfinite(x) for x in (ask,bid,av,bv)): raise ValueError(f"NON_FINITE_RECORD_AT_OFFSET:{off}")
   if ask<=0 or bid<=0 or ask<bid or av<0 or bv<0: raise ValueError(f"INVALID_QUOTE_AT_OFFSET:{off}")
   ts=hour+timedelta(milliseconds=ms)
   if prev is not None and ts<prev: raise ValueError(f"INTERNAL_TIMESTAMP_ORDER_VIOLATION_AT_OFFSET:{off}")
   prev=ts; result["record_count"]+=1
   if result["first_timestamp"] is None: result["first_timestamp"]=ts.isoformat()
   result["last_timestamp"]=ts.isoformat()
  if result["record_count"]==0: raise ValueError("ZERO_RECORDS")
 except Exception as exc: result["status"]="FAIL"; result["errors"].append(str(exc))
 return result

def main():
 a=args(); root=Path(a.corpus).expanduser().resolve(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 report={"schema":"BATCH01_STRUCTURAL_QUALIFICATION_V2","version":"V4.3","mode":"READ_ONLY_PHYSICAL_CORPUS","corpus":str(root),"expected_count":a.expected_count,"instrument":a.instrument,"source":a.source}
 if not root.exists() or not root.is_dir(): report.update({"verdict":"BLOCKED","reason":"CORPUS_DIRECTORY_UNAVAILABLE"}); out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print("VERDICT=BLOCKED"); return 2
 try: contract=resolve_contract(a.contracts_root,a.instrument,a.source,"BI5")
 except Exception as exc: report.update({"verdict":"BLOCKED","reason":f"INSTRUMENT_CONTRACT_UNAVAILABLE:{exc}"}); out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print("VERDICT=BLOCKED"); return 2
 physical=sorted(p for p in root.rglob("*.bi5") if p.is_file()); physical_set={norm_rel(p,root) for p in physical}; report["physical_files_discovered"]=len(physical)
 if a.expected:
  try: expected=load_expected(Path(a.expected).expanduser().resolve(),root)
  except Exception as exc: report.update({"verdict":"BLOCKED","reason":f"EXPECTED_INVENTORY_UNREADABLE:{exc}"}); out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print("VERDICT=BLOCKED"); return 2
  missing=sorted(expected-physical_set); unexpected=sorted(physical_set-expected); report.update({"expected_files":len(expected),"missing_files":missing,"unexpected_files":unexpected}); inventory="PASS" if not missing and not unexpected and len(expected)==a.expected_count else "FAIL"
 else: report["inventory_status"]="UNVERIFIED"; inventory="BLOCKED"
 results=[qualify_file(p,root,contract) for p in physical]; pf=sum(x["status"]=="PASS" for x in results); ff=sum(x["status"]=="FAIL" for x in results); total=sum(x["record_count"] for x in results); hours=sorted({x.get("hour") for x in results if x.get("hour")}); report.update({"files":results,"qualified_files":pf,"failed_files":ff,"total_records":total,"unique_hours":len(hours),"structural_status":"PASS" if physical and ff==0 and len(physical)==a.expected_count else "FAIL"})
 verdict="BLOCKED" if inventory=="BLOCKED" else "FAIL" if inventory=="FAIL" or ff or len(physical)!=a.expected_count else "PASS"; report["verdict"]=verdict; out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
 print(f"PAYLOADS_DISCOVERED={len(physical)}"); print(f"QUALIFIED_FILES={pf}"); print(f"FAIL_FILES={ff}"); print(f"TOTAL_RECORDS={total}"); print(f"VERDICT={verdict}"); print(f"REPORT={out}"); return 0 if verdict=="PASS" else 1 if verdict=="FAIL" else 2

if __name__=="__main__": raise SystemExit(main())

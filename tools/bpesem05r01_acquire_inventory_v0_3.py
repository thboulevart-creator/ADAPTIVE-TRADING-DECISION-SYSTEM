#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, subprocess, tempfile, urllib.parse, urllib.request, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN_PATH=ROOT/"evidence"/"bpesem05r01"/"provider_artifact_acquisition_plan_v0_3.json"
OUT=ROOT/"evidence"/"bpesem05r01"
PLAN_BLOB="93067b75ecd2d5167b2efe4ebe39042fd3ba7bd8"
ALLOW_PREFIX="https://www.dukascopy.com/client/jforexlib/publicrepo/"
MAX_ARTIFACT_BYTES=20_000_000
TERMS=["bi5","history","historical","tick","instrument","usatech","decimal","scale","factor","jetta","cache","feed","data","transport","message","price"]
ASCII_RE=re.compile(rb"[\x20-\x7e]{4,}")

def git_blob(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()
def h256(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def fetch(url:str)->bytes:
    if not url.startswith(ALLOW_PREFIX): raise RuntimeError("URL outside allowlist")
    p=urllib.parse.urlparse(url)
    if p.hostname!="www.dukascopy.com": raise RuntimeError("unexpected host")
    if ".bi5" in p.path.lower() or "/datafeed/" in p.path.lower(): raise RuntimeError("market-data URL forbidden")
    req=urllib.request.Request(url,headers={"User-Agent":"BPESEM05R01-documentary-recovery/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        data=r.read(MAX_ARTIFACT_BYTES+1)
        if len(data)>MAX_ARTIFACT_BYTES: raise RuntimeError("artifact too large")
        return data
def parse_sha1(b:bytes)->str:
    s=b.decode("ascii","strict").strip().split()[0].lower()
    if not re.fullmatch(r"[0-9a-f]{40}",s): raise RuntimeError("invalid SHA1 sidecar")
    return s
def strings(data:bytes)->list[str]:
    out=[]; seen=set()
    for m in ASCII_RE.findall(data):
        s=m.decode("utf-8","ignore"); low=s.lower()
        if any(t in low for t in TERMS):
            s=s[:1400]
            if s not in seen: out.append(s); seen.add(s)
        if len(out)>=120: break
    return out

if git_blob(PLAN_PATH)!=PLAN_BLOB: raise RuntimeError("plan blob mismatch")
plan=json.loads(PLAN_PATH.read_text(encoding="utf-8"))
if not plan["frozen_before_first_v0_3_artifact_fetch"]: raise RuntimeError("plan not frozen")

ids=[]; resources=[]; poms=[]
with tempfile.TemporaryDirectory(prefix="bpesem05r01-v03-") as td:
    td=Path(td)
    for a in plan["artifacts"]:
        if a.get("market_data_object"): raise RuntimeError("market data artifact forbidden")
        raw=fetch(a["url"]); osh=parse_sha1(fetch(a["sha1_url"])); lsh=hashlib.sha1(raw).hexdigest()
        if lsh!=osh: raise RuntimeError("artifact SHA1 mismatch "+a["artifact_id"])
        pom=fetch(a["pom_url"]); posh=parse_sha1(fetch(a["pom_sha1_url"])); plsh=hashlib.sha1(pom).hexdigest()
        if plsh!=posh: raise RuntimeError("POM SHA1 mismatch "+a["artifact_id"])
        fp=td/(a["artifact_id"]+".jar"); fp.write_bytes(raw)
        ids.append({
          "artifact_id":a["artifact_id"],"coordinate":a["coordinate"],"url":a["url"],"size_bytes":len(raw),
          "official_sha1":osh,"computed_sha1":lsh,"sha1_verification":"PASS","computed_sha256":h256(raw),
          "pom_url":a["pom_url"],"pom_size_bytes":len(pom),"pom_official_sha1":posh,
          "pom_computed_sha1":plsh,"pom_sha1_verification":"PASS","pom_computed_sha256":h256(pom)
        })
        poms.append({"artifact_id":a["artifact_id"],"coordinate":a["coordinate"],"pom_sha256":h256(pom),"pom_text":pom.decode("utf-8","replace")})
        with zipfile.ZipFile(fp) as z:
            for name in z.namelist():
                if name.endswith("/"): continue
                data=z.read(name); low=name.lower(); ss=strings(data)
                if any(t in low for t in TERMS) or ss:
                    resources.append({
                      "artifact_id":a["artifact_id"],"coordinate":a["coordinate"],"entry_path":name,
                      "entry_size":len(data),"entry_sha256":h256(data),
                      "path_term_hit":any(t in low for t in TERMS),"matched_strings":ss
                    })

identity={"schema":"BPESEM05R01_PROVIDER_ARTIFACT_IDENTITY_REGISTRY_V0_3","acquisition_plan_blob":PLAN_BLOB,"artifact_count":len(ids),"all_official_sha1_checks":"PASS","records":ids,"no_market_data_object_acquired":True}
inventory={"schema":"BPESEM05R01_RELEVANT_CLASS_RESOURCE_INVENTORY_V0_3","acquisition_plan_blob":PLAN_BLOB,"terms":TERMS,"record_count":len(resources),"records":resources,"no_market_data_object_acquired":True}
pomset={"schema":"BPESEM05R01_PROVIDER_POM_SNAPSHOT_SET_V0_3","acquisition_plan_blob":PLAN_BLOB,"records":poms}
for fn,obj in [
 ("provider_artifact_identity_registry_v0_3.json",identity),
 ("relevant_class_resource_inventory_v0_3.json",inventory),
 ("provider_pom_snapshot_set_v0_3.json",pomset)
]:
    (OUT/fn).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

print(json.dumps({"artifact_count":len(ids),"resource_records":len(resources),"all_sha1_checks":"PASS","no_market_data_object_acquired":True},indent=2))

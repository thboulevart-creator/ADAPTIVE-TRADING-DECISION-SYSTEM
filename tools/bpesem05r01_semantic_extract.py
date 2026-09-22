#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, subprocess, tempfile, urllib.parse, urllib.request, zipfile
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PLAN_PATH=ROOT/"evidence"/"bpesem05r01"/"provider_artifact_semantic_extraction_plan_v0_1.json"
OUT=ROOT/"evidence"/"bpesem05r01"
PLAN_BLOB="b5dd1bfc3cbd217b7294407adf74855b2127a486"
ALLOW_PREFIX="https://www.dukascopy.com/client/jforexlib/publicrepo/"
MAX_BYTES=20_000_000
ASCII_RE=re.compile(rb"[\x20-\x7e]{4,}")

def git_blob(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()
def h256(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def fetch(url:str)->bytes:
    if not url.startswith(ALLOW_PREFIX): raise RuntimeError("URL outside allowlist")
    p=urllib.parse.urlparse(url)
    if p.hostname!="www.dukascopy.com": raise RuntimeError("unexpected host")
    if ".bi5" in p.path.lower() or "/datafeed/" in p.path.lower():
        raise RuntimeError("market-data object URL forbidden")
    req=urllib.request.Request(url,headers={"User-Agent":"BPESEM05R01-documentary-recovery/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        data=r.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES: raise RuntimeError("artifact too large")
        return data
def sha1_sidecar(url:str)->str:
    raw=fetch(url).decode("ascii","strict").strip().split()[0].lower()
    if not re.fullmatch(r"[0-9a-f]{40}",raw): raise RuntimeError("bad sha1 sidecar")
    return raw
def ascii_strings(data:bytes)->list[str]:
    return [m.decode("utf-8","ignore") for m in ASCII_RE.findall(data)]

if git_blob(PLAN_PATH)!=PLAN_BLOB: raise RuntimeError("semantic extraction plan blob mismatch")
plan=json.loads(PLAN_PATH.read_text(encoding="utf-8"))
if not plan["frozen_before_fetch"]: raise RuntimeError("plan not frozen")

identities=[]
javap_records=[]
msg_records=[]
msg_poms=[]
with tempfile.TemporaryDirectory(prefix="bpesem05r01-sem-") as td_raw:
    td=Path(td_raw)
    jars={}
    for f in plan["fetches"]:
        raw=fetch(f["url"])
        sh256=h256(raw)
        rec={"artifact_id":f["artifact_id"],"url":f["url"],"size_bytes":len(raw),"computed_sha256":sh256}
        if "expected_sha256" in f:
            rec["expected_sha256"]=f["expected_sha256"]
            rec["expected_sha256_verification"]="PASS" if sh256==f["expected_sha256"] else "FAIL"
            if sh256!=f["expected_sha256"]: raise RuntimeError("reinspection SHA256 mismatch "+f["artifact_id"])
        if "sha1_url" in f:
            official=sha1_sidecar(f["sha1_url"])
            local=hashlib.sha1(raw).hexdigest()
            if official!=local: raise RuntimeError("msg SHA1 mismatch "+f["artifact_id"])
            rec["official_sha1"]=official; rec["computed_sha1"]=local; rec["sha1_verification"]="PASS"
            pom=fetch(f["pom_url"]); poff=sha1_sidecar(f["pom_sha1_url"]); plocal=hashlib.sha1(pom).hexdigest()
            if poff!=plocal: raise RuntimeError("msg POM SHA1 mismatch "+f["artifact_id"])
            rec["pom_sha256"]=h256(pom); rec["pom_official_sha1"]=poff; rec["pom_sha1_verification"]="PASS"
            msg_poms.append({"artifact_id":f["artifact_id"],"pom_sha256":h256(pom),"pom_text":pom.decode("utf-8","replace")})
        fp=td/(f["artifact_id"]+".jar"); fp.write_bytes(raw); jars[f["artifact_id"]]=fp
        identities.append(rec)

    # Exact bytecode extraction from pinned greed-common baseline/latest.
    for aid in ["GREED-COMMON-318.4.115-REINSPECTION","GREED-COMMON-318.4.128-REINSPECTION"]:
        jar=jars[aid]
        with zipfile.ZipFile(jar) as z:
            for cls in plan["javap_targets"]:
                entry=cls.replace(".","/")+".class"
                data=z.read(entry)
                cp=subprocess.run(["javap","-classpath",str(jar),"-c","-p","-constants",cls],text=True,capture_output=True,check=False)
                if cp.returncode!=0: raise RuntimeError("javap failed "+aid+" "+cls+"\n"+cp.stderr)
                out=cp.stdout
                javap_records.append({
                    "artifact_id":aid,
                    "class_name":cls,
                    "class_entry":entry,
                    "class_sha256":h256(data),
                    "javap_sha256":h256(out.encode()),
                    "javap_text":out
                })

    # Compact transport/msg semantic inventory.
    terms=[x.lower() for x in plan["msg_search_terms"]]
    for aid in ["MSG-1.1.98.2-JFOREX3","MSG-1.1.98.4-JFOREX3"]:
        jar=jars[aid]
        with zipfile.ZipFile(jar) as z:
            for name in z.namelist():
                if name.endswith("/"): continue
                data=z.read(name)
                ss=ascii_strings(data)
                joined=(name+"\n"+"\n".join(ss)).lower()
                hits=[t for t in terms if t in joined]
                if not hits: continue
                matched=[]
                for s in ss:
                    if any(t in s.lower() for t in terms):
                        matched.append(s[:1200])
                    if len(matched)>=80: break
                msg_records.append({
                    "artifact_id":aid,"entry_path":name,"entry_sha256":h256(data),
                    "hits":hits,"matched_strings":matched
                })

identity={
 "schema":"BPESEM05R01_SEMANTIC_EXTRACTION_IDENTITY_REGISTRY_V0_1",
 "plan_blob":PLAN_BLOB,"records":identities,"no_market_data_object_acquired":True
}
bytecode={
 "schema":"BPESEM05R01_PINNED_GREED_BYTECODE_EXTRACTION_V0_1",
 "plan_blob":PLAN_BLOB,"records":javap_records,"no_network_beyond_planned_provider_artifacts":True
}
msg={
 "schema":"BPESEM05R01_MSG_SEMANTIC_INVENTORY_V0_1",
 "plan_blob":PLAN_BLOB,"record_count":len(msg_records),"records":msg_records,
 "pom_records":msg_poms,"no_market_data_object_acquired":True
}

for fn,obj in [
 ("semantic_extraction_identity_registry_v0_1.json",identity),
 ("pinned_greed_bytecode_extraction_v0_1.json",bytecode),
 ("msg_semantic_inventory_v0_1.json",msg)
]:
    (OUT/fn).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

print(json.dumps({
 "identity_records":len(identities),
 "javap_records":len(javap_records),
 "msg_records":len(msg_records),
 "no_market_data_object_acquired":True
},indent=2))

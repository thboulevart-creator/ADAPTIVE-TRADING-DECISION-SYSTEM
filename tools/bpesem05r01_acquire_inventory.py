#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PLAN_PATH=ROOT/"evidence"/"bpesem05r01"/"provider_artifact_acquisition_plan_v0_1.json"
OUT=ROOT/"evidence"/"bpesem05r01"
PLAN_BLOB="e6e3c2a671ade38ec34f2dad03c02e2e20d06adc"
ALLOW_PREFIX="https://www.dukascopy.com/client/jforexlib/publicrepo/"
MAX_ARTIFACT_BYTES=20_000_000
TERMS=["bi5","history","historical","tick","instrument","usatech","decimal","scale","factor","jetta","cache","feed","data"]
ASCII_RE=re.compile(rb"[\x20-\x7e]{4,}")

def git_blob(path:Path)->str:
    import subprocess
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def sha256_bytes(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()

def fetch(url:str)->bytes:
    if not url.startswith(ALLOW_PREFIX):
        raise RuntimeError("URL outside provider allowlist: "+url)
    parsed=urllib.parse.urlparse(url)
    if parsed.hostname!="www.dukascopy.com":
        raise RuntimeError("unexpected host")
    if ".bi5" in parsed.path.lower() or "/datafeed/" in parsed.path.lower():
        raise RuntimeError("market-data object URL forbidden")
    req=urllib.request.Request(url,headers={"User-Agent":"BPESEM05R01-documentary-recovery/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        data=r.read(MAX_ARTIFACT_BYTES+1)
        if len(data)>MAX_ARTIFACT_BYTES:
            raise RuntimeError("artifact exceeds bounded maximum: "+url)
        return data

def parse_sha1(b:bytes)->str:
    s=b.decode("ascii","strict").strip().split()[0].lower()
    if not re.fullmatch(r"[0-9a-f]{40}",s):
        raise RuntimeError("invalid sha1 sidecar")
    return s

def relevant_strings(data:bytes)->list[str]:
    out=[]
    seen=set()
    for m in ASCII_RE.findall(data):
        try:
            s=m.decode("utf-8","ignore")
        except Exception:
            continue
        low=s.lower()
        if any(t in low for t in TERMS):
            s=s[:1000]
            if s not in seen:
                out.append(s); seen.add(s)
        if len(out)>=80:
            break
    return out

if git_blob(PLAN_PATH)!=PLAN_BLOB:
    raise RuntimeError("acquisition plan blob mismatch")
plan=json.loads(PLAN_PATH.read_text(encoding="utf-8"))
if not plan.get("frozen_before_first_artifact_fetch"):
    raise RuntimeError("plan not frozen")
if any(a.get("market_data_object") for a in plan["artifacts"]):
    raise RuntimeError("market data artifact in acquisition plan")

identity_records=[]
resource_records=[]
pom_records=[]
with tempfile.TemporaryDirectory(prefix="bpesem05r01-") as td:
    td=Path(td)
    for a in plan["artifacts"]:
        artifact_bytes=fetch(a["url"])
        official_sha1=parse_sha1(fetch(a["sha1_url"]))
        local_sha1=hashlib.sha1(artifact_bytes).hexdigest()
        if local_sha1!=official_sha1:
            raise RuntimeError("artifact official SHA1 mismatch: "+a["artifact_id"])
        pom_bytes=fetch(a["pom_url"])
        pom_official_sha1=parse_sha1(fetch(a["pom_sha1_url"]))
        pom_local_sha1=hashlib.sha1(pom_bytes).hexdigest()
        if pom_local_sha1!=pom_official_sha1:
            raise RuntimeError("POM official SHA1 mismatch: "+a["artifact_id"])

        fp=td/(a["artifact_id"]+".jar")
        fp.write_bytes(artifact_bytes)
        identity_records.append({
            "artifact_id":a["artifact_id"],
            "coordinate":a["coordinate"],
            "url":a["url"],
            "artifact_type":a["artifact_type"],
            "size_bytes":len(artifact_bytes),
            "official_sha1":official_sha1,
            "computed_sha1":local_sha1,
            "sha1_verification":"PASS",
            "computed_sha256":sha256_bytes(artifact_bytes),
            "pom_url":a["pom_url"],
            "pom_size_bytes":len(pom_bytes),
            "pom_official_sha1":pom_official_sha1,
            "pom_computed_sha1":pom_local_sha1,
            "pom_sha1_verification":"PASS",
            "pom_computed_sha256":sha256_bytes(pom_bytes),
        })
        pom_records.append({
            "artifact_id":a["artifact_id"],
            "coordinate":a["coordinate"],
            "pom_sha256":sha256_bytes(pom_bytes),
            "pom_text":pom_bytes.decode("utf-8","replace")
        })

        try:
            with zipfile.ZipFile(fp) as z:
                names=z.namelist()
                for name in names:
                    low=name.lower()
                    path_hit=any(t in low for t in TERMS)
                    if name.endswith("/"):
                        continue
                    data=z.read(name)
                    strings=relevant_strings(data)
                    if path_hit or strings:
                        resource_records.append({
                            "artifact_id":a["artifact_id"],
                            "coordinate":a["coordinate"],
                            "entry_path":name,
                            "entry_size":len(data),
                            "entry_sha256":sha256_bytes(data),
                            "path_term_hit":path_hit,
                            "matched_strings":strings,
                        })
        except zipfile.BadZipFile:
            raise RuntimeError("not a valid JAR/ZIP: "+a["artifact_id"])

identity={
    "schema":"BPESEM05R01_PROVIDER_ARTIFACT_IDENTITY_REGISTRY_V0_1",
    "acquisition_plan_blob":PLAN_BLOB,
    "provider_origin":"Dukascopy official Maven/public repository",
    "artifact_count":len(identity_records),
    "all_official_sha1_checks":"PASS",
    "records":identity_records,
    "no_market_data_object_acquired":True
}
inventory={
    "schema":"BPESEM05R01_RELEVANT_CLASS_RESOURCE_INVENTORY_V0_1",
    "acquisition_plan_blob":PLAN_BLOB,
    "terms":TERMS,
    "record_count":len(resource_records),
    "records":resource_records,
    "no_market_data_object_acquired":True
}
poms={
    "schema":"BPESEM05R01_PROVIDER_POM_SNAPSHOT_SET_V0_1",
    "acquisition_plan_blob":PLAN_BLOB,
    "records":pom_records
}
for fn,obj in [
    ("provider_artifact_identity_registry_v0_1.json",identity),
    ("relevant_class_resource_inventory_v0_1.json",inventory),
    ("provider_pom_snapshot_set_v0_1.json",poms),
]:
    (OUT/fn).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

summary={
    "artifact_count":len(identity_records),
    "resource_records":len(resource_records),
    "artifact_sha256":{x["artifact_id"]:x["computed_sha256"] for x in identity_records},
    "all_sha1_checks":"PASS",
    "no_market_data_object_acquired":True,
}
print(json.dumps(summary,indent=2))

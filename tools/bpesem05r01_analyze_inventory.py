#!/usr/bin/env python3
from __future__ import annotations
import json, re, hashlib
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05r01"
INV=json.loads((E/"relevant_class_resource_inventory_v0_1.json").read_text(encoding="utf-8"))
POMS=json.loads((E/"provider_pom_snapshot_set_v0_1.json").read_text(encoding="utf-8"))
IDS=json.loads((E/"provider_artifact_identity_registry_v0_1.json").read_text(encoding="utf-8"))

FOCUS=["bi5","usatech","decimal","factor","history","historical","jetta","tick","instrument","scale"]
def rec_text(r):
    return (r["entry_path"]+"\n"+"\n".join(r.get("matched_strings",[]))).lower()

term_hits={}
for t in FOCUS:
    rs=[r for r in INV["records"] if t in rec_text(r)]
    term_hits[t]={
        "record_count":len(rs),
        "records":[{
            "artifact_id":r["artifact_id"],
            "entry_path":r["entry_path"],
            "entry_sha256":r["entry_sha256"],
            "matched_strings":[s for s in r.get("matched_strings",[]) if t in s.lower()][:12]
        } for r in rs[:80]]
    }

# Cross-version DDS2 path/hash ledger for relevant entries.
dds=[r for r in INV["records"] if r["artifact_id"].startswith("DDS2-JCLIENT-")]
by_path=defaultdict(dict)
for r in dds:
    ver=r["artifact_id"].replace("DDS2-JCLIENT-","").replace("-JAR","")
    by_path[r["entry_path"]][ver]=r["entry_sha256"]
ledger=[]
versions=["3.6.34","3.6.37","3.6.48","3.6.49","3.6.51"]
for p,m in by_path.items():
    if len(m)<2: continue
    vals=[m.get(v) for v in versions]
    changed=len(set(x for x in vals if x is not None))>1 or any(x is None for x in vals)
    if changed:
        ledger.append({"entry_path":p,"hash_by_version":m,"changed":True})
ledger.sort(key=lambda x:x["entry_path"])

# Dependency summaries.
pom_deps=[]
for r in POMS["records"]:
    txt=r["pom_text"]
    try:
        root=ET.fromstring(txt)
        deps=[]
        for d in root.findall(".//dependency"):
            def tx(tag):
                e=d.find(tag); return (e.text or "").strip() if e is not None else None
            deps.append({"groupId":tx("groupId"),"artifactId":tx("artifactId"),"version":tx("version"),"scope":tx("scope")})
        props={}
        pe=root.find("properties")
        if pe is not None:
            for child in list(pe):
                props[child.tag]=(child.text or "").strip()
        pom_deps.append({"artifact_id":r["artifact_id"],"dependencies":deps,"properties":props})
    except Exception as e:
        pom_deps.append({"artifact_id":r["artifact_id"],"parse_error":str(e)})

# Focus candidates scored by number of focus terms.
candidates=[]
for r in INV["records"]:
    txt=rec_text(r)
    hits=[t for t in FOCUS if t in txt]
    if len(hits)>=2 or any(t in txt for t in ["bi5","usatech","jetta"]):
        candidates.append({
            "artifact_id":r["artifact_id"],
            "entry_path":r["entry_path"],
            "entry_sha256":r["entry_sha256"],
            "hits":hits,
            "matched_strings":r.get("matched_strings",[])[:30]
        })
candidates.sort(key=lambda x:(-len(x["hits"]),x["entry_path"],x["artifact_id"]))

out={
  "schema":"BPESEM05R01_PROVIDER_ARTIFACT_INVENTORY_ANALYSIS_V0_1",
  "identity_registry_blob_expected":"ff0e950eef72dee5497e6db480cd8ce9e16fc31a",
  "inventory_blob_expected":"92e1d8a467682f530bde4c2e34bf718d638eddc3",
  "artifact_count":IDS["artifact_count"],
  "term_hits":term_hits,
  "focus_candidates":candidates[:250],
  "changed_relevant_entries_count":len(ledger),
  "changed_relevant_entries":ledger[:500],
  "pom_dependency_summaries":pom_deps,
  "no_network_performed":True
}
(E/"provider_artifact_inventory_analysis_v0_1.json").write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps({
 "artifact_count":out["artifact_count"],
 "term_counts":{k:v["record_count"] for k,v in term_hits.items()},
 "focus_candidates":len(candidates),
 "changed_relevant_entries":len(ledger)
},indent=2))

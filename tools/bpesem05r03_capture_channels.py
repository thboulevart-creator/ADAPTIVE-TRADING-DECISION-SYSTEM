#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, subprocess, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"evidence"/"bpesem05r03"/"provider_channel_acquisition_plan_v0_1.json"
OUT=ROOT/"evidence"/"bpesem05r03"
PLAN_BLOB="83f82b27898c1a6fbe0a31ef04196317e2f972ff"
MAX_BYTES=3_000_000

def git_blob(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

class Inspector(HTMLParser):
    def __init__(self,base:str):
        super().__init__(convert_charrefs=True)
        self.base=base
        self.title=[]
        self.in_title=False
        self.forms=[]
        self.current_form=None
        self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="title":
            self.in_title=True
        if tag=="form":
            action=urllib.parse.urljoin(self.base,d.get("action",""))
            self.current_form={"action":action,"method":d.get("method","get").upper(),"controls":[]}
            self.forms.append(self.current_form)
        if tag in {"input","select","textarea","button"} and self.current_form is not None:
            item={
                "tag":tag,
                "name":d.get("name"),
                "type":d.get("type"),
                "id":d.get("id"),
                "required":("required" in d),
                "value_present":("value" in d),
            }
            # Do not persist dynamic values/tokens.
            self.current_form["controls"].append(item)
    def handle_endtag(self,tag):
        if tag=="title":
            self.in_title=False
        if tag=="form":
            self.current_form=None
    def handle_data(self,data):
        if self.in_title:
            self.title.append(data)
        s=" ".join(data.split())
        if s:
            self.text.append(s)

def safe_get(url:str):
    u=urllib.parse.urlparse(url)
    if u.scheme!="https" or not (u.hostname=="www.dukascopy.com" or (u.hostname or "").endswith(".dukascopy.com")):
        raise RuntimeError("non-provider URL forbidden: "+url)
    if "/datafeed/" in u.path.lower() or ".bi5" in u.path.lower():
        raise RuntimeError("market-data URL forbidden")
    req=urllib.request.Request(url,method="GET",headers={"User-Agent":"BPESEM05R03-channel-resolution/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r:
        final=r.geturl()
        fu=urllib.parse.urlparse(final)
        if not (fu.hostname=="www.dukascopy.com" or (fu.hostname or "").endswith(".dukascopy.com")):
            raise RuntimeError("redirect outside provider domain: "+final)
        data=r.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:
            raise RuntimeError("response exceeds bound")
        return {
            "final_url":final,
            "status":getattr(r,"status",200),
            "content_type":r.headers.get("Content-Type"),
            "data":data,
        }

if git_blob(PLAN)!=PLAN_BLOB:
    raise RuntimeError("channel acquisition plan blob mismatch")
plan=json.loads(PLAN.read_text(encoding="utf-8"))
if plan["allowed_methods"]!=["GET"]:
    raise RuntimeError("only GET allowed")

records=[]
for candidate in plan["candidates"]:
    res=safe_get(candidate["url"])
    text=res["data"].decode("utf-8","replace")
    ins=Inspector(res["final_url"]); ins.feed(text)
    normalized_text=" ".join(ins.text)
    lower=normalized_text.lower()
    records.append({
        "channel_id":candidate["channel_id"],
        "declared_class":candidate["class"],
        "requested_url":candidate["url"],
        "final_url":res["final_url"],
        "http_status":res["status"],
        "content_type":res["content_type"],
        "raw_response_sha256":hashlib.sha256(res["data"]).hexdigest(),
        "size_bytes":len(res["data"]),
        "html_title":" ".join(ins.title).strip(),
        "forms":ins.forms,
        "signals":{
            "dukascopy_bank_marker":("Dukascopy Bank SA" in normalized_text),
            "copyright_dukascopy_marker":bool(re.search(r"©\s*1998-2026\s+Dukascopy",normalized_text,re.I)),
            "login_marker":("login" in lower),
            "cannot_post_new_topics":("you cannot post new topics in this forum" in lower),
            "programming_questions_only":("submit programming questions in this forum only" in lower),
            "send_us_message_marker":("send us a message" in lower),
            "message_not_sent_marker":("message has not been sent" in lower),
            "issue_report_marker":("report an issue" in lower or "issue report" in lower),
            "contact_form_required_login_marker":("login name" in lower),
        },
        "selected_nonsecret_text_markers":[
            s for s in [
                "Send us a message" if "send us a message" in lower else None,
                "Message has not been sent" if "message has not been sent" in lower else None,
                "Submit programming questions in this forum only." if "submit programming questions in this forum only" in lower else None,
                "You cannot post new topics in this forum" if "you cannot post new topics in this forum" in lower else None,
                "Dukascopy Bank SA" if "Dukascopy Bank SA" in normalized_text else None,
            ] if s
        ],
    })

capture={
    "schema":"BPESEM05R03_PROVIDER_CHANNEL_READONLY_CAPTURE_V0_1",
    "plan_blob":PLAN_BLOB,
    "method_used":"GET_ONLY",
    "records":records,
    "no_form_submission":True,
    "no_email_sent":True,
    "no_ticket_created":True,
    "no_inquiry_sent":True,
    "no_market_data_object_requested":True,
}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"provider_channel_readonly_capture_v0_1.json").write_text(
    json.dumps(capture,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8"
)
print(json.dumps({
    "records":len(records),
    "channels":{r["channel_id"]:{
        "status":r["http_status"],
        "sha256":r["raw_response_sha256"],
        "forms":len(r["forms"]),
        "final_url":r["final_url"]
    } for r in records},
    "no_contact":True
},indent=2))

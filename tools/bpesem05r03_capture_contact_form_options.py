#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"evidence"/"bpesem05r03"/"provider_channel_acquisition_plan_v0_1.json"
OUT=ROOT/"evidence"/"bpesem05r03"/"provider_contact_form_options_v0_1.json"
PLAN_BLOB="83f82b27898c1a6fbe0a31ef04196317e2f972ff"

def git_blob(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

class SelectParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current_select=None
        self.current_option=None
        self.selects={}
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="select":
            self.current_select=d.get("name") or d.get("id")
            if self.current_select:
                self.selects.setdefault(self.current_select,[])
        elif tag=="option" and self.current_select:
            self.current_option={
                "value":d.get("value"),
                "selected":("selected" in d),
                "disabled":("disabled" in d),
                "text":""
            }
    def handle_data(self,data):
        if self.current_option is not None:
            self.current_option["text"] += data
    def handle_endtag(self,tag):
        if tag=="option" and self.current_option is not None and self.current_select:
            self.current_option["text"]=" ".join(self.current_option["text"].split())
            self.selects[self.current_select].append(self.current_option)
            self.current_option=None
        elif tag=="select":
            self.current_select=None

if git_blob(PLAN)!=PLAN_BLOB:
    raise RuntimeError("plan identity mismatch")
plan=json.loads(PLAN.read_text(encoding="utf-8"))
candidate=[x for x in plan["candidates"] if x["channel_id"]=="DUKASCOPY_SWISS_CONTACT_FORM"][0]
url=candidate["url"]
u=urllib.parse.urlparse(url)
if u.hostname!="www.dukascopy.com" or u.scheme!="https":
    raise RuntimeError("unexpected host")
req=urllib.request.Request(url,method="GET",headers={"User-Agent":"BPESEM05R03-channel-resolution/1.0"})
with urllib.request.urlopen(req,timeout=45) as r:
    data=r.read(500000)
    final=r.geturl()
if urllib.parse.urlparse(final).hostname!="www.dukascopy.com":
    raise RuntimeError("redirect outside provider")
p=SelectParser(); p.feed(data.decode("utf-8","replace"))
out={
  "schema":"BPESEM05R03_PROVIDER_CONTACT_FORM_OPTIONS_V0_1",
  "plan_blob":PLAN_BLOB,
  "channel_id":"DUKASCOPY_SWISS_CONTACT_FORM",
  "requested_url":url,
  "final_url":final,
  "raw_response_sha256":hashlib.sha256(data).hexdigest(),
  "select_options":p.selects,
  "method_used":"GET_ONLY",
  "no_form_submission":True,
  "no_contact":True
}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(out,indent=2))

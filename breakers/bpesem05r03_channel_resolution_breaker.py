#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, subprocess, urllib.parse
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05r03"
REPORT=Path(os.environ.get("BPESEM05R03_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem05r03_channel_resolution_adversarial_break_2026-09-22.md")))

INPUTS={
"evidence/bpesem05r02/provider_primary_authority_inquiry_contract_v0_1.json":"3eeb079b834102a2c8983563bd21088ad50796ed",
"evidence/bpesem05r02/inquiry_contract_qualification_v0_1.json":"87971297e47bfe78e030dadf0a61c03e94b4957a",
"reports/data-qualification/bpesem05r02_final_closeout_2026-09-22.md":"d69741d86d6bcac0a413e5e08f1ca889f612b14e",
"99-BACKUP/SESSION-2026-09-22-BPESEM05R02-FINAL-CLOSEOUT.md":"225f5d8fd4e38d0493b5d6d0bd2969e7f928a841",
"reports/data-qualification/post_bpesem05r02_qualified_inquiry_contract_consumer_route_selection_2026-09-22.md":"b05b6b1e0afd2d1ea02a57f8fd123b72187c0501",
"evidence/bpesem05r03/provider_channel_acquisition_plan_v0_1.json":"83f82b27898c1a6fbe0a31ef04196317e2f972ff",
"evidence/bpesem05r03/provider_channel_readonly_capture_v0_1.json":"6e02a39d728c001ac5e6c80ce4689ea5b2622737",
"evidence/bpesem05r03/provider_contact_form_options_v0_1.json":"8d541369f7512da015f1da171cafc90f4712444a",
}

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def blob(path:str)->str:
    return git("hash-object",path)
def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None)
    return hashlib.sha256(canon(x)).hexdigest()
def read(name:str)->dict:
    return json.loads((E/name).read_text(encoding="utf-8"))

attacks=[]; defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond: defects.append(name)

check("R01_GOVERNED_INPUT_IDENTITIES",all(blob(p)==b for p,b in INPUTS.items()),"qualified contract and channel captures remain exact")

inventory=read("provider_contact_channel_inventory_v0_1.json")
owner=read("provider_channel_ownership_evidence_v0_1.json")
binding=read("provider_channel_identity_binding_v0_1.json")
constraints=read("channel_constraint_manifest_v0_1.json")
auth=read("channel_authentication_requirement_v0_1.json")
cap=read("outbound_capability_constraints_v0_1.json")
decision=read("channel_resolution_decision_v0_1.json")
horizon=read("current_channel_evidence_horizon_v0_1.json")
attest=read("no_contact_execution_attestation_v0_1.json")

for name,obj,field in [
 ("R02_INVENTORY_SEAL",inventory,"inventory_seal"),
 ("R03_OWNERSHIP_SEAL",owner,"ownership_seal"),
 ("R04_BINDING_SEAL",binding,"decision_seal"),
 ("R05_CONSTRAINT_SEAL",constraints,"constraint_seal"),
 ("R06_AUTH_SEAL",auth,"authentication_seal"),
 ("R07_CAPABILITY_SEAL",cap,"capability_seal"),
 ("R08_DECISION_SEAL",decision,"decision_seal"),
 ("R09_HORIZON_SEAL",horizon,"horizon_seal"),
 ("R10_ATTESTATION_SEAL",attest,"attestation_seal"),
]:
    check(name,obj[field]==seal(obj,field),field+" recomputes")

check("R11_EXACT_THREE_ACTIONABLE_CHANNELS",len(inventory["channels"])==3,"general contact, report issue and knowledge-base candidates adjudicated")

sel=decision["selected_channel"]
check("R12_EXACT_SELECTED_ENDPOINT",
      sel["endpoint"]=="https://www.dukascopy.com/plugins/contactForm/?b=swiss&id=contact&lang=en&mob=0"
      and urllib.parse.urlparse(sel["endpoint"]).hostname=="www.dukascopy.com",
      "exact provider-controlled endpoint bound")

check("R13_PROVIDER_OWNERSHIP_VERIFIED",
      owner["ownership_status"]=="VERIFIED_PROVIDER_CONTROLLED_CHANNEL"
      and all(x.get("same_provider_controlled_host",True) for x in owner["evidence"]),
      "ownership is bound to provider landing page and provider-controlled host")

check("R14_RESULT_BOUND",
      decision["result"]=="OFFICIAL_PROVIDER_CHANNEL_BOUND",
      "Stage R reaches exact allowed PASS taxonomy")

check("R15_TECHNICAL_TOPIC_EXACT",
      sel["topic_value"]=="3" and sel["topic_label"]=="Live trading support. Technical support",
      "technical-support topic is exact")

req=constraints["required_fields"]
check("R16_REQUIRED_FIELDS_EXACT",
      set(req)=={"clear_mode","clear_firstname","clear_lastname","clear_email","clear_details"}
      and all(v["required"] for v in req.values()),
      "all captured required fields are preserved")

opt=constraints["optional_fields"]
check("R17_LOGIN_OPTIONAL",
      opt["clear_login"]["required"] is False and auth["account_login_required_by_observed_html"] is False,
      "account login is not required by captured contact form")

check("R18_PHONE_OPTIONAL",
      opt["clear_phone"]["required"] is False,
      "phone is optional")

check("R19_NO_SUBJECT_ASSUMPTION",
      constraints["observed_capabilities"]["subject_field_observed"] is False and cap["subject_supported"] is False,
      "Stage P cannot invent a subject field")

check("R20_NO_ATTACHMENT_ASSUMPTION",
      constraints["observed_capabilities"]["attachment_field_observed"] is False and cap["attachments_observed"] is False,
      "Stage P cannot assume attachments")

check("R21_DETAILS_BODY_PRESENT",
      constraints["observed_capabilities"]["free_text_details_field_observed"] is True and cap["single_free_text_body_field"]=="clear_details",
      "deterministic inquiry body field exists")

check("R22_REPORT_ISSUE_REJECTED",
      any(x["channel_id"]=="REPORT_ISSUE" and "LOGIN_NAME_REQUIRED" in x["reason_codes"] for x in decision["rejected_channels"]),
      "issue-report route not arbitrarily selected")

check("R23_FORUM_REJECTED_CAPTURED_STATE",
      any(x["channel_id"]=="JFOREX_KNOWLEDGE_BASE" and "CANNOT_POST_NEW_TOPICS_IN_CAPTURED_STATE" in x["reason_codes"] for x in decision["rejected_channels"]),
      "forum captured state cannot post")

check("R24_NO_CHANNEL_AMBIGUITY",
      inventory["channels"][0]["candidate_status"]=="ELIGIBLE"
      and sum(1 for x in inventory["channels"] if x["candidate_status"]=="ELIGIBLE")==1,
      "exactly one eligible initial channel remains")

check("R25_NO_PACKAGE_MATERIALIZATION",
      cap["final_outbound_package_not_materialized"] is True
      and attest["final_outbound_package_materialized"] is False,
      "Stage R does not create outbound inquiry package")

check("R26_NO_SEND_AUTHORIZATION",
      decision["send_authorized"] is False and decision["contact_authorized"] is False,
      "channel binding cannot authorize send")

check("R27_STAGE_P_ONLY_NEXT_EFFECT",
      decision["outbound_package_materialization_authorized_next"] is True,
      "only Stage P package materialization becomes eligible next")

check("R28_MUTABILITY_FAIL_REOPEN",
      "fail/reopen" in horizon["known_mutability"],
      "material channel changes before send require reopen")

check("R29_CAPTURE_SUFFICIENT_FOR_STAGE_P",
      horizon["selected_channel_constraints_sufficient_for_stage_p"] is True,
      "required channel constraints are known")

check("R30_ALL_CONTACT_FLAGS_FALSE",
      all(v is False for v in attest.values() if isinstance(v,bool)),
      "no contact, submission, market-data or downstream execution occurred")

check("R31_FORM_METHOD_RECORDED_NOT_EXECUTED",
      constraints["form_method"]=="POST" and attest["form_submitted"] is False,
      "future method is known but was not executed")

check("R32_IDENTITY_VALUES_DEFERRED",
      cap["requires_user_identity_values_before_stage_p_completion"] is True,
      "Stage R does not invent personal identity values")

check("R33_EXECUTION_MECHANISM_DEFERRED",
      cap["execution_mechanism_not_selected"] is True,
      "manual/browser/tool execution is not preselected")

check("R34_NO_LANE_S_OR_LANE_P",
      attest["lane_s_readjudication"] is False and attest["lane_p"] is False,
      "no authority/downstream stage leak")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=["# B-PE-SEM-05R-03 — CHANNEL RESOLUTION ADVERSARIAL BREAK","",
       "Persisted candidate HEAD attacked: "+git("rev-parse","HEAD"),"",
       "Breaker verdict: "+verdict,""]
for n,s,d in attacks:
    lines += ["## "+n,"",s+" — "+d,""]
lines += ["## Result","","~~~text",
          "attack count = "+str(len(attacks)),
          "demonstrated defects = "+str(len(defects)),
          *(defects or ["NONE"]),
          "~~~","",
          "PASS qualifies only official channel resolution. It does not authorize contact or send.","",
          "No form submission, email, support ticket, inquiry, BI5 request, Lane S re-adjudication or Lane P work occurred.","","STOP."]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":git("rev-parse","HEAD"),"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))

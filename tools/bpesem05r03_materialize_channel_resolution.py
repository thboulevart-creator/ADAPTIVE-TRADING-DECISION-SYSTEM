#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem05r03"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r03_channel_resolution_candidate_2026-09-22.md"

INPUTS={
"04-REFERENCE/AI-OPERATING-MEMORY.md":"0ec6687b288bdd76284fe05e2e437d3bd2b89518",
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
def write(name:str,obj:dict):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

for p,b in INPUTS.items():
    if blob(p)!=b:
        raise RuntimeError("governed input blob mismatch: "+p)

head=git("rev-parse","HEAD")
capture=json.loads((ROOT/"evidence/bpesem05r03/provider_channel_readonly_capture_v0_1.json").read_text(encoding="utf-8"))
options=json.loads((ROOT/"evidence/bpesem05r03/provider_contact_form_options_v0_1.json").read_text(encoding="utf-8"))
records={r["channel_id"]:r for r in capture["records"]}
contact=records["DUKASCOPY_SWISS_CONTACT_FORM"]
landing=records["DUKASCOPY_SWISS_GENERAL_CONTACT_PAGE"]
issue=records["DUKASCOPY_SWISS_REPORT_ISSUE"]
forum=records["DUKASCOPY_JFOREX_KNOWLEDGE_BASE"]

contact_form=contact["forms"][0]
controls={x["name"]:x for x in contact_form["controls"] if x.get("name")}
mode_options=options["select_options"]["clear_mode"]
technical=[x for x in mode_options if x["value"]=="3" and x["text"]=="Live trading support. Technical support"]
if len(technical)!=1:
    raise RuntimeError("exact technical-support option not uniquely present")

inventory={
 "schema":"BPESEM05R03_PROVIDER_CONTACT_CHANNEL_INVENTORY_V0_1",
 "candidate_parent_head":head,
 "source_capture_blob":INPUTS["evidence/bpesem05r03/provider_channel_readonly_capture_v0_1.json"],
 "channels":[
  {"channel_id":"GENERAL_CONTACT_FORM","source_id":"DUKASCOPY_SWISS_CONTACT_FORM","channel_class":"official_provider_contact_form","endpoint":contact["final_url"],"http_status":contact["http_status"],"raw_capture_sha256":contact["raw_response_sha256"],"candidate_status":"ELIGIBLE"},
  {"channel_id":"REPORT_ISSUE","source_id":"DUKASCOPY_SWISS_REPORT_ISSUE","channel_class":"official_provider_issue_report_form","endpoint":issue["final_url"],"http_status":issue["http_status"],"raw_capture_sha256":issue["raw_response_sha256"],"candidate_status":"NOT_SELECTED"},
  {"channel_id":"JFOREX_KNOWLEDGE_BASE","source_id":"DUKASCOPY_JFOREX_KNOWLEDGE_BASE","channel_class":"official_provider_public_support_forum","endpoint":forum["final_url"],"http_status":forum["http_status"],"raw_capture_sha256":forum["raw_response_sha256"],"candidate_status":"NOT_SELECTED"},
 ],
 "no_contact_performed":True
}
inventory["inventory_seal"]=seal(inventory,"inventory_seal")

ownership={
 "schema":"BPESEM05R03_PROVIDER_CHANNEL_OWNERSHIP_EVIDENCE_V0_1",
 "provider":"Dukascopy Bank SA",
 "selected_channel_id":"GENERAL_CONTACT_FORM",
 "evidence":[
  {"type":"provider_landing_page","url":landing["final_url"],"raw_sha256":landing["raw_response_sha256"],"dukascopy_bank_marker":landing["signals"]["dukascopy_bank_marker"],"copyright_marker":landing["signals"]["copyright_dukascopy_marker"],"send_us_message_marker":landing["signals"]["send_us_message_marker"]},
  {"type":"selected_endpoint_host_binding","url":contact["final_url"],"host":"www.dukascopy.com","same_provider_controlled_host":True},
 ],
 "ownership_status":"VERIFIED_PROVIDER_CONTROLLED_CHANNEL"
}
ownership["ownership_seal"]=seal(ownership,"ownership_seal")

constraints={
 "schema":"BPESEM05R03_CHANNEL_CONSTRAINT_MANIFEST_V0_1",
 "selected_channel_id":"GENERAL_CONTACT_FORM",
 "endpoint":contact["final_url"],
 "form_method":"POST",
 "required_fields":{
   "clear_mode":{"required":controls["clear_mode"]["required"],"selected_option_value":"3","selected_option_label":"Live trading support. Technical support"},
   "clear_firstname":{"required":controls["clear_firstname"]["required"]},
   "clear_lastname":{"required":controls["clear_lastname"]["required"]},
   "clear_email":{"required":controls["clear_email"]["required"]},
   "clear_details":{"required":controls["clear_details"]["required"]},
 },
 "optional_fields":{
   "clear_login":{"required":controls["clear_login"]["required"]},
   "clear_phone":{"required":controls["clear_phone"]["required"]},
 },
 "observed_capabilities":{
   "subject_field_observed":False,
   "free_text_details_field_observed":True,
   "attachment_field_observed":False,
   "captcha_field_observed":False,
   "explicit_login_required":False
 },
 "available_mode_options":mode_options,
 "package_materialization_effect":"Stage P must bind mode=3 plus user identity fields and exact sealed inquiry body; no package is materialized in Stage R."
}
constraints["constraint_seal"]=seal(constraints,"constraint_seal")

auth={
 "schema":"BPESEM05R03_CHANNEL_AUTHENTICATION_REQUIREMENT_V0_1",
 "selected_channel_id":"GENERAL_CONTACT_FORM",
 "account_login_required_by_observed_html":False,
 "login_field_present":True,
 "login_field_required":False,
 "required_identity_fields":["clear_firstname","clear_lastname","clear_email"],
 "optional_identity_fields":["clear_login","clear_phone"],
 "authentication_status":"NO_ACCOUNT_AUTHENTICATION_REQUIRED_BY_CAPTURED_FORM_CONSTRAINTS"
}
auth["authentication_seal"]=seal(auth,"authentication_seal")

cap={
 "schema":"BPESEM05R03_OUTBOUND_CAPABILITY_CONSTRAINTS_V0_1",
 "selected_channel_id":"GENERAL_CONTACT_FORM",
 "single_free_text_body_field":"clear_details",
 "topic_field":"clear_mode",
 "topic_binding":{"value":"3","label":"Live trading support. Technical support"},
 "subject_supported":False,
 "attachments_observed":False,
 "requires_user_identity_values_before_stage_p_completion":True,
 "execution_mechanism_not_selected":True,
 "final_outbound_package_not_materialized":True
}
cap["capability_seal"]=seal(cap,"capability_seal")

decision={
 "schema":"BPESEM05R03_CHANNEL_RESOLUTION_DECISION_V0_1",
 "result":"OFFICIAL_PROVIDER_CHANNEL_BOUND",
 "selected_channel":{
   "channel_id":"GENERAL_CONTACT_FORM",
   "provider":"Dukascopy Bank SA",
   "channel_class":"official_provider_contact_form",
   "endpoint":"https://www.dukascopy.com/plugins/contactForm/?b=swiss&id=contact&lang=en&mob=0",
   "method_for_future_submission":"POST",
   "topic_value":"3",
   "topic_label":"Live trading support. Technical support"
 },
 "selection_rationale":[
   "Provider-owned general contact landing page explicitly routes users to Send us a message.",
   "Selected form is on the provider-controlled dukascopy.com host.",
   "The form exposes an exact technical-support topic value 3.",
   "The captured form does not require an account login; identity is supplied through required first name, last name and email fields.",
   "The form provides a free-text details field suitable for the qualified inquiry body.",
   "Report an Issue is issue/complaint-oriented and requires login plus complaint classification.",
   "JForex Knowledge Base is programming-specific but is not postable in the captured anonymous state and is a public forum."
 ],
 "rejected_channels":[
   {"channel_id":"REPORT_ISSUE","reason_codes":["ISSUE_REPORT_SCOPE_NARROWER_THAN_GENERAL_TECHNICAL_INQUIRY","LOGIN_NAME_REQUIRED","COMPLAINT_TYPE_REQUIRED"]},
   {"channel_id":"JFOREX_KNOWLEDGE_BASE","reason_codes":["CANNOT_POST_NEW_TOPICS_IN_CAPTURED_STATE","AUTHENTICATION_OR_ACCOUNT_STATE_REQUIRED","PUBLIC_FORUM_PROVENANCE_AND_EXPOSURE"]},
 ],
 "contact_authorized":False,
 "contact_performed":False,
 "outbound_package_materialization_authorized_next":True,
 "send_authorized":False
}
decision["decision_seal"]=seal(decision,"decision_seal")

horizon={
 "schema":"BPESEM05R03_CURRENT_CHANNEL_EVIDENCE_HORIZON_V0_1",
 "captured_channel_pages":5,
 "source_capture_blob":"6e02a39d728c001ac5e6c80ce4689ea5b2622737",
 "contact_form_options_blob":"8d541369f7512da015f1da171cafc90f4712444a",
 "selected_channel_current_raw_sha256":contact["raw_response_sha256"],
 "selected_channel_constraints_sufficient_for_stage_p":True,
 "known_mutability":"Provider web forms are live mutable surfaces; Stage P must bind this exact Stage R evidence and fail/reopen if material channel constraints change before send.",
 "overall_status":"OFFICIAL_PROVIDER_CHANNEL_BOUND"
}
horizon["horizon_seal"]=seal(horizon,"horizon_seal")

attest={
 "schema":"BPESEM05R03_NO_CONTACT_EXECUTION_ATTESTATION_V0_1",
 "provider_contact":False,
 "provider_inquiry_sent":False,
 "support_ticket_created":False,
 "form_submitted":False,
 "email_sent":False,
 "final_outbound_package_materialized":False,
 "provider_bi5_get":False,
 "historical_market_data_object_acquisition":False,
 "lane_s_readjudication":False,
 "lane_p":False,
 "full_interval":False,
 "d_materialization":False,
 "backtest":False,
 "paper_broker_live":False
}
attest["attestation_seal"]=seal(attest,"attestation_seal")

for name,obj in [
 ("provider_contact_channel_inventory_v0_1.json",inventory),
 ("provider_channel_ownership_evidence_v0_1.json",ownership),
 ("provider_channel_identity_binding_v0_1.json",decision),
 ("channel_constraint_manifest_v0_1.json",constraints),
 ("channel_authentication_requirement_v0_1.json",auth),
 ("outbound_capability_constraints_v0_1.json",cap),
 ("channel_resolution_decision_v0_1.json",decision),
 ("current_channel_evidence_horizon_v0_1.json",horizon),
 ("no_contact_execution_attestation_v0_1.json",attest),
]:
    write(name,obj)

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(f"""# B-PE-SEM-05R-03 — OFFICIAL PROVIDER CONTACT CHANNEL RESOLUTION — CANDIDATE

Candidate parent HEAD: {head}

Result:

~~~text
channel resolution = OFFICIAL_PROVIDER_CHANNEL_BOUND

selected channel =
Dukascopy Swiss official Send us a message form

endpoint =
https://www.dukascopy.com/plugins/contactForm/?b=swiss&id=contact&lang=en&mob=0

future topic =
value 3
Live trading support. Technical support

account authentication required by captured form =
NO

required identity fields =
first name
last name
email

required message field =
details

provider contact performed =
NO

outbound package materialized =
NO

send authorized =
NO
~~~

Report an Issue was not selected because it is issue/complaint-oriented and requires a login field plus complaint classification.

The JForex Knowledge Base was not selected because the captured anonymous state says new topics cannot be posted.

No provider contact, form submission, email, support ticket, inquiry, BI5 request, Lane S re-adjudication or Lane P work occurred.
""",encoding="utf-8")

print(json.dumps({
 "candidate_parent_head":head,
 "result":decision["result"],
 "selected_endpoint":decision["selected_channel"]["endpoint"],
 "topic":decision["selected_channel"]["topic_value"],
 "contact_performed":decision["contact_performed"],
 "send_authorized":decision["send_authorized"]
},indent=2))

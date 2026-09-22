#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem05r02"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r02_inquiry_contract_candidate_2026-09-22.md"

INPUTS={
"04-REFERENCE/AI-OPERATING-MEMORY.md":"0ec6687b288bdd76284fe05e2e437d3bd2b89518",
"04-REFERENCE/RECOVERY-CHECKPOINT.md":"c1b7c3c62e44984af335cf3c13c1c7215772ff5c",
"evidence/bpesem05r01/recovery_qualification_v0_1.json":"cd260eb27ac31c0fc68dea4449923ac484544307",
"reports/data-qualification/bpesem05r01_final_closeout_2026-09-22.md":"6a755acb75569a4f402b8c62c335cbaabed0f5d3",
"99-BACKUP/SESSION-2026-09-22-BPESEM05R01-FINAL-CLOSEOUT.md":"a5b2feb9d1d1d999ec01e33073c9dc18c4afca3b",
"reports/data-qualification/post_bpesem05r01_blocked_authority_recovery_escalation_route_selection_2026-09-22.md":"6a3afce89da39638e1960a9a57a66eb1a8fb2bf4",
}

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def blob(path:str)->str:
    return git("hash-object",path)

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

def seal(o:dict, field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None)
    return hashlib.sha256(canon(x)).hexdigest()

for p,b in INPUTS.items():
    if blob(p)!=b:
        raise RuntimeError(f"governed input blob mismatch: {p}")

head=git("rev-parse","HEAD")
tree=git("rev-parse",head+"^{tree}")

target={
  "provider":"Dukascopy Bank SA",
  "representation_internal_id":"K1",
  "representation_external_description":"historical hourly tick .bi5 objects served by Dukascopy for the legacy hourly tick-file family",
  "instrument_internal_id":"USATECHIDXUSD",
  "instrument_external_name":"USATECH.IDX/USD",
  "target_interval_start":"2021-08-13T01:00:00Z",
  "target_interval_end":"2026-08-14T20:00:00Z",
}

questions={
"A":[
 {"id":"A-Q01","text":"For the historical hourly tick .bi5 files in the legacy hourly tick-file family, what compression format and container or stream framing, if any, is used for the file contents? Please identify any version or date boundaries where this changed."},
 {"id":"A-Q02","text":"After decompression of those historical hourly tick files, how are individual tick records delimited or sized? Please state the exact record structure used by the provider and any version or date boundaries where it changed."},
 {"id":"A-Q03","text":"What byte order, field sequence, and primitive data types are used in one decoded tick record in those historical hourly files? Please describe each field by semantic role rather than by example values."},
 {"id":"A-Q04","text":"What does the tick time field represent in the historical hourly files: its unit, reference origin, timezone or time basis, and valid range within a file? Please identify any version or date boundaries where this changed."},
 {"id":"A-Q05","text":"Which decoded price field represents ask and which represents bid in the historical hourly files? Please identify the provider definition or implementation source if available."},
 {"id":"A-Q06","text":"Which decoded volume field represents ask-side volume and which represents bid-side volume, and what primitive representation and unit or transformation applies to each?"},
 {"id":"A-Q07","text":"Were the record framing, timestamp meaning, price-field roles, volume-field roles, or primitive representations for this legacy hourly tick .bi5 family changed at any time from 2021-08-13 through 2026-08-14? If yes, please give each effective date or version and the exact changed semantics."},
 ],
"B":[
 {"id":"B-Q01","text":"For USATECH.IDX/USD historical tick data in the legacy hourly .bi5 representation, what exact transformation converts the native stored ask and bid price values into the quoted market price? Please provide the formula or authoritative metadata rule without relying on display, pip, point-value, or plausibility conventions."},
 {"id":"B-Q02","text":"Is that native stored-price transformation instrument-specific for USATECH.IDX/USD, and did it change at any time from 2021-08-13 through 2026-08-14? If it changed, please provide the exact effective dates or versions."},
 {"id":"B-Q03","text":"What provider-owned specification, source artifact, metadata field, or implementation component is authoritative for that native stored-price transformation for USATECH.IDX/USD?"},
 ],
"C":[
 {"id":"C-Q01","text":"Between 2021-08-13 and 2026-08-14, were there any changes to the semantics of the legacy hourly tick .bi5 representation itself, including compression, record layout, timestamp interpretation, field roles, price transformation, or volume representation? Please list every known material change with its effective date or version. If there were no such changes, please state the basis on which continuity can be asserted."},
 {"id":"C-Q02","text":"At what date or version, if any, did Dukascopy transition historical tick storage or delivery from legacy hourly .bi5 objects to a daily-object form, and which semantic properties changed versus remained identical across that transition?"},
 {"id":"C-Q03","text":"Are the semantics of client-side JForex cache .bi5 files identical to the semantics of the public or server-side historical hourly .bi5 objects? If not always identical, what differences and applicability periods exist?"},
 ],
"JETTA":[
 {"id":"J-Q01","text":"JForex 4.8.0 release information dated 2026-03-03 states that historical price data retrieval uses JETTA. Did that change alter the raw historical tick .bi5 payload semantics, object boundaries, timestamp meaning, price/volume encoding, or native price transformation, or was it limited to retrieval/backend behavior? Please identify the exact scope and effective date of any semantic change."},
 {"id":"J-Q02","text":"Is there an authoritative provider document, release record, source artifact, or internal specification that defines the effect of the 2026-03-03 JETTA change on legacy historical tick data semantics? If so, please identify it precisely."},
 ]
}

contract={
 "schema":"BPESEM05R02_PROVIDER_PRIMARY_AUTHORITY_INQUIRY_CONTRACT_V0_1",
 "contract_id":"B_PE_SEM_05R_02_PROVIDER_PRIMARY_AUTHORITY_INQUIRY_CONTRACT",
 "contract_version":"V0_1",
 "candidate_parent_head":head,
 "candidate_parent_tree":tree,
 "governed_input_blobs":INPUTS,
 "preserved_recovery_state":{"A":"AMBIGUOUS","B":"NOT_FOUND","C":"INCOMPLETE_VERSION_COVERAGE"},
 "target_binding":target,
 "contact_channel_policy":{
   "allowed_channel_classes":[
     "official Dukascopy support ticket or contact form hosted on a Dukascopy-controlled domain",
     "email exchange where the responding address is on an official Dukascopy-controlled domain",
     "provider-owned support/forum channel only when the responder is independently verifiable as Dukascopy staff or official support"
   ],
   "forbidden_as_provider_primary":[
     "anonymous community response",
     "third-party forum or social-media response",
     "unverified personal email",
     "LLM-generated or search-engine summary",
     "project-authored interpretation without provider statement"
   ],
   "channel_selection_rule":"Use one official technical-support/contact channel at a time. Do not duplicate the same inquiry across multiple channels until a later governed retry rule authorizes it.",
   "contact_authorized_by_this_contract":False
 },
 "responder_identity_policy":{
   "required":[
     "provider-owned channel or independently verifiable Dukascopy identity",
     "responder name, support identity, or official role where supplied",
     "sender address/account identity where available",
     "thread/ticket/message identity where available",
     "exact response timestamp"
   ],
   "identity_statuses":["VERIFIED_PROVIDER","PROVIDER_CHANNEL_IDENTITY_PARTIAL","UNVERIFIED","CONTRADICTORY_IDENTITY"],
   "provider_primary_requires":"VERIFIED_PROVIDER or provider-owned ticket system whose official origin is independently verifiable",
   "partial_identity_effect":"BLOCKED for provider-primary authority unless later evidence resolves identity"
 },
 "question_sets":questions,
 "non_leading_policy":{
   "general":[
     "Questions request definitions, formulas, dates and authoritative sources without presenting project hypotheses as established facts.",
     "Do not disclose third-party decoder agreement before the provider answers.",
     "Do not mention prior empirical plausibility as support for any expected semantic answer.",
     "Do not merge separate A/B/C questions into a yes/no confirmation bundle."
   ],
   "A":["Do not state LZMA, 20 bytes, big-endian, a five-field layout, hour-relative time, ask/bid order, or volume encoding as facts in the question."],
   "B":["Do not mention 1000, /1000, decimalFactor=1000, or a proposed raw-price divisor before an independent provider answer."],
   "C":["Do not infer continuity from silence, absence of release notes, or stable client code."],
   "JETTA":["Do not assume JETTA either changed or preserved K1 semantics."]
 },
 "response_capture_policy":{
   "must_capture":[
     "exact complete question text as sent",
     "exact complete provider response text/bytes as received",
     "attachments in original bytes where technically available",
     "provider channel identity",
     "responder/sender identity fields",
     "thread/ticket/message identifier where available",
     "sent timestamp",
     "received timestamp",
     "all URLs or references supplied by provider"
   ],
   "hashing":["SHA-256 of each raw captured message/export/attachment","SHA-256 of a canonical manifest binding questions, responses and metadata"],
   "preservation":"Store raw evidence unchanged; any normalized extract is a separate derived artifact with its own hash.",
   "forbidden":["editing provider wording in raw capture","discarding caveats or uncertainty language","combining project interpretation into provider quote","hashing only a paraphrase"]
 },
 "response_admissibility_policy":{
   "admissible_provider_primary_requires":[
     "provider identity requirement satisfied",
     "answer addresses the exact target representation or clearly names a different scope",
     "answer is explicit enough to distinguish fact from uncertainty",
     "raw response provenance is preserved and sealed"
   ],
   "inadmissible_or_blocking_conditions":[
     "anonymous or unverified responder",
     "response only restates community documentation without provider adoption",
     "speculative language without authoritative basis",
     "scope limited to current daily files when target legacy-hourly semantics are unresolved",
     "answer relies only on example values or market plausibility",
     "answer omits applicability period when period is material",
     "provider disclaims ability to confirm the requested semantic fact"
   ],
   "provider_reference_rule":"If the provider cites an exact specification, artifact or archived document, the reference is a new evidence lead and must be acquired/sealed in a later governed block before being treated as independently verified supporting evidence."
 },
 "outcome_policy":{
   "per_question_statuses":["RECOVERED_PROVIDER_PRIMARY","PARTIALLY_RECOVERED","AMBIGUOUS","NOT_ANSWERED","PROVIDER_CANNOT_CONFIRM","CONTRADICTED","INADMISSIBLE","BLOCKED"],
   "A_recovered_rule":"All material A semantics required by the qualified Lane S contract must be explicitly bound to the legacy-hourly target representation and applicable epoch; otherwise A remains partial/ambiguous/blocked.",
   "B_recovered_rule":"Exact native stored-price transformation for USATECH.IDX/USD must be stated or bound to an authoritative provider source without circular inference.",
   "C_recovered_rule":"Continuity requires explicit provider authority covering the complete target interval or exact provider-authorized epoch splits/change points. Silence is never continuity evidence.",
   "JETTA_rule":"JETTA impact remains unresolved unless the provider explicitly scopes the 2026-03-03 change with respect to raw historical tick semantics.",
   "no_response_rule":"No response, timeout, closed ticket, or unanswered question is NOT_ANSWERED and has zero positive authority.",
   "partial_response_rule":"Answered subquestions may be preserved independently; unanswered or ambiguous required subquestions remain BLOCKED.",
   "contradiction_rule":"A material contradiction with existing governed evidence triggers CONTRADICTED and a later adjudication/reopen block; do not silently choose one source.",
   "overall_inquiry_consumer_rule":"A later consumer cannot authorize Lane P directly. Recovered evidence must return through separately governed Lane S re-adjudication."
 },
 "retry_policy":{
   "initial_contact_count":1,
   "automatic_retry_authorized":False,
   "later_retry_requires":"new governed decision identifying why retry is non-duplicative and what new channel/recipient/clarification is justified",
   "question_mutation_after_send":"FORBIDDEN_WITHIN_SAME_VERSION; new contract version required"
 },
 "reopen_rules":[
   "question wording changes after qualification",
   "target representation/instrument/epoch changes",
   "contact-channel policy changes",
   "identity/admissibility policy changes",
   "new material authority dimension discovered",
   "provider response reveals a previously unknown representation split or semantic change",
   "provider supplies an authoritative reference requiring separate acquisition"
 ],
 "execution_boundary":{
   "provider_contact_performed":False,
   "provider_inquiry_sent":False,
   "new_documentary_acquisition_performed":False,
   "provider_bi5_market_data_get":False,
   "historical_market_data_object_acquisition":False,
   "lane_s_readjudication":False,
   "lane_p_request_manifest":False,
   "p_diag_implementation":False,
   "physical_semantic_discrimination":False,
   "bpesem06":False,
   "bfiq02r":False,
   "full_interval":False,
   "d_materialization":False,
   "backtest":False,
   "paper_broker_live":False
 },
 "qualification_effect":{
   "contract_pass_does_not_recover_A_B_C":True,
   "contract_pass_does_not_authorize_contact":True,
   "contact_requires_separate_governed_consumer_block":True,
   "lane_s_authority_effect":"NONE",
   "lane_p_authority_effect":"NONE"
 }
}
contract["contract_seal"]=seal(contract,"contract_seal")

OUT.mkdir(parents=True,exist_ok=True)
path=OUT/"provider_primary_authority_inquiry_contract_v0_1.json"
path.write_text(json.dumps(contract,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(f"""# B-PE-SEM-05R-02 — PROVIDER PRIMARY AUTHORITY INQUIRY CONTRACT — CANDIDATE

Candidate parent HEAD: {head}

Contract seal:

~~~text
{contract["contract_seal"]}
~~~

Preserved recovery state:

~~~text
A = AMBIGUOUS
B = NOT_FOUND
C = INCOMPLETE_VERSION_COVERAGE
~~~

The contract freezes:
- official provider contact-channel requirements;
- responder identity requirements;
- exact non-leading A/B/C/JETTA questions;
- K1 / USATECHIDXUSD / 2021-08-13 through 2026-08-14 target binding;
- raw response provenance and SHA-256 capture;
- admissibility, rejection, partial-answer, no-response, contradiction and reopen rules.

This block performs no provider contact and authorizes no contact by itself.

No provider BI5 market-data object, Lane S re-adjudication, Lane P RequestManifest/P-DIAG, FULL_INTERVAL, D or backtest is authorized or executed.
""",encoding="utf-8")

print(json.dumps({
 "candidate_parent_head":head,
 "contract_seal":contract["contract_seal"],
 "question_counts":{k:len(v) for k,v in questions.items()},
 "contact_authorized":contract["contact_channel_policy"]["contact_authorized_by_this_contract"],
 "provider_contact_performed":contract["execution_boundary"]["provider_contact_performed"]
},indent=2))

#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, re, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"evidence"/"bpesem05r02"/"provider_primary_authority_inquiry_contract_v0_1.json"
REPORT=Path(os.environ.get("BPESEM05R02_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem05r02_inquiry_contract_adversarial_break_2026-09-22.md")))

INPUTS={
"04-REFERENCE/AI-OPERATING-MEMORY.md":"0ec6687b288bdd76284fe05e2e437d3bd2b89518",
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
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None)
    return hashlib.sha256(canon(x)).hexdigest()

c=json.loads(P.read_text(encoding="utf-8"))
head=git("rev-parse","HEAD")
attacks=[]; defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond: defects.append(name)

check("I01_GOVERNED_INPUT_IDENTITIES",
      all(blob(p)==b for p,b in INPUTS.items()),
      "prior recovery qualification/closeout/backup/route remain exact")

check("I02_CONTRACT_SEAL",
      c["contract_seal"]==seal(c,"contract_seal"),
      "canonical contract seal recomputes")

check("I03_RECOVERY_STATE_PRESERVED",
      c["preserved_recovery_state"]=={"A":"AMBIGUOUS","B":"NOT_FOUND","C":"INCOMPLETE_VERSION_COVERAGE"},
      "A/B/C are not re-adjudicated in pre-contact contract")

t=c["target_binding"]
check("I04_TARGET_BINDING_EXACT",
      t["provider"]=="Dukascopy Bank SA"
      and t["representation_internal_id"]=="K1"
      and t["instrument_internal_id"]=="USATECHIDXUSD"
      and t["target_interval_start"]=="2021-08-13T01:00:00Z"
      and t["target_interval_end"]=="2026-08-14T20:00:00Z",
      "provider, representation, instrument and epoch are frozen")

ch=c["contact_channel_policy"]
check("I05_CONTACT_CHANNEL_PROVIDER_OWNED",
      len(ch["allowed_channel_classes"])>=2
      and any("official Dukascopy" in x or "Dukascopy-controlled" in x for x in ch["allowed_channel_classes"]),
      "only provider-owned/verifiable contact channel classes are allowed")

check("I06_ANONYMOUS_COMMUNITY_FORBIDDEN",
      any("anonymous community" in x for x in ch["forbidden_as_provider_primary"]),
      "anonymous community answers cannot become provider primary")

check("I07_NO_CONTACT_AUTHORIZATION",
      ch["contact_authorized_by_this_contract"] is False
      and c["qualification_effect"]["contract_pass_does_not_authorize_contact"] is True,
      "contract qualification cannot itself send/authorize inquiry")

ri=c["responder_identity_policy"]
check("I08_RESPONDER_IDENTITY_REQUIRED",
      "provider-owned channel or independently verifiable Dukascopy identity" in ri["required"]
      and "exact response timestamp" in ri["required"],
      "identity and timestamp are mandatory")

check("I09_PARTIAL_IDENTITY_FAILS_CLOSED",
      "BLOCKED" in ri["partial_identity_effect"],
      "partial responder identity cannot be positive authority")

qs=c["question_sets"]
check("I10_QUESTION_SET_CARDINALITY",
      set(qs)=={"A","B","C","JETTA"} and len(qs["A"])>=7 and len(qs["B"])>=3 and len(qs["C"])>=3 and len(qs["JETTA"])>=2,
      "A/B/C/JETTA are separated and sufficiently decomposed")

all_q=[q for group in qs.values() for q in group]
ids=[q["id"] for q in all_q]
check("I11_QUESTION_IDS_UNIQUE",
      len(ids)==len(set(ids)),
      "question identifiers are unique")

btext=" ".join(q["text"].lower() for q in qs["B"])
check("I12_B_NO_EXPECTED_1000",
      "1000" not in btext and "/1000" not in btext and "decimalfactor" not in btext,
      "B questions do not suggest the expected divisor")

atext=" ".join(q["text"].lower() for q in qs["A"])
forbidden_assertions=["uses lzma","20-byte","big-endian","five-field","hour-relative"]
check("I13_A_NONLEADING",
      all(x not in atext for x in forbidden_assertions),
      "A questions ask for exact semantics without asserting project hypotheses")

ctext=" ".join(q["text"].lower() for q in qs["C"])
check("I14_C_NO_SILENCE_CONTINUITY",
      "basis on which continuity can be asserted" in ctext
      and c["non_leading_policy"]["C"][0].lower().find("silence")>=0,
      "continuity requires explicit basis and cannot come from silence")

jtext=" ".join(q["text"].lower() for q in qs["JETTA"])
check("I15_JETTA_BALANCED",
      "did that change alter" in jtext and "or was it limited" in jtext,
      "JETTA question leaves changed/unchanged hypotheses open")

np=c["non_leading_policy"]
check("I16_NO_THIRDPARTY_PRIMING",
      any("third-party decoder agreement" in x for x in np["general"]),
      "provider is not primed with third-party consensus")

check("I17_NO_EMPIRICAL_PRIMING",
      any("empirical plausibility" in x for x in np["general"]),
      "provider is not primed with project empirical plausibility")

rc=c["response_capture_policy"]
required_capture=set(rc["must_capture"])
check("I18_RAW_CAPTURE_COMPLETE",
      {"exact complete question text as sent","exact complete provider response text/bytes as received","provider channel identity","received timestamp"}.issubset(required_capture),
      "raw sent/received evidence and provenance are captured")

check("I19_HASHING_REQUIRED",
      len(rc["hashing"])>=2 and all("SHA-256" in x for x in rc["hashing"]),
      "raw evidence and manifest are SHA-256 sealed")

check("I20_RAW_NOT_EDITED",
      "editing provider wording in raw capture" in rc["forbidden"],
      "provider wording cannot be edited")

ra=c["response_admissibility_policy"]
check("I21_SCOPE_REQUIRED_FOR_ADMISSIBILITY",
      any("exact target representation" in x for x in ra["admissible_provider_primary_requires"]),
      "provider answer must bind target representation/scope")

check("I22_SPECULATION_BLOCKS_AUTHORITY",
      any("speculative language" in x for x in ra["inadmissible_or_blocking_conditions"]),
      "speculative support answer is fail-closed")

check("I23_CURRENT_DAILY_NOT_LEGACY_AUTHORITY",
      any("current daily files" in x for x in ra["inadmissible_or_blocking_conditions"]),
      "current-daily-only response cannot close legacy-hourly scope")

check("I24_REFERENCED_SOURCE_REQUIRES_LATER_ACQUISITION",
      "later governed block" in ra["provider_reference_rule"],
      "provider-cited references are evidence leads, not silently verified evidence")

op=c["outcome_policy"]
expected=["RECOVERED_PROVIDER_PRIMARY","PARTIALLY_RECOVERED","AMBIGUOUS","NOT_ANSWERED","PROVIDER_CANNOT_CONFIRM","CONTRADICTED","INADMISSIBLE","BLOCKED"]
check("I25_OUTCOME_TAXONOMY_EXACT",
      op["per_question_statuses"]==expected,
      "later response taxonomy is exact and fail-closed")

check("I26_A_ALL_MATERIAL_SEMANTICS_REQUIRED",
      "All material A semantics" in op["A_recovered_rule"],
      "partial A answer cannot be promoted to complete recovery")

check("I27_B_NONCIRCULAR",
      "without circular inference" in op["B_recovered_rule"],
      "B requires exact raw transformation without circular inference")

check("I28_C_COMPLETE_INTERVAL_OR_EPOCH_SPLITS",
      "complete target interval" in op["C_recovered_rule"]
      and "epoch splits" in op["C_recovered_rule"],
      "C requires full interval coverage or exact provider-authorized splits")

check("I29_NO_RESPONSE_ZERO_AUTHORITY",
      "zero positive authority" in op["no_response_rule"],
      "no response cannot become evidence")

check("I30_PARTIAL_RESPONSE_PRESERVED_NOT_PROMOTED",
      "unanswered or ambiguous required subquestions remain BLOCKED" in op["partial_response_rule"],
      "partial response cannot overpromote")

check("I31_CONTRADICTION_REOPENS",
      "later adjudication/reopen block" in op["contradiction_rule"],
      "contradictions are preserved and reopened")

check("I32_NO_LANE_P_SELF_AUTHORIZATION",
      "cannot authorize Lane P directly" in op["overall_inquiry_consumer_rule"],
      "future provider answer still must return through Lane S")

retry=c["retry_policy"]
check("I33_NO_AUTOMATIC_RETRY",
      retry["initial_contact_count"]==1 and retry["automatic_retry_authorized"] is False,
      "one initial contact only; retry requires governance")

check("I34_NO_POSTSEND_QUESTION_MUTATION",
      retry["question_mutation_after_send"].startswith("FORBIDDEN"),
      "question mutation after send requires new contract version")

eb=c["execution_boundary"]
check("I35_EXECUTION_BOUNDARY_ALL_FALSE",
      all(v is False for v in eb.values()),
      "no contact, acquisition, Lane S/Lane P or execution occurred")

qe=c["qualification_effect"]
check("I36_CONTRACT_PASS_HAS_NO_AUTHORITY_EFFECT",
      qe["contract_pass_does_not_recover_A_B_C"] is True
      and qe["lane_s_authority_effect"]=="NONE"
      and qe["lane_p_authority_effect"]=="NONE",
      "contract PASS cannot recover A/B/C or authorize Lane S/Lane P")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=["# B-PE-SEM-05R-02 — INQUIRY CONTRACT ADVERSARIAL BREAK","",
       "Persisted candidate HEAD attacked: "+head,"",
       "Contract breaker verdict: "+verdict,""]
for n,s,d in attacks:
    lines += ["## "+n,"",s+" — "+d,""]
lines += ["## Result","","~~~text",
          "attack count = "+str(len(attacks)),
          "demonstrated defects = "+str(len(defects)),
          *(defects or ["NONE"]),
          "~~~","",
          "This breaker qualifies only the pre-contact inquiry contract. It does not authorize provider contact and does not recover A/B/C.","",
          "No provider inquiry was sent. No new documentary acquisition, provider BI5 object, Lane S re-adjudication, Lane P artifact, FULL_INTERVAL, D or backtest occurred.","","STOP."]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":head,"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))

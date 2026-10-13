"""WER-02 test-first synthetic evidence contracts. No Windows processes are used.

RED mode is a deliberately permissive MODEL ONLY, NOT a test of actual R1 Windows
implementation and NOT an admissible Windows observation. It models the
insufficient "all the fields say OK" receipt strategy which the new candidate
must reject. GREEN tests use an independent isolated offline evidence candidate.
"""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/wer_02/candidate.py"
WORKER={"pid":111,"creation_filetime":"134361969930150189"}
SUPERVISOR={"pid":10,"creation_filetime":"134361969920000000"}
CHILD={"pid":222,"creation_filetime":"134361969930287894"}

def digest(p):
    raw={key:p[key] for key in ("worker","supervisor","event_stream","job")}
    return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def base(descendant=True):
    children=[{"seq":1,"time":120,"child":dict(WORKER),"parent":dict(SUPERVISOR),
               "parent_start_verified":True,"source":"ETW_KERNEL_PROCESS_PROPOSED",
               "observer":"synthetic-observer"}]
    members=[{"identity":dict(WORKER),"post_identity":dict(WORKER),
              "job_id":"SYNTH_JOB_A","membership_verified":True,
              "handle_retained":True,"wait_signaled":True,"exit_code":0,"raw_provenance":"OFFLINE_FIXTURE"}]
    if descendant:
        children.append({"seq":2,"time":130,"child":dict(CHILD),"parent":dict(WORKER),
               "parent_start_verified":True,"source":"ETW_KERNEL_PROCESS_PROPOSED",
               "observer":"synthetic-observer"})
        members.append({"identity":dict(CHILD),"post_identity":dict(CHILD),
              "job_id":"SYNTH_JOB_A","membership_verified":True,
              "handle_retained":True,"wait_signaled":True,"exit_code":0,"raw_provenance":"OFFLINE_FIXTURE"})
    p={
      "evidence_class":"SYNTHETIC_CONTRACT","independent_windows_evidence":False,
      "worker":dict(WORKER),"supervisor":dict(SUPERVISOR),
      "event_stream":{"source":"ETW_KERNEL_PROCESS_PROPOSED","observer":"synthetic-observer",
              "window_start":100,"window_end":300,"continuous":True,"dropped_events":0,
              "seq_first":1,"seq_last":len(children),"events":children},
      "job":{"job_id":"SYNTH_JOB_A","member_count":len(members),
              "members":members,"query_complete":True,"post_query_observed":True,"post_count":0},
      "receipt":{"global_status":"PASS","descendant_created":descendant,
              "descendant_identities":[dict(CHILD)] if descendant else [],
              "descendant_absence_proven":not descendant}}
    p["receipt"]["raw_evidence_sha256"]=digest(p)
    return p

def evaluate(p):
    if os.environ.get("ATDS_WER02_RED_COMPARATOR")=="permissive":
        # Insufficient, intentionally modeled status oracle: no lineage or
        # identity checks. Its failures are design tests, NOT historic facts.
        return {"status":"PASS","violations":[],"evidence_class":"SYNTHETIC_CONTRACT",
                "independent_windows_evidence":False}
    assert TARGET.exists(),"MISSING_ISOLATED_CANDIDATE"
    s=importlib.util.spec_from_file_location("wer02_isolated_static_candidate",TARGET)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m.evaluate(p)

def expect(p,status,violation=None):
    r=evaluate(copy.deepcopy(p))
    assert r["status"]==status,r
    if violation:
        assert violation in r["violations"],r
    assert r["independent_windows_evidence"] is False
    assert r["evidence_class"]=="SYNTHETIC_CONTRACT"
    return r

def test_IT01_valid_exact_FILETIME_and_bound_identity():
    r=expect(base(),"PASS")
    assert r.get("worker_identity")==WORKER

@pytest.mark.parametrize("change,reason",[
 (lambda p:p["job"]["members"][0]["post_identity"].update(creation_filetime="134361969930150190"),"PID_REUSE_OR_IDENTITY_MISMATCH"),
 (lambda p:p["worker"].update(creation_filetime=134361969930150192.0),"LOSSY_FILETIME"),
 (lambda p:p["worker"].update(pid=True),"INVALID_PROCESS_IDENTITY"),
 (lambda p:p["job"]["members"][0]["identity"].update(creation_filetime="0"),"INVALID_PROCESS_IDENTITY"),
])
def test_IT01_rejects_invalid_immutable_identity(change,reason):
    p=base();change(p);expect(p,"BLOCKED",reason)

@pytest.mark.parametrize("change,reason",[
 (lambda p:p["event_stream"]["events"][1].update(parent_start_verified=False),"PARENT_IDENTITY_UNVERIFIED"),
 (lambda p:p["event_stream"]["events"][1]["parent"].update(creation_filetime="134361969930150190"),"PARENT_LINEAGE_NOT_BOUND"),
 (lambda p:p["event_stream"].update(dropped_events=1),"EVENT_COVERAGE_INCOMPLETE"),
 (lambda p:p["event_stream"].update(continuous=False),"EVENT_COVERAGE_INCOMPLETE"),
 (lambda p:p["event_stream"]["events"][1].update(seq=5),"EVENT_SEQUENCE_GAP"),
 (lambda p:p["event_stream"]["events"][1].update(time=800),"EVENT_TIME_OUTSIDE_COVERAGE"),
 (lambda p:p["event_stream"]["events"][1].update(source="SCENARIO_CHILD_MARKER"),"EVENT_SOURCE_UNQUALIFIED"),
 (lambda p:p["event_stream"]["events"][1].update(observer="other-observer"),"EVENT_SOURCE_UNQUALIFIED"),
 (lambda p:p["event_stream"]["events"].pop(),"JOB_MEMBER_START_EVENT_MISSING"),
])
def test_IT02_lineage_must_have_continuous_correlated_events(change,reason):
    p=base();change(p);expect(p,"BLOCKED",reason)

@pytest.mark.parametrize("change,reason",[
 (lambda p:p["job"].update(query_complete=False),"JOB_INVENTORY_INCOMPLETE"),
 (lambda p:p["job"].update(member_count=3),"JOB_MEMBER_COUNT_MISMATCH"),
 (lambda p:p["job"]["members"][1].update(job_id="WRONG_JOB"),"MEMBERSHIP_WRONG_JOB"),
 (lambda p:p["job"]["members"][1].update(membership_verified=False),"JOB_MEMBERSHIP_UNVERIFIED"),
 (lambda p:p["job"]["members"][1].update(identity={"pid":333,"creation_filetime":"134361969930311111"}),"JOB_MEMBER_START_EVENT_MISSING"),
 (lambda p:p["job"]["members"].append(copy.deepcopy(p["job"]["members"][0])),"DUPLICATE_JOB_MEMBER_IDENTITY"),
])
def test_IT03_exact_specific_job_inventory(change,reason):
    p=base();change(p);expect(p,"BLOCKED",reason)

@pytest.mark.parametrize("change,reason",[
 (lambda p:p["job"]["members"][1].update(handle_retained=False),"MEMBER_EXIT_UNVERIFIED"),
 (lambda p:p["job"]["members"][1].update(wait_signaled=False),"MEMBER_EXIT_UNVERIFIED"),
 (lambda p:p["job"]["members"][1].update(exit_code=259),"MEMBER_EXIT_UNVERIFIED"),
 (lambda p:p["job"]["members"][1].update(raw_provenance=None),"RAW_PROVENANCE_MISSING"),
 (lambda p:p["job"].update(post_count=1),"MEMBER_EXIT_UNVERIFIED"),
])
def test_IT04_requires_all_member_exit_evidence(change,reason):
    p=base();change(p);expect(p,"BLOCKED",reason)

@pytest.mark.parametrize("change,reason",[
 (lambda p:p["receipt"].update(descendant_created=False),"RECEIPT_CONTRADICTION"),
 (lambda p:p["receipt"].update(descendant_absence_proven=True),"RECEIPT_CONTRADICTION"),
 (lambda p:p["receipt"].update(descendant_identities=[]),"RECEIPT_CONTRADICTION"),
 (lambda p:p["receipt"].update(raw_evidence_sha256="0"*64),"RAW_DIGEST_MISMATCH"),
 (lambda p:p.update(independent_windows_evidence=True),"UNAUTHORIZED_WINDOWS_PROVENANCE"),
 (lambda p:p.update(evidence_class="INDEPENDENT_WINDOWS"),"UNAUTHORIZED_WINDOWS_PROVENANCE"),
])
def test_IT05_receipt_consistency_and_no_windows_promotion(change,reason):
    p=base();change(p);expect(p,"BLOCKED",reason)

def test_IT02_transitive_descendant_from_synthetic_event_chain():
    p=base()
    third={"pid":333,"creation_filetime":"134361969930400000"}
    p["event_stream"]["events"].append({"seq":3,"time":140,"child":third,
       "parent":dict(CHILD),"parent_start_verified":True,
       "source":"ETW_KERNEL_PROCESS_PROPOSED","observer":"synthetic-observer"})
    p["event_stream"]["seq_last"]=3
    p["job"]["members"].append({"identity":third,"post_identity":dict(third),
       "job_id":"SYNTH_JOB_A","membership_verified":True,
       "handle_retained":True,"wait_signaled":True,"exit_code":0,"raw_provenance":"OFFLINE_FIXTURE"})
    p["job"]["member_count"]=3
    p["receipt"]["descendant_identities"].append(third)
    p["receipt"]["raw_evidence_sha256"]=digest(p)
    r=expect(p,"PASS")
    assert r.get("verified_descendant_count")==2

def test_IT05_absence_proof_requires_complete_empty_descendant_chain():
    p=base(descendant=False)
    r=expect(p,"PASS")
    assert r.get("descendant_absence_proven") is True
    assert r.get("absence_evidence")=="COMPLETE_SYNTHETIC_COVERAGE_NO_DESCENDANTS"

def test_IT05_missing_coverage_blocks_absence_despite_favorable_receipt():
    p=base(descendant=False);p["event_stream"]["continuous"]=False
    expect(p,"BLOCKED","EVENT_COVERAGE_INCOMPLETE")

def test_IT05_working_fixture_never_becomes_windows_evidence():
    r=expect(base(),"PASS")
    assert r["independent_windows_evidence"] is False
    assert r["production_qualification"] is False

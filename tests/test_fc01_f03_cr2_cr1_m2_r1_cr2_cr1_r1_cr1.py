"""R1-CR1 test-first evidence gates. Synthetic dictionaries only; no Windows worker launches."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import copy
import pytest

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/member_evidence.py"

def load():
    assert MOD.exists(), "RED_MISSING_ISOLATED_MEMBER_CLASSIFICATION"
    spec=importlib.util.spec_from_file_location("r1cr1_member_evidence",MOD)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def member(pid=500,start=900, parent_pid=400,parent_start=200, role="worker"):
    return {"pid":pid,"start":start,"parent_pid":parent_pid,"parent_start":parent_start,
      "parent_identity_verified":True,"membership_verified":True,
      "exit_wait_zero":True,"exit_code":88,"post_start":start,
      "raw_provenance":"R1_JOB_MEMBER_PRE_AND_POST_OBSERVED",
      "external_lineage_proven":role=="other"}

def fixture():
    return {"worker":{"pid":500,"start":900},
     "supervisor":{"pid":400,"start":200},
     "members_before":[member()],
     "job_member_count_before":1,"job_members_post_count":0,
     "post_query_observed":True,"explicit_child_marker":False,
     "explicit_child_pid":None,"explicit_child_start":None,
     "termination_action":"TERMINATE_JOB"}

def run(obs):
    return load().classify_and_validate_members(obs)

def assert_pass(obs):
    v=run(obs);assert v["status"]=="PASS",v
    assert v["unclassified_count"]==0
    return v

def assert_blocked(obs,reason):
    v=run(obs);assert v["status"]=="BLOCKED",v
    assert reason in v["violations"],v

def test_JM01_single_primary_worker():
    v=assert_pass(fixture())
    assert v["classifications"]=={"500":"PRIMARY_WORKER"}
    assert v["descendant_absence_proven"] is True

def test_JM02_two_members_parent_bound_descendant():
    x=fixture()
    x["members_before"].append(member(600,910,500,900,"child"))
    x["job_member_count_before"]=2
    v=assert_pass(x)
    assert v["classifications"]["600"]=="VERIFIED_DESCENDANT"
    assert v["descendant_absence_proven"] is False

def test_JM03_unknown_second_member_blocks():
    x=fixture();n=member(600,910,888,111)
    n["parent_identity_verified"]=False
    x["members_before"].append(n);x["job_member_count_before"]=2
    assert_blocked(x,"UNCLASSIFIED_JOB_MEMBER")

def test_JM04_invalid_member_creation_identity_blocks():
    x=fixture();x["members_before"][0]["start"]=0
    assert_blocked(x,"MEMBER_IDENTITY_INVALID")

def test_JM05_PID_reuse_different_post_identity_blocks():
    x=fixture();x["members_before"][0]["post_start"]=901
    assert_blocked(x,"MEMBER_START_IDENTITY_MISMATCH")

def test_JM06_absence_claim_contradicted_by_child_blocks():
    x=fixture()
    x["members_before"].append(member(600,910,500,900))
    x["job_member_count_before"]=2;x["claimed_descendant_absent"]=True
    assert_blocked(x,"CONTRADICTORY_DESCENDANT_ABSENCE")

def test_JM07_member_active_after_termination_blocks():
    x=fixture();x["members_before"][0]["exit_wait_zero"]=False
    x["job_members_post_count"]=1
    assert_blocked(x,"MEMBER_TERMINATION_NOT_VERIFIED")

def test_JM08_inconsistent_job_member_count_blocks():
    x=fixture();x["job_member_count_before"]=2
    assert_blocked(x,"JOB_MEMBER_COUNT_MISMATCH")

def test_JM09_independently_observed_single_member_absence():
    v=assert_pass(fixture())
    assert v["absence_evidence"]=="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"

def test_JM10_all_identified_descendants_terminated():
    x=fixture();x["members_before"].append(member(600,910,500,900))
    x["job_member_count_before"]=2
    v=assert_pass(x)
    assert v["all_member_exits_verified"] is True

def test_JM11_missing_raw_source_provenance_blocks():
    x=fixture();x["members_before"][0]["raw_provenance"]=None
    assert_blocked(x,"MEMBER_RAW_PROVENANCE_MISSING")

def test_JM12_other_member_requires_independent_parent_lineage():
    x=fixture();x["members_before"].append(member(700,910,300,100,"other"))
    x["job_member_count_before"]=2
    v=assert_pass(x)
    assert v["classifications"]["700"]=="OTHER_IDENTIFIED_JOB_MEMBER"
    assert v["descendant_absence_proven"] is True
    # No mere other-parent assertion without independent lineage evidence
    y=copy.deepcopy(x);y["members_before"][1]["external_lineage_proven"]=False
    assert_blocked(y,"UNCLASSIFIED_JOB_MEMBER")

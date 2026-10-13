"""Isolated GREEN-R1 test-first contract. No Windows worker, Java, or networking.

RED phase: set ATDS_GREEN_R1_PHASE=legacy; compare to frozen historical adapter.
GREEN phase: default, explicitly import the isolated GREEN validator.
No historical test or receipt is modified.
"""
from __future__ import annotations
import copy
import importlib.util
import os
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
ORACLE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_oracle.py"
CANDIDATE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/green_r1/validator.py"
assert ORACLE.exists(), "MISSING_FROZEN_ORACLE"

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def call(case,change=None):
    old=load(ORACLE,"green_r1_frozen_oracle")
    evidence=old.case(case)
    if change:change(evidence)
    if os.environ.get("ATDS_GREEN_R1_PHASE")=="legacy":
        target=old.historical()
    else:
        target=load(CANDIDATE,"green_r1_isolated_candidate")
    return evidence,target.classify_and_validate_members(copy.deepcopy(evidence))

def status(case,expected,change=None,reason=None):
    evidence,result=call(case,change)
    assert result["status"]==expected,(case,result)
    if reason is not None:
        assert reason in result["violations"],(case,result)
    return evidence,result

def test_JM01_valid_single_primary_worker():
    _,r=status("JM01","PASS")
    assert r["classifications"]=={"500":"PRIMARY_WORKER"}
    assert r["descendant_absence_proven"] is True
    assert r["absence_evidence"]=="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"

def test_JM02_verified_synthetic_descendant():
    _,r=status("JM02","PASS")
    assert r["classifications"]["600"]=="VERIFIED_DESCENDANT"
    assert r["descendant_absence_proven"] is False

def test_JM03_unknown_member_reason():
    _,r=status("JM03","BLOCKED",reason="UNCLASSIFIED_JOB_MEMBER")
    assert r["unclassified_count"]==1
    assert r["descendant_absence_proven"] is False

def test_JM04_invalid_creation_identity_cannot_imply_absence():
    _,r=status("JM04","BLOCKED",reason="MEMBER_IDENTITY_INVALID")
    assert r["descendant_absence_proven"] is False

def test_JM05_post_start_must_match_pre_start():
    status("JM05","BLOCKED",reason="MEMBER_START_IDENTITY_MISMATCH")

def test_JM06_declared_absence_contradicts_verified_synthetic_descendant():
    status("JM06","BLOCKED",reason="CONTRADICTORY_DESCENDANT_ABSENCE")

def test_JM07_member_exit_must_be_verified():
    _,r=status("JM07","BLOCKED",reason="MEMBER_TERMINATION_NOT_VERIFIED")
    assert r["all_member_exits_verified"] is False

def test_JM08_count_must_match_inventory():
    status("JM08","BLOCKED",reason="JOB_MEMBER_COUNT_MISMATCH")

def test_JM09_absence_requires_complete_classification_and_provenance():
    _,r=status("JM09","PASS")
    assert r["absence_evidence"]=="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"
    assert r["evidence_class"]=="SYNTHETIC_CONTRACT"
    assert r["independent_windows_evidence"] is False
    assert r["production_qualification"] is False

def test_JM10_all_descendant_exits_verified():
    _,r=status("JM10","PASS")
    assert r["all_member_exits_verified"] is True
    assert r["classifications"]["600"]=="VERIFIED_DESCENDANT"

def test_JM11_member_raw_provenance_required():
    status("JM11","BLOCKED",reason="MEMBER_RAW_PROVENANCE_MISSING")

def test_JM12_other_verified_job_member_and_unverified_variant():
    _,r=status("JM12","PASS")
    assert r["classifications"]["700"]=="OTHER_IDENTIFIED_JOB_MEMBER"
    assert r["descendant_absence_proven"] is True
    status("JM12","BLOCKED",lambda x:x["members_before"][1].update(external_lineage_proven=False),
           "UNCLASSIFIED_JOB_MEMBER")

def mutate_member(name,value):
    return lambda x:x["members_before"][0].__setitem__(name,value)

def add_extra_member(x):
    x["members_before"].append(copy.deepcopy(x["members_before"][0]))
    x["job_member_count_before"]=2

@pytest.mark.parametrize("case,change,reason",[
 ("JM01",mutate_member("pid",True),"MEMBER_IDENTITY_INVALID"),
 ("JM01",mutate_member("start",None),"MEMBER_IDENTITY_INVALID"),
 ("JM01",mutate_member("post_start",None),"MEMBER_START_IDENTITY_MISMATCH"),
 ("JM01",mutate_member("post_start",901),"MEMBER_START_IDENTITY_MISMATCH"),
 ("JM01",mutate_member("membership_verified",False),"MEMBER_JOB_MEMBERSHIP_UNVERIFIED"),
 ("JM01",mutate_member("raw_provenance","FAKE"),"MEMBER_RAW_PROVENANCE_INVALID"),
 ("JM01",mutate_member("parent_identity_verified",False),"UNCLASSIFIED_JOB_MEMBER"),
 ("JM01",mutate_member("parent_start",201),"UNCLASSIFIED_JOB_MEMBER"),
 ("JM01",mutate_member("exit_wait_zero",False),"MEMBER_TERMINATION_NOT_VERIFIED"),
 ("JM01",mutate_member("exit_code",259),"MEMBER_TERMINATION_NOT_VERIFIED"),
 ("JM01",mutate_member("exit_code","88"),"MEMBER_TERMINATION_NOT_VERIFIED"),
 ("JM01",lambda x:x.__setitem__("job_members_post_count",1),"MEMBER_TERMINATION_NOT_VERIFIED"),
 ("JM01",lambda x:x.__setitem__("post_query_observed",False),"JOB_POST_QUERY_NOT_VERIFIED"),
 ("JM01",lambda x:x.__setitem__("termination_action","UNKNOWN"),"TERMINATION_ACTION_MISSING"),
 ("JM01",lambda x:x.__setitem__("global_status","BLOCKED"),"CONTRADICTORY_GLOBAL_STATUS"),
 ("JM01",lambda x:x.__setitem__("evidence_class","INDEPENDENT_WINDOWS"),"UNAUTHORIZED_EVIDENCE_CLASS"),
 ("JM01",lambda x:x.__setitem__("descendant_absence_proven",False),"CONTRADICTORY_DESCENDANT_ABSENCE_PROOF"),
 ("JM01",lambda x:x.__setitem__("descendant_created",True),"CONTRADICTORY_DESCENDANT_CREATED"),
 ("JM01",lambda x:x.__setitem__("descendant_identities",[{"pid":900,"start":1000}]),"DESCENDANT_IDENTITY_MISMATCH"),
 ("JM01",lambda x:x.__setitem__("explicit_child_marker",True),"DESCENDANT_MARKER_UNVERIFIED"),
 ("JM01",add_extra_member,"DUPLICATE_JOB_MEMBER_IDENTITY"),
 ("JM01",lambda x:x.__setitem__("job_member_count_before",True),"JOB_MEMBER_COUNT_MISMATCH"),
 ("JM02",lambda x:x.__setitem__("descendant_created",False),"CONTRADICTORY_DESCENDANT_CREATED"),
 ("JM02",lambda x:x.__setitem__("descendant_identities",[]),"DESCENDANT_IDENTITY_MISMATCH"),
 ("JM02",lambda x:x["members_before"][1].update(parent_identity_verified=False),"UNCLASSIFIED_JOB_MEMBER"),
 ("JM02",lambda x:x["members_before"][1].update(parent_start=901),"UNCLASSIFIED_JOB_MEMBER"),
 ("JM02",lambda x:x["members_before"][1].update(raw_provenance=None),"MEMBER_RAW_PROVENANCE_MISSING"),
 ("JM12",lambda x:x["members_before"][1].update(parent_identity_verified=False),"UNCLASSIFIED_JOB_MEMBER"),
 ("JM12",lambda x:x["members_before"][1].update(external_lineage_proven="True"),"UNCLASSIFIED_JOB_MEMBER"),
])
def test_ADV_FAIL_CLOSED(case,change,reason):
    _,r=status(case,"BLOCKED",change=change,reason=reason)
    assert r["descendant_absence_proven"] is False

def test_ADV_verified_synthetic_lineage_not_windows_proof():
    _,r=status("JM02","PASS")
    assert r["evidence_class"]=="SYNTHETIC_CONTRACT"
    assert r["independent_windows_evidence"] is False
    assert r["production_qualification"] is False

def test_ADV_unverified_reparenting_never_favorable():
    _,r=status("JM12","BLOCKED",lambda x:x["members_before"][1].update(parent_pid=500,parent_start=901,external_lineage_proven=False),
               "UNCLASSIFIED_JOB_MEMBER")
    assert r["descendant_absence_proven"] is False

def test_ADV_cross_field_proof_does_not_mask_invalid_member():
    _,r=status("JM04","BLOCKED",reason="MEMBER_IDENTITY_INVALID")
    assert r["absence_evidence"]!="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"
    assert r["descendant_absence_proven"] is False

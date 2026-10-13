"""Independent GREEN-R1 adversarial cross-field and descendant lineage tests.
A separate P3 synthetic test surface, without Windows workers or production code.
"""
import importlib.util
from pathlib import Path
import copy

ROOT=Path(__file__).resolve().parents[1]
ORACLE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_oracle.py"
GREEN=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/green_r1/validator.py"
def load(p):
    s=importlib.util.spec_from_file_location("independent_"+p.stem,p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m
def call(case="JM01",mod=None):
    o=load(ORACLE);x=o.case(case)
    if mod:mod(x)
    return load(GREEN).classify_and_validate_members(copy.deepcopy(x))
def blocked(r,reason):
    assert r["status"]=="BLOCKED",r
    assert reason in r["violations"],r
    assert r["descendant_absence_proven"] is False
    assert r["independent_windows_evidence"] is False
    assert r["production_qualification"] is False

def test_A01_post_creation_mismatch_invalidates_individual_exit_proof():
    r=call(mod=lambda x:x["members_before"][0].update(post_start=901))
    blocked(r,"MEMBER_START_IDENTITY_MISMATCH")
    assert r["all_member_exits_verified"] is False

def test_A02_invalid_member_creation_prevents_favorable_exit_proof():
    r=call(mod=lambda x:x["members_before"][0].update(start=0))
    blocked(r,"MEMBER_IDENTITY_INVALID")
    assert r["all_member_exits_verified"] is False

def test_A03_missing_raw_provenance_is_not_complete_individual_exit_proof():
    r=call(mod=lambda x:x["members_before"][0].update(raw_provenance=None))
    blocked(r,"MEMBER_RAW_PROVENANCE_MISSING")
    assert r["all_member_exits_verified"] is False

def test_A04_duplicate_identical_identity_is_not_complete_member_inventory():
    def change(x):
        x["members_before"].append(copy.deepcopy(x["members_before"][0]))
        x["job_member_count_before"]=2
    r=call(mod=change)
    blocked(r,"DUPLICATE_JOB_MEMBER_IDENTITY")
    assert r["all_member_exits_verified"] is False

def test_A05_unobserved_worker_list_is_blocking():
    r=call(mod=lambda x:(x.__setitem__("members_before",[]),x.__setitem__("job_member_count_before",0)))
    blocked(r,"PRE_TERMINATION_JOB_MEMBERS_UNKNOWN")

def test_A06_non_boolean_explicit_child_marker_is_blocking():
    r=call(mod=lambda x:x.__setitem__("explicit_child_marker","TRUE"))
    blocked(r,"DESCENDANT_MARKER_UNVERIFIED")

def test_A07_non_boolean_absence_claim_is_blocking():
    r=call(mod=lambda x:x.__setitem__("claimed_descendant_absent","TRUE"))
    blocked(r,"CONTRADICTORY_DESCENDANT_ABSENCE")

def test_A08_positive_descendant_and_false_created_assertion_conflict():
    r=call("JM02",lambda x:x.__setitem__("descendant_created",False))
    blocked(r,"CONTRADICTORY_DESCENDANT_CREATED")

def test_A09_other_member_cannot_hide_mismatched_worker_parent_start():
    def change(x):
        n=x["members_before"][1]
        n.update(parent_pid=500,parent_start=901,parent_identity_verified=True,external_lineage_proven=True)
    r=call("JM12",change)
    blocked(r,"UNCLASSIFIED_JOB_MEMBER")

def test_A10_transitive_descendant_with_bound_parent_identity_is_classified():
    def change(x):
        x["members_before"].append(load(ORACLE).member(650,930,600,910,"child"))
        x["job_member_count_before"]=3
    r=call("JM02",change)
    assert r["status"]=="PASS",r
    assert r["classifications"]["650"]=="VERIFIED_DESCENDANT"
    assert r["verified_descendant_count"]==2
    assert r["descendant_absence_proven"] is False

def test_A11_provenance_tags_never_promote_synthetic_to_windows():
    r=call("JM02")
    assert r["status"]=="PASS",r
    assert r["evidence_class"]=="SYNTHETIC_CONTRACT"
    assert r["independent_windows_evidence"] is False
    assert r["production_qualification"] is False

def test_A12_inconsistent_global_pass_claim_cannot_override_real_blocker():
    r=call("JM07",lambda x:x.__setitem__("global_status","PASS"))
    blocked(r,"CONTRADICTORY_GLOBAL_STATUS")

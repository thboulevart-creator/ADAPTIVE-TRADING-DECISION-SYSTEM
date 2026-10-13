"""R1-CR1-RED-R1-CR2: frozen, synthetic-only RED oracle evidence.

Test oracle / fixture construction only: NOT a GREEN runtime implementation,
NOT Job Object instrumentation, and never evidence of observed Windows
parent-child relationships. No subprocess, sockets, provider, or file mutation.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEGACY_PATH = ROOT / "tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/member_evidence.py"
ORIGINAL_TEST = ROOT / "tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1.py"
LEGACY_SHA256 = "6260021b5e1259677413c341587de92d71168e96ce2d2abc5b51446434fa2c85"
ORIGINAL_TEST_SHA256 = "65cb60153e6a7458adce0373ad51d95e84c3c4fb84ca19e2843dceb8a8944282"
EVIDENCE_CLASS = "LEGACY_ADAPTER"
INPUT_CLASS = "SYNTHETIC_CONTRACT"
WINDOWS_EVIDENCE = False

def verify_frozen_sources():
    sha = lambda x: hashlib.sha256(x.read_bytes()).hexdigest()
    if sha(LEGACY_PATH) != LEGACY_SHA256 or sha(ORIGINAL_TEST) != ORIGINAL_TEST_SHA256:
        raise RuntimeError("CR2_FROZEN_HISTORICAL_SOURCE_DRIFT")
    return {"historical_adapter_sha256": LEGACY_SHA256,
            "original_test_sha256": ORIGINAL_TEST_SHA256}

def historical():
    verify_frozen_sources()
    spec = importlib.util.spec_from_file_location("cr2_frozen_r1_red_adapter", LEGACY_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if mod.OBSERVED_WINDOWS_EVIDENCE is not False:
        raise RuntimeError("FORBIDDEN_WINDOWS_EVIDENCE_PROMOTION")
    return mod

def member(pid=500, start=900, parent_pid=400, parent_start=200, role="worker"):
    return {"pid":pid, "start":start, "parent_pid":parent_pid,
            "parent_start":parent_start, "parent_identity_verified":True,
            "membership_verified":True, "exit_wait_zero":True, "exit_code":88,
            "post_start":start, "raw_provenance":"R1_JOB_MEMBER_PRE_AND_POST_OBSERVED",
            "external_lineage_proven": role == "other"}

def good():
    return {"worker":{"pid":500,"start":900},
            "supervisor":{"pid":400,"start":200},
            "members_before":[member()],
            "job_member_count_before":1,
            "job_members_post_count":0,
            "post_query_observed":True,
            "explicit_child_marker":False,
            "explicit_child_pid":None,
            "explicit_child_start":None,
            "termination_action":"TERMINATE_JOB"}

def case(case_id):
    """Exactly one case constructor per immutable JM requirement."""
    x=good()
    if case_id in ("JM02","JM06","JM10"):
        x["members_before"].append(member(600,910,500,900,"child"))
        x["job_member_count_before"]=2
        if case_id=="JM06":x["claimed_descendant_absent"]=True
    elif case_id=="JM03":
        x["members_before"].append(member(600,910,888,111))
        x["members_before"][1]["parent_identity_verified"]=False
        x["job_member_count_before"]=2
    elif case_id=="JM04":
        x["members_before"][0]["start"]=0
    elif case_id=="JM05":
        x["members_before"][0]["post_start"]=901
    elif case_id=="JM07":
        x["members_before"][0]["exit_wait_zero"]=False
        x["job_members_post_count"]=1
    elif case_id=="JM08":
        x["job_member_count_before"]=2
    elif case_id=="JM11":
        x["members_before"][0]["raw_provenance"]=None
    elif case_id=="JM12":
        x["members_before"].append(member(700,910,300,100,"other"))
        x["job_member_count_before"]=2
    elif case_id not in ("JM01","JM09"):
        raise ValueError("UNKNOWN_FROZEN_CASE:"+case_id)
    return x

def observe(case_id, change=None):
    x=case(case_id)
    if change is not None:change(x)
    return historical().classify_and_validate_members(copy.deepcopy(x))

# This table defines oracle interpretation, never implementation/green status.
MATRIX = {
 "JM01":{"expected_old_status":"PASS","kind":"EXISTING_POSITIVE_CONTROL","gap":"NONE"},
 "JM02":{"expected_old_status":"BLOCKED","kind":"SYNTHETIC_FALSE_BLOCK","gap":"NO_INDEPENDENT_DESCENDANT_CLASSIFICATION"},
 "JM03":{"expected_old_status":"BLOCKED","kind":"REASON_SPECIFICITY","gap":"UNCLASSIFIED_JOB_MEMBER_NOT_REPORTED"},
 "JM04":{"expected_old_status":"BLOCKED","kind":"CROSS_FIELD_CONSISTENCY","gap":"INVALID_IDENTITY_WITH_FAVORABLE_ABSENCE"},
 "JM05":{"expected_old_status":"PASS","kind":"INPUT_TRANSPORT_OMISSION","gap":"POST_START_IDENTITY_IGNORED"},
 "JM06":{"expected_old_status":"BLOCKED","kind":"REASON_AND_TRANSPORT","gap":"CLAIMED_ABSENCE_NOT_BOUND_TO_PROVEN_LINEAGE"},
 "JM07":{"expected_old_status":"BLOCKED","kind":"REASON_SPECIFICITY","gap":"NORMALIZED_TERMINATION_REASON_MISSING"},
 "JM08":{"expected_old_status":"PASS","kind":"INPUT_TRANSPORT_OMISSION","gap":"JOB_MEMBER_COUNT_IGNORED"},
 "JM09":{"expected_old_status":"PASS","kind":"ABSENCE_PROOF_SEMANTICS","gap":"ENUMERATED_EMPTY_ONLY"},
 "JM10":{"expected_old_status":"BLOCKED","kind":"SYNTHETIC_FALSE_BLOCK","gap":"TERMINATED_DESCENDANT_UNCLASSIFIED"},
 "JM11":{"expected_old_status":"PASS","kind":"INPUT_TRANSPORT_OMISSION","gap":"RAW_PROVENANCE_IGNORED"},
 "JM12":{"expected_old_status":"BLOCKED","kind":"SYNTHETIC_FALSE_BLOCK","gap":"EXTERNAL_LINEAGE_NOT_CLASSIFIED"},
}

def matrix_observations():
    verify_frozen_sources()
    result=[]
    for key,rule in MATRIX.items():
        v=observe(key)
        if v["status"] != rule["expected_old_status"]:
            raise AssertionError("DRIFTED_BASELINE:"+key)
        result.append({"test_id":key,"expected_legacy_status":rule["expected_old_status"],
                       "observed_legacy_status":v["status"],"evidence_class":EVIDENCE_CLASS,
                       "input_class":INPUT_CLASS,"independent_windows_evidence":False,
                       "gap_class":rule["kind"],"gap_id":rule["gap"],
                       "observed_violations":v["violations"],
                       "observed_classifications":v["classifications"],
                       "observed_descendant_absence_proven":v["descendant_absence_proven"],
                       "observed_absence_evidence":v["absence_evidence"]})
    return result

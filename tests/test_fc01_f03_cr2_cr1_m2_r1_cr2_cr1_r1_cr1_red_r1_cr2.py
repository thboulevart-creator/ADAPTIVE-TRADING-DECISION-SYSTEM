"""RED-R1-CR2: 12 *legacy gap capture* tests; passing means RED demonstrated.

These tests DO NOT demand a GREEN implementation or attest to Windows behavior.
Frozen CR1 tests/receipts remain unchanged. No worker/network subprocess.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/red_r1_cr2_oracle.py"

def module():
    if not FILE.is_file():
        raise AssertionError("MISSING_NEW_CR2_ORACLE")
    spec=importlib.util.spec_from_file_location("r1_cr1_red_r1_cr2_oracle",FILE)
    oracle=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    assert oracle.WINDOWS_EVIDENCE is False
    assert oracle.EVIDENCE_CLASS == "LEGACY_ADAPTER"
    assert oracle.INPUT_CLASS == "SYNTHETIC_CONTRACT"
    assert len(oracle.MATRIX)==12
    oracle.verify_frozen_sources()
    return oracle

def observed(case_id, expected_status):
    o=module()
    record=o.observe(case_id)
    assert record["status"]==expected_status,(case_id,record)
    assert o.MATRIX[case_id]["expected_old_status"]==expected_status
    assert record["status"] in ("PASS","BLOCKED")
    return o,record

def test_JM01_positive_worker_control_remains_pass():
    o,v=observed("JM01","PASS")
    assert v["classifications"]=={"500":"PRIMARY_WORKER"}
    assert v["unclassified_count"]==0
    assert v["descendant_absence_proven"] is True

def test_JM02_verified_synthetic_descendant_is_legacy_false_block():
    o,v=observed("JM02","BLOCKED")
    fixture=o.case("JM02")
    assert fixture["members_before"][1]["parent_pid"]==fixture["worker"]["pid"]
    assert fixture["members_before"][1]["parent_start"]==fixture["worker"]["start"]
    assert fixture["members_before"][1]["parent_identity_verified"] is True
    assert v["classifications"]["600"]=="UNCLASSIFIED_MEMBER"
    assert "DESCENDANT_ABSENCE_UNPROVEN" in v["violations"]

def test_JM03_unclassified_member_reason_specificity_red():
    _,v=observed("JM03","BLOCKED")
    assert v["classifications"]["600"]=="UNCLASSIFIED_MEMBER"
    assert "DESCENDANT_ABSENCE_UNPROVEN" in v["violations"]
    assert "UNCLASSIFIED_JOB_MEMBER" not in v["violations"]
    assert v["descendant_absence_proven"] is False

def test_JM04_invalid_identity_and_favorable_absence_contradict():
    _,v=observed("JM04","BLOCKED")
    assert "JOB_MEMBER_EXIT_IDENTITY_INCOMPLETE" in v["violations"]
    assert "MEMBER_IDENTITY_INVALID" not in v["violations"]
    assert v["descendant_absence_proven"] is True  # invalid favorable cross-field legacy defect
    assert v["classifications"]["500"]=="UNCLASSIFIED_MEMBER"

def test_JM05_post_creation_identity_mismatch_is_not_forwarded():
    o,v=observed("JM05","PASS")
    assert o.case("JM05")["members_before"][0]["post_start"]==901
    prior=o.observe("JM01")
    assert prior==v  # data dropped at the historical synthetic adapter boundary

def test_JM06_confirmed_synthetic_child_absence_claim_is_ignored():
    o,v=observed("JM06","BLOCKED")
    x=o.case("JM06")
    assert x["members_before"][1]["parent_identity_verified"] is True
    assert x["claimed_descendant_absent"] is True
    assert "CONTRADICTORY_DESCENDANT_ABSENCE" not in v["violations"]
    without_claim=o.observe("JM06",lambda d:d.pop("claimed_descendant_absent"))
    assert without_claim==v # claim transport absent; cannot prove real Windows parentage

def test_JM07_termination_block_exists_but_normalized_reason_missing():
    _,v=observed("JM07","BLOCKED")
    assert "JOB_MEMBERS_STILL_ACTIVE_OR_UNKNOWN" in v["violations"]
    assert "WORKER_EXIT_NOT_VERIFIED" in v["violations"]
    assert "MEMBER_TERMINATION_NOT_VERIFIED" not in v["violations"]
    assert v["all_member_exits_verified"] is False

def test_JM08_job_member_count_mismatch_is_not_forwarded():
    o,v=observed("JM08","PASS")
    assert o.case("JM08")["job_member_count_before"]==2
    assert len(o.case("JM08")["members_before"])==1
    assert v==o.observe("JM01")

def test_JM09_enumerated_empty_does_not_demonstrate_full_provenance():
    o,v=observed("JM09","PASS")
    assert v["absence_evidence"]=="ENUMERATED_EMPTY"
    assert v["absence_evidence"]!="ENUMERATED_MEMBERS_ALL_CLASSIFIED_NO_DESCENDANTS"
    lost_provenance=o.observe("JM09",lambda x:x["members_before"][0].update(raw_provenance=None))
    assert lost_provenance==v

def test_JM10_all_exited_but_synthetic_child_remains_unclassified():
    _,v=observed("JM10","BLOCKED")
    assert v["all_member_exits_verified"] is True
    assert v["classifications"]["600"]=="UNCLASSIFIED_MEMBER"
    assert v["descendant_absence_proven"] is False

def test_JM11_raw_provenance_absence_is_not_forwarded():
    o,v=observed("JM11","PASS")
    assert o.case("JM11")["members_before"][0]["raw_provenance"] is None
    assert v==o.observe("JM01")

def test_JM12_independently_declared_external_lineage_does_not_classify():
    o,v=observed("JM12","BLOCKED")
    n=o.case("JM12")["members_before"][1]
    assert n["external_lineage_proven"] is True
    assert n["parent_pid"]!=o.case("JM12")["worker"]["pid"]
    assert v["classifications"]["700"]=="UNCLASSIFIED_MEMBER"
    without_lineage=o.observe("JM12",lambda x:x["members_before"][1].update(external_lineage_proven=False))
    assert without_lineage==v  # strictly synthetic fixture, not Windows independent evidence

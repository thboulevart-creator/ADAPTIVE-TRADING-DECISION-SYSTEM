"""WER-02 separate adversarial re-break of *synthetic* proof candidate.

These are not observations of real Windows ETW or Jobs. No subprocess spawned.
"""
from pathlib import Path
import copy
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/"tests/test_fc01_f03_cr2_cr1_m2_r1_cr2_cr1_r1_cr1_wer_02_contract.py"
CANDIDATE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2_cr1_r1_cr1/wer_02/candidate.py"
def load(p):
    s=importlib.util.spec_from_file_location("wer02_adv_"+p.stem,p)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m
o=load(ORIGINAL)
c=load(CANDIDATE)

def check(p,violation):
    p["receipt"]["raw_evidence_sha256"]=o.digest(p)
    r=c.evaluate(copy.deepcopy(p))
    assert r["status"]=="BLOCKED",r
    assert violation in r["violations"],r
    assert r["independent_windows_evidence"] is False
    return r

def test_AD01_extra_unaccounted_start_event_must_block():
    p=o.base()
    p["event_stream"]["events"].append({"seq":3,"time":140,
        "child":{"pid":444,"creation_filetime":"134361969930500000"},
        "parent":dict(o.SUPERVISOR),"parent_start_verified":True,
        "source":"ETW_KERNEL_PROCESS_PROPOSED","observer":"synthetic-observer"})
    p["event_stream"]["seq_last"]=3
    check(p,"UNACCOUNTED_PROCESS_START_EVENT")

def test_AD02_recycled_PID_across_start_event_stream_must_block():
    p=o.base()
    p["event_stream"]["events"].append({"seq":3,"time":141,
        "child":{"pid":222,"creation_filetime":"134361969930500000"},
        "parent":dict(o.WORKER),"parent_start_verified":True,
        "source":"ETW_KERNEL_PROCESS_PROPOSED","observer":"synthetic-observer"})
    p["event_stream"]["seq_last"]=3
    check(p,"PID_REUSE_OR_IDENTITY_MISMATCH")

def test_AD03_claimed_global_PASS_cannot_hide_negative_member_evidence():
    p=o.base()
    p["job"]["members"][1]["raw_provenance"]=None
    check(p,"RECEIPT_CONTRADICTION")

def test_AD04_event_timestamp_out_of_order_must_fail_closed():
    p=o.base()
    p["event_stream"]["events"][0]["time"]=140
    p["event_stream"]["events"][1]["time"]=120
    check(p,"EVENT_CAUSAL_ORDER_INVALID")

def test_AD05_extra_nested_windows_provenance_claim_rejected():
    p=o.base()
    p["receipt"]["evidence_class"]="INDEPENDENT_WINDOWS"
    check(p,"UNAUTHORIZED_WINDOWS_PROVENANCE")

def test_AD06_missing_primary_worker_event_blocks():
    p=o.base()
    p["event_stream"]["events"]=p["event_stream"]["events"][1:]
    p["event_stream"]["seq_first"]=2
    check(p,"JOB_MEMBER_START_EVENT_MISSING")

def test_AD07_a_good_synthetic_fixture_remains_green():
    p=o.base()
    r=c.evaluate(p)
    assert r["status"]=="PASS",r
    assert r["production_qualification"] is False

def test_AD08_mixed_integer_and_string_exact_filetime_canonicalized():
    p=o.base()
    p["worker"]["creation_filetime"]=134361969930150189
    p["job"]["members"][0]["post_identity"]["creation_filetime"]=134361969930150189
    p["job"]["members"][0]["identity"]["creation_filetime"]=134361969930150189
    p["event_stream"]["events"][0]["child"]["creation_filetime"]=134361969930150189
    p["event_stream"]["events"][1]["parent"]["creation_filetime"]=134361969930150189
    p["receipt"]["raw_evidence_sha256"]=o.digest(p)
    r=c.evaluate(p)
    assert r["status"]=="PASS",r

def test_AD09_scientific_notation_filetime_rejected():
    p=o.base()
    p["event_stream"]["events"][0]["child"]["creation_filetime"]="1.34361969930150189e17"
    check(p,"INVALID_PROCESS_IDENTITY")

def test_AD10_exit_observation_unavailable_requires_blocking():
    p=o.base()
    p["job"]["members"][0]["wait_signaled"]=None
    check(p,"MEMBER_EXIT_UNVERIFIED")

def test_AD11_windows_kind_at_event_stream_boundary_forbidden():
    p=o.base()
    p["event_stream"]["evidence_class"]="INDEPENDENT_WINDOWS"
    check(p,"UNAUTHORIZED_WINDOWS_PROVENANCE")

def test_AD12_missing_process_creation_correlator_not_accepted():
    p=o.base()
    p["event_stream"]["events"][1]["parent_start_verified"]="TRUE"
    check(p,"PARENT_IDENTITY_UNVERIFIED")

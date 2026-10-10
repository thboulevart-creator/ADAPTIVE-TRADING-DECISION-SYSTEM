"""M2-R1-CR1 preregistered RED/GREEN evidence-contract tests. No worker launches."""
import hashlib
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
CAPTURE=ROOT/"tools/fc01_f03_cr2/m2_r1_cr1/receipt_capture.py"
FREEZE=ROOT/"GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR1-PREEXECUTION-FREEZE-V0.1.json"
SCENARIOS=(
    "RC-01","RC-02","RC-03","RC-04","RC-05","RC-06",
    "RC-07","RC-08","RC-09","RC-10","RC-11","RC-12",
)

@pytest.fixture(scope="module")
def frozen():
    obj=json.loads(FREEZE.read_text(encoding="utf-8"))
    assert obj["max_worker_launches"]==24
    assert obj["planned_worker_launches"]==13
    assert len(obj["scenario_runs"])==13
    assert obj["allowed_additional_launches"]==0
    return obj

@pytest.fixture(scope="module")
def implementation(frozen):
    if not CAPTURE.exists():
        return None
    spec=importlib.util.spec_from_file_location("m2r1_cr1_capture",CAPTURE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def good():
    return {
        "campaign_id":"M2R1CR1_20261010_CAP01",
        "run_id":"normal_A","scenario_id":"valid",
        "source_sha256":"a"*64,"binary_sha256":"b"*64,
        "supervisor_pid":123,"supervisor_start_filetime_utc":133801000000000000,
        "worker_pid":456,"worker_start_filetime_utc":133801000000000001,
        "job_limit_bytes":268435456,"job_assigned_before_resume":True,
        "job_current_bytes":12000000,"job_peak_bytes":13000000,
        "stdout_sha256":hashlib.sha256(b"RESULT=PUBLISHED\n").hexdigest(),
        "stderr_sha256":hashlib.sha256(b"").hexdigest(),
        "supervisor_exit_code":0,"worker_exit_code":0,
        "termination_confirmed":True,"tree_terminated":True,
        "child_identities":[],"publication_attempted":True,
        "final_present":True,"final_sha256":"c"*64,
        "recovery_action":"NOT_REQUIRED","recovery_result":"NOT_REQUIRED",
        "memory_failure_signal":"NONE","win32_last_error":"NOT_OBSERVED",
        "start_timestamp_utc":"2026-10-10T16:00:00Z",
        "end_timestamp_utc":"2026-10-10T16:00:01Z",
        "receipt_stage":"FINAL","capture_precreated":True,
        "original_stdout_persisted_during_process":True,
        "original_stderr_persisted_during_process":True,
        "evidence_mode":"DIRECT_IN_PROCESS",
    }

MUTATIONS={
 "RC-01":("stdout_sha256",None),
 "RC-02":("stderr_sha256",None),
 "RC-03":("worker_pid",None),
 "RC-04":("worker_start_filetime_utc",0),
 "RC-05":("job_current_bytes",None),
 "RC-06":("termination_confirmed",None),
 "RC-07":("tree_terminated",None),
 "RC-08":("memory_failure_signal","NOT_OBSERVED"),
 "RC-09":("stdout_sha256","0"*64),
 "RC-10":("receipt_stage","CAPTURE_ABORTED"),
 "RC-11":("capture_precreated",False),
 "RC-12":("evidence_mode","RETROSPECTIVE_INFERRED"),
}

@pytest.mark.parametrize("case",SCENARIOS)
def test_rc_fail_closed_and_genuine_capture_contract(implementation,frozen,case):
    assert implementation is not None, "RED: isolated receipt-capture owner missing"
    obj=good()
    if case=="RC-08":
        obj["supervisor_exit_code"]=22
        obj["worker_exit_code"]="NOT_OBSERVED"
        obj["termination_confirmed"]=True
        obj["final_present"]=False
    field,value=MUTATIONS[case]
    obj[field]=value
    output=implementation.validate(obj,b"RESULT=PUBLISHED\n",b"")
    assert output["status"]=="BLOCKED",(case,output)
    assert output["violations"],case

def test_rc_valid_control(implementation,frozen):
    assert implementation is not None,"RED: capture owner missing"
    assert implementation.validate(good(),b"RESULT=PUBLISHED\n",b"")["status"]=="PASS"

def test_rc_frozen_modes_do_not_authorize_live_provider(implementation,frozen):
    assert implementation is not None,"RED: candidate absent"
    src=CAPTURE.read_text(encoding="utf-8")
    assert "ClientFactory" not in src and "sendOrder" not in src and "MetaTrader" not in src
    assert frozen["scope"]["provider_requests"]==0

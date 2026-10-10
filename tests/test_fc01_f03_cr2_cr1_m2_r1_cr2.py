"""CR2 test-first contract: conditional final SHA, direct isolated JVM stream evidence.
All tests are pure synthetic inputs; NO Windows worker launches.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"tools/fc01_f03_cr2/m2_r1_cr2/receipt_contract.py"
FROZEN=ROOT/"GOVERNANCE/AO-E0-B12-DATA-01-FC01-JF02-F03-CR2-CR1-M2-R1-CR2-PREEXECUTION-FREEZE-V0.1.json"

@pytest.fixture(scope="module")
def contract():
    if not TARGET.is_file():
        return None
    spec=importlib.util.spec_from_file_location("cr2_contract",TARGET)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

@pytest.fixture(scope="module")
def freeze():
    packet=json.loads(FROZEN.read_text(encoding="utf8"))
    assert len(packet["campaign_runs"])==13
    assert packet["campaign_budget"]==13
    assert packet["regression_budget"]["worker_launches"]==0
    return packet


def raw():
    return {kind:content for kind,content in [
        ("supervisor_stdout",b"RESULT=PUBLISHED\n"),("supervisor_stderr",b""),
        ("jvm_stdout",b"JVM-SYNTHETIC-TEST\n"),("jvm_stderr",b""),
    ]}


def valid():
    x={
      "campaign_id":"M2R1CR2_20261010_CAP01","run_id":"normal_A","scenario":"valid",
      "final_present":True,"final_absence_verified":False,
      "final_sha256":hashlib.sha256(b"FINAL").hexdigest(),
      "final_bytes_verified":True,
      "supervisor_pid":101,"supervisor_start_filetime_utc":134361201931850216,
      "worker_pid":102,"worker_start_filetime_utc":134361201932179565,
      "job_limit_bytes":268435456,"assigned_before_resume":True,
      "job_current_bytes":405504,"job_peak_bytes":413696,
      "termination_confirmed":True,"tree_terminated":True,
      "descendant_created":False,"descendant_identities":[],
      "memory_failure":"NONE","publication_after_failure":False,
      "receipt_precreated":True,"capture_pre_resumed":True,
      "handle_allowlist_verified":True,
      "supervisor_crash":False,"recovery_proof":"NOT_APPLICABLE",
      "four_streams_independent":True,
      "streams":{k:{"sha256":hashlib.sha256(v).hexdigest(),
                   "length":len(v),"source":("jvm" if k.startswith("jvm_") else "supervisor"),
                   "created_prelaunch":True,"closed_and_readback":True}
                 for k,v in raw().items()}
    }
    return x


@pytest.mark.parametrize("number",list(range(1,17)))
def test_cr2_preregistered_cases(contract,freeze,number):
    assert contract is not None,"RED: CR2 validator implementation absent"
    pkt=valid();bytes_=raw();expected="BLOCKED"
    if number==1:
        pkt.update(final_present=False,final_absence_verified=True,final_sha256=None,
                   final_bytes_verified=False,memory_failure="JAVA_OUT_OF_MEMORY")
        expected="PASS"
    elif number==2: pkt["final_sha256"]=None
    elif number==3: pkt["final_sha256"]="0"*64
    elif number==4: pkt.update(final_present=None,final_absence_verified=False,final_sha256=None)
    elif number==5: pkt["streams"].pop("jvm_stdout")
    elif number==6: pkt["streams"].pop("jvm_stderr")
    elif number==7:
        pkt["streams"]["jvm_stderr"]["length"]=0
        expected="PASS"
    elif number==8: pkt["streams"]["jvm_stdout"]["created_prelaunch"]=False
    elif number==9: pkt["streams"]["jvm_stdout"]["sha256"]="0"*64
    elif number==10: pkt["worker_start_filetime_utc"]=0
    elif number==11: pkt["termination_confirmed"]=False
    elif number==12: pkt.update(descendant_created=True,descendant_identities=[])
    elif number==13:
        pkt.update(supervisor_crash=True,recovery_proof="NOT_OBSERVED",
                   termination_confirmed=False)
    elif number==14: pkt["receipt_precreated"]=False
    elif number==15: pkt.update(publication_after_failure=True,memory_failure="JAVA_OUT_OF_MEMORY")
    elif number==16: expected="PASS"
    result=contract.validate(pkt,bytes_,expected_final_sha256=hashlib.sha256(b"FINAL").hexdigest())
    assert result["status"]==expected,(number,result)
    if expected=="BLOCKED":
        assert result["violations"],number


def test_cr2_no_live_api(contract,freeze):
    assert contract is not None,"RED: isolated validator absent"
    source=TARGET.read_text(encoding="utf8")
    assert "sendOrder" not in source and "ClientFactory" not in source
    assert freeze["firewall"]["provider_requests"]==0

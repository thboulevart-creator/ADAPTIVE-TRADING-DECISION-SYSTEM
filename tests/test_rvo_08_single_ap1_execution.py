from pathlib import Path
import json
import pytest
from tools import rvo_08_single_ap1_execution as r

def test_rvo08_contract_and_budget():
    assert r.CONTRACT=="ATDS_RVO_08_FIRST_REAL_CC02_SINGLE_AP1_EXECUTION_V0_1"
    assert r.TIMEOUT_SECONDS==3600
    assert r.MAX_OUTPUT_BYTES==32*1024*1024

def test_rvo08_authority_none():
    assert r.AUTHORITY_NONE=={"scientific":False,"operational":False,"trading":False,"capital":False}

def test_rvo08_canonical_digest_deterministic():
    assert r.sha256_bytes(r.canonical({"b":2,"a":1}))==r.sha256_bytes(r.canonical({"a":1,"b":2}))

def test_rvo08_verify_rejects_second_invocation_count(tmp_path: Path):
    out=tmp_path/"out.json"; out.write_text("{}",encoding="utf-8")
    freeze=tmp_path/"freeze.json"; freeze.write_text(json.dumps({"x":1}),encoding="utf-8")
    receipt=tmp_path/"receipt.json"
    receipt.write_text(json.dumps({
      "status":"RVO_08_SINGLE_AP1_EXECUTION_COMPLETE","invocation_count":2,"automatic_retry":False,
      "exit_code":0,"timeout_observed":False,"m03_executed":False,"authority":r.AUTHORITY_NONE,
      "output_transport":str(out),"output_bytes":2,"output_sha256":r.sha256_path(out),
      "freeze_sha256":r.sha256_path(freeze)
    }),encoding="utf-8")
    ledger=tmp_path/"ledger.json"; ledger.write_text(json.dumps({"invocation_count":2,"state":"COMPLETED"}),encoding="utf-8")
    class A: pass
    a=A(); a.freeze=str(freeze); a.execution_receipt=str(receipt); a.ledger=str(ledger)
    with pytest.raises(RuntimeError,match="INVOCATION_COUNT_INVALID"):
        r.verify(a)

def test_rvo08_spec_is_factory_generated_real_claim(tmp_path: Path):
    a=r._make_real_cc02_spec(tmp_path/"a")
    assert a.experiment_spec_id.startswith("EXS-")
    assert "One AP1 invocation only" in a.protocol
    assert "no M03 execution" in a.protocol

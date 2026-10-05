from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import os
import struct
import subprocess
import tempfile
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.context import build_context
from src.data.dataset_admissibility import DatasetIdentity
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.research.execution import QualifiedResearchInput, run_qualified_research
from src.research.input_binding import bind_execution_input, corpus_inventory_hash, sha256_file
from src.research_run_evidence import derive_runtime_research_identity, from_research_execution
from src.revision import produce_revision_decision
from src import p1_12c_qualified_producer_execution as p12c

CONTRACT = "ATDS_RVO_08_FIRST_REAL_CC02_SINGLE_AP1_EXECUTION_V0_1"
REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"
RVO07_BLOB = "828851954c12745021c7463befb9761e5eaa51bc"
DATA02_BLOB = "ccfccda676abfe7e02082a331557ffed14e1f32b"
P121_BLOB = "49142e1928cf32ec10ed9a4809388a782559ad42"
SMF_BLOB = "b7bf4f20d24aebafb9ff6c6e9029330afb9c0921"
G05_BLOB = "60a17b59aa03a41d517ee887c565d314a3d92ce5"
AP1_BLOB = "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
RUNTIME_LOCK_DIGEST = "5b77e0c094812f3e7e9d25efdb87bd3da92748bc6f8a436ffe52cefe6d38f6c4"
RUNTIME_LOCK_ID = "RPRL-5b77e0c094812f3e7e9d25efdb87bd3d"
TIMEOUT_SECONDS = 3600
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
MEMORY_AUTHORITY = "RVO_08_NON_EMPIRICAL_PREREGISTRATION_SCAFFOLD_V0_1"
MEMORY_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_NONE = {"scientific":False,"operational":False,"trading":False,"capital":False}

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def sha256_path(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(root: Path, *args: str) -> str:
    cp=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True,check=False)
    if cp.returncode:
        raise RuntimeError("GIT_FAILED:"+cp.stderr.strip())
    return cp.stdout.strip()

def require(cond: bool, code: str) -> None:
    if not cond:
        raise RuntimeError(code)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def _write_seed_bi5(path: Path) -> None:
    records=b"".join((
        struct.pack(">IIIff",1,100200,100000,1.5,2.0),
        struct.pack(">IIIff",2,100300,100100,1.0,1.25),
    ))
    path.write_bytes(lzma.compress(records,format=lzma.FORMAT_ALONE))

def _make_real_cc02_spec(tmp: Path):
    seed=tmp/"seed"
    corpus=seed/"corpus"
    corpus.mkdir(parents=True,exist_ok=True)
    _write_seed_bi5(corpus/"2026010200.bi5")
    seed_contract=seed/"seed-contract.json"
    seed_contract.write_text(json.dumps({
        "asset_id":"RVO08_NON_EMPIRICAL_SCAFFOLD",
        "source":"RVO08_CONTROL",
        "format":"BI5",
        "record_size":20,
        "record_struct":">IIIff",
        "timestamp_unit":"milliseconds",
        "price_scale":1000,
    },sort_keys=True,separators=(",",":")),encoding="utf-8")
    qi=QualifiedResearchInput(
        corpus_root=corpus,
        contract_path=seed_contract,
        expected_corpus_hash=corpus_inventory_hash(corpus),
        expected_contract_hash=sha256_file(seed_contract),
    )
    ident=derive_runtime_research_identity(qi)
    dataset=DatasetIdentity(
        dataset_id=ident.dataset_id,dataset_version=ident.dataset_version,
        content_hash=ident.corpus_sha256,format=ident.format,
        schema_version="dukascopy-bi5-v1",
        instrument=ident.instrument,granularity="tick",timezone_storage="UTC",
    )
    context=build_context(
        dataset,configuration_version=ident.configuration_version,
        observation_start="2026-01-02T00:00:00.001000+00:00",
        observation_end="2026-01-02T00:00:00.002000+00:00",
    )
    result=run_qualified_research(qi)
    evidence=from_research_execution(qi,result,code_version="963f02e93db63bef36c25d58c3634096a2247e6a",context=context,dataset=dataset)
    decision=produce_decision(evidence,context=context,decision="HOLD")
    action=engage_qualification_action(decision,behavior="NO_ACTION")
    observed=observe_qualification_result(action,outcome="RVO08_PREREGISTRATION_SCAFFOLD_ONLY")
    trace=produce_decision_trace(evidence,decision,action,observed)
    episode=produce_observational_memory_episode(trace,action,observed)
    capture=persist_witnessed_memory_episode(tmp/"memory",episode,authority_id=MEMORY_AUTHORITY)
    historical=reattest_persisted_memory_episode(
        capture.record_path,capture.receipt_path,
        expected_contract_id=MEMORY_CONTRACT,
        expected_authority_id=MEMORY_AUTHORITY,
        expected_receipt_sha256=capture.receipt_sha256,
    )
    scope=create_audit_scope(
        question="What exact first real CC02 descriptive AP1 execution has been separately human-authorized after RVO-07 GO?",
        expected_registration_ids=(historical.registration_id,),
        context_fields=("context_id","decision","behavior"),
    )
    assessment=audit_memory_collection(scope,(historical,))
    revision=produce_revision_decision(
        assessment,scope,"REQUEST_NEW_EXPERIMENT",
        "Execute exactly one real AP1 retrospective descriptive census on the exact DATA-02-admitted USTECH_PROFILE_MINUTE_CORE_V0_1 corpus, without M03 execution or scientific interpretation.",
    )
    request=produce_follow_up_request(revision)
    return specify_experiment(
        request,
        hypothesis_statement="The exact admitted AP0 corpus has a descriptive intraday and spread distribution measurable by the frozen AP1 producer.",
        prediction="One authorized AP1 invocation will either produce the frozen AP1_COMPLETE schema bound to the exact AP0 manifest or fail closed.",
        falsification_rule="Any owner-identity drift, manifest mismatch, runtime mismatch, nonzero exit, timeout, output-size breach, schema/status mismatch, or unexpected authority fails the execution qualification.",
        protocol="One AP1 invocation only; exact DATA-02/P1/runtime bindings; no automatic retry; no M03 execution; no OOS, backtest, trading, or capital.",
        measurement_plan="Run the frozen AP1 producer once over all 61 admitted AP0 Parquet files and retain its canonical descriptive JSON strictly as an execution result.",
    )

def _read_json(path: Path) -> dict[str,Any]:
    obj=json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj,dict),"JSON_OBJECT_REQUIRED")
    return obj

def _verify_prereq_receipts(repo_root: Path) -> None:
    pins={
      "reports/program/2026-10-05-RVO-07-QUALIFICATION-RECEIPT-V0.1.json":RVO07_BLOB,
      "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json":DATA02_BLOB,
      "reports/program/2026-10-05-P1-21-QUALIFICATION-RECEIPT-V0.1.json":P121_BLOB,
      "reports/program/2026-10-05-SMF-AP1-M03-01-QUALIFICATION-RECEIPT-V0.1.json":SMF_BLOB,
      "reports/program/2026-10-05-G05-01-QUALIFICATION-RECEIPT-V0.1.json":G05_BLOB,
      "tools/ap1_intraday_spread_census.py":AP1_BLOB,
    }
    for path,blob in pins.items():
        require(git(repo_root,"rev-parse","HEAD:"+path)==blob,"OWNER_BLOB_MISMATCH:"+path)

def _verify_fresh_receipts(g05: dict[str,Any], rvo07: dict[str,Any], head: str, tree: str) -> None:
    require(g05.get("status")=="G05_01_WORKSPACE_DRY_READY","G05_NOT_READY")
    require(g05.get("identity",{}).get("head")==head and g05.get("identity",{}).get("tree")==tree,"G05_HEAD_TREE_MISMATCH")
    require(g05.get("runtime_lock",{}).get("runtime_lock_digest")==RUNTIME_LOCK_DIGEST,"RUNTIME_LOCK_MISMATCH")
    require(g05.get("ap0",{}).get("dataset_identity")==DATASET_IDENTITY,"G05_DATASET_MISMATCH")
    require(g05.get("ap0",{}).get("manifest_sha256")==MANIFEST_SHA256,"G05_MANIFEST_MISMATCH")
    require(g05.get("ap0",{}).get("parquet_file_count")==61,"G05_FILE_COUNT_MISMATCH")
    require(g05.get("ap0",{}).get("parquet_content_opened") is False,"G05_PARQUET_ALREADY_OPENED")
    forbidden=g05.get("forbidden_observations",{})
    require(all(forbidden.get(k) is False for k in ("ap1_executed","m03_executed","new_empirical_result","oos_consumed","parquet_statistical_open")),"G05_FORBIDDEN_OBSERVATION")
    require(rvo07.get("verdict")=="GO" and rvo07.get("readiness")=="PRE_EXECUTION_READINESS_GO","RVO07_NOT_GO")
    fr=rvo07.get("pre_result_freeze",{})
    require(fr.get("head")==head and fr.get("tree")==tree,"RVO07_HEAD_TREE_MISMATCH")
    require(all(v.get("status")=="PRE_EXECUTION_REQUALIFIED_CLOSED" for v in rvo07.get("gaps",{}).values()),"RVO07_GAP_OPEN")
    require(rvo07.get("execution_authorized") is False,"RVO07_AUTHORITY_LAUNDERING")

def build_real_plan(*, repo_root: Path, ap0_root: Path, ap0_manifest: Path, output: Path, resource_contract: Path, python_real_binary: Path):
    data_receipt=repo_root/"reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"
    runtime_evidence_path=repo_root/"GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json"
    producer=repo_root/"tools/ap1_intraday_spread_census.py"
    runner=repo_root/"tools/p1_12c_sandbox_runner.py"
    require(sha256_path(ap0_manifest)==MANIFEST_SHA256,"AP0_MANIFEST_SHA256_MISMATCH")
    require(not output.exists(),"AP1_OUTPUT_ALREADY_EXISTS")
    with tempfile.TemporaryDirectory(prefix="rvo08-spec-") as td:
        specification=_make_real_cc02_spec(Path(td))
        bound=bind_execution_input(
            ap0_root,resource_contract,
            corpus_inventory_hash(ap0_root),
            sha256_file(resource_contract),
        )
        execution_binding=bind_experiment_execution(specification,bound)
        qualified_input=qualify_experiment_execution_input(execution_binding)
        data_binding=p12c.bind_real_data_owner_evidence(data_receipt,result_exposed=False)
        profile=p12c.qualify_ap1_invocation_profile(producer,result_exposed=False)
        runtime_evidence=_read_json(runtime_evidence_path)
        runtime_lock=p12c.qualify_real_producer_runtime_lock(
            runtime_evidence,profile,
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=TIMEOUT_SECONDS,
            material_environment={"PYTHONHASHSEED":"0","PYTHONDONTWRITEBYTECODE":"1"},
            result_exposed=False,
        )
        require(runtime_lock.runtime_lock_id==RUNTIME_LOCK_ID and runtime_lock.runtime_lock_digest==RUNTIME_LOCK_DIGEST,"RUNTIME_LOCK_IDENTITY_MISMATCH")
        require(sha256_path(python_real_binary)==runtime_lock.python_binary_sha256,"PYTHON_BINARY_HASH_MISMATCH")
        plan=p12c.qualify_real_producer_execution_plan(
            qualified_input,data_binding,profile,runtime_lock,
            producer_path=producer,
            ap0_root_transport=str(ap0_root),
            ap0_manifest_transport=str(ap0_manifest),
            output_transport=str(output),
            expected_output_schema=p12c.AP1_OUTPUT_SCHEMA,
            expected_output_status=p12c.AP1_OUTPUT_STATUS,
            expected_output_contract="ATDS_AP1_CANONICAL_JSON_OUTPUT_V1",
            maximum_output_bytes=MAX_OUTPUT_BYTES,
            result_exposed=False,
        )
        cmd=p12c.build_ap1_runner_command(
            plan,profile,
            python_executable=str(python_real_binary),
            runner_path=runner,
            producer_path=producer,
        )
        return {
          "specification":asdict(specification),
          "execution_binding":asdict(execution_binding),
          "qualified_input":asdict(qualified_input),
          "data_binding":asdict(data_binding),
          "invocation_profile":asdict(profile),
          "runtime_lock":asdict(runtime_lock),
          "plan":asdict(plan),
          "command":list(cmd),
          "command_digest":sha256_bytes(canonical(list(cmd))),
          "resource_contract_sha256":sha256_path(resource_contract),
          "resource_contract_blob":git(repo_root,"rev-parse","HEAD:GOVERNANCE/RVO-08-AP0-RESOURCE-CONTRACT-V0.1.json"),
        }

def prepare(args) -> int:
    repo_root=Path(args.repo_root).resolve()
    main_root=Path(args.main_checkout_root).resolve()
    ap0_root=Path(args.ap0_root).resolve()
    ap0_manifest=Path(args.ap0_manifest).resolve()
    output=Path(args.output).resolve()
    freeze_out=Path(args.freeze_out).resolve()
    resource_contract=Path(args.resource_contract).resolve()
    python_real=Path(args.python_real_binary).resolve()
    head=git(repo_root,"rev-parse","HEAD")
    tree=git(repo_root,"rev-parse","HEAD^{tree}")
    require(head==args.expected_head and tree==args.expected_tree,"WORKSPACE_HEAD_TREE_MISMATCH")
    require(git(repo_root,"branch","--show-current")=="","WORKSPACE_NOT_DETACHED")
    require(git(repo_root,"status","--porcelain","--untracked-files=all")=="","WORKSPACE_DIRTY")
    require(git(main_root,"status","--porcelain","--untracked-files=all")=="","MAIN_CHECKOUT_DIRTY")
    _verify_prereq_receipts(repo_root)
    g05=_read_json(Path(args.g05_receipt))
    rvo07=_read_json(Path(args.rvo07_receipt))
    _verify_fresh_receipts(g05,rvo07,head,tree)
    require(not output.exists(),"AP1_OUTPUT_ALREADY_EXISTS")
    built=build_real_plan(repo_root=repo_root,ap0_root=ap0_root,ap0_manifest=ap0_manifest,output=output,resource_contract=resource_contract,python_real_binary=python_real)
    freeze={
      "schema":"ATDS_RVO_08_PRE_RESULT_EXECUTION_FREEZE_V0_1",
      "status":"PRE_RESULT_EXECUTION_FROZEN",
      "repository":REPOSITORY,"branch":BRANCH,"head":head,"tree":tree,
      "rvo07_external_receipt_sha256":sha256_path(Path(args.rvo07_receipt)),
      "g05_external_receipt_sha256":sha256_path(Path(args.g05_receipt)),
      "experiment_spec_id":built["specification"]["experiment_spec_id"],
      "execution_binding_id":built["execution_binding"]["execution_binding_id"],
      "experiment_execution_input_id":built["qualified_input"]["experiment_execution_input_id"],
      "p1_data_evidence_binding_id":built["data_binding"]["p1_data_evidence_binding_id"],
      "p1_data_evidence_binding_digest":built["data_binding"]["p1_data_evidence_binding_digest"],
      "invocation_profile_id":built["invocation_profile"]["invocation_profile_id"],
      "invocation_profile_digest":built["invocation_profile"]["invocation_profile_digest"],
      "runtime_lock_id":built["runtime_lock"]["runtime_lock_id"],
      "runtime_lock_digest":built["runtime_lock"]["runtime_lock_digest"],
      "real_producer_execution_plan_id":built["plan"]["real_producer_execution_plan_id"],
      "real_producer_execution_plan_digest":built["plan"]["real_producer_execution_plan_digest"],
      "resource_contract_blob":built["resource_contract_blob"],
      "resource_contract_sha256":built["resource_contract_sha256"],
      "ap0_root_transport":str(ap0_root),"ap0_manifest_transport":str(ap0_manifest),
      "output_transport":str(output),"maximum_output_bytes":MAX_OUTPUT_BYTES,
      "command":built["command"],"command_digest":built["command_digest"],
      "invocation_budget":1,"automatic_retry":False,"invocations_observed":0,
      "result_exposed":False,"m03_execution_authorized":False,
      "authority":dict(AUTHORITY_NONE),
    }
    freeze["freeze_digest"]=sha256_bytes(canonical(freeze))
    freeze_out.parent.mkdir(parents=True,exist_ok=True)
    freeze_out.write_bytes(json.dumps(freeze,sort_keys=True,indent=2,ensure_ascii=False).encode("utf-8")+b"\n")
    print("RVO_08_PREPARED")
    for k in ("experiment_spec_id","execution_binding_id","experiment_execution_input_id","real_producer_execution_plan_id","real_producer_execution_plan_digest","command_digest","freeze_digest"):
        print(k.upper()+"="+str(freeze[k]))
    print("FREEZE="+str(freeze_out))
    return 0

def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False).encode("utf-8")+b"\n")

def execute_once(args) -> int:
    freeze_path=Path(args.freeze).resolve()
    freeze=_read_json(freeze_path)
    repo_root=Path(args.repo_root).resolve()
    main_root=Path(args.main_checkout_root).resolve()
    ap0_root=Path(freeze["ap0_root_transport"])
    ap0_manifest=Path(freeze["ap0_manifest_transport"])
    output=Path(freeze["output_transport"])
    resource_contract=Path(args.resource_contract).resolve()
    python_real=Path(args.python_real_binary).resolve()
    ledger=Path(args.ledger).resolve()
    receipt_path=Path(args.execution_receipt).resolve()
    require(freeze.get("status")=="PRE_RESULT_EXECUTION_FROZEN","FREEZE_STATUS_INVALID")
    require(git(repo_root,"rev-parse","HEAD")==freeze["head"] and git(repo_root,"rev-parse","HEAD^{tree}")==freeze["tree"],"EXECUTION_HEAD_TREE_DRIFT")
    require(git(repo_root,"branch","--show-current")=="","WORKSPACE_NOT_DETACHED")
    require(git(repo_root,"status","--porcelain","--untracked-files=all")=="","WORKSPACE_DIRTY")
    require(git(main_root,"status","--porcelain","--untracked-files=all")=="","MAIN_CHECKOUT_DIRTY")
    require(not output.exists(),"AP1_OUTPUT_ALREADY_EXISTS")
    require(not ledger.exists(),"SECOND_AP1_INVOCATION_BLOCKED")
    require(not receipt_path.exists(),"EXECUTION_RECEIPT_ALREADY_EXISTS")
    built=build_real_plan(repo_root=repo_root,ap0_root=ap0_root,ap0_manifest=ap0_manifest,output=output,resource_contract=resource_contract,python_real_binary=python_real)
    checks={
      "experiment_spec_id":built["specification"]["experiment_spec_id"],
      "execution_binding_id":built["execution_binding"]["execution_binding_id"],
      "experiment_execution_input_id":built["qualified_input"]["experiment_execution_input_id"],
      "p1_data_evidence_binding_id":built["data_binding"]["p1_data_evidence_binding_id"],
      "p1_data_evidence_binding_digest":built["data_binding"]["p1_data_evidence_binding_digest"],
      "invocation_profile_id":built["invocation_profile"]["invocation_profile_id"],
      "invocation_profile_digest":built["invocation_profile"]["invocation_profile_digest"],
      "runtime_lock_id":built["runtime_lock"]["runtime_lock_id"],
      "runtime_lock_digest":built["runtime_lock"]["runtime_lock_digest"],
      "real_producer_execution_plan_id":built["plan"]["real_producer_execution_plan_id"],
      "real_producer_execution_plan_digest":built["plan"]["real_producer_execution_plan_digest"],
      "command_digest":built["command_digest"],
    }
    for key,value in checks.items():
        require(freeze.get(key)==value,"FREEZE_REBUILD_MISMATCH:"+key)
    require(sha256_path(freeze_path)==args.expected_freeze_sha256,"FREEZE_FILE_SHA256_MISMATCH")
    started=utc_now()
    ledger.parent.mkdir(parents=True,exist_ok=True)
    with ledger.open("x",encoding="utf-8") as fh:
        json.dump({"schema":"ATDS_RVO_08_ONE_SHOT_LEDGER_V0_1","state":"STARTED","invocation_count":1,"started_at":started,"freeze_sha256":args.expected_freeze_sha256,"command_digest":built["command_digest"]},fh,sort_keys=True,indent=2)
        fh.write("\n")
        fh.flush(); os.fsync(fh.fileno())
    env=os.environ.copy()
    env.update({"PYTHONHASHSEED":"0","PYTHONDONTWRITEBYTECODE":"1"})
    t0=time.monotonic()
    timeout_observed=False
    try:
        cp=subprocess.run(built["command"],capture_output=True,text=False,check=False,timeout=TIMEOUT_SECONDS,env=env)
        exit_code=cp.returncode
        stdout=cp.stdout or b""
        stderr=cp.stderr or b""
    except subprocess.TimeoutExpired as exc:
        timeout_observed=True
        exit_code=None
        stdout=exc.stdout or b""
        stderr=exc.stderr or b""
    ended=utc_now()
    duration=time.monotonic()-t0
    base={
      "schema":"ATDS_RVO_08_SINGLE_AP1_EXECUTION_RECEIPT_V0_1",
      "freeze_sha256":args.expected_freeze_sha256,
      "freeze_digest":freeze["freeze_digest"],
      "head":freeze["head"],"tree":freeze["tree"],
      "command_digest":built["command_digest"],
      "invocation_count":1,"automatic_retry":False,
      "started_at":started,"ended_at":ended,"duration_seconds":duration,
      "timeout_seconds":TIMEOUT_SECONDS,"timeout_observed":timeout_observed,
      "exit_code":exit_code,
      "stdout_sha256":sha256_bytes(stdout),"stderr_sha256":sha256_bytes(stderr),
      "runtime_lock_id":RUNTIME_LOCK_ID,"runtime_lock_digest":RUNTIME_LOCK_DIGEST,
      "ap0_manifest_sha256":MANIFEST_SHA256,"producer_blob":AP1_BLOB,
      "output_transport":str(output),
      "result_semantics":"EXECUTION_RESULT_ONLY",
      "m03_executed":False,
      "authority":dict(AUTHORITY_NONE),
    }
    if timeout_observed:
        receipt={**base,"status":"BLOCKED_AP1_TIMEOUT"}
        _write_json(receipt_path,receipt)
        return 3
    if exit_code!=0:
        receipt={**base,"status":"BLOCKED_AP1_EXECUTION_FAILED"}
        _write_json(receipt_path,receipt)
        return 4
    if not output.is_file():
        receipt={**base,"status":"BLOCKED_AP1_OUTPUT_MISSING"}
        _write_json(receipt_path,receipt)
        return 5
    size=output.stat().st_size
    if size<=0 or size>MAX_OUTPUT_BYTES:
        receipt={**base,"status":"BLOCKED_AP1_OUTPUT_SIZE","output_bytes":size}
        _write_json(receipt_path,receipt)
        return 6
    raw=output.read_bytes()
    try:
        payload=json.loads(raw.decode("utf-8"))
    except Exception:
        receipt={**base,"status":"BLOCKED_AP1_OUTPUT_JSON","output_bytes":size,"output_sha256":sha256_bytes(raw)}
        _write_json(receipt_path,receipt)
        return 7
    valid=(
      payload.get("schema")==p12c.AP1_OUTPUT_SCHEMA and
      payload.get("status")==p12c.AP1_OUTPUT_STATUS and
      payload.get("input_identity")==DATASET_IDENTITY and
      payload.get("binding",{}).get("ap0_manifest_sha256")==MANIFEST_SHA256 and
      payload.get("binding",{}).get("ap0_files_rehashed")==61 and
      payload.get("scope",{}).get("strategy_agnostic") is True and
      payload.get("scope",{}).get("returns_calculated") is False and
      payload.get("scope",{}).get("signals_calculated") is False and
      payload.get("scope",{}).get("pnl_calculated") is False
    )
    if not valid:
        receipt={**base,"status":"BLOCKED_AP1_OUTPUT_CONTRACT","output_bytes":size,"output_sha256":sha256_bytes(raw)}
        _write_json(receipt_path,receipt)
        return 8
    receipt={
      **base,
      "status":"RVO_08_SINGLE_AP1_EXECUTION_COMPLETE",
      "execution_status":"EXECUTED",
      "output_bytes":size,
      "output_sha256":sha256_bytes(raw),
      "output_schema":payload["schema"],
      "output_status":payload["status"],
      "output_contract_checks":"PASS",
      "scientific_finding":False,
      "strategy_validated":False,
      "trading_signal":False,
    }
    _write_json(receipt_path,receipt)
    ledger_state=_read_json(ledger)
    ledger_state.update({"state":"COMPLETED","ended_at":ended,"execution_receipt_sha256":sha256_path(receipt_path),"output_sha256":receipt["output_sha256"]})
    _write_json(ledger,ledger_state)
    print("RVO_08_SINGLE_AP1_EXECUTION_COMPLETE")
    print("EXIT_CODE=0")
    print("OUTPUT_BYTES="+str(size))
    print("OUTPUT_SHA256="+receipt["output_sha256"])
    print("OUTPUT_SCHEMA="+receipt["output_schema"])
    print("OUTPUT_STATUS="+receipt["output_status"])
    print("EXECUTION_RECEIPT="+str(receipt_path))
    return 0

def verify(args) -> int:
    freeze=_read_json(Path(args.freeze))
    receipt=_read_json(Path(args.execution_receipt))
    ledger=_read_json(Path(args.ledger))
    output=Path(receipt["output_transport"])
    require(receipt.get("status")=="RVO_08_SINGLE_AP1_EXECUTION_COMPLETE","EXECUTION_RECEIPT_NOT_COMPLETE")
    require(receipt.get("invocation_count")==1 and receipt.get("automatic_retry") is False,"INVOCATION_COUNT_INVALID")
    require(receipt.get("exit_code")==0 and receipt.get("timeout_observed") is False,"EXECUTION_NOT_SUCCESSFUL")
    require(receipt.get("m03_executed") is False,"M03_EXECUTED")
    require(receipt.get("authority")==AUTHORITY_NONE,"AUTHORITY_LAUNDERING")
    require(ledger.get("invocation_count")==1 and ledger.get("state")=="COMPLETED","ONE_SHOT_LEDGER_INVALID")
    require(output.is_file(),"OUTPUT_MISSING")
    require(output.stat().st_size==receipt["output_bytes"],"OUTPUT_SIZE_DRIFT")
    require(sha256_path(output)==receipt["output_sha256"],"OUTPUT_HASH_DRIFT")
    require(receipt.get("freeze_sha256")==sha256_path(Path(args.freeze)),"FREEZE_BINDING_DRIFT")
    print("RVO_08_VERIFY_PASS")
    print("INVOCATION_COUNT=1")
    print("M03_EXECUTED=FALSE")
    print("OUTPUT_SHA256="+receipt["output_sha256"])
    return 0

def main() -> int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="mode",required=True)
    p=sub.add_parser("prepare")
    for name in ("repo-root","main-checkout-root","expected-head","expected-tree","g05-receipt","rvo07-receipt","ap0-root","ap0-manifest","output","freeze-out","resource-contract","python-real-binary"):
        p.add_argument("--"+name,required=True)
    e=sub.add_parser("execute-once")
    for name in ("repo-root","main-checkout-root","freeze","expected-freeze-sha256","resource-contract","python-real-binary","ledger","execution-receipt"):
        e.add_argument("--"+name,required=True)
    v=sub.add_parser("verify")
    for name in ("freeze","execution-receipt","ledger"):
        v.add_argument("--"+name,required=True)
    args=ap.parse_args()
    if args.mode=="prepare": return prepare(args)
    if args.mode=="execute-once": return execute_once(args)
    return verify(args)

if __name__=="__main__":
    raise SystemExit(main())

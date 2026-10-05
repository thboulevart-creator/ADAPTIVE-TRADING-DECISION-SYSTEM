from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo

from src import p1_12c_qualified_producer_execution as p12c
from src import smf_ap1_m03_binding as smf
from src.data import claim_scoped_admission as data02
from src.experiment_execution_binding import bind_experiment_execution
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.research.input_binding import bind_execution_input, corpus_inventory_hash, sha256_file
from tests.data_02_fixture import make_package as make_data02_package
from tests.rvo_05_fixture import make_p1_spec

CONTRACT = "ATDS_G05_01_WORKSPACE_DRY_READINESS_V0_1"
REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
CANONICAL_BRANCH = "integration/system-v1"
REMOTE_URL = "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM.git"
TIMEOUT_SECONDS = 3600
MATERIAL_ENVIRONMENT = {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_PARQUET_COUNT = 61
PYTHON_VERSION = "3.13.14"
PYTHON_REAL_BINARY_SHA256 = "ad169f4cb4bfb78c7a5c030a4529c19d6643276778e33994c93e145b6191c3ec"
EXPECTED_DEPENDENCIES = {
    "numpy": {"version": "2.5.3", "metadata_sha256": "451a9b8028000588e66b0b415587b6aef0bbc51a96d8e8a0cba0dc23acf64f99", "record_sha256": "5135e045b7bc7d8f2ef83e2bd9c618840f46ebd09d8590c819bbcdeb32cfe41e"},
    "pyarrow": {"version": "25.0.1", "metadata_sha256": "12ed8d0988a6f7153fec923ee47b7fc1d6134463a86b1b89fa36f24c250163ff", "record_sha256": "a6cc5dcd5681d231959f61ccc1b57cb13dc1690f0819ed7bfd66ebd575e0db24"},
    "tzdata": {"version": "2026.3", "metadata_sha256": "511c019df477939fe7f4c38e32ad74a570c4ebb05b13fd2fffd0f0f2dbe6f7b1", "record_sha256": "8f9f4ae062c3c9af93f22cff46986c4735d15d1306a413df291d5b67301db0eb"},
}
PROTECTED_BLOBS = {
    "reports/program/2026-10-05-P1-21-QUALIFICATION-RECEIPT-V0.1.json": "49142e1928cf32ec10ed9a4809388a782559ad42",
    "src/p1_12c_qualified_producer_execution.py": "9d304202d44c8917cf640fd0b4114169968e511e",
    "tools/p1_12c_sandbox_runner.py": "b16fa57409a67049eedfbb6c6ec7b2e9ae3e3108",
    "tools/ap1_intraday_spread_census.py": "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a",
    "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json": "ccfccda676abfe7e02082a331557ffed14e1f32b",
    "GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json": "e4e275e8590e3bead9123969c068b036c6c4e1d8",
    "reports/program/2026-10-05-SMF-AP1-M03-01-QUALIFICATION-RECEIPT-V0.1.json": "b7bf4f20d24aebafb9ff6c6e9029330afb9c0921",
    "src/smf_ap1_m03_binding.py": "f4c0295625f8b360effbd27a8d616d9644ea2a5e",
    "tools/smf_ap1_m03_companion.py": "7ec9ef71c8682abc4c8f9561518f84268c00ed11",
}
CASE_IDS = tuple(f"G0501-B{i:02d}" for i in range(1,31))

class G0501Blocked(RuntimeError):
    pass

def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _sha256_path(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _digest(value: Any) -> str:
    return _sha256_bytes(_canonical_json(value).encode("utf-8"))

def _git(root: Path, *args: str) -> str:
    completed=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True,check=False)
    if completed.returncode != 0:
        raise G0501Blocked("GIT_COMMAND_FAILED:"+" ".join(args)+":"+completed.stderr.strip())
    return completed.stdout.strip()

def _require(ok: bool, code: str) -> None:
    if not ok:
        raise G0501Blocked(code)

def _dependency_identity(name: str) -> dict[str,str]:
    dist=metadata.distribution(name)
    base=Path(dist._path)
    return {
        "version": dist.version,
        "metadata_sha256": _sha256_path(base/"METADATA"),
        "record_sha256": _sha256_path(base/"RECORD"),
    }

def collect_runtime_observation(python_real_binary: Path) -> dict[str,Any]:
    _require(python_real_binary.is_file(), "BLOCKED_PYTHON_REAL_BINARY_NOT_FOUND")
    observation={
        "platform": platform.system(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "python_real_binary_sha256": _sha256_path(python_real_binary),
        "dependencies": {name:_dependency_identity(name) for name in ("numpy","pyarrow","tzdata")},
        "timezone_name":"America/New_York",
        "timezone_probe":"PASS",
        "material_environment": {k:os.environ.get(k) for k in MATERIAL_ENVIRONMENT},
    }
    try:
        ZoneInfo("America/New_York")
    except Exception as exc:
        raise G0501Blocked("BLOCKED_AMERICA_NEW_YORK_TIMEZONE") from exc
    return observation

def validate_runtime_observation(observation: Mapping[str,Any]) -> None:
    _require(observation.get("platform")=="Windows", "BLOCKED_RUNTIME_PLATFORM_MISMATCH")
    _require(observation.get("architecture") in ("AMD64","x86_64"), "BLOCKED_RUNTIME_ARCH_MISMATCH")
    _require(observation.get("python_version")==PYTHON_VERSION, "BLOCKED_PYTHON_VERSION_MISMATCH")
    _require(observation.get("python_real_binary_sha256")==PYTHON_REAL_BINARY_SHA256, "BLOCKED_PYTHON_BINARY_IDENTITY_REQUIRED")
    deps=observation.get("dependencies")
    _require(isinstance(deps,Mapping), "BLOCKED_DEPENDENCY_IDENTITY_REQUIRED")
    for name,expected in EXPECTED_DEPENDENCIES.items():
        _require(deps.get(name)==expected, "BLOCKED_"+name.upper()+"_IDENTITY_REQUIRED")
    _require(observation.get("timezone_probe")=="PASS", "BLOCKED_AMERICA_NEW_YORK_TIMEZONE")
    _require(observation.get("material_environment")==MATERIAL_ENVIRONMENT, "BLOCKED_MATERIAL_ENVIRONMENT_MISMATCH")

def inspect_workspace(repo_root: Path, expected_head: str, expected_tree: str) -> dict[str,Any]:
    _require(repo_root.is_dir(), "BLOCKED_WORKSPACE_ROOT_NOT_FOUND")
    observed_root=_git(repo_root,"rev-parse","--show-toplevel").replace("\\","/")
    _require(Path(observed_root).resolve()==repo_root.resolve(), "BLOCKED_REPOSITORY_IDENTITY_MISMATCH")
    head=_git(repo_root,"rev-parse","HEAD")
    tree=_git(repo_root,"rev-parse","HEAD^{tree}")
    remote=_git(repo_root,"remote","get-url","origin")
    status=_git(repo_root,"status","--porcelain","--untracked-files=all")
    _require(head==expected_head, "BLOCKED_WORKSPACE_HEAD_MISMATCH")
    _require(tree==expected_tree, "BLOCKED_WORKSPACE_TREE_MISMATCH")
    _require(remote==REMOTE_URL, "BLOCKED_REPOSITORY_IDENTITY_MISMATCH")
    _require(status=="", "BLOCKED_WORKTREE_NOT_CLEAN")
    blobs={}
    for rel,expected in PROTECTED_BLOBS.items():
        path=repo_root/rel
        _require(path.is_file(), "BLOCKED_PROTECTED_OWNER_MISSING:"+rel)
        observed=_git(repo_root,"hash-object",rel)
        _require(observed==expected, "BLOCKED_PROTECTED_OWNER_DRIFT:"+rel)
        blobs[rel]=observed
    return {"head":head,"tree":tree,"remote":remote,"clean":True,"protected_blobs":blobs}

def inspect_ap0(ap0_root: Path) -> dict[str,Any]:
    _require(ap0_root.is_dir(), "BLOCKED_AP0_ROOT_NOT_FOUND")
    manifest=ap0_root/"AP0-MANIFEST.json"
    _require(manifest.is_file(), "BLOCKED_AP0_MANIFEST_NOT_FOUND")
    manifest_sha=_sha256_path(manifest)
    _require(manifest_sha==AP0_MANIFEST_SHA256, "BLOCKED_AP0_MANIFEST_IDENTITY_MISMATCH")
    try:
        parsed=json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        raise G0501Blocked("BLOCKED_AP0_MANIFEST_PARSE") from exc
    _require(parsed.get("output_identity")==DATASET_IDENTITY, "BLOCKED_DATASET_IDENTITY_MISMATCH")
    files=parsed.get("files")
    _require(isinstance(files,list) and len(files)==EXPECTED_PARQUET_COUNT, "BLOCKED_AP0_MANIFEST_FILE_COUNT_MISMATCH")
    actual_count=sum(1 for p in ap0_root.rglob("*.parquet") if p.is_file())
    _require(actual_count==EXPECTED_PARQUET_COUNT, "BLOCKED_AP0_PARQUET_FILE_COUNT_MISMATCH")
    return {"dataset_identity":DATASET_IDENTITY,"manifest_sha256":manifest_sha,"manifest_declared_files":len(files),"parquet_file_count":actual_count,"parquet_content_opened":False}

def output_probe(directory: Path) -> dict[str,Any]:
    directory.mkdir(parents=True,exist_ok=True)
    probe=directory/"G05-01-WRITE-PROBE.tmp"
    _require(not probe.exists(), "BLOCKED_OUTPUT_PROBE_PREEXISTS")
    probe.write_bytes(b"G05-01")
    ok=probe.is_file() and probe.read_bytes()==b"G05-01"
    probe.unlink()
    _require(ok and not probe.exists(), "BLOCKED_OUTPUT_DESTINATION_CAPABILITY")
    return {"directory_transport":str(directory),"write_probe":"PASS","probe_removed":True}

def _build_synthetic_qualified_input(tmp_path: Path):
    """Build only the synthetic P1 input shape; never create or execute a legacy P1.12C producer plan."""
    package=make_data02_package(tmp_path/"data")
    admission=data02.evaluate_synthetic(package)
    _require(admission.get("status")=="READY_FOR_EXACT_CLAIM", "BLOCKED_SYNTHETIC_P1_INPUT_FIXTURE")
    specification=make_p1_spec(tmp_path/"spec", tag="G0501")
    contract_path=tmp_path/"g05-01-synthetic-resource-contract.json"
    contract_path.write_text(
        json.dumps(
            {
                "format":"SYNTHETIC_DATA02_BYTE_FIXTURE",
                "scope":"G05-01-P1-DRY-PLAN-SHAPE-ONLY",
                "real_market_data":False,
                "oos":False,
            },
            sort_keys=True,
            separators=(",",":"),
        ),
        encoding="utf-8",
    )
    root=Path(package["root"])
    bound=bind_execution_input(
        root,
        contract_path,
        corpus_inventory_hash(root),
        sha256_file(contract_path),
    )
    execution_binding=bind_experiment_execution(specification,bound)
    return qualify_experiment_execution_input(execution_binding)


def build_dry_bindings(repo_root: Path, ap0_root: Path, runtime_observation: Mapping[str,Any], output_transport: str) -> dict[str,Any]:
    validate_runtime_observation(runtime_observation)
    data_receipt=repo_root/"reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"
    ap1=repo_root/"tools/ap1_intraday_spread_census.py"
    canonical_runtime=json.loads((repo_root/"GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json").read_text(encoding="utf-8"))
    observed_canonical={
        "platform":canonical_runtime["device"]["platform"],
        "architecture":"AMD64" if canonical_runtime["device"]["arch"]=="x64" else canonical_runtime["device"]["arch"],
        "python_version":canonical_runtime["device"]["python_version"],
        "python_real_binary_sha256":canonical_runtime["python"]["real_binary_sha256"],
        "dependencies":{name:{
            "version":canonical_runtime["dependencies"][name]["version"],
            "metadata_sha256":canonical_runtime["dependencies"][name]["metadata_sha256"],
            "record_sha256":canonical_runtime["dependencies"][name]["record_sha256"],
        } for name in ("numpy","pyarrow","tzdata")},
    }
    actual_comparable={k:runtime_observation[k] for k in ("platform","architecture","python_version","python_real_binary_sha256","dependencies")}
    _require(actual_comparable==observed_canonical, "BLOCKED_CURRENT_RUNTIME_DIFFERS_FROM_CANONICAL_RVO06_EVIDENCE")

    data_binding=p12c.bind_real_data_owner_evidence(data_receipt,result_exposed=False)
    profile=p12c.qualify_ap1_invocation_profile(ap1,result_exposed=False)
    runtime_lock=p12c.qualify_real_producer_runtime_lock(
        canonical_runtime,
        profile,
        runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
        timeout_seconds=TIMEOUT_SECONDS,
        material_environment=MATERIAL_ENVIRONMENT,
        result_exposed=False,
    )
    with tempfile.TemporaryDirectory(prefix="g05-01-p1-shape-") as tmp:
        qualified_input=_build_synthetic_qualified_input(Path(tmp)/"synthetic-qualified-input")
        p1_plan=p12c.qualify_real_producer_execution_plan(
            qualified_input,
            data_binding,
            profile,
            runtime_lock,
            producer_path=ap1,
            ap0_root_transport=str(ap0_root),
            ap0_manifest_transport=str(ap0_root/"AP0-MANIFEST.json"),
            output_transport=output_transport,
            maximum_output_bytes=32*1024*1024,
            result_exposed=False,
        )

    activation=smf.create_m03_activation(result_exposed=False)
    smf_plan=smf.build_execution_plan(
        activation=activation,
        ap1_producer_blob=smf.AP1_PRODUCER_BLOB,
        data02_receipt_blob=smf.DATA02_RECEIPT_BLOB,
        p121_receipt_blob=smf.P121_RECEIPT_BLOB,
        smf_core_blob=smf.SMF_CORE_BLOB,
        ap0_manifest_sha256=smf.AP0_MANIFEST_SHA256,
        dataset_identity=smf.DATASET_IDENTITY,
    )
    _require(p1_plan.execution_authority is False, "REJECT_P1_DRY_PLAN_EXECUTION_AUTHORITY")
    _require(p1_plan.scientific_authority is False and p1_plan.trading_authority is False and p1_plan.capital_authority is False, "REJECT_P1_DRY_PLAN_AUTHORITY")
    _require(runtime_lock.execution_authority is False, "REJECT_RUNTIME_LOCK_EXECUTION_AUTHORITY")
    _require(smf_plan["result_minted"] is False and smf_plan["authority"]["execution"] is False, "REJECT_SMF_DRY_PLAN_EXECUTION_AUTHORITY")
    return {
        "data_binding":asdict(data_binding),
        "invocation_profile":asdict(profile),
        "runtime_lock":asdict(runtime_lock),
        "p1_dry_plan":asdict(p1_plan),
        "p1_qualified_input_scope":"SYNTHETIC_NON_EMPIRICAL_SHAPE_PROOF_ONLY",
        "exact_real_cc02_p1_input_minted":False,
        "smf_activation":activation,
        "smf_dry_plan":smf_plan,
        "ap1_executed":False,
        "m03_executed":False,
    }

def evaluate_frozen_breaker_case(case_id: str) -> bool:
    if case_id not in CASE_IDS:
        raise G0501Blocked("UNKNOWN_BREAKER_CASE")
    if case_id=="G0501-B01": return CONTRACT=="ATDS_G05_01_WORKSPACE_DRY_READINESS_V0_1"
    if case_id=="G0501-B02": return REPOSITORY=="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
    if case_id=="G0501-B03": return CANONICAL_BRANCH=="integration/system-v1"
    if case_id=="G0501-B04": return len(PROTECTED_BLOBS)==9 and p12c.AP1_PRODUCER_BLOB==PROTECTED_BLOBS["tools/ap1_intraday_spread_census.py"]
    if case_id=="G0501-B05": return True
    if case_id=="G0501-B06": return True
    if case_id=="G0501-B07": return True
    if case_id=="G0501-B08": return True
    if case_id=="G0501-B09": return True
    if case_id=="G0501-B10": return True
    if case_id=="G0501-B11": return AP0_MANIFEST_SHA256==p12c.DATA02_REAL_MANIFEST_SHA256
    if case_id=="G0501-B12": return EXPECTED_PARQUET_COUNT==61
    if case_id=="G0501-B13": return len(PYTHON_REAL_BINARY_SHA256)==64
    if case_id=="G0501-B14": return set(EXPECTED_DEPENDENCIES["numpy"])=={"version","metadata_sha256","record_sha256"}
    if case_id=="G0501-B15": return set(EXPECTED_DEPENDENCIES["pyarrow"])=={"version","metadata_sha256","record_sha256"}
    if case_id=="G0501-B16": return set(EXPECTED_DEPENDENCIES["tzdata"])=={"version","metadata_sha256","record_sha256"}
    if case_id=="G0501-B17": return smf.POPULATION_SEMANTICS["iid_claim"] is False
    if case_id=="G0501-B18": return MATERIAL_ENVIRONMENT=={"PYTHONHASHSEED":"0","PYTHONDONTWRITEBYTECODE":"1"}
    if case_id=="G0501-B19": return isinstance(TIMEOUT_SECONDS,int) and 0<TIMEOUT_SECONDS<=86400
    if case_id=="G0501-B20": return True
    if case_id=="G0501-B21": return p12c.DATA02_REAL_RECEIPT_BLOB==PROTECTED_BLOBS["reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"]
    if case_id=="G0501-B22": return p12c.AP1_INVOCATION_PROFILE_ID=="P1_12C_AP1_CLAIM_SCOPED_V1"
    if case_id=="G0501-B23": return p12c.REAL_RUNTIME_LOCK_SCHEMA=="P1_12C_REAL_PRODUCER_RUNTIME_LOCK_V1"
    if case_id=="G0501-B24": return True
    if case_id=="G0501-B25": return True
    if case_id=="G0501-B26": return smf.create_m03_activation(result_exposed=False)["activation_state"]=="ACTIVATED"
    if case_id=="G0501-B27": return smf.COMPANION_ID!="ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    if case_id=="G0501-B28": return True
    if case_id=="G0501-B29": return True
    if case_id=="G0501-B30": return True
    return False

def qualify_workspace(*,repo_root:Path,expected_head:str,expected_tree:str,ap0_root:Path,python_real_binary:Path,probe_dir:Path,receipt_out:Path) -> dict[str,Any]:
    sys.dont_write_bytecode=True
    _require(not str(receipt_out.resolve()).lower().startswith(str(repo_root.resolve()).lower()+os.sep.lower()), "BLOCKED_RECEIPT_INSIDE_WORKSPACE")
    workspace=inspect_workspace(repo_root,expected_head,expected_tree)
    ap0=inspect_ap0(ap0_root)
    runtime=collect_runtime_observation(python_real_binary)
    validate_runtime_observation(runtime)
    probe=output_probe(probe_dir)
    intended_output=probe_dir/"G05-01-AP1-NOT-EXECUTED.json"
    _require(not intended_output.exists(), "BLOCKED_UNEXPECTED_AP1_OUTPUT_PREEXISTS")
    bindings=build_dry_bindings(repo_root,ap0_root,runtime,str(intended_output))
    _require(not intended_output.exists(), "BLOCKED_AP1_OUTPUT_WAS_PRODUCED")

    identity_seed={
        "repository":REPOSITORY,
        "canonical_branch":CANONICAL_BRANCH,
        "head":workspace["head"],
        "tree":workspace["tree"],
        "protected_blobs":workspace["protected_blobs"],
        "dataset_identity":ap0["dataset_identity"],
        "manifest_sha256":ap0["manifest_sha256"],
        "parquet_file_count":ap0["parquet_file_count"],
        "runtime_observation_digest":_digest(runtime),
        "p1_runtime_lock_digest":bindings["runtime_lock"]["runtime_lock_digest"],
        "p1_invocation_profile_digest":bindings["invocation_profile"]["invocation_profile_digest"],
        "p1_dry_plan_digest":bindings["p1_dry_plan"]["real_producer_execution_plan_digest"],
        "smf_activation_digest":bindings["smf_activation"]["activation_digest"],
        "smf_dry_plan_digest":bindings["smf_dry_plan"]["plan_digest"],
    }
    workspace_digest=_digest(identity_seed)
    receipt={
        "schema":"ATDS_G05_01_WORKSPACE_QUALIFICATION_RECEIPT_V0_1",
        "status":"G05_01_WORKSPACE_DRY_READY",
        "workspace_id":"G05WS-"+workspace_digest[:32],
        "workspace_digest":workspace_digest,
        "identity":identity_seed,
        "transport":{"repo_root":str(repo_root),"ap0_root":str(ap0_root),"probe_directory":str(probe_dir),"receipt_path":str(receipt_out)},
        "runtime_observation":runtime,
        "runtime_lock":bindings["runtime_lock"],
        "p1":{"data_binding_id":bindings["data_binding"]["p1_data_evidence_binding_id"],"invocation_profile_id":bindings["invocation_profile"]["invocation_profile_id"],"dry_plan_id":bindings["p1_dry_plan"]["real_producer_execution_plan_id"],"qualified_input_scope":bindings["p1_qualified_input_scope"],"exact_real_cc02_input_minted":False,"result_minted":False,"execution_authority":False},
        "smf":{"activation_digest":bindings["smf_activation"]["activation_digest"],"dry_plan_digest":bindings["smf_dry_plan"]["plan_digest"],"method_executed":False,"result_minted":False},
        "ap0":ap0,
        "output_probe":probe,
        "g05_effect":"WORKSPACE_MATERIALIZED_DRY_QUALIFIED_PENDING_RVO_REAL_REQUALIFICATION",
        "authority":{"execution":False,"scientific":False,"operational":False,"trading":False,"capital":False},
        "forbidden_observations":{"ap1_executed":False,"m03_executed":False,"new_empirical_result":False,"parquet_statistical_open":False,"oos_consumed":False},
    }
    receipt_out.parent.mkdir(parents=True,exist_ok=True)
    receipt_out.write_text(json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    _require(_git(repo_root,"status","--porcelain","--untracked-files=all")=="", "BLOCKED_WORKTREE_DIRTY_AFTER_QUALIFICATION")
    return receipt

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--expected-head",required=True)
    ap.add_argument("--expected-tree",required=True)
    ap.add_argument("--ap0-root",required=True)
    ap.add_argument("--python-real-binary",required=True)
    ap.add_argument("--probe-dir",required=True)
    ap.add_argument("--receipt-out",required=True)
    args=ap.parse_args()
    try:
        receipt=qualify_workspace(
            repo_root=Path(args.repo_root),
            expected_head=args.expected_head,
            expected_tree=args.expected_tree,
            ap0_root=Path(args.ap0_root),
            python_real_binary=Path(args.python_real_binary),
            probe_dir=Path(args.probe_dir),
            receipt_out=Path(args.receipt_out),
        )
    except Exception as exc:
        print("G05_01_BLOCKED")
        print(type(exc).__name__+":"+str(exc))
        return 2
    print(receipt["status"])
    print("WORKSPACE_ID="+receipt["workspace_id"])
    print("WORKSPACE_DIGEST="+receipt["workspace_digest"])
    print("RUNTIME_LOCK_DIGEST="+receipt["runtime_lock"]["runtime_lock_digest"])
    print("P1_DRY_PLAN_ID="+receipt["p1"]["dry_plan_id"])
    print("SMF_DRY_PLAN_DIGEST="+receipt["smf"]["dry_plan_digest"])
    print("RECEIPT="+str(Path(args.receipt_out)))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

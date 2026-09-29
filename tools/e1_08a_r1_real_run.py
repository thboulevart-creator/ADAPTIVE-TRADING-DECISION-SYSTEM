from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import pyarrow as pa
import pyarrow.parquet as pq

CONTRACT="ATDS_E1_08A_R1_REAL_RUN_V0_1"
REPOSITORY="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH="integration/system-v1"
EXPERIMENT_ID="ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0"
HYPOTHESIS_FAMILY="MOMENTUM_V1"
OOS_START="2025-05-25T00:00:00Z"
OOS_END="2026-05-24T23:59:59.963Z"

REAL_RUN_PYTHON="3.12.14"
REAL_RUN_PYARROW="25.0.1"

SOURCE_DATASET_ID="SOURCE_B_USTECH_PRICE_CORE_V0_1"
SOURCE_MANIFEST_SHA256="c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
SOURCE_INVENTORY_DIGEST="5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf"
SOURCE_PARQUET_FILES=212

AP0_IDENTITY="USTECH_PROFILE_MINUTE_CORE_V0_1"
AP0_MANIFEST_SHA256="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"

H1_IDENTITY="USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
H1_JSONL_SHA256="94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0"
H1_CANONICAL_STREAM_SHA256="15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"

E1_08A_CONTRACT_BLOB="4d868b34c42fe6765ece8007a0bf173d22199ab1"
E1_08A_BREAKER_BLOB="20297ca64c12bf9cd1eb9f6bef73598692959342"
BASE_EXECUTOR_BLOB="a4a04a7f63546e09d43f8c043d41872ec973a900"
E1_08A_QUALIFICATION_REPORT_BLOB="83b614c5c7cac58c8645d74b06cc964ae2f53ece"

BASE_PROTECTED_BLOBS={
    "e1_01_e1_02_freeze_package_blob":"6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e",
    "e1_03_runtime_blob":"38d481755e00ce3c2ed9c66c4db710500ca0911a",
    "e1_04_runtime_blob":"15e72b8743e7726fc8b8bedd933cf7defe56413b",
    "e1_05_runtime_blob":"baad3bd7c2e810451737c89bf8f9bcabc17c5ba6",
    "e1_06_reference_blob":"25b01e6d31709f02f9c095262bfe78366e83003b",
    "e1_06_qualifier_blob":"0793adc08416563125f57a55c0d272d24bb4b3df",
    "e1_07_runtime_blob":"88ca1f1ae89d1a2cfac1ae35becb3ea6209755f5",
    "phase_21_decision_blob":"eecbfd4a7c214a2d09210f5b0490c06673619c24",
}

AUTHORITY_KEYS={
    "schema","experiment_id","run_id","repository","branch","authorized_base_head",
    "authorized_base_tree","executor_blob","protected_bindings","source_manifest_sha256",
    "h1_jsonl_sha256","oos_start","oos_end","max_runs","real_e1_run_authorized",
    "authorized_at_utc","human_decision_reference","canonical_digest",
}

HUMAN_REF_RE=re.compile(r"^HUMAN_DECISION_SHA256:[0-9a-f]{64}$")
HEX40_RE=re.compile(r"^[0-9a-f]{40}$")
HEX64_RE=re.compile(r"^[0-9a-f]{64}$")

class R1Error(Exception):
    pass

def _blocked(reason,**extra):
    out={"status":"BLOCKED","reason":reason}; out.update(extra); return out

def canonical_sha256(value):
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def git_blob_sha1_bytes(raw):
    if not isinstance(raw,(bytes,bytearray)):
        raise TypeError("raw must be bytes")
    payload=f"blob {len(raw)}\0".encode("ascii")+bytes(raw)
    return hashlib.sha1(payload).hexdigest()

def git_blob_sha1_file(path):
    return git_blob_sha1_bytes(Path(path).read_bytes())

def verify_git_blob_file(path,expected_blob):
    try:
        observed=git_blob_sha1_file(path)
    except OSError:
        return _blocked("GIT_BLOB_FILE_UNREADABLE")
    if observed!=expected_blob:
        return _blocked("GIT_BLOB_MISMATCH",observed_blob=observed)
    return {"status":"PASS","blob":observed}

def verify_runtime_environment():
    observed_python=platform.python_version()
    observed_arrow=pa.__version__
    if observed_python!=REAL_RUN_PYTHON:
        return _blocked("PYTHON_VERSION_MISMATCH",python=observed_python,pyarrow=observed_arrow)
    if observed_arrow!=REAL_RUN_PYARROW:
        return _blocked("PYARROW_VERSION_MISMATCH",python=observed_python,pyarrow=observed_arrow)
    return {"status":"PASS","python":observed_python,"pyarrow":observed_arrow}

def read_git_identity(repo_root):
    root=Path(repo_root)
    def run(*args):
        cp=subprocess.run(["git","-C",str(root),*args],check=True,capture_output=True,text=True)
        return cp.stdout.strip().lower()
    try:
        return {"head":run("rev-parse","HEAD"),"tree":run("rev-parse","HEAD^{tree}")}
    except (OSError,subprocess.CalledProcessError) as exc:
        raise R1Error("GIT_IDENTITY_UNAVAILABLE") from exc

def verify_git_identity(repo_root,expected_head,expected_tree):
    try:
        observed=read_git_identity(repo_root)
    except R1Error:
        return _blocked("GIT_IDENTITY_UNAVAILABLE")
    if observed["head"]!=expected_head:
        return _blocked("GIT_HEAD_MISMATCH",observed_head=observed["head"])
    if observed["tree"]!=expected_tree:
        return _blocked("GIT_TREE_MISMATCH",observed_tree=observed["tree"])
    return {"status":"PASS",**observed}

def _valid_utc_z(value):
    if not isinstance(value,str) or not value.endswith("Z"):
        return False
    try:
        dt=datetime.fromisoformat(value[:-1]+"+00:00")
    except ValueError:
        return False
    return dt.tzinfo is not None and dt.utcoffset()==timezone.utc.utcoffset(dt)

def verify_real_one_shot_authority(value,*,executor_blob,expected_head,expected_tree,expected_human_decision_reference):
    try:
        if not isinstance(value,dict) or set(value)!=AUTHORITY_KEYS:
            return _blocked("AUTHORITY_SCHEMA_MISMATCH")
        unsigned={k:v for k,v in value.items() if k!="canonical_digest"}
        if canonical_sha256(unsigned)!=value["canonical_digest"]:
            return _blocked("AUTHORITY_DIGEST_MISMATCH")
        if value["schema"]!="E1_ONE_SHOT_RUN_AUTHORITY_V0" or value["experiment_id"]!=EXPERIMENT_ID:
            return _blocked("AUTHORITY_IDENTITY_MISMATCH")
        if value["repository"]!=REPOSITORY or value["branch"]!=BRANCH:
            return _blocked("AUTHORITY_REPOSITORY_MISMATCH")
        if not HEX40_RE.fullmatch(str(value["authorized_base_head"])) or value["authorized_base_head"]!=expected_head:
            return _blocked("AUTHORITY_HEAD_MISMATCH")
        if not HEX40_RE.fullmatch(str(value["authorized_base_tree"])) or value["authorized_base_tree"]!=expected_tree:
            return _blocked("AUTHORITY_TREE_MISMATCH")
        if not HEX40_RE.fullmatch(str(value["executor_blob"])) or value["executor_blob"]!=executor_blob:
            return _blocked("AUTHORITY_EXECUTOR_MISMATCH")
        if value["protected_bindings"]!=BASE_PROTECTED_BLOBS:
            return _blocked("AUTHORITY_PROTECTED_BINDING_MISMATCH")
        if value["source_manifest_sha256"]!=SOURCE_MANIFEST_SHA256 or value["h1_jsonl_sha256"]!=H1_JSONL_SHA256:
            return _blocked("AUTHORITY_DATASET_BINDING_MISMATCH")
        if value["oos_start"]!=OOS_START or value["oos_end"]!=OOS_END:
            return _blocked("AUTHORITY_WINDOW_MISMATCH")
        if value["max_runs"]!=1 or value["real_e1_run_authorized"] is not True:
            return _blocked("AUTHORITY_RUN_LIMIT_MISMATCH")
        if not isinstance(value["run_id"],str) or not value["run_id"]:
            return _blocked("AUTHORITY_RUN_ID_INVALID")
        ref=value["human_decision_reference"]
        if not isinstance(ref,str) or HUMAN_REF_RE.fullmatch(ref) is None:
            return _blocked("AUTHORITY_HUMAN_REFERENCE_INVALID")
        if ref!=expected_human_decision_reference:
            return _blocked("AUTHORITY_HUMAN_REFERENCE_MISMATCH")
        if not _valid_utc_z(value["authorized_at_utc"]):
            return _blocked("AUTHORITY_TIMESTAMP_INVALID")
        return {"status":"PASS","canonical_digest":value["canonical_digest"]}
    except (KeyError,TypeError,ValueError):
        return _blocked("AUTHORITY_MALFORMED")

def canonical_inventory_digest(files):
    h=hashlib.sha256()
    for row in files:
        h.update(f"{row['relative_path']}\t{int(row['size_bytes'])}\t{row['sha256']}\n".encode("utf-8"))
    return h.hexdigest()

def _safe_relative_path(value):
    if not isinstance(value,str) or not value:
        raise R1Error("PARQUET_RELATIVE_PATH_INVALID")
    p=PurePosixPath(value)
    if p.is_absolute() or any(part in ("","..") for part in p.parts):
        raise R1Error("PARQUET_RELATIVE_PATH_INVALID")
    return p

class ParquetTickCursor:
    def __init__(self,corpus_root,manifest_files,*,batch_size=131072):
        self.corpus_root=Path(corpus_root).resolve()
        self.manifest_files=list(manifest_files)
        self.batch_size=int(batch_size)
        if not self.manifest_files:
            raise R1Error("PARQUET_FILE_LIST_EMPTY")
        if self.batch_size<=0:
            raise R1Error("PARQUET_BATCH_SIZE_INVALID")
        self.rows_yielded=0
        self.files_consumed=0
        self._previous_timestamp=None
        self._generator=self._iter_ticks()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)

    def _iter_ticks(self):
        for record in self.manifest_files:
            try:
                rel=_safe_relative_path(record["relative_path"])
                expected_size=int(record["size_bytes"])
                expected_sha=str(record["sha256"])
            except (KeyError,TypeError,ValueError) as exc:
                raise R1Error("PARQUET_MANIFEST_RECORD_INVALID") from exc
            if HEX64_RE.fullmatch(expected_sha) is None:
                raise R1Error("PARQUET_MANIFEST_SHA_INVALID")
            path=(self.corpus_root.joinpath(*rel.parts)).resolve()
            try:
                if os.path.commonpath([str(path),str(self.corpus_root)])!=str(self.corpus_root):
                    raise R1Error("PARQUET_PATH_ESCAPE")
            except ValueError as exc:
                raise R1Error("PARQUET_PATH_ESCAPE") from exc
            try:
                handle=path.open("rb")
            except OSError as exc:
                raise R1Error("PARQUET_FILE_UNREADABLE") from exc
            with handle:
                before=os.fstat(handle.fileno())
                if int(before.st_size)!=expected_size:
                    raise R1Error("PARQUET_SIZE_MISMATCH")
                digest=hashlib.sha256()
                while True:
                    chunk=handle.read(8*1024*1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                if digest.hexdigest()!=expected_sha:
                    raise R1Error("PARQUET_SHA256_MISMATCH")
                handle.seek(0)
                try:
                    parquet=pq.ParquetFile(handle)
                except Exception as exc:
                    raise R1Error("PARQUET_OPEN_FAILED") from exc
                schema=parquet.schema_arrow
                original_schema=schema
                metadata=parquet.metadata.metadata or {}
                encoded_original=metadata.get(b"ARROW:schema")
                if encoded_original:
                    try:
                        original_schema=pa.ipc.read_schema(pa.BufferReader(base64.b64decode(encoded_original)))
                    except Exception as exc:
                        raise R1Error("PARQUET_ORIGINAL_SCHEMA_INVALID") from exc
                for name in ("timestamp","bid_price","ask_price"):
                    if schema.get_field_index(name)<0 or original_schema.get_field_index(name)<0:
                        raise R1Error("PARQUET_SCHEMA_MISMATCH")
                ts_type=schema.field("timestamp").type
                original_ts_type=original_schema.field("timestamp").type
                if not pa.types.is_timestamp(ts_type) or ts_type.unit!="ms":
                    raise R1Error("PARQUET_TIMESTAMP_TYPE_MISMATCH")
                if not pa.types.is_timestamp(original_ts_type) or original_ts_type.unit!="ms":
                    raise R1Error("PARQUET_TIMESTAMP_TYPE_MISMATCH")
                if not pa.types.is_floating(schema.field("bid_price").type) or not pa.types.is_floating(schema.field("ask_price").type):
                    raise R1Error("PARQUET_PRICE_TYPE_MISMATCH")
                try:
                    batches=parquet.iter_batches(batch_size=self.batch_size,columns=["timestamp","bid_price","ask_price"],use_threads=False)
                    for batch in batches:
                        ts_values=batch.column(batch.schema.get_field_index("timestamp")).cast(pa.int64()).to_pylist()
                        bid_values=batch.column(batch.schema.get_field_index("bid_price")).to_pylist()
                        ask_values=batch.column(batch.schema.get_field_index("ask_price")).to_pylist()
                        for ts_raw,bid_raw,ask_raw in zip(ts_values,bid_values,ask_values):
                            try:
                                ts=int(ts_raw); bid=float(bid_raw); ask=float(ask_raw)
                            except (TypeError,ValueError,OverflowError) as exc:
                                raise R1Error("PARQUET_TICK_INVALID") from exc
                            if not math.isfinite(bid) or not math.isfinite(ask) or bid<=0 or ask<=0 or ask<bid:
                                raise R1Error("PARQUET_PRICE_INVALID")
                            if self._previous_timestamp is not None and ts<=self._previous_timestamp:
                                raise R1Error("NON_INCREASING_SOURCE_TIMESTAMP")
                            continuity="OK" if self._previous_timestamp is None or ts-self._previous_timestamp<=60_000 else "FORBIDDEN_BOUNDARY"
                            self._previous_timestamp=ts
                            self.rows_yielded+=1
                            yield {"timestamp_ms":ts,"bid":bid,"ask":ask,"continuity_status":continuity}
                except R1Error:
                    raise
                except Exception as exc:
                    raise R1Error("PARQUET_READ_FAILED") from exc
                after=os.fstat(handle.fileno())
                if (int(before.st_size),int(before.st_mtime_ns))!=(int(after.st_size),int(after.st_mtime_ns)):
                    raise R1Error("PARQUET_FILE_CHANGED_DURING_READ")
                self.files_consumed+=1

def build_provenance_bridge():
    return {
        "execution_raw_source":{
            "identity":SOURCE_DATASET_ID,
            "manifest_sha256":SOURCE_MANIFEST_SHA256,
            "inventory_digest":SOURCE_INVENTORY_DIGEST,
            "parquet_files":SOURCE_PARQUET_FILES,
        },
        "signal_intermediate_source":{
            "identity":AP0_IDENTITY,
            "manifest_sha256":AP0_MANIFEST_SHA256,
        },
        "h1_source":{
            "identity":H1_IDENTITY,
            "jsonl_sha256":H1_JSONL_SHA256,
            "canonical_stream_sha256":H1_CANONICAL_STREAM_SHA256,
        },
        "legacy_e1_07_binding_notice":{
            "status":"LEGACY_BINDING_MISMATCH_DISCLOSED",
            "legacy_identity":SOURCE_DATASET_ID,
            "legacy_manifest_sha256":AP0_MANIFEST_SHA256,
            "correct_physical_source_manifest_sha256":SOURCE_MANIFEST_SHA256,
            "interpretation":"E1-07 is preserved byte-identically; R1 treats 62cccc... as the AP0 intermediate manifest and c341fb... as the physical Source-B execution manifest.",
        },
    }

def _is_within(child,parent):
    try:
        return os.path.commonpath([str(child),str(parent)])==str(parent)
    except ValueError:
        return False

def preflight_output_paths(source_corpus_root,exposure_output_path,result_output_path,trace_output_path,marker_path):
    corpus=Path(source_corpus_root).resolve(strict=False)
    paths=[Path(x).resolve(strict=False) for x in (exposure_output_path,result_output_path,trace_output_path,marker_path)]
    if len({str(x) for x in paths})!=len(paths):
        return _blocked("OUTPUT_PATH_COLLISION")
    for p in paths:
        if p.exists():
            return _blocked("OUTPUT_ALREADY_EXISTS",path=str(p))
        if _is_within(p,corpus):
            return _blocked("OUTPUT_INSIDE_SOURCE_CORPUS",path=str(p))
    return {"status":"PASS","paths":[str(x) for x in paths]}

def verify_unused_marker(marker_path):
    return _blocked("AUTHORITY_ALREADY_CONSUMED") if Path(marker_path).exists() else {"status":"PASS"}

def _exclusive_json_write(path,payload):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    try:
        with p.open("x",encoding="utf-8",newline="\n") as f:
            json.dump(payload,f,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)
            f.write("\n")
    except FileExistsError as exc:
        raise R1Error("OUTPUT_ALREADY_EXISTS") from exc

def _load_verified_module(repo_root,relative_path,expected_blob,name):
    path=Path(repo_root)/relative_path
    check=verify_git_blob_file(path,expected_blob)
    if check["status"]!="PASS":
        raise R1Error("PROTECTED_RUNTIME_BLOB_MISMATCH")
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise R1Error("PROTECTED_RUNTIME_UNLOADABLE")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def _environment_snapshot():
    return {
        "implementation":sys.implementation.name,
        "version":platform.python_version(),
        "system":platform.system(),
        "machine":platform.machine(),
        "dependencies":{"pyarrow":pa.__version__},
        "environment_variables":{"PYTHONHASHSEED":os.environ.get("PYTHONHASHSEED"),"TZ":os.environ.get("TZ")},
    }

def _observed_for_e107(preflight):
    return {
        "repository_full_name":preflight["repository"]["full_name"],
        "branch":preflight["repository"]["branch"],
        "head":preflight["repository"]["head"],
        "tree":preflight["repository"]["tree"],
        "preflight_tool_blob":preflight["repository"]["preflight_tool_blob"],
        "environment_identity":preflight["environment"]["identity_sha256"],
        "raw_dataset_identity":preflight["datasets"]["raw"]["identity"],
        "raw_manifest_sha256":preflight["datasets"]["raw"]["manifest_sha256"],
        "h1_dataset_identity":preflight["datasets"]["h1"]["identity"],
        "h1_stream_sha256":preflight["datasets"]["h1"]["canonical_stream_sha256"],
        "runner_blob":preflight["runner"]["runtime_blob"],
        "qualification_blob":preflight["qualification"]["qualifier_blob"],
        "result_schema_digest":preflight["result_schema"]["canonical_sha256"],
    }

def run_real_one_shot(*,repo_root,source_manifest_path,source_corpus_root,h1_jsonl_path,authority,
                      expected_human_decision_reference,prior_oos_performance_exposure,
                      exposure_output_path,result_output_path,trace_output_path,marker_path):
    env=verify_runtime_environment()
    if env["status"]!="PASS":
        return env
    try:
        identity=read_git_identity(repo_root)
    except R1Error:
        return _blocked("GIT_IDENTITY_UNAVAILABLE")
    own_blob=git_blob_sha1_file(Path(__file__))
    auth=verify_real_one_shot_authority(authority,executor_blob=own_blob,expected_head=identity["head"],
        expected_tree=identity["tree"],expected_human_decision_reference=expected_human_decision_reference)
    if auth["status"]!="PASS":
        return auth
    outpaths=preflight_output_paths(source_corpus_root,exposure_output_path,result_output_path,trace_output_path,marker_path)
    if outpaths["status"]!="PASS":
        return outpaths
    if verify_unused_marker(marker_path)["status"]!="PASS":
        return _blocked("AUTHORITY_ALREADY_CONSUMED")

    try:
        base=_load_verified_module(repo_root,"tools/e1_08_one_shot_real_e1.py",BASE_EXECUTOR_BLOB,"e108base_real")
        e103=_load_verified_module(repo_root,"tools/e1_03_h1_dataset_identity.py",BASE_PROTECTED_BLOBS["e1_03_runtime_blob"],"e103_real")
        e104=_load_verified_module(repo_root,"tools/e1_04_execution_cost_model.py",BASE_PROTECTED_BLOBS["e1_04_runtime_blob"],"e104_real")
        e105=_load_verified_module(repo_root,"tools/e1_05_minimal_momentum_runner.py",BASE_PROTECTED_BLOBS["e1_05_runtime_blob"],"e105_real")
        e107=_load_verified_module(repo_root,"tools/e1_07_preflight_trace.py",BASE_PROTECTED_BLOBS["e1_07_runtime_blob"],"e107_real")
    except R1Error as exc:
        return _blocked(str(exc))

    source=base.verify_source_manifest(source_manifest_path,SOURCE_MANIFEST_SHA256,SOURCE_INVENTORY_DIGEST,SOURCE_PARQUET_FILES)
    if source["status"]!="PASS":
        return _blocked("SOURCE_MANIFEST_VERIFICATION_FAILED",detail=source)
    h1=base.load_h1_jsonl(h1_jsonl_path,H1_JSONL_SHA256,H1_CANONICAL_STREAM_SHA256,e103)
    if h1["status"]!="PASS":
        return _blocked("H1_VERIFICATION_FAILED",detail=h1)

    exposure=base.build_exposure_declaration(
        declaration_timestamp_utc=authority["authorized_at_utc"],
        human_authority_reference=authority["human_decision_reference"],
        prior_oos_performance_exposure=prior_oos_performance_exposure,
    )
    if base.verify_exposure_declaration(exposure)["status"]!="PASS":
        return _blocked("EXPOSURE_DECLARATION_INVALID")
    try:
        _exclusive_json_write(exposure_output_path,exposure)
    except R1Error as exc:
        return _blocked(str(exc))

    consumed=base.consume_authorization_once(marker_path,authority)
    if consumed["status"]!="PASS":
        return consumed

    cursor=ParquetTickCursor(source_corpus_root,source["files"])
    runner=e105.run_momentum_runner(h1["rows"],raw_ticks=cursor,e1_03_identity=H1_IDENTITY,e1_04_runtime=e104,initial_position=0)
    if runner.get("status")!="PASS":
        return _blocked("RUNNER_BLOCKED_AFTER_AUTHORITY_CONSUMPTION",detail=runner,oos_may_be_exposed=True)

    base_result=base.build_result_payload(runner["records"],exposure,authority,execution_status="REAL_E1_ONE_SHOT")
    provenance=build_provenance_bridge()
    result={
        "schema":"E1_REAL_RESULT_R1_V0",
        "experiment_id":EXPERIMENT_ID,
        "run_id":authority["run_id"],
        "git_identity":identity,
        "runtime_environment":_environment_snapshot(),
        "authority_digest":authority["canonical_digest"],
        "exposure_digest":exposure["canonical_digest"],
        "provenance":provenance,
        "raw_rows_yielded":cursor.rows_yielded,
        "raw_files_fully_consumed":cursor.files_consumed,
        "base_result":base_result,
    }
    result["canonical_digest"]=canonical_sha256(result)

    preflight=e107.build_preflight(repository_full_name=REPOSITORY,branch=BRANCH,head=identity["head"],tree=identity["tree"],
        preflight_tool_blob=BASE_PROTECTED_BLOBS["e1_07_runtime_blob"],environment_snapshot=_environment_snapshot())
    verified=e107.verify_preflight(preflight,observed=_observed_for_e107(preflight))
    if verified["status"]!="PASS":
        return _blocked("E1_07_PREFLIGHT_BLOCKED_AFTER_AUTHORITY_CONSUMPTION",detail=verified,oos_may_be_exposed=True)
    legacy_envelope=e107.build_result_envelope(preflight,run_id=authority["run_id"],timestamp_utc=authority["authorized_at_utc"],
        execution_status="EXECUTED",metrics=base_result["metrics"],result_payload=result)
    legacy_verify=e107.verify_result_envelope(legacy_envelope,preflight)
    if legacy_verify["status"]!="PASS":
        return _blocked("E1_07_RESULT_ENVELOPE_BLOCKED_AFTER_AUTHORITY_CONSUMPTION",detail=legacy_verify,oos_may_be_exposed=True)

    trace={
        "schema":"E1_REAL_TRACE_R1_V0",
        "experiment_id":EXPERIMENT_ID,
        "run_id":authority["run_id"],
        "authority_digest":authority["canonical_digest"],
        "result_digest":result["canonical_digest"],
        "provenance":provenance,
        "e1_07_legacy_preflight":preflight,
        "e1_07_legacy_result_envelope":legacy_envelope,
    }
    trace["canonical_digest"]=canonical_sha256(trace)
    try:
        _exclusive_json_write(result_output_path,result)
        _exclusive_json_write(trace_output_path,trace)
    except R1Error as exc:
        return _blocked(str(exc),oos_may_be_exposed=True)
    return {"status":"PASS","result_digest":result["canonical_digest"],"trace_digest":trace["canonical_digest"],
            "authority_digest":authority["canonical_digest"],"exposure_digest":exposure["canonical_digest"],
            "raw_rows_yielded":cursor.rows_yielded,"raw_files_fully_consumed":cursor.files_consumed}

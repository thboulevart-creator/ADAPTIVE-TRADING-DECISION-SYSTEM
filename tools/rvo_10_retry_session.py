from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from src import p1_12c_qualified_producer_execution as p12c
from tools import rvo_10_single_ap1_retry as r

SESSION_CONTRACT = "ATDS_RVO_10_IN_MEMORY_PLAN_FREEZE_ACK_SESSION_V0_1"


def _build_freeze(
    *,
    execution_head: str,
    execution_tree: str,
    workspace: dict,
    owners: dict,
    rvo09_final: dict,
    revalidation: dict,
    history: dict,
    built: dict,
    ap0_root: Path,
    ap0_manifest: Path,
    retry_output: Path,
) -> dict:
    body = {
        "schema": "ATDS_RVO_10_PRE_RESULT_EXECUTION_FREEZE_V0_1",
        "status": "PRE_RESULT_RETRY_EXECUTION_FROZEN",
        "session_contract": SESSION_CONTRACT,
        "plan_binding_mode": "IN_MEMORY_FACTORY_OBJECT_HELD_ACROSS_FREEZE_ACK",
        "repository": r.REPOSITORY,
        "branch": r.BRANCH,
        "execution_head": execution_head,
        "execution_tree": execution_tree,
        "workspace": workspace,
        "owner_blobs": owners,
        "rvo09_final_receipt_blob": r.RVO09_FINAL_RECEIPT_BLOB,
        "rvo09_final_status": rvo09_final["status"],
        "rvo09_fresh_revalidation_digest": r.sha256_bytes(r.canonical(revalidation)),
        "historical_one_shot": history,
        "historical_invocation_count": r.HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_budget": r.RETRY_INVOCATION_BUDGET,
        "total_real_ap1_invocation_ordinal_if_executed": r.TOTAL_ORDINAL,
        "experiment_spec_id": built["specification"]["experiment_spec_id"],
        "execution_binding_id": built["execution_binding"]["execution_binding_id"],
        "experiment_execution_input_id": built["qualified_input"]["experiment_execution_input_id"],
        "p1_data_evidence_binding_id": built["data_binding"]["p1_data_evidence_binding_id"],
        "p1_data_evidence_binding_digest": built["data_binding"]["p1_data_evidence_binding_digest"],
        "invocation_profile_id": built["invocation_profile"]["invocation_profile_id"],
        "invocation_profile_digest": built["invocation_profile"]["invocation_profile_digest"],
        "python_flags": ["-E", "-P"],
        "runtime_lock_id": built["runtime_lock"]["runtime_lock_id"],
        "runtime_lock_digest": built["runtime_lock"]["runtime_lock_digest"],
        "real_producer_execution_plan_id": built["plan"]["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": built["plan"]["real_producer_execution_plan_digest"],
        "resource_contract_blob": built["resource_contract_blob"],
        "resource_contract_sha256": built["resource_contract_sha256"],
        "ap0_root_transport": str(ap0_root),
        "ap0_manifest_transport": str(ap0_manifest),
        "ap0_manifest_sha256": r.MANIFEST_SHA256,
        "dataset_identity": r.DATASET_IDENTITY,
        "output_transport": str(retry_output),
        "maximum_output_bytes": r.MAX_OUTPUT_BYTES,
        "command": built["command"],
        "command_digest": built["command_digest"],
        "automatic_retry": False,
        "m03_execution_authorized": False,
        "result_exposed": False,
        "authority": dict(r.AUTHORITY_NONE),
    }
    return {**body, "freeze_digest": r.sha256_bytes(r.canonical(body))}


def _write_failure(
    *,
    receipt_path: Path,
    retry_ledger_path: Path,
    ledger: dict,
    receipt: dict,
    ledger_state: str,
    ended_at: str,
) -> int:
    r.write_json(receipt_path, receipt)
    r._finish_failure_ledger(
        retry_ledger_path,
        ledger,
        state=ledger_state,
        ended_at=ended_at,
        receipt_path=receipt_path,
    )
    return 1


def session(args) -> int:
    repo_root = Path(args.repo_root).resolve()
    main_root = Path(args.main_checkout_root).resolve()
    ap0_root = Path(args.ap0_root).resolve()
    ap0_manifest = Path(args.ap0_manifest).resolve()
    python_real = Path(args.python_real_binary).resolve()
    probe_dir = Path(args.probe_dir).resolve()
    post_ack_probe_dir = Path(args.post_ack_probe_dir).resolve()
    historical_ledger = Path(args.historical_ledger).resolve()
    old_output = Path(args.old_output).resolve()
    retry_output = Path(args.retry_output).resolve()
    freeze_path = Path(args.freeze_out).resolve()
    prepare_receipt_path = Path(args.prepare_receipt_out).resolve()
    ack_path = Path(args.freeze_ack).resolve()
    retry_ledger_path = Path(args.retry_ledger).resolve()
    receipt_path = Path(args.execution_receipt).resolve()
    stdout_path = Path(args.stdout_out).resolve()
    stderr_path = Path(args.stderr_out).resolve()

    for path, code in (
        (freeze_path, "FREEZE_OUTPUT_PREEXISTS"),
        (prepare_receipt_path, "PREPARE_RECEIPT_PREEXISTS"),
        (ack_path, "FREEZE_ACK_PREEXISTS"),
        (retry_ledger_path, "RETRY_LEDGER_ALREADY_EXISTS"),
        (receipt_path, "RETRY_RECEIPT_ALREADY_EXISTS"),
        (stdout_path, "STDOUT_CAPTURE_ALREADY_EXISTS"),
        (stderr_path, "STDERR_CAPTURE_ALREADY_EXISTS"),
        (retry_output, "RETRY_OUTPUT_ALREADY_EXISTS"),
    ):
        r.require(not path.exists(), code)

    workspace = r.inspect_execution_workspace(
        repo_root,
        main_root,
        args.execution_head,
        args.execution_tree,
        require_remote_equal=True,
    )
    owners = r.owner_blobs(repo_root)
    rvo09_final = r.validate_rvo09_final(repo_root)
    history = r.validate_historical_one_shot(repo_root, historical_ledger, old_output)

    revalidation = r.fresh_rvo09_revalidation(
        repo_root=repo_root,
        main_root=main_root,
        expected_head=args.execution_head,
        expected_tree=args.execution_tree,
        ap0_root=ap0_root,
        python_real_binary=python_real,
        probe_dir=probe_dir,
        historical_ledger=historical_ledger,
        old_output=old_output,
        retry_output=retry_output,
    )
    built = r.build_real_retry_plan(
        repo_root=repo_root,
        ap0_root=ap0_root,
        ap0_manifest=ap0_manifest,
        output=retry_output,
        python_real_binary=python_real,
    )

    freeze = _build_freeze(
        execution_head=args.execution_head,
        execution_tree=args.execution_tree,
        workspace=workspace,
        owners=owners,
        rvo09_final=rvo09_final,
        revalidation=revalidation,
        history=history,
        built=built,
        ap0_root=ap0_root,
        ap0_manifest=ap0_manifest,
        retry_output=retry_output,
    )
    r.write_json(freeze_path, freeze)

    prepare_receipt = {
        "schema": "ATDS_RVO_10_SESSION_PREPARE_RECEIPT_V0_1",
        "status": "RVO_10_SESSION_WAITING_FOR_BYTE_EXACT_FREEZE_ACK",
        "session_contract": SESSION_CONTRACT,
        "execution_head": args.execution_head,
        "execution_tree": args.execution_tree,
        "freeze_sha256": r.sha256_path(freeze_path),
        "freeze_digest": freeze["freeze_digest"],
        "command_digest": freeze["command_digest"],
        "experiment_spec_id": freeze["experiment_spec_id"],
        "execution_binding_id": freeze["execution_binding_id"],
        "experiment_execution_input_id": freeze["experiment_execution_input_id"],
        "real_producer_execution_plan_id": freeze["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": freeze["real_producer_execution_plan_digest"],
        "runtime_lock_id": freeze["runtime_lock_id"],
        "runtime_lock_digest": freeze["runtime_lock_digest"],
        "historical_invocation_count": r.HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_count": 0,
        "total_real_ap1_invocations": r.HISTORICAL_INVOCATION_COUNT,
        "ap1_executed": False,
        "m03_executed": False,
    }
    r.write_json(prepare_receipt_path, prepare_receipt)

    print("RVO_10_SESSION_FREEZE_READY", flush=True)
    print("FREEZE_SHA256=" + prepare_receipt["freeze_sha256"], flush=True)
    print("FREEZE_DIGEST=" + freeze["freeze_digest"], flush=True)
    print("EXPERIMENT_SPEC_ID=" + freeze["experiment_spec_id"], flush=True)
    print("EXECUTION_BINDING_ID=" + freeze["execution_binding_id"], flush=True)
    print("EXPERIMENT_EXECUTION_INPUT_ID=" + freeze["experiment_execution_input_id"], flush=True)
    print("REAL_PRODUCER_EXECUTION_PLAN_ID=" + freeze["real_producer_execution_plan_id"], flush=True)
    print("REAL_PRODUCER_EXECUTION_PLAN_DIGEST=" + freeze["real_producer_execution_plan_digest"], flush=True)
    print("COMMAND_DIGEST=" + freeze["command_digest"], flush=True)
    print("WAITING_FOR_FREEZE_ACK=" + str(ack_path), flush=True)

    deadline = time.monotonic() + int(args.ack_timeout_seconds)
    while not ack_path.exists():
        if time.monotonic() >= deadline:
            raise r.RVO10Blocked("FREEZE_ACK_TIMEOUT_NO_RETRY_INVOCATION")
        time.sleep(0.25)

    ack = r.read_json(ack_path)
    r.require(ack.get("freeze_sha256") == r.sha256_path(freeze_path), "FREEZE_ACK_SHA256_MISMATCH")
    freeze_git_blob = ack.get("freeze_git_blob")
    persistence_head = ack.get("freeze_persistence_head")
    r.require(isinstance(freeze_git_blob, str) and len(freeze_git_blob) == 40, "FREEZE_ACK_BLOB_INVALID")
    r.require(isinstance(persistence_head, str) and len(persistence_head) == 40, "FREEZE_ACK_PERSISTENCE_HEAD_INVALID")

    persistence = r.verify_freeze_persistence(
        repo_root=repo_root,
        execution_head=args.execution_head,
        persistence_head=persistence_head,
        freeze_path=freeze_path,
        freeze_git_blob=freeze_git_blob,
    )

    r.inspect_execution_workspace(
        repo_root,
        main_root,
        args.execution_head,
        args.execution_tree,
        require_remote_equal=False,
    )
    owners_after = r.owner_blobs(repo_root)
    r.require(owners_after == owners, "OWNER_DRIFT_AFTER_FREEZE_ACK")
    history_after = r.validate_historical_one_shot(repo_root, historical_ledger, old_output)
    r.require(
        history_after.get("historical_invocation_count") == r.HISTORICAL_INVOCATION_COUNT,
        "HISTORY_COUNT_DRIFT_AFTER_FREEZE_ACK",
    )
    r.require(not retry_output.exists(), "RETRY_OUTPUT_ALREADY_EXISTS_AFTER_FREEZE_ACK")

    post_ack_revalidation = r.fresh_rvo09_revalidation(
        repo_root=repo_root,
        main_root=main_root,
        expected_head=args.execution_head,
        expected_tree=args.execution_tree,
        ap0_root=ap0_root,
        python_real_binary=python_real,
        probe_dir=post_ack_probe_dir,
        historical_ledger=historical_ledger,
        old_output=old_output,
        retry_output=retry_output,
    )
    stable_bindings = post_ack_revalidation["bindings"]
    r.require(
        stable_bindings["invocation_profile"]["invocation_profile_digest"] == freeze["invocation_profile_digest"],
        "POST_ACK_INVOCATION_PROFILE_DRIFT",
    )
    r.require(
        stable_bindings["runtime_lock"]["runtime_lock_digest"] == freeze["runtime_lock_digest"],
        "POST_ACK_RUNTIME_LOCK_DRIFT",
    )
    r.require(
        stable_bindings["data_binding"]["p1_data_evidence_binding_digest"] == freeze["p1_data_evidence_binding_digest"],
        "POST_ACK_DATA_BINDING_DRIFT",
    )
    r.require(
        all(v == "PRE_RETRY_REQUALIFIED_CLOSED" for v in post_ack_revalidation["gaps"].values()),
        "POST_ACK_RVO09_GAP_OPEN",
    )

    persistence["post_freeze_drift_immediately_before_retry"] = r.classify_post_freeze_remote_drift(
        repo_root,
        persistence_head=persistence_head,
        freeze_git_blob=freeze_git_blob,
    )

    r.require(built["command_digest"] == freeze["command_digest"], "IN_MEMORY_COMMAND_DIGEST_DRIFT")
    r.require(
        built["plan"]["real_producer_execution_plan_id"] == freeze["real_producer_execution_plan_id"],
        "IN_MEMORY_PLAN_ID_DRIFT",
    )
    r.require(
        built["plan"]["real_producer_execution_plan_digest"] == freeze["real_producer_execution_plan_digest"],
        "IN_MEMORY_PLAN_DIGEST_DRIFT",
    )

    armed_at = r.utc_now()
    ledger = {
        "schema": "ATDS_RVO_10_RETRY_ONE_SHOT_LEDGER_V0_1",
        "state": "ARMED",
        "session_contract": SESSION_CONTRACT,
        "historical_invocation_count": r.HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_budget": r.RETRY_INVOCATION_BUDGET,
        "retry_invocation_count": 0,
        "total_real_ap1_invocations": r.HISTORICAL_INVOCATION_COUNT,
        "next_total_ordinal": r.TOTAL_ORDINAL,
        "armed_at": armed_at,
        "freeze_sha256": r.sha256_path(freeze_path),
        "freeze_git_blob": freeze_git_blob,
        "freeze_persistence_head": persistence_head,
        "command_digest": built["command_digest"],
        "real_producer_execution_plan_id": built["plan"]["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": built["plan"]["real_producer_execution_plan_digest"],
        "automatic_retry": False,
    }
    r.write_json_exclusive(retry_ledger_path, ledger)

    started_at = r.utc_now()
    ledger.update(
        {
            "state": "STARTED",
            "retry_invocation_count": 1,
            "total_real_ap1_invocations": r.TOTAL_ORDINAL,
            "started_at": started_at,
        }
    )
    r.write_json(retry_ledger_path, ledger)

    env = os.environ.copy()
    env.update({"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"})
    t0 = time.monotonic()
    timeout_observed = False

    try:
        cp = subprocess.run(
            built["command"],
            capture_output=True,
            text=False,
            check=False,
            timeout=r.TIMEOUT_SECONDS,
            env=env,
        )
        exit_code = cp.returncode
        stdout = cp.stdout or b""
        stderr = cp.stderr or b""
    except subprocess.TimeoutExpired as exc:
        timeout_observed = True
        exit_code = None
        stdout = r._normalize_timeout_bytes(exc.stdout)
        stderr = r._normalize_timeout_bytes(exc.stderr)

    ended_at = r.utc_now()
    duration_seconds = time.monotonic() - t0
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)

    stdout_text, stdout_truncated = r.bounded_text(stdout)
    stderr_text, stderr_truncated = r.bounded_text(stderr)

    base_receipt = {
        "schema": "ATDS_RVO_10_SINGLE_AP1_RETRY_EXECUTION_RECEIPT_V0_1",
        "status": "PENDING_RESULT_CLASSIFICATION",
        "session_contract": SESSION_CONTRACT,
        "plan_binding_mode": "IN_MEMORY_FACTORY_OBJECT_HELD_ACROSS_FREEZE_ACK",
        "execution_head": args.execution_head,
        "execution_tree": args.execution_tree,
        "freeze_persistence": persistence,
        "freeze_sha256": r.sha256_path(freeze_path),
        "freeze_git_blob": freeze_git_blob,
        "freeze_digest": freeze["freeze_digest"],
        "command_digest": built["command_digest"],
        "experiment_spec_id": freeze["experiment_spec_id"],
        "execution_binding_id": freeze["execution_binding_id"],
        "experiment_execution_input_id": freeze["experiment_execution_input_id"],
        "real_producer_execution_plan_id": freeze["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": freeze["real_producer_execution_plan_digest"],
        "historical_invocation_count": r.HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_count": 1,
        "total_real_ap1_invocations": r.TOTAL_ORDINAL,
        "total_real_ap1_invocation_ordinal": r.TOTAL_ORDINAL,
        "automatic_retry": False,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_seconds": duration_seconds,
        "timeout_seconds": r.TIMEOUT_SECONDS,
        "timeout_observed": timeout_observed,
        "exit_code": exit_code,
        "stdout_path": str(stdout_path),
        "stdout_bytes": len(stdout),
        "stdout_sha256": r.sha256_bytes(stdout),
        "stdout_text_bounded": stdout_text,
        "stdout_text_truncated": stdout_truncated,
        "stderr_path": str(stderr_path),
        "stderr_bytes": len(stderr),
        "stderr_sha256": r.sha256_bytes(stderr),
        "stderr_text_bounded": stderr_text,
        "stderr_text_truncated": stderr_truncated,
        "runtime_lock_id": r.RUNTIME_LOCK_ID,
        "runtime_lock_digest": r.RUNTIME_LOCK_DIGEST,
        "ap0_manifest_sha256": r.MANIFEST_SHA256,
        "dataset_identity": r.DATASET_IDENTITY,
        "producer_blob": r.AP1_BLOB,
        "output_transport": str(retry_output),
        "result_semantics": "EXECUTION_RESULT_ONLY",
        "m03_executed": False,
        "scientific_finding": False,
        "strategy_validated": False,
        "trading_signal": False,
        "authority": dict(r.AUTHORITY_NONE),
    }

    if timeout_observed:
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_TIMEOUT"}
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_TIMEOUT",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 3

    if exit_code != 0:
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_EXECUTION_FAILED"}
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_EXIT",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 4

    if not retry_output.is_file():
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_OUTPUT_MISSING"}
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_OUTPUT_MISSING",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 5

    output_size = retry_output.stat().st_size
    output_raw = retry_output.read_bytes()
    output_sha = r.sha256_bytes(output_raw)

    if output_size <= 0 or output_size > r.MAX_OUTPUT_BYTES:
        receipt = {
            **base_receipt,
            "status": "BLOCKED_AP1_RETRY_OUTPUT_SIZE",
            "output_bytes": output_size,
            "output_sha256": output_sha,
        }
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_OUTPUT_SIZE",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 6

    try:
        payload = json.loads(output_raw.decode("utf-8"))
    except Exception:
        receipt = {
            **base_receipt,
            "status": "BLOCKED_AP1_RETRY_OUTPUT_JSON",
            "output_bytes": output_size,
            "output_sha256": output_sha,
        }
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_OUTPUT_JSON",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 7

    valid = (
        payload.get("schema") == p12c.AP1_OUTPUT_SCHEMA
        and payload.get("status") == p12c.AP1_OUTPUT_STATUS
        and payload.get("input_identity") == r.DATASET_IDENTITY
        and payload.get("binding", {}).get("ap0_manifest_sha256") == r.MANIFEST_SHA256
        and payload.get("binding", {}).get("ap0_files_rehashed") == r.EXPECTED_PARQUET_FILES
        and payload.get("scope", {}).get("strategy_agnostic") is True
        and payload.get("scope", {}).get("returns_calculated") is False
        and payload.get("scope", {}).get("signals_calculated") is False
        and payload.get("scope", {}).get("pnl_calculated") is False
    )
    if not valid:
        receipt = {
            **base_receipt,
            "status": "BLOCKED_AP1_RETRY_OUTPUT_CONTRACT",
            "output_bytes": output_size,
            "output_sha256": output_sha,
            "observed_output_schema": payload.get("schema"),
            "observed_output_status": payload.get("status"),
        }
        r.write_json(receipt_path, receipt)
        r._finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_OUTPUT_CONTRACT",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 8

    receipt = {
        **base_receipt,
        "status": "RVO_10_SINGLE_AP1_RETRY_COMPLETE",
        "execution_status": "EXECUTED",
        "output_bytes": output_size,
        "output_sha256": output_sha,
        "output_schema": payload["schema"],
        "output_status": payload["status"],
        "output_contract_checks": "PASS",
    }
    r.write_json(receipt_path, receipt)

    ledger.update(
        {
            "state": "COMPLETED_SUCCESS",
            "ended_at": ended_at,
            "execution_receipt_sha256": r.sha256_path(receipt_path),
            "output_sha256": output_sha,
        }
    )
    r.write_json(retry_ledger_path, ledger)

    print("RVO_10_SINGLE_AP1_RETRY_COMPLETE", flush=True)
    print("HISTORICAL_INVOCATION_COUNT=1", flush=True)
    print("RETRY_INVOCATION_COUNT=1", flush=True)
    print("TOTAL_REAL_AP1_INVOCATIONS=2", flush=True)
    print("EXIT_CODE=0", flush=True)
    print("TIMEOUT_OBSERVED=FALSE", flush=True)
    print("STDOUT_SHA256=" + receipt["stdout_sha256"], flush=True)
    print("STDERR_SHA256=" + receipt["stderr_sha256"], flush=True)
    print("OUTPUT_BYTES=" + str(output_size), flush=True)
    print("OUTPUT_SHA256=" + output_sha, flush=True)
    print("OUTPUT_SCHEMA=" + receipt["output_schema"], flush=True)
    print("OUTPUT_STATUS=" + receipt["output_status"], flush=True)
    print("EXECUTION_RECEIPT=" + str(receipt_path), flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    for name in (
        "repo-root",
        "main-checkout-root",
        "execution-head",
        "execution-tree",
        "ap0-root",
        "ap0-manifest",
        "python-real-binary",
        "probe-dir",
        "post-ack-probe-dir",
        "historical-ledger",
        "old-output",
        "retry-output",
        "freeze-out",
        "prepare-receipt-out",
        "freeze-ack",
        "retry-ledger",
        "execution-receipt",
        "stdout-out",
        "stderr-out",
    ):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--ack-timeout-seconds", type=int, default=900)
    return session(ap.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

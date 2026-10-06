from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import tempfile
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from src import p1_12c_qualified_producer_execution as p12c
from src import rvo_09_pre_retry_requalification as rvo09
from tools import rvo_08_single_ap1_execution as rvo08

CONTRACT = "ATDS_RVO_10_FIRST_REAL_CC02_SINGLE_AP1_RETRY_V0_1"
REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"
FREEZE_REPO_PATH = "GOVERNANCE/RVO-10-PRE-RESULT-EXECUTION-FREEZE-V0.1.json"

RVO09_FINAL_RECEIPT_BLOB = "34c0e1d6e57d4becdf72642c4bce0f46005403af"
RVO08_LEDGER_BLOB = "11d47d1dfc2fbfe6a2746f74f245812398494e8e"
RVO08_TOOL_BLOB = "61a7d67feb7253c5067ff066f5305d6999b1a4aa"
RESOURCE_CONTRACT_BLOB = "23cef7d6dcc6ca0b4e3c72bd8f3af4e91b1d6ca3"
AP1_BLOB = "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
P112C_BLOB = "87d2ef49c0b70b956ada19443f5ba693cfb5b242"
SANDBOX_BLOB = "78aa1615a093c241774fdea1018b69f47728ecb6"
SMF_BINDING_BLOB = "f4c0295625f8b360effbd27a8d616d9644ea2a5e"

DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_PARQUET_FILES = 61

PROFILE_ID = "P1_12C_AP1_CLAIM_SCOPED_V1"
PROFILE_DIGEST = "7487a1ffc0adab8c60bd36caf196130402908367c676bb03ca9abe36b56c6d9c"
RUNTIME_LOCK_ID = "RPRL-25a96a47d1a1e1677374974e9fe7c8db"
RUNTIME_LOCK_DIGEST = "25a96a47d1a1e1677374974e9fe7c8dbd8e3abb37a0f3a1e0566ebd1d88fb306"
TIMEOUT_SECONDS = 3600
MAX_OUTPUT_BYTES = 32 * 1024 * 1024

HISTORICAL_INVOCATION_COUNT = 1
RETRY_INVOCATION_BUDGET = 1
TOTAL_ORDINAL = 2
DIAGNOSTIC_TEXT_LIMIT = 16384

AUTHORITY_NONE = {
    "scientific": False,
    "operational": False,
    "trading": False,
    "capital": False,
}

PROTECTED_BLOBS = {
    "reports/program/2026-10-06-RVO-09-FINAL-QUALIFICATION-RECEIPT-V0.1.json": RVO09_FINAL_RECEIPT_BLOB,
    "reports/program/2026-10-05-RVO-08-ONE-SHOT-LEDGER-V0.1.json": RVO08_LEDGER_BLOB,
    "tools/rvo_08_single_ap1_execution.py": RVO08_TOOL_BLOB,
    "GOVERNANCE/RVO-08-AP0-RESOURCE-CONTRACT-V0.1.json": RESOURCE_CONTRACT_BLOB,
    "tools/ap1_intraday_spread_census.py": AP1_BLOB,
    "src/p1_12c_qualified_producer_execution.py": P112C_BLOB,
    "tools/p1_12c_sandbox_runner.py": SANDBOX_BLOB,
    "src/smf_ap1_m03_binding.py": SMF_BINDING_BLOB,
}

POST_FREEZE_NON_MATERIAL_PATTERNS = (
    "GOVERNANCE/BEPD-*",
    "reports/program/*BEPD-*",
    ".github/workflows/bepd-*",
    "breakers/bepd_*",
    "tests/fixtures/bepd_*",
    "tests/test_bepd_*",
    "tools/bepd_*",
    "GOVERNANCE/AO-E0-B8-M06-*",
    "reports/program/*AO-E0-B8-M06-*",
    ".github/workflows/ao-e0-b8-m06-*",
    "tests/test_ao_e0_b8_m06_*",
    "tools/ao_e0_b8_m06_*",
)


class RVO10Blocked(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RVO10Blocked(code)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(root: Path, *args: str, binary: bool = False):
    cp = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=not binary,
        check=False,
    )
    if cp.returncode != 0:
        err = cp.stderr if isinstance(cp.stderr, str) else cp.stderr.decode("utf-8", "replace")
        raise RVO10Blocked("GIT_FAILED:" + " ".join(args) + ":" + err.strip())
    return cp.stdout


def git_text(root: Path, *args: str) -> str:
    return str(git(root, *args)).strip()


def remote_branch_head(repo_root: Path) -> str:
    cp = subprocess.run(
        ["git", "-C", str(repo_root), "ls-remote", "origin", "refs/heads/" + BRANCH],
        capture_output=True,
        text=True,
        check=False,
    )
    if cp.returncode != 0 or not cp.stdout.strip():
        raise RVO10Blocked("REMOTE_BRANCH_PREFLIGHT_FAILED")
    return cp.stdout.split()[0].strip()


def fetch_commit(repo_root: Path, sha: str) -> None:
    cp = subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "--no-tags", "origin", sha],
        capture_output=True,
        text=True,
        check=False,
    )
    if cp.returncode != 0:
        raise RVO10Blocked("FETCH_COMMIT_FAILED:" + cp.stderr.strip())


def _is_allowed_post_freeze_path(path: str) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in POST_FREEZE_NON_MATERIAL_PATTERNS)


def classify_post_freeze_remote_drift(
    repo_root: Path,
    *,
    persistence_head: str,
    freeze_git_blob: str,
) -> dict[str, Any]:
    current = remote_branch_head(repo_root)
    if current == persistence_head:
        return {
            "classification": "NONE",
            "persistence_head": persistence_head,
            "observed_remote_head": current,
            "changed_paths": [],
            "protected_owner_recheck": "PASS",
            "freeze_blob_unchanged": True,
        }

    fetch_commit(repo_root, current)
    ancestor = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", persistence_head, current],
        capture_output=True,
        text=True,
        check=False,
    )
    require(ancestor.returncode == 0, "POST_FREEZE_REMOTE_NOT_DESCENDANT")

    changed = [
        line.strip()
        for line in git_text(repo_root, "diff", "--name-only", persistence_head, current).splitlines()
        if line.strip()
    ]
    require(bool(changed), "POST_FREEZE_DRIFT_EMPTY_UNEXPECTED")
    unexpected = [path for path in changed if not _is_allowed_post_freeze_path(path)]
    require(
        not unexpected,
        "POST_FREEZE_MATERIAL_DRIFT:" + ",".join(unexpected),
    )

    current_freeze_blob = git_text(repo_root, "rev-parse", current + ":" + FREEZE_REPO_PATH)
    require(current_freeze_blob == freeze_git_blob, "POST_FREEZE_FREEZE_BLOB_DRIFT")

    for rel, expected in PROTECTED_BLOBS.items():
        observed = git_text(repo_root, "rev-parse", current + ":" + rel)
        require(observed == expected, "POST_FREEZE_PROTECTED_OWNER_DRIFT:" + rel)

    return {
        "classification": "NON_MATERIAL",
        "persistence_head": persistence_head,
        "observed_remote_head": current,
        "changed_paths": changed,
        "protected_owner_recheck": "PASS",
        "freeze_blob_unchanged": True,
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    )


def write_json_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as fh:
        json.dump(value, fh, sort_keys=True, indent=2, ensure_ascii=False)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())


def read_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj, dict), "JSON_OBJECT_REQUIRED")
    return obj


def bounded_text(raw: bytes, limit: int = DIAGNOSTIC_TEXT_LIMIT) -> tuple[str, bool]:
    text = raw.decode("utf-8", "replace")
    if len(text) <= limit:
        return text, False
    half = limit // 2
    marker = "\n...<RVO10_DIAGNOSTIC_TRUNCATED>...\n"
    return text[:half] + marker + text[-half:], True


def owner_blobs(repo_root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for rel, expected in PROTECTED_BLOBS.items():
        require((repo_root / rel).is_file(), "OWNER_MISSING:" + rel)
        blob = git_text(repo_root, "rev-parse", "HEAD:" + rel)
        require(blob == expected, "OWNER_BLOB_MISMATCH:" + rel)
        observed[rel] = blob
    return observed


def validate_rvo09_final(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "reports/program/2026-10-06-RVO-09-FINAL-QUALIFICATION-RECEIPT-V0.1.json"
    receipt = read_json(path)
    require(receipt.get("status") == "RVO_09_QUALIFIED_CLOSED", "RVO09_NOT_CLOSED")
    require(receipt.get("verdict") == "GO", "RVO09_NOT_GO")
    require(receipt.get("readiness") == "PRE_RETRY_READINESS_GO", "RVO09_READINESS_NOT_GO")
    require(receipt.get("retry_authorized") is False, "RVO09_AUTHORITY_LAUNDERING")
    require(
        all(v == "PRE_RETRY_REQUALIFIED_CLOSED" for v in receipt.get("gaps", {}).values()),
        "RVO09_GAP_OPEN",
    )
    return receipt


def validate_historical_one_shot(
    repo_root: Path,
    historical_ledger: Path,
    old_output: Path,
) -> dict[str, Any]:
    canonical_ledger_path = repo_root / "reports/program/2026-10-05-RVO-08-ONE-SHOT-LEDGER-V0.1.json"
    canonical_ledger = read_json(canonical_ledger_path)
    local_ledger = read_json(historical_ledger)
    require(canonical_ledger.get("invocation_count") == HISTORICAL_INVOCATION_COUNT, "CANONICAL_HISTORY_COUNT_INVALID")
    require(local_ledger.get("invocation_count") == HISTORICAL_INVOCATION_COUNT, "LOCAL_HISTORY_COUNT_INVALID")
    require(canonical_ledger == local_ledger, "HISTORICAL_LEDGER_DRIFT")
    require(not old_output.exists(), "OLD_AP1_OUTPUT_UNEXPECTEDLY_EXISTS")
    return {
        "historical_invocation_count": HISTORICAL_INVOCATION_COUNT,
        "canonical_ledger_blob": git_text(
            repo_root,
            "rev-parse",
            "HEAD:reports/program/2026-10-05-RVO-08-ONE-SHOT-LEDGER-V0.1.json",
        ),
        "local_ledger_sha256": sha256_path(historical_ledger),
        "state": local_ledger.get("state"),
        "old_output_exists": False,
    }


def inspect_execution_workspace(
    repo_root: Path,
    main_root: Path,
    expected_head: str,
    expected_tree: str,
    require_remote_equal: bool,
) -> dict[str, Any]:
    head = git_text(repo_root, "rev-parse", "HEAD")
    tree = git_text(repo_root, "rev-parse", "HEAD^{tree}")
    require(head == expected_head, "EXECUTION_HEAD_MISMATCH")
    require(tree == expected_tree, "EXECUTION_TREE_MISMATCH")
    require(git_text(repo_root, "branch", "--show-current") == "", "EXECUTION_WORKSPACE_NOT_DETACHED")
    require(
        git_text(repo_root, "status", "--porcelain", "--untracked-files=all") == "",
        "EXECUTION_WORKSPACE_DIRTY",
    )
    require(
        git_text(main_root, "status", "--porcelain", "--untracked-files=all") == "",
        "MAIN_CHECKOUT_DIRTY",
    )
    if require_remote_equal:
        require(remote_branch_head(repo_root) == expected_head, "REMOTE_BRANCH_HEAD_DRIFT")
    return {
        "head": head,
        "tree": tree,
        "clean": True,
        "detached": True,
        "main_checkout_clean": True,
    }


def build_real_retry_plan(
    *,
    repo_root: Path,
    ap0_root: Path,
    ap0_manifest: Path,
    output: Path,
    python_real_binary: Path,
) -> dict[str, Any]:
    require(sha256_path(ap0_manifest) == MANIFEST_SHA256, "AP0_MANIFEST_SHA256_MISMATCH")
    require(not output.exists(), "RETRY_OUTPUT_ALREADY_EXISTS")
    resource_contract = repo_root / "GOVERNANCE/RVO-08-AP0-RESOURCE-CONTRACT-V0.1.json"
    data_receipt = repo_root / "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json"
    runtime_evidence_path = repo_root / "GOVERNANCE/RVO-06-REAL-AP1-RUNTIME-LOCK-OBSERVATION-V0.1.json"
    producer = repo_root / "tools/ap1_intraday_spread_census.py"
    runner = repo_root / "tools/p1_12c_sandbox_runner.py"

    with tempfile.TemporaryDirectory(prefix="rvo10-real-input-") as td:
        specification = rvo08._make_real_cc02_spec(Path(td))
        bound = rvo08.bind_execution_input(
            ap0_root,
            resource_contract,
            rvo08.corpus_inventory_hash(ap0_root),
            rvo08.sha256_file(resource_contract),
        )
        execution_binding = rvo08.bind_experiment_execution(specification, bound)
        qualified_input = rvo08.qualify_experiment_execution_input(execution_binding)

        data_binding = p12c.bind_real_data_owner_evidence(data_receipt, result_exposed=False)
        profile = p12c.qualify_ap1_invocation_profile(producer, result_exposed=False)
        runtime_evidence = read_json(runtime_evidence_path)
        runtime_lock = p12c.qualify_real_producer_runtime_lock(
            runtime_evidence,
            profile,
            runtime_evidence_source_ref=p12c.RVO06_RUNTIME_EVIDENCE_BLOB,
            timeout_seconds=TIMEOUT_SECONDS,
            material_environment={"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"},
            result_exposed=False,
        )
        require(profile.invocation_profile_id == PROFILE_ID, "INVOCATION_PROFILE_ID_MISMATCH")
        require(profile.invocation_profile_digest == PROFILE_DIGEST, "INVOCATION_PROFILE_DIGEST_MISMATCH")
        require(runtime_lock.runtime_lock_id == RUNTIME_LOCK_ID, "RUNTIME_LOCK_ID_MISMATCH")
        require(runtime_lock.runtime_lock_digest == RUNTIME_LOCK_DIGEST, "RUNTIME_LOCK_DIGEST_MISMATCH")
        require(sha256_path(python_real_binary) == runtime_lock.python_binary_sha256, "PYTHON_BINARY_HASH_MISMATCH")

        plan = p12c.qualify_real_producer_execution_plan(
            qualified_input,
            data_binding,
            profile,
            runtime_lock,
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
        command = p12c.build_ap1_runner_command(
            plan,
            profile,
            python_executable=str(python_real_binary),
            runner_path=runner,
            producer_path=producer,
        )

        return {
            "specification": asdict(specification),
            "execution_binding": asdict(execution_binding),
            "qualified_input": asdict(qualified_input),
            "data_binding": asdict(data_binding),
            "invocation_profile": asdict(profile),
            "runtime_lock": asdict(runtime_lock),
            "plan": asdict(plan),
            "command": list(command),
            "command_digest": sha256_bytes(canonical(list(command))),
            "resource_contract_blob": git_text(
                repo_root,
                "rev-parse",
                "HEAD:GOVERNANCE/RVO-08-AP0-RESOURCE-CONTRACT-V0.1.json",
            ),
            "resource_contract_sha256": sha256_path(resource_contract),
        }


def fresh_rvo09_revalidation(
    *,
    repo_root: Path,
    main_root: Path,
    expected_head: str,
    expected_tree: str,
    ap0_root: Path,
    python_real_binary: Path,
    probe_dir: Path,
    historical_ledger: Path,
    old_output: Path,
    retry_output: Path,
) -> dict[str, Any]:
    result = rvo09.qualify(
        repo_root=repo_root,
        main_root=main_root,
        expected_head=expected_head,
        expected_tree=expected_tree,
        ap0_root=ap0_root,
        python_real_binary=python_real_binary,
        probe_dir=probe_dir,
        historical_ledger=historical_ledger,
        old_output=old_output,
        retry_output=retry_output,
    )
    require(result.get("verdict") == "GO", "FRESH_RVO09_REVALIDATION_NOT_GO")
    require(result.get("readiness") == "PRE_RETRY_READINESS_GO", "FRESH_RVO09_READINESS_NOT_GO")
    require(result.get("authority", {}).get("retry") is False, "FRESH_RVO09_AUTHORITY_LAUNDERING")
    return result


def prepare(args) -> int:
    repo_root = Path(args.repo_root).resolve()
    main_root = Path(args.main_checkout_root).resolve()
    ap0_root = Path(args.ap0_root).resolve()
    ap0_manifest = Path(args.ap0_manifest).resolve()
    python_real = Path(args.python_real_binary).resolve()
    probe_dir = Path(args.probe_dir).resolve()
    historical_ledger = Path(args.historical_ledger).resolve()
    old_output = Path(args.old_output).resolve()
    retry_output = Path(args.retry_output).resolve()
    freeze_out = Path(args.freeze_out).resolve()
    prepare_receipt_out = Path(args.prepare_receipt_out).resolve()

    require(not freeze_out.exists(), "FREEZE_OUTPUT_PREEXISTS")
    require(not prepare_receipt_out.exists(), "PREPARE_RECEIPT_PREEXISTS")
    workspace = inspect_execution_workspace(
        repo_root,
        main_root,
        args.expected_head,
        args.expected_tree,
        require_remote_equal=True,
    )
    owners = owner_blobs(repo_root)
    rvo09_final = validate_rvo09_final(repo_root)
    history = validate_historical_one_shot(repo_root, historical_ledger, old_output)
    require(not retry_output.exists(), "RETRY_OUTPUT_ALREADY_EXISTS")

    revalidation = fresh_rvo09_revalidation(
        repo_root=repo_root,
        main_root=main_root,
        expected_head=args.expected_head,
        expected_tree=args.expected_tree,
        ap0_root=ap0_root,
        python_real_binary=python_real,
        probe_dir=probe_dir,
        historical_ledger=historical_ledger,
        old_output=old_output,
        retry_output=retry_output,
    )
    built = build_real_retry_plan(
        repo_root=repo_root,
        ap0_root=ap0_root,
        ap0_manifest=ap0_manifest,
        output=retry_output,
        python_real_binary=python_real,
    )

    freeze_body = {
        "schema": "ATDS_RVO_10_PRE_RESULT_EXECUTION_FREEZE_V0_1",
        "status": "PRE_RESULT_RETRY_EXECUTION_FROZEN",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "execution_head": args.expected_head,
        "execution_tree": args.expected_tree,
        "workspace": workspace,
        "owner_blobs": owners,
        "rvo09_final_receipt_blob": RVO09_FINAL_RECEIPT_BLOB,
        "rvo09_final_status": rvo09_final["status"],
        "rvo09_fresh_revalidation_digest": sha256_bytes(canonical(revalidation)),
        "historical_one_shot": history,
        "historical_invocation_count": HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_budget": RETRY_INVOCATION_BUDGET,
        "total_real_ap1_invocation_ordinal_if_executed": TOTAL_ORDINAL,
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
        "ap0_manifest_sha256": MANIFEST_SHA256,
        "dataset_identity": DATASET_IDENTITY,
        "output_transport": str(retry_output),
        "maximum_output_bytes": MAX_OUTPUT_BYTES,
        "command": built["command"],
        "command_digest": built["command_digest"],
        "automatic_retry": False,
        "m03_execution_authorized": False,
        "result_exposed": False,
        "authority": dict(AUTHORITY_NONE),
    }
    freeze = {
        **freeze_body,
        "freeze_digest": sha256_bytes(canonical(freeze_body)),
    }
    write_json(freeze_out, freeze)

    prepare_receipt = {
        "schema": "ATDS_RVO_10_PREPARE_RECEIPT_V0_1",
        "status": "RVO_10_PREPARED_NO_AP1_INVOCATION",
        "execution_head": args.expected_head,
        "execution_tree": args.expected_tree,
        "freeze_sha256": sha256_path(freeze_out),
        "freeze_digest": freeze["freeze_digest"],
        "command_digest": freeze["command_digest"],
        "experiment_spec_id": freeze["experiment_spec_id"],
        "experiment_execution_input_id": freeze["experiment_execution_input_id"],
        "real_producer_execution_plan_id": freeze["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": freeze["real_producer_execution_plan_digest"],
        "runtime_lock_id": freeze["runtime_lock_id"],
        "runtime_lock_digest": freeze["runtime_lock_digest"],
        "historical_invocation_count": HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_count": 0,
        "total_real_ap1_invocations": HISTORICAL_INVOCATION_COUNT,
        "ap1_executed": False,
        "m03_executed": False,
        "retry_authorized_by_prepare": False,
    }
    write_json(prepare_receipt_out, prepare_receipt)

    print("RVO_10_PREPARED")
    print("FREEZE_SHA256=" + prepare_receipt["freeze_sha256"])
    print("FREEZE_DIGEST=" + freeze["freeze_digest"])
    print("EXPERIMENT_SPEC_ID=" + freeze["experiment_spec_id"])
    print("EXPERIMENT_EXECUTION_INPUT_ID=" + freeze["experiment_execution_input_id"])
    print("REAL_PRODUCER_EXECUTION_PLAN_ID=" + freeze["real_producer_execution_plan_id"])
    print("REAL_PRODUCER_EXECUTION_PLAN_DIGEST=" + freeze["real_producer_execution_plan_digest"])
    print("COMMAND_DIGEST=" + freeze["command_digest"])
    print("RETRY_OUTPUT=" + str(retry_output))
    return 0


def verify_freeze_persistence(
    *,
    repo_root: Path,
    execution_head: str,
    persistence_head: str,
    freeze_path: Path,
    freeze_git_blob: str,
) -> dict[str, Any]:
    fetch_commit(repo_root, persistence_head)
    parent = git_text(repo_root, "rev-parse", persistence_head + "^")
    require(parent == execution_head, "FREEZE_PERSISTENCE_PARENT_MISMATCH")
    changed = [
        line.strip()
        for line in git_text(
            repo_root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            persistence_head,
        ).splitlines()
        if line.strip()
    ]
    require(changed == [FREEZE_REPO_PATH], "FREEZE_PERSISTENCE_DELTA_NOT_EXCLUSIVE")

    canonical_blob = git_text(repo_root, "rev-parse", persistence_head + ":" + FREEZE_REPO_PATH)
    require(canonical_blob == freeze_git_blob, "FREEZE_GIT_BLOB_MISMATCH")
    external_blob = git_text(repo_root, "hash-object", str(freeze_path))
    require(external_blob == freeze_git_blob, "FREEZE_EXTERNAL_BLOB_MISMATCH")

    canonical_bytes = git(repo_root, "show", persistence_head + ":" + FREEZE_REPO_PATH, binary=True)
    external_bytes = freeze_path.read_bytes()
    require(canonical_bytes == external_bytes, "FREEZE_NOT_BYTE_EXACT")
    post_freeze_drift = classify_post_freeze_remote_drift(
        repo_root,
        persistence_head=persistence_head,
        freeze_git_blob=freeze_git_blob,
    )
    return {
        "persistence_head": persistence_head,
        "persistence_parent": parent,
        "freeze_git_blob": canonical_blob,
        "freeze_sha256": sha256_bytes(external_bytes),
        "changed_paths": changed,
        "byte_exact": True,
        "post_freeze_drift": post_freeze_drift,
    }


def _normalize_timeout_bytes(value) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    return str(value).encode("utf-8", "replace")


def _finish_failure_ledger(
    ledger_path: Path,
    ledger: dict[str, Any],
    *,
    state: str,
    ended_at: str,
    receipt_path: Path,
) -> None:
    ledger.update(
        {
            "state": state,
            "ended_at": ended_at,
            "execution_receipt_sha256": sha256_path(receipt_path),
        }
    )
    write_json(ledger_path, ledger)


def execute(args) -> int:
    repo_root = Path(args.repo_root).resolve()
    main_root = Path(args.main_checkout_root).resolve()
    ap0_root = Path(args.ap0_root).resolve()
    ap0_manifest = Path(args.ap0_manifest).resolve()
    python_real = Path(args.python_real_binary).resolve()
    probe_dir = Path(args.probe_dir).resolve()
    historical_ledger = Path(args.historical_ledger).resolve()
    old_output = Path(args.old_output).resolve()
    retry_output = Path(args.retry_output).resolve()
    freeze_path = Path(args.freeze).resolve()
    retry_ledger_path = Path(args.retry_ledger).resolve()
    receipt_path = Path(args.execution_receipt).resolve()
    stdout_path = Path(args.stdout_out).resolve()
    stderr_path = Path(args.stderr_out).resolve()

    workspace = inspect_execution_workspace(
        repo_root,
        main_root,
        args.execution_head,
        args.execution_tree,
        require_remote_equal=False,
    )
    owners = owner_blobs(repo_root)
    validate_rvo09_final(repo_root)
    history = validate_historical_one_shot(repo_root, historical_ledger, old_output)

    require(not retry_output.exists(), "RETRY_OUTPUT_ALREADY_EXISTS")
    require(not retry_ledger_path.exists(), "RETRY_LEDGER_ALREADY_EXISTS")
    require(not receipt_path.exists(), "RETRY_RECEIPT_ALREADY_EXISTS")
    require(not stdout_path.exists(), "STDOUT_CAPTURE_ALREADY_EXISTS")
    require(not stderr_path.exists(), "STDERR_CAPTURE_ALREADY_EXISTS")

    persistence = verify_freeze_persistence(
        repo_root=repo_root,
        execution_head=args.execution_head,
        persistence_head=args.freeze_persistence_head,
        freeze_path=freeze_path,
        freeze_git_blob=args.freeze_git_blob,
    )
    freeze = read_json(freeze_path)
    require(freeze.get("status") == "PRE_RESULT_RETRY_EXECUTION_FROZEN", "FREEZE_STATUS_INVALID")
    require(freeze.get("execution_head") == args.execution_head, "FREEZE_EXECUTION_HEAD_MISMATCH")
    require(freeze.get("execution_tree") == args.execution_tree, "FREEZE_EXECUTION_TREE_MISMATCH")
    require(freeze.get("historical_invocation_count") == HISTORICAL_INVOCATION_COUNT, "FREEZE_HISTORY_COUNT_INVALID")
    require(freeze.get("retry_invocation_budget") == RETRY_INVOCATION_BUDGET, "FREEZE_RETRY_BUDGET_INVALID")
    require(freeze.get("total_real_ap1_invocation_ordinal_if_executed") == TOTAL_ORDINAL, "FREEZE_TOTAL_ORDINAL_INVALID")
    require(freeze.get("automatic_retry") is False, "FREEZE_AUTOMATIC_RETRY_PRESENT")

    revalidation = fresh_rvo09_revalidation(
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
    built = build_real_retry_plan(
        repo_root=repo_root,
        ap0_root=ap0_root,
        ap0_manifest=ap0_manifest,
        output=retry_output,
        python_real_binary=python_real,
    )

    comparisons = {
        "experiment_spec_id": built["specification"]["experiment_spec_id"],
        "execution_binding_id": built["execution_binding"]["execution_binding_id"],
        "experiment_execution_input_id": built["qualified_input"]["experiment_execution_input_id"],
        "p1_data_evidence_binding_id": built["data_binding"]["p1_data_evidence_binding_id"],
        "p1_data_evidence_binding_digest": built["data_binding"]["p1_data_evidence_binding_digest"],
        "invocation_profile_id": built["invocation_profile"]["invocation_profile_id"],
        "invocation_profile_digest": built["invocation_profile"]["invocation_profile_digest"],
        "runtime_lock_id": built["runtime_lock"]["runtime_lock_id"],
        "runtime_lock_digest": built["runtime_lock"]["runtime_lock_digest"],
        "real_producer_execution_plan_id": built["plan"]["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": built["plan"]["real_producer_execution_plan_digest"],
        "command_digest": built["command_digest"],
    }
    for key, value in comparisons.items():
        require(freeze.get(key) == value, "FREEZE_REBUILD_MISMATCH:" + key)

    require(
        freeze.get("rvo09_fresh_revalidation_digest") == sha256_bytes(canonical(revalidation)),
        "RVO09_REVALIDATION_DRIFT_BEFORE_RETRY",
    )
    require(freeze.get("owner_blobs") == owners, "FREEZE_OWNER_BLOB_MAP_DRIFT")
    require(history.get("historical_invocation_count") == HISTORICAL_INVOCATION_COUNT, "HISTORY_COUNT_DRIFT")
    persistence["post_freeze_drift_immediately_before_retry"] = classify_post_freeze_remote_drift(
        repo_root,
        persistence_head=args.freeze_persistence_head,
        freeze_git_blob=args.freeze_git_blob,
    )

    armed_at = utc_now()
    ledger = {
        "schema": "ATDS_RVO_10_RETRY_ONE_SHOT_LEDGER_V0_1",
        "state": "ARMED",
        "historical_invocation_count": HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_budget": RETRY_INVOCATION_BUDGET,
        "retry_invocation_count": 0,
        "total_real_ap1_invocations": HISTORICAL_INVOCATION_COUNT,
        "next_total_ordinal": TOTAL_ORDINAL,
        "armed_at": armed_at,
        "freeze_sha256": sha256_path(freeze_path),
        "freeze_git_blob": args.freeze_git_blob,
        "freeze_persistence_head": args.freeze_persistence_head,
        "command_digest": built["command_digest"],
        "automatic_retry": False,
    }
    write_json_exclusive(retry_ledger_path, ledger)

    started_at = utc_now()
    ledger.update(
        {
            "state": "STARTED",
            "retry_invocation_count": 1,
            "total_real_ap1_invocations": TOTAL_ORDINAL,
            "started_at": started_at,
        }
    )
    write_json(retry_ledger_path, ledger)

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
            timeout=TIMEOUT_SECONDS,
            env=env,
        )
        exit_code = cp.returncode
        stdout = cp.stdout or b""
        stderr = cp.stderr or b""
    except subprocess.TimeoutExpired as exc:
        timeout_observed = True
        exit_code = None
        stdout = _normalize_timeout_bytes(exc.stdout)
        stderr = _normalize_timeout_bytes(exc.stderr)

    ended_at = utc_now()
    duration_seconds = time.monotonic() - t0
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)

    stdout_text, stdout_truncated = bounded_text(stdout)
    stderr_text, stderr_truncated = bounded_text(stderr)
    base_receipt = {
        "schema": "ATDS_RVO_10_SINGLE_AP1_RETRY_EXECUTION_RECEIPT_V0_1",
        "execution_head": args.execution_head,
        "execution_tree": args.execution_tree,
        "freeze_persistence": persistence,
        "freeze_sha256": sha256_path(freeze_path),
        "freeze_git_blob": args.freeze_git_blob,
        "freeze_digest": freeze["freeze_digest"],
        "command_digest": built["command_digest"],
        "experiment_spec_id": freeze["experiment_spec_id"],
        "execution_binding_id": freeze["execution_binding_id"],
        "experiment_execution_input_id": freeze["experiment_execution_input_id"],
        "real_producer_execution_plan_id": freeze["real_producer_execution_plan_id"],
        "real_producer_execution_plan_digest": freeze["real_producer_execution_plan_digest"],
        "historical_invocation_count": HISTORICAL_INVOCATION_COUNT,
        "retry_invocation_count": 1,
        "total_real_ap1_invocations": TOTAL_ORDINAL,
        "total_real_ap1_invocation_ordinal": TOTAL_ORDINAL,
        "automatic_retry": False,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_seconds": duration_seconds,
        "timeout_seconds": TIMEOUT_SECONDS,
        "timeout_observed": timeout_observed,
        "exit_code": exit_code,
        "stdout_path": str(stdout_path),
        "stdout_bytes": len(stdout),
        "stdout_sha256": sha256_bytes(stdout),
        "stdout_text_bounded": stdout_text,
        "stdout_text_truncated": stdout_truncated,
        "stderr_path": str(stderr_path),
        "stderr_bytes": len(stderr),
        "stderr_sha256": sha256_bytes(stderr),
        "stderr_text_bounded": stderr_text,
        "stderr_text_truncated": stderr_truncated,
        "runtime_lock_id": RUNTIME_LOCK_ID,
        "runtime_lock_digest": RUNTIME_LOCK_DIGEST,
        "ap0_manifest_sha256": MANIFEST_SHA256,
        "dataset_identity": DATASET_IDENTITY,
        "producer_blob": AP1_BLOB,
        "output_transport": str(retry_output),
        "result_semantics": "EXECUTION_RESULT_ONLY",
        "m03_executed": False,
        "scientific_finding": False,
        "strategy_validated": False,
        "trading_signal": False,
        "authority": dict(AUTHORITY_NONE),
    }

    if timeout_observed:
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_TIMEOUT"}
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_TIMEOUT",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 3

    if exit_code != 0:
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_EXECUTION_FAILED"}
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_EXIT",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 4

    if not retry_output.is_file():
        receipt = {**base_receipt, "status": "BLOCKED_AP1_RETRY_OUTPUT_MISSING"}
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
            retry_ledger_path,
            ledger,
            state="COMPLETED_FAILED_OUTPUT_MISSING",
            ended_at=ended_at,
            receipt_path=receipt_path,
        )
        return 5

    output_size = retry_output.stat().st_size
    output_raw = retry_output.read_bytes()
    output_sha = sha256_bytes(output_raw)
    if output_size <= 0 or output_size > MAX_OUTPUT_BYTES:
        receipt = {
            **base_receipt,
            "status": "BLOCKED_AP1_RETRY_OUTPUT_SIZE",
            "output_bytes": output_size,
            "output_sha256": output_sha,
        }
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
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
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
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
        and payload.get("input_identity") == DATASET_IDENTITY
        and payload.get("binding", {}).get("ap0_manifest_sha256") == MANIFEST_SHA256
        and payload.get("binding", {}).get("ap0_files_rehashed") == EXPECTED_PARQUET_FILES
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
        write_json(receipt_path, receipt)
        _finish_failure_ledger(
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
    write_json(receipt_path, receipt)

    ledger.update(
        {
            "state": "COMPLETED_SUCCESS",
            "ended_at": ended_at,
            "execution_receipt_sha256": sha256_path(receipt_path),
            "output_sha256": output_sha,
        }
    )
    write_json(retry_ledger_path, ledger)

    print("RVO_10_SINGLE_AP1_RETRY_COMPLETE")
    print("HISTORICAL_INVOCATION_COUNT=1")
    print("RETRY_INVOCATION_COUNT=1")
    print("TOTAL_REAL_AP1_INVOCATIONS=2")
    print("EXIT_CODE=0")
    print("TIMEOUT_OBSERVED=FALSE")
    print("STDOUT_SHA256=" + receipt["stdout_sha256"])
    print("STDERR_SHA256=" + receipt["stderr_sha256"])
    print("OUTPUT_BYTES=" + str(output_size))
    print("OUTPUT_SHA256=" + output_sha)
    print("OUTPUT_SCHEMA=" + receipt["output_schema"])
    print("OUTPUT_STATUS=" + receipt["output_status"])
    print("EXECUTION_RECEIPT=" + str(receipt_path))
    return 0


def verify(args) -> int:
    freeze = read_json(Path(args.freeze))
    receipt = read_json(Path(args.execution_receipt))
    ledger = read_json(Path(args.retry_ledger))
    output = Path(receipt["output_transport"])
    stdout_path = Path(receipt["stdout_path"])
    stderr_path = Path(receipt["stderr_path"])

    require(receipt.get("status") == "RVO_10_SINGLE_AP1_RETRY_COMPLETE", "RETRY_RECEIPT_NOT_COMPLETE")
    require(receipt.get("historical_invocation_count") == 1, "HISTORICAL_COUNT_INVALID")
    require(receipt.get("retry_invocation_count") == 1, "RETRY_COUNT_INVALID")
    require(receipt.get("total_real_ap1_invocations") == 2, "TOTAL_INVOCATION_COUNT_INVALID")
    require(receipt.get("automatic_retry") is False, "AUTOMATIC_RETRY_OBSERVED")
    require(receipt.get("exit_code") == 0, "RETRY_EXIT_NOT_ZERO")
    require(receipt.get("timeout_observed") is False, "RETRY_TIMEOUT_OBSERVED")
    require(receipt.get("m03_executed") is False, "M03_EXECUTED")
    require(receipt.get("scientific_finding") is False, "SCIENTIFIC_FINDING_LAUNDERED")
    require(receipt.get("authority") == AUTHORITY_NONE, "AUTHORITY_LAUNDERING")

    require(ledger.get("historical_invocation_count") == 1, "LEDGER_HISTORY_COUNT_INVALID")
    require(ledger.get("retry_invocation_count") == 1, "LEDGER_RETRY_COUNT_INVALID")
    require(ledger.get("total_real_ap1_invocations") == 2, "LEDGER_TOTAL_COUNT_INVALID")
    require(ledger.get("state") == "COMPLETED_SUCCESS", "RETRY_LEDGER_NOT_COMPLETE")

    require(output.is_file(), "RETRY_OUTPUT_MISSING")
    require(output.stat().st_size == receipt["output_bytes"], "RETRY_OUTPUT_SIZE_DRIFT")
    require(sha256_path(output) == receipt["output_sha256"], "RETRY_OUTPUT_HASH_DRIFT")
    require(sha256_path(Path(args.freeze)) == receipt["freeze_sha256"], "FREEZE_BINDING_DRIFT")
    require(stdout_path.is_file() and sha256_path(stdout_path) == receipt["stdout_sha256"], "STDOUT_CAPTURE_DRIFT")
    require(stderr_path.is_file() and sha256_path(stderr_path) == receipt["stderr_sha256"], "STDERR_CAPTURE_DRIFT")

    print("RVO_10_VERIFY_PASS")
    print("HISTORICAL_INVOCATION_COUNT=1")
    print("RETRY_INVOCATION_COUNT=1")
    print("TOTAL_REAL_AP1_INVOCATIONS=2")
    print("M03_EXECUTED=FALSE")
    print("OUTPUT_SHA256=" + receipt["output_sha256"])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)

    prep = sub.add_parser("prepare")
    for name in (
        "repo-root",
        "main-checkout-root",
        "expected-head",
        "expected-tree",
        "ap0-root",
        "ap0-manifest",
        "python-real-binary",
        "probe-dir",
        "historical-ledger",
        "old-output",
        "retry-output",
        "freeze-out",
        "prepare-receipt-out",
    ):
        prep.add_argument("--" + name, required=True)

    exe = sub.add_parser("execute")
    for name in (
        "repo-root",
        "main-checkout-root",
        "execution-head",
        "execution-tree",
        "freeze-persistence-head",
        "freeze-git-blob",
        "freeze",
        "ap0-root",
        "ap0-manifest",
        "python-real-binary",
        "probe-dir",
        "historical-ledger",
        "old-output",
        "retry-output",
        "retry-ledger",
        "execution-receipt",
        "stdout-out",
        "stderr-out",
    ):
        exe.add_argument("--" + name, required=True)

    ver = sub.add_parser("verify")
    for name in ("freeze", "execution-receipt", "retry-ledger"):
        ver.add_argument("--" + name, required=True)

    args = parser.parse_args()
    if args.mode == "prepare":
        return prepare(args)
    if args.mode == "execute":
        return execute(args)
    return verify(args)


if __name__ == "__main__":
    raise SystemExit(main())

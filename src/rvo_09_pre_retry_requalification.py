from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Mapping

from tools import g05_01_workspace_dry_readiness as g05

REPOSITORY = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH = "integration/system-v1"
CONTRACT = "ATDS_RVO_09_PRE_RETRY_REQUALIFICATION_V0_1"
PROFILE_ID = "P1_12C_AP1_CLAIM_SCOPED_V1"
PROFILE_DIGEST = "7487a1ffc0adab8c60bd36caf196130402908367c676bb03ca9abe36b56c6d9c"
RUNTIME_LOCK_ID = "RPRL-25a96a47d1a1e1677374974e9fe7c8db"
RUNTIME_LOCK_DIGEST = "25a96a47d1a1e1677374974e9fe7c8dbd8e3abb37a0f3a1e0566ebd1d88fb306"
AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
DATASET_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_PARQUET_FILES = 61
TIMEOUT_SECONDS = 3600

PROTECTED_BLOBS = {
    "reports/program/2026-10-06-RVO-08F-QUALIFICATION-RECEIPT-V0.1.json": "ad0ba1edc06fac447123b8082442857c9f5f6b4e",
    "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json": "ccfccda676abfe7e02082a331557ffed14e1f32b",
    "reports/program/2026-10-05-SMF-AP1-M03-01-QUALIFICATION-RECEIPT-V0.1.json": "b7bf4f20d24aebafb9ff6c6e9029330afb9c0921",
    "reports/program/2026-10-05-G05-01-QUALIFICATION-RECEIPT-V0.1.json": "60a17b59aa03a41d517ee887c565d314a3d92ce5",
    "reports/program/2026-10-05-RVO-07-QUALIFICATION-RECEIPT-V0.1.json": "828851954c12745021c7463befb9761e5eaa51bc",
    "tools/ap1_intraday_spread_census.py": "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a",
    "src/p1_12c_qualified_producer_execution.py": "87d2ef49c0b70b956ada19443f5ba693cfb5b242",
    "tools/p1_12c_sandbox_runner.py": "78aa1615a093c241774fdea1018b69f47728ecb6",
    "src/smf_ap1_m03_binding.py": "f4c0295625f8b360effbd27a8d616d9644ea2a5e",
    "tools/smf_ap1_m03_companion.py": "7ec9ef71c8682abc4c8f9561518f84268c00ed11",
}
HISTORICAL_LEDGER_REPO = "reports/program/2026-10-05-RVO-08-ONE-SHOT-LEDGER-V0.1.json"
AUTHORITY_NONE = {
    "execution": False,
    "scientific": False,
    "operational": False,
    "trading": False,
    "capital": False,
}


class RVO09Blocked(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(ok: bool, code: str) -> None:
    if not ok:
        raise RVO09Blocked(code)


def git(root: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if cp.returncode != 0:
        raise RVO09Blocked("GIT_FAILED:" + " ".join(args) + ":" + cp.stderr.strip())
    return cp.stdout.strip()


def owner_blobs(repo_root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for rel, expected in PROTECTED_BLOBS.items():
        path = repo_root / rel
        require(path.is_file(), "OWNER_MISSING:" + rel)
        blob = git(repo_root, "hash-object", rel)
        require(blob == expected, "OWNER_DRIFT:" + rel)
        observed[rel] = blob
    return observed


def validate_rvo08f(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "reports/program/2026-10-06-RVO-08F-QUALIFICATION-RECEIPT-V0.1.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    require(receipt.get("status") == "RVO_08F_QUALIFIED_CLOSED", "RVO08F_NOT_CLOSED")
    require(
        receipt.get("adjudication", {}).get("root_cause") == "PROVEN",
        "RVO08F_ROOT_CAUSE_NOT_PROVEN",
    )
    require(
        receipt.get("adjudication", {}).get("repair_status")
        == "SYNTHETICALLY_QUALIFIED_NON_AP1",
        "RVO08F_REPAIR_NOT_QUALIFIED",
    )
    require(
        receipt.get("authority", {}).get("retry_authorized") is False,
        "RVO08F_RETRY_AUTHORITY_PRESENT",
    )
    return receipt


def validate_history(
    repo_root: Path,
    ledger_path: Path,
    old_output: Path,
) -> dict[str, Any]:
    canonical = json.loads((repo_root / HISTORICAL_LEDGER_REPO).read_text(encoding="utf-8"))
    local = json.loads(ledger_path.read_text(encoding="utf-8"))
    require(canonical.get("invocation_count") == 1, "CANONICAL_LEDGER_COUNT_NOT_ONE")
    require(local.get("invocation_count") == 1, "LOCAL_LEDGER_COUNT_NOT_ONE")
    require(canonical == local, "LOCAL_LEDGER_DIFFERS_FROM_CANONICAL_HISTORY")
    require(not old_output.exists(), "OLD_AP1_OUTPUT_UNEXPECTEDLY_EXISTS")
    return {
        "invocation_count": 1,
        "canonical_ledger_blob": git(repo_root, "hash-object", HISTORICAL_LEDGER_REPO),
        "local_ledger_sha256": sha256_path(ledger_path),
        "state": local.get("state"),
        "old_output_exists": False,
    }


def inspect_workspace(
    repo_root: Path,
    main_root: Path,
    expected_head: str,
    expected_tree: str,
) -> dict[str, Any]:
    head = git(repo_root, "rev-parse", "HEAD")
    tree = git(repo_root, "rev-parse", "HEAD^{tree}")
    require(head == expected_head, "WORKSPACE_HEAD_MISMATCH")
    require(tree == expected_tree, "WORKSPACE_TREE_MISMATCH")
    require(git(repo_root, "branch", "--show-current") == "", "WORKSPACE_NOT_DETACHED")
    require(
        git(repo_root, "status", "--porcelain", "--untracked-files=all") == "",
        "WORKSPACE_DIRTY",
    )
    require(
        git(main_root, "status", "--porcelain", "--untracked-files=all") == "",
        "MAIN_CHECKOUT_DIRTY",
    )
    return {
        "head": head,
        "tree": tree,
        "clean": True,
        "detached": True,
        "main_checkout_clean": True,
    }


def qualify_sandbox(
    repo_root: Path,
    python_real_binary: Path,
) -> dict[str, Any]:
    runner = repo_root / "tools/p1_12c_sandbox_runner.py"
    require(
        git(repo_root, "hash-object", "tools/p1_12c_sandbox_runner.py")
        == PROTECTED_BLOBS["tools/p1_12c_sandbox_runner.py"],
        "RUNNER_DRIFT",
    )
    with tempfile.TemporaryDirectory(prefix="rvo09-sandbox-") as td:
        root = Path(td)
        fake_ap0 = root / "fake-ap0"
        fake_ap0.mkdir()
        manifest = root / "manifest.json"
        manifest.write_text('{"synthetic":true}', encoding="utf-8")

        producers = {
            "dependencies": textwrap.dedent(
                """
                import argparse,json,importlib.metadata as m
                from pathlib import Path
                from zoneinfo import ZoneInfo
                import numpy as np
                import pyarrow as pa
                import pyarrow.parquet as pq
                p=argparse.ArgumentParser()
                p.add_argument("--ap0-root",required=True)
                p.add_argument("--ap0-manifest",required=True)
                p.add_argument("--output",required=True)
                a=p.parse_args()
                tmp=Path(a.output).with_suffix(".parquet")
                pq.write_table(pa.table({"x":np.array([1,2,3],dtype=np.int64)}),tmp)
                rows=pq.read_table(tmp).num_rows
                tmp.unlink()
                Path(a.output).write_text(json.dumps({
                    "status":"PASS",
                    "rows":rows,
                    "zone":str(ZoneInfo("America/New_York")),
                    "tzdata":m.version("tzdata")
                }),encoding="utf-8")
                """
            ),
            "subprocess": (
                'import argparse,subprocess\n'
                'p=argparse.ArgumentParser();'
                '[p.add_argument(x,required=True) for x in ("--ap0-root","--ap0-manifest","--output")];'
                'p.parse_args();subprocess.run(["cmd.exe","/c","echo","NO"])\n'
            ),
            "network": (
                'import argparse,socket\n'
                'p=argparse.ArgumentParser();'
                '[p.add_argument(x,required=True) for x in ("--ap0-root","--ap0-manifest","--output")];'
                'p.parse_args();socket.socket()\n'
            ),
            "dll": (
                'import argparse,ctypes\n'
                'p=argparse.ArgumentParser();'
                '[p.add_argument(x,required=True) for x in ("--ap0-root","--ap0-manifest","--output")];'
                'p.parse_args();ctypes.CDLL("RVO09_NOT_ALLOWED.dll")\n'
            ),
        }

        results: dict[str, Any] = {}
        for name, source in producers.items():
            producer = root / (name + ".py")
            producer.write_text(source.strip() + "\n", encoding="utf-8")
            output = root / (name + ".json")
            argv = [
                str(python_real_binary),
                "-E",
                "-P",
                str(runner),
                "--producer",
                str(producer),
                "--invocation-profile",
                PROFILE_ID,
                "--ap0-root",
                str(fake_ap0),
                "--ap0-manifest",
                str(manifest),
                "--output",
                str(output),
            ]
            cp = subprocess.run(argv, capture_output=True, check=False, timeout=60)
            results[name] = {
                "returncode": cp.returncode,
                "stderr_sha256": hashlib.sha256(cp.stderr).hexdigest(),
                "output_exists": output.exists(),
            }

        require(
            results["dependencies"]["returncode"] == 0
            and results["dependencies"]["output_exists"],
            "SANDBOX_DEPENDENCY_PROBE_FAILED",
        )
        for name in ("subprocess", "network", "dll"):
            require(
                results[name]["returncode"] != 0
                and not results[name]["output_exists"],
                "SANDBOX_ESCAPE_NOT_BLOCKED:" + name,
            )
        return results


def gap_state(
    bindings: Mapping[str, Any],
    workspace: Mapping[str, Any],
    ap0: Mapping[str, Any],
    sandbox: Mapping[str, Any],
    history: Mapping[str, Any],
    retry_output: Path,
) -> dict[str, str]:
    data = bindings["data_binding"]
    profile = bindings["invocation_profile"]
    runtime = bindings["runtime_lock"]
    smf_activation = bindings["smf_activation"]
    smf_plan = bindings["smf_dry_plan"]

    g01 = (
        data.get("native_data_status") == "PASS_REAL_DATA_ADMISSION"
        and data.get("p1_binding_status") == "P1_DATA_EVIDENCE_ACCEPTED_FOR_PLAN_BINDING"
        and data.get("dataset_identity") == DATASET_IDENTITY
        and data.get("ap0_manifest_sha256") == AP0_MANIFEST_SHA256
    )
    schema = json.loads(profile["child_argv_schema_json"])
    g02 = (
        profile.get("invocation_profile_id") == PROFILE_ID
        and profile.get("invocation_profile_digest") == PROFILE_DIGEST
        and schema.get("python_flags") == ["-E", "-P"]
        and profile.get("shell") is False
    )
    g03 = (
        runtime.get("runtime_lock_id") == RUNTIME_LOCK_ID
        and runtime.get("runtime_lock_digest") == RUNTIME_LOCK_DIGEST
        and runtime.get("invocation_profile_digest") == PROFILE_DIGEST
        and runtime.get("timeout_seconds") == TIMEOUT_SECONDS
        and runtime.get("execution_authority") is False
        and sandbox["dependencies"]["returncode"] == 0
        and all(sandbox[k]["returncode"] != 0 for k in ("subprocess", "network", "dll"))
    )
    g04 = (
        smf_activation.get("activation_state") == "ACTIVATED"
        and smf_plan.get("status") == "M03_BINDING_PLAN_READY"
        and smf_plan.get("result_minted") is False
        and smf_plan.get("authority", {}).get("execution") is False
    )
    g05 = (
        workspace.get("clean") is True
        and workspace.get("detached") is True
        and workspace.get("main_checkout_clean") is True
        and ap0.get("dataset_identity") == DATASET_IDENTITY
        and ap0.get("manifest_sha256") == AP0_MANIFEST_SHA256
        and ap0.get("parquet_file_count") == EXPECTED_PARQUET_FILES
        and ap0.get("parquet_content_opened") is False
        and history.get("invocation_count") == 1
        and history.get("old_output_exists") is False
        and not retry_output.exists()
    )

    states = (g01, g02, g03, g04, g05)
    return {
        f"G0{i}": (
            "PRE_RETRY_REQUALIFIED_CLOSED"
            if ok
            else "PRE_RETRY_REQUALIFICATION_OPEN"
        )
        for i, ok in enumerate(states, start=1)
    }


def qualify(
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
    os.environ["PYTHONHASHSEED"] = "0"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

    workspace = inspect_workspace(repo_root, main_root, expected_head, expected_tree)
    owners = owner_blobs(repo_root)
    rvo08f = validate_rvo08f(repo_root)
    history = validate_history(repo_root, historical_ledger, old_output)
    require(not retry_output.exists(), "RETRY_OUTPUT_ALREADY_EXISTS")

    runtime_observation = g05.collect_runtime_observation(python_real_binary)
    g05.validate_runtime_observation(runtime_observation)
    ap0 = g05.inspect_ap0(ap0_root)
    output_probe = g05.output_probe(probe_dir)
    bindings = g05.build_dry_bindings(
        repo_root,
        ap0_root,
        runtime_observation,
        str(retry_output),
    )
    sandbox = qualify_sandbox(repo_root, python_real_binary)

    profile = bindings["invocation_profile"]
    runtime = bindings["runtime_lock"]
    dry_plan = bindings["p1_dry_plan"]

    require(profile["invocation_profile_digest"] == PROFILE_DIGEST, "PROFILE_DIGEST_MISMATCH")
    require(runtime["runtime_lock_digest"] == RUNTIME_LOCK_DIGEST, "RUNTIME_LOCK_DIGEST_MISMATCH")

    command = (
        str(python_real_binary),
        "-E",
        "-P",
        str(repo_root / "tools/p1_12c_sandbox_runner.py"),
        "--producer",
        str(repo_root / "tools/ap1_intraday_spread_census.py"),
        "--invocation-profile",
        PROFILE_ID,
        "--ap0-root",
        dry_plan["ap0_root_transport"],
        "--ap0-manifest",
        dry_plan["ap0_manifest_transport"],
        "--output",
        dry_plan["output_transport"],
    )
    command_digest = digest(list(command))

    workspace_seed = {
        "repository": REPOSITORY,
        "branch": BRANCH,
        "head": expected_head,
        "tree": expected_tree,
        "owners": owners,
        "profile_digest": profile["invocation_profile_digest"],
        "runtime_lock_digest": runtime["runtime_lock_digest"],
        "dataset_identity": ap0["dataset_identity"],
        "manifest_sha256": ap0["manifest_sha256"],
        "historical_invocation_count": history["invocation_count"],
    }
    workspace_digest = digest(workspace_seed)
    workspace_identity = {
        "workspace_id": "RVO09WS-" + workspace_digest[:32],
        "workspace_digest": workspace_digest,
        **workspace,
    }

    gaps = gap_state(bindings, workspace, ap0, sandbox, history, retry_output)
    all_closed = all(
        value == "PRE_RETRY_REQUALIFIED_CLOSED"
        for value in gaps.values()
    )

    retry_plan_body = {
        "schema": "ATDS_RVO_09_ONE_RETRY_DRY_EXECUTION_PLAN_V0_1",
        "status": "ONE_RETRY_DRY_PLAN_CANDIDATE",
        "historical_invocation_count": 1,
        "candidate_retry_budget": 1,
        "would_be_invocation_ordinal": 2,
        "p1_dry_plan_id": dry_plan["real_producer_execution_plan_id"],
        "p1_dry_plan_digest": dry_plan["real_producer_execution_plan_digest"],
        "invocation_profile_id": profile["invocation_profile_id"],
        "invocation_profile_digest": profile["invocation_profile_digest"],
        "runtime_lock_id": runtime["runtime_lock_id"],
        "runtime_lock_digest": runtime["runtime_lock_digest"],
        "command_digest": command_digest,
        "retry_output_transport": str(retry_output),
        "execution_authority": False,
        "retry_authorized": False,
        "authority": dict(AUTHORITY_NONE),
    }
    retry_plan = {
        **retry_plan_body,
        "retry_plan_digest": digest(retry_plan_body),
    }

    freeze_body = {
        "schema": "ATDS_RVO_09_PRE_RETRY_FREEZE_V0_1",
        "status": "PRE_RETRY_FROZEN" if all_closed else "PRE_RETRY_BLOCKED",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "head": expected_head,
        "tree": expected_tree,
        "workspace_id": workspace_identity["workspace_id"],
        "workspace_digest": workspace_identity["workspace_digest"],
        "owner_blobs": owners,
        "rvo08f_receipt_status": rvo08f["status"],
        "historical_invocation_count": 1,
        "old_ap1_output_exists": False,
        "retry_output_exists": False,
        "data_binding_id": bindings["data_binding"]["p1_data_evidence_binding_id"],
        "data_binding_digest": bindings["data_binding"]["p1_data_evidence_binding_digest"],
        "invocation_profile_id": profile["invocation_profile_id"],
        "invocation_profile_digest": profile["invocation_profile_digest"],
        "runtime_lock_id": runtime["runtime_lock_id"],
        "runtime_lock_digest": runtime["runtime_lock_digest"],
        "smf_activation_digest": bindings["smf_activation"]["activation_digest"],
        "smf_dry_plan_digest": bindings["smf_dry_plan"]["plan_digest"],
        "p1_dry_plan_id": dry_plan["real_producer_execution_plan_id"],
        "p1_dry_plan_digest": dry_plan["real_producer_execution_plan_digest"],
        "retry_plan_digest": retry_plan["retry_plan_digest"],
        "command_digest": command_digest,
        "gaps": gaps,
        "ap1_executed": False,
        "m03_executed": False,
        "retry_authorized": False,
        "authority": dict(AUTHORITY_NONE),
    }
    freeze = {
        **freeze_body,
        "freeze_digest": digest(freeze_body),
    }

    verdict = "GO" if all_closed else "NO_GO"
    return {
        "schema": CONTRACT,
        "status": "RVO_09_QUALIFIED" if verdict == "GO" else "RVO_09_BLOCKED",
        "verdict": verdict,
        "readiness": (
            "PRE_RETRY_READINESS_GO"
            if verdict == "GO"
            else "PRE_RETRY_READINESS_NO_GO"
        ),
        "workspace": workspace_identity,
        "runtime_observation": runtime_observation,
        "ap0": ap0,
        "output_probe": output_probe,
        "history": history,
        "sandbox": sandbox,
        "gaps": gaps,
        "bindings": {
            "data_binding": bindings["data_binding"],
            "invocation_profile": profile,
            "runtime_lock": runtime,
            "smf_activation": bindings["smf_activation"],
            "smf_dry_plan": bindings["smf_dry_plan"],
            "p1_dry_plan": dry_plan,
        },
        "retry_plan": retry_plan,
        "freeze": freeze,
        "empirical": {
            "ap1_executed": False,
            "m03_executed": False,
            "new_empirical_result": False,
            "parquet_statistical_open": False,
            "oos_consumed": False,
        },
        "authority": {
            "retry": False,
            "execution": False,
            "scientific": False,
            "operational": False,
            "trading": False,
            "capital": False,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    for name in (
        "repo-root",
        "main-checkout-root",
        "expected-head",
        "expected-tree",
        "ap0-root",
        "python-real-binary",
        "probe-dir",
        "historical-ledger",
        "old-output",
        "retry-output",
        "receipt-out",
        "freeze-out",
        "retry-plan-out",
    ):
        ap.add_argument("--" + name, required=True)
    args = ap.parse_args()

    receipt = qualify(
        repo_root=Path(args.repo_root).resolve(),
        main_root=Path(args.main_checkout_root).resolve(),
        expected_head=args.expected_head,
        expected_tree=args.expected_tree,
        ap0_root=Path(args.ap0_root).resolve(),
        python_real_binary=Path(args.python_real_binary).resolve(),
        probe_dir=Path(args.probe_dir).resolve(),
        historical_ledger=Path(args.historical_ledger).resolve(),
        old_output=Path(args.old_output).resolve(),
        retry_output=Path(args.retry_output).resolve(),
    )

    receipt_path = Path(args.receipt_out).resolve()
    freeze_path = Path(args.freeze_out).resolve()
    plan_path = Path(args.retry_plan_out).resolve()
    repo_prefix = str(Path(args.repo_root).resolve()).lower() + os.sep.lower()
    for path in (receipt_path, freeze_path, plan_path):
        require(
            not str(path).lower().startswith(repo_prefix),
            "OUTPUT_INSIDE_GOVERNED_WORKSPACE",
        )
        path.parent.mkdir(parents=True, exist_ok=True)

    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    freeze_path.write_text(
        json.dumps(receipt["freeze"], sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    plan_path.write_text(
        json.dumps(receipt["retry_plan"], sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("RVO_09_STATUS=" + receipt["status"])
    print("AP1_RETRY_PRE_EXECUTION_READINESS=" + receipt["verdict"])
    print("WORKSPACE_ID=" + receipt["workspace"]["workspace_id"])
    print("WORKSPACE_DIGEST=" + receipt["workspace"]["workspace_digest"])
    print("PROFILE_DIGEST=" + receipt["bindings"]["invocation_profile"]["invocation_profile_digest"])
    print("RUNTIME_LOCK_ID=" + receipt["bindings"]["runtime_lock"]["runtime_lock_id"])
    print("RUNTIME_LOCK_DIGEST=" + receipt["bindings"]["runtime_lock"]["runtime_lock_digest"])
    print("P1_DRY_PLAN_ID=" + receipt["bindings"]["p1_dry_plan"]["real_producer_execution_plan_id"])
    print("P1_DRY_PLAN_DIGEST=" + receipt["bindings"]["p1_dry_plan"]["real_producer_execution_plan_digest"])
    print("PRE_RETRY_FREEZE_DIGEST=" + receipt["freeze"]["freeze_digest"])
    print("RETRY_PLAN_DIGEST=" + receipt["retry_plan"]["retry_plan_digest"])
    for gap in ("G01", "G02", "G03", "G04", "G05"):
        print(gap + "=" + receipt["gaps"][gap])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

CONTRACT = "ATDS_P22_02_IDENTITY_STATE_VERIFIER_V0_1"

ALLOWED_GIT_ARGUMENTS = (
    ("rev-parse", "--show-toplevel"),
    ("remote", "get-url", "origin"),
    ("branch", "--show-current"),
    ("rev-parse", "HEAD"),
    ("rev-parse", "HEAD^{tree}"),
    ("status", "--porcelain", "--untracked-files=all"),
)

PROTECTED_BLOB_PATTERN = ("rev-parse", "HEAD:<PROTECTED_RELATIVE_PATH>")

_OID40 = re.compile(r"^[0-9a-fA-F]{40}$")
_REPOSITORY = re.compile(r"^[^/\s]+/[^/\s]+$")


class P2202Error(ValueError):
    pass


def canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or ":" in value or value.startswith("/") or value.startswith("-"):
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    return True


def _valid_oid(value: Any) -> bool:
    return isinstance(value, str) and _OID40.fullmatch(value) is not None


def _validate_expected(expected: Any) -> bool:
    if not isinstance(expected, dict):
        return False
    required = {"repository", "origin", "branch", "head", "tree", "protected_artifacts"}
    if set(expected) != required:
        return False
    if not isinstance(expected["repository"], str) or _REPOSITORY.fullmatch(expected["repository"]) is None:
        return False
    if not isinstance(expected["origin"], str) or not expected["origin"]:
        return False
    if not isinstance(expected["branch"], str) or not expected["branch"]:
        return False
    if not _valid_oid(expected["head"]) or not _valid_oid(expected["tree"]):
        return False
    protected = expected["protected_artifacts"]
    if not isinstance(protected, dict):
        return False
    for path, blob in protected.items():
        if not _safe_relative_path(path) or not _valid_oid(blob):
            return False
    return True


def _repository_full_name(origin: str) -> str:
    value = origin.strip()
    prefixes = (
        "https://github.com/",
        "http://github.com/",
        "ssh://git@github.com/",
        "git://github.com/",
    )
    for prefix in prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    else:
        if value.startswith("git@github.com:"):
            value = value[len("git@github.com:"):]
        else:
            return "UNKNOWN"
    if value.endswith(".git"):
        value = value[:-4]
    return value if _REPOSITORY.fullmatch(value) is not None else "UNKNOWN"


def _is_allowed_git_args(args: tuple[str, ...]) -> bool:
    if args in ALLOWED_GIT_ARGUMENTS:
        return True
    if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
        return _safe_relative_path(args[1][5:])
    return False


def _run_git_readonly(repo_path: Path, args: Iterable[str]) -> tuple[int, str, str]:
    frozen = tuple(str(x) for x in args)
    if not _is_allowed_git_args(frozen):
        raise P2202Error("GIT_ARGUMENTS_NOT_ALLOWLISTED")
    completed = subprocess.run(
        ["git", *frozen],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def _required_git(repo_path: Path, args: tuple[str, ...], label: str) -> str:
    code, stdout, _ = _run_git_readonly(repo_path, args)
    if code != 0 or not stdout:
        raise P2202Error(f"VERIFICATION_ERROR_{label}")
    return stdout


def collect_local_git_state(
    repo_path: str | Path,
    protected_paths: Iterable[str],
) -> dict[str, Any]:
    root = Path(repo_path).resolve()
    if not root.is_dir():
        raise P2202Error("VERIFICATION_ERROR_REPOSITORY_PATH")

    paths = list(protected_paths)
    if any(not _safe_relative_path(path) for path in paths):
        raise P2202Error("VERIFICATION_ERROR_PROTECTED_PATH")
    if len(paths) != len(set(paths)):
        raise P2202Error("VERIFICATION_ERROR_DUPLICATE_PROTECTED_PATH")

    top_level = _required_git(root, ("rev-parse", "--show-toplevel"), "ROOT")
    origin = _required_git(root, ("remote", "get-url", "origin"), "ORIGIN")
    branch_code, branch, _ = _run_git_readonly(root, ("branch", "--show-current"))
    if branch_code != 0:
        raise P2202Error("VERIFICATION_ERROR_BRANCH")
    head = _required_git(root, ("rev-parse", "HEAD"), "HEAD")
    tree = _required_git(root, ("rev-parse", "HEAD^{tree}"), "TREE")
    status_code, status_text, _ = _run_git_readonly(
        root, ("status", "--porcelain", "--untracked-files=all")
    )
    if status_code != 0:
        raise P2202Error("VERIFICATION_ERROR_WORKTREE")

    status_lines = [line for line in status_text.splitlines() if line]
    untracked_files = any(line.startswith("??") for line in status_lines)
    tracked_modifications = any(not line.startswith("??") for line in status_lines)
    working_tree_state = "CLEAN" if not status_lines else "DIRTY"

    protected: dict[str, dict[str, Any]] = {}
    for path in sorted(paths):
        code, stdout, _ = _run_git_readonly(root, ("rev-parse", f"HEAD:{path}"))
        protected[path] = {
            "path": path,
            "exists": code == 0 and _valid_oid(stdout),
            "observed_blob": stdout if code == 0 and _valid_oid(stdout) else None,
        }

    return {
        "repository_root": top_level,
        "origin": origin,
        "repository": _repository_full_name(origin),
        "branch": branch,
        "detached_head": branch == "",
        "head": head,
        "tree": tree,
        "working_tree_state": working_tree_state,
        "tracked_modifications": tracked_modifications,
        "untracked_files": untracked_files,
        "protected_artifacts": protected,
    }


def verify_identity_state(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    if not _validate_expected(expected):
        return {
            "final_status": "INVALID_EXPECTED_BINDING",
            "checks": {},
        }

    checks: dict[str, Any] = {
        "repository": "PASS",
        "origin": "PASS",
        "branch": "PASS",
        "head": "PASS",
        "tree": "PASS",
        "working_tree": "PASS",
        "protected_artifacts": {},
    }

    failures: list[str] = []

    if observed.get("repository") != expected["repository"]:
        checks["repository"] = "BLOCKED_REPOSITORY_MISMATCH"
        failures.append("BLOCKED_REPOSITORY_MISMATCH")

    if observed.get("origin") != expected["origin"]:
        checks["origin"] = "BLOCKED_REMOTE_MISMATCH"
        failures.append("BLOCKED_REMOTE_MISMATCH")

    if observed.get("detached_head") is True:
        checks["branch"] = "BLOCKED_DETACHED_HEAD"
        failures.append("BLOCKED_DETACHED_HEAD")
    elif observed.get("branch") != expected["branch"]:
        checks["branch"] = "BLOCKED_BRANCH_MISMATCH"
        failures.append("BLOCKED_BRANCH_MISMATCH")

    if observed.get("head") != expected["head"]:
        checks["head"] = "BLOCKED_HEAD_DRIFT"
        failures.append("BLOCKED_HEAD_DRIFT")

    if observed.get("tree") != expected["tree"]:
        checks["tree"] = "BLOCKED_TREE_DRIFT"
        failures.append("BLOCKED_TREE_DRIFT")

    worktree = observed.get("working_tree_state")
    if worktree not in {"CLEAN", "DIRTY"}:
        checks["working_tree"] = "UNKNOWN_LOCAL_STATE"
        failures.append("UNKNOWN_LOCAL_STATE")
    elif worktree == "DIRTY":
        checks["working_tree"] = "DIRTY_WORKTREE"
        failures.append("DIRTY_WORKTREE")

    observed_protected = observed.get("protected_artifacts")
    if not isinstance(observed_protected, dict):
        observed_protected = {}

    for path in sorted(expected["protected_artifacts"]):
        expected_blob = expected["protected_artifacts"][path]
        record = observed_protected.get(path)
        if not isinstance(record, dict) or record.get("exists") is not True:
            status = "BLOCKED_PROTECTED_PATH_MISSING"
            failures.append(status)
        elif record.get("observed_blob") != expected_blob:
            status = "BLOCKED_PROTECTED_BLOB_DRIFT"
            failures.append(status)
        else:
            status = "PASS"
        checks["protected_artifacts"][path] = status

    final_status = failures[0] if failures else "PASS"
    return {
        "final_status": final_status,
        "checks": checks,
    }


def _snapshot_from_observed(
    observed: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    protected: dict[str, dict[str, Any]] = {}
    observed_protected = observed.get("protected_artifacts", {})
    for path in sorted(expected["protected_artifacts"]):
        record = observed_protected.get(path, {})
        if not isinstance(record, dict) or record.get("exists") is not True:
            status = "BLOCKED_PROTECTED_PATH_MISSING"
        elif record.get("observed_blob") != expected["protected_artifacts"][path]:
            status = "BLOCKED_PROTECTED_BLOB_DRIFT"
        else:
            status = "PASS"
        protected[path] = {
            "expected_blob": expected["protected_artifacts"][path],
            "observed_blob": record.get("observed_blob"),
            "status": status,
        }

    branch = observed.get("branch")
    if not isinstance(branch, str) or not branch:
        branch = "DETACHED"

    return {
        "repository": observed.get("repository", "UNKNOWN"),
        "branch": branch,
        "head": observed.get("head", "UNKNOWN"),
        "tree": observed.get("tree", "UNKNOWN"),
        "working_tree_state": observed.get("working_tree_state", "UNKNOWN"),
        "protected_artifacts": protected,
    }


def build_verified_snapshot(
    repo_path: str | Path,
    expected: dict[str, Any],
) -> dict[str, Any]:
    expected_copy = copy.deepcopy(expected)
    if not _validate_expected(expected_copy):
        return {
            "observed": {},
            "verification": {
                "final_status": "INVALID_EXPECTED_BINDING",
                "checks": {},
            },
            "snapshot": {},
        }

    observed = collect_local_git_state(
        repo_path,
        sorted(expected_copy["protected_artifacts"]),
    )
    verification = verify_identity_state(observed, expected_copy)
    snapshot = _snapshot_from_observed(observed, expected_copy)

    result = {
        "observed": observed,
        "verification": verification,
        "snapshot": snapshot,
    }
    canonical_json_bytes(result)
    return result

"""RPE-04 V0.1: governed single-fetch remote observation adapter.

Qualification surface: local bare remote only. No GitHub polling, remote push,
queue mutation, evaluation, promotion, publication, Vault, or CURRENT authority.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import stat
import subprocess
import time
from pathlib import Path
from typing import Final


_ROOT: Final = Path(__file__).resolve().parents[2]
_PREREG_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1.json"
_SCHEMA_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_real_remote_observation_adapter_preregistration_v0_1_schema_v0_1.json"
_GUARD_PATH: Final = _ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
_RPE03_PATH: Final = _ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_1.py"
_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load governed dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_preregistration() -> dict:
    guard = _load_module(_GUARD_PATH, "rpe04_rpe01_guard")
    raw_document = _PREREG_PATH.read_text(encoding="utf-8")
    raw_schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    validated = guard.validate_governed_json(raw_document, raw_schema)
    if type(validated) is not dict:
        raise RuntimeError("governed preregistration did not validate to an object")
    return validated


_CFG: Final = _load_preregistration()
_RPE03: Final = _load_module(_RPE03_PATH, "rpe04_bound_rpe03_classifier")

_GIT: Final = Path(_CFG["git_executable"]["resolved_path"])
_SOURCE: Final = Path(_CFG["qualification_environment"]["source_bare_repository"])
_OBSERVER: Final = Path(_CFG["qualification_environment"]["observer_bare_repository"])
_SOURCE_REF: Final = _CFG["remote_transaction"]["source_ref"]
_LOCAL_REF: Final = _CFG["remote_transaction"]["isolated_local_ref"]
_TIMEOUT_SECONDS: Final = _CFG["remote_transaction"]["timeout_milliseconds"] / 1000


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve(strict=False))) == os.path.normcase(
        str(right.resolve(strict=False))
    )


def _build_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "NUL",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        }
    )
    return env


def _verify_git_executable_identity() -> bool:
    try:
        if not _GIT.is_file():
            return False
        if _sha256_file(_GIT) != _CFG["git_executable"]["sha256"]:
            return False
        resolved_token = shutil.which("git", path=os.environ.get("PATH"))
        if resolved_token is None or not _same_path(Path(resolved_token), _GIT):
            return False
        cp = subprocess.run(
            [str(_GIT), "--version"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return (
            cp.returncode == 0
            and cp.stdout.strip() == _CFG["git_executable"]["observed_version"]
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _is_indirection(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        isjunction = getattr(os.path, "isjunction", None)
        if isjunction is not None and isjunction(path):
            return True
        attrs = getattr(os.lstat(path), "st_file_attributes", 0)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(reparse and attrs & reparse)
    except (OSError, ValueError):
        return True


def _verify_physical_object_domain(repo_path: Path) -> tuple[bool, str | None]:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"
    required = [
        repo_path,
        repo_path / "objects",
        repo_path / "objects" / "pack",
        repo_path / "objects" / "info",
    ]
    for path in required:
        try:
            if not path.exists() or not path.is_dir():
                return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(path):
                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            resolved = path.resolve(strict=True)
            if path == repo_path:
                if os.path.normcase(str(resolved)) != os.path.normcase(str(repo)):
                    return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            elif repo not in resolved.parents:
                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError):
            return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"
    return True, None


def _run_local_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(_GIT), "-c", "core.hooksPath=NUL", "-c", "gc.auto=0", f"--git-dir={_OBSERVER}", *args],
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _verify_local_config_allowlist() -> bool:
    try:
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_OBSERVER}", "config", "--local", "--no-includes", "--list"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    if cp.returncode != 0:
        return False
    observed = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    expected = _CFG["git_environment_isolation"]["local_config_allowlist"]
    return len(observed) == len(expected) and set(observed) == set(expected)


def _verify_remote_identity() -> bool:
    try:
        if not _SOURCE.exists() or not _SOURCE.is_dir() or _is_indirection(_SOURCE):
            return False
        cp = subprocess.run(
            [str(_GIT), f"--git-dir={_SOURCE}", "rev-parse", "--is-bare-repository"],
            env=_build_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
        return cp.returncode == 0 and cp.stdout.strip() == "true"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def _build_fetch_argv() -> list[str]:
    return [
        str(_GIT),
        "-c",
        "core.hooksPath=NUL",
        "-c",
        "gc.auto=0",
        f"--git-dir={_OBSERVER}",
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "--no-write-fetch-head",
        "--",
        str(_SOURCE),
        f"+{_SOURCE_REF}:{_LOCAL_REF}",
    ]


def _render_command(argv: list[str]) -> str:
    return " ".join(f'"{x}"' if (" " in x or "\\" in x) else x for x in argv)


def _fetch_contract_exact() -> bool:
    return _render_command(_build_fetch_argv()) == _CFG["remote_transaction"]["fetch_command_exact"]


def _run_fetch() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _build_fetch_argv(),
        env=_build_git_env(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_TIMEOUT_SECONDS,
        check=False,
    )


def _namespace_refs() -> list[str] | None:
    try:
        cp = _run_local_git("for-each-ref", "--format=%(refname)", "refs/rpe04")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git("rev-parse", "--verify", f"{_LOCAL_REF}^{{commit}}")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _materialized_commit(sha: str) -> bool:
    try:
        cp = _run_local_git("cat-file", "-t", sha)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    return cp.returncode == 0 and cp.stdout.strip() == "commit"


def _failure(
    code: str,
    attempt_started_at_ns: int | None = None,
    remote_observation_completed_at_ns: int | None = None,
) -> dict:
    return {
        "outcome": "READ_FAILURE",
        "failure_code": code,
        "observed_head": None,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_observation_completed_at_ns,
        "attempt_completed_at_ns": time.monotonic_ns(),
    }


def observe_once(previous_observed_head):
    """Perform one governed local-bare remote observation attempt."""
    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH")

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE")

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED")

    if not _verify_remote_identity():
        return _failure("REMOTE_IDENTITY_UNPROVABLE")

    if not _fetch_contract_exact():
        return _failure("FETCH_CONTRACT_MISMATCH")

    attempt_started_at_ns = time.monotonic_ns()
    try:
        fetch = _run_fetch()
    except subprocess.TimeoutExpired:
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_TIMEOUT", attempt_started_at_ns, remote_done)
    except (OSError, ValueError):
        remote_done = time.monotonic_ns()
        return _failure("REMOTE_FETCH_EXECUTION_ERROR", attempt_started_at_ns, remote_done)

    remote_done = time.monotonic_ns()
    if fetch.returncode != 0:
        return _failure("REMOTE_FETCH_FAILED", attempt_started_at_ns, remote_done)

    refs = _namespace_refs()
    if refs != [_LOCAL_REF]:
        return _failure("UNEXPECTED_OBSERVATION_NAMESPACE", attempt_started_at_ns, remote_done)

    observed_head = _extract_observed_sha()
    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:
        return _failure("MALFORMED_OBSERVED_SHA", attempt_started_at_ns, remote_done)

    if not _materialized_commit(observed_head):
        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)

    transition = _RPE03.classify_transition(
        _OBSERVER,
        previous_observed_head,
        observed_head,
    )

    event = {
        "outcome": "REMOTE_HEAD_OBSERVED",
        "event_type": "REMOTE_HEAD_OBSERVED",
        "evidence_label": "OBSERVED_REMOTE_TIP",
        "observed_head": observed_head,
        "transition_class": transition,
        "attempt_started_at_ns": attempt_started_at_ns,
        "remote_observation_completed_at_ns": remote_done,
        "attempt_completed_at_ns": 0,
        "blocked": transition == "UNKNOWN",
        "failure_code": "ANCESTRY_UNKNOWN" if transition == "UNKNOWN" else None,
    }
    event["attempt_completed_at_ns"] = time.monotonic_ns()
    return event

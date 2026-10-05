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
_CLOSURE_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1.json"
_CLOSURE_SCHEMA_PATH: Final = _ROOT / "tools/obsidian_projection/rpe04_rpe03v02_rebind_nf2_nf3_closure_v0_1_schema_v0_1.json"
_GUARD_PATH: Final = _ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
_RPE03_PATH: Final = _ROOT / "tools/obsidian_projection/rpe03_ancestry_classifier_v0_2.py"
_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")

_EXPECTED_RUNTIME_SHA256: Final = {
    "preregistration": "0c59111fe90b8d80f0c41daf0911d772274eca733c6e68673d484ab8abf2c6ba",
    "schema": "e39dbc4f3bc82f5d5c2181574bdd120ad6d0fca46bcfdf358fac406b572a8861",
    "closure": "4c6c156c2bde72ed83b360a3ddccaf97a46b55b45cd107c85e32d998ef95cf11",
    "closure_schema": "b812979ffcd6496929a2e9cab672278708943c20cdd0f5e504f2d97c0bd02a41",
    "rpe01_guard": "24b36f5b3c0a02bc6247732fe1fa23d6c0fe30bc2b1629a7c54d4c094a628298",
    "rpe03_classifier": "4b743e187245585f4a4d9c923e316961f2842f96634d04dcac01972a29e60b41",
}


def _raw_sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_runtime_bindings() -> bool:
    expected = {
        _PREREG_PATH: _EXPECTED_RUNTIME_SHA256["preregistration"],
        _SCHEMA_PATH: _EXPECTED_RUNTIME_SHA256["schema"],
        _CLOSURE_PATH: _EXPECTED_RUNTIME_SHA256["closure"],
        _CLOSURE_SCHEMA_PATH: _EXPECTED_RUNTIME_SHA256["closure_schema"],
        _GUARD_PATH: _EXPECTED_RUNTIME_SHA256["rpe01_guard"],
        _RPE03_PATH: _EXPECTED_RUNTIME_SHA256["rpe03_classifier"],
    }
    try:
        return all(path.is_file() and _raw_sha256_file(path) == digest for path, digest in expected.items())
    except (OSError, ValueError):
        return False


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load governed dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_preregistration() -> dict:
    if not _verify_runtime_bindings():
        raise RuntimeError("RPE04_RUNTIME_BINDING_MISMATCH")
    guard = _load_module(_GUARD_PATH, "rpe04_rpe01_guard")
    raw_document = _PREREG_PATH.read_text(encoding="utf-8")
    raw_schema = _SCHEMA_PATH.read_text(encoding="utf-8")
    validated = guard.validate_governed_json(raw_document, raw_schema)
    if type(validated) is not dict:
        raise RuntimeError("governed preregistration did not validate to an object")

    closure_document = _CLOSURE_PATH.read_text(encoding="utf-8")
    closure_schema = _CLOSURE_SCHEMA_PATH.read_text(encoding="utf-8")
    closure_validated = guard.validate_governed_json(closure_document, closure_schema)
    if type(closure_validated) is not dict:
        raise RuntimeError("governed closure preregistration did not validate to an object")

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


def _lexists(path: Path) -> bool:
    return os.path.lexists(str(path))


def _inside_root(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _verify_physical_object_domain(repo_path: Path) -> tuple[bool, str | None]:
    legacy_required_dirs = [
        repo_path,
        repo_path / "objects",
        repo_path / "objects" / "pack",
        repo_path / "objects" / "info",
    ]

    try:
        if not _lexists(repo_path):
            return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
        if _is_indirection(repo_path):
            return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
        repo = repo_path.resolve(strict=True)
        if not repo.is_dir():
            return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"

    for path in legacy_required_dirs:
        try:
            if not _lexists(path) or not path.is_dir():
                return False, "PHYSICAL_OBJECT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(path):
                return False, "PHYSICAL_OBJECT_DOMAIN_INDIRECTION"
            resolved = path.resolve(strict=True)
            if not _inside_root(resolved, repo):
                return False, "PHYSICAL_OBJECT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE"

    refs = repo_path / "refs"
    try:
        if not _lexists(refs) or not refs.is_dir():
            return False, "PHYSICAL_GIT_DOMAIN_REQUIRED_PATH_MISSING"
        if _is_indirection(refs):
            return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
        if not _inside_root(refs.resolve(strict=True), repo):
            return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    for required_file in (repo_path / "HEAD", repo_path / "config"):
        try:
            if not _lexists(required_file) or not required_file.is_file():
                return False, "PHYSICAL_GIT_DOMAIN_REQUIRED_PATH_MISSING"
            if _is_indirection(required_file):
                return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
            if not _inside_root(required_file.resolve(strict=True), repo):
                return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    for optional_path in (repo_path / "packed-refs", repo_path / "refs" / "rpe04"):
        if not _lexists(optional_path):
            continue
        try:
            if _is_indirection(optional_path):
                return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
            if not _inside_root(optional_path.resolve(strict=True), repo):
                return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
        except (OSError, RuntimeError, ValueError):
            return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

    alternates = repo_path / "objects" / "info" / "alternates"
    if _lexists(alternates):
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"

    try:
        for current, dirs, files in os.walk(repo, topdown=True, followlinks=False):
            current_path = Path(current)
            for name in [*dirs, *files]:
                child = current_path / name
                if _is_indirection(child):
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
                resolved = child.resolve(strict=True)
                if not _inside_root(resolved, repo):
                    return False, "PHYSICAL_GIT_DOMAIN_ESCAPE"
    except (OSError, RuntimeError, ValueError):
        return False, "PHYSICAL_GIT_DOMAIN_UNPROVABLE"

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
        cp = _run_local_git(
            "for-each-ref",
            "--format=%(refname) %(objectname)",
            _LOCAL_REF,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    lines = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    parts = lines[0].split()
    if len(parts) != 2 or parts[0] != _LOCAL_REF:
        return None
    return parts[1]


def _materialized_object_type(sha: str) -> str | None:
    try:
        cp = _run_local_git("cat-file", "-t", sha)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _materialized_commit(sha: str) -> bool:
    return _materialized_object_type(sha) == "commit"


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

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_OBJECT_DOMAIN_UNPROVABLE", attempt_started_at_ns, remote_done)

    if not _verify_local_config_allowlist():
        return _failure("LOCAL_CONFIG_NOT_ALLOWLISTED", attempt_started_at_ns, remote_done)

    refs = _namespace_refs()
    if refs != [_LOCAL_REF]:
        return _failure("UNEXPECTED_OBSERVATION_NAMESPACE", attempt_started_at_ns, remote_done)

    observed_head = _extract_observed_sha()
    if type(observed_head) is not str or _SHA40_RE.fullmatch(observed_head) is None:
        return _failure("MALFORMED_OBSERVED_SHA", attempt_started_at_ns, remote_done)

    observed_type = _materialized_object_type(observed_head)
    if observed_type is None:
        return _failure("OBSERVED_SHA_NOT_MATERIALIZED", attempt_started_at_ns, remote_done)
    if observed_type != "commit":
        return _failure("EXACT_OBSERVED_REF_NOT_COMMIT", attempt_started_at_ns, remote_done)

    if not _verify_runtime_bindings():
        return _failure("RUNTIME_BINDING_MISMATCH", attempt_started_at_ns, remote_done)

    if not _verify_git_executable_identity():
        return _failure("GIT_EXECUTABLE_IDENTITY_MISMATCH", attempt_started_at_ns, remote_done)

    ok, code = _verify_physical_object_domain(_OBSERVER)
    if not ok:
        return _failure(code or "PHYSICAL_GIT_DOMAIN_UNPROVABLE", attempt_started_at_ns, remote_done)

    transition = _RPE03.classify_transition(
        _OBSERVER,
        previous_observed_head,
        observed_head,
        str(_GIT),
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

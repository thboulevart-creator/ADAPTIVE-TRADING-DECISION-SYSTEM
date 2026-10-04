"""RPE-03 V0.2: fail-closed local Git ancestry classifier with governed executable binding."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Final


_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
_TIMEOUT_SECONDS: Final = 5

_GOVERNED_GIT_PATH: Final = r"C:\Program Files\Git\cmd\git.exe"
_GOVERNED_GIT_SHA256: Final = "81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5"
_GOVERNED_GIT_VERSION: Final = "git version 2.54.0.windows.1"
_MIN_GIT_VERSION: Final = (2, 54, 0)

_SAFE_GIT_ENV_KEYS: Final = {
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_CONFIG_GLOBAL",
    "GIT_TERMINAL_PROMPT",
    "GIT_OPTIONAL_LOCKS",
    "GIT_NO_LAZY_FETCH",
}


def _safe_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        {
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_LAZY_FETCH": "1",
        }
    )
    return env


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def _sha256_file(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _git_version(executable: str) -> str | None:
    try:
        cp = subprocess.run(
            [executable, "--version"],
            env=_safe_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _parse_git_version(text: str | None) -> tuple[int, int, int] | None:
    if type(text) is not str:
        return None
    m = re.fullmatch(r"git version (\d+)\.(\d+)\.(\d+)(?:\..*)?", text)
    if m is None:
        return None
    return tuple(int(x) for x in m.groups())


def _verify_governed_git_executable(governed_git_executable) -> bool:
    if type(governed_git_executable) is not str:
        return False
    try:
        supplied = Path(governed_git_executable).resolve(strict=True)
        expected = Path(_GOVERNED_GIT_PATH).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return False
    if not supplied.is_file() or not _same_path(supplied, expected):
        return False
    if _sha256_file(supplied) != _GOVERNED_GIT_SHA256:
        return False
    version = _git_version(str(supplied))
    if version != _GOVERNED_GIT_VERSION:
        return False
    parsed = _parse_git_version(version)
    if parsed is None or parsed < _MIN_GIT_VERSION:
        return False
    return True


def _run_git(
    repo_path: Path,
    governed_git_executable: str,
    *args: str,
) -> subprocess.CompletedProcess[str] | None:
    cmd = [governed_git_executable, "-c", "core.commitGraph=false", *args]
    try:
        return subprocess.run(
            cmd,
            cwd=str(repo_path),
            env=_safe_git_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None


def _stdout_ok(cp: subprocess.CompletedProcess[str] | None) -> str | None:
    if cp is None or cp.returncode != 0:
        return None
    return cp.stdout.strip()


def _canonical_path(text: str, base: Path) -> Path:
    p = Path(text)
    if not p.is_absolute():
        p = base / p
    return p.resolve(strict=False)


def _verified_domain(
    repo_path: Path,
    governed_git_executable: str,
) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.is_dir():
        return None

    dot_git = repo / ".git"
    if dot_git.is_file():
        return None

    bare_text = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--is-bare-repository")
    )
    git_dir_text = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--absolute-git-dir")
    )
    common_dir_text = _stdout_ok(
        _run_git(
            repo,
            governed_git_executable,
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        )
    )
    if bare_text not in {"true", "false"} or not git_dir_text or not common_dir_text:
        return None

    git_dir = _canonical_path(git_dir_text, repo)
    common_dir = _canonical_path(common_dir_text, repo)
    if not _same_path(git_dir, common_dir):
        return None

    if bare_text == "true":
        if not _same_path(git_dir, repo):
            return None
    else:
        top_text = _stdout_ok(
            _run_git(repo, governed_git_executable, "rev-parse", "--show-toplevel")
        )
        if not top_text:
            return None
        top = _canonical_path(top_text, repo)
        if not _same_path(top, repo):
            return None
        if not dot_git.is_dir():
            return None
        if not _same_path(git_dir, dot_git.resolve(strict=False)):
            return None

    shallow = _stdout_ok(
        _run_git(repo, governed_git_executable, "rev-parse", "--is-shallow-repository")
    )
    if shallow is None or shallow.lower() != "false":
        return None
    if (common_dir / "shallow").exists():
        return None
    if (common_dir / "info" / "grafts").exists():
        return None
    if (common_dir / "objects" / "info" / "alternates").exists():
        return None

    return repo, common_dir


def _valid_commit(repo: Path, sha: object, governed_git_executable: str) -> bool:
    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
        return False
    cp = _run_git(repo, governed_git_executable, "cat-file", "-t", sha)
    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"


def classify_transition(
    repo_path,
    previous_observed_head,
    new_exact_observed_head,
    governed_git_executable,
):
    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""

    if not _verify_governed_git_executable(governed_git_executable):
        return "UNKNOWN"

    if type(new_exact_observed_head) is not str or _SHA40_RE.fullmatch(
        new_exact_observed_head
    ) is None:
        return "UNKNOWN"
    if previous_observed_head is not None and (
        type(previous_observed_head) is not str
        or _SHA40_RE.fullmatch(previous_observed_head) is None
    ):
        return "UNKNOWN"

    try:
        repo_candidate = Path(repo_path)
    except (TypeError, ValueError):
        return "UNKNOWN"

    domain = _verified_domain(repo_candidate, governed_git_executable)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head, governed_git_executable):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head, governed_git_executable):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
        governed_git_executable,
        "merge-base",
        "--is-ancestor",
        previous_observed_head,
        new_exact_observed_head,
    )
    if cp is None:
        return "UNKNOWN"
    if cp.returncode == 0:
        return "FAST_FORWARD"
    if cp.returncode == 1:
        return "NON_FAST_FORWARD"
    return "UNKNOWN"

"""RPE-03 V0.1: fail-closed local Git ancestry classifier.

No network operations are permitted. The classifier rebuilds a sanitized Git
environment, verifies the local object domain, validates commit identities, and
only then maps merge-base ancestry to the governed transition vocabulary.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Final


_SHA40_RE: Final = re.compile(r"[0-9a-f]{40}\Z")
_TIMEOUT_SECONDS: Final = 5
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


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    cmd = ["git", "-c", "core.commitGraph=false", *args]
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


def _verified_domain(repo_path: Path) -> tuple[Path, Path] | None:
    try:
        repo = repo_path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not repo.exists():
        return None

    git_dir_text = _stdout_ok(_run_git(repo, "rev-parse", "--absolute-git-dir"))
    common_dir_text = _stdout_ok(
        _run_git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    )
    if not git_dir_text or not common_dir_text:
        return None

    git_dir = _canonical_path(git_dir_text, repo)
    common_dir = _canonical_path(common_dir_text, repo)
    if os.path.normcase(str(git_dir)) != os.path.normcase(str(common_dir)):
        return None

    shallow = _stdout_ok(_run_git(repo, "rev-parse", "--is-shallow-repository"))
    if shallow is None or shallow.lower() != "false":
        return None

    if (common_dir / "shallow").exists():
        return None
    if (common_dir / "info" / "grafts").exists():
        return None
    if (common_dir / "objects" / "info" / "alternates").exists():
        return None

    return repo, common_dir


def _valid_commit(repo: Path, sha: object) -> bool:
    if type(sha) is not str or _SHA40_RE.fullmatch(sha) is None:
        return False
    cp = _run_git(repo, "cat-file", "-t", sha)
    return cp is not None and cp.returncode == 0 and cp.stdout.strip() == "commit"


def classify_transition(
    repo_path,
    previous_observed_head,
    new_exact_observed_head,
):
    """Return INITIAL, SAME, FAST_FORWARD, NON_FAST_FORWARD, or UNKNOWN."""
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

    domain = _verified_domain(repo_candidate)
    if domain is None:
        return "UNKNOWN"
    repo, _common_dir = domain

    if not _valid_commit(repo, new_exact_observed_head):
        return "UNKNOWN"

    if previous_observed_head is None:
        return "INITIAL"

    if not _valid_commit(repo, previous_observed_head):
        return "UNKNOWN"

    if previous_observed_head == new_exact_observed_head:
        return "SAME"

    cp = _run_git(
        repo,
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

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).with_name("historical_regression_baselines.json")
CHILD_ENV = "P0_HISTORICAL_REPLAY_CHILD"
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

_REPLAY_RESULTS: dict[tuple[str, str], str] = {}
_WORKTREES: dict[str, Path] = {}
_TEMP_ROOT: Path | None = None


def _load_manifest() -> dict[str, str]:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if data.get("schema") != "HISTORICAL_REGRESSION_BASELINES_V1":
        raise pytest.UsageError("historical regression manifest schema mismatch")
    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise pytest.UsageError("historical regression entries missing")
    if data.get("historical_node_count") != 115 or len(entries) != 115:
        raise pytest.UsageError("historical regression node count mismatch")
    files = {node.split("::", 1)[0] for node in entries}
    if data.get("historical_file_count") != 42 or len(files) != 42:
        raise pytest.UsageError("historical regression file count mismatch")
    for nodeid, commit in entries.items():
        if (
            not isinstance(nodeid, str)
            or not nodeid.startswith("tests/")
            or "::" not in nodeid
            or not isinstance(commit, str)
            or not _COMMIT_RE.fullmatch(commit)
        ):
            raise pytest.UsageError(f"invalid historical regression entry: {nodeid!r}")
    return dict(entries)


_ENTRIES = {} if os.environ.get(CHILD_ENV) == "1" else _load_manifest()


def pytest_collection_modifyitems(session, config, items):
    if not _ENTRIES:
        return
    collected = {item.nodeid for item in items}
    missing = sorted(set(_ENTRIES) - collected)
    if missing:
        raise pytest.UsageError(
            "historical regression manifest references missing current nodeids: "
            + ", ".join(missing)
        )


def _run(
    args: list[str],
    *,
    cwd: Path = ROOT,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env[CHILD_ENV] = "1"
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def _worktree_for(commit: str) -> Path:
    global _TEMP_ROOT
    existing = _WORKTREES.get(commit)
    if existing is not None:
        return existing

    verify = _run(["git", "cat-file", "-e", f"{commit}^{{commit}}"])
    if verify.returncode != 0:
        pytest.fail(
            f"historical regression commit is unavailable: {commit}\n{verify.stdout}",
            pytrace=False,
        )

    if _TEMP_ROOT is None:
        _TEMP_ROOT = Path(tempfile.mkdtemp(prefix="p0-historical-regression-"))
    worktree = _TEMP_ROOT / commit[:12]
    added = _run(["git", "worktree", "add", "--detach", str(worktree), commit])
    if added.returncode != 0:
        pytest.fail(
            f"cannot create historical regression worktree for {commit}\n{added.stdout}",
            pytrace=False,
        )
    _WORKTREES[commit] = worktree
    return worktree


def _replay_historical_file(test_file: str, commit: str) -> None:
    cache_key = (test_file, commit)
    if cache_key in _REPLAY_RESULTS:
        return
    worktree = _worktree_for(commit)
    probe = _run([sys.executable, "-m", "pytest", "-q", test_file], cwd=worktree)
    if probe.returncode != 0:
        pytest.fail(
            "historical regression replay failed\n"
            f"file: {test_file}\n"
            f"commit: {commit}\n"
            f"{probe.stdout}",
            pytrace=False,
        )
    _REPLAY_RESULTS[cache_key] = probe.stdout


def pytest_pyfunc_call(pyfuncitem):
    commit = _ENTRIES.get(pyfuncitem.nodeid)
    if commit is None:
        return None
    test_file = pyfuncitem.nodeid.split("::", 1)[0]
    _replay_historical_file(test_file, commit)
    return True


def pytest_sessionfinish(session, exitstatus):
    global _TEMP_ROOT
    for worktree in list(_WORKTREES.values()):
        _run(["git", "worktree", "remove", "--force", str(worktree)])
    _WORKTREES.clear()
    if _TEMP_ROOT is not None:
        shutil.rmtree(_TEMP_ROOT, ignore_errors=True)
        _TEMP_ROOT = None

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
BRANCH = (
    "feat/obsidian-projection-p5d3f-persistent-production-handoff-contract-v0.1"
)
EXPECTED_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
EXPECTED_TEST_BLOB = (
    "6cc6af77efe3c6abb1aaf8ae2df5be9e64cb1bb7"
)
OID40 = re.compile(r"^[0-9a-f]{40}$")


class GovernedRunError(RuntimeError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    *args: str,
    cwd: Path,
    capture: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        text=True,
        capture_output=capture,
        env=env,
    )


def _git(
    repo: Path,
    *args: str,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return _run(
        "git",
        *args,
        cwd=repo,
        capture=capture,
    )


def _stdout(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stdout or "").strip()


def _require_ok(
    result: subprocess.CompletedProcess[str],
    message: str,
) -> None:
    if result.returncode != 0:
        details = (
            (result.stderr or "").strip()
            or (result.stdout or "").strip()
        )
        raise GovernedRunError(
            f"{message}: {details}"
            if details
            else message
        )


def _normalize_origin(origin: str) -> str:
    value = origin.strip()
    for prefix in (
        "git@github.com:",
        "https://github.com/",
        "ssh://git@github.com/",
    ):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    else:
        raise GovernedRunError(
            f"unsupported origin form: {origin}"
        )
    if value.endswith(".git"):
        value = value[:-4]
    return value.strip("/")


def _require_clean(repo: Path, stage: str) -> None:
    result = _git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    _require_ok(result, f"git status failed during {stage}")
    dirty = _stdout(result)
    if dirty:
        raise GovernedRunError(
            f"working tree non propre {stage}: {dirty}"
        )


def _committed_blob(repo: Path, relative: str) -> str:
    result = _git(
        repo,
        "rev-parse",
        f"HEAD:{relative}",
    )
    _require_ok(
        result,
        f"git rev-parse HEAD:{relative} failed",
    )
    return _stdout(result)


def _reexec(repo: Path) -> None:
    script = (
        repo
        / "tools"
        / "obsidian_projection"
        / "p5d3f_persistent_production_handoff_contract_rebreak.py"
    )
    os.execv(
        sys.executable,
        [sys.executable, str(script), *sys.argv[1:]],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-remote-head", required=True)
    parser.add_argument("--expected-candidate-head", required=True)
    args = parser.parse_args()

    if OID40.fullmatch(args.expected_remote_head) is None:
        raise GovernedRunError("invalid --expected-remote-head")
    if OID40.fullmatch(args.expected_candidate_head) is None:
        raise GovernedRunError("invalid --expected-candidate-head")

    repo = _repo_root()

    print(
        "=== P5-D3F PERSISTENT PRODUCTION HANDOFF "
        "CONTRACT RE-BREAK ==="
    )
    print(
        "=== CONTRACT ONLY — NO STAGING CREATION / "
        "NO REAL VAULT ACCESS ==="
    )

    origin = _git(repo, "remote", "get-url", "origin")
    _require_ok(origin, "cannot read origin")
    if _normalize_origin(_stdout(origin)) != EXPECTED_REPOSITORY:
        raise GovernedRunError("repository mismatch")

    _require_clean(repo, "avant P5-D3F persistent contract re-break")
    print("CONTROL_CLONE_CLEAN_BEFORE=PASS")

    fetch = _git(
        repo,
        "fetch",
        "--no-tags",
        "origin",
        BRANCH,
        capture=False,
    )
    _require_ok(fetch, "fetch persistent handoff contract branch failed")

    fetched = _git(repo, "rev-parse", "FETCH_HEAD")
    _require_ok(fetched, "cannot resolve FETCH_HEAD")
    fetched_head = _stdout(fetched)
    print(f"FETCHED_HEAD={fetched_head}")
    if fetched_head != args.expected_remote_head:
        raise GovernedRunError(
            "REMOTE_RACE_GUARD: "
            f"attendu {args.expected_remote_head}, "
            f"reçu {fetched_head}"
        )
    print("REMOTE_RACE_GUARD=PASS")

    exists = _git(
        repo,
        "cat-file",
        "-e",
        f"{args.expected_candidate_head}^{{commit}}",
    )
    _require_ok(exists, "persistent handoff contract candidate missing")

    loaded = _git(repo, "rev-parse", "HEAD")
    _require_ok(loaded, "cannot resolve HEAD")
    if _stdout(loaded) != args.expected_candidate_head:
        checkout = _git(
            repo,
            "switch",
            "--detach",
            args.expected_candidate_head,
            capture=False,
        )
        _require_ok(
            checkout,
            "cannot checkout persistent handoff contract candidate",
        )
        print(
            "P5D3F_PERSISTENT_HANDOFF_CONTRACT_REEXEC_AFTER_CHECKOUT=REQUIRED"
        )
        _reexec(repo)
        raise AssertionError("os.execv returned unexpectedly")

    contract_rel = (
        "tools/obsidian_projection/"
        "persistent_production_handoff_gate_contract_v0_1.json"
    )
    tests_rel = (
        "tests/obsidian_projection/"
        "test_p5d3f_persistent_production_handoff_gate_contract_v0_1.py"
    )

    if _committed_blob(repo, contract_rel) != EXPECTED_CONTRACT_BLOB:
        raise GovernedRunError("persistent handoff contract blob mismatch")
    if _committed_blob(repo, tests_rel) != EXPECTED_TEST_BLOB:
        raise GovernedRunError("persistent handoff contract tests blob mismatch")

    print("P5D3F_PERSISTENT_HANDOFF_CONTRACT_BLOBS=PASS")

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-PERSISTENT-HANDOFF-CONTRACT-PYCACHE"
    )
    pycache.mkdir(parents=True, exist_ok=True)
    env = {
        **os.environ,
        "PYTHONPYCACHEPREFIX": str(pycache),
        "PYTHONDONTWRITEBYTECODE": "1",
    }

    compile_result = _run(
        sys.executable,
        "-m",
        "py_compile",
        "tools/obsidian_projection/"
        "p5d3f_persistent_production_handoff_contract_rebreak.py",
        tests_rel,
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "persistent handoff contract py_compile failed",
    )
    print("P5D3F_PERSISTENT_HANDOFF_CONTRACT_PY_COMPILE=PASS")

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_production_handoff_gate_contract_v0_1",
        "-v",
        cwd=repo,
        env=env,
    )
    if targeted.stdout:
        print(targeted.stdout, end="")
    if targeted.stderr:
        print(targeted.stderr, end="", file=sys.stderr)
    _require_ok(
        targeted,
        "persistent handoff targeted contract tests failed",
    )
    print("P5D3F_PERSISTENT_HANDOFF_CONTRACT_TARGETED=PASS")

    full = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests/obsidian_projection",
        "-p",
        "test_*.py",
        "-v",
        cwd=repo,
        env=env,
    )
    if full.stdout:
        print(full.stdout, end="")
    if full.stderr:
        print(full.stderr, end="", file=sys.stderr)
    _require_ok(full, "full Obsidian suite failed")
    print("P5D3F_PERSISTENT_HANDOFF_CONTRACT_FULL_REBREAK=PASS")

    _require_clean(repo, "après P5-D3F persistent contract re-break")
    print("CONTROL_CLONE_CLEAN=PASS")
    print("P5D3F_PERSISTENT_HANDOFF_CONTRACT_REBREAK_COMPLETED=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernedRunError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(2)

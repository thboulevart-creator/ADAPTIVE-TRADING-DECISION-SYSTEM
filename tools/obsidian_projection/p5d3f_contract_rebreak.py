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
    "feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1"
)
EXPECTED_CONTRACT_BLOB = (
    "64744325251db350d26c0269090ce62d5fa5f2e8"
)
EXPECTED_TEST_BLOB = (
    "6c7f3d5e1962132f4b609b637d176e67ccd376d5"
)
OID40 = re.compile(r"^[0-9a-f]{40}$")


class GovernedRunError(RuntimeError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    *args: str,
    cwd: Path,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        text=True,
        capture_output=capture,
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


def _stdout(
    result: subprocess.CompletedProcess[str],
) -> str:
    return (result.stdout or "").strip()


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
    _require_ok(
        result,
        f"git status failed during {stage}",
    )
    dirty = _stdout(result)
    if dirty:
        raise GovernedRunError(
            f"working tree non propre {stage}: {dirty}"
        )


def _hash_object(repo: Path, relative: str) -> str:
    result = _git(
        repo,
        "hash-object",
        relative,
    )
    _require_ok(
        result,
        f"git hash-object failed for {relative}",
    )
    return _stdout(result)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Governed P5-D3F promotion-handoff "
            "contract qualification re-break."
        )
    )
    parser.add_argument(
        "--expected-remote-head",
        required=True,
    )
    parser.add_argument(
        "--expected-candidate-head",
        required=True,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()

    if not OID40.fullmatch(
        args.expected_remote_head
    ):
        raise GovernedRunError(
            "invalid --expected-remote-head"
        )
    if not OID40.fullmatch(
        args.expected_candidate_head
    ):
        raise GovernedRunError(
            "invalid --expected-candidate-head"
        )

    repo = _repo_root()

    print(
        "=== P5-D3F PROMOTION HANDOFF "
        "CONTRACT RE-BREAK ==="
    )
    print(
        "=== PYTHON / CONTRACT ONLY — "
        "NO HANDOFF RUNTIME / NO LIVE VAULT WRITE ==="
    )
    print(f"CONTROL_REPO_ROOT={repo}")

    origin_result = _git(
        repo,
        "remote",
        "get-url",
        "origin",
    )
    _require_ok(
        origin_result,
        "cannot read origin",
    )
    origin = _stdout(origin_result)
    if _normalize_origin(origin) != EXPECTED_REPOSITORY:
        raise GovernedRunError(
            f"repository mismatch: {origin}"
        )

    _require_clean(
        repo,
        "avant P5-D3F contract re-break",
    )
    print("CONTROL_CLONE_CLEAN_BEFORE=PASS")

    fetch = _git(
        repo,
        "fetch",
        "--no-tags",
        "origin",
        BRANCH,
        capture=False,
    )
    _require_ok(
        fetch,
        "fetch branche P5-D3F échoué",
    )

    fetched = _git(
        repo,
        "rev-parse",
        "FETCH_HEAD",
    )
    _require_ok(
        fetched,
        "cannot resolve FETCH_HEAD",
    )
    fetched_head = _stdout(fetched)
    print(f"FETCHED_HEAD={fetched_head}")
    if fetched_head != args.expected_remote_head:
        raise GovernedRunError(
            "REMOTE_RACE_GUARD: "
            f"attendu {args.expected_remote_head}, "
            f"reçu {fetched_head}"
        )
    print("REMOTE_RACE_GUARD=PASS")

    candidate_exists = _git(
        repo,
        "cat-file",
        "-e",
        f"{args.expected_candidate_head}^{{commit}}",
    )
    _require_ok(
        candidate_exists,
        "candidat P5-D3F introuvable",
    )

    checkout = _git(
        repo,
        "switch",
        "--detach",
        args.expected_candidate_head,
        capture=False,
    )
    _require_ok(
        checkout,
        "checkout candidat P5-D3F impossible",
    )

    head = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    _require_ok(head, "cannot resolve HEAD")
    runtime_head = _stdout(head)
    if runtime_head != args.expected_candidate_head:
        raise GovernedRunError(
            f"runtime HEAD inattendu: {runtime_head}"
        )
    print(f"P5D3F_RUNTIME_HEAD={runtime_head}")

    contract_blob = _hash_object(
        repo,
        "tools/obsidian_projection/"
        "promotion_handoff_contract_v0_1.json",
    )
    test_blob = _hash_object(
        repo,
        "tests/obsidian_projection/"
        "test_promotion_handoff_contract_v0_1.py",
    )

    if contract_blob != EXPECTED_CONTRACT_BLOB:
        raise GovernedRunError(
            "P5-D3F contract blob inattendu: "
            f"{contract_blob}"
        )
    if test_blob != EXPECTED_TEST_BLOB:
        raise GovernedRunError(
            "P5-D3F contract-test blob inattendu: "
            f"{test_blob}"
        )

    print("P5D3F_CONTRACT_BLOB=PASS")
    print("P5D3F_CONTRACT_TEST_BLOB=PASS")

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-CONTRACT-PYCACHE"
    )
    pycache.mkdir(
        parents=True,
        exist_ok=True,
    )

    old_prefix = os.environ.get(
        "PYTHONPYCACHEPREFIX"
    )
    os.environ["PYTHONPYCACHEPREFIX"] = str(
        pycache
    )

    try:
        compile_result = _run(
            sys.executable,
            "-m",
            "py_compile",
            "tools/obsidian_projection/"
            "p5d3f_contract_rebreak.py",
            "tests/obsidian_projection/"
            "test_promotion_handoff_contract_v0_1.py",
            "tests/obsidian_projection/"
            "test_p5d3f_contract_rebreak_runner.py",
            cwd=repo,
        )
        _require_ok(
            compile_result,
            "P5-D3F contract py_compile failed",
        )
        print("P5D3F_CONTRACT_PY_COMPILE=PASS")

        targeted = _run(
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "tests.obsidian_projection."
            "test_promotion_handoff_contract_v0_1",
            "tests.obsidian_projection."
            "test_p5d3f_contract_rebreak_runner",
            "-v",
            cwd=repo,
        )
        _require_ok(
            targeted,
            "P5-D3F targeted contract tests failed",
        )
        print("P5D3F_CONTRACT_TARGETED=PASS")

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
        )
        _require_ok(
            full,
            "full Obsidian suite failed",
        )
        print("P5D3F_FULL_REBREAK=PASS")

        _require_clean(
            repo,
            "après P5-D3F contract re-break",
        )
        print("CONTROL_CLONE_CLEAN=PASS")
        print(
            "P5D3F_CONTRACT_REBREAK_COMPLETED=PASS"
        )
        return 0
    finally:
        if old_prefix is None:
            os.environ.pop(
                "PYTHONPYCACHEPREFIX",
                None,
            )
        else:
            os.environ[
                "PYTHONPYCACHEPREFIX"
            ] = old_prefix


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernedRunError as exc:
        print(
            f"BLOCKED: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)

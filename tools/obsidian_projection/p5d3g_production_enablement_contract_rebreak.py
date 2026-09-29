from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
BRANCH = (
    "feat/obsidian-projection-p5d3g-production-enablement-contract-v0.1"
)
EXPECTED_CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)
EXPECTED_TEST_BLOB = (
    "12873436d6354ffa454253cdf754023378d35076"
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
    _require_ok(
        result,
        f"git status failed during {stage}",
    )
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
        / "p5d3g_production_enablement_contract_rebreak.py"
    )
    os.execv(
        sys.executable,
        [sys.executable, str(script), *sys.argv[1:]],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-remote-head",
        required=True,
    )
    parser.add_argument(
        "--expected-candidate-head",
        required=True,
    )
    args = parser.parse_args()

    if OID40.fullmatch(
        args.expected_remote_head
    ) is None:
        raise GovernedRunError(
            "invalid --expected-remote-head"
        )
    if OID40.fullmatch(
        args.expected_candidate_head
    ) is None:
        raise GovernedRunError(
            "invalid --expected-candidate-head"
        )

    repo = _repo_root()

    print(
        "=== P5-D3G PRODUCTION ENABLEMENT "
        "CONTRACT RE-BREAK ==="
    )
    print(
        "=== CONTRACT ONLY — NO REAL VAULT ACCESS "
        "/ NO PRODUCTION EXECUTION ==="
    )

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
    if _normalize_origin(
        _stdout(origin_result)
    ) != EXPECTED_REPOSITORY:
        raise GovernedRunError(
            "repository mismatch"
        )

    _require_clean(
        repo,
        "avant production-enablement contract re-break",
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
        "fetch production-enablement branch failed",
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
        "production-enablement candidate missing",
    )

    loaded = _git(repo, "rev-parse", "HEAD")
    _require_ok(loaded, "cannot resolve HEAD")
    loaded_head = _stdout(loaded)

    if loaded_head != args.expected_candidate_head:
        checkout = _git(
            repo,
            "switch",
            "--detach",
            args.expected_candidate_head,
            capture=False,
        )
        _require_ok(
            checkout,
            "cannot checkout production-enablement candidate",
        )
        switched = _git(repo, "rev-parse", "HEAD")
        _require_ok(
            switched,
            "cannot resolve switched HEAD",
        )
        if _stdout(switched) != (
            args.expected_candidate_head
        ):
            raise GovernedRunError(
                "candidate checkout mismatch"
            )
        print(
            "P5D3G_PRODUCTION_ENABLEMENT_REEXEC_AFTER_CHECKOUT=REQUIRED"
        )
        _reexec(repo)
        raise AssertionError(
            "os.execv returned unexpectedly"
        )

    contract_blob = _committed_blob(
        repo,
        "tools/obsidian_projection/"
        "production_enablement_gate_contract_v0_1.json",
    )
    test_blob = _committed_blob(
        repo,
        "tests/obsidian_projection/"
        "test_production_enablement_gate_contract_v0_1.py",
    )
    if contract_blob != EXPECTED_CONTRACT_BLOB:
        raise GovernedRunError(
            "production-enablement contract blob mismatch"
        )
    if test_blob != EXPECTED_TEST_BLOB:
        raise GovernedRunError(
            "production-enablement tests blob mismatch"
        )

    print("P5D3G_PRODUCTION_ENABLEMENT_CONTRACT_BLOB=PASS")
    print("P5D3G_PRODUCTION_ENABLEMENT_TEST_BLOB=PASS")

    compile_result = _run(
        sys.executable,
        "-m",
        "py_compile",
        "tools/obsidian_projection/"
        "p5d3g_production_enablement_contract_rebreak.py",
        "tests/obsidian_projection/"
        "test_production_enablement_gate_contract_v0_1.py",
        cwd=repo,
    )
    _require_ok(
        compile_result,
        "production-enablement py_compile failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_PY_COMPILE=PASS"
    )

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_production_enablement_gate_contract_v0_1",
        "-v",
        cwd=repo,
    )
    if targeted.stdout:
        print(targeted.stdout, end="")
    if targeted.stderr:
        print(targeted.stderr, end="", file=sys.stderr)
    _require_ok(
        targeted,
        "production-enablement targeted contract tests failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_CONTRACT_TARGETED=PASS"
    )

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
    if full.stdout:
        print(full.stdout, end="")
    if full.stderr:
        print(full.stderr, end="", file=sys.stderr)
    _require_ok(
        full,
        "full Obsidian suite failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_CONTRACT_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après production-enablement contract re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_CONTRACT_REBREAK_COMPLETED=PASS"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernedRunError as exc:
        print(
            f"BLOCKED: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)

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
    "feat/obsidian-projection-p5d3g-production-enablement-implementation-v0.1"
)
EXPECTED_CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)
EXPECTED_IMPLEMENTATION_BLOB = (
    "64c1b2279835f57c03c9ec2d6a0eae9e349d55ee"
)
EXPECTED_TEST_BLOB = (
    "5a05ac5fccaf7032248f35f8fd2933d5943b100c"
)
EXPECTED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (
    "b8875f8973ddf1076ff20d8e725ce04abbb814a8"
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


def _stdout(
    result: subprocess.CompletedProcess[str],
) -> str:
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


def _committed_blob(
    repo: Path,
    relative: str,
) -> str:
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
        / "p5d3g_production_enablement_implementation_rebreak.py"
    )
    os.execv(
        sys.executable,
        [sys.executable, str(script), *sys.argv[1:]],
    )


def _static_surface_scan(repo: Path) -> None:
    source = (
        repo
        / "tools"
        / "obsidian_projection"
        / "production_enablement.py"
    ).read_text(encoding="utf-8")

    forbidden = (
        "execute_finite_live_publication",
        "PROMOTION_CONFIRMED",
        "os.replace(",
        "threading.Thread",
        "while True",
        "schtasks",
        "CreateService",
        "schedule.",
    )
    hits = [
        token
        for token in forbidden
        if token in source
    ]
    if hits:
        raise GovernedRunError(
            "production execution/background surface present: "
            + ", ".join(hits)
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
        "IMPLEMENTATION SYNTHETIC RE-BREAK ==="
    )
    print(
        "=== NO REAL VAULT ACCESS / NO STAGE-B / "
        "NO PRODUCTION EXECUTION ==="
    )

    origin = _git(
        repo,
        "remote",
        "get-url",
        "origin",
    )
    _require_ok(
        origin,
        "cannot read origin",
    )
    if _normalize_origin(
        _stdout(origin)
    ) != EXPECTED_REPOSITORY:
        raise GovernedRunError(
            "repository mismatch"
        )

    _require_clean(
        repo,
        "avant production-enablement implementation re-break",
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
        "fetch production-enablement implementation branch failed",
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

    exists = _git(
        repo,
        "cat-file",
        "-e",
        f"{args.expected_candidate_head}^{{commit}}",
    )
    _require_ok(
        exists,
        "production-enablement implementation candidate missing",
    )

    loaded = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    _require_ok(
        loaded,
        "cannot resolve HEAD",
    )

    if _stdout(loaded) != (
        args.expected_candidate_head
    ):
        checkout = _git(
            repo,
            "switch",
            "--detach",
            args.expected_candidate_head,
            capture=False,
        )
        _require_ok(
            checkout,
            "cannot checkout production-enablement implementation candidate",
        )
        print(
            "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_REEXEC_AFTER_CHECKOUT=REQUIRED"
        )
        _reexec(repo)
        raise AssertionError(
            "os.execv returned unexpectedly"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "production_enablement_gate_contract_v0_1.json"
        ): EXPECTED_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "production_enablement.py"
        ): EXPECTED_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3g_production_enablement.py"
        ): EXPECTED_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "live_publication_transaction.py"
        ): EXPECTED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
    }

    for relative, expected_blob in expected_blobs.items():
        actual = _committed_blob(
            repo,
            relative,
        )
        if actual != expected_blob:
            raise GovernedRunError(
                f"blob mismatch: {relative}: {actual}"
            )

    print(
        "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_BLOBS=PASS"
    )

    _static_surface_scan(repo)
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_EXECUTION_SURFACE_SCAN=PASS"
    )

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3G-PRODUCTION-ENABLEMENT-IMPLEMENTATION-PYCACHE"
    )
    pycache.mkdir(
        parents=True,
        exist_ok=True,
    )
    env = {
        **os.environ,
        "PYTHONPYCACHEPREFIX":
            str(pycache),
        "PYTHONDONTWRITEBYTECODE":
            "1",
    }

    compile_result = _run(
        sys.executable,
        "-m",
        "py_compile",
        "tools/obsidian_projection/"
        "production_enablement.py",
        "tools/obsidian_projection/"
        "p5d3g_production_enablement_implementation_rebreak.py",
        "tests/obsidian_projection/"
        "test_p5d3g_production_enablement.py",
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "production-enablement implementation py_compile failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_PY_COMPILE=PASS"
    )

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_p5d3g_production_enablement",
        "-v",
        cwd=repo,
        env=env,
    )
    if targeted.stdout:
        print(
            targeted.stdout,
            end="",
        )
    if targeted.stderr:
        print(
            targeted.stderr,
            end="",
            file=sys.stderr,
        )
    _require_ok(
        targeted,
        "production-enablement targeted implementation tests failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_TARGETED=PASS"
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
        env=env,
    )
    if full.stdout:
        print(
            full.stdout,
            end="",
        )
    if full.stderr:
        print(
            full.stderr,
            end="",
            file=sys.stderr,
        )
    _require_ok(
        full,
        "full Obsidian suite failed",
    )
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après production-enablement implementation re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3G_PRODUCTION_ENABLEMENT_IMPLEMENTATION_REBREAK_COMPLETED=PASS"
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

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
    "feat/obsidian-projection-p5d3f-persistent-production-handoff-real-execution-v0.1"
)
EXPECTED_REAL_RUNNER_BLOB = (
    "e56501e3710ab23537975e950aff016e4a832742"
)
EXPECTED_REAL_RUNNER_TEST_BLOB = (
    "97d7577d46f728aae5bfe1e0eadc389121dd7872"
)
EXPECTED_IMPLEMENTATION_BLOB = (
    "d2f40c8b2c8fb06b37bb34442c59d78222046452"
)
EXPECTED_IMPLEMENTATION_TEST_BLOB = (
    "7da1fadeb1b3e9efee54b7ca09f0735277af345c"
)
EXPECTED_GATE_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
EXPECTED_QUALIFIED_P5D3F_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
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


def _require_clean(
    repo: Path,
    stage: str,
) -> None:
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


def _static_surface_scan(repo: Path) -> None:
    source = (
        repo
        / "tools"
        / "obsidian_projection"
        / "p5d3f_persistent_production_handoff_real_execution.py"
    ).read_text(encoding="utf-8")

    required = (
        "--expected-runner-blob",
        "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF",
        "execute_persistent_production_handoff",
        "REAL_VAULT_WRITE_AUTHORIZED=FALSE",
        "LIVE_PUBLICATION_AUTHORIZED=FALSE",
        "MANDATORY_STOP=TRUE",
    )
    for token in required:
        if token not in source:
            raise GovernedRunError(
                "required real-runner guard missing: "
                + token
            )

    forbidden = (
        "execute_finite_live_publication",
        "consume_stage_a_plan_approval",
        "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
        "os.replace(",
        "threading.Thread",
        "while True",
        "schtasks",
        "CreateService",
    )
    hits = [
        token
        for token in forbidden
        if token in source
    ]
    if hits:
        raise GovernedRunError(
            "forbidden later-authority surface present: "
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
        "=== P5-D3F PERSISTENT PRODUCTION HANDOFF "
        "REAL EXECUTION RUNNER SYNTHETIC RE-BREAK ==="
    )
    print(
        "=== NO PERSISTENT STAGING CREATION / "
        "NO REAL VAULT ACCESS ==="
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
        "avant real-execution-runner re-break",
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
        "fetch real-execution-runner branch failed",
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

    if fetched_head != (
        args.expected_remote_head
    ):
        raise GovernedRunError(
            "REMOTE_RACE_GUARD: "
            f"attendu {args.expected_remote_head}, "
            f"reçu {fetched_head}"
        )

    print("REMOTE_RACE_GUARD=PASS")

    local = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    _require_ok(
        local,
        "cannot resolve HEAD",
    )
    if _stdout(local) != (
        args.expected_candidate_head
    ):
        raise GovernedRunError(
            "LOCAL_HEAD_MISMATCH: switch manually to exact candidate before re-break"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "p5d3f_persistent_production_handoff_real_execution.py"
        ): EXPECTED_REAL_RUNNER_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_production_handoff_real_execution_runner.py"
        ): EXPECTED_REAL_RUNNER_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff.py"
        ): EXPECTED_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_production_handoff.py"
        ): EXPECTED_IMPLEMENTATION_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_1.json"
        ): EXPECTED_GATE_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3f_promotion_handoff.py"
        ): EXPECTED_QUALIFIED_P5D3F_BLOB,
    }

    for relative, expected_blob in (
        expected_blobs.items()
    ):
        actual = _committed_blob(
            repo,
            relative,
        )
        if actual != expected_blob:
            raise GovernedRunError(
                f"blob mismatch: {relative}: {actual}"
            )

    print(
        "P5D3F_PERSISTENT_REAL_RUNNER_BLOBS=PASS"
    )

    _static_surface_scan(repo)
    print(
        "P5D3F_PERSISTENT_REAL_RUNNER_SURFACE_SCAN=PASS"
    )

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-PERSISTENT-REAL-RUNNER-PYCACHE"
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
        "p5d3f_persistent_production_handoff_real_execution.py",
        "tests/obsidian_projection/"
        "test_p5d3f_persistent_production_handoff_real_execution_runner.py",
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "real-execution-runner py_compile failed",
    )
    print(
        "P5D3F_PERSISTENT_REAL_RUNNER_PY_COMPILE=PASS"
    )

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_production_handoff_real_execution_runner",
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
        "real-execution-runner targeted tests failed",
    )
    print(
        "P5D3F_PERSISTENT_REAL_RUNNER_TARGETED=PASS"
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
        "P5D3F_PERSISTENT_REAL_RUNNER_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après real-execution-runner re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3F_PERSISTENT_REAL_RUNNER_REBREAK_COMPLETED=PASS"
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

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
    "feat/obsidian-projection-p5d3f-persistent-handoff-recovery-contract-v0.2"
)
EXPECTED_CONTRACT_BLOB = (
    "aef627936b6f745017bcace7e8a3e44270f95674"
)
EXPECTED_TESTS_BLOB = (
    "38c6b5253750ef15e2b6fb3255e748808404b0b4"
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
        "=== P5-D3F PERSISTENT HANDOFF RECOVERY "
        "CONTRACT V0.2 RE-BREAK ==="
    )
    print(
        "=== CONTRACT ONLY — NO PERSISTENT STAGING / "
        "NO REAL VAULT ACCESS ==="
    )

    origin = _git(
        repo,
        "remote",
        "get-url",
        "origin",
    )
    _require_ok(origin, "cannot read origin")

    if _normalize_origin(
        _stdout(origin)
    ) != EXPECTED_REPOSITORY:
        raise GovernedRunError(
            "repository mismatch"
        )

    _require_clean(
        repo,
        "avant recovery contract re-break",
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
        "fetch recovery contract branch failed",
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
    _require_ok(local, "cannot resolve HEAD")

    if _stdout(local) != (
        args.expected_candidate_head
    ):
        raise GovernedRunError(
            "LOCAL_HEAD_MISMATCH: switch manually "
            "to exact candidate before re-break"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_2.json"
        ): EXPECTED_CONTRACT_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_handoff_recovery_contract_v0_2.py"
        ): EXPECTED_TESTS_BLOB,
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
        "P5D3F_RECOVERY_CONTRACT_BLOBS=PASS"
    )

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-RECOVERY-CONTRACT-PYCACHE"
    )
    pycache.mkdir(
        parents=True,
        exist_ok=True,
    )

    env = {
        **os.environ,
        "PYTHONPYCACHEPREFIX": str(pycache),
        "PYTHONDONTWRITEBYTECODE": "1",
    }

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_handoff_recovery_contract_v0_2",
        "-v",
        cwd=repo,
        env=env,
    )
    if targeted.stdout:
        print(targeted.stdout, end="")
    if targeted.stderr:
        print(
            targeted.stderr,
            end="",
            file=sys.stderr,
        )
    _require_ok(
        targeted,
        "recovery contract targeted tests failed",
    )
    print(
        "P5D3F_RECOVERY_CONTRACT_TARGETED=PASS"
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
        print(full.stdout, end="")
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
        "P5D3F_RECOVERY_CONTRACT_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après recovery contract re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3F_RECOVERY_CONTRACT_REBREAK_COMPLETED=PASS"
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

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
    "feat/obsidian-projection-p5d3f-persistent-handoff-recovery-implementation-v0.3"
)
EXPECTED_IMPLEMENTATION_BLOB = (
    "dcd70a9d9794675eab90e41df560f8b030b5dbf3"
)
EXPECTED_TESTS_BLOB = (
    "242305bc0f95bbe243158b5c806255508093a357"
)
EXPECTED_RECOVERY_CONTRACT_BLOB = (
    "aef627936b6f745017bcace7e8a3e44270f95674"
)
EXPECTED_V01_CONTRACT_BLOB = (
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
        / "persistent_production_handoff.py"
    ).read_text(encoding="utf-8")

    required = (
        "RECOVERY_GATE_CONTRACT_BLOB",
        "PRESENT_EMPTY_PACKAGES_RECOVERY",
        "_annotate_body_failure",
        "_cleanup_temp_root_after_success",
        "BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS",
        "p5d3f_temp_root",
        "p5d3f_success_result",
    )
    for token in required:
        if token not in source:
            raise GovernedRunError(
                "required recovery surface missing: "
                + token
            )

    forbidden = (
        "execute_finite_live_publication",
        "PROMOTION_CONFIRMED",
        "STAGE_A",
        "STAGE_B",
        "os.replace(",
        "threading.Thread",
        "while True",
        "schtasks",
        "CreateService",
        '"BLOCKED_TEMPORARY_CLEANUP"',
    )
    hits = [
        token
        for token in forbidden
        if token in source
    ]
    if hits:
        raise GovernedRunError(
            "forbidden or stale surface present: "
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
        "=== P5-D3F PERSISTENT HANDOFF RECOVERY "
        "IMPLEMENTATION V0.3 SYNTHETIC RE-BREAK ==="
    )
    print(
        "=== SYNTHETIC ONLY — NO PERSISTENT STAGING / "
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
        "avant recovery implementation re-break",
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
        "fetch recovery implementation branch failed",
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
            "persistent_production_handoff.py"
        ): EXPECTED_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_handoff_recovery_implementation_v0_3.py"
        ): EXPECTED_TESTS_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_2.json"
        ): EXPECTED_RECOVERY_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_1.json"
        ): EXPECTED_V01_CONTRACT_BLOB,
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
        "P5D3F_RECOVERY_IMPLEMENTATION_BLOBS=PASS"
    )

    _static_surface_scan(repo)
    print(
        "P5D3F_RECOVERY_IMPLEMENTATION_SURFACE_SCAN=PASS"
    )

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-RECOVERY-IMPLEMENTATION-PYCACHE"
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

    compile_result = _run(
        sys.executable,
        "-m",
        "py_compile",
        "tools/obsidian_projection/"
        "persistent_production_handoff.py",
        "tests/obsidian_projection/"
        "test_p5d3f_persistent_handoff_recovery_implementation_v0_3.py",
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "recovery implementation py_compile failed",
    )
    print(
        "P5D3F_RECOVERY_IMPLEMENTATION_PY_COMPILE=PASS"
    )

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_handoff_recovery_implementation_v0_3",
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
        "recovery implementation targeted tests failed",
    )
    print(
        "P5D3F_RECOVERY_IMPLEMENTATION_TARGETED=PASS"
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
        "P5D3F_RECOVERY_IMPLEMENTATION_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après recovery implementation re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3F_RECOVERY_IMPLEMENTATION_REBREAK_COMPLETED=PASS"
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

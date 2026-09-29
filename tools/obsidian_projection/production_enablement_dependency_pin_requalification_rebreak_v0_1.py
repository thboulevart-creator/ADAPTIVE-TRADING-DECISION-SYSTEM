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
    "feat/obsidian-projection-p5d3g-production-enablement-"
    "dependency-pin-requalification-v0.1"
)
EXPECTED_AMENDMENT_BLOB = (
    "6f938414059b2bde425ea17febfbb77635fd91e5"
)
EXPECTED_PRODUCTION_ENABLEMENT_BLOB = (
    "a9c0b46e5e623d765811d6d9b7766f172ca817a6"
)
EXPECTED_REQUAL_TEST_BLOB = (
    "95b5c77c36b261c61b80a9e19ec95e5edcb00658"
)
EXPECTED_HISTORICAL_CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)
EXPECTED_HISTORICAL_TEST_BLOB = (
    "5a05ac5fccaf7032248f35f8fd2933d5943b100c"
)
EXPECTED_HISTORICAL_REBREAK_BLOB = (
    "1c126f27d7a48ec44cbfc6e7eafe056dd5a9cefb"
)
EXPECTED_CONTRACT_TEST_BLOB = (
    "12873436d6354ffa454253cdf754023378d35076"
)
EXPECTED_LIVE_PUBLICATION_BLOB = (
    "2fb34e1c04b4dd32d19b85b488d89f8a702204d0"
)
EXPECTED_UPSTREAM_REQUAL_CONTRACT_BLOB = (
    "734aa3e0242af39263e558750d1c3b4b957f0db2"
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
        f"cannot resolve committed blob: {relative}",
    )
    return _stdout(result)

def _static_surface_scan(repo: Path) -> None:
    source = (
        repo
        / "tools"
        / "obsidian_projection"
        / "production_enablement.py"
    ).read_text(encoding="utf-8")

    required = (
        'QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (',
        '"b8875f8973ddf1076ff20d8e725ce04abbb814a8"',
        'EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB = (',
        '"2fb34e1c04b4dd32d19b85b488d89f8a702204d0"',
        'PRODUCTION_ENABLEMENT_PIN_REQUALIFICATION_CONTRACT_BLOB = (',
        '"6f938414059b2bde425ea17febfbb77635fd91e5"',
        '"production_enablement_dependency_pin_requalification_contract_v0_1.json"',
        '): EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,',
        ') != EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB:',
        '"qualified_live_publication_implementation_blob":',
        'EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,',
    )
    for token in required:
        if token not in source:
            raise GovernedRunError(
                "required requalification surface missing: "
                + token
            )

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
        "DEPENDENCY PIN REQUALIFICATION V0.1 ==="
    )
    print(
        "=== SYNTHETIC ONLY — NO REAL VAULT ACCESS / "
        "NO STAGE-B / NO PRODUCTION EXECUTION ==="
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
        "avant production-enablement dependency-pin re-break",
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
        "fetch requalification branch failed",
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
    if fetched_head != args.expected_remote_head:
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
            "LOCAL_HEAD_MISMATCH"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "production_enablement_dependency_pin_requalification_contract_v0_1.json"
        ): EXPECTED_AMENDMENT_BLOB,
        (
            "tools/obsidian_projection/"
            "production_enablement.py"
        ): EXPECTED_PRODUCTION_ENABLEMENT_BLOB,
        (
            "tests/obsidian_projection/"
            "test_production_enablement_dependency_pin_requalification_v0_1.py"
        ): EXPECTED_REQUAL_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "production_enablement_gate_contract_v0_1.json"
        ): EXPECTED_HISTORICAL_CONTRACT_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3g_production_enablement.py"
        ): EXPECTED_HISTORICAL_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3g_production_enablement_implementation_rebreak.py"
        ): EXPECTED_HISTORICAL_REBREAK_BLOB,
        (
            "tests/obsidian_projection/"
            "test_production_enablement_gate_contract_v0_1.py"
        ): EXPECTED_CONTRACT_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "live_publication_transaction.py"
        ): EXPECTED_LIVE_PUBLICATION_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3g_downstream_dependency_pin_requalification_contract_v0_1.json"
        ): EXPECTED_UPSTREAM_REQUAL_CONTRACT_BLOB,
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
        "PRODUCTION_ENABLEMENT_REQUALIFICATION_BLOBS=PASS"
    )

    _static_surface_scan(repo)
    print(
        "PRODUCTION_ENABLEMENT_REQUALIFICATION_SURFACE_SCAN=PASS"
    )
    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3G-PRODUCTION-ENABLEMENT-PIN-REQUAL-PYCACHE"
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
        "production_enablement.py",
        "tests/obsidian_projection/"
        "test_production_enablement_dependency_pin_requalification_v0_1.py",
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "production-enablement requalification py_compile failed",
    )
    print(
        "PRODUCTION_ENABLEMENT_REQUALIFICATION_PY_COMPILE=PASS"
    )

    targeted = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        "tests.obsidian_projection."
        "test_production_enablement_dependency_pin_requalification_v0_1",
        "tests.obsidian_projection."
        "test_p5d3g_production_enablement",
        "tests.obsidian_projection."
        "test_production_enablement_gate_contract_v0_1",
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
        "production-enablement requalification targeted tests failed",
    )
    print(
        "PRODUCTION_ENABLEMENT_REQUALIFICATION_TARGETED=PASS"
    )

    _require_clean(
        repo,
        "après production-enablement dependency-pin re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "PRODUCTION_ENABLEMENT_DEPENDENCY_PIN_REQUALIFICATION_REBREAK_COMPLETED=PASS"
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

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
    "feat/obsidian-projection-p5d3f-persistent-destination-"
    "verifier-amendment-implementation-v0.1"
)

EXPECTED_CONTRACT_BLOB = (
    "7d13922e51256f2785af4e6d3062116b2bc324d6"
)
EXPECTED_CONTRACT_TESTS_BLOB = (
    "720470db3dc65d9e335139749a8aebdd0e1ca3d6"
)
EXPECTED_RED_TESTS_BLOB = (
    "fa421e6c14f7ebf53cc53170a8aaf9f3821acd0b"
)
EXPECTED_VERIFIER_BLOB = (
    "65edda8427744c0ed8b8dfa7ae0333d474b8c00d"
)
EXPECTED_HANDOFF_BLOB = (
    "cb8dd498fbc503acfcccb38799965c8139db82a7"
)
EXPECTED_IMPLEMENTATION_TESTS_BLOB = (
    "d6e21a492eddfc57a0fcbdd2acbb3d3548882c10"
)
EXPECTED_HISTORICAL_HANDOFF_TESTS_BLOB = (
    "5a388914e3bbb43684373f4e3d03cdec9d16e43d"
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
    verifier = (
        repo
        / "tools"
        / "obsidian_projection"
        / "candidate_generation_staging.py"
    ).read_text(encoding="utf-8")

    handoff = (
        repo
        / "tools"
        / "obsidian_projection"
        / "p5d3f_promotion_handoff.py"
    ).read_text(encoding="utf-8")

    required_verifier = (
        "def verify_candidate_generation(",
        "package root must be below OS temp root",
        "def verify_persistent_candidate_generation(",
        "authorized_staging_root",
        "def _verify_candidate_generation_content(",
        "persistent package wrapper layout mismatch",
        "persistent wrapper generation ID mismatch",
        "_assert_lexical_ancestor_chain_no_alias(",
        "_assert_tree_has_no_aliases(root)",
    )
    for token in required_verifier:
        if token not in verifier:
            raise GovernedRunError(
                "required verifier surface missing: "
                + token
            )

    if verifier.count(
        "def _verify_candidate_generation_content("
    ) != 1:
        raise GovernedRunError(
            "shared candidate verification core count mismatch"
        )

    required_handoff = (
        "verify_candidate_generation,",
        "verify_persistent_candidate_generation,",
        "verify_persistent_candidate_generation(",
        "authorized_staging_root=staging",
        "promotion_staging_root=staging",
        "source/destination verifier descriptors differ",
        "source/destination package byte-tree digest differs",
    )
    for token in required_handoff:
        if token not in handoff:
            raise GovernedRunError(
                "required P5-D3F binding missing: "
                + token
            )

    forbidden = (
        "execute_finite_live_publication",
        "consume_stage_a_plan_approval",
        "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
        "threading.Thread",
        "schtasks",
        "CreateService",
    )
    hits = [
        token
        for token in forbidden
        if token in verifier or token in handoff
    ]
    if hits:
        raise GovernedRunError(
            "forbidden later-authority surface present: "
            + ", ".join(hits)
        )


def _run_tests(
    repo: Path,
    env: dict[str, str],
    *modules: str,
) -> None:
    result = _run(
        sys.executable,
        "-B",
        "-m",
        "unittest",
        *modules,
        "-v",
        cwd=repo,
        env=env,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(
            result.stderr,
            end="",
            file=sys.stderr,
        )

    _require_ok(
        result,
        "targeted amendment tests failed",
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
        "=== P5-D3F PERSISTENT DESTINATION VERIFIER "
        "AMENDMENT V0.1 RE-BREAK ==="
    )
    print(
        "=== SYNTHETIC ONLY — NO REAL PERSISTENT HANDOFF / "
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
        "avant persistent verifier amendment re-break",
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
        "fetch implementation branch failed",
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

    if _stdout(fetched) != (
        args.expected_remote_head
    ):
        raise GovernedRunError(
            "REMOTE_RACE_GUARD: "
            f"attendu {args.expected_remote_head}, "
            f"reçu {_stdout(fetched)}"
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
            "persistent_destination_verifier_amendment_contract_v0_1.json"
        ): EXPECTED_CONTRACT_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_destination_verifier_amendment_contract_v0_1.py"
        ): EXPECTED_CONTRACT_TESTS_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_destination_verifier_amendment_red_v0_1.py"
        ): EXPECTED_RED_TESTS_BLOB,
        (
            "tools/obsidian_projection/"
            "candidate_generation_staging.py"
        ): EXPECTED_VERIFIER_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3f_promotion_handoff.py"
        ): EXPECTED_HANDOFF_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_destination_verifier_amendment_implementation_v0_1.py"
        ): EXPECTED_IMPLEMENTATION_TESTS_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_promotion_handoff.py"
        ): EXPECTED_HISTORICAL_HANDOFF_TESTS_BLOB,
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
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_BLOBS=PASS"
    )

    _static_surface_scan(repo)
    print(
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_SURFACE_SCAN=PASS"
    )

    pycache = (
        Path(tempfile.gettempdir())
        / "ATDS-P5D3F-PERSISTENT-VERIFIER-AMENDMENT-PYCACHE"
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
        "candidate_generation_staging.py",
        "tools/obsidian_projection/"
        "p5d3f_promotion_handoff.py",
        "tests/obsidian_projection/"
        "test_p5d3f_persistent_destination_verifier_amendment_implementation_v0_1.py",
        cwd=repo,
        env=env,
    )
    _require_ok(
        compile_result,
        "amendment py_compile failed",
    )
    print(
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_PY_COMPILE=PASS"
    )

    _run_tests(
        repo,
        env,
        "tests.obsidian_projection."
        "test_p5d3f_persistent_destination_verifier_amendment_contract_v0_1",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_destination_verifier_amendment_red_v0_1",
        "tests.obsidian_projection."
        "test_p5d3f_persistent_destination_verifier_amendment_implementation_v0_1",
        "tests.obsidian_projection."
        "test_p5d3f_promotion_handoff",
    )

    print(
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_TARGETED=PASS"
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
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_FULL_REBREAK=PASS"
    )

    _require_clean(
        repo,
        "après persistent verifier amendment re-break",
    )
    print("CONTROL_CLONE_CLEAN=PASS")
    print(
        "P5D3F_PERSISTENT_VERIFIER_AMENDMENT_REBREAK_COMPLETED=PASS"
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

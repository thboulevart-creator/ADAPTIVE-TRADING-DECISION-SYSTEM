from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from tools.obsidian_projection.persistent_production_handoff import (
    PERSISTENT_STAGING,
    REAL_VAULT,
    execute_persistent_production_handoff,
    validate_persistent_paths,
    validate_staging_prestate,
)


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
RUNNER_BRANCH = (
    "feat/obsidian-projection-p5d3f-persistent-production-handoff-real-execution-v0.1"
)
EXPECTED_IMPLEMENTATION_BLOB = (
    "d2f40c8b2c8fb06b37bb34442c59d78222046452"
)
EXPECTED_TEST_BLOB = (
    "7da1fadeb1b3e9efee54b7ca09f0735277af345c"
)
EXPECTED_GATE_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
EXPECTED_QUALIFIED_P5D3F_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
)

AUTHORIZATION_LITERAL = (
    "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF"
)

OID40 = re.compile(r"^[0-9a-f]{40}$")
RUNNER_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3f_persistent_production_handoff_real_execution.py"
)


class RealExecutionRunnerError(RuntimeError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    *args: str,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )


def _git(
    repo: Path,
    *args: str,
) -> str:
    result = _run(
        "git",
        *args,
        cwd=repo,
    )
    if result.returncode != 0:
        details = (
            (result.stderr or "").strip()
            or (result.stdout or "").strip()
        )
        raise RealExecutionRunnerError(
            "git command failed"
            + (f": {details}" if details else "")
        )
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
        raise RealExecutionRunnerError(
            f"unsupported origin form: {origin}"
        )

    if value.endswith(".git"):
        value = value[:-4]

    return value.strip("/")


def _require_clean(repo: Path) -> None:
    dirty = _git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    if dirty:
        raise RealExecutionRunnerError(
            "BLOCKED_CONTROL_CLONE_DIRTY: "
            + dirty
        )


def _committed_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "rev-parse",
        f"HEAD:{relative}",
    )


def _worktree_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "hash-object",
        "--no-filters",
        relative,
    )


def _verify_exact_runtime(
    repo: Path,
    expected_runner_head: str,
    expected_runner_blob: str,
) -> None:
    if _normalize_origin(
        _git(
            repo,
            "remote",
            "get-url",
            "origin",
        )
    ) != EXPECTED_REPOSITORY:
        raise RealExecutionRunnerError(
            "repository identity mismatch"
        )

    _require_clean(repo)

    local_head = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    if local_head != expected_runner_head:
        raise RealExecutionRunnerError(
            "local HEAD is not the authorized runner HEAD"
        )

    _git(
        repo,
        "fetch",
        "--no-tags",
        "origin",
        RUNNER_BRANCH,
    )
    fetched = _git(
        repo,
        "rev-parse",
        "FETCH_HEAD",
    )
    if fetched != expected_runner_head:
        raise RealExecutionRunnerError(
            "BLOCKED_RUNNER_REMOTE_HEAD_RACE"
        )

    if _committed_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner committed blob mismatch"
        )

    if _worktree_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner worktree blob mismatch"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff.py"
        ): EXPECTED_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_production_handoff.py"
        ): EXPECTED_TEST_BLOB,
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
            raise RealExecutionRunnerError(
                "qualified blob mismatch: "
                + relative
            )


def _snapshot_staging_residual(
    staging: Path,
) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "path": str(staging),
        "exists": False,
        "state": "ABSENT",
        "entries": [],
    }

    try:
        if not staging.exists():
            return snapshot

        snapshot["exists"] = True

        if not staging.is_dir():
            snapshot["state"] = (
                "PRESENT_NON_DIRECTORY"
            )
            return snapshot

        rows: list[dict[str, object]] = []
        for path in sorted(
            staging.rglob("*"),
            key=lambda p: p.relative_to(
                staging
            ).as_posix(),
        ):
            relative = path.relative_to(
                staging
            ).as_posix()

            try:
                if path.is_dir():
                    rows.append(
                        {
                            "path": relative,
                            "type": "DIRECTORY",
                        }
                    )
                elif path.is_file():
                    info = path.stat()
                    rows.append(
                        {
                            "path": relative,
                            "type": "FILE",
                            "size": int(
                                info.st_size
                            ),
                        }
                    )
                else:
                    rows.append(
                        {
                            "path": relative,
                            "type": "OTHER",
                        }
                    )
            except OSError as exc:
                rows.append(
                    {
                        "path": relative,
                        "type": "UNREADABLE",
                        "error_type":
                            type(exc).__name__,
                        "error": str(exc),
                    }
                )

        snapshot["entries"] = rows
        snapshot["state"] = (
            "PRESENT_EMPTY"
            if not rows
            else "PRESENT_NONEMPTY"
        )
        return snapshot

    except Exception as exc:
        snapshot["state"] = (
            "SNAPSHOT_UNAVAILABLE"
        )
        snapshot["snapshot_error_type"] = (
            type(exc).__name__
        )
        snapshot["snapshot_error"] = str(exc)
        return snapshot

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-runner-head",
        required=True,
    )
    parser.add_argument(
        "--expected-runner-blob",
        required=True,
    )
    parser.add_argument(
        "--authorization",
        required=True,
    )
    args = parser.parse_args()

    if OID40.fullmatch(
        args.expected_runner_head
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-head"
        )

    if OID40.fullmatch(
        args.expected_runner_blob
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-blob"
        )

    if args.authorization != (
        AUTHORIZATION_LITERAL
    ):
        raise RealExecutionRunnerError(
            "explicit one-shot human authorization literal missing"
        )

    repo = _repo_root()

    print(
        "=== P5-D3F PERSISTENT PRODUCTION HANDOFF "
        "REAL EXECUTION ==="
    )
    print(
        "AUTHORITY=ONE_FINITE_READY_UNAUTHORIZED_HANDOFF_ONLY"
    )
    print(
        "REAL_VAULT_WRITE_AUTHORIZED=FALSE"
    )
    print(
        "LIVE_PUBLICATION_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_A_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_B_AUTHORIZED=FALSE"
    )

    _verify_exact_runtime(
        repo,
        args.expected_runner_head,
        args.expected_runner_blob,
    )
    print(
        "P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS"
    )

    staging, vault = (
        validate_persistent_paths()
    )

    if staging != PERSISTENT_STAGING.resolve(
        strict=False
    ):
        raise RealExecutionRunnerError(
            "persistent staging identity mismatch"
        )

    if vault != REAL_VAULT.resolve(
        strict=True
    ):
        raise RealExecutionRunnerError(
            "real Vault identity mismatch"
        )

    prestate = validate_staging_prestate(
        staging
    )
    print(
        "P5D3F_PERSISTENT_STAGING_PRESTATE="
        + prestate
    )

    try:
        result = execute_persistent_production_handoff(
            control_repo=repo,
        )
    except Exception as original_exc:
        residual = _snapshot_staging_residual(
            staging
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_ORIGINAL="
            + type(original_exc).__name__
            + ": "
            + str(original_exc),
            file=sys.stderr,
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON="
            + json.dumps(
                residual,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        raise

    if result.get("status") != (
        "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED"
    ):
        raise RealExecutionRunnerError(
            "unexpected persistent handoff status"
        )
    if result.get(
        "publication_authorized"
    ) is not False:
        raise RealExecutionRunnerError(
            "publication authority unexpectedly true"
        )
    if result.get(
        "live_publication_executed"
    ) is not False:
        raise RealExecutionRunnerError(
            "live publication unexpectedly executed"
        )
    if result.get(
        "mandatory_stop"
    ) is not True:
        raise RealExecutionRunnerError(
            "mandatory STOP missing"
        )

    zero = result.get(
        "zero_mutation_proof"
    )
    if (
        not isinstance(zero, dict)
        or zero.get("unchanged") is not True
        or zero.get("status")
        != "PASS_REAL_VAULT_ZERO_MUTATION"
    ):
        raise RealExecutionRunnerError(
            "real Vault zero-mutation proof missing"
        )

    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION=PASS"
    )
    print(
        "REAL_VAULT_ZERO_MUTATION=PASS"
    )
    print(
        "LIVE_PUBLICATION_EXECUTED=FALSE"
    )
    print(
        "MANDATORY_STOP=TRUE"
    )
    print(
        "RESULT_JSON="
        + json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    )

    _require_clean(repo)
    print(
        "CONTROL_CLONE_CLEAN=PASS"
    )
    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION_COMPLETED=PASS"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        RealExecutionRunnerError,
        Exception,
    ) as exc:
        if isinstance(
            exc,
            KeyboardInterrupt,
        ):
            raise
        print(
            f"BLOCKED: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)

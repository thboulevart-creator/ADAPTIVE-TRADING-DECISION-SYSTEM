from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from .finite_candidate_evaluator import (
    FiniteCandidateEvaluatorError,
    evaluate_candidate_finitely,
)
from .observer_tick import (
    INPUT_SCHEMA,
    make_initial_state,
    one_shot_tick,
)


REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3D_SYNTHETIC_QUALIFICATION_REPORT_V0_1"
)
BLOCKED_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3D_SYNTHETIC_QUALIFICATION_BLOCKED_V0_1"
)
FAIL_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3D_SYNTHETIC_QUALIFICATION_FAIL_V0_1"
)
EXPECTED_ORIGIN = (
    "https://github.com/thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM.git"
)


class SyntheticQualificationError(RuntimeError):
    pass


class SyntheticQualificationBlockedError(
    SyntheticQualificationError
):
    pass


def _git(
    repo: Path,
    *args: str,
) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    except (
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        raise SyntheticQualificationBlockedError(
            "synthetic Git fixture unavailable"
        ) from exc
    return completed.stdout.strip()


def _write(
    path: Path,
    data: bytes,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with path.open("xb") as handle:
        handle.write(data)


def _build_synthetic_repo(
    root: Path,
) -> tuple[str, str]:
    root.mkdir()
    _git(root, "init")
    _git(
        root,
        "config",
        "user.email",
        "p5d3d@example.invalid",
    )
    _git(
        root,
        "config",
        "user.name",
        "P5-D3D Synthetic Fixture",
    )
    _git(
        root,
        "remote",
        "add",
        "origin",
        EXPECTED_ORIGIN,
    )

    _write(
        root / "docs" / "source.md",
        (
            b"# Source\n\n"
            b"Binary target: \x60assets/blob.bin\x60\n"
        ),
    )
    _write(
        root / "data" / "refs.json",
        b'{"reference":"docs/source.md"}\n',
    )
    _write(
        root / "src" / "code.py",
        b"VALUE = 1\n",
    )
    _write(
        root / "assets" / "blob.bin",
        b"\x00\x01\x02\x03",
    )

    _git(root, "add", "--all")
    _git(
        root,
        "commit",
        "-m",
        "p5d3d synthetic fixture",
    )

    head = _git(
        root,
        "rev-parse",
        "HEAD",
    )
    tree = _git(
        root,
        "rev-parse",
        "HEAD^{tree}",
    )
    return head, tree


def _activation(
    candidate_head: str,
) -> dict:
    state = make_initial_state()

    observed = one_shot_tick(
        state,
        {
            "schema": INPUT_SCHEMA,
            "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1,
            "observed_head": candidate_head,
            "transition_class": "INITIAL",
            "candidate_head": None,
            "failure_code": None,
        },
    )

    return one_shot_tick(
        observed["next_state"],
        {
            "schema": INPUT_SCHEMA,
            "event_type": "EVALUATION_STARTED",
            "sequence": 2,
            "observed_head": None,
            "transition_class": None,
            "candidate_head": candidate_head,
            "failure_code": None,
        },
    )


def _load_json(
    path: Path,
) -> dict:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8")
        )
    except (
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise SyntheticQualificationError(
            "generated JSON evidence unreadable"
        ) from exc
    if not isinstance(value, dict):
        raise SyntheticQualificationError(
            "generated JSON evidence must be object"
        )
    return value


def run_synthetic_qualification(
    *,
    forbidden_roots: tuple[Path, ...] = (),
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(
        prefix="atds-p5d3d-synthetic-"
    ) as temp:
        root = Path(temp)
        repo = root / "candidate-repo"
        workspace = root / "evaluation-workspace"

        head, tree = _build_synthetic_repo(
            repo
        )
        workspace.mkdir()

        activation = _activation(
            head
        )

        report = evaluate_candidate_finitely(
            activation_tick_result=activation,
            candidate_tree=tree,
            candidate_repo_root=repo,
            evaluation_workspace_root=workspace,
            forbidden_roots=forbidden_roots,
        )

        if report["outcome"] == "BLOCKED":
            raise SyntheticQualificationBlockedError(
                "synthetic control evaluation blocked"
            )
        if report["outcome"] != "QUALIFIED":
            raise SyntheticQualificationError(
                "synthetic control candidate did not qualify"
            )
        if not report[
            "p5d2_result_event_emitted"
        ]:
            raise SyntheticQualificationError(
                "QUALIFIED did not emit P5-D2 result event"
            )
        if report["failure_code"] is not None:
            raise SyntheticQualificationError(
                "QUALIFIED carries failure code"
            )
        if report[
            "candidate_generation_verification_status"
        ] != "PASS_SEALED_UNPROMOTED":
            raise SyntheticQualificationError(
                "synthetic package did not verify"
            )
        if (
            report["live_projection_head_before"]
            != report["live_projection_head_after"]
        ):
            raise SyntheticQualificationError(
                "finite evaluation changed live projection"
            )
        if (
            report["real_vault_modified"]
            or report["current_pointer_created"]
            or report[
                "production_promotion_authorized"
            ]
        ):
            raise SyntheticQualificationError(
                "forbidden authority or mutation reported"
            )

        build_a_manifest = _load_json(
            workspace
            / "build-a"
            / "generated"
            / "manifests"
            / "build-manifest.json"
        )
        build_b_manifest = _load_json(
            workspace
            / "build-b"
            / "generated"
            / "manifests"
            / "build-manifest.json"
        )

        expected_counts = {
            "source_record_count": 4,
            "full_text_count": 3,
            "metadata_only_count": 1,
            "artifact_record_count": 4,
            "relation_record_count": 2,
            "relation_source_body_read_count": 2,
            "metadata_only_body_read_count": 0,
        }

        for manifest in (
            build_a_manifest,
            build_b_manifest,
        ):
            for key, value in expected_counts.items():
                if manifest.get(key) != value:
                    raise SyntheticQualificationError(
                        f"unexpected synthetic build count: {key}"
                    )
            if (
                "pilot_inventory_digest_sha256"
                in manifest
                or "pilot_source_count"
                in manifest
            ):
                raise SyntheticQualificationError(
                    "pilot identity leaked into current-head build"
                )

        if (
            report["projection_a_tree_digest_sha256"]
            != report["projection_b_tree_digest_sha256"]
        ):
            raise SyntheticQualificationError(
                "A/B projection digests differ"
            )

        package = (
            workspace
            / "candidate-package"
        )
        forbidden_names = {
            "CURRENT",
            "CURRENT.md",
            "CURRENT.json",
            "CURRENT.tmp",
            ".obsidian",
            "views",
            ".git",
        }
        for item in package.rglob("*"):
            if item.name in forbidden_names:
                raise SyntheticQualificationError(
                    "forbidden package surface exists"
                )

        return {
            "schema": REPORT_SCHEMA,
            "status":
                "PASS_SYNTHETIC_FINITE_EVALUATION",
            "outcome": report["outcome"],
            "candidate_generation_verification_status":
                report[
                    "candidate_generation_verification_status"
                ],
            "projection_a_equals_b": (
                report[
                    "projection_a_tree_digest_sha256"
                ]
                == report[
                    "projection_b_tree_digest_sha256"
                ]
            ),
            "source_record_count": 4,
            "full_text_count": 3,
            "metadata_only_count": 1,
            "artifact_record_count": 4,
            "relation_record_count": 2,
            "relation_source_body_read_count": 2,
            "metadata_only_body_read_count": 0,
            "p5d2_result_event_emitted": (
                report[
                    "p5d2_result_event_emitted"
                ]
            ),
            "live_projection_head_unchanged": (
                report[
                    "live_projection_head_before"
                ]
                == report[
                    "live_projection_head_after"
                ]
            ),
            "real_vault_modified": False,
            "current_pointer_created": False,
            "production_promotion_authorized":
                False,
            "network_fetch_performed": False,
            "real_candidate_evaluated": False,
            "synthetic_repository_retained": False,
            "synthetic_workspace_retained": False,
        }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "P5-D3D synthetic finite-evaluator "
            "qualification harness."
        )
    )
    parser.add_argument(
        "--forbidden-root",
        action="append",
        default=[],
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    forbidden = tuple(
        Path(item)
        for item in args.forbidden_root
    )

    try:
        report = run_synthetic_qualification(
            forbidden_roots=forbidden,
        )
    except (
        SyntheticQualificationBlockedError,
        FiniteCandidateEvaluatorError,
        OSError,
    ) as exc:
        print(
            json.dumps(
                {
                    "schema": BLOCKED_SCHEMA,
                    "status":
                        "BLOCKED_SYNTHETIC_INFRASTRUCTURE",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    except SyntheticQualificationError as exc:
        print(
            json.dumps(
                {
                    "schema": FAIL_SCHEMA,
                    "status": "FAIL",
                    "error_type":
                        type(exc).__name__,
                    "error_message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

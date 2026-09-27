from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.dynamic_inventory import (
    SecretDetectedError,
)
from tools.obsidian_projection.finite_candidate_evaluator import (
    FiniteCandidateEvaluatorError,
    evaluate_candidate_finitely,
)
from tools.obsidian_projection.git_source import (
    GitSourceError,
)
from tools.obsidian_projection.observer_tick import (
    INPUT_SCHEMA,
    make_initial_state,
    one_shot_tick,
)


HEAD = "1" * 40
TREE = "2" * 40


def activation(
    candidate_head: str = HEAD,
) -> dict:
    observed = one_shot_tick(
        make_initial_state(),
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


class FiniteCandidateEvaluatorTests(
    unittest.TestCase
):
    def test_invalid_activation_is_rejected_before_runtime(
        self,
    ) -> None:
        tick = activation()
        mutant = copy.deepcopy(tick)
        mutant["decision"]["action"] = "NOOP"

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-eval-invalid-"
        ) as temp:
            root = Path(temp)
            repo = root / "repo"
            workspace = root / "workspace"
            repo.mkdir()
            workspace.mkdir()

            with self.assertRaises(
                FiniteCandidateEvaluatorError
            ):
                evaluate_candidate_finitely(
                    activation_tick_result=mutant,
                    candidate_tree=TREE,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                )

    def test_repository_unavailable_is_blocked_without_p5d2_event(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-eval-blocked-"
        ) as temp:
            root = Path(temp)
            repo = root / "repo"
            workspace = root / "workspace"
            repo.mkdir()
            workspace.mkdir()

            with patch(
                "tools.obsidian_projection."
                "finite_candidate_evaluator."
                "FrozenGitSource.verify_repository",
                side_effect=GitSourceError(
                    "synthetic unavailable"
                ),
            ):
                report = evaluate_candidate_finitely(
                    activation_tick_result=activation(),
                    candidate_tree=TREE,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                )

        self.assertEqual(
            report["outcome"],
            "BLOCKED",
        )
        self.assertEqual(
            report["failure_code"],
            "ISOLATED_CANDIDATE_REPOSITORY_UNAVAILABLE",
        )
        self.assertFalse(
            report["p5d2_result_event_emitted"]
        )
        self.assertIsNone(
            report["p5d2_result_tick_digest_sha256"]
        )
        self.assertEqual(
            report["live_projection_head_before"],
            report["live_projection_head_after"],
        )

    def test_secret_detection_rejects_and_emits_failure_event(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-eval-rejected-"
        ) as temp:
            root = Path(temp)
            repo = root / "repo"
            workspace = root / "workspace"
            repo.mkdir()
            workspace.mkdir()

            with (
                patch(
                    "tools.obsidian_projection."
                    "finite_candidate_evaluator."
                    "FrozenGitSource.verify_repository",
                    return_value=None,
                ),
                patch(
                    "tools.obsidian_projection."
                    "finite_candidate_evaluator."
                    "FrozenGitSource.verify_frozen_source",
                    return_value=None,
                ),
                patch(
                    "tools.obsidian_projection."
                    "finite_candidate_evaluator."
                    "build_from_repository",
                    side_effect=SecretDetectedError(
                        "synthetic secret"
                    ),
                ),
            ):
                report = evaluate_candidate_finitely(
                    activation_tick_result=activation(),
                    candidate_tree=TREE,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                )

        self.assertEqual(
            report["outcome"],
            "REJECTED",
        )
        self.assertEqual(
            report["failure_code"],
            "DYNAMIC_INVENTORY_INVALID",
        )
        self.assertTrue(
            report["p5d2_result_event_emitted"]
        )
        self.assertIsNotNone(
            report["p5d2_result_tick_digest_sha256"]
        )
        self.assertEqual(
            report["live_projection_head_before"],
            report["live_projection_head_after"],
        )
        self.assertFalse(
            report["production_promotion_authorized"]
        )
        self.assertFalse(
            report["current_pointer_created"]
        )

    def test_workspace_must_be_os_temp_and_separate(
        self,
    ) -> None:
        tick = activation()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-eval-workspace-"
        ) as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()

            with self.assertRaises(
                FiniteCandidateEvaluatorError
            ):
                evaluate_candidate_finitely(
                    activation_tick_result=tick,
                    candidate_tree=TREE,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=repo,
                )


if __name__ == "__main__":
    unittest.main()

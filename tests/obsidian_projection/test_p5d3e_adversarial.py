from __future__ import annotations

import inspect
import unittest

from tools.obsidian_projection import p5d3e_verify


class P5D3EAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = inspect.getsource(
            p5d3e_verify
        )

    def test_no_production_promotion_surface(self) -> None:
        for forbidden in (
            "promotion_experiment",
            "PROMOTION_CONFIRMED",
            "_write_pointer",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.source,
                )

    def test_no_current_pointer_write_surface(self) -> None:
        for forbidden in (
            'open("CURRENT", "w"',
            "write_text(\"CURRENT",
            "replace(CURRENT",
            "_write_pointer",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.source,
                )

    def test_no_network_client_library(self) -> None:
        for forbidden in (
            "requests",
            "urllib",
            "http.client",
            "socket.",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.source,
                )

    def test_clone_requires_no_hardlinks_and_no_checkout(self) -> None:
        self.assertIn(
            '"--no-hardlinks"',
            self.source,
        )
        self.assertIn(
            '"--no-checkout"',
            self.source,
        )

    def test_candidate_checkout_is_detached(self) -> None:
        self.assertIn(
            '"checkout"',
            self.source,
        )
        self.assertIn(
            '"--detach"',
            self.source,
        )

    def test_alternates_are_explicitly_rejected(self) -> None:
        for required in (
            '"objects"',
            '"info"',
            '"alternates"',
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.source,
                )

    def test_origin_is_restored_to_canonical_github(self) -> None:
        self.assertIn(
            '"remote"',
            self.source,
        )
        self.assertIn(
            '"set-url"',
            self.source,
        )
        self.assertIn(
            '"origin"',
            self.source,
        )
        self.assertIn(
            "CANONICAL_ORIGIN",
            self.source,
        )

    def test_real_vault_is_fingerprinted_before_and_after(self) -> None:
        self.assertGreaterEqual(
            self.source.count("_tree_fingerprint("),
            3,
        )

    def test_qualified_p5d3d_evaluator_is_called(self) -> None:
        self.assertIn(
            "evaluate_candidate_finitely(",
            self.source,
        )

    def test_candidate_package_is_reverified(self) -> None:
        self.assertIn(
            "verify_candidate_generation(",
            self.source,
        )

    def test_remote_tracking_ref_is_exact(self) -> None:
        self.assertIn(
            'REMOTE_TRACKING_REF = (',
            self.source,
        )
        self.assertIn(
            "refs/remotes/origin/integration/system-v1",
            self.source,
        )

    def test_real_success_requires_network_resolution_and_real_candidate(self) -> None:
        self.assertIn(
            "candidate_resolution_network_fetch_performed",
            self.source,
        )
        self.assertIn(
            "real_candidate_evaluated",
            self.source,
        )
        self.assertIn(
            "PASS_REAL_EXACT_HEAD_FINITE_EVALUATION",
            self.source,
        )

    def test_rejected_and_blocked_have_distinct_statuses(self) -> None:
        self.assertIn(
            "FAIL_REAL_CANDIDATE_REJECTED",
            self.source,
        )
        self.assertIn(
            "BLOCKED_REAL_EXACT_HEAD_EVALUATION",
            self.source,
        )

    def test_no_background_or_polling_loop(self) -> None:
        self.assertNotIn(
            "while True",
            self.source,
        )
        self.assertNotIn(
            "time.sleep(",
            self.source,
        )

    def test_report_does_not_emit_sandbox_paths(self) -> None:
        self.assertNotIn(
            '"candidate_repo_root":',
            self.source,
        )
        self.assertNotIn(
            '"evaluation_workspace_root":',
            self.source,
        )


if __name__ == "__main__":
    unittest.main()

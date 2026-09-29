from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.observer_tick import (
    INPUT_SCHEMA,
    ObserverTickError,
    make_initial_state,
    one_shot_tick,
)
from tools.obsidian_projection.p5d3d_verify import (
    _build_synthetic_repo,
)
from tools.obsidian_projection.p5d3f_promotion_handoff import (
    _package_byte_tree_digest,
    run_finite_promotion_handoff,
)
from tools.obsidian_projection.live_publication_transaction import (
    CONTRACT_BLOB,
    REAL_VAULT,
    LivePublicationBlockedError,
    LivePublicationGovernanceError,
    build_publication_plan,
    classify_publication_recovery,
    execute_finite_live_publication,
    publication_plan_digest,
    verify_live_publication,
)


def _fingerprint(
    root: Path,
) -> tuple[tuple[str, int, str], ...]:
    rows: list[tuple[str, int, str]] = []
    for path in sorted(
        (
            p
            for p in root.rglob("*")
            if p.is_file()
        ),
        key=lambda p: p.relative_to(
            root
        ).as_posix(),
    ):
        raw = path.read_bytes()
        rows.append(
            (
                path.relative_to(
                    root
                ).as_posix(),
                len(raw),
                hashlib.sha256(
                    raw
                ).hexdigest(),
            )
        )
    return tuple(rows)


def _candidate_pending_state(
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

    started = one_shot_tick(
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

    passed = one_shot_tick(
        started["next_state"],
        {
            "schema": INPUT_SCHEMA,
            "event_type": "EVALUATION_PASSED",
            "sequence": 3,
            "observed_head": None,
            "transition_class": None,
            "candidate_head": candidate_head,
            "failure_code": None,
        },
    )
    return passed["next_state"]


def _authorization(
    plan: dict,
    *,
    nonce_suffix: str = "a",
) -> dict:
    digest = publication_plan_digest(
        plan
    )
    nonce = hashlib.sha256(
        (
            digest
            + ":"
            + nonce_suffix
        ).encode("ascii")
    ).hexdigest()

    return {
        "schema":
            "ATDS_OBSIDIAN_P5D3G_HUMAN_AUTHORIZATION_V0_1",
        "authorized_action":
            "EXECUTE_ONE_FINITE_LIVE_PUBLICATION_TRANSACTION",
        "plan_digest_sha256":
            digest,
        "candidate_head":
            plan["candidate_head"],
        "candidate_tree":
            plan["candidate_tree"],
        "generation_id":
            plan["generation_id"],
        "publication_mode":
            plan["publication_mode"],
        "expected_previous_current_state":
            plan[
                "expected_previous_current_state"
            ],
        "one_shot_nonce": nonce,
    }


class P5D3GLivePublicationImplementationTests(
    unittest.TestCase
):
    def _fixture(
        self,
        root: Path,
    ) -> dict[str, object]:
        repo = root / "candidate"
        head, tree = _build_synthetic_repo(
            repo
        )

        workspace = root / "evaluation"
        workspace.mkdir()

        staging = root / "promotion-staging"
        staging.mkdir()

        protected = root / "source-vault"
        protected.mkdir()
        (
            protected / "sentinel.txt"
        ).write_text(
            "UNCHANGED\n",
            encoding="utf-8",
        )

        handoff_report = (
            run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=protected,
            )
        )

        handoff = (
            staging
            / "packages"
            / str(
                handoff_report[
                    "generation_id"
                ]
            )
        )

        live = root / "sacrificial-live-vault"
        live.mkdir()

        control = root / "control"
        control.mkdir()

        return {
            "repo": repo,
            "head": head,
            "tree": tree,
            "handoff": handoff,
            "live": live,
            "control": control,
            "protected": protected,
        }

    def test_contract_blob_is_exact(self) -> None:
        self.assertEqual(
            CONTRACT_BLOB,
            "64997ddd9977229961387f66af4de356c045c0ac",
        )

    def test_planning_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-plan-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)

            before = _fingerprint(live)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )

            self.assertEqual(
                plan["publication_mode"],
                "BOOTSTRAP_NO_CURRENT",
            )
            self.assertEqual(
                plan[
                    "expected_previous_current_state"
                ],
                "ABSENT",
            )
            self.assertEqual(
                _fingerprint(live),
                before,
            )
            self.assertFalse(
                (live / "CURRENT.md").exists()
            )
            self.assertFalse(
                (
                    live
                    / "generations"
                ).exists()
            )

    def test_real_vault_path_is_rejected_before_publication(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-real-vault-guard-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            assert isinstance(handoff, Path)

            with self.assertRaises(
                LivePublicationGovernanceError
            ):
                build_publication_plan(
                    handoff_root=handoff,
                    live_vault_root=REAL_VAULT,
                )

    def test_missing_authorization_blocks_without_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-no-auth-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            before = _fingerprint(live)

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=None,
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

            self.assertEqual(
                _fingerprint(live),
                before,
            )

    def test_mismatched_authorization_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-bad-auth-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            auth = _authorization(plan)
            auth["candidate_head"] = "0" * 40

            with self.assertRaises(
                LivePublicationGovernanceError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=auth,
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

    def test_writer_contention_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-writer-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            auth = _authorization(plan)
            (
                control / "P5D3G-WRITER.lock"
            ).write_text(
                "occupied\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=auth,
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

    def test_successful_bootstrap_publication(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-success-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            auth = _authorization(plan)
            state = _candidate_pending_state(
                head
            )

            report = (
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=auth,
                    observer_state=state,
                )
            )

            self.assertEqual(
                report["status"],
                "PASS_LIVE_PUBLICATION_CONFIRMED",
            )
            self.assertTrue(
                report[
                    "p5d2_promotion_confirmed_emitted"
                ]
            )
            self.assertTrue(
                (live / "CURRENT.md").is_file()
            )
            self.assertFalse(
                (live / "CURRENT.tmp").exists()
            )
            self.assertFalse(
                (
                    control
                    / "P5D3G-WRITER.lock"
                ).exists()
            )

            target = (
                live
                / "generations"
                / plan["generation_id"]
            )
            self.assertTrue(
                (
                    target
                    / "PUBLICATION-MANIFEST.json"
                ).is_file()
            )
            self.assertTrue(
                (target / "INDEX.md").is_file()
            )

            verified = verify_live_publication(
                live_vault_root=live,
                expected_generation_id=(
                    plan["generation_id"]
                ),
            )
            self.assertEqual(
                verified["generation_id"],
                plan["generation_id"],
            )

    def test_materialized_package_is_byte_exact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-package-exact-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            execute_finite_live_publication(
                handoff_root=handoff,
                live_vault_root=live,
                control_root=control,
                plan=plan,
                authorization=_authorization(
                    plan
                ),
                observer_state=(
                    _candidate_pending_state(
                        head
                    )
                ),
            )

            source_digest = (
                _package_byte_tree_digest(
                    handoff / "package"
                )
            )
            copied_digest = (
                _package_byte_tree_digest(
                    live
                    / "generations"
                    / plan["generation_id"]
                    / "package"
                )
            )
            self.assertEqual(
                copied_digest,
                source_digest,
            )

    def test_authorization_is_one_shot(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-one-shot-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            auth = _authorization(plan)
            state = _candidate_pending_state(
                head
            )

            execute_finite_live_publication(
                handoff_root=handoff,
                live_vault_root=live,
                control_root=control,
                plan=plan,
                authorization=auth,
                observer_state=state,
            )

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=auth,
                    observer_state=state,
                )

    def test_current_tmp_preexistence_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-stale-tmp-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            (live / "CURRENT.tmp").write_bytes(
                b"stale\n"
            )

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=_authorization(
                        plan
                    ),
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

            self.assertFalse(
                (live / "CURRENT.md").exists()
            )

    def test_current_change_after_plan_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-current-race-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            (live / "CURRENT.md").write_text(
                "changed-after-plan\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=_authorization(
                        plan
                    ),
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

            self.assertFalse(
                (
                    live
                    / "generations"
                ).exists()
            )

    def test_target_collision_blocks_without_overwrite(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-collision-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            target = (
                live
                / "generations"
                / plan["generation_id"]
            )
            target.mkdir(
                parents=True
            )
            marker = target / "FOREIGN.txt"
            marker.write_text(
                "do-not-overwrite\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                LivePublicationBlockedError
            ):
                execute_finite_live_publication(
                    handoff_root=handoff,
                    live_vault_root=live,
                    control_root=control,
                    plan=plan,
                    authorization=_authorization(
                        plan
                    ),
                    observer_state=(
                        _candidate_pending_state(
                            head
                        )
                    ),
                )

            self.assertEqual(
                marker.read_text(
                    encoding="utf-8"
                ),
                "do-not-overwrite\n",
            )

    def test_live_publication_verifier_is_read_only(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-verify-ro-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )
            execute_finite_live_publication(
                handoff_root=handoff,
                live_vault_root=live,
                control_root=control,
                plan=plan,
                authorization=_authorization(
                    plan
                ),
                observer_state=(
                    _candidate_pending_state(
                        head
                    )
                ),
            )

            before = _fingerprint(live)
            verify_live_publication(
                live_vault_root=live,
                expected_generation_id=(
                    plan["generation_id"]
                ),
            )
            self.assertEqual(
                _fingerprint(live),
                before,
            )

    def test_logical_confirmation_failure_is_physical_pending(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-logical-pending-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )

            with patch(
                "tools.obsidian_projection."
                "live_publication_transaction."
                "one_shot_tick",
                side_effect=ObserverTickError(
                    "synthetic logical failure"
                ),
            ):
                report = (
                    execute_finite_live_publication(
                        handoff_root=handoff,
                        live_vault_root=live,
                        control_root=control,
                        plan=plan,
                        authorization=_authorization(
                            plan
                        ),
                        observer_state=(
                            _candidate_pending_state(
                                head
                            )
                        ),
                    )
                )

            self.assertEqual(
                report["status"],
                "PASS_PHYSICAL_PUBLICATION_LOGICAL_CONFIRMATION_PENDING",
            )
            self.assertFalse(
                report[
                    "p5d2_promotion_confirmed_emitted"
                ]
            )
            verified = verify_live_publication(
                live_vault_root=live,
                expected_generation_id=(
                    plan["generation_id"]
                ),
            )
            self.assertEqual(
                verified["generation_id"],
                plan["generation_id"],
            )

    def test_recovery_classifier_distinguishes_not_started_and_new_current(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-recovery-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            control = fx["control"]
            head = fx["head"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)
            assert isinstance(control, Path)
            assert isinstance(head, str)

            plan = build_publication_plan(
                handoff_root=handoff,
                live_vault_root=live,
            )

            before = classify_publication_recovery(
                live_vault_root=live,
                plan=plan,
            )
            self.assertEqual(
                before["classification"],
                "PREVIOUS_CURRENT_TARGET_ABSENT",
            )

            execute_finite_live_publication(
                handoff_root=handoff,
                live_vault_root=live,
                control_root=control,
                plan=plan,
                authorization=_authorization(
                    plan
                ),
                observer_state=(
                    _candidate_pending_state(
                        head
                    )
                ),
            )

            after = classify_publication_recovery(
                live_vault_root=live,
                plan=plan,
            )
            self.assertEqual(
                after["classification"],
                "NEW_CURRENT_TARGET_EXACT_FORWARD_COMPLETE",
            )

    def test_no_background_or_scheduler_surface(
        self,
    ) -> None:
        module_path = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "live_publication_transaction.py"
        )
        source = module_path.read_text(
            encoding="utf-8"
        )

        forbidden = (
            "while True",
            "threading.Thread",
            "schtasks",
            "CreateService",
            "schedule.",
            "polling",
            "P5-D4",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(
                    marker,
                    source,
                )


if __name__ == "__main__":
    unittest.main()

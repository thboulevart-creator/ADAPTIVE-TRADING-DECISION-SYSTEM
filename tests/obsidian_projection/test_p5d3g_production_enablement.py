from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.p5d3d_verify import (
    _build_synthetic_repo,
)
from tools.obsidian_projection.p5d3f_promotion_handoff import (
    run_finite_promotion_handoff,
)
from tools.obsidian_projection.production_enablement import (
    CONTRACT_BLOB,
    QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
    ProductionEnablementBlockedError,
    ProductionEnablementGovernanceError,
    build_real_live_publication_plan,
    consume_stage_a_plan_approval,
    production_plan_digest,
    prove_zero_real_vault_mutation,
    snapshot_real_vault,
)


def _fingerprint(root: Path) -> tuple[tuple[str, int, str], ...]:
    rows: list[tuple[str, int, str]] = []
    for path in sorted(
        (
            p
            for p in root.rglob("*")
            if p.is_file()
        ),
        key=lambda p: p.relative_to(root).as_posix(),
    ):
        raw = path.read_bytes()
        rows.append(
            (
                path.relative_to(root).as_posix(),
                len(raw),
                hashlib.sha256(raw).hexdigest(),
            )
        )
    return tuple(rows)


def _approval(plan: dict, suffix: str = "a") -> dict:
    digest = production_plan_digest(plan)
    nonce = hashlib.sha256(
        (digest + ":" + suffix).encode("ascii")
    ).hexdigest()
    return {
        "schema":
            "ATDS_OBSIDIAN_P5D3G_PRODUCTION_PLAN_APPROVAL_V0_1",
        "authorized_action":
            "APPROVE_ONE_EXACT_REAL_LIVE_PUBLICATION_PLAN_FOR_FUTURE_EXECUTION_REVIEW",
        "plan_digest_sha256": digest,
        "candidate_head": plan["candidate_head"],
        "candidate_tree": plan["candidate_tree"],
        "generation_id": plan["generation_id"],
        "publication_mode": plan["publication_mode"],
        "expected_current_state":
            plan["expected_current_state"],
        "expected_current_sha256":
            plan["expected_current_sha256"],
        "expected_current_tmp_state":
            plan["expected_current_tmp_state"],
        "expected_target_state":
            plan["expected_target_state"],
        "one_shot_nonce": nonce,
    }


class P5D3GProductionEnablementTests(
    unittest.TestCase
):
    def _fixture(
        self,
        root: Path,
    ) -> dict[str, object]:
        repo = root / "candidate"
        head, tree = _build_synthetic_repo(repo)

        workspace = root / "evaluation"
        workspace.mkdir()

        staging = root / "promotion-staging"
        staging.mkdir()

        protected = root / "source-vault"
        protected.mkdir()
        (protected / "sentinel.txt").write_text(
            "UNCHANGED\n",
            encoding="utf-8",
        )

        handoff_report = run_finite_promotion_handoff(
            candidate_head=head,
            candidate_tree=tree,
            candidate_repo_root=repo,
            evaluation_workspace_root=workspace,
            promotion_staging_root=staging,
            live_vault_root=protected,
        )

        handoff = (
            staging
            / "packages"
            / str(handoff_report["generation_id"])
        )

        live = root / "real-live-vault"
        live.mkdir()

        control = root / "control"
        control.mkdir()

        return {
            "head": head,
            "tree": tree,
            "handoff": handoff,
            "live": live,
            "control": control,
            "protected": protected,
        }

    def _build(
        self,
        fx: dict[str, object],
    ) -> dict:
        handoff = fx["handoff"]
        live = fx["live"]
        assert isinstance(handoff, Path)
        assert isinstance(live, Path)

        with patch(
            "tools.obsidian_projection."
            "production_enablement.REAL_VAULT",
            live,
        ):
            return build_real_live_publication_plan(
                handoff_root=handoff,
                real_vault_root=live,
            )

    def test_qualified_authorities_are_exact(self) -> None:
        self.assertEqual(
            CONTRACT_BLOB,
            "5de65f5d13a93d1325d53e1b58536ed0860921f2",
        )
        self.assertEqual(
            QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
            "b8875f8973ddf1076ff20d8e725ce04abbb814a8",
        )

    def test_bootstrap_plan_is_read_only_and_zero_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-plan-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            assert isinstance(live, Path)
            before = _fingerprint(live)

            result = self._build(fx)
            plan = result["plan"]
            proof = result["zero_mutation_proof"]

            self.assertEqual(
                plan["publication_mode"],
                "BOOTSTRAP_NO_CURRENT",
            )
            self.assertEqual(
                plan["expected_current_state"],
                "ABSENT",
            )
            self.assertEqual(
                plan["expected_target_state"],
                "ABSENT",
            )
            self.assertTrue(proof["unchanged"])
            self.assertEqual(before, _fingerprint(live))
            self.assertFalse(
                (live / "CURRENT.md").exists()
            )
            self.assertFalse(
                (live / "CURRENT.tmp").exists()
            )
            self.assertFalse(
                (live / "generations").exists()
            )

    def test_plan_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-determinism-"
        ) as temp:
            fx = self._fixture(Path(temp))
            first = self._build(fx)
            second = self._build(fx)
            self.assertEqual(
                first["plan"],
                second["plan"],
            )
            self.assertEqual(
                production_plan_digest(first["plan"]),
                production_plan_digest(second["plan"]),
            )

    def test_wrong_real_vault_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-wrong-root-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)

            wrong = Path(temp) / "wrong"
            wrong.mkdir()

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementGovernanceError
                ):
                    build_real_live_publication_plan(
                        handoff_root=handoff,
                        real_vault_root=wrong,
                    )

    def test_current_tmp_state_is_captured_without_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-current-tmp-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            assert isinstance(live, Path)
            (live / "CURRENT.tmp").write_text(
                "EXISTING\n",
                encoding="utf-8",
            )
            before = _fingerprint(live)

            result = self._build(fx)

            self.assertEqual(
                result["plan"][
                    "expected_current_tmp_state"
                ],
                "PRESENT",
            )
            self.assertEqual(before, _fingerprint(live))

    def test_target_collision_blocks_without_overwrite(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-target-collision-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            live = fx["live"]
            assert isinstance(handoff, Path)
            assert isinstance(live, Path)

            record = json.loads(
                (
                    handoff
                    / "PROMOTION-HANDOFF.json"
                ).read_text(encoding="utf-8")
            )
            target = (
                live
                / "generations"
                / record["generation_id"]
            )
            target.mkdir(parents=True)
            (target / "sentinel.txt").write_text(
                "UNCHANGED\n",
                encoding="utf-8",
            )
            before = _fingerprint(live)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementBlockedError
                ):
                    build_real_live_publication_plan(
                        handoff_root=handoff,
                        real_vault_root=live,
                    )

            self.assertEqual(before, _fingerprint(live))

    def test_plan_digest_rejects_cherry_picked_fields(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-plan-fields-"
        ) as temp:
            fx = self._fixture(Path(temp))
            plan = dict(self._build(fx)["plan"])
            plan.pop("expected_target_state")
            with self.assertRaises(
                ProductionEnablementGovernanceError
            ):
                production_plan_digest(plan)

    def test_missing_stage_a_approval_blocks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-missing-approval-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            control = fx["control"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)
            assert isinstance(control, Path)
            result = self._build(fx)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementBlockedError
                ):
                    consume_stage_a_plan_approval(
                        handoff_root=handoff,
                        real_vault_root=live,
                        control_root=control,
                        plan=result["plan"],
                        approval=None,
                    )

    def test_mismatched_stage_a_approval_fails(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-bad-approval-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            control = fx["control"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)
            assert isinstance(control, Path)
            plan = self._build(fx)["plan"]
            approval = _approval(plan)
            approval["candidate_head"] = "0" * 40

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementGovernanceError
                ):
                    consume_stage_a_plan_approval(
                        handoff_root=handoff,
                        real_vault_root=live,
                        control_root=control,
                        plan=plan,
                        approval=approval,
                    )

    def test_stage_a_approval_is_one_shot(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-one-shot-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            control = fx["control"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)
            assert isinstance(control, Path)

            plan = self._build(fx)["plan"]
            approval = _approval(plan)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                first = consume_stage_a_plan_approval(
                    handoff_root=handoff,
                    real_vault_root=live,
                    control_root=control,
                    plan=plan,
                    approval=approval,
                )
                self.assertTrue(first["unchanged"])
                with self.assertRaises(
                    ProductionEnablementBlockedError
                ):
                    consume_stage_a_plan_approval(
                        handoff_root=handoff,
                        real_vault_root=live,
                        control_root=control,
                        plan=plan,
                        approval=approval,
                    )

    def test_stage_a_consumption_never_mutates_real_vault(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-approval-readonly-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            control = fx["control"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)
            assert isinstance(control, Path)

            plan = self._build(fx)["plan"]
            approval = _approval(plan)
            before = _fingerprint(live)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                result = consume_stage_a_plan_approval(
                    handoff_root=handoff,
                    real_vault_root=live,
                    control_root=control,
                    plan=plan,
                    approval=approval,
                )

            self.assertTrue(result["unchanged"])
            self.assertEqual(before, _fingerprint(live))
            self.assertTrue(
                (
                    control
                    / "stage-a-approvals"
                    / (
                        approval["one_shot_nonce"]
                        + ".json"
                    )
                ).is_file()
            )

    def test_control_root_may_not_overlap_real_vault(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-control-overlap-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)

            plan = self._build(fx)["plan"]
            approval = _approval(plan)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementGovernanceError
                ):
                    consume_stage_a_plan_approval(
                        handoff_root=handoff,
                        real_vault_root=live,
                        control_root=live,
                        plan=plan,
                        approval=approval,
                    )

    def test_control_root_may_not_overlap_handoff(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-control-handoff-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            handoff = fx["handoff"]
            assert isinstance(live, Path)
            assert isinstance(handoff, Path)

            plan = self._build(fx)["plan"]
            approval = _approval(plan)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                with self.assertRaises(
                    ProductionEnablementGovernanceError
                ):
                    consume_stage_a_plan_approval(
                        handoff_root=handoff,
                        real_vault_root=live,
                        control_root=handoff,
                        plan=plan,
                        approval=approval,
                    )

    def test_zero_mutation_proof_detects_changed_tree(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-zero-proof-"
        ) as temp:
            fx = self._fixture(Path(temp))
            live = fx["live"]
            assert isinstance(live, Path)

            with patch(
                "tools.obsidian_projection."
                "production_enablement.REAL_VAULT",
                live,
            ):
                before = snapshot_real_vault(live)
                (live / "mutation.txt").write_text(
                    "MUTATED\n",
                    encoding="utf-8",
                )
                after = snapshot_real_vault(live)

                with self.assertRaises(
                    ProductionEnablementGovernanceError
                ):
                    prove_zero_real_vault_mutation(
                        before,
                        after,
                    )

    def test_plan_binds_exact_handoff_identity(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-handoff-bind-"
        ) as temp:
            fx = self._fixture(Path(temp))
            handoff = fx["handoff"]
            assert isinstance(handoff, Path)
            result = self._build(fx)
            raw = (
                handoff / "PROMOTION-HANDOFF.json"
            ).read_bytes()
            self.assertEqual(
                result["plan"]["handoff_record_sha256"],
                hashlib.sha256(raw).hexdigest(),
            )

    def test_stage_a_is_explicitly_non_executable(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3g-prod-nonexec-"
        ) as temp:
            fx = self._fixture(Path(temp))
            plan = self._build(fx)["plan"]
            approval = _approval(plan)
            self.assertEqual(
                approval["authorized_action"],
                "APPROVE_ONE_EXACT_REAL_LIVE_PUBLICATION_PLAN_FOR_FUTURE_EXECUTION_REVIEW",
            )
            self.assertNotIn(
                "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
                json.dumps(approval, sort_keys=True),
            )

    def test_source_has_no_execution_or_background_surface(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "production_enablement.py"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "os.replace(",
            "threading.Thread",
            "while True",
            "schtasks",
            "CreateService",
            "schedule.",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()

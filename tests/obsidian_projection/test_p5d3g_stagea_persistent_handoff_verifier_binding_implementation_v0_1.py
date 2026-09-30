import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.p5d3d_verify import _build_synthetic_repo
from tools.obsidian_projection.p5d3f_promotion_handoff import (
    run_finite_promotion_handoff,
)
from tools.obsidian_projection import production_enablement as pe


def _approval(plan: dict, suffix: str = "stagea-binding") -> dict:
    digest = pe.production_plan_digest(plan)
    nonce = hashlib.sha256(
        (digest + ":" + suffix).encode("ascii")
    ).hexdigest()
    return {
        "schema": pe.APPROVAL_SCHEMA,
        "authorized_action": pe.APPROVAL_ACTION,
        "plan_digest_sha256": digest,
        "candidate_head": plan["candidate_head"],
        "candidate_tree": plan["candidate_tree"],
        "generation_id": plan["generation_id"],
        "publication_mode": plan["publication_mode"],
        "expected_current_state": plan["expected_current_state"],
        "expected_current_sha256": plan["expected_current_sha256"],
        "expected_current_tmp_state": plan["expected_current_tmp_state"],
        "expected_target_state": plan["expected_target_state"],
        "one_shot_nonce": nonce,
    }


class P5D3GStageAPersistentHandoffVerifierBindingImplementationV01Tests(
    unittest.TestCase
):
    def _fixture(self, root: Path) -> dict[str, Path]:
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
        report = run_finite_promotion_handoff(
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
            / str(report["generation_id"])
        )
        live = root / "real-live-vault"
        live.mkdir()
        control = root / "control"
        control.mkdir()
        return {
            "staging": staging,
            "handoff": handoff,
            "live": live,
            "control": control,
        }

    def test_explicit_qualicified_persistent_staging_builds_plan(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = self._fixture(Path(temp))
            with (
                patch.object(pe, "REAL_VAULT", fixture["live"]),
                patch.object(
                    pe,
                    "PERSISTENT_STAGING",
                    fixture["staging"],
                ),
            ):
                result = pe.build_real_live_publication_plan(
                    handoff_root=fixture["handoff"],
                    real_vault_root=fixture["live"],
                    promotion_staging_root=fixture["staging"],
                )
            self.assertEqual(
                result["status"],
                "PASS_REAL_LIVE_PUBLICATION_PLAN_READ_ONLY",
            )
            self.assertEqual(
                result["plan"][
                    "qualified_live_publication_implementation_blob"
                ],
                pe.STAGEA_EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
            )
            self.assertFalse(
                result["stage_b_execution_authority"]
            )
            self.assertEqual(
                result["zero_mutation_proof"]["status"],
                "PASS_ZERO_REAL_VAULT_MUTATION_VERIFIED",
            )

    def test_arbitrary_persistent_staging_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = self._fixture(Path(temp))
            wrong = Path(temp) / "wrong-staging"
            wrong.mkdir()
            with (
                patch.object(pe, "REAL_VAULT", fixture["live"]),
                patch.object(
                    pe,
                    "PERSISTENT_STAGING",
                    fixture["staging"],
                ),
            ):
                with self.assertRaises(
                    pe.ProductionEnablementGovernanceError
                ):
                    pe.build_real_live_publication_plan(
                        handoff_root=fixture["handoff"],
                        real_vault_root=fixture["live"],
                        promotion_staging_root=wrong,
                    )

    def test_none_preserves_historical_temp_only_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = self._fixture(Path(temp))
            with patch.object(
                pe,
                "REAL_VAULT",
                fixture["live"],
            ):
                result = pe.build_real_live_publication_plan(
                    handoff_root=fixture["handoff"],
                    real_vault_root=fixture["live"],
                )
            self.assertEqual(
                result["status"],
                "PASS_REAL_LIVE_PUBLICATION_PLAN_READ_ONLY",
            )

    def test_stage_a_consumption_reverifies_persistent_handoff(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = self._fixture(Path(temp))
            with (
                patch.object(pe, "REAL_VAULT", fixture["live"]),
                patch.object(
                    pe,
                    "PERSISTENT_STAGING",
                    fixture["staging"],
                ),
            ):
                planned = pe.build_real_live_publication_plan(
                    handoff_root=fixture["handoff"],
                    real_vault_root=fixture["live"],
                    promotion_staging_root=fixture["staging"],
                )
                result = pe.consume_stage_a_plan_approval(
                    handoff_root=fixture["handoff"],
                    real_vault_root=fixture["live"],
                    control_root=fixture["control"],
                    plan=planned["plan"],
                    approval=_approval(planned["plan"]),
                    promotion_staging_root=fixture["staging"],
                 )
            self.assertEqual(
                result["status"],
                "PASS_STAGE_A_PLAN_APPROVAL_VALIDATED_ZERO_REAL_VAULT_MUTATION",
            )
            self.assertFalse(
                result["stage_b_execution_authority"]
             )
            self.assertTrue(result["unchanged"])


if __name__ == "__main__":
    unittest.main()

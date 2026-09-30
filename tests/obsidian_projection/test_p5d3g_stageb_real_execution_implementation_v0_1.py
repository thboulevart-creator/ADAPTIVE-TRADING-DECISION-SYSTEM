import hashlib
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.p5d3d_verify import _build_synthetic_repo
from tools.obsidian_projection.p5d3f_promotion_handoff import (
    run_finite_promotion_handoff,
)
from tools.obsidian_projection import live_publication_transaction as lp
from tools.obsidian_projection import production_enablement as pe
from tools.obsidian_projection import p5d3g_stageb_real_execution as sb


def _stage_a_approval(plan: dict, nonce: str) -> dict:
    digest = pe.production_plan_digest(plan)
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
def _stage_b_authorization(candidate: dict, nonce: str) -> dict:
    plan = candidate["transaction_plan"]
    return {
        "schema": sb.STAGE_B_AUTH_SCHEMA,
        "authorized_action": sb.STAGE_B_AUTH_ACTION,
        "stage_a_plan_digest_sha256": candidate[
            "stage_a_plan_digest_sha256"
        ],
        "stage_a_approval_digest_sha256": candidate[
            "stage_a_approval_digest_sha256"
        ],
        "stage_a_approval_receipt_sha256": candidate[
            "stage_a_approval_receipt_sha256"
        ],
        "candidate_head": plan["candidate_head"],
        "candidate_tree": plan["candidate_tree"],
        "generation_id": plan["generation_id"],
        "publication_mode": plan["publication_mode"],
        "expected_current_state": plan["expected_previous_current_state"],
        "expected_current_sha256": plan["expected_previous_current_sha256"],
        "expected_current_tmp_state": "ABSENT",
        "expected_target_state": "ABSENT",
        "one_shot_nonce": nonce,
    }


class StageBFixture:
    def __init__(self, root: Path) -> None:
        repo = root / "candidate"
        self.head, self.tree = _build_synthetic_repo(repo)
        workspace = root / "evaluation"
        workspace.mkdir()
        self.staging = root / "promotion-staging"
        self.staging.mkdir()
        protected = root / "protected-source-vault"
        protected.mkdir()
        (protected / "sentinel.txt").write_text(
            "UNCHANGED\n",
            encoding="utf-8",
        )
        report = run_finite_promotion_handoff(
            candidate_head=self.head,
            candidate_tree=self.tree,
            candidate_repo_root=repo,
            evaluation_workspace_root=workspace,
            promotion_staging_root=self.staging,
            live_vault_root=protected,
        )
        self.generation_id = str(report["generation_id"])
        self.handoff = (
            self.staging / "packages" / self.generation_id
        )
        self.live = root / "real-live-vault"
        self.live.mkdir()
        self.control = root / "control"
        self.control.mkdir()

        self.stage_a_plan = None
        self.stage_a_plan_digest = None
        self.stage_a_approval_digest = None
        self.stage_a_receipt = None
        self.stage_a_receipt_sha = None

    def base_patches(self) -> ExitStack:
        stack = ExitStack()
        stack.enter_context(patch.object(lp, "REAL_VAULT", self.live))
        stack.enter_context(patch.object(pe, "REAL_VAULT", self.live))
        stack.enter_context(
            patch.object(pe, "PERSISTENT_STAGING", self.staging)
        )
        stack.enter_context(patch.object(sb, "REAL_VAULT", self.live))
        stack.enter_context(
            patch.object(sb, "PERSISTENT_STAGING", self.staging)
        )
        stack.enter_context(patch.object(sb, "CONTROL_ROOT", self.control))
        return stack
    def prepare_stage_a(self) -> None:
        with self.base_patches():
            planned = pe.build_real_live_publication_plan(
                handoff_root=self.handoff,
                real_vault_root=self.live,
                promotion_staging_root=self.staging,
            )
            self.stage_a_plan = planned["plan"]
            self.stage_a_plan_digest = planned["plan_digest_sha256"]
            approval = _stage_a_approval(
                self.stage_a_plan,
                sb.STAGE_A_RECEIPT_NONCE,
            )
            consumed = pe.consume_stage_a_plan_approval(
                handoff_root=self.handoff,
                real_vault_root=self.live,
                control_root=self.control,
                plan=self.stage_a_plan,
                approval=approval,
                promotion_staging_root=self.staging,
            )
            self.stage_a_approval_digest = consumed[
                "approval_digest_sha256"
            ]
            self.stage_a_receipt = Path(
                consumed["approval_receipt_path"]
            )
            self.stage_a_receipt_sha = hashlib.sha256(
                self.stage_a_receipt.read_bytes()
            ).hexdigest()

    def stage_b_patches(self) -> ExitStack:
        assert self.stage_a_plan is not None
        assert self.stage_a_plan_digest is not None
        assert self.stage_a_approval_digest is not None
        assert self.stage_a_receipt is not None
        assert self.stage_a_receipt_sha is not None
        stack = self.base_patches()
        stack.enter_context(
            patch.object(
                sb,
                "STAGE_A_RECEIPT_PATH",
                self.stage_a_receipt,
            )
        )
        stack.enter_context(
            patch.object(
                sb,
                "EXPECTED_STAGE_A_PLAN_DIGEST",
                self.stage_a_plan_digest,
            )
        )
        stack.enter_context(
            patch.object(
                sb,
                "EXPECTED_STAGE_A_APPROVAL_DIGEST",
                self.stage_a_approval_digest,
            )
        )
        stack.enter_context(
            patch.object(
                sb,
                "EXPECTED_STAGE_A_RECEIPT_SHA256",
                self.stage_a_receipt_sha,
            )
        )
        stack.enter_context(
            patch.object(sb, "EXPECTED_CANDIDATE_HEAD", self.head)
        )
        stack.enter_context(
            patch.object(sb, "EXPECTED_CANDIDATE_TREE", self.tree)
        )
        stack.enter_context(
            patch.object(
                sb,
                "EXPECTED_GENERATION_ID",
                self.generation_id,
            )
        )
        return stack


class P5D3GStageBRealExecutionImplementationV01Tests(unittest.TestCase):
    def _fixture(self, root: Path) -> StageBFixture:
        fx = StageBFixture(root)
        fx.prepare_stage_a()
        return fx

    def test_sacrificial_default_guard_still_rejects_real_vault(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            with fx.stage_b_patches():
                with self.assertRaises(
                    lp.LivePublicationGovernanceError
                ):
                    lp.build_publication_plan(
                        handoff_root=fx.handoff,
                        live_vault_root=fx.live,
                        promotion_staging_root=fx.staging,
                    )

    def test_stage_b_read_only_candidate_has_exact_plan_parity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            with fx.stage_b_patches():
                result = sb.build_stage_b_read_only_candidate(
                    handoff_root=fx.handoff,
                    promotion_staging_root=fx.staging,
                    real_vault_root=fx.live,
                    control_root=fx.control,
                )
            self.assertEqual(
                result["status"],
                "PASS_STAGE_B_REAL_EXECUTION_PREFLIGHT_READ_ONLY",
            )
            self.assertFalse(result["stage_b_execution_authority"])
            self.assertTrue(result["zero_mutation_proof"]["unchanged"])

    def test_stage_a_receipt_tamper_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            assert fx.stage_a_receipt is not None
            fx.stage_a_receipt.write_bytes(
                fx.stage_a_receipt.read_bytes() + b" "
            )
            with fx.stage_b_patches():
                with self.assertRaises(
                    sb.StageBExecutionGovernanceError
                ):
                    sb.build_stage_b_read_only_candidate(
                        handoff_root=fx.handoff,
                        promotion_staging_root=fx.staging,
                        real_vault_root=fx.live,
                        control_root=fx.control,
                    )

    def test_stage_b_authorization_reuse_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            with fx.stage_b_patches():
                candidate = sb.build_stage_b_read_only_candidate(
                    handoff_root=fx.handoff,
                    promotion_staging_root=fx.staging,
                    real_vault_root=fx.live,
                    control_root=fx.control,
                )
                auth = _stage_b_authorization(
                    candidate,
                    "synthetic-stage-b-reuse-0001",
                )
                value, digest = sb._validate_stage_b_authorization(
                    candidate,
                    auth,
                )
                tx_digest = candidate[
                    "transaction_plan_digest_sha256"
                ]
                sb._consume_stage_b_authorization(
                    fx.control,
                    value,
                    digest,
                    tx_digest,
                )
                with self.assertRaises(
                    sb.StageBExecutionBlockedError
                ):
                    sb._consume_stage_b_authorization(
                        fx.control,
                        value,
                        digest,
                        tx_digest,
                    )

    def test_current_tmp_prestate_drift_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            (fx.live / "CURRENT.tmp").write_text(
                "RACE\n",
                encoding="utf-8",
            )
            with fx.stage_b_patches():
                with self.assertRaises(Exception):
                    sb.build_stage_b_read_only_candidate(
                        handoff_root=fx.handoff,
                        promotion_staging_root=fx.staging,
                        real_vault_root=fx.live,
                        control_root=fx.control,
                    )

    def test_target_prestate_drift_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            target = (
                fx.live / "generations" / fx.generation_id
            )
            target.mkdir(parents=True)
            with fx.stage_b_patches():
                with self.assertRaises(Exception):
                    sb.build_stage_b_read_only_candidate(
                        handoff_root=fx.handoff,
                        promotion_staging_root=fx.staging,
                        real_vault_root=fx.live,
                        control_root=fx.control,
                    )
    def test_one_finite_stage_b_synthetic_publication_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fx = self._fixture(Path(temp))
            with fx.stage_b_patches():
                candidate = sb.build_stage_b_read_only_candidate(
                    handoff_root=fx.handoff,
                    promotion_staging_root=fx.staging,
                    real_vault_root=fx.live,
                    control_root=fx.control,
                )
                auth = _stage_b_authorization(
                    candidate,
                    "synthetic-stage-b-execution-0001",
                )
                result = sb.execute_one_real_live_publication(
                    handoff_root=fx.handoff,
                    promotion_staging_root=fx.staging,
                    real_vault_root=fx.live,
                    control_root=fx.control,
                    authorization=auth,
                )

            self.assertEqual(result["status"], lp.SUCCESS_FINAL)
            self.assertTrue(
                result["p5d2_promotion_confirmed_emitted"]
            )
            self.assertTrue(result["mandatory_stop"])
            self.assertTrue((fx.live / "CURRENT.md").is_file())
            self.assertFalse((fx.live / "CURRENT.tmp").exists())
            self.assertTrue(
                (
                    fx.live
                    / "generations"
                    / fx.generation_id
                    / "package"
                ).is_dir()
            )
            self.assertTrue(
                Path(
                    result["stage_b_authorization_receipt_path"]
                ).is_file()
            )


if __name__ == "__main__":
    unittest.main()

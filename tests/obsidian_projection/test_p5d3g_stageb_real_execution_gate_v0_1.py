import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import live_publication_transaction as lp


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3g_stageb_real_execution_gate_contract_v0_1.json"
)
EXPECTED_CONTRACT_BLOB = "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead"


def _committed_blob(relative: str) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


class P5D3GStageBRealExecutionGateV01RedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (REPO_ROOT / CONTRACT_RELATIVE).read_text(encoding="utf-8")
        )

    def test_contract_is_exact_and_real_execution_remains_closed(self) -> None:
        self.assertEqual(
            _committed_blob(CONTRACT_RELATIVE),
            EXPECTED_CONTRACT_BLOB,
        )
        scope = self.contract["qualification_scope"]
        self.assertFalse(scope["real_vault_write_authorized"])
        self.assertFalse(scope["real_live_publication_execution_authorized"])
        self.assertTrue(scope["synthetic_stage_b_execution_authorized"])

    def test_reserved_stage_b_authority_is_exact(self) -> None:
        auth = self.contract["stage_b_authorization"]
        self.assertEqual(
            auth["schema"],
            "ATDS_OBSIDIAN_P5D3G_REAL_LIVE_EXECUTION_AUTHORIZATION_V0_1",
        )
        self.assertEqual(
            auth["authorized_action"],
            "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
        )

    def test_private_real_production_capability_exists(self) -> None:
        self.assertTrue(
            hasattr(lp, "_REAL_PRODUCTION_EXECUTION_CAPABILITY"),
            "REAL_PRODUCTION_CAPABILITY_MISSING",
        )

    def test_stage_b_production_gate_module_exists(self) -> None:
        spec = importlib.util.find_spec(
            "tools.obsidian_projection.p5d3g_stageb_real_execution"
        )
        self.assertIsNotNone(
            spec,
            "STAGE_B_PRODUCTION_GATE_MODULE_MISSING",
        )


if __name__ == "__main__":
    unittest.main()

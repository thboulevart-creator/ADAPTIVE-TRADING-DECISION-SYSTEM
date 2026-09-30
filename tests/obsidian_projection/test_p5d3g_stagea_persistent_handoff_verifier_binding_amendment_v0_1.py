import inspect
import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import live_publication_transaction as lp
from tools.obsidian_projection import production_enablement as pe


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3g_stagea_persistent_handoff_verifier_binding_amendment_contract_v0_1.json"
)
EXPECTED_CONTRACT_BLOB = "f2625a98ac53c737c884f5d276bb41f51ce5f498"
EXPECTED_BASE_PE_BLOB = "a9c0b46e5e623d765811d6d9b7766f172ca817a6"
EXPECTED_BASE_LP_BLOB = "2fb34e1c04b4dd32d19b85b488d89f8a702204d0"
EXPECTED_PERSISTENT_HANDOFF_BLOB = "375607d88bc926e4fd4c297ddc6fedba5506642a"


def _committed_blob(relative: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class P5D3GStageAPersistentHandoffVerifierBindingAmendmentV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (REPO_ROOT / CONTRACT_RELATIVE).read_text(encoding="utf-8")
        )

    def test_contract_is_exact_and_basis_is_frozen(self) -> None:
        self.assertEqual(
            _committed_blob(CONTRACT_RELATIVE),
            EXPECTED_CONTRACT_BLOB,
        )
        basis = self.contract["basis"]
        self.assertEqual(
            basis["production_enablement_blob"],
            EXPECTED_BASE_PE_BLOB,
        )
        self.assertEqual(
            basis["live_publication_blob"],
            EXPECTED_BASE_LP_BLOB,
        )
        self.assertEqual(
            basis["persistent_handoff_blob"],
            EXPECTED_PERSISTENT_HANDOFF_BLOB,
        )

    def test_boundary_opens_only_read_only_plan_build(self) -> None:
        boundary = self.contract["boundary"]
        self.assertTrue(
            boundary["stage_a_plan_build_read_only_authorized"]
        )
        for field, value in boundary.items():
            if field == "stage_a_plan_build_read_only_authorized":
                continue
            with self.subTest(field=field):
                self.assertFalse(value)

    def test_live_publication_verified_handoff_has_optional_staging_binding(
        self,
    ) -> None:
        signature = inspect.signature(lp._verified_handoff)
        self.assertIn("promotion_staging_root", signature.parameters)
        parameter = signature.parameters["promotion_staging_root"]
        self.assertIsNone(parameter.default)

    def test_production_plan_has_optional_staging_binding(self) -> None:
        signature = inspect.signature(pe.build_real_live_publication_plan)
        self.assertIn("promotion_staging_root", signature.parameters)
        parameter = signature.parameters["promotion_staging_root"]
        self.assertIsNone(parameter.default)

    def test_stage_a_consumption_has_optional_staging_binding(self) -> None:
        signature = inspect.signature(pe.consume_stage_a_plan_approval)
        self.assertIn("promotion_staging_root", signature.parameters)
        parameter = signature.parameters["promotion_staging_root"]
        self.assertIsNone(parameter.default)


if __name__ == "__main__":
    unittest.main()

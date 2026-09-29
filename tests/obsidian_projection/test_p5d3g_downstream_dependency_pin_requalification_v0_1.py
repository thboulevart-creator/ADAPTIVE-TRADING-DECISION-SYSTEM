from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import (
    live_publication_transaction as lpt,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
AMENDMENT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3g_downstream_dependency_pin_requalification_contract_v0_1.json"
)
HISTORICAL_CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "live_publication_transaction_contract_v0_1.json"
)

EXPECTED_AMENDMENT_BLOB = (
    "734aa3e0242af39263e558750d1c3b4b957f0db2"
)
EXPECTED_HISTORICAL_CONTRACT_BLOB = (
    "64997ddd9977229961387f66af4de356c045c0ac"
)
EXPECTED_P5D3F_BLOB = (
    "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60"
)
EXPECTED_VERIFIER_BLOB = (
    "398bda75604f8172128fbe0ddaf78cab4cee9f92"
)

def _committed_blob(relative: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class P5D3GDownstreamDependencyPinRequalificationV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (REPO_ROOT / AMENDMENT_RELATIVE).read_text(
                encoding="utf-8"
            )
        )

    def test_amendment_contract_is_exact_and_historical_contract_unchanged(
        self,
    ) -> None:
        self.assertEqual(
            _committed_blob(AMENDMENT_RELATIVE),
            EXPECTED_AMENDMENT_BLOB,
        )
        self.assertEqual(
            _committed_blob(HISTORICAL_CONTRACT_RELATIVE),
            EXPECTED_HISTORICAL_CONTRACT_BLOB,
        )
        self.assertTrue(
            self.contract["preservation"][
                "historical_p5d3g_contract_must_remain_byte_exact"
            ]
        )

    def test_exact_rebindings_are_preregistered(self) -> None:
        bindings = self.contract["exact_rebindings"]
        self.assertEqual(
            bindings["p5d3f_implementation_blob"]["to"],
            EXPECTED_P5D3F_BLOB,
        )
        self.assertEqual(
            bindings["candidate_generation_verifier_blob"]["to"],
            EXPECTED_VERIFIER_BLOB,
        )
        self.assertTrue(
            self.contract["implementation_scope"][
                "all_other_runtime_changes_forbidden"
            ]
        )

    def test_runtime_rebinds_only_to_preregistered_upstream_blobs(
        self,
    ) -> None:
        self.assertEqual(
            lpt.P5D3F_IMPLEMENTATION_BLOB,
            EXPECTED_P5D3F_BLOB,
        )
        self.assertEqual(
            lpt.P5D3C2_VERIFIER_BLOB,
            EXPECTED_VERIFIER_BLOB,
        )

    def test_runtime_requires_exact_amendment_contract_blob(
        self,
    ) -> None:
        self.assertEqual(
            lpt.P5D3G_DEPENDENCY_PIN_REQUALIFICATION_CONTRACT_BLOB,
            EXPECTED_AMENDMENT_BLOB,
        )
        self.assertEqual(
            lpt._TOOLING[AMENDMENT_RELATIVE],
            EXPECTED_AMENDMENT_BLOB,
        )

    def test_requalification_grants_no_real_authority(self) -> None:
        boundary = self.contract["boundary"]
        for field in (
            "real_persistent_handoff_execution_authorized",
            "real_vault_read_authorized",
            "real_vault_write_authorized",
            "live_publication_authorized",
            "current_pointer_creation_authorized",
            "current_pointer_mutation_authorized",
            "promotion_confirmed_authorized",
            "stage_a_authorized",
            "stage_b_authorized",
            "p5d4_authorized",
            "p6_authorized",
            "background_execution_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import production_enablement as pe


REPO_ROOT = Path(__file__).resolve().parents[2]
AMENDMENT_RELATIVE = (
    "tools/obsidian_projection/"
    "production_enablement_dependency_pin_requalification_contract_v0_1.json"
)
HISTORICAL_CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "production_enablement_gate_contract_v0_1.json"
)
HISTORICAL_TEST_RELATIVE = (
    "tests/obsidian_projection/"
    "test_p5d3g_production_enablement.py"
)
HISTORICAL_REBREAK_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3g_production_enablement_implementation_rebreak.py"
)

EXPECTED_AMENDMENT_BLOB = (
    "6f938414059b2bde425ea17febfbb77635fd91e5"
)
EXPECTED_HISTORICAL_CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)
EXPECTED_HISTORICAL_TEST_BLOB = (
    "5a05ac5fccaf7032248f35f8fd2933d5943b100c"
)
EXPECTED_HISTORICAL_REBREAK_BLOB = (
    "1c126f27d7a48ec44cbfc6e7eafe056dd5a9cefb"
)
EXPECTED_HISTORICAL_LIVE_BLOB = (
    "b8875f8973ddf1076ff20d8e725ce04abbb814a8"
)
EXPECTED_EFFECTIVE_LIVE_BLOB = (
    "2fb34e1c04b4dd32d19b85b488d89f8a702204d0"
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


class ProductionEnablementDependencyPinRequalificationV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (REPO_ROOT / AMENDMENT_RELATIVE).read_text(
                encoding="utf-8"
            )
        )

    def test_amendment_and_historical_artifacts_are_exact(
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
        self.assertEqual(
            _committed_blob(HISTORICAL_TEST_RELATIVE),
            EXPECTED_HISTORICAL_TEST_BLOB,
        )
        self.assertEqual(
            _committed_blob(HISTORICAL_REBREAK_RELATIVE),
            EXPECTED_HISTORICAL_REBREAK_BLOB,
        )

    def test_historical_authority_remains_historical(self) -> None:
        self.assertEqual(
            pe.QUALIFIED_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
            EXPECTED_HISTORICAL_LIVE_BLOB,
        )
        self.assertTrue(
            self.contract["historical_preservation"][
                "historical_contract_must_remain_byte_exact"
            ]
        )
        self.assertTrue(
            self.contract["historical_preservation"][
                "historical_test_qualified_authorities_are_exact_must_remain_unchanged"
            ]
        )

    def test_effective_requalification_is_exact(self) -> None:
        binding = self.contract["effective_requalification"]
        self.assertEqual(
            binding["effective_live_publication_blob"],
            EXPECTED_EFFECTIVE_LIVE_BLOB,
        )
        self.assertTrue(
            binding[
                "effective_binding_must_be_explicitly_distinct_from_historical_binding"
            ]
        )

    def test_runtime_exposes_effective_requalified_binding(self) -> None:
        self.assertEqual(
            pe.EFFECTIVE_LIVE_PUBLICATION_IMPLEMENTATION_BLOB,
            EXPECTED_EFFECTIVE_LIVE_BLOB,
        )

    def test_runtime_requires_exact_amendment_contract(self) -> None:
        self.assertEqual(
            pe.PRODUCTION_ENABLEMENT_PIN_REQUALIFICATION_CONTRACT_BLOB,
            EXPECTED_AMENDMENT_BLOB,
        )
        expected = {
            (
                "tools/obsidian_projection/"
                "production_enablement_dependency_pin_requalification_contract_v0_1.json"
            ): EXPECTED_AMENDMENT_BLOB,
            (
                "tools/obsidian_projection/"
                "live_publication_transaction.py"
            ): EXPECTED_EFFECTIVE_LIVE_BLOB,
        }
        for relative, blob in expected.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    pe._TOOLING[relative],
                    blob,
                )

    def test_requalification_grants_no_real_authority(self) -> None:
        boundary = self.contract["boundary"]
        for field, value in boundary.items():
            with self.subTest(field=field):
                self.assertFalse(value)


if __name__ == "__main__":
    unittest.main()

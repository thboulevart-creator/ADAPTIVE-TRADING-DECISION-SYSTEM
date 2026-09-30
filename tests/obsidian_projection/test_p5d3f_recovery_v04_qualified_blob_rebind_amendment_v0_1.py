from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import (
    p5d3f_recovery_real_execution_v0_4 as runner,
)

REPO = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3f_recovery_v04_qualified_blob_rebind_amendment_contract_v0_1.json"
)
CONTRACT_BLOB = "3667488c6cb7a348eab6564b7152049e0ba32d3b"
HISTORICAL_RUNNER_TEST_BLOB = "667e458962aca47a1d3f08ef3f12c80015c1390b"
HISTORICAL_RUNNER_REBREAK_BLOB = "e6c9ab7f98c9fa8f77db3dc98571120e6cbeb7c0"
EFFECTIVE_BRANCH = (
    "feat/obsidian-projection-p5d3f-recovery-v04-qualified-blob-rebind-amendment-v0.1"
)
EFFECTIVE_WRAPPER = "375607d88bc926e4fd4c297ddc6fedba5506642a"
EFFECTIVE_P5D3F = "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60"


def _blob(relative: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class P5D3FRecoveryV04QualifiedBlobRebindAmendmentV01Tests(
    unittest.TestCase
):
    def test_amendment_contract_is_exact(self) -> None:
        self.assertEqual(_blob(CONTRACT_RELATIVE), CONTRACT_BLOB)
        contract = json.loads(
            (REPO / CONTRACT_RELATIVE).read_text(encoding="utf-8")
        )
        self.assertEqual(
            contract["status"], "CANDIDATE_PREREGISTRATION_ONLY"
        )
        self.assertFalse(
            contract["authority"]["real_execution_authorized"]
        )
        self.assertFalse(
            contract["authority"]["one_shot_consumption_authorized"]
        )

    def test_historical_runner_authority_remains_historical(self) -> None:
        self.assertEqual(
            runner.RUNNER_BRANCH,
            "feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.4-monitored-head-pin",
        )
        self.assertEqual(
            runner.EXPECTED_IMPLEMENTATION_BLOB,
            "dcd70a9d9794675eab90e41df560f8b030b5dbf3",
        )
        self.assertEqual(
            runner.EXPECTED_QUALIFIED_P5D3F_BLOB,
            "2108131914cf65bb076b80f5bb63cd63267567fa",
        )

    def test_historical_test_and_rebreak_are_byte_exact(self) -> None:
        self.assertEqual(
            _blob(
                "tests/obsidian_projection/"
                "test_p5d3f_recovery_real_execution_runner_v0_4.py"
            ),
            HISTORICAL_RUNNER_TEST_BLOB,
        )
        self.assertEqual(
            _blob(
                "tools/obsidian_projection/"
                "p5d3f_recovery_real_execution_runner_rebreak_v0_4.py"
            ),
            HISTORICAL_RUNNER_REBREAK_BLOB,
        )

    def test_effective_binding_is_explicit_and_exact(self) -> None:
        self.assertEqual(
            runner.RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB,
            CONTRACT_BLOB,
        )
        self.assertEqual(
            runner.EFFECTIVE_RUNNER_BRANCH,
            EFFECTIVE_BRANCH,
        )
        self.assertEqual(
            runner.EFFECTIVE_IMPLEMENTATION_BLOB,
            EFFECTIVE_WRAPPER,
        )
        self.assertEqual(
            runner.EFFECTIVE_QUALIFIED_P5D3F_BLOB,
            EFFECTIVE_P5D3F,
        )

    def test_runtime_verifier_uses_effective_binding(self) -> None:
        source = (
            REPO
            / "tools"
            / "obsidian_projection"
            / "p5d3f_recovery_real_execution_v0_4.py"
        ).read_text(encoding="utf-8")
        for token in (
            "EFFECTIVE_RUNNER_BRANCH",
            "EFFECTIVE_IMPLEMENTATION_BLOB",
            "EFFECTIVE_QUALIFIED_P5D3F_BLOB",
            "RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB",
        ):
            self.assertIn(token, source)

    def test_rebind_grants_no_new_execution_authority(self) -> None:
        self.assertEqual(
            runner.AUTHORIZATION_LITERAL,
            "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF",
        )
        source = (
            REPO
            / "tools"
            / "obsidian_projection"
            / "p5d3f_recovery_real_execution_v0_4.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "consume_stage_a_plan_approval",
            "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
            "threading.Thread",
            "while True",
            "schtasks",
            "CreateService",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()

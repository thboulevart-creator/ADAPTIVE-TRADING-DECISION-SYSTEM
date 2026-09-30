import json
import subprocess
import unittest
from pathlib import Path

from tools.obsidian_projection import p5d3g_stageb_real_execution as sb

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3g_stageb_prestate_rebind_amendment_contract_v0_1.json"
)
EXPECTED_CONTRACT_BLOB = "441fea40d33aa85dcfc6305d4d32cef39c42388e"
EXPECTED_PLAN = "f83f266e17db3ee90e07eeefbc9baf308b7ddf6714fec16562a34cb4025db3f6"
EXPECTED_APPROVAL = "2ad99ab121c59a09cc0c34a5a91a129547c19d9748344e9960980dbc170caf25"
EXPECTED_RECEIPT = "d7db614a87e53684440ff62b3ccd2c6d92c2b18377fa6c75bc19231e6d726a8f"
EXPECTED_NONCE = "stagea-f83f266e17db3ee90e07eeefbc9baf30-human-approval-02"
EXPECTED_VAULT = "d9024f75989970cf7ce7f4119d48c5e58f141017e36ab089c1921bb82a4b716c"

def _blob(relative: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()

class StageBPrestateRebindAmendmentV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(
            (REPO_ROOT / CONTRACT_RELATIVE).read_text(encoding="utf-8")
        )

    def test_amendment_contract_is_exact(self):
        self.assertEqual(_blob(CONTRACT_RELATIVE), EXPECTED_CONTRACT_BLOB)

    def test_preserved_authority_remains_exact(self):
        preserved = self.contract["preserved_authority"]
        self.assertEqual(
            preserved["candidate_head"],
            "59f1dc26973b0b50efefccf12b26784d1e41f546",
        )
        self.assertEqual(
            preserved["candidate_tree"],
            "beb85ddb99e8a87afc4e8a6ed9b989ed0f83e1ea",
        )
        self.assertEqual(
            preserved["generation_id"],
            "gen-69e845e1b6f60f213dd2e8e90ed493fd6a2a541084be9cfa9df3b2e035877ea0",
        )

    def test_stage_b_module_rebinds_new_stage_a_authority(self):
        self.assertEqual(sb.EXPECTED_STAGE_A_PLAN_DIGEST, EXPECTED_PLAN)
        self.assertEqual(sb.EXPECTED_STAGE_A_APPROVAL_DIGEST, EXPECTED_APPROVAL)
        self.assertEqual(sb.EXPECTED_STAGE_A_RECEIPT_SHA256, EXPECTED_RECEIPT)
        self.assertEqual(sb.STAGE_A_RECEIPT_NONCE, EXPECTED_NONCE)

    def test_stage_b_module_pins_amendment_contract(self):
        self.assertEqual(
            sb.PRESTATE_REBIND_AMENDMENT_CONTRACT_BLOB,
            EXPECTED_CONTRACT_BLOB,
        )
        self.assertEqual(
            sb._TOOLING[CONTRACT_RELATIVE],
            EXPECTED_CONTRACT_BLOB,
        )

    def test_contract_binds_new_real_vault_prestate(self):
        self.assertEqual(
            self.contract["basis"]["new_real_vault_tree_digest_sha256"],
            EXPECTED_VAULT,
        )
        self.assertFalse(
            self.contract["boundary"]["stage_b_real_execution_authorized"]
        )

if __name__ == "__main__":
    unittest.main()

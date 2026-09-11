import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "tools" / "probe_batch01_structural_qualification_v2.py"
COMPAT = ROOT / "tools" / "probe_research_execution_compatibility_v4_3.py"


class ContractConsumerAdversarialTests(unittest.TestCase):
    def test_consumers_do_not_duplicate_price_scale_literal(self):
        for path in (BATCH, COMPAT):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("ask_raw / 1000.0", text, path.name)
            self.assertNotIn("bid_raw / 1000.0", text, path.name)
            self.assertNotIn("ask_raw / 100000.0", text, path.name)
            self.assertNotIn("bid_raw / 100000.0", text, path.name)
            self.assertIn("contract.price_scale", text, path.name)

    def test_consumers_are_syntactically_valid(self):
        for path in (BATCH, COMPAT):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_batch_consumer_resolves_contract_before_decoding(self):
        text = BATCH.read_text(encoding="utf-8")
        self.assertIn("resolve_contract", text)
        self.assertIn("INSTRUMENT_CONTRACT_UNAVAILABLE", text)
        self.assertIn("contract.record_size", text)
        self.assertIn("contract.record_struct", text)

    def test_compatibility_consumer_blocks_missing_bi5_contract(self):
        text = COMPAT.read_text(encoding="utf-8")
        self.assertIn("BI5_CONTRACT_REQUIRED", text)
        self.assertIn("resolve_contract", text)
        self.assertIn("--contracts-root", text)


if __name__ == "__main__":
    unittest.main()

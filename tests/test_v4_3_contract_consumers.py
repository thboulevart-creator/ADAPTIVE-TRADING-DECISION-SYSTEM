import ast
import importlib
import lzma
import struct
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

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

    def test_compatibility_decoder_really_consumes_price_scale(self):
        compat = importlib.import_module("tools.probe_research_execution_compatibility_v4_3")
        raw_record = struct.Struct(">IIIff").pack(76, 21298102, 21294697, 1.0, 1.0)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "2025" / "01" / "27" / "13h_ticks.bi5"
            path.parent.mkdir(parents=True)
            path.write_bytes(lzma.compress(raw_record, format=lzma.FORMAT_ALONE))
            contract_1000 = SimpleNamespace(record_size=20, record_struct=">IIIff", timestamp_unit="milliseconds", price_scale=1000)
            contract_100000 = SimpleNamespace(record_size=20, record_struct=">IIIff", timestamp_unit="milliseconds", price_scale=100000)
            stats_1000 = compat.empty_stats()
            stats_100000 = compat.empty_stats()
            compat.scan_bi5(path, stats_1000, contract_1000)
            compat.scan_bi5(path, stats_100000, contract_100000)
            self.assertNotEqual(stats_1000["spreads"][0], stats_100000["spreads"][0])
            self.assertAlmostEqual(stats_1000["spreads"][0], 3.405)
            self.assertAlmostEqual(stats_100000["spreads"][0], 0.03405)


if __name__ == "__main__":
    unittest.main()

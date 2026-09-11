import json
import tempfile
import unittest
from pathlib import Path

from tools.instrument_contract_v4_3 import load_contract, resolve_contract

VALID = {
    "asset_id": "USATECHIDXUSD",
    "source": "Dukascopy",
    "format": "BI5",
    "record_size": 20,
    "record_struct": ">IIIff",
    "timestamp_unit": "milliseconds",
    "price_scale": 1000,
}


class InstrumentContractAdversarialTests(unittest.TestCase):
    def write(self, payload):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(payload, f)
        f.close()
        self.addCleanup(lambda: Path(f.name).unlink(missing_ok=True))
        return f.name

    def test_valid_contract_loads(self):
        c = load_contract(self.write(VALID))
        self.assertEqual(c.asset_id, "USATECHIDXUSD")
        self.assertEqual(c.price_scale, 1000)
        self.assertEqual(c.record_size, 20)

    def test_missing_price_scale_is_rejected(self):
        payload = dict(VALID)
        del payload["price_scale"]
        with self.assertRaisesRegex(ValueError, "CONTRACT_MISSING_FIELDS:.*price_scale"):
            load_contract(self.write(payload))

    def test_zero_or_negative_scale_is_rejected(self):
        for scale in (0, -1000):
            with self.subTest(scale=scale):
                with self.assertRaisesRegex(ValueError, "INVALID_PRICE_SCALE"):
                    load_contract(self.write(dict(VALID, price_scale=scale)))

    def test_wrong_scale_is_not_silently_normalized(self):
        c = load_contract(self.write(dict(VALID, price_scale=100000)))
        self.assertEqual(c.price_scale, 100000)
        self.assertNotEqual(c.price_scale, 1000)

    def test_unknown_contract_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError, "CONTRACT_NOT_FOUND"):
                resolve_contract(td, "UNKNOWN", "Dukascopy", "BI5")

    def test_identity_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "USATECHIDXUSD-Dukascopy-BI5.json"
            path.write_text(json.dumps(dict(VALID, asset_id="OTHER")), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "CONTRACT_IDENTITY_MISMATCH"):
                resolve_contract(td, "USATECHIDXUSD", "Dukascopy", "BI5")


if __name__ == "__main__":
    unittest.main()

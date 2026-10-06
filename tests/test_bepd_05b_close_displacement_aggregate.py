import importlib.util
import unittest
from decimal import Decimal
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "tools" / "bepd_05b_close_displacement_aggregate.py"
SPEC = importlib.util.spec_from_file_location("bepd05b_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(runner)


def row(i, value, reintegration):
    return {
        "event_id": f"event-{i}",
        "target_week_id": "2026-01-05",
        "sweep_cluster_id": "cluster-a",
        "side": "HIGH" if i % 2 else "LOW",
        "same_week_reintegration": reintegration,
        "close_displacement": Decimal(value),
    }


class TestBEPD05BGlobalAggregation(unittest.TestCase):
    def setUp(self):
        self.rows = [
            row(1, "-2", False),
            row(2, "0", False),
            row(3, "1", True),
            row(4, "3", True),
            row(5, "8", True),
        ]

    def test_exact_global_surface(self):
        core = runner.aggregate_rows(self.rows, 5)
        self.assertEqual(core["N"], 5)
        self.assertEqual(core["MINIMUM"], "-2.000000000000000000")
        self.assertEqual(core["MAXIMUM"], "8.000000000000000000")
        self.assertEqual(core["MEAN"], "2.000000000000000000")
        self.assertEqual(core["MEDIAN"], "1.000000000000000000")
        self.assertEqual(core["P01"], "-1.920000000000000000")
        self.assertEqual(core["P05"], "-1.600000000000000000")
        self.assertEqual(core["P10"], "-1.200000000000000000")
        self.assertEqual(core["P25"], "0.000000000000000000")
        self.assertEqual(core["P50"], "1.000000000000000000")
        self.assertEqual(core["P75"], "3.000000000000000000")
        self.assertEqual(core["P90"], "6.000000000000000000")
        self.assertEqual(core["P95"], "7.000000000000000000")
        self.assertEqual(core["P99"], "7.800000000000000000")
        self.assertEqual(core["P50"], core["MEDIAN"])

    def test_sign_counts_and_fractions(self):
        core = runner.aggregate_rows(self.rows, 5)
        self.assertEqual(core["POSITIVE_COUNT"], 3)
        self.assertEqual(core["ZERO_COUNT"], 1)
        self.assertEqual(core["NEGATIVE_COUNT"], 1)
        self.assertEqual(core["POSITIVE_FRACTION"], {"fraction": "3/5", "decimal": "0.600000000000000000"})
        self.assertEqual(core["ZERO_FRACTION"], {"fraction": "1/5", "decimal": "0.200000000000000000"})
        self.assertEqual(core["NEGATIVE_FRACTION"], {"fraction": "1/5", "decimal": "0.200000000000000000"})

    def test_ecdf_exact_unsmoothed(self):
        core = runner.aggregate_rows(self.rows, 5)
        ecdf = core["EMPIRICAL_CDF"]
        self.assertEqual(len(ecdf), 5)
        self.assertEqual(ecdf[0]["support_value"], "-2")
        self.assertEqual(ecdf[-1]["support_value"], "8")
        self.assertEqual(ecdf[-1]["cumulative_count"], 5)
        self.assertEqual(ecdf[-1]["cumulative_fraction"], "1")
        self.assertEqual(ecdf[-1]["cumulative_decimal"], "1.000000000000000000")

    def test_duplicate_event_id_hard_fails(self):
        bad = list(self.rows)
        bad[4] = dict(bad[4])
        bad[4]["event_id"] = bad[0]["event_id"]
        with self.assertRaisesRegex(ValueError, "event_id uniqueness"):
            runner.aggregate_rows(bad, 5)

    def test_missing_close_displacement_hard_fails(self):
        bad = list(self.rows)
        bad[0] = dict(bad[0])
        bad[0].pop("close_displacement")
        with self.assertRaisesRegex(ValueError, "missing close_displacement"):
            runner.aggregate_rows(bad, 5)

    def test_expected_n_hard_fails(self):
        with self.assertRaisesRegex(ValueError, "N mismatch"):
            runner.aggregate_rows(self.rows, 472)

    def test_negative_zero_and_no_reintegration_retained(self):
        core = runner.aggregate_rows(self.rows, 5)
        self.assertEqual(core["N"], 5)
        self.assertEqual(core["NEGATIVE_COUNT"], 1)
        self.assertEqual(core["ZERO_COUNT"], 1)
        # Both same_week_reintegration=false rows remain in the population,
        # demonstrated by N=5 and the retained -2 and 0 support values.
        supports = [x["support_value"] for x in core["EMPIRICAL_CDF"]]
        self.assertIn("-2", supports)
        self.assertIn("0", supports)

    def test_type7_two_point_interpolation(self):
        vals = [Decimal("0"), Decimal("10")]
        self.assertEqual(runner.q18(runner.type7(vals, Decimal("0.25"))), "2.500000000000000000")
        self.assertEqual(runner.q18(runner.type7(vals, Decimal("0.50"))), "5.000000000000000000")
        self.assertEqual(runner.q18(runner.type7(vals, Decimal("0.75"))), "7.500000000000000000")

    def test_half_even_canonicalization(self):
        self.assertEqual(runner.q18(Decimal("1.0000000000000000005")), "1.000000000000000000")
        self.assertEqual(runner.q18(Decimal("1.0000000000000000015")), "1.000000000000000002")


if __name__ == "__main__":
    unittest.main()

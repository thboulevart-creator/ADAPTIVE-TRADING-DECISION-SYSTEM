import importlib.util
import math
import unittest
from decimal import Decimal
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "tools" / "bepd_08b_absolute_weekly_close_distance.py"
SPEC = importlib.util.spec_from_file_location("bepd08b_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(runner)


def row(i, value, reintegration=True, side="HIGH"):
    return {
        "event_id": f"event-{i}",
        "target_week_id": "2026-01-05",
        "sweep_cluster_id": "cluster-a",
        "side": side,
        "same_week_reintegration": reintegration,
        "close_displacement": Decimal(value),
    }


class TestBEPD08B(unittest.TestCase):
    def setUp(self):
        self.rows = [
            row(1, "-8", False, "HIGH"),
            row(2, "-2", True, "LOW"),
            row(3, "0", False, "HIGH"),
            row(4, "3", True, "LOW"),
            row(5, "8", True, "HIGH"),
        ]

    def test_positive_to_absolute(self):
        self.assertEqual(runner.distances_from_rows([row(1,"3")],1), [Decimal("3")])

    def test_negative_to_same_positive_absolute(self):
        self.assertEqual(runner.distances_from_rows([row(1,"-3")],1), [Decimal("3")])

    def test_zero_to_zero(self):
        self.assertEqual(runner.distances_from_rows([row(1,"0")],1), [Decimal("0")])

    def test_no_negative_distance(self):
        vals=runner.distances_from_rows(self.rows,5)
        self.assertTrue(all(v>=0 for v in vals))

    def test_all_rows_retained(self):
        self.assertEqual(len(runner.distances_from_rows(self.rows,5)),5)

    def test_negative_rows_retained(self):
        self.assertEqual(runner.aggregate_rows(self.rows,5)["N"],5)
        self.assertIn("2", [x["support_value"] for x in runner.aggregate_rows(self.rows,5)["EMPIRICAL_CDF"]])

    def test_positive_rows_retained(self):
        self.assertIn("3", [x["support_value"] for x in runner.aggregate_rows(self.rows,5)["EMPIRICAL_CDF"]])

    def test_zero_rows_retained(self):
        self.assertEqual(runner.aggregate_rows(self.rows,5)["ZERO_COUNT"],1)

    def test_no_reintegration_rows_retained(self):
        self.assertEqual(runner.aggregate_rows(self.rows,5)["N"],5)

    def test_duplicate_event_id_fails(self):
        bad=list(self.rows); bad[4]=dict(bad[4]); bad[4]["event_id"]=bad[0]["event_id"]
        with self.assertRaisesRegex(ValueError,"event_id uniqueness"):
            runner.aggregate_rows(bad,5)

    def test_missing_close_displacement_fails(self):
        bad=list(self.rows); bad[0]=dict(bad[0]); bad[0].pop("close_displacement")
        with self.assertRaisesRegex(ValueError,"missing close_displacement"):
            runner.aggregate_rows(bad,5)

    def test_nonfinite_nan_fails(self):
        bad=[row(1,"NaN")]
        with self.assertRaisesRegex(ValueError,"non-finite"):
            runner.aggregate_rows(bad,1)

    def test_nonfinite_inf_fails(self):
        bad=[row(1,"Infinity")]
        with self.assertRaisesRegex(ValueError,"non-finite"):
            runner.aggregate_rows(bad,1)

    def test_exact_population_fails(self):
        with self.assertRaisesRegex(ValueError,"N mismatch"):
            runner.aggregate_rows(self.rows,472)

    def test_type7(self):
        vals=[Decimal("0"),Decimal("10")]
        self.assertEqual(runner.q18(runner.type7(vals,Decimal("0.25"))),"2.500000000000000000")
        self.assertEqual(runner.q18(runner.type7(vals,Decimal("0.50"))),"5.000000000000000000")
        self.assertEqual(runner.q18(runner.type7(vals,Decimal("0.75"))),"7.500000000000000000")

    def test_p50_equals_median(self):
        c=runner.aggregate_rows(self.rows,5)
        self.assertEqual(c["P50"],c["MEDIAN"])

    def test_exact_ecdf_terminal(self):
        e=runner.aggregate_rows(self.rows,5)["EMPIRICAL_CDF"]
        self.assertEqual(e[-1]["cumulative_count"],5)
        self.assertEqual(e[-1]["cumulative_fraction"],"1")
        self.assertEqual(e[-1]["cumulative_decimal"],"1.000000000000000000")

    def test_zero_count_semantics(self):
        c=runner.aggregate_rows(self.rows,5)
        self.assertEqual(c["ZERO_COUNT"],1)
        self.assertEqual(c["ZERO_FRACTION"],{"fraction":"1/5","decimal":"0.200000000000000000"})

    def test_half_even_serialization(self):
        self.assertEqual(runner.q18(Decimal("1.0000000000000000005")),"1.000000000000000000")
        self.assertEqual(runner.q18(Decimal("1.0000000000000000015")),"1.000000000000000002")

    def test_global_surface_exact_keys(self):
        c=runner.aggregate_rows(self.rows,5)
        expected={"N","MINIMUM","MAXIMUM","MEAN","MEDIAN","P01","P05","P10","P25","P50","P75","P90","P95","P99","ZERO_COUNT","ZERO_FRACTION","EMPIRICAL_CDF"}
        self.assertEqual(set(c),expected)

    def test_no_subgroup_policy(self):
        self.assertEqual(runner.CANONICAL_POLICY["subgroups"],[])

    def test_no_sign_conditional_policy(self):
        self.assertFalse(runner.CANONICAL_POLICY["sign_conditional"])

    def test_no_threshold_policy(self):
        self.assertFalse(runner.CANONICAL_POLICY["threshold_search"])

    def test_no_broker_conversion(self):
        self.assertEqual(runner.CANONICAL_POLICY["unit"],"USTECH_PRICE_UNITS_AS_PERSISTED")

    def test_no_tp_sl(self):
        self.assertFalse(runner.CANONICAL_POLICY["tp"])
        self.assertFalse(runner.CANONICAL_POLICY["sl"])

    def test_no_pnl(self):
        self.assertFalse(runner.CANONICAL_POLICY["pnl"])

    def test_no_prediction_edge_trading(self):
        self.assertFalse(runner.CANONICAL_POLICY["prediction"])
        self.assertFalse(runner.CANONICAL_POLICY["edge"])
        self.assertEqual(runner.CANONICAL_POLICY["trading_authority"],"NONE")

    def test_abs_surface_values(self):
        c=runner.aggregate_rows(self.rows,5)
        self.assertEqual(c["MINIMUM"],"0.000000000000000000")
        self.assertEqual(c["MAXIMUM"],"8.000000000000000000")
        self.assertEqual(c["MEDIAN"],"3.000000000000000000")

    def test_source_policy(self):
        self.assertEqual(runner.CANONICAL_POLICY["source_field"],"close_displacement")
        self.assertEqual(runner.CANONICAL_POLICY["transformation"],"abs(close_displacement)")
        self.assertFalse(runner.CANONICAL_POLICY["market_reconstruction"])


if __name__ == "__main__":
    unittest.main()

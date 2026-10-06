import importlib.util
import unittest
from pathlib import Path

RUNNER_PATH = Path(__file__).resolve().parents[1] / "tools" / "bepd_06b_conditional_time_to_reintegration.py"
SPEC = importlib.util.spec_from_file_location("bepd06b_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(runner)


def row(i, reintegrates, t0, t1):
    return {
        "event_id": f"event-{i}",
        "target_week_id": "2026-01-05",
        "sweep_cluster_id": "cluster-a",
        "same_week_reintegration": reintegrates,
        "take_h1_close_utc": t0,
        "reintegration_h1_close_utc": t1,
    }


class TestBEPD06B(unittest.TestCase):
    def setUp(self):
        self.rows = [
            row(1, True,  "2026-01-05T10:59:00+00:00", "2026-01-05T11:59:00+00:00"),
            row(2, True,  "2026-01-05T10:59:00+00:00", "2026-01-05T12:59:00+00:00"),
            row(3, True,  "2026-01-05T10:59:00+00:00", "2026-01-05T13:59:00+00:00"),
            row(4, True,  "2026-01-05T10:59:00+00:00", "2026-01-05T15:59:00+00:00"),
            row(5, True,  "2026-01-05T10:59:00+00:00", "2026-01-05T20:59:00+00:00"),
            row(6, False, "2026-01-05T10:59:00+00:00", None),
            row(7, False, "2026-01-05T10:59:00+00:00", None),
        ]

    def test_elapsed_utc_hours(self):
        self.assertEqual(str(runner.elapsed_hours("2026-01-05T10:59:00+00:00","2026-01-05T12:59:00+00:00")), "2")

    def test_conditional_surface(self):
        core = runner.aggregate_rows(self.rows, 7, 5, 2)
        self.assertEqual(core["BASE_N"], 7)
        self.assertEqual(core["REINTEGRATION_TRUE_N"], 5)
        self.assertEqual(core["NO_REINTEGRATION_WITHIN_TARGET_WEEK_N"], 2)
        self.assertEqual(core["N_TIMING"], 5)
        self.assertEqual(core["MINIMUM_ELAPSED_UTC_HOURS"], "1.000000000000000000")
        self.assertEqual(core["MAXIMUM_ELAPSED_UTC_HOURS"], "10.000000000000000000")
        self.assertEqual(core["MEAN"], "4.200000000000000000")
        self.assertEqual(core["MEDIAN"], "3.000000000000000000")
        self.assertEqual(core["P50"], core["MEDIAN"])

    def test_type7_quantiles(self):
        core = runner.aggregate_rows(self.rows, 7, 5, 2)
        self.assertEqual(core["P25"], "2.000000000000000000")
        self.assertEqual(core["P75"], "5.000000000000000000")
        self.assertEqual(core["P90"], "8.000000000000000000")

    def test_ecdf_terminal(self):
        core = runner.aggregate_rows(self.rows, 7, 5, 2)
        last = core["EMPIRICAL_CDF"][-1]
        self.assertEqual(last["cumulative_count"], 5)
        self.assertEqual(last["cumulative_fraction"], "1")
        self.assertEqual(last["cumulative_decimal"], "1.000000000000000000")

    def test_false_rows_receive_no_duration(self):
        core = runner.aggregate_rows(self.rows, 7, 5, 2)
        self.assertEqual(core["N_TIMING"], 5)
        self.assertEqual(len(core["EMPIRICAL_CDF"]), 5)

    def test_t1_equal_t0_fails(self):
        bad=[row(1,True,"2026-01-05T10:59:00+00:00","2026-01-05T10:59:00+00:00")]
        with self.assertRaisesRegex(ValueError,"strictly greater"):
            runner.aggregate_rows(bad,1,1,0)

    def test_t1_before_t0_fails(self):
        bad=[row(1,True,"2026-01-05T10:59:00+00:00","2026-01-05T09:59:00+00:00")]
        with self.assertRaisesRegex(ValueError,"strictly greater"):
            runner.aggregate_rows(bad,1,1,0)

    def test_null_t1_for_true_fails(self):
        bad=[row(1,True,"2026-01-05T10:59:00+00:00",None)]
        with self.assertRaisesRegex(ValueError,"T1 null"):
            runner.aggregate_rows(bad,1,1,0)

    def test_non_null_t1_for_false_fails(self):
        bad=[row(1,False,"2026-01-05T10:59:00+00:00","2026-01-05T11:59:00+00:00")]
        with self.assertRaisesRegex(ValueError,"non-null T1"):
            runner.aggregate_rows(bad,1,0,1)

    def test_non_utc_offset_fails(self):
        with self.assertRaisesRegex(ValueError,"offset must be UTC"):
            runner.elapsed_hours("2026-01-05T10:59:00+01:00","2026-01-05T12:59:00+01:00")

    def test_duplicate_event_id_fails(self):
        bad=list(self.rows)
        bad[1]=dict(bad[1]); bad[1]["event_id"]=bad[0]["event_id"]
        with self.assertRaisesRegex(ValueError,"event_id uniqueness"):
            runner.aggregate_rows(bad,7,5,2)

    def test_count_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError,"reintegration true N mismatch"):
            runner.aggregate_rows(self.rows,7,4,3)


if __name__=="__main__":
    unittest.main()
